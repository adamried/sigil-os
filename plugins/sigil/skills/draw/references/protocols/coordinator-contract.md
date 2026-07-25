# Coordinator and state ownership contract

This contract is normative for every Sigil workflow.

## Single writer

The root coordinator is the sole writer of
`.sigil/project-context.md`. A role, custom agent, hook, integration, or
sequential sub-procedure may return evidence but must not commit a phase
transition.

Each transition requires:

1. the expected current state revision;
2. a valid artifact owned by the completed phase;
3. read-back verification after atomic replacement;
4. an audit entry when audit mode is enabled.

Reject stale results whose expected revision differs from the current revision.
Reject a transition based only on a filename.

## Artifact ownership

| Artifact | Responsible role |
|---|---|
| `spec.md`, `clarifications.md` | specification |
| design section or design artifact | design |
| `plan.md`, decision records, research | architecture |
| `tasks.md` | task planning |
| product code and implementation notes | implementation |
| QA reports | validation |
| code-review report | code review |
| `security.md` | security |
| deployment-readiness output | deployment readiness |
| `project-context.md` and phase transitions | root coordinator only |

Roles may write their owned artifacts when authorized. They return a structured
handoff containing: role, phase, inputs used, output paths, validation result,
open risks, requested transition, and expected state revision.

## Hooks

Core correctness never depends on hooks being enabled or trusted. A hook may
surface advisory context only. Every hook-assisted behavior has a coordinator
fallback in `hook-fallbacks.md`.
