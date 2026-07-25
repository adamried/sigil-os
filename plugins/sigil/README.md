# Sigil OS for Codex — Preview

Sigil turns a plain-language feature request into a checkpointed path through
specification, planning, implementation, validation, code review, and security
review.

The preview targets Codex CLI and Codex in the ChatGPT desktop app. macOS has a
recorded local acceptance run; Linux is the intended second runtime and becomes
a claimed preview platform after its CI matrix is green. Core workflows do not
require hooks, custom agents, Jira, Figma, or shared GitHub context. Hooks are
optional advisory conveniences and require separate trust. Jira and Figma
connectors require their own authorization.

Requirements:

- Codex CLI 0.145.0 or newer for the validated preview surface
- Python 3.9 or newer
- `ruamel.yaml` 0.18.x for configuration read/write commands
- Git for repository workflows
- Optional: authenticated `gh` CLI for shared context

After installation, start a new Codex session. Ask to “set up Sigil in this
project” or “build a feature,” or explicitly mention `$sigil:setup` or
`$sigil:draw`.

See `references/support.md` inside the package and the repository’s
`docs/codex-installation.md` for setup, trust, migration, and limitations.
