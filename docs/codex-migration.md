# Move from the Claude edition to Codex

The two editions can coexist in one project. Installing the Codex edition does
not remove Claude's `CLAUDE.md`, root `SIGIL.md`, plugin manifest, commands, or
hooks. Codex setup reuses existing `.sigil/` work and proposes missing files
instead of overwriting it.

## Invocation map

Codex public skills use the plugin namespace shown below. Plain-language
requests work too.

| Claude command | Codex invocation | Codex owner |
|---|---|---|
| `/sigil:draw` | `$sigil:draw` | Public draw skill |
| `/sigil:setup` | `$sigil:setup` | Public setup skill |
| `/sigil:config` | `$sigil:config` | Public config skill |
| `/sigil:spec` | `$sigil:spec` | Public spec skill |
| `/sigil:review` | `$sigil:review` | Public review skill |
| `/sigil:export` | `$sigil:export` | Public export skill |
| `/sigil:learn` | `$sigil:learn` | Public learn skill |
| `/sigil:update` | `$sigil:update` | Public update skill |
| `/sigil:continue` | `$sigil:draw continue` | Draw mode |
| `/sigil:dashboard` | `$sigil:draw dashboard` | Draw mode |
| `/sigil:status` | `$sigil:draw status` | Draw mode |
| `/sigil:tasks` | `$sigil:draw tasks` | Draw mode and pipeline stage |
| `/sigil:constitution` | `$sigil:setup constitution` | Setup/config mode |
| `/sigil:profile` | `$sigil:setup profile` | Setup/config mode |
| `/sigil:connect` | `$sigil:config connect` | Config integration mode |
| `/sigil:audit` | `$sigil:draw audit` | Draw/config mode |
| `/sigil:handoff` | `$sigil:export handoff` | Internal export procedure |
| `/sigil:design` | `$sigil:draw design` | Internal design procedure |

## Behavioral differences in the preview

- Codex automatic commits default to off.
- Hooks are optional advice; the skills own all required checks.
- Optional Codex agents are generated per project after confirmation.
- The Codex preview uses project settings by default. Reading or writing
  `~/.sigil` requires project opt-in and a separate permission.
- Shared GitHub context uses an explicit `gh` adapter and one safe offline queue.

## Existing-project verification

Run `$sigil:setup`. Its plan identifies migration/verification mode. Check the
proposed changes, especially any legacy `/memory/waivers.md` move or state
format migration. State migration offers a dry-run diff and creates a backup.
Waivers remain tracked; setup never silently changes their Git status.

Historical prose is left alone. Only active instructions and templates are
corrected when an old absolute-looking Sigil path would change behavior.
