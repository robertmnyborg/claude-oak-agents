"""Agent metadata and categorization utilities."""

from typing import Dict


def get_agent_category(agent_name: str) -> str:
    """
    Map agent name to display category.
    
    Returns:
        Category name for display grouping
    """
    categories = {
        'product': ['product-strategist', 'business-analyst', 'spec-manager'],
        'development': ['frontend-developer', 'backend-architect', 'mobile-developer', 
                       'blockchain-developer', 'ml-engineer'],
        'quality': ['code-reviewer', 'quality-gate', 'unit-test-expert', 'qa-specialist'],
        'security': ['security-auditor', 'dependency-scanner'],
        'infrastructure': ['infrastructure-specialist', 'systems-architect'],
        'workflow': ['git-workflow-manager', 'project-manager', 'changelog-recorder'],
        'analysis': ['data-scientist', 'state-analyzer', 'agent-auditor', 
                    'performance-optimizer', 'debug-specialist'],
        'documentation': ['technical-writer', 'content-writer'],
        'special': ['design-simplicity-advisor', 'agent-creator', 'general-purpose']
    }
    
    for category, agents in categories.items():
        if agent_name in agents:
            return category
    
    return 'other'


def get_category_color(category: str) -> str:
    """Get display color for agent category."""
    colors = {
        'product': 'BLUE',
        'development': 'GREEN',
        'quality': 'CYAN',
        'security': 'RED',
        'infrastructure': 'MAGENTA',
        'workflow': 'YELLOW',
        'analysis': 'CYAN',
        'documentation': 'BLUE',
        'special': 'MAGENTA'
    }
    return colors.get(category, 'WHITE')


def get_agent_type_category(agent_type: str) -> str:
    """
    Map agent_type metadata to display category.
    
    This is used when reading from frontmatter metadata.
    """
    category_map = {
        'development': 'Development',
        'quality': 'Quality & Testing',
        'security': 'Security',
        'infrastructure': 'Infrastructure',
        'documentation': 'Documentation',
        'meta': 'Meta & Planning',
        'analysis': 'Analysis',
        'utility': 'Utility'
    }
    return category_map.get(agent_type, 'Other')
