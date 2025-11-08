#!/bin/bash
"""
On-Spec-Change Hook - Execute when spec files change

This hook runs when specification files are modified to:
- Detect which spec changed
- Log change reason
- Regenerate YAML if Markdown changed
- Notify related workflows
- Track spec evolution

Usage:
    on_spec_change.sh <spec_file> <change_type> [reason] [--dry-run]

Arguments:
    spec_file     Path to spec file that changed
    change_type   created|modified|deleted|completed
    reason        Optional reason for change

Environment Variables:
    OAK_SPECS_DIR: Specs directory (default: PROJECT_ROOT/specs)
    OAK_SPEC_TRACKING_ENABLED: Enable spec change tracking (default: true)

Exit Codes:
    0: Success
    1: Error during processing
"""

set -e

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SPECS_DIR="${OAK_SPECS_DIR:-$PROJECT_ROOT/specs}"
TELEMETRY_DIR="${OAK_TELEMETRY_DIR:-$PROJECT_ROOT/telemetry}"
SPEC_CHANGES_LOG="$TELEMETRY_DIR/spec_changes.jsonl"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Parse arguments
SPEC_FILE="${1:-}"
CHANGE_TYPE="${2:-modified}"
REASON="${3:-Manual change}"
DRY_RUN=false

if [[ "$4" == "--dry-run" ]] || [[ "$3" == "--dry-run" ]]; then
    DRY_RUN=true
    if [[ "$3" == "--dry-run" ]]; then
        REASON="Manual change"
    fi
fi

# Show help
if [[ "$1" == "--help" || -z "$SPEC_FILE" ]]; then
    echo "Usage: on_spec_change.sh <spec_file> <change_type> [reason] [--dry-run]"
    echo ""
    echo "Arguments:"
    echo "  spec_file     Path to spec file"
    echo "  change_type   created|modified|deleted|completed"
    echo "  reason        Optional reason for change"
    echo ""
    echo "Options:"
    echo "  --dry-run     Run without logging or regeneration"
    echo "  --help        Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  OAK_SPECS_DIR              Specs directory"
    echo "  OAK_SPEC_TRACKING_ENABLED  Enable tracking (default: true)"
    exit 0
fi

# Check if spec tracking is enabled
if [[ "${OAK_SPEC_TRACKING_ENABLED:-true}" != "true" ]]; then
    echo -e "${YELLOW}Spec tracking disabled${NC}" >&2
    exit 0
fi

# Ensure directories exist
mkdir -p "$TELEMETRY_DIR"

# Normalize spec file path
SPEC_FILE=$(realpath "$SPEC_FILE" 2>/dev/null || echo "$SPEC_FILE")

# Extract spec info
extract_spec_info() {
    local spec_file="$1"

    # Get basename
    local basename=$(basename "$spec_file")

    # Extract spec ID from filename (YYYY-MM-DD-name.md -> spec-YYYYMMDD-name)
    local spec_id=""
    if [[ "$basename" =~ ^([0-9]{4})-([0-9]{2})-([0-9]{2})-(.+)\.(md|yaml)$ ]]; then
        local year="${BASH_REMATCH[1]}"
        local month="${BASH_REMATCH[2]}"
        local day="${BASH_REMATCH[3]}"
        local name="${BASH_REMATCH[4]}"
        spec_id="spec-${year}${month}${day}-${name}"
    else
        spec_id="spec-unknown-$(echo "$basename" | sed 's/\.[^.]*$//')"
    fi

    # Determine status from directory
    local status="unknown"
    if [[ "$spec_file" == *"/active/"* ]]; then
        status="active"
    elif [[ "$spec_file" == *"/completed/"* ]]; then
        status="completed"
    elif [[ "$spec_file" == *"/archived/"* ]]; then
        status="archived"
    fi

    # Get file type
    local file_type="${spec_file##*.}"

    echo "$spec_id|$status|$file_type|$basename"
}

# Log spec change
log_spec_change() {
    local spec_id="$1"
    local status="$2"
    local file_type="$3"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${BLUE}[DRY RUN]${NC} Would log spec change: $spec_id"
        return
    fi

    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Get workflow context if available
    local workflow_context=""
    if [[ -n "${OAK_WORKFLOW_ID:-}" ]]; then
        workflow_context=", \"workflow_id\": \"$OAK_WORKFLOW_ID\""
    fi

    local change_record=$(cat <<EOF
{
  "timestamp": "$timestamp",
  "spec_id": "$spec_id",
  "spec_file": "$SPEC_FILE",
  "file_type": "$file_type",
  "change_type": "$CHANGE_TYPE",
  "status": "$status",
  "reason": $(echo "$REASON" | jq -R . 2>/dev/null || echo "\"$REASON\"")$workflow_context
}
EOF
)

    echo "$change_record" >> "$SPEC_CHANGES_LOG"
    echo -e "${GREEN}✓ Spec change logged${NC}" >&2
}

# Regenerate YAML from Markdown
regenerate_yaml() {
    local spec_file="$1"
    local file_type="$2"

    # Only regenerate if Markdown file changed
    if [[ "$file_type" != "md" ]]; then
        return
    fi

    # Get corresponding YAML file
    local yaml_file="${spec_file%.md}.yaml"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${BLUE}[DRY RUN]${NC} Would regenerate: $yaml_file"
        return
    fi

    # Check if YAML generator tool exists
    local generator="$SPECS_DIR/tools/generate_yaml.py"
    if [[ ! -x "$generator" ]]; then
        echo -e "${YELLOW}⚠ YAML generator not found, skipping regeneration${NC}" >&2
        return
    fi

    echo -e "${CYAN}→${NC} Regenerating YAML from Markdown..." >&2

    if "$generator" "$spec_file" > "$yaml_file" 2>&1; then
        echo -e "${GREEN}✓ YAML regenerated: $yaml_file${NC}" >&2
    else
        echo -e "${YELLOW}⚠ YAML regeneration failed${NC}" >&2
    fi
}

# Notify related workflows
notify_workflows() {
    local spec_id="$1"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${BLUE}[DRY RUN]${NC} Would notify workflows using spec: $spec_id"
        return
    fi

    # Find active invocations using this spec
    local invocations_file="$TELEMETRY_DIR/agent_invocations.jsonl"
    if [[ ! -f "$invocations_file" ]]; then
        return
    fi

    # Search for invocations with this spec_id in last 24 hours
    local cutoff=$(date -u -d '24 hours ago' +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-24H +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || echo "")

    local affected_workflows=()

    while IFS= read -r line; do
        if [[ -z "$line" ]]; then
            continue
        fi

        # Check if this invocation uses our spec
        if echo "$line" | grep -q "\"spec_id\": *\"$spec_id\""; then
            # Extract workflow_id
            local workflow_id=$(echo "$line" | grep -o '"workflow_id": *"[^"]*"' | cut -d'"' -f4)
            if [[ -n "$workflow_id" ]] && [[ ! " ${affected_workflows[@]} " =~ " ${workflow_id} " ]]; then
                affected_workflows+=("$workflow_id")
            fi
        fi
    done < "$invocations_file"

    if [[ ${#affected_workflows[@]} -gt 0 ]]; then
        echo -e "${CYAN}→${NC} Spec change affects ${#affected_workflows[@]} active workflow(s)" >&2
        for wf_id in "${affected_workflows[@]}"; do
            echo -e "  ${CYAN}•${NC} $wf_id" >&2
        done
    fi
}

# Track spec evolution
track_evolution() {
    local spec_id="$1"
    local change_type="$2"

    if [[ ! -f "$SPEC_CHANGES_LOG" ]]; then
        return
    fi

    # Count changes for this spec
    local change_count=$(grep "\"spec_id\": *\"$spec_id\"" "$SPEC_CHANGES_LOG" 2>/dev/null | wc -l | tr -d ' ')

    if [[ $change_count -gt 5 ]]; then
        echo -e "${YELLOW}⚠ Note: Spec has been modified $change_count times${NC}" >&2
        echo -e "${YELLOW}  Consider reviewing if spec requirements are stable${NC}" >&2
    fi
}

# Display change summary
display_summary() {
    local spec_id="$1"
    local status="$2"
    local file_type="$3"

    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════${NC}"
    echo -e "${CYAN}  Spec Change Detected${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════${NC}"
    echo ""
    echo "Spec ID: $spec_id"
    echo "File: $(basename "$SPEC_FILE")"
    echo "Type: $file_type"
    echo "Status: $status"
    echo "Change: $CHANGE_TYPE"
    echo "Reason: $REASON"
    echo ""
}

# Main execution
main() {
    # Extract spec info
    local spec_info=$(extract_spec_info "$SPEC_FILE")
    IFS='|' read -r spec_id status file_type basename <<< "$spec_info"

    # Display summary
    display_summary "$spec_id" "$status" "$file_type"

    # Log change
    echo -e "${BLUE}→${NC} Logging spec change..." >&2
    log_spec_change "$spec_id" "$status" "$file_type"

    # Regenerate YAML if needed
    if [[ "$file_type" == "md" ]] && [[ "$CHANGE_TYPE" != "deleted" ]]; then
        regenerate_yaml "$SPEC_FILE" "$file_type"
    fi

    # Notify related workflows
    echo -e "${BLUE}→${NC} Checking for affected workflows..." >&2
    notify_workflows "$spec_id"

    # Track evolution
    track_evolution "$spec_id" "$CHANGE_TYPE"

    echo ""
    echo -e "${GREEN}✓ Spec change processing complete${NC}"
    echo ""
}

# Run main if not sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
