---
name: code-reviewer
description: Perform structured code review against project standards and best practices. Invoke after qa-validator passes to review code quality before deployment.
version: 1.3.0
category: review
chainable: true
invokes: []
invoked_by: [orchestrator]
tools: Read, Write, Glob, Grep
---

# Skill: Code Reviewer

## Purpose

Perform structured code review against project standards, constitution principles, and software engineering best practices. This skill provides a thorough review of code quality, architecture adherence, and maintainability before changes proceed to security review or deployment.

## When to Invoke

- qa-validator passes all checks
- Auto-invoked after all tasks pass validation
- Entering Review phase from Validate phase
- Changes are ready for final quality assessment

## Inputs

**Required:**
```json
{
  "changed_files": ["src/services/auth.ts", "src/models/user.ts"],
  "spec_path": "/.sigil/specs/001-feature/spec.md"
}
```

**Optional:**
```json
{
  "plan_path": "/.sigil/specs/001-feature/plan.md",
  "constitution_path": "/.sigil/constitution.md",
  "review_depth": "standard | thorough",
  "focus_areas": ["error_handling", "architecture"],
  "previous_review": "/.sigil/specs/001-feature/reviews/code-review-v1.md",
  "qa_fix_metadata": {
    "implementation_modified": false,
    "files_changed_classified": {},
    "fix_loop_summary": ""
  }
}
```

**Auto-loaded:**
- Constitution from `/.sigil/constitution.md`
- Project coding standards
- Existing codebase patterns
- `user_track` from `.sigil/config.yaml` (default: `non-technical`)

## User Track Branching

The review report adapts based on the user's track:

**`non-technical` track:**
- Summary-focused report: overall status, blocker count, plain-English descriptions
- Findings use business language ("This code could cause errors for users" not "Unhandled promise rejection")
- Code snippets omitted from findings; replaced with file name and description
- Approval status clearly states what to do next

**`technical` track:**
- Full line-level detail with code snippets, line numbers, and suggested fixes
- Findings reference specific patterns, libraries, and constitution articles
- Includes complexity metrics and architecture analysis
- Tech debt entries include implementation context

## Outputs

**Primary Output:**
```json
{
  "status": "approved | changes_requested | blocked",
  "review_id": "CR-001",
  "timestamp": "2025-01-14T10:30:00Z",
  "files_reviewed": 3,
  "findings": [
    {
      "id": "F001",
      "severity": "suggestion | warning | blocker",
      "category": "style | architecture | error_handling | performance | security",
      "file": "src/auth.ts",
      "line": 42,
      "code_snippet": "...",
      "message": "Consider extracting this to a separate function",
      "suggested_fix": "...",
      "constitution_reference": "Article 5"
    }
  ],
  "summary": {
    "total_findings": 5,
    "blockers": 0,
    "warnings": 2,
    "suggestions": 3
  },
  "approval_conditions": [],
  "commendations": ["Good error handling in auth service"],
  "tech_debt_captured": 2,
  "tech_debt_path": "/.sigil/tech-debt.md"
}
```

**Artifact Output:** `/.sigil/specs/###-feature/reviews/code-review.md`

## Review Criteria

### 1. Code Style (Constitution Article 2)

**Checks:**
- Naming conventions followed
- Consistent formatting
- File organization
- Import structure
- Comment quality (not quantity)

**Examples:**
```
SUGGESTION: Variable 'x' should have a descriptive name
  File: auth.ts:42
  Current: const x = getUserById(id)
  Suggested: const user = getUserById(id)
```

### 2. Architecture (Constitution Article 5)

**Checks:**
- Follows existing patterns in codebase
- No unnecessary abstractions
- Appropriate separation of concerns
- Dependencies in correct direction
- Single responsibility principle

**Examples:**
```
WARNING: This creates a new pattern inconsistent with existing code
  File: services/auth.ts
  Issue: Using class-based service when codebase uses functions
  Recommendation: Follow existing functional pattern or document why different
```

### 3. Error Handling

**Checks:**
- All error cases handled
- Errors logged appropriately
- User-facing errors are helpful
- No swallowed errors
- Appropriate error types used

**Examples:**
```
WARNING: Error is caught but not logged
  File: auth.ts:88
  Code: catch (e) { return null; }
  Suggested: Log error before returning, or re-throw with context
```

### 4. Complexity

**Checks:**
- Functions reasonably sized (guideline: ~20 lines)
- Cyclomatic complexity reasonable
- Nesting depth manageable (max 3-4 levels)
- No overly clever solutions

**Examples:**
```
SUGGESTION: Function is complex (cyclomatic complexity: 12)
  File: validator.ts:validateInput()
  Recommendation: Consider breaking into smaller functions
```

### 5. DRY Principle

**Checks:**
- No duplicate code
- Shared logic extracted appropriately
- But not over-abstracted (per Article 5)

**Examples:**
```
SUGGESTION: Similar code in 3 locations
  Files: auth.ts:45, user.ts:67, session.ts:23
  Pattern: Error formatting logic
  Recommendation: Extract to shared utility if used 3+ times
```

### 6. Testability

**Checks:**
- Code is testable (dependencies injectable)
- No hidden dependencies
- Side effects isolated
- Pure functions where possible

### 7. Documentation

**Checks:**
- Public APIs documented
- Complex logic has comments explaining "why"
- No redundant comments explaining "what"
- README updated if needed

### 8. Constitution Compliance

**Override Loading:** Before checking constitution articles, auto-load active overrides from `/.sigil/waivers.md`. Parse the Active Overrides table for entries with `Status: active` and a non-expired date (or "permanent"). Store the list of overridden articles and their adjusted rules.

**Checks:**
- Article 2: Code style standards
- Article 5: Anti-abstraction principle
- Article 6: Simplicity preference
- Any project-specific rules

**Override-adjusted review:** For articles with an active override, apply the adjusted rule instead of the original constitution rule. Downgrade findings from Blocker to Warning for overridden articles. Note affected findings with `[OVERRIDE]` in the report. For example, if Article 5 has an override allowing a specific abstraction pattern, findings about that pattern are downgraded from Blocker to Warning with `[OVERRIDE]` annotation.

**Active Overrides Applied section:** If any overrides were applied during review, add a section to the review report after the Summary:

```markdown
### Active Overrides Applied

| Article | Override | Expires |
|---------|----------|---------|
| Article 5: Architecture Principles | Allow repository pattern for data access | permanent |
```

## Review Report Template

```markdown
# Code Review: [Feature Name]

**Review ID:** CR-001
**Reviewer:** Code Reviewer Skill
**Date:** [Timestamp]
**Status:** [APPROVED | CHANGES REQUESTED | BLOCKED]

## Summary

| Category | Blockers | Warnings | Suggestions |
|----------|----------|----------|-------------|
| Style | 0 | 1 | 2 |
| Architecture | 0 | 0 | 1 |
| Error Handling | 0 | 1 | 0 |
| Complexity | 0 | 0 | 1 |
| **Total** | **0** | **2** | **4** |

<!-- Only include QA Fix Impact Notice when implementation_modified is true -->
## QA Fix Impact Notice

> **Implementation was modified during the QA fix loop.** The following implementation files were changed by qa-fixer, not the original developer. Review these with extra scrutiny.

| File | Category |
|------|----------|
| [file] | Implementation |

## Findings

### Warnings

#### W001: Error not logged before return
**File:** src/auth.ts:88
**Category:** Error Handling
**Constitution:** Article 2 (Code Standards)

```typescript
// Current
catch (e) {
  return null;
}

// Suggested
catch (e) {
  logger.error('Authentication failed', { error: e });
  return null;
}
```

### Suggestions

#### S001: Consider descriptive variable name
**File:** src/auth.ts:42
**Category:** Style

```typescript
// Current
const x = getUserById(id);

// Suggested
const user = getUserById(id);
```

## Commendations

- Good separation of concerns in service layer
- Comprehensive error types defined
- Tests cover edge cases well

## Approval Status

[APPROVED] — No blocking issues found. Warnings are recommendations for improvement.

**Conditions:** None

**Next Step:** Proceed to security review
```

## Pre-Execution Check

Before starting, update `.sigil/project-context.md`:
- Set **Current Phase** to `review`
- Set **Feature** to the feature being reviewed
- Set **Spec Path** to the active spec directory
- Set **Last Updated** to the current timestamp

If `.sigil/project-context.md` does not exist, create it using the State Tracking format from the `/sigil:draw` command.

## Workflow

```
1. Receive files and spec for review
1b. If qa_fix_metadata provided and implementation_modified is true:
    - Flag implementation files from files_changed_classified for priority review
    - These files were modified during the QA fix loop, not the original implementation
2. Load constitution and project standards
3. For each file:
   a. Parse and analyze structure
   b. Check against review criteria
   c. Compare with existing codebase patterns
   d. Generate findings
4. Cross-file analysis:
   a. Check for duplicated code
   b. Verify architecture consistency
   c. Check dependency directions
5. Compile findings by severity
6. Determine approval status:
   - No blockers → Approved (may have warnings/suggestions)
   - Has blockers → Changes Requested
7. Generate review report
8. Return results
```

## Tech Debt Persistence

After completing the review, if any findings have `severity: "suggestion"`, persist them to `/.sigil/tech-debt.md`:

1. **Read** `/.sigil/tech-debt.md` (create if it doesn't exist)
2. **Duplicate check** — Skip if an entry with the same file and concept already exists
3. **Append** each new suggestion using the entry format below
4. **Cap at 50 items** — If the file exceeds 50 entries, add a warning comment: `<!-- Tech debt backlog at capacity. Review and triage before adding more. -->`
5. **Silent operation** — Do not mention tech-debt persistence to the user unless asked

**Entry format:**

```markdown
- **[Short description]**
  - Feature: [feature-id]
  - Review: [CR-###]
  - File: [file:line]
  - Category: [style | architecture | error_handling | performance | complexity | DRY]
  - Suggested Fix: [Brief suggestion]
  - Added: [YYYY-MM-DD]
```

**File header** (created once):

```markdown
# Tech Debt Backlog

> Non-blocking suggestions from code reviews. Review periodically.

---
```

## Severity Guidelines

### Blocker
Must be fixed before approval:
- Security vulnerabilities
- Data loss potential
- Breaking existing functionality
- Constitution violations (hard rules)

### Warning
Should be fixed, but can proceed:
- Code quality concerns
- Performance issues (non-critical)
- Pattern inconsistencies
- Missing error handling

### Suggestion
Nice to have improvements:
- Style preferences
- Minor refactoring opportunities
- Documentation additions
- Test coverage expansion

## Error Handling

### File Not Found
```
Cannot review file: [Path]
Reason: File not found or inaccessible

Options:
A) Verify file path and retry
B) Exclude from review scope
C) Escalate
```

### Large File Warning
```
File exceeds review threshold: [Path]
Size: [N] lines (threshold: 500)

Recommendation: Consider breaking into smaller modules.
Proceeding with focused review on changed sections only.
```

## Integration

### Receiving from qa-validator
```json
{
  "handoff_from": "qa-validator",
  "validation_status": "pass",
  "changed_files": ["..."],
  "validation_report": "/.sigil/specs/.../qa/validation.md"
}
```

### Passing to security-reviewer
```json
{
  "handoff_to": "security-reviewer",
  "review_status": "approved",
  "review_report": "/.sigil/specs/.../reviews/code-review.md",
  "security_relevant_files": ["src/auth.ts"],
  "findings_for_security": [...]
}
```

## Notes

- Review is read-only; no code changes made
- Focus on significant issues, not nitpicks
- Consider developer experience in feedback tone
- Reference constitution for authority
- Be specific with line numbers and code snippets

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.3.0 | 2026-02-20 | S4-102: Override-adjusted review — auto-loads active overrides from waivers.md, downgrades blockers to warnings for overridden articles, annotates with [OVERRIDE], adds Active Overrides Applied section. |
| 1.2.0 | 2026-02-19 | Added user_track branching — non-technical gets summary-focused report, technical gets line-level detail |
| 1.1.0 | 2026-02-09 | S2-003: Added QA Fix Impact Notice and `qa_fix_metadata` input. SX-002: Added tech-debt persistence for non-blocking suggestions. Added Write tool. |
| 1.0.0 | 2026-01-20 | Initial release |
