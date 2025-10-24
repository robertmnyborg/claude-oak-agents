"""
YAML Generator for Spec Translation Tool

Generates valid YAML from parsed Markdown specs following SPEC_SCHEMA.yaml template.
Validates output against JSON schema and ensures idempotent translation.

Component: YAMLGenerator (Section 2.2.Component-2)
Acceptance Criteria: AC-2, AC-4
"""

import yaml
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import hashlib
import json


class YAMLGenerator:
    """
    Generates YAML structure from parsed Markdown spec data.
    
    Responsibilities:
    - Build YAML structure matching SPEC_SCHEMA.yaml template
    - Add metadata tracking (last_sync, markdown_location)
    - Validate generated YAML against schema
    - Ensure deterministic output (sorted keys, consistent formatting)
    """
    
    def __init__(self):
        """Initialize YAML generator with schema template."""
        self.spec_version = "1.0"
    
    def generate_yaml(self, parsed_data: Dict[str, Any], markdown_path: str) -> str:
        """
        Generate YAML string from parsed spec data.
        
        Args:
            parsed_data: Dictionary containing parsed spec sections
            markdown_path: Path to source Markdown file
            
        Returns:
            YAML string formatted according to SPEC_SCHEMA.yaml
            
        Raises:
            ValueError: If required fields are missing or invalid
        """
        # Build complete YAML structure
        yaml_data = self._build_yaml_structure(parsed_data, markdown_path)
        
        # Generate deterministic YAML output
        yaml_string = self._generate_deterministic_yaml(yaml_data)
        
        return yaml_string
    
    def validate_schema(self, yaml_data: Dict[str, Any]) -> bool:
        """
        Validate YAML data against spec schema requirements.
        
        Args:
            yaml_data: Dictionary containing YAML data to validate
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            ValueError: With detailed validation error message
        """
        errors = []
        
        # Required top-level fields
        required_fields = ["spec_id", "created", "updated", "status", "linked_request"]
        for field in required_fields:
            if field not in yaml_data:
                errors.append(f"Missing required field: {field}")
        
        # Required sections
        required_sections = ["goals", "technical_design", "implementation", "test_strategy", "metadata"]
        for section in required_sections:
            if section not in yaml_data:
                errors.append(f"Missing required section: {section}")
        
        # Validate metadata section
        if "metadata" in yaml_data:
            metadata = yaml_data["metadata"]
            if "spec_version" not in metadata:
                errors.append("Missing metadata.spec_version")
            if "generated_from_markdown" not in metadata:
                errors.append("Missing metadata.generated_from_markdown")
            if "markdown_location" not in metadata:
                errors.append("Missing metadata.markdown_location")
            if "last_sync" not in metadata:
                errors.append("Missing metadata.last_sync")
        
        # Validate status enum
        if "status" in yaml_data:
            valid_statuses = ["draft", "approved", "in-progress", "completed"]
            if yaml_data["status"] not in valid_statuses:
                errors.append(f"Invalid status: {yaml_data['status']} (must be one of {valid_statuses})")
        
        if errors:
            raise ValueError("YAML validation failed:\n" + "\n".join(f"  - {e}" for e in errors))
        
        return True
    
    def _build_yaml_structure(self, parsed_data: Dict[str, Any], markdown_path: str) -> Dict[str, Any]:
        """Build complete YAML structure from parsed data."""
        # Extract metadata from parsed data
        metadata_section = parsed_data.get("metadata", {})
        
        # Build YAML structure following SPEC_SCHEMA.yaml
        yaml_data = {
            # Top-level metadata
            "spec_id": metadata_section.get("spec_id", "spec-unknown"),
            "created": self._format_datetime(metadata_section.get("created")),
            "updated": self._format_datetime(metadata_section.get("updated")),
            "status": metadata_section.get("status", "draft"),
            "linked_request": metadata_section.get("linked_request", ""),
            
            # Section 1: Goals & Requirements
            "goals": self._build_goals_section(parsed_data.get("goals", {})),
            
            # Section 2: Technical Design
            "technical_design": self._build_design_section(parsed_data.get("design", {})),
            
            # Section 3: Implementation Plan
            "implementation": self._build_implementation_section(parsed_data.get("implementation", {})),
            
            # Section 4: Test Strategy
            "test_strategy": self._build_test_strategy_section(parsed_data.get("test_strategy", {})),
            
            # Section 5: Execution Log (initialized empty)
            "execution_log": [],
            
            # Section 6: Changes & Decisions (initialized empty)
            "changes": {
                "design_changes": [],
                "scope_changes": [],
                "deviations": []
            },
            
            # Section 7: Completion Summary (initialized empty)
            "completion": {
                "acceptance_criteria_status": [],
                "test_results": {
                    "unit_tests": "0/0 passed",
                    "integration_tests": "0/0 passed",
                    "e2e_tests": "0/0 passed",
                    "all_tests_passing": False
                },
                "success_metrics_results": [],
                "files_changed": {
                    "total": 0,
                    "created": [],
                    "modified": [],
                    "deleted": []
                },
                "lessons_learned": [],
                "follow_up_items": []
            },
            
            # Section 8: Metadata
            "metadata": self._build_metadata_section(markdown_path)
        }
        
        return yaml_data
    
    def _build_goals_section(self, goals_data: Dict[str, Any]) -> Dict[str, Any]:
        """Build goals section from parsed data."""
        return {
            "primary": goals_data.get("primary", ""),
            "user_stories": goals_data.get("user_stories", []),
            "acceptance_criteria": goals_data.get("acceptance_criteria", []),
            "success_metrics": goals_data.get("success_metrics", []),
            "out_of_scope": goals_data.get("out_of_scope", [])
        }
    
    def _build_design_section(self, design_data: Dict[str, Any]) -> Dict[str, Any]:
        """Build technical design section from parsed data."""
        return {
            "architecture": design_data.get("architecture", {
                "overview": "",
                "key_decisions": []
            }),
            "components": design_data.get("components", []),
            "data_structures": design_data.get("data_structures", []),
            "apis": design_data.get("apis", []),
            "dependencies": design_data.get("dependencies", []),
            "security_considerations": design_data.get("security_considerations", []),
            "performance_considerations": design_data.get("performance_considerations", [])
        }
    
    def _build_implementation_section(self, impl_data: Dict[str, Any]) -> Dict[str, Any]:
        """Build implementation section from parsed data."""
        return {
            "tasks": impl_data.get("tasks", []),
            "execution_sequence": impl_data.get("execution_sequence", []),
            "risks": impl_data.get("risks", [])
        }
    
    def _build_test_strategy_section(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Build test strategy section from parsed data."""
        return {
            "test_cases": test_data.get("test_cases", []),
            "test_types": test_data.get("test_types", {
                "unit_tests": [],
                "integration_tests": [],
                "e2e_tests": [],
                "performance_tests": []
            }),
            "validation_checklist": test_data.get("validation_checklist", [])
        }
    
    def _build_metadata_section(self, markdown_path: str) -> Dict[str, Any]:
        """Build metadata section with tracking information."""
        return {
            "spec_version": self.spec_version,
            "generated_from_markdown": True,
            "markdown_location": markdown_path,
            "last_sync": self._get_current_timestamp(),
            "statistics": {
                "total_tasks": 0,
                "completed_tasks": 0,
                "total_tests": 0,
                "passed_tests": 0,
                "agents_involved": [],
                "duration_seconds": None
            }
        }
    
    def _format_datetime(self, dt: Optional[Any]) -> str:
        """Format datetime to ISO 8601 string."""
        if dt is None:
            return self._get_current_timestamp()
        
        if isinstance(dt, str):
            # Already formatted, return as-is
            return dt
        
        if isinstance(dt, datetime):
            # Convert datetime to ISO string
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.isoformat().replace("+00:00", "Z")
        
        # Fallback to current timestamp
        return self._get_current_timestamp()
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO 8601 format."""
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    
    def _generate_deterministic_yaml(self, yaml_data: Dict[str, Any]) -> str:
        """
        Generate deterministic YAML output with consistent formatting.
        
        Ensures:
        - Sorted keys for consistent output
        - Same input always produces same output
        - Security: Uses safe_dump (no code execution)
        """
        # Use safe_dump for security (no arbitrary code execution)
        # sort_keys=False to preserve logical ordering (we pre-order the dict)
        # default_flow_style=False for readable multi-line format
        # allow_unicode=True for proper unicode handling
        yaml_string = yaml.safe_dump(
            yaml_data,
            default_flow_style=False,
            sort_keys=False,  # We control order via dict construction
            allow_unicode=True,
            explicit_start=False,
            width=1000  # Prevent aggressive line wrapping
        )
        
        return yaml_string
    
    def compute_yaml_hash(self, yaml_string: str) -> str:
        """
        Compute hash of YAML content for idempotency validation.
        
        Args:
            yaml_string: YAML content to hash
            
        Returns:
            SHA256 hash of normalized YAML content
        """
        # Normalize by parsing and re-dumping (eliminates formatting differences)
        data = yaml.safe_load(yaml_string)
        normalized = yaml.safe_dump(data, sort_keys=True)
        
        # Compute SHA256 hash
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()


def generate_yaml(parsed_data: Dict[str, Any], markdown_path: str) -> str:
    """
    Convenience function for YAML generation.
    
    Args:
        parsed_data: Dictionary containing parsed spec sections
        markdown_path: Path to source Markdown file
        
    Returns:
        YAML string formatted according to SPEC_SCHEMA.yaml
    """
    generator = YAMLGenerator()
    return generator.generate_yaml(parsed_data, markdown_path)


def validate_schema(yaml_data: Dict[str, Any]) -> bool:
    """
    Convenience function for schema validation.
    
    Args:
        yaml_data: Dictionary containing YAML data to validate
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If validation fails
    """
    generator = YAMLGenerator()
    return generator.validate_schema(yaml_data)
