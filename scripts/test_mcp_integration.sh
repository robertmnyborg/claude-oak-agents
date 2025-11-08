#!/bin/bash

# Test MCP Server Integration
# Validates Reddit and GitHub MCP servers are properly installed and configured

set -e

echo "================================"
echo "MCP Integration Test Suite"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

success() {
    echo -e "${GREEN}✓${NC} $1"
}

warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

error() {
    echo -e "${RED}✗${NC} $1"
}

# Test 1: Check Node.js version
echo "Test 1: Node.js Version"
NODE_VERSION=$(node --version)
if [[ $NODE_VERSION == v18* ]] || [[ $NODE_VERSION == v19* ]] || [[ $NODE_VERSION == v20* ]] || [[ $NODE_VERSION == v21* ]] || [[ $NODE_VERSION == v22* ]]; then
    success "Node.js version: $NODE_VERSION (✓ >= 18.x required)"
else
    error "Node.js version: $NODE_VERSION (requires >= 18.x)"
    exit 1
fi
echo ""

# Test 2: Check MCP directory structure
echo "Test 2: MCP Directory Structure"
MCP_DIR="/Users/robertnyborg/Projects/claude-oak-agents/mcp"

if [ -d "$MCP_DIR" ]; then
    success "MCP directory exists: $MCP_DIR"
else
    error "MCP directory not found: $MCP_DIR"
    exit 1
fi

if [ -f "$MCP_DIR/package.json" ]; then
    success "package.json exists"
else
    error "package.json not found"
    exit 1
fi

if [ -d "$MCP_DIR/src" ]; then
    success "src directory exists"
else
    error "src directory not found"
    exit 1
fi

if [ -d "$MCP_DIR/dist" ]; then
    success "dist directory exists (servers built)"
else
    warning "dist directory not found - servers not built yet"
    echo "  Run: cd $MCP_DIR && npm install && npm run build"
fi
echo ""

# Test 3: Check source files
echo "Test 3: MCP Server Source Files"
SOURCE_FILES=(
    "telemetry-server.ts"
    "agents-server.ts"
    "reddit-server.ts"
    "github-server.ts"
)

for file in "${SOURCE_FILES[@]}"; do
    if [ -f "$MCP_DIR/src/$file" ]; then
        success "$file exists"
    else
        error "$file not found"
    fi
done
echo ""

# Test 4: Check built files
echo "Test 4: MCP Server Build Artifacts"
if [ -d "$MCP_DIR/dist" ]; then
    BUILD_FILES=(
        "telemetry-server.js"
        "agents-server.js"
        "reddit-server.js"
        "github-server.js"
    )

    for file in "${BUILD_FILES[@]}"; do
        if [ -f "$MCP_DIR/dist/$file" ]; then
            success "$file exists"
        else
            error "$file not found"
        fi
    done
else
    warning "Skipping build artifact check (dist not found)"
fi
echo ""

# Test 5: Check dependencies
echo "Test 5: NPM Dependencies"
if [ -f "$MCP_DIR/package.json" ]; then
    if [ -d "$MCP_DIR/node_modules" ]; then
        success "node_modules directory exists"

        # Check for specific dependency
        if [ -d "$MCP_DIR/node_modules/@modelcontextprotocol" ]; then
            success "@modelcontextprotocol/sdk installed"
        else
            warning "@modelcontextprotocol/sdk not found"
            echo "  Run: cd $MCP_DIR && npm install"
        fi
    else
        warning "node_modules not found"
        echo "  Run: cd $MCP_DIR && npm install"
    fi
fi
echo ""

# Test 6: Test Reddit MCP Server
echo "Test 6: Reddit MCP Server"
if [ -f "$MCP_DIR/dist/reddit-server.js" ]; then
    success "Reddit MCP server file exists"
    success "  (Runtime test skipped - requires MCP client)"
else
    warning "Reddit MCP server not built - skipping runtime test"
fi
echo ""

# Test 7: Test GitHub MCP Server
echo "Test 7: GitHub MCP Server"
if [ -f "$MCP_DIR/dist/github-server.js" ]; then
    success "GitHub MCP server file exists"

    if [ -z "$GITHUB_MCP_TOKEN" ] && [ -z "$GITHUB_TOKEN" ]; then
        warning "GITHUB_MCP_TOKEN not set"
        echo "  Set with: export GITHUB_MCP_TOKEN='ghp_your_token_here'"
    else
        success "GitHub token is set"
    fi

    success "  (Runtime test skipped - requires MCP client)"
else
    warning "GitHub MCP server not built - skipping runtime test"
fi
echo ""

# Test 8: Check Claude Code configuration
echo "Test 8: Claude Code Configuration"
CLAUDE_CONFIG_LOCATIONS=(
    "$HOME/.claude/settings.local.json"
    "$HOME/.config/claude/mcp_servers.json"
)

FOUND_CONFIG=false
for config in "${CLAUDE_CONFIG_LOCATIONS[@]}"; do
    if [ -f "$config" ]; then
        success "Found Claude config: $config"
        FOUND_CONFIG=true

        # Check if MCP servers are configured
        if grep -q "reddit" "$config" 2>/dev/null; then
            success "  Reddit MCP configured"
        else
            warning "  Reddit MCP not configured"
        fi

        if grep -q "github" "$config" 2>/dev/null; then
            success "  GitHub MCP configured"
        else
            warning "  GitHub MCP not configured"
        fi
    fi
done

if [ "$FOUND_CONFIG" = false ]; then
    warning "Claude config file not found"
    echo "  Create config at: $HOME/.claude/settings.local.json"
    echo "  Template available: $MCP_DIR/mcp_config_template.json"
fi
echo ""

# Test 9: Check documentation
echo "Test 9: Documentation"
DOCS=(
    "/Users/robertnyborg/Projects/claude-oak-agents/docs/MCP_INTEGRATION.md"
    "/Users/robertnyborg/Projects/claude-oak-agents/examples/mcp_examples.md"
    "/Users/robertnyborg/Projects/claude-oak-agents/mcp/README.md"
)

for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        success "$(basename $doc) exists"
    else
        warning "$(basename $doc) not found"
    fi
done
echo ""

# Test 10: Environment check
echo "Test 10: Environment Variables"
if [ -n "$GITHUB_MCP_TOKEN" ]; then
    success "GITHUB_MCP_TOKEN is set"
elif [ -n "$GITHUB_TOKEN" ]; then
    success "GITHUB_TOKEN is set (will be used for GitHub MCP)"
else
    warning "No GitHub token set"
    echo "  Set with: export GITHUB_MCP_TOKEN='ghp_your_token_here'"
    echo "  Create token at: https://github.com/settings/tokens"
    echo "  Required scopes: repo, read:packages, read:org, workflow"
fi
echo ""

# Summary
echo "================================"
echo "Test Summary"
echo "================================"
echo ""
echo "Integration Status:"
echo ""

# Check overall status
if [ -d "$MCP_DIR/dist" ] && [ -f "$MCP_DIR/dist/reddit-server.js" ] && [ -f "$MCP_DIR/dist/github-server.js" ]; then
    success "Reddit MCP Server: READY"
    if [ -n "$GITHUB_MCP_TOKEN" ] || [ -n "$GITHUB_TOKEN" ]; then
        success "GitHub MCP Server: READY"
    else
        warning "GitHub MCP Server: NEEDS TOKEN"
    fi
else
    warning "MCP Servers: NEED BUILD"
    echo ""
    echo "To build servers:"
    echo "  cd $MCP_DIR"
    echo "  npm install"
    echo "  npm run build"
fi

echo ""
echo "Next Steps:"
echo ""

if [ ! -d "$MCP_DIR/dist" ]; then
    echo "1. Build MCP servers:"
    echo "   cd $MCP_DIR && npm install && npm run build"
    echo ""
fi

if [ "$FOUND_CONFIG" = false ]; then
    echo "2. Configure Claude Code:"
    echo "   Copy mcp_config_template.json to ~/.claude/settings.local.json"
    echo ""
fi

if [ -z "$GITHUB_MCP_TOKEN" ] && [ -z "$GITHUB_TOKEN" ]; then
    echo "3. Set GitHub token:"
    echo "   export GITHUB_MCP_TOKEN='ghp_your_token_here'"
    echo "   echo 'export GITHUB_MCP_TOKEN=\"ghp_your_token_here\"' >> ~/.zshrc"
    echo ""
fi

echo "For complete documentation:"
echo "  docs/MCP_INTEGRATION.md"
echo "  examples/mcp_examples.md"
echo "  mcp/README.md"
echo ""

echo "================================"
success "Test suite completed"
echo "================================"
