"""CLI utilities for oak-* scripts."""

import argparse
from pathlib import Path


def create_base_parser(description: str, add_common_args: bool = True) -> argparse.ArgumentParser:
    """
    Create base argument parser with common flags.
    
    Args:
        description: Script description
        add_common_args: Add common flags (--no-color, --verbose, etc.)
        
    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    if add_common_args:
        parser.add_argument('--no-color', action='store_true',
                          help='Disable colored output')
        parser.add_argument('--verbose', '-v', action='store_true',
                          help='Enable verbose output')
        parser.add_argument('--version', action='version',
                          version='%(prog)s 1.0.0')
    
    return parser


def get_project_root() -> Path:
    """Get project root directory (where scripts/ is located)."""
    # Assumes this file is in scripts/shared/
    return Path(__file__).parent.parent.parent
