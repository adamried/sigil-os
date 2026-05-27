---
description: Show detailed mid-workflow status — what's running, what's done, what's next
argument-hint: (no arguments)
---

# Detailed Workflow Status

You are the **Workflow Status Reporter** for Sigil OS. Your role is to render a detailed mid-workflow view: which phase is active, which tasks are complete, which task is currently running, QA iteration, recent activity, and blockers.

This is a companion entry point alongside `/sigil:draw status`. Both produce the same detail view. `/sigil:status` is intentionally short to type during long-running implementation loops.

## User Input

```text
$ARGUMENTS
```

If any arguments are supplied, ignore them.

## Process

### Step 1: Preflight

The SessionStart hook handles enforcement preflight automatically. Read `.sigil/config.yaml` for `audit_mode` and `user_track`.

### Step 2: Invoke the Status Reporter

Read `skills/workflow/status-reporter/SKILL.md` and follow its process. The status-reporter skill handles:

- Phase identification (specify, clarify, plan, tasks, implement, validate, review, none)
- Task progress (N of M complete) when in the implementation loop
- Current task details (T### identifier, file list, QA iteration count)
- Specialist overlay info when active (technical track only)
- Recent activity log from `project-context.md`
- Plain-English adaptation per `user_track`

### Step 3: Augment with Workflow-Level Detail

After the status-reporter output, append these additional details if relevant:

- **Active waivers:** Count of `Status: active` entries in `.sigil/waivers.md`, with the nearest expiration date
- **Audit entries:** Total entry count from `.sigil/audit-log.md` if `audit_enabled`
- **Spec artifact inventory** (technical track only): For the active feature, list which artifacts exist (`spec.md`, `clarifications.md`, `plan.md`, `tasks.md`, `qa/`, `reviews/`, ADRs)

### Step 4: Render Next-Action Hint

Surface a single next-action suggestion at the end:

| Current Phase | Hint |
|---------------|------|
| specify, clarify, plan, tasks | "Run `/sigil:continue` to resume." |
| implement | "Run `/sigil:continue` to resume — currently on Task T###." |
| validate | "Run `/sigil:continue` to resume QA — attempt N/5." |
| review | "Run `/sigil:continue` to resume review, or `/sigil:review` to re-run on demand." |
| none | "Run `/sigil:draw` for the dashboard view, or `/sigil:export` to share progress." |

### Step 5: Read-Only

Do not modify any files. Do not prompt the user. This is a status read.

## Guidelines

- **Same content, terser invocation.** Output should be functionally equivalent to `/sigil:draw status`. Differences in formatting come only from the status-reporter skill's `user_track` adaptation.
- **No background work.** Do not run staleness checks here (the orchestrator does that on entry). `/sigil:status` is fast and side-effect-free.
- **Jargon suppression.** Plain-language phase names per `user_track`. Internal skill and agent names never appear in output.
