# Project Foundation: [PROJECT NAME]

> One-time decisions made during project discovery. This document captures the foundational choices that inform the constitution and all subsequent development.
>
> **Created:** [DATE]
> **Status:** [Draft | Approved]
> **Discovery Track:** [Greenfield | Scaffolded]

---

## Problem Statement

### What We're Building

[2-3 sentence description of what this project does and why it matters]

### Target Users

- **Primary:** [Who will use this most?]
- **Secondary:** [Other user types]

### Core Value Proposition

[What unique value does this provide? Why would someone choose this?]

### Success Metrics

- [How will we measure if this project succeeds?]
- [Key performance indicators]

---

## Constraints

### Critical Constraints

These constraints were identified as non-negotiable and shaped all technology decisions.

| Constraint | Value | Impact |
|------------|-------|--------|
| **Platform** | [Web / Mobile / API / CLI / Desktop] | Determines stack options |
| **Budget** | [Free / Low / Moderate / Enterprise] | Limits hosting and services |
| **Timeline** | [Immediate / Standard / Flexible] | Affects complexity tolerance |
| **Team Size** | [Solo / Small / Medium / Large] | Influences architecture |

### Expanded Constraints

Additional constraints discovered during the constraint discovery phase.

#### Technical Constraints

- **Deployment Environment:** [Where will this run?]
- **Performance Requirements:** [Any specific performance needs?]
- **Integration Requirements:** [Must integrate with what systems?]
- **Offline Requirements:** [Must work offline?]

#### Business Constraints

- **Compliance Requirements:** [HIPAA, SOC2, GDPR, etc.]
- **Data Residency:** [Where must data be stored?]
- **Support Requirements:** [What level of support is needed?]

#### Team Constraints

- **Known Skills:** [Technologies the team already knows]
- **Learning Budget:** [How much learning is acceptable?]
- **Maintenance Capacity:** [Who maintains this long-term?]

---

## Technology Stack

### Selected Stack

> **Pattern:** [Stack pattern name from stack-patterns.yaml]

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| **Language** | [e.g., TypeScript] | [e.g., 5.x] | [Why this choice] |
| **Framework** | [e.g., Next.js] | [e.g., 14.x] | [Why this choice] |
| **Database** | [e.g., PostgreSQL] | [e.g., 15+] | [Why this choice] |
| **ORM** | [e.g., Prisma] | [latest] | [Why this choice] |
| **Hosting** | [e.g., Vercel] | — | [Why this choice] |

### Key Technology Decisions

#### Decision 1: [e.g., Why Next.js over Remix]

**Context:** [What problem were we solving?]

**Options Considered:**
1. [Option A] - [Brief description]
2. [Option B] - [Brief description]

**Decision:** [What we chose and why]

**Trade-offs Accepted:** [What we gave up]

#### Decision 2: [e.g., Database choice]

[Repeat format as needed]

### Alternatives Considered

For transparency, these were the other stack options evaluated:

| Stack | Why Not Selected |
|-------|------------------|
| [Alternative 1] | [Reason] |
| [Alternative 2] | [Reason] |

---

## Preferences Captured

Preferences extracted from user's natural language description during problem framing.

### Explicit Preferences

Things the user specifically stated they wanted:

- [e.g., "I want to use React" - captured React preference]
- [e.g., "No paid services" - captured free tier budget]

### Inferred Preferences

Things inferred from context or prior experience:

- [e.g., User mentioned Node.js experience - factored into stack ranking]
- [e.g., User described a "simple" app - avoided complex architectures]

### Things NOT Asked

To avoid redundant questions, these topics were not re-asked because they were captured from the user's description:

- [e.g., Platform type - user said "web app"]
- [e.g., Framework preference - user mentioned React]

---

## Next Steps

### Immediate Actions

1. [ ] Run `/sigil:constitution` to generate project constitution from this foundation
2. [ ] Create initial project structure
3. [ ] Set up development environment

### Constitution Pre-Population

The following constitution articles will be pre-populated from this foundation:

- **Article 1 (Technology Stack):** Language, framework, database from Selected Stack
- **Article 3 (Testing):** Defaults based on framework conventions
- **Article 7 (Accessibility):** Standard WCAG 2.1 AA (unless compliance requires more)

### Open Questions

Questions that arose during discovery but weren't blocking:

- [Any unresolved questions for future consideration]

---

## Approval

By approving this foundation document, we confirm that:

1. The problem statement accurately describes what we're building
2. The constraints reflect our actual limitations
3. The selected technology stack is appropriate for our needs
4. We're ready to proceed to constitution creation

| Role | Name | Date | Approved |
|------|------|------|----------|
| Product Owner | | | [ ] |
| Technical Lead | | | [ ] |

---

## Appendix: Discovery Session Log

### Session Details

- **Date:** [DATE]
- **Duration:** [How long did discovery take?]
- **Participants:** [Who was involved?]

### Key Discussion Points

[Summary of important discussions or decisions made during discovery]

### Changed Decisions

[If any initial decisions were changed, document them here with rationale]
