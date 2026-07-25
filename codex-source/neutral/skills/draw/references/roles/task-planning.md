# Task-planning role

Purpose: decompose an approved plan into independently verifiable work.

Inputs: validated spec, plan, design output, decision records, repository
evidence, track limits, and expected state revision.

Constraints: every task has explicit scope, dependencies, paths, and
acceptance checks; identify disjoint work without assuming parallel support;
do not exceed five tasks in Quick Flow without a user decision.

Outputs: `tasks.md`, dependency order, per-task file scopes, acceptance checks,
parallel-safe groups, and handoff.

Acceptance: no task requires hidden context and no overlapping task is marked
safe for concurrent edits.
