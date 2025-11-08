# OaK Hooks System Documentation

Complete guide to the OaK hooks system for workflow automation, error tracking, and specification management.

## Table of Contents

- [Overview](#overview)
- [Available Hooks](#available-hooks)
- [Installation](#installation)
- [Hook Details](#hook-details)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Telemetry Integration](#telemetry-integration)
- [Troubleshooting](#troubleshooting)

---

## Overview

The OaK hooks system provides automated event handling for:

- **Workflow Management**: Track multi-agent workflows from start to completion
- **Error Tracking**: Capture errors with context and suggest remediation
- **Spec Evolution**: Monitor specification changes and maintain YAML sync
- **Session Management**: Load orchestration rules at session start
- **Telemetry Integration**: All hooks log to centralized telemetry system

### Hook Types

1. **Lifecycle Hooks**: `pre-workflow`, `post-workflow`
2. **Event Hooks**: `on-error`, `on-spec-change`
3. **Session Hooks**: `sessionStart`

---

## Available Hooks

### sessionStart

**Purpose**: Load squad orchestration rules and agent delegation system

**Trigger**: Automatically at session initialization

**Actions**:
- Load CLAUDE.md rules
- Initialize agent delegation system
- Set up environment variables

**Configuration**:
```json
{
  "sessionStart": {
    "description": "Load squad orchestration rules and agent delegation system",
    "script": "./sessionStart.sh",
    "enabled": true
  }
}
```

---

### pre-workflow

**Purpose**: Execute before workflow starts

**Trigger**: Manual invocation before multi-agent workflow

**Actions**:
- Log workflow initiation
- Validate preconditions
- Set workflow environment variables
- Check for conflicts with existing workflows

**Usage**:
```bash
./hooks/pre_workflow.sh <workflow_id> <workflow_description> [--dry-run]
```

**Example**:
```bash
./hooks/pre_workflow.sh wf-20251108-oauth2 "Implement OAuth2 authentication"
```

**Environment Variables Set**:
- `OAK_WORKFLOW_ID`: Current workflow identifier
- `OAK_WORKFLOW_START_TIME`: Workflow start timestamp
- `OAK_WORKFLOW_DESC`: Workflow description

**Telemetry**:
- Logs to: `telemetry/workflow_events.jsonl`
- Event type: `workflow_start`

---

### post-workflow

**Purpose**: Execute after workflow completes

**Trigger**: Manual invocation after multi-agent workflow

**Actions**:
- Log workflow completion
- Calculate workflow statistics
- Clean up workflow state
- Trigger notifications (if enabled)

**Usage**:
```bash
./hooks/post_workflow.sh <workflow_id> <status> [--dry-run]
```

**Arguments**:
- `workflow_id`: Workflow identifier (from pre-workflow)
- `status`: `success`, `failure`, or `partial`

**Example**:
```bash
./hooks/post_workflow.sh wf-20251108-oauth2 success
```

**Statistics Calculated**:
- Total agents executed
- Successful/failed agent count
- Total duration
- Average agent duration

**Telemetry**:
- Logs to: `telemetry/workflow_events.jsonl`
- Event type: `workflow_complete`
- Includes full statistics JSON

---

### on-error

**Purpose**: Execute when errors occur during agent execution

**Trigger**: Manual invocation when error detected

**Actions**:
- Log error details
- Capture context (agent, task, files, git state)
- Create error report
- Suggest remediation steps
- Send notifications (if enabled)

**Usage**:
```bash
./hooks/on_error.sh <error_type> <agent_name> <error_message> [--dry-run]
```

**Error Types**:
- `execution`: General execution error
- `validation`: Validation failure
- `timeout`: Timeout exceeded
- `crash`: Agent crash or fatal error

**Example**:
```bash
./hooks/on_error.sh execution backend-architect "Database connection failed"
```

**Error Reports**:
- Location: `reports/errors/<error_id>.md`
- Includes: Error details, context, suggested remediation
- Format: Markdown with JSON context

**Severity Levels**:
- `critical`: crash, timeout
- `high`: validation
- `medium`: execution
- `low`: other

**Telemetry**:
- Logs to: `telemetry/errors.jsonl`
- Includes: Full error context, git state, recent files

---

### on-spec-change

**Purpose**: Execute when specification files are modified

**Trigger**: Manual invocation after spec file change

**Actions**:
- Detect which spec changed
- Log change reason
- Regenerate YAML if Markdown changed
- Notify related workflows
- Track spec evolution

**Usage**:
```bash
./hooks/on_spec_change.sh <spec_file> <change_type> [reason] [--dry-run]
```

**Change Types**:
- `created`: New spec file created
- `modified`: Existing spec modified
- `deleted`: Spec file deleted
- `completed`: Spec moved to completed

**Example**:
```bash
./hooks/on_spec_change.sh specs/active/2025-11-08-oauth2-implementation.md modified "Updated authentication flow"
```

**Automatic YAML Regeneration**:
- Triggered when Markdown file changes
- Uses: `specs/tools/generate_yaml.py`
- Output: Corresponding `.yaml` file

**Telemetry**:
- Logs to: `telemetry/spec_changes.jsonl`
- Includes: Spec ID, file type, change type, reason

---

## Installation

### Automatic Installation

The hooks are already configured in `hooks/hooks.json`. To enable:

1. Ensure all hooks are executable:
```bash
chmod +x hooks/*.sh
```

2. Verify hooks configuration:
```bash
cat hooks/hooks.json
```

3. Test hooks individually:
```bash
./hooks/pre_workflow.sh --help
./hooks/post_workflow.sh --help
./hooks/on_error.sh --help
./hooks/on_spec_change.sh --help
```

### Environment Variables

Set these in your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
# Required
export OAK_TELEMETRY_DIR="$HOME/Projects/claude-oak-agents/telemetry"

# Optional workflow tracking
export OAK_WORKFLOW_ENABLED=true        # Enable workflow tracking (default: true)

# Optional error tracking
export OAK_ERROR_TRACKING_ENABLED=true  # Enable error tracking (default: true)
export OAK_NOTIFY_ON_ERROR=false        # Send error notifications (default: false)

# Optional spec tracking
export OAK_SPEC_TRACKING_ENABLED=true   # Enable spec tracking (default: true)
export OAK_SPECS_DIR="$HOME/Projects/claude-oak-agents/specs"

# Optional notifications
export OAK_NOTIFY_ENABLED=false         # Enable workflow notifications (default: false)
```

Reload shell:
```bash
source ~/.zshrc  # or ~/.bashrc
```

---

## Hook Details

### Dry Run Mode

All hooks support `--dry-run` mode for testing:

```bash
# Test without logging
./hooks/pre_workflow.sh wf-test-001 "Test workflow" --dry-run

# Preview error report without creating
./hooks/on_error.sh execution test-agent "Test error" --dry-run

# See what would be logged
./hooks/post_workflow.sh wf-test-001 success --dry-run

# Preview spec change processing
./hooks/on_spec_change.sh specs/active/test.md modified "Testing" --dry-run
```

### Exit Codes

All hooks follow standard exit codes:

- `0`: Success
- `1`: Error or validation failure
- `2`: Conflict detected (pre-workflow only)

### Logging Behavior

All hooks:
- Log to JSONL files in `telemetry/`
- Use UTC timestamps
- Include workflow context when available
- Fail gracefully if logging fails
- Never block execution

---

## Configuration

### Enabling/Disabling Hooks

Edit `hooks/hooks.json`:

```json
{
  "pre-workflow": {
    "description": "...",
    "script": "./pre_workflow.sh",
    "enabled": false  // Set to false to disable
  }
}
```

### Per-Hook Configuration

#### Pre-Workflow

Validate preconditions:
- Telemetry directory writable
- Workflow ID format (wf-YYYYMMDD-*)
- Active workflow conflicts (warns if >5 in last hour)

#### Post-Workflow

Statistics calculated:
- Total agents executed
- Success/failure counts
- Duration metrics
- Average agent duration

#### On-Error

Context captured:
- Current workflow ID
- Working directory
- Git status (branch, commit, dirty)
- Recent files (modified in last 10 minutes)

Remediation suggestions based on error type.

#### On-Spec-Change

Spec tracking:
- Change frequency monitoring
- Workflow impact analysis
- YAML regeneration for Markdown changes

---

## Usage Examples

### Complete Workflow Lifecycle

```bash
# 1. Start workflow
./hooks/pre_workflow.sh wf-20251108-feature "Implement new feature"

# 2. Execute agents (workflow_id set automatically)
# ... agent execution happens ...

# 3. Handle errors if needed
./hooks/on_error.sh execution backend-architect "Database schema conflict"

# 4. Complete workflow
./hooks/post_workflow.sh wf-20251108-feature success
```

### Spec-Driven Development

```bash
# 1. Create new spec
./hooks/on_spec_change.sh specs/active/2025-11-08-feature.md created "New feature spec"

# 2. Modify during implementation
./hooks/on_spec_change.sh specs/active/2025-11-08-feature.md modified "Updated acceptance criteria"

# 3. Mark complete
mv specs/active/2025-11-08-feature.md specs/completed/
./hooks/on_spec_change.sh specs/completed/2025-11-08-feature.md completed "Feature implemented"
```

### Error Tracking

```bash
# Execution error
./hooks/on_error.sh execution backend-architect "Connection timeout to database"

# Validation error
./hooks/on_error.sh validation frontend-developer "Invalid prop types in component"

# Timeout error
./hooks/on_error.sh timeout infrastructure-specialist "CDK deploy exceeded 10 minutes"

# Critical crash
./hooks/on_error.sh crash security-auditor "Segmentation fault in scanner"
```

### Notifications

Enable notifications:
```bash
export OAK_NOTIFY_ENABLED=true
export OAK_NOTIFY_ON_ERROR=true
```

Notifications require `automation/oak_notify.sh` to be configured.

---

## Telemetry Integration

### Telemetry Files

Hooks write to these JSONL files:

| File | Hook | Content |
|------|------|---------|
| `telemetry/workflow_events.jsonl` | pre-workflow, post-workflow | Workflow lifecycle events |
| `telemetry/errors.jsonl` | on-error | Error records with context |
| `telemetry/spec_changes.jsonl` | on-spec-change | Specification change history |
| `telemetry/agent_invocations.jsonl` | All | Agent execution records (referenced) |

### Workflow Context

When `OAK_WORKFLOW_ID` is set:
- All hooks include workflow_id in logs
- Agent invocations link to workflow
- Error reports include workflow context
- Spec changes track workflow impact

### Querying Telemetry

```bash
# View workflow events
cat telemetry/workflow_events.jsonl | jq

# View errors
cat telemetry/errors.jsonl | jq

# View spec changes
cat telemetry/spec_changes.jsonl | jq

# Filter by workflow
cat telemetry/workflow_events.jsonl | jq 'select(.workflow_id == "wf-20251108-oauth2")'

# Count errors by type
cat telemetry/errors.jsonl | jq -r '.error_type' | sort | uniq -c
```

---

## Troubleshooting

### Hooks Not Executing

**Check permissions**:
```bash
ls -l hooks/*.sh
# Should show: -rwxr-xr-x
```

**Fix permissions**:
```bash
chmod +x hooks/*.sh
```

**Verify enabled**:
```bash
cat hooks/hooks.json | jq '.[].enabled'
```

### Telemetry Not Logging

**Check directory exists**:
```bash
ls -la telemetry/
```

**Create if missing**:
```bash
mkdir -p telemetry
```

**Check write permissions**:
```bash
touch telemetry/test.txt && rm telemetry/test.txt || echo "Not writable"
```

**Check environment variable**:
```bash
echo $OAK_TELEMETRY_DIR
```

### Workflow Context Not Available

**Check environment variables**:
```bash
echo $OAK_WORKFLOW_ID
echo $OAK_WORKFLOW_START_TIME
```

**Source temp file**:
```bash
source /tmp/oak_workflow_<workflow_id>.env
```

**Re-run pre-workflow**:
```bash
./hooks/pre_workflow.sh <workflow_id> "<description>"
```

### YAML Regeneration Failing

**Check generator exists**:
```bash
ls -l specs/tools/generate_yaml.py
```

**Test generator manually**:
```bash
./specs/tools/generate_yaml.py specs/active/<spec>.md
```

**Check Python dependencies**:
```bash
python3 -c "import yaml, json"
```

### Notifications Not Working

**Check notification script**:
```bash
ls -l automation/oak_notify.sh
```

**Test notification manually**:
```bash
./automation/oak_notify.sh test "Test message"
```

**Check environment variable**:
```bash
echo $OAK_NOTIFY_ENABLED
echo $OAK_NOTIFY_ON_ERROR
```

---

## Integration with OaK System

### Workflow Coordination

Hooks integrate with Phase 2A workflow tracking:

1. **pre-workflow**: Sets `OAK_WORKFLOW_ID` for agent invocations
2. **Agents execute**: Automatically include workflow_id in telemetry
3. **post-workflow**: Aggregates agent statistics from workflow

### Spec-Driven Development

Hooks support spec-manager workflow:

1. **Spec created**: `on-spec-change` logs creation
2. **Spec modified**: YAML regenerated automatically
3. **Implementation**: Agents use spec_id in telemetry
4. **Spec completed**: Change logged with completion reason

### Error Recovery

Hooks enable systematic error handling:

1. **Error detected**: `on-error` creates detailed report
2. **Context captured**: Git state, files, workflow
3. **Remediation suggested**: Based on error type
4. **Notification sent**: Team alerted if configured

---

## Advanced Usage

### Custom Hook Scripts

Create custom hooks by:

1. Add script to `hooks/` directory
2. Make executable: `chmod +x hooks/custom_hook.sh`
3. Add to `hooks/hooks.json`:
```json
{
  "custom-hook": {
    "description": "Custom hook description",
    "script": "./custom_hook.sh",
    "enabled": true
  }
}
```

### Hook Chaining

Chain hooks for complex workflows:

```bash
# Workflow with error handling
./hooks/pre_workflow.sh wf-001 "Feature" || exit 1

# Execute with error capture
if ! execute_agents; then
    ./hooks/on_error.sh execution agent-name "Execution failed"
    ./hooks/post_workflow.sh wf-001 failure
    exit 1
fi

./hooks/post_workflow.sh wf-001 success
```

### Batch Processing

Process multiple hooks:

```bash
# Batch error processing
for error in errors/*.log; do
    error_msg=$(cat "$error")
    ./hooks/on_error.sh execution unknown "$error_msg"
done

# Batch spec processing
for spec in specs/active/*.md; do
    ./hooks/on_spec_change.sh "$spec" modified "Batch update"
done
```

---

## See Also

- [OaK Status Tool](../scripts/oak-status) - System status viewer
- [Workflow Tracking](../telemetry/README.md) - Phase 2A workflow system
- [Telemetry System](../telemetry/README.md) - Complete telemetry documentation
- [Spec Management](../specs/README.md) - Specification system guide

---

## Support

For issues with hooks:

1. Check this documentation
2. Run with `--dry-run` to debug
3. Check telemetry logs for details
4. Review hook source code for specifics
5. File issue in repository if needed

---

*Last updated: 2025-11-08*
