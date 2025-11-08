# Shared Utilities - Quick Reference Card

Fast reference for using shared utilities in oak-* scripts.

## Import Statement

```python
from scripts.shared import (
    Colors,                    # Terminal colors
    load_invocations,          # Load telemetry
    get_recent_invocations,    # Recent telemetry
    get_workflow_invocations,  # Workflow telemetry
    parse_frontmatter,         # Parse YAML frontmatter
    parse_frontmatter_string,  # Parse from string
    get_metadata,              # Get metadata value
    create_base_parser,        # CLI parser factory
    get_project_root,          # Project root path
    get_agent_category,        # Agent category
    get_category_color,        # Category color
    get_agent_type_category    # Type to category
)
```

## Colors (colors.py)

```python
# Use colors
print(f"{Colors.GREEN}Success{Colors.RESET}")
print(f"{Colors.RED}Error{Colors.RESET}")
print(f"{Colors.BOLD}{Colors.BLUE}Header{Colors.RESET}")

# Available colors
Colors.RED, Colors.GREEN, Colors.YELLOW, Colors.BLUE
Colors.MAGENTA, Colors.CYAN, Colors.WHITE, Colors.HEADER

# Formatting
Colors.BOLD, Colors.DIM, Colors.UNDERLINE

# Disable all colors
Colors.disable()
```

## Telemetry Loading (telemetry_loader.py)

```python
from pathlib import Path

# Load all invocations
invocations = load_invocations(Path('telemetry/agent_invocations.jsonl'))

# Load with filters
recent = load_invocations(
    telemetry_file,
    filter_days=7,              # Last 7 days
    filter_agent='backend-architect',
    filter_workflow='wf-123'
)

# Helper functions
recent = get_recent_invocations(telemetry_dir, days=7)
workflow = get_workflow_invocations(telemetry_dir, 'wf-123')
```

## Frontmatter Parsing (markdown_utils.py)

```python
from pathlib import Path

# Parse from file
metadata, content = parse_frontmatter(Path('agents/agent.md'))
print(metadata['agent_name'])
print(metadata['color'])

# Parse from string
metadata, body = parse_frontmatter_string(markdown_text)

# Get specific value
value = get_metadata(Path('agents/agent.md'), 'agent_name', default='unknown')
```

## CLI Utils (cli_utils.py)

```python
# Create parser with common flags
parser = create_base_parser(
    description='My oak script',
    add_common_args=True  # Adds --no-color, --verbose, --version
)

# Add custom arguments
parser.add_argument('--limit', type=int, default=10)
args = parser.parse_args()

# Get project root
project_root = get_project_root()
agents_dir = project_root / 'agents'
```

## Agent Utils (agent_utils.py)

```python
# Get category from agent name
category = get_agent_category('backend-architect')  # 'development'

# Get color for category
color = get_category_color('development')  # 'GREEN'

# Use together
category = get_agent_category(agent_name)
color_name = get_category_color(category)
color = getattr(Colors, color_name, Colors.WHITE)
print(f"{color}{agent_name}{Colors.RESET}")
```

## Common Patterns

### Pattern 1: Colored Terminal Output
```python
from scripts.shared import Colors

# Setup
if args.no_color:
    Colors.disable()

# Use
print(f"{Colors.GREEN}✓ Success{Colors.RESET}")
print(f"{Colors.RED}✗ Error{Colors.RESET}")
print(f"{Colors.BOLD}{Colors.BLUE}=== Header ==={Colors.RESET}")
```

### Pattern 2: Load and Filter Telemetry
```python
from scripts.shared import load_invocations, Colors
from pathlib import Path

telemetry_file = Path('telemetry/agent_invocations.jsonl')
invocations = load_invocations(
    telemetry_file,
    filter_days=7,
    filter_agent='backend-architect'
)

for inv in invocations:
    status = inv.get('outcome', {}).get('status', 'unknown')
    color = Colors.GREEN if status == 'success' else Colors.RED
    print(f"{color}{status}{Colors.RESET}")
```

### Pattern 3: Parse Agent Files
```python
from scripts.shared import parse_frontmatter, get_agent_category, Colors
from pathlib import Path

agents_dir = Path('agents')
for agent_file in agents_dir.glob('*.md'):
    metadata, _ = parse_frontmatter(agent_file)
    agent_name = metadata.get('agent_name', agent_file.stem)
    
    category = get_agent_category(agent_name)
    color_name = get_category_color(category)
    color = getattr(Colors, color_name, Colors.WHITE)
    
    print(f"{color}{agent_name}{Colors.RESET} ({category})")
```

### Pattern 4: Standard CLI Script
```python
from scripts.shared import create_base_parser, Colors

def main():
    parser = create_base_parser('My Script')
    parser.add_argument('--limit', type=int, default=10)
    args = parser.parse_args()
    
    if args.no_color:
        Colors.disable()
    
    if args.verbose:
        print(f"{Colors.DIM}Verbose mode enabled{Colors.RESET}")
    
    # Your logic here
    print(f"{Colors.GREEN}Done{Colors.RESET}")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
```

## Agent Categories

| Category | Agents | Color |
|----------|--------|-------|
| product | product-strategist, business-analyst, spec-manager | BLUE |
| development | frontend-developer, backend-architect, mobile-developer | GREEN |
| quality | code-reviewer, quality-gate, unit-test-expert | CYAN |
| security | security-auditor, dependency-scanner | RED |
| infrastructure | infrastructure-specialist, systems-architect | MAGENTA |
| workflow | git-workflow-manager, project-manager | YELLOW |
| analysis | state-analyzer, debug-specialist, agent-auditor | CYAN |
| documentation | technical-writer, content-writer | BLUE |
| special | design-simplicity-advisor, agent-creator | MAGENTA |

## Common Args (create_base_parser)

When `add_common_args=True`:
- `--no-color` - Disable colored output
- `--verbose`, `-v` - Enable verbose mode
- `--version` - Show version

## Testing

```bash
# Test imports
python3 -c "from scripts.shared import Colors; print('OK')"

# Test colors
python3 -c "from scripts.shared import Colors; print(f'{Colors.GREEN}Success{Colors.RESET}')"

# Test telemetry
python3 -c "from scripts.shared import load_invocations; from pathlib import Path; print(len(load_invocations(Path('telemetry/agent_invocations.jsonl'))))"

# Run example
python3 scripts/shared/EXAMPLE_USAGE.py --limit 5
```

## Files Reference

| File | Purpose | Key Functions |
|------|---------|---------------|
| colors.py | Terminal colors | `Colors` class, `disable()` |
| telemetry_loader.py | Load telemetry | `load_invocations()`, `get_recent_invocations()` |
| markdown_utils.py | Parse frontmatter | `parse_frontmatter()`, `get_metadata()` |
| cli_utils.py | CLI parsers | `create_base_parser()`, `get_project_root()` |
| agent_utils.py | Agent categories | `get_agent_category()`, `get_category_color()` |

## Full Documentation

See `UTILITIES_README.md` for complete documentation with detailed examples.
