#!/usr/bin/env python3
"""
Example script demonstrating shared utilities usage.

This shows how to use all shared utilities in a real oak-* script.
"""

import sys
from pathlib import Path

# Import all shared utilities
from scripts.shared import (
    Colors,
    create_base_parser,
    get_project_root,
    load_invocations,
    get_recent_invocations,
    parse_frontmatter,
    get_agent_category,
    get_category_color
)


def main():
    # 1. CREATE CLI PARSER with common args
    parser = create_base_parser(
        description='Example oak-* script using shared utilities',
        add_common_args=True
    )
    parser.add_argument('--limit', type=int, default=10,
                       help='Number of items to display')
    parser.add_argument('--days', type=int, default=7,
                       help='Number of days of history')
    args = parser.parse_args()
    
    # 2. HANDLE COLORS (--no-color flag)
    if args.no_color:
        Colors.disable()
    
    # 3. GET PROJECT ROOT
    project_root = get_project_root()
    if args.verbose:
        print(f"{Colors.DIM}Project root: {project_root}{Colors.RESET}")
    
    # 4. LOAD TELEMETRY DATA
    print(f"\n{Colors.BOLD}{Colors.BLUE}Loading Telemetry Data{Colors.RESET}")
    print("=" * 60)
    
    telemetry_file = project_root / 'telemetry' / 'agent_invocations.jsonl'
    
    # Load recent invocations (last N days)
    recent_invocations = get_recent_invocations(
        project_root / 'telemetry',
        days=args.days
    )
    
    print(f"Loaded {Colors.GREEN}{len(recent_invocations)}{Colors.RESET} "
          f"invocations from last {args.days} days")
    
    # 5. PARSE AGENT METADATA
    print(f"\n{Colors.BOLD}{Colors.BLUE}Agent Categories{Colors.RESET}")
    print("=" * 60)
    
    agents_dir = project_root / 'agents'
    agent_categories = {}
    
    for agent_file in sorted(agents_dir.glob('*.md')):
        if agent_file.name == 'README.md':
            continue
        
        # Parse frontmatter
        metadata, content = parse_frontmatter(agent_file)
        agent_name = metadata.get('agent_name', agent_file.stem)
        
        # Get category and color
        category = get_agent_category(agent_name)
        color_name = get_category_color(category)
        color = getattr(Colors, color_name, Colors.WHITE)
        
        # Group by category
        if category not in agent_categories:
            agent_categories[category] = []
        agent_categories[category].append((agent_name, color))
    
    # 6. DISPLAY RESULTS with colors
    for category in sorted(agent_categories.keys()):
        category_color = getattr(Colors, get_category_color(category), Colors.WHITE)
        print(f"\n{Colors.BOLD}{category_color}{category.upper()}{Colors.RESET}")
        
        for agent_name, color in sorted(agent_categories[category])[:args.limit]:
            print(f"  {color}• {agent_name}{Colors.RESET}")
    
    # 7. SHOW RECENT ACTIVITY
    print(f"\n{Colors.BOLD}{Colors.BLUE}Recent Activity{Colors.RESET}")
    print("=" * 60)
    
    for inv in recent_invocations[:args.limit]:
        agent = inv.get('agent_name', 'unknown')
        status = inv.get('outcome', {}).get('status', 'unknown')
        duration = inv.get('duration_seconds', 0)
        
        # Color code status
        status_color = Colors.GREEN if status == 'success' else Colors.RED
        
        print(f"{Colors.CYAN}{agent:25}{Colors.RESET} "
              f"{status_color}{status:10}{Colors.RESET} "
              f"{duration:>6.1f}s")
    
    print(f"\n{Colors.GREEN}✓ Example completed successfully{Colors.RESET}\n")
    return 0


if __name__ == '__main__':
    sys.exit(main())
