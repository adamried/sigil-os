---
name: define
description: Problem articulation and complexity triage. Validates that a problem statement is problem-shaped (not solution-shaped), refines it through targeted clarification, and triages to Light / Standard / Complex.
version: 1.0.0
category: pm
chainable: false
invokes: [persona-lookup]
invoked_by: [define-command]
tools: Read, AskUserQuestion
---

# Skill: Define

## Purpose

Help a PM articulate a problem precisely enough to spec it (or decide it doesn't need a spec). Triage the result to one of three downstream tracks.

## When to Invoke

- `/define <description>`
- User says "I want to add X" without explaining the problem
- User asks "should this be a feature?"

## Inputs

- `description`: string — Raw problem or initiative description from the user

## Process

### Step 1: Detect Solution-Shape

A problem-shaped input describes a user pain or business pain. A solution-shaped input names a feature, technology, or UI.

Heuristics for solution-shape:
- Names a specific feature ("a chatbot," "a dashboard," "an integration")
- Names a technology ("use OpenAI," "build in React Native")
- Names a UI element ("a modal," "a sidebar")

If solution-shaped → push back once with a specific question:

```
"{Feature/tech name}" is a solution. What user problem does it solve?

For example: "Customers can't get answers after hours" is a problem.
"A 24/7 chatbot" is a solution.
```

If the user pushes back ("I just want the feature, not a problem") — honor it and proceed, but tag the spec with `solution_first: true` so downstream skills know.

### Step 2: Targeted Clarification (max 3 turns)

Ask up to 3 clarifying questions, one at a time, using `AskUserQuestion`:

1. **Who is affected?** (persona, segment, count if known)
2. **How often does this happen?** (frequency, criticality)
3. **What's the cost of doing nothing?** (impact)

Skip any question the user already answered. After 3 turns, stop — summarize what you have and move to triage.

### Step 3: Refine Problem Statement

Compose a 1–2 sentence problem statement using the user's words where possible:

```
{Affected population} cannot {desired outcome} because {current barrier},
which results in {observable cost}.
```

### Step 4: Triage

Score the problem against three axes (Low / Medium / High):

| Axis | Light | Standard | Complex |
|------|-------|----------|---------|
| **Scope** | Single feature, single team | Multi-feature, single team | Cross-team / cross-product |
| **Ambiguity** | Solution is obvious | Solution requires design exploration | Solution requires research, ADRs, and trade-off analysis |
| **Risk** | Low business / user risk | Moderate risk | Material business or compliance risk |

Triage by dominant signal:

- Any High → **Complex**
- All Low → **Light**
- Anything in between → **Standard**

### Step 5: Output

```json
{
  "problem_statement": "...",
  "triage": "Light | Standard | Complex",
  "rationale": ["...", "..."],
  "next_step_recommendation": "/spec quick \"...\" | /spec \"...\" | /business-case ..."
}
```

The command file (`commands/define.md`) renders this for the user.

## Outputs

- Problem statement (refined)
- Triage verdict
- Next-step recommendation

## Anti-patterns

- **Don't lecture about problem vs solution.** One push-back, then move on.
- **Don't ask all 3 clarifying questions at once.** One at a time, with `AskUserQuestion`.
- **Don't auto-promote to `/spec`.** The user invokes the next command.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-27 | Initial release — S4-001 FR-C02 |
