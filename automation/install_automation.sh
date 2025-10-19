#!/bin/bash
# OaK Agent System - Automation Installation Script
# Installs shell prompts, launchd scheduled tasks, and notification system

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m' # No Color

OAK_PROJECT_DIR="$HOME/Projects/claude-oak-agents"
SHELL_RC="${SHELL_RC:-$HOME/.zshrc}"
LAUNCHAGENTS_DIR="$HOME/Library/LaunchAgents"

echo -e "${BLUE}================================================================${NC}"
echo -e "${BLUE}        OaK AGENT SYSTEM - AUTOMATION INSTALLATION${NC}"
echo -e "${BLUE}================================================================${NC}"

# Check if we're in the right directory
if [ ! -d "$OAK_PROJECT_DIR" ]; then
    echo -e "${RED}Error: Project directory not found: $OAK_PROJECT_DIR${NC}"
    exit 1
fi

cd "$OAK_PROJECT_DIR"

# ============================================================================
# PREREQUISITE CHECK: Telemetry Hooks
# ============================================================================

echo -e "\n${BLUE}Checking prerequisites...${NC}"

# Check if hooks are installed
if [ ! -L "$HOME/.claude/hooks/pre_agent.sh" ] || [ ! -L "$HOME/.claude/hooks/post_agent.sh" ]; then
    echo -e "\n${YELLOW}⚠  Telemetry hooks not installed!${NC}"
    echo -e "\nThe automation system requires telemetry hooks for data collection."
    echo -e "Without hooks, the system cannot track agent performance.\n"
    echo -e "${YELLOW}Would you like to install telemetry hooks now? (y/n)${NC}"
    read -r install_hooks

    if [[ "$install_hooks" =~ ^[Yy]$ ]]; then
        echo -e "\n${BLUE}Installing telemetry hooks...${NC}"
        ./hooks/install_hooks.sh
        echo -e "${GREEN}  ✓ Hooks installed${NC}"
    else
        echo -e "\n${RED}Warning: Automation will run but no data will be collected!${NC}"
        echo -e "Install hooks later with: ${YELLOW}./hooks/install_hooks.sh${NC}\n"
        echo -e "${YELLOW}Continue anyway? (y/n)${NC}"
        read -r continue_anyway
        if [[ ! "$continue_anyway" =~ ^[Yy]$ ]]; then
            echo -e "${RED}Installation cancelled.${NC}"
            exit 1
        fi
    fi
else
    echo -e "${GREEN}  ✓ Telemetry hooks already installed${NC}"
fi

# Create necessary directories
echo -e "\n${BLUE}Creating directories...${NC}"
mkdir -p logs
mkdir -p reports
mkdir -p telemetry
echo -e "${GREEN}  ✓ Directories created${NC}"

# Make scripts executable
echo -e "\n${BLUE}Making scripts executable...${NC}"
chmod +x automation/oak_prompts.sh
chmod +x automation/oak_notify.sh
chmod +x scripts/automation/*.py 2>/dev/null || true
chmod +x scripts/phase4/*.py 2>/dev/null || true
chmod +x scripts/phase5/*.py 2>/dev/null || true
chmod +x scripts/phase6/*.py 2>/dev/null || true
echo -e "${GREEN}  ✓ Scripts are executable${NC}"

# ============================================================================
# STEP 1: Install Shell Prompts (Option A)
# ============================================================================

echo -e "\n${BLUE}================================================================${NC}"
echo -e "${BLUE}STEP 1: Shell Prompt System${NC}"
echo -e "${BLUE}================================================================${NC}"

echo -e "\nThis will add OaK prompt system to your shell RC file."
echo -e "Location: ${YELLOW}$SHELL_RC${NC}"
echo -e "\n${YELLOW}Do you want to install shell prompts? (y/n)${NC}"
read -r install_prompts

if [[ "$install_prompts" =~ ^[Yy]$ ]]; then
    # Check if already installed
    if grep -q "oak_prompts.sh" "$SHELL_RC"; then
        echo -e "${YELLOW}  ⚠  Shell prompts already installed in $SHELL_RC${NC}"
    else
        echo -e "\n# OaK Agent System - Automated Prompts" >> "$SHELL_RC"
        echo "source \"$OAK_PROJECT_DIR/automation/oak_prompts.sh\"" >> "$SHELL_RC"
        echo -e "${GREEN}  ✓ Shell prompts installed${NC}"
        echo -e "${YELLOW}  ⚡ Reload shell: source $SHELL_RC${NC}"
    fi

    # Create initial state file
    if [ ! -f "telemetry/.oak_review_state" ]; then
        cat > telemetry/.oak_review_state <<EOF
LAST_WEEKLY_REVIEW=1970-01-01
LAST_MONTHLY_REVIEW=1970-01-01
LAST_HEALTH_CHECK=1970-01-01
EOF
        echo -e "${GREEN}  ✓ Created state tracking file${NC}"
    fi
else
    echo -e "${YELLOW}  ⊘ Skipped shell prompts${NC}"
fi

# ============================================================================
# STEP 2: Install LaunchD Scheduled Tasks (Option B)
# ============================================================================

echo -e "\n${BLUE}================================================================${NC}"
echo -e "${BLUE}STEP 2: Automated Scheduled Execution${NC}"
echo -e "${BLUE}================================================================${NC}"

echo -e "\nThis will install launchd jobs to automatically run:"
echo -e "  • ${GREEN}Weekly review${NC} - Every Monday at 9am"
echo -e "  • ${GREEN}Monthly analysis${NC} - 1st of month at 10am"
echo -e "  • ${GREEN}Health check${NC} - Every 3 days"
echo -e "  • ${GREEN}Actionable data check${NC} - Daily at 9am"
echo -e "\n${YELLOW}Do you want to install automated execution? (y/n)${NC}"
read -r install_launchd

if [[ "$install_launchd" =~ ^[Yy]$ ]]; then
    mkdir -p "$LAUNCHAGENTS_DIR"

    # Install each launchd plist
    declare -a plists=(
        "com.oak.weekly-review"
        "com.oak.monthly-analysis"
        "com.oak.health-check"
        "com.oak.actionable-check"
    )

    for plist in "${plists[@]}"; do
        source_file="automation/launchd/${plist}.plist"
        target_file="$LAUNCHAGENTS_DIR/${plist}.plist"

        if [ -f "$target_file" ]; then
            echo -e "${YELLOW}  ⚠  Unloading existing: ${plist}${NC}"
            launchctl unload "$target_file" 2>/dev/null || true
        fi

        cp "$source_file" "$target_file"
        launchctl load "$target_file"
        echo -e "${GREEN}  ✓ Installed and loaded: ${plist}${NC}"
    done

    echo -e "\n${GREEN}  ✓ All scheduled tasks installed${NC}"
    echo -e "\n${BLUE}View scheduled tasks:${NC}"
    echo -e "  launchctl list | grep com.oak"
else
    echo -e "${YELLOW}  ⊘ Skipped automated execution${NC}"
fi

# ============================================================================
# STEP 3: Test Notification System
# ============================================================================

echo -e "\n${BLUE}================================================================${NC}"
echo -e "${BLUE}STEP 3: Notification System Test${NC}"
echo -e "${BLUE}================================================================${NC}"

echo -e "\n${YELLOW}Do you want to test notifications? (y/n)${NC}"
read -r test_notifications

if [[ "$test_notifications" =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Sending test notification...${NC}"
    bash automation/oak_notify.sh test

    echo -e "\n${GREEN}✓ Test notification sent!${NC}"
    echo -e "Did you see a notification? If not, check System Preferences > Notifications"
else
    echo -e "${YELLOW}  ⊘ Skipped notification test${NC}"
fi

# ============================================================================
# SUMMARY
# ============================================================================

echo -e "\n${BLUE}================================================================${NC}"
echo -e "${BLUE}              INSTALLATION COMPLETE${NC}"
echo -e "${BLUE}================================================================${NC}"

echo -e "\n${BOLD}What's Installed:${NC}"

if [[ "$install_prompts" =~ ^[Yy]$ ]]; then
    echo -e "  ${GREEN}✓${NC} Shell prompts - Shows reminders when you open terminal"
fi

if [[ "$install_launchd" =~ ^[Yy]$ ]]; then
    echo -e "  ${GREEN}✓${NC} Automated execution - Runs reviews on schedule"
    echo -e "  ${GREEN}✓${NC} Notifications - Alerts when reviews are ready"
fi

echo -e "\n${BOLD}Available Commands:${NC}"
echo -e "  ${GREEN}oak-status${NC}         - View system status"
echo -e "  ${GREEN}oak-weekly-review${NC}  - Run weekly analysis"
echo -e "  ${GREEN}oak-monthly-review${NC} - Run monthly curation"
echo -e "  ${GREEN}oak-health-check${NC}   - Check system health"
echo -e "  ${GREEN}oak-dashboard${NC}      - View performance dashboard"

echo -e "\n${BOLD}Schedule:${NC}"
echo -e "  ${BLUE}Weekly:${NC}  Mondays at 9am (automated)"
echo -e "  ${BLUE}Monthly:${NC} 1st of month at 10am (automated)"
echo -e "  ${BLUE}Health:${NC}  Every 3 days (automated)"
echo -e "  ${BLUE}Daily:${NC}   9am check for actionable data (automated)"

echo -e "\n${BOLD}Logs Location:${NC}"
echo -e "  ${BLUE}$OAK_PROJECT_DIR/logs/${NC}"

echo -e "\n${BOLD}Next Steps:${NC}"
echo -e "  1. ${YELLOW}Reload shell:${NC} source $SHELL_RC"
echo -e "  2. ${YELLOW}Check status:${NC} oak-status"
echo -e "  3. ${YELLOW}Start using agents${NC} - telemetry logs automatically"
echo -e "  4. ${YELLOW}Wait for prompts${NC} - system will notify when reviews are due"

echo -e "\n${GREEN}🎉 Ready to learn and improve!${NC}\n"

# Optional: Show current status
echo -e "${YELLOW}Show current system status now? (y/n)${NC}"
read -r show_status

if [[ "$show_status" =~ ^[Yy]$ ]]; then
    source automation/oak_prompts.sh
    oak-status
fi

echo ""
