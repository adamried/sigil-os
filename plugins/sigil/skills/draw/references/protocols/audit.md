# Audit protocol

When `audit_mode` is enabled, write one session file under `.sigil/audit/`:

`<UTC timestamp without colons>_<feature-slug>.md`

The first content identifies the session, feature, and track. Append events
with timestamp, type, actor/role, action, outcome, and relevant artifact paths.
Commit events additionally include task, commit identifier, and message
summary. Audit files and archive directories are ignored by Git; waivers are
not.

The legacy `.sigil/audit-log.md` is read only by migration. A successful
migration creates session files, renames the legacy file with `.migrated`, and
does not run again.
