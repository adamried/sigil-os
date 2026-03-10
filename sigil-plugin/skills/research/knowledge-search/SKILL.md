---
name: knowledge-search
description: Searches project knowledge base for context, decisions, and patterns. Invoke when user asks "have we done this before", "what's our approach to X", "how do we handle X", "find examples of X", or "check existing patterns". Also invoked by agents before proposing new approaches to verify consistency with established conventions.
version: 1.0.0
category: research
chainable: true
invokes: []
invoked_by: [orchestrator, architect, developer, business-analyst]
tools: Read, Glob, Grep
---

# Skill: Knowledge Search

## Purpose

Search the project's accumulated knowledge base to find relevant context, past decisions, and existing patterns before starting new work. Prevents reinventing solutions and ensures consistency with established approaches.

## When to Invoke

- Starting work on a feature that may relate to existing work
- Checking for established patterns before proposing new ones
- Looking up past decisions that might apply
- Finding reusable components or approaches
- User asks "have we done something like this before?"
- Agent needs context about project conventions

## Inputs

**Required:**
- `query`: string — What to search for (natural language or keywords)

**Optional:**
- `scope`: string — "specs" | "decisions" | "code" | "learnings" | "all" (default: "all")
- `feature_context`: string — Current feature for relevance ranking
- `limit`: number — Maximum results per category (default: 5)

**Auto-loaded:**
- `project_context`: string — `/.sigil/project-context.md`

## Process

### Step 1: Parse Query

```
1. Extract key concepts from query
2. Identify related terms and synonyms
3. Determine search intent:
   - Looking for similar feature?
   - Looking for pattern/approach?
   - Looking for past decision?
   - Looking for code example?
```

### Step 2: Search Specifications

```
1. Glob: /.sigil/specs/**/*.md
2. For each spec:
   a. Check title and summary for relevance
   b. Search requirements for matching concepts
   c. Check user scenarios for similar patterns
3. Rank by relevance (keyword matches, conceptual similarity)
4. Extract relevant excerpts
```

### Step 3: Search Decisions

```
1. Glob: /.sigil/specs/**/adr/*.md (feature ADRs)
2. Read: /.sigil/constitution.md
3. For each decision document:
   a. Check decision title and context
   b. Match against query concepts
   c. Note implications for current work
4. Rank by applicability
```

### Step 4: Search Learnings

```
1. Read: /.sigil/learnings/active/patterns.md
2. Read: /.sigil/learnings/active/gotchas.md
3. Read: /.sigil/learnings/active/decisions.md
4. For each learning:
   a. Match against query
   b. Check if applies to current context
5. Prioritize validated patterns over raw notes
```

### Step 5: Search Code (if scope includes)

```
1. Grep for query terms in /src/**
2. For matching files:
   a. Identify component type (service, component, utility)
   b. Extract relevant code snippets
   c. Note reusability potential
3. Prioritize:
   - Similar implementations
   - Reusable utilities
   - Established patterns
```

### Step 6: Rank and Compile

```
1. Score each result:
   - Keyword match strength
   - Conceptual relevance
   - Recency (newer may be more relevant)
   - Authority (constitution > ADR > pattern > note)
2. Deduplicate overlapping information
3. Group by category
4. Generate summary for requesting agent
```

## Outputs

### Search Results Document

```markdown
## Knowledge Search Results

**Query:** "form validation patterns"
**Scope:** all
**Results Found:** 12 total (5 most relevant per category)

---

### Relevant Specifications

#### /.sigil/specs/002-checkout/spec.md
**Relevance:** 92%
**Summary:** Checkout form with payment validation

**Relevant Excerpt:**
> FR-005: System shall validate credit card format before submission
> FR-006: System shall display inline validation errors

**Why Relevant:** Same form validation pattern needed

---

#### /.sigil/specs/001-user-auth/spec.md
**Relevance:** 78%
**Summary:** Login and registration forms

**Relevant Excerpt:**
> FR-003: Email format shall be validated
> FR-004: Password strength indicator required

**Why Relevant:** Similar input validation requirements

---

### Relevant Decisions

#### ADR-G002: Validation Library Choice
**Relevance:** 95%
**Status:** Accepted

**Decision:** Use Zod for all schema validation

**Implication for Current Work:**
- Must use Zod, not Yup or custom validation
- Follow schema-first pattern
- Use `.safeParse()` for form validation

---

#### Constitution Article 2: Code Standards
**Relevance:** 80%

**Relevant Content:**
> All user inputs must be validated before processing
> Validation errors must be specific and actionable

---

### Relevant Patterns

#### /.sigil/learnings/active/patterns.md
**Pattern:** Form Validation Pattern
**Relevance:** 90%

```
When building forms:
1. Define Zod schema first
2. Use react-hook-form with zodResolver
3. Display errors inline, below inputs
4. Validate on blur for first interaction, then on change
```

---

#### /.sigil/learnings/active/gotchas.md
**Gotcha:** Async Validation
**Relevance:** 75%

```
Don't forget: Email uniqueness check is async.
Use debounce (300ms) to avoid API spam during typing.
See: /src/lib/validators/async-validators.ts
```

---

### Code Examples

#### /src/lib/validators/checkout.ts
**Relevance:** 88%
**Pattern:** Zod schema with custom error messages

```typescript
export const checkoutSchema = z.object({
  email: z.string().email("Please enter a valid email"),
  cardNumber: z.string().regex(/^\d{16}$/, "Card number must be 16 digits"),
});
```

**Reusable:** Yes - same pattern applies

---

### Summary

When implementing form validation for current feature:

1. **Use Zod** for schema definition (ADR-G002)
2. **Follow inline error pattern** from checkout spec
3. **Apply debounce** for any async validation (gotcha)
4. **Reference checkout validator** as template

**Confidence:** High (multiple corroborating sources)

**Suggested Next Step:** Review `/src/lib/validators/checkout.ts` as template
```

### Handoff Data

```json
{
  "query": "form validation patterns",
  "scope": "all",
  "results_count": {
    "specs": 3,
    "decisions": 2,
    "learnings": 4,
    "code": 3
  },
  "top_results": [
    {
      "type": "decision",
      "path": "ADR-G002",
      "relevance": 95,
      "key_point": "Use Zod for validation"
    },
    {
      "type": "pattern",
      "source": "patterns.md",
      "relevance": 90,
      "key_point": "Form validation pattern documented"
    }
  ],
  "actionable_insights": [
    "Use Zod (mandatory per ADR)",
    "Follow inline error pattern",
    "Apply debounce for async validation"
  ],
  "suggested_reference": "/src/lib/validators/checkout.ts",
  "confidence": "high"
}
```

## Search Scope Details

| Scope | Locations Searched | Best For |
|-------|-------------------|----------|
| `specs` | `/.sigil/specs/**/*.md` | Finding similar features |
| `decisions` | `/.sigil/specs/**/adr/*.md`, `/.sigil/constitution.md` | Finding applicable rules |
| `learnings` | `/.sigil/learnings/active/*.md` | Finding patterns and gotchas |
| `code` | `/src/**/*.{ts,tsx,js,jsx}` | Finding implementation examples |
| `all` | All of the above | Comprehensive context |

## Relevance Scoring

```
Score = (keyword_match × 0.3) + (concept_match × 0.4) + (authority × 0.2) + (recency × 0.1)

Where:
- keyword_match: Direct term matches (0-100)
- concept_match: Semantic similarity (0-100)
- authority: Source weight (constitution=100, ADR=90, spec=80, pattern=70, code=60)
- recency: Age factor (newer = higher, max 100)
```

## Query Interpretation

### Query Types

| Query | Interpretation | Primary Scope |
|-------|---------------|---------------|
| "how do we handle X" | Pattern search | learnings, code |
| "have we done X before" | Feature search | specs |
| "what's our approach to X" | Decision search | decisions |
| "example of X" | Code search | code |
| "why do we X" | Decision search | decisions |

### Keyword Expansion

When searching, expand queries:

| Original | Also Search |
|----------|-------------|
| "auth" | authentication, login, session, user |
| "form" | input, validation, submit |
| "API" | endpoint, route, request, response |
| "error" | exception, failure, catch, handle |

## Human Checkpoints

- **Tier:** Auto (search runs automatically)
- Results summarized for agent use
- No human approval needed for searches

## Error Handling

| Error | Resolution |
|-------|------------|
| No results found | Expand search scope, try related terms |
| Too many results | Narrow scope, increase relevance threshold |
| Scope directory missing | Search available scopes only, note gaps |
| Query too vague | Ask for clarification or search all |

## Example Invocations

**Pattern search:**
```
Agent: "How do we handle form validation in this project?"

→ knowledge-search queries "form validation"
→ Finds ADR-G002 (Zod decision)
→ Finds patterns.md entry
→ Finds code examples
→ Returns summary with actionable guidance
```

**Feature similarity:**
```
Agent: "Have we built anything like user profile editing?"

→ knowledge-search queries "user profile edit update"
→ Finds settings spec with profile section
→ Finds related user scenarios
→ Returns reference for approach
```

**Decision lookup:**
```
Agent: "Why do we use PostgreSQL?"

→ knowledge-search queries "PostgreSQL database"
→ Finds constitution Article 1
→ Finds ADR-G001 if exists
→ Returns decision context
```

## End-to-End Example

**User says:** "Have we done something like user profiles before?"

**Step 1 — Parse Query:**
```
Extracted concepts: "user profile", "profile editing", "user settings"
Related terms: account, preferences, avatar, personal info
Search intent: Feature similarity — looking for prior implementations
```

**Step 2 — Search Specifications:**
```
Glob: /.sigil/specs/**/*.md → 14 spec files found

/.sigil/specs/003-account-settings/spec.md
  Relevance: 88%
  Excerpt: "FR-012: User can update display name, avatar, and bio from Settings > Profile"
  Why relevant: Direct profile editing feature

/.sigil/specs/001-user-auth/spec.md
  Relevance: 62%
  Excerpt: "FR-008: Registration collects name, email, and optional avatar"
  Why relevant: Initial profile data collection
```

**Step 3 — Search Decisions:**
```
/.sigil/specs/003-account-settings/adr/ADR-003.md
  Relevance: 91%
  Status: Accepted
  Decision: Profile images stored in S3, referenced by URL in users table
  Implication: Reuse same avatar upload pattern
```

**Step 4 — Search Learnings:**
```
/.sigil/learnings/active/patterns.md
  Pattern: "Image Upload Pattern"
  Relevance: 78%
  Content: "Use presigned S3 URLs for client-side upload. Resize to 256×256 on
  Lambda trigger. See /src/lib/uploads/presigned.ts"

/.sigil/learnings/active/gotchas.md
  Gotcha: "Avatar cache busting"
  Relevance: 72%
  Content: "Append ?v={timestamp} to avatar URLs — CloudFront caches aggressively"
```

**Step 5 — Compile Results:**
```markdown
## Knowledge Search Results

**Query:** "user profiles"
**Results Found:** 8 total (top results shown)

### Summary

Yes — profile editing was implemented in spec 003 (Account Settings).

1. **Reuse the profile form pattern** from /src/features/settings/ProfileForm.tsx
2. **Follow S3 avatar upload** per ADR-003 (presigned URL → Lambda resize)
3. **Apply cache-busting** on avatar URLs (gotcha: CloudFront caching)
4. **Reference registration flow** for initial field set

**Confidence:** High
**Suggested Next Step:** Review /src/features/settings/ProfileForm.tsx as template
```

## Integration Points

- **Invoked by:** Any agent needing project context
- **Works with:** `researcher` (for external knowledge)
- **Works with:** `learning-reader` (for recent learnings)
- **Outputs to:** Requesting agent's working context

## Performance Notes

- Cache frequent searches within session
- Prefer Glob over exhaustive reads for large codebases
- Limit code search to source directories (skip node_modules, build)
- Return excerpts, not full files

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-25 | Initial release - full implementation |
| 0.1.0-stub | 2026-01-16 | Stub created |
