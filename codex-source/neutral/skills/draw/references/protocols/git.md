# Git protocol

Git automation is disabled by default. An explicit project
`commits: enabled` setting permits local feature branches and scoped commits;
it does not authorize pushes, pull requests, deployments, or other remote
writes.

Before branch creation and every commit:

1. inspect the working tree;
2. identify pre-existing and unrelated changes;
3. show the exact in-scope paths;
4. stage only those reviewed paths;
5. verify the staged diff;
6. commit only if the configured workflow and current gate permit it.

Never use broad staging. Never discard or replace unrelated work. Broad
destructive recovery, forced branch replacement, or force-push requires an
explicit request naming that operation. Before discarding one file, show the
exact path and operation and obtain confirmation.

Report security result, report creation, commit creation, and commit
skipped/failed as separate states.
