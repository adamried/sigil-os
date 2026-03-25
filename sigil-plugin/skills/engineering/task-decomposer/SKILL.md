---
name: task-decomposer
description: Breaks implementation plans into executable tasks. Invoke when plan is approved and user requests task breakdown, says "tasks", or "break down".
version: 1.2.0
category: engineering
chainable: true
invokes: [specialist-selection]
invoked_by: [task-planner, orchestrator]
tools: Read, Write, Edit, Glob
---

# Skill: Task Decomposer

## Purpose

Transform implementation plans into ordered, trackable tasks. Creates a clear execution path for the Developer agent.

## When to Invoke

- Plan is approved
- User requests `/tasks`
- User says "break it down" or "create tasks"
- Task Planner agent receives decomposition request

## Inputs

**Required:**
- `plan_path`: string — Path to approved implementation plan

**Optional:**
- `spec_path`: string — Path to spec (for requirement tracing)
- `max_tasks`: number — Maximum tasks before flagging (default: 20)

**Auto-loaded:**
- `project_context`: string — `/.sigil/project-context.md`

## Pre-Execution Check

Before starting, update `.sigil/project-context.md`:
- Set **Current Phase** to `tasks`
- Set **Feature** to the feature being decomposed
- Set **Spec Path** to the active spec directory
- Set **Last Updated** to the current timestamp

If `.sigil/project-context.md` does not exist, create it using the State Tracking format from the `/sigil:draw` command.

## Process

### Step 1: Plan Analysis

```
1. Load plan from plan_path
2. Extract implementation phases
3. Identify file changes (new, modified, deleted)
4. Note dependencies between components
5. Identify testing requirements
```

### Step 2: Task Identification

For each implementation phase, identify tasks:

**Setup Tasks:**
- Directory/file scaffolding
- Configuration changes
- Dependency installation

**Foundation Tasks:**
- Core data models
- Base services/utilities
- Shared components

**Feature Tasks (by User Story):**
- Tests (write first)
- Implementation
- Integration

**Accessibility Tasks:**
- Keyboard navigation
- ARIA labels
- Color contrast fixes

**Finalization Tasks:**
- Integration testing
- Documentation updates
- Cleanup

### Step 3: Dependency Mapping

```
For each task:
  1. Identify what it depends on
  2. Identify what depends on it
  3. Mark as [B] if blocking
  4. Mark as [P] if parallelizable
```

### Step 4: Task Ordering

Order tasks to:
1. Respect dependencies (blockers first)
2. Enable parallel work where possible
3. Group by phase for clarity
4. Place tests before implementations (test-first)

### Step 4.5: Specialist Assignment

For each task, invoke the `specialist-selection` skill with the task description and file list:

```
For each task:
  1. Pass task_description and task_files to specialist-selection
  2. Receive developer_specialist and validation_specialists
  3. Store assignment for use in Step 5
```

If specialist-selection returns no match, the task uses the base agent (no specialist override).

### Step 5: Task Enrichment

For each task, add:

```markdown
- [ ] **T###** [B|P] [Description]
  - Files: `[paths to files affected]`
  - Specialist: [specialist name or "base" if no specialist assigned]
  - Depends on: [T### list]
  - Acceptance: [How to verify complete]
```

### Step 6: Threshold Check

```
If total_tasks > max_tasks:
  - Flag for human review
  - Suggest grouping or phasing
  - May indicate scope too large

If total_tasks < 3:
  - May indicate Quick Flow appropriate
  - Consider simpler workflow
```

### Step 7: Write Output

```
1. Load template from /templates/tasks-template.md
2. Fill in summary metrics
3. Write tasks by phase
4. Generate dependency map
5. Document parallel opportunities
6. Write to spec directory
7. Update project-context.md
```

## Outputs

**Artifact:**
- `/.sigil/specs/###-feature/tasks.md` — Task breakdown

**Handoff Data:**
```json
{
  "tasks_path": "/.sigil/specs/001-feature/tasks.md",
  "plan_path": "/.sigil/specs/001-feature/plan.md",
  "spec_path": "/.sigil/specs/001-feature/spec.md",
  "total_tasks": 12,
  "phases": ["Setup", "Foundation", "Auth Flow", "Accessibility", "Testing"],
  "blocking_tasks": ["T001", "T002", "T005"],
  "parallelizable_groups": [
    ["T003", "T004"],
    ["T007", "T008", "T009"]
  ],
  "requires_human_review": false,
  "estimated_complexity": "standard",
  "first_task": {
    "id": "T001",
    "description": "Set up authentication module directory structure",
    "phase": "Setup",
    "specialist": null,
    "blocking": true,
    "files": ["src/auth/", "src/auth/index.ts"],
    "depends_on": [],
    "acceptance": "Directory exists, exports configured"
  }
}
```

## Task Quality Checklist

Before completing, verify:

- [ ] Every file from plan has associated task(s)
- [ ] Test tasks precede implementation tasks
- [ ] Dependencies form valid DAG (no cycles)
- [ ] Blocking tasks clearly marked
- [ ] Parallel opportunities identified
- [ ] Each task has clear acceptance criteria
- [ ] Accessibility tasks included
- [ ] Specialist assigned for each task (or explicitly "base")
- [ ] Task count within reasonable range

## Task ID Format

```
T### — Sequential number

Examples:
T001 — First task
T002 — Second task
T010 — Tenth task
```

## Phase Naming Convention

Standard phases:
1. **Setup** — Infrastructure, scaffolding
2. **Foundation** — Core components others depend on
3. **[Feature Area]** — Named by user story or capability
4. **Accessibility** — A11y-specific work
5. **Testing** — Final validation tasks

## Human Checkpoints

- **Auto Tier:** Task generation (≤20 tasks)
- **Review Tier:** Task generation (>20 tasks)
- User confirms task breakdown before implementation

## Error Handling

| Error | Resolution |
|-------|------------|
| Plan not approved | Return to planning phase |
| Circular dependencies | Flag and request plan revision |
| Task count excessive | Suggest breaking into multiple features |
| Missing test tasks | Add test tasks automatically |

## Example Task Breakdown

**Input Plan Phase:**
```
Phase 2: Core Implementation
- Create User model
- Create Auth service
- Create Login endpoint
```

**Output Tasks:**
```markdown
## Phase 2: Foundation

### User Model
- [ ] **T003** [B] Write User model tests
  - Files: `src/models/user.test.ts`
  - Acceptance: Tests exist, fail (no implementation yet)

- [ ] **T004** [B] Implement User model
  - Files: `src/models/user.ts`
  - Depends on: T003
  - Acceptance: T003 tests pass

### Auth Service
- [ ] **T005** [P] Write Auth service tests
  - Files: `src/services/auth.test.ts`
  - Depends on: T003
  - Acceptance: Tests exist, fail

- [ ] **T006** [P] Implement Auth service
  - Files: `src/services/auth.ts`
  - Depends on: T004, T005
  - Acceptance: T005 tests pass
```

## Integration Points

- **Invoked by:** `task-planner` or `orchestrator`
- **Receives from:** `technical-planner`
- **Hands off to:** Developer agent (first task)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2.0 | 2026-03-11 | Moved from workflow/ to engineering/ category |
| 1.1.0 | 2026-02-19 | S3-101: Added specialist assignment via specialist-selection skill, Specialist field in task format, specialist check in quality checklist |
| 1.0.0 | 2026-01-20 | Initial release |
