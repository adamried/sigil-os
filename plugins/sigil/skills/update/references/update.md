# Update workflow

Read-only check:

- plugin manifest version;
- `.sigil/SIGIL.md` format version;
- `AGENTS.md` marker version and integrity;
- project state schema version;
- supported runtime and Codex CLI surface.

Project guidance update uses setup plan-and-confirm and never rewrites outside
owned markers.

Local plugin development:

1. rebuild from `codex-source`;
2. replace the existing build metadata with one
   `+codex.<cachebuster>` suffix;
3. read the marketplace name from `marketplace.json`;
4. reinstall from that marketplace;
5. test in a new session against the installed cache copy.

Public versions change only for releases.
