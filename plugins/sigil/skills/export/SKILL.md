---
name: export
description: Create a handoff or export package from existing Sigil specs, plans, tasks, reviews, and implementation evidence. Use for engineer handoff, ticket-ready stories, release evidence, or portable review packages; do not invent missing completion evidence.
---

# Export

Determine the requested destination and package type, then follow
`references/export.md`. Resolve the repository root and validate the source
artifacts before packaging.

Keep one local canonical package. Any remote comment, link, ticket update,
push, or publication is a separate external write: state the destination,
action, and intended content and obtain authorization unless the request
already clearly grants it. On remote failure, preserve the local package and
report the remote outcome independently.
