---
name: framework-selector
description: Recommends UI framework based on target platforms, constraints, and project needs. Invoke when no framework is specified in constitution and UI work is needed.
version: 1.0.0
category: design
chainable: true
invokes: []
invoked_by: [uiux-designer]
tools: Read, Write, Glob, Grep, WebSearch
inputs: [target_platforms, team_constraints, performance_requirements]
outputs: [framework_recommendation, rationale]
---

# Skill: Framework Selector

## Purpose

Analyze project requirements and recommend the most appropriate UI framework. This skill bridges the gap between business requirements (platforms, users) and technical implementation (framework choice).

## When to Invoke

- Constitution does not specify a UI framework
- User asks "what framework should we use?"
- New project without established UI patterns
- UI/UX Designer needs framework decision before component design

## Inputs

**Required:**
- `target_platforms`: string[] — Platforms the UI must support (web, ios, android, desktop, all)

**Optional:**
- `team_constraints`: string — Known team expertise or limitations
- `performance_requirements`: string — Performance-critical needs (offline, real-time, etc.)
- `existing_codebase`: boolean — Whether there's existing code to consider
- `constitution_path`: string — Path to constitution for context

## Process

### Step 1: Platform Analysis

Map target platforms to framework categories:

| Platforms | Framework Category |
|-----------|-------------------|
| Web only | Web frameworks (React, Vue, Svelte, Angular) |
| iOS only | Native iOS (SwiftUI, UIKit) |
| Android only | Native Android (Jetpack Compose, XML) |
| iOS + Android | Cross-platform mobile (React Native, Flutter) |
| Web + Mobile | Universal (React Native Web, Flutter Web, or separate) |
| Desktop | Desktop frameworks (Electron, Tauri, native) |
| All platforms | Evaluate trade-offs carefully |

### Step 2: Constraint Evaluation

Consider constraints that narrow options:
- Team expertise (don't recommend Flutter if team knows React)
- Performance needs (native for high-performance, cross-platform for speed)
- Time to market (cross-platform faster for multi-platform)
- Maintenance (single codebase vs. platform-specific)
- Existing patterns (if codebase exists, prefer consistency)

### Step 3: Generate Options

Present 2-3 viable options with:
- Framework name and category
- Platforms supported
- Key strengths
- Key trade-offs
- Best suited for (scenario)
- Learning curve consideration

### Step 4: Make Recommendation

Recommend one option with clear rationale tied to user's priorities.

## Framework Knowledge Base

### Web Frameworks

| Framework | Best For | Trade-offs |
|-----------|----------|------------|
| **React** | Large apps, ecosystem, hiring | Bundle size, decision fatigue |
| **Vue** | Progressive adoption, simplicity | Smaller ecosystem than React |
| **Svelte** | Performance, small bundles | Smaller community, less tooling |
| **Angular** | Enterprise, opinionated structure | Steep learning curve, verbose |

### Mobile Frameworks

| Framework | Best For | Trade-offs |
|-----------|----------|------------|
| **React Native** | React teams, code sharing with web | Performance ceiling, native bridge |
| **Flutter** | Consistent UI, performance | Dart language, larger app size |
| **SwiftUI** | iOS-first, Apple ecosystem | iOS only, newer/less mature |
| **Jetpack Compose** | Android-first, modern | Android only, newer |

### Cross-Platform

| Framework | Best For | Trade-offs |
|-----------|----------|------------|
| **React Native + Web** | Maximum code sharing | Complexity, compromises |
| **Flutter (all)** | Consistent experience | Dart, web performance |
| **Separate codebases** | Best native experience | Higher maintenance |

## Output Format

```markdown
## Framework Recommendation

### Target Platforms
[List of platforms from input]

### Options Evaluated

#### Option A: [Framework] (Recommended)
- **Platforms:** [Supported platforms]
- **Strengths:** [Key benefits]
- **Trade-offs:** [Considerations]
- **Best for:** [Ideal scenario]
- **Learning curve:** [Low/Medium/High]

#### Option B: [Framework]
- **Platforms:** [Supported platforms]
- **Strengths:** [Key benefits]
- **Trade-offs:** [Considerations]
- **Best for:** [Ideal scenario]
- **Learning curve:** [Low/Medium/High]

### Recommendation
**[Framework]** because [rationale tied to user's specific needs].

### Next Steps
1. Confirm framework selection
2. Update constitution with framework choice
3. Proceed with component design using framework patterns
```

## Handoff Data

```json
{
  "selected_framework": "react-native",
  "target_platforms": ["ios", "android"],
  "rationale": "Cross-platform mobile with React ecosystem benefits",
  "implementation_skill": "react-native-ui",
  "update_constitution": true
}
```

## Human Checkpoint

**Tier:** Review

Framework selection requires user confirmation before:
- Updating constitution
- Proceeding with component design
- Committing to framework-specific patterns

## Error Handling

| Error | Resolution |
|-------|------------|
| No platforms specified | Ask user for target platforms |
| Conflicting requirements | Present trade-offs, ask for priority |
| Unknown framework requested | Research via WebSearch, assess viability |
| All options have significant trade-offs | Present honestly, let user decide |
