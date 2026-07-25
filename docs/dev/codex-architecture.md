# Codex edition architecture

The authored input has two collision-free layers:

- `codex-source/neutral/` contains platform-neutral workflow contracts,
  procedures, roles, specialist overlays, templates, and state metadata.
- `codex-source/codex/` contains the Codex manifest, public skill adapters,
  hooks, apps, deterministic helpers, and package assets.

`tools/build-codex-plugin.py` assembles both layers into `plugins/sigil/`.
That generated directory is the only lint, validation, cache-install, and
release input. Hand edits to generated output are rejected by `--check`.

Eight public outcome skills keep implicit routing inside the description budget.
Internal workflow phases are references, not public skills. The root
coordinator is the only durable-state writer. Nine optional project agents may
execute role contracts, but return evidence to that coordinator and do not own
state.

Hooks are defensive and advisory. Required behavior has an explicit sequential
fallback in the skills. Integrations sit behind stable Jira, Figma, GitHub
shared-context, and external-design-source contracts.

The Claude distribution remains independent during preview. The translation
ledger maps every Claude skill once and the divergence ledger records deliberate
platform differences. A later change may move proven neutral material into a
shared adapter pipeline; generated output must still remain deterministic.
