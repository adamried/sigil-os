# Migration Guide: Global Installation to Plugin

> **Sunset Notice:** The global `install-global.sh` installation method is no longer supported as of v2.0.0. All users should migrate to the plugin architecture described below.

This guide helps existing Sigil OS users migrate from the global `install-global.sh` installation to the new Claude Code plugin architecture.

## Overview

Sigil OS v2.0 transitions from a shell-script-based installation to a Claude Code plugin. This provides:

- **Automatic enforcement** via lifecycle hooks (no more relying on Claude following instructions)
- **Standard distribution** via Claude Code's plugin marketplace
- **Easy updates** via `claude plugin update sigil@sigil-os`
- **Team distribution** via project-scoped plugin configuration

## Prerequisites

- Claude Code v1.0+ with plugin support
- Existing Sigil OS global installation (optional, for migration)

## Migration Steps

### Step 1: Uninstall Global Installation (if present)

If you have an existing global installation:

```bash
# Run the uninstall command
~/.sigil-os/install-global.sh --uninstall

# Or manually remove:
rm -rf ~/.claude/agents/
rm -rf ~/.claude/skills/
rm -rf ~/.claude/chains/
rm -rf ~/.claude/commands/
rm -f ~/.claude/.sigil-version
rm -rf ~/.sigil-os/
```

**Note:** This removes global Sigil components. Your project-specific files (`.sigil/`, `.sigil/specs/`) are not affected.

### Step 2: Install the Plugin

```bash
# Add marketplace and install
claude plugin marketplace add araserel/sigil-os
claude plugin install sigil@sigil-os
```

### Step 3: Verify Installation

Start a new Claude Code session in your project:

```bash
cd your-project
claude
```

Then run:
```
/sigil:draw status
```

You should see the Sigil OS status dashboard.

### Step 4: Update Project Files (if needed)

The plugin will automatically update your project's `SIGIL.md` file on first run. The new version:

- References plugin-based components instead of `~/.claude/` paths
- Uses enforcement version 2.1.0
- Maintains the same mandatory rules

Your `CLAUDE.md` pointer line remains unchanged:
```
<!-- Project: Check for ./SIGIL.md and follow all rules if present -->
```

## What Stays the Same

These project-specific directories are **not affected** by the migration:

| Directory | Purpose | Migration Impact |
|-----------|---------|------------------|
| `.sigil/constitution.md` | Project principles | No change |
| `.sigil/project-context.md` | Workflow state | No change |
| `.sigil/learnings/` | Captured learnings | No change |
| `.sigil/specs/` | Feature specifications | No change |

## What Changes

| Before (v1.x) | After (v2.0) |
|---------------|--------------|
| Components at `~/.claude/` | Components in plugin |
| Manual preflight check | Automatic via SessionStart hook |
| Git-based updates | Plugin marketplace updates |
| `install-global.sh` | `claude plugin install` |
| Instruction-based enforcement | Hook-based enforcement |

## Team Installation

For teams, add Sigil OS to your project's plugin configuration:

**`.claude/settings.json`** (committed to repo):
```json
{
  "plugins": {
    "sigil-os": {
      "enabled": true,
      "version": "2.1.2"
    }
  }
}
```

Team members will automatically have Sigil OS installed when they open the project in Claude Code.

## Troubleshooting

### "Plugin not found" error

Ensure Claude Code v1.0+ is installed and plugin support is enabled:
```bash
claude --version
```

### Old enforcement rules still appearing

If `SIGIL.md` shows v1.x rules, run `/sigil:draw` to trigger the automatic update, or manually delete `SIGIL.md` to regenerate it.

### Skills not invoking correctly

Verify the plugin is installed:
```bash
claude plugin list
```

Should show `sigil-os` in the installed plugins.

### Hook scripts not running

Check that hooks are enabled in your Claude Code settings and that the hook scripts are executable.

## Getting Help

- **Documentation:** `/sigil:draw help`
- **Issues:** https://github.com/araserel/sigil-os/issues
- **Updates:** `/sigil:update`
