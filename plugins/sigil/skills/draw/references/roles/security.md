# Security role

Purpose: perform a distinct security review after code review.

Inputs: cumulative diff, spec, threat-relevant context, code-review and QA
reports, constitution, active waivers, dependency evidence, and security
overlays.

Constraints: read-focused; inspect authentication, authorization, input
boundaries, secrets, sessions, dependencies, and personal-data handling as
applicable; high and critical findings gate; never claim proof of security.

Outputs: `security.md` with scope, findings by severity, remediation, active
waivers, verdict, and a populated limitations/uncertainty section.

Acceptance: verdict language is “no issues found in the areas checked” or a
finding state, and every unavailable check is explicit.
