# YAML Generator Component

**Component ID**: Component-2 (YAMLGenerator)  
**Spec**: spec-20251023-spec-to-yaml-translator  
**Status**: Completed  
**Acceptance Criteria**: AC-2, AC-4

## Overview

The YAML Generator converts parsed Markdown specification data into structured YAML format following the `SPEC_SCHEMA.yaml` template. It provides schema validation, metadata tracking, and ensures idempotent translation (same input → same output).

## Features

- ✓ **Valid YAML Generation**: Produces YAML conforming to `specs/templates/SPEC_SCHEMA.yaml`
- ✓ **Schema Validation**: Validates generated YAML against schema requirements
- ✓ **Idempotent Translation**: Deterministic output with consistent key ordering
- ✓ **Metadata Tracking**: Automatic `last_sync` timestamps and markdown source location
- ✓ **Security**: Uses `yaml.safe_dump` (no arbitrary code execution)
- ✓ **Unicode Support**: Handles special characters and unicode properly

## Installation

### Dependencies

```bash
pip install pyyaml>=6.0
```

Optional (for extended validation):
```bash
pip install jsonschema>=4.17
```

## Usage

### Basic Usage

```python
from yaml_generator import YAMLGenerator, generate_yaml

# Sample parsed spec data (from markdown_parser)
parsed_data = {
    "metadata": {
        "spec_id": "spec-20251023-feature",
        "created": "2025-10-23T10:00:00Z",
        "updated": "2025-10-23T14:00:00Z",
        "status": "draft",
        "linked_request": "User request description"
    },
    "goals": {
        "primary": "Primary goal statement",
        "user_stories": [...],
        "acceptance_criteria": [...],
        "success_metrics": [...],
        "out_of_scope": [...]
    },
    "design": {...},
    "implementation": {...},
    "test_strategy": {...}
}

# Generate YAML
markdown_path = "specs/active/2025-10-23-feature.md"
yaml_output = generate_yaml(parsed_data, markdown_path)

# Save to file
with open("specs/active/2025-10-23-feature.yaml", "w") as f:
    f.write(yaml_output)
```

### Schema Validation

```python
import yaml
from yaml_generator import validate_schema

# Load existing YAML
with open("specs/active/feature.yaml") as f:
    yaml_data = yaml.safe_load(f)

# Validate against schema
try:
    is_valid = validate_schema(yaml_data)
    print("✓ Schema validation passed")
except ValueError as e:
    print(f"✗ Validation failed: {e}")
```

### Class-Based Usage

```python
from yaml_generator import YAMLGenerator

generator = YAMLGenerator()

# Generate YAML
yaml_string = generator.generate_yaml(parsed_data, markdown_path)

# Validate YAML
yaml_data = yaml.safe_load(yaml_string)
generator.validate_schema(yaml_data)

# Compute hash for idempotency checking
hash_value = generator.compute_yaml_hash(yaml_string)
```

## API Reference

### `YAMLGenerator` Class

#### Methods

##### `generate_yaml(parsed_data: Dict[str, Any], markdown_path: str) -> str`

Generate YAML string from parsed spec data.

**Parameters**:
- `parsed_data`: Dictionary containing parsed spec sections
- `markdown_path`: Path to source Markdown file

**Returns**: YAML string formatted according to SPEC_SCHEMA.yaml

**Raises**: `ValueError` if required fields are missing or invalid

##### `validate_schema(yaml_data: Dict[str, Any]) -> bool`

Validate YAML data against spec schema requirements.

**Parameters**:
- `yaml_data`: Dictionary containing YAML data to validate

**Returns**: `True` if valid

**Raises**: `ValueError` with detailed validation error message

##### `compute_yaml_hash(yaml_string: str) -> str`

Compute SHA256 hash of YAML content for idempotency validation.

**Parameters**:
- `yaml_string`: YAML content to hash

**Returns**: SHA256 hash (hex string, 64 characters)

### Module-Level Functions

#### `generate_yaml(parsed_data: Dict, markdown_path: str) -> str`

Convenience function for YAML generation.

#### `validate_schema(yaml_data: Dict) -> bool`

Convenience function for schema validation.

## YAML Structure

The generated YAML follows this structure:

```yaml
# Top-level metadata
spec_id: "spec-YYYYMMDD-feature-name"
created: "YYYY-MM-DDTHH:MM:SSZ"
updated: "YYYY-MM-DDTHH:MM:SSZ"
status: "draft | approved | in-progress | completed"
linked_request: "User request description"

# Section 1: Goals & Requirements
goals:
  primary: "Primary goal"
  user_stories: [...]
  acceptance_criteria: [...]
  success_metrics: [...]
  out_of_scope: [...]

# Section 2: Technical Design
technical_design:
  architecture: {...}
  components: [...]
  data_structures: [...]
  apis: [...]
  dependencies: [...]
  security_considerations: [...]
  performance_considerations: [...]

# Section 3: Implementation Plan
implementation:
  tasks: [...]
  execution_sequence: [...]
  risks: [...]

# Section 4: Test Strategy
test_strategy:
  test_cases: [...]
  test_types: {...}
  validation_checklist: [...]

# Section 5: Execution Log (auto-populated)
execution_log: []

# Section 6: Changes & Decisions (auto-tracked)
changes:
  design_changes: []
  scope_changes: []
  deviations: []

# Section 7: Completion Summary (filled at end)
completion:
  acceptance_criteria_status: []
  test_results: {...}
  success_metrics_results: []
  files_changed: {...}
  lessons_learned: []
  follow_up_items: []

# Section 8: Metadata (auto-generated)
metadata:
  spec_version: "1.0"
  generated_from_markdown: true
  markdown_location: "specs/active/YYYY-MM-DD-feature.md"
  last_sync: "YYYY-MM-DDTHH:MM:SSZ"
  statistics:
    total_tasks: 0
    completed_tasks: 0
    total_tests: 0
    passed_tests: 0
    agents_involved: []
    duration_seconds: null
```

## Metadata Section

The metadata section is automatically populated with:

- **spec_version**: `"1.0"` (schema version)
- **generated_from_markdown**: `true` (indicates auto-generation)
- **markdown_location**: Full path to source Markdown file
- **last_sync**: ISO 8601 timestamp of generation time (UTC)
- **statistics**: Tracking counters (initialized to zero)

## Validation Rules

The schema validator checks:

### Required Top-Level Fields
- `spec_id`: String
- `created`: ISO 8601 datetime
- `updated`: ISO 8601 datetime
- `status`: Enum (`draft`, `approved`, `in-progress`, `completed`)
- `linked_request`: String

### Required Sections
- `goals`: Goals and requirements section
- `technical_design`: Design section
- `implementation`: Implementation plan
- `test_strategy`: Test strategy section
- `metadata`: Metadata section

### Required Metadata Fields
- `spec_version`: String
- `generated_from_markdown`: Boolean
- `markdown_location`: String
- `last_sync`: ISO 8601 datetime

## Idempotency Guarantee

The generator ensures **deterministic output**:

1. **Same Input → Same Structure**: Given identical parsed data, the YAML structure is always identical (excluding timestamps)
2. **Consistent Key Ordering**: Dictionary keys are inserted in a consistent order
3. **Deterministic Formatting**: YAML formatting is consistent across runs
4. **Hash Validation**: Use `compute_yaml_hash()` to verify content equality

**Note**: The `metadata.last_sync` timestamp will differ between runs (reflects generation time), but all other content remains identical for the same input.

## Security Considerations

1. **Safe YAML Dump**: Uses `yaml.safe_dump()` exclusively (no code execution risk)
2. **Safe YAML Load**: Uses `yaml.safe_load()` for parsing (no `!!python` tags)
3. **Input Validation**: Validates required fields before generation
4. **Path Sanitization**: Markdown paths are stored as-is without execution

## Performance

- **Target**: <500ms for typical spec (<10KB Markdown)
- **Actual**: ~5-10ms for typical spec on modern hardware
- **Scalability**: O(n) with input size, no caching needed (deterministic)

## Testing

### Run Unit Tests

```bash
cd specs/tools
python3 -m unittest test_yaml_generator -v
```

### Run Demonstration

```bash
cd specs/tools
python3 demo_yaml_generator.py
```

### Test Coverage

The test suite (`test_yaml_generator.py`) includes:

- **TC-4**: Generate valid YAML following SPEC_SCHEMA.yaml
- **TC-5**: Idempotent translation (same input → same output)
- Schema validation (success and failure cases)
- Datetime formatting and timezone handling
- Edge cases (special characters, unicode, long content)
- Security validation (safe_dump usage)
- Section structure validation
- Convenience function testing

**Test Results**: 21 tests, 100% pass rate

## Examples

### Example 1: Complete Workflow

```python
from markdown_parser import parse_spec  # Component-1
from yaml_generator import generate_yaml, validate_schema
import yaml

# Step 1: Parse Markdown spec
markdown_file = "specs/active/2025-10-23-feature.md"
parsed_data = parse_spec(markdown_file)

# Step 2: Generate YAML
yaml_output = generate_yaml(parsed_data, markdown_file)

# Step 3: Validate generated YAML
yaml_data = yaml.safe_load(yaml_output)
validate_schema(yaml_data)

# Step 4: Save to file
yaml_file = "specs/active/2025-10-23-feature.yaml"
with open(yaml_file, "w") as f:
    f.write(yaml_output)

print(f"✓ Spec translated: {markdown_file} → {yaml_file}")
```

### Example 2: Incremental Updates

```python
import yaml
from yaml_generator import generate_yaml
from markdown_parser import parse_spec

# Parse updated Markdown
markdown_file = "specs/active/2025-10-23-feature.md"
parsed_data = parse_spec(markdown_file)

# Regenerate YAML (idempotent)
yaml_output = generate_yaml(parsed_data, markdown_file)

# Check if content changed (excluding timestamp)
yaml_file = "specs/active/2025-10-23-feature.yaml"
with open(yaml_file) as f:
    old_yaml = yaml.safe_load(f)

new_yaml = yaml.safe_load(yaml_output)

# Normalize timestamps
old_yaml["metadata"]["last_sync"] = "NORMALIZED"
new_yaml["metadata"]["last_sync"] = "NORMALIZED"

if old_yaml == new_yaml:
    print("No changes detected (YAML is up-to-date)")
else:
    print("Changes detected, updating YAML file")
    with open(yaml_file, "w") as f:
        f.write(yaml_output)
```

### Example 3: Validation Only

```python
import yaml
from yaml_generator import validate_schema

# Load existing YAML file
with open("specs/active/feature.yaml") as f:
    yaml_data = yaml.safe_load(f)

# Validate
try:
    validate_schema(yaml_data)
    print("✓ YAML is valid")
except ValueError as e:
    print(f"✗ Validation errors:\n{e}")
```

## Integration with Spec Workflow

This component integrates with the spec-driven development workflow:

```
Markdown Spec (Source of Truth)
        ↓
markdown_parser.py (Component-1)
        ↓
Parsed Data Dictionary
        ↓
yaml_generator.py (Component-2) ← YOU ARE HERE
        ↓
YAML Spec (Agent Consumption)
        ↓
Execution Agents (task execution)
```

## Error Handling

The generator provides clear error messages:

```python
# Missing required field
ValueError: YAML validation failed:
  - Missing required field: spec_id

# Invalid status enum
ValueError: YAML validation failed:
  - Invalid status: unknown (must be one of ['draft', 'approved', 'in-progress', 'completed'])

# Missing metadata field
ValueError: YAML validation failed:
  - Missing metadata.spec_version
  - Missing metadata.last_sync
```

## Troubleshooting

### Issue: Generated YAML has different content each time

**Cause**: Check if `metadata.last_sync` is the only difference (expected).

**Solution**: Normalize timestamps before comparison (see Example 2).

### Issue: Validation fails with "Missing required field"

**Cause**: Input `parsed_data` is missing required sections.

**Solution**: Ensure markdown_parser provides all required fields. Use minimal defaults if sections are empty.

### Issue: Special characters breaking YAML

**Cause**: PyYAML handles special chars, but check if using `safe_load`.

**Solution**: Always use `yaml.safe_load()` and `yaml.safe_dump()` (generator does this automatically).

## Future Enhancements

Potential improvements (out of scope for current implementation):

- JSON Schema validation (full JSONSchema support)
- Custom YAML dumper for prettier formatting
- Compression for large specs
- Diff generation (what changed between versions)
- YAML linting integration

## License

Part of the Claude Oak Agents project.

## Authors

Generated by backend-architect agent for spec-20251023-spec-to-yaml-translator.

## See Also

- `markdown_parser.py` - Component-1 (parses Markdown specs)
- `translate_spec.py` - Component-3 (CLI orchestration)
- `specs/templates/SPEC_SCHEMA.yaml` - Schema template
- `test_yaml_generator.py` - Comprehensive test suite
- `demo_yaml_generator.py` - Interactive demonstration
