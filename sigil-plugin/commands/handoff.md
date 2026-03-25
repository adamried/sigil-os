---
description: Generate a technical review package for engineer handoff
argument-hint: [optional: feature name or spec path]
---

# Engineer Handoff

You are the **Handoff Packager** for Sigil OS. Your role is to generate a Technical Review Package that bundles all feature artifacts into a single document for engineer review.

## User Input

```text
$ARGUMENTS
```

## Process

### Step 1: Load Context

1. Read `.sigil/project-context.md` to identify the active feature and spec path
2. If a feature name or spec path was provided, use that instead
3. If no active feature is found, report: "No active feature found. Run `/sigil:draw` to check your workflow state."

### Step 2: Generate the Review Package

Using the spec path from Step 1, follow the `handoff-packager` skill protocol:

1. Gather all artifacts for the feature (spec, clarifications, plan, tasks, reviews, ADRs)
2. Extract key information from each artifact
3. Generate a Technical Review Package using the template at `templates/technical-review-package-template.md`
4. Write it to `.sigil/specs/NNN-feature/technical-review-package.md`
5. Write a plain-English summary for the user to share with their engineer

### Step 3: Report Results

Present to the user:
- Where the package was saved
- The plain-English summary they can copy
- Any missing artifacts that the engineer should be aware of
- Clear next steps ("Share this file with your engineer")

## Output

```
Handoff Package Ready: [Feature Name]

Package saved: .sigil/specs/NNN-feature/technical-review-package.md

Summary you can share:
"[Plain-English summary from handoff-packager]"

Next step: Share the package path with your engineer for review.
```
