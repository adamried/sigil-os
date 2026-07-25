# Task decomposition procedure

Create ordered tasks with:

- stable identifier and plain-language outcome;
- exact in-scope paths or path-selection rule;
- dependencies;
- acceptance checks and relevant test command;
- risk/specialist triggers;
- whether the task is safe to perform independently.

Tests precede implementation when practical. A task is complete only after its
acceptance evidence passes. Keep feature-level QA, code-review, security, and
commit states separate from task checkboxes.
