---
name: learning-capture
description: Captures learnings after task completion. Records gotchas, decisions, patterns, and task notes for future reference.
version: 1.3.0
category: learning
chainable: false
invokes: [shared-context-sync]
invoked_by: [developer, orchestrator, qa-engineer]
tools: Read, Write, Edit
model: haiku
---

# Skill: Learning Capture

## Purpose

Record what was learned during task completion. This builds institutional memory that helps avoid repeating mistakes and surfaces validated patterns.

## When to Invoke

**Automatically** by the Developer agent before marking a task `[x]` complete.

Do NOT invoke:
- For trivial tasks (documentation-only, config tweaks, formatting)
- If task is marked `[no-learn]` in tasks.md
- If the same learning was already captured this session

## Inputs

**Auto-loaded:**
- Current feature ID from `/.sigil/project-context.md`
- Task just completed (from context)

**Context available:**
- What was implemented
- Any issues encountered
- Decisions made

### Review Findings Input (Orchestrator Mode)

When invoked by the orchestrator after QA fix loops or security review, receives structured findings:

```yaml
mode: review-findings
source: "qa-fix-loop" | "security-review"
feature_id: "###-feature-name"
task_id: "T###"
findings:
  - title: "Short description of issue"
    severity: "Critical | Major | High | Medium"
    category: "Test Failure | Requirement | Security | OWASP A##"
    description: "What went wrong"
    resolution: "How it was fixed"
iterations: 3  # (qa-fix-loop only) number of fix iterations required
```

If `mode: review-findings` is present, skip the normal Process steps and use the **Process: Review Findings Mode** below.

## Process

### Step 1: Identify Current Feature

Read `/.sigil/project-context.md` to get:
- Current feature ID (e.g., `001-user-auth`)
- Feature name

If no active feature, skip capture.

### Step 2: Determine What to Capture

Ask yourself:

| Question | If Yes → Category |
|----------|-------------------|
| Did I encounter something unexpected? | **Gotcha** |
| Did I make an architectural choice? | **Decision** |
| Did I discover a reusable rule? | **Pattern candidate** |
| What did I actually do? | **Task note** |

Most task completions produce a task note. Gotchas, decisions, and pattern candidates are less common.

### Step 3: Check for Duplicates

Before writing, read the target file and check if a similar learning already exists:
- Same concept, different wording = duplicate
- Related but distinct = not a duplicate

If duplicate exists, skip capture.

### Step 4: Write to Appropriate File

**For task notes** → `/.sigil/learnings/active/features/[feature-id].md`

```markdown
## [Feature Name]

### Task Notes

- **[Task ID]** Brief description of what was done
  - Gotcha: Any surprise encountered (optional)
  - Note: Any other relevant detail (optional)
```

**For gotchas** → `/.sigil/learnings/active/gotchas.md`

```markdown
- **[Short description of the trap]**
  - Context: When this happens
  - Solution: How to avoid or fix
  - Feature: [feature-id]
  - Added: [YYYY-MM-DD]
```

**For decisions** → `/.sigil/learnings/active/decisions.md`

```markdown
- **[YYYY-MM-DD] [Decision title]**
  - Choice: What was chosen
  - Rationale: Why
  - Alternatives: What else was considered
  - Feature: [feature-id]
```

**For pattern candidates** → Add to task note with `[PATTERN?]` prefix

```markdown
- **[Task ID]** Built password reset flow
  - [PATTERN?] Always add expires_at column to token tables
```

### Step 5: Confirm Capture (Silent)

Do NOT tell the user about the capture unless there's an error. Learning capture should be invisible during normal operation.

### Step 5b: Push to Shared Repo (if connected)

After local write, check if shared context is active:

1. Read `~/.sigil/registry.json` — look up current project
2. If not active (missing file, or project not in registry) → skip silently
3. If active, format the learning entry in shared format:
   ```markdown
   ## [YYYY-MM-DD] Short title
   - **Contributor:** {git config user.email}
   - **Context:** When/why this applies
   - **Solution:** The learning content
   - **Tags:** tag1, tag2 (derived from category)
   ```
4. Map the local category to shared category:
   - Gotcha entry → `gotchas.md`
   - Decision entry → `decisions.md`
   - Pattern candidate (`[PATTERN?]`) → `patterns.md`
   - Task note (with substantive content) → `gotchas.md` (if gotcha noted) or skip (routine task notes don't sync)
5. Invoke `shared-context-sync` push protocol with category, content, and repo name
6. **On failure:** Silent. The push protocol handles queueing internally. Never surface sync errors to the user during task completion.

**What syncs vs what doesn't:**
- Gotchas, decisions, and pattern candidates → sync to shared repo
- Routine task notes (no gotcha, no pattern flag) → local only (too noisy for shared)

---

## Process: Review Findings Mode

Used when the orchestrator invokes this skill after QA fix loops or security review. This mode captures learnings from review handbacks — often the most valuable signals about what went wrong.

### RF-1: Filter Findings

Keep only substantive findings:
- **QA fix-loop:** Keep only `Major` or `Critical` severity. Also skip if the fix loop resolved in iteration 1 (single-pass fixes are routine, not learnings).
- **Security review:** Keep only `Medium`, `High`, or `Critical` severity.

If no findings pass the filter, skip capture entirely (silent exit).

### RF-2: Deduplicate Against Developer Capture

The developer's own learning-capture runs first (Step 6 of the developer agent). Check for existing entries:

1. Read `/.sigil/learnings/active/gotchas.md`
2. Read `/.sigil/learnings/active/features/[feature-id].md`
3. For each filtered finding, check if the same concept is already captured:
   - Same root cause, different wording = duplicate → skip
   - Same area but distinct insight = not a duplicate → capture

If all findings are duplicates, skip capture (silent exit).

### RF-3: Write Gotchas

For each non-duplicate finding, write to `/.sigil/learnings/active/gotchas.md` using the standard format with an added `Source:` field:

```markdown
- **[Short description of the trap]**
  - Context: When this happens
  - Solution: How to avoid or fix
  - Feature: [feature-id]
  - Source: QA fix-loop (N iterations) | Security review (OWASP A##)
  - Added: [YYYY-MM-DD]
```

Also add a task note to `/.sigil/learnings/active/features/[feature-id].md`:

```markdown
- **[Task ID]** [Brief description of what was fixed]
  - Gotcha: [What the review caught]
  - Source: QA fix-loop | Security review
```

### RF-4: Flag Pattern Candidates

For `High` or `Critical` severity security findings, add `[PATTERN?]` tag to the feature notes entry. This feeds into the existing promotion mechanism in `learning-review`:

```markdown
- **[Task ID]** Fixed SQL injection in user query
  - [PATTERN?] Always use parameterized queries for user-supplied values
  - Source: Security review (OWASP A03)
```

### RF-5: Silent Completion

Same as Step 5 — do NOT tell the user about the capture unless there's an error. Review findings capture should be invisible during normal operation.

## Token Budget Limits

Enforce these limits when writing:

| File | Max Items | Action on Exceed |
|------|-----------|------------------|
| patterns.md | 30 | Warn user, suggest `/sigil:learn --review` |
| gotchas.md | 30 | Warn user, suggest `/sigil:learn --review` |
| decisions.md | 20 | Warn user, allow overflow |
| Feature notes | 20 per feature | Summarize older entries |

If a file exceeds its limit:
```
Note: [file] has reached its limit (X items).
Run `/sigil:learn --review` to prune and promote learnings.
```

## Writing Guidelines

### Keep Entries Concise
- 1-2 sentences max per item
- Focus on actionable information
- Use specific terms, not vague descriptions

### Good Examples

```markdown
- **T003** Added JWT refresh token flow
  - Gotcha: Access tokens must be shorter-lived than refresh tokens
  - [PATTERN?] Store refresh tokens in httpOnly cookies, not localStorage
```

```markdown
- **Supabase RLS policies require explicit user_id checks**
  - Context: Queries fail silently when RLS blocks access
  - Solution: Always add `.eq('user_id', userId)` to queries
  - Feature: 001-user-auth
  - Source: QA fix-loop (3 iterations)
  - Added: 2026-01-23
```

> The `Source:` field is optional. Developer-originated captures omit it. Review-originated captures include it to distinguish how the learning was discovered.

### Bad Examples

```markdown
- Did some stuff with auth  # Too vague
- This was really hard to figure out  # Not actionable
- Always use best practices  # Meaningless
```

## Outputs

**Files modified:**
- `/.sigil/learnings/active/features/[feature-id].md` (task notes)
- `/.sigil/learnings/active/gotchas.md` (if gotcha found)
- `/.sigil/learnings/active/decisions.md` (if decision made)

**No handoff data** — This skill completes silently.

## Error Handling

| Error | Resolution |
|-------|------------|
| Feature file doesn't exist | Create it with header |
| learnings directory doesn't exist | Create full path |
| Duplicate detected | Skip silently |
| File exceeds limit | Warn user, still write |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.3.0 | 2026-02-10 | Audit: Expanded invoked_by to include qa-engineer |
| 1.2.0 | 2026-02-09 | S2-101: Added Step 5b — push to shared repo via shared-context-sync after local write |
| 1.1.0 | 2026-01-30 | Added review findings mode for QA/security handback learning capture |
| 1.0.0 | 2026-01-23 | Initial release |
