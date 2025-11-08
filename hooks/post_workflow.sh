#!/bin/bash
"""
Post-Workflow Hook - Execute after workflow completes

This hook runs at the end of a multi-agent workflow to:
- Log workflow completion
- Calculate workflow statistics
- Clean up workflow state
- Trigger notifications if configured

Usage:
    post_workflow.sh <workflow_id> <status> [--dry-run]

Arguments:
    workflow_id    The workflow identifier
    status         success|failure|partial

Environment Variables:
    OAK_TELEMETRY_DIR: Directory for telemetry logs
    OAK_WORKFLOW_ENABLED: Set to "false" to disable workflow tracking
    OAK_NOTIFY_ENABLED: Set to "true" to enable notifications

Exit Codes:
    0: Success
    1: Error during cleanup
"""

set -e

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TELEMETRY_DIR="${OAK_TELEMETRY_DIR:-$PROJECT_ROOT/telemetry}"
WORKFLOW_EVENTS="$TELEMETRY_DIR/workflow_events.jsonl"
AGENT_INVOCATIONS="$TELEMETRY_DIR/agent_invocations.jsonl"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Parse arguments
WORKFLOW_ID="${1:-}"
STATUS="${2:-success}"
DRY_RUN=false

if [[ "$3" == "--dry-run" ]]; then
    DRY_RUN=true
fi

# Show help
if [[ "$1" == "--help" || -z "$WORKFLOW_ID" ]]; then
    echo "Usage: post_workflow.sh <workflow_id> <status> [--dry-run]"
    echo ""
    echo "Arguments:"
    echo "  workflow_id    Workflow identifier"
    echo "  status         success|failure|partial (default: success)"
    echo ""
    echo "Options:"
    echo "  --dry-run      Run without logging or cleanup"
    echo "  --help         Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  OAK_TELEMETRY_DIR    Telemetry directory (default: PROJECT_ROOT/telemetry)"
    echo "  OAK_WORKFLOW_ENABLED Enable/disable workflow tracking (default: true)"
    echo "  OAK_NOTIFY_ENABLED   Enable notifications (default: false)"
    exit 0
fi

# Check if workflow tracking is enabled
if [[ "${OAK_WORKFLOW_ENABLED:-true}" != "true" ]]; then
    echo -e "${YELLOW}Workflow tracking disabled${NC}" >&2
    exit 0
fi

# Log function
log_event() {
    local event_type="$1"
    local status="$2"
    local message="$3"
    local stats="${4:-}"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${BLUE}[DRY RUN]${NC} Would log: $event_type - $status - $message"
        return
    fi

    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%SZ")

    if [[ -n "$stats" ]]; then
        local event=$(cat <<EOF
{"timestamp": "$timestamp", "event_type": "$event_type", "workflow_id": "$WORKFLOW_ID", "status": "$status", "message": "$message", "statistics": $stats}
EOF
)
    else
        local event=$(cat <<EOF
{"timestamp": "$timestamp", "event_type": "$event_type", "workflow_id": "$WORKFLOW_ID", "status": "$status", "message": "$message"}
EOF
)
    fi

    echo "$event" >> "$WORKFLOW_EVENTS"
}

# Calculate workflow statistics
calculate_statistics() {
    if [[ ! -f "$AGENT_INVOCATIONS" ]]; then
        echo "{}"
        return
    fi

    # Get workflow start time from temp file
    local temp_file="/tmp/oak_workflow_${WORKFLOW_ID}.env"
    local start_time=""

    if [[ -f "$temp_file" ]]; then
        source "$temp_file"
        start_time="$OAK_WORKFLOW_START_TIME"
    fi

    # Parse agent invocations for this workflow
    local total_agents=0
    local successful_agents=0
    local failed_agents=0
    local total_duration=0

    while IFS= read -r line; do
        if [[ -z "$line" ]]; then
            continue
        fi

        # Check if this invocation belongs to our workflow
        if echo "$line" | grep -q "\"workflow_id\": *\"$WORKFLOW_ID\""; then
            ((total_agents++))

            # Extract status
            if echo "$line" | grep -q '"status": *"success"'; then
                ((successful_agents++))
            elif echo "$line" | grep -q '"status": *"failure"'; then
                ((failed_agents++))
            fi

            # Extract duration
            local duration=$(echo "$line" | grep -o '"duration_seconds": *[0-9.]*' | grep -o '[0-9.]*' || echo "0")
            total_duration=$(echo "$total_duration + $duration" | bc 2>/dev/null || echo "$total_duration")
        fi
    done < "$AGENT_INVOCATIONS"

    # Calculate workflow duration
    local workflow_duration=0
    if [[ -n "$start_time" ]]; then
        local end_time=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
        local start_epoch=$(date -u -d "$start_time" +%s 2>/dev/null || date -u -j -f "%Y-%m-%dT%H:%M:%SZ" "$start_time" +%s 2>/dev/null || echo "0")
        local end_epoch=$(date -u +%s)
        workflow_duration=$((end_epoch - start_epoch))
    fi

    # Calculate average duration
    local avg_duration=0
    if [[ $total_agents -gt 0 ]]; then
        avg_duration=$(echo "scale=2; $total_duration / $total_agents" | bc 2>/dev/null || echo "0")
    fi

    # Build statistics JSON
    local stats=$(cat <<EOF
{
  "total_agents": $total_agents,
  "successful_agents": $successful_agents,
  "failed_agents": $failed_agents,
  "total_duration_seconds": $total_duration,
  "workflow_duration_seconds": $workflow_duration,
  "average_agent_duration_seconds": $avg_duration
}
EOF
)

    echo "$stats"
}

# Clean up workflow state
cleanup_workflow_state() {
    local temp_file="/tmp/oak_workflow_${WORKFLOW_ID}.env"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${BLUE}[DRY RUN]${NC} Would clean up: $temp_file"
        return
    fi

    if [[ -f "$temp_file" ]]; then
        rm -f "$temp_file"
        echo -e "${GREEN}✓ Cleaned up workflow state${NC}" >&2
    fi

    # Unset environment variables
    unset OAK_WORKFLOW_ID
    unset OAK_WORKFLOW_START_TIME
    unset OAK_WORKFLOW_DESC
}

# Trigger notifications
trigger_notifications() {
    local stats="$1"

    if [[ "${OAK_NOTIFY_ENABLED:-false}" != "true" ]]; then
        return
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${BLUE}[DRY RUN]${NC} Would send notification for workflow $WORKFLOW_ID"
        return
    fi

    # Check if notification script exists
    local notify_script="$PROJECT_ROOT/automation/oak_notify.sh"
    if [[ -x "$notify_script" ]]; then
        echo -e "${CYAN}→${NC} Sending notification..." >&2
        "$notify_script" "workflow_complete" "$WORKFLOW_ID" "$STATUS" "$stats" 2>/dev/null || true
    fi
}

# Format duration for display
format_duration() {
    local seconds=$1

    if [[ $seconds -lt 60 ]]; then
        echo "${seconds}s"
    elif [[ $seconds -lt 3600 ]]; then
        local minutes=$((seconds / 60))
        local secs=$((seconds % 60))
        echo "${minutes}m ${secs}s"
    else
        local hours=$((seconds / 3600))
        local minutes=$(((seconds % 3600) / 60))
        echo "${hours}h ${minutes}m"
    fi
}

# Display workflow summary
display_summary() {
    local stats="$1"

    # Parse statistics
    local total_agents=$(echo "$stats" | grep -o '"total_agents": *[0-9]*' | grep -o '[0-9]*' || echo "0")
    local successful=$(echo "$stats" | grep -o '"successful_agents": *[0-9]*' | grep -o '[0-9]*' || echo "0")
    local failed=$(echo "$stats" | grep -o '"failed_agents": *[0-9]*' | grep -o '[0-9]*' || echo "0")
    local workflow_duration=$(echo "$stats" | grep -o '"workflow_duration_seconds": *[0-9]*' | grep -o '[0-9]*' || echo "0")

    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════${NC}"
    echo -e "${CYAN}  Workflow Summary${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════${NC}"
    echo ""
    echo "Workflow ID: $WORKFLOW_ID"
    echo "Status: $(
        if [[ "$STATUS" == "success" ]]; then
            echo -e "${GREEN}Success${NC}"
        elif [[ "$STATUS" == "failure" ]]; then
            echo -e "${RED}Failed${NC}"
        else
            echo -e "${YELLOW}Partial${NC}"
        fi
    )"
    echo ""
    echo "Agents Executed: $total_agents"
    echo "  Successful: ${GREEN}$successful${NC}"
    if [[ $failed -gt 0 ]]; then
        echo "  Failed: ${RED}$failed${NC}"
    fi
    echo ""
    echo "Total Duration: $(format_duration $workflow_duration)"
    echo ""
}

# Main execution
main() {
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Post-Workflow Hook${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo ""
    echo "Workflow ID: $WORKFLOW_ID"
    echo "Status: $STATUS"
    echo ""

    # Calculate statistics
    echo -e "${BLUE}→${NC} Calculating workflow statistics..."
    local stats=$(calculate_statistics)
    echo -e "${GREEN}✓ Statistics calculated${NC}"

    # Display summary
    display_summary "$stats"

    # Log completion
    echo -e "${BLUE}→${NC} Logging workflow completion..."
    log_event "workflow_complete" "$STATUS" "Workflow completed with status: $STATUS" "$stats"
    echo -e "${GREEN}✓ Completion logged${NC}"

    # Clean up state
    echo -e "${BLUE}→${NC} Cleaning up workflow state..."
    cleanup_workflow_state

    # Trigger notifications
    if [[ "${OAK_NOTIFY_ENABLED:-false}" == "true" ]]; then
        trigger_notifications "$stats"
    fi

    echo ""
    echo -e "${GREEN}✓ Workflow post-processing complete${NC}"
    echo ""
}

# Run main if not sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
