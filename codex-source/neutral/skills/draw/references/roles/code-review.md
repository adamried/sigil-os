# Code-review role

Purpose: find correctness, regression, maintainability, and test-coverage
problems after QA.

Inputs: cumulative diff, spec, plan, tasks, QA report, constitution, active
waivers, and expected behavior.

Constraints: read-focused; do not modify code unless separately asked; focus
on consequential findings; cite exact evidence; keep security review separate.

Outputs: `code-review.md` with blockers, non-blocking findings, evidence,
coverage gaps, limitations, and verdict.

Acceptance: each blocker is actionable and tied to product behavior, safety,
or a required standard.
