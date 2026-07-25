# Developer Documentation

Documentation for contributors and developers extending Sigil OS.

> **Looking for user docs?** See the [main documentation index](../README.md).

---

## Contents

| Document | Purpose |
|----------|---------|
| [Extending Skills](extending-skills.md) | How to create and register new skills |
| [Versioning](versioning.md) | Semantic versioning strategy for skills |
| [Workflow Diagrams](workflow-diagrams.md) | Command flows, track routing, and agent reference |
| [Context Management](context-management.md) | Protocol for maintaining project state across sessions |
| [Error Handling](error-handling.md) | Error taxonomy, codes, escalation paths, and agent error tables |
| [Codex Architecture](codex-architecture.md) | Package layers, runtime boundaries, and divergence decisions |
| [Codex Testing](codex-testing.md) | Deterministic, contract, installation, and release validation |

## Reading Order

1. Start with **Workflow Diagrams** to understand the overall system architecture
2. Read **Extending Skills** when you need to add new capabilities
3. Reference **Versioning** when making changes to existing skills
4. Consult **Context Management** for state persistence details
5. Use **Error Handling** for error classification and recovery protocols
6. Use **Codex Architecture** and **Codex Testing** for Codex-specific changes

## Additional Resources

- [Extending Skills](extending-skills.md) — Adding skills, agents, hooks, and validation
- [CLAUDE.md](../../../CLAUDE.md) — Repository structure and development rules
- [STATUS.md](../../../STATUS.md) — Implementation status
