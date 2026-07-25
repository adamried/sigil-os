# Codex preview capability inventory and non-goals

| Capability | CLI | ChatGPT desktop | Fallback |
|---|---|---|---|
| Local project reads/writes | Yes, subject to sandbox | Yes, when a local project is attached | Read-only planning or explanation |
| Scoped shell and tests | Yes, subject to approval | Depends on attached environment | Report checks that could not run |
| Git | When installed | When available in environment | No branch or commit automation |
| Custom agents | Project `.codex/agents/` | Supported by the parent surface | Sequential role execution |
| Hooks | Local CLI trust flow | Surface-dependent | Coordinator performs every check |
| Jira/Figma apps | When installed and authorized | When installed and authorized | Local ticket/design context |
| GitHub shared context | Authenticated `gh` | Local CLI path only | Local learning plus safe queue |

First-preview non-goals: identical Claude slash-command syntax, Codex IDE
plugin browsing, full ChatGPT Work web/local-development parity, Windows,
PM Copilot, and PO Buddy.
