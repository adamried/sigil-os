# Implementation procedure

For each task:

1. inspect the scoped code, tests, local guidance, and relevant learnings;
2. select deterministic specialist overlays;
3. define a failing or otherwise discriminating verification;
4. implement the smallest change inside scope;
5. run focused checks;
6. hand changed paths and evidence to validation;
7. fix only authorized findings and count each iteration;
8. update the task artifact through the coordinator after validated success;
9. create a scoped local commit only when explicitly enabled.

Pause on unexpected scope, unrelated dirty changes that overlap required
paths, or any shared safety gate.
