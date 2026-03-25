# Glossary

Plain-English definitions for terms used in Sigil. If a word sounds technical, you'll find it here.

---

## Workflow Terms

| Term | What It Means |
|------|---------------|
| **Acceptance Criteria** | The checklist a feature must pass to be considered done |
| **Clarification** | A question-and-answer round that removes confusion from requirements |
| **Constitution** | Your project's rulebook — the standards that all features must follow |
| **Entity** | A type of data your app stores, like a User, Product, or Order |
| **Functional Requirement** | A specific thing the system must do (e.g., "show a login form") |
| **Handoff** | A package of documents passed to engineers so they can start building |
| **Non-Functional Requirement** | How well the system must work — speed, security, or accessibility |
| **Phase** | One stage of the workflow: Assess, Specify, Clarify, Plan, Tasks, Implement, or Review. (Validation runs automatically within the Implement phase after each task.) |
| **Specification (Spec)** | A written plan that describes what a feature should do — the "what," not the "how" |
| **Track** | The workflow path Sigil picks based on size: Quick (small), Standard (medium), or Enterprise (large) |
| **User Scenario** | A short story: "As a [person], I want to [do something] so that [benefit]" |

---

## Priority and Status Terms

| Term | What It Means |
|------|---------------|
| **P1 / P2 / P3** | How important something is: P1 = must have, P2 = should have, P3 = nice to have |
| **Blocker** | A problem that stops all progress until someone fixes it |
| **Human Checkpoint** | A pause in the workflow where Sigil waits for your approval before continuing |

---

## Technical Terms

| Term | What It Means |
|------|---------------|
| **API Endpoint** | A web address where your app sends or receives data — like a mailbox for software |
| **CLI** | Command Line Interface — the text-based window where you type commands |
| **Lint / Format** | Tools that check and fix code style automatically — like spell-check for code |
| **Plugin** | An add-on that gives a program new features (Sigil is a plugin for Claude Code) |
| **QA Loop** | An automatic fix-and-check cycle that runs up to 5 times before asking for help |
| **Repository (Repo)** | A folder tracked by Git (version control software) that stores your project's history |
| **WCAG** | Web Content Accessibility Guidelines — the international standard for making websites usable by everyone, including people with disabilities. Sigil targets WCAG AA (the middle level) by default. |

---

## Configuration Terms

| Term | What It Means |
|------|---------------|
| **Personal Config** | Your personal settings stored in `.sigil/config.yaml`. This file is gitignored — each team member has their own. Contains user track, execution mode, and audit mode. |
| **User Track** | A personal setting that controls how Sigil communicates with you: `non-technical` (plain English, auto-decides technical details) or `technical` (shows implementation details, trade-offs, and specialist names) |
| **Execution Mode** | A personal setting that controls how specialists are selected: `automatic` (Sigil chooses) or `directed` (you choose, requires technical track) |
| **Audit Mode** | An optional setting that logs every workflow step to `.sigil/audit-log.md`. Useful for reviewing what happened after a workflow completes. Enable with `/sigil:config set audit_mode true`. |
| **Audit Log** | The file (`.sigil/audit-log.md`) that records workflow events when audit mode is enabled. View with `/sigil:audit`. |
| **Specialist** | A domain-specific overlay that customizes a base agent's behavior for a particular type of work (e.g., an API Developer specialist makes the Developer agent focus on API contracts and backwards compatibility) |
| **Base Agent** | One of the 9 core agents (like Developer or QA Engineer) that a specialist extends with domain-specific behavior |
| **Specialist Selection** | The process of matching a task to the most appropriate specialist based on what files it touches and what it's about |

---

## Sigil-Specific Terms

| Term | What It Means |
|------|---------------|
| **Agent** | An AI specialist that handles one type of work (e.g., Business Analyst, QA Engineer) |
| **Chain** | A sequence of skills that run together to complete a workflow |
| **Orchestrator** | The central agent that reads your request and sends it to the right specialist |
| **Skill** | A single, reusable ability an agent can use (e.g., "write a spec" or "check code quality") |

---

## Shared Context Terms

| Term | What It Means |
|------|---------------|
| **Shared Context** | A system that syncs learnings and standards across multiple code projects through a shared GitHub repository |
| **Shared Repo** | A GitHub repository that stores learnings and standards shared between projects (e.g., `my-org/platform-context`) |
| **Sentinel File** | The local connection file (`~/.sigil/registry.json`) that maps your projects to their shared repo |
| **Shared Standards** | Organizational rules stored in `shared-standards/` in the shared repo. Applied automatically to project constitutions during setup, connection, and session start via `@inherit` markers |
| **@inherit** | A marker in your constitution (e.g., `<!-- @inherit: shared-standards/security.md -->`) that tells Sigil to pull in standards from the shared repo. Applied automatically during setup and connection — you do not need to add these by hand |
| **@inherit-start / @inherit-end** | Markers that bracket the auto-managed content from a shared standard. Content between these markers is refreshed from the shared repo at every session start. Do not edit content between these markers — use the `### Local Additions` section below them instead |
| **@inherit-pending** | A placeholder marker inserted when a constitution references a shared standard file that does not exist yet in the shared repo. Replaced automatically when the file is created |
| **Discrepancy Detection** | An automatic check that runs after standards are expanded. Flags conflicts between shared standards and local rules — for example, a shared standard requiring 80% test coverage while the local rule says 60% |
| **Enforcement Level** | A tag on a shared standard that controls how strictly it's applied: **required** (must adopt, blocks if missing), **recommended** (suggested, shows warnings on conflict), or **informational** (reference only, not added to constitution). Set in the standard file's frontmatter. Defaults to recommended if not specified |
| **Required Standard** | A shared standard with enforcement level "required" — your organization mandates this rule. It's auto-applied during setup and connection, and missing it blocks your session until resolved |
| **Recommended Standard** | A shared standard with enforcement level "recommended" — suggested but optional. Applied by default but you can opt out. Conflicts show warnings, not blocks |
| **Informational Standard** | A shared standard with enforcement level "informational" — available for reference in the shared repo but not added to your constitution. No warnings or blocks |
| **Integration Adapter** | A configuration that connects Sigil to an external tool (like Jira or Linear). Stored in the shared repo's `integrations/` directory and imported to your project during setup or connection |
| **Ticket-Driven Entry** | Starting a Sigil workflow from an external ticket (e.g., `/sigil:draw PROJ-123` instead of describing a feature in plain text). Sigil fetches the ticket details, categorizes the work type, and routes it through the appropriate workflow |
| **Ticket Loader** | The skill that fetches ticket data from an external tool, enriches it with parent/epic context, categorizes the work type, and hands the enriched context to the main workflow |
| **Ticket Key** | The identifier for a ticket in an external tool (e.g., `PROJ-123` for Jira). Follows the pattern of uppercase letters followed by a dash and numbers |
| **Override** | A temporary exception to a constitution rule, recorded in `/.sigil/waivers.md`. Overrides have an expiration date (or are permanent) and affect how QA validation and code review handle findings for the overridden article. Expired overrides revert to the original rule automatically |
| **Handoff-Back** | The automatic process of updating the originating external ticket after a feature completes. Posts a summary comment, transitions the ticket status, and links artifacts. Only happens for ticket-driven workflows |
| **Adapter Write Protocol** | The part of an integration adapter that writes data back to external tools (posting comments, transitioning statuses, linking artifacts). Write protocols are always non-blocking — failures produce warnings, not halts |
| **Offline Queue** | When the shared repo is unreachable, learnings save locally and sync automatically on your next session start |
| **Project Profile** | A YAML file (`.sigil/project-profile.yaml`) that describes your project's tech stack, exposed APIs, consumed dependencies, and sibling relationships — used by agents for context and cross-repo impact warnings |
| **Profile: Databases** | Optional profile section listing the datastores the project depends on (e.g., PostgreSQL, Redis) with a brief description of each store's purpose |
| **Profile: API Surface** | Optional profile section describing the exposed route modules or endpoint groups, with path prefixes and brief descriptions |
| **Profile: Auth Model** | Optional profile section describing the project's authentication and authorization approach — type (JWT, OAuth2, session, etc.), description, and user roles |
| **Profile: Domain Glossary** | Optional profile section defining project-specific business terms that have meanings unique to this project (e.g., "Listing" means something specific here) |
| **Profile: Project Structure** | Optional profile section annotating key top-level directories with brief descriptions of what each one contains or does |

---

*Don't see a term? Check the [User Guide](user-guide.md) or [Command Reference](command-reference.md).*
