---
name: shared-context-sync
description: Infrastructure skill for shared context sync. Called by learning-capture, learning-reader, draw, connect-wizard, profile-generator, and constitution-writer — not invoked directly by users. Handles sentinel detection, repo identity, push/pull sync, cache management, and offline queue via the gh CLI (S4-001 FR-B06).
version: 2.0.0
category: shared-context
chainable: false
invokes: []
invoked_by: [learning-capture, learning-reader, draw, connect-wizard, profile-generator, constitution-writer]
tools: Read, Write, Edit, Bash
model: haiku
---

# Skill: Shared Context Sync

## Critical Constraint (S4-001 FR-B06)

**NEVER use `git clone`, `git commit`, `git push`, `git pull`, `git fetch`, or any git write/remote operations directly.** The only permitted git commands are read-only local queries: `git rev-parse`, `git remote get-url`, and `git config user.email`. ALL remote repository operations — reading files, creating files, updating files, scaffolding — MUST go through the `gh-sync.sh` helper script:

```
${CLAUDE_PLUGIN_ROOT}/scripts/gh-sync.sh <subcommand> <args...>
```

**Subcommands:**

| Subcommand | Purpose | Replaces |
|------------|---------|----------|
| `read <repo> <path> [<branch>]` | Read a single file's contents | `mcp__github__get_file_contents` (file mode) |
| `list <repo> <path> [<branch>]` | List directory entries (JSON array of `{name, type, path, sha}`) | `mcp__github__get_file_contents` (directory mode) |
| `write <repo> <path> <local-file> <message> [<branch>]` | SHA-safe create-or-update of a single file | `mcp__github__create_or_update_file` |
| `push-batch <repo> <branch> <message> <manifest-json>` | Multi-file commit via the Git Data API | `mcp__github__push_files` |

**Prerequisites:** `gh` CLI must be installed and authenticated (`gh auth login`). `jq` must be installed for JSON output handling. If either is missing or unauthenticated, the helper exits with code 2 and a structured JSON error; queue the operation locally for later retry per the offline-queue protocol. **Never fall back to direct `git` CLI.**

**Migration note:** This skill previously used GitHub MCP tools (`mcp__github__*`). Those references have been removed from this skill's frontmatter. The `.mcp.json` GitHub MCP server registration is retained temporarily for backward compatibility with any unmigrated paths; it will be removed in a follow-up once verification completes.

## Purpose

Provide shared context infrastructure for all Sigil skills. This skill handles:
- Sentinel file detection and validation
- Repository identity detection from git remote
- `gh` CLI availability checking
- Local cache management
- Offline queue management
- Push (on learning capture) and pull (on prime) sync operations
- Profile, standards, scaffolding, discrepancy detection, and integration discovery protocols

Other skills call into this skill's procedures rather than implementing sync logic themselves.

> **Reference:** Detailed protocol specifications for cache management, offline queue, profiles, standards, scaffolding, discrepancy detection, and integration discovery are in `references/sync-protocol.md`.

## Sentinel Detection

### Check if Shared Context is Active

Read `~/.sigil/registry.json`. If the file exists and is valid JSON, shared context may be active for the current project.

**Lookup procedure:**

1. Read `~/.sigil/registry.json`
2. If file missing or invalid JSON → return `{ active: false }`
3. Detect current project identity (see Repo Identity Detection below)
4. Look up current project in `projects` map
5. If found → return `{ active: true, shared_repo: projects[project].shared_repo }`
6. If not found → check `default_repo`
7. If `default_repo` is non-empty → return `{ active: true, shared_repo: default_repo }`
8. Otherwise → return `{ active: false }`

**Sentinel schema:**

```json
{
  "version": 1,
  "default_repo": "my-org/platform-context",
  "connected_at": "2026-02-09T14:30:00Z",
  "projects": {
    "my-org/web-app": {
      "shared_repo": "my-org/platform-context",
      "connected_at": "2026-02-09T14:30:00Z"
    }
  }
}
```

### Write Sentinel Entry

When `sigil connect` completes for a project:

1. Read existing `~/.sigil/registry.json` (or start with empty object if missing)
2. Set `version` to `1` if not present
3. Add/update entry in `projects` map keyed by current project identity
4. If this is the first project, also set `default_repo`
5. Set top-level `connected_at` to current timestamp
6. Write atomically: write to `~/.sigil/registry.tmp.json`, then rename to `~/.sigil/registry.json`

---

## Repo Identity Detection

Determine the current project's `owner/repo` identity from git remote.

**Procedure:**

1. Run `git remote get-url origin`
2. Parse the result:
   - SSH format: `git@github.com:owner/repo.git` → `owner/repo`
   - HTTPS format: `https://github.com/owner/repo.git` → `owner/repo`
   - HTTPS without .git: `https://github.com/owner/repo` → `owner/repo`
3. Strip trailing `.git` if present
4. Return `owner/repo` string

**Error cases:**

| Condition | Behavior |
|-----------|----------|
| No git repo | Return error: "Shared context requires a git repository. Run `git init` first." |
| No remote configured | Return error: "Shared context needs a git remote. Add one with `git remote add origin <url>`." |
| Remote is not GitHub | Return error: "Shared context currently requires a GitHub remote." |
| Parse failure | Return error: "Could not determine project identity from git remote." |

---

## gh CLI Availability Detection

Check whether the `gh` CLI is installed and authenticated before any remote operation.

**Procedure:**

1. Run `command -v gh` — if not found, `gh` is not installed
2. Run `gh auth status` — if non-zero exit, `gh` is not authenticated
3. Run `command -v jq` — if not found, `jq` is not installed (the helper script needs it)

If any check fails, treat the same as the offline case: queue the operation per the offline-queue protocol and surface guidance to the user.

**When the helper or its prerequisites are unavailable:**

Return a structured result indicating the issue with plain-language guidance:

```
Shared context sync requires the `gh` CLI and `jq`. One or both are missing or not authenticated.

To set them up:

  brew install gh jq        # or your platform's package manager
  gh auth login             # follow the OAuth prompts

Once installed and authenticated, retry your last operation. In the meantime,
shared-context writes have been queued locally and will sync on next attempt.
```

The `gh-sync.sh` helper itself runs the equivalent checks (`require_tools()`) and exits with code 2 if any prerequisite is missing. Skills calling the helper should always check the exit code and route failures into the offline queue rather than retrying immediately.

---

## Push Protocol

Called by `learning-capture` after writing a learning locally.

**Inputs:**
- `category`: "patterns" | "gotchas" | "decisions"
- `content`: The formatted learning entry (shared format with metadata)
- `repo_name`: Current project's repo name (from identity detection)

**Procedure:**

1. Check sentinel → if not active, return silently
2. Determine shared repo from sentinel lookup (e.g., `adamried/platform-context`)
3. Split shared repo into `owner` and `repo` parts
4. Determine target file path: `learnings/{repo_name}/{category}.md`
5. Get contributor email via `git config user.email`
6. **Read existing file via `gh-sync.sh`:**
   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/gh-sync.sh read "$owner/$repo" "$target_file_path"
   ```
   - Exit code 0 → file exists; capture stdout as content. SHA is fetched implicitly by `write` (next step) so callers don't need to track it.
   - Exit code 3 → file doesn't exist; start with category header (e.g., `# Patterns — {repo_name}\n\n`).
   - Exit code 2 → gh/jq missing or auth failure; enqueue to offline queue, do not retry inline.
7. **Run duplicate detection** (see Duplicate Detection in `references/sync-protocol.md`)
   - If duplicate found: skip push, return silently
8. Append new entry to existing content; write the updated content to a temporary local file (e.g., `mktemp`).
9. **Write updated file via `gh-sync.sh`:**
   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/gh-sync.sh write "$owner/$repo" "$target_file_path" "$tmp_file" \
       "learning: add {category} entry for {repo_name}"
   ```
   - The helper fetches the current SHA inline and includes it in the PUT payload, so writes are SHA-safe without the caller managing SHAs.
   - Exit code 3 with "SHA conflict" → another writer landed first; the caller re-runs from step 6 (retry once). After one retry, surface to the user.
   - Exit code 2 → enqueue to offline queue.
10. On success: update local cache copy at `~/.sigil/cache/shared/learnings/{repo_name}/{category}.md`
11. On failure: enqueue to offline queue (see Queue Operations in `references/sync-protocol.md`)

**Shared learning entry format:**

```markdown
## [YYYY-MM-DD] Short title
- **Contributor:** {git config user.email}
- **Context:** When/why this applies
- **Solution:** The learning content
- **Related files:** path/to/file.ts (optional)
- **Tags:** tag1, tag2 (optional)
```

The contributor email is obtained from `git config user.email`.

**Graceful failure (FR-011):** If any `gh-sync.sh` call exits non-zero, log a warning ("Shared sync unavailable, learning saved locally") and enqueue to the offline queue. Never block the user's workflow on sync failure.

---

## Pull Protocol

Called by `prime` at session start.

**Procedure:**

1. Check sentinel → if not active, return silently
2. Determine shared repo from sentinel lookup (e.g., `adamried/platform-context`)
3. Split shared repo into `owner` and `repo` parts
4. Read `~/.sigil/cache/shared/last-sync.json` for previous content hashes
5. **List the learnings directory via `gh-sync.sh`:**
   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/gh-sync.sh list "$owner/$repo" "learnings/"
   ```
   Parse the JSON array. For each entry with `type == "dir"` (sub-repo), list its contents:
   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/gh-sync.sh list "$owner/$repo" "learnings/{sub_repo}/"
   ```
   For each file (patterns.md, gotchas.md, decisions.md), read it:
   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/gh-sync.sh read "$owner/$repo" "learnings/{sub_repo}/{file}"
   ```
6. For each file found:
   a. Compare the SHA from the `list` response with the cached SHA in `last-sync.json`
   b. If changed: capture the `read` stdout and update local cache at `~/.sigil/cache/shared/learnings/{sub_repo}/{file}`
   c. If unchanged: skip (cache is current)
7. **List the profiles directory via `gh-sync.sh`** (for S2-102):
   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/gh-sync.sh list "$owner/$repo" "profiles/"
   ```
   Read each profile file and cache to `~/.sigil/cache/shared/profiles/`
8. Update `~/.sigil/cache/shared/last-sync.json` with new SHAs and timestamp
9. **Compute "what's new" diff:**
   - Compare new content with previous cache content
   - Count new `## [date]` heading entries that didn't exist in previous cache
   - Build list of new entry titles for display
10. Drain offline queue (see Queue Operations in `references/sync-protocol.md`)
11. Return:
    - List of new learning entries (for "what's new" display)
    - Count of queued items synced
    - Any errors encountered

**On MCP failure during pull (FR-011):**

1. Log warning: "Shared context unavailable, using cached data."
2. Return cached data from `~/.sigil/cache/shared/`
3. Do NOT delete cache or sentinel
4. Still attempt queue drain (will also fail, items stay queued)
5. Continue session normally — MCP failure must never block session start

---

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Sentinel missing | Return `{ active: false }`. No error, no message. |
| Sentinel invalid JSON | Return `{ active: false }`. Log warning. |
| Git not available | Error: "Shared context requires a git repository. Run `git init` first." |
| No git remote | Error: "Shared context needs a git remote. Add one with `git remote add origin <url>`." |
| Remote is not GitHub | Error: "Shared context currently requires a GitHub remote." |
| MCP not available | Log warning on push/pull. Queue writes. Use cache for reads. |
| MCP read fails (network) | Use cached version. Log: "Shared context unavailable, using cached data." |
| MCP read fails (404) | File doesn't exist yet — start with empty content (for push) or skip (for pull). |
| MCP write fails (permissions) | "Could not write to shared repo. Ask your admin for write access to `{owner}/{repo}`." Queue locally. |
| MCP write fails (network) | Queue locally. Warn on next prime: "N learnings pending sync." |
| MCP write fails (SHA mismatch) | Re-read file, retry once. If still fails, queue locally. |
| Shared repo not accessible | "Could not reach `{owner}/{repo}`. Check that the repository exists and you have access." |
| Cache directory missing | Create it (first-time initialization). |
| Queue item exceeds 3 retries | Move to `failed/` directory. Log. |
| Registry exists but repo unreachable | Use cache. Warn user. Do not delete sentinel. |
| Profile file missing locally | Skip profile push/change detection. No error. |
| Profile push fails (MCP) | Queue locally. Warn: "Profile sync unavailable, saved locally." |
| Profile pull fails (MCP) | Use cached profiles. Log warning. |
| Profile hash cache missing | Create it (first-time initialization). |
| Standards directory empty | Return empty array. No error, no message. |
| Standards pull fails (MCP) | Use cached standards. Log: "Shared standards unavailable, using cached data." |
| Standards pull fails (404) | `shared-standards/` directory doesn't exist yet — return empty array. |
| Standards cache missing | Return empty array (no prior pull has occurred). |
| @inherit marker references missing file | Leave existing expanded content if any; insert `@inherit-pending` marker if no prior expansion. |
| @inherit expand fails (no constitution) | Return silently — nothing to expand. |
| Discrepancy detected | Display warning to user with resolution options. Do not auto-resolve. |
| Integrations directory missing (404) | Return empty array. No error, no message. |
| Integration pull fails (MCP) | Use cached integrations. Log: "Integration configs unavailable, using cached data." |
| Integration config invalid YAML | Skip that adapter, log warning. Continue with valid adapters. |

---

## Integration Points

| Caller | Operation | When |
|--------|-----------|------|
| `learning-capture` | Push | After writing a learning locally |
| `learning-reader` | Read cache | Before loading local learnings |
| `prime` (session start) | Pull + queue drain | At session start |
| `sigil` | Sentinel check | During state detection |
| `connect-wizard` | Write sentinel, scaffold repo | During `sigil connect` |
| `learn` | Queue status | When displaying learning summary |
| `profile-generator` | Profile Push | After writing/updating `.sigil/project-profile.yaml` |
| `prime` (session start) | Profile Pull + change detection | At session start (alongside learning pull) |
| `sigil` (session start) | Standards Pull + Expand + Discrepancy Detection | At session start, when shared context active and constitution has @inherit markers |
| `constitution-writer` | Standards Discover + Standards Pull | During setup, when shared_standards provided |
| `connect-wizard` | Standards Discover + Standards Expand | During connection, when standards found and constitution exists |
| `connect-wizard` | Integration Discovery | During connection Step 8, after standards integration |
| `sigil-setup` | Integration Discovery | During setup Step 3.5, after standards discovery |
| `prime` (session start) | Integration Pull | At session start, when shared context active |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.6.0 | 2026-03-05 | Refactor: extract detailed protocol specs (cache, offline queue, duplicate detection, profiles, standards pull/expand/discover, discrepancy detection, scaffolding, integration discovery/pull) into `references/sync-protocol.md` for progressive disclosure. No behavioral changes. |
| 1.5.0 | 2026-02-20 | S4-103: Integration Discovery and Pull protocols — fetches adapter configs from `integrations/` directory in shared repo. SHA-based caching, graceful MCP failure. Added `integrations/` to cache structure and `integrations_hashes` to last-sync.json. |
| 1.4.0 | 2026-02-20 | S4-101: Enforcement-level awareness — Standards Pull parses YAML frontmatter `enforcement` field (required/recommended/informational, default recommended). Standards Discover returns `enforcement` in schema. Discrepancy Detection uses three-tier severity: required → hard block, recommended → warn with options, informational → silent. Added missing-required-standard pre-check. |
| 1.3.0 | 2026-02-20 | Added Standards protocols — Standards Pull, Standards Expand, Standards Discover, Discrepancy Detection. Added `standards/` to cache structure. Updated `last-sync.json` schema with `standards_hashes`. New integration points for sigil, constitution-writer, connect-wizard. |
| 1.2.0 | 2026-02-09 | S2-102: Added Profile Protocol — profile push, pull, change detection, profile hash cache |
| 1.1.0 | 2026-02-09 | Added specific MCP tool references, scaffolding protocol, duplicate detection V1, expanded error paths, graceful fallback details |
| 1.0.0 | 2026-02-09 | Initial release — sentinel detection, repo identity, cache structure, queue management, push/pull protocols |
