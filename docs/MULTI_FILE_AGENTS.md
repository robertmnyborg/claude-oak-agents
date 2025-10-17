# Multi-File Agent Packages

## Overview

OaK Agents now support both single-file and multi-file package formats, bringing parity with Anthropic's Agent Skills while maintaining OaK's superior telemetry and learning capabilities.

## Architecture

### Single-File Agents (Legacy, Still Supported)

```
agents/
  frontend-developer.md
  backend-architect.md
  security-auditor.md
```

### Multi-File Agent Packages (New)

```
agents/
  security-auditor/
    agent.md              # Main agent definition (required)
    metadata.yaml         # Agent metadata for discovery (required)
    scripts/              # Bundled executable scripts (optional)
      dependency_scan.py
      sast_analyzer.py
      threat_model.py
    reference/            # Reference documentation (optional)
      owasp_top_10.md
      compliance_checklists.md
      cwe_mappings.yaml
    templates/            # Code templates (optional)
      security_test.py.template
      threat_model.yaml.template
    README.md             # Package documentation (optional)
```

## Agent Metadata Format

### metadata.yaml Structure

```yaml
# Agent Identity
name: security-auditor
version: 2.0.0
description: Comprehensive security analysis specialist that identifies vulnerabilities, security anti-patterns, and potential attack vectors across all languages and frameworks.

# Discovery Metadata (loaded at startup)
triggers:
  keywords: [security, vulnerability, audit, compliance, penetration, threat]
  file_patterns: ['*.security', 'security.yml', 'SECURITY.md']
  domains: [security, compliance, penetration-testing]

# Agent Classification
category: quality-security
priority: high
blocking: true  # Can block commits on critical issues
parallel_compatible: [code-reviewer, dependency-scanner]

# Capabilities
capabilities:
  - vulnerability_detection
  - compliance_validation
  - penetration_testing
  - threat_modeling
  - sast_analysis

# Tool Requirements
tools: [Write, Edit, MultiEdit, Read, Bash, Grep, Glob]
model: sonnet

# Bundled Scripts (optional)
scripts:
  - name: dependency_scan
    runtime: python
    entrypoint: scripts/dependency_scan.py
    description: Fast dependency vulnerability scanner using CVE database
    required_packages: [requests, semver]

  - name: sast_analyzer
    runtime: python
    entrypoint: scripts/sast_analyzer.py
    description: Static application security testing analyzer
    required_packages: [tree-sitter, regex]

# Performance Metrics (populated by telemetry)
metrics:
  avg_duration_seconds: 45.2
  success_rate: 0.94
  quality_score: 4.6
  invocation_count: 127
  last_updated: "2025-10-16T10:30:00Z"

# Integration
coordination_patterns:
  - "Runs in parallel with code-reviewer for comprehensive quality gates"
  - "Coordinates with dependency-scanner for supply chain analysis"
  - "Provides security context to infrastructure-specialist"

# Auto-created flag (for agent-creator tracking)
auto_created: false
created_by: human
created_at: "2025-01-15T09:00:00Z"
```

## Bundled Script Specification

### Script Manifest in metadata.yaml

```yaml
scripts:
  - name: dependency_scan
    runtime: python  # python, bash, node, go
    entrypoint: scripts/dependency_scan.py
    description: Fast CVE scanning for dependencies

    # Optional: Runtime requirements
    required_packages:
      - requests>=2.28.0
      - semver>=2.13.0
    python_version: ">=3.8"

    # Optional: Script parameters
    parameters:
      - name: scan_depth
        type: string
        default: "deep"
        options: [shallow, medium, deep]
      - name: severity_threshold
        type: string
        default: "medium"
        options: [low, medium, high, critical]

    # Optional: Expected outputs
    outputs:
      - type: json
        schema: cve_report_v1
      - type: markdown
        description: Human-readable security report
```

### Script Execution from Agent

Agents can invoke bundled scripts using a special syntax in their instructions:

```markdown
## Vulnerability Scanning Process

1. **Dependency Analysis**: Run bundled dependency scanner
   ```bash
   {{script:dependency_scan --depth=deep --format=json}}
   ```

2. **Parse Results**: Process scanner output
   ```python
   # Script output available in $SCRIPT_OUTPUT
   vulnerabilities = json.loads(os.environ['SCRIPT_OUTPUT'])
   ```

3. **Generate Report**: Create actionable security report
```

## Dynamic Agent Discovery

### Metadata-Only System Prompt

Instead of loading full agent definitions into the system prompt, only metadata is preloaded:

```python
# OLD: Full agent definitions in system prompt (heavy)
system_prompt = f"""
Available agents:
{read_all_agent_files()}  # 50KB+ of agent definitions
"""

# NEW: Metadata-only in system prompt (lightweight)
system_prompt = f"""
Available agents metadata:
{load_agent_metadata()}  # 5KB of metadata only

Agent details loaded on-demand when invoked.
"""
```

### Agent Discovery Flow

```
1. User Request
   ↓
2. Main LLM Classification (using metadata only)
   - Keywords: "security", "vulnerability"
   - Matches: security-auditor.triggers.keywords
   ↓
3. Agent Selection Decision
   - Selected: security-auditor
   ↓
4. Load Full Agent Definition (on-demand)
   - Read agents/security-auditor/agent.md
   - Load bundled scripts if needed
   ↓
5. Execute Agent
```

### Benefits

- **Reduced System Prompt Size**: 90% reduction (50KB → 5KB)
- **Faster Classification**: Less context to process
- **Scalability**: Support 100+ agents without prompt bloat
- **Lazy Loading**: Full definitions loaded only when needed

## Model Context Protocol (MCP) Integration

### MCP Telemetry Server

OaK now supports MCP for standardized telemetry and agent coordination:

```typescript
// mcp/telemetry-server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

export class OakTelemetryServer {
  private server: Server;

  constructor() {
    this.server = new Server({
      name: "oak-telemetry",
      version: "1.0.0",
    }, {
      capabilities: {
        resources: {},
        tools: {},
        prompts: {},
      }
    });

    this.setupTools();
    this.setupResources();
  }

  private setupTools() {
    // Tool: Log agent invocation
    this.server.setRequestHandler("tools/call", async (request) => {
      if (request.params.name === "log_agent_invocation") {
        return await this.logInvocation(request.params.arguments);
      }
      // ... other tools
    });
  }

  private setupResources() {
    // Resource: Read telemetry data
    this.server.setRequestHandler("resources/read", async (request) => {
      if (request.params.uri.startsWith("oak://telemetry/")) {
        return await this.readTelemetry(request.params.uri);
      }
    });
  }
}
```

### MCP Configuration

```json
// ~/.config/claude/mcp_servers.json
{
  "mcpServers": {
    "oak-telemetry": {
      "command": "node",
      "args": [
        "/Users/robertnyborg/Projects/claude-oak-agents/mcp/dist/index.js"
      ],
      "env": {
        "OAK_TELEMETRY_DIR": "/Users/robertnyborg/Projects/claude-oak-agents/telemetry"
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

### MCP Resources

OaK exposes agent data via MCP resources:

```
oak://agents/metadata              # All agent metadata
oak://agents/{name}/definition     # Full agent definition
oak://agents/{name}/scripts        # Available scripts
oak://telemetry/invocations        # Recent invocations
oak://telemetry/metrics            # Performance metrics
oak://telemetry/gaps               # Capability gaps
```

### MCP Tools

OaK provides MCP tools for agent operations:

```typescript
// Available MCP tools
{
  "log_agent_invocation": {
    "description": "Log agent invocation with telemetry",
    "inputSchema": {
      "type": "object",
      "properties": {
        "agent_name": { "type": "string" },
        "task_description": { "type": "string" },
        "state_features": { "type": "object" }
      }
    }
  },

  "execute_agent_script": {
    "description": "Execute bundled agent script",
    "inputSchema": {
      "type": "object",
      "properties": {
        "agent_name": { "type": "string" },
        "script_name": { "type": "string" },
        "parameters": { "type": "object" }
      }
    }
  },

  "get_agent_recommendations": {
    "description": "Get ML-recommended agents for task",
    "inputSchema": {
      "type": "object",
      "properties": {
        "task_description": { "type": "string" },
        "context": { "type": "object" }
      }
    }
  }
}
```

## Migration Guide

### Converting Single-File to Multi-File

1. **Create agent directory**:
   ```bash
   mkdir -p agents/security-auditor
   mv agents/security-auditor.md agents/security-auditor/agent.md
   ```

2. **Extract metadata**:
   ```bash
   ./scripts/extract_agent_metadata.py agents/security-auditor/agent.md \
     > agents/security-auditor/metadata.yaml
   ```

3. **Add bundled scripts** (optional):
   ```bash
   mkdir -p agents/security-auditor/scripts
   # Add your scripts here
   ```

4. **Update metadata.yaml** with script definitions

### Backward Compatibility

The agent loader automatically detects format:

```python
def load_agent(agent_path: Path) -> Agent:
    """Load agent from single-file or multi-file format"""

    if agent_path.is_file():
        # Single-file format (legacy)
        return load_single_file_agent(agent_path)

    elif agent_path.is_dir():
        # Multi-file format (new)
        metadata = load_yaml(agent_path / "metadata.yaml")
        definition = load_markdown(agent_path / "agent.md")
        scripts = load_scripts(agent_path / "scripts")

        return Agent(
            metadata=metadata,
            definition=definition,
            scripts=scripts
        )

    else:
        raise ValueError(f"Invalid agent path: {agent_path}")
```

## Best Practices

### When to Use Multi-File Format

✅ **Use multi-file when**:
- Agent needs bundled executable scripts
- Extensive reference documentation required
- Code templates are part of agent's value
- Multiple script utilities needed
- Agent is complex (>500 lines)

❌ **Use single-file when**:
- Simple, instruction-only agent
- No bundled scripts needed
- Agent is <200 lines
- Minimal reference materials

### Script Design Guidelines

1. **Efficiency**: Scripts should be faster than token generation
2. **Reliability**: Pre-tested, deterministic utilities
3. **Reusability**: Generic scripts usable across contexts
4. **Documentation**: Clear parameter descriptions
5. **Error Handling**: Robust error handling and reporting

### Metadata Completeness

Ensure metadata includes:
- ✅ Clear, specific triggers (keywords + file patterns)
- ✅ Accurate capability list
- ✅ Coordination patterns with other agents
- ✅ Script specifications if bundled
- ✅ Version tracking

## Performance Impact

### Metadata Loading (Startup)

```
Single-file (legacy):  Load 29 agents × ~30KB = ~870KB
Multi-file (new):      Load 29 metadata × ~2KB = ~58KB

Reduction: 93% smaller system prompt
```

### Agent Execution

```
Single-file:  Read agent file → Execute
Multi-file:   Read agent.md → Load scripts → Execute

Overhead: ~50ms for script loading (one-time per invocation)
Benefit: Scripts execute 10-100x faster than token generation
```

### Script Execution Examples

```python
# Token generation approach (expensive)
# Sorting 10,000 items: ~5 seconds, 50K tokens

# Script execution approach (efficient)
# Sorting 10,000 items: ~0.05 seconds, 0 tokens

# 100x faster, 0 token cost
```

## Examples

See the following reference implementations:

- [agents/security-auditor/](../agents/security-auditor/) - Multi-file with bundled SAST scripts
- [agents/performance-optimizer/](../agents/performance-optimizer/) - Multi-file with profiling scripts
- [agents/frontend-developer.md](../agents/frontend-developer.md) - Single-file (still valid)

## Implementation Status

- ✅ Multi-file agent package structure
- ✅ Metadata extraction and loading
- ✅ Dynamic agent discovery (metadata-only prompt)
- ✅ Bundled script specification
- ✅ Script execution framework
- ✅ MCP telemetry server
- ✅ MCP agent server
- ✅ Backward compatibility
- ✅ Migration tooling

## Future Enhancements

- [ ] Agent package registry (npm-like for agents)
- [ ] Script dependency management (auto-install packages)
- [ ] Hot-reloading of agent updates
- [ ] Agent versioning and rollback
- [ ] Multi-language script support (Go, Rust, etc.)
