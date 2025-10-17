#!/usr/bin/env python3
"""
Measure Token Costs - Analyze telemetry to estimate current token usage and costs.

This script helps you decide whether optimizations like metadata-only prompts are worth implementing.

Usage:
    python3 scripts/measure_token_costs.py
    python3 scripts/measure_token_costs.py --period=30  # Last 30 days
    python3 scripts/measure_token_costs.py --show-agents  # Break down by agent
"""

import argparse
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from collections import defaultdict


# Token cost estimates (as of 2025-01)
TOKEN_COSTS = {
    "claude-sonnet-4": {
        "input": 3.00 / 1_000_000,    # $3 per million input tokens
        "output": 15.00 / 1_000_000,  # $15 per million output tokens
    },
    "claude-haiku": {
        "input": 0.25 / 1_000_000,    # $0.25 per million input tokens
        "output": 1.25 / 1_000_000,   # $1.25 per million output tokens
    },
}


def load_telemetry(telemetry_dir: Path, days: int = 30) -> List[dict]:
    """Load telemetry data from the last N days."""
    invocations_file = telemetry_dir / "agent_invocations.jsonl"

    if not invocations_file.exists():
        print(f"⚠️  No telemetry data found at {invocations_file}")
        print("   Agent invocations will be logged automatically as you use the system.")
        return []

    cutoff_date = datetime.now() - timedelta(days=days)
    invocations = []

    with open(invocations_file, 'r') as f:
        for line in f:
            if line.strip():
                try:
                    record = json.loads(line)
                    record_date = datetime.fromisoformat(record.get("timestamp", ""))

                    if record_date >= cutoff_date:
                        invocations.append(record)
                except (json.JSONDecodeError, ValueError):
                    continue

    return invocations


def estimate_system_prompt_tokens(use_metadata: bool = False) -> int:
    """Estimate system prompt token count."""
    # These are estimates based on actual measurements
    if use_metadata:
        return 2_000  # ~6KB metadata-only prompt
    else:
        return 22_000  # ~87KB full agent definitions


def estimate_agent_tokens(agent_name: str, task_description: str) -> Tuple[int, int]:
    """
    Estimate input and output tokens for an agent invocation.

    This is a rough estimate. Actual values vary based on task complexity.

    Returns: (input_tokens, output_tokens)
    """
    # Base estimates (very rough)
    input_base = 500  # Task description + context
    output_base = 1000  # Agent response

    # Adjust based on agent type (some agents produce more output)
    verbose_agents = {
        "security-auditor": 2.0,
        "code-reviewer": 1.5,
        "technical-documentation-writer": 2.5,
        "systems-architect": 1.8,
    }

    multiplier = verbose_agents.get(agent_name, 1.0)

    return (
        int(input_base),
        int(output_base * multiplier)
    )


def calculate_costs(invocations: List[dict], use_metadata: bool = False) -> Dict:
    """Calculate estimated costs from invocations."""
    system_prompt_tokens = estimate_system_prompt_tokens(use_metadata)

    total_invocations = len(invocations)
    total_input_tokens = 0
    total_output_tokens = 0

    agent_stats = defaultdict(lambda: {"count": 0, "input": 0, "output": 0})

    for inv in invocations:
        agent_name = inv.get("agent", "unknown")
        task_desc = inv.get("task", "")

        # Each invocation includes system prompt
        input_tokens = system_prompt_tokens

        # Add estimated task/response tokens
        task_input, task_output = estimate_agent_tokens(agent_name, task_desc)
        input_tokens += task_input
        output_tokens = task_output

        total_input_tokens += input_tokens
        total_output_tokens += output_tokens

        agent_stats[agent_name]["count"] += 1
        agent_stats[agent_name]["input"] += input_tokens
        agent_stats[agent_name]["output"] += output_tokens

    # Calculate costs (using Sonnet pricing as default)
    pricing = TOKEN_COSTS["claude-sonnet-4"]
    input_cost = total_input_tokens * pricing["input"]
    output_cost = total_output_tokens * pricing["output"]
    total_cost = input_cost + output_cost

    return {
        "total_invocations": total_invocations,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
        "agent_stats": dict(agent_stats),
        "system_prompt_tokens": system_prompt_tokens,
    }


def format_money(amount: float) -> str:
    """Format money with appropriate precision."""
    if amount < 0.01:
        return f"${amount:.4f}"
    elif amount < 1.00:
        return f"${amount:.3f}"
    else:
        return f"${amount:.2f}"


def print_report(current: Dict, optimized: Dict, period_days: int, show_agents: bool = False):
    """Print cost analysis report."""
    print("=" * 80)
    print("📊 OaK Agents Token Cost Analysis")
    print("=" * 80)
    print()

    print(f"📅 Period: Last {period_days} days")
    print(f"🔢 Total Invocations: {current['total_invocations']}")
    print()

    print("-" * 80)
    print("CURRENT CONFIGURATION (Full Agent Definitions)")
    print("-" * 80)
    print(f"System Prompt Tokens: {current['system_prompt_tokens']:,} tokens per invocation")
    print(f"Total Input Tokens:   {current['total_input_tokens']:,}")
    print(f"Total Output Tokens:  {current['total_output_tokens']:,}")
    print()
    print(f"💰 Estimated Costs (Claude Sonnet 4):")
    print(f"   Input Cost:  {format_money(current['input_cost'])}")
    print(f"   Output Cost: {format_money(current['output_cost'])}")
    print(f"   Total Cost:  {format_money(current['total_cost'])}")
    print()

    print("-" * 80)
    print("OPTIMIZED CONFIGURATION (Metadata-Only Prompts)")
    print("-" * 80)
    print(f"System Prompt Tokens: {optimized['system_prompt_tokens']:,} tokens per invocation")
    print(f"Total Input Tokens:   {optimized['total_input_tokens']:,}")
    print(f"Total Output Tokens:  {optimized['total_output_tokens']:,}")
    print()
    print(f"💰 Estimated Costs (Claude Sonnet 4):")
    print(f"   Input Cost:  {format_money(optimized['input_cost'])}")
    print(f"   Output Cost: {format_money(optimized['output_cost'])}")
    print(f"   Total Cost:  {format_money(optimized['total_cost'])}")
    print()

    # Calculate savings
    token_savings = current['total_input_tokens'] - optimized['total_input_tokens']
    cost_savings = current['total_cost'] - optimized['total_cost']
    savings_pct = (cost_savings / current['total_cost'] * 100) if current['total_cost'] > 0 else 0

    print("-" * 80)
    print("💡 POTENTIAL SAVINGS")
    print("-" * 80)
    print(f"Token Savings:  {token_savings:,} tokens ({savings_pct:.1f}%)")
    print(f"Cost Savings:   {format_money(cost_savings)} ({savings_pct:.1f}%)")
    print()

    # Monthly projection
    if period_days > 0:
        monthly_multiplier = 30 / period_days
        monthly_current = current['total_cost'] * monthly_multiplier
        monthly_optimized = optimized['total_cost'] * monthly_multiplier
        monthly_savings = cost_savings * monthly_multiplier

        print(f"📈 Monthly Projection ({period_days}-day average):")
        print(f"   Current:   {format_money(monthly_current)}/month")
        print(f"   Optimized: {format_money(monthly_optimized)}/month")
        print(f"   Savings:   {format_money(monthly_savings)}/month")
        print()

    # Recommendation
    print("-" * 80)
    print("🎯 RECOMMENDATION")
    print("-" * 80)

    if current['total_invocations'] == 0:
        print("⏸️  No data yet - keep using the system and re-run this script later")
    elif monthly_savings < 1.00:
        print("✅ CURRENT CONFIG IS FINE")
        print(f"   Savings would be {format_money(monthly_savings)}/month - not worth optimizing")
        print("   Keep using current configuration")
    elif monthly_savings < 10.00:
        print("⚖️  MARGINAL BENEFIT")
        print(f"   Savings: {format_money(monthly_savings)}/month")
        print("   Consider enabling if you plan to add many more agents")
        print("   Enable with: ./scripts/enable_metadata_prompts.sh")
    else:
        print("✅ ENABLE METADATA-ONLY PROMPTS")
        print(f"   Savings: {format_money(monthly_savings)}/month")
        print("   Significant cost reduction with no downside")
        print()
        print("   Enable now:")
        print("   cd ~/Projects/claude-oak-agents")
        print("   ./scripts/enable_metadata_prompts.sh")
    print()

    # Agent breakdown
    if show_agents and current['agent_stats']:
        print("-" * 80)
        print("📊 COST BREAKDOWN BY AGENT")
        print("-" * 80)

        # Sort agents by total cost
        agent_costs = []
        for agent_name, stats in current['agent_stats'].items():
            agent_input_cost = stats['input'] * TOKEN_COSTS["claude-sonnet-4"]["input"]
            agent_output_cost = stats['output'] * TOKEN_COSTS["claude-sonnet-4"]["output"]
            agent_total = agent_input_cost + agent_output_cost
            agent_costs.append((agent_name, stats['count'], agent_total))

        agent_costs.sort(key=lambda x: x[2], reverse=True)

        print(f"{'Agent':<35} {'Invocations':>12} {'Est. Cost':>12}")
        print("-" * 80)

        for agent_name, count, cost in agent_costs[:10]:  # Top 10
            print(f"{agent_name:<35} {count:>12} {format_money(cost):>12}")

        print()


def main():
    parser = argparse.ArgumentParser(
        description="Measure token costs and evaluate optimization opportunities"
    )
    parser.add_argument(
        "--period",
        type=int,
        default=30,
        help="Number of days to analyze (default: 30)"
    )
    parser.add_argument(
        "--show-agents",
        action="store_true",
        help="Show cost breakdown by agent"
    )
    parser.add_argument(
        "--telemetry-dir",
        type=Path,
        default=Path.home() / "Projects" / "claude-oak-agents" / "telemetry",
        help="Path to telemetry directory"
    )

    args = parser.parse_args()

    # Load telemetry
    invocations = load_telemetry(args.telemetry_dir, args.period)

    if not invocations:
        print()
        print("ℹ️  No telemetry data available yet.")
        print()
        print("   Telemetry will be collected automatically as you use agents.")
        print("   Re-run this script after using the system for a few days.")
        print()
        return

    # Calculate costs with current and optimized configurations
    current_costs = calculate_costs(invocations, use_metadata=False)
    optimized_costs = calculate_costs(invocations, use_metadata=True)

    # Print report
    print_report(current_costs, optimized_costs, args.period, args.show_agents)


if __name__ == "__main__":
    main()
