# Shared Utilities - Documentation Index

Quick navigation to all documentation and utilities.

## Quick Start

**New to shared utilities?** Start here:
1. Read [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Fast reference card (5 min read)
2. See [EXAMPLE_USAGE.py](EXAMPLE_USAGE.py) - Working example script
3. Browse [UTILITIES_README.md](UTILITIES_README.md) - Complete documentation

## Documentation Files

### For Users

| File | Purpose | Lines | Read Time |
|------|---------|-------|-----------|
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Fast reference card | 239 | 5 min |
| [UTILITIES_README.md](UTILITIES_README.md) | Complete usage guide | 404 | 15 min |
| [EXAMPLE_USAGE.py](EXAMPLE_USAGE.py) | Working demonstration | 114 | 10 min |

### For Maintainers

| File | Purpose | Lines | Read Time |
|------|---------|-------|-----------|
| [SUMMARY.md](SUMMARY.md) | Creation summary | 177 | 10 min |
| [CREATION_REPORT.md](CREATION_REPORT.md) | Delivery report | 293 | 15 min |
| [README.md](README.md) | Original philosophy | 210 | 10 min |

## Python Modules

| Module | Lines | Purpose | Key Functions |
|--------|-------|---------|---------------|
| [colors.py](colors.py) | 33 | Terminal colors | `Colors` class with RED, GREEN, BLUE, etc. |
| [telemetry_loader.py](telemetry_loader.py) | 74 | Load telemetry | `load_invocations()`, `get_recent_invocations()` |
| [markdown_utils.py](markdown_utils.py) | 85 | Parse frontmatter | `parse_frontmatter()`, `get_metadata()` |
| [cli_utils.py](cli_utils.py) | 37 | CLI parsers | `create_base_parser()`, `get_project_root()` |
| [agent_utils.py](agent_utils.py) | 66 | Agent categories | `get_agent_category()`, `get_category_color()` |
| [__init__.py](__init__.py) | 31 | Package exports | All public functions |

## Quick Import

```python
from scripts.shared import (
    Colors,                    # Terminal colors
    load_invocations,          # Load telemetry
    parse_frontmatter,         # Parse YAML frontmatter
    create_base_parser,        # CLI parser factory
    get_agent_category,        # Agent categorization
    get_project_root           # Project root path
)
```

## Common Use Cases

### I want to...

**Add colored output to my script**
→ See [QUICK_REFERENCE.md#colors](QUICK_REFERENCE.md#colors-colorspy)

**Load and filter telemetry data**
→ See [QUICK_REFERENCE.md#telemetry-loading](QUICK_REFERENCE.md#telemetry-loading-telemetry_loaderpy)

**Parse agent frontmatter**
→ See [QUICK_REFERENCE.md#frontmatter-parsing](QUICK_REFERENCE.md#frontmatter-parsing-markdown_utilspy)

**Create a standard CLI parser**
→ See [QUICK_REFERENCE.md#cli-utils](QUICK_REFERENCE.md#cli-utils-cli_utilspy)

**Categorize agents by type**
→ See [QUICK_REFERENCE.md#agent-utils](QUICK_REFERENCE.md#agent-utils-agent_utilspy)

**See a complete working example**
→ Run [EXAMPLE_USAGE.py](EXAMPLE_USAGE.py)

**Understand the design philosophy**
→ Read [README.md](README.md)

## Testing

```bash
# Test all imports
python3 -c "from scripts.shared import Colors, load_invocations, parse_frontmatter, get_agent_category; print('✓ All imports OK')"

# Run example
python3 scripts/shared/EXAMPLE_USAGE.py --limit 5 --days 30

# Test specific utility
python3 -c "from scripts.shared import Colors; print(f'{Colors.GREEN}Success{Colors.RESET}')"
```

## File Statistics

```
Total Files:           12
Python Modules:         7 (440 lines)
Documentation:          5 (1,332 lines)
Code-to-Doc Ratio:      1:3.0
```

## Scripts Using These Utilities

- `oak-insights` - Telemetry analytics (Colors, telemetry_loader)
- `oak-history` - Execution history (Colors, telemetry_loader)
- `oak-status` - System status (Colors, telemetry_loader)
- `oak-discover` - Agent browser (Colors, markdown_utils, agent_utils)
- `oak-templates` - Template manager (markdown_utils)
- `oak-analyze` - Workflow analyzer (Colors, telemetry_loader)
- `oak-mode` - Mode switcher (Colors, cli_utils)

## Next Steps

1. **Getting Started**: Read [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. **Learn by Example**: Run [EXAMPLE_USAGE.py](EXAMPLE_USAGE.py)
3. **Deep Dive**: Read [UTILITIES_README.md](UTILITIES_README.md)
4. **Maintenance**: See [CREATION_REPORT.md](CREATION_REPORT.md)

## Questions?

- **How do I import these utilities?** → See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **What functions are available?** → See [UTILITIES_README.md](UTILITIES_README.md)
- **How do I add new utilities?** → See [README.md](README.md) maintenance section
- **Where are the type hints?** → All modules have 100% type coverage

## Support

For issues or questions:
1. Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for quick answers
2. Read [UTILITIES_README.md](UTILITIES_README.md) for detailed documentation
3. Review [EXAMPLE_USAGE.py](EXAMPLE_USAGE.py) for working code patterns
4. See [CREATION_REPORT.md](CREATION_REPORT.md) for design decisions

---

**Version:** 1.0.0  
**Status:** Production Ready  
**Last Updated:** 2025-11-08
