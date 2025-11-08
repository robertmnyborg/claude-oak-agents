# MCP Server Usage Examples

Complete examples demonstrating Reddit and GitHub MCP server integration with OaK Agents.

## Table of Contents

- [Reddit MCP Examples](#reddit-mcp-examples)
- [GitHub MCP Examples](#github-mcp-examples)
- [Combined Workflow Examples](#combined-workflow-examples)

## Reddit MCP Examples

### Example 1: Market Research

**Scenario**: Research developer sentiment about AI code assistants

**Workflow**:
```
User: "What are developers saying about AI code assistants on Reddit?"

product-strategist workflow:
  1. Search relevant subreddits
  2. Analyze sentiment and themes
  3. Generate insights report
```

**MCP Commands**:
```typescript
// Step 1: Search r/programming
const programmingPosts = await mcp__reddit__search_reddit({
  query: "AI code assistant OR GitHub Copilot OR Claude Code",
  subreddit: "programming",
  time_filter: "month",
  limit: 50
});

// Step 2: Search r/MachineLearning
const mlPosts = await mcp__reddit__search_reddit({
  query: "AI coding tools",
  subreddit: "MachineLearning",
  time_filter: "month",
  limit: 30
});

// Step 3: Get hot discussions
const hotDiscussions = await mcp__reddit__get_subreddit_hot({
  subreddit: "learnprogramming",
  limit: 25
});
```

**Analysis Results**:
- 45 relevant discussions found
- Sentiment: 78% positive, 15% neutral, 7% negative
- Common themes:
  - Productivity gains (mentioned in 67% of posts)
  - Code quality concerns (23% of posts)
  - Learning curve discussions (18% of posts)
- Feature requests: Context awareness, better multi-file support

### Example 2: Feature Validation

**Scenario**: Validate demand for automatic PR description generation

**Workflow**:
```
User: "Is there demand for automatic PR description generation?"

product-strategist validation:
  1. Search for related pain points
  2. Analyze upvotes and engagement
  3. Validate demand
```

**MCP Commands**:
```typescript
// Search for PR-related pain points
const prPainPoints = await mcp__reddit__search_reddit({
  query: "pull request description OR PR description tedious",
  subreddit: "programming",
  sort: "top",
  time_filter: "year",
  limit: 50
});

// Get top post details with comments
const topPost = prPainPoints.posts[0];
const postDetails = await mcp__reddit__get_post_details({
  subreddit: topPost.subreddit,
  post_id: topPost.permalink.split('/')[4],
  comment_limit: 20
});
```

**Validation Results**:
- Found 15+ discussions mentioning this pain point
- Average upvotes: 342 per post
- Sentiment: 87% positive for automation solutions
- Comments reveal specific needs:
  - Automatic change summarization
  - Related issue linking
  - Test coverage reporting
  - Breaking change detection
- **Recommendation**: High demand validated, prioritize for next sprint

### Example 3: Competitive Analysis

**Scenario**: Track what users say about competing tools

**Workflow**:
```typescript
// Monitor r/programming for competitor mentions
const competitorMentions = await mcp__reddit__search_reddit({
  query: "GitHub Copilot vs Claude Code vs Cursor",
  subreddit: "programming",
  sort: "relevance",
  time_filter: "month",
  limit: 30
});

// Get detailed discussions
for (const post of competitorMentions.posts.slice(0, 5)) {
  const details = await mcp__reddit__get_post_details({
    subreddit: post.subreddit,
    post_id: post.permalink.split('/')[4],
    comment_limit: 15
  });

  // Analyze comparative strengths/weaknesses mentioned
}
```

**Insights Extracted**:
- Copilot: Strong autocomplete, weaker on complex refactoring
- Cursor: Good UX, concerns about pricing model
- Claude Code: Praised for reasoning, wants better IDE integration
- Common request: Better multi-file awareness across all tools

## GitHub MCP Examples

### Example 1: Issue Creation from Spec

**Scenario**: Create GitHub issues for all tasks in an OAuth2 implementation spec

**Workflow**:
```
User: "Create GitHub issues for all tasks in the OAuth2 spec"

project-manager workflow:
  1. Read specification sections
  2. Extract acceptance criteria
  3. Create structured GitHub issues
  4. Link to spec and set labels
```

**MCP Commands**:
```typescript
// Step 1: Verify repository access
const repo = await mcp__github__get_repo({
  owner: "your-org",
  repo: "your-project"
});

// Step 2: Create issues from spec sections
const issue1 = await mcp__github__create_issue({
  owner: "your-org",
  repo: "your-project",
  title: "Implement OAuth2 Authorization Code Flow",
  body: `## Description
Implement the authorization code flow as specified in docs/specs/oauth2-spec.md

## Acceptance Criteria
- [ ] Authorization endpoint validates client_id
- [ ] State parameter prevents CSRF attacks
- [ ] PKCE implemented for public clients
- [ ] Token endpoint validates authorization codes

## Related
- Spec: docs/specs/oauth2-spec.md#authorization-flow
- Security requirements: docs/specs/oauth2-spec.md#security`,
  labels: ["feature", "security", "oauth2"],
  assignees: ["backend-dev"]
});

const issue2 = await mcp__github__create_issue({
  owner: "your-org",
  repo: "your-project",
  title: "OAuth2 Token Management and Refresh",
  body: `## Description
Implement token issuance, validation, and refresh mechanisms.

## Acceptance Criteria
- [ ] JWT tokens with proper claims
- [ ] Token expiration and refresh flow
- [ ] Revocation endpoint
- [ ] Token introspection endpoint

## Related
- Spec: docs/specs/oauth2-spec.md#token-management
- Previous: #${issue1.number}`,
  labels: ["feature", "security", "oauth2"]
});

// Create 6 more issues for remaining spec sections...
```

**Result**: 8 issues created with:
- Complete context from specification
- Proper labels and assignees
- Linked dependencies
- Milestone set for current sprint

### Example 2: CI/CD Monitoring and Debugging

**Scenario**: Diagnose why the deployment pipeline failed

**Workflow**:
```
User: "Why did the deployment fail?"

infrastructure-specialist workflow:
  1. Check recent workflow runs
  2. Identify failed runs
  3. Get job details and logs
  4. Analyze failure and suggest fix
```

**MCP Commands**:
```typescript
// Step 1: List recent workflow runs
const runs = await mcp__github__list_workflow_runs({
  owner: "your-org",
  repo: "your-project",
  workflow_id: "deploy.yml",
  status: "failure",
  per_page: 5
});

// Step 2: Get details of most recent failure
const failedRun = await mcp__github__get_workflow_run({
  owner: "your-org",
  repo: "your-project",
  run_id: runs.workflow_runs[0].id
});

// Step 3: Get job-level information
const jobs = await mcp__github__list_workflow_jobs({
  owner: "your-org",
  repo: "your-project",
  run_id: failedRun.id
});

// Analyze failed job
const failedJob = jobs.jobs.find(j => j.conclusion === "failure");
console.log("Failed step:", failedJob.steps.find(s => s.conclusion === "failure"));
```

**Diagnosis**:
```
Failed Run: #1234
Workflow: deploy.yml
Branch: main
Triggered by: push event
Failed Step: "Build Docker Image"
Error: "ERROR: failed to solve: process '/bin/sh -c apt-get install python3-dev' returned exit code 100"

Root Cause: Missing package in apt sources list
Fix: Add python3-dev to Dockerfile apt-get install command
```

**Suggested Fix**:
```dockerfile
# Before
RUN apt-get update && apt-get install -y python3

# After
RUN apt-get update && apt-get install -y python3 python3-dev
```

### Example 3: Automated Code Review

**Scenario**: Review all open PRs and identify issues

**Workflow**:
```typescript
// Step 1: Get all open PRs
const prs = await mcp__github__list_pull_requests({
  owner: "your-org",
  repo: "your-project",
  state: "open",
  per_page: 50
});

// Step 2: Review each PR
for (const pr of prs.pull_requests) {
  // Get PR details
  const prDetails = await mcp__github__get_pull_request({
    owner: "your-org",
    repo: "your-project",
    pull_number: pr.number
  });

  // Check for review criteria
  const issues = [];

  // No description
  if (!prDetails.body || prDetails.body.length < 50) {
    issues.push("Missing or insufficient PR description");
  }

  // No linked issues
  if (!prDetails.body.includes("#") && !prDetails.body.includes("Closes")) {
    issues.push("No linked issues");
  }

  // Large PR (>500 lines)
  if (prDetails.additions + prDetails.deletions > 500) {
    issues.push("Large PR - consider breaking into smaller changes");
  }

  // Report issues
  if (issues.length > 0) {
    console.log(`PR #${pr.number}: ${pr.title}`);
    console.log(`  Issues: ${issues.join(", ")}`);
  }
}
```

**Review Results**:
```
PR #123: Feature: Add OAuth2 support
  Issues: Large PR - consider breaking into smaller changes

PR #124: Fix: Update dependencies
  Issues: Missing or insufficient PR description, No linked issues

PR #125: Refactor: Improve error handling
  ✓ No issues found

Recommendations:
- 2 PRs need attention before merge
- 1 PR ready for review
```

## Combined Workflow Examples

### Example 4: Feature Validation → Spec → Implementation

**Scenario**: Complete workflow from Reddit research to GitHub issues

**Phase 1: Market Research (Reddit MCP)**
```typescript
// product-strategist uses Reddit MCP
const research = await mcp__reddit__search_reddit({
  query: "API rate limiting best practices",
  subreddit: "programming",
  time_filter: "year",
  limit: 50
});

// Analyze discussions
const insights = {
  demand: "High - 32 discussions found",
  sentiment: "87% want better rate limiting",
  common_requests: [
    "Per-user rate limits",
    "API key-based limiting",
    "Clear error messages",
    "Rate limit headers"
  ]
};
```

**Phase 2: Specification (spec-manager)**
```markdown
# API Rate Limiting Feature Spec

## Context
Research shows high demand for improved rate limiting (32 Reddit discussions, 87% positive sentiment).

## Acceptance Criteria
- Per-user rate limits (100 req/min)
- API key-based limiting
- Clear 429 error responses
- Rate limit headers (X-RateLimit-*)

## Success Metrics
- 95% of users stay under limits
- Clear error messages reduce support tickets by 30%
```

**Phase 3: Issue Creation (GitHub MCP)**
```typescript
// project-manager uses GitHub MCP
const issues = [];

issues.push(await mcp__github__create_issue({
  owner: "your-org",
  repo: "your-project",
  title: "Implement Per-User Rate Limiting",
  body: `## Context
Based on community research (32 Reddit discussions showing demand).

## Implementation
- Redis-based rate limiting
- User ID or API key as key
- Sliding window algorithm

## Acceptance Criteria
- [ ] 100 requests/minute per user
- [ ] Configurable limits
- [ ] Unit tests with 90%+ coverage

## Related
- Spec: docs/specs/rate-limiting.md
- Research: Community analysis from r/programming`,
  labels: ["feature", "api", "rate-limiting"],
  assignees: ["backend-dev"]
}));

issues.push(await mcp__github__create_issue({
  owner: "your-org",
  repo: "your-project",
  title: "Add Rate Limit Response Headers",
  body: `## Description
Implement standard rate limit headers in API responses.

## Headers Required
- X-RateLimit-Limit: Maximum requests allowed
- X-RateLimit-Remaining: Requests remaining
- X-RateLimit-Reset: Time when limit resets

## Related
- Previous: #${issues[0].number}`,
  labels: ["feature", "api", "rate-limiting"]
}));
```

**Result**: Complete feature pipeline
- Research validated demand
- Specification created with community insights
- Implementation issues created on GitHub
- Team ready to begin development

### Example 5: Security Monitoring Workflow

**Scenario**: Monitor security discussions and create preventive issues

**Phase 1: Security Research (Reddit MCP)**
```typescript
// security-auditor monitors security subreddits
const securityDiscussions = await mcp__reddit__search_reddit({
  query: "OAuth2 vulnerability OR JWT security issue",
  subreddit: "netsec",
  time_filter: "week",
  limit: 20
});

// Analyze for relevant threats
const relevantThreats = securityDiscussions.posts.filter(post =>
  post.title.includes("JWT") || post.body.includes("token validation")
);
```

**Phase 2: Check Current Implementation (GitHub MCP)**
```typescript
// Search codebase for potential vulnerable code
const codeSearch = await mcp__github__search_code({
  query: "language:typescript jwt verify",
  owner: "your-org",
  repo: "your-project"
});

// Review authentication code
const authFile = await mcp__github__get_file_content({
  owner: "your-org",
  repo: "your-project",
  path: "src/auth/jwt.ts",
  ref: "main"
});
```

**Phase 3: Create Preventive Issues (GitHub MCP)**
```typescript
// security-auditor creates issue if vulnerability found
if (detectedVulnerability) {
  await mcp__github__create_issue({
    owner: "your-org",
    repo: "your-project",
    title: "Security: Strengthen JWT Signature Verification",
    body: `## Security Context
Recent Reddit discussion in r/netsec highlighted JWT signature bypass vulnerabilities.

## Current State
Review of src/auth/jwt.ts shows potential issues:
- Algorithm confusion attack possible
- No key rotation mechanism

## Recommended Actions
- [ ] Enforce specific algorithm (RS256)
- [ ] Implement key rotation
- [ ] Add algorithm whitelist
- [ ] Security audit before next release

## References
- Reddit discussion: [link]
- OWASP JWT Cheatsheet: [link]`,
    labels: ["security", "critical", "auth"],
    assignees: ["security-team-lead"]
  });
}
```

**Result**: Proactive security management
- Community security intelligence gathered
- Current implementation audited
- Preventive issues created before exploitation
- Security team alerted to emerging threats

## Integration Best Practices

### 1. Chain MCP Servers

Use Reddit for research, then GitHub for implementation:
```
Reddit MCP → Insights → Spec → GitHub MCP → Issues
```

### 2. Context Preservation

Always link back to source:
```typescript
body: `Based on Reddit research: ${redditPostUrl}
Community sentiment: 87% positive
Implementation spec: docs/specs/feature.md`
```

### 3. Automate Workflows

Create repeatable patterns:
```typescript
async function featureValidationWorkflow(featureIdea: string) {
  // 1. Reddit research
  const research = await redditMarketResearch(featureIdea);

  // 2. Validate demand
  if (research.sentiment < 0.7) return "Low demand";

  // 3. Create spec
  const spec = await createSpecification(featureIdea, research);

  // 4. Create GitHub issues
  const issues = await createImplementationIssues(spec);

  return { research, spec, issues };
}
```

### 4. Monitor and Track

Use both MCPs for continuous monitoring:
```typescript
// Weekly workflow
async function weeklyMonitoring() {
  // Check Reddit for emerging trends
  const trends = await getRedditTrends();

  // Check GitHub for stalled PRs
  const stalledPRs = await getStalledPullRequests();

  // Generate report
  return generateWeeklyReport(trends, stalledPRs);
}
```

## Troubleshooting Examples

See `docs/MCP_INTEGRATION.md` for complete troubleshooting guide.

## Additional Resources

- **Setup Guide**: `docs/MCP_INTEGRATION.md`
- **MCP Server Code**: `mcp/src/reddit-server.ts`, `mcp/src/github-server.ts`
- **Configuration**: `mcp/mcp_config_template.json`
- **Test Script**: `scripts/test_mcp_integration.sh`
