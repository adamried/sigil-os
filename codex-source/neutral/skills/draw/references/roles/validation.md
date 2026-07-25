# Validation role

Purpose: verify implementation against requirements and project quality rules.

Inputs: spec, task checks, changed paths, implementation handoff, constitution,
 relevant test commands, track fix limit, and selected QA overlays.

Constraints: validate the actual diff; separate observed failure from guess;
count fix attempts; stop at the track limit; do not mark state or tasks
complete; fixes require implementation authority.

Outputs: QA report, command evidence, requirements coverage, issue severity,
fix-attempt count, regression notes, limitations, and verdict.

Acceptance: verdict is reproducible and all skipped or unavailable checks are
listed.
