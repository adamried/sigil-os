#!/bin/bash
# gh-sync.sh — Shared-context sync helper using the `gh` CLI.
#
# Replaces the previous GitHub MCP integration with a local CLI helper
# (S4-001 FR-B06). All shared-context skills (shared-context-sync,
# connect-wizard, profile-generator) route remote file operations through
# this script — they never call `gh` or `git` directly.
#
# Requirements:
#   - `gh` CLI installed and authenticated (`gh auth login`).
#   - `jq` for JSON parsing/output formatting.
#
# Subcommands:
#   read <owner/repo> <path> [<branch>]
#     Print the file's contents to stdout. Exit 0 on success, 1 if not found,
#     2 on auth/network failure.
#
#   list <owner/repo> <path> [<branch>]
#     Print a JSON array of entries at the directory path, each
#     `{"name", "type", "path", "sha"}`. Exit 0 on success, 1 if not found.
#
#   write <owner/repo> <path> <local-file> <commit-message> [<branch>]
#     SHA-safe create-or-update of <path> from <local-file>. Reads the
#     current file SHA if it exists and includes it in the request so
#     concurrent writes are detected. Prints the response JSON. Exit 0 on
#     success, 2 on auth/network failure, 3 on SHA conflict.
#
#   push-batch <owner/repo> <branch> <commit-message> <manifest-json>
#     Push multiple files in a single commit. <manifest-json> is a path to
#     a JSON file containing `[{"path": "...", "local_file": "..."}]`.
#     Uses the Git Data API (`gh api`) to construct a tree + commit + ref
#     update so the changes land as one commit. Prints the new commit SHA.
#
# Exit codes (all subcommands):
#   0 — success
#   1 — usage error (bad/missing args)
#   2 — gh/jq missing or auth failure
#   3 — remote operation failed (SHA conflict, not found, etc.)
#
# Offline behavior:
#   When `gh` is missing OR auth is missing, this script exits with code 2
#   and prints a structured JSON error to stderr. The caller (skill) is
#   responsible for queueing the operation locally per its offline-queue
#   protocol — this script never falls back to `git` CLI.

set -e

# ---------- Utilities ----------

err() {
    echo "{\"error\": \"$1\", \"exit_code\": $2}" >&2
    exit "$2"
}

require_tools() {
    command -v gh >/dev/null 2>&1 || err "gh CLI not installed — run 'brew install gh' or equivalent" 2
    command -v jq >/dev/null 2>&1 || err "jq not installed — run 'brew install jq' or equivalent" 2
    gh auth status >/dev/null 2>&1 || err "gh not authenticated — run 'gh auth login'" 2
}

parse_repo() {
    # Validate "owner/repo" form
    case "$1" in
        */*) echo "$1" ;;
        *)   err "repo must be in <owner/repo> form (got: $1)" 1 ;;
    esac
}

default_branch() {
    # Discover the default branch when caller did not provide one
    gh api "repos/$1" --jq '.default_branch' 2>/dev/null || echo "main"
}

# ---------- Subcommand: read ----------

sub_read() {
    [ $# -ge 2 ] || err "Usage: gh-sync.sh read <owner/repo> <path> [<branch>]" 1
    local repo path branch
    repo=$(parse_repo "$1")
    path="$2"
    branch="${3:-$(default_branch "$repo")}"
    require_tools

    local response
    if response=$(gh api "repos/$repo/contents/$path?ref=$branch" 2>/dev/null); then
        # Decode base64 content
        echo "$response" | jq -r '.content' | base64 --decode 2>/dev/null \
            || err "failed to decode file content" 3
    else
        err "file not found: $repo/$path@$branch" 3
    fi
}

# ---------- Subcommand: list ----------

sub_list() {
    [ $# -ge 2 ] || err "Usage: gh-sync.sh list <owner/repo> <path> [<branch>]" 1
    local repo path branch
    repo=$(parse_repo "$1")
    path="$2"
    branch="${3:-$(default_branch "$repo")}"
    require_tools

    local response
    if response=$(gh api "repos/$repo/contents/$path?ref=$branch" 2>/dev/null); then
        # If it's a directory, response is an array. If it's a file, it's an object — wrap.
        if echo "$response" | jq -e 'type == "array"' >/dev/null; then
            echo "$response" | jq '[.[] | {name, type, path, sha}]'
        else
            echo "$response" | jq '[. | {name, type, path, sha}]'
        fi
    else
        err "path not found: $repo/$path@$branch" 3
    fi
}

# ---------- Subcommand: write ----------

sub_write() {
    [ $# -ge 4 ] || err "Usage: gh-sync.sh write <owner/repo> <path> <local-file> <commit-message> [<branch>]" 1
    local repo path local_file commit_msg branch existing_sha content_b64
    repo=$(parse_repo "$1")
    path="$2"
    local_file="$3"
    commit_msg="$4"
    branch="${5:-$(default_branch "$repo")}"
    require_tools

    [ -f "$local_file" ] || err "local file not found: $local_file" 1

    # Base64-encode without line wrapping
    if base64 --help 2>&1 | grep -q -- "-w "; then
        content_b64=$(base64 -w 0 "$local_file")
    else
        content_b64=$(base64 < "$local_file" | tr -d '\n')
    fi

    # Fetch existing SHA if file exists (for safe update)
    existing_sha=$(gh api "repos/$repo/contents/$path?ref=$branch" --jq '.sha' 2>/dev/null || echo "")

    local payload
    if [ -n "$existing_sha" ]; then
        payload=$(jq -n \
            --arg msg "$commit_msg" \
            --arg content "$content_b64" \
            --arg sha "$existing_sha" \
            --arg branch "$branch" \
            '{message: $msg, content: $content, sha: $sha, branch: $branch}')
    else
        payload=$(jq -n \
            --arg msg "$commit_msg" \
            --arg content "$content_b64" \
            --arg branch "$branch" \
            '{message: $msg, content: $content, branch: $branch}')
    fi

    # PUT to contents API
    if response=$(echo "$payload" | gh api --method PUT "repos/$repo/contents/$path" --input - 2>&1); then
        echo "$response"
    else
        # Check for SHA conflict (HTTP 409 or 422 with "does not match")
        if echo "$response" | grep -qiE "does not match|conflict"; then
            err "SHA conflict — remote file changed; refetch and retry" 3
        else
            err "write failed: $response" 3
        fi
    fi
}

# ---------- Subcommand: push-batch ----------

sub_push_batch() {
    [ $# -ge 4 ] || err "Usage: gh-sync.sh push-batch <owner/repo> <branch> <commit-message> <manifest-json>" 1
    local repo branch commit_msg manifest
    repo=$(parse_repo "$1")
    branch="$2"
    commit_msg="$3"
    manifest="$4"
    require_tools

    [ -f "$manifest" ] || err "manifest file not found: $manifest" 1

    # Validate manifest is an array of {path, local_file}
    if ! jq -e 'type == "array" and all(.path != null and .local_file != null)' "$manifest" >/dev/null 2>&1; then
        err "manifest must be a JSON array of {path, local_file} objects" 1
    fi

    # Get current branch HEAD commit SHA
    local base_sha base_tree_sha
    base_sha=$(gh api "repos/$repo/git/ref/heads/$branch" --jq '.object.sha' 2>/dev/null) \
        || err "branch not found: $branch" 3
    base_tree_sha=$(gh api "repos/$repo/git/commits/$base_sha" --jq '.tree.sha' 2>/dev/null) \
        || err "failed to fetch base tree" 3

    # Build tree entries by creating a blob for each file
    local tree_entries="[]"
    local count
    count=$(jq 'length' "$manifest")
    local i=0
    while [ "$i" -lt "$count" ]; do
        local entry_path entry_local blob_sha content_b64
        entry_path=$(jq -r ".[$i].path" "$manifest")
        entry_local=$(jq -r ".[$i].local_file" "$manifest")
        [ -f "$entry_local" ] || err "manifest entry $i: local file not found: $entry_local" 1

        # Base64-encode without line wrapping
        if base64 --help 2>&1 | grep -q -- "-w "; then
            content_b64=$(base64 -w 0 "$entry_local")
        else
            content_b64=$(base64 < "$entry_local" | tr -d '\n')
        fi

        # Create blob
        blob_sha=$(jq -n --arg c "$content_b64" '{content: $c, encoding: "base64"}' \
            | gh api --method POST "repos/$repo/git/blobs" --input - --jq '.sha' 2>/dev/null) \
            || err "blob create failed for $entry_path" 3

        tree_entries=$(echo "$tree_entries" | jq \
            --arg p "$entry_path" \
            --arg s "$blob_sha" \
            '. + [{path: $p, mode: "100644", type: "blob", sha: $s}]')
        i=$((i + 1))
    done

    # Create tree
    local new_tree_sha
    new_tree_sha=$(jq -n --arg base "$base_tree_sha" --argjson entries "$tree_entries" \
        '{base_tree: $base, tree: $entries}' \
        | gh api --method POST "repos/$repo/git/trees" --input - --jq '.sha' 2>/dev/null) \
        || err "tree create failed" 3

    # Create commit
    local new_commit_sha
    new_commit_sha=$(jq -n \
        --arg msg "$commit_msg" \
        --arg tree "$new_tree_sha" \
        --arg parent "$base_sha" \
        '{message: $msg, tree: $tree, parents: [$parent]}' \
        | gh api --method POST "repos/$repo/git/commits" --input - --jq '.sha' 2>/dev/null) \
        || err "commit create failed" 3

    # Update ref
    jq -n --arg sha "$new_commit_sha" '{sha: $sha, force: false}' \
        | gh api --method PATCH "repos/$repo/git/refs/heads/$branch" --input - >/dev/null 2>&1 \
        || err "ref update failed (may be force-push protection or stale base)" 3

    echo "{\"commit_sha\": \"$new_commit_sha\", \"branch\": \"$branch\", \"files\": $count}"
}

# ---------- Main ----------

[ $# -ge 1 ] || err "Usage: gh-sync.sh {read|list|write|push-batch} [args...]" 1

SUBCOMMAND="$1"
shift
case "$SUBCOMMAND" in
    read)       sub_read "$@" ;;
    list)       sub_list "$@" ;;
    write)      sub_write "$@" ;;
    push-batch) sub_push_batch "$@" ;;
    *) err "unknown subcommand: $SUBCOMMAND" 1 ;;
esac
