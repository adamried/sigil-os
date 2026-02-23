# Changelog

## [0.28.0] - 2026-02-20

### Fixed

#### Post-Audit Fix Package (Round 1 — Structural)
- **Complexity assessment in `/sigil` Step 3:** Plain-text feature descriptions now route through `complexity-assessor` before reaching spec-writer. Scores determine Quick Flow (7-10), Standard (11-16), or Enterprise (17-21) track. Quick Flow path defined with lightweight spec, no clarifier, 1 QA fix attempt, no formal code/security review.
- **Conditional UI/UX, researcher, and ADR steps in `/sigil` Step 4:** Auto-continue table now includes `uiux-designer` (conditional on UI components), `researcher` (Enterprise track or unknowns), and `adr-writer` (significant decisions) between clarifier and task-decomposer.
- **Separated security review from code review in `/sigil`:** Code review and security review are now sequential, distinct steps after all tasks complete. Security review is conditional on file types touched. Fixed duplicate step numbering.
- **Quick Flow constitution handling:** Changed from warn-and-continue to block-and-redirect, matching sigil.md's blocking behavior. Added safety-net note for direct chain invocation.

#### Post-Audit Fix Package (Round 2 — Hygiene)
- **full-pipeline.md learning-reader model:** Removed separate learning-reader orchestration step. Developer Agent box now notes learnings are loaded internally. Updated state transitions to match sigil.md's model.
- **Deleted 8 orphaned files:** Removed `handoff-template.md` and 6 unreferenced prompt files in `templates/prompts/`. Updated `templates/README.md` to reflect actual template inventory (11 templates).
- **sigil-learn.md command names:** Fixed `/learn` → `/sigil-learn` references and duplicate `/sigil` entry → `/sigil status`.
- **sigil-profile.md duplicate Related Commands:** Fixed duplicate `/sigil` entry → `/sigil status`.
- **CLAUDE.md directory listing:** Updated stale skill category names (`quality/` → `qa/`, `ui-implementation/` → `ui/`, added `review/`, `specification/`, `integration/`).
- **Discovery chain cross-references:** Fixed `invokes: []` → proper downstream targets for `problem-framing`, `constraint-discovery`, and `stack-recommendation`.
- **QA Engineer version history:** Reordered entries to chronological (1.0.0 → 1.1.0 → 1.2.0 → 1.3.0).
- **output-formats.md sync with sigil.md:** Added `/sigil PROJ-123` and `/sigil-config` to Help Output. Updated separator definition from 50 to 52 characters to match sigil.md canonical outputs.
- **Scaffold waivers.md in sigil-setup:** Added Step 6.6 to scaffold `.sigil/waivers.md` from template during setup.
- **Chain-alignment linter check:** New `check_chain_sigil_alignment()` function validates that skills in chain diagrams appear in sigil.md. Warns on missing references, excludes optional extensions (deploy-checker, DevOps).

## [0.27.0] - 2026-02-20

### Added

#### S4-102: Proactive Overrides
- **Waiver template:** New `templates/waiver-template.md` with Active Overrides table format, field documentation, and examples.
- **Override expiration check in `/sigil`:** New Step 1.4 reads `waivers.md`, parses active overrides, checks expiration dates, auto-marks expired overrides, and presents resolution options (acknowledge / extend / convert to permanent).
- **Override-adjusted qa-validator v1.2.0:** Auto-loads active overrides from `waivers.md`. For overridden articles, validates against adjusted rules instead of original constitution rules. Marks findings with `[OVERRIDE]`. Adds "Active Overrides Applied" section to validation report.
- **Override-adjusted code-reviewer v1.3.0:** Same pattern — loads overrides, applies adjusted rules, downgrades blockers to warnings for overridden articles, annotates with `[OVERRIDE]`, adds override section to report.
- **Override section in handoff-packager v1.3.0:** New Step 3e extracts active overrides and includes summary table in handoff package so reviewing engineers know what exceptions are in effect.
- **Status dashboard updated:** Constitution line now shows active override count and nearest expiration (e.g., "| 1 active override (expires Feb 28)").

#### S4-104 Phase 2: Handoff-Back
- **handoff-back skill v1.0.0:** 4-step process — check ticket context, assemble summary, invoke adapter write protocols, confirm. Graceful degradation on write failures. Automatic after code review for ticket-driven features.
- **Jira adapter v1.1.0 write protocols:** Post Summary (addCommentToJiraIssue), Transition Status (transitionJiraIssue with available-transitions check), Link Artifact (remote links with fallback to comment).
- **Handoff-back prompt in `/sigil`:** After code review passes for ticket-driven features, auto-invokes handoff-back. Adds "Update ticket and close" option to next-action prompt.
- **Adapter authoring guide:** New `docs/adapter-authoring.md` — guide for creating new adapters using Jira as reference.

### Changed
- **Documentation updated:** user-guide.md (overrides section, handoff-back in ticket workflow), troubleshooting.md (expired overrides, handoff-back failures), glossary.md (override, handoff-back, adapter write protocol), command-reference.md (override checks, handoff-back behavior, ticket routing details).

## [0.26.0] - 2026-02-20

### Added

#### S4-101: Enforcement Levels for Shared Standards
- **Enforcement-level awareness in shared-context-sync v1.4.0:** Standards Pull and Standards Discover now parse YAML frontmatter `enforcement` field from standard files. Three levels: `required` (hard block if missing), `recommended` (warn on conflict), `informational` (silent). Defaults to `recommended` if absent.
- **Enforcement-aware Discrepancy Detection:** New missing-required-standard pre-check verifies all `required` standards have `@inherit` markers. Discrepancies now include `enforcement`, `severity`, and `blocking` fields. Required conflicts block the session; recommended conflicts warn; informational conflicts are silent.
- **Hard-block resolution in `/sigil` command:** Step 1.3 now inspects discrepancy results for blocking items. If any `blocking: true` discrepancies exist, displays hard-block format and halts until resolved. Warning-only discrepancies display and proceed.
- **Enforcement-aware connect-wizard v1.3.0:** Step 7 groups standards by enforcement level — required standards auto-apply, recommended standards prompt user, informational standards mentioned only.
- **Enforcement-aware constitution-writer v2.3.0:** Step 0c always emits `@inherit` for required standards, default-includes recommended (user can skip), skips informational. Step 3b displays enforcement icons and legend.
- **Status dashboard updated:** Constitution line shows inherited standard counts with enforcement breakdown (e.g., "7 articles (3 inherited: 1 required, 2 recommended)").

#### S4-103: External Tool Configuration
- **Integration Discovery Protocol in shared-context-sync v1.5.0:** Fetches adapter configs from `integrations/` directory in shared repo. SHA-based caching, graceful MCP failure fallback. Added `integrations/` to cache structure and `integrations_hashes` to last-sync.json.
- **Integration Pull Protocol:** Refreshes cached adapter configs at session start alongside standards pull.
- **Integration discovery in `/sigil-setup`:** Step 3.5 now invokes Integration Discovery after standards discovery, checks MCP availability per adapter, and imports org defaults to `.sigil/config.yaml`.
- **Integration setup in connect-wizard v1.4.0:** New Step 8 discovers integrations, displays available adapters with MCP status, fetches org defaults for configured ones. Previous Step 8 (Confirmation) renumbered to Step 9.
- **Integration skill category:** New `sigil-plugin/skills/integration/` directory with README.

#### S4-104 Phase 1: Ticket-Driven Entry
- **ticket-loader skill v1.0.0:** 6-step process — validate adapter, fetch ticket, fetch parent, categorize (feature/bug/maintenance/enhancement), assemble enriched context, hand off to orchestrator. Returns structured context with ticket_key, category, ticket_metadata, enriched description.
- **Jira adapter skill v1.0.0:** Phase 1 (read-only) — Fetch Ticket, Fetch Parent, Categorize protocols via Atlassian MCP tools. Configuration schema for `.sigil/integrations/jira.yaml`. Category mapping: Bug→bug, Story→feature, Task→enhancement, labels→maintenance.
- **Ticket-key routing in `/sigil`:** Step 2 detects `[A-Z][A-Z0-9]+-\d+` pattern, invokes ticket-loader, routes by category. Maintenance → Quick Flow, bug → cap Standard, feature/enhancement → normal assessment.
- **Enriched-context path in `/sigil` Step 3:** If input came from ticket-loader, passes ticket_metadata alongside enriched_description to spec-writer.
- **Ticket metadata in complexity-assessor v1.1.0:** Optional `ticket_metadata` input — story points → scope, labels → integration, related tickets → dependencies scoring. Category overrides: maintenance → force Quick Flow, bug → cap Standard.
- **Chain updates:** full-pipeline v1.4.0 documents ticket-loader as alternate entry, adds ticket fields to context preservation. quick-flow v1.2.0 documents maintenance flag handling.

### Changed
- **`/sigil` help output:** Added `/sigil PROJ-123` format for ticket-driven entry.
- **Natural language triggers:** Added ticket-key patterns ("Work on PROJ-123", "Pick up PROJ-123").
- **`/sigil-setup` completion summary:** Added integrations status line.
- **Documentation updated:** shared-context-setup.md (enforcement levels, external tool integrations), multi-team-workflow.md (enforcement levels in shared standards), glossary.md (8 new terms), troubleshooting.md (required standard blocks, ticket key not recognized, no adapter configured), command-reference.md (ticket-key format, integration discovery), user-guide.md (ticket-driven workflow, enforcement levels).

## [0.25.1] - 2026-02-20

### Fixed
- **Setup now scaffolds project-context.md:** `/sigil-setup` creates `.sigil/project-context.md` from the template with default values, preventing Claude Code from improvising a malformed stub when enforcement rules require loading it.
- **Auto-commit spec artifacts before implementation:** The orchestrator now commits spec.md, plan.md, and tasks.md to git before entering the implementation loop, creating a restore point in case of session loss. Commit is local-only and non-blocking (failures produce a warning, not a halt).

### Added
- **External Context Integration enforcement (SIGIL.md v2.4.0):** New enforcement section ensures MCP-fetched content (Atlassian, Figma, Jira, etc.) is routed through the `/sigil` workflow pipeline as spec-writer input rather than treated as standalone actions.

### Changed
- **Documentation moved to root:** User-facing docs relocated from `sigil-plugin/docs/` to root `docs/` for easier access. Internal dev docs moved from `docs/` to `dev-docs/` (gitignored). All cross-references updated.

## [0.25.0] - 2026-02-20

### Added
- **Shared Standards @inherit Implementation:** Standards from `shared-standards/` in the shared repo now flow into project constitutions automatically. Four new protocols in shared-context-sync v1.3.0: Standards Pull (fetches standards via MCP with SHA-based caching), Standards Expand (processes @inherit markers in constitution.md with start/end block format), Standards Discover (lists available standards with article mappings), and Discrepancy Detection (flags conflicts between inherited and local content).
- **Standards-aware constitution generation (constitution-writer v2.2.0):** Accepts `shared_standards` input, emits `@inherit` markers with expanded content for articles with mapped shared standards, shows Standards Integration Summary, adds `### Local Additions` sections.
- **Shared context step in `/sigil-setup`:** New Step 3.5 asks about shared context before constitution creation. If the user connects, shared standards are discovered and passed to the constitution writer.
- **Session-start standards refresh (`/sigil` command):** Step 1 now pulls latest standards and re-expands @inherit blocks before reading the constitution. Discrepancies are flagged with resolution options.
- **Active standards integration in connect-wizard v1.2.0:** Step 7 now offers to apply discovered standards to an existing constitution, handles content duplication (>70% overlap detection), and runs discrepancy detection.
- **Troubleshooting entries:** Added 4 new entries for standards not appearing, @inherit-pending markers, standards conflict warnings, and @inherit not expanding.
- **Glossary entries:** Added @inherit-start/@inherit-end, @inherit-pending, and Discrepancy Detection. Updated @inherit and Shared Standards definitions.

### Changed
- **shared-context-sync v1.3.0:** Added `standards/` to local cache structure, `standards_hashes` to last-sync.json schema, standards-specific error handling entries, new integration points for sigil/constitution-writer/connect-wizard callers.
- **`/sigil` state detection reordered:** Shared context sentinel check and standards expansion now run before project foundation and context checks (items 2-3, was item 5).
- **Status dashboard format:** Constitution line now shows inherited article count (e.g., "7 articles (3 from shared standards)").
- **Documentation updated:** shared-context-setup.md, multi-team-workflow.md, user-guide.md, command-reference.md, troubleshooting.md, glossary.md all updated to reflect automatic @inherit expansion, start/end marker format, and discrepancy detection.

## [0.24.0] - 2026-02-19

### Fixed
- **`/sigil-update` hardcoded version:** Removed hardcoded "2.1.1" version string; now reads dynamically from `plugin.json`.
- **shared-context-sync version history ordering:** Fixed descending order (was 1.0.0, 1.2.0, 1.1.0 → now 1.2.0, 1.1.0, 1.0.0).
- **learning-reader version history ordering:** Fixed descending order.
- **quick-spec output contradiction:** Template said "not persisted" but Output section said it is. Clarified that specs persist to `/.sigil/specs/stories/` for downstream skills.
- **Quick Flow diagram:** Updated to match quick-spec persistence fix.
- **handoff-packager frontmatter version:** Frontmatter said 1.1.0 while version history showed 1.2.0. Synced frontmatter to 1.2.0.

### Added
- **Handoff destination branching (handoff-packager v1.2.0):** Users now choose between Option A (Branch + Technical Review Package) or Option B (Branch + Backlog Stories). Option B invokes story-preparer for Jira/Linear/Asana export. Single exit point for completed features.
- **knowledge-search in BA and Architect (v1.2.0 each):** Both agents now invoke knowledge-search for broader project context before starting work. Complements the existing learning-reader integration.
- **UI framework skills in Developer (v1.1.0):** Documented conditional routing to react-ui, vue-ui, flutter-ui, swift-ui, and react-native-ui based on project tech stack.
- **code-reviewer user_track branching (v1.2.0):** Non-technical track gets summary-focused report with plain-English descriptions; technical track gets full line-level detail with code snippets.
- **WCAG glossary entry:** Added Web Content Accessibility Guidelines definition to glossary.
- **`model` frontmatter field documented:** Added `model` field to skill definition format, extending-skills guide, and skills README with usage guidance.
- **Multi-team guide cross-reference:** Added link to multi-team-workflow.md from user guide's Learning Loop section.
- **Design phase label:** Standard Track workflow diagram now labels Phase 2 as "DESIGN + PLAN".
- **Enterprise track in user guide:** Added section explaining Enterprise track triggers (score 17-21), what it adds (research, mandatory ADRs, security review), and how to override track selection.
- **Specialist merge protocol doc:** Extracted merge logic from inline command/agent definitions into `docs/dev/specialist-merge-protocol.md`. Documents field precedence, tool union, constraint inheritance, and examples.
- **Artifact naming convention doc:** Created `docs/dev/artifact-naming-convention.md` cataloging all skill-generated artifacts, naming rules, and directory structure.
- **Phase count consistency:** Aligned glossary, user guide, and key concepts to 7 user-facing stages (Validate runs within Implement, Design runs within Plan).

### Changed
- **sprint-planner archived:** Removed from active skills, agents, chains, and docs. Moved to `archive/skills/sprint-planner/`.
- **story-preparer routing:** Now invoked by handoff-packager (was task-planner). Updated frontmatter, integration points, and agent references.
- **task-planner trimmed:** Removed sprint-planner and story-preparer from Skills Invoked; removed "stories", "backlog", and "sprint" trigger words.
- **technical-planner human checkpoints:** Standardized to track-based table format matching adr-writer.
- **Plugin version:** 0.23.1 → 0.24.0 (plugin.json, marketplace.json). ENFORCEMENT_VERSION unchanged at 2.3.0.
- **Quick Reference printable:** Updated phase header from 8 to 7 phases (removed Validate), version to 0.24.0, Task Planner description from "sprint planning" to "dependency ordering".

### Removed
- **VERSION file:** Deleted redundant `VERSION` file (was stale at 2.1.3; canonical version lives in `plugin.json`).

## [0.23.1] - 2026-02-19

### Changed
- **Personal config moved to `.sigil/config.yaml`:** `user_track` and `execution_mode` are now stored in `.sigil/config.yaml` (gitignored) instead of the `## Configuration` section in SIGIL.md. This prevents personal preferences from being committed to git and silently overriding other team members' settings.
- **SIGIL.md template:** Removed `## Configuration` YAML block. Updated `## Configuration Compliance` rule to reference `.sigil/config.yaml` with defaults.
- **`/sigil-config` command:** Reads and writes `.sigil/config.yaml` instead of SIGIL.md. Gracefully handles missing file by using defaults.
- **`/sigil-setup` command:** Writes config to `.sigil/config.yaml` immediately after role selection (Step 3). Adds `.sigil/config.yaml` to `.gitignore` entries.
- **Orchestrator, 4 skills, full-pipeline chain:** All config readers updated from SIGIL.md to `.sigil/config.yaml` with fallback defaults.
- **Automatic upgrade path:** When preflight-check detects an old-style `## Configuration` YAML block in SIGIL.md during update, it migrates values to `.sigil/config.yaml` and removes the block.
- **Plugin version:** 0.23.0 → 0.23.1 (plugin.json, marketplace.json). ENFORCEMENT_VERSION stays 2.3.0 (enforcement rules unchanged).

## [0.23.0] - 2026-02-19

### Added

**S3-100: Configuration System**
- **`/sigil-config` command:** View, set, and reset project-level configuration (user track, execution mode). Supports display, set, and reset modes with validation and human-readable descriptions.
- **Configuration section in SIGIL.md:** New `## Configuration` and `## Configuration Compliance` sections in the SIGIL.md enforcement template. Default config: `user_track: non-technical`, `execution_mode: automatic`.
- **Track question in `/sigil-setup`:** New Step 3 asks "What best describes your role?" to set user track during project setup. Selection persists to SIGIL.md Configuration section.
- **User track branching in 4 skills:** constitution-writer (v2.1.0), clarifier (v1.2.0), status-reporter (v1.1.0), and handoff-packager (v1.1.0) now adapt behavior based on `user_track`. Non-technical track auto-resolves technical decisions and uses plain English; technical track surfaces trade-offs and implementation details.
- **Orchestrator configuration awareness:** Session startup reads SIGIL.md Configuration. Routing, output formatting, and specialist visibility adapt to user track.
- **Full-pipeline configuration loading:** Pre-chain step loads `user_track` and `execution_mode` and passes them through the chain.

**S3-101: Specialist Agent Library**
- **9 specialist agent definitions** in `agents/specialists/`: api-developer, frontend-developer, data-developer, integration-developer (extend developer); functional-qa, edge-case-qa, performance-qa (extend qa-engineer); appsec-reviewer, data-privacy-reviewer (extend security). Each is 30-55 lines of domain-specific overrides.
- **`specialist-selection` skill (v1.0.0):** Selects appropriate specialist agents via file scope matching, keyword matching, and tech stack filtering. Handles multi-domain tasks and validation specialist assignment rules.
- **Specialist assignment in task-decomposer (v1.1.0):** New Step 4.5 invokes specialist-selection for each task. Tasks now include a `Specialist:` field.
- **Specialist loading in implementation loop:** `/sigil` command's Step 4b now loads specialist definitions, merges with base agents, and applies specialist behavior per-task. QA validation and security review phases also use specialist overlays.
- **Specialist routing in orchestrator (v1.6.0):** Added specialist-selection to Skills Invoked, specialist visibility rules by user track, and specialist routing documentation.
- **Full-pipeline specialist integration (v1.3.0):** specialist-selection added to per-task loop diagram (dev + QA), state transitions updated, agents-vs-skills note updated.
- **Agents README updated:** Replaced placeholder with full Specialists section covering inheritance model, all 9 specialists, and custom specialist instructions.

### Changed
- **ENFORCEMENT_VERSION:** 2.2.0 → 2.3.0 (preflight-check SKILL.md, preflight-check.sh, SIGIL.md template)
- **Plugin version:** 0.22.0 → 0.23.0 (plugin.json, marketplace.json)
- **SIGIL.md upgrade path:** When updating SIGIL.md from an older version, existing Configuration YAML values are parsed and merged back into the new template.
- **`/sigil-setup` renumbered:** Steps 3-7 renumbered to 4-8 to accommodate new track question at Step 3.

## [0.22.0] - 2026-02-18

### Added
- **Post-Completion Handoff Prompt (S25-004):** After code review passes, the orchestrator now presents a next-action prompt with three options: build another feature, hand off to an engineer, or wrap up. Handoff packages can now be generated inline at the natural completion point, without requiring users to independently remember `/sigil-handoff`. The standalone `/sigil-handoff` command remains available.
- **Feature Complete output template:** Added canonical completion summary format to `output-formats.md` for consistent post-review output.

### Changed
- **Command Retirement (S25-001):** Retired 8 slash commands whose functionality is already handled by the `/sigil` orchestrator: `sigil-spec`, `sigil-status`, `sigil-clarify`, `sigil-plan`, `sigil-tasks`, `sigil-validate`, `sigil-review`, `sigil-prime`. Users now use `/sigil "description"` to start features, `/sigil continue` to resume, and `/sigil` for status. Workflow phases (specify, clarify, plan, tasks, validate, review) and context loading run automatically.
- **Orchestrator updated:** Replaced `Skill(skill: "sigil-validate")` and `Skill(skill: "sigil-review")` invocations with direct skill SKILL.md reads, since command files no longer exist. Help output reduced from 18 commands to 10.
- **Preflight-check updated:** SIGIL.md enforcement template no longer lists retired commands. Mandatory skill invocation table replaced with orchestrator-handles-it explanation. ENFORCEMENT_VERSION bumped from 2.1.0 to 2.2.0.
- **Skill triggers updated:** Six skills (spec-writer, status-reporter, clarifier, technical-planner, qa-validator, code-reviewer) updated to reflect auto-invocation instead of standalone command triggers.
- **All documentation updated:** command-reference.md, user-guide.md, troubleshooting.md, shared-context-setup.md, multi-team-workflow.md, workflow-diagrams.md, quick-start.md, glossary.md, and example walkthrough updated to remove retired command references. Retired Commands migration table added to command-reference.md.
- **Cross-references cleaned:** Updated orchestrator.md, discovery-chain.md, output-formats.md, sigil-setup.md, sigil-connect.md, sigil-handoff.md, sigil-learn.md, sigil-profile.md, connect-wizard, profile-generator, shared-context-sync, visual-analyzer, and technical-planner to remove all retired command references.

### Removed
- Deleted 8 command files: `sigil-spec.md`, `sigil-status.md`, `sigil-clarify.md`, `sigil-plan.md`, `sigil-tasks.md`, `sigil-validate.md`, `sigil-review.md`, `sigil-prime.md`

## [2.1.3] - 2026-02-13

### Fixed
- **Broken link in status-reporter:** Fixed `context-management.md` reference missing `dev/` subdirectory (`/docs/context-management.md` → `/docs/dev/context-management.md`)

## [2.1.2] - 2026-02-12

### Fixed
- **ENFORCEMENT_VERSION drift:** Aligned preflight-check.sh and SKILL.md frontmatter to canonical 2.1.0
- **VERSION file drift:** Synced VERSION file (was 2.1.0, plugin.json was 2.1.1)
- **Troubleshooting paths:** Corrected `/memory` references to `.sigil/` throughout troubleshooting.md
- **Broken contributor links:** Fixed dead links to non-existent Development Workflows doc in docs/README.md and docs/dev/README.md
- **Legacy command references:** Updated `/memory/`, `/constitution`, `/status`, `/spec` to current `.sigil/`, `/sigil-constitution`, `/sigil-status`, `/sigil-spec` in test scenario docs
- **Test validator false errors:** Fixed validator to not error on never-run scenarios; corrected scenario output mode registry from FULL to QUICK
- **Broken checklist reference:** Fixed final-review-checklist.md reference to archived future-considerations.md
- **Stale skill versions:** Updated learning-capture, learning-reader, and preflight-check versions in versioning.md
- **Migration doc versions:** Updated enforcement version (2.0.0 → 2.1.0) and plugin version (2.0.0 → 2.1.2) in migration guide

### Fixed (Hooks)
- **session-summary.sh:** Field extraction now matches actual `project-context.md` format (`**Key:**` not `**Key**:`); fixed `Tasks Completed` → `Completed` to match template
- **verify-context-update.sh:** Implementation file detection now handles both absolute and relative paths
- **verify-context-update.sh:** Constitution update detection uses fixed-string match (`grep -qF`) to avoid false positives from wildcard dot

### Added
- `/sigil-handoff` command for engineer handoff package generation (renamed from `/handoff` to match `/sigil-*` namespace)
- `/sigil-handoff` and `/sigil-setup` added to workflow diagrams, command reference, and `/sigil help` output

### Changed
- **Installation instructions:** Updated Claude Code install from deprecated `npm install -g` to native installer (`curl` for Mac/Linux/WSL, desktop installer for Windows); removed Node.js as a prerequisite
- **Removed `installation.md`:** Consolidated install instructions into quick-start.md and the Setup Guide; the separate file was outdated and redundant

### Docs
- Updated README.md, quick-start.md, and Setup Guide (Notion + printable) with cross-platform install instructions
- Updated `/sigil-update` examples to use version-agnostic placeholders
- Fixed command reference to include `/sigil-setup` in overview, quick reference, and full section

## [2.1.0] - 2026-02-10

### Changed
- **Rebrand:** Prism OS → Sigil OS ("Inscribe it. Ship it.")
- Renamed `prism-plugin/` → `sigil-plugin/`
- Renamed all `/prism*` commands → `/sigil*` commands
- Updated all internal references, paths, and documentation
- Plugin install is now `claude plugin install sigil@sigil-os`
- Marketplace is now `claude plugin marketplace add araserel/sigil-os`
- Enforcement file renamed from `PRISM.md` → `SIGIL.md`

### Notes
- This is a name-only change — no logic, workflow, agent, skill, or hook behavior changes
- All existing workflows, specs, and project constitutions continue to work unchanged

## [2.0.0] - 2026-02-05 [now Sigil OS]

### Changed
- **BREAKING:** Migrated from configuration-layer framework to Claude Code plugin architecture
- Installation now uses `claude plugin install` instead of `install-global.sh`
- All agents, skills, commands, and templates bundled under `sigil-plugin/`
- Enforcement model changed from instruction-based to hook-based (programmatic)

### Added
- `plugin.json` manifest as canonical source of truth
- `hooks/` directory with 4 lifecycle hooks:
  - `preflight-check.sh` (SessionStart)
  - `verify-context-update.sh` (PostToolUse)
  - `validate-track-routing.sh` (SubagentStart)
  - `session-summary.sh` (Stop)
- Plugin marketplace distribution support

### Removed
- `install-global.sh` (replaced by plugin install)
- `~/.sigil-os/` update mechanism
- Legacy `sigil/` directory structure

### Migration Notes
- Existing users: Uninstall old global installation, then use `claude plugin install sigil@sigil-os`
- See ADR-D013 for full architectural decision record
