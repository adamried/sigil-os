# Helper contracts

All helpers require Python 3.9+ on macOS or Linux, reject unknown arguments
before file operations, redact credential-shaped output, and use:

| Code | Meaning |
|---|---|
| 0 | success |
| 1 | validation failure |
| 2 | usage error |
| 3 | missing dependency or unsupported runtime |
| 4 | permission or authorization failure |
| 5 | conflict, corruption, or stale state |
| 6 | remote/provider failure |

Project helpers receive `--root <resolved-repository-root>`. Nontrivial
migrations expose `--dry-run`. Writes use same-directory temporary files,
atomic replacement, and read-back verification. They reject paths and symlinks
that escape approved roots.

Configuration uses `ruamel.yaml` 0.18.x to preserve unknown keys, comments,
ordering, and quoting. This is the documented exception to the standard-library
preference. Python below 3.11 additionally uses `tomli` for validation when the
optional TOML merge helper is called.
