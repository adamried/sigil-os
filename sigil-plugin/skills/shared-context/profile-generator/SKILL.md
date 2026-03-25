---
name: profile-generator
description: Auto-detect project tech stack and interactively generate a project profile for cross-repo awareness.
version: 1.1.0
category: shared-context
chainable: false
invokes: [shared-context-sync]
invoked_by: [profile, orchestrator]
tools: Read, Write, Bash, Glob, Grep, mcp__github__get_file_contents, mcp__github__create_or_update_file
model: sonnet
---

# Skill: Profile Generator

## Purpose

Scan a project's codebase to auto-detect the tech stack, then interactively prompt the user for description, exposed APIs/events, consumed dependencies, and sibling project references. Generates `.sigil/project-profile.yaml` and optionally publishes to the shared repo if connected.

## Critical Constraint

**NEVER use `git clone`, `git commit`, `git push`, `git pull`, `git fetch`, or any git write/remote operations for publishing profiles.** The only permitted git commands are read-only local queries: `git remote get-url` (for repo identity) and `git config` (for user info). Profile publishing to the shared repo MUST go through the `shared-context-sync` skill's Profile Push protocol, which uses GitHub MCP tools. If MCP is unavailable, queue the operation locally rather than falling back to git CLI.

## When to Invoke

- User runs `/sigil:profile`
- User says "init profile", "create project profile", "what does this project expose", "set up tech stack"
- Orchestrator routes a profile-related request

## Inputs

**Optional:**
- `mode`: `"generate"` (default) or `"view"` — If `view`, display current profile and exit

**Auto-loaded:**
- Codebase files (scanned for tech stack signals)
- `.sigil/project-profile.yaml` (if exists — for update flow)

## Process

### Step 1: Check for Existing Profile

Read `.sigil/project-profile.yaml`:

- **If exists and mode is `generate`:**
  ```
  A project profile already exists.

    Name: web-app
    Stack: TypeScript, Next.js 14, React 18
    Last modified: 2026-02-09

  What would you like to do?
  1. View the current profile
  2. Update it (re-scan and re-prompt)
  3. Cancel
  ```

- **If exists and mode is `view`:** Display formatted profile (see Step 8) and exit.
- **If missing:** Proceed to Step 2.

### Step 2: Scan Codebase for Signals

Scan for the following files to detect tech stack:

**Auto-Detection Sources:**

| Signal File | Detects |
|-------------|---------|
| `package.json` | Node.js, npm packages, frameworks (React, Next.js, Express, Vue, Angular, Svelte, etc.) |
| `tsconfig.json` | TypeScript |
| `requirements.txt` / `pyproject.toml` / `setup.py` | Python, pip packages, frameworks (Django, Flask, FastAPI) |
| `Cargo.toml` | Rust, crate dependencies |
| `go.mod` | Go, module dependencies |
| `Gemfile` | Ruby, gems, Rails |
| `build.gradle` / `build.gradle.kts` / `pom.xml` | Java/Kotlin, Gradle/Maven |
| `Package.swift` | Swift, iOS/macOS |
| `pubspec.yaml` | Dart/Flutter |
| `Dockerfile` / `docker-compose.yml` | Container infrastructure |
| `vercel.json` / `netlify.toml` / `fly.toml` | Hosting platform |
| `.github/workflows/` | CI/CD (GitHub Actions) |
| `jest.config.*` / `vitest.config.*` / `playwright.config.*` / `pytest.ini` | Testing frameworks |
| `tailwind.config.*` | Tailwind CSS |
| `.env` / `.env.example` | Environment variables (check for database URLs, service names) |

**Detection procedure:**

1. Use Glob to check for each signal file
2. For files that exist, read key fields:
   - `package.json`: `dependencies`, `devDependencies` → extract framework names and versions
   - `go.mod`: `module` line + `require` block
   - `Cargo.toml`: `[dependencies]` section
   - etc.
3. Aggregate findings into categories:
   - **Languages:** Detected programming languages
   - **Frameworks:** Detected frameworks with versions
   - **Infrastructure:** Hosting, databases, services
   - **Testing:** Test frameworks and tools

4. **Detect enhanced context** (signals for optional profile sections):
   - **Databases:** Check `.env` / `.env.example` for `DATABASE_URL`, `REDIS_URL`, `MONGO_URI`; check `docker-compose.yml` for service images (`postgres`, `redis`, `mongo`, `mysql`); check `package.json` for db driver packages (`pg`, `mongoose`, `mysql2`, `ioredis`)
   - **API Surface:** Check for route directories (`src/routes/`, `src/api/`, `app/api/`, `pages/api/`); list immediate subdirectory names as potential route modules
   - **Auth Model:** Check for auth middleware files (`middleware.ts`, `auth.ts`, `guards/`, `passport.js`); check `package.json` for auth packages (`next-auth`, `passport`, `jsonwebtoken`, `clerk`, `supabase`)
   - **Project Structure:** List top-level directories under `src/` (or project root if no `src/`); filter out common tooling dirs (`.git`, `node_modules`, `.next`, `dist`, `build`)

### Step 3: Display Detected Stack

```
Project Profile Setup
==============================

I scanned your project and found:

  Languages: TypeScript, CSS
  Frameworks: Next.js 14, React 18, Tailwind CSS
  Testing: Jest, Playwright
  Infrastructure: (none detected)

Look right? [Y/n]:
```

If user says no, ask what to change and incorporate corrections.

### Step 4: Prompt for Description

```
What does this project do? (1-2 sentences, plain language)
>
```

### Step 5: Prompt for Exposes (optional)

```
Does this project provide APIs, events, or packages
that other projects use? [y/N]:
```

If yes:
```
Describe what it provides (plain language):
>
```

Parse the plain-language response into structured `exposes` entries:
- Identify type: `rest-api`, `graphql`, `event`, `package`, `web-app`, `grpc`
- Extract description

If the user's description is ambiguous, ask a follow-up to clarify the type or specific endpoints/events.

### Step 6: Prompt for Consumes (optional)

```
Does this project consume APIs, events, or packages
from other projects? [y/N]:
```

If yes:
```
Describe what it consumes (plain language):
>
```

Parse into structured `consumes` entries:
- Identify type, source project name, description
- Extract specific endpoints or events if mentioned

### Step 7: Prompt for Depends On (optional)

```
Does this project depend on any sibling projects? [y/N]:
```

If yes:
```
List the project names (comma-separated):
>
```

### Step 7a: Databases (optional)

If databases were detected in Step 2 sub-step 4:
```
I detected these data stores: postgres, redis

Are these right? Any others to add? [Enter to confirm or describe changes]:
>
```

For each confirmed store, ask:
```
What's {store_name} used for? (brief phrase, e.g. "primary app database", "session cache")
>
```

If no databases detected, ask:
```
Does this project use any databases or data stores? [y/N]:
```
If yes, prompt for name and purpose. Skip this section if no.

### Step 7b: API Surface (optional)

If route directories were detected:
```
I found these route modules: auth, users, orders, payments

Would you like to describe any of these? [y/N]:
```

If yes, for each route module they want to describe:
```
What does /{route} do? (brief description + path prefix if non-obvious)
>
```

Skip if user declines or no routes detected.

### Step 7c: Auth Model (optional)

If auth signals were detected, or always ask:
```
Does this project handle authentication or authorization? [y/N]:
```

If yes:
```
Auth type (e.g. JWT, OAuth2, session, API key, magic link):
>
Brief description (who logs in, what they can do):
>
Roles (e.g. admin, user, viewer — comma-separated, or leave blank):
>
```

### Step 7d: Domain Glossary (optional)

```
Does your project have business terms that are project-specific?
(e.g. "Listing" means something specific here, not just any listing)
[y/N]:
```

If yes:
```
Enter up to 10 terms, one per line, in format: Term = Definition
(Leave a blank line when done)
>
```

Parse each line as `Term = Definition`. Accept up to 10 entries.

### Step 7e: Project Structure (optional)

Show detected top-level directories:
```
Here are your main directories:
  src/api, src/components, src/hooks, src/lib, src/models, src/pages, src/utils

Would you like to annotate what 5-7 of these do? [y/N]:
```

If yes, for each selected directory:
```
What is {dir}/ for? (brief phrase)
>
```

### Step 8: Generate YAML

Generate `.sigil/project-profile.yaml` with inline comments:

```yaml
# Project Profile — generated by /sigil:profile
# This file describes what your project exposes, consumes, and depends on.
# Sigil agents use this to understand your project's boundaries.
# Edit this file anytime — changes sync on your next session start.

name: {repo_name}
description: {user_description}

tech_stack:
  languages:
    - {language1}
    - {language2}
  frameworks:
    - {framework1}
    - {framework2}
  infrastructure:
    # Hosting, databases, services
    - {infra1}
  testing:
    - {test1}
    - {test2}

exposes:
  # What this project provides to others
  - type: {type}
    description: {description}

consumes:
  # What this project needs from others
  - type: {type}
    source: {source_project}
    description: {description}

depends_on:
  # Sibling projects this project relies on
  - {project1}

contacts:
  # Optional — who to ask about this project
  owner: {from git config user.name}
  team: ""

# ── Optional sections — omit entirely if empty ──────────────

databases:
  # Data stores this project depends on
  - name: {store_name}
    purpose: {brief purpose}

api_surface:
  # Route modules / exposed endpoint groups
  - route: /{path}
    description: {what it does}

auth_model:
  # Authentication and authorization approach
  type: {auth_type}
  description: {who logs in and what they can do}
  roles:
    - {role1}
    - {role2}

domain_glossary:
  # Project-specific business terms
  {Term}: {Definition}

project_structure:
  # Key directories and their purpose
  {dir/}: {brief purpose}
```

ALWAYS include ALL required sections (name through contacts). Omit optional sections (databases through project_structure) entirely if the user skipped or provided no data for them. For required sections with no data, use descriptive N/A messages:
- `exposes:` → `# This project does not expose APIs or services to other projects`
- `consumes:` → `# This project does not consume external APIs or services`
- `depends_on:` → `# This project has no sibling project dependencies`
- `contacts:` → `owner: (not configured)` / `team: (not configured)`

Write to `.sigil/project-profile.yaml`.

### Step 9: Publish to Shared Repo (if connected)

1. Check sentinel via `shared-context-sync` sentinel detection
2. If connected: invoke `shared-context-sync` Profile Push
3. Display result:

**If published:**
```
Profile saved: .sigil/project-profile.yaml
Published to shared repo: profiles/{repo_name}.yaml

Other projects will see your profile on their next session start.
```

**If not connected:**
```
Profile saved: .sigil/project-profile.yaml

To share this with other projects, run /sigil:connect first.
```

**If publish failed:**
```
Profile saved: .sigil/project-profile.yaml
Shared sync failed — queued for next session start.
```

## Outputs

**Artifact:**
- `.sigil/project-profile.yaml` — Project profile YAML file

**Handoff Data:**
```json
{
  "profile_path": ".sigil/project-profile.yaml",
  "repo_name": "web-app",
  "published": true,
  "tech_stack": {
    "languages": ["TypeScript", "CSS"],
    "frameworks": ["Next.js 14", "React 18"]
  }
}
```

## Error Handling

| Scenario | Behavior |
|----------|----------|
| No codebase files found | Skip auto-detection, ask user to describe stack manually |
| `.sigil/` directory missing | Create it before writing profile |
| Profile YAML is malformed on update | Back up existing file, generate fresh |
| MCP publish fails | Queue for retry, save locally, warn user |
| Git not initialized | Profile generation works (solo mode), skip publish step |
| No git remote | Profile generation works, skip repo name detection — prompt user for project name |

## Human Tier

**Tier:** Review

User reviews the generated profile before it is saved. The detected tech stack, description, and exposes/consumes are all confirmed interactively.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-09 | Initial release — auto-detection, interactive generation, shared repo publish |
