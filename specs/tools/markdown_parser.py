"""
Markdown Spec Parser

Extracts structured data from Markdown specification files.
Parses sections: metadata, goals, design, implementation, test_strategy.
Preserves linkages and cross-references between sections.

Author: backend-architect
Task: task-1 (spec-20251023-spec-to-yaml-translator)
"""

import re
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime


class ParseError(Exception):
    """Raised when parsing fails due to invalid or missing sections."""
    pass


def parse_spec(file_path: str) -> Dict[str, Any]:
    """
    Parse Markdown spec file and extract structured data.
    
    Args:
        file_path: Path to Markdown spec file
        
    Returns:
        Dict matching ParsedSpec structure with all sections
        
    Raises:
        ParseError: If required sections are missing or malformed
        FileNotFoundError: If spec file doesn't exist
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Spec file not found: {file_path}")
    
    content = path.read_text(encoding='utf-8')
    
    # Parse all sections
    parsed = {
        "metadata": _parse_metadata(content, file_path),
        "goals": _parse_goals(content),
        "design": _parse_design(content),
        "implementation": _parse_implementation(content),
        "test_strategy": _parse_test_strategy(content)
    }
    
    return parsed


def _parse_metadata(content: str, file_path: str) -> Dict[str, str]:
    """Extract metadata from frontmatter (Created, Updated, Status, Spec ID)."""
    metadata = {}
    
    # Spec ID (required)
    spec_id_match = re.search(r'\*\*Spec ID\*\*:\s*(.+)', content)
    if not spec_id_match:
        raise ParseError(f"Missing required metadata: Spec ID in {file_path}")
    metadata["spec_id"] = spec_id_match.group(1).strip()
    
    # Created date (required)
    created_match = re.search(r'\*\*Created\*\*:\s*(.+)', content)
    if not created_match:
        raise ParseError(f"Missing required metadata: Created date in {file_path}")
    metadata["created"] = created_match.group(1).strip()
    
    # Updated date (required)
    updated_match = re.search(r'\*\*Updated\*\*:\s*(.+)', content)
    if not updated_match:
        raise ParseError(f"Missing required metadata: Updated date in {file_path}")
    metadata["updated"] = updated_match.group(1).strip()
    
    # Status (required)
    status_match = re.search(r'\*\*Status\*\*:\s*(.+)', content)
    if not status_match:
        raise ParseError(f"Missing required metadata: Status in {file_path}")
    metadata["status"] = status_match.group(1).strip()
    
    return metadata


def _parse_goals(content: str) -> Dict[str, Any]:
    """Extract Goals & Requirements section (1.x)."""
    goals = {
        "primary": "",
        "user_stories": [],
        "acceptance_criteria": [],
        "success_metrics": [],
        "out_of_scope": []
    }
    
    # Primary Goal (1.1)
    primary_match = re.search(
        r'### 1\.1 Primary Goal(.+?)(?=\n### |\n## |$)',
        content,
        re.DOTALL
    )
    if primary_match:
        goals["primary"] = primary_match.group(1).strip()
    
    # User Stories (1.2)
    user_stories_match = re.search(
        r'### 1\.2 User Stories(.+?)(?=\n### |\n## |$)',
        content,
        re.DOTALL
    )
    if user_stories_match:
        stories_text = user_stories_match.group(1)
        story_pattern = r'-\s+\*\*As an? (.+?)\*\*,\s+\*\*I want\*\*\s+(.+?),\s+\*\*so that\*\*\s+(.+?)(?=\n-|\n###|\n##|$)'
        for match in re.finditer(story_pattern, stories_text, re.DOTALL):
            goals["user_stories"].append({
                "role": match.group(1).strip(),
                "capability": match.group(2).strip(),
                "benefit": match.group(3).strip()
            })
    
    # Acceptance Criteria (1.3)
    ac_match = re.search(
        r'### 1\.3 Acceptance Criteria\n.+?\n\n(.+?)(?=###|\n##|$)',
        content,
        re.DOTALL
    )
    if ac_match:
        ac_text = ac_match.group(1)
        # Pattern: - [ ] **AC-1**: Description
        ac_pattern = r'-\s+\[([x ])\]\s+\*\*([A-Z]+-\d+)\*\*:\s+(.+?)(?=\n-|\n###|\n##|$)'
        for match in re.finditer(ac_pattern, ac_text, re.DOTALL):
            status = "completed" if match.group(1).strip() == "x" else "pending"
            criterion_text = match.group(3).strip()
            
            # Extract linkages from criterion
            links = _extract_linkages(criterion_text)
            
            goals["acceptance_criteria"].append({
                "id": match.group(2).strip(),
                "criterion": criterion_text,
                "status": status,
                "linked_tasks": [l for l in links if l.startswith("task-")],
                "linked_tests": [l for l in links if l.startswith("tc-")]
            })
    
    # Success Metrics (1.4)
    metrics_match = re.search(
        r'### 1\.4 Success Metrics\n.+?\n\n(.+?)(?=\n### |\n## |$)',
        content,
        re.DOTALL
    )
    if metrics_match:
        metrics_text = metrics_match.group(1)
        metric_pattern = r'-\s+(.+?)(?:\n(?=-)|$)'
        for match in re.finditer(metric_pattern, metrics_text):
            goals["success_metrics"].append(match.group(1).strip())
    
    # Out of Scope (1.5)
    oos_match = re.search(
        r'### 1\.5 Out of Scope\n.+?\n\n(.+?)(?=\n### |\n## |\n---|$)',
        content,
        re.DOTALL
    )
    if oos_match:
        oos_text = oos_match.group(1)
        oos_pattern = r'-\s+(.+?)(?:\n(?=-)|$)'
        for match in re.finditer(oos_pattern, oos_text):
            goals["out_of_scope"].append(match.group(1).strip())
    
    return goals


def _parse_design(content: str) -> Dict[str, Any]:
    """Extract Technical Design section (2.x)."""
    design = {
        "architecture": {"overview": "", "key_decisions": []},
        "components": [],
        "data_structures": [],
        "apis": [],
        "dependencies": [],
        "security_considerations": [],
        "performance_considerations": []
    }
    
    # Architecture Overview (2.1)
    arch_match = re.search(
        r'### 2\.1 Architecture Overview\n(.+?)(?=###|\n##|$)',
        content,
        re.DOTALL
    )
    if arch_match:
        arch_text = arch_match.group(1)
        
        # Extract overview (before "Key Design Decisions")
        overview_match = re.search(r'\*\*Approach\*\*:\s*(.+?)(?=\n\n|\*\*Key Design Decisions\*\*|$)', arch_text, re.DOTALL)
        if overview_match:
            design["architecture"]["overview"] = overview_match.group(1).strip()
        
        # Extract key decisions
        decisions_match = re.search(r'\*\*Key Design Decisions\*\*:\n(.+?)(?=###|\n##|$)', arch_text, re.DOTALL)
        if decisions_match:
            decisions_text = decisions_match.group(1)
            decision_pattern = r'\d+\.\s+\*\*(.+?)\*\*:\s+(.+?)(?=\n\d+\.|\n###|\n##|$)'
            for match in re.finditer(decision_pattern, decisions_text, re.DOTALL):
                design["architecture"]["key_decisions"].append({
                    "decision": match.group(1).strip(),
                    "rationale": match.group(2).strip()
                })
    
    # Components (2.2)
    components_match = re.search(
        r'### 2\.2 Components(.+?)(?=\n### |\n## |$)',
        content,
        re.DOTALL
    )
    if components_match:
        components_text = components_match.group(1)
        # Pattern: - **Component N**: Name
        component_pattern = r'-\s+\*\*Component \d+\*\*:\s+(.+?)\n(.+?)(?=\n-\s+\*\*Component|\n###|\n##|$)'
        for match in re.finditer(component_pattern, components_text, re.DOTALL):
            component_name = match.group(1).strip()
            component_details = match.group(2).strip()

            # Extract component details
            component = {
                "name": component_name,
                "location": _extract_field(component_details, "Location"),
                "responsibility": _extract_field(component_details, "Responsibility"),
                "interfaces": _extract_list_field(component_details, "Interfaces"),
                "dependencies": _extract_list_field(component_details, "Dependencies"),
                "links_to": _extract_linkages(component_details)
            }
            design["components"].append(component)
    
    # Data Structures (2.3)
    data_structures_match = re.search(
        r'### 2\.3 Data Structures\n(.+?)(?=###|\n##|$)',
        content,
        re.DOTALL
    )
    if data_structures_match:
        ds_text = data_structures_match.group(1)
        # Extract YAML/code block data structures
        code_block_pattern = r'```(?:yaml)?\n(.+?)\n```'
        for match in re.finditer(code_block_pattern, ds_text, re.DOTALL):
            design["data_structures"].append({
                "definition": match.group(1).strip()
            })
    
    # APIs / Interfaces (2.4)
    apis_match = re.search(
        r'### 2\.4 APIs / Interfaces\n(.+?)(?=###|\n##|$)',
        content,
        re.DOTALL
    )
    if apis_match:
        apis_text = apis_match.group(1)
        # Extract code blocks (bash examples)
        code_block_pattern = r'```bash\n(.+?)\n```'
        for match in re.finditer(code_block_pattern, apis_text, re.DOTALL):
            design["apis"].append({
                "example": match.group(1).strip()
            })
    
    # Dependencies (2.5)
    deps_match = re.search(
        r'### 2\.5 Dependencies\n.+?\n\n(.+?)(?=###|\n##|$)',
        content,
        re.DOTALL
    )
    if deps_match:
        deps_text = deps_match.group(1)
        # Pattern: - **name** version - reason
        dep_pattern = r'-\s+\*\*(.+?)\*\*\s+(.+?)\s+-\s+(.+?)(?=\n-|\n###|\n##|$)'
        for match in re.finditer(dep_pattern, deps_text):
            design["dependencies"].append({
                "name": match.group(1).strip(),
                "version": match.group(2).strip(),
                "reason": match.group(3).strip(),
                "type": "external"
            })
    
    # Security Considerations (2.6)
    security_match = re.search(
        r'### 2\.6 Security Considerations\n(.+?)(?=###|\n##|$)',
        content,
        re.DOTALL
    )
    if security_match:
        security_text = security_match.group(1)
        security_pattern = r'-\s+\*\*(.+?)\*\*:\s+(.+?)(?=\n-|\n###|\n##|$)'
        for match in re.finditer(security_pattern, security_text):
            design["security_considerations"].append({
                "concern": match.group(1).strip(),
                "mitigation": match.group(2).strip()
            })
    
    # Performance Considerations (2.7)
    performance_match = re.search(
        r'### 2\.7 Performance Considerations\n(.+?)(?=###|\n##|$)',
        content,
        re.DOTALL
    )
    if performance_match:
        perf_text = performance_match.group(1)
        perf_pattern = r'-\s+\*\*(.+?)\*\*:\s+(.+?)(?=\n-|\n###|\n##|$)'
        for match in re.finditer(perf_pattern, perf_text):
            design["performance_considerations"].append({
                "metric": match.group(1).strip(),
                "target": match.group(2).strip()
            })
    
    return design


def _parse_implementation(content: str) -> Dict[str, Any]:
    """Extract Implementation Plan section (3.x)."""
    implementation = {
        "tasks": [],
        "execution_sequence": [],
        "risks": []
    }
    
    # Tasks (3.1)
    tasks_match = re.search(
        r'### 3\.1 Task Breakdown(.+?)(?=\n### |\n## |$)',
        content,
        re.DOTALL
    )
    if tasks_match:
        tasks_text = tasks_match.group(1)
        # Pattern: #### Task N: Name
        task_pattern = r'#### (.+?)\n(.+?)(?=\n####|\n###|\n##|$)'
        for match in re.finditer(task_pattern, tasks_text, re.DOTALL):
            task_name = match.group(1).strip()
            task_details = match.group(2).strip()
            
            # Extract task fields
            task = {
                "name": task_name,
                "id": _extract_field(task_details, "ID"),
                "description": _extract_field(task_details, "Description"),
                "agent": _extract_field(task_details, "Agent"),
                "files": _extract_list_field(task_details, "Files"),
                "depends_on": _extract_field(task_details, "Depends On"),
                "estimate": _extract_field(task_details, "Estimate"),
                "status": _extract_checkbox_field(task_details, "Status"),
                "links_to": _extract_linkages(task_details)
            }
            implementation["tasks"].append(task)
    
    # Execution Sequence (3.2)
    sequence_match = re.search(
        r'### 3\.2 Execution Sequence(.+?)(?=\n### |\n## |$)',
        content,
        re.DOTALL
    )
    if sequence_match:
        sequence_text = sequence_match.group(1)
        # Extract stages from text (simple parsing)
        stage_pattern = r'\*\*(Parallel Stage|Sequential Stage) \d+\*\*:\s+([^\n]+)'
        for match in re.finditer(stage_pattern, sequence_text):
            stage_type = "parallel" if "Parallel" in match.group(1) else "sequential"
            tasks_text = match.group(2).strip()
            implementation["execution_sequence"].append({
                "stage": stage_type,
                "tasks": [t.strip() for t in re.split(r'\s*\+\s*', tasks_text)]
            })
    
    # Risks (3.3)
    risks_match = re.search(
        r'### 3\.3 Risk Assessment(.+?)(?=\n### |\n## |$)',
        content,
        re.DOTALL
    )
    if risks_match:
        risks_text = risks_match.group(1)
        # Table format: | Risk | Impact | Probability | Mitigation |
        risk_pattern = r'\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|'
        for match in re.finditer(risk_pattern, risks_text):
            # Skip table header and separator
            risk_text = match.group(1).strip()
            if risk_text == "Risk" or risk_text.startswith("---"):
                continue
            implementation["risks"].append({
                "risk": risk_text,
                "impact": match.group(2).strip(),
                "probability": match.group(3).strip(),
                "mitigation": match.group(4).strip(),
                "status": "identified"
            })
    
    return implementation


def _parse_test_strategy(content: str) -> Dict[str, Any]:
    """Extract Test Strategy section (4.x)."""
    test_strategy = {
        "test_cases": [],
        "test_types": {},
        "validation_checklist": []
    }
    
    # Test Cases (4.1)
    test_cases_match = re.search(
        r'### 4\.1 Test Cases(.+?)(?=\n### |\n## |$)',
        content,
        re.DOTALL
    )
    if test_cases_match:
        tc_text = test_cases_match.group(1)
        # Pattern: #### Test Case N: Name
        tc_pattern = r'#### (.+?)\n(.+?)(?=\n####|\n###|\n##|$)'
        for match in re.finditer(tc_pattern, tc_text, re.DOTALL):
            tc_name = match.group(1).strip()
            tc_details = match.group(2).strip()
            
            # Extract test case fields
            test_case = {
                "name": tc_name,
                "id": _extract_field(tc_details, "TC-ID"),
                "description": _extract_field(tc_details, "Description"),
                "given": _extract_field(tc_details, "Given"),
                "when": _extract_field(tc_details, "When"),
                "then": _extract_field(tc_details, "Then"),
                "links_to": _extract_linkages(tc_details),
                "status": _extract_checkbox_field(tc_details, "Status"),
                "test_type": "unit"  # Default, could be inferred from description
            }
            test_strategy["test_cases"].append(test_case)
    
    # Test Types (4.2)
    test_types_match = re.search(
        r'### 4\.2 Test Types(.+?)(?=\n### |\n## |$)',
        content,
        re.DOTALL
    )
    if test_types_match:
        tt_text = test_types_match.group(1)
        # Extract test type categories with checkboxes
        type_categories = ["Unit Tests", "Integration Tests", "End-to-End Tests", "Performance Tests"]
        for category in type_categories:
            category_pattern = rf'-\s+\*\*{category}\*\*:\n(.+?)(?=\n-\s+\*\*|\n###|\n##|$)'
            category_match = re.search(category_pattern, tt_text, re.DOTALL)
            if category_match:
                tests_text = category_match.group(1)
                # Match both bulleted items with checkboxes and without
                checkbox_pattern = r'(?:^|\n)\s+-\s+\[([x ])\]\s+(.+?)(?=\n\s+-\s+\[|$)'
                tests = []
                for checkbox_match in re.finditer(checkbox_pattern, tests_text, re.DOTALL):
                    status = "completed" if checkbox_match.group(1).strip() == "x" else "pending"
                    test_text = checkbox_match.group(2).strip()
                    # Remove trailing newlines and extra whitespace
                    test_text = test_text.split('\n')[0].strip()
                    tests.append({
                        "test": test_text,
                        "status": status
                    })
                category_key = category.lower().replace(" ", "_").replace("-", "_")
                test_strategy["test_types"][category_key] = tests
    
    # Validation Checklist (4.3)
    checklist_match = re.search(
        r'### 4\.3 Validation Checklist\n.+?\n\n(.+?)(?=###|\n##|$)',
        content,
        re.DOTALL
    )
    if checklist_match:
        checklist_text = checklist_match.group(1)
        checkbox_pattern = r'-\s+\[([x ])\]\s+(.+?)(?=\n-|\n###|\n##|$)'
        for match in re.finditer(checkbox_pattern, checklist_text):
            status = "completed" if match.group(1).strip() == "x" else "pending"
            test_strategy["validation_checklist"].append({
                "check": match.group(2).strip(),
                "status": status
            })
    
    return test_strategy


def _extract_linkages(text: str) -> List[str]:
    """Extract linkage references from 'Links to:' annotations."""
    linkages = []
    
    # Pattern: Links to: [AC-1, TC-2] or Links to: [Goals: AC-1]
    links_pattern = r'\*\*Links to\*\*:\s*\n?\s*-?\s*(.+?)(?=\n-\s+\*\*|\n###|\n##|\n####|$)'
    links_match = re.search(links_pattern, text, re.DOTALL)
    
    if links_match:
        links_text = links_match.group(1).strip()
        # Extract individual references
        # Pattern matches: AC-1, tc-2, [2.2.Component-1], task-1, etc.
        ref_pattern = r'([A-Za-z]+-\d+|\[\d+\.\d+\.[\w-]+\]|task-\d+|tc-\d+)'
        for ref_match in re.finditer(ref_pattern, links_text):
            linkages.append(ref_match.group(1).strip('[]'))
    
    return linkages


def _extract_field(text: str, field_name: str) -> str:
    """Extract single field value (e.g., 'ID: task-1')."""
    # Try with backticks first
    pattern = rf'-\s+\*\*{field_name}\*\*:\s+`(.+?)`'
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()

    # Try without backticks (match until newline)
    pattern = rf'-\s+\*\*{field_name}\*\*:\s+([^\n]+)'
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()

    return ""


def _extract_list_field(text: str, field_name: str) -> List[str]:
    """Extract list field values (e.g., 'Files: file1.py, file2.py')."""
    pattern = rf'-\s+\*\*{field_name}\*\*:\s+([^\n]+)'
    match = re.search(pattern, text)
    if match:
        values_text = match.group(1).strip()
        # Remove backticks and split by comma
        values_text = values_text.replace('`', '')
        return [v.strip() for v in values_text.split(',') if v.strip()]
    return []


def _extract_checkbox_field(text: str, field_name: str) -> str:
    """Extract checkbox status field (e.g., 'Status: [ ] Pending')."""
    pattern = rf'-\s+\*\*{field_name}\*\*:\s+\[([x ])\]'
    match = re.search(pattern, text)
    if match:
        checkbox = match.group(1).strip()
        return "completed" if checkbox == "x" else "pending"

    # Fallback: try without checkbox
    fallback_pattern = rf'-\s+\*\*{field_name}\*\*:\s+([^\n]+)'
    fallback_match = re.search(fallback_pattern, text)
    if fallback_match:
        status_text = fallback_match.group(1).strip().lower()
        if "pending" in status_text or "[ ]" in status_text:
            return "pending"
        elif "completed" in status_text or "[x]" in status_text:
            return "completed"

    return "pending"
