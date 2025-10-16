#!/usr/bin/env python3
"""
End-to-End Telemetry Test

Tests the complete telemetry workflow:
1. Create test workspace
2. Extract state features
3. Log agent invocations
4. Log success metrics
5. Analyze performance
"""

import sys
import tempfile
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from telemetry.logger import TelemetryLogger
from telemetry.analyzer import TelemetryAnalyzer
from state_analysis.feature_extractor import FeatureExtractor


def create_test_workspace():
    """Create a temporary test workspace with sample files."""
    temp_dir = Path(tempfile.mkdtemp(prefix="oak_test_"))

    # Create sample Python files
    (temp_dir / "main.py").write_text("""
def hello():
    print("Hello, OaK!")

if __name__ == "__main__":
    hello()
""")

    (temp_dir / "utils.py").write_text("""
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
""")

    # Create test file
    (temp_dir / "test_main.py").write_text("""
from main import hello

def test_hello():
    # Test would go here
    pass
""")

    # Create README
    (temp_dir / "README.md").write_text("# Test Project\n\nA test project for OaK.")

    print(f"✅ Created test workspace at: {temp_dir}")
    return temp_dir


def test_state_extraction(workspace_dir):
    """Test state feature extraction."""
    print("\n" + "="*70)
    print("TESTING STATE EXTRACTION")
    print("="*70)

    extractor = FeatureExtractor(workspace_dir=workspace_dir)
    features = extractor.extract_all_features()

    print(f"\n📊 Extracted Features:")
    print(f"  Languages: {features['codebase']['languages']}")
    print(f"  File Count: {features['codebase']['file_count']}")
    print(f"  LOC: {features['codebase']['loc']}")
    print(f"  Tests Exist: {features['context']['tests_exist']}")
    print(f"  Docs Exist: {features['context']['docs_exist']}")

    assert features['codebase']['languages'] == ['Python']
    assert features['codebase']['file_count'] == 3
    assert features['context']['tests_exist'] == True
    assert features['context']['docs_exist'] == True

    print("\n✅ State extraction tests passed!")
    return features


def test_telemetry_logging(features):
    """Test telemetry logging workflow."""
    print("\n" + "="*70)
    print("TESTING TELEMETRY LOGGING")
    print("="*70)

    # Use temp directory for telemetry
    temp_telemetry = Path(tempfile.mkdtemp(prefix="oak_telemetry_"))
    logger = TelemetryLogger(telemetry_dir=temp_telemetry)

    print(f"\n📝 Logging to: {temp_telemetry}")

    # Simulate multiple agent invocations
    test_scenarios = [
        {
            "agent_name": "frontend-developer",
            "agent_type": "development",
            "task_description": "Add dark mode toggle",
            "duration": 120,
            "status": "success",
            "quality": 4
        },
        {
            "agent_name": "backend-architect",
            "agent_type": "development",
            "task_description": "Design API endpoints",
            "duration": 180,
            "status": "success",
            "quality": 5
        },
        {
            "agent_name": "frontend-developer",
            "agent_type": "development",
            "task_description": "Fix responsive layout",
            "duration": 90,
            "status": "success",
            "quality": 4
        },
        {
            "agent_name": "unit-test-expert",
            "agent_type": "quality",
            "task_description": "Write unit tests",
            "duration": 150,
            "status": "success",
            "quality": 5
        },
        {
            "agent_name": "frontend-developer",
            "agent_type": "development",
            "task_description": "Optimize bundle size",
            "duration": 200,
            "status": "partial",
            "quality": 3
        }
    ]

    invocation_ids = []

    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n  [{i}/{len(test_scenarios)}] Logging: {scenario['agent_name']} - {scenario['task_description']}")

        # Log invocation
        inv_id = logger.log_invocation(
            agent_name=scenario["agent_name"],
            agent_type=scenario["agent_type"],
            task_description=scenario["task_description"],
            state_features=features
        )
        invocation_ids.append(inv_id)

        # Update with completion
        logger.update_invocation(
            invocation_id=inv_id,
            duration_seconds=scenario["duration"],
            outcome_status=scenario["status"],
            files_modified=[f"src/file{i}.ts"],
            tools_used=["Read", "Edit", "Bash"]
        )

        # Log success metric
        logger.log_success_metric(
            invocation_id=inv_id,
            success=(scenario["status"] == "success"),
            quality_rating=scenario["quality"],
            feedback_source="human",
            feedback_notes=f"Test scenario {i}"
        )

    print(f"\n✅ Logged {len(invocation_ids)} agent invocations")
    return temp_telemetry


def test_telemetry_analysis(telemetry_dir):
    """Test telemetry analysis."""
    print("\n" + "="*70)
    print("TESTING TELEMETRY ANALYSIS")
    print("="*70)

    analyzer = TelemetryAnalyzer(telemetry_dir=telemetry_dir)

    # Load data
    invocations = analyzer.load_invocations()
    metrics = analyzer.load_metrics()

    print(f"\n📈 Loaded Data:")
    print(f"  Total Invocations: {len(invocations)}")
    print(f"  Total Metrics: {len(metrics)}")

    assert len(invocations) == 5
    assert len(metrics) == 5

    # Generate statistics
    stats = analyzer.generate_statistics()

    print(f"\n📊 Generated Statistics:")
    print(f"  Total Invocations: {stats['total_invocations']}")
    print(f"  Unique Agents: {len(stats['agents'])}")

    # Check frontend-developer stats
    frontend_stats = stats['agents'].get('frontend-developer')
    if frontend_stats:
        print(f"\n  Frontend Developer Stats:")
        print(f"    Invocations: {frontend_stats['invocation_count']}")
        print(f"    Success Rate: {frontend_stats['success_rate']*100:.1f}%")
        print(f"    Avg Quality: {frontend_stats['average_quality']:.2f}/5.0")
        print(f"    Avg Duration: {frontend_stats['average_duration_seconds']:.1f}s")

    # Get rankings
    rankings = analyzer.get_agent_ranking()

    print(f"\n🏆 Agent Rankings:")
    for i, (agent_name, score, agent_stats) in enumerate(rankings, 1):
        print(f"  {i}. {agent_name}: {score:.3f} "
              f"({agent_stats['invocation_count']} uses, "
              f"{agent_stats['success_rate']*100:.0f}% success)")

    # Save statistics
    analyzer.save_statistics()
    print(f"\n💾 Statistics saved to: {telemetry_dir / 'performance_stats.json'}")

    print("\n✅ Telemetry analysis tests passed!")
    return stats


def main():
    """Run end-to-end test."""
    print("\n" + "="*70)
    print("CLAUDE OAK AGENTS - END-TO-END TELEMETRY TEST")
    print("="*70)

    try:
        # Step 1: Create test workspace
        workspace = create_test_workspace()

        # Step 2: Extract state features
        features = test_state_extraction(workspace)

        # Step 3: Test telemetry logging
        telemetry_dir = test_telemetry_logging(features)

        # Step 4: Test telemetry analysis
        stats = test_telemetry_analysis(telemetry_dir)

        # Final summary
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70)
        print(f"\nTest workspace: {workspace}")
        print(f"Telemetry data: {telemetry_dir}")
        print(f"\nYou can inspect the telemetry files:")
        print(f"  cat {telemetry_dir}/agent_invocations.jsonl")
        print(f"  cat {telemetry_dir}/success_metrics.jsonl")
        print(f"  cat {telemetry_dir}/performance_stats.json")

        return 0

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
