#!/usr/bin/env node

/**
 * OaK Agents MCP Server
 *
 * Provides access to agent metadata, definitions, and bundled scripts via MCP.
 * Supports dynamic agent discovery and script execution.
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ListToolsRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import * as fs from "fs/promises";
import * as path from "path";
import { spawn } from "child_process";

interface AgentMetadata {
  name: string;
  version: string;
  description: string;
  triggers: {
    keywords: string[];
    file_patterns: string[];
    domains: string[];
  };
  category: string;
  priority: string;
  capabilities: string[];
  scripts?: string[];
}

class OakAgentsServer {
  private server: Server;
  private agentsDir: string;
  private metadataCache: Map<string, AgentMetadata> = new Map();

  constructor() {
    this.agentsDir = process.env.OAK_AGENTS_DIR || path.join(process.env.HOME!, "Projects/claude-oak-agents/agents");

    this.server = new Server(
      {
        name: "oak-agents",
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
      console.error("[MCP Error]", error);
    };

    process.on("SIGINT", async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private setupHandlers(): void {
    // List available resources
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => {
      await this.loadMetadata();

      const resources = [
        {
          uri: "oak://agents/metadata",
          name: "All Agents Metadata",
          description: "Metadata for all available agents",
          mimeType: "application/json",
        },
      ];

      // Add individual agent resources
      for (const [name, metadata] of this.metadataCache.entries()) {
        resources.push(
          {
            uri: `oak://agents/${name}/definition`,
            name: `${name} Definition`,
            description: `Full agent definition for ${name}`,
            mimeType: "text/markdown",
          },
          {
            uri: `oak://agents/${name}/metadata`,
            name: `${name} Metadata`,
            description: `Metadata for ${name}`,
            mimeType: "application/json",
          }
        );

        if (metadata.scripts && metadata.scripts.length > 0) {
          resources.push({
            uri: `oak://agents/${name}/scripts`,
            name: `${name} Scripts`,
            description: `Bundled scripts for ${name}`,
            mimeType: "application/json",
          });
        }
      }

      return { resources };
    });

    // Read resource content
    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      const uri = request.params.uri;

      if (!uri.startsWith("oak://agents/")) {
        throw new Error(`Unknown resource: ${uri}`);
      }

      const parts = uri.replace("oak://agents/", "").split("/");

      if (parts.length === 1 && parts[0] === "metadata") {
        // All agents metadata
        await this.loadMetadata();
        return {
          contents: [
            {
              uri,
              mimeType: "application/json",
              text: JSON.stringify(Array.from(this.metadataCache.values()), null, 2),
            },
          ],
        };
      }

      if (parts.length === 2) {
        const [agentName, resourceType] = parts;

        switch (resourceType) {
          case "definition":
            return {
              contents: [
                {
                  uri,
                  mimeType: "text/markdown",
                  text: await this.getAgentDefinition(agentName),
                },
              ],
            };

          case "metadata":
            await this.loadMetadata();
            const metadata = this.metadataCache.get(agentName);
            if (!metadata) {
              throw new Error(`Agent not found: ${agentName}`);
            }
            return {
              contents: [
                {
                  uri,
                  mimeType: "application/json",
                  text: JSON.stringify(metadata, null, 2),
                },
              ],
            };

          case "scripts":
            return {
              contents: [
                {
                  uri,
                  mimeType: "application/json",
                  text: await this.getAgentScripts(agentName),
                },
              ],
            };

          default:
            throw new Error(`Unknown resource type: ${resourceType}`);
        }
      }

      throw new Error(`Invalid resource URI: ${uri}`);
    });

    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: "find_agents",
            description: "Find agents matching keywords, domains, or file patterns",
            inputSchema: {
              type: "object",
              properties: {
                keywords: {
                  type: "array",
                  items: { type: "string" },
                  description: "Keywords to match",
                },
                domain: {
                  type: "string",
                  description: "Domain to match",
                },
                file_path: {
                  type: "string",
                  description: "File path to match against patterns",
                },
              },
            },
          },
          {
            name: "execute_agent_script",
            description: "Execute a bundled agent script",
            inputSchema: {
              type: "object",
              properties: {
                agent_name: {
                  type: "string",
                  description: "Name of the agent",
                },
                script_name: {
                  type: "string",
                  description: "Name of the script to execute",
                },
                parameters: {
                  type: "object",
                  description: "Script parameters",
                },
              },
              required: ["agent_name", "script_name"],
            },
          },
          {
            name: "get_agent_recommendations",
            description: "Get recommended agents for a task (ML-powered in Phase 6)",
            inputSchema: {
              type: "object",
              properties: {
                task_description: {
                  type: "string",
                  description: "Description of the task",
                },
                context: {
                  type: "object",
                  description: "Additional context (language, framework, etc.)",
                },
              },
              required: ["task_description"],
            },
          },
        ],
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      switch (name) {
        case "find_agents":
          return await this.findAgents(args as any);

        case "execute_agent_script":
          return await this.executeScript(args as any);

        case "get_agent_recommendations":
          return await this.getRecommendations(args as any);

        default:
          throw new Error(`Unknown tool: ${name}`);
      }
    });
  }

  private async loadMetadata(): Promise<void> {
    if (this.metadataCache.size > 0) return;

    const entries = await fs.readdir(this.agentsDir, { withFileTypes: true });

    for (const entry of entries) {
      if (entry.name.startsWith(".") || entry.name.startsWith("_")) continue;
      if (["pending_review", "rejected", "README.md"].includes(entry.name)) continue;

      try {
        const metadata = await this.loadAgentMetadata(entry.name);
        if (metadata) {
          this.metadataCache.set(metadata.name, metadata);
        }
      } catch (error) {
        console.error(`Failed to load metadata for ${entry.name}:`, error);
      }
    }
  }

  private async loadAgentMetadata(agentName: string): Promise<AgentMetadata | null> {
    const agentPath = path.join(this.agentsDir, agentName);
    const stat = await fs.stat(agentPath);

    if (stat.isDirectory()) {
      // Multi-file format
      const metadataFile = path.join(agentPath, "metadata.yaml");
      try {
        const content = await fs.readFile(metadataFile, "utf-8");
        // Simple YAML parsing for metadata (production would use proper YAML parser)
        return this.parseSimpleYaml(content);
      } catch {
        return null;
      }
    } else if (agentName.endsWith(".md")) {
      // Single-file format - extract from frontmatter
      const content = await fs.readFile(agentPath, "utf-8");
      return this.extractFrontmatterMetadata(content, agentName.replace(".md", ""));
    }

    return null;
  }

  private parseSimpleYaml(content: string): AgentMetadata {
    // Simplified YAML parsing - production would use yaml library
    const lines = content.split("\n");
    const data: any = {};

    for (const line of lines) {
      const match = line.match(/^(\w+):\s*(.+)$/);
      if (match) {
        const [, key, value] = match;
        try {
          data[key] = JSON.parse(value.replace(/'/g, '"'));
        } catch {
          data[key] = value.trim();
        }
      }
    }

    return data as AgentMetadata;
  }

  private extractFrontmatterMetadata(content: string, name: string): AgentMetadata | null {
    if (!content.startsWith("---")) return null;

    const parts = content.split("---");
    if (parts.length < 3) return null;

    try {
      const frontmatter = this.parseSimpleYaml(parts[1]);
      return {
        name: frontmatter.name || name,
        version: "1.0.0",
        description: frontmatter.description || "",
        triggers: {
          keywords: [],
          file_patterns: [],
          domains: [name.split("-")[0]],
        },
        category: "special-purpose",
        priority: frontmatter.priority || "medium",
        capabilities: [],
      };
    } catch {
      return null;
    }
  }

  private async getAgentDefinition(agentName: string): Promise<string> {
    const multiFilePath = path.join(this.agentsDir, agentName, "agent.md");
    const singleFilePath = path.join(this.agentsDir, `${agentName}.md`);

    try {
      return await fs.readFile(multiFilePath, "utf-8");
    } catch {
      try {
        return await fs.readFile(singleFilePath, "utf-8");
      } catch {
        throw new Error(`Agent definition not found: ${agentName}`);
      }
    }
  }

  private async getAgentScripts(agentName: string): Promise<string> {
    const metadata = this.metadataCache.get(agentName);
    if (!metadata || !metadata.scripts) {
      return JSON.stringify([]);
    }

    const scriptsDir = path.join(this.agentsDir, agentName, "scripts");

    try {
      const scriptFiles = await fs.readdir(scriptsDir);
      const scripts = scriptFiles.map((file) => ({
        name: file.replace(/\.[^.]+$/, ""),
        path: path.join(scriptsDir, file),
      }));

      return JSON.stringify(scripts, null, 2);
    } catch {
      return JSON.stringify([]);
    }
  }

  private async findAgents(args: {
    keywords?: string[];
    domain?: string;
    file_path?: string;
  }): Promise<{ content: Array<{ type: string; text: string }> }> {
    await this.loadMetadata();

    let matches: AgentMetadata[] = Array.from(this.metadataCache.values());

    if (args.keywords) {
      matches = matches.filter((agent) =>
        args.keywords!.some((kw) => agent.triggers.keywords.some((trigger) => trigger.toLowerCase().includes(kw.toLowerCase())))
      );
    }

    if (args.domain) {
      matches = matches.filter((agent) =>
        agent.triggers.domains.some((d) => d.toLowerCase() === args.domain!.toLowerCase())
      );
    }

    if (args.file_path) {
      matches = matches.filter((agent) =>
        agent.triggers.file_patterns.some((pattern) => {
          const regex = new RegExp(pattern.replace(/\*/g, ".*"));
          return regex.test(args.file_path!);
        })
      );
    }

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(matches, null, 2),
        },
      ],
    };
  }

  private async executeScript(args: {
    agent_name: string;
    script_name: string;
    parameters?: Record<string, any>;
  }): Promise<{ content: Array<{ type: string; text: string }> }> {
    const scriptPath = path.join(this.agentsDir, args.agent_name, "scripts", `${args.script_name}.py`);

    try {
      await fs.access(scriptPath);
    } catch {
      return {
        content: [
          {
            type: "text",
            text: `Script not found: ${args.script_name}`,
          },
        ],
      };
    }

    return new Promise((resolve) => {
      const python = spawn("python3", [scriptPath]);

      let stdout = "";
      let stderr = "";

      python.stdout.on("data", (data) => {
        stdout += data.toString();
      });

      python.stderr.on("data", (data) => {
        stderr += data.toString();
      });

      python.on("close", (code) => {
        resolve({
          content: [
            {
              type: "text",
              text: JSON.stringify(
                {
                  success: code === 0,
                  stdout,
                  stderr,
                  returncode: code,
                },
                null,
                2
              ),
            },
          ],
        });
      });
    });
  }

  private async getRecommendations(args: {
    task_description: string;
    context?: Record<string, any>;
  }): Promise<{ content: Array<{ type: string; text: string }> }> {
    await this.loadMetadata();

    // Simple keyword-based recommendations (Phase 6 will use ML)
    const taskLower = args.task_description.toLowerCase();
    const matches: Array<{ agent: string; score: number }> = [];

    for (const [name, metadata] of this.metadataCache.entries()) {
      let score = 0;

      // Match keywords
      for (const keyword of metadata.triggers.keywords) {
        if (taskLower.includes(keyword.toLowerCase())) {
          score += 10;
        }
      }

      // Match capabilities
      for (const capability of metadata.capabilities) {
        if (taskLower.includes(capability.toLowerCase().replace(/_/g, " "))) {
          score += 5;
        }
      }

      if (score > 0) {
        matches.push({ agent: name, score });
      }
    }

    matches.sort((a, b) => b.score - a.score);

    const recommendations = matches.slice(0, 5).map((m) => ({
      agent: m.agent,
      confidence: Math.min(m.score / 20, 1.0),
      metadata: this.metadataCache.get(m.agent),
    }));

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(recommendations, null, 2),
        },
      ],
    };
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error("OaK Agents MCP Server running on stdio");
  }
}

const server = new OakAgentsServer();
server.run().catch(console.error);
