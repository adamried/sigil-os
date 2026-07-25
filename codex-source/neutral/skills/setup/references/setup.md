# Setup behavior

Fresh setup creates only files declared in `state-files.json`. Existing setup
enters verification mode and proposes additions without replacing committed
project artifacts.

The durable `AGENTS.md` block is:

```text
<!-- SIGIL-CODEX-START v1 -->
When a request uses Sigil, read `.sigil/SIGIL.md` before acting.
Use the installed Sigil public skill that matches the requested outcome.
Sigil workflow pacing never changes Codex permissions or managed policy.
<!-- SIGIL-CODEX-END -->
```

The helper treats marker `v1` as a checked format. Duplicate, unbalanced, or
unknown-version markers are conflicts, not repair opportunities.

The detailed neutral rules live in `.sigil/SIGIL.md`. Setup completion always
requires a new session before those durable instructions are assumed active.
