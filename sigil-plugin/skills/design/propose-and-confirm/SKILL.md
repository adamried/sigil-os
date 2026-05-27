---
name: propose-and-confirm
description: Manages end-of-task design-drift patches. Surfaces unified diffs via AskUserQuestion with Accept/Reject/Edit options. design.md is never auto-edited. Autonomous-mode batches patches for end-of-run review.
version: 1.0.0
category: design
chainable: false
invokes: []
invoked_by: [uiux-designer, developer, frontend-developer]
tools: Read, Write, Edit, AskUserQuestion
---

# Skill: Propose-and-Confirm

## Purpose

When an agent observes design drift during a UI task — new tokens, new components, new patterns not in `.sigil/design.md` — present a unified diff via `AskUserQuestion` at end-of-task. User accepts (writes to design.md), rejects (drops to `.sigil/tech-debt.md`), or edits the patch first.

**Critical:** design.md is NEVER auto-edited (FR-H03). Even on Accept, render the final diff for one last confirmation before write.

## When to Invoke

- UI/UX Designer Step 8.5 (before handoff to Architect)
- Developer Step 6.5 (before handoff to QA)
- frontend-developer specialist inheriting the same gates
- End-of-run batch review when `execution_mode: autonomous` (FR-H04)

## Inputs

- `observations`: array of drift items the agent observed during the task
- `task_context`: which task / spec / feature this is for
- `mode`: `interactive | batch` (batch == autonomous queueing)

## Process

### Step 1: Format the Patch

For each observation, build a structured patch entry:

```
{
  "kind": "token | component | pattern",
  "section": "<which section of design.md is affected>",
  "change_type": "add | update | remove",
  "before": "<current state in design.md, or null if new>",
  "after": "<proposed state>",
  "rationale": "<why the agent observed this>",
  "source_task": "<task ID>"
}
```

### Step 2: Build the Unified Diff View

For human review, render as a Markdown patch:

```markdown
## Design Drift Detected — {task ID}

The agent observed N changes during this task that aren't yet in `.sigil/design.md`:

### Change 1: New token (color.brand-accent)

**Section 2 — Color System**

```diff
  | secondary | #5B8DEF | Secondary CTAs, accents |
+ | brand-accent | #FF6B35 | Highlight color introduced for callouts |
```

**Rationale:** The task introduced a callout component requiring a new accent hue distinct from secondary.

### Change 2: New component (CalloutBanner)

**Section 5 — Component Inventory**

```diff
+ | CalloutBanner | `src/components/CalloutBanner.tsx` | Highlight box; uses brand-accent token |
```

### Change 3: Layout pattern (sticky bottom CTA)

**Section 6 — Layout Patterns**

```diff
+ - Sticky bottom CTA pattern: full-width primary button anchored at bottom of mobile screens, respecting safe-area-inset
```
```

### Step 3: Interactive Mode

When `mode: interactive` (default for `automatic` and `directed` execution modes), surface via `AskUserQuestion`:

```
What should I do with these N changes?

  1. Accept all — append to design.md (you'll see a final diff before write)
  2. Reject all — drop to .sigil/tech-debt.md as deferred design debt
  3. Edit first — let me modify the patch before deciding
  4. Pick per-change (show me one at a time)
```

#### Accept path

1. Render the **final unified diff** that will be applied to design.md.
2. Final confirmation: "Apply? (Yes / Cancel)".
3. On Yes: apply the diff. Append an entry to the Revision History:
   ```
   | {YYYY-MM-DD} | Propose-and-confirm | Accepted N changes from task {ID}: brief summary |
   ```
4. On Cancel: drop to .sigil/tech-debt.md (same as Reject path).

#### Reject path

1. Append to `.sigil/tech-debt.md` (create lazily on first rejection):
   ```markdown
   ## {YYYY-MM-DD} — Design drift rejected from task {ID}

   The following observations were surfaced but not adopted into design.md:

   {patch content}

   **Reason for rejection:** {if the user provided one — optional}
   ```
2. Confirm to user: "Saved to .sigil/tech-debt.md. design.md unchanged."

#### Edit path

Present the patch in an editable view. After user edits, return to Step 3 with the modified patch.

#### Pick per-change path

Loop through each change, asking Accept / Reject / Edit for each.

### Step 4: Batch Mode (Autonomous — FR-H04)

When `mode: batch` (caller is in `execution_mode: autonomous`):

1. Do NOT prompt inline.
2. Append the patch (as a JSON object) to a workflow-state file: `.sigil/.autonomous-patches.json`.
3. Return silently. The orchestrator's end-of-run cumulative-diff review (S4-001 FR-A01 Step 0b) reads this file and presents the batch alongside other autonomous-mode review items.

### Step 5: design.md Write Guard (FR-H03)

**Pre-write contract:** Before writing to `.sigil/design.md`, verify the caller is one of:

- `setup` (initial generation)
- `design-md-generator` skill (regeneration via `/sigil:design`)
- This skill (`propose-and-confirm`) with an explicit user Accept

If the caller doesn't match, abort with an error: "design.md write rejected — no authorized path."

A linter rule (S4-002 verification work) should grep for direct writes to `.sigil/design.md` from any other skill or agent and fail the build if found.

## Outputs

- A patched `.sigil/design.md` (if Accepted), OR
- A `.sigil/tech-debt.md` entry (if Rejected, or if Accept was cancelled at the final-diff confirmation), OR
- A queued entry in `.sigil/.autonomous-patches.json` (if batch mode)

## Anti-patterns

- **Auto-applying patches.** No exceptions. Even Accept requires a final-diff confirmation.
- **Skipping the final diff in interactive mode.** The user sees the exact write before it lands.
- **Treating tech-debt.md as dead.** When the user later runs `/sigil:design`, surface pending rejections from tech-debt.md as a reminder.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-27 | Initial release — S4-002 FR-H01..H04 |
