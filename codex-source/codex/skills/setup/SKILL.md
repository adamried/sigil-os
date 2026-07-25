---
name: setup
description: Initialize, verify, migrate, or remove Sigil project guidance. Use when the user asks to set up Sigil, install its AGENTS.md block, configure a new project, verify an existing .sigil directory, generate optional project agents, or cleanly remove Codex-specific guidance.
---

# Setup

Determine from the user’s request whether they want a fresh setup, migration
verification, optional custom agents, repair guidance, or removal.

## Safety contract

1. Resolve and verify the repository root using
   `../draw/references/protocols/repository-root.md`.
2. Run `scripts/sigil-setup plan --root <resolved-root>` before any write.
3. Present the planned files in plain language. If `.sigil/` already exists,
   enter migration/verification mode: preserve existing content and propose
   only missing Codex files or explicit migrations.
4. Apply only after confirmation with
   `scripts/sigil-setup apply --root <resolved-root> --confirmed` and the
   selected options.
5. Never rewrite `AGENTS.md`. The helper inserts or replaces only the
   `SIGIL-CODEX` marker block and halts on duplicate, unbalanced, or corrupt
   markers.
6. Leave `CLAUDE.md`, root `SIGIL.md`, existing constitution, specs, plans,
   tasks, learnings, waivers, and design files byte-identical unless the user
   confirms a separately displayed migration.

## Choices

Explain these in ordinary language and persist the answers:

- communication track: non-technical (default) or technical;
- workflow pacing: automatic (default), directed, or autonomous;
- whether Sigil may create branches and commits; commits default off;
- whether project audit history is enabled;
- whether to use an opted-in global preferences file under `~/.sigil`;
- whether to generate optional project-scoped custom agents;
- optional Jira, Figma, and shared-context setup.

Sigil workflow pacing does not change Codex sandbox or approval settings.

## Optional custom agents

The sequential coordinator is the baseline. If the user opts in, explain that
agent files will be added under `.codex/agents/`, Codex loads them as project
configuration, parent policy still wins, and a new session is required. Run
`scripts/sigil-agent-generate` only after confirmation. Declining changes
nothing.

## Removal

Show a removal plan before changing anything. Preview the marker-only change
with `scripts/sigil-agents-block remove --root <resolved-root> --dry-run`, then
run it without `--dry-run` only after confirmation. If optional agents exist,
run `scripts/sigil-agent-generate remove --root <resolved-root> --confirmed`;
the helper moves only the nine known Sigil agent files to a recoverable
`.codex/agents/.sigil-removed/` directory. Preserve `.sigil/`, `CLAUDE.md`,
root `SIGIL.md`, user-authored `AGENTS.md` text, and unrelated Codex agents.

## Completion

State exactly: “Start a new Codex session before relying on the new Sigil
guidance or generated agents.”

Hooks are optional local scripts that require separate review and trust. All
core behavior works when they are untrusted or disabled.
