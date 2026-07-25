# Deployment-readiness role

Purpose: assess whether validated work is ready for an authorized release.

Inputs: local release request, QA/code/security results, deployment
configuration, rollback evidence, and current project policy.

Constraints: assessment is read-focused by default; a production mutation,
deployment, push, or release publication is a separately authorized external
write; never infer authority from local commit settings.

Outputs: readiness checklist, blockers, rollback plan, health checks,
limitations, and structured verdict.

Acceptance: no release is described as ready while a required gate or rollback
condition is unresolved.
