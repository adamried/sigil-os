---
name: qa-fixer
description: Attempt automated remediation of validation failures. Invoke when qa-validator finds fixable issues, before escalating to human.
version: 1.2.0
category: qa
chainable: true
invokes: []
invoked_by: [qa-engineer, qa-validator]
tools: Read, Write, Edit, Bash, Glob
---

# Skill: QA Fixer

## Purpose

Attempt automated remediation of validation failures before escalating to human review. This skill handles routine fixes like lint errors, formatting issues, and simple type corrections, allowing the validation loop to complete without human intervention for common issues.

## When to Invoke

- qa-validator reports fixable issues
- Validation loop iteration < 5
- Issues are in fixable categories (lint, format, simple types)

## Inputs

**Required:**
```json
{
  "validation_report_path": "/.sigil/specs/001-feature/qa/task-T001-validation.md",
  "issues": [
    {
      "type": "lint",
      "file": "src/auth.ts",
      "line": 42,
      "message": "Missing semicolon",
      "rule": "semi",
      "auto_fixable": true
    }
  ],
  "iteration": 1
}
```

**Optional:**
```json
{
  "max_iterations": 5,
  "fix_categories": ["lint", "format", "imports"],
  "dry_run": false,
  "issue_history": {}
}
```

## Outputs

**Primary Output:**
```json
{
  "status": "fixed | partial | escalate",
  "iteration": 2,
  "fixes_applied": [
    {
      "issue": "lint error line 42",
      "file": "src/auth.ts",
      "fix_type": "auto-format",
      "change": "Added semicolon",
      "verified": true
    }
  ],
  "remaining_issues": [],
  "unfixable_issues": [
    {
      "issue": "Type error",
      "reason": "Requires logic change, not auto-fixable"
    }
  ],
  "spec_inferences": [
    {
      "ambiguity": "Whether empty input returns null or throws",
      "inferred_behavior": "Return null for consistency with existing handlers",
      "confidence": "high",
      "source": "[auto]"
    }
  ],
  "files_changed_classified": {
    "test": ["src/auth.test.ts"],
    "implementation": ["src/auth.ts"],
    "config": [],
    "other": []
  },
  "implementation_modified": true,
  "issue_history": {
    "lint:src/auth.ts:semi": {"first_seen": 1, "fixed_in": 1, "status": "resolved"},
    "test:src/auth.test.ts:missing-edge-case": {"first_seen": 1, "status": "open"}
  },
  "next_action": "revalidate | escalate | human_review"
}
```

**Artifact Output:** `/.sigil/specs/###-feature/qa/task-{id}-fix-{iteration}.md`

## Fix Categories

### 1. Lint Errors (Auto-Fixable)

```bash
# ESLint auto-fix
npx eslint --fix [files]

# Prettier format
npx prettier --write [files]

# Python
ruff check --fix .
black .
```

**Handles:**
- Missing semicolons
- Trailing whitespace
- Import ordering
- Quote style
- Indentation

### 2. Format Issues (Auto-Fixable)

```bash
# Apply project formatter
npm run format
```

**Handles:**
- Line length
- Bracket spacing
- Trailing commas
- Newline at EOF

### 3. Import Issues (Auto-Fixable)

```bash
# Organize imports
npx eslint --fix --rule 'import/order: error'
```

**Handles:**
- Unused imports (remove)
- Missing imports (add if obvious)
- Import ordering
- Duplicate imports

### 4. Simple Type Errors (Semi-Auto)

**Can Fix:**
- Missing return type annotations (infer from usage)
- Unused variable warnings (prefix with _)
- Obvious type mismatches (string vs String)

**Cannot Fix:**
- Logic errors causing type mismatches
- Complex generic type issues
- Structural type incompatibilities

### 5. Test Fixes (Flagged for Review)

**Can Attempt:**
- Generate test stubs for uncovered requirements
- Update test assertions for changed behavior (FLAG)
- Fix import paths in test files

**Always Flag:**
- Any behavioral test changes
- New test generation
- Test removal

### 6. Accessibility Fixes (Semi-Auto)

**Can Fix:**
- Missing alt text (generate placeholder, flag for review)
- Missing labels (add aria-label)
- Color contrast (suggest fix, don't apply)

**Cannot Fix:**
- Structural accessibility issues
- Complex ARIA patterns

## Pre-Execution Check

Before starting, update `.sigil/project-context.md`:
- Set **Current Phase** to `validate`
- Set **Feature** to the feature being fixed
- Set **Spec Path** to the active spec directory
- Set **Last Updated** to the current timestamp

If `.sigil/project-context.md` does not exist, create it using the State Tracking format from the `/sigil:draw` command.

## Workflow

```
1. Receive issues from qa-validator
2. Categorize by fixability:
   - Auto-fixable → Apply immediately
   - Semi-auto → Attempt with flagging
   - Manual-only → Add to unfixable list
2b. Check for [REGRESSION]-flagged issues:
    - Do NOT attempt auto-fix on regressions
    - Update issue_history: status → "regression", add regressed_in
    - Escalate immediately per qa-escalation-policy
3. For each auto-fixable issue:
   a. Apply fix
   b. Verify fix resolved issue
   c. Log change
4. For semi-auto issues:
   a. Attempt fix
   b. Flag for human review
5. Generate fix report
5b. Classify all changed files:
    - **Test:** matches `*test*`, `*spec*`, `*_test*`, `*.test.*`, or in `test/`/`tests/`/`__tests__/` directories
    - **Implementation:** source files not matching test patterns
    - **Config:** matches `*.config.*`, `*.json`, `*.yaml`, `*.yml`, `*.toml`
    - **Other:** everything else
    - Set `implementation_modified: true` if any implementation files were changed
6. Determine next action:
   - All fixed → Return for re-validation
   - Some remaining → Escalate if iteration >= 5
   - Unfixable found → Escalate immediately
7. Return results
```

## Fix Report Template

```markdown
# Fix Report: T001 (Iteration 2)

**Task:** [Task name]
**Fixed:** [Timestamp]
**Status:** [FIXED | PARTIAL | ESCALATE]

## Fixes Applied

| Issue | File | Fix | Verified |
|-------|------|-----|----------|
| Missing semicolon | auth.ts:42 | Added semicolon | Yes |
| Unused import | auth.ts:3 | Removed import | Yes |

## Changes Made

### auth.ts
```diff
- import { unused } from 'module'
+
  // Line 42
- const x = 5
+ const x = 5;
```

## Regressions

| Fingerprint | Fixed In | Reappeared In | Status |
|-------------|----------|---------------|--------|
| lint:auth.ts:semi | Iteration 1 | Iteration 3 | ESCALATE |

> This section only appears when regressions are detected.

## Remaining Issues

| Issue | File | Reason Not Fixed |
|-------|------|------------------|
| Type error | service.ts:88 | Requires logic change |

## File Classification

| File | Category |
|------|----------|
| auth.ts | Implementation |
| auth.test.ts | Test |

**Implementation Modified:** Yes

## Flagged for Review

1. **Generated test stub** for `loginUser` — needs assertions filled in

## Next Action

[Revalidate] — 1 issue fixed, proceeding to re-validation
```

## Error Handling

### Fix Breaks Other Things
```
Fix caused new issue:
- Original: [Original issue]
- Fix applied: [What was done]
- New issue: [What broke]

Action: Reverting fix, escalating original issue.
```

### Fix Fails to Apply
```
Fix failed to apply:
- Issue: [Issue description]
- Attempted fix: [What was tried]
- Error: [Error message]

Action: Adding to unfixable list.
```

### Iteration Limit Reached
```
Fix loop limit reached (5 iterations).

Persistent issues:
1. [Issue 1] — Attempted [N] times
2. [Issue 2] — Attempted [N] times

Analysis: [Why these can't be auto-fixed]

Escalating to human review.
```

## Escalation Triggers

See [`qa-escalation-policy/SKILL.md`](../qa-escalation-policy/SKILL.md) for the canonical escalation policy shared across all QA skills and the QA Engineer agent.

## Safety Guardrails

### Never Auto-Fix
- Security-related code
- Business logic
- Data handling/validation
- Authentication/authorization
- Test assertions (without flagging)
- API contracts

### Always Verify
- Run linter after fix to confirm resolution
- Check for new issues introduced
- Ensure file still parses correctly

### Always Log
- Every change made
- Before/after state
- Verification result

## Spec Clarification Tagging

When qa-fixer infers spec behavior to resolve an ambiguity (e.g., deciding how to handle an edge case not explicitly covered in the spec), it must:

1. **Tag the inference as `[auto]`** — All inferred behaviors are tagged with `**Source:** [auto]` to distinguish them from human-confirmed clarifications (`[human]`).

2. **Include a Spec Inferences table in the fix report:**

```markdown
## Spec Inferences

| Ambiguity | Inferred Behavior | Confidence | Source |
|-----------|-------------------|------------|--------|
| [What was unclear] | [What was assumed] | [high/medium/low] | [auto] |
```

3. **Append to clarifications.md** with `**Source:** [auto]`:

```markdown
### Auto-Resolved: [Category] — [Ambiguity]
**Context:** Encountered during QA fix loop (iteration N)
**Answer:** [Inferred behavior]
**Source:** [auto]
**Confidence:** [high/medium/low]
**Spec Update:** [How spec was interpreted]
```

Low-confidence inferences should be flagged for human review rather than applied silently.

## Integration with Validation Loop

```
┌─────────────────┐
│  qa-validator   │
│  (finds issues) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│   qa-fixer      │────▶│   Revalidate    │
│  (iteration 1)  │     │                 │
└────────┬────────┘     └────────┬────────┘
         │                       │
    (if unfixable)          (if still fails)
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│    Escalate     │     │   qa-fixer      │
│   to human      │     │  (iteration 2)  │
└─────────────────┘     └─────────────────┘
                               ...
                        (max 5 iterations)
```

## Iteration Strategy

### Iteration 1-2: Aggressive Auto-Fix
- Apply all auto-fixable changes
- Attempt semi-auto fixes

### Iteration 3-4: Conservative
- Only auto-fix clear issues
- Flag more for review
- Start documenting persistent issues

### Iteration 5: Final Attempt
- Document all remaining issues
- Prepare escalation report
- Suggest manual fixes

## Issue History Tracking

The `issue_history` object is maintained across fix loop iterations, tracking each fingerprint's lifecycle.

**Flow:**
1. On first invocation, `issue_history` may be empty or absent — initialize from current issues (all `open`, `first_seen: 1`).
2. On subsequent invocations, `issue_history` is passed in from qa-validator (which received it from the prior qa-fixer output).
3. Each iteration, update the history:
   - **New fingerprints** (not in history) → add with `status: "open"`, `first_seen: {current_iteration}`
   - **Fixed fingerprints** (in history but not in current issues) → set `status: "resolved"`, `fixed_in: {current_iteration}`
   - **Regression fingerprints** (flagged `[REGRESSION]` by qa-validator) → set `status: "regression"`, `regressed_in: {current_iteration}`

**Status values:**
- `open` — Issue exists and has not been fixed yet
- `resolved` — Issue was fixed in a previous iteration and has not reappeared
- `regression` — Issue was fixed but reappeared in a later iteration

The complete `issue_history` is included in the output JSON and passed to qa-validator on re-entry for regression comparison.

## Notes

- Preserve git history readability (combine related fixes)
- Don't auto-fix in files outside task scope
- Respect project's existing fix configurations
- Log all changes for audit trail

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-20 | Initial release |
| 1.1.0 | 2026-02-09 | SX-003: Added `[auto]` source tags for spec inferences. S2-003: Added `implementation_modified` flag and file classification in fix reports. |
| 1.2.0 | 2026-02-09 | SX-005: Added `issue_history` to input/output (FR-002), regression escalation rule (FR-004), Regressions section in fix report (FR-005), Issue History Tracking section |
