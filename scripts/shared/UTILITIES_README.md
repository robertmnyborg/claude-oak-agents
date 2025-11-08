# Shared Utilities

Common utilities used by oak-* scripts to eliminate code duplication.

## Overview

This directory contains reusable Python utilities extracted from duplicated code across 7+ oak-* scripts. These utilities follow the KISS principle and use only the Python standard library (no external dependencies).

## Modules

### colors.py

ANSI color codes and formatting for terminal output.

**Usage:**
```python
from scripts.shared import Colors

# Use colors
print(f"{Colors.GREEN}Success{Colors.RESET}")
print(f"{Colors.RED}Error{Colors.RESET}")
print(f"{Colors.BOLD}{Colors.BLUE}Header{Colors.RESET}")

# Disable colors (for --no-color flag)
if args.no_color:
    Colors.disable()
```

**Available Colors:**
- `RED`, `GREEN`, `YELLOW`, `BLUE`, `MAGENTA`, `CYAN`, `WHITE`
- `HEADER` (purple/magenta)

**Formatting:**
- `BOLD`, `DIM`, `UNDERLINE`

**Reset:**
- `RESET`, `END` (alias for compatibility)

### telemetry_loader.py

Load and filter telemetry data from JSONL files.

**Usage:**
```python
from scripts.shared import load_invocations, get_recent_invocations
from pathlib import Path

# Load all invocations
telemetry_file = Path('telemetry/agent_invocations.jsonl')
invocations = load_invocations(telemetry_file)

# Load with filters
recent = load_invocations(
    telemetry_file,
    filter_days=7,              # Last 7 days
    filter_agent='backend-architect',
    filter_workflow='wf-20251022-abc123'
)

# Helper functions
recent = get_recent_invocations(telemetry_dir, days=7)
workflow_invocations = get_workflow_invocations(telemetry_dir, 'wf-123')
```

**Functions:**
- `load_invocations(file, filter_days, filter_agent, filter_workflow)` - Load with optional filters
- `get_recent_invocations(dir, days)` - Get last N days
- `get_workflow_invocations(dir, workflow_id)` - Get specific workflow

### markdown_utils.py

Parse YAML frontmatter from markdown files.

**Usage:**
```python
from scripts.shared import parse_frontmatter, get_metadata
from pathlib import Path

# Parse frontmatter from file
agent_file = Path('agents/backend-architect.md')
metadata, content = parse_frontmatter(agent_file)

print(metadata['agent_name'])  # 'backend-architect'
print(metadata['color'])       # 'green'
print(metadata['tags'])        # ['backend', 'database', 'api']

# Get specific metadata value
agent_name = get_metadata(agent_file, 'agent_name', default='unknown')

# Parse from string (not file)
from scripts.shared import parse_frontmatter_string
metadata, body = parse_frontmatter_string(markdown_content)
```

**Functions:**
- `parse_frontmatter(file_path)` - Returns `(metadata_dict, body_content)`
- `parse_frontmatter_string(content)` - Parse from string instead of file
- `get_metadata(file_path, key, default)` - Get single metadata value

### cli_utils.py

Argument parser factory and common CLI utilities.

**Usage:**
```python
from scripts.shared import create_base_parser, get_project_root

# Create parser with common flags
parser = create_base_parser(
    description='My oak script',
    add_common_args=True  # Adds --no-color, --verbose, --version
)

# Add custom arguments
parser.add_argument('--limit', type=int, default=10)

args = parser.parse_args()

# Use common args
if args.no_color:
    Colors.disable()
if args.verbose:
    print("Verbose mode enabled")

# Get project root
project_root = get_project_root()  # Returns Path to claude-oak-agents/
agents_dir = project_root / 'agents'
```

**Functions:**
- `create_base_parser(description, add_common_args)` - Create ArgumentParser with standard flags
- `get_project_root()` - Get Path to project root directory

**Common Args Added:**
- `--no-color` - Disable colored output
- `--verbose`, `-v` - Enable verbose output
- `--version` - Show version

### agent_utils.py

Agent categorization and metadata utilities.

**Usage:**
```python
from scripts.shared import get_agent_category, get_category_color, get_agent_type_category

# Get category from agent name
category = get_agent_category('backend-architect')  # Returns: 'development'
category = get_agent_category('security-auditor')   # Returns: 'security'

# Get color for category
color = get_category_color('development')  # Returns: 'GREEN'
color = get_category_color('security')     # Returns: 'RED'

# Get category from frontmatter agent_type
display_category = get_agent_type_category('development')  # Returns: 'Development'
```

**Categories:**
- `product` - Product strategist, business analyst, spec manager
- `development` - Frontend, backend, mobile, blockchain, ML
- `quality` - Code reviewer, quality gate, testing experts
- `security` - Security auditor, dependency scanner
- `infrastructure` - Infrastructure specialist, systems architect
- `workflow` - Git workflow, project manager, changelog
- `analysis` - Data scientist, state analyzer, debug specialist
- `documentation` - Technical writer, content writer
- `special` - Design simplicity advisor, agent creator, general purpose
- `other` - Unknown/uncategorized agents

**Category Colors:**
- `product` → BLUE
- `development` → GREEN
- `quality` → CYAN
- `security` → RED
- `infrastructure` → MAGENTA
- `workflow` → YELLOW
- `analysis` → CYAN
- `documentation` → BLUE
- `special` → MAGENTA

## Complete Example

Here's a complete oak-* script using all utilities:

```python
#!/usr/bin/env python3
"""oak-example - Example script using shared utilities"""

import sys
from pathlib import Path

# Add shared to path (if needed)
sys.path.insert(0, str(Path(__file__).parent / 'shared'))

# Import from shared utilities
from scripts.shared import (
    Colors,
    create_base_parser,
    get_project_root,
    load_invocations,
    parse_frontmatter,
    get_agent_category,
    get_category_color
)

def main():
    # Create parser with common args
    parser = create_base_parser('Example oak script')
    parser.add_argument('--limit', type=int, default=10)
    args = parser.parse_args()
    
    # Handle --no-color
    if args.no_color:
        Colors.disable()
    
    # Get project root
    project_root = get_project_root()
    
    # Load telemetry
    telemetry_file = project_root / 'telemetry' / 'agent_invocations.jsonl'
    invocations = load_invocations(telemetry_file, filter_days=7)
    
    # Parse agent metadata
    agents_dir = project_root / 'agents'
    for agent_file in agents_dir.glob('*.md'):
        metadata, content = parse_frontmatter(agent_file)
        agent_name = metadata.get('agent_name', agent_file.stem)
        
        # Get category and color
        category = get_agent_category(agent_name)
        color_name = get_category_color(category)
        color = getattr(Colors, color_name, Colors.WHITE)
        
        # Display
        print(f"{color}{agent_name}{Colors.RESET} ({category})")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
```

## Import Patterns

**From oak-* scripts (in scripts/ directory):**
```python
from scripts.shared import Colors, load_invocations, parse_frontmatter
```

**From agent scripts (in agents/*/scripts/):**
```python
import sys
from pathlib import Path

# Add shared to path
shared_path = Path(__file__).parent.parent.parent.parent / "scripts" / "shared"
sys.path.insert(0, str(shared_path))

from scripts.shared import Colors, load_invocations
```

## Design Principles

1. **KISS (Keep It Simple, Stupid)**: Simple, focused functions over complex abstractions
2. **No External Dependencies**: Uses only Python standard library
3. **Well-Documented**: Type hints, docstrings, and examples for all functions
4. **Backward Compatible**: Aliases (e.g., `Colors.END` = `Colors.RESET`) for compatibility
5. **Extracted from Real Code**: All utilities come from actual duplicated code in oak-* scripts

## Testing

Test utilities directly from command line:

```bash
# Test colors
python3 -c "from scripts.shared import Colors; print(f'{Colors.GREEN}Success{Colors.RESET}')"

# Test telemetry loader
python3 -c "from scripts.shared import load_invocations; from pathlib import Path; print(len(load_invocations(Path('telemetry/agent_invocations.jsonl'))))"

# Test frontmatter parsing
python3 -c "from scripts.shared import parse_frontmatter; from pathlib import Path; m, _ = parse_frontmatter(Path('agents/backend-architect.md')); print(m)"

# Test project root
python3 -c "from scripts.shared import get_project_root; print(get_project_root())"

# Test agent categories
python3 -c "from scripts.shared import get_agent_category; print(get_agent_category('backend-architect'))"
```

## Line Counts

| Module | Lines | Purpose |
|--------|-------|---------|
| colors.py | 37 | ANSI color codes and formatting |
| telemetry_loader.py | 78 | Load and filter telemetry data |
| markdown_utils.py | 95 | Parse YAML frontmatter from markdown |
| cli_utils.py | 37 | CLI argument parser utilities |
| agent_utils.py | 68 | Agent categorization and metadata |
| __init__.py | 32 | Package exports |
| **TOTAL** | **347** | **Complete shared utilities package** |

## Scripts Using These Utilities

- `oak-insights` - Telemetry analytics (Colors, telemetry_loader)
- `oak-history` - Agent execution history (Colors, telemetry_loader)
- `oak-status` - System status dashboard (Colors, telemetry_loader)
- `oak-discover` - Agent browser (Colors, markdown_utils, agent_utils)
- `oak-templates` - Template manager (markdown_utils)
- `oak-analyze` - Workflow analyzer (Colors, telemetry_loader)
- `oak-mode` - Mode switcher (Colors, cli_utils)

## Future Enhancements

Utilities will be added **only when duplication is observed** in 2+ scripts:

- `file_utils.py` - File I/O helpers (when duplicated)
- `validation_utils.py` - Input validation (when duplicated)
- `text_utils.py` - Text processing (when duplicated)

**Do NOT add utilities speculatively**. Wait for actual duplication to emerge.

## Maintenance

### Adding a Utility
1. Verify duplication exists in 2+ scripts
2. Create focused, single-purpose module
3. Add to `__init__.py` exports
4. Document in this README
5. Update line counts

### Removing a Utility
1. Check which scripts reference it
2. If <2 scripts use it, move to specific script
3. Update `__init__.py` exports
4. Remove from README

### Modifying a Utility
1. Ensure backward compatibility (add aliases if needed)
2. Update docstrings and type hints
3. Test all dependent scripts
4. Update README examples if needed

## Questions?

- **"Should I add X utility?"** → Only if 2+ scripts already duplicate it
- **"Can I modify an existing utility?"** → Yes, but maintain backward compatibility
- **"Which module for X function?"** → Follow existing categorization (colors, CLI, parsing, etc.)
- **"Can I use external libraries?"** → No, standard library only

## Summary

These utilities eliminate ~500+ lines of duplicated code across oak-* scripts while maintaining simplicity and zero external dependencies. All utilities are extracted from real code patterns and serve actual, proven needs.
