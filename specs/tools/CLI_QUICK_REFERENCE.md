# CLI Quick Reference Card

**Component**: TranslationCLI  
**Location**: `specs/tools/translate_spec.py`

## Quick Start

```bash
# Translate Markdown to YAML
python3 translate_spec.py --input spec.md --output spec.yaml

# Translate with validation
python3 translate_spec.py --input spec.md --output spec.yaml --validate

# Validate existing YAML
python3 translate_spec.py --validate-yaml spec.yaml
```

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `--input <file>` | Input Markdown spec | `--input spec.md` |
| `--output <file>` | Output YAML file | `--output spec.yaml` |
| `--validate` | Validate after translation | `--validate` |
| `--validate-yaml <file>` | Validate existing YAML | `--validate-yaml spec.yaml` |
| `--watch <file>` | Watch for changes (NOT IMPLEMENTED) | `--watch spec.md` |
| `--help` | Show help message | `--help` |

## Common Workflows

### Initial Translation
```bash
python3 translate_spec.py \
  --input ../active/my-feature.md \
  --output ../active/my-feature.yaml \
  --validate
```

### Incremental Update
```bash
# Edit Markdown spec
vim ../active/my-feature.md

# Regenerate YAML (updates last_sync timestamp)
python3 translate_spec.py \
  --input ../active/my-feature.md \
  --output ../active/my-feature.yaml \
  --validate
```

### Validation Only
```bash
python3 translate_spec.py --validate-yaml ../active/my-feature.yaml
```

### Batch Translation
```bash
for md in ../active/*.md; do
  yaml="${md%.md}.yaml"
  python3 translate_spec.py --input "$md" --output "$yaml" --validate
done
```

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Error (file not found, parse error, validation failed) |

## Output Messages

### Success
```
✅ Successfully translated to: spec.yaml
✅ YAML validation passed
```

### Error
```
❌ Error: File not found - spec.md
❌ Error: Failed to parse Markdown - Missing required metadata
❌ Error: Validation failed - Missing required field: created
```

## Testing

```bash
# Run unit tests
python3 test_cli.py -v

# Run validation script
./validate_cli.sh
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `python: command not found` | Use `python3` instead |
| `No module named 'yaml'` | Install: `pip3 install pyyaml` |
| Parse error | Check spec has required metadata |
| Validation fails | Ensure all required sections present |

## Files

| File | Purpose |
|------|---------|
| `translate_spec.py` | CLI implementation |
| `test_cli.py` | Unit tests (15 tests) |
| `validate_cli.sh` | Validation script |
| `README_CLI.md` | Full documentation |
| `CLI_SUMMARY.md` | Implementation summary |

## Dependencies

- `markdown_parser.py` - Markdown parsing
- `yaml_generator.py` - YAML generation
- `pyyaml` - YAML library

## Metadata Tracked

```yaml
metadata:
  spec_version: '1.0'
  generated_from_markdown: true
  markdown_location: ../active/spec.md
  last_sync: '2025-10-24T05:45:59.357238Z'
```

## Help

```bash
python3 translate_spec.py --help
```

## See Also

- [CLI README](README_CLI.md) - Full documentation
- [Parser README](README.md) - Markdown parser docs
- [Generator README](README_YAML_GENERATOR.md) - YAML generator docs
- [Integration Example](INTEGRATION_EXAMPLE.md) - Full example
