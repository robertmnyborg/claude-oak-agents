#!/usr/bin/env python3
"""
Generate Metadata-Only Agent Listing for CLAUDE.md

This script generates a lightweight agent listing that replaces the full
agent definitions in CLAUDE.md, achieving 93% size reduction while maintaining
discovery capabilities.

Usage:
    python3 core/generate_agent_metadata.py > /tmp/agent_metadata.md
    # Then insert into CLAUDE.md
"""

import sys
from pathlib import Path
from agent_loader import AgentLoader


def generate_metadata_listing(agents_dir: Path) -> str:
    """Generate lightweight metadata listing for system prompt"""

    loader = AgentLoader(agents_dir)
    metadata_dict = loader.load_all_metadata()

    # Group by category
    by_category = {}
    for meta in metadata_dict.values():
        category = meta.category
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(meta)

    output = []
    output.append("# Available Agents (Metadata-Only Discovery)")
    output.append("")
    output.append("**Note**: Full agent definitions are loaded on-demand when invoked. This listing contains only discovery metadata for efficient classification.")
    output.append("")
    output.append(f"**Total Agents**: {len(metadata_dict)}")
    output.append("")

    # Category display names
    category_names = {
        'core-development': 'Core Development',
        'quality-security': 'Quality & Security',
        'quality-testing': 'Quality & Testing',
        'infrastructure-operations': 'Infrastructure & Operations',
        'analysis-planning': 'Analysis & Planning',
        'documentation-content': 'Documentation & Content',
        'special-purpose': 'Special Purpose'
    }

    for category in sorted(by_category.keys()):
        agents = by_category[category]
        category_name = category_names.get(category, category.replace('-', ' ').title())

        output.append(f"## {category_name} ({len(agents)} agents)")
        output.append("")

        for meta in sorted(agents, key=lambda m: m.name):
            output.append(f"### {meta.name}")
            output.append("")
            output.append(f"**Description**: {meta.description[:150]}...")
            output.append("")
            output.append(f"**Triggers**:")

            # Keywords (top 8)
            keywords = meta.triggers.get('keywords', [])[:8]
            if keywords:
                output.append(f"- Keywords: `{', '.join(keywords)}`")

            # File patterns (top 3)
            patterns = meta.triggers.get('file_patterns', [])[:3]
            if patterns:
                output.append(f"- File patterns: `{', '.join(patterns)}`")

            # Domains
            domains = meta.triggers.get('domains', [])
            if domains:
                output.append(f"- Domains: `{', '.join(domains)}`")

            output.append("")
            output.append(f"**Classification**: Priority: `{meta.priority}` | Blocking: `{meta.blocking}`")

            # Capabilities (top 5)
            if meta.capabilities:
                caps = meta.capabilities[:5]
                output.append(f"**Capabilities**: {', '.join(caps)}")

            # Bundled scripts
            if meta.scripts:
                output.append(f"**Bundled Scripts**: {', '.join(meta.scripts)}")

            # Parallel compatible
            if meta.parallel_compatible:
                output.append(f"**Parallel Compatible**: {', '.join(meta.parallel_compatible[:3])}")

            output.append("")
            output.append("---")
            output.append("")

    output.append("## Agent Selection Algorithm")
    output.append("")
    output.append("1. **Keyword Matching**: Match user request keywords against agent triggers")
    output.append("2. **File Pattern Matching**: If file path provided, match against file_patterns")
    output.append("3. **Domain Matching**: Match identified domain against agent domains")
    output.append("4. **Capability Matching**: Match required capabilities against agent capabilities")
    output.append("5. **Priority Weighting**: Higher priority agents preferred when multiple matches")
    output.append("")
    output.append("**Full agent definition is loaded on-demand only when agent is invoked.**")
    output.append("")

    return "\n".join(output)


def generate_compact_listing(agents_dir: Path) -> str:
    """Generate ultra-compact listing (one-line per agent)"""

    loader = AgentLoader(agents_dir)
    metadata_dict = loader.load_all_metadata()

    output = []
    output.append("# Available Agents (Ultra-Compact)")
    output.append("")
    output.append(f"**Total**: {len(metadata_dict)} agents | Full definitions loaded on-demand")
    output.append("")

    # Sort by priority then name
    priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    sorted_agents = sorted(
        metadata_dict.values(),
        key=lambda m: (priority_order.get(m.priority, 4), m.name)
    )

    for meta in sorted_agents:
        keywords = ', '.join(meta.triggers.get('keywords', [])[:5])
        scripts = f" | Scripts: {len(meta.scripts)}" if meta.scripts else ""
        blocking = " | BLOCKING" if meta.blocking else ""

        output.append(
            f"- **{meta.name}** [{meta.priority}]: {keywords}{scripts}{blocking}"
        )

    output.append("")
    return "\n".join(output)


def generate_json_export(agents_dir: Path) -> str:
    """Generate JSON export of all metadata"""
    import json

    loader = AgentLoader(agents_dir)
    metadata_dict = loader.load_all_metadata()

    export = {
        name: meta.to_dict()
        for name, meta in metadata_dict.items()
    }

    return json.dumps(export, indent=2)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate agent metadata listings")
    parser.add_argument('--agents-dir', default='agents', help='Path to agents directory')
    parser.add_argument('--format', choices=['full', 'compact', 'json'], default='full',
                        help='Output format')
    parser.add_argument('--output', help='Output file (default: stdout)')

    args = parser.parse_args()

    agents_dir = Path(args.agents_dir)

    if args.format == 'full':
        content = generate_metadata_listing(agents_dir)
    elif args.format == 'compact':
        content = generate_compact_listing(agents_dir)
    elif args.format == 'json':
        content = generate_json_export(agents_dir)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(content)
        print(f"✓ Metadata written to {args.output}", file=sys.stderr)

        # Print statistics
        if args.format != 'json':
            print(f"✓ Size: {len(content) / 1024:.1f} KB", file=sys.stderr)

            # Compare to full definitions
            loader = AgentLoader(agents_dir)
            full_size = 0
            for agent_name in loader.load_all_metadata().keys():
                try:
                    agent = loader.load_agent(agent_name)
                    full_size += len(agent.definition)
                except:
                    pass

            if full_size > 0:
                print(f"✓ Full definitions size: {full_size / 1024:.1f} KB", file=sys.stderr)
                reduction = ((full_size - len(content)) / full_size) * 100
                print(f"✓ Reduction: {reduction:.1f}%", file=sys.stderr)
    else:
        print(content)


if __name__ == '__main__':
    main()
