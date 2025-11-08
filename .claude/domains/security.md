---
domain: security
priority: 2
primary_agent: security-auditor
secondary_agents: [dependency-scanner, infrastructure-specialist, qa-specialist]
related_agents: [systems-architect, debug-specialist]
---

# Domain: Security & Compliance

## Tech Stack

### Security Tools
- **SAST (Static Analysis)**: ESLint security plugins, Semgrep, SonarQube
- **DAST (Dynamic Analysis)**: OWASP ZAP, Burp Suite
- **Dependency Scanning**: npm audit, Snyk, Dependabot, OWASP Dependency-Check
- **Container Scanning**: Docker scan, Trivy, Clair, Anchore
- **Secret Scanning**: git-secrets, TruffleHog, GitGuardian
- **Code Review**: CodeQL, Checkmarx

### AWS Security Services
- **IAM**: Identity and Access Management
- **KMS**: Key Management Service (encryption keys)
- **Secrets Manager**: Secure credential storage
- **WAF**: Web Application Firewall
- **Shield**: DDoS protection
- **GuardDuty**: Threat detection
- **Security Hub**: Centralized security findings
- **Inspector**: Vulnerability assessment
- **CloudTrail**: API audit logging
- **Config**: Resource compliance monitoring

### Authentication & Authorization
- **JWT**: JSON Web Tokens for stateless auth
- **OAuth 2.0**: Third-party authorization
- **SAML**: Enterprise SSO
- **API Keys**: Service-to-service authentication
- **MFA**: Multi-Factor Authentication (AWS Cognito, Auth0)

### Encryption
- **At Rest**: KMS, S3 encryption, RDS encryption, DynamoDB encryption
- **In Transit**: TLS 1.2+, HTTPS, SSL certificates (ACM)
- **End-to-End**: Application-level encryption

### Compliance & Standards
- **OWASP Top 10**: Web application security risks
- **CIS Benchmarks**: Security configuration standards
- **PCI DSS**: Payment card security
- **HIPAA**: Healthcare data protection
- **GDPR**: Data privacy regulations
- **SOC 2**: Security, availability, confidentiality

## Patterns & Conventions

### Security-First Development
1. **Shift Left**: Security testing early in development
2. **Defense in Depth**: Multiple layers of security
3. **Least Privilege**: Minimal required permissions
4. **Zero Trust**: Never trust, always verify
5. **Fail Secure**: Default to secure state on errors

### Secure Coding Practices
1. **Input Validation**: Validate all user inputs
2. **Output Encoding**: Prevent XSS attacks
3. **Parameterized Queries**: Prevent SQL injection
4. **Error Handling**: Don't leak sensitive information
5. **Logging**: Audit security-relevant events (no sensitive data)

### Authentication Patterns
1. **Password Requirements**: Strong password policies
2. **Token Management**: Secure JWT storage and rotation
3. **Session Management**: Secure session handling, timeout
4. **MFA Enforcement**: Multi-factor for sensitive operations
5. **Account Lockout**: Prevent brute force attacks

### Authorization Patterns
1. **RBAC (Role-Based Access Control)**: Permissions based on roles
2. **ABAC (Attribute-Based Access Control)**: Fine-grained policies
3. **ACL (Access Control Lists)**: Resource-level permissions
4. **IAM Policies**: AWS resource permissions
5. **API Gateway Authorizers**: Lambda-based authorization

### Data Protection
1. **Encryption at Rest**: Encrypt databases, S3, volumes
2. **Encryption in Transit**: TLS for all communications
3. **Data Masking**: Hide sensitive data in logs/UI
4. **Tokenization**: Replace sensitive data with tokens
5. **Secure Deletion**: Securely wipe sensitive data

### Secret Management
1. **AWS Secrets Manager**: Automatic rotation, versioning
2. **Parameter Store**: Non-sensitive configuration
3. **Environment Variables**: Runtime secrets (not in code)
4. **No Hardcoded Secrets**: Never commit secrets to git
5. **Secret Rotation**: Regular credential updates

### Network Security
1. **VPC Isolation**: Private subnets for sensitive resources
2. **Security Groups**: Stateful firewall rules
3. **NACLs**: Network-level access control
4. **WAF Rules**: Protect against common attacks
5. **API Gateway Throttling**: Rate limiting

## Security Workflows

### Threat Modeling
```
1. Identify Assets: What needs protection?
2. Identify Threats: What can go wrong?
3. Identify Vulnerabilities: Where are weaknesses?
4. Assess Risk: Likelihood × Impact
5. Define Mitigations: How to reduce risk?
6. Validate: Test security controls
```

### Secure Development Lifecycle
```
Requirements → Threat Modeling → Secure Design → Secure Coding →
Security Testing → Security Review → Deploy → Monitor → Respond
```

### Incident Response
```
1. Detect: Identify security incident
2. Contain: Limit damage
3. Eradicate: Remove threat
4. Recover: Restore services
5. Post-Mortem: Learn and improve
```

## Agent Workflows

### Security Review (All Changes)
**Trigger**: Any code change, infrastructure update
```
[primary-agent] → security-auditor → [continue workflow]
```

### Dependency Security Scan
**Trigger**: "Check dependencies for vulnerabilities", "Run security audit"
```
dependency-scanner → security-auditor (review findings) → [fix if needed]
```

### Authentication Implementation
**Trigger**: "Add JWT authentication", "Implement OAuth login"
```
spec-manager → security-auditor (design review) → infrastructure-specialist (implementation) → security-auditor (code review) → qa-specialist → git-workflow-manager
```

### API Security Hardening
**Trigger**: "Secure API endpoints", "Add rate limiting"
```
security-auditor (assessment) → infrastructure-specialist (implementation) → security-auditor (verification) → qa-specialist
```

### Secrets Management Setup
**Trigger**: "Move secrets to Secrets Manager", "Rotate API keys"
```
security-auditor (identify secrets) → infrastructure-specialist (setup Secrets Manager) → security-auditor (verify) → git-workflow-manager
```

### Vulnerability Remediation
**Trigger**: "Fix CVE-2024-1234", "Update vulnerable dependency"
```
dependency-scanner (identify) → security-auditor (assess risk) → infrastructure-specialist (fix) → dependency-scanner (verify) → qa-specialist → git-workflow-manager
```

### Penetration Testing
**Trigger**: "Perform security audit", "Pen test application"
```
security-auditor (automated scans + manual testing) → [document findings] → infrastructure-specialist (remediation) → security-auditor (retest)
```

## Triggers

### Keywords
- **Security**: security, secure, auth, authorization, authentication
- **Vulnerabilities**: vulnerability, CVE, exploit, patch, fix
- **Encryption**: encrypt, decrypt, TLS, SSL, certificate
- **Secrets**: secret, password, API key, credential, token
- **Attacks**: XSS, SQL injection, CSRF, DDoS, malware
- **Compliance**: OWASP, PCI, HIPAA, GDPR, compliance, audit
- **Access Control**: IAM, permission, role, policy, RBAC
- **Monitoring**: intrusion, threat, GuardDuty, WAF

### File Patterns
- `src/auth/**/*`, `src/security/**/*`
- `*.security.ts`, `*.auth.ts`
- `package.json`, `package-lock.json`, `yarn.lock`
- `Dockerfile`, `docker-compose.yml`
- `serverless.yml`, `lib/**/*.ts` (CDK)
- `.env.example` (check for secrets)
- `iam/**/*`, `policies/**/*`

### Tech Stack Mentions
- JWT, OAuth, SAML
- AWS IAM, KMS, Secrets Manager, WAF
- Snyk, npm audit, Dependabot
- OWASP ZAP, Burp Suite
- Docker scan, Trivy

## Quality Standards

### Security Code Review Checklist
- [ ] No hardcoded secrets or credentials
- [ ] Input validation on all user inputs
- [ ] Output encoding to prevent XSS
- [ ] Parameterized queries (no SQL injection)
- [ ] Proper error handling (no info leakage)
- [ ] Authentication on protected endpoints
- [ ] Authorization checks before data access
- [ ] HTTPS enforced for all communications
- [ ] Secrets stored in Secrets Manager
- [ ] Logging without sensitive data
- [ ] Rate limiting on public APIs
- [ ] CORS properly configured

### Dependency Security Standards
- Zero high or critical vulnerabilities in production
- Regular dependency updates (monthly)
- Automated dependency scanning in CI/CD
- Review and approve all dependency updates
- Pin dependency versions (no wildcards)

### Infrastructure Security Standards
- All data encrypted at rest (RDS, S3, DynamoDB)
- TLS 1.2+ for all communications
- IAM least-privilege policies
- Security groups with minimal access
- Private subnets for databases
- WAF enabled for public APIs
- CloudTrail enabled for audit
- GuardDuty enabled for threat detection

### Authentication Requirements
- Strong password policy (12+ chars, complexity)
- Password hashing (bcrypt, Argon2)
- JWT with short expiration (15 min access, 7 day refresh)
- MFA for admin accounts
- Account lockout after failed attempts
- Secure session management

### Authorization Requirements
- Role-based access control (RBAC)
- Verify permissions on every request
- No client-side authorization only
- Audit logs for permission changes
- Regular access reviews

## Common Security Tasks

### Implementing JWT Authentication
1. **Setup**:
   - Install jsonwebtoken library
   - Generate RSA key pair or shared secret
   - Store secret in AWS Secrets Manager

2. **Login Flow**:
   - Validate username/password
   - Hash password comparison (bcrypt)
   - Generate access token (15 min expiry)
   - Generate refresh token (7 day expiry)
   - Return both tokens

3. **Authentication Middleware**:
   - Extract token from Authorization header
   - Verify token signature
   - Check token expiration
   - Attach user to request object
   - Handle invalid/expired tokens

4. **Token Refresh**:
   - Validate refresh token
   - Generate new access token
   - Optionally rotate refresh token

### Input Validation
1. **Validation Library**: Use Joi, Zod, or class-validator
2. **Validate All Inputs**:
   - Query parameters
   - Path parameters
   - Request body
   - Headers
3. **Sanitization**: Remove/escape dangerous characters
4. **Type Checking**: Ensure correct data types
5. **Range Checks**: Min/max values, length limits
6. **Whitelist**: Allow only expected values

### Preventing SQL Injection
1. **Use ORM/Query Builder**: Sequelize, TypeORM, Prisma
2. **Parameterized Queries**: Never concatenate SQL
3. **Input Validation**: Validate before using in queries
4. **Least Privilege**: Database user with minimal permissions
5. **Error Handling**: Don't expose SQL errors to users

### Preventing XSS
1. **Output Encoding**: Escape HTML, JavaScript, URLs
2. **Content Security Policy**: CSP headers
3. **Input Validation**: Reject scripts in user input
4. **Use Framework Protections**: React auto-escapes
5. **Sanitize HTML**: DOMPurify for rich text

### Secrets Management
1. **Identify Secrets**: API keys, passwords, tokens, certificates
2. **Create Secrets in AWS**:
   ```bash
   aws secretsmanager create-secret \
     --name prod/api/stripe-key \
     --secret-string "sk_live_xyz"
   ```
3. **Retrieve at Runtime**:
   ```typescript
   const secret = await secretsManager.getSecretValue({
     SecretId: 'prod/api/stripe-key'
   }).promise();
   ```
4. **Rotate Regularly**: Set up automatic rotation
5. **Audit Access**: CloudTrail logs secret access

### Setting Up WAF
1. **Create WAF Web ACL**
2. **Add Managed Rules**:
   - Core Rule Set (OWASP Top 10)
   - Known Bad Inputs
   - SQL Injection
   - Linux/Windows OS rules
3. **Custom Rules**:
   - Rate limiting (e.g., 2000 req/5min per IP)
   - Geo-blocking if needed
   - IP whitelist/blacklist
4. **Associate with Resources**: ALB, CloudFront, API Gateway
5. **Monitor**: CloudWatch metrics, sampled requests

### Dependency Scanning
1. **Run npm audit**: `npm audit` or `yarn audit`
2. **Review Vulnerabilities**: Check severity and exploitability
3. **Update Dependencies**: `npm audit fix` or manual updates
4. **Breaking Changes**: Test after updates
5. **Snyk Integration**: `npx snyk test`, monitor continuously
6. **CI/CD Integration**: Fail builds on high/critical vulnerabilities

## Integration Points

### Frontend Integration
- **Authentication Tokens**: Secure storage (httpOnly cookies)
- **CORS Configuration**: Whitelist frontend domains
- **CSP Headers**: Content Security Policy
- **Input Validation**: Client-side + server-side
- **XSS Prevention**: Output encoding

### Backend Integration
- **Authentication Middleware**: Protect endpoints
- **Authorization Logic**: Check permissions
- **Input Validation**: Sanitize all inputs
- **Secrets Access**: Retrieve from Secrets Manager
- **Audit Logging**: Log security events

### Infrastructure Integration
- **IAM Policies**: Least-privilege access
- **KMS Encryption**: Encrypt S3, RDS, DynamoDB
- **WAF Rules**: Protect APIs and websites
- **Security Groups**: Network-level firewall
- **Secrets Manager**: Centralized secret storage

### Data Integration
- **Encryption**: Encrypt sensitive columns
- **Access Control**: Database-level permissions
- **Audit Logging**: Track data access
- **Data Masking**: Hide sensitive data in non-prod

## Domain-Specific Commands

### Dependency Scanning
```bash
# npm audit
npm audit
npm audit --json
npm audit fix

# Yarn audit
yarn audit
yarn audit --json

# Snyk
npx snyk test
npx snyk monitor
snyk test --severity-threshold=high

# OWASP Dependency Check
dependency-check --project myapp --scan .
```

### Container Scanning
```bash
# Docker scan
docker scan myapp:latest
docker scan --severity high myapp:latest

# Trivy
trivy image myapp:latest
trivy image --severity HIGH,CRITICAL myapp:latest

# Anchore
anchore-cli image add myapp:latest
anchore-cli image vuln myapp:latest all
```

### Secret Scanning
```bash
# git-secrets
git secrets --scan
git secrets --scan-history

# TruffleHog
trufflehog git file://. --since-commit HEAD~10

# gitleaks
gitleaks detect --source . --verbose
```

### AWS Security Commands
```bash
# IAM policy validation
aws accessanalyzer validate-policy --policy-document file://policy.json

# Secrets Manager
aws secretsmanager create-secret --name my-secret --secret-string "value"
aws secretsmanager get-secret-value --secret-id my-secret
aws secretsmanager rotate-secret --secret-id my-secret

# KMS
aws kms create-key --description "My encryption key"
aws kms encrypt --key-id <key-id> --plaintext "secret"
aws kms decrypt --ciphertext-blob <encrypted>

# Security Hub findings
aws securityhub get-findings

# GuardDuty findings
aws guardduty list-findings --detector-id <id>
```

### OWASP ZAP
```bash
# Active scan
zap-cli --zap-url http://localhost:8080 active-scan http://myapp.com

# Spider
zap-cli --zap-url http://localhost:8080 spider http://myapp.com

# Report
zap-cli --zap-url http://localhost:8080 report -o report.html -f html
```

## Decision Framework

### When to Use This Domain
- ✅ Implementing authentication/authorization
- ✅ Reviewing code for security issues
- ✅ Scanning dependencies for vulnerabilities
- ✅ Setting up encryption
- ✅ Managing secrets and credentials
- ✅ Configuring WAF and network security
- ✅ Responding to security incidents
- ✅ Compliance audits and assessments

### When to Coordinate with Other Domains
- **All Domains**: Security review required for ALL changes
- **Frontend**: XSS prevention, CORS, CSP
- **Backend**: Authentication, authorization, input validation
- **Infrastructure**: IAM, encryption, network security
- **Data**: Database encryption, access control

### Risk Assessment Matrix
```
RISK = LIKELIHOOD × IMPACT

Likelihood:
- High: Easily exploitable, publicly known
- Medium: Requires some effort/skill
- Low: Difficult to exploit

Impact:
- Critical: Data breach, system compromise
- High: Sensitive data exposure
- Medium: Limited data exposure
- Low: Minimal impact

Priority = Risk Level
```

## Example Scenarios

### Scenario 1: JWT Authentication
**Request**: "Add JWT authentication to API"

**Domain Detection**: Security + Backend (keywords: JWT, authentication, API)

**Workflow**:
```
spec-manager:
  - Define authentication requirements
  - Specify token expiration strategy
  - Document login/logout flow

security-auditor:
  1. Design Review:
     - Recommend RS256 over HS256 (public/private keys)
     - Access token: 15 min expiry
     - Refresh token: 7 day expiry, rotation
     - Store in httpOnly cookies (not localStorage)
     - Implement rate limiting on login

infrastructure-specialist:
  1. Implementation:
     - Install jsonwebtoken, bcrypt
     - Generate RSA key pair
     - Store private key in Secrets Manager
     - Create POST /auth/login endpoint
     - Create POST /auth/refresh endpoint
     - Create authentication middleware

  2. Code:
     ```typescript
     // Generate tokens
     const accessToken = jwt.sign(
       { userId, role },
       privateKey,
       { algorithm: 'RS256', expiresIn: '15m' }
     );

     // Middleware
     const authenticate = async (req, res, next) => {
       const token = req.cookies.accessToken;
       try {
         const payload = jwt.verify(token, publicKey);
         req.user = payload;
         next();
       } catch (err) {
         res.status(401).json({ error: 'Unauthorized' });
       }
     };
     ```

security-auditor (Code Review):
  - ✅ Private key in Secrets Manager
  - ✅ RS256 algorithm (secure)
  - ✅ Short access token expiry
  - ✅ httpOnly cookies
  - ✅ Error doesn't leak info
  - ⚠️  Add rate limiting
  - ⚠️  Add account lockout after 5 failed attempts

infrastructure-specialist (Updates):
  - Add express-rate-limit
  - Implement lockout logic

qa-specialist:
  - Test successful login
  - Test invalid credentials
  - Test token expiration
  - Test refresh token flow
  - Test rate limiting

git-workflow-manager:
  - Commit authentication implementation
  - Document API endpoints
```

### Scenario 2: Dependency Vulnerability
**Request**: "Fix high severity vulnerability in lodash"

**Domain Detection**: Security (keywords: vulnerability, fix)

**Workflow**:
```
dependency-scanner:
  1. Scan:
     - npm audit
     - Identify: lodash@4.17.15 (Prototype Pollution)
     - Severity: High
     - Fix available: lodash@4.17.21

security-auditor:
  1. Risk Assessment:
     - Vulnerability: Prototype Pollution
     - Exploitability: Medium (requires specific usage)
     - Impact: High (code execution possible)
     - Priority: Fix immediately

  2. Verify Usage:
     - Search codebase for lodash usage
     - Confirm vulnerable patterns exist
     - Assess actual risk in our context

infrastructure-specialist:
  1. Update:
     - npm update lodash@4.17.21
     - OR yarn upgrade lodash@4.17.21
     - Verify package-lock.json updated

  2. Test:
     - Run unit tests
     - Run integration tests
     - Check for breaking changes

dependency-scanner (Verify):
  - npm audit (should show 0 vulnerabilities)
  - Confirm lodash@4.17.21 installed

qa-specialist:
  - Regression testing
  - Verify no functionality broken

git-workflow-manager:
  - Commit: "fix(security): upgrade lodash to 4.17.21 (CVE-2020-8203)"
  - Link to security advisory
```

### Scenario 3: Secrets in Code
**Request**: "Found API key hardcoded in code"

**Domain Detection**: Security (keywords: API key, hardcoded)

**Workflow**:
```
security-auditor:
  1. Immediate Actions:
     - Rotate the exposed API key (invalidate old one)
     - Check git history (how long exposed?)
     - Search public GitHub for leaked key
     - Scan logs for unauthorized usage

  2. Assessment:
     - Which service? (Stripe, AWS, etc.)
     - What permissions?
     - Any suspicious activity?

infrastructure-specialist:
  1. Create Secret in AWS:
     ```bash
     aws secretsmanager create-secret \
       --name prod/stripe/api-key \
       --secret-string "sk_live_NEW_KEY"
     ```

  2. Update Code:
     ```typescript
     // Before (BAD)
     const stripeKey = 'sk_live_EXPOSED_KEY';

     // After (GOOD)
     const { SecretString } = await secretsManager
       .getSecretValue({ SecretId: 'prod/stripe/api-key' })
       .promise();
     const stripeKey = SecretString;
     ```

  3. Update Environment Variables:
     - Remove hardcoded key
     - Add reference to Secrets Manager
     - Update serverless.yml or CDK

  4. Git History Cleanup:
     - Use git-filter-repo to remove from history
     - Force push (coordinate with team)

security-auditor (Verification):
  - ✅ Old key rotated
  - ✅ New key in Secrets Manager
  - ✅ Code updated
  - ✅ Git history cleaned
  - ✅ No suspicious activity detected

git-workflow-manager:
  - Commit: "security: move API key to Secrets Manager"
  - Document secret management process
```

### Scenario 4: SQL Injection Vulnerability
**Request**: "Security scan found SQL injection risk"

**Domain Detection**: Security + Backend (keywords: SQL injection, vulnerability)

**Workflow**:
```
security-auditor:
  1. Identify Vulnerable Code:
     ```typescript
     // VULNERABLE
     const query = `SELECT * FROM users WHERE email = '${email}'`;
     db.query(query);
     ```

  2. Demonstrate Exploit:
     - Input: `'; DROP TABLE users; --`
     - Resulting query: `SELECT * FROM users WHERE email = ''; DROP TABLE users; --'`

  3. Risk Assessment:
     - Severity: Critical
     - Exploitability: High (easy to exploit)
     - Impact: Critical (data loss, unauthorized access)
     - Priority: Fix immediately

infrastructure-specialist:
  1. Fix with Parameterized Query:
     ```typescript
     // FIXED
     const query = 'SELECT * FROM users WHERE email = ?';
     db.query(query, [email]);
     ```

  2. OR use ORM:
     ```typescript
     // FIXED with ORM
     const user = await User.findOne({ where: { email } });
     ```

  3. Find All Instances:
     - Grep for string concatenation in SQL
     - Review all database queries
     - Fix all vulnerable patterns

security-auditor (Code Review):
  - ✅ Parameterized queries used
  - ✅ No string concatenation in SQL
  - ✅ Input validation added
  - ✅ Verify ORM queries safe

qa-specialist:
  - Test with malicious inputs
  - Verify SQL injection prevented
  - Test legitimate use cases still work

git-workflow-manager:
  - Commit: "fix(security): prevent SQL injection in user queries"
  - Document secure query patterns
```

## Anti-Patterns to Avoid

### Common Security Mistakes
1. **Security Through Obscurity**: Hiding implementation isn't security
2. **Client-Side Validation Only**: Always validate on server
3. **Rolling Your Own Crypto**: Use established libraries
4. **Trusting User Input**: Validate and sanitize everything
5. **Storing Passwords Plaintext**: Always hash (bcrypt, Argon2)
6. **Weak Password Policies**: Enforce strong passwords
7. **No Rate Limiting**: Vulnerable to brute force
8. **Logging Sensitive Data**: Never log passwords, tokens, PII

### Infrastructure Security Mistakes
- **Public S3 Buckets**: Default to private
- **Overly Permissive IAM**: Use least privilege
- **No Encryption**: Encrypt at rest and in transit
- **Missing WAF**: Protect public endpoints
- **No Monitoring**: Deploy GuardDuty, Security Hub
- **Secrets in Environment Variables**: Use Secrets Manager
- **SSH Keys in Code**: Use IAM roles, Session Manager

### Authentication Mistakes
- **Long-Lived Tokens**: Keep access tokens short
- **No Token Refresh**: Implement refresh token flow
- **Tokens in URLs**: Use headers or cookies
- **localStorage for Tokens**: Use httpOnly cookies
- **No MFA**: Require for admin accounts
- **Weak Session Management**: Implement timeout, secure cookies

## Success Metrics

### Security Metrics
- Zero high/critical vulnerabilities in production
- Mean time to patch (MTTP): < 24 hours for critical
- Security scan coverage: 100% of code
- Dependency scan frequency: Daily
- Secrets in code: 0 instances

### Compliance Metrics
- OWASP Top 10 coverage: 100%
- Security training completion: 100% of team
- Security reviews: All PRs reviewed
- Penetration test frequency: Quarterly
- Incident response time: < 1 hour

### Monitoring Metrics
- Failed login attempts: Track anomalies
- API error rate: Monitor 4xx/5xx
- WAF blocked requests: Trend analysis
- GuardDuty findings: Investigate all high
- CloudTrail events: Audit sensitive operations

## Resources & References

### Standards & Guidelines
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

### AWS Security
- [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/)
- [AWS Well-Architected Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/)
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

### Tools & Libraries
- [Snyk](https://snyk.io/)
- [OWASP ZAP](https://www.zaproxy.org/)
- [jwt.io](https://jwt.io/) - JWT debugger
- [Burp Suite](https://portswigger.net/burp)

### Learning Resources
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [AWS Security Blog](https://aws.amazon.com/blogs/security/)
