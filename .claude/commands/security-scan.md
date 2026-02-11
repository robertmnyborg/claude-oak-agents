# Security Scan

Run security analysis on a codebase path using the security-auditor agent.

## Usage
/security-scan [path]

## What This Does
1. Scans code for vulnerabilities (injection, XSS, auth issues, hardcoded secrets)
2. Checks against OWASP Top 10
3. Optionally reviews dependencies for known CVEs
4. Generates prioritized findings with specific remediation steps

## Example
/security-scan src/api

## Output
Security report with findings categorized as CRITICAL/HIGH/MEDIUM/LOW, each with:
- Description of the vulnerability
- Impact assessment
- Specific code fix
