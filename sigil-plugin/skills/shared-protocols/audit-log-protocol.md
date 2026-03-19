# Shared Protocol: Audit Log

> **Referenced by:** The orchestrator (`sigil.md`) and skills using the `pre-execution-check` protocol.

## Purpose

Standardize how workflow events are appended to `.sigil/audit-log.md` when audit mode is enabled. This protocol ensures a consistent, append-only execution trace across all workflow phases.

## When to Log

Only log when `audit_mode: true` in `.sigil/config.yaml`. If the key is missing or set to `false`, skip all logging silently.

## How to Check

1. Read `.sigil/config.yaml`
2. Parse the YAML content
3. Check if `audit_mode` equals `true` (string or boolean)
4. If not `true`, do not log — return immediately

## Session Header

On the **first audit entry** of a workflow run, write a session header before the entry:

```markdown
## Session: {ISO-8601 timestamp} | Feature: {feature name or "New Feature"}
```

The session header is written once per `/sigil "description"` or `/sigil continue` invocation. Subsequent entries in the same workflow run append under this header without repeating it.

## Entry Format

Each entry is an H3 with a timestamp, followed by bullet fields:

```markdown
### [{HH:MM:SS}] {Entry Title}
- **{Field}**: {Value}
- **{Field}**: {Value}
```

## Entry Types

### workflow-start
Written when a workflow begins (after preflight, before routing).

Required fields:
- **Input**: The user's feature description or ticket key
- **Track**: Selected track and complexity score (e.g., `Standard (complexity: 14/21)`)

### phase
Written when a workflow phase begins.

Required fields:
- **Skill**: The skill being invoked (use internal name)
- **Outcome**: Brief result after the phase completes (e.g., `Created spec.md (5 requirements)`)

### handoff
Written when an agent handoff occurs.

Required fields:
- **Reason**: Why the handoff is happening
- **Skills used**: Skills invoked by the agent
- **Outcome**: Result of the agent's work

### task
Written per implementation task.

Required fields:
- **Specialist**: Specialist name or "base"
- **Outcome**: `Complete (attempt N/5)` or `Failed — escalated`

### completion
Written when a workflow finishes.

Required fields:
- **Tasks**: Total completed count
- **Code review**: Status summary
- **Security review**: Status summary or "Skipped"
- **Duration**: Approximate wall-clock time from session start

## Append-Only Rules

1. **Never delete or modify** existing entries in the audit log
2. **Always append** new entries at the end of the file
3. If the file does not exist when logging is attempted, create it from `templates/audit-log-template.md` first
4. If the file cannot be written (permissions, etc.), log a warning but do not block the workflow

## File Location

`.sigil/audit-log.md` — lives alongside other ephemeral `.sigil/` artifacts. Gitignored by default.

## Skills Using This Protocol

- Orchestrator (`sigil.md`) — primary consumer, logs all entry types
- Skills using `pre-execution-check` protocol — log `phase` entries automatically when audit mode is enabled
