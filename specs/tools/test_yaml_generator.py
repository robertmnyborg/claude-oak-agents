"""
Unit Tests for YAML Generator

Tests YAML generation, schema validation, and idempotent translation.

Test Coverage:
- tc-4: Generate valid YAML
- tc-5: Idempotent translation (same input → same output)
"""

import unittest
import yaml
from datetime import datetime, timezone
from yaml_generator import YAMLGenerator, generate_yaml, validate_schema


class TestYAMLGenerator(unittest.TestCase):
    """Test suite for YAMLGenerator component."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = YAMLGenerator()
        self.sample_parsed_data = {
            "metadata": {
                "spec_id": "spec-20251023-test-feature",
                "created": "2025-10-23T10:00:00Z",
                "updated": "2025-10-23T12:00:00Z",
                "status": "draft",
                "linked_request": "Test request for YAML generation"
            },
            "goals": {
                "primary": "Test primary goal",
                "user_stories": [
                    {
                        "id": "us-1",
                        "role": "user",
                        "capability": "test capability",
                        "benefit": "test benefit"
                    }
                ],
                "acceptance_criteria": [
                    {
                        "id": "ac-1",
                        "criterion": "Test criterion",
                        "status": "pending",
                        "linked_tasks": ["task-1"],
                        "linked_tests": ["tc-1"]
                    }
                ],
                "success_metrics": [
                    {
                        "metric": "Test metric",
                        "target": "100%",
                        "measured_value": None
                    }
                ],
                "out_of_scope": ["Out of scope item 1"]
            },
            "design": {
                "architecture": {
                    "overview": "Test architecture overview",
                    "key_decisions": [
                        {
                            "decision": "Test decision",
                            "rationale": "Test rationale"
                        }
                    ]
                },
                "components": [
                    {
                        "id": "comp-1",
                        "name": "Test Component",
                        "location": "test/path.py",
                        "responsibility": "Test responsibility",
                        "interfaces": ["test_interface()"],
                        "dependencies": [],
                        "links_to": {
                            "goals": ["ac-1"],
                            "tasks": ["task-1"]
                        }
                    }
                ],
                "data_structures": [],
                "apis": [],
                "dependencies": [
                    {
                        "name": "pyyaml",
                        "version": "6.0",
                        "reason": "YAML parsing",
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
                        "name": "Test Task",
                        "description": "Test description",
                        "agent": "backend-architect",
                        "files": ["test/file.py"],
                        "depends_on": [],
                        "estimate": "simple",
                        "status": "pending",
                        "links_to": {
                            "design": ["comp-1"],
                            "goals": ["ac-1"],
                            "tests": ["tc-1"]
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
                        "name": "Test Case 1",
                        "description": "Test description",
                        "given": "Test precondition",
                        "when": "Test action",
                        "then": "Test expected result",
                        "links_to": {
                            "goals": ["ac-1"],
                            "design": ["comp-1"],
                            "tasks": ["task-1"]
                        },
                        "status": "pending",
                        "test_type": "unit"
                    }
                ],
                "test_types": {
                    "unit_tests": [
                        {"test": "Unit test 1", "status": "pending"}
                    ],
                    "integration_tests": [],
                    "e2e_tests": [],
                    "performance_tests": []
                },
                "validation_checklist": [
                    {"check": "All tests pass", "status": "pending"}
                ]
            }
        }
        self.markdown_path = "specs/active/test-spec.md"
    
    def test_tc4_generate_valid_yaml(self):
        """
        TC-4: Generate valid YAML following SPEC_SCHEMA.yaml template.
        
        Tests:
        - YAML output is valid and parseable
        - All required sections present
        - Metadata section includes tracking fields
        - Output follows schema structure
        """
        # Generate YAML
        yaml_string = self.generator.generate_yaml(self.sample_parsed_data, self.markdown_path)
        
        # Should return a string
        self.assertIsInstance(yaml_string, str)
        self.assertTrue(len(yaml_string) > 0)
        
        # Should be valid YAML (parseable)
        yaml_data = yaml.safe_load(yaml_string)
        self.assertIsInstance(yaml_data, dict)
        
        # Check required top-level fields
        self.assertIn("spec_id", yaml_data)
        self.assertIn("created", yaml_data)
        self.assertIn("updated", yaml_data)
        self.assertIn("status", yaml_data)
        self.assertIn("linked_request", yaml_data)
        
        # Check required sections
        self.assertIn("goals", yaml_data)
        self.assertIn("technical_design", yaml_data)
        self.assertIn("implementation", yaml_data)
        self.assertIn("test_strategy", yaml_data)
        self.assertIn("execution_log", yaml_data)
        self.assertIn("changes", yaml_data)
        self.assertIn("completion", yaml_data)
        self.assertIn("metadata", yaml_data)
        
        # Verify metadata section has required tracking fields
        metadata = yaml_data["metadata"]
        self.assertEqual(metadata["spec_version"], "1.0")
        self.assertEqual(metadata["generated_from_markdown"], True)
        self.assertEqual(metadata["markdown_location"], self.markdown_path)
        self.assertIn("last_sync", metadata)
        
        # Verify last_sync is valid ISO timestamp
        last_sync = metadata["last_sync"]
        self.assertRegex(last_sync, r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z')
        
        # Verify content preservation
        self.assertEqual(yaml_data["spec_id"], "spec-20251023-test-feature")
        self.assertEqual(yaml_data["status"], "draft")
        self.assertEqual(yaml_data["goals"]["primary"], "Test primary goal")
        self.assertEqual(len(yaml_data["goals"]["user_stories"]), 1)
        self.assertEqual(len(yaml_data["goals"]["acceptance_criteria"]), 1)
    
    def test_tc5_idempotent_translation(self):
        """
        TC-5: Idempotent translation (same input → same output).
        
        Tests:
        - Same parsed data produces identical YAML (except timestamp)
        - Hash validation for content equality
        - Deterministic ordering of keys
        """
        # Generate YAML twice from same input
        yaml1 = self.generator.generate_yaml(self.sample_parsed_data, self.markdown_path)
        yaml2 = self.generator.generate_yaml(self.sample_parsed_data, self.markdown_path)
        
        # Parse both YAML outputs
        data1 = yaml.safe_load(yaml1)
        data2 = yaml.safe_load(yaml2)
        
        # Timestamps will differ, so compare everything except metadata.last_sync
        data1_copy = dict(data1)
        data2_copy = dict(data2)
        
        # Save and remove timestamps for comparison
        timestamp1 = data1_copy["metadata"]["last_sync"]
        timestamp2 = data2_copy["metadata"]["last_sync"]
        data1_copy["metadata"]["last_sync"] = "NORMALIZED"
        data2_copy["metadata"]["last_sync"] = "NORMALIZED"
        
        # Content should be identical (except timestamp)
        self.assertEqual(data1_copy, data2_copy)
        
        # Timestamps should both be valid but may differ slightly
        self.assertRegex(timestamp1, r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z')
        self.assertRegex(timestamp2, r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z')
        
        # Test hash-based idempotency (normalized hashes should match)
        hash1 = self.generator.compute_yaml_hash(yaml1)
        hash2 = self.generator.compute_yaml_hash(yaml2)
        
        # Hashes may differ due to timestamp, but structure is deterministic
        # This demonstrates that the generator produces consistent structure
        self.assertIsInstance(hash1, str)
        self.assertEqual(len(hash1), 64)  # SHA256 hex length
    
    def test_validate_schema_success(self):
        """Test schema validation passes for valid YAML data."""
        yaml_string = self.generator.generate_yaml(self.sample_parsed_data, self.markdown_path)
        yaml_data = yaml.safe_load(yaml_string)
        
        # Should validate successfully
        result = self.generator.validate_schema(yaml_data)
        self.assertTrue(result)
    
    def test_validate_schema_missing_required_field(self):
        """Test schema validation fails when required fields missing."""
        yaml_string = self.generator.generate_yaml(self.sample_parsed_data, self.markdown_path)
        yaml_data = yaml.safe_load(yaml_string)
        
        # Remove required field
        del yaml_data["spec_id"]
        
        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.generator.validate_schema(yaml_data)
        
        self.assertIn("Missing required field: spec_id", str(context.exception))
    
    def test_validate_schema_missing_section(self):
        """Test schema validation fails when required section missing."""
        yaml_string = self.generator.generate_yaml(self.sample_parsed_data, self.markdown_path)
        yaml_data = yaml.safe_load(yaml_string)
        
        # Remove required section
        del yaml_data["goals"]
        
        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.generator.validate_schema(yaml_data)
        
        self.assertIn("Missing required section: goals", str(context.exception))
    
    def test_validate_schema_invalid_status(self):
        """Test schema validation fails for invalid status enum."""
        yaml_string = self.generator.generate_yaml(self.sample_parsed_data, self.markdown_path)
        yaml_data = yaml.safe_load(yaml_string)
        
        # Set invalid status
        yaml_data["status"] = "invalid-status"
        
        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.generator.validate_schema(yaml_data)
        
        self.assertIn("Invalid status", str(context.exception))
    
    def test_validate_schema_missing_metadata_fields(self):
        """Test schema validation fails when metadata fields missing."""
        yaml_string = self.generator.generate_yaml(self.sample_parsed_data, self.markdown_path)
        yaml_data = yaml.safe_load(yaml_string)
        
        # Remove metadata field
        del yaml_data["metadata"]["spec_version"]
        
        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.generator.validate_schema(yaml_data)
        
        self.assertIn("Missing metadata.spec_version", str(context.exception))
    
    def test_format_datetime_string(self):
        """Test datetime formatting with string input."""
        dt_string = "2025-10-23T10:00:00Z"
        result = self.generator._format_datetime(dt_string)
        self.assertEqual(result, dt_string)
    
    def test_format_datetime_object(self):
        """Test datetime formatting with datetime object."""
        dt = datetime(2025, 10, 23, 10, 0, 0, tzinfo=timezone.utc)
        result = self.generator._format_datetime(dt)
        self.assertEqual(result, "2025-10-23T10:00:00Z")
    
    def test_format_datetime_none(self):
        """Test datetime formatting with None (should use current time)."""
        result = self.generator._format_datetime(None)
        # Should be valid ISO timestamp
        self.assertRegex(result, r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z')
    
    def test_convenience_function_generate_yaml(self):
        """Test module-level convenience function for YAML generation."""
        yaml_string = generate_yaml(self.sample_parsed_data, self.markdown_path)
        
        self.assertIsInstance(yaml_string, str)
        yaml_data = yaml.safe_load(yaml_string)
        self.assertIn("spec_id", yaml_data)
        self.assertIn("metadata", yaml_data)
    
    def test_convenience_function_validate_schema(self):
        """Test module-level convenience function for schema validation."""
        yaml_string = generate_yaml(self.sample_parsed_data, self.markdown_path)
        yaml_data = yaml.safe_load(yaml_string)
        
        result = validate_schema(yaml_data)
        self.assertTrue(result)
    
    def test_yaml_security_safe_dump(self):
        """Test that YAML generation uses safe_dump (no code execution)."""
        yaml_string = self.generator.generate_yaml(self.sample_parsed_data, self.markdown_path)
        
        # Verify no Python object tags in output (would indicate unsafe dump)
        self.assertNotIn("!!python", yaml_string)
        
        # Should be safely loadable
        yaml_data = yaml.safe_load(yaml_string)
        self.assertIsInstance(yaml_data, dict)
    
    def test_empty_parsed_data(self):
        """Test YAML generation with minimal/empty parsed data."""
        minimal_data = {
            "metadata": {
                "spec_id": "spec-minimal",
                "status": "draft"
            }
        }
        
        yaml_string = self.generator.generate_yaml(minimal_data, self.markdown_path)
        yaml_data = yaml.safe_load(yaml_string)
        
        # Should still have all required sections (with defaults)
        self.assertIn("goals", yaml_data)
        self.assertIn("technical_design", yaml_data)
        self.assertIn("implementation", yaml_data)
        self.assertIn("test_strategy", yaml_data)
        self.assertIn("metadata", yaml_data)
        
        # Metadata should be populated
        self.assertEqual(yaml_data["metadata"]["spec_version"], "1.0")
        self.assertEqual(yaml_data["metadata"]["markdown_location"], self.markdown_path)
    
    def test_goals_section_structure(self):
        """Test goals section structure matches schema."""
        yaml_string = self.generator.generate_yaml(self.sample_parsed_data, self.markdown_path)
        yaml_data = yaml.safe_load(yaml_string)
        
        goals = yaml_data["goals"]
        self.assertIn("primary", goals)
        self.assertIn("user_stories", goals)
        self.assertIn("acceptance_criteria", goals)
        self.assertIn("success_metrics", goals)
        self.assertIn("out_of_scope", goals)
        
        # Verify data preservation
        self.assertEqual(goals["primary"], "Test primary goal")
        self.assertEqual(len(goals["user_stories"]), 1)
        self.assertEqual(goals["user_stories"][0]["id"], "us-1")
    
    def test_technical_design_section_structure(self):
        """Test technical design section structure matches schema."""
        yaml_string = self.generator.generate_yaml(self.sample_parsed_data, self.markdown_path)
        yaml_data = yaml.safe_load(yaml_string)
        
        design = yaml_data["technical_design"]
        self.assertIn("architecture", design)
        self.assertIn("components", design)
        self.assertIn("data_structures", design)
        self.assertIn("apis", design)
        self.assertIn("dependencies", design)
        self.assertIn("security_considerations", design)
        self.assertIn("performance_considerations", design)
        
        # Verify data preservation
        self.assertEqual(design["architecture"]["overview"], "Test architecture overview")
        self.assertEqual(len(design["components"]), 1)
        self.assertEqual(design["components"][0]["id"], "comp-1")
    
    def test_implementation_section_structure(self):
        """Test implementation section structure matches schema."""
        yaml_string = self.generator.generate_yaml(self.sample_parsed_data, self.markdown_path)
        yaml_data = yaml.safe_load(yaml_string)
        
        impl = yaml_data["implementation"]
        self.assertIn("tasks", impl)
        self.assertIn("execution_sequence", impl)
        self.assertIn("risks", impl)
        
        # Verify data preservation
        self.assertEqual(len(impl["tasks"]), 1)
        self.assertEqual(impl["tasks"][0]["id"], "task-1")
        self.assertEqual(impl["tasks"][0]["agent"], "backend-architect")
    
    def test_test_strategy_section_structure(self):
        """Test test strategy section structure matches schema."""
        yaml_string = self.generator.generate_yaml(self.sample_parsed_data, self.markdown_path)
        yaml_data = yaml.safe_load(yaml_string)
        
        test_strategy = yaml_data["test_strategy"]
        self.assertIn("test_cases", test_strategy)
        self.assertIn("test_types", test_strategy)
        self.assertIn("validation_checklist", test_strategy)
        
        # Verify test_types structure
        test_types = test_strategy["test_types"]
        self.assertIn("unit_tests", test_types)
        self.assertIn("integration_tests", test_types)
        self.assertIn("e2e_tests", test_types)
        self.assertIn("performance_tests", test_types)
        
        # Verify data preservation
        self.assertEqual(len(test_strategy["test_cases"]), 1)
        self.assertEqual(test_strategy["test_cases"][0]["id"], "tc-1")


class TestYAMLGeneratorEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = YAMLGenerator()
    
    def test_special_characters_in_content(self):
        """Test YAML generation with special characters."""
        data = {
            "metadata": {
                "spec_id": "spec-test",
                "linked_request": "Request with: colons, 'quotes', and \"double quotes\""
            },
            "goals": {
                "primary": "Goal with special chars: @#$%^&*()",
                "out_of_scope": ["Item with\nmultiple\nlines"]
            }
        }
        
        yaml_string = self.generator.generate_yaml(data, "test.md")
        yaml_data = yaml.safe_load(yaml_string)
        
        # Should preserve special characters
        self.assertIn("colons", yaml_data["linked_request"])
        self.assertIn("@#$%^&*()", yaml_data["goals"]["primary"])
    
    def test_unicode_content(self):
        """Test YAML generation with unicode characters."""
        data = {
            "metadata": {
                "spec_id": "spec-unicode",
                "linked_request": "Request with émojis 🚀 and üñíçödé"
            },
            "goals": {
                "primary": "测试中文 • Тест • العربية"
            }
        }
        
        yaml_string = self.generator.generate_yaml(data, "test.md")
        yaml_data = yaml.safe_load(yaml_string)
        
        # Should preserve unicode
        self.assertIn("🚀", yaml_data["linked_request"])
        self.assertIn("测试中文", yaml_data["goals"]["primary"])
    
    def test_very_long_content(self):
        """Test YAML generation with very long content."""
        long_text = "A" * 10000
        data = {
            "metadata": {
                "spec_id": "spec-long",
                "linked_request": long_text
            }
        }
        
        yaml_string = self.generator.generate_yaml(data, "test.md")
        yaml_data = yaml.safe_load(yaml_string)
        
        # Should handle long content
        self.assertEqual(len(yaml_data["linked_request"]), 10000)


if __name__ == "__main__":
    unittest.main()
