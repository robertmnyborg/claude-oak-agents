"""
Unit Tests for Markdown Spec Parser

Tests parsing of spec files, linkage preservation, and error handling.

Author: backend-architect
Task: task-1 (spec-20251023-spec-to-yaml-translator)
Test Coverage: tc-1, tc-2, tc-3
"""

import unittest
import tempfile
import os
from pathlib import Path

from markdown_parser import parse_spec, ParseError


class TestMarkdownParser(unittest.TestCase):
    """Test suite for Markdown spec parser."""
    
    def setUp(self):
        """Create temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def _create_test_spec(self, content: str) -> str:
        """Helper to create temporary spec file."""
        file_path = os.path.join(self.test_dir, "test_spec.md")
        Path(file_path).write_text(content, encoding='utf-8')
        return file_path
    
    def test_tc1_parse_complete_spec(self):
        """
        TC-1: Parse complete spec with all sections.
        Given: Valid Markdown spec with all sections
        When: Parser processes spec file
        Then: Parsed data structure contains all sections with correct values
        """
        spec_content = """# Spec: Test Spec

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: in-progress
**Spec ID**: spec-20251023-test

---

## 1. Goals & Requirements

### 1.1 Primary Goal
Build a test feature for validation.

### 1.2 User Stories
- **As a developer**, **I want** to test parsing, **so that** I can validate functionality.
- **As a user**, **I want** simple interface, **so that** I can use it easily.

### 1.3 Acceptance Criteria
Clear, testable criteria:

- [ ] **AC-1**: Parser extracts metadata correctly
- [x] **AC-2**: Parser preserves linkages

### 1.4 Success Metrics
How we measure success:

- 100% parsing accuracy
- Zero data loss

### 1.5 Out of Scope
Not doing:

- Real-time parsing
- GUI editor

---

## 2. Technical Design

### 2.1 Architecture Overview
**Approach**: Regex-based parsing

The tool uses simple regex patterns.

**Key Design Decisions**:
1. **Python over Shell**: Better regex support
2. **Fail-fast**: Clear error messages

### 2.2 Components
Breakdown of components:

- **Component 1**: Parser
  - **Location**: `specs/tools/parser.py`
  - **Responsibility**: Extract data from Markdown
  - **Interfaces**:
    - `parse_spec(file_path: str) -> Dict`
  - **Dependencies**: `re`, `pathlib`
  - **Links to**: [Goals: AC-1]

### 2.3 Data Structures
Key data models:

```yaml
ParsedSpec:
  metadata:
    spec_id: str
    created: datetime
```

### 2.4 APIs / Interfaces

**CLI Interface**:
```bash
python parser.py --input spec.md
```

### 2.5 Dependencies
External dependencies:

- **pytest** v7.0+ - Testing framework
- **pyyaml** v6.0+ - YAML handling

### 2.6 Security Considerations
- **Input validation**: Sanitize file paths
- **Safe parsing**: No arbitrary code execution

### 2.7 Performance Considerations
- **Target performance**: <500ms for typical spec
- **Optimization strategy**: Lazy parsing

---

## 3. Implementation Plan

### 3.1 Task Breakdown
Detailed tasks:

#### Task 1: Create Parser
- **ID**: `task-1`
- **Description**: Build regex-based parser
- **Agent**: backend-architect
- **Files**: `parser.py`, `test_parser.py`
- **Depends On**: none
- **Estimate**: moderate (4 hours)
- **Links to**:
  - Design: [2.2.Component-1]
  - Goals: [AC-1]
  - Tests: [tc-1, tc-2]
- **Status**: [x] Completed

### 3.2 Execution Sequence
Task dependencies:

**Parallel Stage 1**: task-1
**Sequential Stage 2**: task-2

**Estimated Total**: 6 hours

### 3.3 Risk Assessment
Potential risks:

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Regex too brittle | High | Medium | Comprehensive tests |
| Performance issues | Low | Low | Profile and optimize |

---

## 4. Test Strategy

### 4.1 Test Cases
Comprehensive test scenarios:

#### Test Case 1: Parse Complete Spec
- **TC-ID**: `tc-1`
- **Description**: Parser extracts all sections
- **Given**: Valid Markdown spec with all sections
- **When**: Parser processes spec file
- **Then**: Parsed data contains all sections
- **Links to**:
  - Goals: [AC-1]
  - Design: [2.2.Component-1]
  - Tasks: [task-1]
- **Status**: [x] Completed

#### Test Case 2: Preserve Linkages
- **TC-ID**: `tc-2`
- **Description**: Parser preserves cross-references
- **Given**: Markdown with linkages
- **When**: Parser processes spec
- **Then**: Linkages preserved in parsed data
- **Links to**:
  - Goals: [AC-2]
  - Tasks: [task-1]
- **Status**: [ ] Pending

### 4.2 Test Types
Test categories:

- **Unit Tests**:
  - [x] Parser metadata extraction
  - [ ] Parser linkage preservation
  - [ ] Error handling

- **Integration Tests**:
  - [ ] End-to-end parsing
  - [ ] Schema validation

### 4.3 Validation Checklist
Sign-off criteria:

- [x] All test cases pass
- [ ] Code reviewed
- [ ] Documentation complete
"""
        
        file_path = self._create_test_spec(spec_content)
        result = parse_spec(file_path)
        
        # Verify metadata
        self.assertEqual(result["metadata"]["spec_id"], "spec-20251023-test")
        self.assertEqual(result["metadata"]["created"], "2025-10-23")
        self.assertEqual(result["metadata"]["updated"], "2025-10-23")
        self.assertEqual(result["metadata"]["status"], "in-progress")
        
        # Verify goals
        self.assertEqual(result["goals"]["primary"], "Build a test feature for validation.")
        self.assertEqual(len(result["goals"]["user_stories"]), 2)
        self.assertEqual(result["goals"]["user_stories"][0]["role"], "developer")
        self.assertEqual(len(result["goals"]["acceptance_criteria"]), 2)
        self.assertEqual(result["goals"]["acceptance_criteria"][0]["id"], "AC-1")
        self.assertEqual(result["goals"]["acceptance_criteria"][0]["status"], "pending")
        self.assertEqual(result["goals"]["acceptance_criteria"][1]["status"], "completed")
        self.assertEqual(len(result["goals"]["success_metrics"]), 2)
        self.assertEqual(len(result["goals"]["out_of_scope"]), 2)
        
        # Verify design
        self.assertIn("Regex-based parsing", result["design"]["architecture"]["overview"])
        self.assertEqual(len(result["design"]["architecture"]["key_decisions"]), 2)
        self.assertEqual(len(result["design"]["components"]), 1)
        self.assertEqual(result["design"]["components"][0]["name"], "Parser")
        self.assertEqual(result["design"]["components"][0]["location"], "specs/tools/parser.py")
        self.assertEqual(len(result["design"]["data_structures"]), 1)
        self.assertEqual(len(result["design"]["dependencies"]), 2)
        
        # Verify implementation
        self.assertEqual(len(result["implementation"]["tasks"]), 1)
        self.assertEqual(result["implementation"]["tasks"][0]["id"], "task-1")
        self.assertEqual(result["implementation"]["tasks"][0]["agent"], "backend-architect")
        self.assertEqual(result["implementation"]["tasks"][0]["status"], "completed")
        self.assertEqual(len(result["implementation"]["execution_sequence"]), 2)
        self.assertEqual(len(result["implementation"]["risks"]), 2)
        
        # Verify test strategy
        self.assertEqual(len(result["test_strategy"]["test_cases"]), 2)
        self.assertEqual(result["test_strategy"]["test_cases"][0]["id"], "tc-1")
        self.assertEqual(result["test_strategy"]["test_cases"][0]["status"], "completed")
        self.assertEqual(result["test_strategy"]["test_cases"][1]["status"], "pending")
        self.assertIn("unit_tests", result["test_strategy"]["test_types"])
        self.assertEqual(len(result["test_strategy"]["validation_checklist"]), 3)
    
    def test_tc2_preserve_linkages(self):
        """
        TC-2: Preserve linkages between sections.
        Given: Markdown spec with explicit linkages
        When: Parser processes spec
        Then: Parsed data includes all linkages as structured references
        """
        spec_content = """# Spec: Linkage Test

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-20251023-linkage-test

## 1. Goals & Requirements

### 1.1 Primary Goal
Test linkage preservation.

### 1.2 User Stories
- **As a developer**, **I want** linkage tracking, **so that** I can trace dependencies.

### 1.3 Acceptance Criteria

- [ ] **AC-1**: Linkages preserved correctly
- [ ] **AC-2**: Cross-references maintained

## 2. Technical Design

### 2.1 Architecture Overview
**Approach**: Test approach

### 2.2 Components

- **Component 1**: TestComponent
  - **Location**: `test.py`
  - **Responsibility**: Test linkages
  - **Interfaces**: None
  - **Dependencies**: None
  - **Links to**: [Goals: AC-1, AC-2]

## 3. Implementation Plan

### 3.1 Task Breakdown

#### Task 1: Test Task
- **ID**: `task-1`
- **Description**: Test task with linkages
- **Agent**: backend-architect
- **Files**: `test.py`
- **Depends On**: none
- **Estimate**: 1 hour
- **Links to**:
  - Design: [2.2.Component-1]
  - Goals: [AC-1]
  - Tests: [tc-1, tc-2]
- **Status**: [ ] Pending

### 3.2 Execution Sequence
**Parallel Stage 1**: task-1

### 3.3 Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Test risk | Low | Low | Test mitigation |

## 4. Test Strategy

### 4.1 Test Cases

#### Test Case 1: Linkage Test
- **TC-ID**: `tc-1`
- **Description**: Verify linkages work
- **Given**: Spec with linkages
- **When**: Parse spec
- **Then**: Linkages preserved
- **Links to**:
  - Goals: [AC-1, AC-2]
  - Design: [2.2.Component-1]
  - Tasks: [task-1]
- **Status**: [ ] Pending

### 4.2 Test Types

- **Unit Tests**:
  - [ ] Linkage parsing

### 4.3 Validation Checklist

- [ ] Linkages verified
"""
        
        file_path = self._create_test_spec(spec_content)
        result = parse_spec(file_path)
        
        # Verify component linkages
        component_links = result["design"]["components"][0]["links_to"]
        self.assertIn("AC-1", component_links)
        self.assertIn("AC-2", component_links)
        
        # Verify task linkages
        task_links = result["implementation"]["tasks"][0]["links_to"]
        self.assertIn("2.2.Component-1", task_links)
        self.assertIn("AC-1", task_links)
        self.assertIn("tc-1", task_links)
        self.assertIn("tc-2", task_links)
        
        # Verify test case linkages
        tc_links = result["test_strategy"]["test_cases"][0]["links_to"]
        self.assertIn("AC-1", tc_links)
        self.assertIn("AC-2", tc_links)
        self.assertIn("2.2.Component-1", tc_links)
        self.assertIn("task-1", tc_links)
    
    def test_tc3_handle_malformed_markdown_missing_spec_id(self):
        """
        TC-3: Handle malformed Markdown (missing Spec ID).
        Given: Markdown spec with missing required section
        When: Parser processes spec
        Then: Raises ParseError with message indicating missing section
        """
        spec_content = """# Spec: Incomplete

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft

## 1. Goals & Requirements

### 1.1 Primary Goal
Missing spec ID.
"""
        
        file_path = self._create_test_spec(spec_content)
        
        with self.assertRaises(ParseError) as context:
            parse_spec(file_path)
        
        self.assertIn("Spec ID", str(context.exception))
    
    def test_tc3_handle_malformed_markdown_missing_created(self):
        """
        TC-3: Handle malformed Markdown (missing Created date).
        Given: Markdown spec missing Created date
        When: Parser processes spec
        Then: Raises ParseError
        """
        spec_content = """# Spec: Incomplete

**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-20251023-test

## 1. Goals & Requirements

### 1.1 Primary Goal
Missing created date.
"""
        
        file_path = self._create_test_spec(spec_content)
        
        with self.assertRaises(ParseError) as context:
            parse_spec(file_path)
        
        self.assertIn("Created", str(context.exception))
    
    def test_tc3_handle_nonexistent_file(self):
        """
        TC-3: Handle nonexistent file.
        Given: File path that doesn't exist
        When: Parser attempts to process
        Then: Raises FileNotFoundError
        """
        file_path = "/nonexistent/path/to/spec.md"
        
        with self.assertRaises(FileNotFoundError):
            parse_spec(file_path)
    
    def test_parse_user_stories(self):
        """Test parsing of user stories section."""
        spec_content = """# Spec: User Story Test

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-20251023-user-story-test

## 1. Goals & Requirements

### 1.1 Primary Goal
Test user story parsing.

### 1.2 User Stories
- **As a product owner**, **I want** feature prioritization, **so that** I can maximize value.
- **As a developer**, **I want** clear requirements, **so that** I can implement efficiently.
- **As an end user**, **I want** intuitive UI, **so that** I can accomplish tasks quickly.
"""
        
        file_path = self._create_test_spec(spec_content)
        result = parse_spec(file_path)
        
        user_stories = result["goals"]["user_stories"]
        self.assertEqual(len(user_stories), 3)

        # Verify first user story
        self.assertEqual(user_stories[0]["role"], "product owner")
        self.assertEqual(user_stories[0]["capability"], "feature prioritization")
        self.assertEqual(user_stories[0]["benefit"], "I can maximize value.")

        # Verify second user story
        self.assertEqual(user_stories[1]["role"], "developer")
        self.assertEqual(user_stories[1]["capability"], "clear requirements")

        # Verify third user story
        self.assertEqual(user_stories[2]["role"], "end user")
        self.assertEqual(user_stories[2]["benefit"], "I can accomplish tasks quickly.")
    
    def test_parse_architecture_decisions(self):
        """Test parsing of architecture key decisions."""
        spec_content = """# Spec: Architecture Test

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-20251023-arch-test

## 2. Technical Design

### 2.1 Architecture Overview
**Approach**: Microservices architecture

**Key Design Decisions**:
1. **Go over Python**: Better performance and concurrency
2. **PostgreSQL over MongoDB**: ACID compliance required
3. **Event-driven**: Enables loose coupling and scalability
"""
        
        file_path = self._create_test_spec(spec_content)
        result = parse_spec(file_path)
        
        decisions = result["design"]["architecture"]["key_decisions"]
        self.assertEqual(len(decisions), 3)
        
        self.assertEqual(decisions[0]["decision"], "Go over Python")
        self.assertIn("performance", decisions[0]["rationale"])
        
        self.assertEqual(decisions[1]["decision"], "PostgreSQL over MongoDB")
        self.assertIn("ACID", decisions[1]["rationale"])
    
    def test_parse_dependencies(self):
        """Test parsing of external dependencies."""
        spec_content = """# Spec: Dependency Test

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-20251023-dep-test

## 2. Technical Design

### 2.5 Dependencies
External libraries:

- **pyyaml** v6.0+ - YAML parsing and generation
- **jsonschema** v4.17+ - JSON Schema validation
- **click** v8.1+ - CLI framework
"""
        
        file_path = self._create_test_spec(spec_content)
        result = parse_spec(file_path)
        
        dependencies = result["design"]["dependencies"]
        self.assertEqual(len(dependencies), 3)
        
        self.assertEqual(dependencies[0]["name"], "pyyaml")
        self.assertEqual(dependencies[0]["version"], "v6.0+")
        self.assertIn("YAML", dependencies[0]["reason"])
        
        self.assertEqual(dependencies[1]["name"], "jsonschema")
        self.assertIn("validation", dependencies[1]["reason"])
    
    def test_parse_test_types(self):
        """Test parsing of test types section."""
        spec_content = """# Spec: Test Types Test

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-20251023-test-types

## 4. Test Strategy

### 4.2 Test Types
Breakdown by category:

- **Unit Tests**:
  - [x] Parser unit tests
  - [ ] Generator unit tests
  - [ ] CLI unit tests

- **Integration Tests**:
  - [x] End-to-end translation
  - [ ] Schema validation
"""
        
        file_path = self._create_test_spec(spec_content)
        result = parse_spec(file_path)
        
        test_types = result["test_strategy"]["test_types"]
        
        self.assertIn("unit_tests", test_types)
        self.assertEqual(len(test_types["unit_tests"]), 3)
        self.assertEqual(test_types["unit_tests"][0]["status"], "completed")
        self.assertEqual(test_types["unit_tests"][1]["status"], "pending")
        
        self.assertIn("integration_tests", test_types)
        self.assertEqual(len(test_types["integration_tests"]), 2)
        self.assertEqual(test_types["integration_tests"][0]["status"], "completed")
    
    def test_parse_real_spec_file(self):
        """Test parsing the actual spec file this implementation is based on."""
        # Use the real spec file path
        real_spec_path = "/Users/robertnyborg/Projects/claude-oak-agents/specs/active/2025-10-23-spec-to-yaml-translator.md"
        
        # Only run this test if the file exists
        if not Path(real_spec_path).exists():
            self.skipTest(f"Real spec file not found: {real_spec_path}")
        
        result = parse_spec(real_spec_path)
        
        # Verify it parses successfully
        self.assertIsNotNone(result)
        self.assertIn("metadata", result)
        self.assertIn("goals", result)
        self.assertIn("design", result)
        self.assertIn("implementation", result)
        self.assertIn("test_strategy", result)
        
        # Verify metadata
        self.assertEqual(result["metadata"]["spec_id"], "spec-20251023-spec-to-yaml-translator")
        
        # Verify we got some goals
        self.assertTrue(len(result["goals"]["user_stories"]) > 0)
        self.assertTrue(len(result["goals"]["acceptance_criteria"]) > 0)
        
        # Verify we got components
        self.assertTrue(len(result["design"]["components"]) > 0)
        
        # Verify we got tasks
        self.assertTrue(len(result["implementation"]["tasks"]) > 0)
        
        # Verify we got test cases
        self.assertTrue(len(result["test_strategy"]["test_cases"]) > 0)


if __name__ == '__main__':
    unittest.main()
