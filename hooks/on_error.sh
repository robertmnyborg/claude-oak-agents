#!/bin/bash
"""
On-Error Hook - Execute when errors occur

This hook runs when an error is detected during agent execution to:
- Log error details
- Capture context (agent, task, files)
- Send notifications if configured
- Create error report
- Suggest remediation

Usage:
    on_error.sh <error_type> <agent_name> <error_message> [--dry-run]

Arguments:
    error_type      Type of error (execution|validation|timeout|crash)
    agent_name      Agent that encountered the error
    error_message   Error message or description

Environment Variables:
    OAK_TELEMETRY_DIR: Directory for telemetry logs
    OAK_ERROR_TRACKING_ENABLED: Set to "false" to disable error tracking
    OAK_NOTIFY_ON_ERROR: Set to "true" to enable error notifications

Exit Codes:
    0: Success (error logged)
    1: Failed to log error
"""

set -e

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TELEMETRY_DIR="${OAK_TELEMETRY_DIR:-$PROJECT_ROOT/telemetry}"
ERROR_LOG="$TELEMETRY_DIR/errors.jsonl"
REPORTS_DIR="$PROJECT_ROOT/reports/errors"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Parse arguments
ERROR_TYPE="${1:-unknown}"
AGENT_NAME="${2:-unknown}"
ERROR_MESSAGE="${3:-No error message provided}"
DRY_RUN=false

shift 3 2>/dev/null || true

if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
fi

# Show help
if [[ "$ERROR_TYPE" == "--help" ]]; then
    echo "Usage: on_error.sh <error_type> <agent_name> <error_message> [--dry-run]"
    echo ""
    echo "Arguments:"
    echo "  error_type     Type: execution|validation|timeout|crash"
    echo "  agent_name     Agent that encountered the error"
    echo "  error_message  Error description"
    echo ""
    echo "Options:"
    echo "  --dry-run      Run without logging"
    echo "  --help         Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  OAK_TELEMETRY_DIR          Telemetry directory"
    echo "  OAK_ERROR_TRACKING_ENABLED Enable error tracking (default: true)"
    echo "  OAK_NOTIFY_ON_ERROR        Enable error notifications (default: false)"
    exit 0
fi

# Check if error tracking is enabled
if [[ "${OAK_ERROR_TRACKING_ENABLED:-true}" != "true" ]]; then
    echo -e "${YELLOW}Error tracking disabled${NC}" >&2
    exit 0
fi

# Ensure directories exist
mkdir -p "$TELEMETRY_DIR"
mkdir -p "$REPORTS_DIR"

# Generate error ID
generate_error_id() {
    local timestamp=$(date +%Y%m%d%H%M%S)
    local random=$(openssl rand -hex 4 2>/dev/null || echo "$(date +%s)")
    echo "err-${timestamp}-${random}"
}

# Capture context
capture_context() {
    local context="{}"

    # Get workflow context if available
    if [[ -n "${OAK_WORKFLOW_ID:-}" ]]; then
        context=$(echo "$context" | jq ". + {\"workflow_id\": \"$OAK_WORKFLOW_ID\"}" 2>/dev/null || echo "$context")
    fi

    # Get current directory
    local cwd=$(pwd)
    context=$(echo "$context" | jq ". + {\"working_directory\": \"$cwd\"}" 2>/dev/null || echo "$context")

    # Get git status if in repo
    if git rev-parse --git-dir > /dev/null 2>&1; then
        local branch=$(git branch --show-current 2>/dev/null || echo "unknown")
        local commit=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
        local dirty=$(git diff --quiet 2>/dev/null && echo "false" || echo "true")

        context=$(echo "$context" | jq ". + {\"git\": {\"branch\": \"$branch\", \"commit\": \"$commit\", \"dirty\": $dirty}}" 2>/dev/null || echo "$context")
    fi

    # Get recent files modified (last 10 minutes)
    local recent_files=$(find . -type f -mmin -10 -not -path '*/\.*' 2>/dev/null | head -10 | jq -R . | jq -s . 2>/dev/null || echo "[]")
    context=$(echo "$context" | jq ". + {\"recent_files\": $recent_files}" 2>/dev/null || echo "$context")

    echo "$context"
}

# Log error
log_error() {
    local error_id="$1"
    local context="$2"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${BLUE}[DRY RUN]${NC} Would log error: $error_id"
        return
    fi

    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Create error record
    local error_record=$(cat <<EOF
{
  "timestamp": "$timestamp",
  "error_id": "$error_id",
  "error_type": "$ERROR_TYPE",
  "agent_name": "$AGENT_NAME",
  "error_message": $(echo "$ERROR_MESSAGE" | jq -R . 2>/dev/null || echo "\"$ERROR_MESSAGE\""),
  "context": $context,
  "severity": "$(determine_severity "$ERROR_TYPE")"
}
EOF
)

    echo "$error_record" >> "$ERROR_LOG"
    echo -e "${GREEN}✓ Error logged: $error_id${NC}" >&2
}

# Determine severity
determine_severity() {
    local error_type="$1"

    case "$error_type" in
        crash|timeout)
            echo "critical"
            ;;
        validation)
            echo "high"
            ;;
        execution)
            echo "medium"
            ;;
        *)
            echo "low"
            ;;
    esac
}

# Create error report
create_error_report() {
    local error_id="$1"
    local context="$2"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${BLUE}[DRY RUN]${NC} Would create error report: $REPORTS_DIR/$error_id.md"
        return
    fi

    local report_file="$REPORTS_DIR/${error_id}.md"
    local timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    cat > "$report_file" <<EOF
# Error Report: $error_id

**Generated:** $timestamp

## Error Details

- **Type:** $ERROR_TYPE
- **Agent:** $AGENT_NAME
- **Severity:** $(determine_severity "$ERROR_TYPE")

## Error Message

\`\`\`
$ERROR_MESSAGE
\`\`\`

## Context

\`\`\`json
$context
\`\`\`

## Suggested Remediation

$(suggest_remediation "$ERROR_TYPE" "$AGENT_NAME")

## Next Steps

1. Review error message and context
2. Check agent logs for additional details
3. Verify input parameters and preconditions
4. Re-run agent with corrected inputs
5. If error persists, file issue in agent repository

---

*Generated by OaK Error Tracking System*
EOF

    echo -e "${GREEN}✓ Error report created: $report_file${NC}" >&2
}

# Suggest remediation
suggest_remediation() {
    local error_type="$1"
    local agent_name="$2"

    case "$error_type" in
        execution)
            echo "- Verify input parameters are correct"
            echo "- Check file permissions and paths"
            echo "- Review agent prerequisites"
            echo "- Check system resources (disk space, memory)"
            ;;
        validation)
            echo "- Review validation rules for $agent_name"
            echo "- Verify input format matches expected schema"
            echo "- Check for missing required fields"
            echo "- Validate data types and constraints"
            ;;
        timeout)
            echo "- Increase timeout limit if task is resource-intensive"
            echo "- Check for infinite loops or blocking operations"
            echo "- Review network connectivity if remote calls involved"
            echo "- Consider breaking task into smaller chunks"
            ;;
        crash)
            echo "- Check agent logs for stack traces"
            echo "- Verify all dependencies are installed"
            echo "- Check for recent code changes that may have introduced bugs"
            echo "- Test with minimal input to isolate issue"
            echo "- Consider filing bug report with reproduction steps"
            ;;
        *)
            echo "- Review error message for specific guidance"
            echo "- Check agent documentation for troubleshooting"
            echo "- Verify system configuration"
            ;;
    esac
}

# Send notification
send_notification() {
    local error_id="$1"
    local severity="$2"

    if [[ "${OAK_NOTIFY_ON_ERROR:-false}" != "true" ]]; then
        return
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${BLUE}[DRY RUN]${NC} Would send notification for error $error_id"
        return
    fi

    # Check if notification script exists
    local notify_script="$PROJECT_ROOT/automation/oak_notify.sh"
    if [[ -x "$notify_script" ]]; then
        echo -e "${MAGENTA}→${NC} Sending error notification..." >&2
        "$notify_script" "error" "$error_id" "$severity" "$AGENT_NAME" 2>/dev/null || true
    fi
}

# Display error summary
display_error_summary() {
    local error_id="$1"
    local severity="$2"

    echo ""
    echo -e "${RED}═══════════════════════════════════════════${NC}"
    echo -e "${RED}  Error Detected${NC}"
    echo -e "${RED}═══════════════════════════════════════════${NC}"
    echo ""
    echo "Error ID: $error_id"
    echo "Type: $ERROR_TYPE"
    echo "Agent: $AGENT_NAME"
    echo "Severity: $(
        if [[ "$severity" == "critical" ]]; then
            echo -e "${RED}Critical${NC}"
        elif [[ "$severity" == "high" ]]; then
            echo -e "${YELLOW}High${NC}"
        else
            echo -e "${BLUE}$severity${NC}"
        fi
    )"
    echo ""
    echo "Message:"
    echo "  $ERROR_MESSAGE"
    echo ""
    echo -e "${YELLOW}→ Error report: $REPORTS_DIR/$error_id.md${NC}"
    echo ""
}

# Main execution
main() {
    # Generate error ID
    local error_id=$(generate_error_id)

    # Capture context
    echo -e "${BLUE}→${NC} Capturing error context..." >&2
    local context=$(capture_context)

    # Log error
    echo -e "${BLUE}→${NC} Logging error..." >&2
    log_error "$error_id" "$context"

    # Create error report
    echo -e "${BLUE}→${NC} Creating error report..." >&2
    create_error_report "$error_id" "$context"

    # Determine severity
    local severity=$(determine_severity "$ERROR_TYPE")

    # Display summary
    display_error_summary "$error_id" "$severity"

    # Send notification if enabled
    if [[ "${OAK_NOTIFY_ON_ERROR:-false}" == "true" ]]; then
        send_notification "$error_id" "$severity"
    fi

    echo -e "${GREEN}✓ Error tracking complete${NC}" >&2
    echo ""
}

# Run main if not sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
