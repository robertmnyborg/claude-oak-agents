# Oak Discovery Tools

Three interactive CLI tools for exploring and analyzing the claude-oak-agents system.

## Tools Overview

### 1. oak-discover - Agent & Workflow Browser

Interactive tool for browsing agents, searching capabilities, and exploring workflow patterns.

**Features:**
- List all agents by category (Development, Quality, Security, Infrastructure, etc.)
- Search agents by keyword or capability
- Show detailed agent information (description, tools, model tier)
- Preview agent prompts
- Display common workflow patterns
- Interactive menu navigation

**Usage:**

```bash
# Interactive menu mode (default)
./scripts/oak-discover

# List all agents by category
./scripts/oak-discover --list

# List agents with detailed information
./scripts/oak-discover --list --details

# Search for agents
./scripts/oak-discover --search "backend"
./scripts/oak-discover --search "security"
./scripts/oak-discover --search "API"

# Show specific agent details
./scripts/oak-discover --show backend-architect
./scripts/oak-discover --show security-auditor

# Show workflow patterns
./scripts/oak-discover --workflows
```

**Example Output:**

```
================================================================================
Oak Agents Portfolio (21 agents)
================================================================================

Development:
  backend-architect [balanced]
    Backend architecture specialist responsible for database design...

  frontend-developer [balanced]
    Frontend development specialist responsible for UI/UX implementation...

Quality & Testing:
  quality-gate [balanced]
    Unified code review, maintainability analysis, and validation...

  unit-test-expert [fast]
    Comprehensive unit test creation and coverage validation...
```

---

### 2. oak-insights - Telemetry Analytics Dashboard

Analytics dashboard showing agent usage patterns, performance metrics, and recommendations.

**Features:**
- Most-used agents with success rates
- Most-used workflows
- Average task duration by agent
- Recent invocations (last N)
- Performance trend analysis
- Automated recommendations based on patterns

**Usage:**

```bash
# Full dashboard (default)
./scripts/oak-insights

# Show specific sections
./scripts/oak-insights --agents           # Agent leaderboard only
./scripts/oak-insights --workflows        # Workflow summary only
./scripts/oak-insights --recent           # Recent activity only
./scripts/oak-insights --performance      # Performance analysis only
./scripts/oak-insights --recommendations  # Recommendations only

# Control number of items displayed
./scripts/oak-insights --limit 20         # Show top 20 instead of 10
./scripts/oak-insights --agents -n 5      # Show top 5 agents
```

**Example Output:**

```
================================================================================
Most-Used Agents (Top 10)
================================================================================

Rank  Agent                          Invocations     Success Rate    Avg Duration
--------------------------------------------------------------------------------
1     design-simplicity-advisor      3               100.0%               8.7s
2     backend-architect              3               100.0%              48.7s
3     unit-test-expert               3               100.0%              17.0s

================================================================================
Recommendations
================================================================================

💡  Agent 'security-auditor' has high average duration (142.8s). Investigate performance bottlenecks.
⚠️  Agent 'frontend-developer' has 5.0% failure rate. Review error patterns.
```

---

### 3. oak-history - Session Analytics & Command Reference

Command history and session analytics tool with workflow grouping and filtering.

**Features:**
- Show recent agent invocations
- Group invocations by workflow
- Show task sequences with parent/child relationships
- Duration and success rate tracking
- Filter by agent, date, or workflow
- Agent sequence visualization
- Summary statistics

**Usage:**

```bash
# Show all recent invocations
./scripts/oak-history

# Filter by agent
./scripts/oak-history --agent backend-architect
./scripts/oak-history -a security-auditor

# Filter by workflow
./scripts/oak-history --workflow wf-20251022-abc123
./scripts/oak-history -w wf-test-20251029-001

# Filter by date
./scripts/oak-history --date 2025-10-22
./scripts/oak-history --last-days 7

# Control output
./scripts/oak-history --limit 20          # Show last 20 invocations
./scripts/oak-history --full              # Show full details (files modified)
./scripts/oak-history --sequence          # Show agent sequence visualization
./scripts/oak-history --stats             # Show summary statistics only

# Combine filters
./scripts/oak-history --agent backend-architect --last-days 7 --stats
./scripts/oak-history --workflow wf-test-20251029-001 --full
```

**Example Output:**

```
================================================================================
Workflow Invocations
================================================================================

Workflow: wf-test-20251029-001
  Steps: 4 | Total Duration: 275.0s | Success Rate: 100.0%

  1.   2025-10-30 00:37:39 | design-simplicity-advisor | success    |   25.0s
    Task: Review API design for simplicity
  2.   2025-10-30 00:38:09 | backend-architect         | success    |  145.0s
    Task: Implement REST API endpoints
  3.   2025-10-30 00:40:39 | security-auditor          | success    |   55.0s
    Task: Security review of API implementation
  4.   2025-10-30 00:41:39 | unit-test-expert          | success    |   50.0s
    Task: Create unit tests for API

================================================================================
Summary Statistics
================================================================================

  Total Invocations: 4
  Success: 4 | Failure: 0
  Success Rate: 100.0%
  Total Duration: 275.0s | Average: 68.8s
  Unique Agents: 4
  Unique Workflows: 1
```

---

## Common Use Cases

### Exploring the Agent System

```bash
# What agents are available?
./scripts/oak-discover --list

# What can the backend-architect do?
./scripts/oak-discover --show backend-architect

# Find all agents related to security
./scripts/oak-discover --search security
```

### Analyzing Performance

```bash
# Which agents are used most?
./scripts/oak-insights --agents

# Which workflows are common?
./scripts/oak-insights --workflows

# What's slowing us down?
./scripts/oak-insights --performance
```

### Reviewing History

```bash
# What happened today?
./scripts/oak-history --date 2025-10-30

# What did backend-architect do this week?
./scripts/oak-history --agent backend-architect --last-days 7

# Show me a specific workflow
./scripts/oak-history --workflow wf-test-20251029-001 --full
```

### Debugging and Troubleshooting

```bash
# Find agents with failures
./scripts/oak-insights --performance

# Check specific agent success rate
./scripts/oak-history --agent debug-specialist --stats

# See what went wrong in a workflow
./scripts/oak-history --workflow wf-20251022-abc123 --full
```

---

## Configuration

All tools support custom paths via command-line arguments:

```bash
# Custom agents directory
./scripts/oak-discover --agents-dir /path/to/agents

# Custom telemetry file
./scripts/oak-insights --telemetry-file /path/to/agent_invocations.jsonl
./scripts/oak-history --telemetry-file /path/to/agent_invocations.jsonl
```

**Default paths:**
- Agents: `/Users/robertnyborg/Projects/claude-oak-agents/agents`
- Telemetry: `/Users/robertnyborg/Projects/claude-oak-agents/telemetry/agent_invocations.jsonl`

---

## Color Coding

All tools use color coding for better readability:

**Status Colors:**
- 🟢 Green: Success, high performance
- 🟡 Yellow: Warning, moderate performance
- 🔴 Red: Failure, low performance

**Model Tiers:**
- 🟢 Green: Fast tier (Haiku)
- 🟡 Yellow: Balanced tier (Sonnet)
- 🔴 Red: Premium tier (Opus)

**Element Colors:**
- 🔵 Blue: Headings, titles
- 🔷 Cyan: Agent names, workflow IDs
- 🟨 Yellow: Metadata, timestamps

---

## Data Sources

**oak-discover** reads from:
- Agent markdown files in `agents/` directory
- Parses YAML frontmatter for metadata

**oak-insights** reads from:
- `telemetry/agent_invocations.jsonl` (JSONL format)

**oak-history** reads from:
- `telemetry/agent_invocations.jsonl` (JSONL format)

---

## Requirements

- Python 3.7+
- Standard library only (no external dependencies)
- Terminal with ANSI color support

---

## Installation

Scripts are already executable. If needed:

```bash
chmod +x scripts/oak-discover
chmod +x scripts/oak-insights
chmod +x scripts/oak-history
```

---

## Tips and Tricks

**Quick Reference:**

```bash
# Morning standup: What happened yesterday?
./scripts/oak-history --last-days 1

# Weekly review: Performance and recommendations
./scripts/oak-insights

# New team member: Browse all capabilities
./scripts/oak-discover

# Planning: What workflow patterns exist?
./scripts/oak-discover --workflows

# Debugging: Trace a specific workflow
./scripts/oak-history --workflow <ID> --full --sequence
```

**Power User Shortcuts:**

```bash
# Add to ~/.bashrc or ~/.zshrc
alias oak-agents='cd /Users/robertnyborg/Projects/claude-oak-agents/scripts'
alias oak-browse='./scripts/oak-discover'
alias oak-stats='./scripts/oak-insights'
alias oak-recent='./scripts/oak-history --last-days 1'
```

---

## Troubleshooting

**No agents found:**
- Check `--agents-dir` points to correct directory
- Verify agent files exist and have `.md` extension

**No telemetry data:**
- Check `--telemetry-file` points to correct JSONL file
- Verify telemetry system is enabled and collecting data
- Run at least one agent invocation to generate data

**Malformed line warnings:**
- JSONL file may have corrupted entries
- Tools skip bad lines and continue processing
- Review `telemetry/agent_invocations.jsonl` for issues

**Colors not showing:**
- Terminal may not support ANSI colors
- Try different terminal emulator
- Colors are aesthetic only, tools function without them

---

## Future Enhancements

Potential features for future versions:

- **Export formats**: JSON, CSV, HTML reports
- **Trend visualization**: ASCII charts and graphs
- **Real-time monitoring**: Watch mode for live updates
- **Agent comparison**: Side-by-side agent analysis
- **Workflow builder**: Interactive workflow design tool
- **Performance profiling**: Detailed bottleneck analysis
- **Cost tracking**: Token usage and cost estimation
- **Team analytics**: Multi-user collaboration metrics

---

## Contributing

To add new features or improve existing tools:

1. Edit the Python scripts in `scripts/`
2. Test with existing telemetry data
3. Update this README with new features
4. Submit changes via git-workflow-manager

---

## License

Same as claude-oak-agents project.

---

## Support

For issues or questions:
- Check CLAUDE.md for agent system documentation
- Review telemetry data quality
- Inspect agent frontmatter for metadata issues
- Verify Python 3.7+ is installed
