#!/bin/bash
# Uninstall OaK Telemetry Hooks

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================================${NC}"
echo -e "${BLUE}        CLAUDE OAK AGENTS - HOOK UNINSTALLATION${NC}"
echo -e "${BLUE}================================================================${NC}"

CLAUDE_DIR="$HOME/.claude"
HOOKS_DIR="$CLAUDE_DIR/hooks"

# Check if hooks exist
if [ ! -d "$HOOKS_DIR" ]; then
    echo -e "\n${YELLOW}No hooks directory found. Nothing to uninstall.${NC}"
    exit 0
fi

echo -e "\n${BLUE}Removing hooks...${NC}"

# Remove pre-agent hook
if [ -L "$HOOKS_DIR/pre_agent.sh" ]; then
    rm "$HOOKS_DIR/pre_agent.sh"
    echo -e "${GREEN}  ✓ Removed pre_agent.sh${NC}"
elif [ -f "$HOOKS_DIR/pre_agent.sh" ]; then
    mv "$HOOKS_DIR/pre_agent.sh" "$HOOKS_DIR/pre_agent.sh.removed.$(date +%s)"
    echo -e "${GREEN}  ✓ Backed up and removed pre_agent.sh${NC}"
fi

# Remove post-agent hook
if [ -L "$HOOKS_DIR/post_agent.sh" ]; then
    rm "$HOOKS_DIR/post_agent.sh"
    echo -e "${GREEN}  ✓ Removed post_agent.sh${NC}"
elif [ -f "$HOOKS_DIR/post_agent.sh" ]; then
    mv "$HOOKS_DIR/post_agent.sh" "$HOOKS_DIR/post_agent.sh.removed.$(date +%s)"
    echo -e "${GREEN}  ✓ Backed up and removed post_agent.sh${NC}"
fi

# Restore backups if they exist
BACKUPS=$(find "$HOOKS_DIR" -name "*.backup.*" 2>/dev/null || true)
if [ -n "$BACKUPS" ]; then
    echo -e "\n${YELLOW}Found backup hooks:${NC}"
    echo "$BACKUPS"
    echo -e "${YELLOW}Would you like to restore them? (y/n)${NC}"
    read -r response

    if [[ "$response" =~ ^[Yy]$ ]]; then
        for backup in $BACKUPS; do
            original=$(echo "$backup" | sed 's/\.backup\.[0-9]*$//')
            mv "$backup" "$original"
            echo -e "${GREEN}  ✓ Restored $(basename "$original")${NC}"
        done
    fi
fi

echo -e "\n${BLUE}================================================================${NC}"
echo -e "${GREEN}✓ Uninstallation complete!${NC}"
echo -e "${BLUE}================================================================${NC}"

echo -e "\n${BLUE}Note:${NC} Environment variables in your shell RC file were not removed."
echo -e "To completely remove OaK telemetry, also delete these lines from ~/.zshrc or ~/.bashrc:"
echo -e "  export OAK_TELEMETRY_ENABLED=..."
echo -e "  export OAK_TELEMETRY_DIR=..."
echo -e "  export OAK_PROMPT_FEEDBACK=..."
echo -e "  export PYTHONPATH=...claude-oak-agents..."

echo -e "\n${BLUE}Telemetry data preserved at:${NC}"
echo -e "  ~/Projects/claude-oak-agents/telemetry/"
echo -e "  (Delete manually if desired)"

echo -e "\n${GREEN}To reinstall: ./hooks/install_hooks.sh${NC}\n"
