# Hook fallback map

Hooks are advisory, untrusted until reviewed, and may be disabled by the user
or an administrator.

| Hook convenience | Coordinator-owned behavior |
|---|---|
| setup/staleness notice | compare the `.sigil/SIGIL.md` format version during the draw/setup preamble |
| team configuration hint | read project configuration during setup and draw |
| design-context hint | check the design setting and `.sigil/design.md` at the design gate |
| state-update reminder | validate state after every confirmed phase |
| role-routing warning | select roles from the active chain |
| session persistence reminder | persist confirmed progress before reporting completion |

A hook error produces at most a warning. It never aborts the workflow. Hooks
are useful guardrails, not a complete enforcement boundary.
