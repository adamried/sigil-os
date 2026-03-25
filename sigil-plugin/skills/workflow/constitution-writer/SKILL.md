---
name: constitution-writer
description: Creates project constitution through guided conversation accessible to non-technical users. Uses tiered questions (auto-decide technical details, translate necessary questions, keep business decisions) with a maximum of 3 interaction rounds. Invoke when setting up a new project or when user says "constitution", "project principles", or "project setup". Can be pre-populated from project foundation or codebase assessment.
version: 2.3.0
category: workflow
chainable: true
invokes: []
invoked_by: [foundation-writer, orchestrator, codebase-assessment]
tools: Read, Write, Edit, Glob
---

# Skill: Constitution Writer

## Purpose

Guide users through creating their project constitution—the immutable principles that govern all agent decisions. Designed for non-technical users (product managers, founders, business stakeholders) with zero coding knowledge required. Technical details are auto-decided; user-facing questions use plain language.

## When to Invoke

- New project setup
- User requests `/sigil:constitution`
- User asks about "project principles" or "project rules"
- No constitution exists in `/.sigil/constitution.md`
- After Discovery chain completes (invoked by foundation-writer)

## Design Principles

### Tiered Question Strategy

All constitution questions are categorized into three tiers:

**Tier 1 — Auto-Decide (Never Ask User)**
Technical implementation details decided by Sigil based on detected stack and best practices:

| Topic | Auto-Decision Logic |
|-------|---------------------|
| TypeScript strictness | Always strict mode for TS projects |
| Naming conventions | Framework-appropriate (PascalCase components for React, etc.) |
| Import organization | Standard for detected framework |
| Error handling patterns | Best practices for stack |
| Architecture patterns | Framework defaults (feature folders for React, etc.) |
| Max file/function length | Sensible defaults (50 lines function, 300 lines file) |
| Code organization rules | Infer from detected stack |
| Type safety level | Strict for typed languages |
| Formatter config | Framework standard (Prettier for JS/TS, Black for Python, etc.) |
| Linter config | Framework standard (ESLint for JS/TS, Ruff for Python, etc.) |

**Tier 2 — Translate (Ask in Plain Language)**
Questions with user impact that need translation from technical to plain language:

| Technical Concept | Plain Language Version |
|-------------------|------------------------|
| Test coverage target | "How thoroughly should features be tested before you see them?" |
| Offline tolerance | "Should the app work when users have no internet?" |
| Testing requirements | "How much testing do you want before features ship?" |
| External service dependencies | "Should I ask before adding features that need external services (like payment processors or email senders)?" |
| Accessibility level | "Should this work for everyone, including people with disabilities?" |

**Tier 3 — Ask Directly (Business Decisions)**
Questions users can answer without technical knowledge:

| Question | Why Keep |
|----------|----------|
| Approval requirements | Users understand "Ask me before deleting files" |
| What requires sign-off | Direct business decision |
| Project type/rigor level | Users know if they're building an MVP or enterprise product |

### Maximum 3 Interaction Rounds

The setup flow MUST complete in 3 or fewer rounds. Never exceed this regardless of project complexity.

### "Why This Matters" Context

Every user-facing question includes a one-sentence explanation of real-world impact.

### Smart Defaults with Opt-Out

Replace open-ended questions with pre-configured defaults the user can accept or change.

## Inputs

**Required:**
- `project_name`: string — Name of the project

**Optional:**
- `tech_preferences`: object — Any known technology preferences
- `existing_constitution`: string — Path to existing constitution to update
- `user_track`: string — From `.sigil/config.yaml` (`non-technical` | `technical`)

**From Discovery Chain (when invoked by foundation-writer):**
- `foundation_path`: string — Path to approved foundation document
- `pre_populated_constitution`: object — Pre-filled data from Discovery

**From Assessment Path (when invoked by codebase-assessment):**
- `detected_stack`: object — Stack detected from codebase analysis
- `classification`: string — "scaffolded" | "mature"

**From Setup Path (when shared context is active):**
- `shared_standards`: array (optional) — Available shared standards from Standards Discover protocol, each with `filename`, `title`, `summary`, `article_mapping`, and `content`

## Process

### Step 0: Load Configuration

```
1. Read .sigil/config.yaml. If not found, use defaults.
2. Extract user_track value (default: non-technical)
3. Store for use throughout the flow
```

**User track branching:**
- **`non-technical` (default):** Current behavior — auto-decide all Tier 1 items silently, translate Tier 2 questions to plain language, keep 3-round maximum
- **`technical`:** Show Tier 1 auto-decisions for override opportunity ("I'll use strict TypeScript — want to change this?"), ask Tier 2 questions in technical framing ("What test coverage target? (default: 60%)"), add Round 3 technical questions: architectural pattern preference, test framework preference, CI/CD pipeline preference

### Step 0b: Check for Pre-Population Sources

```
Determine pre-population path (in priority order):

1. IF foundation_path provided:
   → Use Foundation Path (from Discovery chain)
   - Load /.sigil/project-foundation.md
   - Extract pre_populated_constitution data
   - Pre-fill stack information
   - Skip Round 1, go directly to Round 2

2. ELSE IF detected_stack provided:
   → Use Assessment Path (from codebase-assessment)
   - Use detected_stack for Round 1 pre-population
   - Show detection summary for user confirmation

3. ELSE IF no constitution exists AND repo appears established:
   → Invoke codebase-assessment first
   - Run assessment to detect stack
   - If stack detected, continue with Assessment Path
   - If no stack detected, fall through to Standard Path

4. ELSE:
   → Use Standard Path
   - Ask Round 1 with graceful stack question
```

### Step 0c: Check for Shared Standards

```
IF shared_standards provided (non-empty array):
  → Group standards by enforcement level:
    - required: Always emit @inherit markers (no user choice)
    - recommended: Default-include (user can skip individual ones)
    - informational: Skip — do not add to constitution
  → Map each included standard to its article via article_mapping
  → For mapped articles, plan to emit @inherit markers + expanded
    content instead of generating local content in Step 3
  → For standards with article_mapping = null, skip (user can
    add manually later)
  → Store the mapping (with enforcement levels) for use in Step 3
```

This check runs regardless of which pre-population path was selected above. Shared standards override generated content for their mapped articles. Required standards are always included; recommended standards are included by default but can be skipped during Round 3 if the user opts out; informational standards are never embedded.

### Step 1: Check for Existing Constitution

```
Check if /.sigil/constitution.md exists:

- If exists and not updating:
  Show: "This project already has a constitution. Would you like to
         view it, or start fresh?"
  Options: View current | Start fresh | Cancel

- If exists and updating: Load for modification

- If not exists: Proceed with new creation
```

### Step 2: Three-Round Guided Flow

#### Round 1: Stack Validation

**When stack detected (Assessment or Foundation path):**
```
I detected you're building with:
- Language: [detected]
- Framework: [detected]
- Database: [detected]

Is this correct? Anything to add or change?
```

**When stack NOT detected:**
```
I couldn't detect your tech stack automatically.
What are you building with?

A few questions:
- What programming language? (e.g., TypeScript, Python, Go)
- Using a framework? (e.g., Next.js, Django, Express)
- Using a database? (e.g., PostgreSQL, MongoDB, none yet)
```

**Error Case:** If detection fails entirely, show: "I couldn't detect your tech stack automatically. Let me ask a few questions instead." Then ask the above questions.

#### Project Category Detection (after Round 1)

Based on the detected/confirmed stack, classify the project into one of these categories. This determines which Round 3 questions are relevant:

| Category | Detection Criteria |
|----------|-------------------|
| **Backend API/Service** | Backend framework detected (Express, FastAPI, Django REST, Spring Boot, etc.) + no frontend framework |
| **Frontend/Fullstack** | Frontend framework detected (React, Next.js, Vue, Nuxt, Svelte, Angular, etc.) |
| **Mobile** | Mobile framework detected (React Native, Flutter, Swift/UIKit, Kotlin/Jetpack) |
| **CLI Tool** | No web or mobile framework; CLI libraries detected (Commander, Click, Cobra, etc.) |
| **Library/Package** | No application framework; library structure indicators (exports only, no app entry point) |

Store the detected category for use in Round 3 filtering.

#### Round 2: Project Type (Single Cascading Question)

**Use the `AskUserQuestion` tool** (not inline numbered lists) for this choice.

```
What kind of project is this?

Why this matters: This shapes how much testing, security checks,
and documentation I set up. You can always adjust later.

1. MVP / Prototype
   Ship fast, add polish later. Minimal testing, flexible structure.

2. Production App
   Balance speed with stability. Standard testing, proven patterns.

3. Enterprise
   Maximum rigor. Comprehensive testing, full documentation,
   strict reviews.
```

This single choice auto-configures ALL Tier 1 decisions:

| Setting | MVP | Production | Enterprise |
|---------|-----|------------|------------|
| Test coverage | Essential paths only | 60%+ coverage | 80%+ coverage |
| Test-first | Not required | For complex features | Required for all features |
| Security rigor | Standard best practices | Standard + auth review | Maximum + audit trail |
| Approval gates | Major changes only | Deps, DB, auth, deploys | All changes reviewed |
| Documentation | Light | Standard | Comprehensive |
| Code review | Optional | Required for key areas | Required for everything |
| E2E testing | Critical flows only | Key user journeys | All user flows |

#### Round 3: Optional Preferences (Context-Filtered)

**Use the `AskUserQuestion` tool** (not inline numbered lists) for all user choices in Round 3.

Filter questions based on the project category detected after Round 1:

| Question | Backend | Frontend | Mobile | CLI | Library |
|----------|---------|----------|--------|-----|---------|
| External services approval | Ask | Ask | Ask | Ask | Ask |
| Offline support | **Skip** | Ask | Ask | **Skip** | **Skip** |
| Accessibility (WCAG) | **Skip** | Ask | Ask | **Skip** | **Skip** |

**Always ask — External services:**
```
Should I ask before adding features that need external
services (like payment processors or email senders)?

Why this matters: External services may have costs or require
accounts to set up.

- Yes (Recommended): I'll flag these for your approval
- No: I'll add them as needed
```

**Ask only for Frontend, Mobile — Offline support:**
```
Should the app work when users have no internet?

Why this matters: Offline mode means users can access their data
with poor signal, but adds complexity.

- Yes: Works offline, syncs when connected
- No (Default): Requires internet connection
```

For skipped projects (Backend, CLI, Library): Auto-apply default "Requires internet connection."

**Ask only for Frontend, Mobile — Accessibility:**
```
How accessible should this be?

Why this matters: Accessibility ensures people with disabilities
can use your app. It's also a legal requirement in many countries.

- Works for everyone (Recommended): Follows accessibility
  standards so all users can participate
- Standard: Basic accessibility included
```

For skipped projects (Backend, CLI, Library): Mark Article 7 as "N/A — no user interface."

### Step 3: Auto-Configure and Generate

Using the project type selection + stack detection + optional preferences:

1. **Auto-decide all Tier 1 items** based on stack and project type
2. **Load template** from `/templates/constitution-template.md`
3. **Fill in all [BRACKETED] placeholders** in the template. Preserve EXACT article names (`Article 1: Technology Stack`, not `Tech Stack`), subsection names, and checkbox formatting. Do not restructure or rename any sections.

   **For articles WITHOUT a mapped shared standard:** Fill normally with:
   - Detected/confirmed stack (Article 1)
   - Auto-decided code standards with jargon translations (Article 2)
   - Project-type-appropriate testing (Article 3)
   - Stack-appropriate security with translations (Article 4)
   - Framework-standard architecture (Article 5)
   - Project-type-appropriate approvals (Article 6)
   - Selected accessibility level (Article 7)

   **For articles WITH a mapped shared standard** (from Step 0c):
   1. Keep the article heading (exact match from template)
   2. Emit `<!-- @inherit: shared-standards/{filename} -->` directive
   3. Emit `<!-- @inherit-start: shared-standards/{filename} -->` marker
   4. Insert the actual standard content (from `shared_standards` array)
   5. Emit `<!-- @inherit-end: shared-standards/{filename} -->` marker
   6. Add empty `### Local Additions` section below the end marker
   7. Do NOT generate additional content for this article — the shared standard is the source of truth

4. **Add inline jargon explanations** for all technical terms (including within expanded shared standard content)
5. **Write to** `/.sigil/constitution.md`

### Step 3b: Standards Integration Summary (if shared_standards provided)

Show the user which articles use shared standards (with enforcement levels) and which are locally generated:

```
Standards Integration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

From shared standards:
  🔒 Article 4: Security Mandates ← security-standards.md (required)
  📋 Article 7: Accessibility Standards ← accessibility.md (recommended)

Generated locally:
  📋 Article 1: Technology Stack
  📋 Article 2: Code Standards
  📋 Article 3: Testing Requirements
  📋 Article 5: Architecture Principles
  📋 Article 6: Approval Requirements

🔒 = required by your organization (cannot be removed)
📋 = recommended (can be customized or removed)

Want to add project-specific rules on top of any
inherited article? You can edit the "Local Additions"
sections in your constitution anytime.
```

Use the `AskUserQuestion` tool to ask if the user wants to add any project-specific additions now:
- **Looks good** — Proceed to Step 4
- **Add local rules** — For each inherited article, ask for any project-specific additions to place in the `### Local Additions` section

### Step 4: Gitignore Handling

**Auto-add (no prompt needed):**
```gitignore
# Sigil OS - Ephemeral artifacts (auto-added)
.sigil/project-context.md
.sigil/learnings/
.sigil/waivers.md
.sigil/tech-debt.md
.sigil/specs/**/clarifications.md
```

**Prompt user:**
```
Should your team share the project constitution via git?

Why this matters: If you work with a team, sharing the constitution
means everyone (and all AI tools) follow the same rules.

- Yes (Recommended for teams): Constitution is version controlled
- No (Solo projects): Constitution stays local only
```

Implementation:
- Check if `.gitignore` exists; create if not
- Append entries without duplication
- Use clear comment header: `# Sigil OS - Ephemeral artifacts`
- If user says No to sharing: also add `.sigil/constitution.md`

**Error case:** If gitignore write fails, show: "Couldn't update .gitignore — you may need to add these entries manually: [list entries]"

### Step 5: Confirm and Explain

Show a plain-language summary:

```
Your constitution is ready!

Here's what I set up:

**Tech Stack:** [Language] + [Framework] + [Database]

**Quality Level:** [Project Type]
- Testing: [plain description, e.g., "Key features tested before shipping"]
- Security: [plain description, e.g., "User data kept private, no secrets in code"]
- Reviews: [plain description, e.g., "I'll ask before adding new tools or changing the database"]

**Accessibility:** [plain description]

This is saved at /.sigil/constitution.md. All AI agents will follow
these rules automatically.

To change it later, run /sigil:constitution edit.
```

## Outputs

**Artifact:**
- `/.sigil/constitution.md` — Complete project constitution

**Handoff Data:**
```json
{
  "constitution_path": "/.sigil/constitution.md",
  "project_name": "Project Name",
  "project_type": "mvp|production|enterprise",
  "articles_completed": 7,
  "key_decisions": [
    "TypeScript as primary language",
    "Next.js framework",
    "PostgreSQL database",
    "Production-level testing and security"
  ]
}
```

## Project Type Cascade Details

### MVP / Prototype

Auto-configures:
- **Article 2 (Code Standards):** Framework defaults, relaxed complexity limits (100 lines function, 500 lines file), standard formatting
- **Article 3 (Testing):** Essential paths tested, no coverage mandate, test-first not required
- **Article 4 (Security):** Standard best practices (no secrets in code, validate user input, auth where needed)
- **Article 5 (Architecture):** Simple structure, pragmatic patterns, no strict layering
- **Article 6 (Approvals):** Major changes only (new services, breaking changes)
- **Article 7 (Accessibility):** Basic accessibility (keyboard nav, alt text, contrast)

### Production App

Auto-configures:
- **Article 2:** Strict formatting, moderate complexity limits (50 lines function, 300 lines file), type safety enforced
- **Article 3:** 60%+ coverage, integration tests for APIs, test-first for complex features, E2E for key flows
- **Article 4:** Auth required by default, environment variables for secrets, input validation, dependency review
- **Article 5:** Feature-based organization, service layer pattern, composition over inheritance
- **Article 6:** Dependencies, database changes, auth changes, and production deploys require approval
- **Article 7:** WCAG 2.1 AA minimum, keyboard navigation, screen reader support

### Enterprise

Auto-configures:
- **Article 2:** Strict formatting, strict complexity limits (30 lines function, 200 lines file), full type safety, comprehensive documentation
- **Article 3:** 80%+ coverage, all APIs tested, test-first required, E2E for all user flows, performance testing
- **Article 4:** All endpoints authenticated, secrets manager, audit trail, security review for all changes, vulnerability SLA
- **Article 5:** Strict layering, dependency injection, SOLID principles, documented architecture decisions
- **Article 6:** All code changes reviewed, architecture decisions require approval, deployment plans required
- **Article 7:** WCAG 2.1 AAA target, comprehensive assistive technology support, accessibility testing in CI

## Jargon Translation

When generating the constitution, include inline explanations for technical terms:

| Technical Term | Inline Explanation |
|----------------|-------------------|
| RLS (Row-Level Security) | (keeps each user's data private) |
| TypeScript strict mode | (catches more bugs before they reach users) |
| React Query | (handles loading and caching data) |
| Environment variables | (secure storage for passwords and API keys) |
| Functional components | (modern React pattern, easier to maintain) |
| E2E tests | (tests that simulate real user actions) |
| CI/CD | (automatic testing and deployment) |
| PascalCase | (naming style: MyComponent) |
| camelCase | (naming style: myFunction) |
| snake_case | (naming style: my_function) |
| ORM | (tool that simplifies database access) |
| JWT | (secure login tokens) |
| SOLID principles | (design guidelines for maintainable code) |
| Dependency injection | (pattern that makes code easier to test) |
| WCAG | (Web Content Accessibility Guidelines — the international standard) |
| ARIA | (attributes that help screen readers understand your app) |
| Parameterized queries | (prevents database attacks from user input) |
| Prettier | (automatic code formatting tool) |
| ESLint | (automatic code quality checker) |

**Format in constitution:**
```markdown
- TypeScript strict mode (catches more bugs before they reach users) enabled
- Row-Level Security (keeps each user's data private) enabled on ALL tables
```

## Error Handling

All errors shown to users MUST be plain language with actionable next steps. Log technical details for debugging; surface only the friendly message.

| Technical Error | User-Friendly Message |
|-----------------|----------------------|
| ENOENT / File not found | "I couldn't find [filename]. Make sure you're in the right project folder." |
| EACCES / Permission denied | "I don't have permission to modify [file]. You may need to check your folder permissions." |
| ETIMEDOUT / Network timeout | "Connection issues — couldn't reach [service]. Check your internet and try again." |
| JSON parse error | "The [filename] file has formatting issues. I'll try to fix it, or you can restore from backup." |
| Stack detection failed | "I couldn't detect your tech stack automatically. Let me ask a few questions instead." |
| Git operation failed | "Couldn't update .gitignore — you may need to add these entries manually: [list entries]" |
| Constitution already exists | "This project already has a constitution. Want to view it, or start fresh?" |
| Template not found | Use embedded fallback template (no user-facing error) |
| Foundation data conflicts | User input takes precedence (no error, just override) |
| Monorepo detected | "I found multiple tech setups in your project. Let me focus on the main one — you can adjust if needed." |

## Human Checkpoints

- **Review Tier:** Constitution creation (user reviews final document)
- User confirms stack in Round 1
- User selects project type in Round 2
- Final constitution shown for approval before saving

## Foundation Integration

When invoked from the Discovery chain (via `foundation-writer`):

### Pre-Population Behavior

| Data | Source | User Action |
|------|--------|-------------|
| Language, framework, database | Foundation document | Confirm in Round 1 (or skip if confident) |
| All technical details | Auto-decided from stack + project type | None — automatic |
| Project type | Asked in Round 2 | Select one option |
| Optional preferences | Asked in Round 3 | Answer or skip |

### Abbreviated Flow

When foundation data is available:
1. Show detected stack from foundation → User confirms (Round 1)
2. Ask project type (Round 2)
3. Ask optional preferences (Round 3)
4. Generate constitution with auto-decided technical details

## Assessment Path Integration

When invoked from `codebase-assessment`:

### Trigger Conditions

1. No `/.sigil/constitution.md` exists
2. No `/.sigil/project-foundation.md` exists
3. Codebase-assessment classifies repo as "scaffolded" or "mature"

### Assessment Path Flow

1. Show: "Analyzing your project..."
2. Present detected stack in plain language (Round 1)
3. Ask project type (Round 2)
4. Ask optional preferences (Round 3)
5. Generate constitution

### Handling Detection Issues

- **Uncertain fields:** Show what was found, ask user to clarify in plain language
- **Missing fields:** Ask gracefully: "I couldn't detect a database. Are you using one?"
- **Conflicting signals:** Show: "I found multiple [items]. Which one is your primary?"
- **Detection failure:** Fall back to friendly manual questions (no error shown)

## Backward Compatibility

- Existing constitutions in `/.sigil/constitution.md` continue to work unchanged
- The 7-article structure is preserved
- Only the creation flow changes — the output format stays the same
- Constitutions created by previous versions are fully valid

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-20 | Initial release |
| 1.1.0 | 2026-01-20 | Added Foundation integration, pre-population support |
| 1.2.0 | 2026-01-27 | Added Assessment Path integration for established repos |
| 2.3.0 | 2026-02-20 | S4-101: Enforcement-aware @inherit — required standards always included, recommended default-included (user can skip), informational never embedded. Step 3b displays enforcement icons and legend. |
| 2.2.0 | 2026-02-20 | Standards-aware generation — accepts `shared_standards` input, emits @inherit markers for articles with mapped shared standards, shows Standards Integration Summary (Step 3b), adds `### Local Additions` sections |
| 2.1.0 | 2026-02-19 | S3-100: Added user_track branching — technical track shows Tier 1 decisions for override, uses technical framing for Tier 2, adds Round 3 technical questions |
| 2.0.0 | 2026-01-29 | Non-technical user refactor: tiered questions, 3-round max, plain language, smart defaults, jargon translation, gitignore handling, friendly errors |
