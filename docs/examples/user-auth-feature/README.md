# Example: User Authentication Feature

This walkthrough shows how a Product Manager used Sigil to specify, plan, and hand off a user authentication feature. Follow along to see each stage of the workflow in action.

---

## The Scenario

**Background:** Sarah is a Product Manager at a startup building TaskFlow, a productivity application. The team needs to add user authentication so people can create accounts, log in, and keep their data private.

**The Challenge:** Sarah knows *what* users need (login, registration, password reset) but isn't sure how to communicate all the technical details to her engineering team. Previous handoffs have resulted in back-and-forth questions, misunderstandings, and rework.

**The Goal:** Use Sigil to create a complete, unambiguous specification that engineers can implement without confusion.

---

## Step 1: Setting Up the Constitution

Before creating any features, Sarah's team established a project constitution. This document captures the "rules of the road" that all features must follow.

**Command:** `/sigil:constitution`

**What Sarah Did:** She worked with her tech lead to answer questions about the project's technology choices, coding standards, and requirements.

**Result:** The constitution (see `constitution.md`) established:

| Area | Decision |
|------|----------|
| Language | TypeScript 5.x |
| Framework | Next.js 14 with App Router |
| Database | PostgreSQL 15 with Prisma ORM |
| Auth Library | NextAuth.js |
| Testing | 60% minimum coverage, test-first for critical paths |
| Accessibility | WCAG 2.1 Level AA minimum |

**Why This Matters:** The constitution prevents debates during implementation. When an engineer asks "Should I use SQL or NoSQL?", the answer is already documented: PostgreSQL. This saves time and ensures consistency.

---

## Step 2: Creating the Specification

With the constitution in place, Sarah was ready to describe the authentication feature.

**Command:** `/sigil:draw "Add user authentication to the application"`

**What Sarah Provided:**

> "We need users to be able to create accounts with email and password, log in, log out, and reset their passwords if they forget them. Sessions should persist so users don't have to log in every time. We might want social login later."

**What Sigil Produced:** A structured specification (see `spec.md`) containing:

### User Scenarios

Sigil identified 8 user scenarios and assigned priorities:

| Priority | Scenario | Description |
|----------|----------|-------------|
| P1 (Must) | US-001 | Create account with email/password |
| P1 (Must) | US-002 | Log in with credentials |
| P1 (Must) | US-003 | Log out |
| P1 (Must) | US-004 | Session persistence |
| P2 (Should) | US-005 | Password reset via email |
| P2 (Should) | US-006 | Clear error messages |
| P3 (Nice) | US-007 | Google login |
| P3 (Nice) | US-008 | Two-factor authentication |

### Requirements

The spec distinguished between **functional requirements** (what the system does) and **non-functional requirements** (how well it does it):

**Functional Examples:**
- FR-003: System shall enforce password requirements (8+ chars, 1 number, 1 special char)
- FR-007: System shall send password reset emails within 2 minutes

**Non-Functional Examples:**
- NFR-001: Login page loads in under 2 seconds
- NFR-003: Password storage follows OWASP guidelines (bcrypt, 12+ rounds)

### Key Entities

The spec defined what data would be stored:

```
User: id, email, passwordHash, createdAt, lastLoginAt, emailVerified
Session: id, userId, token, expiresAt, createdAt
```

**What Sarah Noticed:** The spec captured details she hadn't explicitly mentioned, like rate limiting for security and accessibility requirements. Sigil filled in best practices based on the constitution.

---

## Step 3: Clarification Session

Some requirements were ambiguous. Sigil asked targeted questions to resolve them.

**What happened next:** Sigil automatically started clarification

**What Happened:** Over two rounds, Sigil asked 7 questions (see `clarifications.md`):

### Round 1: Core Decisions

**Q1: Password Requirements**
> "What are the minimum password requirements?"
>
> Options:
> - A) 8 characters minimum, no other requirements
> - B) 8 characters with at least 1 number
> - C) 8 characters with 1 number and 1 special character
> - D) Custom requirements

**Sarah's Answer:** C

**Why She Chose This:** It balances security with usability. Too strict and users write passwords down; too lenient and accounts get compromised.

**Q2: Session Duration**
> "How long should user sessions last?"
>
> Options: Browser close / 24 hours / 7 days / 30 days

**Sarah's Answer:** 24 hours

**Why:** Security matters more than convenience for this application. Users on shared computers need protection.

**Q4: Failed Login Handling**
> "How should the system handle failed login attempts?"
>
> Options: Generic message / Specific error / Generic + rate limit / Account lockout

**Sarah's Answer:** Generic message + rate limit after 5 attempts

**Why:** Specific errors help attackers enumerate valid emails. Rate limiting prevents brute force without frustrating legitimate users who mistype.

### Round 2: Future Features

**Q5: OAuth Providers**
> "Which social login providers should be supported?"

**Sarah's Answer:** Google only (as P3)

**Why:** Google covers most users. Additional providers add complexity without proportional value. Can add more later.

**Q7: Two-Factor Authentication**
> "How should 2FA be implemented?"

**Sarah's Answer:** Authenticator app (TOTP), as P3

**Why:** SMS is less secure (SIM swapping). Authenticator apps are free and widely used. Making it P3 allows focus on core auth first.

---

## Step 4: Reviewing the Plan

With requirements clarified, Sigil generated an implementation plan.

**What happened next:** Sigil automatically generated the plan

**What Sigil Produced:** A technical plan (see `plan.md`) with:

### Constitution Gate Checks

The plan verified it followed the rules:

- [x] Maximum 3 new packages (NextAuth.js, bcrypt, zod)
- [x] No new infrastructure required
- [x] Uses existing database
- [x] Standard Next.js patterns

### Project Structure

A map of what files would be created or modified:

```
src/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   └── forgot-password/page.tsx
│   └── api/auth/[...nextauth]/route.ts
├── components/auth/
│   ├── LoginForm.tsx
│   ├── RegisterForm.tsx
│   └── PasswordInput.tsx
└── lib/
    ├── auth.ts
    └── validations/auth.ts
```

### API Contracts

Exact definitions of how the system would communicate:

```
POST /api/auth/register
Request: { email, password, name? }
Response (success): { success: true, user: { id, email, name } }
Response (error): { success: false, error: { code, message, fields? } }
```

### Risk Assessment

Potential problems and how they'd be prevented:

| Risk | Mitigation |
|------|------------|
| Password breach | bcrypt + monitoring |
| Session hijacking | Secure cookies, rotation |
| Brute force attack | Rate limiting, lockout |
| Email enumeration | Generic error messages |

**What Sarah Reviewed:**

1. **Does this match what we asked for?** Yes - all P1 and P2 features included
2. **Are the file locations sensible?** Yes - follows existing project patterns
3. **Are there any red flags?** No - security measures look appropriate

---

## Step 5: Task Breakdown

Finally, Sigil converted the plan into actionable tasks.

**What happened next:** Sigil automatically broke the plan into tasks

**What Sigil Produced:** 18 tasks across 3 phases (see `tasks.md`):

### Understanding the Task List

Each task includes:

| Element | Purpose |
|---------|---------|
| Task ID | Unique reference (T001, T002, etc.) |
| Description | What needs to be done |
| Files | What will be created or changed |
| Acceptance Criteria | How to know it's complete |
| Dependencies | What must be done first |
| Test First? | Whether to write tests before code |

### Task Symbols

```
[ ] Not started
[~] In progress
[x] Complete
[P] Can run in parallel with others
[B] Blocking - others depend on this
```

### Sample Tasks

**T001: Set up NextAuth.js configuration [B]**
- Files: `src/lib/auth.ts` (new), `package.json` (modify)
- Acceptance: NextAuth installed, config created, types configured
- This blocks other tasks - must be done first

**T006: Implement password hashing utilities [P]**
- Files: `src/lib/auth-utils.ts` (new)
- Acceptance: hashPassword and verifyPassword functions working
- Can run in parallel with T007 (PasswordInput component)

### Dependency Map

The plan includes a visual map showing which tasks depend on others:

```
T001 (Config) ──────┐
                    ├──► T005 (API) ──► T013 (Provider) ──► T014 (Middleware)
T002 (Schema) ──► T003 (Migration) ──┘
```

**What This Tells Engineers:**

- Start with T001 (config) and T002 (schema) - they have no dependencies
- T003 (migration) needs T002 finished first
- T005 (API route) needs both T001 and T003 complete
- T006 and T007 can run in parallel once T001 is done

---

## Step 6: The Handoff

With everything documented, Sarah was ready to hand off to engineering.

**Command:** `/sigil:handoff`

**What Engineers Received:**

1. **Specification** - What to build and why
2. **Clarifications** - Decisions already made (no need to re-ask)
3. **Implementation Plan** - How to build it
4. **Task Breakdown** - What to do in what order

**The Result:** Engineers could start immediately without a lengthy kickoff meeting. Questions that would normally come up ("How long should sessions last?" "What about 2FA?") were already answered.

---

## Key Learnings

### What Worked Well

1. **The constitution saved time** - Technology decisions were already made, so the plan could be specific.

2. **Clarification prevented rework** - Questions like "Should we do account lockout or rate limiting?" were resolved before coding started.

3. **Dependencies were clear** - Engineers knew what to work on first and what could run in parallel.

4. **Nothing was ambiguous** - Password requirements, session duration, error messages - all explicitly defined.

### Tips for Your Projects

1. **Be specific in your initial description** - The more detail you provide to `/sigil:draw "description"`, the fewer clarification rounds needed.

2. **Answer clarification questions thoughtfully** - These decisions affect implementation. Take time to consider the options.

3. **Review the plan with your tech lead** - They may spot issues or have suggestions before tasks are created.

4. **Use the task breakdown for sprint planning** - The dependency map shows what can be parallelized.

---

## Files in This Example

| File | Description |
|------|-------------|
| `constitution.md` | Project rules and standards |
| `spec.md` | Feature specification |
| `clarifications.md` | Questions and answers |
| `plan.md` | Implementation plan |
| `tasks.md` | Task breakdown with dependencies |

---

*This example demonstrates a Standard track workflow. Quick Flow and Enterprise tracks follow similar patterns with different levels of detail.*
