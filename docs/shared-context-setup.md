# Shared Context Setup Guide

Share learnings and standards across your code projects through a shared GitHub repository.

## What You Need

Before you start, make sure you have:

1. **A GitHub account** with access to create repositories.
2. **GitHub MCP** connected to Claude Code. If you are not sure, `/sigil-connect` will check for you and guide you through setup.
3. **A git repository** with a remote set for each project you want to connect.

## Step 1: Create a Shared Repository

Create a new repository on GitHub to hold your shared context.

1. Go to [github.com/new](https://github.com/new).
2. Name it something like `platform-context` or `shared-context`.
3. Make it **private** (recommended).
4. Add a short description (optional).
5. Click **Create repository**.

You should now see an empty repository on GitHub.

> **Tip:** If you are a solo developer with multiple projects, you can use the same shared repo for all of them. Teams can also share one repo across all their projects.

## Step 2: Connect Your Project

Open your project in Claude Code and run:

```
/sigil-connect your-username/platform-context
```

Replace `your-username/platform-context` with the path to your shared repo.

Sigil will:
- Check that GitHub MCP is available
- Verify access to the shared repo
- Set up the directory structure (if the repo is empty)
- Create a local connection file at `~/.sigil/registry.json`

You should now see a confirmation message with your shared repo and project details.

> **Note:** If GitHub MCP is not configured, Sigil will walk you through setting it up. Follow the on-screen instructions, then restart Claude Code and run `/sigil-connect` again.

## Step 3: Verify the Connection

Run `/sigil` to see the status dashboard. It should show:

```
Shared Context: Connected
  Repo: your-username/platform-context
  Queued: 0 pending syncs
```

Context loads automatically at session start. If the repo is new, there won't be any shared learnings yet.

You should now see shared context status in your session output.

## Step 4: Connect Additional Projects

Repeat Step 2 for each project you want to share context between.

1. Open the next project in Claude Code.
2. Run `/sigil-connect your-username/platform-context`.

Each project gets its own entry in `~/.sigil/registry.json`. All projects connected to the same shared repo share learnings.

## How It Works After Setup

### Learnings sync automatically

- When you capture a learning (via `/sigil-learn` or during task completion), it writes locally **and** pushes to the shared repo.
- When you start a session, the latest shared learnings load automatically.
- A "what's new" summary shows any new entries since your last session.

### Project profiles sync too

Run `/sigil-profile` to create a project profile. It describes your tech stack, what your project exposes (APIs, events, packages), and what it consumes from other projects. Optional sections cover databases, API surface, auth model, domain glossary, and project structure.

- When you create or update a profile, it publishes to the shared repo's `profiles/` directory.
- When you start a session, profiles from connected projects load automatically.
- If your plan changes something another project depends on, Sigil warns you during planning.

> **Tip:** Profiles work even without shared context. In solo mode, `/sigil-profile` still generates a local profile that gives Sigil better understanding of your project.

### Offline support

If GitHub MCP is unreachable (network down, MCP not running):
- Learnings and profiles save locally and queue for later sync.
- Cached shared learnings and sibling profiles load from your last successful pull.
- Queued items sync automatically on your next session start.

### Shared standards

The `shared-standards/` folder in your shared repo holds organization-level rules that apply across all your projects. These are things like security policies, accessibility requirements, coding conventions, or compliance mandates — anything that should be consistent everywhere, not just in one project.

Shared standards are applied **automatically** — you do not need to add markers by hand.

**Adding standards:**

Create markdown files directly in the `shared-standards/` directory of your shared repo on GitHub. For example:
- `shared-standards/security-standards.md` — Authentication rules, data handling policies
- `shared-standards/accessibility.md` — WCAG compliance requirements
- `shared-standards/coding-conventions.md` — Naming patterns, file organization rules
- `shared-standards/api-guidelines.md` — API versioning, error format standards

Each file should contain the rules in plain language. Sigil agents read and follow them just like local constitution rules.

**How standards reach your project:**

Standards flow into your project's constitution automatically at three points:

1. **During `/sigil-setup`:** If you connect to shared context during setup, Sigil discovers available standards and writes them directly into your constitution using `@inherit` markers.
2. **During `/sigil-connect`:** If your project already has a constitution, Sigil offers to apply available standards to the matching articles.
3. **At every session start (`/sigil`):** Sigil pulls the latest version of each standard from the shared repo and refreshes the content in your constitution. If a standard changed upstream, your project picks it up automatically.

**What it looks like in your constitution:**

```markdown
## Article 4: Security Mandates

<!-- @inherit: shared-standards/security-standards.md -->
<!-- @inherit-start: shared-standards/security-standards.md -->
[content from shared standard — auto-managed by Sigil, do not edit between these markers]
<!-- @inherit-end: shared-standards/security-standards.md -->

### Local Additions
- Rate limit all public endpoints to 100 req/min
```

The content between `@inherit-start` and `@inherit-end` is managed by Sigil — it gets refreshed from the shared repo every session. Your project-specific rules go in the `### Local Additions` section below, which Sigil never touches.

**Enforcement levels:**

Each shared standard can have an enforcement level set by whoever maintains the shared repo. There are three levels:

| Level | What it means | What happens |
|-------|--------------|--------------|
| **Required** | Must be adopted — no exceptions without a waiver | Auto-applied during setup and connection. If missing from your constitution, Sigil blocks the session until you apply it or request a waiver. |
| **Recommended** | Should be adopted — you can opt out | Sigil asks during setup and connection. If your local rules conflict, you see a warning with options to update, waive, or skip. |
| **Informational** | Reference material — not enforced | Available in the shared repo for reading. Not added to your constitution. |

To set an enforcement level, the standard file in the shared repo should include a YAML frontmatter block at the top:

```markdown
---
enforcement: required
---

# Security Standards

Your rules here...
```

If no enforcement level is set, Sigil treats the standard as **recommended** by default.

**Discrepancy detection:**

If your local rules conflict with a shared standard (for example, the standard requires 80% test coverage but your local rule says 60%), Sigil flags the discrepancy and handles it based on the enforcement level:

- **Required** standard conflict: blocks you from proceeding until resolved.
- **Recommended** standard conflict: shows a warning with options to update, waive, or skip.
- **Informational** standard conflict: silent (no warning shown).

**External tool integrations:**

If your shared repo has an `integrations/` directory with adapter configs (e.g., `jira.yaml`), Sigil discovers them during setup or connection. These adapters let you start features from tickets in external tools like Jira — just run `/sigil PROJ-123` with a ticket key instead of typing a feature description.

**Why this matters:**

- Update a standard once in the shared repo, and every connected project picks it up on the next session start.
- New projects get your organization's standards immediately during setup.
- Each project can still add its own rules on top of shared ones. The `### Local Additions` section is yours to edit freely.
- Conflicts between shared and local rules are detected automatically, with severity matching the standard's importance.
- External tool configs are shared across teams so everyone uses the same setup.

For more details on the @inherit pattern, see the [Multi-Team Workflow Guide](multi-team-workflow.md#how-shared-standards-work).

## Disconnecting

To disconnect a project from shared context:

1. Open `~/.sigil/registry.json` in a text editor.
2. Remove the project's entry from the `projects` map.
3. If no projects remain, delete the file.

There is no `/disconnect` command. The connection file contains no secrets — just a repo path.

## Troubleshooting

### "GitHub MCP not found"

GitHub MCP is not configured in your Claude Code session.

**Fix:** Run this in your terminal:
```
claude mcp add-json -s user github '{"type":"http","url":"https://api.githubcopilot.com/mcp","headers":{"Authorization":"Bearer YOUR_GITHUB_PAT"}}'
```
Replace `YOUR_GITHUB_PAT` with a GitHub personal access token. Then restart Claude Code.

### "Could not reach the shared repo"

The repository doesn't exist or you don't have access.

**Fix:** Check that the repo path is correct (`owner/repo`) and that your GitHub token has access to the repository.

### "Could not write to shared repo"

You have read access but not write access.

**Fix:** Ask the repository owner to grant you write access, or use a GitHub token with the `repo` scope.

### Learnings not appearing in other projects

Learnings may not have synced yet.

**Fix:** Start a new session in the other project to pull the latest shared learnings. Check `/sigil-learn` to see if any items are queued.

### "Shared context unavailable, using cached data"

GitHub MCP failed during the pull. Sigil is using the last cached copy.

**Fix:** This is expected during network issues. Sigil continues working normally. The cache updates on your next successful session start.
