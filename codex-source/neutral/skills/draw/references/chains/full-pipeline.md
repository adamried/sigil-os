# Full Pipeline

Use Standard for moderate multi-step features. Use Enterprise for high-risk,
cross-system, compliance-sensitive, or architecture-heavy work.

Sequence:

1. assess complexity and select Standard or Enterprise;
2. create or validate the project constitution;
3. write `spec.md`;
4. resolve ambiguity in `clarifications.md`, at most three rounds;
5. for UI work, complete the design procedure using local context and optional
   Figma reads;
6. write `plan.md`;
7. for Enterprise, complete focused research and persist its sources;
8. for Enterprise or any significant decision, write decision records;
9. write `tasks.md` with dependencies, scope, and acceptance checks;
10. for each task: select overlays, implement, validate, and run the bounded
    fix loop;
11. after all tasks pass QA, perform code review;
12. perform security review as a distinct subsequent phase when risk triggers
    or the selected track requires it;
13. write `security.md` with scope, findings, verdict, and limitations;
14. create a verification commit only when commits are enabled and all gates
    permit it;
15. produce handoff and optional external-write outcomes;
16. persist complete state and relevant learnings.

Fix limits: Standard at most three attempts per task; Enterprise at most five.
Exhaustion pauses at the safety gate.

Each numbered phase has its own artifact or structured verdict. Research and
decision-record phases are functional Enterprise work, not placeholders.
