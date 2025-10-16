# Hooks Directory

Automatic telemetry logging hooks for Claude agents (Phase 1.5).

## Overview

The hooks system enables automatic telemetry logging for all agent invocations without requiring manual instrumentation. When enabled, every agent that executes will have its invocation logged with state features, duration, outcome, and optional human feedback.

## Architecture

```
Agent Execution Flow (with hooks):

1. Main LLM delegates to agent
   ↓
2. pre_agent_hook.py executes
   - Extracts state features
   - Logs invocation start
   - Stores invocation ID in temp file
   ↓
3. Agent executes normally
   ↓
4. post_agent_hook.py executes
   - Retrieves invocation ID
   - Calculates duration
   - Logs completion with outcome
   - Optionally prompts for feedback
   ↓
5. Telemetry data ready for analysis
```

## Installation

### Quick Install

```bash
# Make install script executable
chmod +x hooks/install_hooks.sh

# Run installation
./hooks/install_hooks.sh
```

The installer will:
1. Create symlinks in `~/.claude/hooks/`
2. Add environment variables to your shell RC file (optional)
3. Set up telemetry directory
4. Make hook scripts executable

### Manual Install

1. **Create symlinks:**
   ```bash
   ln -s ~/Projects/claude-oak-agents/hooks/pre_agent_hook.py ~/.claude/hooks/pre_agent.sh
   ln -s ~/Projects/claude-oak-agents/hooks/post_agent_hook.py ~/.claude/hooks/post_agent.sh
   ```

2. **Add to shell RC (~/.zshrc or ~/.bashrc):**
   ```bash
   export OAK_TELEMETRY_ENABLED=true
   export OAK_TELEMETRY_DIR="$HOME/Projects/claude-oak-agents/telemetry"
   export OAK_PROMPT_FEEDBACK=false
   export PYTHONPATH="$HOME/Projects/claude-oak-agents:$PYTHONPATH"
   ```

3. **Reload shell:**
   ```bash
   source ~/.zshrc  # or ~/.bashrc
   ```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OAK_TELEMETRY_ENABLED` | `true` | Enable/disable telemetry logging |
| `OAK_TELEMETRY_DIR` | `~/Projects/claude-oak-agents/telemetry` | Where to store logs |
| `OAK_PROMPT_FEEDBACK` | `false` | Prompt for feedback after each agent |
| `PYTHONPATH` | - | Must include project root |

### Enable/Disable Telemetry

**Temporarily disable:**
```bash
export OAK_TELEMETRY_ENABLED=false
```

**Re-enable:**
```bash
export OAK_TELEMETRY_ENABLED=true
```

**Permanently disable:**
```bash
# Edit ~/.zshrc or ~/.bashrc
export OAK_TELEMETRY_ENABLED=false
```

## Usage

Once installed, hooks work automatically. No changes to agent invocations required!

```bash
# Before hooks: Manual logging required
User: "Implement feature X"
Main LLM: [delegates to agent]
Agent: [executes]
# No telemetry logged ❌

# After hooks: Automatic logging
User: "Implement feature X"
Main LLM: [delegates to agent]
pre_agent_hook: [logs start with state features] ✅
Agent: [executes]
post_agent_hook: [logs completion with duration] ✅
# Telemetry automatically logged!
```

## Viewing Telemetry Data

```bash
# View raw logs
cat telemetry/agent_invocations.jsonl | jq

# View success metrics
cat telemetry/success_metrics.jsonl | jq

# Generate statistics
./scripts/analyze_telemetry.sh

# Or use Python
python -c "
from telemetry.analyzer import TelemetryAnalyzer
analyzer = TelemetryAnalyzer()
analyzer.print_summary()
"
```

## Interactive Feedback

Enable interactive feedback prompts after each agent:

```bash
export OAK_PROMPT_FEEDBACK=true
```

When enabled, you'll be prompted after each agent execution:
```
📊 Quick feedback for backend-architect:
  Success? (y/n): y
  Quality (1-5): 4
  ✓ Feedback recorded!
```

**Tip:** Keep this disabled during active development to avoid interruptions. Enable during review/testing phases.

## Hook Scripts

### pre_agent_hook.py

**Purpose:** Log agent invocation start

**Actions:**
1. Check if telemetry is enabled
2. Extract state features from workspace
3. Log invocation with TelemetryLogger
4. Store invocation ID in temp file
5. Exit without blocking agent execution

**Error Handling:** Fails silently if telemetry unavailable (doesn't block agent)

### post_agent_hook.py

**Purpose:** Log agent completion

**Actions:**
1. Check if telemetry is enabled
2. Retrieve invocation ID from temp file
3. Calculate execution duration
4. Determine outcome from exit code
5. Update invocation with completion data
6. Optionally prompt for feedback
7. Clean up temp file

**Error Handling:** Fails silently if telemetry unavailable

## Troubleshooting

### Hooks not executing

**Check symlinks:**
```bash
ls -la ~/.claude/hooks/
```

Should show:
```
pre_agent.sh -> /Users/.../claude-oak-agents/hooks/pre_agent_hook.py
post_agent.sh -> /Users/.../claude-oak-agents/hooks/post_agent_hook.py
```

**Check permissions:**
```bash
ls -l hooks/*.py
# Should show executable permission: -rwxr-xr-x
```

**Fix permissions:**
```bash
chmod +x hooks/*.py
```

### "ModuleNotFoundError" errors

**Check PYTHONPATH:**
```bash
echo $PYTHONPATH
# Should include: /Users/.../claude-oak-agents
```

**Add if missing:**
```bash
export PYTHONPATH="$HOME/Projects/claude-oak-agents:$PYTHONPATH"
```

### Telemetry not logging

**Check if enabled:**
```bash
echo $OAK_TELEMETRY_ENABLED
# Should show: true
```

**Check directory:**
```bash
echo $OAK_TELEMETRY_DIR
ls -la $OAK_TELEMETRY_DIR
# Should exist and be writable
```

**Check logs:**
```bash
# Hooks write to stderr, visible in terminal
# Look for: "✓ Logged agent start: ..."
```

### Agent execution blocked

**This should never happen!** Hooks are designed to fail silently.

If hooks are blocking execution:
1. Check for syntax errors: `python3 hooks/pre_agent_hook.py --help`
2. Disable hooks temporarily: `export OAK_TELEMETRY_ENABLED=false`
3. Uninstall hooks: `./hooks/uninstall_hooks.sh`

## Uninstallation

```bash
# Run uninstaller
./hooks/uninstall_hooks.sh
```

The uninstaller will:
1. Remove hook symlinks
2. Offer to restore previous hooks (if any)
3. Preserve telemetry data
4. Provide instructions for manual cleanup

**Note:** Environment variables in shell RC file are NOT removed automatically. Delete them manually if desired.

## Security & Privacy

### What Gets Logged

- **Agent name and type**
- **Task description** (as provided to agent)
- **State features:** Languages, frameworks, file counts, test status, etc.
- **Execution data:** Duration, outcome, files modified
- **Workspace path** (can contain sensitive info)

### What Does NOT Get Logged

- File contents
- Environment variables (except what's in state features)
- User credentials
- Network requests
- Tool outputs

### Privacy Considerations

- All data stored **locally** in `telemetry/` directory
- No data sent to external services
- Add `telemetry/*.jsonl` to `.gitignore` to prevent commits
- Review logs before sharing: `cat telemetry/agent_invocations.jsonl | jq`

### Sensitive Data

If working with sensitive codebases:
1. Disable telemetry: `export OAK_TELEMETRY_ENABLED=false`
2. Or exclude sensitive repos in hooks (modify pre_agent_hook.py)
3. Or use separate telemetry directory per project

## Advanced Configuration

### Per-Project Telemetry

```bash
# In project-specific .env or script
export OAK_TELEMETRY_DIR="/path/to/project/.telemetry"
```

### Conditional Logging

Modify `pre_agent_hook.py` to add conditions:

```python
def is_telemetry_enabled():
    # Disable for specific paths
    workspace = get_workspace_dir()
    if "sensitive-project" in str(workspace):
        return False

    # Disable for specific agents
    if agent_name in ["general-purpose", "agent-creator"]:
        return False

    # Default check
    enabled = os.getenv("OAK_TELEMETRY_ENABLED", "true").lower()
    return enabled in ["true", "1", "yes", "on"]
```

### Custom Telemetry Backend

Replace TelemetryLogger with custom implementation:

```python
# In pre_agent_hook.py
from my_custom_telemetry import CustomLogger

logger = CustomLogger(endpoint="https://my-telemetry-api.com")
logger.log_invocation(...)
```

## Integration with Phase 3

Hooks integrate seamlessly with OaK Phase 3 (feature-based decomposition):

1. **pre-hook** extracts state features → available to project-manager
2. **project-manager** uses features for decomposition
3. **post-hook** logs execution results
4. **telemetry analyzer** provides historical data for future planning

This creates a feedback loop: better state analysis → better planning → better execution data → better future planning.

## Future Enhancements

Planned improvements:
- [ ] Tool usage tracking (which tools agent used)
- [ ] Automatic outcome detection (parse logs for errors)
- [ ] Real-time dashboard
- [ ] Integration with ML pipeline (Phase 6)
- [ ] Agent performance alerts
- [ ] Automatic A/B testing

## Support

Issues with hooks? Check:
1. [Troubleshooting section above](#troubleshooting)
2. [Main README](../README.md)
3. [Implementation Guide](../docs/oak-design/IMPLEMENTATION_GUIDE.md)
4. [GitHub Issues](https://github.com/your-org/claude-oak-agents/issues)
