# OaK Mode Switching - Quick Reference Card

## Launch Commands

```bash
# Default mode (from config)
./scripts/oak-mode

# Specific modes
./scripts/oak-mode --guided     # For PMs
./scripts/oak-mode --expert     # For Engineers
./scripts/oak-mode --auto       # Reference

# Configuration
./scripts/oak-mode --set-default guided
./scripts/oak-mode --show
```

## Guided Mode Workflows

1. **Create Feature Specification** → spec-manager
2. **Design Database Schema** → backend-architect
3. **Prototype UI Components** → frontend-developer
4. **Map User Workflows** → product-strategist
5. **Create Product Roadmap** → product-strategist
6. **Analyze Business Problem** → product-strategist (Eigenquestions)
7. **Fork Repo and Create PR** → git-workflow-manager
8. **Run Security Scan** → security-auditor + dependency-scanner

## Expert Mode Commands

```bash
# Agent invocation
agent <name> <task>
agent backend-architect Design OAuth2 schema

# Workflows
workflow secure-api
workflow database-migration
workflow feature-spec
workflow security-audit

# Spec management
spec create <feature>
spec load <id>
spec list
spec update <id>

# System tools
status                  # oak-status
analyze                 # oak-analyze
discover                # oak-discover

# Mode switching
guided                  # Switch to guided
auto                    # Switch to auto
exit                    # Exit expert mode
```

## Workflow Patterns (Expert Mode)

### Secure API
```
design-simplicity-advisor
  ↓
backend-architect
  ↓
security-auditor
  ↓
quality-gate
```

### Database Migration
```
backend-architect
  ↓
quality-gate
  ↓
git-workflow-manager
```

### Feature Spec
```
spec-manager (collaborative)
```

### Security Audit
```
security-auditor + dependency-scanner
  ↓
quality-gate
```

## Auto Mode Flow

```
User Request
  ↓
Classification (INFORMATION|IMPLEMENTATION|ANALYSIS|COORDINATION)
  ↓
Domain Detection (Frontend|Backend|Infrastructure|Security|Data)
  ↓
Agent Selection (domain router)
  ↓
Workflow Execution
  ↓
Telemetry Tracking
```

## Configuration File

**Location:** `~/.oak/config.json`

```json
{
  "mode": "auto|guided|expert",
  "preferences": {
    "color": true,
    "verbose": false,
    "auto_save": true
  },
  "recent_workflows": [],
  "favorite_agents": []
}
```

## When to Use Each Mode

### Guided Mode
- **Who:** PMs, BAs, non-technical users
- **When:** Creating specs, designing schemas, prototyping
- **Why:** Step-by-step guidance with approvals

### Expert Mode
- **Who:** Engineers, DevOps, power users
- **When:** Direct agent control, workflow execution
- **Why:** Fast, command-line efficiency

### Auto Mode
- **Who:** All users (default)
- **When:** Standard OaK workflows
- **Why:** Automatic, intelligent routing

## Common Patterns

### PM Workflow (Guided)
```
1. Launch guided mode
2. Select "Create Feature Specification"
3. Provide feature name
4. Approve each section (Goals → Design → Plan → Tests)
5. Spec created in specs/active/
```

### Engineer Workflow (Expert)
```bash
oak> workflow secure-api
oak> spec create oauth2-integration
oak> agent backend-architect Implement OAuth2 endpoints
oak> status
```

### Default Workflow (Auto)
```
User to Claude: "Create React button component"
→ Auto classification and routing
→ Agents execute automatically
```

## File Locations

- **Main script:** `scripts/oak-mode`
- **Modes:** `scripts/modes/{guided,expert,auto}.py`
- **Config:** `~/.oak/config.json`
- **History:** `~/.oak/expert_history`
- **Docs:** `scripts/modes/README.md`

## Troubleshooting

**Config not created?**
```bash
mkdir -p ~/.oak
./scripts/oak-mode --show
```

**Mode not switching?**
```bash
./scripts/oak-mode --set-default <mode>
cat ~/.oak/config.json
```

**Import errors?**
```bash
cd /path/to/claude-oak-agents
python3 scripts/oak-mode
```

## Help Resources

- **Full docs:** `scripts/modes/README.md`
- **Summary:** `MODE_SWITCHING_SUMMARY.md`
- **PM guide:** `docs/PM_QUICK_START.md`
- **Agent patterns:** `.claude/AGENT_PATTERNS.md`
- **Domain router:** `core/domain_router.py`
