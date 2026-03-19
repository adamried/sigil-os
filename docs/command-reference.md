# Command Reference

> Quick reference for all Sigil commands.

---

## Command Overview

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/sigil` | **Unified entry point** — status, start, resume | Starting any workflow |
| `/sigil-setup` | Initialize Sigil OS in a new project | First-time project setup |
| `/sigil-handoff` | Generate engineer review package | Ready for technical review |
| `/sigil-constitution` | View or edit project rules | First-time setup or updates |
| `/sigil-learn` | View, search, or review learnings | Reviewing institutional memory |
| `/sigil-connect` | Connect project to shared context repo | Multi-project sharing setup |
| `/sigil-profile` | Generate or view project profile | Describing your tech stack and APIs |
| `/sigil-config` | View or change configuration (user track, execution mode, audit mode) | Adjusting Sigil's behavior |
| `/sigil-audit` | View or manage the workflow audit log | Reviewing what happened in a workflow |
| `/sigil-update` | Check for and install Sigil updates | Keeping Sigil current |

---

## Command Flow

`/sigil` is the recommended entry point. It detects your project state and routes to the right phase automatically. All workflow phases (specification, clarification, planning, tasks, validation, review) are handled automatically by the orchestrator.

```
/sigil-setup (one-time project setup)
        ↓
/sigil "description" (start a feature — all phases run automatically)
        ↓
    Specify → Clarify → Plan → Tasks → Implement → Validate → Review
        ↓
    Next-action prompt: build another feature, hand off, or wrap up
```

After code review passes, Sigil offers your next step inline — including engineer handoff. You can also run `/sigil-handoff` independently at any time.

You can use `/sigil` or `/sigil status` at any point to see where you are.

---

## /sigil

The unified entry point for all Sigil workflows. This is the recommended way to interact with Sigil.

### Syntax

```
/sigil
/sigil "feature description"
/sigil PROJ-123
/sigil continue
/sigil status
/sigil help
```

### Variants

| Usage | What It Does |
|-------|-------------|
| `/sigil` | Show status dashboard and suggest next action |
| `/sigil "description"` | Start building a new feature from your description |
| `/sigil PROJ-123` | Start from an external ticket (Jira, etc.) — fetches ticket details and routes by work type |
| `/sigil continue` | Resume where you left off |
| `/sigil status` | Show detailed workflow status |
| `/sigil help` | Show all available commands |

### What It Does

1. Runs a **preflight check** to verify Sigil is installed correctly
2. Loads your project context from `project-context.md`
3. If shared context is active and your constitution has inherited standards, **pulls the latest standards** and refreshes them in your constitution. Flags any conflicts based on enforcement levels (required standards block, recommended standards warn).
4. **Checks for expired overrides** in `/.sigil/waivers.md` and warns about any that need attention.
5. Detects your current workflow state
6. Routes to the appropriate action:
   - No active workflow → Suggests starting one
   - Active workflow → Shows status and suggests next step
   - With a description → Starts the spec-first workflow
   - With a ticket key (e.g., `PROJ-123`) → Fetches ticket details and routes by work type:
     - `maintenance` tickets → Quick Flow
     - `pre-decomposed` stories (Stories with acceptance criteria) → Implement-Ready chain (skips spec writing — AC is the spec)
     - `bug` → Standard track
     - `feature`/`enhancement` → Normal routing
7. After a feature completes (code review passes):
   - If the feature came from a ticket, **automatically updates the ticket** with a summary and status transition
   - Presents a **next-action prompt**:
     - **Build another feature** — start a new spec immediately
     - **Hand off to an engineer** — generate a review package inline (same as `/sigil-handoff`)
     - **Update ticket and close** — (if ticket-driven) update the originating ticket
     - **Done for now** — wrap up the session

### Natural Language Alternatives

You don't need to remember the exact syntax. These all work:

| Instead of... | You can say... |
|---------------|----------------|
| `/sigil "Add login"` | "I want to add user login" |
| `/sigil PROJ-123` | "Work on PROJ-123" or "Pick up PROJ-123" |
| `/sigil status` | "What's the progress?" |
| `/sigil continue` | "Keep going" or "Next step" |
| `/sigil help` | "What can you do?" |

### When to Use

- **Every time you start a session** — `/sigil` orients you
- **Starting a new feature** — `/sigil "your description"`
- **Returning after a break** — `/sigil continue`

---

## /sigil-constitution

View or edit your project's rules and standards.

### Syntax

```
/sigil-constitution
```

### What It Does

1. If no constitution exists: Guides you through creating one
2. If constitution exists: Shows current rules and allows updates

### First-Time Setup

When you run `/sigil-constitution` for the first time, Sigil asks about:

1. **Technology Stack** — What languages and frameworks to use
2. **Code Standards** — Naming conventions and style rules
3. **Testing Requirements** — What level of testing is needed
4. **Security Mandates** — Authentication and data protection rules
5. **Architecture Principles** — Design patterns to follow
6. **Approval Requirements** — What needs human review
7. **Accessibility Standards** — Inclusivity requirements

### Example Session

```
Sigil: Let's set up your project constitution.
I'll ask a few questions about your preferences.

What programming language will this project use?
> TypeScript

What framework, if any?
> Next.js

What database will you use?
> PostgreSQL

...
```

### Expected Output

```markdown
# Project Constitution

## Article 1: Technology Stack
- **Language:** TypeScript
- **Framework:** Next.js
- **Database:** PostgreSQL

## Article 2: Code Standards
- All functions must have explicit return types
- Use camelCase for variables, PascalCase for components

## Article 3: Testing Requirements
- All API endpoints must have integration tests
- Minimum 60% code coverage

...
```

### When to Use

- **First time:** At project start, before any features
- **Updates:** When project standards need to change

### Why It Matters

The constitution ensures:
- Consistent decisions across all features
- AI agents follow your project's rules
- No need to repeat preferences

---

## /sigil-handoff

Generate a package for engineer review.

### Syntax

```
/sigil-handoff
```

### What It Does

1. Gathers all artifacts from your feature
2. Creates a summary document for technical review
3. Highlights any items needing engineer attention
4. Provides a plain-language summary you can share

### When to Use

- Before production deployment
- When you want an engineer to review the work
- When technical sign-off is required

### Example Output

```markdown
## Technical Review Package: Contact Form

### Quick Context
- **What:** Contact form for visitor messages
- **Why:** Enable customer support communication
- **Status:** Implementation complete, pending review

### What Was Built
| Artifact | Status |
|----------|--------|
| Specification | Complete |
| Implementation Plan | Complete |
| Code Changes | 3 files modified |
| Tests | All passing |

### Quality Summary
- Code Review: No issues found
- Security Review: Passed
- Test Coverage: 85%

### Items for Engineer Review
1. Email configuration in production
2. Rate limiting settings

### Files Changed
- components/ContactForm.tsx
- pages/api/contact.ts
- styles/contact.css
```

### What to Do With It

1. Share the package path with your engineer
2. Include the summary when you reach out
3. Wait for their feedback
4. Address any requested changes

### Plain-Language Summary

Sigil provides a summary you can copy:

> "This package has everything needed to review the contact form feature. It includes what we asked for, how it was built, and what the automated checks found. Please let me know if anything needs changing before we go live."

---

## /sigil-learn

View, search, or review project learnings.

### Syntax

```
/sigil-learn
/sigil-learn --review
/sigil-learn --search "query"
```

### Variants

| Usage | What It Does |
|-------|-------------|
| `/sigil-learn` | Show current learnings summary |
| `/sigil-learn --review` | Start interactive review and cleanup session |
| `/sigil-learn --search "query"` | Search learnings for specific topics |

### What It Does

1. **Default:** Shows a summary of active learnings across all categories (patterns, gotchas, decisions, feature notes)
2. **Review mode:** Walks you through learnings to promote, archive, or prune
3. **Search:** Finds learnings matching your query

### When to Use

- After completing a feature — review what was learned
- Starting a new feature — check relevant patterns
- Periodically — clean up with `--review`

### Expected Output

```markdown
## Active Learnings

### Patterns (12 active)
- Always validate form inputs server-side
- Use server actions for mutations in Next.js
- ...

### Gotchas (5 active)
- API rate limit is 100 requests/minute
- ...

### Recent Decisions (3)
- Chose PostgreSQL over MongoDB for relational data
- ...
```

---

## /sigil-connect

Connect your project to a shared context repository for cross-project learnings.

### Syntax

```
/sigil-connect
/sigil-connect org/repo
```

### Variants

| Usage | What It Does |
|-------|-------------|
| `/sigil-connect` | Start the guided setup wizard (3 steps) |
| `/sigil-connect org/repo` | Connect directly to a specific shared repo |

### What It Does

1. Checks that GitHub MCP is available
2. Validates access to the shared repository
3. Scaffolds the repo structure if empty (learnings, profiles, shared-standards)
4. Creates a local connection file at `~/.sigil/registry.json`
5. Discovers shared standards (with enforcement levels) and applies them to your constitution — required standards are auto-applied, recommended standards ask for confirmation
6. Discovers external tool integrations (e.g., Jira adapter) and imports org-level defaults

### After Connecting

- Learnings sync automatically when you use `/sigil-learn`
- Latest shared context loads automatically at session start
- A "what's new" summary shows entries added since your last session
- Shared standards refresh automatically at each session start
- External tool adapters are available for ticket-driven workflows (e.g., `/sigil PROJ-123`)

### When to Use

- Setting up cross-project sharing for the first time
- Connecting an additional project to an existing shared repo
- When you work on more than one code project

### Disconnecting

Remove the project's entry from `~/.sigil/registry.json` or delete the file. No separate disconnect command is needed.

### Related

- [Shared Context Setup Guide](shared-context-setup.md) — Full setup walkthrough
- [Multi-Team Workflow](multi-team-workflow.md) — How shared context works across teams

---

## /sigil-profile

Generate or view your project's profile — a description of your tech stack, exposed APIs, and consumed dependencies.

### Syntax

```
/sigil-profile
/sigil-profile --view
```

### Variants

| Usage | What It Does |
|-------|-------------|
| `/sigil-profile` | Interactive profile generation (or update if one exists) |
| `/sigil-profile --view` | Display the current project profile |

### What It Does

1. Scans your codebase for tech stack signals (package.json, Cargo.toml, go.mod, etc.)
2. Shows detected languages, frameworks, and tools for confirmation
3. Asks for a short project description
4. Optionally asks what APIs or events your project exposes and consumes
5. Optionally asks about databases, auth model, domain glossary, and project structure (Steps 7a–7e)
6. Generates `.sigil/project-profile.yaml`
7. If connected to shared context, publishes the profile for sibling projects to see

### Profile Sections

| Section | Required | Description |
|---------|----------|-------------|
| `name` | Yes | Repository/project name |
| `description` | Yes | Plain-language project summary |
| `tech_stack` | Yes | Languages, frameworks, infrastructure, testing |
| `exposes` | Yes | APIs, events, or packages this project provides |
| `consumes` | Yes | External services or APIs this project uses |
| `depends_on` | Yes | Sibling project dependencies |
| `contacts` | Yes | Owner and team contact info |
| `databases` | Optional | Data stores with names and purposes |
| `api_surface` | Optional | Route modules with path and description |
| `auth_model` | Optional | Auth type, description, and roles |
| `domain_glossary` | Optional | Project-specific business term definitions |
| `project_structure` | Optional | Key directory annotations |

### When to Use

- When setting up a new project
- After major tech stack changes
- When you want sibling projects to know about your APIs or events

### Example

```
/sigil-profile
```

**Sigil responds:**
```
Project Profile Setup
==============================

I scanned your project and found:

  Languages: TypeScript, CSS
  Frameworks: Next.js 14, React 18, Tailwind CSS
  Testing: Jest, Playwright
  Infrastructure: (none detected)

Look right? [Y/n]: y

What does this project do? (1-2 sentences)
> Customer-facing web application for product catalog and checkout

Profile saved: .sigil/project-profile.yaml
Published to shared repo: profiles/web-app.yaml
```

### After Creating a Profile

- Your profile loads into every session automatically
- Sibling projects see your profile on their next session start
- The architect agent warns you if your changes might affect projects that consume your APIs

### Related

- `/sigil-connect` — Connect to a shared repo to share profiles across projects

---

## /sigil-setup

Initialize Sigil OS in a new project.

### Syntax

```
/sigil-setup
```

### What It Does

1. Creates the `.sigil/` directory structure
2. Asks your role (Product/Business or Engineering/Technical) and saves to `.sigil/config.yaml`
3. Asks about shared context — if you work across multiple projects, connects to a shared repo and discovers organizational standards
4. Runs the constitution writer to set up project principles (with shared standards applied automatically if available)
5. Optionally generates a project profile
6. Creates `SIGIL.md` with enforcement rules
7. Adds a pointer to `CLAUDE.md`

### When to Use

- First time using Sigil in a project
- When `/sigil` detects no `.sigil/` directory and recommends setup

### What You Get

After setup completes:

```
.sigil/
├── config.yaml        ← Your personal settings (gitignored)
├── constitution.md    ← Your project's rules
├── project-context.md ← Workflow state tracker
└── learnings/         ← Empty, ready for use
SIGIL.md               ← Enforcement rules
CLAUDE.md              ← Updated with pointer
```

---

## /sigil-config

View or change your project's Sigil configuration.

### Syntax

```
/sigil-config
/sigil-config set <key> <value>
/sigil-config reset
```

### Variants

| Usage | What It Does |
|-------|-------------|
| `/sigil-config` | Show current settings and offer to change them |
| `/sigil-config set user_track technical` | Switch to technical mode |
| `/sigil-config set user_track non-technical` | Switch to non-technical mode |
| `/sigil-config set execution_mode directed` | Enable directed execution (technical track only) |
| `/sigil-config set audit_mode true` | Enable workflow audit logging |
| `/sigil-config set audit_mode false` | Disable workflow audit logging |
| `/sigil-config reset` | Reset all settings to defaults |

### Settings

| Setting | Options | Default | What It Controls |
|---------|---------|---------|-----------------|
| **User Track** | `non-technical`, `technical` | `non-technical` | Communication style, question depth, detail level |
| **Execution Mode** | `automatic`, `directed` | `automatic` | How specialists are selected (directed requires technical track) |
| **Audit Mode** | `true`, `false` | `false` | Whether workflow events are logged to `.sigil/audit-log.md` |

### User Track Details

**Non-Technical (default):**
- Plain English communication — no jargon or file paths
- Technical decisions made automatically with sensible defaults
- Progress shown as "3 of 8 steps done"
- Best for product managers, founders, and business stakeholders

**Technical:**
- Shows agent names, specialist names, and implementation details
- Surfaces technical trade-offs for your input
- Progress shown as "T003/T008 implementing (api-developer)"
- Best for engineers and technical leads

### When to Use

- After initial setup if you want to change your track
- When switching between non-technical and technical workflows
- To enable directed mode for manual specialist selection

---

## /sigil-audit

View or manage the workflow audit log.

### Syntax

```
/sigil-audit
/sigil-audit full
/sigil-audit session
/sigil-audit clear
```

### Variants

| Usage | What It Does |
|-------|-------------|
| `/sigil-audit` | Show summary of the most recent workflow session |
| `/sigil-audit full` | Show the complete audit log (all sessions) |
| `/sigil-audit session` | Show details for the current/most recent session only |
| `/sigil-audit clear` | Archive the current log and start fresh |

### What It Does

1. Reads the audit log at `.sigil/audit-log.md`
2. Displays workflow events — which phases ran, in what order, what decisions were made
3. Adapts detail level to your user track (plain language for non-technical, agent/skill names for technical)

### Prerequisites

Audit mode must be enabled first:

```
/sigil-config set audit_mode true
```

Once enabled, every `/sigil` workflow automatically logs events. Disable with `/sigil-config set audit_mode false`.

### When to Use

- After a workflow completes — review what happened step by step
- Debugging — understand why a specific decision was made
- Handoff — share the audit log with an engineer for context

### Related

- `/sigil-config` — Enable/disable audit mode

---

## /sigil-update

Check for and install Sigil OS updates.

### Syntax

```
/sigil-update
```

### What It Does

1. Checks the current installed version against the latest available
2. Reports what's new in the latest version
3. Guides you through the update process if an update is available

### When to Use

- Periodically to stay current
- When you encounter unexpected behavior
- When new features are announced

### Expected Output

```markdown
## Sigil OS Update Check

Current version: X.Y.Z
Latest version: X.Y.Z+1

### What's New
- [Summary of changes in latest version]

Run the update? (Y/n)
```

---

## Quick Reference Card

| Command | Purpose | Example |
|---------|---------|---------|
| `/sigil` | Entry point — status + routing | `/sigil "Add user login"` |
| `/sigil-setup` | Initialize project | `/sigil-setup` |
| `/sigil-handoff` | Engineer review | `/sigil-handoff` |
| `/sigil-constitution` | Set project rules | `/sigil-constitution` |
| `/sigil-learn` | View/review learnings | `/sigil-learn --review` |
| `/sigil-connect` | Shared context setup | `/sigil-connect org/repo` |
| `/sigil-profile` | Project profile | `/sigil-profile --view` |
| `/sigil-config` | Configure Sigil | `/sigil-config set user_track technical` |
| `/sigil-audit` | View audit log | `/sigil-audit` |
| `/sigil-update` | Check for updates | `/sigil-update` |

### Typical Workflow

```
1. /sigil-setup (one-time project setup)
2. /sigil "feature description" (all phases run automatically)
3. /sigil (check progress anytime)
4. /sigil continue (resume after a break)
5. /sigil-handoff (before deployment)
```

### Retired Commands

These commands have been removed. Use `/sigil` instead — it handles all workflow phases automatically.

| Old Command | What to Use Instead |
|-------------|-------------------|
| `sigil-spec` | `/sigil "description"` |
| `sigil-clarify` | `/sigil continue` (auto-invoked) |
| `sigil-plan` | `/sigil continue` (auto-invoked) |
| `sigil-tasks` | `/sigil continue` (auto-invoked) |
| `sigil-validate` | Runs automatically after each task |
| `sigil-review` | Runs automatically after all tasks pass |
| `sigil-status` | `/sigil` or `/sigil status` |
| `sigil-prime` | Context loads automatically at session start |

---

## Getting Help

- **"What should I do next?"** — Get guidance on next steps
- **"I'm stuck on..."** — Get help with a specific issue
- **"Explain..."** — Get clarification on any concept

---

## Related Documents

- [Quick-Start Tutorial](quick-start.md) — Learn by doing
- [User Guide](user-guide.md) — Comprehensive coverage
- [Troubleshooting](troubleshooting.md) — Common issues and solutions
