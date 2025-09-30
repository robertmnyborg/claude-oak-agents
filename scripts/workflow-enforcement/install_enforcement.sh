#!/bin/bash
# install_enforcement.sh - Install workflow enforcement system
# Sets up git hooks, directories, and initial state

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
GIT_HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
WORKFLOW_SCRIPTS_DIR="$PROJECT_ROOT/scripts/workflow-enforcement"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Installation modes
MODE_INSTALL="install"
MODE_UNINSTALL="uninstall"
MODE_STATUS="status"

log() {
    echo -e "${GREEN}[INSTALLER]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}✅${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."

    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        error "Not in a git repository"
        echo "  Please run this script from within a git repository"
        exit 1
    fi

    # Check if scripts exist
    local required_scripts=(
        "quality_gate_validator.sh"
        "workflow_state_manager.sh"
        "git-hooks/pre-commit"
        "git-hooks/post-commit"
    )

    for script in "${required_scripts[@]}"; do
        if [ ! -f "$SCRIPT_DIR/$script" ]; then
            error "Required script not found: $script"
            echo "  Please ensure all workflow scripts are present"
            exit 1
        fi
    done

    success "Prerequisites check passed"
}

# Backup existing hooks
backup_hooks() {
    log "Backing up existing git hooks..."

    local backup_dir="$GIT_HOOKS_DIR/backup_$(date +%Y%m%d_%H%M%S)"
    local backed_up=false

    for hook in pre-commit post-commit; do
        if [ -f "$GIT_HOOKS_DIR/$hook" ]; then
            if [ ! -d "$backup_dir" ]; then
                mkdir -p "$backup_dir"
            fi
            cp "$GIT_HOOKS_DIR/$hook" "$backup_dir/$hook"
            info "Backed up: $hook → $backup_dir/$hook"
            backed_up=true
        fi
    done

    if [ "$backed_up" = true ]; then
        success "Existing hooks backed up to: $backup_dir"
    else
        info "No existing hooks to backup"
    fi
}

# Install git hooks
install_hooks() {
    log "Installing git hooks..."

    # Install pre-commit hook
    cp "$SCRIPT_DIR/git-hooks/pre-commit" "$GIT_HOOKS_DIR/pre-commit"
    chmod +x "$GIT_HOOKS_DIR/pre-commit"
    success "Installed pre-commit hook"

    # Install post-commit hook
    cp "$SCRIPT_DIR/git-hooks/post-commit" "$GIT_HOOKS_DIR/post-commit"
    chmod +x "$GIT_HOOKS_DIR/post-commit"
    success "Installed post-commit hook"
}

# Make scripts executable
make_executable() {
    log "Setting script permissions..."

    chmod +x "$SCRIPT_DIR/quality_gate_validator.sh"
    chmod +x "$SCRIPT_DIR/workflow_state_manager.sh"
    chmod +x "$SCRIPT_DIR/git-hooks/pre-commit"
    chmod +x "$SCRIPT_DIR/git-hooks/post-commit"

    success "Scripts made executable"
}

# Create necessary directories
create_directories() {
    log "Creating necessary directories..."

    # Create workflow archive directory
    mkdir -p "$PROJECT_ROOT/.workflow_archive"
    success "Created .workflow_archive directory"

    # Add to .gitignore if not already there
    if [ -f "$PROJECT_ROOT/.gitignore" ]; then
        if ! grep -q "^.workflow_state" "$PROJECT_ROOT/.gitignore"; then
            echo ".workflow_state" >> "$PROJECT_ROOT/.gitignore"
            info "Added .workflow_state to .gitignore"
        fi
        if ! grep -q "^.workflow_archive" "$PROJECT_ROOT/.gitignore"; then
            echo ".workflow_archive/" >> "$PROJECT_ROOT/.gitignore"
            info "Added .workflow_archive/ to .gitignore"
        fi
        if ! grep -q "^.workflow_bypass" "$PROJECT_ROOT/.gitignore"; then
            echo ".workflow_bypass" >> "$PROJECT_ROOT/.gitignore"
            info "Added .workflow_bypass to .gitignore"
        fi
        if ! grep -q "^.workflow_bypass_log" "$PROJECT_ROOT/.gitignore"; then
            echo ".workflow_bypass_log" >> "$PROJECT_ROOT/.gitignore"
            info "Added .workflow_bypass_log to .gitignore"
        fi
    fi
}

# Install workflow enforcement
install_enforcement() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}     Workflow Enforcement Installation             ${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
    echo ""

    check_prerequisites
    backup_hooks
    install_hooks
    make_executable
    create_directories

    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}     ✅ Installation Complete!                     ${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
    echo ""
    echo "The workflow enforcement system is now active."
    echo ""
    echo "Usage:"
    echo "  1. Start work:     $WORKFLOW_SCRIPTS_DIR/workflow_state_manager.sh init"
    echo "  2. Stage changes:  git add <files>"
    echo "  3. Run quality:    $WORKFLOW_SCRIPTS_DIR/quality_gate_validator.sh"
    echo "  4. Commit:         git commit -m 'Your message'"
    echo ""
    echo "Commands:"
    echo "  • Check status:    $WORKFLOW_SCRIPTS_DIR/workflow_state_manager.sh status"
    echo "  • Reset workflow:  $WORKFLOW_SCRIPTS_DIR/workflow_state_manager.sh reset"
    echo "  • Uninstall:       $0 uninstall"
    echo ""
}

# Uninstall workflow enforcement
uninstall_enforcement() {
    echo ""
    echo -e "${YELLOW}═══════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}     Workflow Enforcement Uninstallation           ${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════${NC}"
    echo ""

    read -p "Are you sure you want to uninstall the workflow enforcement? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        info "Uninstallation cancelled"
        exit 0
    fi

    log "Removing git hooks..."

    # Remove hooks
    if [ -f "$GIT_HOOKS_DIR/pre-commit" ]; then
        rm "$GIT_HOOKS_DIR/pre-commit"
        success "Removed pre-commit hook"
    fi

    if [ -f "$GIT_HOOKS_DIR/post-commit" ]; then
        rm "$GIT_HOOKS_DIR/post-commit"
        success "Removed post-commit hook"
    fi

    # Clean up state files
    if [ -f "$PROJECT_ROOT/.workflow_state" ]; then
        rm "$PROJECT_ROOT/.workflow_state"
        success "Removed workflow state"
    fi

    # Ask about archive
    if [ -d "$PROJECT_ROOT/.workflow_archive" ]; then
        read -p "Remove workflow archives? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$PROJECT_ROOT/.workflow_archive"
            success "Removed workflow archives"
        fi
    fi

    # Check for backups
    if ls "$GIT_HOOKS_DIR"/backup_* 1> /dev/null 2>&1; then
        echo ""
        warning "Backup hooks found in: $GIT_HOOKS_DIR/backup_*"
        echo "  To restore: cp $GIT_HOOKS_DIR/backup_*/pre-commit $GIT_HOOKS_DIR/"
    fi

    echo ""
    success "Workflow enforcement uninstalled"
    echo ""
}

# Show status
show_status() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}     Workflow Enforcement Status                   ${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo ""

    # Check hooks
    echo "Git Hooks:"
    if [ -f "$GIT_HOOKS_DIR/pre-commit" ]; then
        if grep -q "workflow" "$GIT_HOOKS_DIR/pre-commit"; then
            echo -e "  pre-commit:  ${GREEN}✅ Installed${NC}"
        else
            echo -e "  pre-commit:  ${YELLOW}⚠️  Different hook installed${NC}"
        fi
    else
        echo -e "  pre-commit:  ${RED}❌ Not installed${NC}"
    fi

    if [ -f "$GIT_HOOKS_DIR/post-commit" ]; then
        if grep -q "workflow" "$GIT_HOOKS_DIR/post-commit"; then
            echo -e "  post-commit: ${GREEN}✅ Installed${NC}"
        else
            echo -e "  post-commit: ${YELLOW}⚠️  Different hook installed${NC}"
        fi
    else
        echo -e "  post-commit: ${RED}❌ Not installed${NC}"
    fi

    # Check scripts
    echo ""
    echo "Workflow Scripts:"
    local scripts=(
        "quality_gate_validator.sh"
        "workflow_state_manager.sh"
    )

    for script in "${scripts[@]}"; do
        if [ -f "$WORKFLOW_SCRIPTS_DIR/$script" ] && [ -x "$WORKFLOW_SCRIPTS_DIR/$script" ]; then
            echo -e "  $script: ${GREEN}✅ Available${NC}"
        else
            echo -e "  $script: ${RED}❌ Not found or not executable${NC}"
        fi
    done

    # Check current workflow state
    echo ""
    if [ -f "$PROJECT_ROOT/.workflow_state" ]; then
        echo "Current Workflow:"
        "$WORKFLOW_SCRIPTS_DIR/workflow_state_manager.sh" status 2>/dev/null || echo "  Unable to read state"
    else
        echo "Current Workflow: None active"
    fi

    echo ""
}

# Show usage
usage() {
    cat <<EOF
Usage: $0 [COMMAND]

Commands:
    install     Install workflow enforcement system (default)
    uninstall   Remove workflow enforcement system
    status      Show current installation status

Options:
    -h, --help  Show this help message

Examples:
    $0                    # Install enforcement
    $0 install            # Install enforcement
    $0 uninstall          # Remove enforcement
    $0 status             # Check status

Description:
    This script installs a git workflow enforcement system that ensures
    all code changes pass quality gates before being committed. It uses
    git hooks to enforce a 3-step workflow:

    1. Implementation (write code)
    2. Quality Gate (review, test, validate)
    3. Git Operations (commit, push)

    The system prevents commits unless quality gates have passed,
    ensuring consistent code quality and preventing bypass of review
    processes.

EOF
}

# Main function
main() {
    local mode="$MODE_INSTALL"

    # Parse arguments
    case "${1:-}" in
        install)
            mode="$MODE_INSTALL"
            ;;
        uninstall)
            mode="$MODE_UNINSTALL"
            ;;
        status)
            mode="$MODE_STATUS"
            ;;
        -h|--help|help)
            usage
            exit 0
            ;;
        "")
            mode="$MODE_INSTALL"
            ;;
        *)
            error "Unknown command: $1"
            usage
            exit 1
            ;;
    esac

    # Change to project root
    cd "$PROJECT_ROOT"

    # Execute based on mode
    case "$mode" in
        "$MODE_INSTALL")
            install_enforcement
            ;;
        "$MODE_UNINSTALL")
            uninstall_enforcement
            ;;
        "$MODE_STATUS")
            show_status
            ;;
    esac
}

# Run main function
main "$@"