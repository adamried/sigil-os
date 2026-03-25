---
name: security-reviewer
description: Identify security vulnerabilities and validate compliance with security mandates. Invoke for security-sensitive changes or as part of Review phase.
version: 1.0.0
category: review
chainable: true
invokes: []
invoked_by: [security]
tools: Read, Bash, Glob, Grep
---

# Skill: Security Reviewer

## Purpose

Identify security vulnerabilities and validate compliance with constitution security mandates (Article 4). This skill performs OWASP-aligned security analysis, dependency auditing, and ensures secure coding practices are followed.

## When to Invoke

- After code-reviewer completes (for security-sensitive changes)
- User requests `/security` or "security review"
- Changes involve authentication, authorization, or data handling
- New dependencies added
- API endpoints modified

## Inputs

**Required:**
```json
{
  "changed_files": ["src/auth.ts", "src/api/users.ts"],
  "constitution_path": "/.sigil/constitution.md"
}
```

**Optional:**
```json
{
  "dependency_manifest": "package.json",
  "scan_depth": "surface | deep",
  "focus_areas": ["auth", "injection", "data_exposure"],
  "previous_review": "/.sigil/specs/.../reviews/security-review-v1.md"
}
```

**Auto-loaded:**
- Constitution Article 4 (Security)
- Package manifests (package.json, requirements.txt)
- .env.example (to check for exposed secrets)

## Outputs

**Primary Output:**
```json
{
  "status": "secure | warnings | vulnerabilities_found",
  "review_id": "SR-001",
  "timestamp": "2025-01-14T10:30:00Z",
  "findings": [
    {
      "id": "SEC-001",
      "severity": "info | low | medium | high | critical",
      "category": "A01-A10",
      "owasp_id": "A03:2021",
      "cwe_id": "CWE-79",
      "file": "src/api/users.ts",
      "line": 42,
      "code_snippet": "...",
      "description": "Potential XSS vulnerability",
      "impact": "Attacker could execute scripts in user context",
      "remediation": "Sanitize user input before rendering",
      "references": ["https://owasp.org/...", "https://cwe.mitre.org/..."]
    }
  ],
  "dependency_audit": {
    "packages_scanned": 142,
    "vulnerabilities": {
      "critical": 0,
      "high": 1,
      "medium": 2,
      "low": 5
    },
    "outdated_packages": 12,
    "details": [...]
  },
  "constitution_compliance": {
    "article_4_compliant": true,
    "violations": []
  },
  "approval_recommendation": "approve | conditional | block"
}
```

**Artifact Output:** `/.sigil/specs/###-feature/reviews/security-review.md`

## OWASP Top 10 Checks (2021)

### A01:2021 – Broken Access Control

**Checks:**
- Authorization on all endpoints
- Resource-level access control
- No IDOR vulnerabilities
- CORS properly configured
- Directory traversal protection

**Patterns to Find:**
```javascript
// Dangerous: No auth check
app.get('/api/users/:id', (req, res) => {
  return db.getUser(req.params.id);
});

// Safe: Auth + ownership check
app.get('/api/users/:id', requireAuth, checkOwnership, (req, res) => {
  return db.getUser(req.params.id);
});
```

### A02:2021 – Cryptographic Failures

**Checks:**
- Sensitive data encrypted at rest
- TLS for data in transit
- Strong algorithms (no MD5, SHA1 for security)
- Proper key management
- No hardcoded secrets

**Patterns to Find:**
```javascript
// Dangerous
const hash = crypto.createHash('md5').update(password).digest('hex');

// Safe
const hash = await bcrypt.hash(password, 12);
```

### A03:2021 – Injection

**Checks:**
- SQL injection (parameterized queries)
- XSS (output encoding)
- Command injection
- LDAP injection
- NoSQL injection

**Patterns to Find:**
```javascript
// Dangerous: SQL injection
db.query(`SELECT * FROM users WHERE id = ${userId}`);

// Safe: Parameterized
db.query('SELECT * FROM users WHERE id = $1', [userId]);
```

### A04:2021 – Insecure Design

**Checks:**
- Threat modeling considerations
- Security requirements in spec
- Defense in depth
- Fail-secure defaults

### A05:2021 – Security Misconfiguration

**Checks:**
- No debug mode in production
- Secure defaults
- Error handling doesn't leak info
- Security headers configured
- Unnecessary features disabled

**Patterns to Find:**
```javascript
// Dangerous
app.use(errorHandler({ showStack: true }));

// Safe
app.use(errorHandler({ showStack: process.env.NODE_ENV === 'development' }));
```

### A06:2021 – Vulnerable Components

**Checks:**
- Dependencies with known CVEs
- Outdated packages
- Unmaintained dependencies
- License compliance

**Commands:**
```bash
npm audit
pip-audit
snyk test
```

### A07:2021 – Identification & Auth Failures

**Checks:**
- Strong password policy
- Rate limiting on auth
- Secure session management
- No credential exposure in logs
- MFA support (if required)

**Patterns to Find:**
```javascript
// Dangerous: Logging credentials
logger.info(`User login: ${email}, password: ${password}`);

// Safe
logger.info(`User login attempt: ${email}`);
```

### A08:2021 – Software & Data Integrity

**Checks:**
- Dependency integrity (lock files)
- Code signing (if applicable)
- CI/CD pipeline security

### A09:2021 – Security Logging & Monitoring

**Checks:**
- Security events logged
- No sensitive data in logs
- Log integrity protected
- Alerting configured

### A10:2021 – Server-Side Request Forgery

**Checks:**
- URL validation
- No open redirects
- Allowlist for external requests

**Patterns to Find:**
```javascript
// Dangerous: SSRF
const response = await fetch(userProvidedUrl);

// Safe: Allowlist
const allowedHosts = ['api.example.com'];
if (!allowedHosts.includes(new URL(url).hostname)) {
  throw new Error('Invalid URL');
}
```

## Security Review Report Template

```markdown
# Security Review: [Feature Name]

**Review ID:** SR-001
**Reviewer:** Security Reviewer Skill
**Date:** [Timestamp]
**Status:** [SECURE | WARNINGS | VULNERABILITIES FOUND]

## Summary

| Severity | Count | Categories |
|----------|-------|------------|
| Critical | 0 | — |
| High | 1 | A03 Injection |
| Medium | 2 | A01 Access Control |
| Low | 3 | A05 Misconfiguration |
| Info | 2 | Best practices |

## Findings

### HIGH: SQL Injection Vulnerability

**ID:** SEC-001
**OWASP:** A03:2021 Injection
**CWE:** CWE-89
**File:** src/api/users.ts:42

**Vulnerable Code:**
```typescript
const user = await db.query(`SELECT * FROM users WHERE id = ${id}`);
```

**Impact:**
Attacker could read, modify, or delete database records.

**Remediation:**
```typescript
const user = await db.query('SELECT * FROM users WHERE id = $1', [id]);
```

**References:**
- https://owasp.org/Top10/A03_2021-Injection/
- https://cwe.mitre.org/data/definitions/89.html

---

## Dependency Audit

| Package | Current | Vulnerable | Severity | CVE |
|---------|---------|------------|----------|-----|
| lodash | 4.17.19 | <4.17.21 | High | CVE-2021-23337 |

**Recommendation:** Run `npm audit fix` to resolve.

## Constitution Compliance

**Article 4 (Security):**
- [x] Auth required by default: Compliant
- [x] Secrets in environment variables: Compliant
- [ ] Input validation: 1 violation found

## Approval Recommendation

**CONDITIONAL** — Must fix HIGH severity finding before deployment.

### Required Actions
1. Fix SQL injection in users.ts:42
2. Update lodash to ≥4.17.21

### Next Step
After fixes applied, re-run security review.
```

## Pre-Execution Check

Before starting, update `.sigil/project-context.md`:
- Set **Current Phase** to `review`
- Set **Feature** to the feature being reviewed
- Set **Spec Path** to the active spec directory
- Set **Last Updated** to the current timestamp

If `.sigil/project-context.md` does not exist, create it using the State Tracking format from the `/sigil:draw` command.

## Workflow

```
1. Receive files and constitution for review
2. Load Article 4 security requirements
3. For each file:
   a. Scan for vulnerability patterns
   b. Check auth/authz patterns
   c. Identify sensitive data handling
   d. Flag security-relevant code
4. Run dependency audit:
   a. npm audit / pip-audit / etc.
   b. Check for known CVEs
   c. Flag outdated dependencies
5. Check constitution compliance
6. Compile findings by severity
7. Determine approval recommendation:
   - No high/critical → Approve
   - High/critical found → Conditional/Block
8. Generate security report
9. Return results
```

## Severity Classification

### Critical
Immediate exploitation risk:
- Remote code execution
- Authentication bypass
- SQL injection with data exposure
- Hardcoded production credentials

**Action:** Block deployment, fix immediately.

### High
Significant risk requiring exploit:
- Privilege escalation
- Stored XSS
- Sensitive data exposure
- Broken access control

**Action:** Fix before deployment.

### Medium
Limited exploitation potential:
- CSRF without sensitive action
- Information disclosure (non-sensitive)
- Session fixation
- Reflected XSS (limited context)

**Action:** Fix in current release.

### Low
Minimal impact:
- Verbose error messages
- Missing security headers
- Outdated (non-vulnerable) dependencies

**Action:** Track and address in maintenance.

### Info
Best practice recommendations:
- Security hardening opportunities
- Defense in depth suggestions

**Action:** Consider for future improvement.

## Escalation Triggers

**Immediately escalate when:**
- Critical or high severity finding
- Active vulnerability pattern
- Credentials or secrets exposed
- Production data at risk
- Compliance violation (GDPR, HIPAA, etc.)

## Error Handling

### Cannot Determine Risk
```
Unable to assess security risk for: [Pattern]
Context: [Why assessment failed]

Recommend: Manual security review by human.
```

### Audit Tool Failure
```
Dependency audit failed: [Error]

Options:
A) Retry with different tool
B) Manual dependency review
C) Escalate to DevOps
```

## Integration

### Receiving from code-reviewer
```json
{
  "handoff_from": "code-reviewer",
  "review_status": "approved",
  "security_relevant_files": ["src/auth.ts"],
  "code_review_report": "/.sigil/specs/.../reviews/code-review.md"
}
```

### Passing to deploy-checker
```json
{
  "handoff_to": "deploy-checker",
  "security_status": "approved",
  "security_report": "/.sigil/specs/.../reviews/security-review.md",
  "conditions": [],
  "blocked": false
}
```

## Notes

- Err on the side of caution; flag uncertain patterns
- Consider context (internal vs external facing)
- Check for security by design, not just absence of bugs
- Reference OWASP and CWE for authority
- Critical/High findings require human approval tier

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-20 | Initial release |
