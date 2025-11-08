# OaK MCP Servers

Model Context Protocol (MCP) servers for OaK Agents, providing standardized access to telemetry data and agent coordination.

## Overview

OaK provides four MCP servers:

1. **oak-telemetry** - Telemetry data access and logging
2. **oak-agents** - Agent discovery, metadata, and script execution
3. **reddit** - Reddit public API integration for community research and market insights
4. **github** - GitHub API integration for repository management, issues, PRs, and CI/CD

## Installation

```bash
cd mcp
npm install
npm run build
```

## Configuration

Add to `~/.claude/settings.local.json` (Claude Code Desktop) or create `~/.config/claude/mcp_servers.json`:

```json
{
  "mcpServers": {
    "oak-telemetry": {
      "command": "node",
      "args": [
        "/Users/robertnyborg/Projects/claude-oak-agents/mcp/dist/telemetry-server.js"
      ],
      "env": {
        "OAK_TELEMETRY_DIR": "/Users/robertnyborg/Projects/claude-oak-agents/telemetry",
        "OAK_TELEMETRY_ENABLED": "true"
      }
    },
    "oak-agents": {
      "command": "node",
      "args": [
        "/Users/robertnyborg/Projects/claude-oak-agents/mcp/dist/agents-server.js"
      ],
      "env": {
        "OAK_AGENTS_DIR": "/Users/robertnyborg/Projects/claude-oak-agents/agents"
      }
    },
    "reddit": {
      "command": "node",
      "args": [
        "/Users/robertnyborg/Projects/claude-oak-agents/mcp/dist/reddit-server.js"
      ]
    },
    "github": {
      "command": "node",
      "args": [
        "/Users/robertnyborg/Projects/claude-oak-agents/mcp/dist/github-server.js"
      ],
      "env": {
        "GITHUB_MCP_TOKEN": "${GITHUB_MCP_TOKEN}"
      }
    }
  }
}
```

**GitHub Authentication**: Set `GITHUB_MCP_TOKEN` environment variable with your Personal Access Token:

```bash
export GITHUB_MCP_TOKEN="ghp_your_token_here"
echo 'export GITHUB_MCP_TOKEN="ghp_your_token_here"' >> ~/.zshrc  # or ~/.bashrc
```

Create token at: https://github.com/settings/tokens
Required scopes: `repo`, `read:packages`, `read:org`, `workflow`

## OaK Telemetry Server

### Resources

- `oak://telemetry/invocations` - Recent agent invocations (last 100)
- `oak://telemetry/metrics` - Aggregated performance metrics by agent
- `oak://telemetry/gaps` - Detected capability gaps
- `oak://telemetry/summary` - High-level summary (text)

### Tools

#### log_agent_invocation

Log an agent invocation with telemetry data.

```typescript
{
  "agent_name": "security-auditor",
  "task_description": "Scan codebase for vulnerabilities",
  "state_features": {
    "languages": ["typescript", "python"],
    "frameworks": ["react", "fastapi"]
  }
}
```

Returns: `invocation_id`

#### update_invocation

Update invocation with completion data.

```typescript
{
  "invocation_id": "inv_1234567890_abc123",
  "duration_seconds": 45.2,
  "outcome": "success",
  "quality_score": 4.5
}
```

#### query_telemetry

Query telemetry data with filters.

```typescript
{
  "agent_name": "security-auditor",  // optional
  "start_date": "2025-10-01T00:00:00Z",  // optional
  "end_date": "2025-10-16T23:59:59Z",  // optional
  "limit": 50  // optional
}
```

Returns: Array of invocations

### Usage Example

```typescript
// Log agent start
const result = await use_mcp_tool("oak-telemetry", "log_agent_invocation", {
  agent_name: "frontend-developer",
  task_description: "Implement dark mode toggle",
  state_features: {
    languages: ["typescript"],
    frameworks: ["react"],
    has_tests: true
  }
});

const invocation_id = JSON.parse(result.content[0].text);

// ... agent executes ...

// Log completion
await use_mcp_tool("oak-telemetry", "update_invocation", {
  invocation_id,
  duration_seconds: 120.5,
  outcome: "success",
  quality_score: 5
});
```

## OaK Agents Server

### Resources

- `oak://agents/metadata` - Metadata for all agents (lightweight)
- `oak://agents/{name}/definition` - Full agent definition (on-demand)
- `oak://agents/{name}/metadata` - Individual agent metadata
- `oak://agents/{name}/scripts` - Bundled scripts for agent

### Tools

#### find_agents

Find agents matching keywords, domains, or file patterns.

```typescript
{
  "keywords": ["security", "vulnerability"],  // optional
  "domain": "security",  // optional
  "file_path": "src/auth/login.ts"  // optional
}
```

Returns: Array of matching agent metadata

#### execute_agent_script

Execute a bundled agent script.

```typescript
{
  "agent_name": "security-auditor",
  "script_name": "dependency_scan",
  "parameters": {
    "scan_depth": "deep",
    "severity_threshold": "medium",
    "output_format": "json"
  }
}
```

Returns: Script execution result (stdout, stderr, returncode)

#### get_agent_recommendations

Get ML-recommended agents for a task (keyword-based in current version, ML-powered in Phase 6).

```typescript
{
  "task_description": "Fix authentication vulnerability in login endpoint",
  "context": {
    "language": "typescript",
    "framework": "express"
  }
}
```

Returns: Array of recommended agents with confidence scores

### Usage Example

```typescript
// Find agents for security task
const agents = await use_mcp_tool("oak-agents", "find_agents", {
  keywords: ["security", "vulnerability", "audit"]
});

console.log(agents); // ["security-auditor", "dependency-scanner", ...]

// Execute bundled script
const scanResult = await use_mcp_tool("oak-agents", "execute_agent_script", {
  agent_name: "security-auditor",
  script_name: "dependency_scan",
  parameters: {
    scan_depth: "deep",
    output_format: "json"
  }
});

const vulnerabilities = JSON.parse(scanResult.content[0].text);
```

## Integration with OaK Hooks

MCP servers can replace traditional hooks for cleaner integration:

### Before (Hooks)

```python
# pre_agent_hook.py - Custom script
logger = TelemetryLogger()
logger.log_invocation(agent_name, task)
```

### After (MCP)

```typescript
// Use standard MCP tool
await use_mcp_tool("oak-telemetry", "log_agent_invocation", {
  agent_name,
  task_description
});
```

### Migration Path

1. **Phase 1** (Current): Hooks continue to work
2. **Phase 2**: Add MCP as optional alternative
3. **Phase 3**: Deprecate hooks, recommend MCP
4. **Phase 4**: MCP becomes primary interface

## Benefits of MCP Integration

### 1. Standardization
- Industry-standard protocol (Anthropic-backed)
- Consistent interface across tools
- Better ecosystem integration

### 2. Simplicity
- No custom hook scripts needed
- Built-in error handling
- Automatic retry logic

### 3. Scalability
- Efficient resource access
- Lazy loading of agent definitions
- Query optimization

### 4. Debugging
- Standard MCP inspector tools
- Request/response logging
- Performance monitoring

## Development

### Build

```bash
npm run build
```

### Watch Mode

```bash
npm run watch
```

### Testing

```bash
# Test telemetry server
node dist/telemetry-server.js <<EOF
{"jsonrpc":"2.0","id":1,"method":"tools/list"}
EOF

# Test agents server
node dist/agents-server.js <<EOF
{"jsonrpc":"2.0","id":1,"method":"resources/list"}
EOF
```

## Troubleshooting

### Server not starting

```bash
# Check Node.js version (requires 18+)
node --version

# Rebuild
rm -rf dist node_modules
npm install
npm run build
```

### "Module not found" errors

```bash
# Install dependencies
npm install @modelcontextprotocol/sdk
```

### MCP not recognized by Claude

```bash
# Verify configuration file location
ls -la ~/.config/claude/mcp_servers.json

# Check JSON syntax
cat ~/.config/claude/mcp_servers.json | jq .

# Restart Claude Code
```

## Future Enhancements

- [ ] WebSocket transport for real-time updates
- [ ] Multi-user telemetry aggregation
- [ ] Agent performance dashboards
- [ ] ML model serving via MCP
- [ ] Distributed agent coordination
- [ ] Agent marketplace integration

## Reddit MCP Server

### Overview

Access Reddit's public API for community research and market insights. No authentication required.

### Resources

- `reddit://frontpage` - Current Reddit frontpage posts
- `reddit://popular` - Popular posts across Reddit
- `reddit://all` - Posts from r/all

### Tools

#### get_subreddit_hot
Get hot posts from a specific subreddit.

```typescript
{
  "subreddit": "programming",
  "limit": 25
}
```

#### get_subreddit_new
Get newest posts from a specific subreddit.

```typescript
{
  "subreddit": "MachineLearning",
  "limit": 25
}
```

#### get_subreddit_top
Get top posts from a specific subreddit.

```typescript
{
  "subreddit": "learnprogramming",
  "time_filter": "week",  // hour, day, week, month, year, all
  "limit": 25
}
```

#### get_post_details
Get detailed information about a specific post including comments.

```typescript
{
  "subreddit": "programming",
  "post_id": "abc123",
  "comment_limit": 10
}
```

#### search_reddit
Search across Reddit or within a specific subreddit.

```typescript
{
  "query": "AI coding assistants",
  "subreddit": "programming",  // optional
  "sort": "relevance",  // relevance, hot, top, new, comments
  "time_filter": "month",
  "limit": 25
}
```

#### get_user_posts
Get public posts from a Reddit user.

```typescript
{
  "username": "example_user",
  "sort": "new",  // new, hot, top, controversial
  "limit": 25
}
```

### Usage Examples

```typescript
// Market research
const posts = await use_mcp_tool("reddit", "search_reddit", {
  query: "automated code review",
  subreddit: "programming",
  time_filter: "month"
});

// Community sentiment
const hotPosts = await use_mcp_tool("reddit", "get_subreddit_hot", {
  subreddit: "MachineLearning",
  limit: 50
});

// Post analysis
const details = await use_mcp_tool("reddit", "get_post_details", {
  subreddit: "programming",
  post_id: "abc123",
  comment_limit: 20
});
```

## GitHub MCP Server

### Overview

Direct GitHub integration for AI tools with comprehensive API access. Requires GitHub Personal Access Token.

### Resources

- `github://user/repos` - Repositories accessible to authenticated user
- `github://user/profile` - Authenticated user profile information

### Tools

#### Repository Tools

**list_repos** - List repositories for a user or organization

```typescript
{
  "owner": "anthropics",  // optional, defaults to authenticated user
  "type": "all",  // all, owner, public, private, member
  "sort": "updated",  // created, updated, pushed, full_name
  "per_page": 30
}
```

**get_repo** - Get detailed information about a specific repository

```typescript
{
  "owner": "anthropics",
  "repo": "anthropic-sdk-typescript"
}
```

**search_code** - Search for code across GitHub repositories

```typescript
{
  "query": "language:typescript async function",
  "owner": "anthropics",  // optional
  "repo": "anthropic-sdk-typescript",  // optional
  "per_page": 30
}
```

**get_file_content** - Get contents of a file from a repository

```typescript
{
  "owner": "anthropics",
  "repo": "anthropic-sdk-typescript",
  "path": "src/index.ts",
  "ref": "main"  // optional: branch, tag, or commit SHA
}
```

#### Issue Tools

**list_issues** - List issues for a repository

```typescript
{
  "owner": "anthropics",
  "repo": "anthropic-sdk-typescript",
  "state": "open",  // open, closed, all
  "labels": "bug,enhancement",  // optional
  "per_page": 30
}
```

**get_issue** - Get details of a specific issue

```typescript
{
  "owner": "anthropics",
  "repo": "anthropic-sdk-typescript",
  "issue_number": 123
}
```

**create_issue** - Create a new issue in a repository

```typescript
{
  "owner": "anthropics",
  "repo": "anthropic-sdk-typescript",
  "title": "Bug: Authentication failure",
  "body": "Detailed description of the issue",
  "labels": ["bug", "priority-high"],
  "assignees": ["username"]
}
```

**update_issue** - Update an existing issue

```typescript
{
  "owner": "anthropics",
  "repo": "anthropic-sdk-typescript",
  "issue_number": 123,
  "state": "closed",
  "labels": ["bug", "resolved"]
}
```

#### Pull Request Tools

**list_pull_requests** - List pull requests for a repository

```typescript
{
  "owner": "anthropics",
  "repo": "anthropic-sdk-typescript",
  "state": "open",  // open, closed, all
  "base": "main",  // optional: filter by base branch
  "per_page": 30
}
```

**get_pull_request** - Get details of a specific pull request

```typescript
{
  "owner": "anthropics",
  "repo": "anthropic-sdk-typescript",
  "pull_number": 456
}
```

**create_pull_request** - Create a new pull request

```typescript
{
  "owner": "anthropics",
  "repo": "anthropic-sdk-typescript",
  "title": "Feature: Add new functionality",
  "body": "Detailed PR description",
  "head": "feature-branch",
  "base": "main",
  "draft": false
}
```

#### GitHub Actions Tools

**list_workflow_runs** - List workflow runs for a repository

```typescript
{
  "owner": "anthropics",
  "repo": "anthropic-sdk-typescript",
  "workflow_id": "ci.yml",  // optional
  "branch": "main",  // optional
  "status": "completed",  // optional
  "per_page": 30
}
```

**get_workflow_run** - Get details of a specific workflow run

```typescript
{
  "owner": "anthropics",
  "repo": "anthropic-sdk-typescript",
  "run_id": 789
}
```

**list_workflow_jobs** - List jobs for a workflow run

```typescript
{
  "owner": "anthropics",
  "repo": "anthropic-sdk-typescript",
  "run_id": 789
}
```

#### Commit and Branch Tools

**list_commits** - List commits for a repository

```typescript
{
  "owner": "anthropics",
  "repo": "anthropic-sdk-typescript",
  "sha": "main",  // optional: branch or commit SHA
  "path": "src/",  // optional: only commits containing this path
  "per_page": 30
}
```

**get_commit** - Get a specific commit

```typescript
{
  "owner": "anthropics",
  "repo": "anthropic-sdk-typescript",
  "ref": "abc123"  // commit SHA
}
```

**list_branches** - List branches for a repository

```typescript
{
  "owner": "anthropics",
  "repo": "anthropic-sdk-typescript",
  "per_page": 30
}
```

### Usage Examples

```typescript
// Repository analysis
const repos = await use_mcp_tool("github", "list_repos", {
  owner: "anthropics",
  sort: "updated"
});

// Issue management
const issue = await use_mcp_tool("github", "create_issue", {
  owner: "anthropics",
  repo: "anthropic-sdk-typescript",
  title: "Feature Request: Add streaming support",
  body: "Detailed feature description...",
  labels: ["enhancement"]
});

// CI/CD monitoring
const runs = await use_mcp_tool("github", "list_workflow_runs", {
  owner: "anthropics",
  repo: "anthropic-sdk-typescript",
  status: "failure"
});

// Code search
const results = await use_mcp_tool("github", "search_code", {
  query: "language:typescript streaming",
  owner: "anthropics"
});
```

## Integration with OaK Agents

### Product Strategist + Reddit MCP

```typescript
// Market research workflow
const research = await use_mcp_tool("reddit", "search_reddit", {
  query: "AI code assistants pain points",
  subreddit: "programming",
  time_filter: "month"
});

// Analyze sentiment and identify feature requests
// product-strategist processes results...
```

### Git Workflow Manager + GitHub MCP

```typescript
// Enhanced PR creation
const pr = await use_mcp_tool("github", "create_pull_request", {
  owner: "user",
  repo: "project",
  title: "Feature: OAuth2 integration",
  body: generatedPRDescription,
  head: "feature/oauth2",
  base: "main"
});

// Link related issues
await use_mcp_tool("github", "update_issue", {
  owner: "user",
  repo: "project",
  issue_number: 123,
  body: `Resolved by #${pr.number}`
});
```

### Infrastructure Specialist + GitHub MCP

```typescript
// Monitor deployment workflows
const runs = await use_mcp_tool("github", "list_workflow_runs", {
  owner: "user",
  repo: "project",
  workflow_id: "deploy.yml",
  status: "failure"
});

// Get failure details
const failedRun = await use_mcp_tool("github", "get_workflow_run", {
  owner: "user",
  repo: "project",
  run_id: runs.workflow_runs[0].id
});

// Analyze and report infrastructure issues
```

## Resources

- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [Anthropic MCP Documentation](https://docs.anthropic.com/mcp)
- [OaK Multi-File Agents](../docs/MULTI_FILE_AGENTS.md)
- [OaK Migration Guide](../docs/MIGRATION_GUIDE.md)
- [Reddit API Documentation](https://www.reddit.com/dev/api)
- [GitHub REST API Documentation](https://docs.github.com/rest)
