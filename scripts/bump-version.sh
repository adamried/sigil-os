#!/bin/bash
# bump-version.sh — Bump version across all locations for a Sigil OS plugin.
#
# Updates a plugin's version in three locations atomically:
#   1. <plugin>/.claude-plugin/plugin.json  →  "version": "X.Y.Z"
#   2. .claude-plugin/marketplace.json      →  the matching plugin entry's "version"
#   3. README.md                            →  version badge (only for sigil-plugin)
#
# Usage:
#   bump-version.sh <plugin> <new-version>
#   bump-version.sh --show               Display current version of each plugin and exit
#   bump-version.sh --help               Show this usage
#
# <plugin> is:  sigil-plugin
# <new-version> is a semver string like 0.33.0 (no leading "v")
#
# Examples:
#   scripts/bump-version.sh sigil-plugin 0.33.0
#   scripts/bump-version.sh --show
#
# Requires: jq

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MARKETPLACE="$REPO_ROOT/.claude-plugin/marketplace.json"

usage() {
    sed -n '1,/^set -e$/p' "$0" | grep -E '^#' | sed 's/^# \{0,1\}//'
    exit 1
}

require_jq() {
    command -v jq >/dev/null 2>&1 || { echo "ERROR: jq is required" >&2; exit 2; }
}

show_versions() {
    require_jq
    echo "Current plugin versions:"
    echo ""
    printf "  %-15s  %s\n" "Plugin" "Version"
    printf "  %-15s  %s\n" "---------------" "-------"
    for plugin in sigil-plugin; do
        manifest="$REPO_ROOT/$plugin/.claude-plugin/plugin.json"
        if [ -f "$manifest" ]; then
            version=$(jq -r '.version' "$manifest")
            printf "  %-15s  %s\n" "$plugin" "$version"
        else
            printf "  %-15s  %s\n" "$plugin" "(not built yet)"
        fi
    done
    echo ""
    echo "Marketplace manifest: $MARKETPLACE"
    if [ -f "$MARKETPLACE" ]; then
        jq -r '.plugins[] | "  \(.name): \(.version)"' "$MARKETPLACE"
    fi
    exit 0
}

# ---------- Args ----------

case "${1:-}" in
    --show) show_versions ;;
    -h|--help) usage ;;
    "") usage ;;
esac

if [ $# -lt 2 ]; then
    echo "ERROR: need <plugin> <new-version>" >&2
    usage
fi

PLUGIN="$1"
NEW_VERSION="$2"

# Validate plugin name
case "$PLUGIN" in
    sigil-plugin) ;;
    *) echo "ERROR: unknown plugin '$PLUGIN' (use sigil-plugin)" >&2; exit 1 ;;
esac

# Validate semver shape
if ! echo "$NEW_VERSION" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z.-]+)?$'; then
    echo "ERROR: '$NEW_VERSION' is not a valid semver (e.g. 0.33.0 or 1.0.0-beta.1)" >&2
    exit 1
fi

require_jq

# Plugin manifest
PLUGIN_DIR="$REPO_ROOT/$PLUGIN"
MANIFEST="$PLUGIN_DIR/.claude-plugin/plugin.json"

if [ ! -f "$MANIFEST" ]; then
    echo "ERROR: plugin manifest not found: $MANIFEST" >&2
    exit 1
fi

# Marketplace manifest must exist
if [ ! -f "$MARKETPLACE" ]; then
    echo "ERROR: marketplace manifest not found: $MARKETPLACE" >&2
    exit 1
fi

# Determine marketplace name (jq filter key) — must match `name` field in plugin.json
PLUGIN_NAME_IN_MARKETPLACE=$(jq -r '.name' "$MANIFEST")

OLD_VERSION=$(jq -r '.version' "$MANIFEST")

if [ "$OLD_VERSION" = "$NEW_VERSION" ]; then
    echo "Version already at $NEW_VERSION. Nothing to do."
    exit 0
fi

# ---------- Update plugin.json ----------

tmp=$(mktemp)
jq --arg v "$NEW_VERSION" '.version = $v' "$MANIFEST" > "$tmp"
mv "$tmp" "$MANIFEST"
echo "  updated: $PLUGIN/.claude-plugin/plugin.json   $OLD_VERSION → $NEW_VERSION"

# ---------- Update marketplace.json ----------

tmp=$(mktemp)
jq --arg name "$PLUGIN_NAME_IN_MARKETPLACE" --arg v "$NEW_VERSION" \
    '.plugins |= map(if .name == $name then .version = $v else . end)' \
    "$MARKETPLACE" > "$tmp"
mv "$tmp" "$MARKETPLACE"
echo "  updated: .claude-plugin/marketplace.json     [$PLUGIN_NAME_IN_MARKETPLACE] → $NEW_VERSION"

# ---------- Update README badge (sigil-plugin only) ----------

if [ "$PLUGIN" = "sigil-plugin" ]; then
    README="$REPO_ROOT/README.md"
    if [ -f "$README" ]; then
        # Replace version badge like: [![Version](https://img.shields.io/badge/version-0.32.0-blue)]
        # Or any "version-X.Y.Z" pattern in a badge URL.
        if grep -qE "version-[0-9]+\.[0-9]+\.[0-9]+" "$README"; then
            sed -i.bak -E "s/version-[0-9]+\.[0-9]+\.[0-9]+/version-$NEW_VERSION/g" "$README"
            rm -f "$README.bak"
            echo "  updated: README.md                            (version badge)"
        else
            echo "  skipped: README.md (no version badge pattern found)"
        fi
    fi
fi

echo ""
echo "Bumped $PLUGIN: $OLD_VERSION → $NEW_VERSION"
echo ""
echo "Next steps:"
echo "  1. Update $PLUGIN's CHANGELOG.md (or CHANGELOG.md at repo root for sigil-plugin)"
echo "  2. Commit the version bump together with the changelog entry"
echo "  3. Tag the release after merge: git tag v$NEW_VERSION && git push --tags"
