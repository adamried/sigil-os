---
name: accessibility
description: Generates WCAG 2.1 accessibility requirements for UI components. Ensures AA compliance minimum, AAA where feasible.
version: 1.0.0
category: design
chainable: true
invokes: []
invoked_by: [uiux-designer, qa-validator]
tools: Read, Write, Glob
inputs: [component_specs, user_flows]
outputs: [accessibility_requirements, aria_specs, keyboard_navigation]
---

# Skill: Accessibility

## Purpose

Generate comprehensive accessibility requirements for UI components, ensuring WCAG 2.1 AA compliance at minimum. This skill produces actionable requirements that developers can implement and QA can validate.

## When to Invoke

- After component design is complete
- Before handoff to Architect
- During QA validation (to verify requirements)
- When accessibility-specific questions arise

## Inputs

**Required:**
- `component_specs_path`: string — Path to component specifications

**Optional:**
- `user_flows_path`: string — Path to UX patterns document
- `existing_a11y`: string — Path to existing accessibility documentation
- `target_level`: string — "AA" (default) or "AAA"

## Process

### Step 1: Component Audit

For each component, evaluate against WCAG criteria:

**Perceivable:**
- Text alternatives for non-text content
- Captions/alternatives for media
- Content adaptable to different presentations
- Distinguishable content (contrast, resize, spacing)

**Operable:**
- Keyboard accessible
- Enough time to read/use content
- No seizure-inducing content
- Navigable (focus order, headings, skip links)

**Understandable:**
- Readable text
- Predictable behavior
- Input assistance (labels, errors, suggestions)

**Robust:**
- Compatible with assistive technologies
- Valid, parseable markup

### Step 2: ARIA Requirements

For each interactive component, specify:

| Component | Role | States | Properties |
|-----------|------|--------|------------|
| Button | button | aria-pressed, aria-disabled | aria-label (if icon-only) |
| Modal | dialog | aria-modal | aria-labelledby, aria-describedby |
| Tab | tab | aria-selected | aria-controls |
| Alert | alert | aria-live | aria-atomic |

### Step 3: Keyboard Navigation

Define keyboard interaction for each component:

| Component | Key | Action |
|-----------|-----|--------|
| Button | Enter/Space | Activate |
| Dropdown | Arrow Down | Open/next option |
| Modal | Escape | Close |
| Tab list | Arrow Left/Right | Switch tabs |

Document focus management:
- Focus trap for modals
- Focus return after close
- Skip links for navigation
- Focus visible indicators

### Step 4: Color and Contrast

Specify requirements:
- Normal text: 4.5:1 contrast ratio
- Large text (18px+ or 14px+ bold): 3:1
- UI components: 3:1 against background
- Focus indicators: 3:1 against adjacent colors

Flag any components with potential contrast issues.

### Step 5: Screen Reader Requirements

For each component, specify announcements:

| Component | Announcement | When |
|-----------|--------------|------|
| Form field | Label + error | On focus, on error |
| Button | Label + state | On focus |
| Alert | Full message | On appearance |
| Loading | "Loading" + completion | Start and end |

### Step 6: Mobile Accessibility

If mobile platform:
- Touch target minimum: 44x44 points
- Gesture alternatives for swipe actions
- VoiceOver/TalkBack compatibility
- Dynamic type support (iOS) / font scaling (Android)

## Output Format

```markdown
## Accessibility Requirements: [Feature Name]

### Compliance Target
**Minimum:** WCAG 2.1 Level AA
**Target:** WCAG 2.1 Level AAA where feasible

### Component Requirements

#### [ComponentName]

**ARIA:**
| Attribute | Value | Condition |
|-----------|-------|-----------|
| role | [role] | Always |
| aria-label | [text] | When [condition] |
| aria-expanded | true/false | When [condition] |

**Keyboard:**
| Key | Action |
|-----|--------|
| Tab | Focus component |
| Enter | Activate |
| Escape | [If applicable] |

**Focus:**
- Focus visible: [Yes/Custom style]
- Focus order: [Position in tab order]
- Focus trap: [If applicable]

**Announcements:**
| Event | Announcement |
|-------|--------------|
| Focus | [What screen reader says] |
| Activation | [Result announcement] |
| Error | [Error format] |

**Contrast:**
- Text: [Requirement]
- Interactive elements: [Requirement]

---

[Repeat for each component]

### Form Accessibility

**Labels:**
- All inputs have associated labels (explicit or aria-labelledby)
- Required fields indicated visually AND via aria-required

**Errors:**
- Error messages linked to inputs via aria-describedby
- Error summary at form top with links to fields
- Errors announced via aria-live region

**Instructions:**
- Format hints in aria-describedby
- Character counts announced

### Navigation

**Skip Links:**
- "Skip to main content" at page top
- "Skip to navigation" if applicable

**Landmarks:**
| Landmark | Element | Purpose |
|----------|---------|---------|
| main | main content area | Primary content |
| navigation | nav element | Main navigation |
| search | search form | Search functionality |

**Headings:**
- Proper hierarchy (h1 → h2 → h3, no skips)
- Descriptive heading text
- One h1 per page

### Media (if applicable)
- Images: Alt text or decorative (alt="")
- Video: Captions required
- Audio: Transcript required

### Testing Checklist
- [ ] Keyboard-only navigation works
- [ ] Screen reader announces correctly
- [ ] Focus visible on all interactive elements
- [ ] Color contrast meets requirements
- [ ] Touch targets meet minimum size (mobile)
- [ ] Zoom to 200% doesn't break layout
- [ ] Reduced motion respected
```

## Handoff Data

```json
{
  "compliance_level": "AA",
  "components_audited": 12,
  "aria_roles_specified": ["button", "dialog", "alert", "tab"],
  "keyboard_patterns": ["button", "modal", "dropdown", "tabs"],
  "known_risks": [],
  "testing_requirements": ["keyboard", "screen-reader", "contrast"]
}
```

## Common Patterns Reference

### Modal Dialog
- role="dialog", aria-modal="true"
- aria-labelledby pointing to title
- Focus trap while open
- Escape to close
- Return focus to trigger on close

### Form Validation
- aria-invalid="true" on invalid fields
- aria-describedby linking to error message
- aria-live="polite" region for error summary
- Focus first invalid field on submit

### Loading States
- aria-busy="true" on loading container
- aria-live="polite" announcement
- "Loading complete" announcement

### Tabs
- role="tablist" on container
- role="tab" on tabs, role="tabpanel" on panels
- aria-selected on active tab
- Arrow keys to navigate, Tab to exit

## Human Checkpoint

**Tier:** Auto (generation) + Review (as part of design review)

## Error Handling

| Error | Resolution |
|-------|------------|
| Component type unknown | Use generic interactive requirements |
| Conflict with design | Flag for UI/UX Designer decision |
| AAA not feasible | Document why, ensure AA met |
