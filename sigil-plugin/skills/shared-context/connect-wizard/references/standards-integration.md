# Connect Wizard: Standards Integration

> **Referenced by:** `connect-wizard` SKILL.md — protocol for applying shared team standards to constitutions.

## Purpose

Define how shared team standards from a shared context repository are applied to project constitutions during the `/sigil-connect` setup flow.

## Enforcement Levels

Each shared standard file has an `enforcement` field in its YAML frontmatter:

| Level | Behavior | User Choice |
|-------|----------|-------------|
| `required` | Must be applied — blocks workflow if missing | Auto-apply; no opt-out |
| `recommended` | Should be applied — warns if missing | Prompt user; default yes |
| `informational` | Available for reference — no enforcement | Mention; user can opt-in |

Default enforcement level (if frontmatter is absent): `recommended`

## Integration Discovery Protocol

When connecting to a shared context repo:

1. **Fetch standards directory** — Read `shared-standards/` from the shared repo via GitHub MCP
2. **Parse each standard file:**
   - Extract `enforcement` level from frontmatter
   - Extract `article` mapping (which constitution article this standard maps to)
   - Extract `description` for display
3. **Group by enforcement level** for presentation

## Standards Application Flow

### Step 1: Present Discovered Standards

```markdown
Found shared standards from your team:

Required (automatically applied):
  ✅ Security Mandates — Maps to Article 4

Recommended (applied by default — you can skip):
  📋 Testing Requirements — Maps to Article 3
  📋 Code Style Guide — Maps to Article 2

Informational (available if you want them):
  ℹ️  Architecture Patterns — Maps to Article 5
  ℹ️  Performance Guidelines — No article mapping
```

### Step 2: Apply Standards

For each standard, based on enforcement level:

**Required:**
- Auto-add `@inherit` marker to the corresponding constitution article
- No user prompt — this is mandatory
- If constitution doesn't have the corresponding article, add it

**Recommended:**
- Ask user: "Apply [standard name]? (Y/n)"
- Default to yes
- If user accepts, add `@inherit` marker
- If user skips, log skip reason (optional)

**Informational:**
- Mention availability: "Your team also has guidelines for [topic]. Want to include them?"
- Default to no — only add if user explicitly opts in
- If user declines, no further action

### Step 3: Conflict Detection

After applying standards, check for conflicts:

| Conflict Type | Resolution |
|--------------|-----------|
| Standard and local article have overlapping content (>70% similarity) | Merge — keep local additions after inherited content |
| Standard contradicts local article | Present both, ask user which to keep |
| Standard maps to an article that doesn't exist locally | Create the article with inherited content |
| Multiple standards map to the same article | Apply in order, concatenate with section breaks |

## Integration Discovery for Tool Adapters

When connecting, also check for integration configurations:

1. **Fetch integrations directory** — Read `integrations/` from shared repo
2. **For each adapter config found:**
   - Check if the required MCP server is available (e.g., Atlassian MCP for Jira)
   - If MCP available: offer to import org defaults to `.sigil/config.yaml`
   - If MCP unavailable: note the integration exists but can't be configured yet
3. **Present discovered integrations:**

```markdown
Integrations available from your team:

  ✅ Jira — Atlassian MCP detected, org defaults available
  ⚠️ Slack — Slack MCP not configured (skip for now)
  ✅ Context7 — Available for documentation lookups
```

## Post-Connection Verification

After standards and integrations are applied:

1. **Run Standards Expand** — Process all `@inherit` markers in constitution
2. **Run Discrepancy Detection** — Check for conflicts between inherited and local content
3. **Present summary:**

```markdown
Connection complete!

Standards applied:
  ✅ Security Mandates (required) → Article 4
  ✅ Testing Requirements (recommended) → Article 3
  ⏭️  Architecture Patterns (informational) — skipped

Integrations configured:
  ✅ Jira — org defaults imported

Next: Run /sigil to start building with your team's standards.
```

## Creating New Shared Standards

To add a new standard to a shared context repo, use `templates/shared-standard-template.md` as the starting point. The template includes:
- **YAML frontmatter** with `enforcement`, `article`, `description`, `version`, `maintained_by`, and `last_updated` fields — required by the Standards Discover Protocol
- **Section structure** for purpose, scope, rules, exceptions, a constitution article snippet, and a verification checklist

Commit the completed file to `shared-standards/{standard-name}.md` in the shared repo. It will be discovered automatically on the next `/sigil-connect` or session start.

## Error Handling

| Error | Resolution |
|-------|-----------|
| MCP unavailable | Queue standards for offline application; add to sync queue |
| Standard file parse error | Skip that standard, warn user, continue with others |
| Article mapping invalid | Skip mapping, apply standard as standalone reference |
| Constitution doesn't exist | Run constitution-writer first with standards pre-loaded |
