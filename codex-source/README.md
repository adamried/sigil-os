# Sigil Codex source

This directory is the authored source for the Codex distribution.

- `neutral/` contains platform-neutral workflow contracts, role procedures,
  templates, and integration policy.
- `codex/` contains Codex packaging, public skill entry points, hooks, and
  Python adapters.
- `VERSION` is the Codex base version.

Run `python3 tools/build-codex-plugin.py` from the repository root to assemble
`plugins/sigil/`. The generated package is committed so local marketplace
installation and installed-cache tests exercise the exact release input.

The Claude distribution remains independently installable from
`sigil-plugin/`. A release claims behavior parity only after the release
checklist verifies both editions and synchronizes their public versions.
