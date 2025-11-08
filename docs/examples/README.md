# Reusable Examples Library

This directory contains extracted, reusable examples and patterns referenced throughout the OaK documentation. Instead of duplicating examples across multiple documents, source docs link to these canonical examples.

## Structure

```
examples/
├── workflows/          # Complete workflow examples
│   ├── oauth2-implementation.md
│   ├── api-creation.md
│   ├── database-migration.md
│   └── secure-deployment.md
├── agent-patterns/     # Common agent coordination patterns
│   ├── spec-driven-development.md
│   ├── quality-gates.md
│   └── git-workflow.md
└── code-snippets/      # Reusable code patterns
    ├── typescript-patterns.md
    ├── error-handling.md
    └── testing-patterns.md
```

## Usage

Examples are referenced in documentation using relative links:

```markdown
For a complete OAuth2 implementation workflow, see
[OAuth2 Implementation](../examples/workflows/oauth2-implementation.md).
```

## Benefits

- **Single source of truth**: Update examples once, changes reflected everywhere
- **Consistency**: Same patterns used across all documentation
- **Maintainability**: Easier to keep examples current
- **Discoverability**: Central location for finding implementation patterns

## Contributing

When adding examples:
1. Ensure example is reusable (appears in 3+ locations)
2. Include complete context and working code
3. Document assumptions and prerequisites
4. Add cross-references to related patterns
5. Update source documents to link to example
