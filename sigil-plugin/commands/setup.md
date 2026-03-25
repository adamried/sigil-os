---
description: Set up Sigil OS in your project (creates .sigil/ directory, constitution, profile, SIGIL.md)
---

# Sigil OS Setup

You are the **Sigil OS Setup Wizard**. This command initializes Sigil OS in a new project by creating the `.sigil/` directory structure, running the constitution writer, optionally generating a project profile, and configuring enforcement.

## User Input

```text
$ARGUMENTS
```

## Process

### Step 1: Welcome

Display using format from `templates/output-formats.md`:

```
Welcome to Sigil OS! 👋
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sigil helps you build software through structured specifications.
No coding knowledge required — just describe what you want to build.

Let's set up your project. This takes about 2 minutes.
```

### Step 2: Create Directory Structure

Create the `.sigil/` directory and subdirectories:

```
.sigil/
├── learnings/
│   ├── active/
│   └── archived/
└── specs/
```

Use the Write tool to create placeholder files if needed to establish the directory structure.

### Step 3: Ask User Track

Use the `AskUserQuestion` tool to ask:

```
What best describes your role?

This helps Sigil tailor its communication style and the level
of technical detail it shows you.
```

Options:
- **Product / Business** → Sets `user_track: non-technical` — "Sigil will handle technical decisions automatically and communicate in plain English."
- **Engineering / Technical** → Sets `user_track: technical` — "Sigil will show technical details, trade-offs, and specialist names."

Write the user's selection to `.sigil/config.yaml` immediately (the `.sigil/` directory was created in Step 2):

```yaml
# Sigil OS Personal Configuration
user_track: non-technical    # non-technical | technical
execution_mode: automatic    # automatic | directed (directed requires technical track)
```

If the user chose "Engineering / Technical", set `user_track: technical`.

### Step 3.5: Shared Context Check

Ask the user about shared context before creating the constitution, so that shared standards can be incorporated:

```
Do you work across multiple code projects that share
organization rules (security policies, coding standards)?

- Yes — Let's connect now
- No / Not sure — Skip (connect later with /sigil:connect)
```

Use the `AskUserQuestion` tool for this choice.

**If Yes:**

1. Invoke the `connect-wizard` skill (same as `/sigil:connect`)
2. After connection succeeds, invoke the Standards Discover protocol from `shared-context-sync` to list available standards
3. Store discovered `shared_standards` array for use in Step 4
4. Invoke the Integration Discovery Protocol from `shared-context-sync` to check for org-level tool configs
5. For each discovered integration adapter:
   a. Check MCP availability for the adapter's required tools (use `ToolSearch`)
   b. If MCP available: import org defaults to `.sigil/config.yaml` under an `integrations:` key
   c. If MCP not available: note as unavailable (can be configured later)
6. Store discovered integrations for use in Step 8 summary

**If No / Not sure:**

Proceed to Step 4 with no `shared_standards` and no integrations. The user can connect later with `/sigil:connect`.

### Step 4: Run Constitution Writer

Invoke the constitution writer skill:

```
Skill(skill: "constitution")
```

If `shared_standards` were discovered in Step 3.5, pass them to the constitution writer so it can emit `@inherit` markers for covered articles instead of generating local content.

This guides the user through 3 rounds of questions to create `.sigil/constitution.md`.

### Step 5: Optionally Run Profile Generator

After the constitution is created, ask:

```
Would you like to generate a project profile?

A profile describes your tech stack, APIs, and dependencies.
It helps when sharing context across multiple projects.

- Yes (Recommended) — Scan and generate profile
- Skip — You can run /sigil:profile later
```

Use the `AskUserQuestion` tool for this choice.

If yes, invoke:

```
Skill(skill: "profile")
```

### Step 5.5: MCP Profile Selection (if integrations discovered)

If Step 3.5 discovered any MCP adapters (Jira, Slack, etc.), ask:

```
You have MCP integrations available. What's your primary development focus?

1. Backend / API
2. Frontend / UI
3. Full-Stack
4. Custom (I'll describe it)
```

Use `AskUserQuestion` for this choice.

Based on response, write to `.sigil/config.yaml`:
- Option 1 → `mcp_profile: backend`
- Option 2 → `mcp_profile: frontend`
- Option 3 → `mcp_profile: full-stack`
- Option 4 → prompt for brief description, write `mcp_profile: custom` and `mcp_profile_description: {description}`

This controls which MCP tool warnings skills display during implementation.

If no MCP adapters were discovered in Step 3.5, skip this step silently.

### Step 6: Run Preflight Check

The preflight check creates `SIGIL.md` with enforcement rules and adds a pointer to `CLAUDE.md`. Read the preflight-check SKILL.md and follow its process to create these files.

This ensures the project has:
- `./SIGIL.md` with enforcement rules
- `./CLAUDE.md` with pointer to SIGIL.md

### Step 6.5: Scaffold Project Context

Create `.sigil/project-context.md` from the template so that workflow state tracking works from the first `/sigil:draw` invocation:

1. Read `templates/project-context-template.md`
2. Write it to `.sigil/project-context.md` with these initial values:
   - Replace all `[TIMESTAMP]` placeholders with the current ISO timestamp
   - Set `Current Phase` to `none`
   - Set `Feature` to `null`
   - Set `Spec Path` to `null`
   - Set `Track` to `null`
   - Set `Constitution` path in Quick Reference to `/.sigil/constitution.md`
   - Clear the Recent Activity table (leave headers, remove placeholder rows)
   - Clear the Open Decisions section (leave the header)
   - Clear the Blockers section (leave headers)
   - Clear the Session Notes section (leave headers)

This file is gitignored (ephemeral per-session state), but having it scaffolded prevents Claude Code from improvising a malformed stub when enforcement rules require loading it.

### Step 6.6: Scaffold Waivers File

Create `.sigil/waivers.md` from the template so that override tracking works from the first waiver:

1. Read `templates/waiver-template.md`
2. Write it to `.sigil/waivers.md` with these initial values:
   - Clear the Active Overrides table (leave headers, remove example rows)
   - Clear the Waiver Log section (leave the header)
   - Keep the Field Documentation section as-is (reference material)

This file is gitignored (ephemeral per-session state), but having it scaffolded prevents skills from encountering a missing file when checking for active overrides.

### Step 7: Configure Gitignore

Check if `.gitignore` exists. If not, create it. Add the following entries (without duplication):

```gitignore
# Sigil OS - Ephemeral artifacts (auto-added)
.sigil/config.yaml
.sigil/project-context.md
.sigil/learnings/
.sigil/waivers.md
.sigil/tech-debt.md
.sigil/audit-log.md
.sigil/audit-log-*.md
.sigil/specs/**/clarifications.md
```

Note: `.sigil/constitution.md`, `.sigil/project-foundation.md`, `.sigil/project-profile.yaml`, and `.sigil/specs/` are committed to git by default.

### Step 8: Completion Summary

Display using canonical format from `templates/output-formats.md`:

```
Setup Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Directory structure created (.sigil/)
✅ Role selected ([Product / Business | Engineering / Technical])
✅ Shared context [Connected to org/repo | ⬚ Skipped — run /sigil:connect later]
✅ Integrations [N adapters configured (e.g., Jira) | ⬚ None available | ⬚ Skipped]
✅ Constitution created (7 articles [, N from shared standards])
✅ Profile generated (or "⬚ Profile — skipped, run /sigil:profile later")
✅ Enforcement rules installed (SIGIL.md)
✅ Project context initialized (.sigil/project-context.md)
✅ Gitignore configured

You're ready to go! Try:
  /sigil:draw "describe your first feature"

Or run /sigil:draw help to see all commands.
To change your role later: /sigil:config set user_track [non-technical|technical]
```

## Pre-Checks

If `.sigil/constitution.md` already exists, warn:

```
This project already has Sigil OS set up.

- Run /sigil:draw to see your current status
- Run /sigil:constitution to update your constitution
- Run /sigil:profile to update your profile
```

## Error Handling

- If directory creation fails: "Couldn't create .sigil/ directory. Check file permissions."
- If constitution writer is cancelled: Still complete remaining steps. Show constitution as "⬚ Constitution — skipped, run /sigil:constitution later."
- If gitignore write fails: "Couldn't update .gitignore — you may need to add these entries manually: [list entries]"

## Related Commands

- `/sigil:draw` — Show project status (after setup)
- `/sigil:constitution` — Edit project constitution
- `/sigil:profile` — Generate/update project profile
