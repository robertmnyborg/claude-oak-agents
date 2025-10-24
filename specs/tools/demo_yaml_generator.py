#!/usr/bin/env python3
"""
Demonstration script for YAML Generator

Shows how to use the YAML generator to convert parsed spec data to YAML format.
"""

import yaml
from yaml_generator import YAMLGenerator, generate_yaml, validate_schema


def main():
    """Demonstrate YAML generator functionality."""
    print("=" * 80)
    print("YAML Generator Demonstration")
    print("=" * 80)
    print()
    
    # Sample parsed spec data (would come from markdown_parser in real usage)
    sample_data = {
        "metadata": {
            "spec_id": "spec-20251023-demo-feature",
            "created": "2025-10-23T10:00:00Z",
            "updated": "2025-10-23T14:30:00Z",
            "status": "draft",
            "linked_request": "Create a demo feature for YAML generation"
        },
        "goals": {
            "primary": "Demonstrate YAML generation capabilities",
            "user_stories": [
                {
                    "id": "us-1",
                    "role": "developer",
                    "capability": "convert specs to YAML",
                    "benefit": "agents can consume structured data"
                }
            ],
            "acceptance_criteria": [
                {
                    "id": "ac-1",
                    "criterion": "Generate valid YAML from parsed data",
                    "status": "pending",
                    "linked_tasks": ["task-1"],
                    "linked_tests": ["tc-1"]
                },
                {
                    "id": "ac-2",
                    "criterion": "Validate YAML against schema",
                    "status": "pending",
                    "linked_tasks": ["task-1"],
                    "linked_tests": ["tc-2"]
                }
            ],
            "success_metrics": [
                {
                    "metric": "Translation accuracy",
                    "target": "100%",
                    "measured_value": None
                }
            ],
            "out_of_scope": [
                "Reverse translation (YAML → Markdown)"
            ]
        },
        "design": {
            "architecture": {
                "overview": "Python-based YAML generator using PyYAML library",
                "key_decisions": [
                    {
                        "decision": "Use PyYAML for YAML generation",
                        "rationale": "Standard library, secure safe_dump, wide adoption"
                    }
                ]
            },
            "components": [
                {
                    "id": "comp-1",
                    "name": "YAMLGenerator",
                    "location": "specs/tools/yaml_generator.py",
                    "responsibility": "Generate YAML from parsed spec data",
                    "interfaces": ["generate_yaml()", "validate_schema()"],
                    "dependencies": ["pyyaml", "jsonschema"],
                    "links_to": {
                        "goals": ["ac-1", "ac-2"],
                        "tasks": ["task-1"]
                    }
                }
            ],
            "dependencies": [
                {
                    "name": "pyyaml",
                    "version": "6.0+",
                    "reason": "YAML parsing and generation",
                    "type": "pip"
                }
            ],
            "security_considerations": [],
            "performance_considerations": []
        },
        "implementation": {
            "tasks": [
                {
                    "id": "task-1",
                    "name": "Implement YAML Generator",
                    "description": "Build YAML structure generator with validation",
                    "agent": "backend-architect",
                    "files": ["specs/tools/yaml_generator.py"],
                    "depends_on": [],
                    "estimate": "simple",
                    "status": "completed",
                    "links_to": {
                        "design": ["comp-1"],
                        "goals": ["ac-1", "ac-2"],
                        "tests": ["tc-1", "tc-2"]
                    }
                }
            ],
            "execution_sequence": [
                {
                    "stage": 1,
                    "parallel": False,
                    "tasks": ["task-1"]
                }
            ],
            "risks": []
        },
        "test_strategy": {
            "test_cases": [
                {
                    "id": "tc-1",
                    "name": "Generate valid YAML",
                    "description": "Test YAML generation produces valid output",
                    "given": "Parsed spec data",
                    "when": "Generate YAML",
                    "then": "Output is valid YAML following schema",
                    "links_to": {
                        "goals": ["ac-1"],
                        "design": ["comp-1"],
                        "tasks": ["task-1"]
                    },
                    "status": "passed",
                    "test_type": "unit"
                },
                {
                    "id": "tc-2",
                    "name": "Idempotent translation",
                    "description": "Same input produces same output",
                    "given": "Parsed spec data",
                    "when": "Generate YAML twice",
                    "then": "Both outputs are identical (except timestamp)",
                    "links_to": {
                        "goals": ["ac-2"],
                        "design": ["comp-1"],
                        "tasks": ["task-1"]
                    },
                    "status": "passed",
                    "test_type": "unit"
                }
            ],
            "test_types": {
                "unit_tests": [
                    {"test": "YAML generation tests", "status": "passed"}
                ],
                "integration_tests": [],
                "e2e_tests": [],
                "performance_tests": []
            },
            "validation_checklist": []
        }
    }
    
    markdown_path = "specs/active/demo-spec.md"
    
    print("Step 1: Generate YAML from parsed data")
    print("-" * 80)
    
    # Generate YAML
    generator = YAMLGenerator()
    yaml_output = generator.generate_yaml(sample_data, markdown_path)
    
    print(f"Generated YAML ({len(yaml_output)} bytes):")
    print()
    print(yaml_output[:500] + "...\n")  # Show first 500 chars
    
    print("Step 2: Validate generated YAML")
    print("-" * 80)
    
    # Parse YAML back to validate it's valid
    yaml_data = yaml.safe_load(yaml_output)
    
    try:
        is_valid = generator.validate_schema(yaml_data)
        print(f"✓ Schema validation: {'PASSED' if is_valid else 'FAILED'}")
    except ValueError as e:
        print(f"✗ Schema validation FAILED: {e}")
        return
    
    print()
    print("Step 3: Verify metadata section")
    print("-" * 80)
    
    metadata = yaml_data["metadata"]
    print(f"Spec Version: {metadata['spec_version']}")
    print(f"Generated from Markdown: {metadata['generated_from_markdown']}")
    print(f"Markdown Location: {metadata['markdown_location']}")
    print(f"Last Sync: {metadata['last_sync']}")
    
    print()
    print("Step 4: Test idempotency")
    print("-" * 80)
    
    # Generate twice and compare
    yaml_output_1 = generator.generate_yaml(sample_data, markdown_path)
    yaml_output_2 = generator.generate_yaml(sample_data, markdown_path)
    
    data_1 = yaml.safe_load(yaml_output_1)
    data_2 = yaml.safe_load(yaml_output_2)
    
    # Normalize timestamps for comparison
    data_1["metadata"]["last_sync"] = "NORMALIZED"
    data_2["metadata"]["last_sync"] = "NORMALIZED"
    
    if data_1 == data_2:
        print("✓ Idempotency test: PASSED")
        print("  Same input produces identical output (excluding timestamp)")
    else:
        print("✗ Idempotency test: FAILED")
    
    print()
    print("Step 5: Test convenience functions")
    print("-" * 80)
    
    # Test module-level convenience functions
    yaml_conv = generate_yaml(sample_data, markdown_path)
    yaml_conv_data = yaml.safe_load(yaml_conv)
    
    try:
        validate_schema(yaml_conv_data)
        print("✓ Convenience functions: WORKING")
    except ValueError:
        print("✗ Convenience functions: FAILED")
    
    print()
    print("=" * 80)
    print("Demonstration complete!")
    print("=" * 80)
    print()
    print("Summary:")
    print("  - YAML generation: ✓")
    print("  - Schema validation: ✓")
    print("  - Metadata tracking: ✓")
    print("  - Idempotent translation: ✓")
    print("  - Convenience functions: ✓")
    print()


if __name__ == "__main__":
    main()
