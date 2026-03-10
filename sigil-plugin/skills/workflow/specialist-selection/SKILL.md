---
name: specialist-selection
description: Selects appropriate specialist agents for implementation and validation tasks based on file scope, keywords, and project context. Invoke during task decomposition and before implementation/validation phases.
version: 1.1.0
category: workflow
chainable: true
invokes: []
invoked_by: [task-decomposer, orchestrator]
tools: Read, Glob
---

# Skill: Specialist Selection

## Purpose

Select the most appropriate specialist agent(s) for a given task based on file scope, description keywords, and project tech stack. Returns a specialist assignment that the implementation loop uses to load specialist behavior overrides on top of base agents.

## When to Invoke

- During task decomposition (after Step 4, before task enrichment)
- Before implementation phase when Orchestrator needs specialist routing
- Before validation phase to select appropriate QA/security specialists

## Inputs

**Required:**
- `task_description`: string — Task description text
- `task_files`: string[] — Files the task will touch

**Optional:**
- `constitution_path`: string — Path to constitution (for project type/rigor)
- `tech_stack`: object — Detected tech stack from constitution or profile

## Process

### Step 1: Developer Specialist Selection

For implementation tasks, run a selection cascade to find the best developer specialist:

#### 1a. File Scope Matching (Highest Priority)

Match file paths against specialist domains:

<!-- payment-developer: tabled, see dev-docs/payment-developer-draft.md -->

| Path Pattern | Specialist |
|-------------|-----------|
| `**/api/**`, `**/routes/**`, `**/endpoints/**`, `**/controllers/**` | `api-developer` |
| `**/components/**`, `**/pages/**`, `**/views/**`, `**/layouts/**`, `**/styles/**`, `**/*.css`, `**/*.scss` | `frontend-developer` |
| `**/models/**`, `**/migrations/**`, `**/schema/**`, `**/seeds/**`, `**/db/**` | `data-developer` |
| `**/integrations/**`, `**/external/**`, `**/clients/**`, `**/webhooks/**`, `**/services/*-client.*` | `integration-developer` |

#### 1b. Description Keyword Matching (Secondary)

If no file scope match, check task description:

| Keywords | Specialist |
|----------|-----------|
| "API", "endpoint", "route", "REST", "GraphQL", "request", "response", "middleware" | `api-developer` |
| "component", "UI", "render", "CSS", "layout", "responsive", "animation", "accessibility" | `frontend-developer` |
| "schema", "migration", "query", "database", "model", "index", "seed", "ORM" | `data-developer` |
| "integration", "third-party", "webhook", "OAuth", "SDK", "external service", "retry" | `integration-developer` |

#### 1c. Tech Stack Filter

Exclude specialists irrelevant to the project stack:
- No frontend framework detected → exclude `frontend-developer`
- No database detected → exclude `data-developer`
- No external integrations in plan → exclude `integration-developer`

#### 1d. Fallback

If no specialist matched or all were excluded → use base `developer` agent (no specialist override).

### Step 2: Multi-Domain Handling

When a task touches multiple specialist domains:

1. **Dominant domain** (>60% of files): Assign that specialist
2. **Secondary domain** (20-40% of files): Add a collaboration note referencing the secondary specialist's priorities
3. **Even split** (within 20%): Recommend splitting the task into domain-specific subtasks. Flag for task-decomposer review.

### Step 3: Validation Specialist Selection

For QA validation phases, select specialists based on these rules:

| Specialist | Assignment Rule |
|-----------|----------------|
| `functional-qa` | **Always assigned** — every task gets functional validation |
| `edge-case-qa` | Assign when: project type is Standard or Enterprise, OR constitution specifies high-reliability requirements |
| `performance-qa` | Assign when: project type is Enterprise, OR spec mentions performance requirements, OR task touches database/query files or frontend bundle files |
| `appsec-reviewer` | Assign when: task touches auth/login/session/password/upload/input files, OR description contains security keywords |
| `data-privacy-reviewer` | Assign when: task touches user data/PII/profile/payment/consent files, OR description mentions GDPR/CCPA/privacy/compliance |

Multiple validation specialists can be assigned to the same task. They run in sequence.

### Step 4: Security Specialist Selection

For the security review phase (after all tasks complete):

- `appsec-reviewer`: Assign if any task in the feature touched auth, input handling, or file upload code
- `data-privacy-reviewer`: Assign if any task in the feature touched PII, user data, or compliance-related code
- Both can be assigned. If neither matches, use base `security` agent.

## Outputs

**Specialist Assignment:**
```json
{
  "task_id": "T003",
  "developer_specialist": "api-developer",
  "developer_specialist_reason": "Files match API path pattern (src/api/auth.ts)",
  "collaboration_notes": "Secondary domain: data-developer (touches migration file)",
  "validation_specialists": ["functional-qa", "appsec-reviewer"],
  "validation_reasons": {
    "functional-qa": "Always assigned",
    "appsec-reviewer": "Task touches auth files"
  }
}
```

**No Specialist Match:**
```json
{
  "task_id": "T001",
  "developer_specialist": null,
  "developer_specialist_reason": "Setup task — no specialist domain match, using base developer agent",
  "validation_specialists": ["functional-qa"],
  "validation_reasons": {
    "functional-qa": "Always assigned"
  }
}
```

## Specialist Loading Protocol

When a specialist is assigned, the implementation loop loads it by:

1. Read `agents/specialists/[name].md`
2. Read base agent from `extends` field (e.g., `agents/developer.md`)
3. Merge: specialist sections override base agent sections of the same name
4. Adopt merged behavior for the duration of that task

Tasks without a specialist assignment use the base agent directly.

## Worked Example

A feature spec calls for "Add Stripe webhook endpoint to handle payment confirmations and update the orders table."

**Input:**
```json
{
  "task_description": "Implement Stripe webhook endpoint for payment_intent.succeeded events, validate signature, update order status in DB",
  "task_files": [
    "src/api/webhooks/stripe.ts",
    "src/api/webhooks/stripe.test.ts",
    "src/models/order.ts",
    "src/migrations/20260301_add_payment_status.ts"
  ]
}
```

**Step 1 — Developer Specialist Selection:**

File scope matching:
- `src/api/webhooks/stripe.ts` → matches `**/api/**` → `api-developer` (2 files)
- `src/models/order.ts` → matches `**/models/**` → `data-developer` (1 file)
- `src/migrations/20260301_add_payment_status.ts` → matches `**/migrations/**` → `data-developer` (1 file)

Domain breakdown: api-developer 50%, data-developer 50% — even split (within 20%).

However, keyword matching breaks the tie: "webhook", "endpoint" strongly signal `api-developer`.

Secondary domain note added for `data-developer` (migration + model file).

**Step 2 — Validation Specialist Selection:**

- `functional-qa` — always assigned
- `appsec-reviewer` — description contains "validate signature" (security keyword), files touch input handling
- `edge-case-qa` — project type is Standard (from constitution)

**Result:**
```json
{
  "task_id": "T007",
  "developer_specialist": "api-developer",
  "developer_specialist_reason": "Files match API path pattern (src/api/webhooks/stripe.ts); keywords 'webhook', 'endpoint' confirm",
  "collaboration_notes": "Secondary domain: data-developer (touches src/models/order.ts and migration file — ensure ORM conventions followed)",
  "validation_specialists": ["functional-qa", "edge-case-qa", "appsec-reviewer"],
  "validation_reasons": {
    "functional-qa": "Always assigned",
    "edge-case-qa": "Project type is Standard",
    "appsec-reviewer": "Task involves webhook signature validation and external input handling"
  }
}
```

## Error Handling

| Error | Resolution |
|-------|------------|
| Specialist file not found | Log warning, fall back to base agent |
| Multiple equally strong matches | Use first match from file scope; add collaboration note for second |
| Tech stack unknown | Skip tech stack filter, use file scope and keyword matching only |
| All specialists excluded by filter | Use base agent |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-19 | Initial release (S3-101) |
| 1.1.0 | 2026-02-26 | Removed payment-developer routing (tabled — specialist file removed in af0e2c8) |
