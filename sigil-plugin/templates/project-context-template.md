# Project Context

> Auto-updated file tracking current project state across sessions.
> Used by `/sigil:draw` command for workflow detection and resume capability.
>
> **Last Updated:** [TIMESTAMP]

---

## Active Workflow

> This section is read by `/sigil:draw continue` to resume work. Keep it current.

- **Current Phase:** none
- **Feature:** null
- **Spec Path:** null
- **Track:** null
- **Started:** null
- **Last Updated:** [TIMESTAMP]

### Phase Values
<!-- Valid phases: specify | clarify | plan | tasks | implement | validate | review | none -->

---

## Current Work

### Active Feature
- **Feature:** [Feature name or "None"]
- **Spec Path:** [/.sigil/specs/###-feature/ or "N/A"]
- **Track:** [Quick Flow | Standard | Enterprise]

### Current Phase
- **Phase:** [Assessment | Specify | Clarify | Plan | Tasks | Implement | Validate | Review | Complete]
- **Status:** [In Progress | Blocked | Awaiting Review | Complete]
- **Active Agent:** [Orchestrator | Business Analyst | Architect | Task Planner | Developer | QA Engineer | Security | DevOps]

### Current Task (if in Implement phase)
- **Task ID:** [T### or "N/A"]
- **Description:** [Task description]
- **Status:** [Not Started | In Progress | Validating | Complete]

---

## Progress Summary

### Completed Phases
- [ ] Phase 0: Assessment — Complexity assessed, track selected
- [ ] Phase 1: Specify — Spec created
- [ ] Phase 2: Clarify — Ambiguities resolved
- [ ] Phase 3: Plan — Implementation plan created
- [ ] Phase 4: Tasks — Tasks decomposed
- [ ] Phase 5: Implement — Code written
- [ ] Phase 6: Validate — QA passed
- [ ] Phase 7: Review — Approved

### Tasks Overview (if applicable)
- **Total Tasks:** [N]
- **Completed:** [N]
- **In Progress:** [N]
- **Remaining:** [N]

---

## Recent Activity

<!-- Last 5 significant actions, newest first -->

| Timestamp | Action | Agent | Outcome |
|-----------|--------|-------|---------|
| [TIME] | [Action taken] | [Agent] | [Result] |
| [TIME] | [Action taken] | [Agent] | [Result] |
| [TIME] | [Action taken] | [Agent] | [Result] |
| [TIME] | [Action taken] | [Agent] | [Result] |
| [TIME] | [Action taken] | [Agent] | [Result] |

---

## Open Decisions

<!-- Decisions awaiting human input -->

### Decision 1: [Topic]
- **Context:** [Why this decision is needed]
- **Options:** [Available choices]
- **Recommended:** [Suggested option]
- **Status:** Awaiting input

<!-- Add more decisions as needed -->

---

## Blockers

<!-- Issues preventing progress -->

### Active Blockers
- [ ] [Blocker description] — [Required action]

### Resolved Blockers
- [x] [Resolved blocker] — [How it was resolved]

---

## Session Notes

<!-- Agents add notes for context continuity -->

### Key Decisions Made This Session
- [Decision 1]
- [Decision 2]

### Important Context for Next Session
- [Context 1]
- [Context 2]

### Known Issues or Concerns
- [Issue 1]
- [Issue 2]

---

## Quick Reference

### Key Files
- Constitution: `/.sigil/constitution.md`
- Current Spec: [Path or "N/A"]
- Current Plan: [Path or "N/A"]
- Current Tasks: [Path or "N/A"]

### Next Human Touchpoint
- **Action Needed:** [What user needs to do]
- **Tier:** [Auto | Review | Approve]
- **Context:** [Why this needs attention]
