---
name: business-case
description: Generates a Business Case document for Complex-track initiatives (from /define triage). Uses the generalized business-case template with Executive Summary, Problem, Solution, Investment, Risks, Alternatives, Recommendation sections.
version: 1.0.0
category: pm
chainable: false
invokes: []
invoked_by: [define-command]
tools: Read, AskUserQuestion
---

# Skill: Business Case

## Purpose

Produce a Business Case for Complex-track initiatives — features large enough to warrant explicit investment analysis before spec work begins. Uses `references/business-case-template.md`.

## When to Invoke

- `/define` triage returns Complex
- User says "make the business case" or "I need to justify this to leadership"

## Inputs

- `define_output`: the prior `/define` output (problem statement + triage rationale)

## Process

### Step 1: Load Template

Read `references/business-case-template.md`. All sections are populated through targeted user input.

### Step 2: Walk Through Sections

For each section, ask 1–2 focused questions, then write the section. Use `AskUserQuestion` to keep input bounded.

**Section walk-through:**

1. **Executive Summary** — written last (depends on remaining sections), but show a placeholder
2. **Problem** — pre-populated from `/define` output; user confirms or refines
3. **Solution** — what we're proposing, in plain language. Ask: "What are the 2–3 key capabilities?"
4. **Business Impact** — Ask: "Quantified benefits (revenue, cost saving, retention)?" + "Qualitative benefits?"
5. **Investment** — Ask: "Engineering / design / other cost estimate?" + "Headcount needs?"
6. **Risks** — Ask: "What's the single biggest risk?" + "Other notable risks?"
7. **Alternatives Considered** — Ask: "Why not do nothing?" + "What other approaches did you consider?"
8. **Recommendation** — Compose based on the above; user confirms
9. **Executive Summary** — Write last, derived from the above

### Step 3: Quantification Rules

- **Estimates are explicitly labeled.** Use ranges or confidence tiers (High / Med / Low confidence) when exact figures aren't available.
- **Don't fabricate numbers.** If the user doesn't have a quantified benefit, write "Qualitative only — pending data" rather than inventing one.

### Step 4: Output

Render the full Business Case as Markdown. Surface next steps:

```
Next steps:
  1. Share with leadership / stakeholders for decision
  2. If approved, run `/spec from-define` to write the Validated Spec
  3. If declined, archive — don't proceed to spec
```

## Outputs

- A Markdown Business Case document, ready to share

## Anti-patterns

- **Fabricated numbers.** Don't make up ROI figures. Qualitative + "pending data" is better than fake quantification.
- **Solution disguised as problem.** The Problem section restates the `/define` problem, not the proposed solution.
- **Dropping Alternatives Considered.** Always include "Do nothing" — it forces the cost-of-inaction analysis.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-27 | Initial release — S4-001 FR-C07 |
