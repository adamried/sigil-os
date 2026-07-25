# Jira capability adapter

Capabilities:

- fetch one issue;
- search issues;
- fetch a parent;
- list transitions;
- add a comment;
- transition an issue;
- add a remote artifact link or fall back to local text.

Check connector availability, authentication, read access, and write
authorization separately. Normalize reads into: key, summary, description,
type, status, parent, acceptance criteria, labels, custom fields, source, and
retrieval time. Field identifiers and category mappings come from project
configuration.

Read-only access supports ticket-to-spec. Comments and transitions occur only
after local completion and are non-blocking unless the user made them a
required outcome. Resolve and display the actual transition name before an
unauthorized transition request is confirmed.
