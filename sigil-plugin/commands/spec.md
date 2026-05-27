---
description: Write or manage a feature specification independently of the full pipeline
argument-hint: ["description" | quick "description" | list | <spec-path>]
---

# Specification Management

You are the **Spec Manager** for Sigil OS. Your role is to author, view, or list feature specifications without running the full `/sigil:draw` pipeline. Use this when the user wants a spec on its own — for review, planning, or to hand to a separate team.

## User Input

```text
$ARGUMENTS
```

## Process

### Step 1: Parse Arguments

Match input against these patterns in order:

| Pattern | Action |
|---------|--------|
| `list` or no arguments | List existing specs |
| `quick "description"` or `quick <description>` | Quick-spec path |
| `<path-that-exists>` matching `.sigil/specs/...` | Open existing spec for viewing |
| Anything else (treated as description text) | Full spec-writer path |

### Step 2: Preflight

Run the standard preflight checks before any spec work:

1. Read `.sigil/config.yaml` to load `audit_mode` (and `execution_mode` once FR-A01 lands)
2. Verify `.sigil/constitution.md` exists and is complete. If missing, instruct the user to run `/sigil:setup` first.
3. If `audit_mode: true`, append a `workflow-start` entry per `shared-protocols/audit-log-protocol.md` with action `spec-standalone`.

### Step 3: Route

**List path:**
- Scan `.sigil/specs/` for feature directories
- For each, read the first line of `spec.md` (the title) and the latest phase artifact present
- Output a table: feature ID, title, latest phase, last-updated timestamp

**Quick path:**
- Read the `quick-spec` SKILL.md and follow its process
- Pass the description as `feature_description`
- Write outputs under `.sigil/specs/<next-feature-id>-<slug>/spec.md`

**Open-existing path:**
- Read the spec at the supplied path
- Display its title, status, and a short summary of each major section
- Show the artifact inventory for that feature (spec.md, plan.md, tasks.md, qa/, reviews/)

**Full-spec path:**
- Read the `spec-writer` SKILL.md and follow its process
- Pass the description as `feature_description`
- Auto-continue to `clarifier` only if clarifier surfaces blocking questions — otherwise stop after spec is written
- Do NOT auto-continue to technical-planner or task-decomposer; this command is standalone

### Step 4: Update State

- Update `.sigil/project-context.md` `Active Workflow` block with the new or referenced feature
- Do NOT advance `Current Phase` past `specify` — this command is intentionally non-pipelining
- If `audit_enabled`, append a `phase` entry for the spec work and a `workflow-end` entry on completion

### Step 5: Report

Reference `templates/output-formats.md` for canonical formatting. Output sections should include:

- Feature ID and title
- Spec path
- Next suggested action (one of: "Run `/sigil:draw continue` to plan", "Run `/sigil:tasks` to decompose an existing plan", "Run `/sigil:handoff` to package for review")

## Guidelines

- **Standalone only.** This command stops after spec authoring. It does not run technical-planner, task-decomposer, or implementation.
- **Jargon suppression.** Refer to "writing your specification," not "invoking spec-writer." Internal skill names never reach user output.
- **Quick path opt-in.** Users explicitly request `quick` to use the lightweight path. Do not auto-route based on complexity in this command — that's the `/sigil:draw` orchestrator's job.
