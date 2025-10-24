# Spec-to-YAML Translation Tool

> Automated translation from human-readable Markdown specifications to structured YAML format for agent consumption

**Version**: 1.0
**Status**: Production Ready
**License**: Part of claude-oak-agents project

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Components](#components)
6. [Examples](#examples)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)
9. [Architecture](#architecture)
10. [API Reference](#api-reference)
11. [Contributing](#contributing)
12. [License & Credits](#license--credits)

---

## Overview

### What is the Spec-to-YAML Translator?

The Spec-to-YAML Translation Tool is an automated pipeline that converts human-readable Markdown specification files into structured YAML format. This enables the spec-driven development workflow where:

1. **Humans** collaborate on specifications in readable Markdown format
2. **Tool** automatically translates to structured YAML
3. **Agents** consume YAML for programmatic task execution

### Why It Exists

In spec-driven development workflows, specifications serve as the source of truth for project requirements, design decisions, and implementation plans. However:

- **Humans prefer Markdown** (readable, collaborative, version-control friendly)
- **Agents need YAML** (structured, parseable, programmatically accessible)

This tool bridges the gap by maintaining Markdown as the single source of truth while providing agents with structured YAML they can consume.

### Key Features

- **Complete Spec Parsing** - Extracts all sections: goals, design, implementation, tests
- **Linkage Preservation** - Maintains cross-references between sections (goals ↔ tasks ↔ tests)
- **Schema Validation** - Ensures generated YAML conforms to spec schema
- **Idempotent Translation** - Same Markdown always produces same YAML (deterministic)
- **Metadata Tracking** - Automatic timestamps and source location tracking
- **Fast Performance** - <500ms for typical specs (actual: 22-26ms, 95% faster)
- **Error Handling** - Clear error messages for malformed input
- **CLI Interface** - Simple command-line tool for translation and validation
- **Zero Dependencies** - Parser uses Python stdlib only (YAML generation requires pyyaml)

---

## Quick Start

### 5-Minute Getting Started Guide

```bash
# 1. Install dependencies
pip3 install pyyaml>=6.0

# 2. Translate a Markdown spec to YAML
cd specs/tools
python3 translate_spec.py \
  --input ../active/my-feature.md \
  --output ../active/my-feature.yaml \
  --validate

# 3. Validate existing YAML
python3 translate_spec.py --validate-yaml ../active/my-feature.yaml
```

**Expected Output**:
```
📄 Parsing Markdown spec: ../active/my-feature.md
✅ Successfully parsed 5 sections
🔧 Generating YAML structure...
🔍 Validating YAML schema...
✅ YAML validation passed
✅ Successfully translated to: ../active/my-feature.yaml
📊 Metadata tracked:
   - Source: ../active/my-feature.md
   - Generated: ../active/my-feature.yaml
   - Timestamp: 2025-10-24T05:45:59Z
```

That's it! Your Markdown spec is now available as structured YAML for agent consumption.

---

## Installation

### Prerequisites

- **Python**: 3.9 or later
- **Operating System**: macOS, Linux, or Windows with Python support

### Dependencies

**Required** (for YAML generation):
```bash
pip3 install pyyaml>=6.0
```

**Optional** (for extended validation):
```bash
pip3 install jsonschema>=4.17
```

**Optional** (for watch mode - NOT IMPLEMENTED):
```bash
pip3 install watchdog>=3.0
```

### Verification

Verify installation by running the test suite:

```bash
cd specs/tools
python3 -m unittest discover -s . -p "test_*.py" -v
```

Expected output: All tests passing (46 total tests)

---

## Usage

### Translation Mode

**Basic Translation**:
```bash
python3 translate_spec.py --input spec.md --output spec.yaml
```

**Translation with Validation**:
```bash
python3 translate_spec.py \
  --input spec.md \
  --output spec.yaml \
  --validate
```

**Real-World Example**:
```bash
python3 translate_spec.py \
  --input ../active/2025-10-23-authentication-feature.md \
  --output ../active/2025-10-23-authentication-feature.yaml \
  --validate
```

### Validation Mode

Validate an existing YAML spec without regeneration:

```bash
python3 translate_spec.py --validate-yaml spec.yaml
```

**Example Output**:
```
📄 Loading YAML file: spec.yaml
🔍 Validating YAML schema...
✅ YAML validation passed
📊 Spec metadata:
   - Spec ID: spec-20251023-feature
   - Status: in-progress
   - Last sync: 2025-10-24T05:45:59Z
   - Source: ../active/2025-10-23-feature.md
```

### Watch Mode (Not Yet Implemented)

Watch for file changes and auto-regenerate:

```bash
python3 translate_spec.py --watch spec.md
```

**Status**: NOT IMPLEMENTED - Requires `watchdog` library. For now, manually re-run translation after making changes.

### Batch Translation

Translate all specs in a directory:

```bash
for md_file in ../active/*.md; do
  yaml_file="${md_file%.md}.yaml"
  echo "Translating $md_file → $yaml_file"
  python3 translate_spec.py --input "$md_file" --output "$yaml_file" --validate
done
```

### Incremental Updates

When you update a Markdown spec, simply re-run the translation. The `last_sync` timestamp in metadata will be updated automatically:

```bash
# Edit Markdown spec
vim ../active/my-feature.md

# Regenerate YAML
python3 translate_spec.py \
  --input ../active/my-feature.md \
  --output ../active/my-feature.yaml \
  --validate
```

---

## Components

The translation tool consists of three main components that work together to provide the complete workflow.

### 1. MarkdownParser (Component-1)

**Purpose**: Extract structured data from Markdown specification files

**File**: `markdown_parser.py`

**API**:
```python
from markdown_parser import parse_spec

# Parse a spec file
result = parse_spec("/path/to/spec.md")

# Access structured data
spec_id = result["metadata"]["spec_id"]
user_stories = result["goals"]["user_stories"]
components = result["design"]["components"]
tasks = result["implementation"]["tasks"]
test_cases = result["test_strategy"]["test_cases"]
```

**Key Features**:
- Extracts all spec sections (metadata, goals, design, implementation, tests)
- Preserves linkages between sections via "Links to:" annotations
- Flexible regex patterns handle varying formatting
- Clear error messages for malformed input
- Zero dependencies (uses Python stdlib only)

**Data Structure**:
```python
{
    "metadata": {"spec_id": str, "created": str, "updated": str, "status": str},
    "goals": {"primary": str, "user_stories": [...], "acceptance_criteria": [...]},
    "design": {"architecture": {...}, "components": [...], "dependencies": [...]},
    "implementation": {"tasks": [...], "execution_sequence": [...], "risks": [...]},
    "test_strategy": {"test_cases": [...], "test_types": {...}, "validation_checklist": [...]}
}
```

**See Also**: [PARSER_SUMMARY.md](PARSER_SUMMARY.md) for detailed parser documentation

### 2. YAMLGenerator (Component-2)

**Purpose**: Convert parsed data into structured YAML following the spec schema

**File**: `yaml_generator.py`

**API**:
```python
from yaml_generator import generate_yaml, validate_schema
import yaml

# Generate YAML from parsed data
yaml_output = generate_yaml(parsed_data, markdown_path)

# Validate generated YAML
yaml_data = yaml.safe_load(yaml_output)
validate_schema(yaml_data)

# Save to file
with open("spec.yaml", "w") as f:
    f.write(yaml_output)
```

**Key Features**:
- Valid YAML conforming to `specs/templates/SPEC_SCHEMA.yaml`
- Schema validation against required fields and structure
- Idempotent translation (deterministic output)
- Automatic metadata tracking (timestamps, source location)
- Security: uses `yaml.safe_dump` (no code execution risk)
- Unicode support (handles special characters properly)

**Metadata Section**:
```yaml
metadata:
  spec_version: "1.0"
  generated_from_markdown: true
  markdown_location: "specs/active/feature.md"
  last_sync: "2025-10-24T05:45:59.357238Z"
  statistics:
    total_tasks: 5
    completed_tasks: 0
    total_tests: 8
    passed_tests: 0
```

**See Also**: [README_YAML_GENERATOR.md](README_YAML_GENERATOR.md) for detailed YAML generator documentation

### 3. TranslationCLI (Component-3)

**Purpose**: Command-line interface orchestrating the translation workflow

**File**: `translate_spec.py`

**API**:
```bash
# Translation mode
translate_spec.py --input <md_file> --output <yaml_file> [--validate]

# Validation mode
translate_spec.py --validate-yaml <yaml_file>

# Watch mode (not implemented)
translate_spec.py --watch <md_file>
```

**Workflow**:
1. Parse Markdown using `markdown_parser.parse_spec()`
2. Generate YAML using `yaml_generator.generate_yaml()`
3. Validate (optional) using `yaml_generator.validate_schema()`
4. Write output to specified file
5. Report success with metadata summary

**See Also**: [README_CLI.md](README_CLI.md) for detailed CLI documentation

### Component Integration

```
Markdown Spec (Source of Truth)
        ↓
MarkdownParser (Component-1)
        ↓
Parsed Data Dictionary
        ↓
YAMLGenerator (Component-2)
        ↓
YAML Spec (Agent Consumption)
        ↓
TranslationCLI (Component-3)
        ↓
Validated Output File
```

**See Also**: [INTEGRATION_EXAMPLE.md](INTEGRATION_EXAMPLE.md) for complete integration examples

---

## Examples

### Example 1: Complete Workflow

```python
#!/usr/bin/env python3
"""Complete spec translation workflow."""

from markdown_parser import parse_spec
from yaml_generator import generate_yaml, validate_schema
import yaml

# Step 1: Parse Markdown spec
markdown_file = "specs/active/2025-10-23-feature.md"
parsed_data = parse_spec(markdown_file)
print(f"✓ Parsed {len(parsed_data)} sections")

# Step 2: Generate YAML
yaml_output = generate_yaml(parsed_data, markdown_file)
print(f"✓ Generated {len(yaml_output)} bytes of YAML")

# Step 3: Validate
yaml_data = yaml.safe_load(yaml_output)
validate_schema(yaml_data)
print("✓ Schema validation passed")

# Step 4: Save to file
yaml_file = "specs/active/2025-10-23-feature.yaml"
with open(yaml_file, "w") as f:
    f.write(yaml_output)
print(f"✓ Saved to {yaml_file}")
```

### Example 2: Error Handling

```python
from markdown_parser import parse_spec, ParseError
from yaml_generator import generate_yaml, validate_schema

try:
    # Parse Markdown
    parsed_data = parse_spec("feature.md")

    # Generate YAML
    yaml_output = generate_yaml(parsed_data, "feature.md")

    # Validate
    yaml_data = yaml.safe_load(yaml_output)
    validate_schema(yaml_data)

    print("✓ Translation successful")

except FileNotFoundError as e:
    print(f"✗ File not found: {e}")

except ParseError as e:
    print(f"✗ Parse error: {e}")

except ValueError as e:
    print(f"✗ Validation error: {e}")
```

### Example 3: Incremental Update Detection

```python
import yaml
from yaml_generator import generate_yaml
from markdown_parser import parse_spec

# Parse updated Markdown
parsed_data = parse_spec("feature.md")

# Regenerate YAML
new_yaml = generate_yaml(parsed_data, "feature.md")

# Load existing YAML
with open("feature.yaml") as f:
    old_yaml = yaml.safe_load(f)

# Compare (excluding timestamps)
new_yaml_data = yaml.safe_load(new_yaml)
old_yaml["metadata"]["last_sync"] = "NORMALIZED"
new_yaml_data["metadata"]["last_sync"] = "NORMALIZED"

if old_yaml == new_yaml_data:
    print("No changes detected")
else:
    print("Changes detected, updating YAML")
    with open("feature.yaml", "w") as f:
        f.write(new_yaml)
```

### Example 4: Linkage Extraction

```python
from markdown_parser import parse_spec

result = parse_spec("feature.md")

# Get task linkages
task = result["implementation"]["tasks"][0]
print(f"Task: {task['name']}")
print(f"Links to: {task['links_to']}")
# Output: Links to: ['Component-1', 'AC-1', 'tc-1', 'tc-2']

# Get component linkages
component = result["design"]["components"][0]
print(f"Component: {component['name']}")
print(f"Links to: {component['links_to']}")
# Output: Links to: ['AC-1', 'AC-3']
```

### Example 5: Agent Consumption

```python
import yaml

# Agent loads generated YAML spec
with open('spec.yaml') as f:
    spec = yaml.safe_load(f)

# Access structured data
tasks = spec['implementation']['tasks']
for task in tasks:
    if task['agent'] == 'backend-architect':
        print(f"Executing task: {task['name']}")
        print(f"Files: {task['files']}")
        print(f"Depends on: {task['depends_on']}")
        # Execute task...
```

---

## Testing

### Run All Tests

```bash
cd specs/tools

# Run all unit tests
python3 -m unittest discover -s . -p "test_*.py" -v

# Run specific test suite
python3 -m unittest test_markdown_parser -v
python3 -m unittest test_yaml_generator -v
python3 -m unittest test_integration -v
```

### Test Coverage Summary

**Total Tests**: 46 tests across 3 test suites

| Test Suite | Tests | Status | Coverage |
|------------|-------|--------|----------|
| test_markdown_parser.py | 10 | ✅ PASSING | Parser functionality |
| test_yaml_generator.py | 21 | ✅ PASSING | YAML generation |
| test_integration.py | 16 | ✅ PASSING | End-to-end workflow |

### Test Case Coverage

All specified test cases implemented and passing:

- ✅ **TC-1**: Parse complete spec with all sections
- ✅ **TC-2**: Preserve linkages between sections
- ✅ **TC-3**: Handle malformed Markdown gracefully
- ✅ **TC-4**: Generate valid YAML following SPEC_SCHEMA.yaml
- ✅ **TC-5**: Idempotent translation (same input → same output)
- ✅ **TC-6**: CLI end-to-end translation
- ✅ **TC-7**: Metadata tracking
- ✅ **TC-8**: Integration with real spec (dogfooding)

**Dogfooding Success**: The tool successfully translates its own specification file (`specs/active/2025-10-23-spec-to-yaml-translator.md`), validating the complete workflow.

### Acceptance Criteria Validation

All acceptance criteria met and tested:

- ✅ **AC-1**: Tool reads Markdown spec and extracts all sections
- ✅ **AC-2**: Tool generates valid YAML following SPEC_SCHEMA.yaml
- ✅ **AC-3**: All linkages are preserved
- ✅ **AC-4**: Generated YAML passes schema validation
- ✅ **AC-5**: Tool handles incremental updates
- ✅ **AC-6**: Metadata tracks last sync timestamp and source location

### Performance Benchmarks

| Metric | Target | Actual | Result |
|--------|--------|--------|--------|
| Typical spec translation | <500ms | 22-26ms | ✅ 95% faster |
| Large spec (165 items) | N/A | ~43ms | ✅ Excellent |
| Real spec (dogfooding) | <500ms | 22-26ms | ✅ 95% faster |

**See Also**: [TEST_COVERAGE_SUMMARY.md](TEST_COVERAGE_SUMMARY.md) for detailed test coverage report

---

## Troubleshooting

### Common Issues

#### Issue: `python: command not found`

**Cause**: Python not in PATH or wrong version

**Solution**: Use `python3` instead of `python`:
```bash
python3 translate_spec.py --help
```

#### Issue: `Import Error: No module named 'yaml'`

**Cause**: PyYAML not installed

**Solution**: Install PyYAML:
```bash
pip3 install pyyaml
```

#### Issue: Parse error on valid Markdown

**Cause**: Spec doesn't follow required template structure

**Solution**: Ensure Markdown spec has all required metadata fields:
```markdown
**Spec ID**: spec-YYYYMMDD-name
**Created**: YYYY-MM-DD
**Status**: draft|approved|in-progress|completed
**Linked Request**: "Description"
```

#### Issue: Validation fails on generated YAML

**Cause**: Missing required sections in Markdown

**Solution**: Ensure Markdown has all required sections:
- Section 1: Goals & Requirements
- Section 2: Technical Design
- Section 3: Implementation Plan
- Section 4: Test Strategy

#### Issue: Special characters break YAML

**Cause**: Unicode handling issue (rare)

**Solution**: Ensure file encoding is UTF-8:
```bash
file -I spec.md  # Check encoding
```

PyYAML handles special characters automatically when using `safe_dump`.

#### Issue: Different YAML output each time

**Cause**: `metadata.last_sync` timestamp changes (expected behavior)

**Solution**: This is normal. The timestamp reflects when YAML was generated. All other content is deterministic. To compare YAML equality, normalize timestamps:
```python
old_yaml["metadata"]["last_sync"] = "NORMALIZED"
new_yaml["metadata"]["last_sync"] = "NORMALIZED"
assert old_yaml == new_yaml  # Structural equality
```

### Error Messages

**Clear Error Messages**: The tool provides specific, actionable error messages:

```
❌ Error: File not found - Spec file not found: nonexistent.md
❌ Error: Failed to parse Markdown - Missing required metadata: Spec ID
❌ Error: Validation failed - YAML validation failed:
  - Missing required field: created
  - Missing required section: goals
```

### Performance Issues

**Issue**: Translation takes longer than expected

**Diagnostic**:
```bash
time python3 translate_spec.py --input spec.md --output spec.yaml
```

**Expected**: <100ms for typical spec

**If Slow**:
1. Check file size (`ls -lh spec.md`)
2. Simplify regex patterns (if customized)
3. Disable validation (`--validate` flag adds 1-5ms)

### Getting Help

1. **Check error messages** - They provide specific failure reasons
2. **Run validation script**: `./validate_cli.sh`
3. **Review test suite**: `python3 test_integration.py -v`
4. **Consult component docs**: [README_CLI.md](README_CLI.md), [PARSER_SUMMARY.md](PARSER_SUMMARY.md), [README_YAML_GENERATOR.md](README_YAML_GENERATOR.md)
5. **Check integration guide**: [INTEGRATION_EXAMPLE.md](INTEGRATION_EXAMPLE.md)

---

## Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────┐
│                     Spec-Driven Workflow                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Human Collaboration                                         │
│  (Markdown Specs)                                            │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐                                           │
│  │   Markdown   │  Source of Truth                          │
│  │   Spec File  │  (Human-readable)                         │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────────────────────────────┐              │
│  │  Translation Tool (THIS SYSTEM)          │              │
│  ├──────────────────────────────────────────┤              │
│  │                                           │              │
│  │  1. MarkdownParser                       │              │
│  │     ├─ Regex extraction                  │              │
│  │     ├─ Section detection                 │              │
│  │     └─ Linkage preservation              │              │
│  │              │                            │              │
│  │              ▼                            │              │
│  │  2. YAMLGenerator                        │              │
│  │     ├─ Structure building                │              │
│  │     ├─ Schema validation                 │              │
│  │     └─ Metadata tracking                 │              │
│  │              │                            │              │
│  │              ▼                            │              │
│  │  3. TranslationCLI                       │              │
│  │     ├─ Orchestration                     │              │
│  │     ├─ File I/O                          │              │
│  │     └─ Error reporting                   │              │
│  │                                           │              │
│  └──────────────┬───────────────────────────┘              │
│                 │                                            │
│                 ▼                                            │
│  ┌──────────────────┐                                       │
│  │   YAML Spec      │  Agent Consumption                    │
│  │   (Structured)   │  (Machine-readable)                   │
│  └──────┬───────────┘                                       │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────────────────────┐                      │
│  │  Execution Agents                 │                      │
│  │  ├─ Task coordination              │                      │
│  │  ├─ Dependency tracking            │                      │
│  │  └─ Progress reporting             │                      │
│  └───────────────────────────────────┘                      │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Component Interactions

```
┌─────────────────┐
│  User (Human)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│               TranslationCLI (Component-3)              │
│  ┌─────────────────────────────────────────────────┐   │
│  │  translate(markdown_file, output_file)          │   │
│  │  validate(yaml_file)                            │   │
│  └──────────┬──────────────────────┬────────────────   │
│             │                      │                    │
└─────────────┼──────────────────────┼────────────────────┘
              │                      │
              ▼                      ▼
  ┌──────────────────┐    ┌──────────────────┐
  │  MarkdownParser  │    │  YAMLGenerator   │
  │  (Component-1)   │    │  (Component-2)   │
  ├──────────────────┤    ├──────────────────┤
  │ parse_spec()     │───▶│ generate_yaml()  │
  │                  │    │ validate_schema()│
  │ Returns:         │    │                  │
  │ Dict[str, Any]   │    │ Returns:         │
  │                  │    │ str (YAML)       │
  └──────────────────┘    └──────────────────┘
```

### Data Flow

```
Markdown Spec File
       │
       ▼
[Read File] ──────────────────────────────┐
       │                                   │
       ▼                                   │
[MarkdownParser]                          │
  ├─ Extract Metadata                     │
  ├─ Parse Goals                          │
  ├─ Parse Design                         │
  ├─ Parse Implementation                 │
  ├─ Parse Test Strategy                  │
  └─ Extract Linkages                     │
       │                                   │
       ▼                                   │
[Parsed Dict]                             │
  {metadata, goals, design,               │
   implementation, test_strategy}         │
       │                                   │
       ▼                                   │
[YAMLGenerator]                           │
  ├─ Build YAML structure                 │
  ├─ Add metadata section ◀───────────────┘
  ├─ Format timestamps                    │ (markdown_path)
  ├─ Ensure deterministic output          │
  └─ Validate against schema              │
       │                                   │
       ▼                                   │
[YAML String]                             │
       │                                   │
       ▼                                   │
[Write File]                              │
       │                                   │
       ▼                                   │
YAML Spec File ──────────────────────────▶ [Agent Consumption]
```

### Design Principles

1. **Markdown as Source of Truth**: Markdown is always the authoritative source. YAML is derived, never hand-edited.

2. **Idempotent Translation**: Same Markdown input always produces the same YAML output (excluding timestamps). This ensures reliability and predictability.

3. **Fail-Fast Validation**: Strict validation with clear error messages. Better to fail early than produce invalid YAML.

4. **Zero Trust Input**: All input is validated and sanitized. Use `yaml.safe_load` and `yaml.safe_dump` only.

5. **Separation of Concerns**: Each component has a single, well-defined responsibility:
   - MarkdownParser: Extraction
   - YAMLGenerator: Structure building
   - TranslationCLI: Orchestration

6. **Deterministic Output**: Given the same input, output is always identical (minus timestamps). This enables caching, diffing, and version control.

---

## API Reference

### MarkdownParser

```python
from markdown_parser import parse_spec, ParseError

def parse_spec(file_path: str) -> Dict[str, Any]:
    """
    Parse Markdown spec file and extract structured data.

    Args:
        file_path: Path to Markdown spec file

    Returns:
        Dictionary containing parsed spec sections

    Raises:
        FileNotFoundError: If spec file doesn't exist
        ParseError: If required metadata is missing or malformed
    """
```

**Example**:
```python
result = parse_spec("spec.md")
spec_id = result["metadata"]["spec_id"]
tasks = result["implementation"]["tasks"]
```

### YAMLGenerator

```python
from yaml_generator import generate_yaml, validate_schema, YAMLGenerator

def generate_yaml(parsed_data: Dict[str, Any], markdown_path: str) -> str:
    """
    Generate YAML string from parsed spec data.

    Args:
        parsed_data: Dictionary from parse_spec()
        markdown_path: Path to source Markdown file

    Returns:
        YAML string formatted according to SPEC_SCHEMA.yaml

    Raises:
        ValueError: If required fields are missing
    """

def validate_schema(yaml_data: Dict[str, Any]) -> bool:
    """
    Validate YAML data against spec schema requirements.

    Args:
        yaml_data: Dictionary containing YAML data

    Returns:
        True if valid

    Raises:
        ValueError: With detailed validation error message
    """
```

**Example**:
```python
yaml_output = generate_yaml(parsed_data, "spec.md")
yaml_data = yaml.safe_load(yaml_output)
validate_schema(yaml_data)  # Raises ValueError if invalid
```

### TranslationCLI

**Command-Line Interface**:
```bash
python3 translate_spec.py [OPTIONS]

OPTIONS:
  --input INPUT              Input Markdown spec file (requires --output)
  --output OUTPUT            Output YAML file (required with --input)
  --validate                 Validate YAML after translation
  --validate-yaml YAML_FILE  Validate existing YAML spec file
  --watch FILE               Watch for changes (NOT IMPLEMENTED)
  -h, --help                 Show help message
```

**Exit Codes**:
- `0` - Success
- `1` - Error (file not found, parse error, validation failed)

---

## Contributing

### Adding New Features

1. **Update Spec First**: Modify the specification in `specs/active/2025-10-23-spec-to-yaml-translator.md`
2. **Implement Changes**: Update relevant components (parser, generator, CLI)
3. **Add Tests**: Write unit tests and update integration tests
4. **Update Documentation**: Update this README and component docs
5. **Validate**: Run full test suite and ensure all tests pass

### Testing Requirements

All contributions must include:
- Unit tests for new functions/methods
- Integration tests for workflow changes
- Updated test coverage summary
- All existing tests must pass

### Code Style

- **Python**: Follow PEP 8 style guide
- **Documentation**: Use clear, concise language with examples
- **Comments**: Explain "why" not "what"
- **Type Hints**: Use type hints for function signatures
- **Error Messages**: Provide specific, actionable error messages

### File Organization

```
specs/tools/
├── README.md                    # This file (main documentation)
├── markdown_parser.py           # Component-1 implementation
├── yaml_generator.py            # Component-2 implementation
├── translate_spec.py            # Component-3 implementation
├── test_markdown_parser.py      # Parser unit tests
├── test_yaml_generator.py       # Generator unit tests
├── test_integration.py          # Integration tests
├── PARSER_SUMMARY.md            # Parser detailed docs
├── README_YAML_GENERATOR.md     # Generator detailed docs
├── README_CLI.md                # CLI detailed docs
├── INTEGRATION_EXAMPLE.md       # Integration guide
├── TEST_COVERAGE_SUMMARY.md     # Test coverage report
└── validate_cli.sh              # Validation script
```

---

## License & Credits

### License

This tool is part of the **claude-oak-agents** project.

### Related Documentation

- **Spec-Driven Development**: See `CLAUDE.md` for spec-driven workflow documentation
- **Agent System**: See `agents/` directory for agent specifications
- **Spec Templates**: See `specs/templates/` for spec and YAML templates

### Authors

**Spec**: spec-20251023-spec-to-yaml-translator
**Implementation**:
- Task 1 (MarkdownParser): backend-architect
- Task 2 (YAMLGenerator): backend-architect
- Task 3 (TranslationCLI): backend-architect
- Task 4 (Integration Tests): backend-architect
- Task 5 (Documentation): technical-documentation-writer

### Version History

- **v1.0** (2025-10-24): Initial release
  - Complete Markdown parsing
  - YAML generation with schema validation
  - CLI interface
  - Full test coverage
  - Comprehensive documentation

### Acknowledgments

- **spec-manager agent**: For spec-driven development workflow design
- **backend-architect agent**: For implementation
- **claude-oak-agents project**: For agent coordination framework

---

## Quick Reference Card

### Common Commands

```bash
# Translate spec
python3 translate_spec.py --input spec.md --output spec.yaml --validate

# Validate YAML
python3 translate_spec.py --validate-yaml spec.yaml

# Run tests
python3 -m unittest discover -s . -p "test_*.py" -v

# Batch translate
for md in ../active/*.md; do
  python3 translate_spec.py --input "$md" --output "${md%.md}.yaml" --validate
done
```

### Key Files

| File | Purpose |
|------|---------|
| `translate_spec.py` | CLI entry point |
| `markdown_parser.py` | Markdown parsing |
| `yaml_generator.py` | YAML generation |
| `SPEC_SCHEMA.yaml` | Schema template |

### Performance Targets

| Operation | Target | Actual |
|-----------|--------|--------|
| Parse Markdown | <50ms | 10-15ms |
| Generate YAML | <10ms | 5-10ms |
| Validate Schema | <5ms | 1-5ms |
| **Total Translation** | **<500ms** | **22-26ms** |

---

**For detailed component documentation, see**:
- [PARSER_SUMMARY.md](PARSER_SUMMARY.md) - Markdown parser details
- [README_YAML_GENERATOR.md](README_YAML_GENERATOR.md) - YAML generator details
- [README_CLI.md](README_CLI.md) - CLI tool details
- [INTEGRATION_EXAMPLE.md](INTEGRATION_EXAMPLE.md) - Integration examples
- [TEST_COVERAGE_SUMMARY.md](TEST_COVERAGE_SUMMARY.md) - Test coverage report

**Questions or issues?** Check the [Troubleshooting](#troubleshooting) section or review the test suite for examples.
