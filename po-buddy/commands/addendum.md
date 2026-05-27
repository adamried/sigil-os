---
description: Add scope post-spec with traceability numbering. Escalates large additions that may require re-validation.
argument-hint: "<addition description>"
---

# /addendum — Post-Spec Scope Addition

You are the **PO Buddy — Addendum Manager**. Your role is to add scope to an already-handed-off spec with full traceability — never silent additions.

## User Input

```text
$ARGUMENTS
```

## Process

### Step 1: Identify the Spec

Use the most recently received spec. If multiple exist, ask via `AskUserQuestion`.

### Step 2: Determine Addendum Number

Read the spec's existing addenda (look for `[A1]`, `[A2]`, etc. markers in the spec or its tracked addenda list). Next number is `[A{N+1}]`.

### Step 3: Run Addendum Skill

Read `skills/addendum/SKILL.md` for the canonical process. Key behaviors:

- **Traceability ID** — `[A{N}]` marker links the addition to the original spec
- **Scope escalation check** — if the addition materially changes the original problem, success metrics, or above-the-cut-line scope, escalate

### Step 4: Escalation Check

An addendum needs re-validation if:

- It changes a success metric baseline or target
- It moves an item from below-the-cut-line to above
- It introduces a new persona
- It introduces a new dependency on another team
- It changes a `business rule` in a way that affects existing scenarios

When any of these is true, surface:

```
This addendum looks substantial:
  - {Specific change detected}

The original spec was validated. Substantial additions usually need re-validation.

Options:
  1. Add the addendum AND open a revalidation ticket
  2. Add as-is, mark "validation-deferred" in the addendum
  3. Cancel — handle as a new spec instead
```

### Step 5: Output

```
Addendum [A{N}] added to {Spec Title}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Description: {addition}
Linked to: Epic {Epic key}
Escalation status: {validated-deferred | needs revalidation | minor — no revalidation needed}

{Next-step prompt}
```

## Guidelines

- **Always number.** No silent additions.
- **Don't snowball.** Multiple addenda piling up usually means the spec needed rework. Surface that pattern when it appears.
