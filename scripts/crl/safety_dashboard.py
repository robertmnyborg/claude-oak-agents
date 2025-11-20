#!/usr/bin/env python3
"""
Safety Dashboard for Continual Reinforcement Learning

Displays real-time safety metrics and system health.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.safety_monitor import SafetyMonitor
from core.rollback_manager import RollbackManager
from core.variant_proposer import VariantProposer
from core.q_learning import QLearningEngine
from core.agent_basis import AgentBasisManager


class SafetyDashboard:
    """
    Real-time safety dashboard for CRL system monitoring.
    
    Displays:
    - Auto-applied variants (last 30 days)
    - Human approval queue
    - Rollback events
    - Performance degradation alerts
    - Variant proposal queue
    """
    
    def __init__(self):
        """Initialize dashboard with CRL components."""
        self.safety_monitor = SafetyMonitor()
        self.rollback_manager = RollbackManager()
        self.variant_proposer = VariantProposer()
        self.q_learning = QLearningEngine()
        self.agent_basis = AgentBasisManager()
    
    def display(self) -> None:
        """Display complete safety dashboard."""
        print("\n" + "=" * 80)
        print("CRL SAFETY DASHBOARD")
        print("=" * 80)
        print(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print("=" * 80)
        
        # Section 1: System Health Overview
        self._display_system_health()
        
        # Section 2: Recent Rollbacks
        self._display_recent_rollbacks()
        
        # Section 3: Pending Proposals
        self._display_pending_proposals()
        
        # Section 4: High-Confidence Variants
        self._display_high_confidence_variants()
        
        # Section 5: Degradation Alerts
        self._display_degradation_alerts()
        
        print("\n" + "=" * 80)
        print("END OF DASHBOARD")
        print("=" * 80 + "\n")
    
    def _display_system_health(self) -> None:
        """Display overall system health metrics."""
        print("\n" + "-" * 80)
        print("SYSTEM HEALTH OVERVIEW")
        print("-" * 80)
        
        # Count Q-table entries
        q_entries = self.q_learning.get_all_q_values()
        total_entries = len(q_entries)
        
        # Count agents with variants
        agents_dir = self.agent_basis.basis_dir
        if agents_dir.exists():
            agent_names = [
                d.name for d in agents_dir.iterdir()
                if d.is_dir() and not d.name.startswith('.')
            ]
            total_agents = len(agent_names)
        else:
            total_agents = 0
        
        # Count recent rollbacks (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_rollbacks = [
            r for r in self.rollback_manager.get_rollback_history()
            if datetime.fromisoformat(r['timestamp'].rstrip('Z')) > thirty_days_ago
        ]
        
        # Count pending proposals
        pending_proposals = self.variant_proposer.get_proposals(status="pending")
        
        print(f"Total Q-table Entries: {total_entries}")
        print(f"Active Agents with Variants: {total_agents}")
        print(f"Rollbacks (Last 30 Days): {len(recent_rollbacks)}")
        print(f"Pending Proposals: {len(pending_proposals)}")
        
        # Health status
        if len(recent_rollbacks) == 0 and len(pending_proposals) < 5:
            status = "HEALTHY"
            color = "✓"
        elif len(recent_rollbacks) < 3:
            status = "STABLE"
            color = "○"
        else:
            status = "ATTENTION NEEDED"
            color = "!"
        
        print(f"\nSystem Status: {color} {status}")
    
    def _display_recent_rollbacks(self) -> None:
        """Display recent rollback events."""
        print("\n" + "-" * 80)
        print("RECENT ROLLBACKS (Last 10)")
        print("-" * 80)
        
        rollbacks = self.rollback_manager.get_rollback_history(limit=10)
        
        if not rollbacks:
            print("No rollbacks recorded")
            return
        
        for rollback in rollbacks:
            timestamp = datetime.fromisoformat(rollback['timestamp'].rstrip('Z'))
            print(f"\n{rollback['rollback_id']} - {timestamp.strftime('%Y-%m-%d %H:%M')}")
            print(f"  Agent: {rollback['agent_name']}")
            print(f"  Task Type: {rollback['task_type']}")
            print(f"  Rollback: {rollback['from_variant']} → {rollback['to_variant']}")
            print(f"  Reason: {rollback['reason']}")
    
    def _display_pending_proposals(self) -> None:
        """Display pending variant proposals."""
        print("\n" + "-" * 80)
        print("PENDING PROPOSALS")
        print("-" * 80)
        
        proposals = self.variant_proposer.get_proposals(status="pending")
        
        if not proposals:
            print("No pending proposals")
            return
        
        # Sort by confidence (highest first)
        proposals.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        for proposal in proposals[:10]:  # Show top 10
            print(f"\n{proposal['proposal_id']} - Confidence: {proposal['confidence']:.0%}")
            print(f"  Agent: {proposal['agent_name']}")
            print(f"  Task Type: {proposal['task_type']}")
            print(f"  Type: {proposal['proposal_type']}")
            print(f"  Reasoning: {proposal['reasoning']}")
    
    def _display_high_confidence_variants(self) -> None:
        """Display variants ready for auto-apply."""
        print("\n" + "-" * 80)
        print("HIGH-CONFIDENCE VARIANTS (Auto-Apply Ready)")
        print("-" * 80)
        
        # Get all Q-table entries
        q_entries = self.q_learning.get_all_q_values()
        
        # Filter for high confidence (Q > 0.9, visits >= 10)
        high_confidence = [
            entry for entry in q_entries
            if entry.q_value >= 0.9 and entry.n_visits >= 10
        ]
        
        if not high_confidence:
            print("No high-confidence variants ready for auto-apply")
            return
        
        # Sort by Q-value (highest first)
        high_confidence.sort(key=lambda x: x.q_value, reverse=True)
        
        for entry in high_confidence[:10]:  # Show top 10
            # Parse state_action key
            parts = entry.state_action.split(':')
            if len(parts) == 3:
                agent_name, task_type, variant_id = parts
                
                print(f"\n{agent_name} / {task_type} / {variant_id}")
                print(f"  Q-value: {entry.q_value:.3f}")
                print(f"  Visits: {entry.n_visits}")
                print(f"  Last Updated: {entry.last_updated}")
                
                # Check if should auto-apply
                decision, reasoning = self.safety_monitor.should_auto_apply_variant(
                    agent_name, task_type, variant_id, entry.q_value, entry.n_visits
                )
                print(f"  Decision: {decision.upper()}")
    
    def _display_degradation_alerts(self) -> None:
        """Display active degradation alerts."""
        print("\n" + "-" * 80)
        print("DEGRADATION ALERTS")
        print("-" * 80)
        
        # Get all Q-table entries
        q_entries = self.q_learning.get_all_q_values()
        
        # Check each variant for degradation
        alerts = []
        
        for entry in q_entries:
            # Parse state_action key
            parts = entry.state_action.split(':')
            if len(parts) == 3:
                agent_name, task_type, variant_id = parts
                
                # Check for degradation
                degraded, metrics = self.safety_monitor.check_performance_degradation(
                    agent_name, task_type, variant_id
                )
                
                if degraded:
                    alerts.append({
                        "agent_name": agent_name,
                        "task_type": task_type,
                        "variant_id": variant_id,
                        "metrics": metrics
                    })
        
        if not alerts:
            print("No active degradation alerts - system performing well!")
            return
        
        for alert in alerts:
            print(f"\n⚠️  ALERT: {alert['agent_name']} / {alert['task_type']} / {alert['variant_id']}")
            
            metrics = alert['metrics']
            
            if metrics.get('degraded_success'):
                print(f"  Success Rate Drop: {metrics['baseline_success_rate']:.1%} → "
                      f"{metrics['recent_success_rate']:.1%} "
                      f"({metrics['success_drop_pct']:.1%} drop)")
            
            if metrics.get('degraded_reward'):
                print(f"  Reward Drop: {metrics['baseline_avg_reward']:.2f} → "
                      f"{metrics['recent_avg_reward']:.2f} "
                      f"({metrics['reward_drop_pct']:.1%} drop)")
            
            if metrics.get('degraded_error'):
                print(f"  Error Rate Increase: {metrics['baseline_error_rate']:.1%} → "
                      f"{metrics['recent_error_rate']:.1%} "
                      f"({metrics['error_increase_pct']:.1%} increase)")
            
            print(f"  Sample Size: {metrics['sample_size']} invocations")
            print(f"  → RECOMMENDATION: Trigger rollback")


def main():
    """Run the safety dashboard."""
    dashboard = SafetyDashboard()
    dashboard.display()


if __name__ == "__main__":
    main()
