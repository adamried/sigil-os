---
name: routing-rules
description: Single source of truth for orchestrator routing logic — trigger words, natural language patterns, routing precedence, and context-aware routing.
version: 1.0.0
category: workflow
chainable: false
invokes: []
invoked_by: [orchestrator]
type: reference
---

# Skill: Routing Rules (Reference)

> **This is a reference skill.** It is not invoked directly. The orchestrator reads this file to determine routing behavior.

## Purpose

Centralize all routing logic in one place so the orchestrator (`sigil.md`) has a single source of truth for how to interpret user input and route to the correct workflow.

## Routing Precedence

When multiple routing rules could match, apply in this order:

1. **Explicit command** — `/sigil:draw continue`, `/sigil:draw status`, `/sigil:draw help`
2. **Ticket key** — Matches `[A-Z][A-Z0-9]+-\d+` pattern (e.g., `PROJ-123`)
3. **Resume intent** — "continue", "keep going", "next step", "what's next"
4. **Status intent** — "status", "where are we", "show progress", "what's done"
5. **Help intent** — "help", "what can you do", "how does this work"
6. **Feature description** — Any other text → new feature workflow

## Trigger Word Matrix

| Trigger Words | Route | Notes |
|--------------|-------|-------|
| `continue`, `next`, `keep going`, `what's next`, `resume` | Resume current workflow | Reads project-context.md for current phase |
| `status`, `where are we`, `show progress`, `what's done` | Status dashboard | Invokes status-reporter skill |
| `help`, `what can you do`, `how does this work` | Help output | Shows command reference |
| `PROJ-123` (ticket pattern) | Ticket-loader → routing by category | Fetches ticket, routes by type |
| `build`, `create`, `add`, `implement`, `make`, `I want`, `we need` | New feature workflow | Complexity assessment → track selection |
| `fix`, `bug`, `broken`, `not working`, `error` | New feature workflow | Often routes to Quick Flow via complexity |
| `update`, `change`, `modify`, `refactor` | New feature workflow | Complexity determines track |
| `discover`, `new project`, `start fresh`, `greenfield` | Discovery track | Triggers codebase-assessment first |

## Natural Language Patterns

### Feature Start Patterns
```
"I want to build..."        → feature description
"Let's create..."           → feature description
"Build me..."               → feature description
"Add..."                    → feature description
"Implement..."              → feature description
"Create feature..."         → feature description
"Can we add..."             → feature description
"I need..."                 → feature description
"We should have..."         → feature description
```

### Resume Patterns
```
"Continue"                  → /sigil:draw continue
"Keep going"                → /sigil:draw continue
"Next step"                 → /sigil:draw continue
"What's next"               → /sigil:draw continue
"Where were we"             → /sigil:draw continue
"Pick up where we left off" → /sigil:draw continue
"Let's keep working"        → /sigil:draw continue
```

### Status Patterns
```
"What's the status"         → /sigil:draw status
"Where are we"              → /sigil:draw status
"Show progress"             → /sigil:draw status
"What's done"               → /sigil:draw status
"How far along"             → /sigil:draw status
"Progress update"           → /sigil:draw status
```

### Ticket Patterns
```
"Work on PROJ-123"          → /sigil:draw PROJ-123
"Pick up PROJ-123"          → /sigil:draw PROJ-123
"Start PROJ-123"            → /sigil:draw PROJ-123
"PROJ-123"                  → /sigil:draw PROJ-123
```

## Context-Aware Routing

### When a Feature is In Progress

If `project-context.md` shows an active workflow, and the user provides a new feature description:

1. **Warn** — "You have a feature in progress: [name]"
2. **Offer options:**
   - Continue current feature
   - Park current and start new
   - Cancel

### When No Constitution Exists

If the user provides a feature description but no constitution exists:

1. **Block** — Cannot start feature work without a constitution
2. **Redirect** — Run constitution-writer first
3. **Then resume** — Return to feature description after constitution is created

### When Greenfield Detected

If codebase-assessment finds no code or minimal scaffolding:

1. **Suggest** — Discovery track before feature work
2. **Allow override** — User can skip discovery if they choose

## Ticket Category Routing

After ticket-loader categorizes a ticket:

| Category | Route |
|----------|-------|
| `maintenance` | Quick Flow (skip complexity assessor) |
| `pre-decomposed` | Implement-Ready chain (story = task, AC = spec) |
| `bug` (no security labels) | Standard track (cap, skip Enterprise) |
| `feature` | Normal routing via complexity assessment |
| `enhancement` | Normal routing via complexity assessment |

## Track Selection After Complexity Assessment

| Score Range | Track | Key Differences |
|-------------|-------|-----------------|
| 7–10 | Quick Flow | Lightweight spec, skip clarifier, 1 QA fix attempt, no formal code/security review |
| 11–16 | Standard | Full pipeline with all phases |
| 17–21 | Enterprise | Full pipeline + mandatory research + mandatory ADRs + mandatory security review |
