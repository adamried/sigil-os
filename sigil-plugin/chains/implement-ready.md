---
name: implement-ready
description: Streamlined implementation workflow for pre-decomposed stories with acceptance criteria. Skips spec-writer, clarifier, and task-decomposer.
version: 1.0.0
track: quick, standard
entry_skill: ticket-loader
---

# Chain: Implement-Ready

## Overview

The implement-ready chain is a streamlined workflow for stories that arrive pre-written with acceptance criteria from Jira. It treats the story as a single task and the acceptance criteria as the spec, skipping spec-writer, clarifier, and task-decomposer entirely.

## When to Use

- Ticket-loader categorizes the ticket as `pre-decomposed`
- Story has acceptance criteria already written in Jira
- No architecture planning or spec authoring needed — the story IS the spec

## What This Chain Does NOT Invoke

The following skills/agents are explicitly skipped:
- `spec-writer` — AC serves as the spec
- `clarifier` — story is assumed pre-clarified
- `uiux-designer` — not invoked (design is in the story)
- `architect` / `technical-planner` — no architecture phase
- `task-decomposer` — story = single task

## Pre-Chain: Preflight Check

Same as full-pipeline: the `preflight-check` skill runs via the SessionStart hook before this chain begins.

## Pre-Chain: Configuration Loading

After preflight, the Orchestrator reads `.sigil/config.yaml` (defaults apply if missing). The `user_track` and `execution_mode` values are passed through the chain.

## Chain Sequence

```
┌─────────────────────┐
│   ticket-loader     │ ← Entry (ticket key input, category = pre-decomposed)
└─────────────────────┘
         │ [enriched_description + ticket_metadata + acceptance_criteria]
         ▼
┌─────────────────────┐
│ complexity-assessor  │ ← Score the story
└─────────────────────┘
         │
         │ [If score >= 17 → ESCALATE to full-pipeline]
         │ [If score < 17 → continue]
         ▼
┌─────────────────────┐
│ constitution-check   │ ← Verify against project constitution
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│ specialist-selection │ ← Assign dev specialist
│ (developer)         │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│   Developer Agent    │ ← Story = single task, AC = spec
│ (+ specialist overlay)│
│ (loads learnings     │
│  internally via      │
│  learning-reader)    │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│ specialist-selection │ ← Assign QA specialists
│ (validation)        │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│    qa-validator      │
│ (+ specialist overlay)│
└─────────────────────┘
         │
     [If issues found]
         ▼
┌─────────────────────┐
│     qa-fixer         │ ← Quick: max 1 / Standard: max 5
└─────────────────────┘
         │
     [If fix loop resolved with
      iterations > 1 AND Major+]
         ▼
┌──────────────────────────┐
│ learning-capture (review)│
│ (silent, non-blocking)   │
└──────────────────────────┘
         │
         ▼
┌─────────────────────┐
│   code-reviewer      │ ← Code review
└─────────────────────┘
         │
         │ [If security-related]
         ▼
┌─────────────────────┐
│  security-reviewer   │ ← Conditional
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│    handoff-back      │ ← Write results back to ticket
└─────────────────────┘
         │
         ▼
      Complete
```

## Enterprise Escalation

If complexity-assessor scores the story at 17 or above (Enterprise threshold):

1. Inform the user: "This story scores as Enterprise complexity. It needs full specification and planning."
2. Redirect to the `full-pipeline` chain with the existing `enriched_description` and `ticket_metadata`
3. The full-pipeline will run spec-writer, clarifier, technical-planner, and task-decomposer as normal

## Implementation Note

The Developer Agent receives:
- **Task description:** The story summary from Jira
- **Acceptance criteria:** The AC field from Jira (treated as the spec)
- **Files:** Inferred from the story description and codebase context
- **Context:** `ticket_metadata` from ticket-loader

There is no tasks.md file. The story IS the single task. The Developer follows its normal workflow (load learnings → understand → test first → implement → verify → capture learnings) with the AC as acceptance criteria.

## QA Fix Loop Limits

| Track | Max Fix Iterations |
|-------|--------------------|
| Quick | 1 |
| Standard | 5 |

If the fix loop exceeds the limit, escalate to the user.

## Human Checkpoints

| Checkpoint | Tier | Condition |
|------------|------|-----------|
| Enterprise escalation | Review | Score >= 17 |
| Code review | Review | After implementation |
| Security review | Approve | If security-related changes |
| QA escalation | Review | Fix loop exceeded |

## Error Handling

### Story Has No Acceptance Criteria
```
If acceptance_criteria is empty after extraction:
  1. This should not happen (categorize would not return pre-decomposed)
  2. If it does, fall back to feature routing (full-pipeline)
```

### Constitution Check Fails
```
If no constitution exists:
  1. Prompt user to run /sigil:setup
  2. Do not proceed without constitution
```

### Complexity Too High
```
If complexity score >= 17:
  1. Inform user of escalation
  2. Redirect to full-pipeline with preserved context
```

## Context Preservation

Between skills, preserve:
- `chain_id`: Unique identifier for this chain execution
- `track`: Selected workflow track (quick or standard)
- `user_track`: Configuration user track (non-technical | technical)
- `execution_mode`: Configuration execution mode (automatic | directed)
- `ticket_key`: External ticket key (e.g., `PROJ-123`)
- `ticket_metadata`: Full ticket metadata from ticket-loader
- `ticket_category`: `pre-decomposed`
- `acceptance_criteria`: The AC text from Jira

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-25 | Initial release — GB-fork: implement-ready chain for pre-decomposed stories |
