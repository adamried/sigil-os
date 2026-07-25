# Design procedure

1. Check the persisted design opt-in or opt-out; do not re-ask a declined
   question.
2. Load `.sigil/design.md` when enabled and present.
3. Inspect existing UI patterns and accessibility conventions.
4. If the user supplied Figma context, use the read capability after
   availability and authentication checks; otherwise use the local fallback.
5. Define flows, empty/loading/error/success states, components, tokens,
   responsive behavior, keyboard behavior, semantic structure, contrast, and
   assistive-technology expectations.
6. Trace every design choice to a requirement and list sources.
7. Propose changes to normative design context; never refresh it silently.
