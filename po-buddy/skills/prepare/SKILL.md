---
name: prepare
description: Push approved stories to a configurable target (default Jira when Atlassian MCP present). Two-step create pattern (skeleton + edit), field mapping, epic linking, mandatory PO confirmation gate before any external write.
version: 1.0.0
category: po
chainable: false
invokes: []
invoked_by: [prepare-command]
tools: Read, AskUserQuestion
---

# Skill: Prepare

## Purpose

Push a story (or batch of stories) to an external system — typically Jira, optionally Confluence, optionally a local Markdown export. Always require explicit PO confirmation before the external write.

## When to Invoke

- `/prepare <story-id> [--target jira|confluence|local]`
- After `/story` produces a story and the user wants to push it

## Inputs

- `story_content`: the story to push
- `target`: `jira | confluence | local` (default: `jira` if Atlassian MCP present, else `local`)

## Process

### Step 1: Target Resolution

| Target | Adapter required | Default? |
|--------|------------------|----------|
| `jira` | Atlassian MCP `create_issue` + `update_issue` | When MCP present |
| `confluence` | Atlassian MCP `create_page` | Never default |
| `local` | None | When MCP absent |

If `jira` requested but MCP missing, surface and fall back to `local` (with user confirmation).

### Step 2: Two-Step Create Pattern (Jira target)

The two-step pattern avoids partial writes on failure:

1. **Skeleton create** — create a Jira ticket with minimum required fields:
   - Title
   - Type (Story)
   - Description placeholder ("Pending content")
   - Epic Link (parent epic key)
2. **Edit to full content** — update the ticket with:
   - Full description (As a / I want / So that)
   - Acceptance Criteria (plain GIVEN/WHEN/THEN — Jira's bold rendering in AC is unreliable)
   - Notes
   - Labels (the Backend/Web/Mobile label)

If Step 1 succeeds but Step 2 fails → the skeleton remains. Surface the gap, keep the skeleton key, let the user manually finish or retry.

If Step 1 fails → no orphaned skeleton. Surface and retry or fall back to local.

### Step 3: Field Mapping

Project-specific field mappings live in `references/atlassian-config.md` (if it exists). Common mappings:

| Story field | Jira field |
|-------------|-----------|
| Title | Summary |
| Label (Backend/Web/Mobile) | Labels |
| Persona | Custom field (varies by project) |
| Epic key | Epic Link |
| Notes | Comments OR description appendix |

If the mapping file doesn't exist, use Jira's standard fields only.

### Step 4: PO Confirmation Gate (MANDATORY)

Before ANY external write, surface via `AskUserQuestion`:

```
About to push to Jira:

  Title:       {Title}
  Epic Link:   {Epic key}
  Labels:      {Label}
  Persona:     {Persona}

Confirm push?
  1. Push as shown above
  2. Edit first (open editable view)
  3. Cancel
```

This is non-negotiable — don't push silently. Even when `--target local`, surface the confirm so the user sees the final form before output.

### Step 5: Output

```
Story Pushed: {Title}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Target:    {jira | confluence | local}
Ticket:    {KEY-123 | URL | local path}
Epic:      {Epic key} (linked)
Status:    {Created | Pending edit | Local-only}

{Next-step prompt — e.g., "Continue with next story in the Story Map?"}
```

## Outputs

- A pushed ticket (Jira), page (Confluence), or local Markdown file
- A confirmation entry the user can keep for their records

## Anti-patterns

- **Single-shot create.** Always two-step (skeleton + edit) for Jira so failures don't leave orphans.
- **Silent push.** PO confirmation gate is mandatory.
- **Bulk push without per-story confirm.** Loop the confirmation gate — don't batch-approve.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-27 | Initial release — S4-001 FR-C22 |
