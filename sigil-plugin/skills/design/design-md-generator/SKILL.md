---
name: design-md-generator
description: Generate or regenerate .sigil/design.md — the normative design source-of-truth. Supports greenfield interview path and explore mode for existing projects. Selects mobile or web profile per project setup choice.
version: 1.0.0
category: design
chainable: false
invokes: []
invoked_by: [setup, design]
tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# Skill: Design.md Generator

## Purpose

Produce `.sigil/design.md` — the project's normative design source-of-truth (S4-002 FR-E01). Two paths:

- **Greenfield interview** (FR-E03) — when the project has no source files yet
- **Explore mode** (FR-E04) — when source files exist, extract tokens and component inventory before writing

## When to Invoke

- `/sigil:setup` Step 5.6 "Design Skills + design.md (Optional)" — user accepts design.md generation
- `/sigil:design` (bare invocation) — regenerate existing design.md

## Inputs

- `profile`: `mobile | web` (user picks at setup; informs which template to use)
- `mode`: `greenfield | explore | regenerate`

## Process

### Step 1: Determine Profile

If invoked from `/sigil:setup`, the user picked the profile in that flow. If invoked from `/sigil:design` (regenerate), read the existing `.sigil/design.md` frontmatter for `profile:` and confirm with the user before changing.

Load the matching template:

- `templates/design-md-mobile.md` for `mobile`
- `templates/design-md-web.md` for `web`

Profile schemas have full parity (S4-002 NFR-005) — sigil-os does NOT ship a "reduced web fallback." Web is first-class.

### Step 2: Detect Greenfield vs. Existing

```
1. Count source files (extensions: ts, tsx, js, jsx, py, swift, kt, dart, ...).
   Exclude node_modules, dist, build, .git, .next, target, .venv.
2. Check for theme files: tailwind.config.*, *.module.css with variables,
   theme.ts/js, styles/tokens.*, theme.json
3. Check for component directories: **/components/**, **/screens/**,
   **/views/**, **/widgets/**
```

Decision rule:

- Source files < 5 AND no theme files AND no component dirs → **Greenfield**
- Otherwise → **Explore mode**

### Step 3a: Greenfield Interview (FR-E03)

Walk through six questions using `AskUserQuestion`:

1. **Brand voice** — How should the product feel? (Calm, energetic, professional, playful, premium, approachable, etc.)
2. **Target platforms** (mobile profile only) — iOS, Android, or both?
3. **Color** — Primary brand color (hex or named). Then surface/background preference (light, dark, follow OS).
4. **Typography** — Primary font family. Preference: system fonts (fast, native feel) or custom?
5. **Motion** — Restrained (minimal animation), standard, or expressive?
6. **Accessibility baseline** — WCAG AA (default), AA + specific assistive tech, or AAA?

Populate the template's YAML frontmatter from answers. Generate sensible defaults for everything else (spacing scale, radii, easing curves) following platform conventions.

### Step 3b: Explore Mode (FR-E04)

For existing projects, extract real values rather than asking:

1. **Token extraction:**
   - **Tailwind config:** read theme.colors, theme.spacing, theme.fontFamily, theme.borderRadius
   - **CSS custom properties:** scan `*.css`, `*.scss` for `:root { --primary: ... }` patterns
   - **Theme objects:** read `theme.ts`, `tokens.ts`, `colors.ts` exports
   - **iOS Asset Catalogs** (mobile + iOS): read `Assets.xcassets/Colors/*.colorset/Contents.json`
   - **Android resources** (mobile + Android): read `res/values/colors.xml`, `res/values/dimens.xml`

2. **Component inventory:**
   - Glob `**/components/**`, `**/screens/**` (mobile), `**/views/**` (web), `**/widgets/**` (Flutter)
   - For each component, record path and any obvious variant naming (Button, ButtonPrimary, ButtonGhost...)

3. **Confirmation step:**
   Render the extracted values to the user via `AskUserQuestion`:

```
Detected design tokens:
  Primary color:    #1E5AFF (from tailwind.config.js theme.colors.primary)
  Typography:       Inter (from theme.ts)
  Spacing scale:    [0, 4, 8, 12, 16, 24, 32, 48]
  Components found: 47 in src/components/

Look right?
  1. Yes, write design.md with these values
  2. Adjust before writing
  3. Cancel
```

Never write to `.sigil/design.md` without user confirmation in explore mode.

### Step 4: Write design.md

Render the chosen template with:

- YAML frontmatter populated from interview answers or extracted tokens
- Markdown body using template defaults for any unspecified guidance
- Initial Revision History entry: `{date} | Setup/Regenerate | Initial generation via {greenfield interview | explore mode}`

Write to `.sigil/design.md`. Verify the file is committed to git (not gitignored):

- `.sigil/design-skills/` (external skills cache) IS gitignored
- `.sigil/design.md` (this file) is NOT gitignored — it's normative project content

### Step 5: Update Config

Update `.sigil/config.yaml` `design:` block:

```yaml
design:
  enabled: true
  profile: mobile | web
  skills: []          # populated by /sigil:design add
  component_globs:    # optional override; defaults baked into design-skills-loader
    - "**/components/**"
    - "**/screens/**"
    - "**/views/**"
    - "**/widgets/**"
```

If the user declined design.md generation in setup, set `design.enabled: false` instead and do not write the file.

### Step 6: Report

```
Design source-of-truth written
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Path:    .sigil/design.md
Profile: {mobile | web}
Source:  {greenfield interview | explore mode}

UI tasks will now load this file at the start of every run.
Backend tasks pay zero overhead — the UI-task gate is deterministic.

Next:
  /sigil:design add <url>     — register an external design skill
  /sigil:design suggest       — show the 4 example external skills
  /sigil:design               — regenerate this file (always with user
                                 confirmation; never auto)
```

## Outputs

- `.sigil/design.md` (or no file if user declined)
- Updated `.sigil/config.yaml` `design:` block

## Anti-patterns

- **Auto-write in explore mode.** The user MUST confirm extracted tokens before write.
- **Auto-regenerate without confirmation.** `/sigil:design` regenerate always uses `AskUserQuestion` to confirm overwrite.
- **Reduced web fallback.** Web profile is full-parity with mobile — do not strip sections.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-27 | Initial release — S4-002 FR-E01, FR-E03, FR-E04 |
