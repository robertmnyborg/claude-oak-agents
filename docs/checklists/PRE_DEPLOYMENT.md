# Pre-Deployment Enforcement Checklist

## Purpose

This checklist is used by the **deployment-manager agent** (and should be referenced by all agents before deployment) to ensure compliance with project structure, deployment patterns, and quality standards.

**When to use this checklist:**
- Before any deployment to AWS
- Before creating deployment-related commits
- After major restructuring or cleanup
- When onboarding new applications to the project

---

## 1. Project Structure Validation

### 1.1 Root Directory Organization

- [ ] **Only allowed files exist in root**
  - `claude.md` ✓
  - `README.md` ✓
  - `SPEC.md` ✓
  - Standard config files (`.gitignore`, `package.json`, etc.) ✓
  - No other `.md` files in root ✓

- [ ] **All documentation organized into subdirectories**
  - All other `.md` files moved to `docs/` with topic-based subdirectories ✓
  - Architecture docs in `docs/architecture/` ✓
  - Workflow guides in `docs/workflows/` ✓
  - Deployment docs in `docs/deployment/` ✓

- [ ] **Bot outputs confined to oak/ directory**
  - Logs in `oak/logs/` ✓
  - Reports in `oak/reports/` ✓
  - Telemetry in `oak/telemetry/` ✓
  - No bot outputs in root or code directories ✓

- [ ] **Code organized into code-dirs/**
  - Logical separation of codebases ✓
  - Clear naming (e.g., `frontend/`, `backend/`, `async-processors/`) ✓
  - No `src/` directory at root level (should be in code-dirs/) ✓

**Validation Command:**
```bash
# Check root directory only has allowed files
ls *.md | grep -v -E '^(README|SPEC|claude)\.md$' && echo "❌ FAIL: Unexpected .md files in root" || echo "✅ PASS: Root clean"

# Check docs directory exists and has subdirectories
test -d docs && ls -d docs/*/ >/dev/null 2>&1 && echo "✅ PASS: Docs organized" || echo "❌ FAIL: Docs not organized"

# Check oak directory structure
test -d oak/logs && test -d oak/reports && echo "✅ PASS: Oak structure correct" || echo "❌ FAIL: Oak structure missing"
```

---

## 2. Type Management Validation

### 2.1 Shared Types Removal

- [ ] **No shared/ directory exists at root level**
  - Search for `shared/` or `types/` directory ✓
  - If found, MUST be moved to backend or deleted ✓

- [ ] **All types live in backend codebase**
  - Type definitions in `code-dirs/backend/` ✓
  - No duplicate type files across projects ✓

- [ ] **API clients generated from Swagger/OpenAPI**
  - Swagger/OpenAPI specification exists ✓
  - Client generation script exists ✓
  - No manually maintained type files ✓

- [ ] **No type drift between backend and clients**
  - Clients regenerated from latest Swagger spec ✓
  - Generation verified successful ✓

**Validation Command:**
```bash
# Check for shared directory at root
test -d shared && echo "❌ FAIL: shared/ directory exists at root" || echo "✅ PASS: No shared/ directory"

# Check for types in backend
test -d code-dirs/backend && grep -r "type\|interface" code-dirs/backend >/dev/null && echo "✅ PASS: Types in backend" || echo "⚠️  WARNING: No types found in backend"

# Check for Swagger spec
find . -name "swagger.yaml" -o -name "openapi.yaml" -o -name "swagger.json" | head -1 && echo "✅ PASS: API spec found" || echo "❌ FAIL: No API specification"
```

---

## 3. AI-Generated Artifacts Cleanup

### 3.1 Required Deletions

- [ ] **No duplicate package lock files**
  - If using `yarn.lock`, no `package-lock.json` exists ✓
  - If using `pnpm-lock.yaml`, no `package-lock.json` or `yarn.lock` exists ✓

- [ ] **No test artifacts from AI**
  - No `test-portfolio-api.ssh` ✓
  - No `test-*.tmp` files ✓
  - No `debug-*.log` files in code directories ✓

- [ ] **No temporary exploration files**
  - No `scratch.js`, `temp.ts`, `testing.py` ✓
  - No `output-*.txt` files ✓

- [ ] **No unused boilerplate**
  - No empty directories ✓
  - No generated files not in use ✓

**Validation Command:**
```bash
# Check for duplicate lock files (adjust based on your package manager)
if [ -f yarn.lock ]; then
  test -f package-lock.json && echo "❌ FAIL: Both yarn.lock and package-lock.json exist" || echo "✅ PASS: No duplicate lock files"
fi

# Check for test artifacts
find . -name "test-*.ssh" -o -name "test-*.tmp" -o -name "scratch.*" -o -name "temp.*" | head -1 && echo "❌ FAIL: Test artifacts found" || echo "✅ PASS: No test artifacts"
```

---

## 4. Docker Configuration Validation

### 4.1 Containerization Requirements

- [ ] **Each application has a Dockerfile**
  - `code-dirs/frontend/Dockerfile` exists ✓
  - `code-dirs/backend/Dockerfile` exists (if separate) ✓
  - Additional apps have Dockerfiles ✓

- [ ] **Next.js apps are NOT split**
  - Frontend and API routes in same container ✓
  - No separate frontend/backend containers for Next.js ✓
  - Dockerfile builds unified Next.js app ✓

- [ ] **Multi-stage builds used**
  - Dockerfile has `deps`, `builder`, `runner` stages ✓
  - Production image is optimized ✓

- [ ] **Environment variables configured**
  - `.env.example` exists for local development ✓
  - Production env vars in AWS Parameter Store ✓
  - No secrets in Dockerfile or committed code ✓

**Validation Command:**
```bash
# Check for Dockerfiles
find code-dirs/ -name "Dockerfile" -type f | while read dockerfile; do
  echo "✅ Found: $dockerfile"
done

# Check Next.js apps aren't split (if Next.js is used)
if [ -f code-dirs/frontend/next.config.js ]; then
  grep -r "api/" code-dirs/frontend/pages >/dev/null && echo "✅ PASS: Next.js unified" || echo "⚠️  WARNING: Check Next.js structure"
fi

# Check for multi-stage builds
find code-dirs/ -name "Dockerfile" -type f -exec grep -l "AS deps" {} \; | while read df; do
  echo "✅ Multi-stage: $df"
done
```

---

## 5. CDK Infrastructure Validation

### 5.1 Infrastructure Pattern Compliance

- [ ] **CDK constructs follow established pattern**
  - Static site construct exists ✓
  - CloudFront distribution configured ✓
  - S3 bucket for static assets ✓

- [ ] **CloudFront configuration correct**
  - Routes static assets to S3 ✓
  - Routes dynamic requests to container ✓
  - Single domain configuration ✓

- [ ] **All apps containerized**
  - No non-containerized deployments ✓
  - Container orchestration configured (ECS/Fargate) ✓

- [ ] **Infrastructure testing**
  - CDK synth produces valid CloudFormation ✓
  - No circular dependencies ✓
  - Resource limits within AWS account quotas ✓

**Validation Command:**
```bash
# Check for CDK infrastructure
if [ -d code-dirs/infrastructure ]; then
  cd code-dirs/infrastructure
  npx cdk synth --quiet && echo "✅ PASS: CDK synth successful" || echo "❌ FAIL: CDK synth failed"
  cd -
fi

# Check for CloudFront in infrastructure
grep -r "cloudfront" code-dirs/infrastructure >/dev/null && echo "✅ PASS: CloudFront configured" || echo "⚠️  WARNING: No CloudFront config found"
```

---

## 6. SPEC.md Validation

### 6.1 Product Spec 2 Compliance

- [ ] **SPEC.md exists in root**
  - File located at `~/Projects/[project]/SPEC.md` ✓

- [ ] **Follows Product Spec 2 structure**
  - Has all required sections from template ✓
  - Focus on WHAT, not HOW ✓

- [ ] **No prohibited content**
  - No database schemas ✓
  - No code implementation details ✓
  - No specific languages/frameworks ✓
  - No system architecture diagrams with technical specifics ✓

- [ ] **Inputs and Outputs clearly defined**
  - Inputs section describes user interactions and data sources ✓
  - Outputs section describes UI components and API endpoints functionally ✓
  - Data sources referenced without implementation details ✓

**Validation Command:**
```bash
# Check SPEC.md exists
test -f SPEC.md && echo "✅ PASS: SPEC.md exists" || echo "❌ FAIL: No SPEC.md"

# Check for prohibited content (should find very few matches, only in examples or "do not include" sections)
grep -i "class\|schema\|table\|migration\|implementation" SPEC.md | wc -l | awk '{if ($1 > 30) print "⚠️  WARNING: Many implementation terms found (" $1 ")"; else print "✅ PASS: Minimal implementation terms"}'

# Check for required sections
grep -E "## 1\. Problem Statement|## 2\. User Stories|## 3\. Inputs|## 4\. Outputs" SPEC.md >/dev/null && echo "✅ PASS: Key sections present" || echo "❌ FAIL: Missing required sections"
```

---

## 7. Documentation Quality

### 7.1 Documentation Organization

- [ ] **All docs in appropriate subdirectories**
  - No loose documentation files ✓
  - Clear topic-based organization ✓

- [ ] **Documentation up to date**
  - Deployment docs reflect current infrastructure ✓
  - Architecture docs match actual implementation ✓
  - API docs match current endpoints ✓

- [ ] **No consumed instructions in project**
  - Old agent instructions moved or deleted ✓
  - No obsolete guidance files ✓

**Validation Command:**
```bash
# Check docs organization
test -d docs && ls docs/ | while read subdir; do
  test -d "docs/$subdir" && echo "✅ Subdirectory: docs/$subdir"
done

# Check for loose .md files in root (except allowed)
find . -maxdepth 1 -name "*.md" | grep -v -E '(README|SPEC|claude)\.md' && echo "⚠️  WARNING: Loose .md files in root" || echo "✅ PASS: No loose docs in root"
```

---

## 8. Deployment Readiness

### 8.1 Build and Test

- [ ] **All applications build successfully**
  - Frontend builds without errors ✓
  - Backend builds without errors ✓
  - Docker images build successfully ✓

- [ ] **Tests pass**
  - Unit tests pass ✓
  - Integration tests pass (if applicable) ✓
  - E2E tests pass (if applicable) ✓

- [ ] **Linting and formatting**
  - Code passes linter ✓
  - Code is properly formatted ✓
  - No TypeScript errors (if applicable) ✓

**Validation Command:**
```bash
# Build check (adjust based on your build system)
if [ -f package.json ]; then
  yarn build && echo "✅ PASS: Build successful" || echo "❌ FAIL: Build failed"
fi

# Docker build check
find code-dirs/ -name "Dockerfile" -type f | while read dockerfile; do
  dir=$(dirname "$dockerfile")
  docker build -t test-build "$dir" && echo "✅ PASS: Docker build successful for $dir" || echo "❌ FAIL: Docker build failed for $dir"
done
```

### 8.2 Security and Secrets

- [ ] **No secrets in code**
  - No hardcoded API keys ✓
  - No database credentials in files ✓
  - No AWS access keys in code ✓

- [ ] **Secrets management configured**
  - AWS Parameter Store configured ✓
  - Secrets Manager configured (if needed) ✓
  - Environment variable injection working ✓

- [ ] **.gitignore properly configured**
  - `.env` files ignored ✓
  - `node_modules/` ignored ✓
  - Build artifacts ignored ✓

**Validation Command:**
```bash
# Check for potential secrets (basic scan)
grep -r -E "API_KEY|PASSWORD|SECRET|aws_access_key" --include="*.ts" --include="*.js" --include="*.py" code-dirs/ && echo "⚠️  WARNING: Potential secrets found" || echo "✅ PASS: No obvious secrets in code"

# Check .gitignore exists
test -f .gitignore && grep -E "\.env|node_modules" .gitignore >/dev/null && echo "✅ PASS: .gitignore configured" || echo "❌ FAIL: .gitignore missing or incomplete"
```

---

## 9. Post-Deployment Documentation

### 9.1 Required Documentation Updates

After successful deployment:

- [ ] **Update deployment log**
  - Create `oak/logs/deployment-YYYY-MM-DD.md` ✓
  - Document what was deployed ✓
  - Record any issues encountered ✓

- [ ] **Update deployment docs**
  - Add new patterns to `docs/deployment/` ✓
  - Document configuration changes ✓
  - Update runbooks if needed ✓

- [ ] **Clean up deployment artifacts**
  - Remove temporary files ✓
  - Archive old deployment files ✓

---

## 10. Final Validation

### 10.1 Complete Checklist

Before proceeding with deployment, verify ALL items above are checked. If any item fails:

1. **Stop deployment immediately**
2. **Document the failure** in `oak/logs/pre-deployment-YYYY-MM-DD.md`
3. **Remediate the issue** following deployment-manager.md guidance
4. **Re-run this checklist** from the beginning

### 10.2 Sign-off

**Deployment Manager Agent**: [Agent completion timestamp]
**Validation Date**: [YYYY-MM-DD HH:MM:SS]
**Deployment Approved**: [ ] Yes / [ ] No - Remediation required

**Notes:**
[Any additional context, warnings, or recommendations]

---

## Quick Reference Commands

Run all validation commands in sequence:

```bash
#!/bin/bash
# Save as: validate-deployment.sh

echo "=== Pre-Deployment Validation ==="

# 1. Root directory
echo -e "\n1. Root Directory:"
ls *.md 2>/dev/null | grep -v -E '^(README|SPEC|claude)\.md$' && echo "❌ Unexpected .md files" || echo "✅ Root clean"

# 2. Documentation
echo -e "\n2. Documentation:"
test -d docs && ls -d docs/*/ >/dev/null 2>&1 && echo "✅ Docs organized" || echo "❌ Docs missing"

# 3. Oak structure
echo -e "\n3. Oak Directory:"
test -d oak/logs && test -d oak/reports && echo "✅ Oak structure correct" || echo "❌ Oak structure missing"

# 4. Shared types
echo -e "\n4. Type Management:"
test -d shared && echo "❌ shared/ directory exists" || echo "✅ No shared/ directory"

# 5. Lock files
echo -e "\n5. Lock Files:"
if [ -f yarn.lock ]; then
  test -f package-lock.json && echo "❌ Duplicate lock files" || echo "✅ Clean lock files"
fi

# 6. Dockerfiles
echo -e "\n6. Docker Configuration:"
find code-dirs/ -name "Dockerfile" 2>/dev/null | while read df; do echo "✅ $df"; done

# 7. SPEC.md
echo -e "\n7. SPEC.md:"
test -f SPEC.md && echo "✅ SPEC.md exists" || echo "❌ No SPEC.md"

# 8. CDK
echo -e "\n8. Infrastructure:"
if [ -d code-dirs/infrastructure ]; then
  cd code-dirs/infrastructure && npx cdk synth --quiet >/dev/null 2>&1 && echo "✅ CDK valid" || echo "❌ CDK synth failed"
  cd - >/dev/null
fi

# 9. Secrets
echo -e "\n9. Security:"
test -f .gitignore && grep -E "\.env|node_modules" .gitignore >/dev/null && echo "✅ .gitignore configured" || echo "❌ .gitignore issue"

echo -e "\n=== Validation Complete ==="
```

Make executable: `chmod +x validate-deployment.sh`

Run before deployment: `./validate-deployment.sh`

---

## Appendix: Common Issues and Remediation

### Issue: Unexpected .md files in root
**Remediation**: Move to appropriate `docs/` subdirectory
```bash
mv file.md docs/[appropriate-subdirectory]/
```

### Issue: shared/ directory exists
**Remediation**: Move types to backend
```bash
mkdir -p code-dirs/backend/types
mv shared/* code-dirs/backend/types/
rm -rf shared/
```

### Issue: Duplicate lock files
**Remediation**: Keep only the lock file for your package manager
```bash
# If using yarn:
rm package-lock.json

# If using npm:
rm yarn.lock
```

### Issue: Next.js app is split
**Remediation**: Consolidate into single container - See DEPLOYMENT_PATTERN.md

### Issue: Secrets in code
**Remediation**: Move to Parameter Store and update code to use env vars
```bash
# Store in Parameter Store
aws ssm put-parameter --name "/app/secret" --value "..." --type "SecureString"

# Update .gitignore
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
```

---

**Version**: 1.0
**Last Updated**: 2025-10-24
**Maintained By**: deployment-manager agent
