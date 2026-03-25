---
name: visual-analyzer
description: Analyzes visual artifacts (mockups, wireframes, screenshots) to extract UI requirements for specifications. Invoke when user provides images or design files.
version: 1.0.0
category: workflow
chainable: true
invokes: []
invoked_by: [spec-writer, business-analyst]
tools: Read
---

# Skill: Visual Analyzer

## Purpose

Extract functional requirements, UI elements, and accessibility considerations from visual artifacts. Bridges the gap between design files and structured specifications.

## When to Invoke

- User provides mockups, wireframes, or screenshots
- User references design files (Figma, Sketch links)
- User says "based on this design", "from the mockup", "look at this"
- spec-writer receives visual assets with feature request

## Inputs

**Required:**
- `visual_asset`: image — The image file to analyze (PNG, JPG, PDF, or screenshot)

**Optional:**
- `context`: string — User's description of what the visual represents
- `focus_areas`: string[] — Specific elements to analyze ("navigation", "form", "buttons")
- `spec_path`: string — Related spec for context alignment

**Auto-loaded:**
- `constitution`: string — `/.sigil/constitution.md` (for accessibility requirements)

## Process

### Step 1: Visual Inventory

Scan the image to identify all UI elements:

```
1. Layout Structure
   - Header, footer, sidebars, main content
   - Grid/column structure
   - Responsive breakpoints (if indicated)

2. Interactive Elements
   - Buttons (primary, secondary, icon)
   - Links and navigation
   - Form inputs (text, select, checkbox, radio)
   - Modals and overlays

3. Content Elements
   - Headings and text hierarchy
   - Images and icons
   - Data displays (tables, lists, cards)

4. State Indicators
   - Loading states
   - Empty states
   - Error states
   - Success states
```

### Step 2: Interaction Mapping

For each interactive element, infer behavior:

```
1. Click/tap actions
   - What happens when clicked?
   - Navigation destination
   - State change triggered

2. Form behaviors
   - Validation requirements
   - Submit actions
   - Error handling patterns

3. Navigation flows
   - Menu structure
   - Breadcrumb patterns
   - Back/forward relationships
```

### Step 3: Accessibility Analysis

Check against constitution accessibility requirements:

```
1. Color Contrast
   - Text on background contrast ratio
   - Button/link visibility
   - Icon clarity

2. Text Sizing
   - Heading hierarchy
   - Body text readability
   - Touch target sizes

3. Structure
   - Logical heading order
   - Landmark regions implied
   - Focus order inference

4. Interactive Elements
   - Button labels clear
   - Form labels visible
   - Error message placement
```

### Step 4: Gap Identification

Note missing or ambiguous elements:

```
1. Missing States
   - No error state shown
   - No loading state shown
   - No empty state shown

2. Unclear Behaviors
   - Button action not obvious
   - Form validation rules unclear
   - Navigation destination unknown

3. Accessibility Gaps
   - Low contrast areas
   - Missing labels
   - Unclear focus order
```

### Step 5: Requirements Extraction

Convert analysis into structured requirements:

```
For each element:
  1. Create functional requirement (FR-xxx)
  2. Define acceptance criteria
  3. Note accessibility requirement if applicable
  4. Flag ambiguities for clarification
```

## Outputs

**Analysis Document:**

```markdown
## Visual Analysis: [Asset Name]

### Overview
[Brief description of what the visual shows]

### Layout Structure
- **Type:** [Single page | Multi-section | Modal | etc.]
- **Regions:** [Header, Sidebar, Main, Footer]
- **Grid:** [Columns, responsive notes]

### UI Elements Identified

| Element | Type | Location | Implied Behavior |
|---------|------|----------|------------------|
| Logo | Image/Link | Header left | Navigates to home |
| Login button | Primary button | Header right | Opens login modal |
| Search input | Text field | Header center | Filters content |

### Extracted Requirements

**Functional Requirements:**

| ID | Requirement | Source Element | Priority |
|----|-------------|----------------|----------|
| FR-V01 | System shall display logo that links to homepage | Logo | P1 |
| FR-V02 | User shall be able to log in via header button | Login button | P1 |
| FR-V03 | User shall be able to search content | Search input | P2 |

**Accessibility Requirements:**

| ID | Requirement | WCAG | Priority |
|----|-------------|------|----------|
| A11Y-V01 | Logo shall have alt text | 1.1.1 | P1 |
| A11Y-V02 | Search shall have visible label | 1.3.1 | P1 |
| A11Y-V03 | Focus order shall follow visual order | 2.4.3 | P1 |

### Missing States

- [ ] **Error state:** Not shown for login failure
- [ ] **Loading state:** Not shown for search
- [ ] **Empty state:** Not shown for no results

### Ambiguities Detected

1. **Login button:** Modal or new page? Needs clarification.
2. **Search:** Real-time or on-submit? Needs clarification.
3. **Navigation:** Mobile behavior not shown.

### Recommended Clarifications

1. What happens when login fails?
2. Does search filter immediately or on button click?
3. How does navigation behave on mobile?
```

**Handoff Data:**

```json
{
  "asset_analyzed": "mockup-homepage.png",
  "elements_found": 12,
  "requirements_extracted": {
    "functional": 8,
    "accessibility": 5
  },
  "missing_states": ["error", "loading", "empty"],
  "ambiguities": [
    "Login interaction pattern unclear",
    "Search behavior not specified"
  ],
  "clarification_questions": [
    "What happens when login fails?",
    "Does search filter immediately or on submit?"
  ],
  "accessibility_concerns": [
    "Verify contrast ratio on blue buttons"
  ]
}
```

## Analysis Guidelines

### Element Recognition

| Visual Pattern | Interpret As |
|----------------|--------------|
| Rectangular outline with text | Button or input |
| Underlined text | Link |
| Checkbox/circle with text | Selection input |
| Hamburger icon (☰) | Mobile menu trigger |
| X icon | Close/dismiss action |
| Magnifying glass | Search functionality |
| Gear icon | Settings access |
| User avatar | Profile/account access |

### State Inference

If only one state is shown, flag others as needed:

| Shown State | Also Need |
|-------------|-----------|
| Default form | Error, success, loading |
| Populated list | Empty state |
| Logged-in view | Logged-out view |
| Desktop layout | Mobile/tablet layout |

### Accessibility Defaults

When not specified, recommend:

- Minimum 4.5:1 contrast for text
- Minimum 44x44px touch targets
- Visible focus indicators
- Skip navigation link
- Proper heading hierarchy

## Human Checkpoints

- **Tier:** Auto (analysis runs automatically)
- Ambiguities flagged for user clarification
- Accessibility concerns highlighted for review

## Error Handling

| Error | Resolution |
|-------|------------|
| Image not readable | Request clearer image or describe verbally |
| Multiple screens in one image | Analyze each section, ask for individual files |
| Low resolution | Note limitations, ask for higher resolution |
| Design system reference only | Request actual mockup or describe elements |

## Example Invocations

**With mockup:**
```
User: /sigil:draw "Build the checkout flow"
      [attached: checkout-page.png]

→ visual-analyzer extracts form fields, buttons, step indicators
→ Returns requirements for checkout form, validation, navigation
```

**With wireframe:**
```
User: Create the dashboard based on this wireframe
      [attached: dashboard-wireframe.pdf]

→ visual-analyzer identifies widgets, charts, navigation
→ Returns requirements for each dashboard component
```

**With screenshot:**
```
User: I want something like this [screenshot of competitor]
      but with our branding

→ visual-analyzer identifies patterns to replicate
→ Returns requirements inspired by reference
→ Flags elements that need original design
```

## Integration Points

- **Invoked by:** `spec-writer` when visual assets provided
- **Invoked by:** `business-analyst` for design analysis
- **Outputs to:** Specification requirements
- **Feeds into:** `clarifier` for ambiguity resolution

## Notes

- Analysis is inference-based; always confirm with user
- Visual analysis supplements, not replaces, user requirements
- Flag all assumptions for verification
- Prioritize accessibility from the start

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-25 | Initial release - full implementation |
| 0.1.0-stub | 2026-01-16 | Stub created |
