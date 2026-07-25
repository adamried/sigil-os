# Support and capability contract

Sigil’s Codex preview targets local Codex CLI and Codex in the ChatGPT desktop
app. The helper runtime supports macOS and Linux; the release evidence matrix
controls which operating systems are publicly claimed. Plugin browsing is not
an IDE-extension capability. Core feature workflows require a writable local
project, Python 3.9+, and Git when version-control behavior is requested.

Unavailable capabilities degrade as follows:

| Capability | Result when unavailable |
|---|---|
| Local file writes | Explain that setup or implementation requires a writable local project; offer read-only planning or review. |
| Shell commands | Explain which validation cannot run; do not invent results. |
| Git | Continue without branch or commit automation and report that limitation. |
| Custom agents | Adopt every role sequentially in the root coordinator. |
| Hooks | Run all checks from the coordinator fallback map. |
| Jira | Continue from the user’s description and local artifacts. |
| Figma | Continue from the spec, local design context, and accessibility requirements. |
| GitHub shared context | Keep local learnings and queue an authorized failed push safely. |

Sigil execution modes never expand Codex permissions. Managed workspace policy,
sandboxing, approval requirements, and explicit user instructions remain in
control.
