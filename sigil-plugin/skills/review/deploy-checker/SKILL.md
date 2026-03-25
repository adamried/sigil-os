---
name: deploy-checker
description: Validate deployment readiness for target environment. Invoke before deployment to ensure all gates are passed.
version: 1.0.0
category: review
chainable: true
invokes: []
invoked_by: [devops, orchestrator]
tools: Read, Bash, Glob, Grep
---

# Skill: Deploy Checker

## Purpose

Validate that changes are ready for deployment to the target environment. This skill is the final gate before deployment, ensuring all quality checks have passed, reviews are complete, and the deployment has proper safeguards in place.

## When to Invoke

- After security-reviewer completes
- User requests `/deploy-check` or "check deployment readiness"
- Before deploying to any environment
- As part of CI/CD pipeline gate

## Inputs

**Required:**
```json
{
  "spec_path": "/.sigil/specs/001-feature/spec.md",
  "target_environment": "development | staging | production"
}
```

**Optional:**
```json
{
  "validation_report": "/.sigil/specs/001-feature/qa/validation.md",
  "review_reports": [
    "/.sigil/specs/001-feature/reviews/code-review.md",
    "/.sigil/specs/001-feature/reviews/security-review.md"
  ],
  "has_migrations": true,
  "migration_files": ["migrations/001_add_users.sql"],
  "feature_flags": ["feature_new_auth"],
  "rollback_plan": "/.sigil/specs/001-feature/rollback.md"
}
```

**Auto-loaded:**
- Constitution (for deployment requirements)
- CI/CD configuration
- Environment configuration

## Outputs

**Primary Output:**
```json
{
  "status": "ready | blocked | conditional",
  "environment": "production",
  "timestamp": "2025-01-14T10:30:00Z",
  "checklist": [
    {
      "item": "qa_validation",
      "status": "pass | fail | skip | pending",
      "details": "All tests passing",
      "required": true
    },
    {
      "item": "code_review",
      "status": "pass",
      "details": "Approved with no blockers",
      "required": true
    },
    {
      "item": "security_review",
      "status": "pass",
      "details": "No vulnerabilities found",
      "required": true
    },
    {
      "item": "migrations_valid",
      "status": "pass",
      "details": "1 migration, reversible",
      "required": true
    },
    {
      "item": "rollback_plan",
      "status": "missing",
      "details": "No rollback plan found",
      "required": false
    }
  ],
  "blocking_items": [],
  "warnings": [
    "Rollback plan missing — recommended for production"
  ],
  "deploy_recommendation": "proceed | defer | block",
  "approval_required": true,
  "approval_tier": "review | approve"
}
```

**Artifact Output:** `/.sigil/specs/###-feature/reviews/deploy-readiness.md`

## Readiness Checklist

### 1. QA Validation (Required)

**Check:** qa-validator passed all checks

**Verify:**
- All tests passing
- No lint errors
- Type checks clean
- Coverage meets threshold

**Source:** `/.sigil/specs/###-feature/qa/validation.md`

### 2. Code Review (Required)

**Check:** code-reviewer approved

**Verify:**
- No blocking findings
- Warnings acknowledged or addressed
- Constitution compliance confirmed

**Source:** `/.sigil/specs/###-feature/reviews/code-review.md`

### 3. Security Review (Required for production)

**Check:** security-reviewer approved

**Verify:**
- No high/critical vulnerabilities
- Dependencies audited
- Constitution Article 4 compliant

**Source:** `/.sigil/specs/###-feature/reviews/security-review.md`

### 4. Database Migrations (If applicable)

**Check:** Migrations are valid and reversible

**Verify:**
- Migration files exist and parse correctly
- Migrations are reversible (down migration exists)
- No destructive operations without explicit approval
- Migration order is correct

**Commands:**
```bash
# Validate migration syntax
npm run db:migrate:check

# Test migration in staging
npm run db:migrate:dry-run
```

### 5. Environment Configuration

**Check:** All required env vars documented

**Verify:**
- New env vars listed in .env.example
- Secrets not in code
- Environment-specific configs identified

**Files to Check:**
- `.env.example`
- `config/` directory
- CI/CD environment definitions

### 6. Feature Flags (If applicable)

**Check:** Feature flags configured for target environment

**Verify:**
- Flag exists in configuration
- Default state documented
- Rollout plan defined (if gradual)

### 7. Rollback Plan (Recommended for production)

**Check:** Rollback procedure documented

**Verify:**
- Steps to revert code changes
- Database rollback procedure (if migrations)
- Feature flag disable procedure
- Verification steps post-rollback

### 8. Monitoring & Alerting

**Check:** Observability configured

**Verify:**
- Error tracking active
- Key metrics identified
- Alerts configured for failures
- Dashboard updated (if applicable)

### 9. Documentation

**Check:** User-facing changes documented

**Verify:**
- README updated (if applicable)
- API documentation updated (if applicable)
- Changelog entry added

## Deploy Readiness Report Template

```markdown
# Deploy Readiness Report

**Feature:** [Feature Name]
**Environment:** [Target]
**Date:** [Timestamp]
**Status:** [READY | BLOCKED | CONDITIONAL]

## Checklist

| Item | Status | Required | Details |
|------|--------|----------|---------|
| QA Validation | PASS | Yes | All 42 tests passing |
| Code Review | PASS | Yes | Approved, 0 blockers |
| Security Review | PASS | Yes | No vulnerabilities |
| Migrations | PASS | Yes | 1 migration, reversible |
| Env Config | PASS | Yes | All vars documented |
| Feature Flags | N/A | No | No flags for this feature |
| Rollback Plan | MISSING | Recommended | Not provided |
| Monitoring | PASS | No | Error tracking active |
| Documentation | PASS | No | README updated |

## Blocking Items

None

## Warnings

1. **Rollback plan missing** — Recommended to document rollback procedure for production deployments.

## Deployment Steps

1. Ensure all CI checks pass
2. Run database migrations: `npm run db:migrate`
3. Deploy application: `npm run deploy:production`
4. Verify health checks pass
5. Monitor error rates for 15 minutes

## Rollback Procedure

[Not documented — recommend creating before production deploy]

## Approval

**Required:** Yes (production deployment)
**Tier:** Approve

---

**Recommendation:** PROCEED with noted warning about rollback plan.
```

## Environment-Specific Requirements

### Development

**Required:**
- QA validation pass

**Optional:**
- Code review
- Security review
- Rollback plan

**Approval:** None (Auto tier)

### Staging

**Required:**
- QA validation pass
- Code review pass

**Optional:**
- Security review (required if auth changes)
- Rollback plan

**Approval:** Review tier

### Production

**Required:**
- QA validation pass
- Code review pass
- Security review pass
- Migrations valid (if applicable)
- Environment config complete

**Recommended:**
- Rollback plan
- Monitoring configured

**Approval:** Approve tier (always)

## Pre-Execution Check

Before starting, update `.sigil/project-context.md`:
- Set **Current Phase** to `review`
- Set **Feature** to the feature being checked for deployment
- Set **Spec Path** to the active spec directory
- Set **Last Updated** to the current timestamp

If `.sigil/project-context.md` does not exist, create it using the State Tracking format from the `/sigil:draw` command.

## Workflow

```
1. Receive deployment request with target environment
2. Load all review reports and validation results
3. Determine required checks for environment
4. Verify each checklist item:
   a. Check report exists
   b. Verify status is passing
   c. Confirm no blocking issues
5. Check environment-specific requirements:
   a. Migrations (if applicable)
   b. Env vars (if new ones added)
   c. Feature flags (if used)
6. Assess deployment risk
7. Determine approval requirement
8. Generate readiness report
9. Return results with recommendation
```

## Error Handling

### Missing Reports
```
Deployment blocked: Missing required report.

Missing: [Report type]
Expected at: [Path]

Options:
A) Generate missing report (invoke skill)
B) Skip check with documentation
C) Block deployment
```

### Stale Reports
```
Warning: Report may be stale.

Report: [Type]
Generated: [Timestamp]
Last code change: [Timestamp]

Recommend: Re-run [skill] to ensure current.
```

### Migration Validation Failed
```
Deployment blocked: Migration validation failed.

Error: [Migration error message]

Options:
A) Fix migration and retry
B) Rollback migration changes
C) Escalate to DBA
```

## Approval Matrix

| Environment | Security Changes | DB Changes | Normal Changes |
|-------------|------------------|------------|----------------|
| Development | Auto | Auto | Auto |
| Staging | Review | Review | Review |
| Production | Approve | Approve | Approve |

## Integration

### Receiving from security-reviewer
```json
{
  "handoff_from": "security-reviewer",
  "security_status": "approved",
  "security_report": "/.sigil/specs/.../reviews/security-review.md"
}
```

### Passing to DevOps Agent
```json
{
  "handoff_to": "devops-agent",
  "deploy_status": "ready",
  "deploy_report": "/.sigil/specs/.../reviews/deploy-readiness.md",
  "environment": "production",
  "approval_required": true,
  "deploy_steps": [...]
}
```

## Escalation Triggers

Escalate when:
- Security review has unresolved high/critical findings
- Migrations are irreversible for production
- Required reports are missing and can't be generated
- Environment configuration incomplete
- Multiple warnings for production deployment

## Notes

- Be stricter for production than staging/dev
- Flag missing recommended items but don't block for them
- Consider deployment timing (avoid high-traffic periods)
- Ensure rollback is tested when possible
- Production requires explicit human approval always

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-20 | Initial release |
