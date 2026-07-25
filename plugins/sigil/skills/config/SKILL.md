---
name: config
description: Show or change Sigil project preferences, constitution access, project profile, integration registry, audit settings, workflow pacing, communication track, or commit automation. Use for configuration and connection requests; do not start feature implementation.
---

# Config

Determine from the user’s request whether they want to show settings, set or
reset a value, manage constitution/profile information, configure an
integration, or inspect audit policy.

Resolve the repository root, then use `scripts/sigil-config`; do not merge YAML
by hand. `show` reports every effective value with its `project`, `global`, or
`default` provenance. The global layer is ignored unless the project records
explicit opt-in.

Before a write:

1. Validate the key and value.
2. Explain the resulting behavior in plain language.
3. For `~/.sigil`, explain the outside-workspace file and obtain explicit
   opt-in.
4. Preserve unknown keys and comments.

`execution_mode` controls Sigil checkpoint pacing only. It never changes
Codex permissions, sandboxing, approvals, managed policy, or hook trust.
Automated commits remain off unless explicitly enabled. Remote actions require
their own authorization.

For constitution, profile, connection, and audit submodes, follow
`references/configuration.md`.
