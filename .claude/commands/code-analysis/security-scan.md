# Security Scan

Run comprehensive security analysis including vulnerability scanning and dependency checks.

## Usage
/security-scan [path] [--include-deps] [--severity critical|high|medium|low]

## What This Does
1. Scans code for security vulnerabilities and injection risks
2. Checks authentication/authorization patterns and secrets management
3. Optionally scans dependencies for known vulnerabilities
4. Generates security report with prioritized remediation steps

## Example
/security-scan src/api --include-deps --severity high

## Agent Coordination
1. **security-auditor**: Primary security analysis (code patterns, auth/authz, input validation)
2. **dependency-scanner**: Dependency security if --include-deps (vulnerabilities, license compliance)
3. **Main LLM**: Synthesizes findings and formats report

## Output
Comprehensive security report including:
```markdown
## Security Scan Report

### Summary
- Files scanned: 24
- Vulnerabilities found: 3 critical, 5 high, 12 medium
- Dependencies scanned: 156
- Security score: 72/100 (target: >80)

### Critical Vulnerabilities
1. **SQL Injection Risk** - src/api/users.ts:45
   - Severity: CRITICAL
   - Description: Unsanitized user input in SQL query
   - Impact: Database compromise possible
   - Remediation: Use parameterized queries
   - Code: `db.query('SELECT * FROM users WHERE id=' + userId)`
   - Fix: `db.query('SELECT * FROM users WHERE id=$1', [userId])`

2. **Hardcoded Secret** - src/config/db.ts:12
   - Severity: CRITICAL
   - Description: Database password in source code
   - Impact: Credential exposure in version control
   - Remediation: Move to environment variables
   - Code: `const password = 'prod_db_pass_123'`
   - Fix: `const password = process.env.DB_PASSWORD`

3. **Missing Authentication** - src/api/admin.ts:78
   - Severity: CRITICAL
   - Description: Admin endpoint lacks authentication
   - Impact: Unauthorized access to admin functions
   - Remediation: Add authentication middleware

### High Severity Issues
4. **XSS Vulnerability** - src/views/profile.tsx:34
5. **CSRF Token Missing** - src/api/payment.ts:56
6. **Weak Password Hash** - src/auth/password.ts:23
7. **Unvalidated Redirect** - src/api/oauth.ts:89
8. **Information Disclosure** - src/api/errors.ts:12

### Dependency Vulnerabilities
- lodash@4.17.15: Prototype pollution (CVE-2020-8203) - CRITICAL
- express@4.16.0: Denial of Service (CVE-2022-24999) - HIGH
- jsonwebtoken@8.5.0: Signature bypass (CVE-2022-23529) - HIGH

### Recommendations
1. **Immediate Actions** (Critical)
   - Fix SQL injection in users.ts
   - Remove hardcoded credentials
   - Add authentication to admin endpoints

2. **Short-term** (High)
   - Implement XSS prevention
   - Add CSRF protection
   - Upgrade vulnerable dependencies

3. **Long-term** (Medium)
   - Implement security headers
   - Add rate limiting
   - Set up security monitoring

### Compliance Status
- OWASP Top 10: 3 violations found
- CWE Coverage: 156/200 categories checked
- Security Headers: 4/10 missing
```

Returns: Comprehensive security report with prioritized remediation steps

## See Also
For related commands, see [Quality Commands](../shared/related-quality-commands.md)
