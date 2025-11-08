# MCP Server Integrations

## Overview

Claude-oak-agents integrates with four Model Context Protocol (MCP) servers for enhanced external capabilities:

1. **oak-telemetry** - Internal telemetry data access and logging
2. **oak-agents** - Internal agent discovery, metadata, and script execution
3. **reddit** - Reddit public API integration for community research and market insights
4. **github** - GitHub API integration for repository management, issues, PRs, and CI/CD

This document focuses on the Reddit and GitHub MCP servers that extend OaK capabilities with external data sources and integrations.

## Quick Start

### 1. Build MCP Servers

```bash
cd /Users/robertnyborg/Projects/claude-oak-agents/mcp
npm install
npm run build
```

### 2. Configure Claude Code

Add the MCP server configuration to your Claude Code settings:

**File**: `~/.claude/settings.local.json`

```json
{
  "mcpServers": {
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

Or use the template:

```bash
cat mcp/mcp_config_template.json
# Copy relevant sections to your Claude settings
```

### 3. Set Up GitHub Authentication

```bash
# Generate GitHub Personal Access Token at:
# https://github.com/settings/tokens

# Set environment variable
export GITHUB_MCP_TOKEN="ghp_your_token_here"

# Make it persistent
echo 'export GITHUB_MCP_TOKEN="ghp_your_token_here"' >> ~/.zshrc  # or ~/.bashrc

# Source your shell config
source ~/.zshrc
```

**Required GitHub Token Scopes**:
- `repo` - Full repository access
- `read:packages` - Read package metadata
- `read:org` - Read organization data
- `workflow` - Update GitHub Actions workflows

### 4. Restart Claude Code

After configuration, restart Claude Code to load the MCP servers.

## Reddit MCP Server

### Purpose

Access Reddit's public API for content analysis and community research.

### Use Cases

**Market Research**:
- "What are developers saying about AI coding tools on Reddit?"
- "Analyze r/programming posts about code review practices"
- Gather competitive intelligence from technology subreddits

**Community Insights**:
- "Find trending discussions about Claude Code"
- Identify pain points and feature requests from developer communities
- Track sentiment around specific technologies or approaches

**Trend Tracking**:
- Monitor emerging technologies in relevant subreddits
- Identify patterns in community discussions
- Track recurring questions and issues

**User Feedback**:
- "Gather feedback on feature ideas from relevant subreddits"
- Validate product hypotheses with community data
- Understand user workflows and challenges

### Available Tools

#### mcp__reddit__get_subreddit_hot

Browse hot posts from a specific subreddit.

**Example**:
```
"Show me top posts from r/MachineLearning today"
```

**Parameters**:
- `subreddit` (string) - Subreddit name without r/ prefix
- `limit` (number, optional) - Number of posts (default: 25, max: 100)

#### mcp__reddit__get_subreddit_new

Get newest posts from a specific subreddit.

**Example**:
```
"What are the latest discussions in r/programming?"
```

**Parameters**:
- `subreddit` (string) - Subreddit name
- `limit` (number, optional) - Number of posts

#### mcp__reddit__get_subreddit_top

Get top posts from a subreddit over a time period.

**Example**:
```
"Show me top posts from r/learnprogramming this week"
```

**Parameters**:
- `subreddit` (string) - Subreddit name
- `time_filter` (string, optional) - Time period: hour, day, week, month, year, all (default: day)
- `limit` (number, optional) - Number of posts

#### mcp__reddit__get_post_details

Get detailed information about a specific post including comments.

**Example**:
```
"Analyze this Reddit post and top comments"
```

**Parameters**:
- `subreddit` (string) - Subreddit name
- `post_id` (string) - Reddit post ID
- `comment_limit` (number, optional) - Number of top-level comments (default: 10)

#### mcp__reddit__search_reddit

Search across Reddit or within a specific subreddit.

**Example**:
```
"Search Reddit for discussions about automated code review"
```

**Parameters**:
- `query` (string) - Search query
- `subreddit` (string, optional) - Limit to specific subreddit
- `sort` (string, optional) - Sort by: relevance, hot, top, new, comments (default: relevance)
- `time_filter` (string, optional) - Time period
- `limit` (number, optional) - Number of results

#### mcp__reddit__get_user_posts

Get public posts from a Reddit user.

**Example**:
```
"Show me recent posts by user example_user"
```

**Parameters**:
- `username` (string) - Reddit username without u/ prefix
- `sort` (string, optional) - Sort by: new, hot, top, controversial (default: new)
- `limit` (number, optional) - Number of posts

### Configuration

**Authentication**: None required (public API)

**Rate Limiting**: Reddit's public JSON endpoints have rate limits. The server respects these automatically.

## GitHub MCP Server

### Purpose

Direct GitHub integration for AI tools with natural language interactions.

### Value Over gh CLI

While OaK agents can use `gh` CLI via Bash tool, GitHub MCP provides:

- Native integration with better context awareness
- Natural language interactions (no command construction needed)
- Richer API access (actions, security findings, dependabot)
- Better error handling and structured responses
- More capabilities than `gh` CLI alone
- Protocol layer specifically designed for AI tools

**Recommendation**: Use BOTH
- **GitHub MCP**: AI-driven workflows, natural language operations
- **gh CLI**: Scripted automation, terminal operations, existing workflows

### Use Cases

**Repository Management**:
- "Browse code in the main repository"
- "Search for authentication logic across all repos"
- "Get file contents from specific branch"

**Issue Automation**:
- "Create an issue for the bug discussed above"
- "List all high-priority bugs"
- "Update issue #123 with resolution details"

**PR Management**:
- "List open PRs and their status"
- "Create PR from feature branch"
- "Get details of PR #456 with review status"

**CI/CD Monitoring**:
- "Check GitHub Actions workflow status"
- "Why did the latest deployment fail?"
- "List failed workflow runs for debugging"

**Security Analysis**:
- "Review Dependabot alerts and security findings"
- "Check for vulnerable dependencies"
- "List security advisories affecting this project"

### Available Toolsets

The GitHub MCP server provides comprehensive API access organized into toolsets:

**Core Tools**:
- Repository management (list, get, search)
- Code search and file access
- Commit and branch operations

**Issue & PR Tools**:
- Issue CRUD operations
- Pull request management
- Label and assignee management

**CI/CD Tools**:
- Workflow run monitoring
- Job status and logs
- Actions artifact access

**Security Tools** (via GitHub API):
- Dependabot alert access
- Security advisory review
- Vulnerability scanning integration

### Available Tools

#### Repository Tools

**mcp__github__list_repos** - List repositories
```
"Show me all repositories I have access to"
```

**mcp__github__get_repo** - Get repository details
```
"Get details about the anthropic-sdk-typescript repo"
```

**mcp__github__search_code** - Search code across repositories
```
"Find all TypeScript files that use async/await"
```

**mcp__github__get_file_content** - Get file contents
```
"Show me the contents of src/index.ts from main branch"
```

#### Issue Tools

**mcp__github__list_issues** - List repository issues
```
"Show me all open bugs labeled 'critical'"
```

**mcp__github__get_issue** - Get issue details
```
"Get details of issue #123"
```

**mcp__github__create_issue** - Create new issue
```
"Create an issue for this authentication bug"
```

**mcp__github__update_issue** - Update existing issue
```
"Close issue #123 and add 'resolved' label"
```

#### Pull Request Tools

**mcp__github__list_pull_requests** - List PRs
```
"Show me all open PRs targeting main branch"
```

**mcp__github__get_pull_request** - Get PR details
```
"Get details of PR #456"
```

**mcp__github__create_pull_request** - Create new PR
```
"Create PR from feature branch to main"
```

#### GitHub Actions Tools

**mcp__github__list_workflow_runs** - List workflow runs
```
"Show me recent CI workflow runs"
```

**mcp__github__get_workflow_run** - Get workflow run details
```
"Why did workflow run #789 fail?"
```

**mcp__github__list_workflow_jobs** - List jobs in a workflow run
```
"Show me all jobs in the failed workflow run"
```

#### Commit and Branch Tools

**mcp__github__list_commits** - List repository commits
```
"Show me recent commits to the feature branch"
```

**mcp__github__get_commit** - Get commit details
```
"Get details of commit abc123"
```

**mcp__github__list_branches** - List repository branches
```
"Show me all branches in this repo"
```

### Configuration

**Authentication**: Required - GitHub Personal Access Token

**Environment Variable**: `GITHUB_MCP_TOKEN`

**Token Creation**:
1. Go to https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `read:packages`, `read:org`, `workflow`
4. Copy token and set environment variable

**Security Best Practices**:
- Never commit tokens to git
- Use environment variables for token storage
- Rotate tokens periodically
- Use fine-grained tokens when possible (if supported)
- Limit token scopes to minimum required

## Integration with OaK Agents

### Product Manager Workflows

#### Market Research (Reddit MCP)

**Scenario**: Research what developers are saying about similar tools

**Workflow**:
```
User: "Research developer sentiment about AI code assistants"

product-strategist:
  1. Uses Reddit MCP to search r/programming, r/MachineLearning, r/learnprogramming
  2. Analyzes top posts and comments from the past month
  3. Identifies common themes:
     - Productivity gains: 78% positive sentiment
     - Code quality concerns: 23% mention
     - Learning curve: frequent discussion point
  4. Generates insights report with feature recommendations
```

**MCP Tools Used**:
- `mcp__reddit__search_reddit` - Find relevant discussions
- `mcp__reddit__get_post_details` - Analyze specific threads
- `mcp__reddit__get_subreddit_top` - Trending topics

#### Issue Management (GitHub MCP)

**Scenario**: Create GitHub issues for all acceptance criteria in a spec

**Workflow**:
```
User: "Create GitHub issues for all tasks in the OAuth2 spec"

project-manager:
  1. Reads specification sections
  2. Extracts acceptance criteria and tasks
  3. Uses GitHub MCP to create structured issues
  4. Links issues to spec file in issue body
  5. Assigns appropriate labels (feature, security, testing)
  6. Sets milestone for sprint
  Result: 8 issues created with complete context
```

**MCP Tools Used**:
- `mcp__github__create_issue` - Create issues
- `mcp__github__list_repos` - Verify target repository
- `mcp__github__update_issue` - Add labels and milestones

### Engineer Workflows

#### Code Review (GitHub MCP)

**Scenario**: Review open PRs and identify issues

**Workflow**:
```
User: "Review open PRs in the project"

git-workflow-manager:
  1. Uses GitHub MCP to fetch open PRs
  2. Gets PR details including changed files
  3. Analyzes code changes for patterns
  4. Identifies potential issues
  5. Generates review comments
```

**MCP Tools Used**:
- `mcp__github__list_pull_requests` - Get open PRs
- `mcp__github__get_pull_request` - PR details
- `mcp__github__get_file_content` - Review changed files

#### CI/CD Monitoring (GitHub MCP)

**Scenario**: Diagnose deployment failure

**Workflow**:
```
User: "Why did the deployment fail?"

infrastructure-specialist:
  1. Uses GitHub MCP to check Actions workflow status
  2. Retrieves most recent workflow run
  3. Gets job details and logs
  4. Identifies failure point: "Docker build failed due to missing dependency"
  5. Analyzes error context
  6. Suggests fix: "Add 'python3-dev' to Dockerfile apt-get install"
```

**MCP Tools Used**:
- `mcp__github__list_workflow_runs` - Get recent runs
- `mcp__github__get_workflow_run` - Run details
- `mcp__github__list_workflow_jobs` - Job-level information

### Combined Workflows

#### Feature Validation Pipeline

**Scenario**: Validate feature idea with community + create implementation issues

**Workflow**:
```
User: "Validate and plan automatic PR description generation feature"

Combined workflow:
  1. product-strategist + Reddit MCP:
     - Search r/programming for "PR description automation"
     - Analyze sentiment and demand signals
     - Find 15+ discussions, 87% positive sentiment
     - Validate: High demand confirmed

  2. spec-manager:
     - Create feature specification
     - Define acceptance criteria
     - Document technical requirements

  3. project-manager + GitHub MCP:
     - Create implementation issues
     - Link to specification
     - Assign to appropriate team members
     - Set priority labels
```

## Troubleshooting

### Reddit MCP Issues

**Problem**: No results returned for subreddit

**Solutions**:
- Check subreddit name spelling (no r/ prefix)
- Verify subreddit is public
- Try broader search terms
- Check if subreddit exists

**Problem**: Rate limit errors

**Solutions**:
- Reddit's public API has rate limits
- Add delays between requests
- Reduce number of requests
- Consider caching results

### GitHub MCP Issues

**Problem**: Authentication failed

**Solutions**:
- Verify `GITHUB_MCP_TOKEN` is set: `echo $GITHUB_MCP_TOKEN`
- Check token hasn't expired
- Verify required scopes are granted
- Regenerate token if necessary

**Problem**: Permission denied errors

**Solutions**:
- Check token has required scopes
- Verify access to target repository
- Check organization permissions
- Use correct repository owner/name

**Problem**: Rate limiting

**Solutions**:
- GitHub API: 5000 requests/hour for authenticated users
- Use conditional requests when possible
- Cache frequently accessed data
- Respect rate limit headers

**Problem**: Server not starting

**Solutions**:
```bash
# Rebuild MCP servers
cd /Users/robertnyborg/Projects/claude-oak-agents/mcp
rm -rf dist node_modules
npm install
npm run build

# Check Node.js version (requires 18+)
node --version

# Verify configuration
cat mcp_config_template.json
```

## Testing Integration

### Test Reddit MCP

```bash
# Test server directly
cd /Users/robertnyborg/Projects/claude-oak-agents/mcp
node dist/reddit-server.js <<EOF
{"jsonrpc":"2.0","id":1,"method":"tools/list"}
EOF
```

### Test GitHub MCP

```bash
# Set token
export GITHUB_MCP_TOKEN="your_token_here"

# Test server
node dist/github-server.js <<EOF
{"jsonrpc":"2.0","id":1,"method":"tools/list"}
EOF
```

### Test from Claude Code

Once configured, test with natural language commands:

**Reddit**:
```
"Show me top posts from r/programming today"
```

**GitHub**:
```
"List my repositories sorted by recent updates"
```

## Best Practices

### Reddit MCP

1. **Be Specific**: Use targeted subreddits for better signal-to-noise ratio
2. **Time Filters**: Use appropriate time filters to get relevant discussions
3. **Comment Analysis**: Include top comments for full context
4. **Sentiment Analysis**: Look for patterns across multiple threads
5. **Rate Limiting**: Respect Reddit's API limits, add delays if needed

### GitHub MCP

1. **Token Security**: Never commit tokens, use environment variables
2. **Scope Minimization**: Only grant required scopes
3. **Error Handling**: Check for API errors and rate limits
4. **Batch Operations**: Group related operations when possible
5. **Audit Trail**: Log important operations for compliance

### Integration Patterns

1. **Separation of Concerns**: Reddit for research, GitHub for execution
2. **Workflow Chaining**: Use product-strategist → spec-manager → project-manager flows
3. **Context Preservation**: Link issues to specifications and research
4. **Telemetry**: Track MCP usage via oak-telemetry server
5. **Fallback**: Have manual processes when MCP unavailable

## Future Enhancements

### Planned Features

- [ ] Reddit sentiment analysis integration
- [ ] GitHub security scanning via MCP
- [ ] Automated issue triage workflows
- [ ] Reddit community health metrics
- [ ] GitHub repository insights dashboard
- [ ] Cross-reference Reddit discussions with GitHub issues
- [ ] Automated competitive analysis
- [ ] Community-driven feature prioritization

### Integration Roadmap

**Phase 1** (Current): Basic Reddit and GitHub MCP access
**Phase 2**: Enhanced analytics and sentiment analysis
**Phase 3**: Automated workflow orchestration
**Phase 4**: ML-powered insights and recommendations
**Phase 5**: Real-time monitoring and alerts
**Phase 6**: Community-driven development workflows

## Resources

### Official Documentation

- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [Anthropic MCP Documentation](https://docs.anthropic.com/mcp)
- [Reddit API Documentation](https://www.reddit.com/dev/api)
- [GitHub REST API Documentation](https://docs.github.com/rest)

### OaK Documentation

- [MCP Server README](../mcp/README.md)
- [OaK Multi-File Agents](../docs/MULTI_FILE_AGENTS.md)
- [OaK Migration Guide](../docs/MIGRATION_GUIDE.md)
- [Agent Development Guide](../docs/by-role/engineers/agent-development.md)

### Tools and Libraries

- [@modelcontextprotocol/sdk](https://www.npmjs.com/package/@modelcontextprotocol/sdk)
- [GitHub CLI (gh)](https://cli.github.com/)
- [Reddit JSON Endpoints](https://github.com/reddit-archive/reddit/wiki/JSON)

## Support

For issues or questions:
- Check [Troubleshooting](#troubleshooting) section
- Review MCP server logs in Claude Code
- Test servers directly with command-line JSON-RPC
- Verify environment variables and configuration
- Ensure latest MCP server build (`npm run build`)

## Version History

- **v1.0.0** (2025-11-08): Initial Reddit and GitHub MCP server integration
  - Reddit public API support (subreddits, search, posts, comments, users)
  - GitHub comprehensive API support (repos, issues, PRs, actions, commits)
  - Full documentation and examples
  - Integration with OaK agent workflows
