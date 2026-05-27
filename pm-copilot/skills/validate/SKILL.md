---
name: validate
description: 10-point validation checklist for a Validated Spec. Includes adversarial Villain Check. Promotes spec to Validated status on full pass, or returns specific revision feedback. Max 3 rounds.
version: 1.0.0
category: pm
chainable: false
invokes: [persona-lookup]
invoked_by: [validate-command]
tools: Read, AskUserQuestion
---

# Skill: Validate

## Purpose

Run a structured 10-point validation against a draft Validated Spec, plus an adversarial Villain Check. Either promote the spec to `Validated` or return it with specific feedback. Cap iteration at 3 rounds.

## When to Invoke

- `/validate <spec-id>`
- `/validate` (uses most recent Draft spec)

## Inputs

- `spec_path` or `spec_content`: the Draft Validated Spec
- `round_counter`: integer (incremented by caller; starts at 1)

## Process

### Step 1: 10-Point Checklist (Promotion Rule — must pass ALL 10)

Score each as Pass / Fail with specific reasoning when Fail.

| # | Check | Pass Criteria |
|---|-------|---------------|
| 1 | **Problem clarity** | One paragraph, clearly states user / business pain, not a solution |
| 2 | **Quantified impact** | At least one quantitative measure (% affected, $ impact, frequency, count) |
| 3 | **Success metrics** | At least one primary metric with baseline + target + measurement source |
| 4 | **Cut Line explicit** | Section 4 has a clear above/below the cut line split |
| 5 | **Personas present** | At least one named persona; multi-persona features distinguish primary vs. secondary |
| 6 | **Journey completeness** | Each primary persona has a journey covering trigger → outcome |
| 7 | **Scenarios testable** | Given/When/Then format; outcomes are observable |
| 8 | **Dependencies named** | All known external dependencies listed with status and risk |
| 9 | **Design context honest** | Either references existing designs OR opens a design ticket — no hand-waving |
| 10 | **Open questions tracked** | Each open question has an owner and target answer date |

### Step 2: Villain Check (FR-C04)

An adversarial check that stress-tests the happy path. The Villain Check was introduced during `/spec` journey work (FR-C04) — by `/validate` time, it should be a confirmation, not a first encounter.

Pick the most plausible adversarial scenario:

- **Adversarial user:** A bad actor or unhappy customer takes the journey
- **Edge case:** A non-default state (offline, slow network, accessibility tooling active)
- **Failure mode:** A dependency fails partway through

For the chosen scenario, walk through the journeys in Section 5. If any journey breaks, list:

- Which journey
- Where it breaks
- What the spec is missing (a scenario, a business rule, an open question)

Villain Check passes if no journey breaks OR if all breaks are covered by explicit Open Questions.

### Step 3: Verdict

| Verdict | Trigger | Action |
|---------|---------|--------|
| **Promote** | All 10 pass AND Villain Check passes | Update spec `Status: Validated`. Surface: "Run `/handoff` to package for engineering." |
| **Revise** | Any of 10 fails OR Villain Check finds an uncovered break | Return checklist with Fail details. Round counter increments. |
| **Escalate** | `round_counter >= 3` | Stop iterating. Present structured "what's blocking" summary. |

### Step 4: Escalation (after 3 rounds)

When 3 rounds fail to promote:

```
Escalation: 3 validation rounds without promotion
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Persistent gaps:
  - {Check that keeps failing}: {what's wrong}
  - {Check that keeps failing}: {what's wrong}

Options:
  1. Narrow scope — reduce ambition so the gaps become non-applicable
  2. Open these as known unknowns in the Open Questions section, and ship
     a spec that acknowledges them
  3. Park the spec — return when you have answers

Your call.
```

Use `AskUserQuestion`. Don't pick for them.

## Outputs

```json
{
  "verdict": "Promote | Revise | Escalate",
  "round": 1,
  "checklist": [
    {"check": "Problem clarity", "result": "Pass", "note": ""},
    {"check": "Cut Line explicit", "result": "Fail", "note": "Section 4 has no explicit cut line — all items appear above"}
  ],
  "villain_check": {"result": "Pass | Fail", "scenario": "...", "breaks": []},
  "next_step": "..."
}
```

## Anti-patterns

- **Vague feedback.** "Section 4 is weak" — say specifically what's missing.
- **Auto-promoting on Villain doubt.** If you can't confidently say a journey holds up, mark Villain `Fail` with the specific concern.
- **More than 3 rounds.** The cap exists to force decision-making — don't sneak a 4th round through.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-27 | Initial release — S4-001 FR-C04 |
