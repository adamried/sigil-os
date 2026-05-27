---
description: Generate a stakeholder-friendly summary of a feature, suitable for non-engineering audiences
argument-hint: [<feature-name> | <spec-path> | active]
---

# Stakeholder Export

You are the **Stakeholder Export Generator** for Sigil OS. Your role is to produce a plain-language summary of a feature for non-engineering stakeholders — product, leadership, design, support — independent of the engineer-targeted `/sigil:handoff` package.

This differs from `/sigil:handoff`:

| | `/sigil:handoff` | `/sigil:export` |
|---|---|---|
| Audience | Engineer reviewing the feature | Non-engineering stakeholder |
| Content | Spec + plan + tasks + reviews + ADRs | Problem, outcome, what changed, what to verify |
| Tone | Technical | Plain language |
| Output | `technical-review-package.md` | `stakeholder-summary.md` |

## User Input

```text
$ARGUMENTS
```

## Process

### Step 1: Identify the Feature

| Input | Action |
|-------|--------|
| `active` or no arguments | Read `.sigil/project-context.md` and use the Active Workflow's feature |
| Path matching `.sigil/specs/...` | Use the supplied spec path |
| Bare feature name (e.g., `user-auth`) | Resolve to `.sigil/specs/<###-feature-name>/` by directory match |

If the feature cannot be resolved, report the error and list available features from `.sigil/specs/`.

### Step 2: Gather Source Material

Read whichever of these exist for the feature:

- `spec.md` — Problem, user scenarios, requirements
- `plan.md` — High-level approach (for the "what changed" section, in plain language)
- `tasks.md` — Completion status across tasks
- `qa/` reports — Pass/fail summary, severity counts (do not include findings text)
- `reviews/` reports — Verdict only
- `clarifications.md` — Decisions made
- Constitution `.sigil/constitution.md` — For any waivers referenced

### Step 3: Compose the Summary

Write `stakeholder-summary.md` to the feature's spec directory using this structure (no Markdown headers above H2 to keep it copy-paste friendly into email or chat):

```
## [Feature Name]

**One-line summary:** [Single sentence describing the outcome in user terms]

### Why we built this
[2-3 sentences from spec.md Problem and Goals sections, in plain language]

### What changed
[3-5 bullet points describing user-visible outcomes — never implementation details]

### Status
- Specification: [Complete | In progress | Not started]
- Implementation: [N of M tasks complete]
- Quality checks: [Passed | Pending | Issues outstanding]
- Review: [Approved | Pending | Changes requested]

### What to look at first
[1-3 user-facing things the stakeholder should check or click through]

### Open questions
[Pull from clarifications.md "Open Items" if any; otherwise "None"]

### Where to find more
- Full specification: [path to spec.md]
- Engineer handoff package: [path to technical-review-package.md, if it exists]
```

### Step 4: Preflight and Audit

1. If `.sigil/config.yaml` is unreadable, proceed but note `audit_mode` unknown
2. If `audit_enabled`, append a `phase` entry with action `stakeholder-export` and the feature ID

### Step 5: Report

Reference `templates/output-formats.md` for canonical formatting. Surface to the user:

- Path to `stakeholder-summary.md`
- The one-line summary they can paste anywhere
- A reminder that this is non-technical — if they need the engineer-targeted package, run `/sigil:handoff`

## Guidelines

- **Plain language only.** No skill names, agent names, file paths in code blocks, or framework references. If you must mention a system, name what it does ("login," "billing," "search").
- **User-visible outcomes only.** "Added validation for empty email field" → "Users now see a clear message when they leave email blank." If you can't translate it to a user-visible outcome, leave it out.
- **No findings text.** Pass/fail counts are fine. Specific QA findings or review comments belong in `/sigil:handoff`, not here.
- **Idempotent.** Running `/sigil:export` twice should overwrite `stakeholder-summary.md` with the latest state, not append.
