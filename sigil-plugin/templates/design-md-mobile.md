---
# YAML token frontmatter — machine-readable design tokens.
# Skills (uiux-designer, developer, frontend-developer) read this block to
# pull project tokens without parsing the full Markdown body.
profile: mobile
brand:
  name: "{Project Name}"
  voice: "{Friendly | Professional | Playful | Authoritative | ...}"
  platforms: ["ios", "android"]   # or just one
color:
  primary: "#000000"
  secondary: "#000000"
  surface: "#FFFFFF"
  background: "#FFFFFF"
  on_primary: "#FFFFFF"
  on_surface: "#000000"
  semantic:
    success: "#00A86B"
    warning: "#FFB200"
    error: "#D72631"
    info: "#1E5AFF"
  dark_mode_overrides: {}
typography:
  font_family_primary: "{e.g., SF Pro, Roboto, Inter, system}"
  font_family_secondary: "{optional}"
  scale:
    display: { size: 32, line_height: 40, weight: 700 }
    h1:      { size: 28, line_height: 36, weight: 700 }
    h2:      { size: 22, line_height: 30, weight: 600 }
    h3:      { size: 18, line_height: 26, weight: 600 }
    body:    { size: 16, line_height: 24, weight: 400 }
    caption: { size: 13, line_height: 18, weight: 400 }
spacing:
  unit: 4    # base unit in points/dp
  scale: [0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64]
radii:
  none: 0
  sm: 4
  md: 8
  lg: 16
  pill: 999
motion:
  duration_fast: 150
  duration_base: 250
  duration_slow: 400
  easing_standard: "cubic-bezier(0.4, 0.0, 0.2, 1)"
  easing_emphasis: "cubic-bezier(0.4, 0.0, 0.6, 1)"
accessibility:
  contrast_minimum: "WCAG-AA"
  minimum_touch_target_dp: 44
  reduced_motion_supported: true
---

# Design: {Project Name}

> Normative design source-of-truth. Agents read this in full on every UI task. When external design skills disagree, **this file wins** (S4-002 FR-E02).
>
> design.md is **never** auto-edited. Updates come only from: `/sigil:setup`, `/sigil:design` regeneration, or user-accepted propose-and-confirm patches.

---

## 1. Brand Voice and Personality

{One paragraph describing the brand's personality, tone, and emotional resonance. E.g., "Calm, confident, and minimal — favors clarity over cleverness. Visual humor lives in motion, not copy."}

**Core attributes:** {3-5 single words — e.g., approachable, precise, energetic}

---

## 2. Color System

Primary palette derived from the YAML frontmatter. Document semantic intent below.

| Token | Hex | Purpose |
|-------|-----|---------|
| primary | `{value}` | Brand identity, primary CTAs |
| secondary | `{value}` | Secondary CTAs, accents |
| surface | `{value}` | Cards, sheets, elevated surfaces |
| background | `{value}` | App background |
| on_primary | `{value}` | Text/icons on primary |
| on_surface | `{value}` | Default text on surfaces |
| success | `{value}` | Positive feedback |
| warning | `{value}` | Caution, non-blocking issues |
| error | `{value}` | Errors, destructive actions |
| info | `{value}` | Neutral information |

**Dark mode:** {Yes — with overrides in frontmatter | No — light only | Auto from OS}

---

## 3. Typography

Type scale defined in frontmatter. Notes below.

- **Primary family:** {family}
- **Secondary family:** {family or "none — primary used for all weights"}
- **Hierarchy guidance:** {When to use display vs h1, etc.}

---

## 4. Spacing

Base unit: 4dp. Use the scale ([0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64]) — do not introduce off-scale values.

Common composition patterns:

- **Tight grouping (related content):** 4–8dp
- **Default content gap:** 16dp
- **Section separation:** 24–32dp
- **Screen-level breathing room:** 40+dp

---

## 5. Component Inventory

List the project's named components and where they live. Updated by the design-md-generator's `explore` mode (S4-002 FR-E04) and via propose-and-confirm patches.

| Component | Location | Notes |
|-----------|----------|-------|
| {ComponentName} | `{path}` | {Status, variants, accessibility callouts} |

---

## 6. Layout Patterns

How the app structures its screens. Examples: bottom tab navigation, stack-based modal flows, full-bleed media, list-detail.

- {Pattern}
- {Pattern}

---

## 7. Iconography

- **Icon set:** {SF Symbols | Material Symbols | Custom | Lucide}
- **Default size:** {16, 20, 24, 32}
- **Stroke / fill convention:** {filled by default | outlined by default | both}

---

## 8. Imagery

- **Photographic style:** {if applicable}
- **Illustration style:** {if applicable}
- **Avatar conventions:** {default placeholder, shape, sizing}

---

## 9. Motion

Defined in frontmatter. Guidance below.

- **Use durations 150ms (fast), 250ms (base), 400ms (slow).**
- **Use easing_standard for entering/exiting; easing_emphasis for state changes.**
- Reduced-motion: respect OS preference; replace motion with instantaneous transitions or fades only.

---

## 10. Forms and Inputs

- **Label placement:** {above | floating | inline}
- **Required indicator:** {asterisk | "required" tag | none}
- **Error display:** {inline below field | toast | summary at top}
- **Submit button position:** {bottom-anchored | inline-end}

---

## 11. Navigation Patterns

- **Primary navigation:** {bottom tabs | drawer | tab bar at top}
- **Back navigation:** {OS back | in-app back button | swipe-back gesture}
- **Modal patterns:** {full-sheet, half-sheet, alert dialog}

---

## 12. Empty, Loading, and Error States

Each major surface should declare its variants:

- **Loading:** {skeleton | spinner | shimmer}
- **Empty:** {illustration + CTA | text-only}
- **Error:** {inline retry | full-screen | toast}

---

## 13. Accessibility

- **Contrast minimum:** WCAG AA (or higher per frontmatter)
- **Touch targets:** 44dp minimum
- **Screen reader labels:** every interactive element has a label
- **Reduced motion:** OS preference respected
- **Dynamic type:** {supported | not supported}

---

## 14. Platform-Specific Notes

### iOS

- {iOS-specific patterns followed — e.g., SF Symbols, Human Interface Guidelines deviations}

### Android

- {Android-specific patterns — e.g., Material 3 components, edge-to-edge handling}

---

## 15. Open Questions and Decisions

Document design tensions explicitly:

- **{Open question}** — {context, options being considered, deadline if any}
- **{Decision made}** — {what was decided, why, when}

---

## Revision History

| Date | Source | Summary |
|------|--------|---------|
| {YYYY-MM-DD} | Setup / Regenerate / Propose-and-confirm | {summary of change} |
