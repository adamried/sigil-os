# Tasks: [FEATURE NAME]

> **Spec:** [/.sigil/specs/###-feature/spec.md]
> **Plan:** [/.sigil/specs/###-feature/plan.md]
> **Created:** [DATE]
> **Status:** [Draft | Active | Complete]

---

## Task Legend

| Symbol | Meaning |
|--------|---------|
| `[ ]` | Not started |
| `[~]` | In progress |
| `[x]` | Complete |
| `[!]` | Blocked |
| `[P]` | Parallelizable with other [P] tasks in same phase |
| `[B]` | Blocking — must complete before next phase |

---

## Summary

| Metric | Count |
|--------|-------|
| Total Tasks | [N] |
| Completed | [N] |
| In Progress | [N] |
| Blocked | [N] |
| Remaining | [N] |

---

## Feature-Level Status

Tracks gates that apply to the feature as a whole, not to individual tasks. The orchestrator updates this table at each phase transition.

| Gate | Status | Notes |
|------|--------|-------|
| QA validation | [ ] Not started / [~] In progress / [x] Pass / [!] Failing | [Latest QA report path or attempt N/5] |
| Code review | [ ] Not started / [~] In progress / [x] Approved / [!] Changes requested | [Path to code-review report] |
| Security review | [ ] Not started / [~] In progress / [x] Pass / [!] Findings outstanding / [—] N/A (Quick Flow) | [Path to `.sigil/specs/<feature>/security.md`] |
| Verification commit | [ ] Not yet / [x] Committed `<short-sha>` / [—] N/A (Quick Flow) | `verified: <feature> security pass` |

**Notes:**
- Quick Flow features skip Security review and Verification commit. Mark both as `[—] N/A (Quick Flow)`.
- Verification commit is only emitted after Security review passes. If security fails, leave the verification gate unchecked.
- This table is feature-level. Per-task status remains in the Task Legend below.

---

## Phase 1: Setup

<!-- Infrastructure, configuration, and scaffolding -->

- [ ] **T001** [B] [Description of setup task]
  - Files: `[paths to files]`
  - Acceptance: [How to verify complete]

- [ ] **T002** [P] [Description of parallelizable setup task]
  - Files: `[paths to files]`
  - Acceptance: [How to verify complete]

**Phase 1 Exit Criteria:**
- [ ] All setup tasks complete
- [ ] Project builds without errors
- [ ] Development environment verified

---

## Phase 2: Foundation

<!-- Core infrastructure that other phases depend on -->

- [ ] **T003** [B] [Description of foundational task]
  - Files: `[paths to files]`
  - Depends on: T001
  - Acceptance: [How to verify complete]

- [ ] **T004** [B] [Description of foundational task]
  - Files: `[paths to files]`
  - Depends on: T001
  - Acceptance: [How to verify complete]

**Phase 2 Exit Criteria:**
- [ ] Foundation code complete
- [ ] Unit tests passing
- [ ] No lint errors

---

## Phase 3: [User Story/Feature Area]

<!-- Group tasks by user story or feature area -->

### US-001: [User Story Title]

**Tests (write first, must fail initially):**
- [ ] **T005** [P] Write unit tests for [component]
  - Files: `[test file paths]`
  - Tests: [List of test cases]

**Implementation:**
- [ ] **T006** [P] Implement [component]
  - Files: `[implementation file paths]`
  - Depends on: T005 (tests exist)
  - Acceptance: T005 tests pass

- [ ] **T007** [P] Implement [related component]
  - Files: `[implementation file paths]`
  - Depends on: T003, T004
  - Acceptance: [How to verify]

### US-002: [User Story Title]

**Tests:**
- [ ] **T008** Write integration tests for [flow]
  - Files: `[test file paths]`
  - Tests: [List of test cases]

**Implementation:**
- [ ] **T009** Implement [component]
  - Files: `[implementation file paths]`
  - Depends on: T006, T008
  - Acceptance: T008 tests pass

---

## Phase 4: Integration

<!-- Connecting components, API wiring, etc. -->

- [ ] **T010** [B] Wire [component] to [component]
  - Files: `[paths to files]`
  - Depends on: T006, T009
  - Acceptance: [Integration test or verification]

- [ ] **T011** [P] Add error handling for [area]
  - Files: `[paths to files]`
  - Acceptance: [Error scenarios handled]

---

## Phase 5: Accessibility & Polish

<!-- WCAG compliance, UX refinements -->

- [ ] **T012** [P] Add keyboard navigation to [component]
  - Files: `[paths to files]`
  - Acceptance: Full keyboard access verified

- [ ] **T013** [P] Add ARIA labels to [component]
  - Files: `[paths to files]`
  - Acceptance: Screen reader tested

- [ ] **T014** [P] Verify color contrast compliance
  - Files: `[paths to files]`
  - Acceptance: WCAG 2.1 AA contrast ratios met

---

## Phase 6: Testing & Validation

<!-- Final quality assurance -->

- [ ] **T015** Run full test suite
  - Acceptance: All tests pass

- [ ] **T016** Run accessibility audit
  - Tool: [axe/WAVE/manual]
  - Acceptance: No critical issues

- [ ] **T017** Manual testing of critical paths
  - Scenarios: [List critical user flows]
  - Acceptance: All scenarios pass

---

## Dependencies Map

```
T001 ─────┬────► T003 ────► T006 ────► T010
          │                   │
          └────► T004 ────► T007 ────┘
                              │
T002 ─────────────────────────┴────► T009
```

---

## Parallel Opportunities

Tasks that can be worked on simultaneously:

| Group | Tasks | Requires |
|-------|-------|----------|
| Setup | T001, T002 | Nothing |
| Foundation | T003, T004 | T001 |
| US-001 Implementation | T006, T007 | T003, T004, T005 |
| Accessibility | T012, T013, T014 | Phase 4 complete |

---

## Blockers Log

| Task | Blocker | Identified | Resolved | Resolution |
|------|---------|------------|----------|------------|
| [Task ID] | [What's blocking] | [Date] | [Date or Pending] | [How resolved] |

---

## Notes

### Implementation Notes
<!-- Discoveries, gotchas, tips for future reference -->

- [Note about implementation detail]

### Deferred Items
<!-- Items discovered during implementation to address later -->

- [Item to address in future iteration]

---

## Completion Checklist

- [ ] All tasks marked complete
- [ ] All tests passing
- [ ] No lint/type errors
- [ ] Accessibility requirements met
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Ready for QA validation
