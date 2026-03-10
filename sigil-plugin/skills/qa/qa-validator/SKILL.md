---
name: qa-validator
description: Run automated quality checks against completed tasks. Invoke after Developer marks task complete to verify quality standards are met.
version: 1.2.0
category: qa
chainable: true
invokes: [qa-fixer]
invoked_by: [qa-engineer]
tools: Read, Write, Bash, Glob, Grep
---

# Skill: QA Validator

## Purpose

Automatically verify that completed work meets quality standards before human review. This skill is the first gate in the Validate phase, ensuring code changes pass automated checks before proceeding to code review.

## When to Invoke

- Developer marks task as complete
- Auto-invoked after each task implementation completes
- Entering Validate phase from Implement phase
- Re-validation after qa-fixer applies fixes

## Inputs

**Required:**
```json
{
  "task_id": "T001",
  "changed_files": ["src/services/auth.ts", "tests/auth.test.ts"],
  "spec_path": "/.sigil/specs/001-feature/spec.md"
}
```

**Optional:**
```json
{
  "constitution_path": "/.sigil/constitution.md",
  "validation_level": "standard | strict",
  "skip_checks": ["lint"],
  "focus_checks": ["tests", "requirements"],
  "issue_history": {}
}
```

**Auto-loaded:**
- Constitution from `/.sigil/constitution.md` (if exists)
- Package manager config (package.json, requirements.txt, etc.)
- Existing test configuration

## Outputs

**Primary Output:**
```json
{
  "status": "pass | fail | partial",
  "task_id": "T001",
  "timestamp": "2025-01-14T10:30:00Z",
  "checks": [
    {
      "name": "unit_tests",
      "status": "pass | fail | skip | error",
      "details": "42 tests passed, 0 failed",
      "duration_ms": 3500
    },
    {
      "name": "lint",
      "status": "fail",
      "details": "3 errors in auth.ts",
      "issues": [
        {"file": "auth.ts", "line": 42, "message": "...", "fingerprint": "lint:auth.ts:semi"}
      ]
    },
    {
      "name": "type_check",
      "status": "pass",
      "details": "No type errors"
    },
    {
      "name": "requirements_coverage",
      "status": "pass",
      "coverage": "100%",
      "details": "All 5 acceptance criteria have tests"
    }
  ],
  "blocking_issues": [
    {"check": "lint", "count": 3, "severity": "error"}
  ],
  "warnings": [
    {"check": "coverage", "message": "Line coverage at 75%, target is 80%"}
  ],
  "next_action": "proceed | fix | escalate",
  "fix_candidates": [
    {"issue": "lint errors", "auto_fixable": true}
  ]
}
```

**Artifact Output:** `/.sigil/specs/###-feature/qa/task-{id}-validation.md`

## Validation Checks

### 1. Unit Tests
```bash
# Detect test runner and execute
npm test          # JavaScript/TypeScript
pytest            # Python
go test ./...     # Go
```

**Pass Criteria:**
- All tests pass
- No skipped tests (without documented reason)
- Test execution completes without error

### 2. Lint/Format
```bash
# Run project linter
npm run lint      # ESLint
ruff check .      # Python
golangci-lint run # Go
```

**Pass Criteria:**
- No errors (warnings acceptable with documentation)
- Formatting matches project style

### 3. Type Check (if applicable)
```bash
# TypeScript
npx tsc --noEmit

# Python with type hints
mypy .
```

**Pass Criteria:**
- No type errors
- No implicit any (per constitution)

### 4. Requirements Coverage

Map spec requirements to implementation:

```markdown
## Requirements Coverage

| Requirement | Implementation | Test | Status |
|-------------|----------------|------|--------|
| User can login | auth.ts:login() | auth.test.ts:45 | Covered |
| Invalid password shows error | auth.ts:82 | auth.test.ts:67 | Covered |
```

**Pass Criteria:**
- Each P1 acceptance criterion has corresponding test
- Tests exercise the requirement behavior

### 5. Regression Check
```bash
# Run full test suite, not just new tests
npm test -- --coverage
```

**Pass Criteria:**
- Existing tests still pass
- No new console errors/warnings
- Coverage not decreased

### 6. Accessibility (if UI changes)
```bash
# Run accessibility linter
npx eslint-plugin-jsx-a11y
npx axe-core
```

**Pass Criteria:**
- WCAG 2.1 AA compliance (per constitution Article 7)
- No critical accessibility issues

### 7. Constitution Compliance

**Override Loading:** Before checking constitution articles, auto-load active overrides from `/.sigil/waivers.md`. Parse the Active Overrides table for entries with `Status: active` and a non-expired date (or "permanent"). Store the list of overridden articles and their adjusted rules.

Check against relevant constitution articles:
- Article 2: Code Standards
- Article 3: Testing requirements
- Article 5: Anti-abstraction (no unnecessary complexity)
- Article 7: Accessibility

**Override-adjusted validation:** For articles with an active override, apply the adjusted rule from the override instead of the original constitution rule. Mark any findings affected by an override with `[OVERRIDE]` in the issue title. For example, if Article 3 requires 80% coverage but an active override reduces it to 50%, validate against the 50% threshold and mark it `[OVERRIDE] Coverage check (50% via active override)`.

**Active Overrides Applied section:** If any overrides were applied during validation, add a section to the validation report:

```markdown
### Active Overrides Applied

| Article | Override | Expires |
|---------|----------|---------|
| Article 3: Testing Requirements | Coverage reduced to 50% | 2026-03-15 |
```

## Issue Fingerprinting

Each issue in `checks[].issues[]` receives a stable `fingerprint` for cross-iteration identity.

**Format:** `{check}:{file}:{rule}`

**Examples:**
- `lint:src/auth.ts:semi`
- `test:src/auth.test.ts:missing-edge-case`
- `type:src/api/handler.ts:TS2345`

**Rule resolution:**
- If the check tool provides a rule ID (e.g., ESLint rule `semi`, TypeScript error `TS2345`), use it directly.
- If no rule ID exists, use a normalized short form of the message: lowercase, spaces replaced with hyphens, truncated to 40 characters.

**Line numbers are excluded** — they shift after fixes, so fingerprints use only check, file, and rule to remain stable across iterations.

## Pre-Execution Check

Before starting, update `.sigil/project-context.md`:
- Set **Current Phase** to `validate`
- Set **Feature** to the feature being validated
- Set **Spec Path** to the active spec directory
- Set **Last Updated** to the current timestamp

If `.sigil/project-context.md` does not exist, create it using the State Tracking format from the `/sigil` command.

## Workflow

```
1. Receive validation request with task details
2. Load spec and constitution
3. Identify appropriate checks for changed files
4. Execute checks in parallel where possible:
   - Tests (blocking)
   - Lint (can be auto-fixed)
   - Types (blocking)
   - Requirements coverage (informational)
5. Compile results
5b. If iteration > 1 and issue_history provided:
    - Compare current fingerprints against issue_history
    - Flag issues with status "resolved" that reappear as [REGRESSION]
6. Determine next action:
   - All pass → proceed to code review
   - Fixable failures → invoke qa-fixer
   - Blocking failures → escalate
7. Generate validation report
8. Return results
```

## Validation Report Template

```markdown
# Validation Report: T001

**Task:** [Task name]
**Validated:** [Timestamp]
**Status:** [PASS | FAIL | PARTIAL]

## Summary

| Check | Status | Details |
|-------|--------|---------|
| Unit Tests | PASS | 42/42 passed |
| Lint | FAIL | 3 errors |
| Types | PASS | No errors |
| Requirements | PASS | 5/5 covered |
| Regression | PASS | No regressions |

## Regressions

| Fingerprint | Fixed In | Reappeared In |
|-------------|----------|---------------|

## Issues

### Blocking
1. **Lint error** at auth.ts:42 — Missing semicolon

### Warnings
1. Line coverage at 75% (target: 80%)

## Next Action

[Fix required — invoking qa-fixer]
```

## Error Handling

### Test Environment Not Configured
```
Validation blocked: Test environment not configured.

Missing: [package.json scripts.test | pytest.ini | ...]

Options:
A) Configure test environment and retry
B) Skip test check with documentation
C) Escalate to DevOps
```

### Flaky Test Detected
```
Potential flaky test detected:
- Test: [Name]
- Behavior: Passed on retry after initial failure

Recommend: Mark as flaky and investigate, or fix test reliability.
```

### Check Timeout
```
Check timed out: [Check name]
Duration: [Time] (limit: [Limit])

Options:
A) Retry with extended timeout
B) Skip check and document
C) Investigate performance issue
```

## Escalation Triggers

See [`qa-escalation-policy/SKILL.md`](../qa-escalation-policy/SKILL.md) for the canonical escalation policy shared across all QA skills and the QA Engineer agent.

## Loop Behavior

```
┌─────────────────┐
│  qa-validator   │
└────────┬────────┘
         │
    ┌────┴────┐
    │  Pass?  │
    └────┬────┘
         │
    Yes  │  No
    ┌────┴────┐──────────────────┐
    │         │                  │
    ▼         │                  ▼
┌─────────────┴──┐      ┌──────────────┐
│  Proceed to    │      │  qa-fixer    │
│  code-reviewer │      └──────┬───────┘
└────────────────┘             │
                               ▼
                      ┌──────────────┐
                      │  Re-validate │
                      │  (loop ≤5)   │
                      └──────────────┘
```

## Integration with Agents

### Receiving from Developer
```json
{
  "handoff_from": "developer",
  "task_id": "T001",
  "files_changed": ["..."],
  "tests_added": ["..."],
  "acceptance_criteria_claimed": ["..."]
}
```

### Passing to qa-fixer (on failure)
```json
{
  "validation_report_path": "/.sigil/specs/.../qa/task-T001-validation.md",
  "issues": [...],
  "iteration": 1,
  "fixable_issues": [...],
  "issue_history": {}
}
```

### Passing to code-reviewer (on pass)
```json
{
  "validation_status": "pass",
  "validation_report_path": "/.sigil/specs/.../qa/task-T001-validation.md",
  "files_reviewed": ["..."],
  "coverage_summary": {...}
}
```

## Notes

- Run checks in parallel where possible for speed
- Cache check results to avoid redundant runs on re-validation
- Log all validation runs for debugging
- Respect project's existing CI configuration where present

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-20 | Initial release |
| 1.2.0 | 2026-02-20 | S4-102: Override-adjusted validation — auto-loads active overrides from waivers.md, applies adjusted rules for overridden articles, marks results with [OVERRIDE], adds Active Overrides Applied section to report. |
| 1.1.0 | 2026-02-09 | SX-005: Added issue fingerprints (FR-001), regression comparison step (FR-003), issue_history in inputs and qa-fixer handoff, Regressions section in validation report |
