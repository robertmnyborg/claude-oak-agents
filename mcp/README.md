# OaK MCP Servers

Model Context Protocol (MCP) servers for OaK Agents, providing standardized access to telemetry data and agent coordination.

## Overview

OaK provides two MCP servers:

1. **oak-telemetry** - Telemetry data access and logging
2. **oak-agents** - Agent discovery, metadata, and script execution

## Installation

```bash
cd mcp
npm install
npm run build
```

## Configuration

Add to `~/.config/claude/mcp_servers.json`:

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
    }
  }
}
```

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

## Resources

- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [Anthropic MCP Documentation](https://docs.anthropic.com/mcp)
- [OaK Multi-File Agents](../docs/MULTI_FILE_AGENTS.md)
- [OaK Migration Guide](../docs/MIGRATION_GUIDE.md)
