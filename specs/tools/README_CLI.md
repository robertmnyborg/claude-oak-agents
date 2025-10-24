# Spec Translation CLI Tool

Command-line interface for translating Markdown specifications to YAML format.

**Component**: TranslationCLI (Section 2.2.Component-3)  
**Acceptance Criteria**: AC-5, AC-6  
**Task**: task-3 (spec-20251023-spec-to-yaml-translator)

## Overview

The `translate_spec.py` CLI tool orchestrates the Markdown parser and YAML generator to provide a seamless translation workflow. It supports three operation modes:

1. **Translation Mode**: Convert Markdown specs to YAML
2. **Validation Mode**: Validate existing YAML specs
3. **Watch Mode**: Auto-regenerate on changes (NOT IMPLEMENTED)

## Installation

No installation required - Python 3.9+ with standard library.

**Dependencies**:
- `markdown_parser.py` - Markdown parsing functionality
- `yaml_generator.py` - YAML generation and validation
- `pyyaml` - YAML processing library

## Usage

### Translation Mode

Translate a Markdown spec to YAML format:

```bash
python3 translate_spec.py --input spec.md --output spec.yaml
```

Translate with validation:

```bash
python3 translate_spec.py --input spec.md --output spec.yaml --validate
```

**Example**:
```bash
python3 translate_spec.py \
  --input ../active/2025-10-23-feature.md \
  --output ../active/2025-10-23-feature.yaml \
  --validate
```

**Output**:
```
📄 Parsing Markdown spec: ../active/2025-10-23-feature.md
✅ Successfully parsed 5 sections
🔧 Generating YAML structure...
🔍 Validating YAML schema...
✅ YAML validation passed
✅ Successfully translated to: ../active/2025-10-23-feature.yaml
📊 Metadata tracked:
   - Source: ../active/2025-10-23-feature.md
   - Generated: ../active/2025-10-23-feature.yaml
   - Timestamp: 2025-10-24T05:45:59.357238Z
```

### Validation Mode

Validate an existing YAML spec:

```bash
python3 translate_spec.py --validate-yaml spec.yaml
```

**Example**:
```bash
python3 translate_spec.py --validate-yaml ../active/2025-10-23-feature.yaml
```

**Output**:
```
📄 Loading YAML file: ../active/2025-10-23-feature.yaml
🔍 Validating YAML schema...
✅ YAML validation passed
📊 Spec metadata:
   - Spec ID: spec-20251023-feature
   - Status: in-progress
   - Last sync: 2025-10-24T05:45:59.357238Z
   - Source: ../active/2025-10-23-feature.md
```

### Watch Mode (Not Implemented)

Watch for file changes and auto-regenerate:

```bash
python3 translate_spec.py --watch spec.md
```

**Status**: NOT IMPLEMENTED - Requires `watchdog` library.  
For now, manually re-run translation after making changes.

## Command-Line Options

```
usage: translate_spec.py [-h]
                         (--input INPUT | --validate-yaml VALIDATE_YAML | --watch WATCH)
                         [--output OUTPUT] [--validate]

Translate Markdown specs to YAML format

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         Input Markdown spec file (requires --output)
  --validate-yaml VALIDATE_YAML
                        Validate existing YAML spec file
  --watch WATCH         Watch Markdown file for changes (NOT IMPLEMENTED)
  --output OUTPUT       Output YAML file (required with --input)
  --validate            Validate YAML after translation
```

## Workflow

### Translation Workflow

1. **Parse Markdown**: Extract structured data using `parse_spec()`
2. **Generate YAML**: Build YAML structure using `generate_yaml()`
3. **Validate (Optional)**: Validate against schema using `validate_schema()`
4. **Write Output**: Save YAML to specified output file
5. **Report Success**: Display metadata and confirmation

### Validation Workflow

1. **Load YAML**: Read YAML file from disk
2. **Validate Schema**: Check required fields and structure
3. **Report Results**: Display validation status and metadata

## Metadata Tracking

The tool automatically tracks metadata for incremental updates:

**Metadata Fields**:
- `last_sync`: ISO 8601 timestamp of last translation
- `markdown_location`: Path to source Markdown file
- `generated_from_markdown`: Boolean flag (always `true`)
- `spec_version`: Schema version used (currently `1.0`)

**Example Metadata**:
```yaml
metadata:
  spec_version: '1.0'
  generated_from_markdown: true
  markdown_location: ../active/2025-10-23-feature.md
  last_sync: '2025-10-24T05:45:59.357238Z'
  statistics:
    total_tasks: 0
    completed_tasks: 0
    total_tests: 0
    passed_tests: 0
    agents_involved: []
    duration_seconds: null
```

## Error Handling

The CLI provides clear error messages for common issues:

**File Not Found**:
```
❌ Error: File not found - Spec file not found: nonexistent.md
```

**Parse Error**:
```
❌ Error: Failed to parse Markdown - Missing required metadata: Spec ID
```

**Validation Error**:
```
❌ Error: Validation failed - YAML validation failed:
  - Missing required field: created
  - Missing required section: goals
```

**Exit Codes**:
- `0` - Success
- `1` - Error (file not found, parse error, validation failed)

## Testing

### Run Unit Tests

```bash
python3 test_cli.py -v
```

**Coverage**:
- TC-6: CLI End-to-End Translation
- TC-7: Metadata Tracking
- Error handling and edge cases
- Argument validation
- Unicode support

### Validate Installation

```bash
./validate_cli.sh
```

**Checks**:
- CLI tool exists and is executable
- Help command works
- Unit tests pass
- Translation works with actual spec
- Validation works with generated YAML

## File Structure

```
specs/tools/
├── translate_spec.py       # CLI entry point
├── test_cli.py            # CLI test suite
├── validate_cli.sh        # Validation script
├── markdown_parser.py     # Markdown parsing (dependency)
├── yaml_generator.py      # YAML generation (dependency)
└── README_CLI.md          # This file
```

## Examples

### Basic Translation

```bash
# Translate spec to YAML
python3 translate_spec.py \
  --input ../active/my-feature.md \
  --output ../active/my-feature.yaml

# Validate the result
python3 translate_spec.py --validate-yaml ../active/my-feature.yaml
```

### Translation with Validation

```bash
# Translate and validate in one command
python3 translate_spec.py \
  --input ../active/my-feature.md \
  --output ../active/my-feature.yaml \
  --validate
```

### Batch Translation

```bash
# Translate all specs in active directory
for md_file in ../active/*.md; do
  yaml_file="${md_file%.md}.yaml"
  echo "Translating $md_file → $yaml_file"
  python3 translate_spec.py --input "$md_file" --output "$yaml_file" --validate
done
```

### Incremental Updates

When you update a Markdown spec, simply re-run the translation:

```bash
# Edit Markdown spec
vim ../active/my-feature.md

# Regenerate YAML (metadata tracks last sync)
python3 translate_spec.py \
  --input ../active/my-feature.md \
  --output ../active/my-feature.yaml \
  --validate
```

The `last_sync` timestamp in the YAML metadata will be updated automatically.

## Integration with Spec-Driven Workflow

### spec-manager Integration

The `spec-manager` agent uses this CLI tool to:

1. Auto-generate YAML from user-approved Markdown specs
2. Track metadata for incremental updates
3. Validate YAML before agent consumption
4. Regenerate YAML when Markdown changes

### Agent Consumption

Execution agents consume the generated YAML:

```python
import yaml

# Load generated YAML spec
with open('spec.yaml') as f:
    spec = yaml.safe_load(f)

# Access structured data
tasks = spec['implementation']['tasks']
for task in tasks:
    if task['agent'] == 'backend-architect':
        execute_task(task)
```

## Known Limitations

1. **Watch Mode Not Implemented**: Requires `watchdog` library. Currently must manually re-run translation.
2. **No Reverse Translation**: YAML → Markdown not supported (Markdown is source of truth).
3. **No Spec Generation**: Cannot auto-generate specs from code (manual authoring required).

## Future Enhancements

- [ ] Implement watch mode with `watchdog` library
- [ ] Add diff output for incremental updates
- [ ] Support parallel translation of multiple specs
- [ ] Add dry-run mode (validate without writing)
- [ ] Integration with git hooks (auto-translate on commit)

## Troubleshooting

**Problem**: `python: command not found`  
**Solution**: Use `python3` instead of `python`

**Problem**: `Import Error: No module named 'yaml'`  
**Solution**: Install PyYAML: `pip3 install pyyaml`

**Problem**: Parse error on valid Markdown  
**Solution**: Check that spec follows template structure with required metadata fields

**Problem**: Validation fails on generated YAML  
**Solution**: Ensure Markdown spec has all required sections (Goals, Design, Implementation, Tests)

## See Also

- [Markdown Parser README](README.md) - Markdown parsing documentation
- [YAML Generator README](README_YAML_GENERATOR.md) - YAML generation documentation
- [Parser Summary](PARSER_SUMMARY.md) - Parser implementation details
- [Integration Example](INTEGRATION_EXAMPLE.md) - Full translation example

## Support

For issues or questions:
1. Check error messages for specific failure reasons
2. Run validation script: `./validate_cli.sh`
3. Review test suite: `python3 test_cli.py -v`
4. Consult integration documentation
