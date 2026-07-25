---
name: review
description: Review an implementation, run QA, perform code review, perform a distinct security review, or verify deployment readiness. Use for review and validation requests. Report findings and limitations honestly; do not silently implement fixes unless asked.
---

# Review

Determine whether the user wants validation, code review, security review, or
deployment-readiness review. Load only the corresponding section of
`references/review.md`.

Keep code review and security review separate and sequential. Review-oriented
work is read-focused. Lead with concrete findings, distinguish blockers from
suggestions, and include a populated limitations section describing what was
not verified.

Use calibrated language: “no issues found in the areas checked,” never a claim
that software is proven secure. High or critical security findings, review
blockers, and exhausted QA loops trigger the shared safety gate. Do not change
workflow state unless acting as draw’s root coordinator with a validated
artifact and expected state revision.
