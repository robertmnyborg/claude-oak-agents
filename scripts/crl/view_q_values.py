#!/usr/bin/env python3
"""
Q-Value Dashboard - Visualize Q-Learning State

Displays Q-values for all agents, variants, and task types.
Shows learning progress and helps identify optimal variants.
"""

import sys
from pathlib import Path
from typing import List, Optional
from collections import defaultdict

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.q_learning import QLearningEngine, QEntry


class QValueDashboard:
    """Dashboard for visualizing Q-learning state."""
    
    def __init__(self, q_engine: Optional[QLearningEngine] = None):
        """
        Initialize dashboard.
        
        Args:
            q_engine: Q-learning engine (creates default if None)
        """
        self.q_engine = q_engine or QLearningEngine()
    
    def display_all(self):
        """Display complete Q-value dashboard."""
        print("=" * 80)
        print("Q-VALUE DASHBOARD")
        print("=" * 80)
        print()
        
        # Get all Q-values
        all_entries = self.q_engine.get_all_q_values()
        
        if not all_entries:
            print("No Q-values found. Run some CRL invocations first.")
            return
        
        # Show summary
        self._display_summary(all_entries)
        print()
        
        # Show by agent
        self._display_by_agent(all_entries)
        print()
        
        # Show convergence
        self._display_convergence(all_entries)
        print()
        
        # Show exploration vs exploitation stats
        self._display_exploration_stats(all_entries)
    
    def _display_summary(self, entries: List[QEntry]):
        """Display summary statistics."""
        print("SUMMARY")
        print("-" * 80)
        
        # Extract unique values
        agents = set()
        task_types = set()
        variants = set()
        
        for entry in entries:
            parts = entry.state_action.split(":")
            if len(parts) == 3:
                agents.add(parts[0])
                task_types.add(parts[1])
                variants.add(parts[2])
        
        # Calculate stats
        total_visits = sum(e.n_visits for e in entries)
        avg_q = sum(e.q_value for e in entries) / len(entries)
        min_q = min(e.q_value for e in entries)
        max_q = max(e.q_value for e in entries)
        
        print(f"Total Q-entries: {len(entries)}")
        print(f"Total visits: {total_visits}")
        print(f"Unique agents: {len(agents)}")
        print(f"Unique task types: {len(task_types)}")
        print(f"Unique variants: {len(variants)}")
        print()
        print(f"Q-value range: [{min_q:.3f}, {max_q:.3f}]")
        print(f"Average Q-value: {avg_q:.3f}")
    
    def _display_by_agent(self, entries: List[QEntry]):
        """Display Q-values grouped by agent."""
        print("Q-VALUES BY AGENT")
        print("-" * 80)
        
        # Group by agent
        by_agent = defaultdict(list)
        for entry in entries:
            parts = entry.state_action.split(":")
            if len(parts) == 3:
                agent = parts[0]
                by_agent[agent].append(entry)
        
        # Display each agent
        for agent in sorted(by_agent.keys()):
            agent_entries = by_agent[agent]
            print(f"\n{agent}:")
            print(f"  Total entries: {len(agent_entries)}")
            print(f"  Total visits: {sum(e.n_visits for e in agent_entries)}")
            
            # Group by task type
            by_task = defaultdict(list)
            for entry in agent_entries:
                parts = entry.state_action.split(":")
                task_type = parts[1]
                by_task[task_type].append(entry)
            
            # Display each task type
            for task_type in sorted(by_task.keys()):
                task_entries = by_task[task_type]
                print(f"\n  Task Type: {task_type}")
                print(f"  {'Variant':<20} {'Q-Value':>10} {'Visits':>10} {'Best':>6}")
                print(f"  {'-'*20} {'-'*10} {'-'*10} {'-'*6}")
                
                # Find best variant
                best_entry = max(task_entries, key=lambda e: e.q_value)
                
                # Display variants sorted by Q-value
                for entry in sorted(task_entries, key=lambda e: e.q_value, reverse=True):
                    parts = entry.state_action.split(":")
                    variant = parts[2]
                    is_best = "✓" if entry == best_entry else ""
                    
                    print(f"  {variant:<20} {entry.q_value:>10.3f} {entry.n_visits:>10} {is_best:>6}")
    
    def _display_convergence(self, entries: List[QEntry]):
        """Display convergence metrics."""
        print("CONVERGENCE METRICS")
        print("-" * 80)
        
        # Find entries with high convergence (recent large updates)
        converging = [e for e in entries if e.convergence_score > 0.01]
        stable = [e for e in entries if e.convergence_score <= 0.01 and e.n_visits >= 5]
        
        print(f"Converging entries (score > 0.01): {len(converging)}")
        print(f"Stable entries (score ≤ 0.01, visits ≥ 5): {len(stable)}")
        print()
        
        if converging:
            print("Top 5 Still Learning (highest convergence scores):")
            print(f"{'State-Action':<50} {'Q-Value':>10} {'Convergence':>12} {'Visits':>8}")
            print(f"{'-'*50} {'-'*10} {'-'*12} {'-'*8}")
            
            for entry in sorted(converging, key=lambda e: e.convergence_score, reverse=True)[:5]:
                print(f"{entry.state_action:<50} {entry.q_value:>10.3f} "
                      f"{entry.convergence_score:>12.3f} {entry.n_visits:>8}")
        
        print()
        
        if stable:
            print("Top 5 Stable (lowest convergence scores with sufficient visits):")
            print(f"{'State-Action':<50} {'Q-Value':>10} {'Convergence':>12} {'Visits':>8}")
            print(f"{'-'*50} {'-'*10} {'-'*12} {'-'*8}")
            
            for entry in sorted(stable, key=lambda e: e.convergence_score)[:5]:
                print(f"{entry.state_action:<50} {entry.q_value:>10.3f} "
                      f"{entry.convergence_score:>12.3f} {entry.n_visits:>8}")
    
    def _display_exploration_stats(self, entries: List[QEntry]):
        """Display exploration vs exploitation statistics."""
        print("EXPLORATION VS EXPLOITATION")
        print("-" * 80)
        
        # Group by visit count to see exploration coverage
        never_visited = [e for e in entries if e.n_visits == 0]
        rarely_visited = [e for e in entries if 0 < e.n_visits < 5]
        well_explored = [e for e in entries if e.n_visits >= 5]
        
        total = len(entries)
        
        print(f"Never visited: {len(never_visited)} ({len(never_visited)/total*100:.1f}%)")
        print(f"Rarely visited (1-4): {len(rarely_visited)} ({len(rarely_visited)/total*100:.1f}%)")
        print(f"Well explored (5+): {len(well_explored)} ({len(well_explored)/total*100:.1f}%)")
        print()
        
        if well_explored:
            print("Most Explored State-Actions:")
            print(f"{'State-Action':<50} {'Q-Value':>10} {'Visits':>8}")
            print(f"{'-'*50} {'-'*10} {'-'*8}")
            
            for entry in sorted(well_explored, key=lambda e: e.n_visits, reverse=True)[:5]:
                print(f"{entry.state_action:<50} {entry.q_value:>10.3f} {entry.n_visits:>8}")


def main():
    """Run Q-value dashboard."""
    import argparse
    
    parser = argparse.ArgumentParser(description="View Q-learning statistics")
    parser.add_argument("--agent", help="Filter by agent name", default=None)
    parser.add_argument("--task-type", help="Filter by task type", default=None)
    parser.add_argument("--qtable", help="Path to Q-table file", default=None)
    
    args = parser.parse_args()
    
    # Initialize Q-learning engine
    if args.qtable:
        q_engine = QLearningEngine(qtable_file=Path(args.qtable))
    else:
        q_engine = QLearningEngine()
    
    # Create dashboard
    dashboard = QValueDashboard(q_engine)
    
    # Display
    dashboard.display_all()
    
    print()
    print("=" * 80)
    print(f"Q-table location: {q_engine.qtable_file}")
    print("=" * 80)


if __name__ == "__main__":
    main()
