"""
Test suite for translate_spec.py CLI tool

Tests CLI end-to-end translation and metadata tracking.
Covers test cases: tc-6 (CLI E2E), tc-7 (Metadata Tracking)

Author: backend-architect
Task: task-3 (spec-20251023-spec-to-yaml-translator)
"""

import unittest
import tempfile
import shutil
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Import CLI functions
from translate_spec import translate_spec, validate_yaml_file, main


class TestTranslateCLI(unittest.TestCase):
    """Test translate_spec CLI functionality."""
    
    def setUp(self):
        """Create temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
        self.test_md_path = Path(self.test_dir) / "test_spec.md"
        self.test_yaml_path = Path(self.test_dir) / "test_spec.yaml"
        
        # Create minimal valid Markdown spec
        self.test_md_content = """# Test Spec

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-test-001
**Linked Request**: "Test request"

## 1. Goals & Requirements

### 1.1 Primary Goal
Test primary goal

### 1.2 User Stories
- **As a tester**, **I want** to test, **so that** it works

### 1.3 Acceptance Criteria
- [ ] **AC-1**: Test criterion

### 1.4 Success Metrics
- Test metric

### 1.5 Out of Scope
- Test out of scope

## 2. Technical Design

### 2.1 Architecture Overview
**Approach**: Test approach

### 2.2 Components
- **Component 1**: TestComponent

### 2.3 Data Structures
```yaml
test: data
```

### 2.4 APIs / Interfaces
```bash
test command
```

### 2.5 Dependencies
- **test-lib** v1.0 - test purpose

### 2.6 Security Considerations
- **Test**: Mitigation

### 2.7 Performance Considerations
- **Test**: Target

## 3. Implementation Plan

### 3.1 Task Breakdown
#### Task 1: Test Task
- **ID**: `task-1`
- **Description**: Test description

### 3.2 Execution Sequence
**Parallel Stage 1**: task-1

### 3.3 Risk Assessment
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Test risk | Low | Low | Test mitigation |

## 4. Test Strategy

### 4.1 Test Cases
#### Test Case 1: Test
- **TC-ID**: `tc-1`
- **Description**: Test

### 4.2 Test Types
- **Unit Tests**:
  - [ ] Test

### 4.3 Validation Checklist
- [ ] Test checklist
"""
        self.test_md_path.write_text(self.test_md_content, encoding='utf-8')
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)
    
    def test_tc6_cli_end_to_end_translation(self):
        """
        TC-6: CLI End-to-End Translation
        
        Given: Valid Markdown spec file
        When: Run translate_spec with --input, --output, --validate
        Then: YAML file created, validation passes, exit code 0
        """
        # Execute translation
        success = translate_spec(
            str(self.test_md_path),
            str(self.test_yaml_path),
            validate=True
        )
        
        # Assert success
        self.assertTrue(success, "Translation should succeed")
        
        # Assert YAML file exists
        self.assertTrue(self.test_yaml_path.exists(), "YAML file should be created")
        
        # Assert YAML is valid
        yaml_content = self.test_yaml_path.read_text(encoding='utf-8')
        yaml_data = yaml.safe_load(yaml_content)
        
        # Basic structure checks
        self.assertIn('spec_id', yaml_data)
        self.assertEqual(yaml_data['spec_id'], 'spec-test-001')
        self.assertIn('goals', yaml_data)
        self.assertIn('technical_design', yaml_data)
        self.assertIn('implementation', yaml_data)
        self.assertIn('test_strategy', yaml_data)
        self.assertIn('metadata', yaml_data)
    
    def test_tc7_metadata_tracking(self):
        """
        TC-7: Metadata Tracking
        
        Given: Translated YAML spec
        When: Inspect metadata section
        Then: Contains last_sync timestamp and markdown_location path
        """
        # Execute translation
        success = translate_spec(str(self.test_md_path), str(self.test_yaml_path))
        self.assertTrue(success)
        
        # Load YAML
        yaml_content = self.test_yaml_path.read_text(encoding='utf-8')
        yaml_data = yaml.safe_load(yaml_content)
        
        # Assert metadata section exists
        self.assertIn('metadata', yaml_data)
        metadata = yaml_data['metadata']
        
        # Assert required metadata fields
        self.assertIn('last_sync', metadata, "Metadata should contain last_sync timestamp")
        self.assertIn('markdown_location', metadata, "Metadata should contain markdown_location")
        self.assertIn('generated_from_markdown', metadata, "Metadata should contain generated_from_markdown flag")
        self.assertIn('spec_version', metadata, "Metadata should contain spec_version")
        
        # Assert metadata values
        self.assertEqual(metadata['markdown_location'], str(self.test_md_path))
        self.assertTrue(metadata['generated_from_markdown'])
        self.assertEqual(metadata['spec_version'], '1.0')
        
        # Assert timestamp format (ISO 8601 with Z)
        timestamp = metadata['last_sync']
        self.assertRegex(timestamp, r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*Z')
    
    def test_translate_missing_input_file(self):
        """Test translation with missing input file."""
        success = translate_spec('nonexistent.md', str(self.test_yaml_path))
        self.assertFalse(success, "Translation should fail for missing file")
    
    def test_translate_invalid_markdown(self):
        """Test translation with invalid Markdown (missing required fields)."""
        invalid_md = Path(self.test_dir) / "invalid.md"
        invalid_md.write_text("# Invalid\n\nNo metadata", encoding='utf-8')
        
        success = translate_spec(str(invalid_md), str(self.test_yaml_path))
        self.assertFalse(success, "Translation should fail for invalid Markdown")
    
    def test_validate_yaml_file_success(self):
        """Test YAML validation with valid file."""
        # First create a valid YAML
        translate_spec(str(self.test_md_path), str(self.test_yaml_path))
        
        # Validate it
        success = validate_yaml_file(str(self.test_yaml_path))
        self.assertTrue(success, "Validation should pass for valid YAML")
    
    def test_validate_yaml_file_missing(self):
        """Test YAML validation with missing file."""
        success = validate_yaml_file('nonexistent.yaml')
        self.assertFalse(success, "Validation should fail for missing file")
    
    def test_validate_yaml_file_invalid(self):
        """Test YAML validation with invalid YAML."""
        invalid_yaml = Path(self.test_dir) / "invalid.yaml"
        invalid_yaml.write_text("invalid: yaml: content:", encoding='utf-8')
        
        success = validate_yaml_file(str(invalid_yaml))
        self.assertFalse(success, "Validation should fail for invalid YAML")
    
    def test_validate_yaml_file_missing_required_fields(self):
        """Test YAML validation with missing required fields."""
        incomplete_yaml = Path(self.test_dir) / "incomplete.yaml"
        incomplete_yaml.write_text("spec_id: test\n", encoding='utf-8')
        
        success = validate_yaml_file(str(incomplete_yaml))
        self.assertFalse(success, "Validation should fail for incomplete YAML")
    
    def test_output_directory_creation(self):
        """Test that output directory is created if it doesn't exist."""
        nested_output = Path(self.test_dir) / "nested" / "dir" / "output.yaml"
        
        success = translate_spec(str(self.test_md_path), str(nested_output))
        self.assertTrue(success)
        self.assertTrue(nested_output.exists())
        self.assertTrue(nested_output.parent.exists())


class TestCLIArguments(unittest.TestCase):
    """Test CLI argument parsing and validation."""
    
    def test_main_no_arguments(self):
        """Test main() with no arguments."""
        with patch('sys.argv', ['translate_spec.py']):
            with patch('sys.stderr'):
                with self.assertRaises(SystemExit) as cm:
                    main()
                self.assertIn(cm.exception.code, [1, 2], "Should exit with error code")
    
    def test_main_input_without_output(self):
        """Test main() with --input but no --output."""
        with patch('sys.argv', ['translate_spec.py', '--input', 'test.md']):
            with patch('sys.stderr'):
                exit_code = main()
                self.assertEqual(exit_code, 1, "Should fail with --input but no --output")
    
    def test_main_validate_yaml(self):
        """Test main() with --validate-yaml."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump({
                'spec_id': 'test',
                'created': '2025-10-23',
                'updated': '2025-10-23',
                'status': 'draft',
                'linked_request': 'test',
                'goals': {},
                'technical_design': {},
                'implementation': {},
                'test_strategy': {},
                'metadata': {
                    'spec_version': '1.0',
                    'generated_from_markdown': True,
                    'markdown_location': 'test.md',
                    'last_sync': '2025-10-23T00:00:00Z'
                }
            }, f)
            yaml_file = f.name
        
        try:
            with patch('sys.argv', ['translate_spec.py', '--validate-yaml', yaml_file]):
                exit_code = main()
                self.assertEqual(exit_code, 0, "Should succeed validating valid YAML")
        finally:
            Path(yaml_file).unlink()
    
    def test_main_watch_not_implemented(self):
        """Test main() with --watch (not implemented)."""
        with patch('sys.argv', ['translate_spec.py', '--watch', 'test.md']):
            with patch('sys.stderr'):
                with self.assertRaises(SystemExit) as cm:
                    main()
                self.assertEqual(cm.exception.code, 1, "Should exit with code 1 for not implemented")
    
    def test_main_keyboard_interrupt(self):
        """Test main() handles KeyboardInterrupt gracefully."""
        with patch('sys.argv', ['translate_spec.py', '--input', 'test.md', '--output', 'test.yaml']):
            with patch('translate_spec.translate_spec', side_effect=KeyboardInterrupt):
                with patch('sys.stderr'):
                    exit_code = main()
                    self.assertEqual(exit_code, 1, "Should exit with code 1 on interrupt")


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""
    
    def setUp(self):
        """Create temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)
    
    def test_unicode_handling(self):
        """Test translation with Unicode characters."""
        unicode_md = Path(self.test_dir) / "unicode.md"
        unicode_yaml = Path(self.test_dir) / "unicode.yaml"
        
        content = """# Unicode Test

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-unicode-001
**Linked Request**: "Test 测试 тест テスト"

## 1. Goals & Requirements

### 1.1 Primary Goal
Unicode: 你好世界 Привет мир こんにちは世界

### 1.2 User Stories
- **As a user**, **I want** Unicode, **so that** it works

### 1.3 Acceptance Criteria
- [ ] **AC-1**: Unicode support

### 1.4 Success Metrics
- Unicode metric

### 1.5 Out of Scope
- None

## 2. Technical Design

### 2.1 Architecture Overview
**Approach**: Unicode approach

## 3. Implementation Plan

### 3.1 Task Breakdown
#### Task 1: Unicode Task
- **ID**: `task-1`

### 3.2 Execution Sequence
**Parallel Stage 1**: task-1

### 3.3 Risk Assessment
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Unicode | Low | Low | Test |

## 4. Test Strategy

### 4.1 Test Cases
#### Test Case 1: Unicode
- **TC-ID**: `tc-1`

### 4.2 Test Types
- **Unit Tests**:
  - [ ] Unicode

### 4.3 Validation Checklist
- [ ] Unicode
"""
        unicode_md.write_text(content, encoding='utf-8')
        
        success = translate_spec(str(unicode_md), str(unicode_yaml))
        self.assertTrue(success, "Should handle Unicode characters")
        
        # Verify Unicode preserved
        yaml_content = unicode_yaml.read_text(encoding='utf-8')
        self.assertIn('你好世界', yaml_content)
        self.assertIn('Привет мир', yaml_content)
        self.assertIn('こんにちは世界', yaml_content)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
