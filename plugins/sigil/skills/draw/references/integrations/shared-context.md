# Shared-context capability adapter

The initial transport is authenticated `gh` behind a capability contract.
Core learning capture remains local when it is unavailable.

Before use, check the executable and authentication. Every operation receives
an explicit repository and branch. A write compares the expected remote
content identifier before updating. A moved identifier returns a conflict and
never overwrites.

After bounded failure, store one redacted queue entry with operation, target,
branch, target path, local content path or scrubbed content, capture time, and
idempotency identifier. Authentication is re-derived during replay. Replaying
twice must create at most one remote change.
