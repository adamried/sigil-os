---
name: quick-story
description: Writes individual stories using the project-configurable story format from references/story-formats.md. Dual-purpose — quick standalone OR from an approved Story Map. Enforces No-HOW policy, one-label rule, on-demand Figma usage.
version: 1.0.0
category: po
chainable: false
invokes: [persona-lookup]
invoked_by: [story-command]
tools: Read, AskUserQuestion
---

# Skill: Quick Story

## Purpose

Write a single well-formed story that engineering can implement directly. Uses the project's configured story format. Backs both quick standalone stories and from-map stories.

## When to Invoke

- `/story "<description>"` (quick mode)
- `/story from-map <story-id>` (from-map mode)
- `/story from-map all` (iterate over all approved map stories)

## Inputs

- `mode`: `quick | from-map | from-map-all`
- `story_input`: quick description OR Story Map story reference

## Process

### Step 1: Load Format

Read `references/story-formats.md`. If it exists, use the project's configured format. If not, use the built-in default (see template below).

**Default format (used when no override exists):**

```markdown
**Title:** [Backend|Web|Mobile] - {Short Title}

**As a** {persona}
**I want** {capability}
**So that** {outcome}

### Acceptance Criteria
- **GIVEN** {state}
- **WHEN** {action}
- **THEN** {observable outcome}

### Notes
- {Implementation hints, dependencies, edge cases — at the WHAT level, not HOW}

### Labels
- {Backend|Web|Mobile} (exactly one)
```

### Step 2: Resolve Persona

Use `persona-lookup` to resolve the persona by name. Exactly one persona per story. If the input references multiple personas, split into multiple stories.

### Step 3: Apply Label Rule (FR-C11)

Exactly one of Backend / Web / Mobile. Same rule as `decompose` Step 3 — split if spanning multiple, never dual-label.

### Step 4: No-HOW Enforcement (FR-C11)

The story is WHAT and WHY. NEVER include:

- Class names, function names, method signatures
- Specific API endpoints, route paths, query strings
- Specific library or framework choices
- Implementation patterns or design patterns

When the user's input contains implementation details, rewrite to abstract them away. Example:

| User says (HOW) | Story says (WHAT) |
|-----------------|-------------------|
| "Add a POST /api/users endpoint" | "Add capability to create a new user" |
| "Use React Context for the auth state" | "Persist authenticated state across the session" |
| "Implement the strategy pattern for payment providers" | "Support multiple payment providers behind a single checkout flow" |

### Step 5: Figma Usage (FR-C11)

On-demand only:

- If the user mentions a specific Figma frame → one Figma MCP `get_frame` call
- If no frame is referenced → no Figma calls
- Never bulk-load frames in quick-story mode

### Step 6: AC Format (FR-C11)

Same rules as `decompose`:

- Chat / Confluence: bold GIVEN/WHEN/THEN
- Jira AC field: plain GIVEN/WHEN/THEN

### Step 7: From-Map-All Iteration

When `mode == from-map-all`:

1. Load all stories from the approved Story Map
2. Write the first one
3. Surface via `AskUserQuestion`: "Continue to next? Skip? Edit this one?"
4. Iterate

Don't bulk-output all stories at once — chat readability suffers and Figma batching opportunities are lost.

### Step 8: Output

Render the story in the configured format. Include:

- Title, persona, AC, notes, labels
- Linked Epic (from Story Map context)
- Linked Frame (if Figma was consulted)

## Outputs

A Markdown story matching `references/story-formats.md` (or the default).

## Anti-patterns

- **HOW in the story.** Strip and rewrite.
- **Multi-persona, multi-label, multi-outcome stories.** Split.
- **Bulk Figma calls.** On-demand only.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-27 | Initial release — S4-001 FR-C11, FR-C19 |
