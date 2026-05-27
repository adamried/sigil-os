# Story Formats

> Define your team's story format here. The `quick-story` skill uses this format when generating stories.
>
> If this file is missing or empty, `quick-story` falls back to the built-in default (shown below for reference).

---

## Active Format

**Format name:** {Your team's name for this format}

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

**Rules:**

- One persona per story (from `references/personas.md`)
- One label per story (Backend OR Web OR Mobile)
- AC bold in chat/Confluence rendering; plain text in Jira AC field
- No implementation details (no class names, endpoint paths, library mentions)

---

## Format Variations

> If your team has multiple format variations (e.g., one for backend stories, one for design-heavy stories), document them here.

### Variation: {Name}

**When to use:** {Trigger}

```markdown
{Variation format}
```

---

## Anti-Patterns

Examples of HOW that should NOT appear in stories:

- "Add a POST /api/users endpoint"  →  "Add capability to create a new user"
- "Use React Context for auth state"  →  "Persist authenticated state across session"
- "Implement strategy pattern for payments"  →  "Support multiple payment providers behind one checkout flow"
