---
name: design-skills-loader
description: Sync external design-skill repositories into .sigil/design-skills/ as advisory context. 30-day TTL refresh, network-failure fallback to cached copies, Tier-1 manifest budget under ~1.5K tokens. design.md is normative; these skills are advisory.
version: 1.0.0
category: design
chainable: false
invokes: []
invoked_by: [design]
tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# Skill: Design Skills Loader

## Purpose

Manage advisory external design skills synced from GitHub URLs or local paths into `.sigil/design-skills/<slug>/`. Maintain a Tier-1 manifest under ~1.5K tokens for always-on inclusion. Refresh skills every 30 days. Never block a UI task on network failure — fall back to cached copies.

**Authority:** design.md is normative (FR-E02). These skills are advisory. When they disagree, design.md wins.

## When to Invoke

- `/sigil:design add <url-or-path>` — register a new skill
- `/sigil:design remove <slug>` — drop a skill from the registry
- `/sigil:design refresh [<slug>]` — force re-sync
- `/sigil:design list` — show all registered skills
- `/sigil:design preview <url-or-slug>` — fetch metadata without cloning
- `/sigil:design suggest` — show 4 example URLs + non-endorsement disclaimer
- SessionStart hook (Phase 1) surfaces the manifest summary
- UI/UX Designer and developer agents load the manifest summary as advisory context (Phase 2)

## Inputs

- `action`: `add | remove | refresh | list | preview | suggest`
- `target`: URL, slug, or local path (subcommand-dependent)

## Process

### Storage Layout

```
.sigil/
├── design.md                       ← normative (committed, never auto-edited)
├── design-skills/                  ← gitignored
│   ├── .manifest.json              ← generated, always-on (~1.5K tokens)
│   ├── <slug>/                     ← one directory per registered skill
│   │   ├── SKILL.md                ← cloned content
│   │   ├── references/             ← cloned content (optional)
│   │   └── .meta.json              ← slug, source, cached_at, hash
│   └── ...
```

### Step 1: Add a Skill (`action: add`)

```
1. Validate target: must be GitHub URL (https://github.com/owner/repo) or local path
2. Derive slug from repo name (last path segment, lowercase, hyphenated)
3. If slug already registered, prompt: "Replace existing? Force refresh? Cancel?"
4. Sync (see Step 5 — Sync Procedure)
5. Update .sigil/config.yaml design.skills[]:
     - slug, source, enabled: true, cached_at: <ISO timestamp>
6. Regenerate .manifest.json (Step 4)
7. Confirm to user
```

### Step 2: Remove (`action: remove`)

```
1. Confirm with the user: "Remove <slug>? Cached files at .sigil/design-skills/<slug>/ will be deleted."
2. Delete .sigil/design-skills/<slug>/
3. Remove from .sigil/config.yaml design.skills[]
4. Regenerate .manifest.json
```

### Step 3: Refresh (`action: refresh`)

```
For each (or one) registered skill:
1. Compare cached_at to now; if < 30 days AND not forced → skip
2. Otherwise: re-run Sync Procedure (Step 5)
3. Update cached_at
4. Regenerate .manifest.json
```

### Step 4: Manifest Generation (Tier-1 Budget — FR-F03, ~1.5K tokens)

`.sigil/design-skills/.manifest.json` is the always-on file. Budget: ~1.5K tokens.

Format:

```json
{
  "version": 1,
  "generated_at": "<ISO>",
  "skills": [
    {
      "slug": "...",
      "source": "...",
      "summary": "<1-sentence purpose from SKILL.md frontmatter description>",
      "references": ["..."],
      "cached_at": "<ISO>",
      "enabled": true
    }
  ]
}
```

**Budget enforcement (auto-trim order):**

1. If estimated tokens > 1.5K, trim each skill's `summary` to one line (drop multi-line descriptions).
2. If still over, drop the `references` field entirely from each entry.
3. If still over, mark skills `enabled: false` from the oldest `cached_at` until under budget.
4. Surface a one-time warning to the user: "Manifest at budget — N skills enabled, M deferred. Remove some with `/sigil:design remove <slug>`."

### Step 5: Sync Procedure

For each skill:

```
1. If source is a GitHub URL:
   - Use `git clone --depth 1 <url> .sigil/design-skills/<slug>/`
   - Authenticate via gh CLI: if `gh auth setup-git` has been run, git clone
     reuses gh credentials for private repos (FR-F06)
   - On network failure (no connectivity, auth failure, repo not found):
     - If a cached copy exists at .sigil/design-skills/<slug>/, leave it alone
       (FR-F04 — never block a UI task on sync failure)
     - Surface a one-line warning: "Sync failed for <slug>; using cached copy from <cached_at>"
     - Continue (do not exit non-zero)

2. If source is a local path:
   - Use rsync (or cp -r) to mirror into .sigil/design-skills/<slug>/

3. Compute SHA-256 of the SKILL.md to detect changes; record in .meta.json
```

### Step 6: Preview (`action: preview`)

Without cloning, fetch the SKILL.md frontmatter from the URL via `gh api repos/<owner>/<repo>/contents/SKILL.md` (returns base64-encoded content; decode and parse the YAML block). Render summary to the user.

If preview fails (private repo without auth, no SKILL.md at root), surface the gap with guidance.

### Step 7: Suggest (`action: suggest` — FR-F05)

Surface the 4 example URLs **with explicit non-endorsement disclaimer**:

```
Suggested external design skills (NOT endorsed)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The following 4 skills are commonly referenced in the design-skills
community. They are NOT endorsed by sigil-os, by Anthropic, or by their
authors. Their authors do not support this project. Use at your own risk.

  1. Impeccable     https://github.com/<placeholder-org>/impeccable-design
  2. Huashu         https://github.com/<placeholder-org>/huashu-design
  3. UI/UX Pro Max  https://github.com/<placeholder-org>/uiux-pro-max
  4. Taste          https://github.com/<placeholder-org>/taste-design

To inspect before adding:
  /sigil:design preview <url>

To register:
  /sigil:design add <url>
```

> **Note:** The URLs above are placeholders. Sigil-os does not curate the actual list — projects supply their own design-skill repositories. The pattern matches gb-code-buddy v0.39.0 verbatim with the disclaimer intact.

### Step 8: List (`action: list`)

Render the manifest as a human-readable table:

```
Registered Design Skills
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

slug                source                       cached_at       enabled
impeccable          github.com/.../impeccable    2026-05-15      ✓
taste               github.com/.../taste         2026-04-30      ✓ (TTL exceeded — refresh recommended)
my-local            ./design-local               2026-05-27      ✓

Manifest size: 0.8K / 1.5K tokens
Run `/sigil:design refresh` to sync stale skills.
```

## Network-Failure Fallback Contract (FR-F04)

Sync failures NEVER block a UI task. The cascade is:

1. Try fresh sync via gh CLI.
2. If sync fails AND cached copy exists → use cached copy, log warning.
3. If sync fails AND no cached copy exists → skip this skill (do not include in manifest), log warning.

UI tasks always have a non-fatal manifest to work with.

## Output

Per action:

- `add` / `remove` / `refresh` — updated `.sigil/design-skills/<slug>/` cache, updated `design.skills[]` in `.sigil/config.yaml`, regenerated `.sigil/design-skills/.manifest.json`, and a one-line confirmation to the user
- `list` — the registry table (Step 8 format)
- `preview` — rendered SKILL.md frontmatter summary; no files written
- `suggest` — the 4 example URLs with the mandatory non-endorsement disclaimer (Step 7 format)

Warnings (sync failure, budget trims) are surfaced inline and never block.

## Anti-patterns

- **Treating advisory as normative.** design.md is normative; these skills are advisory. When they disagree, design.md wins.
- **Skipping the disclaimer in `suggest`.** The non-endorsement language is mandatory — these aren't sigil-curated picks.
- **Blocking a UI task on sync failure.** Fall back to cached copies; never abort.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-27 | Initial release — S4-002 FR-F01..F06 |
