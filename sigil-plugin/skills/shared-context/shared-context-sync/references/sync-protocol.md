# Shared Context Sync -- Protocol Reference

This file contains detailed protocol specifications extracted from the main SKILL.md. It covers cache management, offline queue, profiles, standards, scaffolding, discrepancy detection, and integration discovery.

---

## Local Cache Structure

The local cache mirrors the shared repo state and stores the offline queue.

**Directory layout:**

```
~/.sigil/
├── registry.json                    # Sentinel file
└── cache/
    └── shared/
        ├── last-sync.json           # Timestamp + hashes of last successful pull
        ├── learnings/               # Cached copy of shared learnings
        │   ├── web-app/
        │   │   ├── patterns.md
        │   │   ├── gotchas.md
        │   │   └── decisions.md
        │   └── api-server/
        │       └── ...
        ├── profiles/                # Cached sibling profiles (S2-102)
        │   └── api-server.yaml
        ├── standards/               # Cached shared standards
        │   ├── security-standards.md
        │   ├── accessibility.md
        │   └── coding-conventions.md
        ├── integrations/            # Cached integration adapter configs
        │   └── jira.yaml
        └── queue/                   # Pending offline writes
            └── 1707234600000.json
```

### `last-sync.json` Schema

Tracks when the last successful pull occurred and content hashes for "what's new" detection.

```json
{
  "last_pull": "2026-02-09T14:30:00Z",
  "content_hashes": {
    "learnings/web-app/patterns.md": "sha256:abc123...",
    "learnings/web-app/gotchas.md": "sha256:def456...",
    "learnings/api-server/patterns.md": "sha256:789ghi..."
  },
  "standards_hashes": {
    "shared-standards/security-standards.md": "sha256:jkl012...",
    "shared-standards/accessibility.md": "sha256:mno345..."
  },
  "integrations_hashes": {
    "integrations/jira.yaml": "sha256:pqr678..."
  }
}
```

### Cache Initialization

When shared context activates for the first time (no cache directory exists):

1. Create `~/.sigil/cache/shared/` directory tree
2. Create empty `last-sync.json` with `{ "last_pull": null, "content_hashes": {}, "standards_hashes": {}, "integrations_hashes": {} }`
3. Create empty `learnings/`, `profiles/`, `standards/`, `integrations/`, and `queue/` directories

---

## Offline Queue

When an MCP write fails, persist the operation for later retry.

### Queue Item Schema

File: `~/.sigil/cache/shared/queue/{timestamp_ms}.json`

```json
{
  "operation": "append",
  "target": "learnings/web-app/patterns.md",
  "content": "## [2026-02-09] Use AbortController for fetch cancellation\n- **Contributor:** adam@example.com\n- **Context:** When making API calls that may be cancelled\n- **Solution:** Wrap fetch in AbortController, abort in cleanup\n- **Tags:** react, api, performance\n",
  "queued_at": "2026-02-09T14:30:00Z",
  "attempts": 0,
  "last_attempt": null,
  "error": null
}
```

### Queue Operations

**Enqueue (on MCP write failure):**

1. Create queue item JSON with `attempts: 0`
2. Use current timestamp in milliseconds as filename
3. Write to `~/.sigil/cache/shared/queue/`

**Drain (at session start or next successful MCP write):**

1. List all `.json` files in `~/.sigil/cache/shared/queue/`
2. Sort by filename (chronological order)
3. For each item:
   a. Read queue item JSON to get `target` path and `content`
   b. Determine shared repo from sentinel
   c. Attempt MCP write:
      ```
      mcp__github__get_file_contents(owner, repo, path=item.target)
      ```
      Then append content and write:
      ```
      mcp__github__create_or_update_file(
        owner, repo, path=item.target,
        content=existing + item.content,
        message="learning: sync queued entry",
        branch="main", sha=existing_sha
      )
      ```
   d. On success: delete the queue file, update local cache
   e. On failure: increment `attempts`, update `last_attempt` and `error`
   f. If `attempts >= 3`: log permanent failure, move to `~/.sigil/cache/shared/queue/failed/`
4. Report: "Synced X queued learnings. Y failed (see ~/.sigil/cache/shared/queue/failed/)."

**Queue Status:**

Return count of pending and failed items for display in `/sigil-learn` and `/sigil` status.

---

## Duplicate Detection (Rule-Based V1)

Before appending a learning to the shared repo (step 7 of Push Protocol), check for duplicates.

**Procedure:**

1. Parse existing entries from the target file (each `## [date] Title` block is one entry)
2. Extract keywords from the new entry's title and solution text
3. For each existing entry in the same category file:
   a. **Title similarity:** Compare normalized titles (lowercase, stripped of dates). If >70% word overlap -> potential duplicate
   b. **Tag overlap:** If both entries have tags, check for >=50% tag overlap
   c. **Recency:** If a potential duplicate was added within the last 7 days -> strong duplicate signal
4. If all three signals match -> **flag as duplicate**, skip the push
5. If only title matches but tags/recency differ -> **allow** (may be a refinement)

**On duplicate detected:**

- Do NOT push to shared repo
- Do NOT queue locally
- Log: "Duplicate learning detected -- skipping shared sync. Run `/sigil-learn --review` to manage."
- Still write locally (local capture is unaffected)

**Limitations (V1):**

- Keyword-based only, no semantic matching
- May miss paraphrased duplicates
- Errs on the side of allowing writes (better to have near-duplicates than miss entries)

---

## Profile Protocol

### Profile Push

Called by `profile-generator` after writing or updating `.sigil/project-profile.yaml`.

**Inputs:**
- `repo_name`: Current project's repo name (from identity detection)

**Procedure:**

1. Check sentinel -> if not active, return silently
2. Determine shared repo from sentinel lookup (e.g., `araserel/platform-context`)
3. Split shared repo into `owner` and `repo` parts
4. Determine target file path: `profiles/{repo_name}.yaml`
5. Read local `.sigil/project-profile.yaml`
6. **Read existing file via MCP:**
   ```
   mcp__github__get_file_contents(owner, repo, path="profiles/{repo_name}.yaml")
   ```
   - If file exists: extract SHA from response
   - If file doesn't exist (404): SHA is null (new file)
7. **Write profile via MCP:**
   ```
   mcp__github__create_or_update_file(
     owner, repo,
     path="profiles/{repo_name}.yaml",
     content=local_profile_content,
     message="profile: update {repo_name} project profile",
     branch="main",
     sha=existing_file_sha  # Required for updates, omit for new files
   )
   ```
   - **SHA safety:** Always pass the SHA from step 6 when updating. If SHA mismatch occurs (concurrent write), re-read the file and retry once.
8. On success: update local hash cache at `~/.sigil/cache/shared/profile-hashes.json`
9. On failure: enqueue to offline queue with `operation: "overwrite"` and `target: "profiles/{repo_name}.yaml"`

**Graceful failure:** If any MCP call fails, log a warning ("Profile sync unavailable, profile saved locally") and enqueue to the offline queue. Never block the user's workflow on sync failure.

### Profile Pull

Called by `prime` at session start (as part of pull protocol).

**Procedure:**

1. Check sentinel -> if not active, return silently
2. Determine shared repo from sentinel lookup
3. Split shared repo into `owner` and `repo` parts
4. **Read profiles directory via MCP:**
   ```
   mcp__github__get_file_contents(owner, repo, path="profiles/")
   ```
   This returns an array of directory entries. For each `.yaml` file:
   ```
   mcp__github__get_file_contents(owner, repo, path="profiles/{filename}")
   ```
5. For each profile file found:
   a. Compare SHA from response with cached SHA in `~/.sigil/cache/shared/profile-hashes.json`
   b. If changed: decode content (base64) and update local cache at `~/.sigil/cache/shared/profiles/{filename}`
   c. If unchanged: skip (cache is current)
6. Update `~/.sigil/cache/shared/profile-hashes.json` with new SHAs
7. Return sibling profile list (excluding current project's profile)

**On MCP failure during pull:**

1. Log warning: "Profile sync unavailable, using cached profiles."
2. Return cached profiles from `~/.sigil/cache/shared/profiles/`
3. Continue session normally -- MCP failure must never block session start

### Profile Change Detection

Called by `prime` to determine if the local profile needs republishing.

**Procedure:**

1. Read `.sigil/project-profile.yaml` -- if missing, return (no profile to sync)
2. Compute SHA256 hash of file contents
3. Read `~/.sigil/cache/shared/profile-hashes.json`
4. Compare local hash with cached `local_hash` entry
5. If different -> trigger Profile Push, then update `local_hash` in cache
6. If same -> skip (no changes since last sync)

**Cache schema (`~/.sigil/cache/shared/profile-hashes.json`):**

```json
{
  "local_hash": "sha256:abc123...",
  "remote_profiles": {
    "api-server.yaml": "github_sha_from_api",
    "web-app.yaml": "github_sha_from_api"
  }
}
```

---

## Standards Pull Protocol

Called by `/sigil` at session start and by `constitution-writer` during setup.

**Procedure:**

1. Check sentinel -> if not active, return silently
2. Determine shared repo from sentinel lookup (e.g., `araserel/platform-context`)
3. Split shared repo into `owner` and `repo` parts
4. **Read shared-standards directory via MCP:**
   ```
   mcp__github__get_file_contents(owner, repo, path="shared-standards/")
   ```
   This returns an array of directory entries. For each `.md` file (excluding `.gitkeep`):
   ```
   mcp__github__get_file_contents(owner, repo, path="shared-standards/{filename}")
   ```
5. For each file found:
   a. Compare SHA from response with cached SHA in `~/.sigil/cache/shared/last-sync.json` under `standards_hashes`
   b. If changed: decode content (base64) and update local cache at `~/.sigil/cache/shared/standards/{filename}`
   c. If unchanged: skip (cache is current)
   d. **Parse enforcement level from YAML frontmatter:** If the file begins with `---`, extract the `enforcement` field from the YAML block. Valid values: `required`, `recommended`, `informational`. If absent, malformed, or not one of the valid values, default to `recommended`.
6. Update `~/.sigil/cache/shared/last-sync.json` with new SHAs under `standards_hashes`
7. Return list of standard files with their content and parsed `enforcement` level

**On MCP failure during pull:**

1. Log warning: "Shared standards unavailable, using cached data."
2. Read cached standards from `~/.sigil/cache/shared/standards/`
3. Return cached content
4. Continue normally -- MCP failure must never block session start

---

## Standards Expand Protocol

Called after Standards Pull to process `@inherit` markers in `constitution.md`.

**Procedure:**

1. Read `/.sigil/constitution.md`
2. Find all `<!-- @inherit: shared-standards/{filename} -->` lines
3. For each marker:
   a. Look up `{filename}` in the pulled/cached standards
   b. **If `@inherit-start`/`@inherit-end` block already exists** below the marker:
      - Replace content between `<!-- @inherit-start: shared-standards/{filename} -->` and `<!-- @inherit-end: shared-standards/{filename} -->` with fresh standard content
   c. **If no block exists yet:**
      - Insert immediately after the `@inherit` line:
        ```
        <!-- @inherit-start: shared-standards/{filename} -->
        [content from shared standard -- auto-managed by Sigil, do not edit between these markers]
        <!-- @inherit-end: shared-standards/{filename} -->
        ```
   d. **If referenced standard is not available** (not in pulled or cached data):
      - If prior expansion exists: leave it unchanged
      - If no prior expansion exists: insert `<!-- @inherit-pending: {filename} -->` after the marker
4. Preserve all content outside the `@inherit-start`/`@inherit-end` blocks -- headings, `### Local Additions` sections, and any other user content are never modified
5. Write updated constitution back to `/.sigil/constitution.md`
6. Return list of expanded markers and their status

**Marker format example:**

```markdown
## Article 4: Security Mandates

<!-- @inherit: shared-standards/security-standards.md -->
<!-- @inherit-start: shared-standards/security-standards.md -->
[content from shared standard -- auto-managed by Sigil, do not edit between these markers]
<!-- @inherit-end: shared-standards/security-standards.md -->

### Local Additions
- Rate limit all public endpoints to 100 req/min
```

On re-expansion, content between `@inherit-start` and `@inherit-end` is replaced with fresh content. The `@inherit` directive line is always preserved. Local Additions sections below the end marker are never touched.

---

## Standards Discover Protocol

Called by `connect-wizard` and `constitution-writer` to list available standards.

**Procedure:**

1. Read `shared-standards/` directory via MCP (or from cache if MCP unavailable)
2. For each `.md` file (excluding `.gitkeep`):
   a. Extract title (first `# ` heading) and first paragraph
   b. **Parse enforcement level from YAML frontmatter:** If the file begins with `---`, extract the `enforcement` field. Valid values: `required`, `recommended`, `informational`. Default to `recommended` if absent or invalid.
   c. Infer `article_mapping` from filename:

   | Filename | Suggested Article |
   |----------|-------------------|
   | `security-standards.md` | Article 4: Security Mandates |
   | `accessibility.md` | Article 7: Accessibility Standards |
   | `coding-conventions.md` | Article 2: Code Standards |
   | `testing-standards.md` | Article 3: Testing Requirements |
   | Other filenames | `null` (user chooses placement) |

3. Return array of discovered standards:

```json
[
  {
    "filename": "security-standards.md",
    "title": "Security Standards",
    "summary": "First paragraph of the file...",
    "article_mapping": "Article 4: Security Mandates",
    "enforcement": "required",
    "content": "Full file content..."
  }
]
```

**On MCP failure:** Return cached standards from `~/.sigil/cache/shared/standards/` with the same format, or empty array if no cache exists.

---

## Discrepancy Detection

Runs after Standards Expand to flag conflicts between inherited and local content. Uses enforcement levels to determine severity and blocking behavior.

**Procedure:**

1. **Missing required standard check:** Before comparing content, verify that every standard with `enforcement: required` has a corresponding `@inherit` marker in the constitution. For each required standard:
   - Look up its `article_mapping`
   - Check if the constitution contains `<!-- @inherit: shared-standards/{filename} -->` for that standard
   - If missing -> add a hard-block discrepancy (the project cannot proceed without adopting this standard)

2. For each article in the constitution that has both an expanded `@inherit` block AND local content (content outside the `@inherit-start`/`@inherit-end` markers but still within the same article):
   a. **Numeric threshold comparison:** Extract numeric values (e.g., coverage percentages, line limits, rate limits) from both inherited and local content. If local content specifies a weaker threshold than the inherited standard, flag it.
   b. **Required/optional flag comparison:** If the inherited standard marks something as "required" or "must" and local content marks the same item as "optional" or "should," flag it.
   c. **Contradictory rules:** If local content explicitly contradicts an inherited rule (e.g., inherited says "all endpoints authenticated," local says "public endpoints allowed"), flag it.

3. **Apply enforcement-level severity** to each discrepancy based on the standard's enforcement level:

   | Enforcement | Severity | Blocking | Behavior |
   |-------------|----------|----------|----------|
   | `required` | hard block | `true` | Must be resolved before proceeding. No skip option. |
   | `recommended` | warning | `false` | Show warning with options: update / waive / skip this session. |
   | `informational` | info | `false` | Silent -- do not display to user. Log for audit only. |

4. Return list of discrepancies:

```json
[
  {
    "article": "Article 4: Security Mandates",
    "type": "missing_required_standard",
    "enforcement": "required",
    "severity": "hard_block",
    "blocking": true,
    "inherited": "security-standards.md",
    "local": null,
    "suggestion": "This standard is required by your organization. Apply it now or request a waiver from your team lead."
  },
  {
    "article": "Article 3: Testing Requirements",
    "type": "weaker_threshold",
    "enforcement": "recommended",
    "severity": "warning",
    "blocking": false,
    "inherited": "Minimum 80% test coverage",
    "local": "60% coverage target",
    "suggestion": "Update local target to match shared standard (80%) or document a waiver"
  }
]
```

5. If no discrepancies found, return empty array

**Display format for user:**

For **required** (hard block) discrepancies:
```
Required Standard Missing

Article 4: Security Mandates (required)
  Your organization requires this standard but it is
  not applied to your project constitution.

  Standard: security-standards.md

Options:
  1. Apply now -- add @inherit marker and expand
  2. Request waiver -- log exception for team review
```

For **recommended** (warning) discrepancies:
```
Standards Discrepancy Detected

Article 3: Testing Requirements (recommended)
  Shared standard requires: 80% test coverage
  Your local rule says: 60% coverage target

Options:
  1. Update local rule to match shared standard
  2. Keep local rule and log a waiver
  3. Skip for now
```

**Informational** discrepancies are not displayed.

---

## Scaffolding Protocol

Called by `connect-wizard` when a shared repo is empty or missing the expected structure.

**Procedure:**

1. Check repo contents via MCP:
   ```
   mcp__github__get_file_contents(owner, repo, path="/")
   ```
2. If repo only has README.md or is empty, scaffold using a single commit:
   ```
   mcp__github__push_files(
     owner, repo, branch="main",
     message="chore: initialize shared context structure",
     files=[
       { path: "README.md", content: <README content from connect-wizard> },
       { path: "shared-standards/.gitkeep", content: "" },
       { path: "profiles/.gitkeep", content: "" },
       { path: "learnings/.gitkeep", content: "" }
     ]
   )
   ```
3. On success: return `{ scaffolded: true }`
4. On failure: return error with message for connect-wizard to display

---

## Integration Discovery Protocol

Called by `connect-wizard` Step 8 and `sigil-setup` Step 3.5 to discover org-level integration adapter configs from the shared repo.

**Procedure:**

1. Check sentinel -> if not active, return `{ integrations: [] }`
2. Determine shared repo from sentinel lookup
3. Split shared repo into `owner` and `repo` parts
4. **Read integrations directory via MCP:**
   ```
   mcp__github__get_file_contents(owner, repo, path="integrations/")
   ```
   - If 404 (directory doesn't exist) -> return `{ integrations: [] }`
   - If returns directory listing -> proceed
5. For each `.yaml` file in the directory:
   ```
   mcp__github__get_file_contents(owner, repo, path="integrations/{filename}")
   ```
6. Parse each adapter config. Expected schema:
   ```yaml
   adapter: jira          # adapter identifier
   name: Jira             # display name
   mcp_tools:             # required MCP tools
     - mcp__claude_ai_Atlassian__getJiraIssue
     - mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql
   config:                # org-level default configuration
     project_keys: [PROJ, TEAM]
     category_mapping:      # issue type -> Sigil category
       bug: [Bug, Defect]
       feature: [Story, Feature]
       enhancement: [Task, Improvement]
       maintenance: [Chore, "Tech Debt"]
     label_overrides:        # label -> category (overrides type mapping)
       maintenance: [tech-debt, refactor, cleanup]
     status_mapping:
       done: ["Done", "Closed"]
       in_progress: ["In Progress", "In Review"]
   ```
7. For each adapter, cache locally at `~/.sigil/cache/shared/integrations/{filename}`
8. Update `~/.sigil/cache/shared/last-sync.json` with SHAs under `integrations_hashes`
9. Return array of discovered integrations:
   ```json
   [
     {
       "adapter": "jira",
       "name": "Jira",
       "filename": "jira.yaml",
       "mcp_tools": ["mcp__claude_ai_Atlassian__getJiraIssue", "..."],
       "config": { "project_keys": ["PROJ", "TEAM"] }
     }
   ]
   ```

**On MCP failure:** Return cached integrations from `~/.sigil/cache/shared/integrations/` or empty array if no cache exists.

---

## Integration Pull Protocol

Called at session start (alongside Standards Pull) to refresh cached adapter configs.

**Procedure:**

1. Check sentinel -> if not active, return silently
2. Determine shared repo from sentinel lookup
3. Split shared repo into `owner` and `repo` parts
4. **Read integrations directory via MCP:**
   ```
   mcp__github__get_file_contents(owner, repo, path="integrations/")
   ```
5. For each `.yaml` file found:
   a. Compare SHA from response with cached SHA in `~/.sigil/cache/shared/last-sync.json` under `integrations_hashes`
   b. If changed: decode content (base64) and update local cache at `~/.sigil/cache/shared/integrations/{filename}`
   c. If unchanged: skip (cache is current)
6. Update `~/.sigil/cache/shared/last-sync.json` with new SHAs under `integrations_hashes`
7. Return list of available integrations

**On MCP failure during pull:**

1. Log warning: "Integration configs unavailable, using cached data."
2. Return cached integrations from `~/.sigil/cache/shared/integrations/`
3. Continue session normally -- MCP failure must never block session start
