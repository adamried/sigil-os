---
description: Run code review or security review on demand, independently of the full pipeline
argument-hint: [code | security | full | <spec-path>]
---

# On-Demand Review

You are the **Review Coordinator** for Sigil OS. Your role is to run code review, security review, or both on the current set of changes — without requiring a full `/sigil:draw` cycle. Use this when the user has made changes outside the pipeline and wants a structured review pass.

## User Input

```text
$ARGUMENTS
```

## Process

### Step 1: Parse Arguments

| Pattern | Scope |
|---------|-------|
| `code` or no arguments | Code review only |
| `security` | Security review only |
| `full` | Code review then security review |
| `<spec-path>` (matches `.sigil/specs/...`) | Review the listed feature's accumulated changes |

### Step 2: Identify the Change Set

Determine which files to review:

1. If a spec path is provided, read `.sigil/specs/<feature>/tasks.md` and collect every file referenced across completed tasks
2. Otherwise, use the current git working tree: `git diff --name-only HEAD` plus untracked files (`git ls-files --others --exclude-standard`)
3. If both are empty, report "No changes detected" and exit gracefully

### Step 3: Preflight

1. Read `.sigil/config.yaml` to load `audit_mode` and (when available) `execution_mode`
2. Load `.sigil/constitution.md` — reviews enforce constitutional rules
3. Load `.sigil/waivers.md` if it exists — active waivers inform review verdicts
4. If `audit_enabled`, append a `workflow-start` entry with action `review-standalone` and the chosen scope

### Step 4: Run Reviews

**Code review (scope `code` or `full`):**
- Read the `code-reviewer` SKILL.md and follow its process
- Pass the change set and (if available) the spec path
- Produce a verdict (Approve / Approve with comments / Request changes) and a written report
- Write report to `.sigil/specs/<feature>/reviews/code-review-<timestamp>.md` when a spec path is in scope; otherwise to `.sigil/reviews/code-review-<timestamp>.md`

**Security review (scope `security` or `full`):**
- Invoke the `specialist-selection` skill to determine if `appsec-reviewer` or `data-privacy-reviewer` should overlay the base security agent
- Read the `security-reviewer` SKILL.md and follow its process
- Produce a verdict and written report; write to the same `reviews/` directory pattern as code review
- For the `full` scope, run only after the code review completes — sequential, not concurrent

### Step 5: Report

Reference `templates/output-formats.md` for canonical formatting. Surface for each review run:

- Scope, verdict, and counts of Blockers / Warnings / Suggestions
- Report file path
- Top three highest-severity findings (one line each)
- If verdict is "Request changes", a Next-Action prompt listing the user's options (fix-and-rerun, waive, defer)

If `audit_enabled`, append a `phase` entry for each review and a `workflow-end` entry on completion.

## Guidelines

- **Sequential, not parallel.** When scope is `full`, code review runs before security review. They have different agents and different criteria — do not merge them.
- **Verdict authority.** Code review and security review can each block independently. A "code Approve" verdict does not override a "security Request changes" verdict.
- **No fix loop here.** This command produces reports. It does not enter the QA fixer loop — that's the `/sigil:draw` orchestrator's job. If the user wants fixes, prompt them to run `/sigil:draw continue` (when a spec is in scope) or to address findings manually.
- **Jargon suppression.** Say "reviewing your code" or "running a security check," not "invoking code-reviewer" or "running security-reviewer."
