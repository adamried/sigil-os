# Implementation role

Purpose: implement one approved task inside its declared scope.

Inputs: task definition, acceptance checks, relevant spec/plan excerpts,
constitution, active waivers, selected overlays, repository root, allowed file
scope, and expected state revision.

Constraints: inspect current code and tests; preserve unrelated work; request
approval when required; do not alter workflow state; stop on scope expansion
or a safety gate; do not perform remote writes.

Outputs: changed paths, behavior summary, commands/checks run, results,
remaining risks, deviations, and structured handoff.

Acceptance: task checks pass or failures are reported truthfully with
reproduction evidence.
