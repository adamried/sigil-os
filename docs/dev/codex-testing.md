# Testing the Codex edition

## Free deterministic lane

```bash
python3 tools/build-codex-plugin.py --check
python3 tools/codex-plugin-linter.py --verbose
python3 tools/vendor/validate_plugin.py plugins/sigil
python3 -m unittest -v \
  tests.test_codex_helpers \
  tests.test_codex_hooks \
  tests.test_codex_build_and_linter
python3 tools/codex-contract-runner.py --dry-run
```

The helper suite covers root and path safety, setup/migration preservation,
configuration provenance, marker corruption, state revisions, audit migration,
task rows, agent files, integrity checks, redaction, and queues. The hook suite
covers every shipped event and fail-open shape. The linter suite seeds a real
failure for checks 01 through 22.

## Installed-cache lane

With Codex CLI 0.145.0 available:

```bash
python3 -m unittest -v tests.e2e.test_codex_install
```

This uses a temporary `CODEX_HOME`; it does not change the operator's installed
plugins. It verifies marketplace discovery, install, enablement, cache contents,
public skills, and setup output.

For an iterative local reinstall, keep public version `0.33.0-beta.1` and stamp
build metadata:

```bash
python3 tools/build-codex-plugin.py --cachebuster dev1
codex plugin remove sigil@sigil-os
codex plugin add sigil@sigil-os
```

Increment only the cachebuster (`dev2`, `dev3`, and so on), rebuild the clean
public package before committing, and start a new session after every reinstall.
Never edit the installed cache.

## Model contracts

The 68-contract dry run is free. Paid execution must run from a regular terminal
or CI, not from inside an agent session:

```bash
python3 tools/codex-contract-runner.py --test CX-001
```

The runner uses a fresh Git repository, explicit read-only sandbox, no network,
JSONL event capture, and a generated output schema. Never add a dangerous
sandbox or hook-trust bypass flag to CI.

## Release scenarios

Definitions and evidence rules live in `test-runs/scenarios/codex/`. A preview
claim is limited to cells with recorded evidence in `os-matrix.md`.
