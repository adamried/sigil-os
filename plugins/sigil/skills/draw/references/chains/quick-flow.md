# Quick Flow

Use only for a small, well-understood change with at most five tasks and no
meaningful security, privacy, migration, or architecture risk.

Sequence:

1. assess complexity and confirm the request is safe for Quick Flow;
2. load constitution and active waivers;
3. write a lightweight persisted `spec.md`;
4. write a flat `tasks.md` with at most five tasks;
5. implement one scoped task at a time;
6. validate each task, with at most one fix attempt;
7. report completion and capture a learning only for a substantive resolved
   issue;
8. perform separately authorized ticket updates if requested.

Quick Flow does not silently skip security-sensitive work. If auth, sessions,
payments, personal data, input boundaries, or migrations appear, pause and
offer Standard Flow. Code review, security review, and verification commit are
marked not applicable only after that risk check.

Artifacts must be valid before the coordinator transitions:
`spec.md` → `tasks.md` → implementation evidence → QA result → complete.
