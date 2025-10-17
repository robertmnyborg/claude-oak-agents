# Migration Guide: Single-File to Multi-File Agents

This guide explains how to migrate existing single-file agents to the new multi-file package format with bundled scripts and enhanced metadata.

## When to Migrate

✅ **Migrate when**:
- Agent would benefit from bundled executable scripts
- Extensive reference documentation is needed
- Code templates are valuable for users
- Agent complexity is high (>500 lines)
- Multiple utility scripts would improve efficiency

❌ **Keep single-file when**:
- Agent is simple (<200 lines)
- No scripts or reference materials needed
- Agent is instruction-only
- Minimal complexity

## Migration Steps

### Step 1: Create Multi-File Structure

```bash
# Example: Migrating security-auditor

# 1. Create agent directory
mkdir -p agents/security-auditor/{scripts,reference,templates}

# 2. Move existing agent file
mv agents/security-auditor.md agents/security-auditor/agent.md

# 3. Extract metadata
python3 core/agent_loader.py --command=extract-metadata \
  --agent=security-auditor \
  --output=agents/security-auditor/metadata.yaml
```

### Step 2: Enhance Metadata

Edit `metadata.yaml` to add discovery triggers and capabilities:

```yaml
# Agent Identity
name: security-auditor
version: 2.0.0  # Increment from 1.0.0
description: |
  Comprehensive security analysis specialist...

# Discovery Metadata (NEW - critical for dynamic discovery)
triggers:
  keywords:
    - security
    - vulnerability
    - audit
    - compliance
    # Add 5-15 keywords for best discovery
  file_patterns:
    - "*.security"
    - "security.yml"
    - "**/security/**"
    # Add file patterns that indicate agent relevance
  domains:
    - security
    - compliance
    - penetration-testing

# Agent Classification
category: quality-security  # See categories below
priority: high  # low, medium, high, critical
blocking: true  # Can block commits?
parallel_compatible:  # Agents that can run in parallel
  - code-reviewer
  - dependency-scanner

# Capabilities (NEW - for ML-powered recommendations)
capabilities:
  - vulnerability_detection
  - compliance_validation
  - penetration_testing
  - threat_modeling

# ... rest of metadata
```

### Step 3: Add Bundled Scripts (Optional)

Create executable scripts in `scripts/` directory:

```bash
# Example: dependency scanner
cat > agents/security-auditor/scripts/dependency_scan.py <<'EOF'
#!/usr/bin/env python3
"""
Fast dependency vulnerability scanner
"""

import json
import sys
import argparse

# ... script implementation ...

if __name__ == "__main__":
    main()
EOF

chmod +x agents/security-auditor/scripts/dependency_scan.py
```

### Step 4: Update metadata.yaml with Script Specs

```yaml
scripts:
  - name: dependency_scan
    runtime: python
    entrypoint: scripts/dependency_scan.py
    description: Fast CVE scanning for dependencies
    required_packages:
      - requests>=2.28.0
      - packaging>=21.0
    python_version: ">=3.8"

    parameters:
      - name: scan_depth
        type: string
        default: "deep"
        options: [shallow, medium, deep]

    outputs:
      - type: json
        schema: cve_report_v1
      - type: markdown
```

### Step 5: Add Reference Documentation (Optional)

```bash
# Add reference materials
cat > agents/security-auditor/reference/owasp_top_10.md <<'EOF'
# OWASP Top 10 Security Risks

## 1. Broken Access Control
...
EOF
```

### Step 6: Add Templates (Optional)

```bash
# Add code templates
cat > agents/security-auditor/templates/security_test.py.template <<'EOF'
#!/usr/bin/env python3
"""
Security test template for {{package_name}}
"""

import pytest

def test_authentication():
    """Test authentication mechanisms"""
    # TODO: Implement
    pass
EOF
```

### Step 7: Test Migration

```bash
# Test metadata loading
python3 core/agent_loader.py --command=metadata --agents-dir=agents \
  | jq '.security_auditor'

# Test full agent loading
python3 core/agent_loader.py --command=load --agents-dir=agents \
  --agent=security-auditor

# Test script execution
cd agents/security-auditor
python3 scripts/dependency_scan.py --directory=. --output-format=markdown
```

### Step 8: Update Telemetry (Automatic)

The system will automatically update metrics in `metadata.yaml`:

```yaml
metrics:
  avg_duration_seconds: 45.2
  success_rate: 0.94
  quality_score: 4.6
  invocation_count: 127
  last_updated: "2025-10-16T10:30:00Z"
```

## Agent Categories

Choose the appropriate category:

- `core-development` - frontend, backend, mobile, blockchain, ml
- `quality-security` - security auditor, dependency scanner
- `quality-testing` - unit test expert, qa specialist
- `infrastructure-operations` - infrastructure specialist, systems architect
- `analysis-planning` - business analyst, data scientist, project manager
- `documentation-content` - technical writer, content writer
- `special-purpose` - agent creator, debug specialist, general purpose

## Script Development Guidelines

### 1. Script Structure

```python
#!/usr/bin/env python3
"""
Script description - what it does and why it's faster than token generation
"""

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="...")
    parser.add_argument("--param", help="...")
    args = parser.parse_args()

    # Implementation
    result = perform_task(args)

    # Output (JSON for machine parsing)
    print(json.dumps(result, indent=2))

    # Exit code (0 = success, 1+ = failure)
    sys.exit(0 if result['success'] else 1)

if __name__ == "__main__":
    main()
```

### 2. Efficiency Requirements

Scripts should be 10-100x faster than token generation:

| Task | Token Generation | Script Execution | Speedup |
|------|------------------|------------------|---------|
| Sort 10K items | ~5s, 50K tokens | ~0.05s, 0 tokens | 100x |
| Parse 1MB JSON | ~10s, 100K tokens | ~0.1s, 0 tokens | 100x |
| CVE scan (100 deps) | ~30s, 200K tokens | ~2s, 0 tokens | 15x |
| Secret detection | ~15s, 80K tokens | ~0.5s, 0 tokens | 30x |

### 3. Error Handling

```python
try:
    result = risky_operation()
    return {"success": True, "data": result}
except SpecificError as e:
    return {"success": False, "error": str(e), "suggestion": "..."}
except Exception as e:
    return {"success": False, "error": f"Unexpected: {e}"}
```

### 4. Output Formats

Support multiple output formats:

```python
def generate_output(data, format='json'):
    if format == 'json':
        return json.dumps(data, indent=2)
    elif format == 'markdown':
        return generate_markdown_report(data)
    elif format == 'sarif':  # For CI/CD integration
        return generate_sarif(data)
```

## Reference Documentation Best Practices

### Structure

```
reference/
  overview.md           # High-level concept
  methodology.md        # Detailed methodology
  examples.md           # Code examples
  checklists.md         # Quick reference checklists
  mappings.yaml         # Data mappings (CWE, CVE, etc.)
```

### Content Guidelines

- **Concise**: Each doc <500 lines
- **Actionable**: Specific guidance, not theory
- **Examples**: Code samples for each concept
- **Updated**: Keep synchronized with main agent

## Template Best Practices

### Template Variables

Use `{{variable_name}}` syntax:

```python
# templates/security_test.py.template
def test_{{function_name}}_authentication():
    """Test authentication for {{function_name}}"""
    client = {{client_class}}()
    # Test implementation
```

### Template Categories

- **Test templates**: Unit test, integration test, security test
- **Configuration templates**: Security configs, compliance configs
- **Documentation templates**: Security reports, compliance reports
- **Code templates**: Secure implementations, best practices

## Backward Compatibility

Single-file agents continue to work without migration:

```python
# Agent loader supports both formats
def load_agent(agent_path):
    if agent_path.is_dir():
        # Multi-file format
        return load_multi_file(agent_path)
    elif agent_path.suffix == '.md':
        # Single-file format (legacy)
        return load_single_file(agent_path)
```

## Migration Checklist

- [ ] Created multi-file directory structure
- [ ] Moved agent.md to new location
- [ ] Created metadata.yaml with:
  - [ ] Version incremented to 2.0.0+
  - [ ] Comprehensive trigger keywords (5-15)
  - [ ] File patterns for auto-detection
  - [ ] Domain classifications
  - [ ] Capabilities list
  - [ ] Coordination patterns
- [ ] Added bundled scripts (if applicable):
  - [ ] Scripts are executable (chmod +x)
  - [ ] Scripts have shebang line
  - [ ] Scripts include argparse interface
  - [ ] Scripts output JSON
  - [ ] Scripts registered in metadata.yaml
- [ ] Added reference documentation (if applicable)
- [ ] Added templates (if applicable)
- [ ] Tested metadata loading
- [ ] Tested agent loading
- [ ] Tested script execution
- [ ] Verified backward compatibility
- [ ] Updated agent invocation patterns (if needed)

## Troubleshooting

### "Agent not found" error

```bash
# Check agent directory structure
ls -la agents/security-auditor/

# Should show:
# - agent.md (required)
# - metadata.yaml (required)
# - scripts/ (optional)
# - reference/ (optional)
# - templates/ (optional)
```

### "Script execution failed"

```bash
# Check script permissions
ls -l agents/security-auditor/scripts/

# Make executable if needed
chmod +x agents/security-auditor/scripts/*.py

# Test script directly
python3 agents/security-auditor/scripts/dependency_scan.py --help
```

### "Metadata parsing error"

```bash
# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('agents/security-auditor/metadata.yaml'))"

# Common issues:
# - Missing required fields (name, description, triggers)
# - Invalid YAML syntax (indentation, colons)
# - Unsupported field values
```

## Examples

See these reference implementations:

- [agents/security-auditor-multifile/](../agents/security-auditor-multifile/) - Complete example with scripts, reference docs, and templates
- [agents/performance-optimizer/](../agents/performance-optimizer/) - Multi-file with profiling scripts (if exists)
- [agents/frontend-developer.md](../agents/frontend-developer.md) - Single-file example (still valid)

## Migration Script

Automated migration helper:

```bash
#!/bin/bash
# migrate_agent.sh - Automate agent migration

AGENT_NAME=$1

if [ -z "$AGENT_NAME" ]; then
  echo "Usage: ./migrate_agent.sh <agent-name>"
  exit 1
fi

echo "Migrating $AGENT_NAME to multi-file format..."

# Create structure
mkdir -p "agents/$AGENT_NAME"/{scripts,reference,templates}

# Move agent file
if [ -f "agents/$AGENT_NAME.md" ]; then
  mv "agents/$AGENT_NAME.md" "agents/$AGENT_NAME/agent.md"
  echo "✓ Moved agent definition"
fi

# Extract metadata (if extractor exists)
if [ -f "core/extract_metadata.py" ]; then
  python3 core/extract_metadata.py "agents/$AGENT_NAME/agent.md" \
    > "agents/$AGENT_NAME/metadata.yaml"
  echo "✓ Extracted metadata"
else
  # Create minimal metadata
  cat > "agents/$AGENT_NAME/metadata.yaml" <<EOF
name: $AGENT_NAME
version: 2.0.0
description: "TODO: Add description"

triggers:
  keywords: []
  file_patterns: []
  domains: []

category: special-purpose
priority: medium
blocking: false
parallel_compatible: []
capabilities: []

tools: [Write, Edit, Read, Bash, Grep, Glob]
model: sonnet

auto_created: false
created_by: human
created_at: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
EOF
  echo "✓ Created metadata template (TODO: Fill in triggers and capabilities)"
fi

echo ""
echo "Migration complete! Next steps:"
echo "1. Edit agents/$AGENT_NAME/metadata.yaml - add triggers and capabilities"
echo "2. Add bundled scripts to agents/$AGENT_NAME/scripts/ (optional)"
echo "3. Add reference docs to agents/$AGENT_NAME/reference/ (optional)"
echo "4. Test with: python3 core/agent_loader.py --command=load --agent=$AGENT_NAME"
```

Save as `scripts/migrate_agent.sh` and use:

```bash
chmod +x scripts/migrate_agent.sh
./scripts/migrate_agent.sh security-auditor
```

## Next Steps

After migration:

1. **Test thoroughly**: Verify agent works in both classification and execution
2. **Monitor telemetry**: Check if performance improves with bundled scripts
3. **Gather feedback**: See if scripts provide value
4. **Iterate**: Refine triggers, add more scripts, update documentation
5. **Share**: Contribute successful patterns back to community

## Support

- [Multi-File Agents Documentation](MULTI_FILE_AGENTS.md)
- [Agent Loader Source](../core/agent_loader.py)
- [Example Agents](../agents/)
- [GitHub Issues](https://github.com/robertmnyborg/claude-oak-agents/issues)
