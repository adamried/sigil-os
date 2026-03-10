---
name: preflight-check
description: Creates SIGIL.md with enforcement rules and adds a pointer to the project's CLAUDE.md. Now invoked automatically via SessionStart hook.
version: 2.4.0
category: workflow
chainable: true
invoked_by: [hook:SessionStart]
tools: Read, Write, Edit
model: haiku
---

# Skill: Preflight Check

## Purpose

Create a standalone `SIGIL.md` file with mandatory enforcement rules and ensure the project's `CLAUDE.md` contains a lightweight pointer to it.

**Note:** In Sigil OS v2.0+, this skill is invoked automatically by the `SessionStart` hook (`hooks/preflight-check.sh`). The hook runs checks and outputs JSON instructions; Claude then uses this skill's content to create/update files as needed.

## Constants

```
ENFORCEMENT_VERSION: 2.4.0
```

**Versioning:** `ENFORCEMENT_VERSION` tracks independently from the Sigil OS plugin version in `plugin.json`. Bump it only when the enforcement section content changes (new rules, modified instructions). Plugin releases that don't change enforcement content leave this version unchanged.

## When to Invoke

- Automatically via SessionStart hook at the start of every `/sigil` command
- When the hook output indicates SIGIL.md needs to be created or updated

## Process

### Part A: Installation Verification (Handled by Hook)

The SessionStart hook (`hooks/preflight-check.sh`) handles installation verification. Since Sigil OS is now a Claude Code plugin, installation status is managed by the plugin system.

### Part A2: Directory Check

If `.sigil/` directory does not exist, this project has not been set up with Sigil OS yet. Recommend `/sigil-setup` to the user instead of attempting to create files inline:

> Sigil OS is not set up in this project. Run `/sigil-setup` to get started.

### Part B: Create/Update SIGIL.md and Add Pointer to CLAUDE.md

The hook outputs JSON with instructions. Follow these steps based on the hook output:

#### Logic

1. Read `./CLAUDE.md` from the project root.
2. **Dev repo guard:** If the file contains the string `Sigil OS Development Environment`, skip entirely. This is the Sigil development repository — enforcement rules are not appropriate here. Report nothing.
3. **Check/create SIGIL.md:**
   - If hook indicates `sigil_md_action: "create"` → create SIGIL.md with content below. Report: `Created SIGIL.md with Sigil enforcement rules (v2.4.0).`
   - If hook indicates `sigil_md_action: "update"` → overwrite SIGIL.md with content below. When the old SIGIL.md has a `## Configuration` section with a YAML block, extract the `user_track` and `execution_mode` values, write them to `.sigil/config.yaml`, and add `.sigil/config.yaml` to `.gitignore` if not already present. Omit the `## Configuration` YAML block from the new SIGIL.md (the template below no longer includes it). Report: `Updated SIGIL.md enforcement rules to v2.4.0.` If config was migrated, also report: `Migrated personal config to .sigil/config.yaml.`
   - If hook indicates `sigil_md_action: "none"` → skip (already current).
4. **Check CLAUDE.md for pointer:**
   - If hook indicates `needs_pointer: true`:
     - If `has_legacy_block: true` → remove the entire legacy block (from `<!-- SIGIL-OS-ENFORCEMENT-START` through `<!-- SIGIL-OS-ENFORCEMENT-END -->`), then add the pointer. Report: `Migrated legacy enforcement block to SIGIL.md.`
     - Otherwise → add the pointer as the **first line** of the file (or after any frontmatter/YAML header). Report: `Added SIGIL.md pointer to ./CLAUDE.md.`
   - If no `./CLAUDE.md` exists → create it with only the pointer line. Report: `Created ./CLAUDE.md with SIGIL.md pointer.`

#### Pointer Line

Use this exact content as the pointer:

```
<!-- Project: Check for ./SIGIL.md and follow all rules if present -->
```

#### Report

Only print a message if something changed:
- Created SIGIL.md: `Created SIGIL.md with Sigil enforcement rules (v2.4.0).`
- Updated SIGIL.md version: `Updated SIGIL.md enforcement rules to v2.4.0.`
- Created CLAUDE.md: `Created ./CLAUDE.md with SIGIL.md pointer.`
- Added pointer to existing CLAUDE.md: `Added SIGIL.md pointer to ./CLAUDE.md.`
- Migrated legacy block: `Migrated legacy enforcement block to SIGIL.md.`
- Skipped (current version and pointer present, or dev repo): Print nothing.

## SIGIL.md Content

The following is the canonical SIGIL.md content. Use this exact content (substituting the current `ENFORCEMENT_VERSION` into the version marker) when creating or updating the file.

```markdown
<!-- SIGIL-OS v2.4.0 -->
# Sigil OS — Enforcement Rules

These rules are MANDATORY. They override default Claude Code behavior for all workflow actions.

## Component Locations

Sigil OS components are provided by the **sigil-os plugin**:
- **Agents:** 9 specialist agents (orchestrator, architect, developer, qa-engineer, security, uiux-designer, business-analyst, task-planner, devops)
- **Skills:** Organized by category (workflow, design, QA, review, research, learning, ui, engineering, specification)
- **Chains:** Pipeline definitions (full-pipeline, quick-flow, discovery-chain)
- **Commands:** Slash command definitions (sigil, sigil-setup, sigil-constitution, sigil-handoff, etc.)

All components are automatically available when the sigil-os plugin is installed.

## Mandatory Skill Invocation

When performing workflow actions, you MUST use the Skill tool with the exact skill name. NEVER perform these actions inline or by writing files directly.

| Action | MUST do | NEVER do instead |
|--------|--------|------------------|
| Start a feature workflow | Use `/sigil "description"` | Write a spec.md file yourself |
| View/edit constitution | `Skill(skill: "sigil-constitution")` | Edit constitution.md directly |
| Capture learnings | `Skill(skill: "sigil-learn")` | Write to learnings files directly |
| Show workflow status | Use `/sigil` or `/sigil status` | Summarize status yourself |

The following actions are handled automatically by the `/sigil` orchestrator and should not be invoked manually:
- Specification writing (auto-invoked when you describe a feature)
- Clarification (auto-invoked after spec if ambiguities exist)
- Planning (auto-invoked after clarification)
- Task breakdown (auto-invoked after planning)
- QA validation (auto-invoked after each task implementation)
- Code review (auto-invoked after all tasks pass validation)
- Context loading (auto-runs at session start via hook)

**Note:** Design skills (`ui-designer`, `accessibility`, `ux-patterns`, etc.) are invoked by the UI/UX Designer agent during the Plan phase, not listed here. They are called through agent delegation, not direct user commands.

## Mandatory Chain Following

Before executing a multi-phase workflow, you MUST:
1. Read the appropriate chain definition (e.g., `full-pipeline`, `quick-flow`)
2. Follow the chain's defined sequence of skills — do NOT skip phases
3. Execute handoffs between phases using the chain's transition rules

## Mandatory Agent Behavior

Before implementing code, you MUST:
1. Read the `developer` agent definition and follow its protocols (test-first, learning capture, constitution compliance)
2. Before QA validation, read the `qa-engineer` agent definition and follow its validation checklist

When delegating to specialist agents via the Task tool, you MUST set `subagent_type` to the matching agent name (e.g., `subagent_type: "developer"`, `subagent_type: "qa-engineer"`).

## Mandatory Context Loading

At the start of any workflow, you MUST read these files (if they exist):
1. `.sigil/constitution.md` — Project principles (NEVER violate these)
2. `.sigil/project-context.md` — Current workflow state
3. `.sigil/learnings/active/patterns.md` — Validated patterns to follow
4. `.sigil/learnings/active/gotchas.md` — Known traps to avoid
5. `.sigil/waivers.md` — Constitution waivers (load before constitution checks)
6. `.sigil/tech-debt.md` — Non-blocking review suggestions (load during review phase)

## Mandatory State Updates

After each phase transition (e.g., spec complete -> planning), you MUST update `.sigil/project-context.md` with:
- Current phase name
- Feature being worked on
- Spec path
- Timestamp of transition

## Automatic Workflow Handoffs

When these artifacts are created during a /sigil workflow, the next phase begins automatically:

| After Creating | Next Phase | How |
|----------------|-----------|-----|
| `spec.md` | Clarification | Auto-continue to clarifier |
| `clarifications.md` | Planning | Auto-continue to technical-planner |
| `plan.md` | Task Breakdown | Auto-continue to task-decomposer |
| `tasks.md` | Implementation | Auto-continue to Developer agent |
| Task code changes | Validation | Invoke qa-validator |
| All tasks validated | Code Review | Read code-reviewer SKILL.md and run review |

## External Context Integration

When MCP tools (Atlassian, Figma, Jira, GitHub Issues, Linear, etc.) are used to fetch work items, designs, or requirements in the same session as a `/sigil` workflow invocation:

1. Treat the fetched content as **input context** for the spec-writer, not as standalone completed actions
2. When the user invokes `/sigil "description"` after fetching external context, pass all relevant fetched content (ticket descriptions, acceptance criteria, design references, linked requirements) as part of the feature description to the spec-writer
3. Do NOT generate specs, tasks, or implementation plans outside of the `/sigil` workflow. All specification work MUST flow through the orchestrator's pipeline
4. If external context was fetched but `/sigil` has not been invoked, prompt the user: "I've gathered context from [source]. Would you like to start a Sigil workflow with this? Run `/sigil` with a feature description to begin."

CORRECT: Fetch Jira ticket → User runs `/sigil "implement JIRA-123 login feature"` → Spec-writer receives ticket context + description
INCORRECT: Fetch Jira ticket → Generate spec.md directly from ticket → Start coding
INCORRECT: Fetch Jira ticket → Create project-context.md stub → Stop

## Implementation Loop Rule

After `tasks.md` is created, the develop/validate loop runs automatically:
1. Pick the first unblocked incomplete task
2. Implement it (following developer agent protocol)
3. Validate it (following qa-engineer agent protocol)
4. If validation fails, fix and re-validate (max 5 attempts)
5. Move to the next task
6. After all tasks pass validation, read the code-reviewer SKILL.md and run review on all changed files

Do NOT wait for user input between tasks. The loop continues until all tasks are complete or a blocker requires human decision.

## Configuration Compliance

Read `.sigil/config.yaml` at session start. If the file does not exist, use defaults: `user_track: non-technical`, `execution_mode: automatic`. Adapt all user-facing communication, question depth, and detail level to the configured `user_track`. When `user_track` is `non-technical`, auto-resolve technical decisions with sensible defaults and communicate in plain English without agent names, phase jargon, or file paths. When `user_track` is `technical`, surface technical trade-offs, show agent and specialist names, and include implementation details. Respect `execution_mode` for team composition decisions (S3-102).

## Correct vs Incorrect Examples

CORRECT: Use `/sigil "description"` to start a feature workflow.
INCORRECT: Write a `spec.md` file directly without the workflow.

CORRECT: Read the chain definition then follow each phase in order.
INCORRECT: Jump directly to implementation after the user describes a feature.

CORRECT: Read the developer agent definition before writing code.
INCORRECT: Start writing code using default Claude Code behavior.

CORRECT: Read the qa-validator SKILL.md and follow its process to run QA checks.
INCORRECT: Review the code yourself and declare it "looks good."
```

## Outputs

- **Status:** `PASS` (hook check passed), `SKIP` (dev repo)
- **Side effect:** `SIGIL.md` may be created or updated; `CLAUDE.md` may have pointer added or legacy block removed
- **Console:** Creation/update status (single line each, only if something changed)
