# Chains Directory

Contains skill chain definitions that orchestrate multi-skill workflows.

## Core Chains

| Chain | File | Use Case |
|-------|------|----------|
| Full Pipeline | `full-pipeline.md` | Standard/Enterprise track features (includes UI/UX design phase) |
| Quick Flow | `quick-flow.md` | Bug fixes, small changes |
| Discovery Chain | `discovery-chain.md` | New project setup and stack selection |
| Implement-Ready | `implement-ready.md` | Streamlined workflow for pre-decomposed tickets with acceptance criteria — skips spec/clarify/task-decompose, treats story as single task |

## Full Pipeline Overview

The full pipeline now includes a design phase for features with UI components:

```
Spec → Clarify → [UI/UX Design] → Plan → Tasks → Implement → Validate → Review
```

The UI/UX Design phase is automatically inserted when the feature has UI components. It handles:
- Framework selection (if not in constitution)
- Component hierarchy design
- Accessibility requirements (WCAG 2.1 AA)
- Figma integration (if available)

## Chain Definition Format

```markdown
---
name: chain-name
description: When to use this chain
track: quick|standard|enterprise|discovery|all
---

# Chain: [Name]

## Use Case
[When this chain applies]

## Skill Sequence
[Ordered list of skills with conditions]

## State Transitions
[What triggers moves between skills]

## Human Checkpoints
[Where the chain pauses for approval]

## Error Handling
[How failures are managed]
```

## Chain Execution

Chains are invoked by:
1. Orchestrator selecting based on complexity assessment
2. User explicitly requesting a track
3. Skills invoking as part of their workflow
