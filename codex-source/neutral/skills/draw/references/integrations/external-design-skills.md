# External design-skill governance

External instruction repositories are optional, untrusted, and advisory.

Before first use:

1. display the source URL and exact commit revision;
2. obtain explicit approval;
3. stage content in an approved directory;
4. reject traversal, escaping symlinks, executable files, and files over the
   documented size limit;
5. record the pinned commit in `.manifest.json`.

A refresh may stage a newer pinned revision but cannot silently change
`.sigil/design.md` or another normative artifact. Present a reviewable
proposal and apply only after confirmation.
