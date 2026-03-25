---
name: technical-planner
description: Creates implementation plans from clarified specifications. Invoke when spec is clarified and user requests planning, says "plan", or "how should we build".
version: 1.2.0
category: engineering
chainable: true
invokes: [researcher, adr-writer]
invoked_by: [architect, orchestrator]
tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch
---

# Skill: Technical Planner

## Purpose

Transform clarified specifications into actionable implementation plans. Identifies technical approach, file changes, dependencies, and risks.

## When to Invoke

- Spec is clarified (no remaining ambiguities)
- Auto-invoked after clarifier completes
- User says "how should we build this" or "create a plan"
- Architect agent receives planning request

## Inputs

**Required:**
- `spec_path`: string — Path to clarified spec

**Optional:**
- `clarifications_path`: string — Path to clarifications if they exist
- `research_results`: object — Output from researcher skill if pre-research done

**Auto-loaded:**
- `constitution_path`: string — `/.sigil/constitution.md`
- `project_context`: string — `/.sigil/project-context.md`
- `current_profile`: object — From `/.sigil/project-profile.yaml` (if exists)
- `sibling_profiles`: array — From `~/.sigil/cache/shared/profiles/` (if connected)

## Pre-Execution Check

Before starting, update `.sigil/project-context.md`:
- Set **Current Phase** to `plan`
- Set **Feature** to the feature being planned
- Set **Spec Path** to the active spec directory
- Set **Last Updated** to the current timestamp

If `.sigil/project-context.md` does not exist, create it using the State Tracking format from the `/sigil:draw` command.

## Process

### Step 1: Context Loading

```
1. Load spec from spec_path
2. Load clarifications if present
3. Load constitution for technology constraints
4. Scan existing codebase structure
5. Identify relevant existing code
```

### Step 2: Research Phase (if needed)

For unfamiliar technologies or approaches:

```
1. Invoke researcher skill with specific questions
2. Research runs in parallel for multiple topics
3. Collect findings before proceeding
4. Document sources and recommendations
```

### Step 3: Technical Analysis

Analyze requirements to determine:

1. **Architecture Impact:** New components, modified components
2. **Data Model Changes:** New tables, schema modifications
3. **API Changes:** New endpoints, modified contracts
4. **Integration Points:** External services, internal modules
5. **Security Implications:** Auth, data handling, validation

### Step 4: Constitution Gate Checks

Validate approach against constitution gates:

**Simplicity Gate:**
- [ ] Solution uses ≤3 new dependencies
- [ ] No new infrastructure required
- [ ] Complexity proportional to problem

**Anti-Abstraction Gate:**
- [ ] Uses framework directly (no wrappers)
- [ ] No premature abstraction
- [ ] Follows existing patterns

**Integration-First Gate:**
- [ ] API contracts defined
- [ ] Data models documented
- [ ] Integration points identified

**Accessibility Gate:**
- [ ] WCAG requirements identified
- [ ] Keyboard navigation planned
- [ ] Screen reader behavior specified

**Cross-Repo Impact Gate (if profiles available):**

Run this gate when `current_profile` and `sibling_profiles` are loaded in context.

1. Load current project profile and sibling profiles from auto-loaded context
2. Parse plan changes for API, event, or package modifications:
   - New/modified/deleted API endpoints
   - Changed event names or payloads
   - Package interface changes
3. For each change that affects an `exposes` entry in the current profile:
   a. Search sibling profiles' `consumes` entries where `source` matches the current project name
   b. If matches found → this change has cross-repo impact
4. If cross-repo impacts detected, add a warning section to the plan:

```markdown
## Cross-Repo Impact Warning

The following changes may affect sibling projects:

| Change | Affected Project | What They Consume |
|--------|-----------------|-------------------|
| Modified `GET /api/products` | web-app | Product catalog API |
| Removed `order.completed` event | mobile-app | Order status updates |

**Action required:** Coordinate with affected project owners before proceeding.
```

5. Prompt user with options:
   - **Proceed** — Acknowledge impact, continue with plan
   - **Modify** — Adjust plan to avoid breaking changes
   - **Continue anyway** — Skip warning (not recommended)

If no profiles are available (solo mode or no profile configured), skip this gate silently.

- [ ] Cross-repo impact checked (if profiles loaded)
- [ ] Affected sibling projects identified
- [ ] Impact warning included in plan (if applicable)

### Step 5: Plan Generation

Using template and analysis:

```
1. Load template from /templates/plan-template.md
2. Document technical context
3. Record gate check results
4. List project structure changes (new/modified/deleted files)
5. Define API contracts if applicable
6. Document data model changes if applicable
7. List new dependencies with justification
8. Assess risks and mitigations
9. Outline testing strategy
10. Define implementation phases
```

### Step 6: ADR Identification

Identify decisions worthy of ADRs:

```
If decision meets ADR criteria:
  - Technology choice with alternatives
  - Architecture pattern selection
  - Trade-off with long-term implications
  - Breaking change or migration
Then:
  - Add to ADRs to Create list
  - Invoke adr-writer for each
```

### Step 7: Write Outputs

```
1. Write plan.md to spec directory
2. Write research.md if research conducted
3. Write data-model.md if data changes needed
4. Create adr/ directory if ADRs needed
5. Update project-context.md
```

## Outputs

**Primary Artifact:**
- `/.sigil/specs/###-feature/plan.md` — Implementation plan

**Secondary Artifacts (if applicable):**
- `/.sigil/specs/###-feature/research.md` — Research findings
- `/.sigil/specs/###-feature/data-model.md` — Data changes
- `/.sigil/specs/###-feature/adr/ADR-###-topic.md` — Architecture decisions

**Handoff Data:**
```json
{
  "plan_path": "/.sigil/specs/001-feature/plan.md",
  "spec_path": "/.sigil/specs/001-feature/spec.md",
  "estimated_complexity": "standard",
  "gate_violations": [],
  "requires_adr": true,
  "adr_topics": ["Authentication approach"],
  "files_to_modify": [
    "src/auth/login.ts",
    "src/api/users.ts"
  ],
  "files_to_create": [
    "src/auth/oauth.ts",
    "src/auth/oauth.test.ts"
  ],
  "new_dependencies": [
    {"name": "jose", "version": "^5.0.0", "reason": "JWT handling"}
  ],
  "research_conducted": true,
  "risk_level": "medium"
}
```

## Plan Quality Checklist

Before completing, verify:

- [ ] Technical context matches constitution
- [ ] All gate checks documented (pass or justified violation)
- [ ] File changes comprehensive (no surprises during implementation)
- [ ] API contracts complete for new endpoints
- [ ] Data changes include migration path
- [ ] Dependencies justified and security-reviewed
- [ ] Risks identified with mitigations
- [ ] Testing strategy covers all requirement types
- [ ] Implementation phases logical and sequential
- [ ] ADRs created for significant decisions

## Human Checkpoints

| Track | Tier | Behavior |
|-------|------|----------|
| Quick Flow | Auto | Plan inferred from quick-spec, no separate review |
| Standard | Review | User reviews plan before proceeding to task breakdown |
| Enterprise | Review | User reviews plan; ADRs presented separately for approval |

## Error Handling

| Error | Resolution |
|-------|------------|
| Spec not clarified | Return to clarifier skill |
| Constitution violation | Document violation, request human approval |
| Unknown technology | Invoke researcher skill |
| Breaking changes detected | Flag for explicit approval |

## Complexity Assessment

Plan should estimate implementation complexity:

| Level | Criteria | Track |
|-------|----------|-------|
| Simple | ≤5 files, no dependencies, no data changes | Quick Flow |
| Standard | ≤15 files, few dependencies, minor data changes | Standard |
| Complex | Many files, multiple dependencies, significant data changes | Enterprise |

## Example Invocations

**From spec:**
```
Architect: The user authentication spec is ready. Let me create an implementation plan.
```

**With research:**
```
User: Research best practices for OAuth2 with Next.js before planning
```

**After clarification:**
```
Clarifier: All questions resolved. Handing off to technical-planner.
Technical Planner: Creating implementation plan for user authentication...
```

## Integration Points

- **Invokes:** `researcher` for unknown technologies
- **Invokes:** `adr-writer` for significant decisions
- **Invoked by:** `architect` or `orchestrator`
- **Hands off to:** `task-decomposer`

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2.0 | 2026-03-11 | Moved from workflow/ to engineering/ category |
| 1.1.0 | 2026-02-09 | S2-102: Added Cross-Repo Impact Gate, auto-loaded current_profile and sibling_profiles inputs |
| 1.0.0 | 2026-01-20 | Initial release |
