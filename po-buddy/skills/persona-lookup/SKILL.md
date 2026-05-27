---
name: persona-lookup
description: Looks up project personas from references/personas.md. Resolves persona references by name, surfaces persona attributes for journey mapping, and applies the Villain Check anti-persona concept.
version: 1.0.0
category: pm
chainable: false
invokes: []
invoked_by: [define, specify, validate]
tools: Read
---

# Skill: Persona Lookup

## Purpose

Resolve persona names to their full attribute profiles for use in journey mapping (`specify`), problem articulation (`define`), and adversarial scenario stress-testing (Villain Check in `validate`).

This skill is configurable — projects define their personas in `references/personas.md`. There is no hardcoded persona list. A starter template is provided at setup.

## When to Invoke

- Any time another skill references a persona by name
- Villain Check needs an adversarial persona (anti-persona pattern)

## Inputs

- `persona_name`: string — the persona to resolve
- `mode`: `lookup | list | villain` (default: `lookup`)

## Process

### Step 1: Load Personas File

Read `references/personas.md`. If the file doesn't exist, return:

```
No personas defined yet. Run `/setup` (or add references/personas.md manually).

A starter template is at the bottom of communication-style.md for reference.
```

### Step 2: Mode Behavior

| Mode | Behavior |
|------|----------|
| `lookup` | Find the persona by name. Return their attributes. Case-insensitive match. |
| `list` | List all defined personas with one-line summaries |
| `villain` | Return the project's anti-persona (Villain) — used by `/validate` for adversarial stress-testing |

### Step 3: Anti-Persona (Villain) Concept

The Villain is a configurable anti-persona — NOT a hardcoded character. Projects define their own. Common patterns:

- **Bad-faith user** — tries to exploit, cheat, or break the system
- **Reluctant adopter** — has to use the product but doesn't want to
- **Mistake-prone user** — accidentally takes destructive paths
- **Stressed user** — distracted, in a hurry, fat-fingers

The `references/personas.md` file should include a `## Villain` section (or equivalent anti-persona). If absent, return:

```
No Villain / anti-persona defined yet. The Villain Check needs an adversarial
persona to stress-test journeys.

Add one to references/personas.md, or define one in conversation now.
```

## Outputs

For `lookup`:

```json
{
  "name": "{Persona Name}",
  "role": "{role}",
  "context": "{situational context}",
  "goals": ["..."],
  "frustrations": ["..."]
}
```

For `list`: array of one-line persona summaries.

For `villain`: the anti-persona's attributes plus a suggested stress-test scenario.

## Anti-patterns

- **Don't invent personas.** If a name isn't in the file, ask the user to add it or pick from the list.
- **Don't hardcode personas.** This skill is project-configurable on purpose.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-27 | Initial release — S4-001 FR-C16 |
