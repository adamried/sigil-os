---
name: scope-check
description: Validates that work stays within declared scope. Detects scope creep mid-conversation, identifies cross-team handoffs based on configurable team-scope.md, and generates handoff messages dynamically.
version: 1.0.0
category: pm
chainable: false
invokes: []
invoked_by: [specify, handoff-prep]
tools: Read
---

# Skill: Scope Check

## Purpose

Two responsibilities:

1. **Scope creep detection** — surface when a conversation drifts outside the spec's declared scope
2. **Cross-team routing** — when team-scope.md defines multi-team boundaries, identify when work crosses teams and generate the handoff message

This skill is configurable — projects define team boundaries in `references/team-scope.md`. There is no hardcoded team list. Single-team projects skip team routing entirely.

## When to Invoke

- `specify` runs scope-check after writing Section 4 (Scope)
- `handoff-prep` runs scope-check to determine target team
- User says "is this in scope?" or "who owns this?"

## Inputs

- `feature_description`: string
- `affected_files_or_domains`: array of strings (optional)
- `mode`: `creep | routing` (default: `creep`)

## Process

### Step 1: Load Team Scope (Routing Mode Only)

Read `references/team-scope.md`. The file defines teams and their domains:

```markdown
## Team A
**Domains:** authentication, user management, billing
**Lead:** {Name}
**Notes:** ...

## Team B
**Domains:** search, recommendations, analytics
**Lead:** {Name}
```

If the file doesn't exist OR has only one team defined → single-team mode. Skip routing entirely.

### Step 2: Mode Behavior

#### Mode: `creep`

Compare current conversation against the spec's declared scope (above the Cut Line in Section 4). Surface any of the following as creep:

- A new feature appears that wasn't in scope
- A persona appears that wasn't in personas.md
- A dependency appears that wasn't in Section 7
- A success metric is being changed mid-conversation

Output a structured creep alert when detected. The user decides whether to absorb (revise spec), defer (open question), or reject (out of scope).

#### Mode: `routing`

Match the feature's affected domains against team-scope entries. Output the target team plus a handoff message.

**Handoff message template (generated dynamically per team config):**

```
This work belongs to {Team Name} (lead: {Lead Name}).

Their domains include: {matched domains}.

Recommended path:
  1. PM Copilot `/handoff` produces the package
  2. Hand the Epic key + Confluence link to {Team Name}'s PO
  3. {Team Name}'s PO runs po-buddy `/receive {Epic key}`
```

If multiple teams match (cross-team work): output all matched teams and the cross-team coordination message.

### Step 3: Single-Team Mode

When team-scope.md is missing or has one team, skip routing entirely. Output:

```
{single team mode — no cross-team routing applies}
```

## Outputs

For `creep`:

```json
{
  "creep_detected": true | false,
  "items": [
    {"type": "feature | persona | dependency | metric", "description": "...", "suggested_action": "absorb | defer | reject"}
  ]
}
```

For `routing`:

```json
{
  "target_team": "{Team Name | (default)}",
  "matched_domains": ["..."],
  "cross_team": true | false,
  "handoff_message": "..."
}
```

## Anti-patterns

- **Don't flag every detail change as creep.** Only material additions to scope, personas, dependencies, or metrics.
- **Don't fabricate team boundaries.** Single-team mode is valid — don't pretend multi-team when the config doesn't support it.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-27 | Initial release — S4-001 FR-C14, FR-C16 |
