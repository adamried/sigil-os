# Capability checks

Check a capability immediately before it is needed:

- local project read/write access;
- scoped command execution;
- Git availability and repository status;
- optional custom-agent support;
- optional connector or CLI availability, authentication, and write
  authorization as three separate facts.

If a capability is missing, explain what is unavailable and continue with the
documented fallback. Do not return a raw trace. No optional capability may
block a local core workflow.
