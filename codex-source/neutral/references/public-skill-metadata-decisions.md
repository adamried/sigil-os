# Public skill metadata decisions

The eight public skills intentionally omit per-skill `agents/openai.yaml` in
the preview. Their frontmatter descriptions are sufficient for implicit
routing, no skill has a mandatory connector, and the plugin-level interface
already supplies presentation metadata. This avoids implying Jira or Figma is
required for core workflows.

Revisit per-skill UI metadata after installed-build usability testing. Any
future surprising or internal-leaning alias must disable implicit invocation.
