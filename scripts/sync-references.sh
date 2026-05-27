#!/bin/bash
# sync-references.sh — Sync shared-references/ to plugin reference directories.
#
# shared-references/ is the source of truth for files shared across plugins
# (Validated Spec template, communication style, business case, design ticket,
# story decomposition). This script copies them into each plugin's references/
# directory at build time. Plugins never read from shared-references/ at
# runtime — they read from their own copies.
#
# Usage:
#   sync-references.sh              Sync all references to all plugins
#   sync-references.sh --check      Exit non-zero if any plugin copy is out of sync (CI use)
#   sync-references.sh --list       Show the distribution table and exit
#
# Exit codes:
#   0 — success (or --check passed)
#   1 — usage error or missing source file
#   2 — one or more plugin copies out of sync (--check mode)

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="$REPO_ROOT/shared-references"

# Distribution table: which references go to which plugin reference directories.
# Format: "<source-file>|<dest-plugin>/<dest-subpath>"
#
# Edit this list to add/remove distributions. Plugin paths are relative to REPO_ROOT.
DISTRIBUTIONS=(
    "validated-spec-template.md|pm-copilot/references/validated-spec-template.md"
    "validated-spec-template.md|po-buddy/references/validated-spec-template.md"
    "communication-style.md|pm-copilot/references/communication-style.md"
    "communication-style.md|po-buddy/references/communication-style.md"
    "business-case-template.md|pm-copilot/references/business-case-template.md"
    "design-ticket-template.md|pm-copilot/references/design-ticket-template.md"
    "design-ticket-template.md|po-buddy/references/design-ticket-template.md"
    "story-decomposition-template.md|po-buddy/references/story-decomposition-template.md"
)

# ---------- Helpers ----------

usage() {
    sed -n '1,/^set -e$/p' "$0" | grep -E '^#' | sed 's/^# \{0,1\}//'
    exit 1
}

list_distributions() {
    echo "Distribution table:"
    echo ""
    printf "  %-40s → %s\n" "Source (shared-references/)" "Destination"
    printf "  %-40s   %s\n" "----------------------------------------" "------------------------------------------------------------"
    for entry in "${DISTRIBUTIONS[@]}"; do
        src="${entry%%|*}"
        dst="${entry##*|}"
        printf "  %-40s → %s\n" "$src" "$dst"
    done
    exit 0
}

# ---------- Args ----------

MODE="sync"
case "${1:-}" in
    --check) MODE="check" ;;
    --list)  list_distributions ;;
    -h|--help) usage ;;
    "") ;;
    *) echo "Unknown argument: $1" >&2; usage ;;
esac

# ---------- Validate source files exist ----------

missing_sources=0
for entry in "${DISTRIBUTIONS[@]}"; do
    src="${entry%%|*}"
    if [ ! -f "$SOURCE_DIR/$src" ]; then
        echo "ERROR: source file missing: shared-references/$src" >&2
        missing_sources=$((missing_sources + 1))
    fi
done
if [ "$missing_sources" -gt 0 ]; then
    exit 1
fi

# ---------- Sync or check ----------

out_of_sync=0
synced=0
skipped=0

for entry in "${DISTRIBUTIONS[@]}"; do
    src_rel="${entry%%|*}"
    dst_rel="${entry##*|}"
    src="$SOURCE_DIR/$src_rel"
    dst="$REPO_ROOT/$dst_rel"
    dst_dir="$(dirname "$dst")"

    # Skip distributions where the plugin directory doesn't exist yet (e.g. pm-copilot
    # not built yet). This lets the script work during incremental rollout.
    plugin_root="$(echo "$dst_rel" | cut -d/ -f1)"
    if [ ! -d "$REPO_ROOT/$plugin_root" ]; then
        if [ "$MODE" = "check" ]; then
            # In check mode, missing plugin dir is fine — it means nothing to sync.
            :
        else
            echo "  skip: $plugin_root/ does not exist yet — leaving $dst_rel"
        fi
        skipped=$((skipped + 1))
        continue
    fi

    if [ "$MODE" = "check" ]; then
        if [ ! -f "$dst" ]; then
            echo "  out of sync: $dst_rel does not exist (run sync-references.sh)" >&2
            out_of_sync=$((out_of_sync + 1))
        elif ! cmp -s "$src" "$dst"; then
            echo "  out of sync: $dst_rel differs from shared-references/$src_rel" >&2
            out_of_sync=$((out_of_sync + 1))
        fi
    else
        # Sync
        mkdir -p "$dst_dir"
        if [ -f "$dst" ] && cmp -s "$src" "$dst"; then
            : # already in sync
        else
            cp "$src" "$dst"
            echo "  synced: $dst_rel"
            synced=$((synced + 1))
        fi
    fi
done

# ---------- Summary ----------

if [ "$MODE" = "check" ]; then
    if [ "$out_of_sync" -gt 0 ]; then
        echo "" >&2
        echo "$out_of_sync file(s) out of sync. Run 'scripts/sync-references.sh' to fix." >&2
        exit 2
    fi
    echo "All plugin reference copies in sync."
    exit 0
else
    echo ""
    if [ "$synced" -eq 0 ]; then
        echo "Already in sync. ($skipped distribution(s) skipped — plugin not built yet)"
    else
        echo "Synced $synced file(s). ($skipped distribution(s) skipped — plugin not built yet)"
    fi
fi
