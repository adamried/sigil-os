# Repository-root and path-boundary protocol

1. Start with the session working directory.
2. If Git is available and the directory is inside a repository, resolve the
   top-level directory with a scoped Git query.
3. Otherwise ask the user to confirm the intended project directory.
4. Resolve the candidate to a canonical path and verify it is inside an
   authorized workspace root.
5. Reject traversal, absolute user-supplied subpaths, NUL bytes, and symlinks
   whose resolved target leaves an authorized root.
6. Pass the resolved root explicitly to helpers. Helpers do not independently
   guess another project root.
7. Express project files as repository-relative paths in instructions and as
   resolved paths beneath the verified root inside scripts.

Allowed roots are the verified project root, the plugin root for read-only
resources, an explicitly opted-in global Sigil directory, and the operating
system’s temporary directory for short-lived staging. Delete temporary data
when its documented use ends.
