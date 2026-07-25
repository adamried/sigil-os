# Codex preview release checklist

## Installable

- [x] Built package is deterministic and validates
- [x] Local marketplace is recognized by Codex CLI 0.145.0
- [x] Isolated install is enabled and exposes eight skills
- [x] Installed-cache setup preserves existing `AGENTS.md` text
- [x] Setup creates no undeclared files

## Core Parity

- [ ] Quick Flow transcript green
- [ ] Standard Flow transcript green with separate review stages
- [ ] Discovery empty/established transcripts green
- [ ] Implement-Ready transcript green
- [ ] Resume uses two genuine sessions
- [ ] Dirty-worktree preservation transcript green

## Full Parity

- [ ] Hooks-disabled scenario green
- [ ] Agents-absent scenario green
- [ ] Agents-installed scenario green with equivalent artifacts
- [ ] Jira absence and dedicated authenticated-resource scenarios green
- [ ] Figma absence and dedicated authenticated-resource scenarios green
- [ ] Shared-context offline queue/replay scenario green
- [ ] macOS matrix complete
- [ ] Linux matrix complete
- [ ] Documentation behavior review complete

## Publication

- [x] Preview label appears in manifest, marketplace, README, guide, and notes
- [x] Version policy is machine-readable
- [x] Claude/Codex divergence ledger is current
- [x] Migration and clean removal are documented
- [x] Printable deferral and trigger are recorded
- [ ] First authenticated model-contract cost/time recorded
- [ ] Full installed-cache evidence attached to the release

## Nine-item release bundle

- [x] Exact generated plugin package validated by both Codex validators
- [x] Marketplace entry validated and isolated-install tested
- [ ] Immutable public source tag or revision recorded
- [x] Installation and removal instructions included
- [ ] Supported surfaces and OS list limited to completed matrix evidence
- [x] Required and optional dependencies listed
- [x] Known limitations and preview gates listed
- [x] Existing-project migration and divergence digest included
- [ ] Final test summary and evidence links attached

Before public directory submission:

- [x] Author, license, category, icons, and descriptions are complete
- [ ] Any listing screenshots are captured from this exact version and carry a
  `0.33.0-beta.1` taken-at annotation
- [x] Jira, Figma, GitHub, and OpenAI data paths and official terms are linked

Do not remove “preview” until Core Parity is green on every claimed surface.
Regenerate Codex printable guides after Core Parity passes on one claimed
surface and the public skill set remains frozen.
