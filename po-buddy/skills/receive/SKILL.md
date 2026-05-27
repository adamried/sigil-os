---
name: receive
description: Ingest a Validated Spec from PM Copilot output, Confluence, or local file. Validates the four-field handoff contract (Epic key, Confluence link, Target team, Context). Runs completeness check against the 10-section template.
version: 1.0.0
category: po
chainable: false
invokes: [scope-check]
invoked_by: [receive-command]
tools: Read, AskUserQuestion
---

# Skill: Receive

## Purpose

Ingest a Validated Spec and prepare it for decomposition. Enforce the cross-plugin handoff contract from PM Copilot's `/handoff` (FR-C05): Epic key, Confluence link, Target team, Context line all required.

## When to Invoke

- `/receive <source>` (PM Copilot output, Confluence link, Jira key, or local file)

## Inputs

Required (per FR-C09 handoff contract):

- `epic_key`: string or `(none)`
- `confluence_link`: URL or `(none)`
- `target_team`: string or `(default)`
- `context`: one-sentence summary

Plus:

- `spec_source`: path, URL, or paste-in content

## Process

### Step 1: Validate Contract Inputs

All four contract fields must be present. Missing fields are NOT silently defaulted — prompt the user.

```
The following are required to receive this spec:
  - Epic key: {missing | present: KEY-123}
  - Confluence link: {missing | present}
  - Target team: {missing | present}
  - Context: {missing | present}

Please provide missing fields, or re-run PM Copilot's `/handoff` to get them.
```

### Step 2: Load Spec Content

Resolve `spec_source`:

- **Paste-in content** — already loaded
- **Local file path** — read the file
- **Confluence URL** — Atlassian MCP `get_page` (if available)
- **Jira Epic key** — Atlassian MCP `get_epic` (if available)

If MCP isn't available for a remote source, surface the gap and offer local-paste fallback.

### Step 3: Completeness Check

Read `references/validated-spec-template.md`. Compare the received spec against the 10 sections:

| # | Section | Required for decompose? |
|---|---------|-------------------------|
| 1 | TL;DR | Yes |
| 2 | Problem | Yes |
| 3 | Success Metrics | Yes |
| 4 | Scope (with Cut Line) | Yes — Cut Line is critical |
| 5 | User Journeys | Yes |
| 6 | Scenarios & Business Rules | Yes |
| 7 | Dependencies | Yes (can be empty if truly none) |
| 8 | Design Context | Optional (warn if missing for UI features) |
| 9 | Assumptions | Optional |
| 10 | Open Questions | Optional |

For each missing required section, flag specifically.

### Step 4: Team Identification

If `references/team-scope.md` exists, run `scope-check` in routing mode to verify the target team matches the spec's domain. If mismatch:

```
The handoff says Target team: {team A}, but this spec's domain looks like
{team B}'s area.

Confirm:
  1. Keep target team as {team A} — they own this
  2. Re-route to {team B}
  3. Investigate cross-team coordination
```

For single-team projects, skip this step entirely.

### Step 5: Verdict

| Verdict | Trigger |
|---------|---------|
| **Accept** | All contract inputs present + all required sections present |
| **Accept with gaps** | Contract inputs present, but Sections 8/9/10 missing or weak (optional sections only) |
| **Reject** | Contract input missing OR any required section missing/empty |

## Outputs

```json
{
  "verdict": "Accept | Accept with gaps | Reject",
  "contract": {"epic_key": "...", "confluence_link": "...", "target_team": "...", "context": "..."},
  "completeness": [
    {"section": "...", "status": "Present | Missing | Weak"}
  ],
  "team_routing": {"target_team": "...", "mismatch": false},
  "next_step": "..."
}
```

## Anti-patterns

- **Silent contract default.** All four fields are explicit. No "(default)" without surfacing.
- **Auto-decomposing on Accept.** `/decompose` is a separate user-invoked step.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-27 | Initial release — S4-001 FR-C09 |
