---
name: handoff-prep
description: Packages a Validated Spec for handoff. Supports local, Confluence, and Jira Epic targets via adapter pattern. Emits the cross-plugin output contract (Epic key, Confluence link, Target team, Context line).
version: 1.0.0
category: pm
chainable: false
invokes: [scope-check]
invoked_by: [handoff-command]
tools: Read, AskUserQuestion
---

# Skill: Handoff Prep

## Purpose

Take a `Status: Validated` spec and prepare it for downstream consumption. Always emit the four-field output contract (Epic key, Confluence link, Target team, Context line) so the PO Buddy `/receive` command can ingest it.

## When to Invoke

- `/handoff <spec-id> [--target local|confluence|jira]`

## Inputs

- `spec_path` or `spec_content`: the Validated Spec
- `target`: `local | confluence | jira` (default: `local`)

## Process

### Step 1: Status Gate

The spec MUST be `Status: Validated`. If `Draft`, return: "Run `/validate` first — this spec hasn't been validated."

### Step 2: Target Resolution

| Target | Adapter required | Behavior |
|--------|------------------|----------|
| `local` | None | Render the package as a Markdown block in conversation |
| `confluence` | Atlassian MCP | Create a Confluence page; capture URL |
| `jira` | Atlassian MCP | Create a Jira Epic with spec embedded; capture key |

If the requested target's adapter is missing, surface the gap with `AskUserQuestion`:

```
You requested {target}, but the Atlassian MCP isn't configured in this session.

  1. Fall back to local handoff (returns Markdown for you to paste)
  2. Cancel — configure the MCP first, then re-run /handoff
```

### Step 3: Target Team

Determine target team:

1. If `references/team-scope.md` exists and the spec references a domain that maps to a team → use that team
2. If user has previously selected a team in this session → use it
3. Else → `(default)` placeholder

### Step 4: Output Contract (FR-C05)

Always emit these four fields, even for local-only:

```
Epic key:         {KEY-123 | (none)}
Confluence link:  {URL | (none)}
Target team:      {Team name | (default)}
Context:          {One-sentence summary, derived from spec TL;DR}
```

The PO Buddy `/receive` command reads these as required inputs (FR-C09 input contract).

### Step 5: Render Package

For target `local`:

```
## Handoff Package — {Spec Title}

### Output Contract
- **Epic key:** {value}
- **Confluence link:** {value}
- **Target team:** {value}
- **Context:** {value}

### Spec
{full spec content embedded}

### Next Steps
- PO: Run `/receive {Epic key or local path}` in po-buddy
- Engineering: Run `/sigil:draw "{Epic key or feature name}"` to start
```

For target `confluence`: same package, plus the Confluence page URL written into the link field.

For target `jira`: spec body becomes the Epic description; output contract fields plus epic key.

### Step 6: Promote

Mark the spec `Status: Handed Off` (in conversation; user's spec store is wherever they keep it).

## Outputs

- The four-field contract block (always)
- The Handoff Package (target-specific format)

## Anti-patterns

- **Silently falling back to local** when MCP target was requested. Always surface the gap.
- **Omitting the contract** for local-only. The contract appears in every handoff, even with placeholder values.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-27 | Initial release — S4-001 FR-C05 |
