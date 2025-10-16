#!/usr/bin/env python3
"""
State Analysis Test Script

Tests the state-analysis feature extraction on the current project.
"""

import sys
import json
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from state_analysis.feature_extractor import FeatureExtractor


def analyze_current_project():
    """Analyze the claude-oak-agents project itself."""
    print("="*70)
    print("ANALYZING CLAUDE OAK AGENTS PROJECT")
    print("="*70)

    extractor = FeatureExtractor(workspace_dir=PROJECT_ROOT)

    print("\n🔍 Extracting features...")
    features = extractor.extract_all_features()

    print("\n" + "="*70)
    print("CODEBASE FEATURES")
    print("="*70)

    codebase = features["codebase"]
    print(f"\n📝 Languages: {', '.join(codebase['languages']) if codebase['languages'] else 'None detected'}")
    print(f"🔧 Frameworks: {', '.join(codebase['frameworks']) if codebase['frameworks'] else 'None detected'}")
    print(f"📊 Lines of Code: {codebase['loc']:,}")
    print(f"📁 File Count: {codebase['file_count']}")
    print(f"⚙️  Complexity: {codebase['complexity']}")
    print(f"🏗️  Architecture: {codebase['architecture']}")

    print("\n" + "="*70)
    print("CONTEXT FEATURES")
    print("="*70)

    context = features["context"]
    print(f"\n✅ Tests Exist: {context['tests_exist']}")
    print(f"📖 Docs Exist: {context['docs_exist']}")
    print(f"🔀 Git Clean: {context['git_clean']}")
    print(f"📦 Dependencies Outdated: {context['dependencies_outdated']}")
    print(f"🏗️  Build Status: {context['build_status']}")

    # Detailed breakdown
    print("\n" + "="*70)
    print("DETAILED ANALYSIS")
    print("="*70)

    # Language distribution
    print("\n📊 Language Distribution:")
    lang_files = {}
    for lang in codebase['languages']:
        # Count files for each language
        ext_map = {
            'Python': ['.py'],
            'JavaScript': ['.js', '.jsx'],
            'TypeScript': ['.ts', '.tsx'],
            'Markdown': ['.md']
        }
        if lang in ext_map:
            count = sum(1 for ext in ext_map[lang]
                       for _ in PROJECT_ROOT.rglob(f"*{ext}"))
            lang_files[lang] = count
            print(f"  {lang}: {count} files")

    # Framework detection
    if codebase['frameworks']:
        print("\n🔧 Detected Frameworks:")
        for fw in codebase['frameworks']:
            print(f"  • {fw}")

    # Architecture insights
    print(f"\n🏗️  Architecture Pattern: {codebase['architecture']}")
    if codebase['architecture'] == 'monolithic':
        print("  → Single unified codebase")
    elif codebase['architecture'] == 'microservices':
        print("  → Multiple independent services")

    # Complexity insights
    print(f"\n⚙️  Complexity Level: {codebase['complexity']}")
    complexity_desc = {
        'trivial': 'Very small project (<1K LOC)',
        'low': 'Small project (1K-5K LOC)',
        'medium': 'Medium project (5K-20K LOC)',
        'high': 'Large project (20K-100K LOC)',
        'very_high': 'Very large project (>100K LOC)'
    }
    print(f"  → {complexity_desc.get(codebase['complexity'], 'Unknown')}")

    # Save full output
    output_file = PROJECT_ROOT / "state_analysis_output.json"
    with open(output_file, "w") as f:
        json.dump(features, f, indent=2)

    print(f"\n💾 Full analysis saved to: {output_file}")

    return features


def provide_recommendations(features):
    """Provide recommendations based on state analysis."""
    print("\n" + "="*70)
    print("RECOMMENDATIONS")
    print("="*70)

    recommendations = []

    codebase = features["codebase"]
    context = features["context"]

    # Test recommendations
    if not context["tests_exist"]:
        recommendations.append("⚠️  No tests detected - recommend unit-test-expert agent")
    elif context["tests_passing"] == False:
        recommendations.append("⚠️  Tests failing - recommend debug-specialist agent")

    # Documentation recommendations
    if not context["docs_exist"]:
        recommendations.append("📝 No documentation - recommend technical-documentation-writer")

    # Complexity recommendations
    if codebase["complexity"] in ["high", "very_high"]:
        recommendations.append("🏗️  High complexity - recommend systems-architect for review")

    # Git recommendations
    if context["git_clean"] == False:
        recommendations.append("🔀 Uncommitted changes - recommend git-workflow-manager")

    # Language-specific recommendations
    if "Python" in codebase["languages"]:
        recommendations.append("🐍 Python detected - ml-engineer available for ML tasks")

    if "TypeScript" in codebase["languages"] or "JavaScript" in codebase["languages"]:
        recommendations.append("⚛️  JS/TS detected - frontend-developer for UI work")

    if recommendations:
        print()
        for rec in recommendations:
            print(f"  {rec}")
    else:
        print("\n  ✅ No specific recommendations - project looks good!")


def main():
    """Run state analysis test."""
    try:
        features = analyze_current_project()
        provide_recommendations(features)

        print("\n" + "="*70)
        print("✅ STATE ANALYSIS COMPLETE")
        print("="*70)

        return 0

    except Exception as e:
        print(f"\n❌ ANALYSIS FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
