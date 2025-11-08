---
template_id: security-audit-checklist
template_name: Security Audit Checklist
category: security
difficulty: advanced
estimated_time: 8-12 hours
tags: [security, audit, owasp, compliance, penetration-testing]
author: claude-oak-agents
version: 1.0.0
last_updated: 2025-11-08
popularity: 93
dependencies: [owasp-zap, nmap, burp-suite]
related_templates: [saas-auth-complete, rest-crud-api]
---

# Security Audit Checklist

Comprehensive security review framework covering OWASP Top 10, infrastructure security, and compliance requirements.

## Overview

This template provides a systematic security audit process including:
- OWASP Top 10 vulnerability assessment
- Infrastructure security review (AWS, Azure, GCP)
- Authentication and authorization audit
- Data protection and encryption review
- Dependency and supply chain security
- Compliance validation (GDPR, SOC2, HIPAA)
- Penetration testing procedures

## Use Cases

- **Pre-Production Security Review**: Validate security before launch
- **Periodic Security Audits**: Quarterly or annual security assessments
- **Incident Response**: Post-breach security review
- **Compliance Certification**: SOC2, ISO27001, HIPAA compliance prep
- **Third-Party Security Assessment**: Vendor security evaluation

## Requirements

### Technical Prerequisites
- Application access (staging environment preferred)
- Source code repository access
- Infrastructure access (cloud console, SSH)
- Security scanning tools (OWASP ZAP, Burp Suite, Nmap)
- Static analysis tools (SonarQube, Snyk, Bandit)

### Documentation Required
- Architecture diagrams
- Data flow diagrams
- Authentication/authorization design
- Infrastructure topology
- Dependency list (package.json, requirements.txt, etc.)

## Implementation Plan

### Phase 1: Information Gathering (2 hours)

**1.1 Application Reconnaissance**
- Map all endpoints and routes
- Identify authentication mechanisms
- Document data flows
- Review architecture diagrams
- List third-party integrations

**1.2 Technology Stack Analysis**
```yaml
technology_inventory:
  frontend:
    framework: React 18.2.0
    dependencies: [react-router, axios, zod]

  backend:
    framework: Express 4.18.2
    runtime: Node.js 18.x
    database: PostgreSQL 15
    cache: Redis 7.0
    dependencies: [jsonwebtoken, bcrypt, prisma]

  infrastructure:
    cloud_provider: AWS
    services: [EC2, RDS, S3, CloudFront, Lambda]
    iac: AWS CDK (TypeScript)

  security_tools:
    - helmet.js (security headers)
    - express-rate-limit (rate limiting)
    - cors (CORS policy)
```

### Phase 2: OWASP Top 10 Assessment (4 hours)

**2.1 A01:2021 - Broken Access Control**

**Checks**:
- [ ] Authorization enforced on all protected endpoints
- [ ] User cannot access other users' data (IDOR test)
- [ ] Admin functions require admin role
- [ ] Direct object references use UUIDs (not sequential IDs)
- [ ] File upload restrictions (type, size, location)
- [ ] API endpoints validate user permissions

**Test Procedure**:
```bash
# IDOR (Insecure Direct Object Reference) test
curl -H "Authorization: Bearer USER1_TOKEN" \
  https://api.example.com/users/USER2_ID

# Expected: 403 Forbidden
# Actual: 200 OK with USER2 data? → VULNERABILITY
```

**2.2 A02:2021 - Cryptographic Failures**

**Checks**:
- [ ] HTTPS enforced (no HTTP allowed)
- [ ] TLS 1.2+ only (no SSLv3, TLS 1.0/1.1)
- [ ] Strong cipher suites configured
- [ ] Passwords hashed with bcrypt/Argon2 (cost factor ≥12)
- [ ] Sensitive data encrypted at rest (AES-256)
- [ ] Secrets not hardcoded in source code
- [ ] Database connections encrypted (SSL/TLS)

**Test Procedure**:
```bash
# Check TLS version and ciphers
nmap --script ssl-enum-ciphers -p 443 example.com

# Verify password hashing
# Check database: Password column should store bcrypt/Argon2 hashes
SELECT password FROM users LIMIT 1;
# Expected: $2b$12$... (bcrypt) or $argon2id$... (Argon2)
```

**2.3 A03:2021 - Injection**

**Checks**:
- [ ] SQL queries use parameterized statements (no string concatenation)
- [ ] NoSQL queries sanitized (MongoDB, DynamoDB)
- [ ] OS command injection prevented (no shell execution with user input)
- [ ] LDAP injection prevented
- [ ] XML injection prevented (XXE disabled)
- [ ] Input validation on all user inputs

**Test Procedure**:
```bash
# SQL injection test
curl -X POST https://api.example.com/login \
  -d "email=admin' OR '1'='1&password=anything"

# Expected: 400 Bad Request (validation error)
# Actual: 200 OK (logged in)? → VULNERABILITY

# Command injection test
curl https://api.example.com/ping?host=8.8.8.8;cat%20/etc/passwd

# Expected: 400 Bad Request
# Actual: File contents returned? → VULNERABILITY
```

**2.4 A04:2021 - Insecure Design**

**Checks**:
- [ ] Rate limiting on authentication endpoints
- [ ] Account lockout after failed login attempts
- [ ] Password reset tokens single-use and time-limited
- [ ] Business logic validated (e.g., negative quantity prevention)
- [ ] Race condition prevention (idempotency keys)
- [ ] Security requirements in design phase

**2.5 A05:2021 - Security Misconfiguration**

**Checks**:
- [ ] Security headers configured (CSP, X-Frame-Options, etc.)
- [ ] Default credentials changed
- [ ] Unnecessary services disabled
- [ ] Error messages don't leak sensitive info
- [ ] Directory listing disabled
- [ ] Admin panel not publicly accessible
- [ ] CORS policy restrictive (not `*` in production)

**Test Procedure**:
```bash
# Check security headers
curl -I https://example.com

# Should include:
# Strict-Transport-Security: max-age=31536000
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff
# Content-Security-Policy: default-src 'self'
```

**2.6 A06:2021 - Vulnerable and Outdated Components**

**Checks**:
- [ ] All dependencies up-to-date (npm audit, pip-audit)
- [ ] No critical/high severity vulnerabilities
- [ ] Dependency scanning in CI/CD pipeline
- [ ] SBOMs (Software Bill of Materials) maintained
- [ ] Automated dependency updates (Dependabot, Renovate)

**Test Procedure**:
```bash
# NPM audit
npm audit --audit-level=high

# Python dependencies
pip-audit

# Expected: 0 vulnerabilities
# Actual: Critical/high vulnerabilities? → MUST FIX
```

**2.7 A07:2021 - Identification and Authentication Failures**

**Checks**:
- [ ] Passwords meet complexity requirements (12+ chars)
- [ ] Multi-factor authentication available
- [ ] Session IDs regenerated after login
- [ ] Logout invalidates session/token
- [ ] Password reset flow secure (token, email verification)
- [ ] Brute force protection (rate limiting, CAPTCHA)
- [ ] No credentials in URLs or logs

**2.8 A08:2021 - Software and Data Integrity Failures**

**Checks**:
- [ ] CI/CD pipeline secured (no unauthorized access)
- [ ] Dependencies verified (integrity hashes, SRI)
- [ ] Auto-update mechanism secure
- [ ] Unsigned packages rejected
- [ ] Code signing for releases

**2.9 A09:2021 - Security Logging and Monitoring Failures**

**Checks**:
- [ ] Authentication events logged (login, logout, failed attempts)
- [ ] Authorization failures logged
- [ ] Input validation failures logged
- [ ] Security events monitored (alerts configured)
- [ ] Logs protected from tampering
- [ ] PII not logged (passwords, tokens, credit cards)

**2.10 A10:2021 - Server-Side Request Forgery (SSRF)**

**Checks**:
- [ ] URL validation on server-side requests
- [ ] Whitelist of allowed domains/IPs
- [ ] Prevent requests to internal network (169.254.x.x, 10.x.x.x)
- [ ] Disable HTTP redirects (or validate redirect targets)

### Phase 3: Infrastructure Security (2 hours)

**3.1 AWS Security Checklist**

**IAM**:
- [ ] Root account MFA enabled
- [ ] IAM users have MFA
- [ ] Principle of least privilege applied
- [ ] No long-term access keys (use IAM roles)
- [ ] IAM Access Analyzer enabled
- [ ] Password policy enforced (14+ chars, rotation)

**Network**:
- [ ] VPC configured with public/private subnets
- [ ] Security groups restrictive (no 0.0.0.0/0 on SSH)
- [ ] NACLs configured
- [ ] VPC Flow Logs enabled
- [ ] AWS WAF configured (rate limiting, geo-blocking)

**Data**:
- [ ] S3 buckets not publicly accessible
- [ ] S3 bucket encryption enabled (AES-256 or KMS)
- [ ] RDS encryption at rest enabled
- [ ] RDS automated backups enabled
- [ ] Secrets Manager for sensitive data (not environment variables)

**Monitoring**:
- [ ] CloudTrail enabled (all regions)
- [ ] CloudWatch alarms configured
- [ ] GuardDuty enabled (threat detection)
- [ ] Security Hub enabled (compliance dashboards)
- [ ] Config rules for compliance monitoring

**3.2 Container Security**

**Docker**:
- [ ] Base images from trusted sources
- [ ] Images scanned for vulnerabilities (Trivy, Snyk)
- [ ] Non-root user in Dockerfile
- [ ] Minimal image size (multi-stage builds)
- [ ] No secrets in images (use secret management)

**Kubernetes**:
- [ ] RBAC configured (least privilege)
- [ ] Network policies defined
- [ ] Pod Security Standards enforced
- [ ] Secrets stored in Kubernetes Secrets (or external vault)
- [ ] Runtime security (Falco, Aqua Security)

### Phase 4: Authentication & Authorization Audit (1 hour)

**4.1 Authentication Review**

**Checks**:
- [ ] Strong password policy (12+ chars, complexity)
- [ ] MFA available and encouraged
- [ ] Session timeout configured (15-30 min idle)
- [ ] Secure password reset flow (email verification, token expiry)
- [ ] Account lockout after 5 failed attempts
- [ ] No credentials in source code

**4.2 Authorization Review**

**Checks**:
- [ ] Role-Based Access Control (RBAC) implemented
- [ ] Authorization enforced on all endpoints (not just UI)
- [ ] Horizontal privilege escalation prevented (user A cannot access user B data)
- [ ] Vertical privilege escalation prevented (user cannot become admin)
- [ ] API endpoints validate permissions (not just authentication)

### Phase 5: Data Protection Audit (1 hour)

**5.1 Data Classification**

**Classify Data**:
- **Public**: Marketing content, documentation
- **Internal**: Business data, analytics
- **Confidential**: User PII, financial data
- **Restricted**: Passwords, payment details, health records

**5.2 Encryption Requirements**

**Checks**:
- [ ] Data in transit encrypted (TLS 1.2+)
- [ ] Data at rest encrypted (AES-256)
- [ ] Database encryption enabled
- [ ] Backups encrypted
- [ ] File uploads encrypted (if containing PII)
- [ ] Key rotation policy defined (90 days)

**5.3 Data Retention and Deletion**

**Checks**:
- [ ] Data retention policy documented
- [ ] Automatic data deletion implemented (GDPR right to be forgotten)
- [ ] Backups respect retention policy
- [ ] Soft delete for audit trail
- [ ] Hard delete for sensitive data

### Phase 6: Compliance Validation (2 hours)

**6.1 GDPR Compliance**

**Checks**:
- [ ] Privacy policy available
- [ ] Cookie consent banner
- [ ] Data processing agreement (DPA) with vendors
- [ ] User consent recorded for data processing
- [ ] Right to access (data export)
- [ ] Right to erasure (account deletion)
- [ ] Data breach notification process (72 hours)

**6.2 SOC 2 Compliance**

**Checks**:
- [ ] Access controls documented
- [ ] Change management process
- [ ] Incident response plan
- [ ] Vendor risk assessment
- [ ] Security awareness training
- [ ] Audit logs retained (1 year)

**6.3 HIPAA Compliance (if applicable)**

**Checks**:
- [ ] PHI encrypted in transit and at rest
- [ ] Access controls for PHI
- [ ] Audit logs for PHI access
- [ ] Business Associate Agreements (BAA) signed
- [ ] Risk assessment completed

## Agent Workflow

```yaml
agent_sequence:
  phase_1_reconnaissance:
    - agent: security-auditor
      task: "Map application attack surface and technology stack"
      duration: "2 hours"

  phase_2_vulnerability_assessment:
    - agent: security-auditor
      task: "OWASP Top 10 assessment with automated and manual testing"
      duration: "4 hours"

  phase_3_infrastructure_review:
    - agent: infrastructure-specialist
      task: "AWS/cloud security configuration review"
      duration: "2 hours"

    - agent: security-auditor
      task: "Container and Kubernetes security audit"
      duration: "1 hour"

  phase_4_code_review:
    - agent: security-auditor
      task: "Static code analysis and secure coding review"
      duration: "2 hours"

  phase_5_compliance:
    - agent: security-auditor
      task: "GDPR, SOC2, HIPAA compliance validation"
      duration: "2 hours"

  phase_6_reporting:
    - agent: security-auditor
      task: "Compile findings, prioritize risks, create remediation plan"
      duration: "2 hours"

    - agent: git-workflow-manager
      task: "Create security report and remediation tracking issues"
```

## Testing Methodology

### Automated Scanning
```bash
# OWASP ZAP automated scan
zap-cli quick-scan --self-contained --start-options "-config api.disablekey=true" \
  https://staging.example.com

# Dependency scanning
npm audit --audit-level=moderate
snyk test

# Static analysis
sonarqube-scanner \
  -Dsonar.projectKey=my-project \
  -Dsonar.sources=src

# Container scanning
trivy image myapp:latest
```

### Manual Testing
- Burp Suite for manual penetration testing
- Authentication bypass attempts
- Authorization bypass attempts (IDOR, privilege escalation)
- Business logic testing (negative quantities, race conditions)

## Risk Prioritization

### Severity Levels

**Critical** (Fix immediately):
- SQL injection
- Authentication bypass
- Hardcoded credentials
- Data exposure (public S3 buckets)

**High** (Fix within 1 week):
- XSS vulnerabilities
- CSRF vulnerabilities
- Missing rate limiting
- Outdated dependencies (critical CVEs)

**Medium** (Fix within 1 month):
- Missing security headers
- Information disclosure
- Weak password policy
- Moderate dependency vulnerabilities

**Low** (Fix as time permits):
- Missing HSTS header
- HTTP methods not restricted
- Verbose error messages
- Minor dependency updates

## Remediation Plan Template

```markdown
## Security Finding: SQL Injection in Login Endpoint

**Severity**: Critical
**CVSS Score**: 9.8 (Critical)
**Affected Component**: /api/login endpoint
**Vulnerability Type**: CWE-89 (SQL Injection)

### Description
The login endpoint constructs SQL queries using string concatenation with user input, allowing SQL injection attacks.

### Proof of Concept
```bash
curl -X POST https://api.example.com/login \
  -d "email=admin' OR '1'='1&password=anything"
# Result: Authentication bypass
```

### Impact
- Complete database compromise
- Authentication bypass (admin access)
- Data exfiltration
- Data manipulation/deletion

### Remediation
1. Replace string concatenation with parameterized queries
2. Implement input validation (email format, max length)
3. Add WAF rules to block SQL injection patterns

### Code Fix
```typescript
// BEFORE (vulnerable)
const query = `SELECT * FROM users WHERE email = '${email}' AND password = '${hash}'`;

// AFTER (secure)
const query = 'SELECT * FROM users WHERE email = $1 AND password = $2';
const result = await db.query(query, [email, hash]);
```

### Verification
- [ ] Code review confirms fix implemented
- [ ] Unit tests verify parameterized queries
- [ ] Penetration test confirms vulnerability resolved
- [ ] No similar vulnerabilities in codebase (grep audit)

### Timeline
- Discovery: 2025-11-08
- Reported: 2025-11-08
- Fixed: TBD (Target: 2025-11-09)
- Verified: TBD
```

## Common Pitfalls

### 1. False Sense of Security
**Problem**: Passing automated scans doesn't mean application is secure
**Solution**: Combine automated + manual testing, business logic review

### 2. Ignoring Low Severity Findings
**Problem**: Multiple low severity issues can combine into high risk
**Solution**: Fix all findings, prioritize by exploitability

### 3. No Retesting
**Problem**: Assuming fixes work without verification
**Solution**: Retest all findings after remediation

### 4. Security as Afterthought
**Problem**: Bolting on security after development complete
**Solution**: Security reviews at design phase, ongoing testing

### 5. Insufficient Scope
**Problem**: Only testing web application, ignoring infrastructure
**Solution**: Holistic approach (app + infrastructure + dependencies)

## Success Criteria

- [ ] OWASP Top 10 assessment completed
- [ ] Infrastructure security reviewed
- [ ] Dependency scanning passed (0 critical/high CVEs)
- [ ] Authentication and authorization audited
- [ ] Data protection measures validated
- [ ] Compliance requirements verified
- [ ] Security report generated with risk scores
- [ ] Remediation plan created with timelines
- [ ] Executive summary for leadership
- [ ] Technical details for engineering team

## Deliverables

1. **Executive Summary** (1-2 pages)
   - Overall security posture (Low/Medium/High risk)
   - Critical findings count
   - Compliance status
   - Recommended next steps

2. **Technical Report** (10-30 pages)
   - Methodology
   - Findings (severity, impact, remediation)
   - Evidence (screenshots, logs, code snippets)
   - Remediation timeline

3. **Remediation Tracking**
   - GitHub issues for each finding
   - Assigned owners
   - Target fix dates
   - Verification checklist

4. **Retest Report** (after fixes)
   - Verification of all fixes
   - Residual risk assessment
   - Sign-off for production deployment

## Timeline Example

**Week 1**: Information gathering + automated scanning
**Week 2**: Manual testing (OWASP Top 10, penetration testing)
**Week 3**: Infrastructure and compliance review
**Week 4**: Report writing and remediation planning
**Week 5+**: Retest after fixes implemented
