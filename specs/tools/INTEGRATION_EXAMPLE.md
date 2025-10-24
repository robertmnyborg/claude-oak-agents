# Integration Example: Markdown Parser → YAML Generator

This document shows how Component-1 (MarkdownParser) and Component-2 (YAMLGenerator) work together.

## Complete Workflow

```python
#!/usr/bin/env python3
"""
Complete spec translation workflow example.
Demonstrates markdown_parser → yaml_generator integration.
"""

from markdown_parser import parse_spec
from yaml_generator import generate_yaml, validate_schema
import yaml

def translate_spec(markdown_file: str, yaml_file: str):
    """
    Translate Markdown spec to YAML format.
    
    Args:
        markdown_file: Path to source Markdown spec
        yaml_file: Path to output YAML file
    """
    print(f"Translating: {markdown_file} → {yaml_file}")
    print("-" * 80)
    
    # Step 1: Parse Markdown spec
    print("Step 1: Parsing Markdown spec...")
    parsed_data = parse_spec(markdown_file)
    print(f"  ✓ Parsed {len(parsed_data)} sections")
    
    # Step 2: Generate YAML
    print("Step 2: Generating YAML...")
    yaml_output = generate_yaml(parsed_data, markdown_file)
    print(f"  ✓ Generated {len(yaml_output)} bytes of YAML")
    
    # Step 3: Validate YAML
    print("Step 3: Validating YAML schema...")
    yaml_data = yaml.safe_load(yaml_output)
    try:
        validate_schema(yaml_data)
        print("  ✓ Schema validation passed")
    except ValueError as e:
        print(f"  ✗ Schema validation failed:\n{e}")
        return False
    
    # Step 4: Save to file
    print("Step 4: Saving YAML to file...")
    with open(yaml_file, "w") as f:
        f.write(yaml_output)
    print(f"  ✓ Saved to {yaml_file}")
    
    # Step 5: Verify metadata
    print("Step 5: Verifying metadata...")
    metadata = yaml_data["metadata"]
    print(f"  - Spec Version: {metadata['spec_version']}")
    print(f"  - Markdown Location: {metadata['markdown_location']}")
    print(f"  - Last Sync: {metadata['last_sync']}")
    
    print("-" * 80)
    print("✓ Translation complete!")
    return True


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python3 integration_example.py <markdown_file> <yaml_file>")
        print("\nExample:")
        print("  python3 integration_example.py \\")
        print("    specs/active/2025-10-23-feature.md \\")
        print("    specs/active/2025-10-23-feature.yaml")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    yaml_file = sys.argv[2]
    
    success = translate_spec(markdown_file, yaml_file)
    sys.exit(0 if success else 1)
```

## Expected Data Flow

### Input: Markdown Spec

```markdown
# Spec: Feature Name

**Spec ID**: spec-20251023-feature-name
**Created**: 2025-10-23
**Status**: draft
**Linked Request**: User request description

## 1. Goals & Requirements

### 1.1 Primary Goal
Build feature X to solve problem Y.

### 1.2 User Stories
- **As a** user, **I want** capability, **so that** benefit

### 1.3 Acceptance Criteria
- [ ] **AC-1**: Criterion 1
- [ ] **AC-2**: Criterion 2

...
```

### Intermediate: Parsed Data (from markdown_parser)

```python
{
    "metadata": {
        "spec_id": "spec-20251023-feature-name",
        "created": "2025-10-23T00:00:00Z",
        "updated": "2025-10-23T00:00:00Z",
        "status": "draft",
        "linked_request": "User request description"
    },
    "goals": {
        "primary": "Build feature X to solve problem Y.",
        "user_stories": [
            {
                "id": "us-1",
                "role": "user",
                "capability": "capability",
                "benefit": "benefit"
            }
        ],
        "acceptance_criteria": [
            {
                "id": "ac-1",
                "criterion": "Criterion 1",
                "status": "pending",
                "linked_tasks": [],
                "linked_tests": []
            },
            {
                "id": "ac-2",
                "criterion": "Criterion 2",
                "status": "pending",
                "linked_tasks": [],
                "linked_tests": []
            }
        ],
        "success_metrics": [],
        "out_of_scope": []
    },
    "design": {...},
    "implementation": {...},
    "test_strategy": {...}
}
```

### Output: YAML Spec (from yaml_generator)

```yaml
spec_id: spec-20251023-feature-name
created: '2025-10-23T00:00:00Z'
updated: '2025-10-23T00:00:00Z'
status: draft
linked_request: User request description

goals:
  primary: Build feature X to solve problem Y.
  user_stories:
  - id: us-1
    role: user
    capability: capability
    benefit: benefit
  acceptance_criteria:
  - id: ac-1
    criterion: Criterion 1
    status: pending
    linked_tasks: []
    linked_tests: []
  - id: ac-2
    criterion: Criterion 2
    status: pending
    linked_tasks: []
    linked_tests: []
  success_metrics: []
  out_of_scope: []

technical_design:
  architecture:
    overview: ''
    key_decisions: []
  components: []
  data_structures: []
  apis: []
  dependencies: []
  security_considerations: []
  performance_considerations: []

implementation:
  tasks: []
  execution_sequence: []
  risks: []

test_strategy:
  test_cases: []
  test_types:
    unit_tests: []
    integration_tests: []
    e2e_tests: []
    performance_tests: []
  validation_checklist: []

execution_log: []

changes:
  design_changes: []
  scope_changes: []
  deviations: []

completion:
  acceptance_criteria_status: []
  test_results:
    unit_tests: 0/0 passed
    integration_tests: 0/0 passed
    e2e_tests: 0/0 passed
    all_tests_passing: false
  success_metrics_results: []
  files_changed:
    total: 0
    created: []
    modified: []
    deleted: []
  lessons_learned: []
  follow_up_items: []

metadata:
  spec_version: '1.0'
  generated_from_markdown: true
  markdown_location: specs/active/2025-10-23-feature-name.md
  last_sync: '2025-10-24T05:30:00.123456Z'
  statistics:
    total_tasks: 0
    completed_tasks: 0
    total_tests: 0
    passed_tests: 0
    agents_involved: []
    duration_seconds: null
```

## Component Responsibilities

### Component-1: MarkdownParser

**Input**: Markdown spec file  
**Output**: Parsed data dictionary (Python dict)  
**Responsibilities**:
- Extract structured data from Markdown sections
- Parse user stories, acceptance criteria, tasks, etc.
- Preserve linkages between sections
- Return Python dictionary with all parsed data

### Component-2: YAMLGenerator (THIS COMPONENT)

**Input**: Parsed data dictionary + markdown path  
**Output**: YAML string  
**Responsibilities**:
- Build YAML structure matching SPEC_SCHEMA.yaml
- Add metadata section with tracking info
- Validate against schema requirements
- Ensure deterministic output (idempotency)
- Use safe YAML operations (security)

## Data Contract

The **interface** between markdown_parser and yaml_generator is the `parsed_data` dictionary:

### Required Fields

```python
parsed_data = {
    "metadata": {
        "spec_id": str,           # Required
        "created": str|datetime,   # Required (ISO 8601)
        "updated": str|datetime,   # Required (ISO 8601)
        "status": str,             # Required (draft|approved|in-progress|completed)
        "linked_request": str      # Required
    },
    "goals": {
        "primary": str,
        "user_stories": List[Dict],
        "acceptance_criteria": List[Dict],
        "success_metrics": List[Dict],
        "out_of_scope": List[str]
    },
    "design": {
        "architecture": Dict,
        "components": List[Dict],
        "data_structures": List[Dict],
        "apis": List[Dict],
        "dependencies": List[Dict],
        "security_considerations": List[Dict],
        "performance_considerations": List[Dict]
    },
    "implementation": {
        "tasks": List[Dict],
        "execution_sequence": List[Dict],
        "risks": List[Dict]
    },
    "test_strategy": {
        "test_cases": List[Dict],
        "test_types": Dict,
        "validation_checklist": List[Dict]
    }
}
```

### Optional/Defaults

The YAML generator provides sensible defaults for missing fields:
- Missing sections → empty lists/dicts
- Missing metadata fields → current timestamp or default values
- Missing nested fields → empty structures

This ensures the YAML generator always produces valid output even if the markdown parser returns partial data.

## Error Handling

### Markdown Parser Errors

```python
try:
    parsed_data = parse_spec(markdown_file)
except FileNotFoundError:
    print(f"Error: Markdown file not found: {markdown_file}")
except ValueError as e:
    print(f"Error parsing Markdown: {e}")
```

### YAML Generator Errors

```python
try:
    yaml_output = generate_yaml(parsed_data, markdown_file)
except ValueError as e:
    print(f"Error generating YAML: {e}")
    # parsed_data is missing required fields
```

### Schema Validation Errors

```python
try:
    validate_schema(yaml_data)
except ValueError as e:
    print(f"Schema validation failed:\n{e}")
    # YAML structure doesn't match schema requirements
```

## Testing Integration

```python
def test_integration():
    """Test markdown_parser → yaml_generator integration."""
    # Parse sample Markdown
    markdown_file = "specs/active/test-spec.md"
    parsed_data = parse_spec(markdown_file)
    
    # Generate YAML
    yaml_output = generate_yaml(parsed_data, markdown_file)
    
    # Validate
    yaml_data = yaml.safe_load(yaml_output)
    validate_schema(yaml_data)
    
    # Verify metadata
    assert yaml_data["metadata"]["markdown_location"] == markdown_file
    assert yaml_data["metadata"]["spec_version"] == "1.0"
    assert yaml_data["metadata"]["generated_from_markdown"] == True
    
    print("✓ Integration test passed")
```

## Performance

Typical workflow timing:

1. **Parse Markdown** (Component-1): 10-50ms for typical spec
2. **Generate YAML** (Component-2): 5-10ms
3. **Validate Schema**: 1-5ms
4. **Save to File**: 1-5ms

**Total**: <100ms for complete translation workflow

## Next Steps

After implementing Component-2 (YAMLGenerator):

1. **Component-3**: TranslationCLI - CLI orchestration
2. **Integration**: Connect all components
3. **Workflow**: Add file watching for auto-regeneration
4. **Validation**: JSON Schema integration for stricter validation

## See Also

- `yaml_generator.py` - Component-2 implementation
- `markdown_parser.py` - Component-1 implementation
- `README_YAML_GENERATOR.md` - YAML generator documentation
- `specs/templates/SPEC_SCHEMA.yaml` - Schema template
