#!/bin/bash
# workflow_state_manager.sh - Manage workflow state for git enforcement
# Handles state initialization, updates, verification, and recovery

set -e

# Configuration
WORKFLOW_STATE=".workflow_state"
WORKFLOW_ARCHIVE=".workflow_archive"
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Commands
CMD_INIT="init"
CMD_UPDATE="update"
CMD_VERIFY="verify"
CMD_RESET="reset"
CMD_STATUS="status"
CMD_RECOVER="recover"

usage() {
    cat <<EOF
Usage: $0 [COMMAND] [OPTIONS]

Commands:
    init        Initialize workflow state for new work
    update      Update workflow phase and status
    verify      Verify code hasn't changed since quality gate
    reset       Reset workflow state (clears all)
    status      Show current workflow status
    recover     Attempt to recover from corrupted state

Options:
    -p, --phase PHASE      Set workflow phase (IMPLEMENTATION|QUALITY_GATE|GIT_OPERATIONS)
    -s, --status STATUS    Set status (IN_PROGRESS|COMPLETED|FAILED)
    -h, --help            Show this help message

Examples:
    $0 init                           # Start new workflow
    $0 update -p QUALITY_GATE -s IN_PROGRESS
    $0 verify                         # Check if code changed
    $0 status                         # View current state
EOF
}

log() {
    echo -e "${GREEN}[STATE]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Calculate hash of staged changes
calculate_hash() {
    if [ -n "$(git diff --cached)" ]; then
        git diff --cached | sha256sum | cut -d' ' -f1
    else
        echo "NO_STAGED_CHANGES"
    fi
}

# Initialize workflow state
init_workflow() {
    log "Initializing workflow state..."

    if [ -f "$WORKFLOW_STATE" ]; then
        warning "Existing workflow state found. Archiving..."
        archive_state
    fi

    local hash=$(calculate_hash)
    cat > "$WORKFLOW_STATE" <<EOF
PHASE=IMPLEMENTATION
STATUS=IN_PROGRESS
QUALITY_GATE_PASSED=false
HASH=$hash
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
INITIALIZED_BY=$USER
INITIALIZED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF

    log "Workflow state initialized"
    info "Phase: IMPLEMENTATION"
    info "Status: IN_PROGRESS"
}

# Update workflow state
update_workflow() {
    local phase=""
    local status=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -p|--phase)
                phase="$2"
                shift 2
                ;;
            -s|--status)
                status="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done

    if [ ! -f "$WORKFLOW_STATE" ]; then
        error "No workflow state found. Run '$0 init' first."
        exit 1
    fi

    # Read current state
    source "$WORKFLOW_STATE"

    # Update specified fields
    if [ -n "$phase" ]; then
        PHASE="$phase"
        log "Updated phase to: $phase"
    fi

    if [ -n "$status" ]; then
        STATUS="$status"
        log "Updated status to: $status"
    fi

    # Recalculate hash if moving to quality gate
    if [ "$phase" = "QUALITY_GATE" ] && [ "$status" = "IN_PROGRESS" ]; then
        HASH=$(calculate_hash)
        log "Updated code hash for quality gate"
    fi

    # Write updated state
    cat > "$WORKFLOW_STATE" <<EOF
PHASE=$PHASE
STATUS=$STATUS
QUALITY_GATE_PASSED=$QUALITY_GATE_PASSED
HASH=$HASH
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
INITIALIZED_BY=$INITIALIZED_BY
INITIALIZED_AT=$INITIALIZED_AT
LAST_UPDATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF

    log "Workflow state updated"
}

# Verify code hasn't changed
verify_workflow() {
    if [ ! -f "$WORKFLOW_STATE" ]; then
        error "No workflow state found"
        exit 1
    fi

    source "$WORKFLOW_STATE"
    local current_hash=$(calculate_hash)

    if [ "$current_hash" = "$HASH" ]; then
        log "✅ Code verification passed - no changes since quality gate"
        return 0
    else
        error "❌ Code verification failed - changes detected since quality gate"
        warning "Expected hash: $HASH"
        warning "Current hash: $current_hash"
        warning "Run quality gate again before committing"
        return 1
    fi
}

# Reset workflow state
reset_workflow() {
    if [ -f "$WORKFLOW_STATE" ]; then
        log "Resetting workflow state..."
        archive_state
        rm -f "$WORKFLOW_STATE"
        log "Workflow state reset"
    else
        info "No workflow state to reset"
    fi
}

# Show workflow status
show_status() {
    if [ ! -f "$WORKFLOW_STATE" ]; then
        info "No active workflow"
        return
    fi

    source "$WORKFLOW_STATE"

    echo ""
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo -e "${BLUE}       Workflow Status Report          ${NC}"
    echo -e "${BLUE}═══════════════════════════════════════${NC}"
    echo ""

    # Phase indicator
    case $PHASE in
        IMPLEMENTATION)
            echo -e "Phase:    ${YELLOW}[1/3] IMPLEMENTATION${NC}"
            ;;
        QUALITY_GATE)
            echo -e "Phase:    ${YELLOW}[2/3] QUALITY_GATE${NC}"
            ;;
        GIT_OPERATIONS)
            echo -e "Phase:    ${YELLOW}[3/3] GIT_OPERATIONS${NC}"
            ;;
        *)
            echo -e "Phase:    ${RED}UNKNOWN: $PHASE${NC}"
            ;;
    esac

    # Status indicator
    case $STATUS in
        IN_PROGRESS)
            echo -e "Status:   ${YELLOW}⏳ IN_PROGRESS${NC}"
            ;;
        COMPLETED)
            echo -e "Status:   ${GREEN}✅ COMPLETED${NC}"
            ;;
        FAILED)
            echo -e "Status:   ${RED}❌ FAILED${NC}"
            ;;
        *)
            echo -e "Status:   ${RED}UNKNOWN: $STATUS${NC}"
            ;;
    esac

    # Quality gate status
    if [ "$QUALITY_GATE_PASSED" = "true" ]; then
        echo -e "Quality:  ${GREEN}✅ PASSED${NC}"
    else
        echo -e "Quality:  ${YELLOW}⏸ PENDING${NC}"
    fi

    echo ""
    echo "Details:"
    echo "  Initialized: $INITIALIZED_AT"
    echo "  By user:     $INITIALIZED_BY"
    echo "  Last update: ${LAST_UPDATE:-$TIMESTAMP}"
    echo "  Code hash:   ${HASH:0:8}..."
    echo ""

    # Next steps suggestion
    echo "Next steps:"
    case "$PHASE:$STATUS" in
        "IMPLEMENTATION:IN_PROGRESS")
            echo "  → Complete implementation work"
            echo "  → Run: quality_gate_validator.sh"
            ;;
        "IMPLEMENTATION:COMPLETED")
            echo "  → Run: quality_gate_validator.sh"
            ;;
        "QUALITY_GATE:IN_PROGRESS")
            echo "  → Quality gate validation in progress..."
            ;;
        "QUALITY_GATE:COMPLETED")
            if [ "$QUALITY_GATE_PASSED" = "true" ]; then
                echo "  → Ready to commit!"
                echo "  → Run: git commit -m 'Your message'"
            else
                echo "  → Quality gate failed"
                echo "  → Fix issues and re-run validation"
            fi
            ;;
        "QUALITY_GATE:FAILED")
            echo "  → Fix quality issues"
            echo "  → Run: quality_gate_validator.sh"
            ;;
        "GIT_OPERATIONS:IN_PROGRESS")
            echo "  → Git operations in progress..."
            ;;
        "GIT_OPERATIONS:COMPLETED")
            echo "  → Workflow complete!"
            echo "  → Run: $0 reset"
            ;;
    esac
    echo ""
}

# Archive current state
archive_state() {
    if [ ! -f "$WORKFLOW_STATE" ]; then
        return
    fi

    mkdir -p "$WORKFLOW_ARCHIVE"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    cp "$WORKFLOW_STATE" "$WORKFLOW_ARCHIVE/workflow_state_${timestamp}.bak"
    info "State archived to: $WORKFLOW_ARCHIVE/workflow_state_${timestamp}.bak"
}

# Recover from corrupted state
recover_workflow() {
    log "Attempting to recover workflow state..."

    # Check for archived states
    if [ -d "$WORKFLOW_ARCHIVE" ]; then
        local latest=$(ls -t "$WORKFLOW_ARCHIVE"/workflow_state_*.bak 2>/dev/null | head -1)
        if [ -n "$latest" ]; then
            warning "Found archived state: $latest"
            read -p "Restore from this backup? (y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                cp "$latest" "$WORKFLOW_STATE"
                log "State recovered from backup"
                show_status
                return 0
            fi
        fi
    fi

    # Check git status for clues
    if [ -n "$(git diff --cached)" ]; then
        warning "Found staged changes. Initializing fresh state..."
        init_workflow
        update_workflow -p QUALITY_GATE -s IN_PROGRESS
        log "Created new state based on staged changes"
    else
        info "No staged changes found. Starting fresh..."
        init_workflow
    fi
}

# Main command dispatcher
main() {
    if [ $# -eq 0 ]; then
        usage
        exit 1
    fi

    case "$1" in
        $CMD_INIT)
            init_workflow
            ;;
        $CMD_UPDATE)
            shift
            update_workflow "$@"
            ;;
        $CMD_VERIFY)
            verify_workflow
            ;;
        $CMD_RESET)
            reset_workflow
            ;;
        $CMD_STATUS)
            show_status
            ;;
        $CMD_RECOVER)
            recover_workflow
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            error "Unknown command: $1"
            usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@"