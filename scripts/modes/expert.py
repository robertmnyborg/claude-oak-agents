#!/usr/bin/env python3
"""
Expert Mode - Direct control interface for experienced engineers

Provides command-line interface with direct agent invocation, workflow control,
and full system access for power users.
"""

import os
import sys
import cmd
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
import readline

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.domain_router import DomainRouter
from core.agent_loader import AgentLoader

# Add scripts directory to path for shared imports
SCRIPTS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from shared import Colors


class ExpertShell(cmd.Cmd):
    """Interactive shell for expert mode"""

    intro = f"""
{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}
{Colors.BOLD}{Colors.BLUE}Welcome to OaK Expert Mode{Colors.END}
{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}

{Colors.CYAN}Direct control interface for experienced engineers.{Colors.END}

Type '{Colors.BOLD}help{Colors.END}' or '{Colors.BOLD}?{Colors.END}' for commands.
Type '{Colors.BOLD}discover{Colors.END}' to browse available agents.
Type '{Colors.BOLD}exit{Colors.END}' to quit.
"""

    prompt = f"{Colors.BOLD}{Colors.GREEN}oak> {Colors.END}"

    def __init__(self):
        super().__init__()
        self.project_root = Path(__file__).parent.parent.parent
        self.domain_router = DomainRouter()
        self.agent_loader = AgentLoader(self.project_root / "agents")
        self.history_file = Path.home() / ".oak" / "expert_history"
        self.load_history()

    def load_history(self):
        """Load command history"""
        if self.history_file.exists():
            try:
                readline.read_history_file(self.history_file)
            except Exception:
                pass

    def save_history(self):
        """Save command history"""
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            readline.write_history_file(self.history_file)
        except Exception:
            pass

    def do_agent(self, arg):
        """
        Invoke agent directly.

        Usage: agent <name> <task>
        Example: agent backend-architect Design user authentication schema
        """
        parts = arg.split(maxsplit=1)
        if len(parts) < 2:
            print(f"{Colors.RED}Usage: agent <name> <task>{Colors.END}")
            return

        agent_name, task = parts

        # Validate agent exists
        try:
            agent = self.agent_loader.load_agent(agent_name)
        except ValueError:
            print(f"{Colors.RED}Agent not found: {agent_name}{Colors.END}")
            print(f"{Colors.YELLOW}Use 'discover' to see available agents.{Colors.END}")
            return

        print(f"\n{Colors.CYAN}Invoking agent:{Colors.END} {agent_name}")
        print(f"{Colors.CYAN}Task:{Colors.END} {task}\n")

        # In production, this would invoke the agent via Claude API
        print(f"{Colors.YELLOW}[DEMO MODE - Agent invocation would happen here]{Colors.END}")
        print(f"{Colors.GREEN}Agent: {agent.metadata.name}{Colors.END}")
        print(f"{Colors.GREEN}Description: {agent.metadata.description}{Colors.END}\n")

    def do_workflow(self, arg):
        """
        Start workflow pattern.

        Usage: workflow <pattern>
        Patterns: secure-api, database-migration, feature-spec, security-audit
        """
        patterns = {
            "secure-api": self.workflow_secure_api,
            "database-migration": self.workflow_database_migration,
            "feature-spec": self.workflow_feature_spec,
            "security-audit": self.workflow_security_audit
        }

        pattern = arg.strip().lower()
        if not pattern:
            print(f"{Colors.BOLD}Available workflow patterns:{Colors.END}")
            for p in patterns.keys():
                print(f"  - {p}")
            return

        workflow_func = patterns.get(pattern)
        if workflow_func:
            workflow_func()
        else:
            print(f"{Colors.RED}Unknown workflow pattern: {pattern}{Colors.END}")

    def workflow_secure_api(self):
        """Execute secure API workflow"""
        print(f"\n{Colors.BOLD}Secure API Workflow{Colors.END}")
        print(f"{Colors.CYAN}Coordination: design-simplicity-advisor → backend-architect → security-auditor → quality-gate{Colors.END}\n")

        endpoint = input(f"API endpoint to create: ")
        if not endpoint:
            return

        print(f"\n{Colors.GREEN}Executing workflow...{Colors.END}\n")
        self._invoke_workflow_agent("design-simplicity-advisor", f"Analyze approach for {endpoint}")
        self._invoke_workflow_agent("backend-architect", f"Implement {endpoint}")
        self._invoke_workflow_agent("security-auditor", f"Security review of {endpoint}")
        self._invoke_workflow_agent("quality-gate", f"Validate implementation")

        print(f"\n{Colors.GREEN}Workflow complete!{Colors.END}\n")

    def workflow_database_migration(self):
        """Execute database migration workflow"""
        print(f"\n{Colors.BOLD}Database Migration Workflow{Colors.END}")
        print(f"{Colors.CYAN}Coordination: backend-architect → quality-gate → git-workflow-manager{Colors.END}\n")

        migration = input(f"Migration description: ")
        if not migration:
            return

        print(f"\n{Colors.GREEN}Executing workflow...{Colors.END}\n")
        self._invoke_workflow_agent("backend-architect", f"Create migration for: {migration}")
        self._invoke_workflow_agent("quality-gate", "Review migration")
        self._invoke_workflow_agent("git-workflow-manager", "Commit migration")

        print(f"\n{Colors.GREEN}Workflow complete!{Colors.END}\n")

    def workflow_feature_spec(self):
        """Execute feature spec workflow"""
        print(f"\n{Colors.BOLD}Feature Specification Workflow{Colors.END}")
        print(f"{Colors.CYAN}Coordination: spec-manager (collaborative spec creation){Colors.END}\n")

        feature = input(f"Feature name: ")
        if not feature:
            return

        print(f"\n{Colors.GREEN}Launching spec-manager...{Colors.END}\n")
        self._invoke_workflow_agent("spec-manager", f"Create spec for: {feature}")

        print(f"\n{Colors.GREEN}Workflow complete!{Colors.END}\n")

    def workflow_security_audit(self):
        """Execute security audit workflow"""
        print(f"\n{Colors.BOLD}Security Audit Workflow{Colors.END}")
        print(f"{Colors.CYAN}Parallel: security-auditor + dependency-scanner → quality-gate{Colors.END}\n")

        scope = input(f"Audit scope (default: full codebase): ").strip()
        if not scope:
            scope = "full codebase"

        print(f"\n{Colors.GREEN}Executing parallel security scan...{Colors.END}\n")
        self._invoke_workflow_agent("security-auditor", f"Audit {scope}")
        self._invoke_workflow_agent("dependency-scanner", "Scan dependencies")
        self._invoke_workflow_agent("quality-gate", "Review security findings")

        print(f"\n{Colors.GREEN}Workflow complete!{Colors.END}\n")

    def _invoke_workflow_agent(self, agent_name: str, task: str):
        """Helper to invoke agent in workflow"""
        print(f"{Colors.CYAN}→ {agent_name}:{Colors.END} {task}")
        # In production, invoke actual agent

    def do_spec(self, arg):
        """
        Spec operations.

        Usage:
          spec create <feature-name>    - Create new spec
          spec load <spec-id>            - Load existing spec
          spec list                      - List all specs
          spec update <spec-id>          - Update spec
        """
        parts = arg.split(maxsplit=1)
        if not parts:
            print(f"{Colors.RED}Usage: spec <action> [args]{Colors.END}")
            return

        action = parts[0]
        args = parts[1] if len(parts) > 1 else ""

        if action == "create":
            self._spec_create(args)
        elif action == "load":
            self._spec_load(args)
        elif action == "list":
            self._spec_list()
        elif action == "update":
            self._spec_update(args)
        else:
            print(f"{Colors.RED}Unknown spec action: {action}{Colors.END}")

    def _spec_create(self, feature_name: str):
        """Create new spec"""
        if not feature_name:
            feature_name = input(f"Feature name: ")

        print(f"\n{Colors.GREEN}Creating spec: {feature_name}{Colors.END}\n")
        self._invoke_workflow_agent("spec-manager", f"Create spec for: {feature_name}")

    def _spec_load(self, spec_id: str):
        """Load existing spec"""
        specs_dir = self.project_root / "specs" / "active"
        if not spec_id:
            print(f"{Colors.RED}Spec ID required{Colors.END}")
            return

        spec_file = specs_dir / f"{spec_id}.md"
        if spec_file.exists():
            print(f"\n{Colors.GREEN}Loading spec: {spec_id}{Colors.END}\n")
            print(spec_file.read_text())
        else:
            print(f"{Colors.RED}Spec not found: {spec_id}{Colors.END}")

    def _spec_list(self):
        """List all specs"""
        specs_dir = self.project_root / "specs" / "active"
        if not specs_dir.exists():
            print(f"{Colors.YELLOW}No specs directory found{Colors.END}")
            return

        specs = list(specs_dir.glob("*.md"))
        if not specs:
            print(f"{Colors.YELLOW}No active specs found{Colors.END}")
            return

        print(f"\n{Colors.BOLD}Active Specs:{Colors.END}\n")
        for spec in sorted(specs):
            print(f"  - {spec.stem}")
        print()

    def _spec_update(self, spec_id: str):
        """Update existing spec"""
        if not spec_id:
            spec_id = input(f"Spec ID: ")

        print(f"\n{Colors.GREEN}Updating spec: {spec_id}{Colors.END}\n")
        self._invoke_workflow_agent("spec-manager", f"Update spec: {spec_id}")

    def do_status(self, arg):
        """Show system status and telemetry."""
        print(f"\n{Colors.GREEN}Running oak-status...{Colors.END}\n")
        status_script = self.project_root / "scripts" / "oak-status"
        if status_script.exists():
            subprocess.run([str(status_script)])
        else:
            print(f"{Colors.RED}oak-status not found{Colors.END}")

    def do_analyze(self, arg):
        """Show analytics dashboard."""
        print(f"\n{Colors.GREEN}Running oak-analyze...{Colors.END}\n")
        analyze_script = self.project_root / "scripts" / "oak-analyze"
        if analyze_script.exists():
            subprocess.run([str(analyze_script)])
        else:
            print(f"{Colors.RED}oak-analyze not found{Colors.END}")

    def do_discover(self, arg):
        """Browse available agents."""
        print(f"\n{Colors.GREEN}Running oak-discover...{Colors.END}\n")
        discover_script = self.project_root / "scripts" / "oak-discover"
        if discover_script.exists():
            subprocess.run([str(discover_script)])
        else:
            # Fallback: show agents from agent loader
            self._show_agents()

    def _show_agents(self):
        """Show available agents"""
        metadata = self.agent_loader.load_all_metadata()

        print(f"\n{Colors.BOLD}Available Agents ({len(metadata)}){Colors.END}\n")

        by_category = {}
        for agent_meta in metadata.values():
            category = agent_meta.category
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(agent_meta)

        for category in sorted(by_category.keys()):
            print(f"{Colors.CYAN}{category}:{Colors.END}")
            for agent in sorted(by_category[category], key=lambda a: a.name):
                print(f"  - {Colors.BOLD}{agent.name}{Colors.END}")
                print(f"    {agent.description[:80]}...")
            print()

    def do_auto(self, arg):
        """Switch to auto mode."""
        print(f"\n{Colors.YELLOW}Switching to auto mode...{Colors.END}\n")
        self.save_history()
        os.execvp(sys.executable, [sys.executable, str(self.project_root / "scripts" / "oak-mode"), "--auto"])

    def do_guided(self, arg):
        """Switch to guided mode."""
        print(f"\n{Colors.YELLOW}Switching to guided mode...{Colors.END}\n")
        self.save_history()
        os.execvp(sys.executable, [sys.executable, str(self.project_root / "scripts" / "oak-mode"), "--guided"])

    def do_exit(self, arg):
        """Exit expert mode."""
        print(f"\n{Colors.GREEN}Goodbye!{Colors.END}\n")
        self.save_history()
        return True

    def do_quit(self, arg):
        """Exit expert mode."""
        return self.do_exit(arg)

    def do_EOF(self, arg):
        """Handle Ctrl+D."""
        print()  # New line
        return self.do_exit(arg)

    def emptyline(self):
        """Do nothing on empty line."""
        pass

    def default(self, line):
        """Handle unknown commands."""
        print(f"{Colors.RED}Unknown command: {line}{Colors.END}")
        print(f"{Colors.YELLOW}Type 'help' for available commands.{Colors.END}")


def main():
    """Entry point"""
    try:
        shell = ExpertShell()
        shell.cmdloop()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user{Colors.END}")
        sys.exit(0)


if __name__ == "__main__":
    main()
