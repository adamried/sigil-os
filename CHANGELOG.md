# Changelog

## [Unreleased]

### Added

#### S4-002 Phase 1: Design schema + generator + setup integration (FR-E01–E05, FR-I02–I04)

First layer of the design context system. Ships the schemas, generator, and setup integration; agent integration (Phase 2) and external skills (Phase 3) land separately.

**Templates (FR-E01, NFR-005 — first-class web parity):**

- `sigil-plugin/templates/design-md-mobile.md` — 15-section mobile-first schema with YAML token frontmatter (brand, color, typography, spacing, radii, motion, accessibility tokens). iOS + Android platform notes.
- `sigil-plugin/templates/design-md-web.md` — 15-section web schema, full parity with mobile (NOT a reduced fallback). Adds web-specific tokens: breakpoints, shadows, mono font family, container queries.

Both templates have identical section count and token completeness — web is first-class.

**Generator skill (FR-E03, FR-E04):**

`sigil-plugin/skills/design/design-md-generator/` — Single skill, two paths:

- **Greenfield interview** when source files < 5 and no theme files / component dirs exist. Six questions: brand voice, target platforms (mobile), color, typography, motion, accessibility baseline. Sensible platform-default fills for the rest.
- **Explore mode** when source files exist. Extracts tokens from `tailwind.config.*`, CSS custom properties, theme objects, iOS Asset Catalogs, Android resources. Inventories components. **Always confirms extracted values with the user before writing.**

`.sigil/design.md` is committed to git (it's normative project content). `.sigil/design-skills/` is gitignored (synced cache).

**SessionStart hook (FR-I03):**

`sigil-plugin/hooks/load-design-context.sh` registered in `hooks.json`. Fast-paths under 100ms when `design.enabled: false` (NFR-002). When enabled, surfaces only design.md path + skills manifest count — does NOT load design.md content (that's per-UI-task work for the agents in Phase 2).

**Setup integration (FR-I04, FR-E05 — hard-no decline):**

`commands/setup.md` Step 5.6 "Design Skills + design.md (Optional)" adds two independent opt-in prompts:

- **Prompt A:** External design skills (with 4-example curated list + non-endorsement disclaimer, deferred to Phase 3)
- **Prompt B:** Generate `.sigil/design.md` now / later / skip

Either prompt can be declined independently. Declines persist as `design.enabled: false`. No command may re-prompt — the only re-entry is `/sigil:design enable` (Phase 3).

**Config schema (FR-I02):**

```yaml
design:
  enabled: true | false        # explicit user choice — never auto-flipped
  profile: mobile | web        # set at setup, can change via /sigil:design
  skills: []                   # populated by /sigil:design add (Phase 3)
  component_globs: [...]       # optional override for net-new detection (Phase 2)
```

#### S4-001 Phase 5: Reconciliation wrap-up (NFR-005, FR-B02, FR-B03, FR-D05) + reserved flag (FR-A06)

**Linter multi-plugin support (NFR-005):**
- `tools/workflow-linter.py` gains two new checks: `check_companion_plugins` (lightweight structural validation for pm-copilot and po-buddy — plugin.json, commands/, skills/, frontmatter presence) and `check_shared_references_sync` (invokes `scripts/sync-references.sh --check` and surfaces out-of-sync files as errors).
- Linter now covers 110 files (was 107).
- Companion plugins that don't exist yet are skipped silently — supports incremental rollout.

**Routing extraction (FR-B02):**
- `commands/draw.md` no longer inlines a Natural Language Triggers table. All routing logic (trigger words, NL patterns, ticket detection, precedence) lives in `skills/workflow/routing-rules/SKILL.md` as the single source of truth.
- Orchestrator references `routing-rules` instead of duplicating it. Future routing changes require only one edit.

**Audit directory model (FR-B03 — full):**
- `skills/shared-protocols/audit-log-protocol.md` documents the new canonical storage: per-session files at `.sigil/audit/<ISO-timestamp>_<feature-slug>.md`. Legacy single-file `.sigil/audit-log.md` is auto-migrated on first audit interaction; the original is renamed to `.sigil/audit-log.md.migrated` (preserved, not deleted).
- `commands/audit.md` adds six subcommands: `latest` (default), `list`, `trace <session>`, `agent <name>`, `events <type>`, `clear`. Legacy `full` and `session` subcommands remain for pre-migration backward compat.

**CI workflow (FR-D05):**
- `.github/workflows/lint.yml` runs the workflow linter and the shared-references sync check on every PR and main push. Either failure blocks merge.

**Parallel execution config flag reserved (FR-A06, partial):**
- `parallel_execution: true|false` recognized by `/sigil:config` and persisted in config files. Setting `true` surfaces a one-time "reserved" notice — the underlying worktree-based parallel runner is deferred to a future spec. The config schema is forward-compatible so users can opt in once the runner ships.

**Deferred:**
- **FR-A06 (worktree-based parallel runner).** The full implementation requires significant orchestrator and developer-agent changes to support team-lead merge resolution. The config flag is reserved (above) but the runner is not yet implemented.
- **FR-C06 (design review command for Figma friction log).** P3 priority; designed for a Figma-only PM workflow that's better served by a focused future spec.

#### S4-001 Phase 4: PO Buddy plugin (po-buddy@0.1.0)

New plugin `po-buddy/` runs in Claude.ai Cowork — receives validated specs from PM Copilot, decomposes into stories, refines existing stories, prepares sprint-ready work. Generalized from gb-code-buddy's PO Buddy with all GasBuddy-specific content stripped (FR-C08).

**Commands (FR-C09–C12, C20):**

- `/receive <source> [Epic-key] [Confluence] [Team]` — Ingest a Validated Spec. Enforces the four-field cross-plugin handoff contract (FR-C09). Runs completeness check against the 10-section template.
- `/decompose [<epic-key>]` — Generate a phased Story Map from a received spec. Mandatory Approval Gate before any individual story is written. Figma MCP phased usage (no calls in Step 1, batching when 3+ frames in Step 2). Backend/Web/Mobile labels (one per story). AC format adapts to output target (FR-C10).
- `/story "<description>" | from-map <story-id> | from-map all` — Write individual stories. Quick standalone OR from approved Story Map. No-HOW policy. On-demand Figma usage only (FR-C11).
- `/addendum <description>` — Post-spec scope addition with `[A#]` traceability. Escalation check for substantial changes (FR-C12).
- `/design-ticket <title> [--target]` — Create UI/UX design request ticket using `references/design-ticket-template.md`. Local / Confluence / Jira targets (FR-C20).

**Skills (FR-C09–C12, C14, C16, C19–C23):**

- `receive` — handoff contract validation, completeness check, team identification
- `decompose` — Story Map generation with Figma phased rules, label assignment, AC format adaptation, Approval Gate
- `quick-story` — story writing with No-HOW enforcement and configurable format (FR-C19)
- `story-refinement` — improve existing stories with format compliance + quality checklist, refine-vs-rewrite logic (FR-C21)
- `prepare` — two-step Jira create pattern (skeleton + edit), mandatory PO confirmation gate (FR-C22)
- `sprint-summary` — read-only sprint planning summary; never writes externally (FR-C23)
- `addendum` — numbered `[A#]` addenda with substance categorization and revalidation routing
- `persona-lookup`, `scope-check`, `product-knowledge` — shared with PM Copilot (FR-C16)

**Configurable references (FR-C13, C14, C19):**

- `references/personas.md` (starter shipped; project customizes)
- `references/team-scope.md` (single-team mode by default; multi-team optional)
- `references/story-formats.md` (default format shipped; project overrides)
- `references/validated-spec-template.md`, `design-ticket-template.md`, `story-decomposition-template.md`, `communication-style.md` (synced from `shared-references/`)

**SessionStart hook (FR-D06 tightened for PO):** `po-buddy/hooks/hooks.json` declares NO SessionStart hook. All references load on demand. Per the FR-D06 update, PO Buddy is intentionally lighter than PM Copilot — only the skills that need a reference load it.

Marketplace manifest already lists po-buddy@0.1.0 from Phase 2.

#### S4-001 Phase 3: PM Copilot plugin (pm-copilot@0.1.0)

New plugin `pm-copilot/` runs in Claude.ai Cowork — no Bash, no file writes, no git. Helps PMs articulate problems, write validated specs, and hand off to engineering. Generalized from gb-code-buddy's PM Copilot, stripped of all GasBuddy-specific content.

**Commands (FR-C01, C02, C03, C04, C05):**

- `/define <problem>` — Problem articulation + Light / Standard / Complex triage. Pushes back on solution-shaped input.
- `/spec <description>` — 10-section Validated Spec from `references/validated-spec-template.md`. Supports `quick` mode (lightweight) and `from-define` (continues from prior Define). Includes persona selection guide and Discovery Design Brief detection.
- `/validate [<spec-id>]` — 10-point validation checklist with Villain Check. Max 3 rounds. Promotes to `Validated` status on full pass.
- `/handoff [<spec-id>] [--target local|confluence|jira]` — Packages spec with mandatory cross-plugin output contract (Epic key, Confluence link, Target team, Context line) for PO Buddy `/receive` consumption.

**Skills (FR-C07, C13, C14, C16):**

- `define` — problem-shape detection, triage axes (scope/ambiguity/risk)
- `specify` — 10-section writer with persona selection and Discovery Design Brief
- `validate` — 10-point checklist + Villain Check + Promote/Revise/Escalate verdict
- `handoff-prep` — output contract emitter, target adapter (local/Confluence/Jira)
- `business-case` — Complex-track Business Case using `references/business-case-template.md`
- `persona-lookup` — configurable personas resolver; supports anti-persona (Villain) pattern
- `scope-check` — scope creep detection + cross-team routing via `references/team-scope.md`
- `product-knowledge` — token-efficient index + on-demand load pattern (≤ 2K tokens always-on)

**Configurable references (FR-C13, C14, C17):**

- `references/personas.md` (starter template shipped; project customizes)
- `references/communication-style.md` (synced from `shared-references/`)
- `references/validated-spec-template.md` (synced)
- `references/business-case-template.md` (synced)
- `references/design-ticket-template.md` (synced)
- `references/team-scope.md` (project provides when multi-team)

**SessionStart hook (FR-D06):** Loads only `communication-style.md` + the product-knowledge index. Other references load on demand. Budget target ~2.5K tokens — well under the 6K cap.

PM Copilot runs in Claude.ai Cowork and depends on the marketplace manifest entry added in Phase 2.

#### S4-001 Phase 2: Multi-plugin infrastructure (FR-D01, FR-D02, FR-D03, FR-D04)

Sigil-os is becoming a three-plugin marketplace (sigil-plugin + pm-copilot + po-buddy). Phase 2 adds the cross-plugin scaffolding:

- **`shared-references/`** (FR-D01) — Single source of truth for files shared across plugins:
  - `validated-spec-template.md` — 10-section PM-to-engineering spec
  - `communication-style.md` — Tone, challenge model, yielding policy, output modes
  - `business-case-template.md` — ROI / investment analysis for Complex-track features
  - `design-ticket-template.md` — UI/UX design request format
  - `story-decomposition-template.md` — Story Map output format
- **`scripts/sync-references.sh`** (FR-D02) — Distributes `shared-references/` to each plugin's `references/` directory at build time. Supports `--check` (CI use, exits non-zero if out of sync) and `--list` (shows distribution table). Plugins never read from `shared-references/` at runtime — they read their own copies. Gracefully skips distributions to plugin directories that don't exist yet.
- **`scripts/bump-version.sh`** (FR-D03) — Atomically bumps a plugin's version in `plugin.json`, `marketplace.json`, and (for sigil-plugin) the README badge. Supports `--show` to list current versions across all three plugins.
- **`.claude-plugin/marketplace.json`** (FR-D04) updated to list all three plugins: `sigil@0.32.0`, `pm-copilot@0.1.0` (placeholder), `po-buddy@0.1.0` (placeholder). PM and PO plugin directories will land in Phase 3 and Phase 4.

#### S4-001 FR-A07: Three-layer configuration cascade

Configuration now loads from three layers in cascade order:

1. **Defaults** (built-in)
2. **Global** — `~/.sigil/config.yaml` (personal preferences across all projects)
3. **Project** — `.sigil/config.yaml` (current project overrides)

Project wins over Global wins over Defaults.

**`/sigil:config` updates:**
- Display mode reads both layers and shows each value with a `(project)`, `(global)`, or `(default)` provenance tag, plus a Layers-loaded footer.
- `set [--global] <key> <value>` writes to the project layer by default; pass `--global` to write to `~/.sigil/config.yaml` (created on first write).
- `reset [--global]` removes the target file (instead of writing defaults) so lower layers govern cleanly.

**Orchestrator (`commands/draw.md` Step 0b)** now performs the cascade at session start and carries effective values (`user_track`, `execution_mode`, `audit_mode`) into the session context. No skill or chain needs to know about layers — they consume effective values only.

Existing projects that only have `.sigil/config.yaml` continue to work unchanged.

#### S4-001 FR-A10: Greenfield profile interview

`profile-generator` (now 1.2.0) gains a greenfield interview path. When the project has fewer than 5 source files AND no recognizable signal files (`package.json`, `Cargo.toml`, etc.), the skill skips its auto-detection scan and runs a structured six-question interview:

1. Primary language
2. Framework or runtime
3. Test runner
4. Package manager
5. Deploy target
6. Linked product docs (Confluence, Notion, README)

Output schema is unchanged — downstream consumers don't care which path filled the profile. Two metadata flags (`population_method`, `greenfield`) are recorded so later tooling can distinguish detected vs. interviewed projects.

### Changed

#### S4-001 FR-B06: GitHub MCP → `gh` CLI migration

Cross-repo shared-context sync no longer requires GitHub MCP. A new helper script `sigil-plugin/scripts/gh-sync.sh` routes all remote file operations through the `gh` CLI:

| Subcommand | Purpose | Replaces |
|------------|---------|----------|
| `read <repo> <path> [<branch>]` | Read a single file | `mcp__github__get_file_contents` (file) |
| `list <repo> <path> [<branch>]` | List directory entries as JSON | `mcp__github__get_file_contents` (dir) |
| `write <repo> <path> <local-file> <message> [<branch>]` | SHA-safe create-or-update | `mcp__github__create_or_update_file` |
| `push-batch <repo> <branch> <message> <manifest-json>` | Multi-file single-commit push via Git Data API | `mcp__github__push_files` |

Prerequisites: `gh` CLI authenticated (`gh auth login`) and `jq` installed. If either is missing, the helper exits with code 2 and a structured JSON error; the calling skill queues the operation locally (no fallback to direct `git` CLI).

**Skills migrated:**
- `shared-context-sync` → 2.0.0 (Critical Constraint, gh CLI Availability Detection section, Push/Pull procedures all reference `gh-sync.sh`; `mcp__github__*` removed from `tools:`)
- `connect-wizard` → 1.5.0 (frontmatter, Step 2 availability check, scaffolding all reference `gh-sync.sh`; `mcp__github__*` removed from `tools:`)
- `profile-generator` → unchanged version (frontmatter cleanup; Critical Constraint references `gh-sync.sh`)

**CLAUDE.md updates:** "Available Integrations" table now lists `gh` CLI as the primary integration with GitHub MCP marked as deprecating. Architecture Principle 7 updated to reflect the migration.

**Backward compatibility:** The `.mcp.json` GitHub MCP server registration is retained temporarily for unmigrated paths. It will be removed in a follow-up after end-to-end verification on a test shared-context repo.

#### S4-001 FR-B05: Output format centralization

`commands/draw.md` no longer duplicates output templates inline. The Welcome screen, Status Dashboard, Help output, Continue/Resume header, and Step 5 Visual Status Format are now defined only in `templates/output-formats.md`. The orchestrator references the canonical sections by name.

`templates/output-formats.md` Help Output expanded to include the new commands shipped in FR-A05 (standalone pipeline) and FR-A09 (companion entries):

- Companion Commands: `/sigil:dashboard`, `/sigil:status`, `/sigil:continue`
- Pipeline Stage Commands: `/sigil:spec`, `/sigil:tasks`, `/sigil:review`, `/sigil:export`

The contract is now explicit: if a needed format is missing, add it to `output-formats.md` first; never inline a new format in a command or skill file.

#### S4-001 FR-A08: Dynamic QA fix limits

QA fix-loop iteration limits no longer appear as hardcoded numbers (`5`, `1`) inside chain files. The `qa-engineer` agent (now 1.4.0) is the canonical source: a new **Fix Limits** table specifies max attempts per track (Standard/Enterprise: 5; Quick Flow: 1) and supports per-project overrides via `.sigil/config.yaml`.

`chains/full-pipeline.md` (→ 1.7.0) and `chains/quick-flow.md` (→ 1.6.0) reference the agent's table instead of inlining the numbers. Track-dependent behavior is preserved.

Note: The orchestrator (`commands/draw.md`) keeps progress-display references like `attempt N/5` since it renders the indicator at runtime — those values are derived from the agent's table per the active track.

#### S4-001 FR-B07: Preflight skill-resolution hint (enforcement v2.5.0)

`SIGIL.md` now ships with an explicit Skill Resolution section listing the 12 skill categories and the canonical lookup path:

```
${CLAUDE_PLUGIN_ROOT}/skills/<category>/<skill-name>/SKILL.md
```

This eliminates the multi-minute Glob fallback that occurred when Claude resolved a skill name without knowing its category. The phase-handoff table also gained `security` and `verified` rows reflecting FR-A02/A03/A04.

Component locations updated to reflect 10 agents (was 9) and the additional commands shipped in FR-A05/A09. Enforcement version bumped from 2.4.0 to 2.5.0 in both `skills/workflow/preflight-check/SKILL.md` and `hooks/preflight-check.sh` (these stay synchronized).

#### S4-001 FR-B01: Code Reviewer is now a canonical agent handoff

Reconciled the code review invocation model. Previously the orchestrator and QA Engineer invoked the `code-reviewer` skill directly, despite a `code-reviewer` agent file already existing. The agent and skill now have a clear, single-source contract:

- **Code Reviewer agent** (`agents/code-reviewer.md`, bumped to 1.1.0) is the canonical entry point for all code review work. Receives the QA Engineer's validation report and runs the review using its skill internally.
- **`code-reviewer` skill** (bumped to 1.4.0) is now invoked only by the agent. Frontmatter `invoked_by` updated. A new Invocation Contract section makes this explicit.
- **Orchestrator** (`commands/draw.md`) and **QA Engineer** (`agents/qa-engineer.md`) now hand off to the agent, not the skill.
- **`/sigil:review`** standalone command also routes through the agent for consistency.

Sigil-os retains its existing richer code-reviewer implementation (verdict system, user track adaptation, waiver awareness, review checklist) — only the invocation path changed.

### Added

#### S4-001 FR-A01: Autonomous execution mode

Added a third option to `execution_mode`: `autonomous`. When enabled, the orchestrator runs the entire pipeline without per-step interactive prompts. Standard checkpoints (phase transitions, "ready to plan?", "ready to decompose?") are auto-accepted. The mode ends with a mandatory cumulative-diff review covering all branch commits.

**Safety gates always pause regardless of mode:**

- Constitution Article violations
- Security blockers (Critical/High findings)
- Code review "Request changes" with blockers
- QA fix loop exhaustion
- Override expirations and inheritance conflicts
- Out-of-scope file detection in per-task commits (FR-A03)
- Fatal errors and unrecoverable state

**Requires** `user_track: technical`. Toggling `execution_mode: autonomous` via `/sigil:config` surfaces a one-time acknowledgement explaining the trade-off; users must explicitly opt in.

Affects `commands/config.md`, `commands/draw.md` (Step 0b adds an Autonomous Mode Behavior subsection), `chains/full-pipeline.md` (→ 1.6.0), and `chains/quick-flow.md` (→ 1.5.0). `automatic` and `directed` modes are unchanged.

#### S4-001 FR-A02 / FR-A03 / FR-A04: Feature branch + per-task commits + verified commits

The full-pipeline workflow now produces a cleaner git history without manual intervention:

- **Feature branch (FR-A02).** Before committing spec artifacts, the orchestrator creates a feature branch — using the constitution Article 2 naming convention if defined, otherwise `sigil/<spec-dir-name>`. The branch is local until the eventual push/PR checkpoint.
- **Per-task commits (FR-A03).** After each task's QA validation passes, the orchestrator commits the task's vetted files via the `commit-conventions` skill. Out-of-scope changes are detected (modifications to files not in the task's declared file list) and the user is prompted via `AskUserQuestion` to include / stash / discard. No silent inclusion of out-of-scope changes. No broad `git add -A`. Per-task commits apply to both full pipeline and Quick Flow.
- **Per-feature security report (FR-A04).** After security review runs, the security agent now writes `.sigil/specs/<feature>/security.md` as the canonical security record for that feature. The file has a fixed structure (Scope, Summary, Findings, Verdict, Sign-off) and is the source of truth for the subsequent verified commit.
- **Verified commit (FR-A04).** When security review passes on the full pipeline, the orchestrator emits a feature-level `verified: <feature> security pass` commit that references the security.md path. This is the new `verified:` commit type defined in `commit-conventions`. Quick Flow opts out entirely — no security review, no security.md, no verified commit.
- **Feature-Level Status table.** `templates/tasks-template.md` gains a Feature-Level Status block tracking QA / code review / security review / verification commit gates separately from per-task status. Quick Flow marks security and verification as `[—] N/A (Quick Flow)`.
- **Chain version bumps.** `chains/full-pipeline.md` → 1.5.0, `chains/quick-flow.md` → 1.4.0 documenting these changes.

Updated agents (`developer`, `security`), the orchestrator (`commands/draw.md`), the `commit-conventions` skill (now 1.1.0), the chains, and `templates/tasks-template.md`.

#### S4-001 FR-A09: Three companion entry commands

Added `/sigil:dashboard`, `/sigil:status`, and `/sigil:continue` as terse companion entry points alongside `/sigil:draw`:

- **`/sigil:dashboard`** — Read-only project status overview with a single suggested next action. Mirrors the dashboard `/sigil:draw` shows with no arguments, but never prompts the user.
- **`/sigil:status`** — Read-only detailed mid-workflow status. Delegates to the existing `status-reporter` skill. Adds an active-waivers count, audit-entries count, and (technical track) spec artifact inventory.
- **`/sigil:continue`** — Resume the current workflow. Delegates to the same logic as `/sigil:draw continue`. Single source of truth remains in `commands/draw.md`.

`/sigil:draw` remains the recommended unified entry point. These commands provide shorter invocations for common operations during long sessions without forking workflow logic.

#### S4-001 FR-A05: Four standalone pipeline commands

Added four new commands so users can run pipeline stages independently of the unified `/sigil:draw` orchestrator:

- **`/sigil:spec`** — Write or manage a feature specification on its own. Supports `list`, `quick "description"`, opening an existing spec by path, or starting a full spec from a description. Stops after spec authoring; does not auto-advance through clarifier/planner/decomposer.
- **`/sigil:review`** — Run code or security review on demand. Scopes: `code` (default), `security`, `full` (both sequentially), or against a specific spec path. Produces reports under `.sigil/specs/<feature>/reviews/` or `.sigil/reviews/`. Does not enter the QA fixer loop.
- **`/sigil:export`** — Produce a stakeholder-friendly, plain-language summary of a feature for non-engineering audiences. Writes `stakeholder-summary.md` to the feature's spec directory. Distinct from `/sigil:handoff` (engineer-targeted).
- **`/sigil:tasks`** — Decompose an existing `plan.md` into tasks. Non-destructive by default — if `tasks.md` exists, offers regenerate/append/cancel via `AskUserQuestion`.

`/sigil:draw` remains the recommended unified entry point. These commands give users finer-grained access for spec-only work, on-demand reviews, stakeholder communication, and post-hoc task decomposition.

---

## [0.32.0] - 2026-03-20

### Changed

#### Breaking: Command Rename — `/sigil-*` → `/sigil:*`

All commands renamed to remove the redundant `sigil-` prefix. The plugin namespace (`sigil:`) already provides collision avoidance with Claude Code built-ins, making the prefix unnecessary. The main entry point gets a new name: `/sigil:draw` — thematic with the "Inscribe it. Ship it." tagline.

| Old | New |
|-----|-----|
| `/sigil` | `/sigil:draw` |
| `/sigil-setup` | `/sigil:setup` |
| `/sigil-audit` | `/sigil:audit` |
| `/sigil-config` | `/sigil:config` |
| `/sigil-constitution` | `/sigil:constitution` |
| `/sigil-connect` | `/sigil:connect` |
| `/sigil-handoff` | `/sigil:handoff` |
| `/sigil-learn` | `/sigil:learn` |
| `/sigil-profile` | `/sigil:profile` |
| `/sigil-update` | `/sigil:update` |

All cross-references in skills, chains, agents, templates, hooks, and docs updated.

#### Version

- Plugin version bumped from 0.31.0 to 0.32.0 (plugin.json, marketplace.json, README.md).

---

## [0.31.0] - 2026-03-18

### Added

- **`/sigil-audit` command** — View and manage the workflow audit log. Supports summary, full, session, and clear modes. Shows a plain-language view for non-technical track and skill/agent names for technical track. (`commands/sigil-audit.md`)
- **Audit log protocol** — Reusable shared protocol for appending workflow events to `.sigil/audit-log.md`. Defines session headers, entry types (workflow-start, phase, handoff, task, completion), and append-only rules. (`skills/shared-protocols/audit-log-protocol.md`)
- **Audit log template** — Starter file created when audit mode is first enabled. (`templates/audit-log-template.md`)
- **Audit status in status dashboard** — When `audit_mode: true`, the `/sigil` status dashboard shows `Audit Mode: Active | Entries: {n}` after the Constitution line, so users can confirm audit is running at a glance. (`commands/sigil.md`, `templates/output-formats.md`)
- **Shared Standard template** — `templates/shared-standard-template.md` for organizations to define structured, machine-readable engineering standards that can be pulled into project constitutions via shared context sync. Includes YAML frontmatter (enforcement level, article mapping, description), rules, exceptions, constitution article snippet, and verification checklist. Referenced in `connect-wizard/references/standards-integration.md`.

### Changed

- **`/sigil-config`** — Added `audit_mode` setting (true/false). Displays audit mode status and description in config view. Creates audit log file when enabled. (`commands/sigil-config.md`)
- **`/sigil-setup`** — Step 3.5 (shared context connection) now runs before Step 4 (constitution creation), so discovered shared standards can be passed to the constitution writer during initial setup. (`commands/sigil-setup.md`)
- **`sigil.md` orchestrator** — Added Step 0b (load audit mode flag), per-phase audit logging throughout the workflow, and audit entry count detection for the status dashboard. (`commands/sigil.md`)
- **Pre-execution check protocol** — Extended with optional audit log step: skills record a `phase` entry when `audit_mode: true`. (`skills/shared-protocols/pre-execution-check.md`)
- **Full pipeline and Quick Flow chains** — Updated to reflect audit logging at phase transitions. (`chains/full-pipeline.md`, `chains/quick-flow.md`)
- **Command reference** — Added `/sigil-audit` command documentation and audit mode configuration details. (`docs/command-reference.md`)

### Version

- Plugin version bumped from 0.30.0 to 0.31.0 (plugin.json, marketplace.json, README.md).

---

## [0.30.0] - 2026-03-11

### Added

#### New Reference Files
- **Shared Protocol: Pre-Execution Check** — Reusable protocol for updating project-context.md before skill execution. Skills reference this instead of inlining identical instructions. (`skills/shared-protocols/pre-execution-check.md`)
- **Constitution Writer article templates** — Project-type cascade (MVP/Production/Enterprise) with auto-config defaults per article, plus jargon translation table for non-technical users. (`skills/workflow/constitution-writer/references/article-templates.md`)
- **Constitution Writer question bank** — Tiered question strategy (Auto-Decide / Translate / Ask Directly) with project category detection and context-filtered questions. (`skills/workflow/constitution-writer/references/question-bank.md`)
- **Routing Rules reference skill** — Single source of truth for orchestrator routing logic: trigger word matrix, natural language patterns, routing precedence, context-aware routing. (`skills/workflow/routing-rules/SKILL.md`)
- **Code Reviewer review checklist** — Detailed review criteria covering code style, architecture, error handling, complexity, DRY, security, performance, and testing with severity levels. (`skills/review/code-reviewer/references/review-checklist.md`)
- **QA Fixer fix categories** — Categorizes fix types (lint, format, import, type, test, accessibility) with auto-fix capabilities, escalation rules, and language-specific tool mappings. (`skills/qa/qa-fixer/references/fix-categories.md`)
- **Foundation Writer example** — Complete worked example of a foundation document (TaskFlow project). (`skills/engineering/foundation-writer/references/example-foundation.md`)
- **Knowledge Search scoring algorithm** — Explicit scoring formula with keyword match, recency, source weight, and context relevance components. (`skills/research/knowledge-search/references/scoring-algorithm.md`)
- **Connect Wizard standards integration** — Protocol for applying shared team standards to constitutions with enforcement levels, integration discovery for tool adapters. (`skills/shared-context/connect-wizard/references/standards-integration.md`)

#### New Agent
- **Code Reviewer agent v1.0.0** — Dedicated agent for code review with structured verdict system (Approve/Request Changes/Block), learning integration, tech debt tracking, and override awareness.

#### New Engineering Skills
- **Commit Conventions v1.0.0** — Generalized commit conventions reference skill. Conventional Commits format, configurable ticket prefix detection from branch name, constitution-based overrides.
- **Test Generator v1.0.0** — Framework-agnostic test generation. Auto-detects test framework (Jest, pytest, Go test, RSpec, Vitest, etc.), generates tests following project patterns, supports coverage-driven and TDD modes.
- **Database Migration v1.0.0** — Tool-agnostic migration generation. Detects migration tool (Prisma, Knex, Alembic, Flyway, etc.), generates migration + rollback files, validates data integrity and destructive change safety.
- **Documentation Generator v1.0.0** — Code-analysis-based documentation generation. README generation, API doc extraction, inline doc standards per language (JSDoc, docstrings, GoDoc).
- **Refactoring Backend v1.0.0** — Structured backend refactoring with safety guarantees. Service extraction, dependency analysis, API compatibility preservation, test-first refactoring.
- **Refactoring Frontend v1.0.0** — Structured frontend refactoring with safety guarantees. Component extraction, state management refactoring, bundle impact analysis, accessibility preservation.

### Changed

#### Skill Reorganization
- **foundation-writer v1.1.0** — Moved from `workflow/` to `engineering/` category. Engineering skills handle technical implementation; workflow skills handle orchestration mechanics.
- **task-decomposer v1.2.0** — Moved from `workflow/` to `engineering/` category.
- **technical-planner v1.2.0** — Moved from `workflow/` to `engineering/` category.
- **spec-writer v1.1.0** — Moved from `workflow/` to `specification/` category. Specification authoring is a distinct concern from orchestration.

#### Version
- Plugin version bumped from 0.29.0 to 0.30.0 (plugin.json, marketplace.json, README.md).
- `docs/dev/extending-skills.md` — Updated skill category table to reflect reorganization and new skills.

## [0.29.0] - 2026-03-09

### Added

#### Group A — Pure Enhancements (sigil-gb → sigil-os merge)
- **Model tier assignments:** Added `model:` frontmatter field to all 9 agent files and 2 workflow skills — `opus` for Orchestrator, Developer, QA Engineer, Architect, Security; `sonnet` for Business Analyst, DevOps, Task Planner, UI/UX Designer; `haiku` for preflight-check and status-reporter.
- **Implement-Ready chain v1.0.0:** New chain for pre-decomposed tickets (Stories with acceptance criteria). Skips spec-writer, clarifier, and task-decomposer; treats the story as a single task with AC as the spec.
- **Quick Flow handoff-back step (v1.3.0):** Added conditional handoff-back step after qa-fixer/learning-capture — writes results back to the originating ticket when `ticket_key` exists in context.
- **Skill-frontmatter JSON Schema:** New `sigil-plugin/schemas/skill-frontmatter.json` for linting SKILL.md frontmatter fields including model tier validation.
- **UI skill worked examples:** Full end-to-end StatusBadge examples added to Flutter, SwiftUI, and Vue 3 UI skills (component + tests + handoff JSON).
- **knowledge-search worked example:** Added full query→result worked example (user profiles search through all 5 steps) and updated invocation triggers in description.
- **specialist-selection v1.1.0:** Removed tabled `payment-developer` specialist routing; added Stripe webhook worked example with keyword tiebreaking; updated version history.
- **figma-review updates:** Added invocation triggers to description; expanded `tools` field with explicit Figma MCP tool names (`mcp__figma__get_design_context`, `mcp__figma__get_screenshot`, `mcp__figma__get_metadata`, `mcp__figma__get_variable_defs`).
- **status-reporter invocation triggers:** Updated description to include "where are we", "show progress", "what's done" triggers.
- **clarifier invokes comment:** Documented that orchestrator handles routing after clarifier completes, not direct invocation.

#### Group B — Items Requiring Setup Docs
- **Pre-decomposed ticket routing in `/sigil`:** Ticket routing table now shows `pre-decomposed → Implement-Ready chain` (Stories with non-empty acceptance criteria bypass spec/clarify/task-decompose).
- **Jira skill v1.2.1:** Pre-decomposed category detection (Story + non-empty AC → `pre-decomposed`); epic name override (parent epic summary matched against `maintenance_epic_patterns` → `maintenance`); configurable custom field IDs for story_points and acceptance_criteria via `config.custom_fields`.
- **Jira adapter config template:** New `sigil-plugin/integrations/jira.yaml` — generalized template with setup instructions for copying to a shared context repo.
- **Team config hook:** New `sigil-plugin/hooks/load-team-config.sh` — detects active team from repo context using user-configured glob patterns in `.sigil/team-config.yaml`; writes `sigil_team`, `sigil_team_id`, `sigil_board_id` to config on session start.
- **Enhanced project profiles (profile-generator v1.1.0):** 5 new optional profile sections with auto-detection and interactive prompts: Databases, API Surface, Auth Model, Domain Glossary, Project Structure. YAML template extended with all 5 sections.
- **MCP profile selection in setup (Step 5.5):** During `/sigil-setup`, if MCP adapters were discovered, user is asked for their primary dev focus (Backend/Frontend/Full-Stack/Custom). Writes `mcp_profile:` to `.sigil/config.yaml` to control MCP tool warnings.

#### Group C — Documentation
- **codebase-assessment reference extraction:** Extracted ~130-line stack detection section to `references/stack-signals.md`; SKILL.md references the file instead of inlining content.
- **shared-context-sync v1.6.0 reference extraction:** Extracted ~570-line protocol documentation to `references/sync-protocol.md`; SKILL.md updated to note it is an infrastructure skill and references the protocol file.

### Changed

- **`tools:` format normalization:** Changed array syntax (`[Read, Write]`) to comma-string (`Read, Write`) across 10+ skill files for consistency with the frontmatter schema.
- **`docs/mcp-integration.md` major rewrite:** Added comprehensive Jira setup section (5 steps: field IDs → template → fill values → push → test) and Team Config Hook documentation. Replaced Slack with Context7 in integrations table; added Status column.
- **`docs/command-reference.md`:** Updated `/sigil-profile` step count 6→7; added Profile Sections table listing all 10 sections (5 required, 5 optional); added pre-decomposed routing details to ticket routing description.
- **`docs/glossary.md`:** Added 5 new entries for optional profile sections (Databases, API Surface, Auth Model, Domain Glossary, Project Structure).
- **Profile description updates:** `docs/user-guide.md`, `docs/shared-context-setup.md`, and `docs/multi-team-workflow.md` updated to mention optional profile sections.
- **`templates/output-formats.md`:** Extended Project Profile format with 5 optional sections.
- **`hooks/hooks.json`:** Added `load-team-config.sh` to SessionStart hooks (async, 5s timeout).
- **chains/README.md:** Added `implement-ready` to chain listing.

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
