# Install Sigil for Codex

> Preview version: **0.33.0-beta.1**

The Codex edition currently works as a local plugin in Codex CLI and the
ChatGPT desktop app. It is not offered as a Codex IDE-extension plugin.

## Before you start

You need:

- macOS for the currently verified local preview run; Linux verification runs
  in CI before a public support claim is promoted;
- Codex CLI 0.145.0 (the version used for this preview's install test; other
  versions may behave differently);
- Git;
- Python 3.9 or newer; and
- `ruamel.yaml` 0.18.x for commands that edit Sigil settings.

Install the small settings dependency with:

```bash
python3 -m pip install "ruamel.yaml==0.18.*"
```

## Add the marketplace

From a cloned copy of this repository:

```bash
codex plugin marketplace add /full/path/to/sigil-os
```

When the repository is published as a Codex marketplace, you can use:

```bash
codex plugin marketplace add adamried/sigil-os
```

Check that Codex can see it:

```bash
codex plugin list --available
```

## Install and enable Sigil

```bash
codex plugin add sigil@sigil-os
codex plugin list
```

The list should show `sigil@sigil-os` as installed and enabled. The preview
includes Jira and Figma connectors. Codex may ask you to connect those services;
you may skip them and use every core local workflow.

## Review hook trust

Sigil includes optional hooks that provide short reminders at session start,
after relevant file edits, when a Sigil agent starts, and before a pending state
transition is abandoned. Codex asks whether you trust local hook commands.

You can decline. Hooks do not enforce the workflow and all core checks remain
in the Sigil skills. Trust hooks only after reviewing
`plugins/sigil/hooks/hooks.json` and its scripts.

## Set up a project

Open the project in Codex, then say:

> Use `$sigil:setup` to set up this project.

Sigil first shows a plan. It writes only after you confirm. Existing `.sigil/`
content, `CLAUDE.md`, root `SIGIL.md`, and text outside Sigil's marked
`AGENTS.md` block are preserved.

At completion, start a new Codex session. This is required for new project
guidance and optional agents to be discovered reliably.

## Optional agents

Setup can generate nine project-scoped agents under `.codex/agents/`. They are
an accelerator, not a requirement. Without them, Sigil performs the same roles
sequentially.

## Remove the Codex edition

```bash
codex plugin remove sigil@sigil-os
codex plugin marketplace remove sigil-os
```

To remove project guidance, ask `$sigil:setup` to remove its marker block before
uninstalling. It can move generated `.codex/agents/sigil_*.toml` files into the
recoverable `.codex/agents/.sigil-removed/` folder. Do not delete `.sigil/`
unless you also intend to delete project specifications, rules, and workflow
history.

See [Codex migration](codex-migration.md), [Codex integrations](codex-integrations.md),
and [troubleshooting](troubleshooting.md).
