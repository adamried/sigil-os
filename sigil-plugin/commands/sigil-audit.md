---
description: View or manage the workflow audit log
argument-hint: [optional: full | session | clear]
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
     /sigil-config set audit_mode true

   Once enabled, every workflow step will be recorded
   in .sigil/audit-log.md for later review.
   ```
   Stop here — do not proceed to any mode below.

2. Read `.sigil/audit-log.md`. If the file does not exist or contains no session entries:
   ```
   Audit log is empty.
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   No workflow events have been recorded yet.
   Run /sigil "description" to start a feature — events
   will be logged automatically.
   ```
   Stop here.

## Modes

### Summary Mode (no arguments — `/sigil-audit`)

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
/sigil-audit full     — show complete log
/sigil-audit session  — current session details
/sigil-audit clear    — archive and reset
```

**Non-technical track:** Use plain language for phases (e.g., "Writing the specification" instead of "spec-writer"). Do not show skill or agent names.

**Technical track:** Show skill names, agent names, and specialist assignments alongside phase descriptions.

### Full Mode (`full`)

Display the entire contents of `.sigil/audit-log.md` as-is. This is the raw append-only log with all sessions.

If the file is very long (>200 lines), show the most recent 3 sessions and note how many older sessions exist:

```
Showing 3 most recent sessions ({N} total in log).
Use /sigil-audit clear to archive older entries.
```

### Session Mode (`session`)

Display only the current/most recent session from the audit log. Parse the file for the last `## Session:` header and display everything from that header to the end of the file.

### Clear Mode (`clear`)

Archive the audit log and start fresh:

1. Confirm with the user:
   ```
   Archive audit log?
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   This will:
   - Move the current log to .sigil/audit-log-{date}.md
   - Create a fresh audit log

   The archived log is not deleted — you can review it later.
   ```
   Use AskUserQuestion with options: "Yes, archive" / "Cancel"

2. If confirmed:
   - Rename `.sigil/audit-log.md` to `.sigil/audit-log-{YYYY-MM-DD}.md`
   - Create a fresh `.sigil/audit-log.md` from `templates/audit-log-template.md`
   - Confirm: `Audit log archived to .sigil/audit-log-{date}.md. Fresh log started.`

3. If cancelled: `Archive cancelled. Log unchanged.`

## Output Format

All output follows `templates/output-formats.md`:
- 52-character `━` separators
- Standard status icons (✅ 🔄 ⬚ ⚠️)

## Error Handling

| Situation | Response |
|-----------|----------|
| No `.sigil/` directory | "Sigil OS is not set up in this project. Run `/sigil-setup` to get started." |
| Audit log file corrupted/unparseable | Show raw file contents and suggest `/sigil-audit clear` to start fresh |
| Permission error on clear | "Couldn't archive the audit log. Check file permissions." |

## Guidelines

- The audit log is read-only from this command — never modify entry content, only archive/reset via clear
- Respect the user's track setting for vocabulary and detail level
- Keep summary mode concise — it should answer "what happened?" at a glance

## Related Commands

- `/sigil-config` — Enable/disable audit mode
- `/sigil` — Run workflows that generate audit entries
