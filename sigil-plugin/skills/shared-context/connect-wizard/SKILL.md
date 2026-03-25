---
name: connect-wizard
description: Interactive setup flow for connecting a project to a shared context repository via GitHub MCP.
version: 1.4.0
category: shared-context
chainable: false
invokes: [shared-context-sync]
invoked_by: [connect]
tools: Read, Write, Bash, ToolSearch, mcp__github__get_file_contents, mcp__github__create_or_update_file, mcp__github__push_files
model: sonnet
---

# Skill: Connect Wizard

## Purpose

Guide users through connecting their project to a shared context repository. Handles GitHub MCP detection, repo validation, directory scaffolding, and sentinel file creation.

## Critical Constraint

**NEVER use `git clone`, `git commit`, `git push`, `git pull`, `git fetch`, or any git write/remote operations.** The only permitted git commands are read-only local queries: `git rev-parse`, `git remote get-url`, and `git config`. ALL remote repository operations — reading files, creating files, scaffolding, validation — MUST go through GitHub MCP tools (`mcp__github__get_file_contents`, `mcp__github__create_or_update_file`, `mcp__github__push_files`). If MCP is unavailable, fail gracefully rather than falling back to git CLI.

## When to Invoke

When the user runs `/sigil:connect` or says "connect to shared context", "set up shared context", "share learnings across projects", etc.

## Inputs

**Mode:** `interactive` (no arguments) or `direct` (repo path provided)

**For direct mode:**
- `repo_path`: `owner/repo` format string

## Process: Interactive Mode

### Step 1: Introduction

Display:
```
Shared Context Setup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sigil can share learnings and project context across
your code projects. This helps when you work on more
than one project — like a frontend and backend, or
mobile and web apps.

Do you work across multiple code projects? [Y/n]:
```

If user says no → exit with: "No problem. You can run `/sigil:connect` anytime if you change your mind."

### Step 2: GitHub MCP Check

Use the `shared-context-sync` skill's GitHub MCP Detection procedure.

**If MCP detected:**
```
Step 1 of 3: GitHub Connection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Checking... GitHub MCP detected.
```

**If MCP not detected:**
```
Step 1 of 3: GitHub Connection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Checking... GitHub MCP not found.

Sharing context requires a GitHub connection (MCP).
Want me to help you set that up? [Y/n]:
```

If yes, display the setup guidance from `shared-context-sync` MCP Detection, then ask user to restart their session and run `/sigil:connect` again.

If no → exit with: "You'll need GitHub MCP to use shared context. Run `/sigil:connect` when you're ready."

### Step 3: Repository Selection

```
Step 2 of 3: Shared Context Repository
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Have you already created a shared context repo
on GitHub? [y/N]:
```

**If yes:**
```
Enter the repo path (e.g., my-org/platform-context):
>
```

**If no:**
```
No problem. Create a new repository on GitHub:
  1. Go to github.com/new
  2. Name it something like "platform-context"
  3. Make it private (recommended)
  4. Come back here with the path

Enter the repo path (e.g., my-org/platform-context):
>
```

### Step 4: Validate and Connect

1. Validate repo path format: must be `owner/repo`
2. Attempt to read from the repo via GitHub MCP to confirm access
3. If repo is empty or missing expected structure → offer to scaffold (see Scaffolding below)
4. If repo is not accessible → show error and allow retry

### Step 5: Scaffold (if needed)

If the repo is empty or doesn't have the shared context structure:

```
This repo is empty. Set up the shared context structure? [Y/n]:
```

If yes, use the `shared-context-sync` Scaffolding Protocol, which creates all files in a single commit via `mcp__github__push_files`:
- `README.md` — auto-generated explanation of the repo's purpose
- `shared-standards/.gitkeep`
- `profiles/.gitkeep`
- `learnings/.gitkeep`

**README.md content:**
```markdown
# Shared Context

This repository stores shared learnings, project profiles, and organizational
standards for use across code projects via [Sigil OS](https://github.com/araserel/sigil-os).

## Structure

- `learnings/` — Per-project learnings (patterns, gotchas, decisions)
- `profiles/` — Per-project profiles (tech stack, APIs, dependencies)
- `shared-standards/` — Organization-level standards

## How it works

Projects connect to this repo using `sigil connect`. After connecting:
- Learnings sync automatically when you use `/sigil:learn`
- Latest shared context loads automatically at session start

Each project's learnings are stored in a subdirectory named after the project.
```

### Step 6: Create Sentinel

Use the `shared-context-sync` skill's Write Sentinel Entry procedure:
1. Detect current project identity (repo identity from git remote)
2. Write/update `~/.sigil/registry.json` with the new project entry
3. Initialize local cache structure if needed

### Step 7: Shared Standards Integration

After connecting, invoke the Standards Discover protocol from `shared-context-sync` to check for available standards (which now include `enforcement` level).

**If no standards found:** Skip silently — no standards to integrate yet.

**If standards found AND constitution exists** (`/.sigil/constitution.md` is present):

1. Group standards by enforcement level and display:
   ```
   Your team has shared standards available:

   Required (auto-applied):
     🔒 security-standards.md → Article 4: Security Mandates

   Recommended:
     📋 accessibility.md → Article 7: Accessibility Standards
     📋 coding-conventions.md → Article 2: Code Standards

   Informational (reference only):
     ℹ️  style-guide.md
   ```

2. **Apply by enforcement level:**
   a. **Required** (`enforcement: required`) — auto-apply without asking. These are organization mandates.
      - For each required standard with an `article_mapping`:
        - Read the corresponding article from the constitution
        - Insert `<!-- @inherit: shared-standards/{filename} -->` marker at the start of the article content
        - If existing local content differs significantly from the standard (>70% overlap): remove the local content to avoid duplication
        - If existing local content covers different topics than the standard (<70% overlap): move it to a `### Local Additions` section below the end marker
        - Insert `<!-- @inherit-start -->` / `<!-- @inherit-end -->` block with the standard content
      - Show: `Applied N required standard(s) automatically.`

   b. **Recommended** (`enforcement: recommended`) — ask user:
      ```
      Apply recommended standards to your constitution? [Y/n]:
      ```
      - If yes: apply same process as required standards above
      - If no: skip, show: "You can apply these later with /sigil:connect."

   c. **Informational** (`enforcement: informational`) — mention only, do not apply:
      ```
      Informational standards are available for reference in
      your shared repo. They are not added to your constitution.
      ```

3. After applying any standards:
   a. Invoke the Standards Expand protocol to write the updated constitution
   b. Run Discrepancy Detection and present any blocking or warning conflicts to the user for resolution

**If standards found AND no constitution exists:**

```
Your team has shared standards available. They will be
applied automatically when you run /sigil:setup to create
your project constitution.
```

### Step 8: Integration Discovery

After standards integration, invoke the Integration Discovery Protocol from `shared-context-sync` to check for org-level tool adapter configs.

**If no integrations found:** Skip silently.

**If integrations found:**

1. Display available adapters with MCP availability status:
   ```
   External Tool Integrations
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Your team has tool integrations available:
     ✅ Jira — MCP connected, ready to use
     ⚠️  Linear — MCP not configured (optional)
   ```

2. For each adapter where MCP tools are available:
   a. Fetch org-level default config from the adapter
   b. Write defaults to `.sigil/config.yaml` under `integrations:` key:
      ```yaml
      integrations:
        jira:
          project_keys: [PROJ, TEAM]
          status_mapping:
            done: ["Done", "Closed"]
            in_progress: ["In Progress", "In Review"]
      ```
   c. Show: `Imported org defaults for {adapter name}.`

3. For adapters where MCP is not available:
   ```
   To enable {adapter name}, configure the {MCP server} MCP server.
   You can do this later — the integration will activate automatically.
   ```

### Step 9: Confirmation

```
Step 3 of 3: Confirm
---------------------

Shared context is now active:
  - Repository: {owner/repo}
  - Learnings sync when you use /sigil:learn
  - Latest context loads automatically at session start
  - Integrations: {N configured, M available}
  - This project: {current-project-identity}

To disconnect later, remove this project's entry
from ~/.sigil/registry.json (or delete the file).

Ready to go.
```

---

## Process: Direct Mode

When invoked with a repo path (e.g., `sigil connect my-org/platform-context`):

1. Skip Steps 1-3 (introduction, MCP check prompt, repo selection prompt)
2. Still perform MCP check silently — if MCP not available, show error and guidance
3. Proceed directly to Step 4 (validate and connect) with the provided repo path
4. Continue through Steps 5-9 as normal

---

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Invalid repo path format | "Repo path should be `owner/repo` (e.g., `my-org/platform-context`)." Allow retry. |
| Repo not accessible via MCP | "Could not reach `{repo}`. Check that the repository exists and you have access." Allow retry. |
| MCP write fails during scaffold | "Could not set up the repo structure. Check your write access to `{repo}`." |
| Git not initialized | Caught by `/sigil:connect` pre-checks, not this skill. |
| No git remote | Caught by `/sigil:connect` pre-checks, not this skill. |
| Already connected | Caught by `/sigil:connect`, shows current config and asks to update. |
| MCP permission denied | "Could not write to shared repo. Ask your admin for write access to `{repo}`." |

---

## Outputs

**On success:**
- `~/.sigil/registry.json` created/updated with project entry
- `~/.sigil/cache/shared/` directory structure initialized
- Shared repo scaffolded (if empty)

**Handoff data:**
```json
{
  "connected": true,
  "shared_repo": "my-org/platform-context",
  "project_identity": "my-org/web-app",
  "scaffolded": true,
  "shared_standards_available": true,
  "shared_standards_applied": true,
  "standards_applied": ["security-standards.md", "accessibility.md"],
  "discrepancies_found": 0,
  "integrations_discovered": ["jira"],
  "integrations_configured": ["jira"],
  "integrations_unavailable": []
}
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.4.0 | 2026-02-20 | S4-103: Integration discovery — new Step 8 discovers org-level adapter configs, checks MCP availability, imports defaults. Previous Step 8 (Confirmation) renumbered to Step 9. |
| 1.3.0 | 2026-02-20 | S4-101: Enforcement-aware standards integration — Step 7 groups standards by enforcement level. Required standards auto-apply, recommended standards prompt user, informational standards mentioned only. |
| 1.2.0 | 2026-02-20 | Active standards integration — Step 7 now offers to apply shared standards to existing constitutions with @inherit markers, handles duplication detection, runs discrepancy detection |
| 1.1.0 | 2026-02-09 | Added MCP tool specifics to scaffolding and standards discovery, references shared-context-sync protocols |
| 1.0.0 | 2026-02-09 | Initial release — interactive and direct connection flows |
