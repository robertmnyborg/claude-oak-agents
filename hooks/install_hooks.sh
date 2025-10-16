#!/bin/bash
# Install OaK Telemetry Hooks
#
# This script sets up automatic telemetry logging for Claude agents.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================================${NC}"
echo -e "${BLUE}          CLAUDE OAK AGENTS - HOOK INSTALLATION${NC}"
echo -e "${BLUE}================================================================${NC}"

# Check if .claude directory exists
CLAUDE_DIR="$HOME/.claude"
if [ ! -d "$CLAUDE_DIR" ]; then
    echo -e "\n${RED}Error: Claude directory not found at $CLAUDE_DIR${NC}"
    echo -e "Please ensure Claude Code is installed."
    exit 1
fi

HOOKS_DIR="$CLAUDE_DIR/hooks"

# Create hooks directory if it doesn't exist
if [ ! -d "$HOOKS_DIR" ]; then
    echo -e "\n${YELLOW}Creating hooks directory...${NC}"
    mkdir -p "$HOOKS_DIR"
fi

# Make hook scripts executable
chmod +x "$SCRIPT_DIR"/*.py

echo -e "\n${BLUE}Step 1: Installing pre-agent hook...${NC}"

# Create symlink for pre-agent hook
if [ -L "$HOOKS_DIR/pre_agent.sh" ] || [ -f "$HOOKS_DIR/pre_agent.sh" ]; then
    echo -e "${YELLOW}  Existing pre_agent.sh found. Backing up...${NC}"
    mv "$HOOKS_DIR/pre_agent.sh" "$HOOKS_DIR/pre_agent.sh.backup.$(date +%s)"
fi

ln -s "$SCRIPT_DIR/pre_agent_hook.py" "$HOOKS_DIR/pre_agent.sh"
echo -e "${GREEN}  ✓ Pre-agent hook installed${NC}"

echo -e "\n${BLUE}Step 2: Installing post-agent hook...${NC}"

# Create symlink for post-agent hook
if [ -L "$HOOKS_DIR/post_agent.sh" ] || [ -f "$HOOKS_DIR/post_agent.sh" ]; then
    echo -e "${YELLOW}  Existing post_agent.sh found. Backing up...${NC}"
    mv "$HOOKS_DIR/post_agent.sh" "$HOOKS_DIR/post_agent.sh.backup.$(date +%s)"
fi

ln -s "$SCRIPT_DIR/post_agent_hook.py" "$HOOKS_DIR/post_agent.sh"
echo -e "${GREEN}  ✓ Post-agent hook installed${NC}"

echo -e "\n${BLUE}Step 3: Setting environment variables...${NC}"

# Check if .zshrc or .bashrc exists
SHELL_RC=""
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [ -n "$SHELL_RC" ] && [ -f "$SHELL_RC" ]; then
    echo -e "${YELLOW}  Would you like to add environment variables to $SHELL_RC? (y/n)${NC}"
    read -r response

    if [[ "$response" =~ ^[Yy]$ ]]; then
        # Check if variables already exist
        if ! grep -q "OAK_TELEMETRY" "$SHELL_RC"; then
            cat >> "$SHELL_RC" << EOF

# Claude OaK Agents - Telemetry Configuration
export OAK_TELEMETRY_ENABLED=true
export OAK_TELEMETRY_DIR="$PROJECT_ROOT/telemetry"
export OAK_PROMPT_FEEDBACK=false  # Set to true to enable interactive feedback prompts
export PYTHONPATH="$PROJECT_ROOT:\$PYTHONPATH"
EOF
            echo -e "${GREEN}  ✓ Environment variables added to $SHELL_RC${NC}"
            echo -e "${YELLOW}  Run 'source $SHELL_RC' to apply changes${NC}"
        else
            echo -e "${YELLOW}  Environment variables already exist in $SHELL_RC${NC}"
        fi
    fi
else
    echo -e "${YELLOW}  Manual setup required. Add these to your shell RC file:${NC}"
    echo -e "    export OAK_TELEMETRY_ENABLED=true"
    echo -e "    export OAK_TELEMETRY_DIR=\"$PROJECT_ROOT/telemetry\""
    echo -e "    export OAK_PROMPT_FEEDBACK=false"
    echo -e "    export PYTHONPATH=\"$PROJECT_ROOT:\$PYTHONPATH\""
fi

echo -e "\n${BLUE}Step 4: Creating telemetry directory...${NC}"

TELEMETRY_DIR="$PROJECT_ROOT/telemetry"
if [ ! -d "$TELEMETRY_DIR" ]; then
    mkdir -p "$TELEMETRY_DIR"
fi
echo -e "${GREEN}  ✓ Telemetry directory ready: $TELEMETRY_DIR${NC}"

echo -e "\n${BLUE}================================================================${NC}"
echo -e "${GREEN}✓ Installation complete!${NC}"
echo -e "${BLUE}================================================================${NC}"

echo -e "\n${BLUE}Next Steps:${NC}"
echo -e "  1. Restart your terminal or run: source ~/.zshrc  # or ~/.bashrc"
echo -e "  2. Verify installation: ls -la $HOOKS_DIR"
echo -e "  3. Test hooks: python scripts/test_telemetry_e2e.py"
echo -e "  4. Agent invocations will now be logged automatically!"

echo -e "\n${BLUE}Configuration:${NC}"
echo -e "  Enable/disable: export OAK_TELEMETRY_ENABLED=true/false"
echo -e "  View logs: cat $TELEMETRY_DIR/agent_invocations.jsonl"
echo -e "  Analyze: ./scripts/analyze_telemetry.sh"

echo -e "\n${BLUE}Uninstall:${NC}"
echo -e "  Run: $SCRIPT_DIR/uninstall_hooks.sh"

echo -e "\n${GREEN}Happy agent orchestration! 🚀${NC}\n"
