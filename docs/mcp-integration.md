# MCP Integration Guide

> Connect Sigil to external tools like Jira, Slack, and Confluence.

> **Audience:** This guide is for advanced users and developers who want to connect Sigil to external services.

---

## Overview

Sigil can connect to external tools through **MCP** (Model Context Protocol — a standard way to link AI assistants to outside services). These connections are **optional**. Sigil works fully without them.

MCP lets Claude access project trackers, wikis, chat tools, and more. You add a connection once, and Sigil uses it automatically during your workflow.

---

## Integration Points

### Overview Table

| Integration | Agent | Skill | Purpose | Status |
|-------------|-------|-------|---------|--------|
| Jira | Orchestrator | jira, ticket-loader | Route tickets through the right workflow | Setup Required |
| Confluence/Notion | Business Analyst | spec-writer | Publish specs to wiki | Available |
| Context7 | Architect | researcher | Access documentation context | Available |
| CI/CD (GitHub Actions, etc.) | DevOps | deploy-checker | Trigger/monitor pipelines | Available |
| Sentry/DataDog | QA Engineer | qa-validator | Access error monitoring | Available |

---

## Jira Integration

Sigil's Jira integration does more than sync tasks — it reads your tickets and routes them to the right workflow automatically. A Story with acceptance criteria goes directly to implementation; a chore labeled `tech-debt` goes to Quick Flow.

### Prerequisites

1. Atlassian MCP configured in Claude Code:
   ```bash
   # The Atlassian MCP is available via claude.ai — enable it in Settings > Integrations
   # or add it manually to your Claude Code MCP config
   ```
2. Access to your Jira instance

### Step 1: Find Your Custom Field IDs

Jira uses custom field IDs that vary between instances. You need two:
- **Story Points** — usually `customfield_10016` but check yours
- **Acceptance Criteria** — your instance may not have this field at all

**How to find your field IDs:**

Option A — Jira Admin (requires admin access):
1. Go to Jira Settings → Issues → Custom Fields
2. Click the field name to see its ID in the URL

Option B — Raw API response (any user):
1. Open `https://your-instance.atlassian.net/rest/api/3/issue/PROJ-1` in a browser (replace PROJ-1 with any ticket)
2. Search for "customfield_" in the response — the field name nearby will tell you which is which

### Step 2: Copy the Config Template

Copy `sigil-plugin/integrations/jira.yaml` to your shared context repo:

```
your-org/platform-context/
└── integrations/
    └── jira.yaml
```

Or inline it under `integrations.jira:` in `.sigil/config.yaml` for project-specific overrides.

### Step 3: Fill In Your Values

```yaml
config:
  project_key: ENG          # Your team's Jira project key

  custom_fields:
    story_points: "customfield_10016"   # From Step 1
    acceptance_criteria: "customfield_13505"  # From Step 1, or "" if unused
```

Also update `status_mapping` if your statuses don't match the defaults, and add any `maintenance_epic_patterns` your org uses for tech debt epics.

### Step 4: Push and Test

1. Commit and push `integrations/jira.yaml` to your shared context repo
2. Run `/sigil:draw PROJ-123` with a real ticket key
3. Sigil will show which workflow it selected:
   - Maintenance ticket → Quick Flow
   - Story with AC → Implement-Ready chain
   - Feature/Bug → Standard track

### Understanding Ticket Routing

When you run `/sigil:draw PROJ-123`, Sigil categorizes the ticket:

| Category | When | Workflow |
|----------|------|----------|
| `maintenance` | Label matches `maintenance_epic_patterns`, or label is tech-debt/chore, or parent epic summary matches | Quick Flow |
| `pre-decomposed` | Story type + non-empty acceptance criteria field | Implement-Ready chain (skips spec writing — AC is the spec) |
| `bug` | Bug/Defect type | Standard track (capped, no Enterprise) |
| `feature` / `enhancement` | Everything else | Normal routing via complexity assessment |

**What `pre-decomposed` means:** When a story already has acceptance criteria written out in Jira, Sigil treats it as ready to implement without going through the full spec-writing and clarification phases. The AC becomes the spec, and the story is treated as a single task.

**What `maintenance` means:** Maintenance work skips the spec phase entirely and goes straight to Quick Flow — a lighter, faster workflow for chores, refactors, and tech debt.

### Team Config Hook

If your team works across multiple repos, the `load-team-config` hook can automatically detect which team is working on a repo and set routing defaults.

**Setup:** Create `.sigil/team-config.yaml`:

```yaml
teams:
  - name: platform
    patterns: ["platform-*", "*-api", "*-infra"]
    team_id: "your-jira-team-id"
    board_id: "123"
  - name: mobile
    patterns: ["*-mobile", "*-ios", "*-android"]
    team_id: "another-team-id"
    board_id: "456"
```

The hook runs at session start, matches the current repo name against the patterns, and writes `sigil_team`, `sigil_team_id`, and `sigil_board_id` to `.sigil/config.yaml`. These values are then available to Jira queries and status reporting.

**Pattern matching:** Patterns use glob syntax — `*` matches any characters. Matches are checked against both the repo name and the git remote URL.

---

## Confluence/Notion Integration

### Purpose

Publish specifications and documentation to your team wiki automatically.

### Integration Points

| Agent | Skill | Action |
|-------|-------|--------|
| Business Analyst | spec-writer | Publish spec to wiki |
| Architect | technical-planner | Publish plan to wiki |
| Security | security-reviewer | Publish security report |

### Configuration

```json
{
  "mcp_server": "confluence",
  "config": {
    "base_url": "https://your-instance.atlassian.net/wiki",
    "space_key": "DOCS",
    "parent_page": "Feature Specifications",
    "template_mapping": {
      "spec": "Feature Specification Template",
      "plan": "Implementation Plan Template"
    }
  }
}
```

### Workflow Enhancement

**Without MCP:**
```
Spec created → /.sigil/specs/###/spec.md (local only)
Team access → Must check repository
```

**With MCP:**
```
Spec created → spec.md AND Confluence page
Team access → Wiki link shared automatically
```

---

## Context7 Integration

### Purpose

Provide architects with rich documentation context during planning.

### Integration Points

| Agent | Skill | Action |
|-------|-------|--------|
| Architect | researcher | Query documentation |
| Architect | technical-planner | Access API references |

### Configuration

```json
{
  "mcp_server": "context7",
  "config": {
    "libraries": [
      "react",
      "next.js",
      "prisma"
    ],
    "priority": "stable_versions"
  }
}
```

### Workflow Enhancement

**Without MCP:**
```
Architect researches → Web search, manual docs lookup
```

**With MCP:**
```
Architect researches → Direct access to indexed documentation
```

---

## CI/CD Integration

### Purpose

Trigger and monitor deployment pipelines from Sigil.

### Integration Points

| Agent | Skill | Action |
|-------|-------|--------|
| DevOps | deploy-checker | Check pipeline status |
| DevOps | — | Trigger deployment |
| QA Engineer | qa-validator | Run CI checks |

### Configuration

```json
{
  "mcp_server": "github",
  "config": {
    "repo": "owner/repo",
    "workflows": {
      "test": "test.yml",
      "deploy_staging": "deploy-staging.yml",
      "deploy_production": "deploy-production.yml"
    }
  }
}
```

### Workflow Enhancement

**Without MCP:**
```
DevOps checks → Manual pipeline inspection
Deployment → Manual trigger
```

**With MCP:**
```
DevOps checks → Automated status from GitHub Actions
Deployment → Triggered through MCP with approval
```

---

## Error Monitoring Integration

### Purpose

Access application error data during QA and debugging.

### Integration Points

| Agent | Skill | Action |
|-------|-------|--------|
| QA Engineer | qa-validator | Check for runtime errors |
| Developer | — | Access error context |

### Configuration

```json
{
  "mcp_server": "sentry",
  "config": {
    "organization": "your-org",
    "project": "your-project",
    "environment": "staging"
  }
}
```

---

## Setting Up MCP

### What You Need

1. Claude Code with MCP support turned on
2. An MCP server for the service you want to connect (e.g., Jira, Slack)
3. Login credentials for that service (API key or token)

### How to Connect a Service

1. **Install the MCP server** for your service.
   ```bash
   # Example: install the Context7 documentation server
   npm install -g @anthropic/mcp-server-context7
   ```

2. **Tell Claude Code about the server.** Add it to your settings file.
   ```json
   // .claude/mcp-config.json
   {
     "servers": {
       "context7": {
         "command": "mcp-server-context7",
         "args": []
       }
     }
   }
   ```

3. **Add your credentials.** Use environment variables — never put passwords in files.

4. **Test the connection.** Start Claude Code and verify the server responds.

You should now see the service listed when you check your MCP connections.

### Sigil-Specific Configuration

Add MCP preferences to your project context:

```markdown
<!-- /.sigil/project-context.md -->

## MCP Integrations

| Service | Status | Purpose |
|---------|--------|---------|
| Jira | Active | Task tracking |
| Confluence | Active | Documentation |
| Context7 | Active | Research |
```

---

## Behavior Without MCP

Sigil is designed to work fully without MCP integrations:

| Feature | Without MCP | With MCP |
|---------|-------------|----------|
| Task tracking | Local `tasks.md` | Local + Jira/Linear |
| Documentation | Local markdown | Local + Confluence |
| Research | Web search | Web + Context7 |
| CI/CD | Manual commands | Automated triggers |
| Notifications | Local status | Local + Slack/Teams |

**Key Principle:** MCP enhances but never replaces core functionality.

---

## Security

### How Data Flows

```
Sigil → MCP Server → External Service
            ↑
     Credentials required
```

Data only flows outward when an MCP server is set up. Without MCP, nothing leaves your machine.

### Best Practices

1. **Give least access** — Only grant the permissions each service needs
2. **Use environment variables** — Never put credentials in files
3. **Review before sending** — Require human approval for sensitive data
4. **Keep local copies** — MCP adds to your local files, never replaces them

> **Warning:** Never send API keys, personal data, security findings, or business secrets to external services.

---

## Troubleshooting

### MCP Server Not Connecting

1. Verify MCP server is installed and running
2. Check configuration file syntax
3. Verify credentials are set
4. Check network connectivity

### Data Not Syncing

1. Verify API permissions
2. Check rate limits
3. Review MCP server logs
4. Verify field mapping

### Integration Conflicts

1. Check for duplicate IDs
2. Verify status mapping
3. Review sync timing

---

## Related Documents

- [Context Management](dev/context-management.md) — Project state
- [Error Handling](dev/error-handling.md) — Integration errors
- [Skills README](../skills/README.md) — Skill catalog
