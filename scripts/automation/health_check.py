from pathlib import Path
import sys

#!/usr/bin/env python3
"""
Daily Health Check

Verifies system is functioning correctly.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def health_check():
    PROJECT_ROOT = Path(__file__).parent.parent.parent

    checks = []

    # Check 1: Telemetry directory writable
    telemetry_dir = PROJECT_ROOT / "telemetry"
    try:
        test_file = telemetry_dir / ".health_check"
        test_file.touch()
        test_file.unlink()
        checks.append(("Telemetry writable", True))
    except Exception as e:
        checks.append(("Telemetry writable", False, str(e)))

    # Check 2: Hooks installed
    hooks_dir = Path.home() / ".claude" / "hooks"
    pre_hook = hooks_dir / "pre_agent.sh"
    post_hook = hooks_dir / "post_agent.sh"

    checks.append(("Pre-hook installed", pre_hook.exists()))
    checks.append(("Post-hook installed", post_hook.exists()))

    # Check 3: Recent invocations
    inv_file = telemetry_dir / "agent_invocations.jsonl"
    if inv_file.exists():
        lines = inv_file.read_text().strip().split("\n")
        checks.append(("Recent invocations", len(lines) > 0))
    else:
        checks.append(("Recent invocations", False))

    # Report
    print(f"\n🏥 Health Check: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    all_pass = True

    for check in checks:
        if check[1]:
            print(f"  ✓ {check[0]}")
        else:
            print(f"  ✗ {check[0]}")
            if len(check) > 2:
                print(f"    Error: {check[2]}")
            all_pass = False

    if all_pass:
        print("\n✓ All checks passed")
        return 0
    else:
        print("\n⚠️  Some checks failed")
        return 1

if __name__ == "__main__":
    from datetime import datetime
    sys.exit(health_check())
