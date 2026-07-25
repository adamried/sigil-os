# Sigil Documentation

Complete documentation for Sigil OS, the specification-driven development system.

---

## For Users

Start here if you use Sigil to build features, manage projects, or work with specifications.

| Document | What It Covers | Start Here If... |
|----------|---------------|------------------|
| [Quick Start](quick-start.md) | Install, set up, and build your first feature | You're new to Sigil |
| [Codex Installation](codex-installation.md) | Install the Codex preview safely | You use Codex CLI or the desktop app |
| [Codex Migration](codex-migration.md) | Claude-to-Codex command and coexistence map | You already use the Claude edition |
| [Codex Integrations](codex-integrations.md) | Separate Jira, Figma, and GitHub setup | You want external context |
| [User Guide](user-guide.md) | Complete reference for daily use | You want the full picture |
| [Command Reference](command-reference.md) | Every slash command with examples | You need command syntax |
| [Troubleshooting](troubleshooting.md) | Common issues and solutions | Something went wrong |
| [Glossary](glossary.md) | Plain-English term definitions | You see an unfamiliar term |
| [Migration from Global](migration-from-global.md) | Migrating from v1.x global install | You used Sigil before v2.0 |

### Reading Order (New Users)

1. [Quick Start](quick-start.md) — Install Sigil and build your first feature
2. [User Guide](user-guide.md) — Learn the full workflow
3. [Command Reference](command-reference.md) — Look up commands as needed

---

## Printable Guides

Downloadable DOCX versions for offline reference or sharing with your team.

These printables currently cover the Claude edition. Codex printables follow
after the preview reaches Core Parity on one supported surface.

| Guide | Description |
|-------|-------------|
| [Setup Guide](printables/Sigil_OS_Setup_Guide.docx) | Install, configure, and start your first project |
| [Quick Reference](printables/Sigil_OS_Quick_Reference.docx) | Commands, workflows, and key concepts at a glance |
| [Setup Testing Guide](printables/Sigil_OS_Setup_Testing_Guide.docx) | Verify your installation is working correctly |

---

## For Developers and Contributors

These documents cover Sigil's internals, architecture, and extension points.

| Document | What It Covers |
|----------|---------------|
| [Developer Docs Index](dev/README.md) | Index of all developer documentation |
| [Extending Skills](dev/extending-skills.md) | Creating and registering new skills |
| [Versioning](dev/versioning.md) | Semantic versioning strategy for skills |
| [Workflow Diagrams](dev/workflow-diagrams.md) | Command flows, agent routing, and track selection |
| [Context Management](dev/context-management.md) | Project state persistence protocol |
| [Error Handling](dev/error-handling.md) | Error taxonomy, codes, and recovery |
| [MCP Integration](mcp-integration.md) | Optional external tool integrations |
| [Codex Architecture](dev/codex-architecture.md) | Source layers, adapters, state ownership, hooks, and agents |
| [Codex Testing](dev/codex-testing.md) | Deterministic, installed-cache, contract, and E2E lanes |

### Reading Order (Contributors)

1. [Workflow Diagrams](dev/workflow-diagrams.md) — Understand the system architecture
2. [Extending Skills](dev/extending-skills.md) — Learn how to add capabilities
3. [Context Management](dev/context-management.md) — Day-to-day development patterns

---

## Examples

The `examples/` directory contains complete worked examples:

| Example | Description |
|---------|-------------|
| [User Auth Feature](examples/user-auth-feature/README.md) | Full walkthrough: spec, clarifications, plan, and tasks |
