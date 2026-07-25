# Review procedure

Code review runs first and examines correctness, regressions, test coverage,
scope, maintainability, and constitution compliance.

Security review runs afterward when the track or changed surface requires it.
It examines applicable threat boundaries and writes a separate report. The
security report includes:

- reviewed paths and evidence;
- findings and severity;
- active relevant waivers;
- remediation;
- verdict;
- limitations and uncertainty.

Neither review silently edits code. Requested fixes return to implementation
and repeat validation before review resumes.
