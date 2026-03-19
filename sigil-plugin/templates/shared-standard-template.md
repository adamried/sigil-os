---
enforcement: recommended          # required | recommended | informational
article: "{Article N: Title}"     # Constitution article this standard maps to (e.g. "Article 4: Security Mandates"). Omit if no direct article mapping.
description: "{One-line summary of what this standard governs}"
version: "1.0.0"
maintained_by: "{team or owner}"
last_updated: "{YYYY-MM-DD}"
---

# Shared Standard: {Standard Name}

## Purpose

{One or two sentences describing what this standard governs and why it exists. Write for a mixed technical/non-technical audience.}

## Scope

Applies to: {project types, languages, frameworks, or teams this standard covers}

Does NOT apply to: {explicit exclusions — prototypes, internal tools, etc.}

## Rules

> **Each rule must be independently verifiable.** Avoid vague requirements ("code should be readable"). Prefer specific, testable statements ("all public API endpoints must require authentication").

### {Rule 1 Title}

{Description of the rule. What must be true. Not how to implement it.}

**Rationale:** {Why this rule exists — the incident, regulation, or principle behind it.}

### {Rule 2 Title}

{Description of the rule.}

**Rationale:** {Why this rule exists.}

<!-- Add as many rules as needed. Each rule = one named section. -->

## Accepted Exceptions

{List scenarios where a project may legitimately deviate from this standard, and what documentation or approval is required.}

| Exception | Conditions | Required Approval |
|-----------|------------|-------------------|
| {scenario} | {conditions under which deviation is acceptable} | {who must approve} |

If no exceptions are allowed, write: "No exceptions. This standard applies universally to all in-scope projects."

## Constitution Article Template

> Copy this block into a project's `constitution.md` to inherit this standard.
> Replace `@inherit` with the standard's content during Standards Expand Protocol.

```markdown
## {Standard Name}

@inherit standards/{standard-id}.md
```

## Verification Checklist

> Used by QA or code review to confirm compliance. Each item must be checkable without specialized tooling.

- [ ] {Checkable verification step}
- [ ] {Checkable verification step}
- [ ] {Checkable verification step}

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | {YYYY-MM-DD} | Initial version |
