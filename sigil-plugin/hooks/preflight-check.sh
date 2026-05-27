#!/bin/bash
# preflight-check.sh
# SessionStart hook: Verify Sigil OS enforcement files and create/update SIGIL.md
#
# This hook replaces the manual preflight-check skill invocation. It runs
# automatically at session start and outputs JSON for Claude to act on.

set -e

PROJECT_ROOT="${CLAUDE_PROJECT_ROOT:-.}"
SIGIL_MD="$PROJECT_ROOT/SIGIL.md"
CLAUDE_MD="$PROJECT_ROOT/CLAUDE.md"
ENFORCEMENT_VERSION="2.5.0"

# Output JSON response
output_json() {
    echo "$1"
    exit 0
}

# Check for dev repo (skip enforcement in Sigil OS development repository)
if [ -f "$CLAUDE_MD" ]; then
    if grep -q "Sigil OS Development Environment" "$CLAUDE_MD" 2>/dev/null; then
        output_json '{"status": "skip", "reason": "dev_repo", "message": "Skipping enforcement in Sigil OS dev repository"}'
    fi
fi

# Initialize status flags
NEEDS_SIGIL_MD="false"
SIGIL_MD_ACTION="none"
NEEDS_POINTER="false"
HAS_LEGACY="false"

# Check SIGIL.md existence and version
if [ -f "$SIGIL_MD" ]; then
    # Extract version from first line: <!-- SIGIL-OS v1.0.0 -->
    CURRENT_VERSION=$(head -1 "$SIGIL_MD" | grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+' | sed 's/v//' || echo "")
    if [ -z "$CURRENT_VERSION" ]; then
        NEEDS_SIGIL_MD="true"
        SIGIL_MD_ACTION="update"
    elif [ "$CURRENT_VERSION" != "$ENFORCEMENT_VERSION" ]; then
        NEEDS_SIGIL_MD="true"
        SIGIL_MD_ACTION="update"
    fi
else
    NEEDS_SIGIL_MD="true"
    SIGIL_MD_ACTION="create"
fi

# Check CLAUDE.md for pointer
POINTER_LINE="<!-- Project: Check for ./SIGIL.md and follow all rules if present -->"

if [ -f "$CLAUDE_MD" ]; then
    if ! grep -qF "$POINTER_LINE" "$CLAUDE_MD" 2>/dev/null; then
        NEEDS_POINTER="true"
    fi
    # Check for legacy enforcement block
    if grep -q "SIGIL-OS-ENFORCEMENT-START" "$CLAUDE_MD" 2>/dev/null; then
        HAS_LEGACY="true"
    fi
else
    NEEDS_POINTER="true"
fi

# Output status for Claude to process
cat << EOF
{
  "status": "check",
  "enforcement_version": "$ENFORCEMENT_VERSION",
  "needs_sigil_md": $NEEDS_SIGIL_MD,
  "sigil_md_action": "$SIGIL_MD_ACTION",
  "needs_pointer": $NEEDS_POINTER,
  "has_legacy_block": $HAS_LEGACY,
  "instructions": {
    "if_create": "Create SIGIL.md with enforcement rules v$ENFORCEMENT_VERSION. Use the content from the preflight-check skill.",
    "if_update": "Update SIGIL.md to enforcement rules v$ENFORCEMENT_VERSION. Preserve any custom sections below the enforcement rules.",
    "if_pointer": "Add the pointer line as the first line of CLAUDE.md (after any frontmatter): $POINTER_LINE",
    "if_legacy": "Remove the legacy SIGIL-OS-ENFORCEMENT block from CLAUDE.md before adding the pointer."
  }
}
EOF
