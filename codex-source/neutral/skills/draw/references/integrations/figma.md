# Figma capability adapter

Sigil v1 requests read capabilities only: inspect a file, inspect a node, and
extract tokens/components. Record file and node identifiers for every adopted
design fact.

If the connector is missing, unauthenticated, declined, or read access is
unavailable, proceed without pressure from:

1. the validated feature specification;
2. `.sigil/design.md` when enabled;
3. existing interface patterns;
4. accessibility requirements.

State which local sources were used. Do not request Figma write scope.
