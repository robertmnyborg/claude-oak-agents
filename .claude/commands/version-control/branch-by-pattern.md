# Branch by Pattern

Create a git branch following established naming conventions with automatic tracking setup.

## Usage
/branch-by-pattern [pattern] [description] [--ticket TICKET-123]

## What This Does
1. Validates branch naming pattern (feature/, bugfix/, hotfix/, refactor/)
2. Sanitizes description to create valid branch name
3. Optionally includes ticket number if provided
4. Creates branch and sets up remote tracking
5. Validates branch doesn't already exist

## Example
/branch-by-pattern feature "oauth2 authentication" --ticket AUTH-456

Creates: feature/AUTH-456-oauth2-authentication

## Agent Coordination
1. **Main LLM**: Validates pattern and formats branch name
2. **git-workflow-manager**: Executes git operations
   - Creates local branch
   - Sets up tracking with -u flag
   - Pushes to remote if requested

## Output
Branch created with format:
- **feature/[TICKET-]description** - New features
- **bugfix/[TICKET-]description** - Bug fixes
- **hotfix/[TICKET-]description** - Production hotfixes
- **refactor/[TICKET-]description** - Code refactoring

Examples:
- feature/AUTH-123-oauth2-flow
- bugfix/API-456-rate-limiting
- hotfix/PROD-789-memory-leak
- refactor/cleanup-legacy-code

Returns:
- Branch name created
- Remote tracking status
- Current branch switched to new branch
