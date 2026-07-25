# Codex integrations

Each integration has its own authorization. Connecting one does not connect the
others.

## Jira through Atlassian Rovo

Dependency: the bundled `atlassian-rovo` app
(`connector_692de805e3ec8191834719067174a384`).

Install Sigil, choose the Atlassian connection, and complete Atlassian's consent
screen. If it is absent or unauthenticated, Sigil asks for ticket details in
plain language and continues locally. It does not treat a failed Jira write as
a completed update.

## Figma

Dependency: the bundled `figma` app
(`connector_68df038e0ba48191908c8434991bbac2`).

Choose the Figma connection and authorize the intended account. Figma seat
permissions still apply; a read-only seat cannot perform writes. If Figma is
missing, Sigil uses the local specification, `.sigil/design.md`, and
accessibility requirements.

## GitHub shared context

Dependencies: GitHub CLI (`gh`) and an authenticated session:

```bash
gh auth login
gh auth status
```

Every shared-context write names the repository, branch, target, and expected
remote revision. A conflict never overwrites remote content. A failed authorized
write is redacted and queued once under `.sigil/queue/shared-context/`; replay is
idempotent. Without `gh` or authentication, local learning still works.

## External design skills

External sources must use HTTPS and a full 40-character commit SHA. Sigil scans
the staged directory for symlinks, executable content, and oversized files,
then records it as untrusted advisory content only after confirmation. Refresh
shows the old and proposed revision before changing the pin. External guidance
cannot override the project constitution, Codex policy, or safety rules.

## Data handling and service terms

Connector content also passes through the Codex/OpenAI service used for the
session. Review your account or organization's terms and data controls before
connecting external systems:

- OpenAI: https://openai.com/policies/
- Atlassian: https://www.atlassian.com/legal and
  https://www.atlassian.com/legal/privacy-policy
- Figma: https://www.figma.com/legal/tos/ and
  https://www.figma.com/legal/privacy/
- GitHub: https://docs.github.com/en/site-policy/github-terms and
  https://docs.github.com/en/site-policy/privacy-policies

Jira reads send the requested issue, search, parent, or transition query and
return Atlassian-hosted ticket content. Authorized writes send the displayed
comment, link, or transition to Atlassian. Figma reads send the requested file
or node identifier and return design context to the session; this preview does
not request Figma writes. Shared-context operations send only the explicitly
reviewed target path and redacted content through `gh` to GitHub.

Your external-service account, organization policies, connector permissions,
and the providers' current terms govern that processing. Sigil does not copy
credentials into project files. Keep customer or production resources out of
test runs unless their owner explicitly approved the exact use.
