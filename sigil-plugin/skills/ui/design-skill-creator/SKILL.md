---
name: design-skill-creator
description: Meta-skill that generates new UI framework skills following the standard contract. Use when project needs a UI framework not covered by built-in skills.
version: 1.0.0
category: ui
chainable: false
invokes: []
invoked_by: [developer, uiux-designer]
tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch
inputs: [framework_name, framework_docs]
outputs: [skill_definition_file]
---

# Skill: Design Skill Creator

## Purpose

Generate new UI framework skills that follow the standard Sigil UI skill contract. This ensures any framework can be supported while maintaining consistent interfaces with the design layer.

## When to Invoke

- Project uses a UI framework not covered by built-in skills
- Constitution specifies an uncommon framework (Angular, Svelte, Solid, etc.)
- Developer cannot find matching UI skill
- User explicitly requests support for a new framework

## Built-in UI Skills

Before creating a new skill, check if one already exists:
- `react-ui` — React 18+, TypeScript, Tailwind/CSS Modules/styled-components
- `react-native-ui` — React Native 0.70+, Expo
- `flutter-ui` — Flutter 3+, Material 3, Cupertino
- `vue-ui` — Vue 3, Composition API
- `swift-ui` — SwiftUI, iOS 15+, macOS 12+

## Inputs

**Required:**
- `framework_name`: string — Name of the framework (e.g., "angular", "svelte", "solid")

**Optional:**
- `framework_docs`: string — URL to official documentation
- `example_project`: string — Path to example project using the framework
- `styling_approach`: string — Primary styling methodology

## Process

### Step 1: Research Framework

```bash
# Search for framework patterns
WebSearch: "[framework] component patterns best practices"
WebSearch: "[framework] TypeScript component example"
WebSearch: "[framework] accessibility patterns"
```

Gather:
- Component structure conventions
- State management patterns
- Styling approaches
- Testing frameworks
- Accessibility APIs

### Step 2: Identify Framework Primitives

Map to standard concepts:

| Concept | React | Vue | Angular | Svelte | Solid |
|---------|-------|-----|---------|--------|-------|
| Component | function/class | .vue SFC | @Component | .svelte | function |
| Props | props object | defineProps | @Input | export let | props |
| State | useState | ref/reactive | property | let | createSignal |
| Events | callbacks | emit | @Output | dispatch | props |
| Children | children prop | slots | ng-content | slot | props.children |
| Lifecycle | useEffect | onMounted | ngOnInit | onMount | createEffect |

### Step 3: Generate Skill Definition

Create skill file following standard structure:

```markdown
---
name: [framework]-ui
description: Implements [Framework] components from design specifications.
version: 1.0.0
category: ui
chainable: true
invokes: []
invoked_by: [developer]
tools: Read, Write, Edit, Bash, Glob
inputs: [component_spec, design_tokens, accessibility_requirements]
outputs: [component_files, style_files, test_files]
---

# Skill: [Framework] UI

## Purpose

Implement [Framework] components from design specifications.

## When to Invoke

- Developer receives task to implement UI component
- Constitution specifies [Framework] as UI framework
- Project configuration indicates [Framework]

## Inputs

**Standard Contract (required for all UI skills):**
\`\`\`json
{
  "component_spec": {
    "name": "string",
    "type": "presentational|container|hybrid",
    "props": [{ "name": "string", "type": "string", "required": "boolean" }],
    "state": [{ "name": "string", "type": "string" }],
    "children": ["string"],
    "events": ["string"]
  },
  "design_tokens": {
    "colors": {},
    "spacing": {},
    "typography": {}
  },
  "accessibility_requirements": {
    "role": "string",
    "aria": {},
    "keyboard": {}
  }
}
\`\`\`

## Process

### Step 1: Detect Project Conventions
[Framework-specific detection logic]

### Step 2: Generate Component
[Framework-specific component generation]

### Step 3: Apply Styling
[Framework-specific styling patterns]

### Step 4: Implement Accessibility
[Framework-specific accessibility APIs]

### Step 5: Generate Tests
[Framework-specific testing patterns]

## Output Format

### File Structure
\`\`\`
[Framework-appropriate structure]
\`\`\`

## [Framework]-Specific Patterns

### [Pattern Category 1]
[Documented patterns]

### [Pattern Category 2]
[Documented patterns]

## Human Checkpoint

**Tier:** Auto
```

### Step 4: Validate Skill

Before saving, verify:
- [ ] Accepts standard input contract
- [ ] Produces standard output structure
- [ ] Documents framework-specific patterns
- [ ] Includes accessibility implementation
- [ ] Includes test generation
- [ ] Follows Sigil skill format

### Step 5: Register Skill

1. Save to `skills/ui/[framework]-ui/SKILL.md`
2. Update skills README with new skill
3. Notify user of new capability

## Output Format

```markdown
## New UI Skill Created

**Skill:** [framework]-ui
**Location:** `skills/ui/[framework]-ui/SKILL.md`

### Capabilities
- Component generation for [Framework]
- [Styling approach] styling support
- [Test framework] test generation
- Accessibility implementation via [API]

### Usage
The Developer agent will automatically use this skill when:
- Constitution specifies [Framework]
- Tasks involve [Framework] component implementation

### Verification
To verify the skill works correctly:
1. Create a simple component spec
2. Invoke Developer with a UI task
3. Check generated code follows [Framework] conventions
```

## Standard Contract Enforcement

All generated UI skills MUST:

1. **Accept these inputs:**
   - `component_spec` (object) — Component definition from ui-designer
   - `design_tokens` (object) — Tokens from figma-review or design-system-reader
   - `accessibility_requirements` (object) — Requirements from accessibility skill

2. **Produce these outputs:**
   - `component_files` — Main component implementation
   - `style_files` — Styling (if separate from component)
   - `test_files` — Component tests

3. **Implement accessibility** using framework's APIs

4. **Follow framework conventions** for file structure and naming

## Example: Creating Angular UI Skill

```markdown
---
name: angular-ui
description: Implements Angular components from design specifications. Supports Angular 16+, TypeScript, and standalone components.
version: 1.0.0
category: ui
chainable: true
invokes: []
invoked_by: [developer]
tools: Read, Write, Edit, Bash, Glob
inputs: [component_spec, design_tokens, accessibility_requirements]
outputs: [component_files, style_files, test_files]
---

# Skill: Angular UI

## Purpose

Implement Angular components from design specifications using standalone components and modern Angular patterns.

## Process

### Step 1: Detect Project Setup
\`\`\`bash
# Check Angular version
ng version
grep "@angular/core" package.json

# Check for standalone default
grep "standalone" angular.json
\`\`\`

### Step 2: Generate Component
\`\`\`typescript
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-custom-button',
  standalone: true,
  imports: [CommonModule],
  template: \`
    <button
      [class]="buttonClasses"
      [disabled]="disabled"
      [attr.aria-disabled]="disabled"
      (click)="handleClick($event)"
      (keydown.enter)="handleClick($event)"
      (keydown.space)="handleClick($event)"
    >
      <ng-content></ng-content>
    </button>
  \`,
  styles: [\`
    .btn { /* styles */ }
  \`]
})
export class CustomButtonComponent {
  @Input() variant: 'primary' | 'secondary' = 'primary';
  @Input() size: 'sm' | 'md' | 'lg' = 'md';
  @Input() disabled = false;
  @Output() clicked = new EventEmitter<MouseEvent>();

  get buttonClasses(): string {
    return \`btn btn--\${this.variant} btn--\${this.size}\`;
  }

  handleClick(event: Event): void {
    if (!this.disabled) {
      this.clicked.emit(event as MouseEvent);
    }
  }
}
\`\`\`

## Angular-Specific Patterns

### Standalone Components
- Preferred over NgModule-based components
- Import dependencies directly in @Component

### Signals (Angular 16+)
- Use for reactive state
- signal() for local state
- computed() for derived values

### Dependency Injection
- inject() function preferred
- Constructor injection still supported
```

## Human Checkpoint

**Tier:** Review

New skill creation requires review before use in production.

## Error Handling

| Error | Resolution |
|-------|------------|
| Framework not found | Ask for documentation URL |
| Patterns unclear | Generate minimal skill, flag for enhancement |
| No accessibility API | Document limitation, use HTML fallbacks |
| Conflicting with existing skill | Suggest extending existing skill |
