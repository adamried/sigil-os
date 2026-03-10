---
name: status-reporter
description: Shows current workflow status. Invoke when user says "where are we", "show progress", "what's done", "what's the status", "what's happening", "/sigil status", or asks about current state of work. Presents progress in plain language.
version: 1.1.0
category: workflow
chainable: false
invokes: []
invoked_by: [orchestrator]
tools: Read, Glob
model: haiku
inputs: [context_path, user_track]
outputs: [status_output]
---

# Skill: Status Reporter

## Purpose

Generate a clear, human-readable status report of the current workflow state. This skill reads the project context and formats it as an easy-to-understand dashboard, adapting detail level to the configured user track.

## When Invoked

**Trigger phrases:**
- "status"
- `/sigil` or `/sigil status`
- "Where are we?"
- "What's the current state?"
- "Show me progress"
- "What's happening?"

**Context:** User wants to understand current workflow state without technical details.

## Workflow

### Step 0: Load Configuration

```
1. Read .sigil/config.yaml. If not found, use defaults.
2. Extract user_track value (default: non-technical)
3. Adapt output formatting based on track
```

**User track branching:**
- **`non-technical`:** Use plain-English phase names ("Writing the code" instead of "Implement"), hide agent names, show progress as "3 of 8 steps done", hide file paths and spec locations
- **`technical`:** Use current behavior (phase names, agent names visible) plus show specialist names when S3-101 specialists are active (e.g., "Developer Agent (api-developer) implementing T003")

### Step 1: Load Context

Read `/.sigil/project-context.md` to get current state:
- Active feature
- Current phase
- Workflow track
- Recent activity
- Open decisions
- Active blockers

### Step 2: Determine Progress

Map workflow phases to progress indicators:

| Phase | Progress |
|-------|----------|
| Assess | 10% |
| Specify | 20% |
| Clarify | 30% |
| Plan | 40% |
| Tasks | 50% |
| Implement | 60% |
| Validate | 75% |
| Review | 90% |
| Complete | 100% |

### Step 3: Format Output

Generate status report in standard format (see Output Format below). Verify icons and separators match `templates/output-formats.md`.

### Step 4: Add Recommendations

Based on current phase and state, suggest the next logical action for the user.

## Input Schema

```json
{
  "context_path": "/.sigil/project-context.md"
}
```

## Output Schema

```json
{
  "feature_name": "Feature being worked on",
  "track": "Quick | Standard | Enterprise",
  "phase": "Current phase",
  "progress_percent": 60,
  "current_activity": "Plain language description",
  "blockers": ["List of blockers or empty"],
  "next_step": "What to do next",
  "status_markdown": "Full formatted output"
}
```

## Output Format

Before displaying, verify icons and separators match `templates/output-formats.md`.

```markdown
📋 Project: {ProjectName}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Active Feature: "{Feature Name}" | Track: {Track}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Assess        — Track determined
✅ Specify       — spec.md created
✅ Clarify       — Requirements clear
✅ Plan          — plan.md created
⬚ Tasks         — Breaking down work
⬚ Implement     — Writing code
⬚ Validate      — Running checks
⬚ Review        — Final review

**Overall:** [██████░░░░] 60%

### Current Activity
{Plain language description of what's happening now}

### Blockers
{List blockers or "None — all clear"}

### Open Decisions
{List pending decisions or "None pending"}

### Next Step
{Clear instruction for user on what to do next}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
*Last updated: {Timestamp}*
```

## Phase Descriptions

Use these plain-language descriptions for each phase:

| Phase | Description |
|-------|-------------|
| Assess | "Determining how to approach your request" |
| Specify | "Writing detailed specification for your feature" |
| Clarify | "Resolving questions about requirements" |
| Plan | "Designing the technical approach" |
| Tasks | "Breaking work into smaller steps" |
| Implement | "Writing the code" |
| Validate | "Running automated quality checks" |
| Review | "Final review and approval" |
| Complete | "Work is finished" |

## Blocker Formatting

Present blockers in user-friendly format:

**Instead of:**
> `BLOCK-003: Iteration limit exceeded in qa-fixer at validation phase`

**Write:**
> "Quality checks found some issues that couldn't be automatically fixed. We need to review them together."

## Next Step Suggestions

Based on phase, suggest appropriate next action:

| Phase | Typical Next Step |
|-------|-------------------|
| Assess | "Review the proposed track and confirm it looks right" |
| Specify | "Review the specification draft for accuracy" |
| Clarify | "Answer the open questions to continue" |
| Plan | "Approve the implementation plan to proceed" |
| Tasks | "No action needed - tasks are being prepared" |
| Implement | "No action needed - code is being written" |
| Validate | "No action needed - running automated checks" |
| Review | "Approve to complete the workflow" |
| Complete | "Work is done! You can start a new request" |

## No Active Workflow

If no workflow is active:

```markdown
## Workflow Status

**No active workflow**

You can start a new workflow by:
- Describing what you want to build
- Asking a question about your project
- Requesting to work on a specific feature

Example: "I want to add a password reset feature"
```

## Error Handling

### Missing Context File

If `/.sigil/project-context.md` doesn't exist:
1. Report "No active workflow"
2. Suggest starting options
3. Don't create error state

### Corrupted Context

If context file has invalid format:
1. Report last known good state if available
2. Note: "Status may be outdated"
3. Suggest re-running the current phase

### Stale Context

If last update was more than 1 day ago:
1. Include warning: "Status may be outdated"
2. Suggest refreshing the context

## Human Tier

**Tier:** Auto

Status reports run automatically on request. No approval needed.

## Integration

### With Orchestrator

Orchestrator invokes status-reporter when:
- User asks for status
- Session starts (as part of context announcement)
- Workflow phase transitions

### With Context Management

This skill reads from but never writes to project context. Context updates are handled by individual agents per the [Context Management Protocol](/docs/dev/context-management.md).

## Notes

- Always use plain language — avoid technical terms
- Progress percentages are approximate guides, not precise measurements
- Focus on what the USER needs to do, not what the system is doing
- Keep it scannable — users should understand status in 10 seconds

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-02-19 | S3-100: Added user_track branching — non-technical uses plain English phase names and hides agent details, technical shows specialist names |
| 1.0.0 | 2026-01-20 | Initial release |
