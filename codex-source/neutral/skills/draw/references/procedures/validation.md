# QA and fix-loop procedure

Validate:

- each acceptance criterion;
- existing and new automated tests;
- lint/type/build checks that apply;
- error and negative paths;
- accessibility for UI work;
- relevant specialist overlay cases;
- the actual cumulative diff.

Classify findings as critical, major, minor, or informational. Provide
reproduction evidence. Quick allows one fix attempt, Standard three, and
Enterprise five. Count an attempt whenever code changes in response to a
finding. Stop and gate when the limit is exhausted.
