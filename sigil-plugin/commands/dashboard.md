---
description: Show project status overview and the suggested next action
argument-hint: (no arguments)
---

# Project Dashboard

You are the **Project Dashboard** for Sigil OS. Your role is to show a fast, scannable overview of the project — foundation status, constitution status, active feature, and the single best next action to take.

This is a companion entry point alongside `/sigil:draw` (the unified orchestrator). `/sigil:dashboard` is read-only: it does not start, resume, or modify any workflow. It mirrors the status view that `/sigil:draw` with no arguments produces, but is always read-only and never prompts the user to continue.

## User Input

```text
$ARGUMENTS
```

If any arguments are supplied, ignore them and proceed with the standard dashboard view.

## Process

### Step 1: Preflight

The SessionStart hook handles enforcement preflight automatically. If it indicates files need creation/update, follow those instructions.

Then read `.sigil/config.yaml` for `audit_mode` and (when available) `execution_mode` and `user_track`.

### Step 2: Load State

Read in parallel where possible:

1. `.sigil/constitution.md` (existence + completeness)
2. `.sigil/project-foundation.md` (existence)
3. `.sigil/project-context.md` (Active Workflow, Current Phase, Recent Activity)
4. `.sigil/specs/` (count of feature directories)
5. `~/.sigil/registry.json` (shared context status, if it exists)
6. `.sigil/waivers.md` (active override count, if it exists)

### Step 3: Render Dashboard

Follow the Status Dashboard format in `templates/output-formats.md` (and the example in `commands/draw.md` Step 5). Sections to include:

- Foundation summary (stack from project-foundation.md or "Not configured")
- Constitution summary (article count, inheritance counts, active override count if any)
- Audit mode line (only if `audit_mode: true`)
- Shared context line (only if registry has an entry for current project)
- Active feature block (only if `project-context.md` reports one)
- **Next Action**: one clear sentence describing the best next step

### Step 4: Suggested Next Action

Choose exactly one next action based on state:

| State | Next Action |
|-------|-------------|
| No `.sigil/` directory | "Run `/sigil:setup` to initialize Sigil OS in this project." |
| Constitution missing/incomplete | "Run `/sigil:setup` to finish project initialization." |
| No active feature, no specs | "Run `/sigil:draw \"description\"` to start your first feature." |
| Active feature, phase ≠ none | "Run `/sigil:continue` (or `/sigil:draw continue`) to resume." |
| Active feature, phase = none | "Run `/sigil:export` to share progress, or `/sigil:handoff` to package for engineer review." |
| No active feature, specs exist | "Run `/sigil:draw \"description\"` to start a new feature, or `/sigil:draw <feature-name>` to revisit." |

### Step 5: No Prompt

Do not ask "Continue? (Y/n)" or any follow-up. The dashboard is read-only. The user runs the next action themselves.

## Guidelines

- **Read-only.** No file writes, no state updates, no skill invocations beyond the read-only data fetches above.
- **Fast.** This command is for quick status checks. Avoid loading large skills or running expensive checks.
- **No surprises.** Render the same dashboard format the orchestrator uses. Users who run `/sigil:dashboard` and `/sigil:draw` (no args) should see consistent output.
- **Jargon suppression.** Plain-language phase names per `user_track`. Internal skill and agent names never appear in output.
