---
name: sprint-summary
description: Generate a structured sprint planning summary from written stories. Read-only — no ticket creation, no external writes.
version: 1.0.0
category: po
chainable: false
invokes: []
invoked_by: [sprint-summary-command]
tools: Read
---

# Skill: Sprint Summary

## Purpose

Aggregate a set of stories (typically a sprint candidate) into a structured planning summary. Read-only — this skill never creates tickets or writes externally. The output is for sprint planning conversations.

## When to Invoke

- User says "summarize this sprint" or "build the sprint plan"
- PO is preparing for sprint planning and needs a structured view

## Inputs

- `stories`: array of story IDs, paths, or paste-in content
- `sprint_name`: optional sprint identifier (e.g., "Sprint 23", "Q2-W3")

## Process

### Step 1: Gather Stories

For each input:

- **Local content** — already loaded
- **Jira keys** — Atlassian MCP `get_issue` (read-only, never write)
- **Confluence URL** — Atlassian MCP `get_page` (read-only)

If MCP isn't available for a remote source, ask for paste-in.

### Step 2: Compute Aggregates

For the story set, compute:

- **Total stories:** N
- **Label breakdown:** Backend / Web / Mobile counts
- **Persona breakdown:** who's affected, how many stories per persona
- **Epic linkage:** how many distinct epics, list them
- **Dependency map:** which stories have explicit dependencies on others
- **Estimate roll-up:** if stories carry estimates (story points, days), sum them

### Step 3: Identify Risks

Surface (without resolving):

- Stories with unresolved Open Questions
- Stories with cross-team dependencies that aren't yet scheduled
- Stories that touch the same files (potential merge conflicts during sprint)
- Stories with weak acceptance criteria (would benefit from refinement)

### Step 4: Output

Render the summary as a Markdown block:

```
Sprint Summary: {Sprint Name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stories:     {N}
Labels:      Backend: {N}  Web: {N}  Mobile: {N}
Epics:       {Count} — {list of Epic keys}
Personas:    {Persona A: N stories, Persona B: N stories}
Estimates:   {Total if applicable}

### Story List
| Story | Label | Persona | Epic | Notes |
|-------|-------|---------|------|-------|
| ...   | ...   | ...     | ...  | ...   |

### Risks
- {Risk 1}
- {Risk 2}

### Recommended Pre-Sprint Actions
- {e.g., "Resolve Story-12's open question with Design before sprint start"}
- {e.g., "Coordinate with Team B on Story-08's cross-team dependency"}
```

### Step 5: Surface Next Steps

```
Next steps:
  1. Review with team in sprint planning
  2. Run `/story-refinement` on any flagged-weak stories before commit
  3. Coordinate cross-team dependencies before kickoff
```

## Outputs

A Markdown sprint planning summary. No external writes. No ticket creation.

## Anti-patterns

- **Writing tickets.** This skill is read-only. Use `/prepare` for writes.
- **Fabricating estimates.** If stories don't carry estimates, say so — don't invent.
- **Optimistic risk summary.** Surface real risks even if uncomfortable. Sprint planning needs honest signals.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-27 | Initial release — S4-001 FR-C23 |
