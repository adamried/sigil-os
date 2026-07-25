---
name: update
description: Check Sigil Codex compatibility, inspect installed and source versions, update the AGENTS.md marker block, or explain the cachebuster reinstall loop. Use for Sigil update, stale guidance, old skills, or version troubleshooting; do not edit Codex caches or config.toml by hand.
---

# Update

Determine whether the user wants a read-only version check, a project-guidance
update, or plugin reinstall guidance. Follow `references/update.md`.

Project updates use the setup plan-and-confirm path and preserve all content
outside Sigil-owned markers. Plugin development updates rebuild from source,
stamp one `+codex.<cachebuster>` suffix, reinstall from the configured
marketplace name read from its file, and require a new session. Never hand-edit
the installed plugin cache or Codex configuration to force refresh.
