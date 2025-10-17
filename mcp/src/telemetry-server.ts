#!/usr/bin/env node

/**
 * OaK Telemetry MCP Server
 *
 * Provides standardized access to OaK agent telemetry data via Model Context Protocol.
 * Replaces custom hooks with MCP-based telemetry collection.
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
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

interface TelemetryConfig {
  telemetryDir: string;
  enabled: boolean;
}

interface AgentInvocation {
  timestamp: string;
  agent_name: string;
  task_description: string;
  state_features: Record<string, any>;
  duration_seconds?: number;
  outcome?: string;
  quality_score?: number;
  invocation_id: string;
}

class OakTelemetryServer {
  private server: Server;
  private config: TelemetryConfig;

  constructor() {
    this.config = {
      telemetryDir: process.env.OAK_TELEMETRY_DIR || path.join(process.env.HOME!, "Projects/claude-oak-agents/telemetry"),
      enabled: process.env.OAK_TELEMETRY_ENABLED !== "false",
    };

    this.server = new Server(
      {
        name: "oak-telemetry",
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
      return {
        resources: [
          {
            uri: "oak://telemetry/invocations",
            name: "Agent Invocations",
            description: "Recent agent invocation logs",
            mimeType: "application/json",
          },
          {
            uri: "oak://telemetry/metrics",
            name: "Performance Metrics",
            description: "Aggregated agent performance metrics",
            mimeType: "application/json",
          },
          {
            uri: "oak://telemetry/gaps",
            name: "Capability Gaps",
            description: "Detected capability gaps and routing failures",
            mimeType: "application/json",
          },
          {
            uri: "oak://telemetry/summary",
            name: "Telemetry Summary",
            description: "High-level telemetry summary",
            mimeType: "text/plain",
          },
        ],
      };
    });

    // Read resource content
    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      const uri = request.params.uri;

      if (!uri.startsWith("oak://telemetry/")) {
        throw new Error(`Unknown resource: ${uri}`);
      }

      const resourceType = uri.replace("oak://telemetry/", "");

      switch (resourceType) {
        case "invocations":
          return {
            contents: [
              {
                uri,
                mimeType: "application/json",
                text: await this.getInvocations(),
              },
            ],
          };

        case "metrics":
          return {
            contents: [
              {
                uri,
                mimeType: "application/json",
                text: await this.getMetrics(),
              },
            ],
          };

        case "gaps":
          return {
            contents: [
              {
                uri,
                mimeType: "application/json",
                text: await this.getCapabilityGaps(),
              },
            ],
          };

        case "summary":
          return {
            contents: [
              {
                uri,
                mimeType: "text/plain",
                text: await this.getSummary(),
              },
            ],
          };

        default:
          throw new Error(`Unknown resource type: ${resourceType}`);
      }
    });

    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: "log_agent_invocation",
            description: "Log an agent invocation with telemetry data",
            inputSchema: {
              type: "object",
              properties: {
                agent_name: {
                  type: "string",
                  description: "Name of the agent being invoked",
                },
                task_description: {
                  type: "string",
                  description: "Description of the task",
                },
                state_features: {
                  type: "object",
                  description: "Extracted state features",
                },
              },
              required: ["agent_name", "task_description"],
            },
          },
          {
            name: "update_invocation",
            description: "Update invocation with completion data",
            inputSchema: {
              type: "object",
              properties: {
                invocation_id: {
                  type: "string",
                  description: "Invocation ID to update",
                },
                duration_seconds: {
                  type: "number",
                  description: "Duration in seconds",
                },
                outcome: {
                  type: "string",
                  description: "Outcome (success/failure/partial)",
                },
                quality_score: {
                  type: "number",
                  description: "Quality score (1-5)",
                },
              },
              required: ["invocation_id"],
            },
          },
          {
            name: "query_telemetry",
            description: "Query telemetry data with filters",
            inputSchema: {
              type: "object",
              properties: {
                agent_name: {
                  type: "string",
                  description: "Filter by agent name",
                },
                start_date: {
                  type: "string",
                  description: "Start date (ISO format)",
                },
                end_date: {
                  type: "string",
                  description: "End date (ISO format)",
                },
                limit: {
                  type: "number",
                  description: "Maximum results to return",
                },
              },
            },
          },
        ],
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      switch (name) {
        case "log_agent_invocation":
          return await this.logInvocation(args as any);

        case "update_invocation":
          return await this.updateInvocation(args as any);

        case "query_telemetry":
          return await this.queryTelemetry(args as any);

        default:
          throw new Error(`Unknown tool: ${name}`);
      }
    });
  }

  private async logInvocation(args: {
    agent_name: string;
    task_description: string;
    state_features?: Record<string, any>;
  }): Promise<{ content: Array<{ type: string; text: string }> }> {
    if (!this.config.enabled) {
      return {
        content: [
          {
            type: "text",
            text: "Telemetry disabled",
          },
        ],
      };
    }

    const invocation: AgentInvocation = {
      timestamp: new Date().toISOString(),
      agent_name: args.agent_name,
      task_description: args.task_description,
      state_features: args.state_features || {},
      invocation_id: this.generateInvocationId(),
    };

    const invocationsFile = path.join(this.config.telemetryDir, "agent_invocations.jsonl");

    try {
      await fs.appendFile(invocationsFile, JSON.stringify(invocation) + "\n");

      return {
        content: [
          {
            type: "text",
            text: `Logged invocation: ${invocation.invocation_id}`,
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error logging invocation: ${error}`,
          },
        ],
      };
    }
  }

  private async updateInvocation(args: {
    invocation_id: string;
    duration_seconds?: number;
    outcome?: string;
    quality_score?: number;
  }): Promise<{ content: Array<{ type: string; text: string }> }> {
    if (!this.config.enabled) {
      return {
        content: [
          {
            type: "text",
            text: "Telemetry disabled",
          },
        ],
      };
    }

    const successFile = path.join(this.config.telemetryDir, "success_metrics.jsonl");

    const metrics = {
      timestamp: new Date().toISOString(),
      invocation_id: args.invocation_id,
      duration_seconds: args.duration_seconds,
      outcome: args.outcome,
      quality_score: args.quality_score,
    };

    try {
      await fs.appendFile(successFile, JSON.stringify(metrics) + "\n");

      return {
        content: [
          {
            type: "text",
            text: `Updated invocation: ${args.invocation_id}`,
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error updating invocation: ${error}`,
          },
        ],
      };
    }
  }

  private async queryTelemetry(args: {
    agent_name?: string;
    start_date?: string;
    end_date?: string;
    limit?: number;
  }): Promise<{ content: Array<{ type: string; text: string }> }> {
    const invocationsFile = path.join(this.config.telemetryDir, "agent_invocations.jsonl");

    try {
      const content = await fs.readFile(invocationsFile, "utf-8");
      const lines = content.trim().split("\n");

      let invocations = lines
        .filter((line) => line.trim())
        .map((line) => JSON.parse(line) as AgentInvocation);

      // Apply filters
      if (args.agent_name) {
        invocations = invocations.filter((inv) => inv.agent_name === args.agent_name);
      }

      if (args.start_date) {
        invocations = invocations.filter((inv) => inv.timestamp >= args.start_date!);
      }

      if (args.end_date) {
        invocations = invocations.filter((inv) => inv.timestamp <= args.end_date!);
      }

      // Apply limit
      if (args.limit) {
        invocations = invocations.slice(-args.limit);
      }

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(invocations, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error querying telemetry: ${error}`,
          },
        ],
      };
    }
  }

  private async getInvocations(): Promise<string> {
    const invocationsFile = path.join(this.config.telemetryDir, "agent_invocations.jsonl");

    try {
      const content = await fs.readFile(invocationsFile, "utf-8");
      const lines = content.trim().split("\n").filter((line) => line.trim());

      // Return last 100 invocations
      const recent = lines.slice(-100).map((line) => JSON.parse(line));

      return JSON.stringify(recent, null, 2);
    } catch (error) {
      return JSON.stringify({ error: String(error) });
    }
  }

  private async getMetrics(): Promise<string> {
    const invocationsFile = path.join(this.config.telemetryDir, "agent_invocations.jsonl");

    try {
      const content = await fs.readFile(invocationsFile, "utf-8");
      const lines = content.trim().split("\n").filter((line) => line.trim());

      const invocations = lines.map((line) => JSON.parse(line) as AgentInvocation);

      // Calculate metrics by agent
      const metricsByAgent: Record<string, any> = {};

      for (const inv of invocations) {
        if (!metricsByAgent[inv.agent_name]) {
          metricsByAgent[inv.agent_name] = {
            total_invocations: 0,
            avg_duration: 0,
            success_rate: 0,
            quality_scores: [],
          };
        }

        metricsByAgent[inv.agent_name].total_invocations++;

        if (inv.duration_seconds) {
          metricsByAgent[inv.agent_name].avg_duration += inv.duration_seconds;
        }

        if (inv.quality_score) {
          metricsByAgent[inv.agent_name].quality_scores.push(inv.quality_score);
        }
      }

      // Calculate averages
      for (const agent in metricsByAgent) {
        const metrics = metricsByAgent[agent];
        metrics.avg_duration /= metrics.total_invocations;

        if (metrics.quality_scores.length > 0) {
          metrics.avg_quality_score =
            metrics.quality_scores.reduce((a: number, b: number) => a + b, 0) / metrics.quality_scores.length;
          delete metrics.quality_scores;
        }
      }

      return JSON.stringify(metricsByAgent, null, 2);
    } catch (error) {
      return JSON.stringify({ error: String(error) });
    }
  }

  private async getCapabilityGaps(): Promise<string> {
    const gapsFile = path.join(this.config.telemetryDir, "routing_failures.jsonl");

    try {
      const content = await fs.readFile(gapsFile, "utf-8");
      const lines = content.trim().split("\n").filter((line) => line.trim());

      const gaps = lines.map((line) => JSON.parse(line));

      return JSON.stringify(gaps, null, 2);
    } catch (error) {
      return JSON.stringify({ error: String(error), gaps: [] });
    }
  }

  private async getSummary(): Promise<string> {
    const invocations = JSON.parse(await this.getInvocations());
    const metrics = JSON.parse(await this.getMetrics());

    let summary = "# OaK Telemetry Summary\n\n";
    summary += `Total Invocations: ${invocations.length}\n\n`;
    summary += "## Metrics by Agent\n\n";

    for (const [agent, agentMetrics] of Object.entries(metrics)) {
      const m = agentMetrics as any;
      summary += `### ${agent}\n`;
      summary += `- Invocations: ${m.total_invocations}\n`;
      summary += `- Avg Duration: ${m.avg_duration?.toFixed(2)}s\n`;
      if (m.avg_quality_score) {
        summary += `- Avg Quality: ${m.avg_quality_score.toFixed(2)}/5\n`;
      }
      summary += "\n";
    }

    return summary;
  }

  private generateInvocationId(): string {
    return `inv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error("OaK Telemetry MCP Server running on stdio");
  }
}

const server = new OakTelemetryServer();
server.run().catch(console.error);
