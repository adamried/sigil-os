---
name: decompose
description: Generates a phased Story Map from a received Validated Spec. Approval Gate before story writing. Figma MCP usage rules (no calls in Step 1, frame-level batching in Step 2). Backend/Web/Mobile labels. AC format adaptation.
version: 1.0.0
category: po
chainable: false
invokes: [persona-lookup, scope-check]
invoked_by: [decompose-command]
tools: Read, AskUserQuestion
---

# Skill: Decompose

## Purpose

Turn a Validated Spec into a phased Story Map using `references/story-decomposition-template.md`. The Story Map is approved before any individual story is written. Apply Figma usage rules, label assignment, and AC format rules per FR-C10.

## When to Invoke

- `/decompose <epic-key-or-spec-id>` after `/receive` accepts a spec

## Inputs

- `spec_content`: the received Validated Spec
- `epic_key`, `confluence_link`, `target_team`, `context`: from handoff contract

## Process

### Step 1: Story Map Structure (NO Figma MCP calls — FR-C10)

Read `references/story-decomposition-template.md`. Walk through the spec's User Journeys (Section 5) and Scenarios (Section 6). Group related scenarios into proposed stories.

**Figma rule:** Step 1 makes NO Figma MCP calls. Story-Map-level structure is derived from journeys + scenarios + persona analysis — visual frames are story-level detail, not structure-level.

Output of Step 1 is a draft Story Map with:

- Phased grouping (1 phase if ≤7 stories, multiple phases if 8+)
- Cross-team prerequisites identified (uses `scope-check`)
- Dependency graph
- Deferred items (anything below the Cut Line from the spec)
- Risks / open questions

### Step 2: Story-Level Detail (Figma MCP allowed — batched)

For each story in the draft map, prepare the per-story metadata:

- **Persona** (resolved via `persona-lookup`)
- **Label** — Backend / Web / Mobile (exactly one — FR-C10)
- **Linked frames** — when a story references a Figma frame, batch Figma MCP calls if 3+ stories reference frames in the same file

**Figma batching rule:** if 3+ stories reference Figma frames, issue all `get_frame` calls in one batch (Figma MCP supports concurrent requests). Don't loop per-story.

### Step 3: Label Assignment Rules (FR-C10)

Exactly one label per story:

- **Backend** — server-side work, APIs, data, integrations, no user-visible UI changes
- **Web** — web-app UI work
- **Mobile** — mobile-app UI work (iOS, Android, React Native, Flutter)

If a story genuinely spans Backend + UI work, **split it** into two stories with a dependency relationship. Don't dual-label.

### Step 4: AC Format Rules (FR-C10)

Acceptance Criteria format adapts to the output target:

| Output Target | AC Format |
|---------------|-----------|
| Chat (this session) | Bold `**GIVEN**`, `**WHEN**`, `**THEN**` |
| Confluence | Bold `**GIVEN**`, `**WHEN**`, `**THEN**` |
| Jira AC field | Plain text `GIVEN`, `WHEN`, `THEN` (Jira's bold rendering in AC is unreliable) |

### Step 5: Approval Gate

Render the Story Map and surface via `AskUserQuestion`:

```
Story Map: {N} stories across {M} phases.

Approve and proceed to /story?
  1. Approve — write individual stories now (or later, one at a time)
  2. Revise — give specific feedback
  3. Cancel
```

**Do not write individual stories without approval.**

### Step 6: Output

Render the full Story Map using `references/story-decomposition-template.md`. Include:

- Source spec
- Epic key
- Target team
- Phases with goals and stories
- Cross-team prerequisites
- Dependency graph (plain-text)
- Deferred items
- Risks / open questions
- Approval status

## Outputs

A Markdown Story Map matching the template, plus a verdict on the Approval Gate.

## Anti-patterns

- **Figma calls in Step 1.** Step 1 is structure-only — no frame inspection.
- **Multi-label stories.** Split instead of dual-labeling.
- **Auto-write stories without approval.** The Approval Gate is mandatory.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-27 | Initial release — S4-001 FR-C10 |
