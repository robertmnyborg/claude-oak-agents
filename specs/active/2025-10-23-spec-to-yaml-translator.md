# Spec: Spec-to-YAML Translation Tool

**Created**: 2025-10-23
**Updated**: 2025-10-23
**Status**: draft
**Spec ID**: spec-20251023-spec-to-yaml-translator
**Linked Request**: "Create a tool to automatically translate Markdown specs to YAML format for agent consumption"

---

## 1. Goals & Requirements

### 1.1 Primary Goal
Build an automated translation tool that converts human-readable Markdown specification files into structured YAML format suitable for agent consumption, enabling the spec-driven development workflow.

### 1.2 User Stories
- **As a spec-manager agent**, **I want** to automatically convert approved Markdown specs to YAML, **so that** I can provide structured data to execution agents without manual transcription.
- **As a developer**, **I want** changes to the Markdown spec to automatically sync to YAML, **so that** both formats remain consistent throughout the development lifecycle.
- **As an execution agent**, **I want** to consume structured YAML specs, **so that** I can programmatically access task assignments, dependencies, and acceptance criteria.

### 1.3 Acceptance Criteria
Clear, testable criteria that define "done":

- [ ] **AC-1**: Tool reads Markdown spec file and extracts all sections (Goals, Design, Implementation, Tests)
- [ ] **AC-2**: Tool generates valid YAML following the spec schema defined in `specs/templates/SPEC_SCHEMA.yaml`
- [ ] **AC-3**: All linkages are preserved (goals ↔ design ↔ tasks ↔ tests with explicit references)
- [ ] **AC-4**: Generated YAML passes JSON schema validation
- [ ] **AC-5**: Tool handles incremental updates (regenerate YAML when Markdown changes)
- [ ] **AC-6**: Metadata tracks last sync timestamp and Markdown source location

### 1.4 Success Metrics
How we measure if this was valuable:

- Translation accuracy: 100% of valid Markdown specs produce valid YAML
- Sync reliability: YAML always reflects current Markdown state
- Agent adoption: Execution agents successfully use YAML specs for task coordination
- User satisfaction: spec-manager workflow functions without manual YAML editing

### 1.5 Out of Scope
What we're explicitly NOT doing (prevents scope creep):

- Reverse translation (YAML → Markdown) - Markdown is source of truth
- Visual spec editor or GUI - command-line tool only
- Automatic spec generation from code - manual spec authoring required
- Real-time collaborative editing - file-based workflow sufficient

---

## 2. Technical Design

### 2.1 Architecture Overview
**Approach**: Python-based parser using regex and YAML libraries

The tool will use a two-phase approach:
1. **Parse Phase**: Extract structured data from Markdown using regex patterns for each section
2. **Generate Phase**: Build YAML structure following the schema template

**Key Design Decisions**:
1. **Python over Shell**: Better regex support, YAML library ecosystem, easier testing
2. **Template-driven**: Use schema template as validation guide
3. **Fail-fast**: Strict validation, clear error messages on parse failures
4. **Idempotent**: Same Markdown always produces same YAML output

### 2.2 Components
Breakdown of system components:

- **Component 1**: MarkdownParser
  - **Location**: `specs/tools/markdown_parser.py`
  - **Responsibility**: Extract structured data from Markdown spec sections
  - **Interfaces**:
    - `parse_spec(file_path: str) -> Dict[str, Any]`
  - **Dependencies**: `re` (regex), `pathlib` (file handling)
  - **Links to**: [Goals: AC-1, AC-3]

- **Component 2**: YAMLGenerator
  - **Location**: `specs/tools/yaml_generator.py`
  - **Responsibility**: Build YAML structure from parsed data
  - **Interfaces**:
    - `generate_yaml(parsed_data: Dict) -> str`
    - `validate_schema(yaml_data: Dict) -> bool`
  - **Dependencies**: `pyyaml`, `jsonschema` (validation)
  - **Links to**: [Goals: AC-2, AC-4]

- **Component 3**: TranslationCLI
  - **Location**: `specs/tools/translate_spec.py`
  - **Responsibility**: CLI entry point for translation workflow
  - **Interfaces**:
    - `translate(markdown_file: str, output_file: str)`
    - `validate(yaml_file: str) -> bool`
  - **Dependencies**: markdown_parser, yaml_generator
  - **Links to**: [Goals: AC-5, AC-6]

### 2.3 Data Structures
Key data models and schemas:

```yaml
# Parsed Spec Data Structure
ParsedSpec:
  metadata:
    spec_id: str
    created: datetime
    updated: datetime
    status: str
  goals:
    primary: str
    user_stories: List[UserStory]
    acceptance_criteria: List[AcceptanceCriterion]
    success_metrics: List[str]
    out_of_scope: List[str]
  design:
    architecture: ArchitectureOverview
    components: List[Component]
    data_structures: List[DataStructure]
    apis: List[API]
    dependencies: List[Dependency]
  implementation:
    tasks: List[Task]
    execution_sequence: List[Stage]
    risks: List[Risk]
  test_strategy:
    test_cases: List[TestCase]
    test_types: TestTypes
    validation_checklist: List[ChecklistItem]
```

**Links to**: [Goals: AC-1, AC-3]

### 2.4 APIs / Interfaces

**CLI Interface**:
```bash
# Translate Markdown to YAML
python specs/tools/translate_spec.py \
  --input specs/active/YYYY-MM-DD-feature.md \
  --output specs/active/YYYY-MM-DD-feature.yaml \
  --validate

# Validate existing YAML
python specs/tools/translate_spec.py \
  --validate-yaml specs/active/YYYY-MM-DD-feature.yaml

# Watch for changes (auto-regenerate)
python specs/tools/translate_spec.py \
  --watch specs/active/YYYY-MM-DD-feature.md
```

**Links to**: [Goals: AC-5, AC-6]

### 2.5 Dependencies
External libraries, services, systems:

- **pyyaml** v6.0+ - YAML parsing and generation
- **jsonschema** v4.17+ - JSON Schema validation
- **watchdog** v3.0+ - File watching for auto-regeneration (optional)
- **click** v8.1+ - CLI framework (optional, could use argparse)

### 2.6 Security Considerations
- **Input validation**: Sanitize file paths to prevent directory traversal
- **Safe YAML**: Use `yaml.safe_load` and `yaml.safe_dump` only (no arbitrary code execution)
- **Error handling**: Don't expose file system structure in error messages

**Links to**: [Goals: AC-4 (validation prevents malformed data)]

### 2.7 Performance Considerations
- **Target performance**: <500ms for typical spec (<10KB Markdown)
- **Optimization strategy**: Lazy parsing (only parse sections when needed)
- **Caching**: No caching needed (translation is deterministic and fast)

**Links to**: [Goals: AC-5 (fast regeneration enables incremental workflow)]

---

## 3. Implementation Plan

### 3.1 Task Breakdown
Detailed tasks with clear agent assignments:

#### Task 1: Create Markdown Parser
- **ID**: `task-1`
- **Description**: Build regex-based parser to extract structured data from Markdown spec sections
- **Agent**: backend-architect
- **Files**: `specs/tools/markdown_parser.py`, `specs/tools/test_markdown_parser.py`
- **Depends On**: none
- **Estimate**: moderate (4-6 hours)
- **Links to**:
  - Design: [2.2.Component-1 (MarkdownParser)]
  - Goals: [AC-1, AC-3]
  - Tests: [tc-1, tc-2, tc-3]
- **Status**: [ ] Pending

#### Task 2: Create YAML Generator
- **ID**: `task-2`
- **Description**: Build YAML structure generator with schema validation
- **Agent**: backend-architect
- **Files**: `specs/tools/yaml_generator.py`, `specs/tools/test_yaml_generator.py`
- **Depends On**: none (can parallelize with task-1)
- **Estimate**: simple (2-3 hours)
- **Links to**:
  - Design: [2.2.Component-2 (YAMLGenerator)]
  - Goals: [AC-2, AC-4]
  - Tests: [tc-4, tc-5]
- **Status**: [ ] Pending

#### Task 3: Create CLI Tool
- **ID**: `task-3`
- **Description**: Build command-line interface orchestrating parser + generator
- **Agent**: backend-architect
- **Files**: `specs/tools/translate_spec.py`, `specs/tools/test_cli.py`
- **Depends On**: task-1, task-2
- **Estimate**: simple (2-3 hours)
- **Links to**:
  - Design: [2.2.Component-3 (TranslationCLI)]
  - Goals: [AC-5, AC-6]
  - Tests: [tc-6, tc-7]
- **Status**: [ ] Pending

#### Task 4: Integration Testing
- **ID**: `task-4`
- **Description**: End-to-end integration tests with real spec examples
- **Agent**: unit-test-expert
- **Files**: `specs/tools/test_integration.py`
- **Depends On**: task-3
- **Estimate**: simple (2 hours)
- **Links to**:
  - Design: [All components]
  - Goals: [AC-1 through AC-6]
  - Tests: [tc-8]
- **Status**: [ ] Pending

#### Task 5: Documentation
- **ID**: `task-5`
- **Description**: README for translation tool with usage examples
- **Agent**: technical-documentation-writer
- **Files**: `specs/tools/README.md`
- **Depends On**: task-4
- **Estimate**: trivial (1 hour)
- **Links to**:
  - Design: [2.4 (CLI Interface)]
  - Goals: [All (documentation of complete feature)]
  - Tests: [Validation checklist item]
- **Status**: [ ] Pending

### 3.2 Execution Sequence
Visualization of task dependencies:

```
task-1 (Parser) ────────┐
                        ↓
task-2 (Generator) ──→ task-3 (CLI) → task-4 (Integration Tests) → task-5 (Docs)
```

**Parallel Stage 1**: task-1 + task-2 (can run concurrently)
**Sequential Stage 2**: task-3 → task-4 → task-5

**Estimated Total**: 11-15 hours

### 3.3 Risk Assessment
Potential blockers and mitigation:

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Markdown structure varies between specs | High | Medium | Define strict Markdown format rules, fail with clear errors |
| YAML schema changes break translations | Medium | Low | Version schema, test against multiple schema versions |
| Parser regex too brittle | High | Medium | Comprehensive test suite covering edge cases, use AST parser if regex insufficient |
| Performance issues with large specs | Low | Low | Profile and optimize if >500ms, lazy parsing if needed |

---

## 4. Test Strategy

### 4.1 Test Cases
Comprehensive test scenarios linked to requirements:

#### Test Case 1: Parse Complete Spec
- **TC-ID**: `tc-1`
- **Description**: Parser extracts all sections from valid Markdown spec
- **Given**: Valid Markdown spec with all sections (Goals, Design, Implementation, Tests)
- **When**: Parser processes spec file
- **Then**: Parsed data structure contains all sections with correct values
- **Links to**:
  - Goals: [AC-1]
  - Design: [2.2.Component-1]
  - Tasks: [task-1]
- **Status**: [ ] Pending

#### Test Case 2: Preserve Linkages
- **TC-ID**: `tc-2`
- **Description**: Parser preserves cross-references between sections
- **Given**: Markdown spec with explicit linkages (e.g., "Links to: AC-1, TC-2")
- **When**: Parser processes spec
- **Then**: Parsed data includes all linkages as structured references
- **Links to**:
  - Goals: [AC-3]
  - Design: [2.2.Component-1, 2.3.DataStructures]
  - Tasks: [task-1]
- **Status**: [ ] Pending

#### Test Case 3: Handle Malformed Markdown
- **TC-ID**: `tc-3`
- **Description**: Parser fails gracefully with clear errors on invalid input
- **Given**: Markdown spec with missing required sections
- **When**: Parser processes spec
- **Then**: Raises ParseError with message indicating missing section
- **Links to**:
  - Goals: [AC-1 (robustness)]
  - Design: [2.6.SecurityConsiderations]
  - Tasks: [task-1]
- **Status**: [ ] Pending

#### Test Case 4: Generate Valid YAML
- **TC-ID**: `tc-4`
- **Description**: Generator produces schema-compliant YAML
- **Given**: Parsed spec data structure
- **When**: Generator creates YAML
- **Then**: Output validates against `specs/templates/SPEC_SCHEMA.yaml`
- **Links to**:
  - Goals: [AC-2, AC-4]
  - Design: [2.2.Component-2]
  - Tasks: [task-2]
- **Status**: [ ] Pending

#### Test Case 5: Idempotent Translation
- **TC-ID**: `tc-5`
- **Description**: Same Markdown produces identical YAML every time
- **Given**: Single Markdown spec file
- **When**: Translate to YAML twice
- **Then**: Both YAML outputs are byte-for-byte identical
- **Links to**:
  - Goals: [AC-5 (deterministic sync)]
  - Design: [2.1.ArchitectureOverview]
  - Tasks: [task-2]
- **Status**: [ ] Pending

#### Test Case 6: CLI End-to-End
- **TC-ID**: `tc-6`
- **Description**: CLI tool translates Markdown to YAML successfully
- **Given**: Valid Markdown spec file
- **When**: Run `translate_spec.py --input spec.md --output spec.yaml --validate`
- **Then**: YAML file created, validation passes, exit code 0
- **Links to**:
  - Goals: [AC-5, AC-6]
  - Design: [2.2.Component-3, 2.4.APIs]
  - Tasks: [task-3]
- **Status**: [ ] Pending

#### Test Case 7: Metadata Tracking
- **TC-ID**: `tc-7`
- **Description**: YAML includes sync metadata
- **Given**: Translated YAML spec
- **When**: Inspect metadata section
- **Then**: Contains `last_sync` timestamp and `markdown_location` path
- **Links to**:
  - Goals: [AC-6]
  - Design: [2.2.Component-3]
  - Tasks: [task-3]
- **Status**: [ ] Pending

#### Test Case 8: Integration with Real Spec
- **TC-ID**: `tc-8`
- **Description**: Tool works with actual spec-driven workflow
- **Given**: This spec file (dogfooding!)
- **When**: Translate this spec to YAML
- **Then**: Generated YAML is valid and usable by spec-manager
- **Links to**:
  - Goals: [All AC-1 through AC-6]
  - Design: [All components]
  - Tasks: [task-4]
- **Status**: [ ] Pending

### 4.2 Test Types
Breakdown by test category:

- **Unit Tests**:
  - [ ] MarkdownParser unit tests (tc-1, tc-2, tc-3)
  - [ ] YAMLGenerator unit tests (tc-4, tc-5)
  - [ ] CLI unit tests (tc-6, tc-7)

- **Integration Tests**:
  - [ ] End-to-end translation (tc-8)
  - [ ] Schema validation integration
  - [ ] Error handling integration

- **End-to-End Tests**:
  - [ ] Translate real specs from `specs/active/`
  - [ ] spec-manager consumes generated YAML

- **Performance Tests**:
  - [ ] Translation completes in <500ms for typical spec
  - [ ] Memory usage remains <50MB for large specs

### 4.3 Validation Checklist
Final sign-off criteria:

- [ ] All test cases pass (tc-1 through tc-8)
- [ ] All acceptance criteria met (AC-1 through AC-6)
- [ ] No critical bugs or regressions
- [ ] Code reviewed and approved
- [ ] Documentation updated (README.md, docstrings)
- [ ] Success metrics baseline established (100% translation accuracy achieved)

---

## 5. Agent Execution Log

**Note**: This section will be auto-populated during implementation by spec-manager.

*No execution logged yet - spec is in draft status*

---

## 6. Changes & Decisions

**Note**: This section tracks deviations from the original plan during implementation.

*No changes yet - spec is in draft status*

---

## 7. Completion Summary

**Note**: Filled in when spec status changes to "completed".

*Not yet completed*

---

## Appendix

### References
- [SPEC_TEMPLATE.md](../templates/SPEC_TEMPLATE.md) - Template this spec follows
- [SPEC_SCHEMA.yaml](../templates/SPEC_SCHEMA.yaml) - Target YAML schema
- [spec-manager.md](../../agents/spec-manager.md) - Agent that will use this tool

### Glossary
- **Markdown spec**: Human-readable specification in Markdown format (source of truth)
- **YAML spec**: Machine-readable specification in YAML format (derived from Markdown)
- **Linkage**: Explicit cross-reference between spec sections (e.g., tasks link to acceptance criteria)
- **Spec-manager**: Agent responsible for spec-driven development workflow
- **Execution agent**: Domain specialist agent that implements tasks defined in spec
