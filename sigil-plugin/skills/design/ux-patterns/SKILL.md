---
name: ux-patterns
description: Designs user flows, interaction patterns, and journey maps from specifications. Ensures UX best practices are applied.
version: 1.0.0
category: design
chainable: true
invokes: []
invoked_by: [uiux-designer]
tools: Read, Write, Glob
inputs: [spec_path, user_scenarios]
outputs: [user_flows, interaction_patterns, state_map]
---

# Skill: UX Patterns

## Purpose

Transform user scenarios from specifications into concrete user flows, interaction patterns, and state management requirements. This skill ensures UX best practices are considered before component design.

## When to Invoke

- After spec is clarified and before component design
- When designing new user-facing features
- When user scenarios need translation to interaction patterns
- UI/UX Designer needs UX foundation for component work

## Inputs

**Required:**
- `spec_path`: string — Path to feature specification

**Auto-loaded:**
- User scenarios from spec (P1/P2/P3)
- Functional requirements

**Optional:**
- `existing_flows`: string[] — Paths to existing UX documentation
- `design_assets`: string[] — Mockups or wireframes

## Process

### Step 1: Extract User Scenarios

From specification, identify:
- Primary user personas
- P1 (must-have) scenarios
- P2/P3 scenarios for completeness
- Entry points to the feature
- Exit points and success states

### Step 2: Map User Flows

For each P1 scenario, create flow:

```
[Entry Point] → [Step 1] → [Decision?] → [Step 2] → [Success State]
                              ↓
                         [Error State]
```

Include:
- Happy path (primary flow)
- Error paths (validation, system errors)
- Edge cases (empty states, loading, permissions)

### Step 3: Define Interaction Patterns

Map abstract actions to concrete interactions:

| User Goal | Interaction Pattern | Notes |
|-----------|---------------------|-------|
| Submit form | Button → Loading → Success/Error | Disable during submit |
| Select option | Dropdown/Radio/Checkbox | Based on option count |
| Navigate | Link/Tab/Breadcrumb | Based on hierarchy |
| Provide input | Text/Number/Date picker | Based on data type |

Apply UX heuristics:
- Visibility of system status
- Match between system and real world
- User control and freedom
- Consistency and standards
- Error prevention
- Recognition over recall
- Flexibility and efficiency
- Aesthetic and minimalist design
- Help users recover from errors
- Help and documentation

### Step 4: State Management Map

Identify states the UI must handle:

| State | Trigger | UI Response |
|-------|---------|-------------|
| Loading | Action initiated | Spinner/skeleton |
| Success | Action completed | Confirmation + next action |
| Error | Action failed | Error message + recovery |
| Empty | No data | Empty state + CTA |
| Partial | Incomplete data | Progress indicator |

### Step 5: Document Edge Cases

For each flow, document:
- What if user refreshes mid-flow?
- What if user navigates away and returns?
- What if session expires?
- What if data changes externally?
- What if user has no permission?

## Output Format

```markdown
## UX Patterns: [Feature Name]

### User Personas
- **Primary:** [Persona description]
- **Secondary:** [If applicable]

### User Flows

#### Flow 1: [Scenario Name] (P1)
```
[Start] → [Action 1] → [Decision Point]
                            ↓ Yes
                       [Action 2] → [Success]
                            ↓ No
                       [Alternative] → [Success]
```

**Happy Path:**
1. User [action]
2. System [response]
3. User [action]
4. System [response] — Success!

**Error Paths:**
- If [condition]: Show [error], allow [recovery]

**Edge Cases:**
- Empty state: [Description]
- Loading state: [Description]

### Interaction Patterns

| Action | Pattern | Rationale |
|--------|---------|-----------|
| [Action] | [Pattern] | [Why this pattern] |

### State Map

| State | Visual | User Can |
|-------|--------|----------|
| Initial | [Description] | [Available actions] |
| Loading | [Description] | [Available actions] |
| Success | [Description] | [Available actions] |
| Error | [Description] | [Available actions] |

### UX Heuristics Applied
- [Heuristic]: [How applied]

### Open UX Questions
- [Any unresolved UX decisions]
```

## Handoff Data

```json
{
  "flows_documented": 3,
  "states_identified": ["initial", "loading", "success", "error", "empty"],
  "interaction_patterns": ["form-submit", "list-filter", "modal-confirm"],
  "edge_cases_documented": true,
  "ux_questions": []
}
```

## Human Checkpoint

**Tier:** Auto (generation) + Review (as part of design review)

UX patterns are reviewed as part of overall design approval.

## Error Handling

| Error | Resolution |
|-------|------------|
| Spec lacks user scenarios | Request clarification from Business Analyst |
| Conflicting scenarios | Flag for user decision |
| Complex flow (>10 steps) | Suggest breaking into sub-flows |
