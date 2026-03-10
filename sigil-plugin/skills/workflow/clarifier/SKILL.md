---
name: clarifier
description: Reduces specification ambiguity through structured Q&A. Invoke when spec has ambiguity flags or user requests clarification.
version: 1.2.0
category: workflow
chainable: true
invokes: [] # Routing after completion handled by orchestrator, not direct invocation
invoked_by: [spec-writer, business-analyst]
tools: Read, Write, Edit
---

# Skill: Clarifier

## Purpose

Systematically reduce ambiguity in specifications through targeted questions. Ensures specs are complete and unambiguous before planning begins.

## When to Invoke

- Spec has `requires_clarification: true` in handoff
- Auto-invoked after spec-writer completes with ambiguities
- User says "let's clarify" or "I have more details"
- Open Questions section has unresolved items

## Inputs

**Required:**
- `spec_path`: string — Path to spec needing clarification

**Optional:**
- `user_track`: string — From `.sigil/config.yaml` (`non-technical` | `technical`)

**From Handoff:**
- `ambiguity_flags`: string[] — List of identified ambiguities
- `iteration`: number — Current clarification round (default: 1)

**Auto-loaded:**
- `max_iterations`: number — Maximum rounds before escalation (default: 3)

## Pre-Execution Check

Before starting, update `.sigil/project-context.md`:
- Set **Current Phase** to `clarify`
- Set **Feature** to the feature being clarified
- Set **Spec Path** to the active spec directory
- Set **Last Updated** to the current timestamp

If `.sigil/project-context.md` does not exist, create it using the State Tracking format from the `/sigil` command.

## Process

### Step 0: Load Configuration

```
1. Read .sigil/config.yaml. If not found, use defaults.
2. Extract user_track value (default: non-technical)
3. Store for use in question generation and presentation
```

**User track branching:**
- **`non-technical`:** Auto-resolve "Technical" category ambiguities with sensible defaults (logged as `[auto — non-technical track]` in clarifications.md). Rephrase remaining questions in business terms. Hide implementation details.
- **`technical`:** Surface all categories including Technical. Add implementation trade-off framing to questions (e.g., "This affects performance vs. maintainability — which matters more here?"). Show file paths and component names in question context.

### Step 1: Load Context

```
1. Read spec from spec_path
2. Load existing clarifications.md if present
3. Identify Open Questions section
4. Load ambiguity flags from handoff
```

### Step 2: Categorize Ambiguities

Classify each ambiguity into categories:

| Category | Description | Example |
|----------|-------------|---------|
| **Scope** | What's included/excluded | "Should this handle admin users too?" |
| **Behavior** | How something should work | "What happens when session expires?" |
| **Edge Case** | Unusual situations | "What if user submits empty form?" |
| **Data** | Data format, validation | "What format should dates use?" |
| **Integration** | External system behavior | "How should we handle API failures?" |
| **Priority** | Importance/ordering | "Is real-time sync required or batch ok?" |
| **Technical** | Implementation constraints | "Must this work offline?" |
| **Accessibility** | A11y-specific needs | "How should errors be announced?" |

### Step 3: Generate Questions

For each ambiguity, create targeted questions:

```
Question Format:
- Context: [Why we're asking]
- Question: [Specific, answerable question]
- Options (if applicable): [Concrete choices]
- Default (if applicable): [Suggested answer if user unsure]
```

**Prioritize questions by:**
1. Blockers (can't proceed without answer)
2. High-impact (affects multiple requirements)
3. Quick wins (easy to answer, high clarity value)

### Step 4: Present Questions

Present questions grouped by category, max 5 per round:

```markdown
## Clarification Round [N]

### Scope Questions
**Q1:** [Question]
- Context: [Why this matters]
- Options: A) [Option] B) [Option] C) Other

### Behavior Questions
**Q2:** [Question]
- Context: [Why this matters]
```

### Step 5: Process Answers

When user provides answers:

```
1. Parse each answer
2. Update spec with clarified requirements
3. Mark Open Questions as resolved
4. Check if new ambiguities surfaced
5. Update clarifications.md with Q&A log
6. Tag each answer with **Source:** [human]
```

### Step 6: Resolution Check

```
If all ambiguities resolved:
  - Set requires_clarification: false
  - Hand off to technical-planner

If new ambiguities found AND iteration < max:
  - Increment iteration
  - Return to Step 2

If iteration >= max AND ambiguities remain:
  - Escalate to human with summary
  - Mark spec as "Needs Human Review"
```

## Outputs

**Artifact:**
- `/.sigil/specs/###-feature/clarifications.md` — Q&A log

**Updated Artifact:**
- `/.sigil/specs/###-feature/spec.md` — Updated with clarifications

**Handoff Data:**
```json
{
  "spec_path": "/.sigil/specs/001-feature/spec.md",
  "clarifications_path": "/.sigil/specs/001-feature/clarifications.md",
  "all_resolved": true,
  "remaining_ambiguities": [],
  "iteration": 2,
  "max_iterations_reached": false,
  "questions_asked": 7,
  "questions_answered": 7,
  "source_tags": "all-human"
}
```

## Clarifications.md Format

```markdown
# Clarifications: [Feature Name]

> **Spec:** [/.sigil/specs/###-feature/spec.md]
> **Rounds:** [N]
> **Status:** [In Progress | Complete]

---

## Round 1 — [Date]

### Q1: [Category] — [Question]
**Context:** [Why we asked]
**Answer:** [User's response]
**Source:** [human]
**Spec Update:** [How spec was modified]

### Q2: [Category] — [Question]
**Context:** [Why we asked]
**Answer:** [User's response]
**Source:** [human]
**Spec Update:** [How spec was modified]

---

## Round 2 — [Date]
...

---

## Resolution Summary

| Original Ambiguity | Resolution |
|--------------------|------------|
| [Ambiguity] | [How resolved] |
```

## Question Templates by Category

### Scope
- "Should [feature] include [capability] or is that separate?"
- "Does this apply to [user type] or only [other user type]?"
- "When you say [term], do you mean [interpretation A] or [interpretation B]?"

### Behavior
- "What should happen when [condition]?"
- "If [scenario], should the system [option A] or [option B]?"
- "How should [component] respond to [event]?"

### Edge Cases
- "What if [unusual situation]?"
- "How should we handle [error condition]?"
- "What's the expected behavior when [boundary condition]?"

### Data
- "What format should [data field] use?"
- "What are valid values for [field]?"
- "Is [field] required or optional?"

### Priority
- "Is [capability] must-have or nice-to-have?"
- "Which is more important: [option A] or [option B]?"
- "Can [feature] launch without [capability]?"

## Human Checkpoints

- **Auto Tier:** Question generation and presentation
- User provides answers (interactive)
- Escalation if max iterations reached

## Error Handling

| Error | Resolution |
|-------|------------|
| Spec not found | Report error, request valid path |
| User skips questions | Mark as "Deferred" not "Resolved" |
| Contradictory answers | Flag and ask for clarification |
| Iteration limit reached | Escalate with summary of remaining issues |

## Example Session

```
Clarifier: I have 4 questions to clarify your authentication feature.

**Q1 (Scope):** Should password reset be part of this feature, or is that a separate spec?
- A) Include password reset
- B) Separate feature (out of scope)
- C) Other

User: B - separate feature

**Q2 (Behavior):** After a failed login attempt, should the system:
- A) Show generic "Invalid credentials" (more secure)
- B) Specify whether email or password was wrong (better UX)
- C) Other

User: A - generic message for security

[...]

Clarifier: All questions resolved. Updating spec and proceeding to planning.
```

## Integration Points

- **Invoked by:** `spec-writer` when ambiguities detected
- **Updates:** Spec document with clarified requirements
- **Hands off to:** `technical-planner` when all resolved

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-20 | Initial release |
| 1.2.0 | 2026-02-19 | S3-100: Added user_track branching — non-technical auto-resolves Technical ambiguities, technical surfaces all categories with trade-off framing |
| 1.1.0 | 2026-02-09 | SX-003: Added `[human]` source tags to clarifications for provenance tracking |
