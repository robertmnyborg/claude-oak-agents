#!/bin/bash
"""
Pre-Workflow Hook - Execute before workflow starts

This hook runs at the beginning of a multi-agent workflow to:
- Log workflow initiation
- Validate preconditions
- Set workflow environment variables
- Check for conflicts with existing workflows

Usage:
    pre_workflow.sh <workflow_id> <workflow_description> [--dry-run]

Environment Variables:
    OAK_TELEMETRY_DIR: Directory for telemetry logs
    OAK_WORKFLOW_ENABLED: Set to "false" to disable workflow tracking

Exit Codes:
    0: Success
    1: Validation failed
    2: Conflict detected
"""

set -e

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TELEMETRY_DIR="${OAK_TELEMETRY_DIR:-$PROJECT_ROOT/telemetry}"
WORKFLOW_EVENTS="$TELEMETRY_DIR/workflow_events.jsonl"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
WORKFLOW_ID="${1:-}"
WORKFLOW_DESC="${2:-}"
DRY_RUN=false

if [[ "$3" == "--dry-run" ]]; then
    DRY_RUN=true
fi

# Show help
if [[ "$1" == "--help" || -z "$WORKFLOW_ID" ]]; then
    echo "Usage: pre_workflow.sh <workflow_id> <workflow_description> [--dry-run]"
    echo ""
    echo "Options:"
    echo "  --dry-run    Run validation without logging"
    echo "  --help       Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  OAK_TELEMETRY_DIR       Telemetry directory (default: PROJECT_ROOT/telemetry)"
    echo "  OAK_WORKFLOW_ENABLED    Enable/disable workflow tracking (default: true)"
    exit 0
fi

# Check if workflow tracking is enabled
if [[ "${OAK_WORKFLOW_ENABLED:-true}" != "true" ]]; then
    echo -e "${YELLOW}Workflow tracking disabled${NC}" >&2
    exit 0
fi

# Ensure telemetry directory exists
mkdir -p "$TELEMETRY_DIR"

# Log function
log_event() {
    local event_type="$1"
    local status="$2"
    local message="$3"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${BLUE}[DRY RUN]${NC} Would log: $event_type - $status - $message"
        return
    fi

    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%SZ")
    local event=$(cat <<EOF
{"timestamp": "$timestamp", "event_type": "$event_type", "workflow_id": "$WORKFLOW_ID", "status": "$status", "message": "$message", "description": "$WORKFLOW_DESC"}
EOF
)
    echo "$event" >> "$WORKFLOW_EVENTS"
}

# Validate preconditions
validate_preconditions() {
    local errors=0

    # Check if telemetry directory is writable
    if [[ ! -w "$TELEMETRY_DIR" ]]; then
        echo -e "${RED}✗ Telemetry directory not writable: $TELEMETRY_DIR${NC}" >&2
        ((errors++))
    fi

    # Check if workflow ID is valid format (wf-YYYYMMDD-*)
    if [[ ! "$WORKFLOW_ID" =~ ^wf-[0-9]{8}- ]]; then
        echo -e "${YELLOW}⚠ Warning: Workflow ID doesn't match expected format (wf-YYYYMMDD-*)${NC}" >&2
    fi

    return $errors
}

# Check for workflow conflicts
check_conflicts() {
    if [[ ! -f "$WORKFLOW_EVENTS" ]]; then
        return 0
    fi

    # Check for workflows started in last hour that haven't completed
    local cutoff=$(date -u -d '1 hour ago' +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-1H +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || echo "")

    if [[ -z "$cutoff" ]]; then
        # Can't determine cutoff, skip conflict check
        return 0
    fi

    local active_workflows=0

    while IFS= read -r line; do
        if [[ -z "$line" ]]; then
            continue
        fi

        # Parse JSON (basic extraction)
        local timestamp=$(echo "$line" | grep -o '"timestamp": *"[^"]*"' | cut -d'"' -f4)
        local event_type=$(echo "$line" | grep -o '"event_type": *"[^"]*"' | cut -d'"' -f4)

        # Skip if older than cutoff
        if [[ "$timestamp" < "$cutoff" ]]; then
            continue
        fi

        # Count workflow_start events
        if [[ "$event_type" == "workflow_start" ]]; then
            ((active_workflows++))
        fi
    done < "$WORKFLOW_EVENTS"

    if [[ $active_workflows -gt 5 ]]; then
        echo -e "${YELLOW}⚠ Warning: $active_workflows workflows started in last hour${NC}" >&2
        echo -e "${YELLOW}  Consider completing active workflows before starting new ones${NC}" >&2
    fi

    return 0
}

# Set workflow environment variables
set_environment() {
    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${BLUE}[DRY RUN]${NC} Would set environment variables:"
        echo "  OAK_WORKFLOW_ID=$WORKFLOW_ID"
        echo "  OAK_WORKFLOW_START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
        return
    fi

    export OAK_WORKFLOW_ID="$WORKFLOW_ID"
    export OAK_WORKFLOW_START_TIME="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

    # Save to temp file for other hooks to access
    local temp_file="/tmp/oak_workflow_${WORKFLOW_ID}.env"
    cat > "$temp_file" <<EOF
OAK_WORKFLOW_ID=$WORKFLOW_ID
OAK_WORKFLOW_START_TIME=$OAK_WORKFLOW_START_TIME
OAK_WORKFLOW_DESC=$WORKFLOW_DESC
EOF

    echo -e "${GREEN}✓ Workflow environment set${NC}" >&2
}

# Main execution
main() {
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Pre-Workflow Hook${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo ""
    echo "Workflow ID: $WORKFLOW_ID"
    echo "Description: $WORKFLOW_DESC"
    echo ""

    # Validate preconditions
    echo -e "${BLUE}→${NC} Validating preconditions..."
    if ! validate_preconditions; then
        log_event "workflow_start" "validation_failed" "Precondition validation failed"
        echo -e "${RED}✗ Validation failed${NC}" >&2
        exit 1
    fi
    echo -e "${GREEN}✓ Preconditions valid${NC}"

    # Check for conflicts
    echo -e "${BLUE}→${NC} Checking for conflicts..."
    if ! check_conflicts; then
        log_event "workflow_start" "conflict_detected" "Conflicting workflows detected"
        echo -e "${RED}✗ Conflicts detected${NC}" >&2
        exit 2
    fi
    echo -e "${GREEN}✓ No conflicts${NC}"

    # Set environment variables
    echo -e "${BLUE}→${NC} Setting workflow environment..."
    set_environment

    # Log workflow start
    log_event "workflow_start" "success" "Workflow initiated successfully"
    echo -e "${GREEN}✓ Workflow started${NC}"
    echo ""
}

# Run main if not sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
