---
name: learning-review
description: Reviews, prunes, and promotes learnings. Helps maintain learning quality by archiving old items and promoting validated patterns.
version: 1.0.0
category: learning
chainable: false
invokes: []
invoked_by: [orchestrator]
tools: Read, Write, Edit
model: sonnet
---

# Skill: Learning Review

## Purpose

Maintain learning quality through periodic review. Promote validated pattern candidates, archive completed feature notes, and deduplicate entries.

## When to Invoke

- User runs `/sigil:learn --review`
- A feature is marked complete in project-context.md
- User asks to "clean up learnings" or "review what we learned"
- Any learning file exceeds its item limit

## Process

### Step 1: Load All Active Learnings

Read all files in `/.sigil/learnings/active/`:
- `patterns.md`
- `gotchas.md`
- `decisions.md`
- `features/*.md`

### Step 2: Identify Candidates for Action

#### Promotion Candidates

Scan feature notes for `[PATTERN?]` markers:

```
Found 3 pattern candidates:

1. "Always add expires_at to token tables"
   From: 001-user-auth, Task 3

2. "Use RLS policies for user-scoped queries"
   From: 001-user-auth, Task 5

3. "Resize images client-side before upload"
   From: 002-product-catalog, Task 8

Promote any to Patterns? (Enter numbers, 'all', or 'none')
```

#### Archive Candidates

Check project-context.md for completed features:

```
Feature 001-user-auth is marked complete.

Archive its task notes? (y/n)
- This moves detailed notes to /archived/
- Promoted patterns and gotchas remain in /active/
- Decisions referencing this feature stay active
```

#### Duplicate Candidates

Identify semantically similar entries:

```
Possible duplicates found:

1. Gotcha: "Supabase storage has 50MB limit"
   Gotcha: "Storage uploads fail over 50MB"
   → Keep first, remove second? (y/n)

2. Pattern: "Add expires_at to tokens"
   Pattern: "Token tables need expiration"
   → Merge into single entry? (y/n)
```

#### Stale Items

Flag items older than 90 days without recent references:

```
Stale items (no recent activity):

1. Decision: "Chose Tailwind over styled-components" (92 days)
   → Keep or archive? (k/a)
```

### Step 3: Execute User Decisions

#### Promoting a Pattern

1. Add to `/.sigil/learnings/active/patterns.md`:
```markdown
- **[Pattern description]**
  - When: Context for when this applies
  - Why: Rationale
  - Promoted: [YYYY-MM-DD] from [feature-id]
```

2. Remove `[PATTERN?]` tag from source feature notes
3. Keep the original task note (just remove the tag)

#### Archiving Feature Notes

1. Move `/.sigil/learnings/active/features/[feature-id].md`
   → `/.sigil/learnings/archived/[feature-id].md`

2. Add archive header:
```markdown
---
archived: YYYY-MM-DD
feature: [feature-id]
reason: Feature complete
---
```

3. Keep any gotchas/decisions that reference this feature (they stay active)

#### Removing Duplicates

1. Keep the more complete/recent entry
2. Delete the duplicate
3. Note in the kept entry: `<!-- Merged duplicate YYYY-MM-DD -->`

### Step 4: Report Summary

```
Learning Review Complete
========================

Promoted:     2 patterns
Archived:     1 feature (15 task notes)
Deduplicated: 3 entries
Kept stale:   1 decision

Current totals:
- Patterns:    12/30
- Gotchas:     8/30
- Decisions:   5/20
- Active features: 2

All limits healthy.
```

### Step 5: Update Project Context

Note the review in `/.sigil/project-context.md`:
```markdown
## Recent Activity
- [YYYY-MM-DD] Learning review: promoted 2 patterns, archived 001-user-auth
```

## Interactive Prompts

### Pattern Promotion

```
Pattern Candidate Review
------------------------

From: 001-user-auth, Task 3

  [PATTERN?] Always add expires_at to token tables

This was marked as a potential pattern during implementation.

Options:
  [p] Promote to patterns.md
  [e] Edit before promoting
  [s] Skip (leave as candidate)
  [d] Delete (not worth keeping)

Choice:
```

### Feature Archive

```
Archive Feature Notes
--------------------

Feature: 001-user-auth (User Authentication)
Status:  Complete
Notes:   15 task notes, 2 pattern candidates

The feature is done. Archiving moves task notes to /archived/
while keeping promoted patterns and gotchas active.

Archive now? (y/n):
```

### Duplicate Resolution

```
Duplicate Detected
-----------------

Entry 1 (patterns.md, line 12):
  "Always validate email format on server"

Entry 2 (patterns.md, line 28):
  "Server-side email validation required"

These appear to be the same pattern.

Options:
  [1] Keep entry 1, remove entry 2
  [2] Keep entry 2, remove entry 1
  [m] Merge into new combined entry
  [k] Keep both (not duplicates)

Choice:
```

## Rules

1. **Always ask before promoting or archiving**
   - Never auto-promote patterns
   - Never auto-archive without confirmation

2. **Never delete without moving first**
   - Archived items go to `/archived/`
   - Nothing is permanently deleted during review

3. **Preserve attribution**
   - Promoted patterns note their source feature
   - Archived files keep their history

4. **Respect limits**
   - If patterns.md is at 30 items, require removal before adding
   - Suggest demotion of older patterns if needed

## Outputs

**Files modified:**
- `/.sigil/learnings/active/patterns.md` (promotions)
- `/.sigil/learnings/active/gotchas.md` (deduplication)
- `/.sigil/learnings/active/decisions.md` (deduplication)
- `/.sigil/learnings/active/features/*.md` (tag removal)
- `/.sigil/learnings/archived/*.md` (archives)
- `/.sigil/project-context.md` (activity log)

## Error Handling

| Error | Resolution |
|-------|------------|
| No learnings exist | "No learnings to review yet" |
| Archive dir missing | Create it |
| File parse error | Skip file, warn user |
| User cancels | Exit gracefully, no changes |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-23 | Initial release |
