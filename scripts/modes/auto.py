#!/usr/bin/env python3
"""
Auto Mode - Classification-based routing (existing OaK behavior)

This is a reference implementation showing how auto mode works.
In practice, auto mode is the default behavior of the Claude OaK system.
"""

import sys
from pathlib import Path

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


def explain_auto_mode():
    """Explain how auto mode works"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}OaK Auto Mode - Classification-Based Routing{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")

    print(f"{Colors.CYAN}Auto mode is the standard Claude OaK behavior.{Colors.END}\n")

    print(f"{Colors.BOLD}How It Works:{Colors.END}\n")

    print(f"{Colors.GREEN}1. Request Classification{Colors.END}")
    print(f"   User makes a request → Main LLM classifies as:")
    print(f"   - INFORMATION (simple questions, file reads)")
    print(f"   - IMPLEMENTATION (code changes, features, fixes)")
    print(f"   - ANALYSIS (research, investigation)")
    print(f"   - COORDINATION (multi-agent workflows)\n")

    print(f"{Colors.GREEN}2. Domain Detection{Colors.END}")
    print(f"   Domain Router analyzes:")
    print(f"   - Keywords in request text")
    print(f"   - File paths being modified")
    print(f"   - Technology stack mentions")
    print(f"   → Identifies domain(s): Frontend, Backend, Infrastructure, Security, Data\n")

    print(f"{Colors.GREEN}3. Agent Selection{Colors.END}")
    print(f"   Based on classification + domain:")
    print(f"   - IMPLEMENTATION + Frontend → frontend-developer")
    print(f"   - IMPLEMENTATION + Backend → backend-architect")
    print(f"   - IMPLEMENTATION + Infrastructure → infrastructure-specialist")
    print(f"   - ANALYSIS + Security → security-auditor")
    print(f"   - ANALYSIS + Business → business-analyst\n")

    print(f"{Colors.GREEN}4. Workflow Execution{Colors.END}")
    print(f"   Standard workflow:")
    print(f"   - design-simplicity-advisor (KISS analysis)")
    print(f"   - domain specialist (implementation)")
    print(f"   - quality-gate (unified validation)")
    print(f"   - git-workflow-manager (commit + PR)\n")

    print(f"{Colors.GREEN}5. Telemetry Tracking{Colors.END}")
    print(f"   All agent invocations logged for:")
    print(f"   - Performance analysis")
    print(f"   - Success rate tracking")
    print(f"   - Workflow optimization\n")

    print(f"{Colors.BOLD}Example Request Flow:{Colors.END}\n")

    print(f'{Colors.CYAN}User:{Colors.END} "Create a React button component with TypeScript"\n')

    print(f"{Colors.YELLOW}Classification:{Colors.END} IMPLEMENTATION")
    print(f"{Colors.YELLOW}Domain Detection:{Colors.END}")
    print(f"  - Keywords matched: react, component, typescript")
    print(f"  - Domain: Frontend (confidence: 0.95)")

    print(f"{Colors.YELLOW}Agent Plan:{Colors.END}")
    print(f"  1. design-simplicity-advisor → Analyze approach")
    print(f"  2. frontend-developer → Create component")
    print(f"  3. quality-gate → Validate code")
    print(f"  4. git-workflow-manager → Commit changes\n")

    print(f"{Colors.GREEN}Result:{Colors.END} Component created, validated, and committed\n")

    print(f"{Colors.BOLD}Available Tools:{Colors.END}\n")
    print(f"  {Colors.CYAN}oak-discover{Colors.END}  - Browse agents and capabilities")
    print(f"  {Colors.CYAN}oak-status{Colors.END}    - System status and telemetry")
    print(f"  {Colors.CYAN}oak-analyze{Colors.END}   - Analytics dashboard")
    print(f"  {Colors.CYAN}oak-history{Colors.END}   - Agent invocation history")
    print(f"  {Colors.CYAN}oak-insights{Colors.END}  - Performance insights\n")

    print(f"{Colors.BOLD}Domain Router Example:{Colors.END}\n")
    demonstrate_domain_router()


def demonstrate_domain_router():
    """Show domain router in action"""
    router = DomainRouter()

    examples = [
        {
            "request": "Fix SQL injection in user query",
            "files": ["src/modules/users/user.repository.ts"]
        },
        {
            "request": "Deploy Lambda function with CDK",
            "files": ["infrastructure/lib/lambda-stack.ts"]
        },
        {
            "request": "Create Vue dashboard component",
            "files": ["src/components/Dashboard.vue"]
        }
    ]

    for example in examples:
        print(f"{Colors.CYAN}Request:{Colors.END} {example['request']}")
        print(f"{Colors.CYAN}Files:{Colors.END} {', '.join(example['files'])}\n")

        domains = router.identify_domains(
            request_text=example['request'],
            file_paths=example['files']
        )

        if domains:
            for domain_match in domains:
                domain_name = domain_match['domain']
                confidence = domain_match['confidence']
                reasons = domain_match['reasons']
                config = domain_match['config']

                print(f"  {Colors.GREEN}→ Domain:{Colors.END} {domain_name.upper()} (confidence: {confidence:.2f})")
                print(f"    {Colors.YELLOW}Primary agent:{Colors.END} {config.primary_agent}")
                print(f"    {Colors.YELLOW}Reasons:{Colors.END} {', '.join(reasons)}")
        else:
            print(f"  {Colors.YELLOW}No specific domain detected (use general-purpose){Colors.END}")

        print()


def main():
    """Entry point"""
    try:
        explain_auto_mode()

        print(f"{Colors.BOLD}This is a reference explanation of auto mode.{Colors.END}")
        print(f"{Colors.BOLD}In production, auto mode is the default OaK behavior.{Colors.END}\n")

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user{Colors.END}")
        sys.exit(0)


if __name__ == "__main__":
    main()
