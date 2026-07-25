---
name: learn
description: Capture, search, review, curate, or share durable Sigil project learnings. Use for lessons from implementation or review, recurring patterns, learning history, or shared-context sync. Do not store secrets or unreviewed personal data.
---

# Learn

Determine whether to capture, search, review, curate, or share a learning and
follow `references/learning.md`.

Resolve the repository root. Load only learning files relevant to the current
request. Before persisting, run deterministic secret redaction and perform a
best-effort personal-data review. Do not claim the latter is guaranteed.

Shared-context pushes require the authenticated `gh` capability, explicit
repository and branch values, network approval where required, and separate
remote-write authorization. Failed writes may enter the secret-free,
idempotent queue; local learning capture must still succeed.
