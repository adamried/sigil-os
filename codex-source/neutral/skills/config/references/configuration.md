# Configuration modes

Known settings:

| Key | Allowed values | Default |
|---|---|---|
| `user_track` | `non-technical`, `technical` | `non-technical` |
| `execution_mode` | `automatic`, `directed`, `autonomous` | `automatic` |
| `audit_mode` | `true`, `false` | `false` |
| `commits` | `enabled`, `disabled` | `disabled` |
| `global_config_opt_in` | `true`, `false` | `false` |
| `design.enabled` | `true`, `false` | no decision |

Project values override opted-in global values, which override defaults.
`show` labels provenance.

Constitution and profile modes read or propose changes to the corresponding
tracked project artifacts. Integration mode changes only the registry and
field mappings; connector authentication remains with the connector. Audit
mode writes ignored per-session files. Clearing audit data is destructive and
requires exact confirmation.

Use `scripts/sigil-config integration-show --root <root>` to inspect the
project registry. Use `integration-set <jira|figma|shared_context>
<true|false>` to enable or disable one adapter. Jira custom fields and category
mappings may be supplied in a project-local JSON mapping with `--mapping-file`;
the helper merges it under the selected integration without changing skill
instructions or storing credentials.
