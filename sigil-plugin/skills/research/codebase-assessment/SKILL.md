---
name: codebase-assessment
description: Analyzes codebase state to determine appropriate Discovery track. Invoke at the start of any new project or when "new project", "start fresh", or "greenfield" is mentioned.
version: 1.1.0
category: research
chainable: true
invokes: [constitution-writer (conditional)]
invoked_by: [orchestrator]
tools: Read, Glob, Grep, Bash
---

# Skill: Codebase Assessment

## Purpose

Determine the current state of the codebase to route to the appropriate Discovery track. This skill runs automatically when a new project workflow begins and classifies the codebase as Greenfield, Scaffolded, or Mature.

## When to Invoke

- Start of any new project conversation
- User mentions "new project", "fresh start", "greenfield"
- User asks "what should I build" in an unfamiliar directory
- Orchestrator routes new request with no active workflow

## Inputs

**Required:**
- `working_directory`: string — Path to the codebase root (defaults to current directory)

**Optional:**
- `user_override`: string — If user specifies "this is a new project" or "this has existing code"

## Process

### Step 1: Signal Detection

Scan for the presence of key indicators:

```
1. Check for dependency manifests:
   - package.json (Node.js/JavaScript)
   - requirements.txt, Pipfile, pyproject.toml (Python)
   - go.mod (Go)
   - Cargo.toml (Rust)
   - Gemfile (Ruby)
   - pom.xml, build.gradle (Java)

2. Check for framework markers:
   - next.config.js, remix.config.js (React frameworks)
   - angular.json, vue.config.js (Other JS frameworks)
   - manage.py, wsgi.py (Django)
   - config/application.rb (Rails)

3. Count code files:
   - *.ts, *.tsx, *.js, *.jsx
   - *.py
   - *.go
   - *.rs
   - *.rb
   - *.java

4. Check for test infrastructure:
   - Test files (*test*, *spec*)
   - Test config (jest.config, pytest.ini, etc.)
   - Test directories (tests/, __tests__/, spec/)

5. Check for CI/CD:
   - .github/workflows/
   - .gitlab-ci.yml
   - Jenkinsfile
   - .circleci/

6. Check for existing Sigil artifacts:
   - /.sigil/constitution.md
   - /.sigil/project-context.md
   - /.sigil/project-foundation.md
   - /.sigil/specs/ directory
```

### Step 2: Stack Detection

When manifest files are found, parse them to detect the technology stack. See `references/stack-signals.md` for per-manifest detection patterns, confidence rules, and output schema.

### Step 3: Classification

Apply classification logic based on detected signals:

```
GREENFIELD when ALL of:
  - No dependency manifest (package.json, requirements.txt, etc.)
  - code_file_count < 5

SCAFFOLDED when ANY of:
  - Has dependency manifest AND dependency_count < 10
  - code_file_count between 5-20
  - Has manifest but no tests AND no CI

MATURE when ANY of:
  - dependency_count >= 10
  - code_file_count > 20
  - has_tests = true
  - has_ci = true
```

### Step 4: Confidence Assessment

Determine confidence in classification:

```
HIGH confidence when:
  - Classification is clear (strong signals present)
  - No conflicting indicators

MEDIUM confidence when:
  - Classification is borderline
  - Some signals contradict

LOW confidence when:
  - Signals are ambiguous
  - User override may be needed
```

### Step 5: Generate Assessment Report

Create a structured report of findings.

## Outputs

**Report Format:**
```json
{
  "classification": "greenfield | scaffolded | mature",
  "confidence": "high | medium | low",
  "signals": {
    "has_manifest": true,
    "manifest_type": "package.json",
    "dependency_count": 45,
    "code_file_count": 127,
    "has_tests": true,
    "has_ci": true,
    "has_sigil_artifacts": false,
    "detected_stack": {
      "language": { "name": "TypeScript", "version": "5.x", "confidence": "confident", "source": "package.json" },
      "framework": { "name": "Next.js", "version": "14.x", "confidence": "confident", "source": "package.json" },
      "database": { "name": "PostgreSQL", "confidence": "confident", "source": "prisma/schema.prisma" },
      "orm": { "name": "Prisma", "version": "5.x", "confidence": "confident", "source": "package.json" },
      "test_framework": { "name": "Jest", "confidence": "confident", "source": "package.json:devDependencies" }
    }
  },
  "rationale": "Established codebase with 45 dependencies and 127 code files. Test and CI infrastructure present.",
  "recommended_track": "assessment-constitution",
  "override_available": true
}
```

**Handoff Data (Greenfield):**
```json
{
  "assessment_complete": true,
  "classification": "greenfield",
  "confidence": "high",
  "recommended_track": "discovery-greenfield",
  "detected_stack": null,
  "next_skill": "problem-framing"
}
```

**Handoff Data (Scaffolded/Mature without Constitution):**
```json
{
  "assessment_complete": true,
  "classification": "mature",
  "confidence": "high",
  "recommended_track": "assessment-constitution",
  "detected_stack": {
    "language": { "name": "TypeScript", "version": "5.x", "confidence": "confident", "source": "package.json" },
    "framework": { "name": "Next.js", "version": "14.x", "confidence": "confident", "source": "package.json" },
    "database": { "name": "PostgreSQL", "confidence": "confident", "source": "prisma/schema.prisma" },
    "orm": { "name": "Prisma", "version": "5.x", "confidence": "confident", "source": "package.json" },
    "test_framework": { "name": "Jest", "confidence": "confident", "source": "package.json:devDependencies" }
  },
  "next_skill": "constitution-writer"
}
```

## Classification Details

### Greenfield (New Project)

**Characteristics:**
- Empty or near-empty directory
- No dependency manifests
- Fewer than 5 code files
- No existing configuration

**Discovery Track:**
- Full Discovery chain
- Problem framing from scratch
- Complete constraint discovery
- Stack recommendation

**User Presentation:**
```
## New Project Detected

This appears to be a new or nearly empty project. I'll guide you through:

1. **Problem Framing** - Understanding what you want to build
2. **Constraint Discovery** - Identifying your limitations and requirements
3. **Stack Recommendation** - Suggesting appropriate technologies
4. **Foundation Document** - Recording decisions for future reference

Ready to start? Tell me about what you want to build.
```

### Scaffolded (Partially Setup)

**Characteristics:**
- Has dependency manifest but minimal dependencies
- Some code files (5-20)
- Framework may be initialized
- No tests or CI yet

**Discovery Track:**
- Abbreviated Discovery chain
- Infer preferences from existing setup
- Confirm/expand constraints
- Validate stack choice

**User Presentation:**
```
## Scaffolded Project Detected

I found an existing project setup:
- **Manifest:** package.json with [N] dependencies
- **Framework:** [Detected framework or "None detected"]
- **Code Files:** [N] files

Since you have a foundation, I'll:
1. **Confirm** your technology choices are intentional
2. **Expand** on any missing constraints
3. **Document** the foundation for consistency

Does this setup represent your intended direction?
```

### Mature (Established Codebase)

**Characteristics:**
- 10+ dependencies
- 20+ code files
- Test infrastructure present
- CI/CD configured

**Discovery Track:**
- Skip Discovery (already has foundation)
- Route to standard workflow
- OR trigger Constitution Inference (Phase 2)

**User Presentation:**
```
## Established Codebase Detected

This appears to be a mature project with:
- **Dependencies:** [N] packages
- **Code Files:** [N] files
- **Testing:** [Present/Absent]
- **CI/CD:** [Present/Absent]

For established codebases, we'll skip discovery and go directly to feature development.

What would you like to build?
```

### Assessment Path Routing

When the classification is `scaffolded` or `mature` AND no constitution exists (`/.sigil/constitution.md` not found):

1. Set `recommended_track: "assessment-constitution"`
2. Include full `detected_stack` in handoff data
3. Invoke `constitution-writer` with detected stack for pre-population

**Assessment Path Presentation:**
```
## Established Codebase Detected

This appears to be a [scaffolded/mature] project. I've detected your technology stack:

| Component | Detected | Source |
|-----------|----------|--------|
| Language | TypeScript 5.x | package.json |
| Framework | Next.js 14.x | package.json |
| Database | PostgreSQL | prisma/schema.prisma |
| ORM | Prisma 5.x | package.json |
| Tests | Jest | package.json:devDependencies |

Before we start building features, let's create a project constitution to capture your standards and principles.

This will take just a few minutes and ensures consistent AI assistance.

Ready to set up your constitution?
```

## User Override

If the user disagrees with the assessment:

```
User: "Actually, this is a brand new project - ignore those files"

Response: "Got it - I'll treat this as a greenfield project and guide you
through full discovery. The existing files won't influence our technology
decisions."

→ Route to greenfield track regardless of signals
```

```
User: "This is already setup, I just want to add features"

Response: "Understood - I'll skip discovery and we can start on your feature.
Just describe what you'd like to build."

→ Route to standard workflow
```

## Human Checkpoints

- **Auto Tier:** Assessment runs automatically
- **Review Tier:** Classification presented for confirmation
- User can override classification at any point

## Error Handling

| Error | Resolution |
|-------|------------|
| Cannot read directory | Ask user for correct path |
| Conflicting signals | Present both interpretations, ask user |
| Unknown manifest type | Treat as scaffolded, ask for clarification |
| Permission denied | Request access or ask user to describe state |

## Integration Points

- **Invoked by:** `orchestrator` at project start
- **Invokes:** `constitution-writer` — ONLY when classification is SCAFFOLDED or MATURE and no existing constitution is detected. This is a conditional invocation, not a guaranteed step.
- **Hands off to:**
  - `problem-framing` — greenfield projects
  - `constitution-writer` — scaffolded/mature without constitution (assessment-constitution track)
  - Standard workflow — mature with existing constitution

## Example Assessments

### Example 1: Empty Directory

```
Signals:
  - No manifest files
  - 0 code files
  - No configuration

Classification: GREENFIELD
Confidence: HIGH
Rationale: Directory is empty. Starting from scratch.
```

### Example 2: npm init Project

```
Signals:
  - package.json exists (0 dependencies beyond defaults)
  - 1 code file (index.js placeholder)
  - No tests or CI

Classification: SCAFFOLDED
Confidence: HIGH
Rationale: Basic npm project initialized but no real code yet.
```

### Example 3: Active Development Project

```
Signals:
  - package.json with 45 dependencies
  - 127 code files
  - Jest tests present
  - GitHub Actions workflow

Classification: MATURE
Confidence: HIGH
Rationale: Established codebase with full infrastructure.
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-20 | Initial release |
| 1.1.0 | 2026-01-27 | Added stack detection (Step 2), assessment-constitution track, constitution-writer invocation |
