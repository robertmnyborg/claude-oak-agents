#!/usr/bin/env python3
"""
Domain Router for claude-oak-agents

Analyzes requests and file contexts to determine the most appropriate domain(s)
for specialized agent routing. Reads domain configurations and returns matched
domain details for optimized agent selection.

Usage:
    from core.domain_router import DomainRouter

    router = DomainRouter()
    domains = router.identify_domains(
        request_text="Create a React component with TypeScript",
        file_paths=["src/components/Button.tsx"]
    )
"""

import os
import re
import yaml
from pathlib import Path
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class DomainConfig:
    """Represents a domain configuration loaded from .claude/domains/"""
    name: str
    priority: int
    primary_agent: str
    secondary_agents: List[str]
    related_agents: List[str]
    keywords: List[str] = field(default_factory=list)
    file_patterns: List[str] = field(default_factory=list)
    tech_stack: List[str] = field(default_factory=list)
    content: str = ""

    @property
    def all_agents(self) -> List[str]:
        """Return all agents (primary + secondary + related)"""
        agents = [self.primary_agent] + self.secondary_agents + self.related_agents
        return list(dict.fromkeys(agents))  # Remove duplicates, preserve order


class DomainRouter:
    """
    Domain-aware routing system for claude-oak-agents.

    Matches user requests and file contexts to domain configurations,
    enabling specialized agent routing based on detected domains.
    """

    def __init__(self, domains_dir: Optional[str] = None):
        """
        Initialize the domain router.

        Args:
            domains_dir: Path to .claude/domains/ directory.
                        If None, uses default relative to this file.
        """
        if domains_dir is None:
            # Default to .claude/domains relative to project root
            project_root = Path(__file__).parent.parent
            domains_dir = project_root / ".claude" / "domains"

        self.domains_dir = Path(domains_dir)
        self.domains: Dict[str, DomainConfig] = {}
        self.load_domains()

    def load_domains(self) -> None:
        """Load all domain configurations from .claude/domains/*.md"""
        if not self.domains_dir.exists():
            print(f"Warning: Domains directory not found: {self.domains_dir}")
            return

        for domain_file in self.domains_dir.glob("*.md"):
            if domain_file.name == "README.md":
                continue

            try:
                domain_config = self._parse_domain_file(domain_file)
                self.domains[domain_config.name] = domain_config
            except Exception as e:
                print(f"Error loading domain {domain_file.name}: {e}")

    def _parse_domain_file(self, file_path: Path) -> DomainConfig:
        """Parse a domain markdown file with YAML frontmatter"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract YAML frontmatter
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
        if not frontmatter_match:
            raise ValueError(f"No YAML frontmatter found in {file_path.name}")

        frontmatter_str, markdown_content = frontmatter_match.groups()
        metadata = yaml.safe_load(frontmatter_str)

        # Extract keywords, file patterns, and tech stack from markdown
        keywords = self._extract_keywords(markdown_content)
        file_patterns = self._extract_file_patterns(markdown_content)
        tech_stack = self._extract_tech_stack(markdown_content)

        return DomainConfig(
            name=metadata['domain'],
            priority=metadata.get('priority', 1),
            primary_agent=metadata['primary_agent'],
            secondary_agents=metadata.get('secondary_agents', []),
            related_agents=metadata.get('related_agents', []),
            keywords=keywords,
            file_patterns=file_patterns,
            tech_stack=tech_stack,
            content=markdown_content
        )

    def _extract_keywords(self, content: str) -> List[str]:
        """Extract keywords from the Triggers > Keywords section"""
        keywords = []

        # Find the Keywords section under Triggers
        keywords_section = re.search(
            r'### Keywords\s*\n(.*?)(?=\n### |\n## |$)',
            content,
            re.DOTALL
        )

        if keywords_section:
            keyword_text = keywords_section.group(1)
            # Extract keywords from bullet points or inline lists
            # Match patterns like: "- **Category**: keyword1, keyword2"
            for line in keyword_text.split('\n'):
                # Remove markdown formatting
                clean_line = re.sub(r'\*\*.*?\*\*:', '', line)
                clean_line = re.sub(r'^[\s\-\*]+', '', clean_line)

                # Split by commas and extract words
                for item in clean_line.split(','):
                    keyword = item.strip().lower()
                    if keyword and len(keyword) > 2:
                        keywords.append(keyword)

        return keywords

    def _extract_file_patterns(self, content: str) -> List[str]:
        """Extract file patterns from the Triggers > File Patterns section"""
        patterns = []

        file_patterns_section = re.search(
            r'### File Patterns\s*\n(.*?)(?=\n### |\n## |$)',
            content,
            re.DOTALL
        )

        if file_patterns_section:
            pattern_text = file_patterns_section.group(1)
            for line in pattern_text.split('\n'):
                # Extract patterns in backticks or plain text
                # Match: `*.tsx`, `src/components/**/*`, etc.
                pattern_matches = re.findall(r'`([^`]+)`', line)
                patterns.extend(pattern_matches)

                # Also match plain patterns at start of line
                if line.strip().startswith('-'):
                    plain_pattern = re.sub(r'^[\s\-\*]+', '', line).strip()
                    if '/' in plain_pattern or '*' in plain_pattern:
                        patterns.append(plain_pattern)

        return patterns

    def _extract_tech_stack(self, content: str) -> List[str]:
        """Extract technology names from Tech Stack section"""
        tech_items = []

        tech_stack_section = re.search(
            r'## Tech Stack\s*\n(.*?)(?=\n## |$)',
            content,
            re.DOTALL
        )

        if tech_stack_section:
            tech_text = tech_stack_section.group(1)
            # Extract from bold markdown: **React**, **TypeScript**, etc.
            tech_matches = re.findall(r'\*\*([^*]+)\*\*', tech_text)
            tech_items.extend([t.strip().lower() for t in tech_matches])

        return tech_items

    def identify_domains(
        self,
        request_text: str = "",
        file_paths: Optional[List[str]] = None,
        confidence_threshold: float = 0.3
    ) -> List[Dict]:
        """
        Identify relevant domains based on request text and file paths.

        Args:
            request_text: The user's request or prompt text
            file_paths: List of file paths being worked on
            confidence_threshold: Minimum confidence score (0.0-1.0) to include domain

        Returns:
            List of matched domains with confidence scores, sorted by score descending
        """
        if file_paths is None:
            file_paths = []

        domain_scores = defaultdict(float)
        domain_reasons = defaultdict(list)

        request_lower = request_text.lower()

        # Score each domain
        for domain_name, domain_config in self.domains.items():
            score = 0.0
            reasons = []

            # 1. Keyword matching (weight: 0.4)
            keyword_matches = sum(
                1 for keyword in domain_config.keywords
                if keyword in request_lower
            )
            if keyword_matches > 0:
                keyword_score = min(keyword_matches / 5.0, 1.0) * 0.4
                score += keyword_score
                reasons.append(f"{keyword_matches} keyword(s) matched")

            # 2. File pattern matching (weight: 0.4)
            file_pattern_matches = sum(
                1 for file_path in file_paths
                for pattern in domain_config.file_patterns
                if self._matches_pattern(file_path, pattern)
            )
            if file_pattern_matches > 0:
                file_score = min(file_pattern_matches / 3.0, 1.0) * 0.4
                score += file_score
                reasons.append(f"{file_pattern_matches} file pattern(s) matched")

            # 3. Tech stack mentions (weight: 0.2)
            tech_matches = sum(
                1 for tech in domain_config.tech_stack
                if tech in request_lower
            )
            if tech_matches > 0:
                tech_score = min(tech_matches / 3.0, 1.0) * 0.2
                score += tech_score
                reasons.append(f"{tech_matches} tech stack item(s) mentioned")

            if score > 0:
                domain_scores[domain_name] = score
                domain_reasons[domain_name] = reasons

        # Filter by confidence threshold and sort by score
        matched_domains = [
            {
                "domain": domain_name,
                "confidence": score,
                "reasons": domain_reasons[domain_name],
                "config": self.domains[domain_name]
            }
            for domain_name, score in domain_scores.items()
            if score >= confidence_threshold
        ]

        matched_domains.sort(key=lambda x: x["confidence"], reverse=True)

        return matched_domains

    def _matches_pattern(self, file_path: str, pattern: str) -> bool:
        """Check if a file path matches a glob-like pattern"""
        # Convert glob pattern to regex
        # *.tsx -> .*\.tsx$
        # **/*.ts -> .*/.*\.ts$
        # src/components/* -> src/components/[^/]+$

        regex_pattern = pattern
        regex_pattern = regex_pattern.replace('.', r'\.')
        regex_pattern = regex_pattern.replace('**/', '.*/')
        regex_pattern = regex_pattern.replace('*', '[^/]+')

        if not regex_pattern.endswith('$'):
            regex_pattern += '$'
        if not regex_pattern.startswith('^'):
            regex_pattern = '.*' + regex_pattern

        return bool(re.match(regex_pattern, file_path))

    def get_domain(self, domain_name: str) -> Optional[DomainConfig]:
        """Get a specific domain configuration by name"""
        return self.domains.get(domain_name)

    def list_domains(self) -> List[str]:
        """List all available domain names"""
        return sorted(self.domains.keys())

    def get_recommended_agents(
        self,
        request_text: str = "",
        file_paths: Optional[List[str]] = None,
        max_agents: int = 5
    ) -> List[str]:
        """
        Get recommended agents based on domain detection.

        Args:
            request_text: The user's request
            file_paths: List of file paths
            max_agents: Maximum number of agents to recommend

        Returns:
            List of agent names, prioritized by domain confidence
        """
        domains = self.identify_domains(request_text, file_paths)

        if not domains:
            return []  # No domains matched, use general-purpose agents

        # Collect agents from matched domains, weighted by confidence
        agent_scores = defaultdict(float)

        for domain_match in domains:
            confidence = domain_match["confidence"]
            config = domain_match["config"]

            # Primary agent gets full confidence score
            agent_scores[config.primary_agent] += confidence

            # Secondary agents get half confidence
            for agent in config.secondary_agents:
                agent_scores[agent] += confidence * 0.5

            # Related agents get quarter confidence
            for agent in config.related_agents:
                agent_scores[agent] += confidence * 0.25

        # Sort by score and return top N
        recommended = sorted(
            agent_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [agent for agent, score in recommended[:max_agents]]

    def format_domain_summary(self, domains: List[Dict]) -> str:
        """Format domain matches into a readable summary"""
        if not domains:
            return "No specific domains detected. Using general-purpose agents."

        summary_lines = ["Detected Domains:"]
        for i, domain_match in enumerate(domains, 1):
            domain_name = domain_match["domain"]
            confidence = domain_match["confidence"]
            reasons = domain_match["reasons"]
            config = domain_match["config"]

            summary_lines.append(
                f"{i}. {domain_name.upper()} (confidence: {confidence:.2f})"
            )
            summary_lines.append(f"   Primary agent: {config.primary_agent}")
            summary_lines.append(f"   Reasons: {', '.join(reasons)}")

        return "\n".join(summary_lines)


def main():
    """Demo usage of DomainRouter"""
    router = DomainRouter()

    print("Available domains:", router.list_domains())
    print()

    # Example 1: Frontend React component
    print("=" * 60)
    print("Example 1: Create a React component")
    print("=" * 60)
    domains = router.identify_domains(
        request_text="Create a reusable button component with TypeScript and Tailwind",
        file_paths=["src/components/Button.tsx"]
    )
    print(router.format_domain_summary(domains))
    print("\nRecommended agents:", router.get_recommended_agents(
        request_text="Create a reusable button component with TypeScript and Tailwind",
        file_paths=["src/components/Button.tsx"]
    ))
    print()

    # Example 2: Backend API with database
    print("=" * 60)
    print("Example 2: Create API endpoint with database")
    print("=" * 60)
    domains = router.identify_domains(
        request_text="Create POST /api/users endpoint with MongoDB integration",
        file_paths=["src/api/routes/users.ts", "src/models/user.model.ts"]
    )
    print(router.format_domain_summary(domains))
    print("\nRecommended agents:", router.get_recommended_agents(
        request_text="Create POST /api/users endpoint with MongoDB integration",
        file_paths=["src/api/routes/users.ts", "src/models/user.model.ts"]
    ))
    print()

    # Example 3: Infrastructure deployment
    print("=" * 60)
    print("Example 3: Deploy with CDK")
    print("=" * 60)
    domains = router.identify_domains(
        request_text="Deploy Lambda function to AWS using CDK",
        file_paths=["infrastructure/lib/lambda-stack.ts"]
    )
    print(router.format_domain_summary(domains))
    print("\nRecommended agents:", router.get_recommended_agents(
        request_text="Deploy Lambda function to AWS using CDK",
        file_paths=["infrastructure/lib/lambda-stack.ts"]
    ))
    print()

    # Example 4: Security vulnerability fix
    print("=" * 60)
    print("Example 4: Fix security vulnerability")
    print("=" * 60)
    domains = router.identify_domains(
        request_text="Fix SQL injection vulnerability in user query",
        file_paths=["src/modules/users/user.repository.ts"]
    )
    print(router.format_domain_summary(domains))
    print("\nRecommended agents:", router.get_recommended_agents(
        request_text="Fix SQL injection vulnerability in user query",
        file_paths=["src/modules/users/user.repository.ts"]
    ))


if __name__ == "__main__":
    main()
