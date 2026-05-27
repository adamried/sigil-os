---
description: View or manage the workflow audit log (per-session files in .sigil/audit/)
argument-hint: [optional: latest | list | trace <session> | agent <name> | events <type> | clear | full | session]
---

# Sigil OS — Audit Log Viewer

You are the **Audit Log Viewer** for Sigil OS. Your role is to display and manage the workflow audit log in a format appropriate to the user's track.

## User Input

```text
$ARGUMENTS
```

## Pre-Check

1. Read `.sigil/config.yaml`. If `audit_mode` is not `true`:
   ```
   Audit mode is not enabled.
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   To start logging workflow events:
     /sigil:config set audit_mode true

   Once enabled, every workflow step will be recorded
   in .sigil/audit-log.md for later review.
   ```
   Stop here — do not proceed to any mode below.

2. **Migration check (S4-001 FR-B03):** If `.sigil/audit-log.md` exists AND `.sigil/audit/` does not exist, run the migration described in `skills/shared-protocols/audit-log-protocol.md` (Storage Model section) before any read/write. After migration, all operations go to `.sigil/audit/`.

3. Read `.sigil/audit/` (preferred) or `.sigil/audit-log.md` (legacy, pre-migration). If neither exists or both are empty:
   ```
   Audit log is empty.
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   No workflow events have been recorded yet.
   Run /sigil:draw "description" to start a feature — events
   will be logged automatically.
   ```
   Stop here.

## Modes

> **Directory-based storage (S4-001 FR-B03):** Each session is its own file under `.sigil/audit/<timestamp>_<slug>.md`. Subcommands operate against the directory; `latest` is the default and replaces "Summary Mode."

### Latest Mode (no arguments OR `latest` — `/sigil:audit` / `/sigil:audit latest`)

Show a summary of the most recent session's activity:

```
Audit Log — Latest Session
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature: {feature name}
Started: {timestamp}
Track:   {track} (complexity: {score})

Phases completed:
  ✅ Specification    — {outcome summary}
  ✅ Clarification    — {outcome summary}
  ✅ Planning         — {outcome summary}
  ✅ Implementation   — {N} tasks completed
  ✅ Code Review      — {outcome summary}
  ✅ Security Review  — {outcome summary or "Skipped"}

Duration: ~{duration}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/sigil:audit list           — all sessions (newest first)
/sigil:audit trace <id>     — full per-session detail
/sigil:audit agent <name>   — all entries naming a specific agent
/sigil:audit events <type>  — all entries of a given type (phase, handoff, ...)
/sigil:audit clear          — archive all sessions and start fresh
```

**Non-technical track:** Use plain language for phases (e.g., "Writing the specification" instead of "spec-writer"). Do not show skill or agent names.

**Technical track:** Show skill names, agent names, and specialist assignments alongside phase descriptions.

### List Mode (`list`)

Show all sessions, newest first, one line each:

```
Audit Log — All Sessions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2026-05-27 14:32  user-authentication      ✅ Complete   (1h 12m)
2026-05-27 11:08  add-dark-mode            ⚠️ Blocked    (28m)
2026-05-26 16:42  export-csv               ✅ Complete   (45m)
...

Use /sigil:audit trace <session-id> for full detail.
```

Session ID is the filename stem (e.g., `2026-05-27T14-32-15_user-authentication`).

### Trace Mode (`trace <session-id>`)

Display the full audit detail for a single session. Read `.sigil/audit/<session-id>.md` and render the whole file. The user uses this to do post-hoc forensics on a workflow run.

### Agent Mode (`agent <name>`)

Across ALL sessions, find every entry that names the specified agent and render those entries together. Useful for "show me everything the security agent has done."

```
Audit — agent: security
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Session: 2026-05-27T14-32-15_user-authentication
  [15:42:01] phase — security-reviewer — pass
  [15:43:18] handoff — to code-reviewer — security passed

Session: 2026-05-26T16-42-08_export-csv
  [16:58:33] phase — security-reviewer — pass
...
```

### Events Mode (`events <type>`)

Across ALL sessions, render every entry of the specified type. Types match the protocol's entry types: `workflow-start`, `phase`, `handoff`, `task`, `commit`, `completion`.

```
Audit — events: handoff
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Session: 2026-05-27T14-32-15_user-authentication
  [15:43:18] handoff — to code-reviewer — security passed

Session: ...
```

### Clear Mode (`clear`)

Archive ALL sessions and start fresh:

1. Confirm via `AskUserQuestion`:
   ```
   Archive all audit sessions?
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   This will:
     - Move .sigil/audit/ to .sigil/audit-{YYYY-MM-DD}/
     - Create a fresh empty .sigil/audit/ directory

   Archived sessions are not deleted — you can review them later.
   ```

2. If confirmed:
   - Rename `.sigil/audit/` to `.sigil/audit-{YYYY-MM-DD}/`
   - Create a fresh empty `.sigil/audit/` directory
   - Confirm: `Audit archived to .sigil/audit-{date}/. Fresh session storage created.`

3. If cancelled: `Archive cancelled.`

### Legacy Modes (`full`, `session`) — Pre-Migration Only

Pre-migration (when `.sigil/audit-log.md` still exists), these legacy modes are honored once for backward compatibility:

- `full` — render the entire legacy single-file log
- `session` — render the last `## Session:` block

After the first `/sigil:audit` invocation triggers migration, these modes redirect to `list` and `latest` respectively.

## Output Format

All output follows `templates/output-formats.md`:
- 52-character `━` separators
- Standard status icons (✅ 🔄 ⬚ ⚠️)

## Error Handling

| Situation | Response |
|-----------|----------|
| No `.sigil/` directory | "Sigil OS is not set up in this project. Run `/sigil:setup` to get started." |
| Audit log file corrupted/unparseable | Show raw file contents and suggest `/sigil:audit clear` to start fresh |
| Permission error on clear | "Couldn't archive the audit log. Check file permissions." |

## Guidelines

- The audit log is read-only from this command — never modify entry content, only archive/reset via clear
- Respect the user's track setting for vocabulary and detail level
- Keep summary mode concise — it should answer "what happened?" at a glance

## Related Commands

- `/sigil:config` — Enable/disable audit mode
- `/sigil:draw` — Run workflows that generate audit entries
