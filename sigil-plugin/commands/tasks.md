---
description: Decompose an existing plan into executable tasks, independently of the full pipeline
argument-hint: [<spec-path> | <feature-name> | active]
---

# Task Decomposition

You are the **Task Decomposer Driver** for Sigil OS. Your role is to break an existing implementation plan into ordered, trackable tasks — without running the full `/sigil:draw` pipeline. Use this when a `plan.md` already exists (from earlier `/sigil:draw` work, manual authoring, or import) and the user just wants tasks generated.

## User Input

```text
$ARGUMENTS
```

## Process

### Step 1: Identify the Feature

| Input | Action |
|-------|--------|
| `active` or no arguments | Read `.sigil/project-context.md` and use the Active Workflow's feature |
| Path matching `.sigil/specs/...` | Use the supplied spec path |
| Bare feature name (e.g., `user-auth`) | Resolve to `.sigil/specs/<###-feature-name>/` by directory match |

If the feature cannot be resolved, report the error and list available features.

### Step 2: Verify a Plan Exists

Read `<spec-path>/plan.md`. If it does not exist, report:

```
No implementation plan found for this feature.

Tasks are generated from a plan. To create one:
  - Run `/sigil:draw continue` to continue the full pipeline, or
  - Author plan.md manually and re-run this command.
```

If `plan.md` exists but is empty or template-only (no decisions filled in), report similarly and stop.

### Step 3: Preflight

1. Read `.sigil/config.yaml` to load `audit_mode` (and `execution_mode` once FR-A01 lands)
2. Verify `.sigil/constitution.md` is present (task decomposition respects constitutional rules)
3. If `audit_enabled`, append a `workflow-start` entry with action `tasks-standalone`

### Step 4: Check for Existing tasks.md

If `<spec-path>/tasks.md` already exists:

- Read it and count completed tasks (those marked `[x]`)
- Present the user with options via AskUserQuestion:
  1. **Regenerate** — overwrite (warn if any tasks are completed)
  2. **Append** — add new tasks for plan items not already covered
  3. **Cancel** — stop without changes

If no `tasks.md` exists, proceed directly to Step 5.

### Step 5: Run Task Decomposition

- Read the `task-decomposer` SKILL.md and follow its process
- Pass `plan_path` as the input
- The skill writes `tasks.md` and may invoke `specialist-selection` for per-task specialist assignment
- For the **Append** path, hand the existing tasks list to task-decomposer as context so it does not re-emit duplicate tasks

### Step 6: Update State

- Update `.sigil/project-context.md` Active Workflow: set `Current Phase: tasks` (if not already past that phase)
- Do NOT auto-advance to the implementation loop — this command stops after decomposition
- If `audit_enabled`, append a `phase` entry for `tasks` and a `workflow-end` entry on completion

### Step 7: Report

Reference `templates/output-formats.md` for canonical formatting. Surface:

- Feature ID and title
- Task count (new + existing if appended)
- Phase breakdown if the decomposition produced phased tasks
- Path to `tasks.md`
- Next suggested action: "Run `/sigil:draw continue` to start implementation"

## Guidelines

- **Plan required.** This command does not author a plan. If `plan.md` is missing, route the user to `/sigil:draw continue` or instruct them to author one.
- **Non-destructive by default.** Never overwrite a `tasks.md` with completed work without explicit user confirmation.
- **Standalone.** Stops after decomposition. Implementation is the orchestrator's job.
- **Jargon suppression.** Say "breaking down the plan into steps," not "invoking task-decomposer."
