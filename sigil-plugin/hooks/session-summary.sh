#!/bin/bash
# session-summary.sh
# Stop hook: Generate session summary and remind about context updates
#
# Runs when Claude finishes responding. Provides a summary of the current
# workflow state to help maintain context across sessions.

set -e

PROJECT_ROOT="${CLAUDE_PROJECT_ROOT:-.}"
CONTEXT_FILE="$PROJECT_ROOT/.sigil/project-context.md"

# If no context file, minimal output
if [ ! -f "$CONTEXT_FILE" ]; then
    cat << EOF
{
  "has_context": false,
  "message": "No active Sigil workflow context."
}
EOF
    exit 0
fi

# Extract key workflow fields from project-context.md
# Template format: - **Key:** value  (colon is inside the bold markers)
extract_field() {
    local key="$1"
    sed -n "s/.*\*\*${key}:\*\* *//p" "$CONTEXT_FILE" 2>/dev/null | head -1
}

FEATURE=$(extract_field 'Feature')
PHASE=$(extract_field 'Current Phase')
SPEC_PATH=$(extract_field 'Spec Path')
TASKS_COMPLETED=$(extract_field 'Completed')
LAST_UPDATED=$(extract_field 'Last Updated')

# Remove markdown formatting
FEATURE=$(echo "$FEATURE" | sed 's/\*//g')
PHASE=$(echo "$PHASE" | sed 's/\*//g')

# Build summary
cat << EOF
{
  "has_context": true,
  "workflow_state": {
    "feature": "${FEATURE:-none}",
    "phase": "${PHASE:-none}",
    "spec_path": "${SPEC_PATH:-none}",
    "tasks_completed": "${TASKS_COMPLETED:-none}",
    "last_updated": "${LAST_UPDATED:-unknown}"
  },
  "reminder": "If you made workflow progress this session, update .sigil/project-context.md with the new state.",
  "next_session_hint": "Run /sigil:draw continue to resume from the current phase."
}
EOF
