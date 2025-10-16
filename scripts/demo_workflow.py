#!/usr/bin/env python3
"""
Demo OaK Workflow

Demonstrates the complete OaK workflow:
1. State analysis
2. Feature ranking
3. Agent selection based on state
4. Telemetry logging
5. Performance analysis
"""

import sys
import json
import tempfile
from pathlib import Path
from datetime import datetime

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from telemetry.logger import TelemetryLogger
from telemetry.analyzer import TelemetryAnalyzer
from state_analysis.feature_extractor import FeatureExtractor


def print_banner(text):
    """Print a formatted banner."""
    print("\n" + "="*70)
    print(text.center(70))
    print("="*70)


def rank_features(features):
    """
    Rank features by importance.

    This is a simplified version of what the state-analyzer agent would do.
    """
    ranked = []

    codebase = features["codebase"]
    context = features["context"]

    # Risk assessment
    risk_level = "low"
    if codebase["complexity"] == "very_high":
        risk_level = "high"
    elif codebase["complexity"] == "high":
        risk_level = "medium"

    if risk_level in ["high", "critical"]:
        ranked.append({
            "feature": "risk_level",
            "value": risk_level,
            "importance": 0.95,
            "reason": "High complexity requires careful planning"
        })

    # Test status
    if not context["tests_exist"]:
        ranked.append({
            "feature": "tests_exist",
            "value": False,
            "importance": 0.90,
            "reason": "No tests means higher risk"
        })
    elif context["tests_passing"] == False:
        ranked.append({
            "feature": "tests_passing",
            "value": False,
            "importance": 0.95,
            "reason": "Broken tests must be fixed first"
        })

    # Complexity
    if codebase["complexity"] in ["high", "very_high"]:
        ranked.append({
            "feature": "complexity",
            "value": codebase["complexity"],
            "importance": 0.75,
            "reason": "Requires systematic decomposition"
        })

    # Documentation
    if not context["docs_exist"]:
        ranked.append({
            "feature": "docs_exist",
            "value": False,
            "importance": 0.60,
            "reason": "Missing documentation reduces maintainability"
        })

    # Git state
    if context["git_clean"] == False:
        ranked.append({
            "feature": "git_clean",
            "value": False,
            "importance": 0.50,
            "reason": "Uncommitted changes should be resolved"
        })

    # Sort by importance
    ranked.sort(key=lambda x: x["importance"], reverse=True)

    return ranked


def recommend_agents(ranked_features, task_type="feature_development"):
    """Recommend agents based on ranked features."""
    recommended = {
        "primary_agents": [],
        "support_agents": [],
        "workflow": "sequential"
    }

    # Check top features
    top_features = {f["feature"]: f["value"] for f in ranked_features[:3]}

    # Risk-based recommendations
    if top_features.get("risk_level") in ["high", "critical"]:
        recommended["primary_agents"].append("security-auditor")
        recommended["primary_agents"].append("systems-architect")

    # Test-based recommendations
    if top_features.get("tests_passing") == False:
        recommended["primary_agents"].insert(0, "debug-specialist")
    elif top_features.get("tests_exist") == False:
        recommended["support_agents"].append("unit-test-expert")

    # Task-based recommendations
    if task_type == "feature_development":
        if "frontend" in task_type.lower():
            recommended["primary_agents"].append("frontend-developer")
        elif "backend" in task_type.lower() or "api" in task_type.lower():
            recommended["primary_agents"].append("backend-architect")
        else:
            # Default for general feature development
            recommended["primary_agents"].append("backend-architect")
            recommended["support_agents"].append("frontend-developer")

    # Documentation recommendations
    if top_features.get("docs_exist") == False:
        recommended["support_agents"].append("technical-documentation-writer")

    # Always include simplicity advisor for implementation
    if task_type in ["feature_development", "refactoring", "architecture"]:
        recommended["support_agents"].insert(0, "design-simplicity-advisor")

    return recommended


def simulate_agent_execution(agent_name, task_description, duration_range=(60, 300)):
    """Simulate agent execution."""
    import random
    import time

    print(f"\n  🤖 Executing: {agent_name}")
    print(f"     Task: {task_description}")

    # Simulate work
    duration = random.randint(*duration_range)
    print(f"     Duration: {duration}s")

    # Simulate success/failure
    success_rate = 0.85
    outcome = "success" if random.random() < success_rate else "partial"

    # Simulate quality
    if outcome == "success":
        quality = random.choice([4, 4, 5, 5, 5])
    else:
        quality = random.choice([2, 3, 3])

    return {
        "duration": duration,
        "outcome": outcome,
        "quality": quality,
        "files_modified": [f"src/{agent_name.replace('-', '_')}_output.ts"]
    }


def demo_workflow():
    """Run the complete demo workflow."""
    print_banner("CLAUDE OAK AGENTS - WORKFLOW DEMO")

    # Step 1: Define a sample task
    print("\n📋 TASK: Implement secure OAuth2 authentication with JWT tokens")
    print("   Domain: Backend")
    print("   Scope: Large")
    print("   Risk: High")

    task_description = "Implement secure OAuth2 authentication with JWT tokens"
    task_type = "feature_development"

    # Step 2: Extract state features
    print_banner("STEP 1: STATE ANALYSIS")

    extractor = FeatureExtractor(workspace_dir=PROJECT_ROOT)
    features = extractor.extract_all_features()

    print(f"\n✅ Extracted features from: {PROJECT_ROOT}")
    print(f"   Languages: {', '.join(features['codebase']['languages'][:3])}")
    print(f"   Complexity: {features['codebase']['complexity']}")
    print(f"   Tests: {features['context']['tests_exist']}")

    # Step 3: Rank features
    print_banner("STEP 2: FEATURE RANKING")

    ranked_features = rank_features(features)

    print(f"\n🏆 Top {len(ranked_features)} Features by Importance:")
    for i, feature in enumerate(ranked_features, 1):
        print(f"\n  {i}. {feature['feature']}: {feature['value']}")
        print(f"     Importance: {feature['importance']:.2f}")
        print(f"     Reason: {feature['reason']}")

    # Step 4: Agent selection
    print_banner("STEP 3: AGENT SELECTION")

    recommendation = recommend_agents(ranked_features, task_type)

    print(f"\n🎯 Recommended Strategy:")
    print(f"\n  Primary Agents:")
    for agent in recommendation["primary_agents"]:
        print(f"    • {agent}")

    print(f"\n  Support Agents:")
    for agent in recommendation["support_agents"]:
        print(f"    • {agent}")

    print(f"\n  Workflow: {recommendation['workflow']}")

    # Step 5: Simulate execution with telemetry
    print_banner("STEP 4: AGENT EXECUTION & TELEMETRY")

    # Use temp directory for demo telemetry
    temp_telemetry = Path(tempfile.mkdtemp(prefix="oak_demo_"))
    logger = TelemetryLogger(telemetry_dir=temp_telemetry)

    print(f"\n📝 Telemetry directory: {temp_telemetry}")

    all_agents = recommendation["primary_agents"] + recommendation["support_agents"]
    invocation_ids = []

    for i, agent_name in enumerate(all_agents, 1):
        print(f"\n[{i}/{len(all_agents)}] Invoking: {agent_name}")

        # Log invocation start
        inv_id = logger.log_invocation(
            agent_name=agent_name,
            agent_type="development" if "developer" in agent_name or "architect" in agent_name else "quality",
            task_description=task_description,
            state_features=features
        )
        invocation_ids.append(inv_id)

        # Simulate execution
        result = simulate_agent_execution(agent_name, task_description)

        # Log completion
        logger.update_invocation(
            invocation_id=inv_id,
            duration_seconds=result["duration"],
            outcome_status=result["outcome"],
            files_modified=result["files_modified"],
            tools_used=["Read", "Edit", "Bash", "Write"]
        )

        # Log success metric
        logger.log_success_metric(
            invocation_id=inv_id,
            success=(result["outcome"] == "success"),
            quality_rating=result["quality"],
            feedback_source="automated_tests",
            feedback_notes=f"Demo execution for {agent_name}"
        )

        print(f"     ✅ Logged invocation: {inv_id[:8]}...")

    # Step 6: Analyze performance
    print_banner("STEP 5: PERFORMANCE ANALYSIS")

    analyzer = TelemetryAnalyzer(telemetry_dir=temp_telemetry)
    stats = analyzer.generate_statistics()

    print(f"\n📊 Analysis Results:")
    print(f"   Total Invocations: {stats['total_invocations']}")
    print(f"   Unique Agents: {len(stats['agents'])}")

    print(f"\n🏆 Agent Performance:")
    for agent_name, agent_stats in stats["agents"].items():
        print(f"\n   {agent_name}:")
        print(f"     Success Rate: {agent_stats['success_rate']*100:.0f}%")
        print(f"     Avg Quality: {agent_stats['average_quality']:.1f}/5.0")
        print(f"     Avg Duration: {agent_stats['average_duration_seconds']:.0f}s")

    # Save statistics
    analyzer.save_statistics()

    # Final summary
    print_banner("WORKFLOW COMPLETE")

    print(f"\n✅ Successfully demonstrated OaK workflow:")
    print(f"   1. ✓ State analysis extracted {len(features['codebase']['languages'])} languages")
    print(f"   2. ✓ Ranked {len(ranked_features)} features by importance")
    print(f"   3. ✓ Selected {len(all_agents)} agents")
    print(f"   4. ✓ Executed agents with telemetry logging")
    print(f"   5. ✓ Generated performance statistics")

    print(f"\n📁 Telemetry Data:")
    print(f"   Location: {temp_telemetry}")
    print(f"   Files:")
    print(f"     • agent_invocations.jsonl")
    print(f"     • success_metrics.jsonl")
    print(f"     • performance_stats.json")

    print(f"\n💡 Next Steps:")
    print(f"   • Review telemetry data: cat {temp_telemetry}/*.jsonl")
    print(f"   • View statistics: cat {temp_telemetry}/performance_stats.json | jq")
    print(f"   • Run analyzer: python telemetry/analyzer.py")

    return temp_telemetry


def main():
    """Run the demo workflow."""
    try:
        telemetry_dir = demo_workflow()
        return 0
    except Exception as e:
        print(f"\n❌ DEMO FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
