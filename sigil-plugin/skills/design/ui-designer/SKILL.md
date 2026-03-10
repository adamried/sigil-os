---
name: ui-designer
description: Creates component hierarchies, layout patterns, and component specifications from UX patterns and specifications.
version: 1.0.0
category: design
chainable: true
invokes: []
invoked_by: [uiux-designer]
tools: Read, Write, Glob
inputs: [spec_path, ux_patterns, framework, design_tokens]
outputs: [component_hierarchy, component_specs, layout_patterns]
---

# Skill: UI Designer

## Purpose

Transform UX patterns and specifications into concrete component architectures. This skill produces the component hierarchy, layout decisions, and component specifications that developers will implement.

## When to Invoke

- After UX patterns are defined
- When framework is known (from constitution or framework-selector)
- UI/UX Designer needs component structure for handoff
- Before accessibility requirements (components inform a11y needs)

## Inputs

**Required:**
- `spec_path`: string — Path to feature specification
- `framework`: string — Target UI framework (react, react-native, flutter, vue, swift-ui)

**Optional:**
- `ux_patterns_path`: string — Path to UX patterns document
- `design_tokens`: object — Design tokens from Figma or design system
- `existing_components`: string[] — Paths to existing component definitions

## Process

### Step 1: Inventory Required UI Elements

From spec and UX patterns, list all UI elements needed:
- Screens/pages/views
- Forms and inputs
- Lists and data displays
- Navigation elements
- Feedback elements (toasts, modals, alerts)
- Loading states

### Step 2: Component Hierarchy Design

Create tree structure:

```
Feature Root
├── ScreenA
│   ├── Header
│   ├── ContentSection
│   │   ├── DataList
│   │   │   └── DataItem
│   │   └── EmptyState
│   └── ActionBar
│       └── PrimaryButton
└── ScreenB
    └── ...
```

Principles:
- Single responsibility per component
- Prefer composition over inheritance
- Identify shared vs. feature-specific components
- Consider reusability without over-abstracting (Article 5)

### Step 3: Component Specification

For each component, define:

```markdown
### ComponentName
**Type:** [Container | Presentational | Hybrid]
**Reusability:** [Feature-specific | Shared | Design system candidate]

**Props/Inputs:**
| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| data | DataType | Yes | - | The data to display |
| onAction | () => void | No | - | Callback for action |

**State:**
| State | Type | Description |
|-------|------|-------------|
| isLoading | boolean | Loading state |

**Children:**
- ChildComponentA
- ChildComponentB

**Events Emitted:**
- onComplete: When action completes
- onError: When action fails

**Layout Notes:**
- [Spacing, alignment, responsive behavior]
```

### Step 4: Layout Patterns

Define layout approach:

| Screen | Layout Pattern | Breakpoints |
|--------|---------------|-------------|
| List view | Stack + scroll | Mobile: single col, Desktop: table |
| Detail view | Header + content + footer | Sticky header on scroll |
| Form | Single column centered | Max-width 600px |

### Step 5: Design Token Mapping

If design tokens provided, map to components:

| Component | Token Usage |
|-----------|-------------|
| PrimaryButton | color.primary, spacing.md, radius.sm |
| Card | color.surface, shadow.sm, radius.md |

If no tokens, recommend defaults:
- Spacing scale: 4, 8, 12, 16, 24, 32, 48
- Color: defer to framework defaults or constitution

### Step 6: Shared Component Identification

Flag components for potential sharing:

| Component | Reuse Potential | Notes |
|-----------|-----------------|-------|
| Button | High | Standardize variants |
| DataList | Medium | Feature-specific data shape |
| FeatureHeader | Low | Too specific |

## Output Format

```markdown
## Component Design: [Feature Name]

### Framework
[Framework name] — [Version if relevant]

### Component Hierarchy

```
[Visual tree structure]
```

### Component Specifications

#### [ComponentName]
**Type:** [Type]
**Reusability:** [Level]

**Props:**
| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|

**State:** [If any]

**Children:** [List]

**Layout:** [Notes]

---

[Repeat for each component]

### Layout Patterns

| Screen/View | Pattern | Responsive Behavior |
|-------------|---------|---------------------|

### Design Tokens Used
[Token mapping or "Using framework defaults"]

### Shared Components
| Component | Status | Action |
|-----------|--------|--------|
| [Name] | [New/Existing] | [Create/Use existing/Extend] |

### Implementation Notes
- [Framework-specific considerations]
- [Performance considerations]
- [Testing considerations]
```

## Handoff Data

```json
{
  "component_count": 12,
  "shared_components": ["Button", "Card", "Modal"],
  "new_shared_components": ["DataList"],
  "framework": "react",
  "design_tokens_used": true,
  "layout_patterns": ["stack", "grid", "flex"]
}
```

## Framework-Specific Patterns

### React
- Functional components with hooks
- Props interface with TypeScript
- Children prop for composition

### React Native
- View/Text/Pressable primitives
- StyleSheet for styles
- Platform-specific when needed

### Flutter
- Widget composition
- StatelessWidget vs StatefulWidget
- Theme integration

### Vue
- Composition API preferred
- Props with validation
- Slots for composition

### SwiftUI
- View protocol
- @State, @Binding, @ObservedObject
- ViewModifier for reusable styling

## Human Checkpoint

**Tier:** Auto (generation) + Review (as part of design review)

## Error Handling

| Error | Resolution |
|-------|------------|
| No framework specified | Invoke framework-selector first |
| Conflicting component names | Prefix with feature name |
| Too many components (>30) | Suggest breaking feature into phases |
