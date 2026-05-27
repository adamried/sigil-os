---
name: addendum
description: Append a numbered addendum to a received spec with [A#] traceability. Detects substantial scope changes that require re-validation back through PM Copilot.
version: 1.0.0
category: po
chainable: false
invokes: [scope-check]
invoked_by: [addendum-command]
tools: Read, AskUserQuestion
---

# Skill: Addendum

## Purpose

Add scope to a previously-received spec with full traceability. Never silent additions. Detect when an addendum is substantial enough to warrant re-validation back through PM Copilot.

## When to Invoke

- `/addendum <description>` against a received spec

## Inputs

- `spec_id`: the parent spec (Epic key, Confluence page, or local path)
- `addition_description`: the new scope being added

## Process

### Step 1: Locate Spec

Use the most recently received spec, OR resolve `spec_id`. If multiple candidates, ask via `AskUserQuestion`.

### Step 2: Compute Addendum Number

Read the spec's existing addenda list (in the spec body, or in a sibling `addenda.md`, or in Jira via Atlassian MCP). Find all `[A{N}]` markers. Next number is `[A{max+1}]`.

If this is the first addendum, start at `[A1]`.

### Step 3: Categorize Addition

Score the addition against escalation triggers:

| Trigger | Substantial? |
|---------|--------------|
| Changes a success metric baseline or target | Yes |
| Moves an item from below-the-cut-line to above | Yes |
| Introduces a new persona not in `references/personas.md` | Yes |
| Introduces a new dependency on another team | Yes |
| Changes a Business Rule affecting existing scenarios | Yes |
| Adds a new scenario to an existing journey | Maybe |
| Adds clarifying notes only | No |
| Edits wording without changing meaning | No |

### Step 4: Escalation Check

If any "Yes" trigger fires, surface:

```
This addendum looks substantial:
  - {Specific change detected}
  - {Specific change detected}

The parent spec was validated by PM. Substantial additions usually need
re-validation.

Options:
  1. Add the addendum AND flag it for revalidation (recommended)
  2. Add as-is, mark "validation-deferred" in the addendum entry
  3. Cancel — this might be better as a new spec
```

Use `AskUserQuestion`. Don't auto-pick.

### Step 5: Write Addendum Entry

Append to the spec (or sibling addenda file):

```markdown
### [A{N}] {YYYY-MM-DD} — {Brief title}

**Added by:** {PO name}
**Trigger:** {What caused this addendum}
**Substance:** {Trivial | Substantial — needs revalidation | Substantial — deferred}

**Addition:**
{Full description}

**Impact on existing spec sections:**
- {Section 4 Scope: moved X above the cut line}
- {Section 5 Journey: added scenario Y}
- {none — pure additive}

**Linked items:**
- Original Epic: {Epic key}
- Revalidation ticket: {Ticket key or N/A}
```

### Step 6: Update Story Map (if exists)

If a Story Map exists for this spec and the addendum adds new in-scope work, prompt:

```
The Story Map for this spec exists. Should the addendum scope be added to the map?
  1. Add as new story(ies) in current phase
  2. Add as new story(ies) in a future phase
  3. Don't update the Story Map (track separately)
```

### Step 7: Output

```
Addendum [A{N}] added to {Spec Title}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Description:    {summary}
Substance:      {Trivial | Substantial | Substantial-deferred}
Linked Epic:    {Epic key}
Revalidation:   {Required (ticket: ...) | Deferred | Not needed}

{Next-step prompt}
```

## Outputs

A numbered addendum entry, linked to the parent spec, with substance categorization.

## Anti-patterns

- **Silent addition.** Numbered with `[A#]`, always.
- **Quiet escalation skip.** When a "substantial" trigger fires, surface it — don't accept-and-move-on.
- **Snowball.** When `[A4]`, `[A5]`, `[A6]` keep piling up, surface: "This many addenda suggest the original spec needed rework — consider a new spec."

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-27 | Initial release — S4-001 FR-C12 |
