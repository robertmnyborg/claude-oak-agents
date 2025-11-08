#!/usr/bin/env python3
"""
Guided Mode - Interactive wizard for PMs and non-technical users

Provides menu-driven workflows for common tasks with clear explanations,
progress updates, and automatic agent coordination.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, List
import subprocess

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.domain_router import DomainRouter

# Color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class GuidedMode:
    """Interactive guided mode for non-technical users"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.domain_router = DomainRouter()

    def print_banner(self):
        """Print welcome banner"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}Welcome to OaK Guided Mode{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")
        print(f"{Colors.CYAN}I'll help you accomplish common tasks with step-by-step guidance.{Colors.END}")
        print(f"{Colors.CYAN}You'll approve each step before we proceed.{Colors.END}\n")

    def show_main_menu(self) -> Optional[int]:
        """Display main menu and get user selection"""
        print(f"\n{Colors.BOLD}What would you like to do?{Colors.END}\n")

        menu_items = [
            ("Create a Feature Specification", "Define requirements and design for a new feature"),
            ("Design a Database Schema", "Create tables, relationships, and migrations"),
            ("Prototype UI Components", "Build React/Vue components with TypeScript"),
            ("Map User Workflows", "Document user journeys and pain points"),
            ("Create Product Roadmap", "Plan features and prioritize development"),
            ("Analyze Business Problem", "Frame problem with Eigenquestions methodology"),
            ("Fork Repo and Create PR", "Professional git workflow with engineering handoff"),
            ("Run Security Scan", "Check for vulnerabilities and compliance issues"),
            ("Exit", "Leave guided mode")
        ]

        for i, (title, description) in enumerate(menu_items, 1):
            print(f"{Colors.CYAN}{i}.{Colors.END} {Colors.BOLD}{title}{Colors.END}")
            print(f"   {description}\n")

        while True:
            try:
                choice = input(f"{Colors.BOLD}Selection [1-{len(menu_items)}]: {Colors.END}").strip()

                if choice.isdigit() and 1 <= int(choice) <= len(menu_items):
                    return int(choice)
                else:
                    print(f"{Colors.RED}Invalid choice. Please enter 1-{len(menu_items)}.{Colors.END}")
            except (EOFError, KeyboardInterrupt):
                return None

    def workflow_create_spec(self):
        """Workflow: Create feature specification"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}Creating Feature Specification{Colors.END}")
        print(f"{Colors.BLUE}{'='*80}{Colors.END}\n")

        print(f"{Colors.CYAN}I'll help you create a spec using the spec-manager agent.{Colors.END}\n")

        # Get feature name
        feature_name = input(f"{Colors.BOLD}What feature are you building? {Colors.END}").strip()
        if not feature_name:
            print(f"{Colors.RED}Feature name required.{Colors.END}")
            return

        # Explain process
        print(f"\n{Colors.GREEN}Great! This will take 10-15 minutes.{Colors.END}")
        print(f"\n{Colors.CYAN}The spec-manager will:{Colors.END}")
        print(f"  1. Define goals and requirements (with your approval)")
        print(f"  2. Design the technical solution (with your approval)")
        print(f"  3. Create an implementation plan (with your approval)")
        print(f"  4. Define testing strategy (with your approval)")

        # Confirm
        proceed = input(f"\n{Colors.BOLD}Ready to start? [Y/n] {Colors.END}").strip().lower()
        if proceed in ['n', 'no']:
            print(f"{Colors.YELLOW}Cancelled.{Colors.END}")
            return

        # Invoke spec-manager
        print(f"\n{Colors.GREEN}Starting spec-manager...{Colors.END}\n")

        task = f"Create specification for: {feature_name}"
        self._invoke_agent("spec-manager", task)

        # Show next steps
        self._show_next_steps([
            "Review the spec",
            "Start implementation",
            "Return to main menu",
            "Exit"
        ])

    def workflow_design_schema(self):
        """Workflow: Design database schema"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}Design Database Schema{Colors.END}")
        print(f"{Colors.BLUE}{'='*80}{Colors.END}\n")

        print(f"{Colors.CYAN}I'll use the backend-architect to design your schema.{Colors.END}\n")

        # Get schema description
        description = input(f"{Colors.BOLD}What data do you need to store? {Colors.END}").strip()
        if not description:
            print(f"{Colors.RED}Description required.{Colors.END}")
            return

        # Ask for database type
        print(f"\n{Colors.BOLD}Which database?{Colors.END}")
        print(f"  1. PostgreSQL (relational)")
        print(f"  2. MongoDB (document)")
        print(f"  3. Let the architect decide")

        db_choice = input(f"\n{Colors.BOLD}Selection [1-3]: {Colors.END}").strip()
        db_types = {"1": "PostgreSQL", "2": "MongoDB", "3": "auto-select"}
        db_type = db_types.get(db_choice, "auto-select")

        # Explain process
        print(f"\n{Colors.GREEN}The backend-architect will:{Colors.END}")
        print(f"  1. Design schema with tables/collections and relationships")
        print(f"  2. Create migration files (DDL)")
        print(f"  3. Suggest indexes for performance")
        print(f"  4. Provide data access patterns")

        proceed = input(f"\n{Colors.BOLD}Proceed? [Y/n] {Colors.END}").strip().lower()
        if proceed in ['n', 'no']:
            return

        # Invoke backend-architect
        task = f"Design {db_type} schema for: {description}"
        self._invoke_agent("backend-architect", task)

        self._show_next_steps([
            "Review schema design",
            "Run migrations",
            "Return to main menu"
        ])

    def workflow_prototype_ui(self):
        """Workflow: Prototype UI components"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}Prototype UI Components{Colors.END}")
        print(f"{Colors.BLUE}{'='*80}{Colors.END}\n")

        print(f"{Colors.CYAN}I'll use the frontend-developer to create components.{Colors.END}\n")

        # Get component description
        component = input(f"{Colors.BOLD}What component do you need? {Colors.END}").strip()
        if not component:
            print(f"{Colors.RED}Component description required.{Colors.END}")
            return

        # Ask for framework
        print(f"\n{Colors.BOLD}Which framework?{Colors.END}")
        print(f"  1. React + TypeScript")
        print(f"  2. Vue + TypeScript")
        print(f"  3. Let the developer decide")

        framework_choice = input(f"\n{Colors.BOLD}Selection [1-3]: {Colors.END}").strip()
        frameworks = {"1": "React + TypeScript", "2": "Vue + TypeScript", "3": "auto-select"}
        framework = frameworks.get(framework_choice, "auto-select")

        # Explain process
        print(f"\n{Colors.GREEN}The frontend-developer will:{Colors.END}")
        print(f"  1. Create component with TypeScript")
        print(f"  2. Set up state management (if needed)")
        print(f"  3. Add styling (Tailwind or styled-components)")
        print(f"  4. Create usage examples")

        proceed = input(f"\n{Colors.BOLD}Proceed? [Y/n] {Colors.END}").strip().lower()
        if proceed in ['n', 'no']:
            return

        # Invoke frontend-developer
        task = f"Create {framework} component: {component}"
        self._invoke_agent("frontend-developer", task)

        self._show_next_steps([
            "Test the component",
            "Integrate into app",
            "Return to main menu"
        ])

    def workflow_map_workflows(self):
        """Workflow: Map user workflows"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}Map User Workflows{Colors.END}")
        print(f"{Colors.BLUE}{'='*80}{Colors.END}\n")

        print(f"{Colors.CYAN}I'll use the product-strategist to map user journeys.{Colors.END}\n")

        # Get workflow description
        workflow = input(f"{Colors.BOLD}Which user workflow? {Colors.END}").strip()
        if not workflow:
            print(f"{Colors.RED}Workflow description required.{Colors.END}")
            return

        # Explain process
        print(f"\n{Colors.GREEN}The product-strategist will:{Colors.END}")
        print(f"  1. Map current user journey with pain points")
        print(f"  2. Identify bottlenecks and friction")
        print(f"  3. Propose improved workflow")
        print(f"  4. Define success metrics")

        proceed = input(f"\n{Colors.BOLD}Proceed? [Y/n] {Colors.END}").strip().lower()
        if proceed in ['n', 'no']:
            return

        # Invoke product-strategist
        task = f"Map user workflow: {workflow}"
        self._invoke_agent("product-strategist", task)

        self._show_next_steps([
            "Review workflow map",
            "Create feature spec to address pain points",
            "Return to main menu"
        ])

    def workflow_create_roadmap(self):
        """Workflow: Create product roadmap"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}Create Product Roadmap{Colors.END}")
        print(f"{Colors.BLUE}{'='*80}{Colors.END}\n")

        print(f"{Colors.CYAN}I'll use the product-strategist for roadmap planning.{Colors.END}\n")

        # Get timeframe
        print(f"{Colors.BOLD}Roadmap timeframe?{Colors.END}")
        print(f"  1. Q1 2026 (3 months)")
        print(f"  2. H1 2026 (6 months)")
        print(f"  3. Full Year 2026")
        print(f"  4. Custom timeframe")

        choice = input(f"\n{Colors.BOLD}Selection [1-4]: {Colors.END}").strip()
        timeframes = {"1": "Q1 2026", "2": "H1 2026", "3": "Full Year 2026"}
        timeframe = timeframes.get(choice, None)

        if not timeframe:
            timeframe = input(f"{Colors.BOLD}Enter custom timeframe: {Colors.END}").strip()

        # Get strategic context
        context = input(f"\n{Colors.BOLD}What's the strategic goal? {Colors.END}").strip()

        # Explain process
        print(f"\n{Colors.GREEN}The product-strategist will:{Colors.END}")
        print(f"  1. Frame strategic objectives")
        print(f"  2. Identify key features and themes")
        print(f"  3. Prioritize using value/effort matrix")
        print(f"  4. Create timeline with milestones")

        proceed = input(f"\n{Colors.BOLD}Proceed? [Y/n] {Colors.END}").strip().lower()
        if proceed in ['n', 'no']:
            return

        # Invoke product-strategist
        task = f"Create product roadmap for {timeframe}: {context}"
        self._invoke_agent("product-strategist", task)

        self._show_next_steps([
            "Review roadmap",
            "Create specs for priority features",
            "Return to main menu"
        ])

    def workflow_analyze_problem(self):
        """Workflow: Analyze business problem"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}Analyze Business Problem{Colors.END}")
        print(f"{Colors.BLUE}{'='*80}{Colors.END}\n")

        print(f"{Colors.CYAN}I'll use the product-strategist with Eigenquestions methodology.{Colors.END}\n")

        # Get problem statement
        problem = input(f"{Colors.BOLD}What problem are you trying to solve? {Colors.END}").strip()
        if not problem:
            print(f"{Colors.RED}Problem statement required.{Colors.END}")
            return

        # Explain Eigenquestions
        print(f"\n{Colors.GREEN}The product-strategist will use Eigenquestions to:{Colors.END}")
        print(f"  1. Identify the root cause (not symptoms)")
        print(f"  2. Frame testable hypotheses")
        print(f"  3. Define success metrics")
        print(f"  4. Propose validation experiments")
        print(f"\n{Colors.CYAN}This helps ensure you're solving the RIGHT problem.{Colors.END}")

        proceed = input(f"\n{Colors.BOLD}Proceed? [Y/n] {Colors.END}").strip().lower()
        if proceed in ['n', 'no']:
            return

        # Invoke product-strategist
        task = f"Apply Eigenquestions methodology to: {problem}"
        self._invoke_agent("product-strategist", task)

        self._show_next_steps([
            "Review analysis",
            "Validate hypotheses",
            "Create feature spec",
            "Return to main menu"
        ])

    def workflow_git_pr(self):
        """Workflow: Fork repo and create PR"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}Fork Repo and Create PR{Colors.END}")
        print(f"{Colors.BLUE}{'='*80}{Colors.END}\n")

        print(f"{Colors.CYAN}I'll use the git-workflow-manager for professional git operations.{Colors.END}\n")

        # Get repo URL
        repo_url = input(f"{Colors.BOLD}GitHub repository URL: {Colors.END}").strip()
        if not repo_url:
            print(f"{Colors.RED}Repository URL required.{Colors.END}")
            return

        # Get branch name
        branch_name = input(f"{Colors.BOLD}Feature branch name: {Colors.END}").strip()
        if not branch_name:
            print(f"{Colors.RED}Branch name required.{Colors.END}")
            return

        # Explain process
        print(f"\n{Colors.GREEN}The git-workflow-manager will:{Colors.END}")
        print(f"  1. Fork the repository")
        print(f"  2. Create feature branch")
        print(f"  3. Commit changes with proper messages")
        print(f"  4. Create PR with complete context")

        proceed = input(f"\n{Colors.BOLD}Proceed? [Y/n] {Colors.END}").strip().lower()
        if proceed in ['n', 'no']:
            return

        # Invoke git-workflow-manager
        task = f"Fork {repo_url}, create branch {branch_name}, and prepare PR"
        self._invoke_agent("git-workflow-manager", task)

        self._show_next_steps([
            "Review PR description",
            "Push to remote",
            "Return to main menu"
        ])

    def workflow_security_scan(self):
        """Workflow: Run security scan"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}Run Security Scan{Colors.END}")
        print(f"{Colors.BLUE}{'='*80}{Colors.END}\n")

        print(f"{Colors.CYAN}I'll coordinate security-auditor and dependency-scanner.{Colors.END}\n")

        # Get scan scope
        print(f"{Colors.BOLD}What to scan?{Colors.END}")
        print(f"  1. Full codebase")
        print(f"  2. Specific directory")
        print(f"  3. Dependencies only")

        choice = input(f"\n{Colors.BOLD}Selection [1-3]: {Colors.END}").strip()

        if choice == "2":
            directory = input(f"{Colors.BOLD}Directory path: {Colors.END}").strip()
            scope = f"directory: {directory}"
        elif choice == "3":
            scope = "dependencies only"
        else:
            scope = "full codebase"

        # Explain process
        print(f"\n{Colors.GREEN}The security team will:{Colors.END}")
        print(f"  1. Scan for OWASP Top 10 vulnerabilities")
        print(f"  2. Check dependency vulnerabilities")
        print(f"  3. Analyze IAM policies and permissions")
        print(f"  4. Generate remediation recommendations")

        proceed = input(f"\n{Colors.BOLD}Proceed? [Y/n] {Colors.END}").strip().lower()
        if proceed in ['n', 'no']:
            return

        # Invoke security agents
        task = f"Security scan for {scope}"
        print(f"\n{Colors.GREEN}Running security-auditor...{Colors.END}")
        self._invoke_agent("security-auditor", task)

        print(f"\n{Colors.GREEN}Running dependency-scanner...{Colors.END}")
        self._invoke_agent("dependency-scanner", "Scan dependencies for vulnerabilities")

        self._show_next_steps([
            "Review security report",
            "Address critical issues",
            "Return to main menu"
        ])

    def _invoke_agent(self, agent_name: str, task: str):
        """Invoke an agent (placeholder - would integrate with actual agent system)"""
        print(f"\n{Colors.YELLOW}[DEMO MODE - Agent invocation would happen here]{Colors.END}")
        print(f"{Colors.CYAN}Agent:{Colors.END} {agent_name}")
        print(f"{Colors.CYAN}Task:{Colors.END} {task}")
        print(f"\n{Colors.GREEN}In production, this would invoke the agent and show progress.{Colors.END}\n")

    def _show_next_steps(self, steps: List[str]):
        """Show next steps menu"""
        print(f"\n{Colors.BOLD}What's next?{Colors.END}")
        for i, step in enumerate(steps, 1):
            print(f"  {i}. {step}")

        choice = input(f"\n{Colors.BOLD}Selection [1-{len(steps)}]: {Colors.END}").strip()
        # Handle next step selection (simplified for now)

    def run(self):
        """Main guided mode loop"""
        self.print_banner()

        workflows = {
            1: self.workflow_create_spec,
            2: self.workflow_design_schema,
            3: self.workflow_prototype_ui,
            4: self.workflow_map_workflows,
            5: self.workflow_create_roadmap,
            6: self.workflow_analyze_problem,
            7: self.workflow_git_pr,
            8: self.workflow_security_scan,
            9: None  # Exit
        }

        while True:
            choice = self.show_main_menu()

            if choice is None or choice == 9:
                print(f"\n{Colors.GREEN}Thanks for using OaK Guided Mode!{Colors.END}\n")
                break

            workflow_func = workflows.get(choice)
            if workflow_func:
                workflow_func()
            else:
                print(f"{Colors.RED}Invalid selection.{Colors.END}")


def main():
    """Entry point"""
    try:
        guided = GuidedMode()
        guided.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user{Colors.END}")
        sys.exit(0)


if __name__ == "__main__":
    main()
