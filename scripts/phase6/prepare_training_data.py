from pathlib import Path
import sys

#!/usr/bin/env python3
"""
Prepare Training Data

Preprocesses telemetry data for machine learning.
"""

import sys
import json
import random
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from telemetry.analyzer import TelemetryAnalyzer

def prepare_training_data():
    analyzer = TelemetryAnalyzer()
    invocations = analyzer.load_invocations()
    metrics = analyzer.load_metrics()

    # Create lookup for metrics
    metrics_by_inv = {m["invocation_id"]: m for m in metrics}

    # Prepare dataset
    dataset = []
    for inv in invocations:
        if inv["invocation_id"] in metrics_by_inv:
            metric = metrics_by_inv[inv["invocation_id"]]

            record = {
                "state_features": inv["state_features"],
                "agent_name": inv["agent_name"],
                "outcome": inv["outcome"]["status"],
                "duration": inv.get("duration_seconds", 0),
                "quality": metric["quality_rating"],
                "success": metric["success"]
            }
            dataset.append(record)

    # Split dataset
    random.shuffle(dataset)
    train_size = int(len(dataset) * 0.7)
    val_size = int(len(dataset) * 0.2)

    train = dataset[:train_size]
    val = dataset[train_size:train_size+val_size]
    test = dataset[train_size+val_size:]

    # Save datasets
    ml_dir = PROJECT_ROOT / "docs" / "experimental" / "phase6" / "ml-data"
    ml_dir.mkdir(parents=True, exist_ok=True)

    for name, data in [("train", train), ("val", val), ("test", test)]:
        with open(ml_dir / f"{name}.json", "w") as f:
            json.dump(data, f, indent=2)
        print(f"✓ Saved {len(data)} records to {name}.json")

    print(f"\nTotal: {len(dataset)} records")
    print(f"Train: {len(train)} (70%)")
    print(f"Val: {len(val)} (20%)")
    print(f"Test: {len(test)} (10%)")

    print("\nNext: Validate data quality")
    print("  python scripts/phase6/validate_training_data.py")

if __name__ == "__main__":
    prepare_training_data()
