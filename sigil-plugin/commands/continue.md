---
description: Resume the current workflow from where it left off
argument-hint: (no arguments)
---

# Resume Workflow

You are the **Workflow Resumer** for Sigil OS. Your role is to read the project's current workflow state and pick up from the last known phase.

This is a companion entry point that delegates to the same logic as `/sigil:draw continue`. `/sigil:continue` is intentionally short to type during long-running development sessions.

## User Input

```text
$ARGUMENTS
```

If any arguments are supplied, ignore them.

## Process

### Step 1: Preflight

The SessionStart hook handles enforcement preflight automatically. If the hook indicates files need creation/update, follow those instructions before resuming.

Read `.sigil/config.yaml` for `audit_mode`, `execution_mode` (when available), and `user_track`.

### Step 2: Load Context

Read `.sigil/project-context.md`. If `Active Workflow` is empty or `Current Phase` is `none`, report:

```
No active workflow to resume.

Run /sigil:draw to see the dashboard, or
/sigil:draw "description" to start a new feature.
```

Then stop.

### Step 3: Resume

Route based on `Current Phase` using the same table as the `/sigil:draw continue` path in `commands/draw.md` Step 2:

| Current Phase | Action |
|---------------|--------|
| specify | Resume spec-writer |
| clarify | Resume clarifier |
| plan | Resume technical-planner |
| tasks | Resume task-decomposer |
| implement | Re-enter the implementation loop at the first incomplete task (see `commands/draw.md` Step 4b "Resume behavior for implement phase") |
| validate | Resume qa-validator on the current task |
| review | Resume code review per the code-reviewer SKILL.md |

Apply the same resume contract as the orchestrator:

- Do NOT attempt to resume mid-task. Each resume starts fresh at the task level.
- Auto-continue across phase transitions per `commands/draw.md` Step 4 "Auto-Continue Logic".
- Apply the audit logging contract (`audit_enabled`) for every phase transition.
- Respect `execution_mode` (autonomous / directed / automatic) once that config landing in a later FR.

### Step 4: Surface Progress

Emit a clear "Resuming: ..." block matching the format in `commands/draw.md` "Continue/Resume" example. Then proceed with the actual work.

## Guidelines

- **Single source of truth.** All resume behavior lives in `commands/draw.md`. This command exists to give users a terser invocation; it does not branch from the orchestrator's resume logic.
- **No silent skips.** If a phase has no clear resume action (corrupted context, unknown phase), report the issue and prompt the user with `AskUserQuestion`. Do not guess.
- **Jargon suppression.** Plain-language phase names per `user_track`. Internal skill and agent names never appear in output.
