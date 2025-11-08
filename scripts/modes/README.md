# OaK Mode Switching System

Interactive mode switcher for Claude OaK Agents providing three distinct interaction styles optimized for different user types.

## Overview

The mode switching system allows users to choose their preferred interaction style:

1. **Guided Mode** - Interactive wizard for PMs and non-technical users
2. **Expert Mode** - Direct control for experienced engineers
3. **Auto Mode** - Automatic classification-based routing (default OaK behavior)

## Quick Start

```bash
# Launch in default mode (from config, or auto if not set)
./scripts/oak-mode

# Launch specific mode
./scripts/oak-mode --guided
./scripts/oak-mode --expert
./scripts/oak-mode --auto

# Set default mode
./scripts/oak-mode --set-default guided

# Show current configuration
./scripts/oak-mode --show
```

## Mode Descriptions

### Guided Mode

**For:** Product Managers, Business Analysts, Non-technical Users

**Interface:** Menu-driven workflow wizard

**Features:**
- Clear step-by-step guidance
- Plain language explanations
- Approval checkpoints before execution
- Progress indicators
- Common workflow templates

**Example Workflows:**
1. Create Feature Specification
2. Design Database Schema
3. Prototype UI Components
4. Map User Workflows
5. Create Product Roadmap
6. Analyze Business Problem (Eigenquestions)
7. Fork Repo and Create PR
8. Run Security Scan

**Usage:**
```bash
./scripts/oak-mode --guided
```

Then select from menu:
```
Welcome to OaK Guided Mode
==========================

What would you like to do?

1. Create a Feature Specification
2. Design a Database Schema
3. Prototype UI Components
...
```

### Expert Mode

**For:** Software Engineers, DevOps Engineers, Technical Users

**Interface:** Command-line shell with direct agent invocation

**Features:**
- Direct agent control
- Command history with readline support
- Workflow pattern execution
- Full system access
- Manual coordination control

**Commands:**
```bash
# Direct agent invocation
agent <name> <task>
agent backend-architect Design OAuth2 authentication schema

# Workflow patterns
workflow secure-api
workflow database-migration
workflow feature-spec
workflow security-audit

# Spec operations
spec create <feature-name>
spec load <spec-id>
spec list
spec update <spec-id>

# System tools
status              # Run oak-status
analyze             # Run oak-analyze
discover            # Browse agents

# Mode switching
guided              # Switch to guided mode
auto                # Switch to auto mode
exit                # Exit expert mode
```

**Usage:**
```bash
./scripts/oak-mode --expert
```

Interactive shell:
```
oak> agent backend-architect Design user authentication schema
oak> workflow secure-api
oak> spec create user-dashboard
oak> status
```

### Auto Mode

**For:** Default behavior - works for all users

**Interface:** Automatic classification and routing (existing OaK behavior)

**How It Works:**
1. **Request Classification** - Main LLM categorizes request type
2. **Domain Detection** - Domain router identifies relevant domains
3. **Agent Selection** - Optimal agents chosen based on classification + domain
4. **Workflow Execution** - Standard workflow with quality gates
5. **Telemetry Tracking** - Performance metrics logged

**Example Flow:**
```
User: "Create a React button component with TypeScript"

Classification: IMPLEMENTATION
Domain Detection:
  - Keywords: react, component, typescript
  - Domain: Frontend (confidence: 0.95)

Agent Plan:
  1. design-simplicity-advisor → Analyze approach
  2. frontend-developer → Create component
  3. quality-gate → Validate code
  4. git-workflow-manager → Commit changes

Result: Component created, validated, and committed
```

**Usage:**
```bash
./scripts/oak-mode --auto
# Or just use existing OaK workflows - auto mode is the default
```

## Configuration

Configuration stored in `~/.oak/config.json`:

```json
{
  "mode": "auto",
  "preferences": {
    "color": true,
    "verbose": false,
    "auto_save": true
  },
  "recent_workflows": [],
  "favorite_agents": []
}
```

### Configuration Commands

```bash
# Show current configuration
./scripts/oak-mode --show

# Set default mode
./scripts/oak-mode --set-default guided
./scripts/oak-mode --set-default expert
./scripts/oak-mode --set-default auto
```

## Mode Persistence

- Mode preference saved to `~/.oak/config.json`
- Remembered across sessions
- Can be changed anytime
- Expert mode saves command history to `~/.oak/expert_history`

## Workflow Examples

### Guided Mode Example

```
User: Launches guided mode
System: Shows menu with 9 options

User: Selects "1. Create a Feature Specification"
System: "What feature are you building?"

User: "User authentication"
System: "This will take 10-15 minutes. The spec-manager will:
         1. Define goals and requirements (with your approval)
         2. Design the technical solution (with your approval)
         3. Create an implementation plan (with your approval)
         4. Define testing strategy (with your approval)
         Ready to start? [Y/n]"

User: Y
System: Invokes spec-manager with approval checkpoints
```

### Expert Mode Example

```bash
oak> workflow secure-api
API endpoint to create: POST /api/users/login

Executing workflow...
→ design-simplicity-advisor: Analyze approach for POST /api/users/login
→ backend-architect: Implement POST /api/users/login
→ security-auditor: Security review of POST /api/users/login
→ quality-gate: Validate implementation

Workflow complete!
```

### Auto Mode Example

```
User (to Claude): "Fix the SQL injection vulnerability in user.repository.ts"

Main LLM Classification: IMPLEMENTATION
Domain Detection:
  - Security (0.90)
  - Backend (0.70)

Agent Plan:
  design-simplicity-advisor → security-auditor → backend-architect → quality-gate → git-workflow-manager

Execution: Automatic workflow with telemetry tracking
```

## Implementation Details

### File Structure

```
scripts/
  oak-mode                    # Main entry point
  modes/
    guided.py                 # Guided mode implementation
    expert.py                 # Expert mode implementation
    auto.py                   # Auto mode reference
    README.md                 # This file

~/.oak/
  config.json                 # User configuration
  expert_history              # Command history (expert mode)
```

### Mode Classes

**ConfigManager** (`oak-mode`):
- Loads/saves configuration
- Manages preferences
- Tracks recent workflows

**GuidedMode** (`guided.py`):
- Interactive menu system
- Workflow templates
- User-friendly explanations

**ExpertShell** (`expert.py`):
- cmd.Cmd-based shell
- Command completion
- History support
- Direct agent invocation

**Auto Mode** (`auto.py`):
- Reference explanation
- Domain router demonstration
- Existing OaK behavior

### Integration with Domain Router

All modes use the domain router for agent selection:

```python
from core.domain_router import DomainRouter

router = DomainRouter()
domains = router.identify_domains(
    request_text="Create React component",
    file_paths=["src/components/Button.tsx"]
)

# Returns:
# [
#   {
#     "domain": "frontend",
#     "confidence": 0.95,
#     "config": {...},
#     "reasons": ["3 keyword(s) matched", "1 file pattern(s) matched"]
#   }
# ]
```

### Integration with Agent Loader

Expert mode loads agent metadata for discovery:

```python
from core.agent_loader import AgentLoader

loader = AgentLoader(Path("agents"))
metadata = loader.load_all_metadata()

# Access agent capabilities
agent = loader.load_agent("backend-architect")
print(agent.metadata.description)
```

## Quality Requirements

### User-Friendliness (Guided Mode)
- ✅ Clear menu systems with descriptions
- ✅ Plain language explanations
- ✅ Approval checkpoints
- ✅ Progress indicators
- ✅ Error handling with helpful messages

### Power User Features (Expert Mode)
- ✅ Direct agent invocation
- ✅ Workflow pattern execution
- ✅ Command history with readline
- ✅ Full system access
- ✅ Mode switching without restart

### Backward Compatibility (Auto Mode)
- ✅ Existing OaK behavior preserved
- ✅ Classification-based routing
- ✅ Domain detection integration
- ✅ Telemetry tracking
- ✅ No breaking changes

## Testing

```bash
# Test mode switching
./scripts/oak-mode --show
./scripts/oak-mode --set-default guided
./scripts/oak-mode --set-default expert
./scripts/oak-mode --set-default auto

# Test guided mode (interactive)
./scripts/oak-mode --guided

# Test expert mode (interactive)
./scripts/oak-mode --expert

# Test auto mode (demonstration)
./scripts/oak-mode --auto
```

## Future Enhancements

### Guided Mode
- Agent invocation integration (currently demo placeholders)
- Real-time progress tracking
- Workflow history and favorites
- Template customization

### Expert Mode
- Tab completion for agent names
- Workflow recording and replay
- Macro support for common commands
- Real-time telemetry dashboard

### Auto Mode
- Machine learning-based classification
- Dynamic confidence threshold adjustment
- User feedback loop for routing improvement
- Automated workflow optimization

## Troubleshooting

**Issue:** Config file not created
```bash
# Manually create config directory
mkdir -p ~/.oak
# Run oak-mode again
./scripts/oak-mode --show
```

**Issue:** Mode not switching
```bash
# Check current mode
./scripts/oak-mode --show

# Force set mode
./scripts/oak-mode --set-default guided

# Verify
cat ~/.oak/config.json
```

**Issue:** Import errors in modes
```bash
# Ensure running from project root
cd /path/to/claude-oak-agents
python3 scripts/oak-mode
```

## Documentation

- **PM Quick Start:** `docs/PM_QUICK_START.md`
- **Agent Patterns:** `.claude/AGENT_PATTERNS.md`
- **Domain Router:** `core/domain_router.py`
- **Agent Loader:** `core/agent_loader.py`
- **Main Rules:** `CLAUDE.md`

## Support

For issues or questions:
1. Check configuration: `./scripts/oak-mode --show`
2. Review logs in `logs/` directory
3. Use `oak-status` for system diagnostics
4. Consult domain router output for routing issues
