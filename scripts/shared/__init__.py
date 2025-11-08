"""
Shared utilities for OaK agents.

This package contains reusable utilities that multiple agents can import.
Only add utilities here when they're genuinely shared across 2+ agents.

Philosophy: KISS - Don't create abstractions until duplication proves they're needed.
"""

from .colors import Colors
from .telemetry_loader import load_invocations, get_recent_invocations, get_workflow_invocations
from .markdown_utils import parse_frontmatter, parse_frontmatter_string, get_metadata
from .cli_utils import create_base_parser, get_project_root
from .agent_utils import get_agent_category, get_category_color, get_agent_type_category

__version__ = "1.0.0"

__all__ = [
    'Colors',
    'load_invocations',
    'get_recent_invocations',
    'get_workflow_invocations',
    'parse_frontmatter',
    'parse_frontmatter_string',
    'get_metadata',
    'create_base_parser',
    'get_project_root',
    'get_agent_category',
    'get_category_color',
    'get_agent_type_category',
]
