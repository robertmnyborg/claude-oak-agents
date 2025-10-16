from pathlib import Path
import sys

#!/usr/bin/env python3
"""
Generate Transition Models

Analyzes telemetry data and creates transition_expectations.yaml
with expected behavior for each agent.
"""

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from telemetry.analyzer import TelemetryAnalyzer
from collections import defaultdict
import yaml

def generate_transition_models():
    analyzer = TelemetryAnalyzer()
    stats = analyzer.generate_statistics()

    models = {"agents": {}}

    for agent_name, agent_stats in stats["agents"].items():
        models["agents"][agent_name] = {
            "expected_duration_minutes": [
                int(agent_stats["average_duration_seconds"] / 60 * 0.5),
                int(agent_stats["average_duration_seconds"] / 60 * 1.5)
            ],
            "success_rate": round(agent_stats["success_rate"], 2),
            "average_quality": round(agent_stats["average_quality"], 1),
            "common_task_types": agent_stats["common_task_types"],
            "preconditions": [],  # TODO: Manual input required
            "postconditions": [],  # TODO: Manual input required
        }

    output_file = PROJECT_ROOT / "models" / "transition_expectations.yaml"
    with open(output_file, "w") as f:
        yaml.dump(models, f, default_flow_style=False)

    print(f"✓ Generated transition models: {output_file}")
    print("\nNext: Review and add preconditions/postconditions")
    print(f"  python scripts/phase4/review_transition_models.py")

if __name__ == "__main__":
    generate_transition_models()
