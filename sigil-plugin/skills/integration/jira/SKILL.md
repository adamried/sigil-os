---
name: jira
description: Adapter for Atlassian Jira — fetches tickets, parents, categorizes work types, and writes implementation results back via Atlassian MCP tools.
version: 1.2.1
category: integration
chainable: false
invokes: []
invoked_by: [ticket-loader, handoff-back]
tools: ToolSearch, mcp__claude_ai_Atlassian__getJiraIssue, mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql, mcp__claude_ai_Atlassian__addCommentToJiraIssue, mcp__claude_ai_Atlassian__transitionJiraIssue, mcp__claude_ai_Atlassian__getJiraIssueRemoteIssueLinks
model: haiku
---

# Skill: Jira Adapter

## Purpose

Provide read access to Jira tickets for the ticket-loader skill. Translates Jira issue data into Sigil's enriched context format using Atlassian MCP tools.

## MCP Requirements

This adapter requires the Atlassian MCP server. Required tools:

| Tool | Purpose | Phase |
|------|---------|-------|
| `mcp__claude_ai_Atlassian__getJiraIssue` | Fetch individual issue by key | Phase 1 (read) |
| `mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql` | Search for related issues | Phase 1 (read) |
| `mcp__claude_ai_Atlassian__addCommentToJiraIssue` | Post implementation summary as comment | Phase 2 (write) |
| `mcp__claude_ai_Atlassian__transitionJiraIssue` | Move ticket to Done status | Phase 2 (write) |
| `mcp__claude_ai_Atlassian__getTransitionsForJiraIssue` | List available status transitions | Phase 2 (write) |

Before invoking any protocol, use `ToolSearch` with query `"+atlassian jira issue"` to verify MCP availability.

## Configuration Schema

Stored in `.sigil/config.yaml` under `integrations.jira:` or in shared repo at `integrations/jira.yaml`:

```yaml
adapter: jira
name: Jira
mcp_tools:
  - mcp__claude_ai_Atlassian__getJiraIssue
  - mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql
config:
  project_key: YOUR_PROJECT_KEY
  category_mapping:
    bug: [Bug, Defect]
    feature: [Story, "User Story", Feature, Epic]
    enhancement: [Task, Improvement, "Sub-task"]
    maintenance: [Chore, "Tech Debt"]
  label_overrides:
    maintenance: [tech-debt, refactor, cleanup, chore, maintenance]
    bug: [bug, defect, regression]
    feature: [feature, new-feature]
  status_mapping:
    done: [Done, Closed, Resolved]
    in_progress: ["In Progress", "In Review", "In Development"]
    todo: ["To Do", Open, Backlog]
  # Custom field IDs — find yours in Jira Admin > Fields
  custom_fields:
    story_points: "customfield_10016"    # Standard Jira; may vary
    acceptance_criteria: ""              # Leave empty if not used
    epic_link: ""                        # Only needed for older Jira configurations
  # Maintenance epic patterns — stories whose parent epic summary matches
  # any of these patterns are routed as maintenance even without a label
  maintenance_epic_patterns:
    - "Technical Debt"
    - "Platform Maintenance"
```

## Protocols

### Fetch Ticket

Called by `ticket-loader` Step 2.

**Input:** `ticket_key` (e.g., `PROJ-123`)

**Procedure:**

1. Load the Atlassian MCP tool:
   ```
   ToolSearch(query: "select:mcp__claude_ai_Atlassian__getJiraIssue")
   ```
2. Fetch the issue:
   ```
   mcp__claude_ai_Atlassian__getJiraIssue(issueIdOrKey: ticket_key)
   ```
3. Extract and return structured data:
   ```json
   {
     "key": "PROJ-123",
     "summary": "Issue summary",
     "description": "Full description text",
     "type": "Story",
     "priority": "High",
     "status": "To Do",
     "labels": ["auth", "user-facing"],
     "story_points": 5,
     "assignee": "jane@example.com",
     "reporter": "pm@example.com",
     "parent_key": "PROJ-100",
     "subtask_count": 3,
     "link_count": 2
   }
   ```
4. Field extraction mapping:
   - `summary` → `fields.summary`
   - `description` → `fields.description` (convert from ADF to plain text if needed)
   - `type` → `fields.issuetype.name`
   - `priority` → `fields.priority.name`
   - `status` → `fields.status.name`
   - `labels` → `fields.labels`
   - `story_points` → `fields[config.custom_fields.story_points]` (fallback: `fields.customfield_10016`)
   - `acceptance_criteria` → `fields[config.custom_fields.acceptance_criteria]` if configured, else `null`
   - `assignee` → `fields.assignee.emailAddress`
   - `reporter` → `fields.reporter.emailAddress`
   - `parent_key` → `fields.parent.key` (if exists)
   - `subtask_count` → length of `fields.subtasks`
   - `link_count` → length of `fields.issuelinks`

**On error:**
- 404 / Not found → return `{ error: "not_found", message: "Ticket {key} not found" }`
- Permission denied → return `{ error: "forbidden", message: "No access to {key}" }`
- MCP failure → return `{ error: "mcp_error", message: "Could not reach Jira" }`

### Fetch Parent

Called by `ticket-loader` Step 3.

**Input:** `parent_key` (e.g., `PROJ-100`)

**Procedure:**

1. Fetch parent issue using same Fetch Ticket protocol
2. Extract summary, description, and acceptance criteria
3. Return:
   ```json
   {
     "key": "PROJ-100",
     "summary": "User Authentication Epic",
     "description": "Epic description...",
     "type": "Epic",
     "acceptance_criteria": "Extracted from description if present"
   }
   ```

**On error:** Return `null` (parent context is non-blocking).

### Categorize

Called by `ticket-loader` Step 4.

**Input:** `type` (issue type name), `labels` (array)

**Procedure:**

1. Read category mapping from config (`.sigil/config.yaml` → `integrations.jira.config.category_mapping`)
2. If no config, use defaults:

   | Jira Issue Type | Sigil Category |
   |----------------|----------------|
   | Bug, Defect | `bug` |
   | Story, User Story, Feature | `feature` |
   | Task, Improvement, Sub-task | `enhancement` |
   | Chore, Tech Debt | `maintenance` |
   | Epic | `feature` |

3. Check label overrides (from config `label_overrides`):
   - If any label matches a category override, that category wins
   - Labels take precedence over issue type

4. **Epic name override** (if category not yet overridden by label AND `parent_key` is non-empty):
   - Fetch parent issue using the Fetch Parent protocol
   - If parent type is "Epic", compare parent summary against `config.maintenance_epic_patterns`
   - If summary matches any pattern (case-insensitive substring match), override category to `maintenance`

5. **Pre-decomposed detection** (if category is still not overridden):
   - If issue type is "Story" AND `acceptance_criteria` field is non-empty → set category to `pre-decomposed`

6. If no match found, default to `enhancement`

7. Return: `{ category: "feature" }`

## Phase 2 Write Protocols

### Post Summary

Called by `handoff-back` Step 3.

**Input:** `ticket_key`, `summary` (markdown string)

**Procedure:**

1. Load the Atlassian MCP tool:
   ```
   ToolSearch(query: "select:mcp__claude_ai_Atlassian__addCommentToJiraIssue")
   ```
2. Post the summary as a comment:
   ```
   mcp__claude_ai_Atlassian__addCommentToJiraIssue(
     issueIdOrKey: ticket_key,
     body: summary
   )
   ```
3. Return `{ posted: true }` on success

**On error:** Return `{ posted: false, error: error_message }`. Non-blocking.

### Transition Status

Called by `handoff-back` Step 3.

**Input:** `ticket_key`, `target_status` (e.g., "Done")

**Procedure:**

1. Load the transitions tool:
   ```
   ToolSearch(query: "select:mcp__claude_ai_Atlassian__getTransitionsForJiraIssue")
   ```
2. Get available transitions:
   ```
   mcp__claude_ai_Atlassian__getTransitionsForJiraIssue(issueIdOrKey: ticket_key)
   ```
3. Find a transition whose `name` matches one of the "done" statuses from config (`integrations.jira.config.status_mapping.done`). If no config, look for "Done", "Closed", or "Resolved".
4. If a matching transition is found:
   ```
   ToolSearch(query: "select:mcp__claude_ai_Atlassian__transitionJiraIssue")
   mcp__claude_ai_Atlassian__transitionJiraIssue(
     issueIdOrKey: ticket_key,
     transitionId: matched_transition.id
   )
   ```
5. Return `{ transitioned: true, new_status: matched_transition.name }`

**On error:**
- No matching transition found → Return `{ transitioned: false, error: "No transition to Done status available" }`
- Transition fails → Return `{ transitioned: false, error: error_message }`
- Non-blocking in both cases.

### Link Artifact

Called by `handoff-back` Step 3.

**Input:** `ticket_key`, `artifact_url` (string), `artifact_title` (string)

**Procedure:**

1. This protocol uses the Jira remote issue links API. Since the Atlassian MCP may not expose a direct "add remote link" tool, check for available tools:
   ```
   ToolSearch(query: "+atlassian remote link")
   ```
2. If a remote link tool is available, add the link.
3. If no tool is available, include the artifact link in the summary comment instead (append to the comment from Post Summary).
4. Return `{ linked: true }` or `{ linked: false, fallback: "included_in_comment" }`

**On error:** Non-blocking. Log and continue.

## Error Handling

| Scenario | Behavior |
|----------|----------|
| MCP not available | Return error with setup guidance |
| Issue not found (404) | Return `not_found` error |
| Permission denied | Return `forbidden` error |
| Rate limited | Return `rate_limited` error with retry guidance |
| Description in ADF format | Best-effort conversion to plain text |
| Custom fields missing | Use `null` for missing fields, continue |
| Story points in custom field | Try common custom field IDs (`customfield_10016`) |
| Comment post fails | Return error, non-blocking |
| Transition not available | Return error with available transitions, non-blocking |
| Remote link tool missing | Fall back to including link in comment |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2.1 | 2026-03-09 | Configurable custom fields (story_points, acceptance_criteria); epic name override for maintenance routing; pre-decomposed detection for Stories with AC; generalized config schema with maintenance_epic_patterns. |
| 1.1.0 | 2026-02-20 | S4-104 Phase 2: Added write protocols — Post Summary (addComment), Transition Status (transitionJiraIssue), Link Artifact (remote links with fallback). |
| 1.0.0 | 2026-02-20 | Initial release — S4-104 Phase 1: Fetch Ticket, Fetch Parent, Categorize protocols (read-only) |
