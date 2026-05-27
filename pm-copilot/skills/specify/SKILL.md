---
name: specify
description: Generates a Validated Spec using the 10-section template. Includes persona selection guide, Discovery Design Brief detection, and design ticket triggering when UI gaps are found.
version: 1.0.0
category: pm
chainable: false
invokes: [persona-lookup, scope-check]
invoked_by: [spec-command]
tools: Read, AskUserQuestion
---

# Skill: Specify

## Purpose

Produce a Validated Spec from a feature description using the 10-section template in `references/validated-spec-template.md`. The output is a structured Markdown artifact that the user can paste anywhere.

## When to Invoke

- `/spec "<description>"` (full mode)
- `/spec from-define` (continues from a prior Define output in this session)
- `/spec quick "<description>"` (lightweight mode — only TL;DR, Problem, Scope, Open Questions)

## Inputs

- `description`: string — feature description, or marker `from-define`
- `mode`: `full | quick`

## Process

### Step 1: Load Context

- `references/validated-spec-template.md` — the canonical 10-section structure
- `references/personas.md` — project's defined personas (if present)
- `references/communication-style.md` — tone, output mode (Artifact Mode for this skill)

### Step 2: Persona Selection Guide (FR-C03)

When the feature affects multiple persona types, surface a persona selection block before writing User Journeys:

```
Multiple personas could apply to this feature:

  1. {Persona A} — primarily affected if {scenario}
  2. {Persona B} — primarily affected if {scenario}
  3. {Persona C} — primarily affected if {scenario}

Who is the primary persona? You can list secondary personas too.
```

Use `AskUserQuestion` so the user picks explicitly. Don't assume.

### Step 3: Discovery Design Brief Detection (FR-C03)

A feature is "genuinely novel" when:

- The product has no comparable existing journey (no analog screen, flow, or interaction)
- The problem space requires divergent exploration (multiple plausible directions)
- Existing personas don't cleanly fit

When detected, offer a Discovery Design Brief INSTEAD of jumping to full scenarios:

```
This looks like genuinely novel territory — no comparable existing journey.

Two options:
  1. Draft a Discovery Design Brief (lightweight exploration scaffold)
  2. Proceed with full spec anyway

Discovery briefs let Design + Engineering explore before locking scope.
```

Let the user choose.

### Step 4: Write the Spec

Use the 10-section template from `references/validated-spec-template.md`:

1. TL;DR
2. Problem
3. Success Metrics
4. Scope (with Cut Line — mandatory)
5. User Journeys
6. Scenarios & Business Rules
7. Dependencies
8. Design Context
9. Assumptions
10. Open Questions

**Section-by-section rules:**

- **TL;DR** — 3-5 sentences, plain language, anyone in the company should understand it
- **Problem** — quantify where possible (% affected, $ impact, frequency)
- **Success Metrics** — at least one primary metric with baseline and target
- **Scope** — Cut Line MUST be explicit. Everything above is must-ship; below is nice-to-have. No spec ships without a Cut Line.
- **User Journeys** — use persona names from Step 2. One journey per primary persona minimum.
- **Scenarios** — Given/When/Then format. Each scenario must be testable.
- **Dependencies** — name teams or systems, include status and risk
- **Design Context** — link to existing designs, note constraints. Triggers `/design-ticket` if UI gaps remain
- **Assumptions** — list explicitly. If any are wrong, return to spec
- **Open Questions** — first-class. Each needs an owner and target answer date

### Step 5: Quick Mode

When `mode == quick`:

- Fill only TL;DR, Problem, Scope (above cut line), Open Questions
- Mark Status: `Draft (quick)`
- Surface: "Run `/validate` only if this needs full validation. Quick specs typically skip straight to PO `/receive`."

### Step 6: Design Ticket Detection

After writing Section 8 (Design Context), check for UI gaps:

- Are there mockups for all primary journeys?
- Are accessibility expectations documented?
- Are responsive / platform behaviors defined?

If gaps exist, offer:

```
This spec has unresolved design questions:
  - {Gap}
  - {Gap}

Want to spin up a design ticket?
```

Use `references/design-ticket-template.md`. The ticket is part of the spec's Open Questions until resolved.

### Step 7: Output

Render the full spec as Markdown. Set `Status: Draft`. Surface:

```
Next: Run `/validate` to run the 10-point checklist.
```

## Outputs

- A Markdown Validated Spec (or Quick Spec) artifact, ready to copy/paste
- Optional design ticket draft if UI gaps surfaced

## Anti-patterns

- **No HOW.** Specs describe WHAT and WHY. Implementation choices belong in engineering plans.
- **No phantom personas.** Don't introduce a persona mid-spec that wasn't picked in Step 2.
- **Cut Line is non-negotiable.** Don't ship a spec without one.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-27 | Initial release — S4-001 FR-C03 |
