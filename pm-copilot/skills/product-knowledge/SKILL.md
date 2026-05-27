---
name: product-knowledge
description: Token-efficient on-demand loader for project product knowledge (personas, team scope, style guide, KB excerpts). Uses an index + on-demand loading pattern to keep always-on context under budget.
version: 1.0.0
category: pm
chainable: false
invokes: []
invoked_by: [define, specify, validate, handoff-prep]
tools: Read, Glob
---

# Skill: Product Knowledge

## Purpose

Provide on-demand access to project-specific product knowledge without loading everything at session start. Maintains a token-efficient index that always-on hooks can include; loads the full content of specific references only when needed.

## When to Invoke

- Another skill needs project-specific context (personas, team scope, brand voice, KB excerpts)
- User asks "where's the {topic} reference?" or "what does our style guide say about X?"

## Inputs

- `topic`: string — the knowledge area requested
- `mode`: `index | load` (default: `index`)

## Process

### Step 1: Index Mode (Default — Loads at SessionStart)

Build a lightweight index of `references/` and any configured KB locations. The index is ≤ 2K tokens — small enough to include in every session via SessionStart hook.

Index format:

```yaml
references:
  - path: references/personas.md
    summary: "Defines 4 personas and 1 anti-persona (Villain) for journey mapping"
    invoked_for: [persona-lookup]

  - path: references/team-scope.md
    summary: "Defines 3 teams and their owned domains (auth, search, billing)"
    invoked_for: [scope-check]

  - path: references/communication-style.md
    summary: "Tone, challenge model, yielding policy, output modes"
    invoked_for: [all skills — loaded at SessionStart]

  - path: references/validated-spec-template.md
    summary: "10-section Validated Spec template"
    invoked_for: [specify, validate]

knowledge_bases:
  - path: kb/style-guide/
    summary: "Brand voice, terminology preferences"
    invoked_for: [specify when writing TL;DR]
```

### Step 2: Load Mode (On Demand)

When another skill needs a specific reference, this skill returns the full content of that file. Caller is responsible for staying within their own token budget.

Load mode never auto-loads at session start — only when explicitly requested by a downstream skill. This is the "on-demand" half of the pattern.

### Step 3: Missing Knowledge

If a requested topic isn't in the index, surface:

```
No reference found for "{topic}".

Available references:
  - personas
  - team-scope
  - communication-style
  - validated-spec-template
  - business-case-template
  - design-ticket-template

If "{topic}" should exist, add it to references/ or KB.
```

## Outputs

For `index`: YAML index of references (always-on, ≤ 2K tokens)
For `load`: full content of the requested reference file

## Token Budget

- **Always-on (index):** ≤ 2K tokens
- **On-demand (load):** unbounded, but caller manages their own budget

The SessionStart hook loads only `communication-style.md` + this index. Other references load only when their skill needs them.

## Anti-patterns

- **Don't auto-load everything at SessionStart.** Index is fine; full content is not.
- **Don't fabricate references.** If a file isn't in `references/`, say so.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-27 | Initial release — S4-001 FR-C16 |
