---
name: quick-flow
description: Streamlined workflow for simple changes—bug fixes, small features, well-understood work.
version: 1.3.0
track: quick
entry_skill: complexity-assessor
---

# Chain: Quick Flow

## Overview

Quick Flow is a streamlined workflow for simple, well-understood changes. It skips the detailed specification and clarification phases, moving directly to a lightweight spec and implementation.

## When to Use

- Complexity assessment returns "Simple" (score 7-10)
- Bug fixes with clear reproduction steps
- Small features with obvious requirements
- Text/copy changes
- Configuration updates
- User explicitly requests "quick" or "just do it"
- Ticket-loader categorizes work as `maintenance` (forced Quick Flow)

### Maintenance Flag Handling

When the orchestrator routes a maintenance ticket to Quick Flow (category `maintenance` from ticket-loader):
- Skip complexity assessor entirely (already determined to be Quick Flow)
- Use a lighter quick-spec: pre-populate Type as "Maintenance" and include ticket metadata
- Constitution constraints still apply but the spec can be minimal
- `ticket_metadata` is preserved in context for handoff-back

## Chain Sequence

```
┌─────────────────────┐
│ complexity-assessor │ ← Entry point
└─────────────────────┘
         │
         │ [If Simple/Quick Flow]
         ▼
┌──────────────────────────┐
│  constitution-check      │ ← File existence check (not a skill invocation)
│  /.sigil/constitution.md │
└──────────────────────────┘
         │
         │ [If exists: inject constraints + tech-stack into quick-spec context]
         │ [If missing: warn user, continue without blocking]
         ▼
┌─────────────────────┐
│    quick-spec       │ ← Lightweight spec (inline)
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  task-decomposer    │ ← Simplified breakdown
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  Developer Agent    │ ← Implementation
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│   qa-validator      │ ← Quick validation
└─────────────────────┘
         │
         │ [If issues, 1 fix attempt]
         ▼
┌─────────────────────┐
│    qa-fixer         │ ← Single fix round
└─────────────────────┘
         │
         │ [If fix resolved Major/Critical issue]
         ▼
┌──────────────────────────┐
│ learning-capture (review)│ ← Rare: only for Major+ fixes
│ (silent, non-blocking)   │
└──────────────────────────┘
         │
         │ [If ticket_key exists in context]
         ▼
┌─────────────────────┐
│    handoff-back      │ ← Write results back to ticket
└─────────────────────┘
         │
         ▼
      Complete
```

## Constitution Check

Before starting quick-spec, verify `/.sigil/constitution.md` exists.

**If exists:** Extract technology stack and code standards constraints. Pass to quick-spec as context so generated specs respect project guardrails.

**If missing:** Block and redirect to constitution setup:
```
Before we can build this, let's set up your project principles.
This takes about 2 minutes and ensures consistent decisions.

Starting constitution setup...
```
→ Run constitution-writer, then return to quick-spec.

Note: When Quick Flow is entered via sigil.md (the normal path), the constitution check has already passed in Step 3.1. This check is a safety net for direct chain invocation.

## Skill Descriptions

### quick-spec (Inline Behavior)

quick-spec is a constraint wrapper skill that invokes spec-writer in lightweight mode. See `skills/specification/quick-spec/SKILL.md` for the constraints applied.

```markdown
# Quick Spec: [Change Description]

**Type:** [Bug Fix | Small Feature | Configuration | Copy Change]
**Files Affected:** [1-5 files]

## What
[One paragraph description]

## Why
[One sentence reason]

## Acceptance
- [ ] [Single criterion]
- [ ] [Single criterion]

## Out of Scope
[Optional—only if ambiguity risk]
```

Generated inline, not persisted unless requested.

### Simplified task-decomposer

For Quick Flow:
- Maximum 5 tasks
- No phase structure (flat list)
- Dependencies implicit
- Minimal documentation

```markdown
## Tasks

- [ ] T1: [Task]
- [ ] T2: [Task]
- [ ] T3: [Task]
```

### Quick qa-validator

Abbreviated validation:
- Tests pass (if tests exist)
- No lint errors
- Files match expected changes
- Single fix attempt if issues found

## State Transitions

### complexity-assessor → constitution-check
**Trigger:** Simple complexity confirmed
**Condition:** Score 7-10 AND user confirms Quick Flow
**Data Passed:** `{ request_description, affected_files_estimate }`

### constitution-check → quick-spec
**Trigger:** Constitution check complete (exists or not)
**Condition:** Always (non-blocking)
**Data Passed:** `{ request_description, affected_files_estimate, constitution_context?: { constraints, tech_stack } }`

### quick-spec → task-decomposer
**Trigger:** Quick spec complete
**Condition:** Always (no clarification phase)
**Data Passed:** `{ quick_spec, files_affected }`

### task-decomposer → Developer
**Trigger:** Tasks ready
**Condition:** ≤5 tasks generated
**Data Passed:** `{ tasks }`

### Developer → qa-validator
**Trigger:** Implementation complete
**Condition:** All tasks done
**Data Passed:** `{ files_changed }`

### qa-validator → qa-fixer
**Trigger:** Issues found
**Condition:** `validation_passed: false` (first time only)
**Data Passed:** `{ issues }`

### qa-fixer → Complete OR Escalate
**Trigger:** Fix attempt complete
**Condition:** If still failing → Escalate to human
**Data Passed:** `{ remaining_issues }` (if escalating)

### qa-fixer → learning-capture (review findings)
**Trigger:** Single fix attempt resolved a substantive issue
**Condition:** `fix resolved AND any issue severity in [Major, Critical]`
**Data Passed:** `{ mode: "review-findings", source: "qa-fix-loop", feature_id, task_id, findings, iterations: 1 }`
**Note:** This triggers rarely in Quick Flow since there is only 1 fix attempt and most Quick Flow issues are minor.

### qa-fixer/learning-capture → handoff-back
**Trigger:** Work complete (after qa-fixer or learning-capture)
**Condition:** `ticket_key` exists in chain context (feature originated from a ticket)
**Data Passed:** `{ ticket_key, adapter, review_status: "APPROVED", tasks_completed, files_changed }`
**Note:** Skipped silently when no ticket_key is present (non-ticket-driven work).

## Human Checkpoints

| Checkpoint | Tier | Condition |
|------------|------|-----------|
| Track confirmation | Auto | After complexity assessment (can override) |
| Quick spec | Auto | Presented but not blocking |
| Completion | Auto | Unless escalated |
| Escalation | Review | If fix fails |

## Task Count Escalation

Quick Flow enforces a maximum of 5 tasks. When task-decomposer generates more than 5 tasks:

1. **Pause** — Do not proceed with implementation
2. **Present options to user:**
   - **A) Escalate to Standard track** — Convert to full pipeline with proper spec and planning. The quick-spec is preserved as a starting point.
   - **B) Scope down** — User selects which tasks to keep (max 5). Remaining tasks are deferred or dropped.
   - **C) Override** — User explicitly accepts >5 tasks in Quick Flow (not recommended). Add warning: *"Quick Flow with >5 tasks loses most of its speed advantage. Consider Standard track."*
3. **Route based on choice:**
   - Option A → Enter full-pipeline at spec-writer
   - Option B → Continue Quick Flow with reduced task list
   - Option C → Continue Quick Flow with full task list (capped at 8 absolute maximum)

### task-decomposer → Escalation (>5 tasks)
**Trigger:** Task count exceeds 5
**Condition:** `task_count > 5`
**Data Passed:** `{ tasks, task_count, quick_spec }`

## Error Handling

### Scope Expansion
```
If during implementation, scope appears larger:
  1. Pause implementation
  2. Notify: "This looks more complex than expected"
  3. Offer: Switch to Standard track OR continue with risk
```

### Single Fix Failure
```
If fix fails on first attempt:
  1. Don't loop—escalate immediately
  2. Present: Issue summary, what was tried
  3. Options: Human fixes OR switch to Standard track
```

### Missing Tests
```
If no tests exist for affected code:
  1. Note in validation: "No existing tests to verify"
  2. Suggest: Manual verification steps
  3. Don't block completion
```

## Example Execution

### Bug Fix
```
User: "Fix the login button that's not working on mobile"

1. complexity-assessor
   → Scores 8/21 → Quick Flow
   → Auto-confirm (obvious fix)

2. quick-spec (inline)
   → Type: Bug Fix
   → Files: src/components/LoginButton.tsx
   → What: Login button unresponsive on mobile due to touch event handling
   → Acceptance: Button works on mobile Safari and Chrome

3. task-decomposer
   → T1: Add touch event handler
   → T2: Test on mobile viewport

4. Developer
   → Implements fix

5. qa-validator
   → Tests pass
   → Lint clean

6. Complete
   → "Fixed login button for mobile. Changes: LoginButton.tsx"
```

### Small Feature
```
User: "Add a loading spinner to the submit button"

1. complexity-assessor
   → Scores 9/21 → Quick Flow

2. quick-spec (inline)
   → Type: Small Feature
   → Files: Button.tsx, Button.css
   → What: Add loading state with spinner to submit buttons

3. task-decomposer
   → T1: Add loading prop to Button
   → T2: Add spinner component
   → T3: Add CSS animation

4. Developer
   → Implements feature

5. qa-validator
   → Passes

6. Complete
```

## Escalation to Standard

Quick Flow can escalate to Standard track when:

1. **Scope grows:** More than 5 files affected
2. **Complexity emerges:** Unexpected dependencies discovered
3. **Ambiguity found:** Can't proceed without clarification
4. **User requests:** "Actually, let's do this properly"

**Escalation process:**
```
1. Preserve quick-spec as starting point
2. Convert to full spec-template format
3. Enter Standard flow at spec-writer (for completion)
4. Continue with clarifier if needed
```

## Limitations

Quick Flow intentionally skips:
- Detailed clarification
- Research phase
- ADRs
- Multiple QA iterations
- Formal code review

These are acceptable trade-offs for genuinely simple work. If any feel risky, switch to Standard.

## Quality Safeguards

Even in Quick Flow:
- Constitution still applies
- Tests must pass (if they exist)
- Lint must be clean
- Security basics checked
- Accessibility not ignored

Quick Flow is "less ceremony," not "less quality."

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.3.0 | 2026-03-05 | Added conditional handoff-back step after qa-fixer/learning-capture — writes results back to originating ticket when ticket_key exists in context. |
| 1.2.0 | 2026-02-20 | S4-104: Maintenance flag handling — maintenance tickets skip complexity assessor, use lighter quick-spec with ticket metadata. |
| 1.1.0 | 2026-02-10 | Audit: Added constitution existence check, task count escalation (>5 tasks) |
| 1.0.0 | 2026-01-20 | Initial release |
