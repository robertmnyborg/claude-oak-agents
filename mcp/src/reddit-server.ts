#!/usr/bin/env node

/**
 * Reddit MCP Server for OaK Agents
 *
 * Provides access to Reddit's public API for content analysis and community research.
 * No authentication required - uses public Reddit JSON endpoints.
 *
 * Features:
 * - Browse frontpage and trending posts
 * - Access posts, comments, and community data from any subreddit
 * - Search across Reddit
 * - Get user profiles (public data only)
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ListToolsRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

interface RedditPost {
  title: string;
  author: string;
  subreddit: string;
  score: number;
  num_comments: number;
  created_utc: number;
  permalink: string;
  url: string;
  selftext?: string;
  is_self: boolean;
}

interface RedditComment {
  author: string;
  body: string;
  score: number;
  created_utc: number;
  permalink: string;
}

class RedditMCPServer {
  private server: Server;
  private readonly baseUrl = "https://www.reddit.com";

  constructor() {
    this.server = new Server(
      {
        name: "reddit",
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
      console.error("[Reddit MCP Error]", error);
    };

    process.on("SIGINT", async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private async fetchReddit(endpoint: string): Promise<any> {
    const url = `${this.baseUrl}${endpoint}.json`;
    const headers = {
      "User-Agent": "OaK-Agents-MCP/1.0.0 (Research Tool)",
    };

    try {
      const response = await fetch(url, { headers });

      if (!response.ok) {
        throw new Error(`Reddit API error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      throw new Error(`Failed to fetch from Reddit: ${error}`);
    }
  }

  private parsePost(data: any): RedditPost {
    return {
      title: data.title,
      author: data.author,
      subreddit: data.subreddit,
      score: data.score,
      num_comments: data.num_comments,
      created_utc: data.created_utc,
      permalink: `https://reddit.com${data.permalink}`,
      url: data.url,
      selftext: data.selftext,
      is_self: data.is_self,
    };
  }

  private parseComment(data: any): RedditComment {
    return {
      author: data.author,
      body: data.body,
      score: data.score,
      created_utc: data.created_utc,
      permalink: `https://reddit.com${data.permalink}`,
    };
  }

  private setupHandlers(): void {
    // List available resources
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => {
      return {
        resources: [
          {
            uri: "reddit://frontpage",
            name: "Reddit Frontpage",
            description: "Current Reddit frontpage posts",
            mimeType: "application/json",
          },
          {
            uri: "reddit://popular",
            name: "Popular Posts",
            description: "Currently popular posts across Reddit",
            mimeType: "application/json",
          },
          {
            uri: "reddit://all",
            name: "All Posts",
            description: "Posts from r/all",
            mimeType: "application/json",
          },
        ],
      };
    });

    // Read resource handler
    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      const uri = request.params.uri;

      if (uri === "reddit://frontpage") {
        const data = await this.fetchReddit("/");
        const posts = data.data.children.map((child: any) => this.parsePost(child.data));
        return {
          contents: [
            {
              uri,
              mimeType: "application/json",
              text: JSON.stringify(posts, null, 2),
            },
          ],
        };
      }

      if (uri === "reddit://popular") {
        const data = await this.fetchReddit("/r/popular");
        const posts = data.data.children.map((child: any) => this.parsePost(child.data));
        return {
          contents: [
            {
              uri,
              mimeType: "application/json",
              text: JSON.stringify(posts, null, 2),
            },
          ],
        };
      }

      if (uri === "reddit://all") {
        const data = await this.fetchReddit("/r/all");
        const posts = data.data.children.map((child: any) => this.parsePost(child.data));
        return {
          contents: [
            {
              uri,
              mimeType: "application/json",
              text: JSON.stringify(posts, null, 2),
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
          {
            name: "get_subreddit_hot",
            description: "Get hot posts from a specific subreddit",
            inputSchema: {
              type: "object",
              properties: {
                subreddit: {
                  type: "string",
                  description: "Subreddit name (without r/ prefix)",
                },
                limit: {
                  type: "number",
                  description: "Number of posts to retrieve (default: 25, max: 100)",
                  default: 25,
                },
              },
              required: ["subreddit"],
            },
          },
          {
            name: "get_subreddit_new",
            description: "Get newest posts from a specific subreddit",
            inputSchema: {
              type: "object",
              properties: {
                subreddit: {
                  type: "string",
                  description: "Subreddit name (without r/ prefix)",
                },
                limit: {
                  type: "number",
                  description: "Number of posts to retrieve (default: 25, max: 100)",
                  default: 25,
                },
              },
              required: ["subreddit"],
            },
          },
          {
            name: "get_subreddit_top",
            description: "Get top posts from a specific subreddit",
            inputSchema: {
              type: "object",
              properties: {
                subreddit: {
                  type: "string",
                  description: "Subreddit name (without r/ prefix)",
                },
                time_filter: {
                  type: "string",
                  description: "Time period (hour, day, week, month, year, all)",
                  enum: ["hour", "day", "week", "month", "year", "all"],
                  default: "day",
                },
                limit: {
                  type: "number",
                  description: "Number of posts to retrieve (default: 25, max: 100)",
                  default: 25,
                },
              },
              required: ["subreddit"],
            },
          },
          {
            name: "get_post_details",
            description: "Get detailed information about a specific post including comments",
            inputSchema: {
              type: "object",
              properties: {
                subreddit: {
                  type: "string",
                  description: "Subreddit name (without r/ prefix)",
                },
                post_id: {
                  type: "string",
                  description: "Reddit post ID",
                },
                comment_limit: {
                  type: "number",
                  description: "Number of top-level comments to retrieve (default: 10)",
                  default: 10,
                },
              },
              required: ["subreddit", "post_id"],
            },
          },
          {
            name: "search_reddit",
            description: "Search across Reddit or within a specific subreddit",
            inputSchema: {
              type: "object",
              properties: {
                query: {
                  type: "string",
                  description: "Search query",
                },
                subreddit: {
                  type: "string",
                  description: "Optional: Limit search to specific subreddit (without r/ prefix)",
                },
                sort: {
                  type: "string",
                  description: "Sort order (relevance, hot, top, new, comments)",
                  enum: ["relevance", "hot", "top", "new", "comments"],
                  default: "relevance",
                },
                time_filter: {
                  type: "string",
                  description: "Time period for search (hour, day, week, month, year, all)",
                  enum: ["hour", "day", "week", "month", "year", "all"],
                  default: "all",
                },
                limit: {
                  type: "number",
                  description: "Number of results (default: 25, max: 100)",
                  default: 25,
                },
              },
              required: ["query"],
            },
          },
          {
            name: "get_user_posts",
            description: "Get public posts from a Reddit user",
            inputSchema: {
              type: "object",
              properties: {
                username: {
                  type: "string",
                  description: "Reddit username (without u/ prefix)",
                },
                sort: {
                  type: "string",
                  description: "Sort order (new, hot, top, controversial)",
                  enum: ["new", "hot", "top", "controversial"],
                  default: "new",
                },
                limit: {
                  type: "number",
                  description: "Number of posts (default: 25, max: 100)",
                  default: 25,
                },
              },
              required: ["username"],
            },
          },
        ],
      };
    });

    // Call tool handler
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        if (name === "get_subreddit_hot") {
          const { subreddit, limit = 25 } = args as { subreddit: string; limit?: number };
          const data = await this.fetchReddit(`/r/${subreddit}/hot?limit=${Math.min(limit, 100)}`);
          const posts = data.data.children.map((child: any) => this.parsePost(child.data));

          return {
            content: [
              {
                type: "text",
                text: JSON.stringify({ subreddit, count: posts.length, posts }, null, 2),
              },
            ],
          };
        }

        if (name === "get_subreddit_new") {
          const { subreddit, limit = 25 } = args as { subreddit: string; limit?: number };
          const data = await this.fetchReddit(`/r/${subreddit}/new?limit=${Math.min(limit, 100)}`);
          const posts = data.data.children.map((child: any) => this.parsePost(child.data));

          return {
            content: [
              {
                type: "text",
                text: JSON.stringify({ subreddit, count: posts.length, posts }, null, 2),
              },
            ],
          };
        }

        if (name === "get_subreddit_top") {
          const { subreddit, time_filter = "day", limit = 25 } = args as {
            subreddit: string;
            time_filter?: string;
            limit?: number
          };
          const data = await this.fetchReddit(`/r/${subreddit}/top?t=${time_filter}&limit=${Math.min(limit, 100)}`);
          const posts = data.data.children.map((child: any) => this.parsePost(child.data));

          return {
            content: [
              {
                type: "text",
                text: JSON.stringify({ subreddit, time_filter, count: posts.length, posts }, null, 2),
              },
            ],
          };
        }

        if (name === "get_post_details") {
          const { subreddit, post_id, comment_limit = 10 } = args as {
            subreddit: string;
            post_id: string;
            comment_limit?: number
          };
          const data = await this.fetchReddit(`/r/${subreddit}/comments/${post_id}?limit=${comment_limit}`);

          const post = this.parsePost(data[0].data.children[0].data);
          const comments = data[1].data.children
            .filter((child: any) => child.kind === "t1")
            .map((child: any) => this.parseComment(child.data))
            .slice(0, comment_limit);

          return {
            content: [
              {
                type: "text",
                text: JSON.stringify({ post, comments, comment_count: comments.length }, null, 2),
              },
            ],
          };
        }

        if (name === "search_reddit") {
          const { query, subreddit, sort = "relevance", time_filter = "all", limit = 25 } = args as {
            query: string;
            subreddit?: string;
            sort?: string;
            time_filter?: string;
            limit?: number;
          };

          const searchPath = subreddit ? `/r/${subreddit}/search` : "/search";
          const params = new URLSearchParams({
            q: query,
            sort,
            t: time_filter,
            limit: Math.min(limit, 100).toString(),
            restrict_sr: subreddit ? "true" : "false",
          });

          const data = await this.fetchReddit(`${searchPath}?${params}`);
          const posts = data.data.children.map((child: any) => this.parsePost(child.data));

          return {
            content: [
              {
                type: "text",
                text: JSON.stringify({
                  query,
                  subreddit: subreddit || "all",
                  count: posts.length,
                  posts
                }, null, 2),
              },
            ],
          };
        }

        if (name === "get_user_posts") {
          const { username, sort = "new", limit = 25 } = args as {
            username: string;
            sort?: string;
            limit?: number;
          };

          const data = await this.fetchReddit(`/user/${username}/submitted?sort=${sort}&limit=${Math.min(limit, 100)}`);
          const posts = data.data.children.map((child: any) => this.parsePost(child.data));

          return {
            content: [
              {
                type: "text",
                text: JSON.stringify({ username, count: posts.length, posts }, null, 2),
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
    console.error("Reddit MCP server running on stdio");
  }
}

const server = new RedditMCPServer();
server.run().catch(console.error);
