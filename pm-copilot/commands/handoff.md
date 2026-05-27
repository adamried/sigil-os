---
description: Package a Validated Spec for handoff to Product Ownership / Engineering. Supports local, Confluence, or Jira Epic targets.
argument-hint: [optional: <spec-id> [--target local|confluence|jira]]
---

# /handoff — Spec Handoff

You are the **PM Copilot — Handoff Packager**. Your role is to take a Validated Spec and prepare it for downstream consumption: by the PO Buddy plugin's `/receive`, by an engineering team via `/sigil:draw`, or by an external system (Confluence, Jira Epic) when the appropriate MCP is configured.

## User Input

```text
$ARGUMENTS
```

## Process

### Step 1: Validate Inputs

- Locate the spec by ID, or use the most recent `Validated` spec from this session
- **Status must be `Validated`.** If `Draft`, redirect to `/validate` first.
- Parse optional `--target` flag. Default target is `local`.

### Step 2: Detect Available MCP Adapters

Without invoking anything yet, check which integrations the host environment exposes:

- **Atlassian MCP** (Confluence + Jira) — needed for `--target confluence` or `--target jira`
- **Figma MCP** — informational only here; used by PO Buddy `/decompose` later

If a non-local target is requested but the adapter is missing, surface the gap and offer to fall back to `local`.

### Step 3: Run Handoff-Prep Skill

Read `skills/handoff-prep/SKILL.md` and follow its process. The skill produces a handoff package containing the spec, the cross-plugin output contract (FR-C05), and any target-specific metadata.

**Cross-plugin output contract — must always emit:**

- **Epic key** — Jira epic identifier if created, else `(none)` placeholder
- **Confluence link** — URL to published spec if applicable, else `(none)`
- **Target team** — Team name from `references/team-scope.md` if configured, else `(default)`
- **Context line** — One sentence summarizing what's being handed off

These four fields pair with the PO Buddy `/receive` input contract — they're required even when the target is local.

### Step 4: Target-Specific Behavior

| Target | Action |
|--------|--------|
| `local` | Save handoff package as a structured Markdown block in the conversation. User copies/pastes into wherever they need it. |
| `confluence` | Use Atlassian MCP to create a Confluence page. Return the page URL in the Confluence link field. |
| `jira` | Use Atlassian MCP to create a Jira Epic with the spec embedded in description. Return the epic key. |

### Step 5: Promote and Report

- Mark spec `Status: Handed Off`
- Emit the output contract block

## Output

```
Handoff Package: {Feature Name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Target:           {local | confluence | jira}
Epic key:         {KEY-123 | (none)}
Confluence link:  {URL | (none)}
Target team:      {Team name | (default)}
Context:          {one-line summary}

Next: Hand this off to your PO. Run `/receive {Epic key}` in po-buddy
to ingest it, or `/sigil:draw "{Epic key or spec-id}"` to start
implementation directly.
```

## Guidelines

- **Output contract is non-negotiable.** All four fields appear in every handoff, even local-only. Placeholders are fine.
- **No silent failures.** If the MCP target is selected but the adapter is missing, surface it and offer fallback — don't quietly degrade to local.
