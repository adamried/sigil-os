---
name: design-system-reader
description: Analyzes existing codebase to extract UI patterns, components, and design tokens. Ensures new designs are consistent with existing system.
version: 1.0.0
category: design
chainable: true
invokes: []
invoked_by: [uiux-designer]
tools: Read, Glob, Grep
inputs: [codebase_path]
outputs: [existing_components, design_tokens, patterns, style_conventions]
---

# Skill: Design System Reader

## Purpose

Analyze an existing codebase to understand current UI patterns, components, and styling conventions. This enables new designs to maintain consistency with the established system.

## When to Invoke

- Before designing components for an existing project
- When checking if a component already exists
- When understanding established patterns before creating new ones
- UI/UX Designer needs context on existing design system

## Inputs

**Required:**
- `codebase_path`: string — Root path of the project (or UI-specific path)

**Optional:**
- `framework`: string — UI framework to focus analysis
- `component_path`: string — Specific path to component library
- `style_path`: string — Specific path to styling (CSS, tokens, theme)

## Process

### Step 1: Framework Detection

If not specified, detect framework:

```bash
# Check package.json dependencies
grep -E "react|vue|angular|svelte|flutter" package.json

# Check for framework-specific files
ls -la src/app.tsx src/App.vue src/main.ts lib/main.dart
```

Framework indicators:
| Files/Patterns | Framework |
|----------------|-----------|
| .tsx, React imports | React |
| .vue files | Vue |
| angular.json | Angular |
| pubspec.yaml, .dart | Flutter |
| .swift, SwiftUI imports | SwiftUI |

### Step 2: Component Discovery

Scan for existing components:

```bash
# React/Vue/Svelte
find src -name "*.tsx" -o -name "*.vue" -o -name "*.svelte" | head -50

# Look for component directories
ls -la src/components/ src/ui/ src/shared/ lib/widgets/
```

Build component inventory:
- Name
- Location
- Type (presentational/container)
- Props/inputs
- Usage count (grep for imports)

### Step 3: Design Token Extraction

Find design tokens/theme configuration:

```bash
# CSS variables
grep -r "--color\|--spacing\|--font" src/

# Theme files
find . -name "theme.*" -o -name "tokens.*" -o -name "variables.*"

# Tailwind config
cat tailwind.config.js

# Style constants
grep -r "colors\|spacing\|fontSize" src/styles/ src/theme/
```

Extract:
- Color palette
- Spacing scale
- Typography scale
- Border radius values
- Shadow definitions
- Breakpoints

### Step 4: Pattern Analysis

Identify recurring patterns:

**Layout patterns:**
```bash
grep -r "flex\|grid\|Stack\|Row\|Column" src/components/
```

**Component patterns:**
- Button variants (primary, secondary, ghost)
- Card structures
- Form layouts
- List patterns
- Modal patterns

**Naming conventions:**
- Component naming (PascalCase, kebab-case)
- File naming
- CSS class naming (BEM, utility, CSS-in-JS)

### Step 5: Style Approach Detection

Identify styling methodology:

| Pattern | Indicator | Approach |
|---------|-----------|----------|
| .module.css imports | CSS Modules | Scoped CSS |
| className={styles.x} | CSS Modules | Scoped CSS |
| styled.div`` | styled-components | CSS-in-JS |
| css={} prop | Emotion | CSS-in-JS |
| className="px-4 py-2" | Tailwind | Utility-first |
| StyleSheet.create | React Native | Platform native |

### Step 6: Compile Report

Generate comprehensive report of findings.

## Output Format

```markdown
## Design System Analysis: [Project Name]

### Framework
**Detected:** [Framework] [Version]
**Styling:** [Approach]

### Component Inventory

| Component | Location | Type | Props | Usage |
|-----------|----------|------|-------|-------|
| Button | /src/components/Button | Presentational | variant, size, disabled | 47 |
| Card | /src/components/Card | Presentational | title, children | 23 |
| Modal | /src/components/Modal | Container | isOpen, onClose | 12 |

**Total Components:** [N]
**Shared Components:** [N]
**Feature-specific:** [N]

### Design Tokens

#### Colors
| Token | Value | Usage |
|-------|-------|-------|
| primary | #3B82F6 | Buttons, links |
| secondary | #6B7280 | Secondary text |
| error | #EF4444 | Error states |

#### Spacing
| Token | Value |
|-------|-------|
| xs | 4px |
| sm | 8px |
| md | 16px |
| lg | 24px |
| xl | 32px |

#### Typography
| Token | Value |
|-------|-------|
| heading-1 | 32px/1.2/600 |
| body | 16px/1.5/400 |
| caption | 12px/1.4/400 |

### Patterns Identified

#### Layout
- Primary layout: [Flex/Grid]
- Container max-width: [Value]
- Page structure: [Header/Main/Footer pattern]

#### Component Patterns
- **Buttons:** [Variants available]
- **Forms:** [Layout pattern, validation pattern]
- **Cards:** [Structure pattern]
- **Modals:** [Implementation pattern]

#### Naming Conventions
- Components: [Convention]
- Files: [Convention]
- CSS: [Convention]

### Recommendations for New Components

Based on existing patterns:
1. Use [tokens] for spacing
2. Follow [naming] convention
3. Extend existing [Component] rather than creating new
4. Style using [approach]

### Gaps Identified
- [Components that could be shared but aren't]
- [Inconsistencies in patterns]
- [Missing tokens]
```

## Handoff Data

```json
{
  "framework": "react",
  "styling_approach": "tailwind",
  "components_found": 24,
  "shared_components": 12,
  "design_tokens": {
    "colors": true,
    "spacing": true,
    "typography": true
  },
  "patterns": ["button-variants", "card-structure", "form-layout"],
  "recommendations": ["extend-button", "use-existing-modal"]
}
```

## Human Checkpoint

**Tier:** Auto

This is a read-only analysis skill.

## Error Handling

| Error | Resolution |
|-------|------------|
| No components found | Report empty, note greenfield |
| Multiple frameworks | Report all, ask which is primary |
| No design tokens | Report missing, suggest creating |
| Inconsistent patterns | Report inconsistencies for awareness |
