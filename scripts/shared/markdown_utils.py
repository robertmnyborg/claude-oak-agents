"""Markdown and YAML frontmatter utilities."""

import re
from typing import Dict, Tuple, Optional, Any
from pathlib import Path


def parse_frontmatter(file_path: Path) -> Tuple[Dict[str, Any], str]:
    """
    Parse YAML frontmatter from markdown file.
    
    Returns:
        Tuple of (metadata_dict, content_without_frontmatter)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Match YAML frontmatter between --- markers
        if not content.startswith('---\n'):
            return {}, content
        
        parts = content.split('---\n', 2)
        if len(parts) < 3:
            return {}, content
        
        frontmatter_text = parts[1]
        body = parts[2]
        
        # Parse YAML frontmatter
        metadata = {}
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                
                # Handle list values
                if value.startswith('[') and value.endswith(']'):
                    value = [v.strip().strip('"\'') for v in value[1:-1].split(',')]
                
                metadata[key] = value
        
        return metadata, body
        
    except Exception:
        return {}, ""


def parse_frontmatter_string(content: str) -> Tuple[Dict[str, Any], str]:
    """
    Parse YAML frontmatter from markdown string.
    
    Returns:
        Tuple of (metadata_dict, content_without_frontmatter)
    """
    frontmatter = {}
    body = content
    
    if content.startswith('---\n'):
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            frontmatter_text = parts[1]
            body = parts[2]
            
            # Simple YAML parsing (key: value format)
            for line in frontmatter_text.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    
                    # Handle list values
                    if value.startswith('[') and value.endswith(']'):
                        value = [v.strip().strip('"\'') for v in value[1:-1].split(',')]
                    
                    frontmatter[key] = value
    
    return frontmatter, body


def get_metadata(file_path: Path, key: str, default: Optional[str] = None) -> Optional[str]:
    """Get specific metadata value from frontmatter."""
    metadata, _ = parse_frontmatter(file_path)
    return metadata.get(key, default)
