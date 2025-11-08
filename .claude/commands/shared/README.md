# Shared Command Resources

This directory contains common sections referenced by multiple slash commands to reduce duplication.

## Available Shared Sections

### related-quality-commands.md
Links to quality-related analysis commands (complexity, security, performance, dependencies).

### related-git-commands.md
Links to version control commands (commit, PR, branching).

### related-pm-commands.md
Links to project management commands (roadmap, velocity, task suggestions).

## Usage in Commands

Reference shared sections at the end of command files:

```markdown
## See Also
For related commands, see:
- [Quality Commands](../shared/related-quality-commands.md)
- [Git Commands](../shared/related-git-commands.md)
```

This creates a navigation mesh between related commands while maintaining single source of truth.
