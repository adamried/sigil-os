---
# YAML token frontmatter — machine-readable design tokens.
# Skills (uiux-designer, developer, frontend-developer) read this block to
# pull project tokens without parsing the full Markdown body.
profile: web
brand:
  name: "{Project Name}"
  voice: "{Friendly | Professional | Playful | Authoritative | ...}"
  platforms: ["web"]
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
  font_family_primary: "{e.g., Inter, system-ui, Söhne}"
  font_family_secondary: "{optional}"
  font_family_mono: "{e.g., JetBrains Mono, ui-monospace}"
  scale:
    display: { size: 56, line_height: 64, weight: 700 }
    h1:      { size: 40, line_height: 48, weight: 700 }
    h2:      { size: 32, line_height: 40, weight: 600 }
    h3:      { size: 24, line_height: 32, weight: 600 }
    body:    { size: 16, line_height: 24, weight: 400 }
    small:   { size: 14, line_height: 20, weight: 400 }
    caption: { size: 12, line_height: 16, weight: 400 }
spacing:
  unit: 4    # base unit in pixels
  scale: [0, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128]
breakpoints:
  sm: 640
  md: 768
  lg: 1024
  xl: 1280
  xxl: 1536
radii:
  none: 0
  sm: 4
  md: 8
  lg: 16
  pill: 999
shadows:
  sm: "0 1px 2px rgba(0,0,0,0.08)"
  md: "0 4px 12px rgba(0,0,0,0.10)"
  lg: "0 12px 32px rgba(0,0,0,0.12)"
motion:
  duration_fast: 150
  duration_base: 250
  duration_slow: 400
  easing_standard: "cubic-bezier(0.4, 0.0, 0.2, 1)"
  easing_emphasis: "cubic-bezier(0.4, 0.0, 0.6, 1)"
accessibility:
  contrast_minimum: "WCAG-AA"
  minimum_touch_target_px: 44
  focus_ring_visible: true
  reduced_motion_supported: true
---

# Design: {Project Name}

> Normative design source-of-truth. Agents read this in full on every UI task. When external design skills disagree, **this file wins** (S4-002 FR-E02).
>
> design.md is **never** auto-edited. Updates come only from: `/sigil:setup`, `/sigil:design` regeneration, or user-accepted propose-and-confirm patches.

---

## 1. Brand Voice and Personality

{One paragraph describing the brand's personality, tone, and emotional resonance.}

**Core attributes:** {3-5 single words}

---

## 2. Color System

Primary palette derived from the YAML frontmatter. Document semantic intent below.

| Token | Hex | Purpose |
|-------|-----|---------|
| primary | `{value}` | Brand identity, primary CTAs |
| secondary | `{value}` | Secondary CTAs, accents |
| surface | `{value}` | Cards, sheets, elevated surfaces |
| background | `{value}` | Page background |
| on_primary | `{value}` | Text/icons on primary |
| on_surface | `{value}` | Default text on surfaces |
| success / warning / error / info | (see frontmatter) | Semantic feedback |

**Dark mode:** {Yes — with overrides in frontmatter | No | Auto from OS via `prefers-color-scheme`}

---

## 3. Typography

Type scale defined in frontmatter. Notes below.

- **Primary family:** {family}
- **Mono family (code, data tables):** {family}
- **Hierarchy:** display for landing heroes; h1 for page titles; h2/h3 for sectioning; body for prose; small/caption for metadata
- **Line length:** target 60–75ch for body prose

---

## 4. Spacing and Layout Grid

Base unit: 4px. Scale: [0, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128].

**Grid:** {12-column with N-px gutter | CSS Grid + container queries | Bespoke}
**Max content width:** {1200px | 1440px | full bleed}

---

## 5. Breakpoints and Responsive Strategy

Defined in frontmatter. Strategy:

- **Mobile-first** (default) — write base styles for narrow screens, add larger via min-width queries.
- **Container queries:** {used for {components} | not used}
- **Fluid type / spacing:** {clamp() | static steps only}

---

## 6. Component Inventory

| Component | Location | Notes |
|-----------|----------|-------|
| {ComponentName} | `{path}` | {Status, variants, accessibility callouts} |

---

## 7. Iconography

- **Icon set:** {Lucide | Phosphor | Heroicons | Custom}
- **Default size:** {16, 20, 24}
- **Stroke width:** {1.5px standard}

---

## 8. Imagery

- **Photographic style:** {if applicable}
- **Illustration style:** {if applicable}
- **Image optimization:** {next/image | astro:image | manual srcset}

---

## 9. Motion

Defined in frontmatter. Guidance below.

- Page transitions: prefer instant or fade only — avoid disorienting transitions
- Hover/focus state: 150ms (fast)
- Layout shifts: 250ms (base) with easing_standard
- Reduced motion: respect `prefers-reduced-motion: reduce` — replace transitions with opacity-only or instant

---

## 10. Forms and Inputs

- **Label placement:** {above | floating | inline-leading}
- **Required indicator:** {asterisk | "(required)" suffix | none}
- **Error display:** inline below field with `role="alert"` and `aria-describedby` linkage
- **Submit button:** primary CTA bottom-end; secondary actions to its left

---

## 11. Navigation Patterns

- **Primary navigation:** {top bar | side rail | hamburger on mobile}
- **Mobile nav transition:** {hamburger drawer | bottom sheet | top-down}
- **Footer:** {required content — legal, sitemap, contact}

---

## 12. Empty, Loading, and Error States

- **Loading:** skeleton screens (preferred) > spinners > shimmer
- **Empty:** illustration + brief message + primary CTA
- **Error:** inline with retry; full-page errors only for hard failures (404, 500)

---

## 13. Accessibility

- **Contrast:** WCAG AA minimum (4.5:1 normal text, 3:1 large text and UI components)
- **Focus rings:** always visible; never `outline: none` without replacement
- **Keyboard navigation:** every interactive element reachable via Tab
- **Touch targets:** 44px minimum on touch devices
- **Skip links:** "Skip to main content" link as first focusable element

---

## 14. Web-Specific Notes

- **Browser support:** {evergreen | last 2 versions | specific list}
- **Print styles:** {explicit print.css | unstyled native | not needed}
- **Email-rendered HTML:** {if applicable, link to email-template guidance}

---

## 15. Open Questions and Decisions

- **{Open question}** — {context}
- **{Decision made}** — {what was decided, why, when}

---

## Revision History

| Date | Source | Summary |
|------|--------|---------|
| {YYYY-MM-DD} | Setup / Regenerate / Propose-and-confirm | {summary} |
