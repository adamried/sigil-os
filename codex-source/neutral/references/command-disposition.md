# Claude-command to Codex-skill disposition

| Claude command | Codex owner |
|---|---|
| `draw` | public `draw` skill |
| `setup` | public `setup` skill |
| `config` | public `config` skill |
| `spec` | public `spec` skill |
| `review` | public `review` skill |
| `export` | public `export` skill |
| `learn` | public `learn` skill |
| `update` | public `update` skill |
| `continue` | `draw` continue mode |
| `dashboard` | `draw` dashboard mode |
| `status` | `draw` status mode |
| `tasks` | `draw` tasks mode and pipeline phase |
| `constitution` | `setup` or `config` constitution mode |
| `profile` | `setup` or `config` profile mode |
| `connect` | `setup` or `config` integration mode |
| `audit` | `draw` or `config` audit mode |
| `handoff` | internal export procedure |
| `design` | internal draw design procedure |

Each row has exactly one canonical owner. A future thin alias may route to the
owner but may not duplicate workflow logic.
