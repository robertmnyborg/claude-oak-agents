#!/usr/bin/env python3
"""
OaK Agent Loader - Multi-File and Single-File Format Support

Loads agents from both legacy single-file format and new multi-file package format.
Supports bundled scripts, metadata extraction, and dynamic discovery.
"""

import os
import json
import yaml
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import subprocess
import sys


@dataclass
class AgentScript:
    """Bundled executable script specification"""
    name: str
    runtime: str  # python, bash, node, go
    entrypoint: Path
    description: str
    required_packages: List[str] = field(default_factory=list)
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    outputs: List[Dict[str, str]] = field(default_factory=list)
    python_version: Optional[str] = None

    def validate(self) -> bool:
        """Validate script exists and is executable"""
        if not self.entrypoint.exists():
            return False
        if not os.access(self.entrypoint, os.X_OK):
            # Try to make executable
            os.chmod(self.entrypoint, 0o755)
        return True

    def execute(self, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the bundled script"""
        if not self.validate():
            raise RuntimeError(f"Script not found or not executable: {self.entrypoint}")

        # Build command based on runtime
        if self.runtime == "python":
            cmd = [sys.executable, str(self.entrypoint)]
        elif self.runtime == "bash":
            cmd = ["bash", str(self.entrypoint)]
        elif self.runtime == "node":
            cmd = ["node", str(self.entrypoint)]
        elif self.runtime == "go":
            cmd = ["go", "run", str(self.entrypoint)]
        else:
            raise ValueError(f"Unsupported runtime: {self.runtime}")

        # Add parameters
        if parameters:
            for param_spec in self.parameters:
                param_name = param_spec['name']
                if param_name in parameters:
                    cmd.append(f"--{param_name}={parameters[param_name]}")

        # Execute
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Script execution timed out (300s limit)"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


@dataclass
class AgentMetadata:
    """Agent metadata for dynamic discovery"""
    name: str
    version: str
    description: str
    triggers: Dict[str, List[str]]
    category: str
    priority: str
    blocking: bool
    parallel_compatible: List[str]
    capabilities: List[str]
    tools: List[str]
    model: str
    scripts: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    coordination_patterns: List[str] = field(default_factory=list)
    auto_created: bool = False
    created_by: str = "human"
    created_at: str = ""

    def matches_keywords(self, keywords: List[str]) -> bool:
        """Check if agent matches any of the keywords"""
        trigger_keywords = self.triggers.get('keywords', [])
        return any(kw.lower() in [t.lower() for t in trigger_keywords] for kw in keywords)

    def matches_file_pattern(self, file_path: str) -> bool:
        """Check if agent matches file pattern"""
        patterns = self.triggers.get('file_patterns', [])
        from fnmatch import fnmatch
        return any(fnmatch(file_path, pattern) for pattern in patterns)

    def matches_domain(self, domain: str) -> bool:
        """Check if agent matches domain"""
        domains = self.triggers.get('domains', [])
        return domain.lower() in [d.lower() for d in domains]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'triggers': self.triggers,
            'category': self.category,
            'priority': self.priority,
            'blocking': self.blocking,
            'parallel_compatible': self.parallel_compatible,
            'capabilities': self.capabilities,
            'scripts': self.scripts,
            'metrics': self.metrics
        }


@dataclass
class Agent:
    """Unified agent representation"""
    metadata: AgentMetadata
    definition: str  # Full markdown definition
    scripts: Dict[str, AgentScript] = field(default_factory=dict)
    reference_docs: Dict[str, str] = field(default_factory=dict)
    templates: Dict[str, str] = field(default_factory=dict)
    package_path: Optional[Path] = None
    is_multi_file: bool = False

    def get_script(self, script_name: str) -> Optional[AgentScript]:
        """Get bundled script by name"""
        return self.scripts.get(script_name)

    def execute_script(self, script_name: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a bundled script"""
        script = self.get_script(script_name)
        if not script:
            raise ValueError(f"Script not found: {script_name}")
        return script.execute(parameters)

    def get_reference(self, doc_name: str) -> Optional[str]:
        """Get reference documentation"""
        return self.reference_docs.get(doc_name)

    def get_template(self, template_name: str) -> Optional[str]:
        """Get code template"""
        return self.templates.get(template_name)


class AgentLoader:
    """Load agents from both single-file and multi-file formats"""

    def __init__(self, agents_dir: Path):
        self.agents_dir = Path(agents_dir)
        self.metadata_cache: Dict[str, AgentMetadata] = {}
        self.agent_cache: Dict[str, Agent] = {}

    def load_all_metadata(self) -> Dict[str, AgentMetadata]:
        """Load metadata for all agents (lightweight, for system prompt)"""
        if self.metadata_cache:
            return self.metadata_cache

        metadata = {}

        for agent_path in self.agents_dir.iterdir():
            if agent_path.name.startswith('.') or agent_path.name.startswith('_'):
                continue
            if agent_path.name in ['pending_review', 'rejected', 'README.md']:
                continue

            try:
                agent_metadata = self._load_metadata(agent_path)
                if agent_metadata:
                    metadata[agent_metadata.name] = agent_metadata
            except Exception as e:
                print(f"Warning: Failed to load metadata for {agent_path.name}: {e}", file=sys.stderr)

        self.metadata_cache = metadata
        return metadata

    def _load_metadata(self, agent_path: Path) -> Optional[AgentMetadata]:
        """Load metadata from single-file or multi-file agent"""

        # Multi-file format: directory with metadata.yaml
        if agent_path.is_dir():
            metadata_file = agent_path / "metadata.yaml"
            if metadata_file.exists():
                with open(metadata_file) as f:
                    data = yaml.safe_load(f)
                    return self._parse_metadata(data)

        # Single-file format: extract from frontmatter
        elif agent_path.is_file() and agent_path.suffix == '.md':
            with open(agent_path) as f:
                content = f.read()
                frontmatter = self._extract_frontmatter(content)
                if frontmatter:
                    # Create metadata from frontmatter
                    return self._frontmatter_to_metadata(frontmatter, agent_path.stem)

        return None

    def _extract_frontmatter(self, content: str) -> Optional[Dict[str, Any]]:
        """Extract YAML frontmatter from markdown"""
        if not content.startswith('---'):
            return None

        parts = content.split('---', 2)
        if len(parts) < 3:
            return None

        try:
            return yaml.safe_load(parts[1])
        except yaml.YAMLError:
            return None

    def _frontmatter_to_metadata(self, frontmatter: Dict[str, Any], name: str) -> AgentMetadata:
        """Convert frontmatter to AgentMetadata"""
        # Infer triggers from description
        description = frontmatter.get('description', '')
        keywords = self._extract_keywords_from_description(description)

        return AgentMetadata(
            name=frontmatter.get('name', name),
            version="1.0.0",  # Default for legacy agents
            description=description,
            triggers={
                'keywords': keywords,
                'file_patterns': [],
                'domains': [frontmatter.get('name', name).split('-')[0]]
            },
            category=self._infer_category(name),
            priority=frontmatter.get('priority', 'medium'),
            blocking=frontmatter.get('blocking', False),
            parallel_compatible=[],
            capabilities=[],
            tools=frontmatter.get('tools', []),
            model=frontmatter.get('model', 'sonnet'),
            auto_created=False,
            created_by='human',
            created_at=''
        )

    def _extract_keywords_from_description(self, description: str) -> List[str]:
        """Extract keywords from description"""
        # Simple keyword extraction (can be enhanced with NLP)
        words = description.lower().split()
        # Remove common words
        stopwords = {'a', 'an', 'the', 'and', 'or', 'but', 'for', 'with', 'on', 'in', 'to', 'from'}
        keywords = [w.strip('.,;:') for w in words if w not in stopwords and len(w) > 3]
        return keywords[:10]  # Top 10 keywords

    def _infer_category(self, name: str) -> str:
        """Infer category from agent name"""
        if any(x in name for x in ['security', 'audit', 'scanner']):
            return 'quality-security'
        elif any(x in name for x in ['test', 'qa']):
            return 'quality-testing'
        elif any(x in name for x in ['frontend', 'backend', 'mobile', 'blockchain', 'ml']):
            return 'core-development'
        elif any(x in name for x in ['infrastructure', 'deploy', 'devops']):
            return 'infrastructure-operations'
        elif any(x in name for x in ['document', 'content', 'technical']):
            return 'documentation-content'
        else:
            return 'special-purpose'

    def _parse_metadata(self, data: Dict[str, Any]) -> AgentMetadata:
        """Parse metadata from YAML data"""
        return AgentMetadata(
            name=data['name'],
            version=data.get('version', '1.0.0'),
            description=data['description'],
            triggers=data.get('triggers', {'keywords': [], 'file_patterns': [], 'domains': []}),
            category=data.get('category', 'special-purpose'),
            priority=data.get('priority', 'medium'),
            blocking=data.get('blocking', False),
            parallel_compatible=data.get('parallel_compatible', []),
            capabilities=data.get('capabilities', []),
            tools=data.get('tools', []),
            model=data.get('model', 'sonnet'),
            scripts=[s['name'] for s in data.get('scripts', [])],
            metrics=data.get('metrics', {}),
            coordination_patterns=data.get('coordination_patterns', []),
            auto_created=data.get('auto_created', False),
            created_by=data.get('created_by', 'human'),
            created_at=data.get('created_at', '')
        )

    def load_agent(self, agent_name: str) -> Agent:
        """Load full agent definition (on-demand)"""

        # Check cache
        if agent_name in self.agent_cache:
            return self.agent_cache[agent_name]

        agent_path = self.agents_dir / agent_name

        # Try multi-file format first
        if agent_path.is_dir():
            agent = self._load_multi_file_agent(agent_path)
        # Try single-file format with .md extension
        elif (self.agents_dir / f"{agent_name}.md").exists():
            agent = self._load_single_file_agent(self.agents_dir / f"{agent_name}.md")
        else:
            raise ValueError(f"Agent not found: {agent_name}")

        self.agent_cache[agent_name] = agent
        return agent

    def _load_single_file_agent(self, agent_file: Path) -> Agent:
        """Load agent from single-file format (legacy)"""
        with open(agent_file) as f:
            content = f.read()

        frontmatter = self._extract_frontmatter(content)
        if frontmatter:
            # Remove frontmatter from definition
            parts = content.split('---', 2)
            definition = parts[2].strip() if len(parts) >= 3 else content
        else:
            frontmatter = {}
            definition = content

        metadata = self._frontmatter_to_metadata(frontmatter, agent_file.stem)

        return Agent(
            metadata=metadata,
            definition=definition,
            scripts={},
            reference_docs={},
            templates={},
            package_path=agent_file,
            is_multi_file=False
        )

    def _load_multi_file_agent(self, agent_dir: Path) -> Agent:
        """Load agent from multi-file package format"""

        # Load metadata
        metadata_file = agent_dir / "metadata.yaml"
        if not metadata_file.exists():
            raise ValueError(f"metadata.yaml not found in {agent_dir}")

        with open(metadata_file) as f:
            metadata_data = yaml.safe_load(f)
        metadata = self._parse_metadata(metadata_data)

        # Load agent definition
        agent_file = agent_dir / "agent.md"
        if not agent_file.exists():
            raise ValueError(f"agent.md not found in {agent_dir}")

        with open(agent_file) as f:
            definition = f.read()

        # Load bundled scripts
        scripts = {}
        if 'scripts' in metadata_data:
            for script_spec in metadata_data['scripts']:
                script = AgentScript(
                    name=script_spec['name'],
                    runtime=script_spec['runtime'],
                    entrypoint=agent_dir / script_spec['entrypoint'],
                    description=script_spec.get('description', ''),
                    required_packages=script_spec.get('required_packages', []),
                    parameters=script_spec.get('parameters', []),
                    outputs=script_spec.get('outputs', []),
                    python_version=script_spec.get('python_version')
                )
                scripts[script.name] = script

        # Load reference docs
        reference_docs = {}
        reference_dir = agent_dir / "reference"
        if reference_dir.exists():
            for ref_file in reference_dir.glob('*.md'):
                with open(ref_file) as f:
                    reference_docs[ref_file.stem] = f.read()

        # Load templates
        templates = {}
        templates_dir = agent_dir / "templates"
        if templates_dir.exists():
            for template_file in templates_dir.iterdir():
                with open(template_file) as f:
                    templates[template_file.name] = f.read()

        return Agent(
            metadata=metadata,
            definition=definition,
            scripts=scripts,
            reference_docs=reference_docs,
            templates=templates,
            package_path=agent_dir,
            is_multi_file=True
        )

    def generate_metadata_summary(self) -> str:
        """Generate lightweight metadata summary for system prompt"""
        metadata = self.load_all_metadata()

        summary = "# Available Agents (Metadata)\n\n"

        # Group by category
        by_category = {}
        for agent_meta in metadata.values():
            category = agent_meta.category
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(agent_meta)

        for category, agents in sorted(by_category.items()):
            summary += f"## {category.replace('-', ' ').title()}\n\n"
            for agent in agents:
                summary += f"- **{agent.name}**: {agent.description[:100]}...\n"
                summary += f"  - Triggers: {', '.join(agent.triggers.get('keywords', [])[:5])}\n"
                summary += f"  - Priority: {agent.priority} | Blocking: {agent.blocking}\n"
                if agent.scripts:
                    summary += f"  - Bundled scripts: {', '.join(agent.scripts)}\n"
                summary += "\n"

        summary += f"\n**Total agents**: {len(metadata)}\n"
        summary += "\n*Full agent definitions loaded on-demand when invoked.*\n"

        return summary

    def save_metadata_cache(self, output_file: Path):
        """Save metadata cache to JSON for fast loading"""
        metadata = self.load_all_metadata()
        cache_data = {
            name: meta.to_dict()
            for name, meta in metadata.items()
        }

        with open(output_file, 'w') as f:
            json.dump(cache_data, f, indent=2)

        print(f"Metadata cache saved: {output_file}")
        print(f"Size: {output_file.stat().st_size / 1024:.1f} KB")


def main():
    """CLI for agent loader"""
    import argparse

    parser = argparse.ArgumentParser(description="OaK Agent Loader")
    parser.add_argument('--agents-dir', default='agents', help='Path to agents directory')
    parser.add_argument('--command', choices=['metadata', 'load', 'summary', 'cache'], required=True)
    parser.add_argument('--agent', help='Agent name (for load command)')
    parser.add_argument('--output', help='Output file (for cache command)')

    args = parser.parse_args()

    loader = AgentLoader(Path(args.agents_dir))

    if args.command == 'metadata':
        metadata = loader.load_all_metadata()
        print(json.dumps({k: v.to_dict() for k, v in metadata.items()}, indent=2))

    elif args.command == 'load':
        if not args.agent:
            print("Error: --agent required for load command")
            sys.exit(1)
        agent = loader.load_agent(args.agent)
        print(f"Loaded: {agent.metadata.name}")
        print(f"Format: {'Multi-file' if agent.is_multi_file else 'Single-file'}")
        print(f"Scripts: {len(agent.scripts)}")
        print(f"Reference docs: {len(agent.reference_docs)}")

    elif args.command == 'summary':
        print(loader.generate_metadata_summary())

    elif args.command == 'cache':
        output = Path(args.output) if args.output else Path('telemetry/agent_metadata_cache.json')
        loader.save_metadata_cache(output)


if __name__ == '__main__':
    main()
