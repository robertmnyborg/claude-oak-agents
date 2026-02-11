# Deployment Readiness Check

Pre-deployment validation combining quality, security, and configuration checks.

## Usage
/deploy-check [--environment staging|production]

## What This Does
1. Validates code quality (quality-gate scoring)
2. Runs security audit (vulnerability scan)
3. Checks test suite status
4. Validates environment configuration
5. Generates go/no-go deployment recommendation

## Example
/deploy-check --environment production

## Output
Deployment readiness report with:
- Overall status (READY / NOT READY)
- Blocking issues that must be fixed
- Warnings that should be addressed
- Checklist of required actions before deployment
