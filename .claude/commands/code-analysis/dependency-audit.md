# Dependency Audit

Comprehensive audit of project dependencies for vulnerabilities, licenses, and supply chain risks.

## Usage
/dependency-audit [--fix-auto] [--report json|markdown] [--license-check]

## What This Does
1. Scans all dependencies for known vulnerabilities
2. Checks for outdated packages with security patches
3. Validates license compliance
4. Identifies supply chain risks
5. Recommends dependency updates
6. Optionally auto-fixes non-breaking updates

## Example
/dependency-audit --license-check --report markdown

## Agent Coordination
1. **dependency-scanner**: Primary audit agent
   - NPM audit / Yarn audit integration
   - CVE database queries
   - License compliance checking
   - Dependency tree analysis
   - Supply chain risk assessment
2. **Main LLM**: Formats report and recommendations

## Output
Dependency Audit Report:
```markdown
## Dependency Audit Report

### Summary
- Total dependencies: 156 (45 direct, 111 transitive)
- Vulnerabilities: 8 critical, 12 high, 23 medium, 15 low
- Outdated packages: 34
- License issues: 2
- Supply chain risks: 3 flagged packages

### Critical Vulnerabilities

1. **lodash@4.17.15** (Direct Dependency)
   - CVE-2020-8203: Prototype Pollution
   - Severity: CRITICAL
   - CVSS Score: 9.8
   - Affected versions: <4.17.21
   - Fix available: 4.17.21
   - Breaking changes: None
   - Action: `yarn upgrade lodash@4.17.21`

2. **jsonwebtoken@8.5.0** (Direct Dependency)
   - CVE-2022-23529: Signature Bypass Vulnerability
   - Severity: CRITICAL
   - CVSS Score: 9.0
   - Affected versions: <9.0.0
   - Fix available: 9.0.0
   - Breaking changes: Algorithm defaults changed
   - Action: Review code + `yarn upgrade jsonwebtoken@9.0.0`

3. **minimist@1.2.5** (Transitive via yargs)
   - CVE-2021-44906: Prototype Pollution
   - Severity: CRITICAL
   - CVSS Score: 8.6
   - Path: yargs@15.0.0 → yargs-parser@18.1.0 → minimist@1.2.5
   - Fix: Upgrade yargs to latest
   - Action: `yarn upgrade yargs@latest`

### High Severity Issues

4. **express@4.16.0** - Denial of Service
5. **axios@0.21.1** - Server-Side Request Forgery
6. **handlebars@4.7.6** - Remote Code Execution
7. **serialize-javascript@3.0.0** - Code Injection

### License Compliance Issues

1. **GPL-3.0 Dependency Detected** - pkg-name@2.1.0
   - License: GPL-3.0 (Copyleft)
   - Project license: MIT
   - Compatibility: INCOMPATIBLE ⚠️
   - Action: Find alternative package or obtain legal approval

2. **Unknown License** - internal-lib@1.0.0
   - License: Not specified
   - Risk: Legal uncertainty
   - Action: Contact maintainer or remove

### Supply Chain Risks

1. **Unmaintained Package** - old-util@1.0.0
   - Last update: 3 years ago
   - Open issues: 45 unresolved
   - Risk: No security patches
   - Recommendation: Migrate to maintained alternative

2. **New Maintainer Warning** - popular-lib@5.0.0
   - Maintainer changed 2 weeks ago
   - Risk: Supply chain compromise
   - Recommendation: Delay upgrade, monitor for issues

3. **Typosquatting Risk** - express-validator@6.0.0
   - Similar to: expresss-validator (malicious package removed)
   - Risk: Accidental installation of malicious version
   - Status: Legitimate package (verified)
   - Action: None, informational only

### Outdated Packages (Non-Security)

Major version updates available:
- react@16.14.0 → 18.2.0 (Breaking changes)
- webpack@4.46.0 → 5.89.0 (Breaking changes)
- typescript@4.5.0 → 5.3.0 (Breaking changes)

Minor/patch updates:
- 31 packages have non-breaking updates available

### Auto-Fix Recommendations

Safe to auto-update (no breaking changes):
```bash
yarn upgrade lodash@4.17.21
yarn upgrade express@4.18.2
yarn upgrade axios@1.6.0
# ... 8 more safe updates
```

Requires manual review (breaking changes):
```bash
yarn upgrade jsonwebtoken@9.0.0  # Review algorithm defaults
yarn upgrade react@18.2.0        # Review component lifecycle changes
```

### Action Plan

**Immediate (Critical)**:
1. Update lodash to fix prototype pollution
2. Update jsonwebtoken (review breaking changes)
3. Update express, axios, handlebars

**Short-term (High Priority)**:
4. Resolve GPL license compatibility issue
5. Replace unmaintained packages
6. Update transitive dependencies via parent packages

**Long-term**:
7. Plan major version upgrades (React 18, Webpack 5, TS 5)
8. Implement automated dependency monitoring
9. Set up Dependabot or Renovate for auto-updates

### Statistics
- Security coverage: 98% of dependencies scanned
- Average dependency age: 1.2 years
- Dependency tree depth: 7 levels (max)
- Duplicate packages: 3 (different versions of same package)

### Estimated Effort
- Critical fixes: 2 hours
- High priority fixes: 4 hours
- Major version upgrades: 16 hours (requires testing)
```

Returns: Comprehensive dependency report with prioritized remediation
