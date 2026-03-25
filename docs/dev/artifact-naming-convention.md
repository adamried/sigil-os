# Artifact Naming Convention

> Standard names and locations for all skill-generated artifacts.

---

## Naming Rules

1. **Kebab-case** for all filenames: `code-review.md`, not `codeReview.md`
2. **Descriptive nouns**, not verb phrases: `plan.md`, not `create-plan.md`
3. **Per-task artifacts** use the pattern `task-{id}-{type}.md`: `task-T001-validation.md`
4. **Versioned artifacts** use iteration suffixes: `task-T001-fix-1.md`, `task-T001-fix-2.md`
5. **ADRs** use the pattern `ADR-###-{slug}.md`: `ADR-001-database-choice.md`

---

## Artifact Catalog

### Project Root (`/.sigil/`)

| Artifact | Skill | Created When |
|----------|-------|-------------|
| `constitution.md` | constitution-writer | Project setup |
| `project-context.md` | (auto-updated) | Session start, phase changes |
| `project-foundation.md` | foundation-writer | Discovery track |
| `project-profile.yaml` | profile-generator | `/sigil:profile` |
| `config.yaml` | `/sigil:setup` | Project setup (gitignored) |
| `tech-debt.md` | code-reviewer | After code review (suggestions) |
| `waivers.md` | (manual) | Constitution waivers |

### Feature Specs (`/.sigil/specs/###-feature/`)

| Artifact | Skill | Created When |
|----------|-------|-------------|
| `spec.md` | spec-writer | Specify phase |
| `clarifications.md` | clarifier | Clarify phase (gitignored) |
| `plan.md` | technical-planner | Plan phase |
| `research.md` | researcher | Plan phase (if research needed) |
| `data-model.md` | technical-planner | Plan phase (if data changes) |
| `tasks.md` | task-decomposer | Tasks phase |
| `technical-review-package.md` | handoff-packager | Handoff (Option A) |
| `stories.md` | story-preparer | Handoff (Option B) |
| `stories-jira.json` | story-preparer | Jira export (Option B) |
| `stories.csv` | story-preparer | CSV export (Option B) |

### QA Reports (`/.sigil/specs/###-feature/qa/`)

| Artifact | Skill | Created When |
|----------|-------|-------------|
| `task-{id}-validation.md` | qa-validator | Per-task validation |
| `task-{id}-fix-{N}.md` | qa-fixer | Fix attempt reports |

### Review Reports (`/.sigil/specs/###-feature/reviews/`)

| Artifact | Skill | Created When |
|----------|-------|-------------|
| `code-review.md` | code-reviewer | Review phase |
| `security-review.md` | security-reviewer | Review phase |
| `deploy-readiness.md` | deploy-checker | Review phase |

### ADRs (`/.sigil/specs/###-feature/adr/`)

| Artifact | Skill | Created When |
|----------|-------|-------------|
| `ADR-###-{slug}.md` | adr-writer | Plan phase (significant decisions) |

### Learnings (`/.sigil/learnings/`)

| Artifact | Skill | Location |
|----------|-------|----------|
| `patterns.md` | learning-capture | `active/` |
| `gotchas.md` | learning-capture | `active/` |
| `decisions.md` | learning-capture | `active/` |
| `{feature-id}.md` | learning-capture | `active/features/` |

### Quick Flow (`/.sigil/specs/stories/`)

| Artifact | Skill | Created When |
|----------|-------|-------------|
| Quick spec file | quick-spec | Quick Flow track |

---

## Directory Structure

```
/.sigil/
├── constitution.md
├── project-context.md
├── project-foundation.md
├── project-profile.yaml
├── config.yaml                    (gitignored)
├── tech-debt.md
├── waivers.md
├── learnings/
│   ├── active/
│   │   ├── patterns.md
│   │   ├── gotchas.md
│   │   ├── decisions.md
│   │   └── features/
│   │       └── {feature-id}.md
│   └── archive/
└── specs/
    ├── stories/                   (Quick Flow specs)
    └── ###-feature/
        ├── spec.md
        ├── clarifications.md      (gitignored)
        ├── plan.md
        ├── research.md            (if needed)
        ├── data-model.md          (if needed)
        ├── tasks.md
        ├── technical-review-package.md  (if handoff Option A)
        ├── stories.md             (if handoff Option B)
        ├── qa/
        │   ├── task-T001-validation.md
        │   └── task-T001-fix-1.md
        ├── reviews/
        │   ├── code-review.md
        │   ├── security-review.md
        │   └── deploy-readiness.md
        └── adr/
            └── ADR-001-{slug}.md
```

---

## Related Documents

- [Workflow Diagrams — File Output Summary](workflow-diagrams.md#12-file-output-summary-by-workflow)
- [Extending Skills](extending-skills.md) — How to define outputs for new skills
