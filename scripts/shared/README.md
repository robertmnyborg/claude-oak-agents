# Shared Agent Utilities

## Purpose

This directory contains **reusable utilities** that multiple agents can import and use.

## Philosophy: KISS First

**Don't create shared utilities prematurely.** Follow this decision tree:

```
Need functionality?
  ↓
  Is it used by 1 agent only?
    → Put it in that agent's scripts/ directory

  Is it used by 2+ agents?
    → Consider putting it here (but read guidelines first)

  Is it a standard library function?
    → Just use the standard library (import directly)

  Is it available in PyPI/npm?
    → Use the library directly (pip install / npm install)
```

## When to Add a Shared Utility

✅ **Add to `scripts/shared/` when:**
- Same code is duplicated in 2+ agents
- Logic is stable and unlikely to change
- Utility is genuinely reusable (not agent-specific)
- Standard libraries don't provide the functionality
- External libraries are overkill for the task

❌ **Don't add to `scripts/shared/` when:**
- Only 1 agent needs it (keep it in agent's scripts/)
- Standard library provides it (use `import os`, `import json`, etc.)
- External library exists (use `pip install library`)
- Logic is still evolving (keep in agent until stable)
- "It might be useful someday" (YAGNI principle)

## Structure

```
scripts/shared/
  __init__.py           # Package initialization
  README.md             # This file
  <utility_name>.py     # Individual utility modules
```

## Usage Example

### From an Agent Script

```python
# In agents/security-auditor/scripts/scan_vulnerabilities.py
import sys
from pathlib import Path

# Add shared scripts to path
shared_path = Path(__file__).parent.parent.parent.parent / "scripts" / "shared"
sys.path.insert(0, str(shared_path))

# Import shared utility
from file_utils import read_json_safe

# Use it
config = read_json_safe("config.json")
```

### Creating a New Shared Utility

1. **Verify it's needed by 2+ agents** (check for duplication)
2. **Create the utility file**:
   ```bash
   touch scripts/shared/my_utility.py
   ```
3. **Write minimal, focused code**:
   ```python
   """
   Brief description of what this utility does.

   Used by:
   - agent-name-1 (for X purpose)
   - agent-name-2 (for Y purpose)
   """

   def my_function(param: str) -> str:
       """Clear docstring explaining what it does."""
       # Keep it simple
       return result
   ```
4. **Document which agents use it** (in the module docstring)
5. **Test it works**:
   ```bash
   python3 -c "from scripts.shared.my_utility import my_function; print(my_function('test'))"
   ```

## Example Utilities (Future)

These will be created **only when duplication is observed**:

- `file_utils.py` - File I/O helpers (when 2+ agents duplicate file reading logic)
- `text_utils.py` - Text processing (when 2+ agents duplicate text manipulation)
- `network_utils.py` - HTTP/API helpers (when 2+ agents duplicate API calls)
- `validation_utils.py` - Input validation (when 2+ agents duplicate validation)

**Current count**: 0 utilities (waiting for actual duplication to emerge)

## Anti-Patterns to Avoid

❌ **Kitchen Sink Utility**:
```python
# BAD: Giant utility with everything
def utils_do_everything(data, mode, format, options, ...):
    if mode == "json":
        # 50 lines
    elif mode == "yaml":
        # 50 lines
    # etc...
```

✅ **Focused Utilities**:
```python
# GOOD: Small, focused functions
def parse_json_safe(filepath: str) -> dict:
    """Parse JSON file with error handling."""
    # 5-10 lines

def parse_yaml_safe(filepath: str) -> dict:
    """Parse YAML file with error handling."""
    # 5-10 lines
```

❌ **Premature Abstraction**:
```python
# BAD: Creating abstraction before duplication exists
class DataProcessor:
    # Complex abstraction layer for single use case
```

✅ **Extract on Duplication**:
```python
# GOOD: Wait until same code appears in 2+ agents, then extract
def extract_tables_from_pdf(pdf_path: str) -> List[dict]:
    """Extract tables from PDF (used by security-auditor and data-scientist)."""
    # Extract common logic after seeing duplication
```

## Maintenance

### Adding a Utility
1. Verify duplication exists (not hypothetical)
2. Create focused, single-purpose utility
3. Document which agents use it
4. Keep it simple (KISS principle)

### Removing a Utility
When a utility is no longer used by 2+ agents:
1. Check which agents reference it
2. If only 1 agent uses it, move it to that agent's scripts/
3. If no agents use it, delete it
4. Update this README

### Refactoring a Utility
When utility grows complex:
1. Consider if it should be multiple utilities
2. Evaluate if an external library is better
3. Re-evaluate if agents really need shared code
4. Simplify before expanding

## Current Utilities

**None yet** - Utilities will be added as duplication emerges from actual agent usage.

## Testing

Test shared utilities:

```bash
# Run all shared utility tests
python3 -m pytest scripts/shared/

# Test specific utility
python3 -c "from scripts.shared.file_utils import read_json_safe; print(read_json_safe('test.json'))"
```

## Best Practices

1. **Wait for Duplication**: Don't predict what will be shared
2. **Keep It Simple**: Small, focused functions over complex abstractions
3. **Document Usage**: Always list which agents use each utility
4. **Test Thoroughly**: Shared code affects multiple agents
5. **Minimize Dependencies**: Prefer standard library over external packages
6. **Version Carefully**: Breaking changes affect multiple agents

## Questions?

- **"Should I create a utility for X?"** → Only if 2+ agents already duplicate it
- **"This might be useful later"** → YAGNI - wait until it's needed
- **"Should I use an external library?"** → Usually yes, if it's well-maintained
- **"How complex should utilities be?"** → As simple as possible, preferably <50 lines

## Summary

**Core Principle**: Utilities emerge from observed duplication, not anticipated reuse.

Wait. Watch. Extract. Simplify.
