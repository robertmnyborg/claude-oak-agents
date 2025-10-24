#!/usr/bin/env python3
"""
Spec Translation CLI Tool

Command-line interface for translating Markdown specs to YAML format.
Orchestrates markdown_parser and yaml_generator with validation and metadata tracking.

Component: TranslationCLI (Section 2.2.Component-3)
Acceptance Criteria: AC-5, AC-6

Usage:
    # Translate Markdown to YAML
    python translate_spec.py --input spec.md --output spec.yaml

    # Translate with validation
    python translate_spec.py --input spec.md --output spec.yaml --validate

    # Validate existing YAML
    python translate_spec.py --validate-yaml spec.yaml

    # Watch for changes (auto-regenerate) - OPTIONAL
    python translate_spec.py --watch spec.md
"""

import argparse
import sys
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

# Import parser and generator
from markdown_parser import parse_spec, ParseError
from yaml_generator import generate_yaml, validate_schema, YAMLGenerator


class TranslationError(Exception):
    """Raised when translation fails."""
    pass


def translate_spec(input_file: str, output_file: str, validate: bool = False) -> bool:
    """
    Translate Markdown spec to YAML format.
    
    Args:
        input_file: Path to Markdown spec file
        output_file: Path to output YAML file
        validate: Whether to validate YAML after generation
        
    Returns:
        True if successful, False otherwise
        
    Raises:
        TranslationError: If translation fails
    """
    try:
        # Step 1: Parse Markdown
        print(f"📄 Parsing Markdown spec: {input_file}")
        parsed_data = parse_spec(input_file)
        print(f"✅ Successfully parsed {len(parsed_data)} sections")
        
        # Step 2: Generate YAML
        print(f"🔧 Generating YAML structure...")
        yaml_string = generate_yaml(parsed_data, input_file)
        
        # Step 3: Optional validation
        if validate:
            print(f"🔍 Validating YAML schema...")
            yaml_data = yaml.safe_load(yaml_string)
            validate_schema(yaml_data)
            print(f"✅ YAML validation passed")
        
        # Step 4: Write YAML to output file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(yaml_string, encoding='utf-8')
        
        print(f"✅ Successfully translated to: {output_file}")
        print(f"📊 Metadata tracked:")
        print(f"   - Source: {input_file}")
        print(f"   - Generated: {output_file}")
        print(f"   - Timestamp: {yaml.safe_load(yaml_string)['metadata']['last_sync']}")
        
        return True
        
    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}", file=sys.stderr)
        return False
    except ParseError as e:
        print(f"❌ Error: Failed to parse Markdown - {e}", file=sys.stderr)
        return False
    except ValueError as e:
        print(f"❌ Error: Validation failed - {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Error: Translation failed - {e}", file=sys.stderr)
        return False


def validate_yaml_file(yaml_file: str) -> bool:
    """
    Validate existing YAML spec file.
    
    Args:
        yaml_file: Path to YAML spec file
        
    Returns:
        True if valid, False otherwise
    """
    try:
        # Load YAML file
        print(f"📄 Loading YAML file: {yaml_file}")
        yaml_path = Path(yaml_file)
        
        if not yaml_path.exists():
            print(f"❌ Error: File not found - {yaml_file}", file=sys.stderr)
            return False
        
        yaml_content = yaml_path.read_text(encoding='utf-8')
        yaml_data = yaml.safe_load(yaml_content)
        
        # Validate schema
        print(f"🔍 Validating YAML schema...")
        validate_schema(yaml_data)
        
        print(f"✅ YAML validation passed")
        print(f"📊 Spec metadata:")
        print(f"   - Spec ID: {yaml_data.get('spec_id', 'N/A')}")
        print(f"   - Status: {yaml_data.get('status', 'N/A')}")
        if 'metadata' in yaml_data:
            print(f"   - Last sync: {yaml_data['metadata'].get('last_sync', 'N/A')}")
            print(f"   - Source: {yaml_data['metadata'].get('markdown_location', 'N/A')}")
        
        return True
        
    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}", file=sys.stderr)
        return False
    except yaml.YAMLError as e:
        print(f"❌ Error: Invalid YAML format - {e}", file=sys.stderr)
        return False
    except ValueError as e:
        print(f"❌ Error: Validation failed - {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Error: Validation failed - {e}", file=sys.stderr)
        return False


def watch_markdown_file(markdown_file: str) -> None:
    """
    Watch Markdown file for changes and auto-regenerate YAML.
    
    Args:
        markdown_file: Path to Markdown spec file to watch
        
    Note:
        This is an OPTIONAL feature requiring the watchdog library.
        Not implemented in this version.
    """
    print(f"⚠️  Watch mode not implemented yet", file=sys.stderr)
    print(f"   Requires 'watchdog' library for file watching", file=sys.stderr)
    print(f"   For now, manually re-run translation after changes", file=sys.stderr)
    sys.exit(1)


def main() -> int:
    """
    Main CLI entry point.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description="Translate Markdown specs to YAML format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Translate Markdown to YAML
  %(prog)s --input specs/active/spec.md --output specs/active/spec.yaml

  # Translate with validation
  %(prog)s --input spec.md --output spec.yaml --validate

  # Validate existing YAML
  %(prog)s --validate-yaml specs/active/spec.yaml

  # Watch for changes (auto-regenerate) - NOT IMPLEMENTED YET
  %(prog)s --watch specs/active/spec.md
        """
    )
    
    # Mutually exclusive operation modes
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '--input',
        type=str,
        help='Input Markdown spec file (requires --output)'
    )
    mode_group.add_argument(
        '--validate-yaml',
        type=str,
        help='Validate existing YAML spec file'
    )
    mode_group.add_argument(
        '--watch',
        type=str,
        help='Watch Markdown file for changes (NOT IMPLEMENTED)'
    )
    
    # Additional options
    parser.add_argument(
        '--output',
        type=str,
        help='Output YAML file (required with --input)'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate YAML after translation'
    )
    
    args = parser.parse_args()
    
    # Validate argument combinations
    if args.input and not args.output:
        print("❌ Error: --output is required when using --input", file=sys.stderr)
        parser.print_help()
        return 1
    
    # Execute based on mode
    try:
        if args.input:
            # Translate mode
            success = translate_spec(args.input, args.output, args.validate)
            return 0 if success else 1
            
        elif args.validate_yaml:
            # Validate mode
            success = validate_yaml_file(args.validate_yaml)
            return 0 if success else 1
            
        elif args.watch:
            # Watch mode (not implemented)
            watch_markdown_file(args.watch)
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
