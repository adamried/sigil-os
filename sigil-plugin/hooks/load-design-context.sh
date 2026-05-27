#!/bin/bash
# load-design-context.sh — SessionStart hook for design context (S4-002 FR-I03)
#
# Fast-path: if design context is disabled in config, exit in < 100ms with a
# minimal "disabled" payload (NFR-002). Otherwise, surface the design.md
# path and the design-skills manifest summary so agents can decide whether
# to load them.
#
# This hook does NOT load design.md content — that's per-UI-task work done
# by the uiux-designer agent and the developer/frontend-developer agents
# (S4-002 FR-G01, FR-G02). This hook only surfaces availability.

set -e

PROJECT_ROOT="${CLAUDE_PROJECT_ROOT:-.}"
CONFIG="$PROJECT_ROOT/.sigil/config.yaml"
DESIGN_MD="$PROJECT_ROOT/.sigil/design.md"
MANIFEST="$PROJECT_ROOT/.sigil/design-skills/.manifest.json"

# Fast-path: no .sigil/ → nothing to do
if [ ! -d "$PROJECT_ROOT/.sigil" ]; then
    echo '{"design_context": "not_set_up"}'
    exit 0
fi

# Fast-path: config says disabled → exit immediately (NFR-002: <100ms)
if [ -f "$CONFIG" ]; then
    if grep -qE '^[[:space:]]*enabled:[[:space:]]*false' "$CONFIG" 2>/dev/null; then
        # Only trust this match if we're inside the `design:` block.
        # Lightweight check: look for "design:" followed by enabled: false
        # within 10 lines. If found, fast-path.
        if awk '/^design:/{f=1; next} f && /^[a-z]/{f=0} f && /enabled:[[:space:]]*false/{print "DISABLED"; exit}' "$CONFIG" 2>/dev/null | grep -q DISABLED; then
            echo '{"design_context": "disabled", "fast_path": true}'
            exit 0
        fi
    fi
fi

# Enabled (or unspecified — treat as enabled-by-default for awareness only)
DESIGN_MD_STATUS="missing"
[ -f "$DESIGN_MD" ] && DESIGN_MD_STATUS="present"

SKILLS_COUNT=0
if [ -f "$MANIFEST" ]; then
    # Count skill entries — naive jq if available, else grep
    if command -v jq >/dev/null 2>&1; then
        SKILLS_COUNT=$(jq '.skills | length' "$MANIFEST" 2>/dev/null || echo 0)
    else
        SKILLS_COUNT=$(grep -c '"slug"' "$MANIFEST" 2>/dev/null || echo 0)
    fi
fi

cat <<EOF
{
  "design_context": "enabled",
  "design_md": {
    "path": "$DESIGN_MD",
    "status": "$DESIGN_MD_STATUS"
  },
  "design_skills": {
    "manifest_path": "$MANIFEST",
    "skills_count": $SKILLS_COUNT
  },
  "guidance": "uiux-designer and developer agents load design.md in full on UI tasks (FR-G01, FR-G02). This hook only surfaces availability."
}
EOF
