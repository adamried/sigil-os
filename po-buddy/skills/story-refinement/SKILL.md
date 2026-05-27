---
name: story-refinement
description: Improve existing stories against team format standards. Quality checklist, format compliance check, refinement-vs-rewrite decision logic (refine if salvageable; rewrite if format is too far off).
version: 1.0.0
category: po
chainable: false
invokes: [persona-lookup]
invoked_by: [story-refinement-command]
tools: Read, AskUserQuestion
---

# Skill: Story Refinement

## Purpose

Improve an existing story (one the user pastes in, or one from a backlog) so it meets the project's story format and quality standards. Decide whether to refine in place or rewrite from scratch.

## When to Invoke

- User pastes in an existing story and asks to improve / refine / clean up
- User says "review this story" or "fix this story"

## Inputs

- `story_content`: the existing story (paste-in or path)

## Process

### Step 1: Load Format Standards

Read `references/story-formats.md` (or the built-in default — same as `quick-story` Step 1).

### Step 2: Format Compliance Check

Compare the existing story to the configured format. Score each:

| Check | Pass / Fail |
|-------|-------------|
| Title follows `[Label] - {Title}` pattern | |
| "As a / I want / So that" present | |
| Acceptance Criteria use GIVEN/WHEN/THEN | |
| Exactly one Backend/Web/Mobile label | |
| One persona named | |
| No HOW (no class names, endpoint paths, library mentions) | |
| Implementation hints in Notes, not in AC | |

### Step 3: Quality Checklist

Beyond format, score quality:

| Check | Pass / Fail |
|-------|-------------|
| Persona is from `references/personas.md` | |
| Outcome (the "so that") is user-observable, not internal | |
| Acceptance criteria are testable (observable state changes) | |
| At least one scenario covers the happy path | |
| Edge cases or error states acknowledged (in Notes or AC) | |

### Step 4: Refine vs Rewrite Decision

| Score | Action |
|-------|--------|
| 0–2 fails | **Refine in place** — apply targeted edits |
| 3–5 fails | **Refine or rewrite** — ask the user (some salvageable structure exists) |
| 6+ fails | **Rewrite** — too many fundamental issues; start fresh from the user's intent |

For "Refine or rewrite," surface via `AskUserQuestion`:

```
This story has {N} format/quality issues — borderline between refine and rewrite.

  1. Refine in place — I'll edit the existing structure
  2. Rewrite from scratch — I'll capture the intent and start fresh
  3. Show me the specific issues first, then I'll decide
```

### Step 5: Apply Refinement OR Rewrite

For refine: produce a diff-style view showing edits. Confirm with user before finalizing.

For rewrite: invoke `quick-story` with the captured intent.

### Step 6: Output

```
Story Refinement: {Original Title}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Format compliance: {N/7 passed}
Quality checklist:  {N/5 passed}
Action:             {Refined in place | Rewritten}

{Refined or rewritten story}

Changes made:
  - {Edit}
  - {Edit}
```

## Outputs

A refined or rewritten story matching the project's format standards.

## Anti-patterns

- **Refining beyond the user's intent.** Don't expand scope. Don't add new acceptance criteria the original didn't imply.
- **Rewriting silently.** If you're rewriting, say so — the user might prefer refine.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-27 | Initial release — S4-001 FR-C21 |
