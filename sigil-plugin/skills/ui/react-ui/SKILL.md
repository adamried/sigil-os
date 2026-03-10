---
name: react-ui
description: Implements React components from design specifications. Supports React 18+, TypeScript, and common styling approaches (Tailwind, CSS Modules, styled-components).
version: 1.0.0
category: ui
chainable: true
invokes: []
invoked_by: [developer]
tools: Read, Write, Edit, Bash, Glob
inputs: [component_spec, design_tokens, accessibility_requirements]
outputs: [component_files, style_files, test_files]
---

# Skill: React UI

## Purpose

Implement React components from design specifications. This skill generates production-ready React code following the component design from UI/UX Designer.

## When to Invoke

- Developer receives task to implement UI component
- Constitution specifies React as UI framework
- Component spec includes React-specific requirements

## Inputs

**Required:**
- `component_spec`: object — Component specification from ui-designer skill

**Standard Contract (all UI skills accept):**
```json
{
  "component_spec": {
    "name": "ComponentName",
    "type": "presentational|container|hybrid",
    "props": [{ "name": "variant", "type": "string", "required": true }],
    "state": [{ "name": "isOpen", "type": "boolean" }],
    "children": ["ChildComponent"],
    "events": ["onClick", "onClose"]
  },
  "design_tokens": {
    "colors": {},
    "spacing": {},
    "typography": {}
  },
  "accessibility_requirements": {
    "role": "button",
    "aria": {},
    "keyboard": {}
  }
}
```

**Optional:**
- `styling_approach`: string — "tailwind" | "css-modules" | "styled-components" | "emotion"
- `test_framework`: string — "vitest" | "jest" | "testing-library"
- `existing_patterns`: string — Path to existing component for reference

## Process

### Step 1: Detect Project Conventions

```bash
# Check for styling approach
grep -l "tailwind" package.json tailwind.config.*
grep -l "styled-components" package.json
ls src/**/*.module.css

# Check for test framework
grep -l "vitest\|jest" package.json

# Check for existing component patterns
ls src/components/*.tsx | head -5
```

### Step 2: Generate Component Code

Based on spec, generate:

**TypeScript Interface:**
```typescript
interface ComponentNameProps {
  variant: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  children?: React.ReactNode;
}
```

**Component Implementation:**
```typescript
export const ComponentName: React.FC<ComponentNameProps> = ({
  variant,
  size = 'md',
  disabled = false,
  onClick,
  children,
}) => {
  // Implementation based on spec
};
```

### Step 3: Apply Styling

Based on detected approach:

**Tailwind:**
```typescript
const variantStyles = {
  primary: 'bg-blue-500 text-white hover:bg-blue-600',
  secondary: 'bg-gray-100 text-gray-800 hover:bg-gray-200',
};
```

**CSS Modules:**
```typescript
import styles from './ComponentName.module.css';
// ...
className={styles[variant]}
```

**styled-components:**
```typescript
const StyledComponent = styled.button<{ variant: string }>`
  background: ${props => props.variant === 'primary' ? '#3B82F6' : '#F3F4F6'};
`;
```

### Step 4: Implement Accessibility

From accessibility requirements:

```typescript
<button
  role="button"
  aria-pressed={isPressed}
  aria-disabled={disabled}
  aria-label={ariaLabel}
  tabIndex={disabled ? -1 : 0}
  onKeyDown={handleKeyDown}
>
```

### Step 5: Generate Tests

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  it('renders with primary variant', () => {
    render(<ComponentName variant="primary">Click me</ComponentName>);
    expect(screen.getByRole('button')).toHaveClass('bg-blue-500');
  });

  it('handles click events', () => {
    const handleClick = vi.fn();
    render(<ComponentName variant="primary" onClick={handleClick}>Click</ComponentName>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalled();
  });

  it('is keyboard accessible', () => {
    const handleClick = vi.fn();
    render(<ComponentName variant="primary" onClick={handleClick}>Click</ComponentName>);
    fireEvent.keyDown(screen.getByRole('button'), { key: 'Enter' });
    expect(handleClick).toHaveBeenCalled();
  });
});
```

## Output Format

### File Structure
```
src/components/ComponentName/
├── ComponentName.tsx        # Main component
├── ComponentName.module.css # Styles (if CSS Modules)
├── ComponentName.test.tsx   # Tests
├── index.ts                 # Barrel export
└── types.ts                 # TypeScript types (if complex)
```

### Generated Files

**ComponentName.tsx:**
```typescript
import React from 'react';
import styles from './ComponentName.module.css';

export interface ComponentNameProps {
  // Props from spec
}

export const ComponentName: React.FC<ComponentNameProps> = (props) => {
  // Implementation
};

ComponentName.displayName = 'ComponentName';
```

**index.ts:**
```typescript
export { ComponentName } from './ComponentName';
export type { ComponentNameProps } from './ComponentName';
```

## Handoff Data

```json
{
  "files_created": [
    "src/components/ComponentName/ComponentName.tsx",
    "src/components/ComponentName/ComponentName.test.tsx",
    "src/components/ComponentName/index.ts"
  ],
  "styling_approach": "tailwind",
  "test_framework": "vitest",
  "accessibility_implemented": true,
  "typescript": true
}
```

## React-Specific Patterns

### Hooks
- useState for local state
- useEffect for side effects
- useCallback for memoized handlers
- useMemo for expensive computations
- useRef for DOM references

### Composition
- Prefer composition over inheritance
- Use children prop for flexibility
- Compound components for complex UI

### Performance
- React.memo for expensive pure components
- Lazy loading for route-level components
- Suspense boundaries for async content

## Human Checkpoint

**Tier:** Auto (within approved implementation scope)

## Error Handling

| Error | Resolution |
|-------|------------|
| Missing design tokens | Use sensible defaults, flag for review |
| Conflicting patterns | Follow existing codebase patterns |
| Test framework not found | Default to vitest, note in output |
