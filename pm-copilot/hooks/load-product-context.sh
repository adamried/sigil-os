#!/bin/bash
# load-product-context.sh — PM Copilot SessionStart hook (FR-D06)
#
# Loads minimum essential product context at session start:
#   - communication-style.md (always-on tone and behavior)
#   - product-knowledge index (lightweight pointer to other references)
#
# Token budget: ≤ 2 files, ~2.5K tokens. Other references load on demand.
#
# Per the FR-D06 update for PM Copilot, this hook is intentionally minimal.
# PO Buddy ships with NO SessionStart hook at all — all references load
# on-demand there. PM gets these two because communication-style affects
# every interaction and product-knowledge index makes lookups fast.

set -e

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-.}"
REFS="$PLUGIN_ROOT/references"

# Output a JSON envelope the host can include in session context
cat << EOF
{
  "loaded_references": [
    {
      "name": "communication-style",
      "path": "$REFS/communication-style.md",
      "purpose": "Tone, challenge model, yielding policy, output modes — applied to every interaction"
    },
    {
      "name": "product-knowledge-index",
      "purpose": "Lightweight index of available references. Full content loaded on demand by individual skills."
    }
  ],
  "on_demand_references": [
    {"name": "personas", "path": "$REFS/personas.md", "loaded_by": ["persona-lookup"]},
    {"name": "team-scope", "path": "$REFS/team-scope.md", "loaded_by": ["scope-check"]},
    {"name": "validated-spec-template", "path": "$REFS/validated-spec-template.md", "loaded_by": ["specify", "validate"]},
    {"name": "business-case-template", "path": "$REFS/business-case-template.md", "loaded_by": ["business-case"]},
    {"name": "design-ticket-template", "path": "$REFS/design-ticket-template.md", "loaded_by": ["specify (when UI gap detected)"]}
  ],
  "budget_target_tokens": 2500,
  "philosophy": "PM Copilot loads only what affects every interaction. Other references load on demand to keep session start fast and cheap."
}
EOF
