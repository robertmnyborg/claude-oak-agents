#!/usr/bin/env python3
"""
Variant Proposer for Continual Reinforcement Learning

Automatically generates proposals for new agent variants based on learning patterns.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from core.agent_basis import AgentBasisManager
from core.q_learning import QLearningEngine
from core.task_classifier import TaskClassifier


class VariantProposer:
    """
    Automatically generates proposals for new agent variants based on learning patterns.
    
    Proposal triggers:
    - Task type has no specialized variant (uses default)
    - Performance gap >20% between best and default variant
    - Consistent underperformance in specific task type
    """
    
    # Proposal thresholds
    PERFORMANCE_GAP_THRESHOLD = 0.20  # 20% gap triggers proposal
    MIN_INVOCATIONS_FOR_PROPOSAL = 50  # Need 50+ invocations to propose
    UNDERPERFORMANCE_THRESHOLD = 0.60  # Q-value < 0.6 is underperforming
    
    def __init__(
        self,
        proposals_file: Optional[Path] = None
    ):
        """
        Initialize variant proposer.
        
        Args:
            proposals_file: Path to variant proposals log
                           (defaults to telemetry/crl/variant_proposals.jsonl)
        """
        self.agent_basis = AgentBasisManager()
        self.q_learning = QLearningEngine()
        self.task_classifier = TaskClassifier()
        
        # Proposals log
        if proposals_file is None:
            project_root = Path(__file__).parent.parent
            proposals_file = project_root / "telemetry" / "crl" / "variant_proposals.jsonl"
        
        self.proposals_file = Path(proposals_file)
        self.proposals_file.parent.mkdir(parents=True, exist_ok=True)
        self.proposals_file.touch(exist_ok=True)
    
    def analyze_and_propose(
        self,
        min_invocations: int = MIN_INVOCATIONS_FOR_PROPOSAL
    ) -> List[Dict[str, Any]]:
        """
        Analyze learning patterns and generate variant proposals.
        
        Args:
            min_invocations: Minimum invocations required before proposing (default: 50)
        
        Returns:
            List of proposals for human review
        """
        proposals = []
        
        # Get all agents
        agents_dir = self.agent_basis.basis_dir
        
        if not agents_dir.exists():
            return []
        
        agent_names = [
            d.name for d in agents_dir.iterdir()
            if d.is_dir() and not d.name.startswith('.')
        ]
        
        # Analyze each agent
        for agent_name in agent_names:
            # Check each task type
            for task_type in self.task_classifier.get_task_types():
                proposal = self._analyze_task_type_performance(
                    agent_name,
                    task_type,
                    min_invocations
                )
                
                if proposal:
                    proposals.append(proposal)
        
        return proposals
    
    def _analyze_task_type_performance(
        self,
        agent_name: str,
        task_type: str,
        min_invocations: int
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze performance for specific (agent, task_type) pair.
        
        Generate proposal if:
        1. No specialized variant exists
        2. Performance significantly below potential
        3. High variance in results suggests need for specialization
        
        Args:
            agent_name: Agent name
            task_type: Task type
            min_invocations: Minimum invocations required
        
        Returns:
            Proposal dictionary if warranted, None otherwise
        """
        # Get all variants for this agent
        variant_ids = self.agent_basis.list_variants(agent_name)
        
        if not variant_ids:
            return None
        
        # Analyze Q-values for each variant
        variant_stats = []
        total_invocations = 0
        
        for variant_id in variant_ids:
            q_value = self.q_learning.get_q_value(agent_name, task_type, variant_id)
            n_visits = self.q_learning.get_visit_count(agent_name, task_type, variant_id)
            
            variant_stats.append({
                "variant_id": variant_id,
                "q_value": q_value,
                "n_visits": n_visits
            })
            
            total_invocations += n_visits
        
        # Check if enough data
        if total_invocations < min_invocations:
            return None
        
        # Sort by Q-value
        variant_stats.sort(key=lambda x: x["q_value"], reverse=True)
        
        best_variant = variant_stats[0]
        default_variant = next(
            (v for v in variant_stats if v["variant_id"] == "default"),
            variant_stats[0]
        )
        
        # Calculate performance gap
        performance_gap = best_variant["q_value"] - default_variant["q_value"]
        
        # Proposal type 1: No specialized variant exists (only default)
        if len(variant_stats) == 1 and variant_stats[0]["variant_id"] == "default":
            if default_variant["q_value"] < self.UNDERPERFORMANCE_THRESHOLD:
                return self._create_proposal(
                    agent_name=agent_name,
                    task_type=task_type,
                    proposal_type="create_specialized_variant",
                    reason=f"No specialized variant exists and default underperforming "
                           f"(Q={default_variant['q_value']:.2f})",
                    supporting_data={
                        "n_invocations": total_invocations,
                        "avg_q_default": default_variant["q_value"],
                        "potential_improvement": self.UNDERPERFORMANCE_THRESHOLD - default_variant["q_value"]
                    }
                )
        
        # Proposal type 2: Large performance gap
        if performance_gap > self.PERFORMANCE_GAP_THRESHOLD:
            return self._create_proposal(
                agent_name=agent_name,
                task_type=task_type,
                proposal_type="promote_variant_to_default",
                reason=f"Large performance gap ({performance_gap:.1%}) between "
                       f"best variant '{best_variant['variant_id']}' and default",
                supporting_data={
                    "n_invocations": total_invocations,
                    "best_variant": best_variant["variant_id"],
                    "best_q_value": best_variant["q_value"],
                    "default_q_value": default_variant["q_value"],
                    "performance_gap": performance_gap
                }
            )
        
        # Proposal type 3: Consistent underperformance
        if (default_variant["q_value"] < self.UNDERPERFORMANCE_THRESHOLD and
            default_variant["n_visits"] >= min_invocations):
            return self._create_proposal(
                agent_name=agent_name,
                task_type=task_type,
                proposal_type="modify_variant_parameters",
                reason=f"Consistent underperformance (Q={default_variant['q_value']:.2f}) "
                       f"over {default_variant['n_visits']} invocations",
                supporting_data={
                    "n_invocations": default_variant["n_visits"],
                    "avg_q_value": default_variant["q_value"],
                    "threshold": self.UNDERPERFORMANCE_THRESHOLD
                }
            )
        
        return None
    
    def _create_proposal(
        self,
        agent_name: str,
        task_type: str,
        proposal_type: str,
        reason: str,
        supporting_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a variant proposal with recommendations.
        
        Args:
            agent_name: Agent name
            task_type: Task type
            proposal_type: Type of proposal (create/modify/promote/retire)
            reason: Human-readable reason
            supporting_data: Supporting metrics and data
        
        Returns:
            Proposal dictionary
        """
        proposal_id = f"prop-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}"
        
        # Generate task-specific recommendations
        recommended_modifications = self._generate_recommendations(task_type)
        
        # Calculate confidence score
        confidence = self._calculate_confidence(proposal_type, supporting_data)
        
        proposal = {
            "proposal_id": proposal_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent_name": agent_name,
            "task_type": task_type,
            "proposal_type": proposal_type,
            "reasoning": reason,
            "confidence": confidence,
            "supporting_data": supporting_data,
            "recommended_modifications": recommended_modifications,
            "status": "pending"
        }
        
        # Log proposal
        with open(self.proposals_file, 'a') as f:
            f.write(json.dumps(proposal) + '\n')
        
        return proposal
    
    def _generate_recommendations(self, task_type: str) -> List[Dict[str, Any]]:
        """
        Generate task-specific recommendations for variant modifications.
        
        Args:
            task_type: Task type
        
        Returns:
            List of recommended modifications
        """
        recommendations = []
        
        # Task-specific recommendations based on common patterns
        if task_type == "security-audit":
            recommendations.extend([
                {
                    "section": "Core Identity",
                    "operation": "append",
                    "content": "Special focus on security vulnerabilities and OWASP Top 10. "
                              "Emphasize secure coding practices and threat modeling."
                },
                {
                    "parameter": "temperature",
                    "value": 0.2,
                    "reason": "Lower temperature for more precise security analysis"
                }
            ])
        
        elif task_type == "performance-opt":
            recommendations.extend([
                {
                    "section": "Core Identity",
                    "operation": "append",
                    "content": "Prioritize performance optimization and efficiency. "
                              "Focus on algorithmic complexity, caching strategies, and resource utilization."
                },
                {
                    "parameter": "temperature",
                    "value": 0.3,
                    "reason": "Lower temperature for systematic performance analysis"
                }
            ])
        
        elif task_type == "api-design":
            recommendations.extend([
                {
                    "section": "Core Identity",
                    "operation": "append",
                    "content": "Focus on RESTful API design principles, OpenAPI specifications, "
                              "and API versioning strategies."
                },
                {
                    "parameter": "temperature",
                    "value": 0.5,
                    "reason": "Balanced temperature for structured API design"
                }
            ])
        
        elif task_type == "database-schema":
            recommendations.extend([
                {
                    "section": "Core Identity",
                    "operation": "append",
                    "content": "Emphasize database normalization, indexing strategies, and migration safety. "
                              "Consider data integrity and query performance."
                },
                {
                    "parameter": "temperature",
                    "value": 0.2,
                    "reason": "Lower temperature for precise schema design"
                }
            ])
        
        else:
            # Generic recommendations
            recommendations.append({
                "section": "Core Identity",
                "operation": "append",
                "content": f"Specialized focus on {task_type} tasks with emphasis on best practices."
            })
        
        return recommendations
    
    def _calculate_confidence(
        self,
        proposal_type: str,
        supporting_data: Dict[str, Any]
    ) -> float:
        """
        Calculate confidence score for a proposal.
        
        Args:
            proposal_type: Type of proposal
            supporting_data: Supporting data and metrics
        
        Returns:
            Confidence score (0.0-1.0)
        """
        n_invocations = supporting_data.get("n_invocations", 0)
        
        # Base confidence on sample size
        if n_invocations < 50:
            base_confidence = 0.5
        elif n_invocations < 100:
            base_confidence = 0.7
        else:
            base_confidence = 0.85
        
        # Adjust based on proposal type
        if proposal_type == "promote_variant_to_default":
            # High confidence if large performance gap
            gap = supporting_data.get("performance_gap", 0)
            if gap > 0.30:
                base_confidence = min(base_confidence + 0.15, 1.0)
        
        elif proposal_type == "create_specialized_variant":
            # Medium confidence for new variants
            base_confidence = min(base_confidence, 0.75)
        
        return round(base_confidence, 2)
    
    def get_proposals(
        self,
        status: Optional[str] = None,
        agent_name: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get variant proposals, optionally filtered.
        
        Args:
            status: Filter by status (pending/approved/rejected) (optional)
            agent_name: Filter by agent name (optional)
            limit: Maximum number of proposals to return (optional)
        
        Returns:
            List of proposal dictionaries (newest first)
        """
        proposals = []
        
        if not self.proposals_file.exists():
            return []
        
        with open(self.proposals_file, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                
                try:
                    proposal = json.loads(line)
                    
                    # Apply filters
                    if status and proposal.get("status") != status:
                        continue
                    if agent_name and proposal.get("agent_name") != agent_name:
                        continue
                    
                    proposals.append(proposal)
                except json.JSONDecodeError:
                    continue
        
        # Sort by timestamp (newest first)
        proposals.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        # Apply limit
        if limit is not None:
            proposals = proposals[:limit]
        
        return proposals


def main():
    """Example usage of variant proposer."""
    print("=" * 60)
    print("Variant Proposer Demo")
    print("=" * 60)
    print()
    
    proposer = VariantProposer()
    
    print("Analyzing agent performance and generating proposals...")
    print()
    
    proposals = proposer.analyze_and_propose(min_invocations=5)  # Lower threshold for demo
    
    if proposals:
        print(f"Generated {len(proposals)} proposal(s):")
        print("=" * 60)
        
        for i, proposal in enumerate(proposals, 1):
            print(f"\nProposal {i}: {proposal['proposal_id']}")
            print(f"Agent: {proposal['agent_name']}")
            print(f"Task Type: {proposal['task_type']}")
            print(f"Type: {proposal['proposal_type']}")
            print(f"Confidence: {proposal['confidence']:.0%}")
            print(f"\nReasoning: {proposal['reasoning']}")
            
            if proposal.get('recommended_modifications'):
                print("\nRecommended Modifications:")
                for mod in proposal['recommended_modifications']:
                    if 'section' in mod:
                        print(f"  - {mod['operation']} to {mod['section']}")
                    elif 'parameter' in mod:
                        print(f"  - Set {mod['parameter']} = {mod['value']}")
                        if 'reason' in mod:
                            print(f"    Reason: {mod['reason']}")
    else:
        print("No proposals generated - all agents performing well!")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
