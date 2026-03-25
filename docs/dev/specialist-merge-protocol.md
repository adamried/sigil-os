# Specialist Merge Protocol

> How specialist agent definitions merge with base agent definitions at runtime.

---

## Overview

Specialist agents customize base agents for domain-specific work. At runtime, the specialist definition is merged with its base agent to produce a combined behavior set. This merge happens per-task — different tasks in the same feature can use different specialists.

## Merge Process

When a task has a specialist assigned (via the `specialist-selection` skill):

```
1. Load base agent definition (e.g., agents/developer.md)
2. Load specialist definition (e.g., agents/specialists/api-developer.md)
3. Verify specialist's `extends` field matches the base agent
4. Merge: specialist sections override matching base sections
5. Adopt merged behavior for the current task only
6. Revert to base agent (or next specialist) for the next task
```

## Field Precedence

| Field | Source | Notes |
|-------|--------|-------|
| **name** | Specialist | Identifies which specialist is active |
| **extends** | Specialist | Declares the base agent (e.g., `developer`) |
| **description** | Specialist | Overrides base description |
| **tools** | Base agent | Specialists do not modify tool permissions |
| **Priority Overrides** | Specialist | Replaces base agent's priority ordering |
| **Evaluation Criteria** | Specialist | Replaces base criteria with domain-specific checks |
| **Risk Tolerance** | Specialist | Replaces base risk assessment |
| **Domain Context** | Specialist | Adds domain-specific knowledge (not present in base) |
| **Collaboration Notes** | Specialist | Adds cross-specialist interaction guidance |
| **Workflow** | Base agent | Specialists inherit the base workflow (test-first, handoff, etc.) |
| **Human Checkpoint** | Base agent | Tier and escalation rules come from the base |
| **Skills Invoked** | Base agent | Specialist does not change which skills are invoked |

**Rule:** Specialist sections override matching sections in the base. Sections that exist only in the base are inherited unchanged. Sections that exist only in the specialist are added.

## Tool Union

Specialists inherit the base agent's tool list. They cannot add or remove tools. This ensures consistent capability boundaries:

- Developer specialists always have: `[Read, Write, Edit, Bash, Glob, Grep]`
- QA specialists always have: `[Read, Write, Edit, Bash, Glob, Grep]`
- Security specialists always have: `[Read, Write, Glob, Grep]`

## Constraint Inheritance

Specialists inherit all base agent constraints:
- Constitution compliance checks
- Learning reader/capture lifecycle
- QA fix loop behavior
- Escalation triggers
- Max fix attempts

Specialists cannot override constraints — they can only add domain-specific evaluation criteria.

## Examples

### Developer + API Developer

```
Base (developer.md):
  - Workflow: test-first → implement → verify → capture
  - Standards: Clean code, minimal changes
  - Skills: learning-reader, learning-capture, react-ui, etc.

Specialist (api-developer.md):
  + Priority Overrides: Contract stability, versioning discipline
  + Evaluation Criteria: Response consistency, backwards compat
  + Risk Tolerance: Very low for breaking changes
  + Domain Context: HTTP semantics, OpenAPI, pagination
  + Collaboration Notes: Works with integration-developer, data-developer

Merged behavior:
  - Workflow: (inherited) test-first → implement → verify → capture
  - Standards: (inherited) Clean code, minimal changes
  - Skills: (inherited) learning-reader, learning-capture, etc.
  - Priorities: (specialist) Contract stability first
  - Evaluation: (specialist) Backwards compat checks
  - Risk: (specialist) Very low for breaking changes
  - Context: (specialist) HTTP semantics, OpenAPI knowledge
```

### QA Engineer + Performance QA

```
Base (qa-engineer.md):
  - Workflow: validate → fix loop → report
  - Skills: qa-validator, qa-fixer, learning-capture

Specialist (performance-qa.md):
  + Priority Overrides: Resource consumption, latency budgets
  + Evaluation Criteria: Query analysis, load patterns
  + Risk Tolerance: Medium (perf degradation is less severe than data loss)

Merged behavior:
  - Workflow: (inherited) validate → fix loop → report
  - Skills: (inherited) qa-validator, qa-fixer, learning-capture
  - Priorities: (specialist) Resource consumption focus
  - Evaluation: (specialist) Query analysis, load patterns
```

## Specialist Visibility

How specialists appear to users depends on the user track:

| Track | Specialist Visibility |
|-------|----------------------|
| `non-technical` | Hidden. Progress shows: "Building: 3/8 steps — Working on form validation" |
| `technical` | Shown. Progress shows: "Task T003 implementing (api-developer)" |

## Lifecycle

```
specialist-selection assigns → Load specialist → Merge with base → Execute task → Revert
```

Each task gets a fresh merge. Specialist state does not carry between tasks.

## Related Documents

- [Agents README](../../agents/README.md) — Specialist catalog and inheritance model
- [specialist-selection SKILL.md](../../skills/workflow/specialist-selection/SKILL.md) — Assignment rules
- [`/sigil:draw` command](../../commands/sigil:draw.md) — Implementation loop that executes the merge
