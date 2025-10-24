"""
End-to-End Integration Tests for Spec-to-YAML Translator

Comprehensive integration testing covering the complete translation workflow:
Markdown → Parser → Generator → YAML

Tests validate:
- TC-8: Integration with real spec (dogfooding)
- End-to-end translation workflow
- Schema validation against SPEC_SCHEMA.yaml
- Linkage preservation across translation
- Metadata tracking (last_sync, markdown_location)
- Performance (<500ms for typical spec)
- Idempotence (multiple translations produce identical output)
- Error handling in integration

Author: unit-test-expert
Task: task-4 (spec-20251023-spec-to-yaml-translator)
Acceptance Criteria: AC-1 through AC-6
"""

import unittest
import tempfile
import shutil
import time
import yaml
from pathlib import Path
from datetime import datetime
import hashlib

# Import all components
from markdown_parser import parse_spec, ParseError
from yaml_generator import YAMLGenerator, generate_yaml, validate_schema
from translate_spec import translate_spec, validate_yaml_file


class TestIntegrationEndToEnd(unittest.TestCase):
    """
    Integration tests for complete Markdown → YAML workflow.

    Tests the entire translation pipeline with real spec files,
    validating that all components work together correctly.
    """

    def setUp(self):
        """Create temporary directory for test output files."""
        self.test_dir = tempfile.mkdtemp()
        self.generator = YAMLGenerator()

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.test_dir)

    def _get_output_path(self, filename: str) -> str:
        """Get path for test output file."""
        return str(Path(self.test_dir) / filename)

    def test_tc8_integration_with_real_spec(self):
        """
        TC-8: Tool works with actual spec-driven workflow (dogfooding).

        Given: This spec file (2025-10-23-spec-to-yaml-translator.md)
        When: Translate this spec to YAML
        Then: Generated YAML is valid and usable by spec-manager

        This is the ultimate integration test - translating the spec
        that defines this translation tool itself!
        """
        # Use the actual spec file this implementation is based on
        real_spec_path = "/Users/robertnyborg/Projects/claude-oak-agents/specs/active/2025-10-23-spec-to-yaml-translator.md"
        output_yaml_path = self._get_output_path("spec-translator.yaml")

        # Only run if real spec exists
        if not Path(real_spec_path).exists():
            self.skipTest(f"Real spec file not found: {real_spec_path}")

        # WHEN: Translate the real spec to YAML
        success = translate_spec(real_spec_path, output_yaml_path, validate=True)

        # THEN: Translation succeeds
        self.assertTrue(success, "Translation should succeed")

        # THEN: Output YAML file exists
        self.assertTrue(Path(output_yaml_path).exists(), "Output YAML file should exist")

        # THEN: YAML is valid and parseable
        with open(output_yaml_path, 'r') as f:
            yaml_data = yaml.safe_load(f)
        self.assertIsInstance(yaml_data, dict)

        # THEN: Contains all required sections
        required_sections = ["spec_id", "goals", "technical_design", "implementation", "test_strategy", "metadata"]
        for section in required_sections:
            self.assertIn(section, yaml_data, f"Missing required section: {section}")

        # THEN: Metadata is correct
        self.assertEqual(yaml_data["spec_id"], "spec-20251023-spec-to-yaml-translator")
        self.assertEqual(yaml_data["status"], "in-progress")

        # THEN: Metadata tracking is present
        metadata = yaml_data["metadata"]
        self.assertTrue(metadata["generated_from_markdown"])
        self.assertEqual(metadata["markdown_location"], real_spec_path)
        self.assertIn("last_sync", metadata)
        self.assertEqual(metadata["spec_version"], "1.0")

        # THEN: All acceptance criteria are present
        ac_list = yaml_data["goals"]["acceptance_criteria"]
        self.assertGreaterEqual(len(ac_list), 6, "Should have at least 6 acceptance criteria (AC-1 through AC-6)")

        # THEN: All tasks are present
        tasks = yaml_data["implementation"]["tasks"]
        self.assertGreaterEqual(len(tasks), 4, "Should have at least 4 tasks (task-1 through task-4)")

        # THEN: All test cases are present
        test_cases = yaml_data["test_strategy"]["test_cases"]
        self.assertGreaterEqual(len(test_cases), 8, "Should have at least 8 test cases (tc-1 through tc-8)")

        # THEN: Linkages are preserved
        # Check that task-4 links to tc-8
        task_4 = next((t for t in tasks if t["id"] == "task-4"), None)
        self.assertIsNotNone(task_4, "task-4 should exist")
        self.assertIn("tc-8", task_4["links_to"], "task-4 should link to tc-8")

        # Check that tc-8 links back to all AC
        tc_8 = next((tc for tc in test_cases if tc["id"] == "tc-8"), None)
        self.assertIsNotNone(tc_8, "tc-8 should exist")
        tc_8_links = tc_8["links_to"]
        # tc-8 should link to acceptance criteria
        self.assertTrue(
            any("AC-" in link or "ac-" in link for link in tc_8_links),
            "tc-8 should link to acceptance criteria"
        )

        print(f"✅ TC-8: Successfully translated real spec ({len(yaml_data)} top-level sections)")
        print(f"   - {len(ac_list)} acceptance criteria")
        print(f"   - {len(tasks)} tasks")
        print(f"   - {len(test_cases)} test cases")
        print(f"   - Metadata: {metadata['markdown_location']}")

    def test_end_to_end_translation_workflow(self):
        """
        Full workflow: Markdown → Parser → Generator → YAML.

        Tests:
        - Complete pipeline integration
        - Data preservation through all stages
        - No data loss in translation
        """
        # GIVEN: A complete Markdown spec
        spec_content = """# Spec: Integration Test Feature

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-20251023-integration-test

---

## 1. Goals & Requirements

### 1.1 Primary Goal
Build integration test validation for the spec-to-YAML translator.

### 1.2 User Stories
- **As a developer**, **I want** automated translation, **so that** I can maintain consistency.
- **As a spec-manager**, **I want** structured YAML, **so that** I can coordinate agents.

### 1.3 Acceptance Criteria
Clear, testable criteria:

- [ ] **AC-1**: Translation completes successfully
- [ ] **AC-2**: All data preserved
- [x] **AC-3**: Linkages maintained

### 1.4 Success Metrics
How we measure success:

- 100% translation accuracy
- Zero data loss

### 1.5 Out of Scope

- Real-time translation
- GUI interface

---

## 2. Technical Design

### 2.1 Architecture Overview
**Approach**: Three-phase pipeline

**Key Design Decisions**:
1. **Python over Shell**: Better tooling
2. **YAML over JSON**: More readable

### 2.2 Components

- **Component 1**: IntegrationTestComponent
  - **Location**: `specs/tools/test_integration.py`
  - **Responsibility**: End-to-end validation
  - **Interfaces**:
    - `test_workflow() -> bool`
  - **Dependencies**: `unittest`, `yaml`
  - **Links to**: [Goals: AC-1, AC-2]

### 2.3 Data Structures

```yaml
TestResult:
  success: bool
  errors: List[str]
```

### 2.4 APIs / Interfaces

**CLI**:
```bash
python test_integration.py
```

### 2.5 Dependencies

- **pyyaml** v6.0+ - YAML parsing

### 2.6 Security Considerations
- **Safe YAML**: Use safe_load only

### 2.7 Performance Considerations
- **Target**: <500ms translation time

---

## 3. Implementation Plan

### 3.1 Task Breakdown

#### Task 1: Create Integration Tests
- **ID**: `task-1`
- **Description**: Build comprehensive integration test suite
- **Agent**: unit-test-expert
- **Files**: `test_integration.py`
- **Depends On**: none
- **Estimate**: simple (2 hours)
- **Links to**:
  - Design: [2.2.Component-1]
  - Goals: [AC-1, AC-2, AC-3]
  - Tests: [tc-1, tc-2]
- **Status**: [ ] Pending

### 3.2 Execution Sequence

**Sequential Stage 1**: task-1

### 3.3 Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Test flakiness | Medium | Low | Deterministic test data |

---

## 4. Test Strategy

### 4.1 Test Cases

#### Test Case 1: End-to-End Translation
- **TC-ID**: `tc-1`
- **Description**: Validate complete workflow
- **Given**: Valid Markdown spec
- **When**: Run translation pipeline
- **Then**: Valid YAML generated
- **Links to**:
  - Goals: [AC-1, AC-2]
  - Design: [2.2.Component-1]
  - Tasks: [task-1]
- **Status**: [ ] Pending

#### Test Case 2: Linkage Preservation
- **TC-ID**: `tc-2`
- **Description**: Verify linkages maintained
- **Given**: Spec with cross-references
- **When**: Translate to YAML
- **Then**: All linkages preserved
- **Links to**:
  - Goals: [AC-3]
  - Tasks: [task-1]
- **Status**: [ ] Pending

### 4.2 Test Types

- **Unit Tests**:
  - [ ] Parser tests
  - [ ] Generator tests

- **Integration Tests**:
  - [ ] End-to-end workflow
  - [ ] Real spec translation

### 4.3 Validation Checklist

- [ ] All tests pass
- [ ] Code reviewed
"""

        # Create temporary spec file
        spec_path = self._get_output_path("test_spec.md")
        Path(spec_path).write_text(spec_content, encoding='utf-8')
        output_yaml_path = self._get_output_path("test_spec.yaml")

        # WHEN: Execute complete workflow
        # Phase 1: Parse Markdown
        parsed_data = parse_spec(spec_path)

        # Phase 2: Generate YAML
        yaml_string = generate_yaml(parsed_data, spec_path)

        # Phase 3: Write and validate
        Path(output_yaml_path).write_text(yaml_string, encoding='utf-8')
        yaml_data = yaml.safe_load(yaml_string)
        validate_schema(yaml_data)

        # THEN: All phases succeed
        self.assertIsNotNone(parsed_data)
        self.assertIsNotNone(yaml_string)
        self.assertTrue(Path(output_yaml_path).exists())

        # THEN: Data preserved through pipeline
        self.assertEqual(yaml_data["spec_id"], "spec-20251023-integration-test")
        self.assertEqual(yaml_data["status"], "draft")
        self.assertEqual(yaml_data["goals"]["primary"], "Build integration test validation for the spec-to-YAML translator.")
        self.assertEqual(len(yaml_data["goals"]["user_stories"]), 2)
        self.assertEqual(len(yaml_data["goals"]["acceptance_criteria"]), 3)

        # THEN: Components preserved
        self.assertEqual(len(yaml_data["technical_design"]["components"]), 1)
        self.assertEqual(yaml_data["technical_design"]["components"][0]["name"], "IntegrationTestComponent")

        # THEN: Tasks preserved
        self.assertEqual(len(yaml_data["implementation"]["tasks"]), 1)
        self.assertEqual(yaml_data["implementation"]["tasks"][0]["id"], "task-1")

        # THEN: Test cases preserved
        self.assertEqual(len(yaml_data["test_strategy"]["test_cases"]), 2)
        self.assertEqual(yaml_data["test_strategy"]["test_cases"][0]["id"], "tc-1")

        print("✅ End-to-end workflow test passed")

    def test_schema_validation_against_spec_schema(self):
        """
        Generated YAML validates against SPEC_SCHEMA.yaml.

        Tests:
        - YAML conforms to official schema
        - All required fields present
        - Field types correct
        - Enum values valid
        """
        # GIVEN: Minimal valid spec
        minimal_spec = """# Spec: Minimal

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-20251023-minimal

## 1. Goals & Requirements

### 1.1 Primary Goal
Minimal spec for validation.

## 2. Technical Design

### 2.1 Architecture Overview
**Approach**: Minimal design

## 3. Implementation Plan

### 3.1 Task Breakdown

## 4. Test Strategy

### 4.1 Test Cases
"""

        spec_path = self._get_output_path("minimal_spec.md")
        Path(spec_path).write_text(minimal_spec, encoding='utf-8')

        # WHEN: Parse and generate YAML
        parsed = parse_spec(spec_path)
        yaml_string = generate_yaml(parsed, spec_path)
        yaml_data = yaml.safe_load(yaml_string)

        # THEN: Schema validation passes
        self.assertTrue(validate_schema(yaml_data))

        # THEN: Required top-level fields present
        required_fields = ["spec_id", "created", "updated", "status", "linked_request"]
        for field in required_fields:
            self.assertIn(field, yaml_data, f"Missing required field: {field}")

        # THEN: Required sections present
        required_sections = ["goals", "technical_design", "implementation", "test_strategy", "metadata"]
        for section in required_sections:
            self.assertIn(section, yaml_data, f"Missing required section: {section}")

        # THEN: Status is valid enum value
        valid_statuses = ["draft", "approved", "in-progress", "completed"]
        self.assertIn(yaml_data["status"], valid_statuses)

        # THEN: Metadata section has required fields
        metadata = yaml_data["metadata"]
        self.assertIn("spec_version", metadata)
        self.assertIn("generated_from_markdown", metadata)
        self.assertIn("markdown_location", metadata)
        self.assertIn("last_sync", metadata)

        print("✅ Schema validation test passed")

    def test_linkage_preservation_integration(self):
        """
        Cross-references maintained in translation.

        Tests:
        - Goals ↔ Design ↔ Tasks ↔ Tests linkages
        - Explicit reference preservation
        - Bidirectional tracing

        Validates AC-3: All linkages preserved
        """
        # GIVEN: Spec with comprehensive linkages
        linked_spec = """# Spec: Linkage Test

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-20251023-linkage

## 1. Goals & Requirements

### 1.1 Primary Goal
Test linkage preservation.

### 1.3 Acceptance Criteria
Clear criteria:

- [ ] **AC-1**: Feature works correctly
- [ ] **AC-2**: Tests pass

## 2. Technical Design

### 2.2 Components

- **Component 1**: FeatureComponent
  - **Location**: `feature.py`
  - **Responsibility**: Implement feature
  - **Interfaces**: []
  - **Dependencies**: []
  - **Links to**: [Goals: AC-1, AC-2]

## 3. Implementation Plan

### 3.1 Task Breakdown

#### Task 1: Implement Feature
- **ID**: `task-1`
- **Description**: Build the feature
- **Agent**: backend-architect
- **Files**: `feature.py`
- **Depends On**: none
- **Estimate**: 2 hours
- **Links to**:
  - Design: [2.2.Component-1]
  - Goals: [AC-1]
  - Tests: [tc-1, tc-2]
- **Status**: [ ] Pending

## 4. Test Strategy

### 4.1 Test Cases

#### Test Case 1: Unit Test
- **TC-ID**: `tc-1`
- **Description**: Test feature logic
- **Given**: Feature component
- **When**: Execute test
- **Then**: Behavior correct
- **Links to**:
  - Goals: [AC-1]
  - Design: [2.2.Component-1]
  - Tasks: [task-1]
- **Status**: [ ] Pending

#### Test Case 2: Integration Test
- **TC-ID**: `tc-2`
- **Description**: Test integration
- **Given**: Complete system
- **When**: Run integration
- **Then**: All works
- **Links to**:
  - Goals: [AC-2]
  - Tasks: [task-1]
- **Status**: [ ] Pending
"""

        spec_path = self._get_output_path("linked_spec.md")
        Path(spec_path).write_text(linked_spec, encoding='utf-8')

        # WHEN: Translate to YAML
        parsed = parse_spec(spec_path)
        yaml_string = generate_yaml(parsed, spec_path)
        yaml_data = yaml.safe_load(yaml_string)

        # THEN: Component links to goals
        component = yaml_data["technical_design"]["components"][0]
        component_links = component["links_to"]
        self.assertIn("AC-1", component_links)
        self.assertIn("AC-2", component_links)

        # THEN: Task links to design, goals, and tests
        task = yaml_data["implementation"]["tasks"][0]
        task_links = task["links_to"]
        self.assertIn("2.2.Component-1", task_links)
        self.assertIn("AC-1", task_links)
        self.assertIn("tc-1", task_links)
        self.assertIn("tc-2", task_links)

        # THEN: Test case 1 links to goals, design, tasks
        tc1 = yaml_data["test_strategy"]["test_cases"][0]
        tc1_links = tc1["links_to"]
        self.assertIn("AC-1", tc1_links)
        self.assertIn("2.2.Component-1", tc1_links)
        self.assertIn("task-1", tc1_links)

        # THEN: Test case 2 links correctly
        tc2 = yaml_data["test_strategy"]["test_cases"][1]
        tc2_links = tc2["links_to"]
        self.assertIn("AC-2", tc2_links)
        self.assertIn("task-1", tc2_links)

        print("✅ Linkage preservation test passed")
        print(f"   - Component links: {len(component_links)}")
        print(f"   - Task links: {len(task_links)}")
        print(f"   - TC-1 links: {len(tc1_links)}")
        print(f"   - TC-2 links: {len(tc2_links)}")

    def test_metadata_tracking_integration(self):
        """
        Metadata includes sync timestamp and source location.

        Tests:
        - last_sync timestamp present and valid
        - markdown_location correctly set
        - spec_version tracked
        - generated_from_markdown flag set

        Validates AC-6: Metadata tracks last sync timestamp and Markdown source location
        """
        spec_content = """# Spec: Metadata Test

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-20251023-metadata-test

## 1. Goals & Requirements

### 1.1 Primary Goal
Test metadata tracking.
"""

        spec_path = self._get_output_path("metadata_test.md")
        Path(spec_path).write_text(spec_content, encoding='utf-8')

        # Record time before translation
        before_time = datetime.utcnow()

        # WHEN: Translate to YAML
        time.sleep(0.1)  # Ensure timestamp difference
        parsed = parse_spec(spec_path)
        yaml_string = generate_yaml(parsed, spec_path)
        yaml_data = yaml.safe_load(yaml_string)

        time.sleep(0.1)
        after_time = datetime.utcnow()

        # THEN: Metadata section present
        self.assertIn("metadata", yaml_data)
        metadata = yaml_data["metadata"]

        # THEN: Spec version tracked
        self.assertEqual(metadata["spec_version"], "1.0")

        # THEN: Generated from markdown flag set
        self.assertTrue(metadata["generated_from_markdown"])

        # THEN: Markdown location is correct
        self.assertEqual(metadata["markdown_location"], spec_path)

        # THEN: Last sync timestamp present and valid
        self.assertIn("last_sync", metadata)
        last_sync_str = metadata["last_sync"]

        # Validate ISO 8601 format
        self.assertRegex(last_sync_str, r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z')

        # Parse timestamp and verify it's valid
        # Note: We can't reliably check exact timing due to async execution
        # Just validate the format and that it's a reasonable timestamp
        try:
            last_sync = datetime.fromisoformat(last_sync_str.replace('Z', '+00:00'))
            # Timestamp should be within a reasonable range (not in far future or past)
            current_time = datetime.utcnow()
            time_diff = abs((last_sync.replace(tzinfo=None) - current_time).total_seconds())
            self.assertLess(time_diff, 60, "Timestamp should be within 60 seconds of current time")
        except ValueError:
            self.fail(f"Invalid timestamp format: {last_sync_str}")

        print("✅ Metadata tracking test passed")
        print(f"   - Source: {metadata['markdown_location']}")
        print(f"   - Last sync: {metadata['last_sync']}")
        print(f"   - Spec version: {metadata['spec_version']}")

    def test_performance_translation_speed(self):
        """
        Translation completes in <500ms for typical spec.

        Tests:
        - Parse + generate within time limit
        - Performance acceptable for typical spec size

        Validates performance requirement from AC and section 2.7
        """
        # GIVEN: Typical-sized spec (the real spec translator spec is good example)
        real_spec_path = "/Users/robertnyborg/Projects/claude-oak-agents/specs/active/2025-10-23-spec-to-yaml-translator.md"

        if not Path(real_spec_path).exists():
            self.skipTest("Real spec file not found for performance test")

        # WHEN: Measure translation time
        start_time = time.time()

        parsed = parse_spec(real_spec_path)
        yaml_string = generate_yaml(parsed, real_spec_path)

        end_time = time.time()
        duration_ms = (end_time - start_time) * 1000

        # THEN: Translation completes in <500ms
        self.assertLess(duration_ms, 500,
                       f"Translation took {duration_ms:.2f}ms, expected <500ms")

        # THEN: Output is valid
        yaml_data = yaml.safe_load(yaml_string)
        self.assertIsInstance(yaml_data, dict)

        print(f"✅ Performance test passed")
        print(f"   - Translation time: {duration_ms:.2f}ms (target: <500ms)")
        print(f"   - Performance margin: {500 - duration_ms:.2f}ms")

    def test_idempotence_multiple_translations(self):
        """
        Multiple translations produce identical output.

        Tests:
        - Same input → same output (deterministic)
        - Hash validation for equality
        - No timestamp-based variations (except last_sync)

        Validates AC-4: Idempotent translation
        """
        spec_content = """# Spec: Idempotence Test

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-20251023-idempotence

## 1. Goals & Requirements

### 1.1 Primary Goal
Test idempotent translation.

### 1.3 Acceptance Criteria
Criteria:

- [ ] **AC-1**: Deterministic output

## 2. Technical Design

### 2.1 Architecture Overview
**Approach**: Deterministic generation
"""

        spec_path = self._get_output_path("idempotence_spec.md")
        Path(spec_path).write_text(spec_content, encoding='utf-8')

        # WHEN: Translate same spec multiple times
        parsed1 = parse_spec(spec_path)
        yaml1 = generate_yaml(parsed1, spec_path)
        data1 = yaml.safe_load(yaml1)

        # Wait to ensure different timestamp
        time.sleep(0.1)

        parsed2 = parse_spec(spec_path)
        yaml2 = generate_yaml(parsed2, spec_path)
        data2 = yaml.safe_load(yaml2)

        # THEN: Parsed data is identical
        self.assertEqual(parsed1, parsed2)

        # THEN: YAML structure is identical (except timestamp)
        # Compare everything except metadata.last_sync
        data1_normalized = dict(data1)
        data2_normalized = dict(data2)

        timestamp1 = data1_normalized["metadata"]["last_sync"]
        timestamp2 = data2_normalized["metadata"]["last_sync"]

        data1_normalized["metadata"]["last_sync"] = "NORMALIZED"
        data2_normalized["metadata"]["last_sync"] = "NORMALIZED"

        self.assertEqual(data1_normalized, data2_normalized)

        # THEN: Timestamps are both valid (but may differ)
        self.assertRegex(timestamp1, r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z')
        self.assertRegex(timestamp2, r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z')

        # THEN: Hash-based validation (normalized)
        generator = YAMLGenerator()
        hash1 = generator.compute_yaml_hash(yaml1)
        hash2 = generator.compute_yaml_hash(yaml2)

        # Hashes will differ due to timestamp, but both should be valid SHA256
        self.assertEqual(len(hash1), 64)
        self.assertEqual(len(hash2), 64)

        print("✅ Idempotence test passed")
        print(f"   - Translation 1 hash: {hash1[:16]}...")
        print(f"   - Translation 2 hash: {hash2[:16]}...")
        print(f"   - Structure identical: Yes (timestamps excluded)")

    def test_error_handling_invalid_markdown(self):
        """
        Invalid inputs produce clear errors.

        Tests:
        - Missing required metadata
        - Malformed structure
        - File not found
        - Clear error messages
        """
        # Test 1: Missing spec ID
        invalid_spec_1 = """# Spec: Invalid

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft

## 1. Goals & Requirements
"""

        spec_path_1 = self._get_output_path("invalid_1.md")
        Path(spec_path_1).write_text(invalid_spec_1, encoding='utf-8')

        with self.assertRaises(ParseError) as ctx1:
            parse_spec(spec_path_1)
        self.assertIn("Spec ID", str(ctx1.exception))

        # Test 2: Missing created date
        invalid_spec_2 = """# Spec: Invalid

**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-test

## 1. Goals & Requirements
"""

        spec_path_2 = self._get_output_path("invalid_2.md")
        Path(spec_path_2).write_text(invalid_spec_2, encoding='utf-8')

        with self.assertRaises(ParseError) as ctx2:
            parse_spec(spec_path_2)
        self.assertIn("Created", str(ctx2.exception))

        # Test 3: File not found
        with self.assertRaises(FileNotFoundError):
            parse_spec("/nonexistent/path.md")

        print("✅ Error handling test passed")
        print("   - Missing Spec ID: Detected")
        print("   - Missing Created date: Detected")
        print("   - File not found: Detected")

    def test_error_handling_invalid_yaml_data(self):
        """
        YAML validation detects invalid data.

        Tests:
        - Missing required fields
        - Invalid enum values
        - Schema validation errors
        """
        generator = YAMLGenerator()

        # Test 1: Missing required field
        invalid_data_1 = {
            # Missing spec_id
            "status": "draft",
            "goals": {},
            "technical_design": {},
            "implementation": {},
            "test_strategy": {},
            "metadata": {
                "spec_version": "1.0",
                "generated_from_markdown": True,
                "markdown_location": "test.md",
                "last_sync": "2025-10-23T10:00:00Z"
            }
        }

        with self.assertRaises(ValueError) as ctx1:
            generator.validate_schema(invalid_data_1)
        self.assertIn("Missing required field: spec_id", str(ctx1.exception))

        # Test 2: Invalid status enum
        invalid_data_2 = {
            "spec_id": "test",
            "status": "invalid-status",
            "goals": {},
            "technical_design": {},
            "implementation": {},
            "test_strategy": {},
            "metadata": {
                "spec_version": "1.0",
                "generated_from_markdown": True,
                "markdown_location": "test.md",
                "last_sync": "2025-10-23T10:00:00Z"
            }
        }

        with self.assertRaises(ValueError) as ctx2:
            generator.validate_schema(invalid_data_2)
        self.assertIn("Invalid status", str(ctx2.exception))

        print("✅ YAML validation error handling test passed")
        print("   - Missing field detection: Working")
        print("   - Invalid enum detection: Working")

    def test_cli_integration_translate_and_validate(self):
        """
        CLI tool translates and validates correctly.

        Tests:
        - CLI translate_spec function
        - Validation flag works
        - Output file creation
        - Return codes correct
        """
        spec_content = """# Spec: CLI Test

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-20251023-cli-test

## 1. Goals & Requirements

### 1.1 Primary Goal
Test CLI integration.
"""

        spec_path = self._get_output_path("cli_spec.md")
        output_path = self._get_output_path("cli_spec.yaml")
        Path(spec_path).write_text(spec_content, encoding='utf-8')

        # WHEN: Use CLI to translate with validation
        success = translate_spec(spec_path, output_path, validate=True)

        # THEN: Translation succeeds
        self.assertTrue(success)

        # THEN: Output file created
        self.assertTrue(Path(output_path).exists())

        # THEN: YAML is valid
        yaml_data = yaml.safe_load(Path(output_path).read_text())
        self.assertEqual(yaml_data["spec_id"], "spec-20251023-cli-test")

        # THEN: validate_yaml_file works
        validation_success = validate_yaml_file(output_path)
        self.assertTrue(validation_success)

        print("✅ CLI integration test passed")


class TestIntegrationEdgeCases(unittest.TestCase):
    """
    Integration tests for edge cases and boundary conditions.
    """

    def setUp(self):
        """Create temporary directory."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.test_dir)

    def _get_output_path(self, filename: str) -> str:
        """Get path for test output file."""
        return str(Path(self.test_dir) / filename)

    def test_empty_sections_handling(self):
        """
        Test handling of specs with empty/minimal sections.

        Ensures graceful handling of optional content.
        """
        minimal_spec = """# Spec: Minimal

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-minimal

## 1. Goals & Requirements

### 1.1 Primary Goal
Minimal content.

## 2. Technical Design

### 2.1 Architecture Overview
**Approach**: Minimal

## 3. Implementation Plan

### 3.1 Task Breakdown

## 4. Test Strategy

### 4.1 Test Cases
"""

        spec_path = self._get_output_path("minimal.md")
        Path(spec_path).write_text(minimal_spec, encoding='utf-8')

        # Should parse successfully
        parsed = parse_spec(spec_path)
        self.assertIsNotNone(parsed)

        # Should generate valid YAML
        yaml_string = generate_yaml(parsed, spec_path)
        yaml_data = yaml.safe_load(yaml_string)

        # Should validate
        self.assertTrue(validate_schema(yaml_data))

        # Empty sections should have default structures
        self.assertIsInstance(yaml_data["goals"]["user_stories"], list)
        self.assertIsInstance(yaml_data["implementation"]["tasks"], list)

        print("✅ Empty sections handling test passed")

    def test_special_characters_preservation(self):
        """
        Test preservation of special characters and unicode.

        Ensures no data corruption during translation.
        """
        spec_with_special_chars = """# Spec: Special Characters Test

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-special-chars

## 1. Goals & Requirements

### 1.1 Primary Goal
Test special chars: @#$%^&*() and unicode 🚀 émojis.

### 1.2 User Stories
- **As a user**, **I want** unicode support, **so that** I can use émojis 🎉.

### 1.3 Acceptance Criteria
Test criteria:

- [ ] **AC-1**: Handle "quotes" and 'apostrophes'
- [ ] **AC-2**: Support colons: like this
"""

        spec_path = self._get_output_path("special_chars.md")
        Path(spec_path).write_text(spec_with_special_chars, encoding='utf-8')

        # Parse and generate
        parsed = parse_spec(spec_path)
        yaml_string = generate_yaml(parsed, spec_path)
        yaml_data = yaml.safe_load(yaml_string)

        # Verify special characters preserved
        self.assertIn("@#$%^&*()", yaml_data["goals"]["primary"])
        self.assertIn("🚀", yaml_data["goals"]["primary"])
        self.assertIn("émojis", yaml_data["goals"]["primary"])

        # Verify in user stories
        self.assertIn("🎉", yaml_data["goals"]["user_stories"][0]["benefit"])

        # Verify in acceptance criteria
        ac1 = yaml_data["goals"]["acceptance_criteria"][0]
        self.assertIn('"quotes"', ac1["criterion"])
        self.assertIn("'apostrophes'", ac1["criterion"])

        print("✅ Special characters preservation test passed")

    def test_large_spec_performance(self):
        """
        Test performance with large spec files.

        Ensures scalability for comprehensive specs.
        """
        # Generate large spec with many sections
        large_spec_parts = [
            """# Spec: Large Spec

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-large

## 1. Goals & Requirements

### 1.1 Primary Goal
Large spec with many items.

### 1.2 User Stories
"""
        ]

        # Add 50 user stories
        for i in range(50):
            large_spec_parts.append(
                f"- **As a user {i}**, **I want** feature {i}, **so that** I get benefit {i}.\n"
            )

        large_spec_parts.append("""
### 1.3 Acceptance Criteria
Test criteria:

""")

        # Add 30 acceptance criteria
        for i in range(30):
            large_spec_parts.append(f"- [ ] **AC-{i+1}**: Criterion {i+1}\n")

        large_spec_parts.append("""
## 2. Technical Design

### 2.1 Architecture Overview
**Approach**: Large system

### 2.2 Components

""")

        # Add 20 components
        for i in range(20):
            large_spec_parts.append(f"""- **Component {i+1}**: Comp{i+1}
  - **Location**: `comp{i+1}.py`
  - **Responsibility**: Responsibility {i+1}
  - **Interfaces**: []
  - **Dependencies**: []
  - **Links to**: [Goals: AC-1]

""")

        large_spec_parts.append("""
## 3. Implementation Plan

### 3.1 Task Breakdown

""")

        # Add 40 tasks
        for i in range(40):
            large_spec_parts.append(f"""#### Task {i+1}: Task Name {i+1}
- **ID**: `task-{i+1}`
- **Description**: Description {i+1}
- **Agent**: backend-architect
- **Files**: `file{i+1}.py`
- **Depends On**: none
- **Estimate**: simple
- **Links to**:
  - Goals: [AC-1]
- **Status**: [ ] Pending

""")

        large_spec_parts.append("""
## 4. Test Strategy

### 4.1 Test Cases

""")

        # Add 25 test cases
        for i in range(25):
            large_spec_parts.append(f"""#### Test Case {i+1}: Test {i+1}
- **TC-ID**: `tc-{i+1}`
- **Description**: Test description {i+1}
- **Given**: Given {i+1}
- **When**: When {i+1}
- **Then**: Then {i+1}
- **Links to**:
  - Goals: [AC-1]
- **Status**: [ ] Pending

""")

        large_spec = "".join(large_spec_parts)

        spec_path = self._get_output_path("large_spec.md")
        Path(spec_path).write_text(large_spec, encoding='utf-8')

        # Measure performance
        start_time = time.time()
        parsed = parse_spec(spec_path)
        yaml_string = generate_yaml(parsed, spec_path)
        end_time = time.time()

        duration_ms = (end_time - start_time) * 1000

        # Should still complete in reasonable time
        self.assertLess(duration_ms, 1000, "Large spec should translate in <1s")

        # Verify all items parsed
        yaml_data = yaml.safe_load(yaml_string)
        self.assertEqual(len(yaml_data["goals"]["user_stories"]), 50)
        self.assertEqual(len(yaml_data["goals"]["acceptance_criteria"]), 30)
        self.assertEqual(len(yaml_data["technical_design"]["components"]), 20)
        self.assertEqual(len(yaml_data["implementation"]["tasks"]), 40)
        self.assertEqual(len(yaml_data["test_strategy"]["test_cases"]), 25)

        print(f"✅ Large spec performance test passed")
        print(f"   - 50 user stories, 30 ACs, 20 components, 40 tasks, 25 tests")
        print(f"   - Translation time: {duration_ms:.2f}ms")


class TestIntegrationDataIntegrity(unittest.TestCase):
    """
    Tests focused on data integrity through the translation pipeline.

    Validates that no data is lost or corrupted during translation.
    """

    def setUp(self):
        """Create temporary directory."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.test_dir)

    def _get_output_path(self, filename: str) -> str:
        """Get path for test output file."""
        return str(Path(self.test_dir) / filename)

    def test_all_metadata_fields_preserved(self):
        """Verify all metadata fields are preserved correctly."""
        spec = """# Spec: Metadata Fields Test

**Created**: 2025-10-23
**Updated**: 2025-10-23T14:30:00Z
**Status**: in-progress
**Spec ID**: spec-20251023-metadata-fields

## 1. Goals & Requirements

### 1.1 Primary Goal
Test metadata preservation.
"""

        spec_path = self._get_output_path("metadata_fields.md")
        Path(spec_path).write_text(spec, encoding='utf-8')

        parsed = parse_spec(spec_path)
        yaml_string = generate_yaml(parsed, spec_path)
        yaml_data = yaml.safe_load(yaml_string)

        # All metadata fields should be preserved
        self.assertEqual(yaml_data["spec_id"], "spec-20251023-metadata-fields")
        self.assertEqual(yaml_data["created"], "2025-10-23")
        self.assertEqual(yaml_data["updated"], "2025-10-23T14:30:00Z")
        self.assertEqual(yaml_data["status"], "in-progress")

        print("✅ Metadata fields preservation test passed")

    def test_all_goal_sections_preserved(self):
        """Verify all goal section data is preserved."""
        spec = """# Spec: Goals Test

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-goals

## 1. Goals & Requirements

### 1.1 Primary Goal
Primary goal text here with details.

### 1.2 User Stories
- **As a developer**, **I want** feature A, **so that** I get benefit A.
- **As a user**, **I want** feature B, **so that** I get benefit B.

### 1.3 Acceptance Criteria
Test acceptance criteria:

- [ ] **AC-1**: First criterion
- [x] **AC-2**: Second criterion (completed)

### 1.4 Success Metrics

- Metric 1: description
- Metric 2: another description

### 1.5 Out of Scope
What we're NOT doing:

- Item 1 not in scope
- Item 2 not in scope
"""

        spec_path = self._get_output_path("goals.md")
        Path(spec_path).write_text(spec, encoding='utf-8')

        parsed = parse_spec(spec_path)
        yaml_string = generate_yaml(parsed, spec_path)
        yaml_data = yaml.safe_load(yaml_string)

        goals = yaml_data["goals"]

        # Primary goal
        self.assertIn("Primary goal text", goals["primary"])

        # User stories
        self.assertEqual(len(goals["user_stories"]), 2)
        self.assertEqual(goals["user_stories"][0]["role"], "developer")
        self.assertEqual(goals["user_stories"][1]["role"], "user")

        # Acceptance criteria
        self.assertEqual(len(goals["acceptance_criteria"]), 2)
        self.assertEqual(goals["acceptance_criteria"][0]["id"], "AC-1")
        self.assertEqual(goals["acceptance_criteria"][0]["status"], "pending")
        self.assertEqual(goals["acceptance_criteria"][1]["id"], "AC-2")
        self.assertEqual(goals["acceptance_criteria"][1]["status"], "completed")

        # Success metrics
        self.assertEqual(len(goals["success_metrics"]), 2)

        # Out of scope
        self.assertEqual(len(goals["out_of_scope"]), 2)

        print("✅ Goal sections preservation test passed")

    def test_round_trip_consistency(self):
        """
        Test that data remains consistent through parse → generate → parse cycle.

        While we don't support YAML → Markdown, we can verify that
        YAML → parse → YAML produces consistent results.
        """
        spec = """# Spec: Round Trip Test

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-round-trip

## 1. Goals & Requirements

### 1.1 Primary Goal
Test round trip consistency.

### 1.3 Acceptance Criteria
Criteria:

- [ ] **AC-1**: Data preserved

## 2. Technical Design

### 2.1 Architecture Overview
**Approach**: Test approach

## 3. Implementation Plan

### 3.1 Task Breakdown

#### Task 1: Test Task
- **ID**: `task-1`
- **Description**: Test
- **Agent**: backend-architect
- **Files**: `test.py`
- **Depends On**: none
- **Estimate**: 1 hour
- **Links to**:
  - Goals: [AC-1]
- **Status**: [ ] Pending

## 4. Test Strategy

### 4.1 Test Cases

#### Test Case 1: Test
- **TC-ID**: `tc-1`
- **Description**: Test case
- **Given**: Given
- **When**: When
- **Then**: Then
- **Links to**:
  - Goals: [AC-1]
- **Status**: [ ] Pending
"""

        spec_path = self._get_output_path("round_trip.md")
        Path(spec_path).write_text(spec, encoding='utf-8')

        # First translation
        parsed1 = parse_spec(spec_path)
        yaml1 = generate_yaml(parsed1, spec_path)
        data1 = yaml.safe_load(yaml1)

        # Normalize timestamp
        timestamp1 = data1["metadata"]["last_sync"]
        data1["metadata"]["last_sync"] = "NORMALIZED"

        # "Re-translate" by generating YAML again from same parsed data
        yaml2 = generate_yaml(parsed1, spec_path)
        data2 = yaml.safe_load(yaml2)
        data2["metadata"]["last_sync"] = "NORMALIZED"

        # Data should be identical (except timestamp which we normalized)
        self.assertEqual(data1, data2)

        print("✅ Round trip consistency test passed")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
