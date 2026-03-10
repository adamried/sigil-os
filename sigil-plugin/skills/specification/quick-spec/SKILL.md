---
name: quick-spec
version: 1.2.0
description: Constraint wrapper around spec-writer for simple, well-understood changes
category: specification
chainable: true
invoked_by: [orchestrator, quick-flow]
invokes: [spec-writer]
tools: Read, Write
---

# Skill: Quick Spec

## Purpose

Acts as a constraint wrapper around spec-writer for the Quick Flow track. Applies a reduced-output mode for simple, well-understood changes that don't need the full specification process.

## When to Invoke

- Complexity assessment returns "Simple" (score 7-10)
- Bug fixes with clear reproduction steps
- Small features with obvious requirements (1-3 day implementation)
- Text/copy changes, configuration updates
- User explicitly requests "quick" or "just do it"

## Constraints Applied

When invoking spec-writer, quick-spec applies these four constraints:

1. **Skip Clarifier** — Assume requirements are complete, do not invoke the clarifier loop
2. **Single Story Output** — Produce one Outcome or System story, not a full PRD
3. **Inline Acceptance Criteria** — Embed AC directly in requirements, no separate AC document
4. **No Technical Spec** — Skip architecture documentation

## Inputs

**Required:**
```json
{
  "request": "string — Description of the change",
  "story_type": "outcome | system"
}
```

**Optional:**
```json
{
  "context_file": "string — Path to relevant context file"
}
```

Defaults: `story_type` defaults to `"outcome"`.

## Quick Spec Template

```markdown
# Quick Spec: [Change Description]

**Type:** [Bug Fix | Small Feature | Configuration | Copy Change]
**Files Affected:** [1-5 files]

## What
[One paragraph description]

## Why
[One sentence reason]

## Acceptance
- [ ] [Single criterion]
- [ ] [Single criterion]

## Out of Scope
[Optional — only if ambiguity risk]
```

## Output

Single story file persisted to `/.sigil/specs/stories/` so downstream skills (technical-planner, task-decomposer) can reference it.

## When NOT to Use

- Feature touches multiple systems
- Requirements are ambiguous
- User requests full specification process
- Complexity exceeds "Simple" threshold

Route to Standard or Enterprise track instead.

## Integration Note

This skill acts as a constraint wrapper around spec-writer, not an independent specification engine. All spec generation logic lives in spec-writer.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2.0 | 2026-02-19 | Fixed output contradiction — spec always persisted to stories directory |
| 1.1.0 | 2026-02-05 | Enriched from stub to proper thin-delegation skill |
| 1.0.0 | 2026-01-20 | Initial release |
