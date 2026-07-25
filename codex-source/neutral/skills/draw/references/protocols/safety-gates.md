# Safety gates

These gates pause every Sigil execution mode, including autonomous pacing.
They do not replace Codex approvals or managed policy.

Pause for:

1. a constitution violation or unresolved required-standard conflict;
2. a high or critical security finding;
3. a code-review blocker;
4. exhaustion of the track’s QA fix limit;
5. an ambiguous destructive or irreversible action;
6. out-of-scope files before an automated commit;
7. an expired waiver requiring a user decision;
8. an external write that the user has not clearly authorized.

At a gate, state the evidence, impact, safe options, and recommended next step
in plain language. Do not imply that workflow pacing grants tool permission.
Record an approved constitution exception in the tracked
`.sigil/waivers.md`.
