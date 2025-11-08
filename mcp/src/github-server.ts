#!/usr/bin/env node

/**
 * GitHub MCP Server for OaK Agents
 *
 * Provides direct GitHub integration for AI tools with natural language interactions.
 * Supports repository management, issue/PR automation, CI/CD intelligence, and code analysis.
 *
 * Features:
 * - Repository browsing, code search, commit analysis
 * - Issue and PR management
 * - GitHub Actions monitoring
 * - Security findings and Dependabot alerts
 * - Better than gh CLI: protocol layer for AI tools with structured responses
 *
 * Authentication: Requires GitHub Personal Access Token (PAT)
 * Required scopes: repo, read:packages, read:org, workflow
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ListToolsRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

interface GitHubConfig {
  token: string;
  baseUrl: string;
}

interface Repository {
  name: string;
  full_name: string;
  description: string;
  private: boolean;
  html_url: string;
  default_branch: string;
  language: string;
  stargazers_count: number;
  updated_at: string;
}

interface Issue {
  number: number;
  title: string;
  state: string;
  user: { login: string };
  body: string;
  labels: Array<{ name: string }>;
  created_at: string;
  updated_at: string;
  html_url: string;
}

interface PullRequest extends Issue {
  head: { ref: string };
  base: { ref: string };
  merged: boolean;
  draft: boolean;
}

class GitHubMCPServer {
  private server: Server;
  private config: GitHubConfig;

  constructor() {
    const token = process.env.GITHUB_MCP_TOKEN || process.env.GITHUB_TOKEN;

    if (!token) {
      throw new Error(
        "GitHub token not found. Set GITHUB_MCP_TOKEN or GITHUB_TOKEN environment variable.\n" +
        "Create token at: https://github.com/settings/tokens\n" +
        "Required scopes: repo, read:packages, read:org, workflow"
      );
    }

    this.config = {
      token,
      baseUrl: "https://api.github.com",
    };

    this.server = new Server(
      {
        name: "github",
        version: "1.0.0",
      },
      {
        capabilities: {
          resources: {},
          tools: {},
        },
      }
    );

    this.setupHandlers();
    this.setupErrorHandling();
  }

  private setupErrorHandling(): void {
    this.server.onerror = (error) => {
      console.error("[GitHub MCP Error]", error);
    };

    process.on("SIGINT", async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private async githubRequest(endpoint: string, options: RequestInit = {}): Promise<any> {
    const url = `${this.config.baseUrl}${endpoint}`;
    const headers = {
      Authorization: `Bearer ${this.config.token}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "OaK-Agents-MCP/1.0.0",
      ...options.headers,
    };

    try {
      const response = await fetch(url, { ...options, headers });

      if (!response.ok) {
        const errorBody = await response.text();
        throw new Error(`GitHub API error: ${response.status} ${response.statusText}\n${errorBody}`);
      }

      return await response.json();
    } catch (error) {
      throw new Error(`Failed to fetch from GitHub: ${error}`);
    }
  }

  private setupHandlers(): void {
    // List available resources
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => {
      return {
        resources: [
          {
            uri: "github://user/repos",
            name: "User Repositories",
            description: "Repositories accessible to the authenticated user",
            mimeType: "application/json",
          },
          {
            uri: "github://user/profile",
            name: "User Profile",
            description: "Authenticated user profile information",
            mimeType: "application/json",
          },
        ],
      };
    });

    // Read resource handler
    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      const uri = request.params.uri;

      if (uri === "github://user/repos") {
        const repos = await this.githubRequest("/user/repos?per_page=100&sort=updated");
        return {
          contents: [
            {
              uri,
              mimeType: "application/json",
              text: JSON.stringify(repos, null, 2),
            },
          ],
        };
      }

      if (uri === "github://user/profile") {
        const user = await this.githubRequest("/user");
        return {
          contents: [
            {
              uri,
              mimeType: "application/json",
              text: JSON.stringify(user, null, 2),
            },
          ],
        };
      }

      throw new Error(`Unknown resource: ${uri}`);
    });

    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          // Repository Tools
          {
            name: "list_repos",
            description: "List repositories for a user or organization",
            inputSchema: {
              type: "object",
              properties: {
                owner: {
                  type: "string",
                  description: "Username or organization name (optional, defaults to authenticated user)",
                },
                type: {
                  type: "string",
                  description: "Repository type filter",
                  enum: ["all", "owner", "public", "private", "member"],
                  default: "all",
                },
                sort: {
                  type: "string",
                  description: "Sort by",
                  enum: ["created", "updated", "pushed", "full_name"],
                  default: "updated",
                },
                per_page: {
                  type: "number",
                  description: "Results per page (max 100)",
                  default: 30,
                },
              },
            },
          },
          {
            name: "get_repo",
            description: "Get detailed information about a specific repository",
            inputSchema: {
              type: "object",
              properties: {
                owner: {
                  type: "string",
                  description: "Repository owner (username or org)",
                },
                repo: {
                  type: "string",
                  description: "Repository name",
                },
              },
              required: ["owner", "repo"],
            },
          },
          {
            name: "search_code",
            description: "Search for code across GitHub repositories",
            inputSchema: {
              type: "object",
              properties: {
                query: {
                  type: "string",
                  description: "Search query (e.g., 'language:typescript async function')",
                },
                owner: {
                  type: "string",
                  description: "Optional: Limit search to specific owner/org",
                },
                repo: {
                  type: "string",
                  description: "Optional: Limit search to specific repository",
                },
                per_page: {
                  type: "number",
                  description: "Results per page (max 100)",
                  default: 30,
                },
              },
              required: ["query"],
            },
          },
          {
            name: "get_file_content",
            description: "Get contents of a file from a repository",
            inputSchema: {
              type: "object",
              properties: {
                owner: {
                  type: "string",
                  description: "Repository owner",
                },
                repo: {
                  type: "string",
                  description: "Repository name",
                },
                path: {
                  type: "string",
                  description: "File path in repository",
                },
                ref: {
                  type: "string",
                  description: "Branch, tag, or commit SHA (optional, defaults to default branch)",
                },
              },
              required: ["owner", "repo", "path"],
            },
          },

          // Issue Tools
          {
            name: "list_issues",
            description: "List issues for a repository",
            inputSchema: {
              type: "object",
              properties: {
                owner: {
                  type: "string",
                  description: "Repository owner",
                },
                repo: {
                  type: "string",
                  description: "Repository name",
                },
                state: {
                  type: "string",
                  description: "Issue state",
                  enum: ["open", "closed", "all"],
                  default: "open",
                },
                labels: {
                  type: "string",
                  description: "Comma-separated list of label names",
                },
                per_page: {
                  type: "number",
                  description: "Results per page (max 100)",
                  default: 30,
                },
              },
              required: ["owner", "repo"],
            },
          },
          {
            name: "get_issue",
            description: "Get details of a specific issue",
            inputSchema: {
              type: "object",
              properties: {
                owner: {
                  type: "string",
                  description: "Repository owner",
                },
                repo: {
                  type: "string",
                  description: "Repository name",
                },
                issue_number: {
                  type: "number",
                  description: "Issue number",
                },
              },
              required: ["owner", "repo", "issue_number"],
            },
          },
          {
            name: "create_issue",
            description: "Create a new issue in a repository",
            inputSchema: {
              type: "object",
              properties: {
                owner: {
                  type: "string",
                  description: "Repository owner",
                },
                repo: {
                  type: "string",
                  description: "Repository name",
                },
                title: {
                  type: "string",
                  description: "Issue title",
                },
                body: {
                  type: "string",
                  description: "Issue description/body",
                },
                labels: {
                  type: "array",
                  items: { type: "string" },
                  description: "Array of label names",
                },
                assignees: {
                  type: "array",
                  items: { type: "string" },
                  description: "Array of usernames to assign",
                },
              },
              required: ["owner", "repo", "title"],
            },
          },
          {
            name: "update_issue",
            description: "Update an existing issue",
            inputSchema: {
              type: "object",
              properties: {
                owner: {
                  type: "string",
                  description: "Repository owner",
                },
                repo: {
                  type: "string",
                  description: "Repository name",
                },
                issue_number: {
                  type: "number",
                  description: "Issue number",
                },
                title: {
                  type: "string",
                  description: "New title",
                },
                body: {
                  type: "string",
                  description: "New body",
                },
                state: {
                  type: "string",
                  enum: ["open", "closed"],
                  description: "New state",
                },
                labels: {
                  type: "array",
                  items: { type: "string" },
                  description: "Array of label names",
                },
              },
              required: ["owner", "repo", "issue_number"],
            },
          },

          // Pull Request Tools
          {
            name: "list_pull_requests",
            description: "List pull requests for a repository",
            inputSchema: {
              type: "object",
              properties: {
                owner: {
                  type: "string",
                  description: "Repository owner",
                },
                repo: {
                  type: "string",
                  description: "Repository name",
                },
                state: {
                  type: "string",
                  description: "PR state",
                  enum: ["open", "closed", "all"],
                  default: "open",
                },
                base: {
                  type: "string",
                  description: "Filter by base branch",
                },
                per_page: {
                  type: "number",
                  description: "Results per page (max 100)",
                  default: 30,
                },
              },
              required: ["owner", "repo"],
            },
          },
          {
            name: "get_pull_request",
            description: "Get details of a specific pull request",
            inputSchema: {
              type: "object",
              properties: {
                owner: {
                  type: "string",
                  description: "Repository owner",
                },
                repo: {
                  type: "string",
                  description: "Repository name",
                },
                pull_number: {
                  type: "number",
                  description: "Pull request number",
                },
              },
              required: ["owner", "repo", "pull_number"],
            },
          },
          {
            name: "create_pull_request",
            description: "Create a new pull request",
            inputSchema: {
              type: "object",
              properties: {
                owner: {
                  type: "string",
                  description: "Repository owner",
                },
                repo: {
                  type: "string",
                  description: "Repository name",
                },
                title: {
                  type: "string",
                  description: "PR title",
                },
                body: {
                  type: "string",
                  description: "PR description",
                },
                head: {
                  type: "string",
                  description: "Branch containing changes",
                },
                base: {
                  type: "string",
                  description: "Branch to merge into",
                },
                draft: {
                  type: "boolean",
                  description: "Create as draft PR",
                  default: false,
                },
              },
              required: ["owner", "repo", "title", "head", "base"],
            },
          },

          // GitHub Actions Tools
          {
            name: "list_workflow_runs",
            description: "List workflow runs for a repository",
            inputSchema: {
              type: "object",
              properties: {
                owner: {
                  type: "string",
                  description: "Repository owner",
                },
                repo: {
                  type: "string",
                  description: "Repository name",
                },
                workflow_id: {
                  type: "string",
                  description: "Optional: Specific workflow ID or filename",
                },
                branch: {
                  type: "string",
                  description: "Optional: Filter by branch",
                },
                status: {
                  type: "string",
                  description: "Optional: Filter by status",
                  enum: ["completed", "action_required", "cancelled", "failure", "neutral", "skipped", "stale", "success", "timed_out", "in_progress", "queued", "requested", "waiting"],
                },
                per_page: {
                  type: "number",
                  description: "Results per page (max 100)",
                  default: 30,
                },
              },
              required: ["owner", "repo"],
            },
          },
          {
            name: "get_workflow_run",
            description: "Get details of a specific workflow run",
            inputSchema: {
              type: "object",
              properties: {
                owner: {
                  type: "string",
                  description: "Repository owner",
                },
                repo: {
                  type: "string",
                  description: "Repository name",
                },
                run_id: {
                  type: "number",
                  description: "Workflow run ID",
                },
              },
              required: ["owner", "repo", "run_id"],
            },
          },
          {
            name: "list_workflow_jobs",
            description: "List jobs for a workflow run",
            inputSchema: {
              type: "object",
              properties: {
                owner: {
                  type: "string",
                  description: "Repository owner",
                },
                repo: {
                  type: "string",
                  description: "Repository name",
                },
                run_id: {
                  type: "number",
                  description: "Workflow run ID",
                },
              },
              required: ["owner", "repo", "run_id"],
            },
          },

          // Commit and Branch Tools
          {
            name: "list_commits",
            description: "List commits for a repository",
            inputSchema: {
              type: "object",
              properties: {
                owner: {
                  type: "string",
                  description: "Repository owner",
                },
                repo: {
                  type: "string",
                  description: "Repository name",
                },
                sha: {
                  type: "string",
                  description: "Branch or commit SHA",
                },
                path: {
                  type: "string",
                  description: "Only commits containing this file path",
                },
                per_page: {
                  type: "number",
                  description: "Results per page (max 100)",
                  default: 30,
                },
              },
              required: ["owner", "repo"],
            },
          },
          {
            name: "get_commit",
            description: "Get a specific commit",
            inputSchema: {
              type: "object",
              properties: {
                owner: {
                  type: "string",
                  description: "Repository owner",
                },
                repo: {
                  type: "string",
                  description: "Repository name",
                },
                ref: {
                  type: "string",
                  description: "Commit SHA",
                },
              },
              required: ["owner", "repo", "ref"],
            },
          },
          {
            name: "list_branches",
            description: "List branches for a repository",
            inputSchema: {
              type: "object",
              properties: {
                owner: {
                  type: "string",
                  description: "Repository owner",
                },
                repo: {
                  type: "string",
                  description: "Repository name",
                },
                per_page: {
                  type: "number",
                  description: "Results per page (max 100)",
                  default: 30,
                },
              },
              required: ["owner", "repo"],
            },
          },
        ],
      };
    });

    // Call tool handler
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        // Repository Tools
        if (name === "list_repos") {
          const { owner, type = "all", sort = "updated", per_page = 30 } = args as any;
          const endpoint = owner
            ? `/users/${owner}/repos?type=${type}&sort=${sort}&per_page=${per_page}`
            : `/user/repos?type=${type}&sort=${sort}&per_page=${per_page}`;

          const repos = await this.githubRequest(endpoint);
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify({ count: repos.length, repositories: repos }, null, 2),
              },
            ],
          };
        }

        if (name === "get_repo") {
          const { owner, repo } = args as { owner: string; repo: string };
          const repository = await this.githubRequest(`/repos/${owner}/${repo}`);
          return {
            content: [{ type: "text", text: JSON.stringify(repository, null, 2) }],
          };
        }

        if (name === "search_code") {
          const { query, owner, repo, per_page = 30 } = args as any;
          let searchQuery = query;

          if (owner && repo) {
            searchQuery = `${query} repo:${owner}/${repo}`;
          } else if (owner) {
            searchQuery = `${query} user:${owner}`;
          }

          const results = await this.githubRequest(`/search/code?q=${encodeURIComponent(searchQuery)}&per_page=${per_page}`);
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify({ query: searchQuery, total_count: results.total_count, items: results.items }, null, 2),
              },
            ],
          };
        }

        if (name === "get_file_content") {
          const { owner, repo, path, ref } = args as any;
          const endpoint = `/repos/${owner}/${repo}/contents/${path}${ref ? `?ref=${ref}` : ""}`;
          const content = await this.githubRequest(endpoint);

          // Decode base64 content if present
          if (content.content && content.encoding === "base64") {
            content.decoded_content = Buffer.from(content.content, "base64").toString("utf-8");
          }

          return {
            content: [{ type: "text", text: JSON.stringify(content, null, 2) }],
          };
        }

        // Issue Tools
        if (name === "list_issues") {
          const { owner, repo, state = "open", labels, per_page = 30 } = args as any;
          let endpoint = `/repos/${owner}/${repo}/issues?state=${state}&per_page=${per_page}`;
          if (labels) {
            endpoint += `&labels=${encodeURIComponent(labels)}`;
          }

          const issues = await this.githubRequest(endpoint);
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify({ count: issues.length, issues }, null, 2),
              },
            ],
          };
        }

        if (name === "get_issue") {
          const { owner, repo, issue_number } = args as any;
          const issue = await this.githubRequest(`/repos/${owner}/${repo}/issues/${issue_number}`);
          return {
            content: [{ type: "text", text: JSON.stringify(issue, null, 2) }],
          };
        }

        if (name === "create_issue") {
          const { owner, repo, title, body, labels, assignees } = args as any;
          const payload: any = { title };
          if (body) payload.body = body;
          if (labels) payload.labels = labels;
          if (assignees) payload.assignees = assignees;

          const issue = await this.githubRequest(`/repos/${owner}/${repo}/issues`, {
            method: "POST",
            body: JSON.stringify(payload),
          });

          return {
            content: [{ type: "text", text: JSON.stringify(issue, null, 2) }],
          };
        }

        if (name === "update_issue") {
          const { owner, repo, issue_number, title, body, state, labels } = args as any;
          const payload: any = {};
          if (title) payload.title = title;
          if (body) payload.body = body;
          if (state) payload.state = state;
          if (labels) payload.labels = labels;

          const issue = await this.githubRequest(`/repos/${owner}/${repo}/issues/${issue_number}`, {
            method: "PATCH",
            body: JSON.stringify(payload),
          });

          return {
            content: [{ type: "text", text: JSON.stringify(issue, null, 2) }],
          };
        }

        // Pull Request Tools
        if (name === "list_pull_requests") {
          const { owner, repo, state = "open", base, per_page = 30 } = args as any;
          let endpoint = `/repos/${owner}/${repo}/pulls?state=${state}&per_page=${per_page}`;
          if (base) {
            endpoint += `&base=${base}`;
          }

          const pulls = await this.githubRequest(endpoint);
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify({ count: pulls.length, pull_requests: pulls }, null, 2),
              },
            ],
          };
        }

        if (name === "get_pull_request") {
          const { owner, repo, pull_number } = args as any;
          const pr = await this.githubRequest(`/repos/${owner}/${repo}/pulls/${pull_number}`);
          return {
            content: [{ type: "text", text: JSON.stringify(pr, null, 2) }],
          };
        }

        if (name === "create_pull_request") {
          const { owner, repo, title, body, head, base, draft = false } = args as any;
          const payload: any = { title, head, base, draft };
          if (body) payload.body = body;

          const pr = await this.githubRequest(`/repos/${owner}/${repo}/pulls`, {
            method: "POST",
            body: JSON.stringify(payload),
          });

          return {
            content: [{ type: "text", text: JSON.stringify(pr, null, 2) }],
          };
        }

        // GitHub Actions Tools
        if (name === "list_workflow_runs") {
          const { owner, repo, workflow_id, branch, status, per_page = 30 } = args as any;
          let endpoint = workflow_id
            ? `/repos/${owner}/${repo}/actions/workflows/${workflow_id}/runs?per_page=${per_page}`
            : `/repos/${owner}/${repo}/actions/runs?per_page=${per_page}`;

          if (branch) endpoint += `&branch=${branch}`;
          if (status) endpoint += `&status=${status}`;

          const runs = await this.githubRequest(endpoint);
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify({ total_count: runs.total_count, workflow_runs: runs.workflow_runs }, null, 2),
              },
            ],
          };
        }

        if (name === "get_workflow_run") {
          const { owner, repo, run_id } = args as any;
          const run = await this.githubRequest(`/repos/${owner}/${repo}/actions/runs/${run_id}`);
          return {
            content: [{ type: "text", text: JSON.stringify(run, null, 2) }],
          };
        }

        if (name === "list_workflow_jobs") {
          const { owner, repo, run_id } = args as any;
          const jobs = await this.githubRequest(`/repos/${owner}/${repo}/actions/runs/${run_id}/jobs`);
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify({ total_count: jobs.total_count, jobs: jobs.jobs }, null, 2),
              },
            ],
          };
        }

        // Commit and Branch Tools
        if (name === "list_commits") {
          const { owner, repo, sha, path, per_page = 30 } = args as any;
          let endpoint = `/repos/${owner}/${repo}/commits?per_page=${per_page}`;
          if (sha) endpoint += `&sha=${sha}`;
          if (path) endpoint += `&path=${encodeURIComponent(path)}`;

          const commits = await this.githubRequest(endpoint);
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify({ count: commits.length, commits }, null, 2),
              },
            ],
          };
        }

        if (name === "get_commit") {
          const { owner, repo, ref } = args as any;
          const commit = await this.githubRequest(`/repos/${owner}/${repo}/commits/${ref}`);
          return {
            content: [{ type: "text", text: JSON.stringify(commit, null, 2) }],
          };
        }

        if (name === "list_branches") {
          const { owner, repo, per_page = 30 } = args as any;
          const branches = await this.githubRequest(`/repos/${owner}/${repo}/branches?per_page=${per_page}`);
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify({ count: branches.length, branches }, null, 2),
              },
            ],
          };
        }

        throw new Error(`Unknown tool: ${name}`);
      } catch (error) {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({ error: String(error) }, null, 2),
            },
          ],
          isError: true,
        };
      }
    });
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error("GitHub MCP server running on stdio");
  }
}

const server = new GitHubMCPServer();
server.run().catch(console.error);
