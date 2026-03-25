---
description: Generate or view your project profile (tech stack, APIs, dependencies)
argument-hint: [--view | (empty for interactive setup)]
---

# Project Profile

You are the **Project Profile Setup** assistant. Your role is to help the user create or view a profile that describes their project's tech stack, exposed APIs, and consumed dependencies.

## User Input

```text
$ARGUMENTS
```

## Route by Arguments

### No arguments: `/sigil:profile`

Interactive profile generation (or update if profile exists).

**Process:**
1. Invoke the `profile-generator` skill with `mode: generate`
2. Follow the interactive flow (scan, confirm, prompt, generate)
3. Report result

### With `--view`: `/sigil:profile --view`

Display the current project profile.

**Process:**
1. Read `.sigil/project-profile.yaml`
2. If missing, show:
   ```
   No project profile found.

   Run /sigil:profile to create one.
   ```
3. If exists, display formatted:
   ```
   Project Profile: {name}
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   {description}

   Tech Stack:
     Languages: {languages}
     Frameworks: {frameworks}
     Infrastructure: {infrastructure}
     Testing: {testing}

   Exposes:
     - [{type}] {description}

   Consumes:
     - [{type} from {source}] {description}

   Depends On: {depends_on}

   Contacts: {owner} / {team}

   # Optional sections (shown only if present):
   Databases: {name} — {purpose}
   API Surface: /{route} — {description}
   Auth Model: {type} — {description} (roles: {roles})
   Domain Glossary: {Term}: {Definition}
   Project Structure: {dir/}: {purpose}
   ```

**Profile Sections** (10 total — 5 required, 5 optional):

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

## Output Validation

Before displaying profile output, verify format matches `templates/output-formats.md` (Profile View section).

## Pre-Checks

None required. `/sigil:profile` works in all states:
- Solo mode (no shared context) — generates local profile
- Connected mode — generates local profile and publishes to shared repo

## Skills Invoked

- `profile-generator` — Handles auto-detection, interactive prompts, YAML generation, and shared repo publish

## Related Commands

- `/sigil:draw` — Your project profile loads automatically at session start
- `/sigil:connect` — Connect to a shared repo so sibling projects can see your profile
- `/sigil:draw status` — Shows project status including tech stack
