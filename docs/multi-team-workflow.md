# How Sigil Works Across Teams and Projects

This guide explains how Sigil shares learnings, standards, and project context across multiple code projects through a shared GitHub repository.

## The Big Picture

Sigil connects product decisions, engineering knowledge, and project standards. Shared context lets all of this flow between projects without manual copying.

```mermaid
flowchart TD
    subgraph SharedRepo["Shared Context Repo (GitHub)"]
        LEARN["learnings/"]
        PROF["profiles/"]
        STD["shared-standards/"]
    end

    subgraph RepoA["Repo A: Web App"]
        CONST_A["Constitution"]
        MEM_A["Local Memory"]
    end

    subgraph RepoB["Repo B: API Server"]
        CONST_B["Constitution"]
        MEM_B["Local Memory"]
    end

    MEM_A <-->|"push / pull via MCP"| LEARN
    MEM_B <-->|"push / pull via MCP"| LEARN
    STD -->|"@inherit"| CONST_A
    STD -->|"@inherit"| CONST_B
```

<!-- Alt text: A diagram showing a shared context repo on GitHub with learnings, profiles, and shared-standards directories. Two project repos (Web App and API Server) push and pull learnings via MCP. Shared standards flow into each repo's constitution via @inherit markers. -->

## How Product People and Engineers Collaborate

Product people use Sigil to build a working prototype. Engineers take over to connect real services, clean up code, and handle edge cases.

```mermaid
flowchart TD
    subgraph Product["Product Person builds prototype"]
        P1["`**1.** Describe feature`"]
        P2["`**2.** Answer questions`"]
        P3["`**3.** Review spec`"]
        P4["`**4.** Build prototype`"]
        P5["`**5.** Validate & review`"]
        P6["`**6.** Create handoff`"]
        P1 --> P2 --> P3 --> P4 --> P5 --> P6
    end

    P6 --> HP["Handoff Package"]

    subgraph Engineering["Engineers finish the project"]
        E1["`**7.** Review handoff`"]
        E2["`**8.** Connect services`"]
        E3["`**9.** Fix UI/UX gaps`"]
        E4["`**10.** Final validation`"]
        E1 --> E2 --> E3 --> E4
    end

    HP --> E1

    E4 -->|"learnings captured"| SR["Shared Context Repo"]
    SR -->|"available to all"| E5["Next session, any project"]
```

<!-- Alt text: A top-down flow with two swim lanes. The product person describes, clarifies, specs, builds, validates, and hands off. The engineer reviews, connects services, fixes gaps, and validates. Learnings flow into the shared context repo, available to anyone in any project. -->

### What the product person does

1. Describe the feature in plain language.
2. Answer Sigil's clarifying questions.
3. Review and approve the spec.
4. Use Sigil to build a functional prototype.
5. Validate and review the prototype.
6. Create a handoff package for engineering.

### What the engineer does

1. Review the handoff package and prototype.
2. Connect the prototype to real backend services.
3. Fix UI/UX issues that the prototype couldn't resolve.
4. Implement remaining features and run final validation.

Every learning discovered during this work is captured and pushed to the shared repo.

## How Shared Context Works

Each person's learnings sync through a shared GitHub repository accessed via GitHub MCP. No external databases or services needed.

### What gets shared

| Category | Example | Who benefits |
|----------|---------|-------------|
| Patterns | "Use React Query's onMutate for optimistic updates" | Anyone starting similar work |
| Gotchas | "DataGrid slows with more than 10,000 rows" | Anyone about to hit the same wall |
| Decisions | "Using Flexbox for the sidebar layout" | Anyone who needs to understand past choices |
| Project Profiles | "API Server exposes /users and /auth endpoints" | Anyone whose project depends on another |

### How syncing happens

```mermaid
flowchart LR
    subgraph SessionA["Engineer A's session"]
        CAPTURE["`Runs **/sigil-learn**`"]
    end

    CAPTURE -->|"push via MCP"| REPO[("Shared Repo")]
    CAPTURE -->|"writes locally"| LOCAL["Local files"]

    REPO -->|"pull via MCP"| SessionB["`Engineer B **starts a session**`"]

    SessionB --> READY["Sees 'what's new' summary"]
```

<!-- Alt text: Engineer A runs /sigil-learn, which pushes to the shared repo via MCP and writes locally. The shared repo delivers the learning when Engineer B starts a session, showing a what's new summary. -->

Key details:

- Learnings push to the shared repo the moment they are captured via `/sigil-learn`. No waiting.
- When anyone starts a new session, shared learnings load automatically.
- A "what's new" summary shows what was added since your last session.
- If GitHub MCP is unreachable, Sigil works normally with local memory and a cached copy of shared learnings. It syncs when the connection returns.
- Failed pushes queue locally and replay automatically on the next session start.

### Project profiles

Each project can publish a profile describing its tech stack, exposed APIs, consumed dependencies, and optional sections for databases, auth model, domain glossary, and project structure. Run `/sigil-profile` to create one.

- Profiles publish to the shared repo's `profiles/` directory automatically.
- When you start a session, sibling profiles load so Sigil knows what other projects expose.
- If your plan changes an API that another project consumes, Sigil warns you during planning.

This is especially useful for teams where one project (like an API server) exposes endpoints that other projects (like a web app or mobile app) consume.

### Automatic gotcha surfacing

When you start work, Sigil loads shared learnings from all connected projects. If someone already hit a problem related to your work, you see the warning before you start.

> **Tip:** One person hitting a bug can save every future session from the same mistake, across all projects connected to the same shared repo.

## How Shared Standards Work

Your project's constitution (the rules that guide how Sigil works) can inherit organizational standards stored in the shared repo. Standards are applied automatically during setup and connection, and refreshed every session.

### The @inherit pattern

When a shared standard applies to an article in your constitution, Sigil writes it using `@inherit` markers:

```markdown
# Constitution: web-app

## Article 1: Technology Stack
[repo-specific content]

## Article 4: Security Mandates

<!-- @inherit: shared-standards/security-standards.md -->
<!-- @inherit-start: shared-standards/security-standards.md -->
- All API endpoints must require authentication
- Use environment variables for secrets
- Input validation on all user-facing forms
- Dependency review required before adding new packages
<!-- @inherit-end: shared-standards/security-standards.md -->

### Local Additions
- Rate limit all public endpoints to 100 req/min
```

### How it works

- Shared standards live in the `shared-standards/` directory of the shared repo.
- During `/sigil-setup` and `/sigil-connect`, Sigil discovers available standards and writes `@inherit` markers into the constitution automatically.
- At every session start, Sigil pulls the latest version of each referenced standard and replaces the content between `@inherit-start` and `@inherit-end` markers. This keeps your constitution current with upstream changes.
- The `@inherit` directive line is always preserved. Content outside the start/end markers — including the article heading and `### Local Additions` section — is never modified.
- If the shared repo is unreachable, Sigil keeps the previously expanded content and logs a warning. Your session continues normally.
- If a referenced standard file does not exist yet, Sigil inserts a `<!-- @inherit-pending -->` marker until the file becomes available.

### Enforcement levels

Each shared standard can be tagged with an enforcement level that controls how strictly it's applied:

| Level | Icon | Behavior |
|-------|------|----------|
| **Required** | 🔒 | Auto-applied. Blocks your session if missing from your constitution. |
| **Recommended** | 📋 | Applied by default during setup. Conflicts show warnings. You can opt out. |
| **Informational** | ℹ️ | Available for reference. Not added to your constitution. |

Standard authors set the enforcement level in the file's frontmatter:

```markdown
---
enforcement: required
---
# Security Standards
...
```

If no level is set, the standard defaults to **recommended**.

### Discrepancy detection

After expanding standards, Sigil checks for conflicts between inherited and local content:

- **Weaker thresholds:** Your local rule sets a lower bar than the shared standard (e.g., 60% coverage vs. 80% required).
- **Contradictory flags:** The standard marks something as "required" but your local rule marks it as "optional."
- **Direct contradictions:** Your local rule says the opposite of the shared standard.

How Sigil handles discrepancies depends on the standard's enforcement level:

- **Required** standards: conflicts block your session until resolved. You must either update your local rule or request a formal waiver.
- **Recommended** standards: conflicts show a warning. You can update the local rule, log a waiver, or skip for now.
- **Informational** standards: conflicts are logged silently — no interruption.

### What this means for your team

- A new project gets your organization's standards immediately during setup.
- When a security rule changes, one update in the shared repo reaches every project on the next session start.
- Each project can still add its own rules in the `### Local Additions` section.
- Required standards ensure critical rules (security, compliance) can't be accidentally skipped.
- Recommended standards provide guidance without blocking — teams can tailor where appropriate.
- Conflicts between shared and local rules are flagged automatically — no more silent drift.

## How Claude Code's Built-In Memory Fits In

Claude Code has automatic Session Memory. It overlaps with some of what Sigil provides.

### Where Sigil adds value

| Need | Claude Code alone | With Sigil shared context |
|------|------------------|--------------------------|
| Personal session recall | Session Memory handles this | Same, plus structured context |
| Cross-project knowledge sharing | Not supported | Shared repo synced via MCP |
| Cross-repo standards | Manual CLAUDE.md copying | Shared standards with @inherit |
| Gotcha prevention | Not supported | Automatic loading from shared learnings |
| Starting a new project | Start from zero | Get all shared learnings on first session start |

## Putting It All Together

Here is how a typical week looks for a team using Sigil with shared context:

**Monday:** Sara (PM) describes a new feature in the web app repo. Sigil writes the spec, asks questions, and Sara answers them. Sara builds a working prototype.

**Tuesday:** Sara validates the prototype and creates a handoff package. Alex (engineer) opens the same repo. `/sigil` loads the latest shared learnings. Alex reviews the handoff and starts connecting to real services.

**Wednesday:** Jordan (engineer) opens the API server repo to build a related endpoint. `/sigil` loads Alex's learnings from yesterday. Sigil warns: "Alex discovered that the DataGrid component slows above 10,000 rows. Consider virtualization." Jordan avoids the issue entirely.

**Thursday:** The team updates shared security standards in the shared repo. Every project picks up the new rules on next `/sigil`.

**Friday:** A new engineer joins. They clone a repo, run `sigil connect my-org/platform-context`, then `/sigil`. They immediately have access to every shared learning. No onboarding doc needed.

## Getting Started

1. Run `/sigil-connect` to set up shared context for your project.
2. See the [Shared Context Setup Guide](shared-context-setup.md) for detailed instructions.

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Shared learnings not loading | Shared context not set up | Run `/sigil-connect` to activate shared context |
| Constitution missing inherited standards | @inherit markers not expanded | Run `/sigil` to pull and expand shared standards |
| Learnings not syncing | GitHub MCP unreachable | Check MCP connection. Learnings queue locally and sync on next `/sigil` |
| New project missing shared learnings | Not connected to shared repo | Run `/sigil-connect my-org/platform-context` |
