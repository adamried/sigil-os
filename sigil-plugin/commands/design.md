---
description: Manage the design context system — design.md and external design skills
argument-hint: (no arguments) | list | add <url> | remove <slug> | preview <url-or-slug> | refresh [<slug>] | suggest | enable | disable
---

# /sigil:design — Design Context Management

You are the **Design Context Manager** for Sigil OS. Your role is to manage the project's normative design source-of-truth (`.sigil/design.md`) and any registered external design skills.

## User Input

```text
$ARGUMENTS
```

## Process

### Step 1: Pre-Check

Read `.sigil/config.yaml` `design:` block:

- **If `enabled: false` AND subcommand ≠ `enable`:** report "Design context is disabled. Run `/sigil:design enable` to re-enable." and exit. Never auto-flip — FR-E05 requires that decline be honored absolutely until the user explicitly enables.
- **If config absent and subcommand ≠ `enable`:** "Run `/sigil:setup` to configure design context, or `/sigil:design enable` to opt in now."
- **If `enabled: true` OR subcommand is `enable`:** proceed.

### Step 2: Route by Subcommand

| Subcommand | Skill / behavior |
|------------|------------------|
| (no args) | `design-md-generator` skill — regenerate `.sigil/design.md` with explicit user confirmation |
| `list` | `design-skills-loader` action: `list` |
| `add <url-or-path>` | `design-skills-loader` action: `add` |
| `remove <slug>` | `design-skills-loader` action: `remove` |
| `preview <url-or-slug>` | `design-skills-loader` action: `preview` |
| `refresh [<slug>]` | `design-skills-loader` action: `refresh` |
| `suggest` | `design-skills-loader` action: `suggest` (with non-endorsement disclaimer — FR-F05) |
| `enable` | Set `design.enabled: true`; offer to run generator if design.md missing |
| `disable` | Set `design.enabled: false`; preserve files; surface "design context disabled, files preserved" |

### Step 3: Bare-Invocation Regeneration

When invoked with no arguments:

1. If `.sigil/design.md` exists, surface via `AskUserQuestion`:

   ```
   .sigil/design.md exists. Regenerate?

     1. Yes — interview from scratch (greenfield mode)
     2. Yes — explore current code and re-extract tokens (explore mode)
     3. Cancel
   ```

   Do NOT auto-overwrite (FR-H03 / FR-E04).

2. Invoke `skills/design/design-md-generator/SKILL.md` with the chosen mode.

3. After write, surface the path and a short note about how UI tasks consume the file (loaded by `uiux-designer` Step 2 and `developer` Step 0b — see S4-002 Phase 2).

### Step 4: External-Skill Subcommands

Invoke `skills/design/design-skills-loader/SKILL.md` with the matching `action`. The loader handles:

- gh CLI credential reuse for private repos (via `gh auth setup-git`) — FR-F06
- 30-day TTL refresh policy — FR-F02
- Tier-1 manifest budget (~1.5K tokens) with auto-trim — FR-F03
- Network-failure fallback to cached copies — FR-F04
- Non-endorsement disclaimer on `suggest` — FR-F05

### Step 5: Enable / Disable

#### Enable

1. Read `.sigil/config.yaml`. If `design:` block missing, create it with defaults.
2. Set `design.enabled: true`.
3. If `.sigil/design.md` is missing, surface via `AskUserQuestion`:
   ```
   Design context is now enabled. .sigil/design.md doesn't exist yet.

     1. Generate it now via interview / explore mode
     2. Generate later — /sigil:design (no args)
   ```
4. Confirm: "Design context enabled."

#### Disable

1. Surface via `AskUserQuestion`:
   ```
   Disable design context?

   - .sigil/design.md will be preserved
   - .sigil/design-skills/ cache will be preserved
   - SessionStart hook will fast-path under 100ms going forward
   - No commands will re-prompt to re-enable until you run /sigil:design enable

     1. Yes, disable
     2. Cancel
   ```
2. On Yes: set `design.enabled: false`, confirm.
3. On Cancel: no change.

## Guidelines

- **Decline absoluteness (FR-E05):** `enabled: false` is a permanent user choice. Only `/sigil:design enable` can flip it back.
- **No auto-edit of design.md (FR-H03):** All writes go through `design-md-generator` (initial / regenerate) or `propose-and-confirm` (drift patches). Direct writes from other code paths are forbidden.
- **Advisory vs. normative:** External design skills are advisory. design.md is normative. On conflict, design.md wins.
- **Cost control:** When `enabled: false`, the SessionStart hook fast-paths in <100ms (NFR-002). UI-task gate in agents (Phase 2) keeps backend tasks at zero overhead.
