# Sigil OS

**Inscribe it. Ship it.**

**Specification-driven development for Claude Code — built for product managers, works for engineers too.**

Sigil is a plugin for Claude Code, Anthropic's AI coding tool. Transform natural language descriptions into implemented, tested features through structured workflows.

> **v0.32.0** · Active development — expect breaking changes between minor versions.

---

## What Is Sigil?

Sigil is like having a technical team that speaks your language. You describe what you want to build in plain English, and Sigil's agents write specs, plan implementation, and generate code — with checkpoints along the way where you review and approve before anything ships. Simple requests get fast-tracked; complex ones get full specification-and-review workflows automatically.

```mermaid
flowchart LR
    A["You describe<br>a feature"] --> B["Sigil writes<br>the spec"] --> C["You review<br>& approve"] --> D["Sigil builds<br>& tests"] --> E["Working<br>code"]

    style A fill:#e0f2fe,stroke:#0ea5e9,color:#1e293b
    style B fill:#a5b4fc,stroke:#6366f1,color:#1e293b
    style C fill:#fef3c7,stroke:#f59e0b,color:#1e293b
    style D fill:#a5b4fc,stroke:#6366f1,color:#1e293b
    style E fill:#d1fae5,stroke:#10b981,color:#1e293b
```

### Two Ways to Work

Sigil adapts to how you think. During setup, you pick a track that shapes the entire experience.

| | Non-Technical (default) | Technical |
|---|---|---|
| **Best for** | Product managers, founders, solo builders | Engineers, tech leads |
| **Communication** | Plain English, no jargon | Agent names, file paths, trade-offs |
| **Technical decisions** | Handled automatically | Surfaced for your input |
| **Progress** | "3 of 8 steps done" | "T003/T008 implementing (api-developer)" |
| **Specialists** | Work silently in the background | Named in output so you can see who's doing what |

Switch anytime with `/sigil:config set user_track technical` (or `non-technical`). Your track is a personal setting — it won't affect your teammates.

---

## Installation

Sigil requires Claude Code with a Pro, Max, or API plan. See [Anthropic's setup guide](https://docs.anthropic.com/en/docs/claude-code) to install Claude Code if you haven't already.

Once Claude Code is installed, add Sigil:

```bash
claude plugin marketplace add araserel/sigil-os
```

```bash
claude plugin install sigil@sigil-os
```

Verify it worked:

```bash
claude plugin list
```

You should see `sigil` in the list.

Something not working? See the [Troubleshooting Guide](docs/troubleshooting.md).

**Quick checklist:**

- [ ] `claude --version` shows a version number
- [ ] `claude plugin list` shows `sigil`
- [ ] `/sigil:draw status` shows the Sigil dashboard

---

## Quick Start

After installing the plugin, set up your first project in four commands:

```
cd your-project
claude
/sigil:setup
/sigil:draw "Add a contact form with email validation"
```

`/sigil:setup` creates your project's constitution (rules that guide Sigil), optionally generates a project profile, and configures enforcement. You only run it once per project.

`/sigil:draw "..."` starts building. Sigil assesses complexity, selects the right workflow track, and assigns specialized agents to handle specification, planning, implementation, and review.

See the [Quick Start Guide](docs/quick-start.md) for a detailed walkthrough.

### How the Build Loop Works

Once Sigil starts building, each task goes through a validate-and-fix cycle before moving on. After all tasks pass, you review the final result.

```mermaid
sequenceDiagram
    actor You
    participant Dev as Developer
    participant QA

    loop Each task
        Dev->>Dev: Build task
        Dev->>QA: Validate
        loop Auto-fix (up to 5 attempts)
            QA-->>Dev: Issues found
            Dev->>QA: Fix applied
        end
        QA-->>Dev: Pass
    end

    Dev->>You: Code review
    You->>Dev: Approved
```

---

## Commands

### Core

| Command | Purpose |
|---------|---------|
| `/sigil:draw` | Show status and menu |
| `/sigil:draw "description"` | Start building a feature |
| `/sigil:draw continue` | Resume where you left off |
| `/sigil:draw help` | Show all commands |

### Setup & Configuration

| Command | Purpose |
|---------|---------|
| `/sigil:setup` | Initialize Sigil in a new project |
| `/sigil:config` | View or change configuration (track, mode) |
| `/sigil:constitution` | View or edit project rules |
| `/sigil:profile` | Generate or view project profile |
| `/sigil:connect` | Link project to shared context repo |

### Utilities

| Command | Purpose |
|---------|---------|
| `/sigil:handoff` | Generate engineer review package |
| `/sigil:learn` | View, search, or review learnings |
| `/sigil:update` | Check for plugin updates |

See the [Command Reference](docs/command-reference.md) for detailed usage.

### Sharing Context Across Projects

Connect multiple projects to a shared GitHub repo. Learnings and project profiles sync automatically so each project benefits from what the others have learned.

```mermaid
---
config:
  layout: dagre
---
flowchart LR
    subgraph Project A
        A1[Learnings]
        A2[Profile]
    end

    subgraph Project B
        B1[Learnings]
        B2[Profile]
    end

    subgraph Project C
        C1[Learnings]
        C2[Profile]
    end

    subgraph Shared Repo
        S1[("Shared<br>Learnings")]
        S2[("Project<br>Profiles")]
    end

    A1 <-->|sync| S1
    B1 <-->|sync| S1
    C1 <-->|sync| S1

    A2 <-->|sync| S2
    B2 <-->|sync| S2
    C2 <-->|sync| S2

    style S1 fill:#a5b4fc,stroke:#6366f1,color:#1e293b
    style S2 fill:#a5b4fc,stroke:#6366f1,color:#1e293b
    style A1 fill:#d1fae5,stroke:#10b981,color:#1e293b
    style A2 fill:#d1fae5,stroke:#10b981,color:#1e293b
    style B1 fill:#e0f2fe,stroke:#0ea5e9,color:#1e293b
    style B2 fill:#e0f2fe,stroke:#0ea5e9,color:#1e293b
    style C1 fill:#fef3c7,stroke:#f59e0b,color:#1e293b
    style C2 fill:#fef3c7,stroke:#f59e0b,color:#1e293b
```

See the [Shared Context Setup Guide](docs/shared-context-setup.md) to get started.

---

## Documentation

- [Quick Start Guide](docs/quick-start.md)
- [User Guide](docs/user-guide.md)
- [Command Reference](docs/command-reference.md)
- [Shared Context Setup](docs/shared-context-setup.md) — share learnings and context across multiple repositories


---

Built for [Claude Code](https://www.anthropic.com/claude-code) by Anthropic.
