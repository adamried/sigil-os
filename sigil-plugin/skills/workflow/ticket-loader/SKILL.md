---
name: ticket-loader
description: Loads and enriches ticket context from external issue trackers via adapter skills. Validates adapter availability, fetches ticket and parent data, categorizes work type, and hands off enriched context to the orchestrator.
version: 1.0.0
category: workflow
chainable: true
invokes: [jira]
invoked_by: [orchestrator]
tools: Read, Glob, ToolSearch
model: haiku
---

# Skill: Ticket Loader

## Purpose

Bridge external issue trackers into the Sigil workflow. When a user provides a ticket key (e.g., `PROJ-123`) instead of a plain-text feature description, this skill fetches the ticket data, enriches it with parent/epic context, categorizes the work type, and produces a structured context object that the orchestrator can route through the standard pipeline.

## When to Invoke

- User provides a ticket key matching `[A-Z][A-Z0-9]+-\d+` pattern as input to `/sigil:draw`
- Orchestrator detects ticket-key format in Step 2

## Inputs

**Required:**
- `ticket_key`: string — The ticket identifier (e.g., `PROJ-123`, `TEAM-456`)

**Auto-loaded:**
- `config`: object — `.sigil/config.yaml` integrations section for adapter lookup

## Process

### Step 1: Validate Adapter

1. Extract project prefix from ticket key (everything before the `-`)
2. Read `.sigil/config.yaml` and check `integrations:` section for a matching adapter
3. Match by `project_keys` array in adapter config
4. If no adapter found for this project prefix:
   ```
   No integration configured for project "{prefix}".

   To use ticket-driven workflows, connect to a shared context
   repo that has adapter configs, or add one manually to
   .sigil/config.yaml.

   You can still describe the feature in plain text instead.
   ```
   → Return error, let orchestrator fall back to plain-text input

5. If adapter found, verify MCP tools are available (use `ToolSearch`)
6. If MCP tools not available:
   ```
   {Adapter name} MCP is not configured in this session.
   Ticket loading requires the {MCP server} connection.

   You can describe the feature in plain text instead,
   or configure MCP and try again.
   ```
   → Return error with fallback guidance

### Step 2: Fetch Ticket

1. Invoke the adapter's Fetch Ticket protocol (e.g., Jira adapter's Fetch Ticket)
2. Pass: `ticket_key`
3. Receive: ticket data (summary, description, type, priority, status, labels, story_points, assignee, reporter)
4. If ticket not found:
   ```
   Could not find ticket {ticket_key}. Check that:
   - The ticket key is correct
   - You have access to this project
   - The ticket hasn't been deleted
   ```
   → Return error

### Step 3: Fetch Parent Context

1. If the ticket has a parent/epic link:
   a. Invoke the adapter's Fetch Parent protocol
   b. Pass: parent ticket key
   c. Receive: parent summary, description, acceptance criteria
2. If no parent link: skip (standalone ticket)
3. If parent fetch fails: continue without parent context (non-blocking)

### Step 4: Categorize

Map the ticket's issue type and labels to a Sigil work category:

| Category | Mapping Criteria |
|----------|-----------------|
| `bug` | Issue type = Bug, Defect, or label contains "bug" |
| `feature` | Issue type = Story, User Story, Feature, or label contains "feature" |
| `enhancement` | Issue type = Task, Improvement, or label contains "enhancement" |
| `maintenance` | Issue type = Chore, Tech Debt, or label contains "maintenance", "tech-debt", "refactor" |

**Priority rules:**
1. Adapter-specific category mapping takes precedence (from adapter config)
2. Labels override issue type if both are present
3. Default to `enhancement` if no match

**Category-specific routing hints:**
- `maintenance` → suggest Quick Flow, skip complexity assessor
- `bug` without security labels → cap at Standard track
- `feature` → full pipeline (no override)
- `enhancement` → standard assessment

### Step 5: Assemble Enriched Context

Build the structured context object:

```json
{
  "source": "ticket",
  "ticket_key": "PROJ-123",
  "category": "feature",
  "adapter": "jira",
  "ticket_metadata": {
    "summary": "As a user, I want to reset my password",
    "description": "Full ticket description...",
    "type": "Story",
    "priority": "High",
    "status": "To Do",
    "labels": ["auth", "user-facing"],
    "story_points": 5,
    "assignee": "jane@example.com",
    "reporter": "pm@example.com",
    "related_ticket_count": 3
  },
  "parent_context": {
    "key": "PROJ-100",
    "summary": "User Authentication Epic",
    "description": "Epic description..."
  },
  "enriched_description": "Feature: As a user, I want to reset my password\n\nFrom ticket PROJ-123 (Story, High priority, 5 story points)\nEpic: User Authentication (PROJ-100)\n\nFull ticket description...",
  "routing_hints": {
    "suggested_track": null,
    "skip_complexity": false,
    "cap_track": null
  }
}
```

### Step 6: Hand Off

Return the enriched context to the orchestrator. The orchestrator uses `enriched_description` as the feature description input and passes `ticket_metadata` through the pipeline for downstream skills (complexity-assessor, handoff-back).

## Outputs

**Handoff Data:**
```json
{
  "source": "ticket",
  "ticket_key": "PROJ-123",
  "category": "feature|bug|enhancement|maintenance",
  "adapter": "jira",
  "ticket_metadata": { ... },
  "parent_context": { ... },
  "enriched_description": "...",
  "routing_hints": { ... }
}
```

## Error Handling

| Scenario | Behavior |
|----------|----------|
| No adapter for project prefix | Show guidance, fall back to plain text input |
| MCP tools not available | Show guidance, fall back to plain text input |
| Ticket not found | Show error with troubleshooting hints |
| Parent fetch fails | Continue without parent context (non-blocking) |
| Adapter returns partial data | Use what's available, default missing fields |
| Config file missing | "No integrations configured. Describe your feature in plain text." |
| Multiple adapters match prefix | Use first match, log warning |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-20 | Initial release — S4-104 Phase 1: ticket validation, fetch, categorization, enriched context assembly |
