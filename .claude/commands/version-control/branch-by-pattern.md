# Branch by Pattern

Create git branch following naming conventions with automatic tracking setup.

## Usage
/branch-by-pattern [pattern] [description] [--ticket TICKET-123]

## What This Does
1. Validates naming pattern and sanitizes description for valid branch name
2. Optionally includes ticket number and sets up remote tracking
3. Creates branch following conventions (feature/, bugfix/, hotfix/, refactor/)

## Example
/branch-by-pattern feature "oauth2 authentication" --ticket AUTH-456

Creates: feature/AUTH-456-oauth2-authentication

## Agent Coordination
1. **Main LLM**: Validates pattern and formats branch name
2. **git-workflow-manager**: Executes git operations and tracking setup

## Output
Branch created following patterns:
- **feature/[TICKET-]description** - New features
- **bugfix/[TICKET-]description** - Bug fixes
- **hotfix/[TICKET-]description** - Production hotfixes
- **refactor/[TICKET-]description** - Code refactoring

Examples:
- feature/AUTH-123-oauth2-flow
- bugfix/API-456-rate-limiting
- hotfix/PROD-789-memory-leak
- refactor/cleanup-legacy-code

Returns: Branch name, remote tracking status, and confirmation of branch switch

## See Also
For related commands, see [Git Commands](../shared/related-git-commands.md)
