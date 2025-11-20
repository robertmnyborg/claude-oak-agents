#!/usr/bin/env python3
"""
Automated Variant Mutation and Evolutionary Search

Generates new variant candidates through mutation and evolutionary algorithms.
Discovers novel high-performing variants automatically.
"""

import random
import copy
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

from core.agent_basis import AgentBasisManager, AgentVariant, PromptModification
from core.q_learning import QLearningEngine


class VariantMutator:
    """
    Automatically generates new variant candidates through mutation.
    
    Mutation strategies:
    - Parameter tweaking (temperature, max_tokens)
    - Prompt modification (add/remove sections)
    - Model tier changes (opus ↔ sonnet ↔ haiku)
    - Combination (merge two high-performing variants)
    """
    
    def __init__(
        self,
        agent_basis: Optional[AgentBasisManager] = None,
        q_learning: Optional[QLearningEngine] = None
    ):
        """
        Initialize variant mutator.
        
        Args:
            agent_basis: Agent basis manager
            q_learning: Q-learning engine for fitness evaluation
        """
        self.agent_basis = agent_basis or AgentBasisManager()
        self.q_learning = q_learning or QLearningEngine()
    
    def mutate_variant(
        self,
        agent_name: str,
        base_variant_id: str,
        mutation_type: str,
        strength: float = 0.2
    ) -> Optional[AgentVariant]:
        """
        Generate new variant by mutating base variant.
        
        Args:
            agent_name: Agent name
            base_variant_id: Variant to mutate
            mutation_type: "parameter", "prompt", "model", "combine"
            strength: Mutation strength (0-1)
        
        Returns:
            New mutated variant or None if mutation fails
        """
        # Load base variant
        base = self.agent_basis.load_variant(agent_name, base_variant_id)
        
        if base is None:
            return None
        
        # Create copy for mutation
        mutated = copy.deepcopy(base)
        
        # Generate new variant ID
        mutated.variant_id = f"{base_variant_id}-mut-{mutation_type[:3]}-{random.randint(1000, 9999)}"
        mutated.description = f"Mutated from {base_variant_id} ({mutation_type})"
        
        # Apply mutation
        if mutation_type == "parameter":
            self._mutate_parameters(mutated, strength)
        elif mutation_type == "prompt":
            self._mutate_prompt(mutated, strength)
        elif mutation_type == "model":
            self._mutate_model_tier(mutated)
        elif mutation_type == "combine":
            # Combine mutation requires second parent
            return None
        else:
            return None
        
        # Reset performance metrics (new variant starts fresh)
        mutated.performance_metrics.invocation_count = 0
        mutated.performance_metrics.success_count = 0
        mutated.performance_metrics.avg_duration = 0.0
        mutated.performance_metrics.avg_quality_score = 0.0
        mutated.performance_metrics.avg_reward = 0.0
        mutated.task_type_performance = {}
        
        return mutated
    
    def _mutate_parameters(self, variant: AgentVariant, strength: float) -> None:
        """
        Mutate model parameters (temperature).
        
        Args:
            variant: Variant to mutate (modified in-place)
            strength: Mutation strength (0-1)
        """
        # Mutate temperature
        delta = random.uniform(-strength, strength)
        variant.temperature = max(0.0, min(1.0, variant.temperature + delta))
    
    def _mutate_prompt(self, variant: AgentVariant, strength: float) -> None:
        """
        Mutate prompt modifications.
        
        Args:
            variant: Variant to mutate (modified in-place)
            strength: Mutation strength (0-1)
        """
        if not variant.prompt_modifications:
            # Add new prompt modification
            new_mod = PromptModification(
                section="Specialization",
                operation="append",
                content=f"Focus on {random.choice(['performance', 'reliability', 'simplicity', 'scalability'])}"
            )
            variant.prompt_modifications.append(new_mod)
            return
        
        # With probability based on strength, add/remove/modify prompt mods
        if random.random() < strength:
            if len(variant.prompt_modifications) > 1 and random.random() < 0.3:
                # Remove random modification
                variant.prompt_modifications.pop(random.randint(0, len(variant.prompt_modifications) - 1))
            else:
                # Add new modification
                focus_areas = ['error handling', 'edge cases', 'documentation', 'testing', 'security']
                new_mod = PromptModification(
                    section="Additional Focus",
                    operation="append",
                    content=f"Pay special attention to {random.choice(focus_areas)}"
                )
                variant.prompt_modifications.append(new_mod)
    
    def _mutate_model_tier(self, variant: AgentVariant) -> None:
        """
        Mutate model tier.
        
        Args:
            variant: Variant to mutate (modified in-place)
        """
        tiers = ["fast", "balanced", "premium"]
        current_idx = tiers.index(variant.model_tier) if variant.model_tier in tiers else 1
        
        # Move up or down one tier
        if current_idx == 0:
            new_idx = 1  # fast → balanced
        elif current_idx == 2:
            new_idx = 1  # premium → balanced
        else:
            new_idx = random.choice([0, 2])  # balanced → fast or premium
        
        variant.model_tier = tiers[new_idx]
    
    def combine_variants(
        self,
        agent_name: str,
        variant1_id: str,
        variant2_id: str,
        crossover_rate: float = 0.5
    ) -> Optional[AgentVariant]:
        """
        Combine two variants through crossover.
        
        Args:
            agent_name: Agent name
            variant1_id: First parent variant
            variant2_id: Second parent variant
            crossover_rate: Crossover probability (0-1)
        
        Returns:
            New combined variant or None if combination fails
        """
        # Load parent variants
        parent1 = self.agent_basis.load_variant(agent_name, variant1_id)
        parent2 = self.agent_basis.load_variant(agent_name, variant2_id)
        
        if parent1 is None or parent2 is None:
            return None
        
        # Create offspring
        offspring = copy.deepcopy(parent1)
        offspring.variant_id = f"combined-{variant1_id[:8]}-{variant2_id[:8]}-{random.randint(1000, 9999)}"
        offspring.description = f"Combined from {variant1_id} and {variant2_id}"
        
        # Crossover model tier
        if random.random() < crossover_rate:
            offspring.model_tier = parent2.model_tier
        
        # Crossover temperature (average)
        offspring.temperature = (parent1.temperature + parent2.temperature) / 2
        
        # Crossover prompt modifications (mix from both parents)
        offspring.prompt_modifications = []
        
        all_mods = parent1.prompt_modifications + parent2.prompt_modifications
        for mod in all_mods:
            if random.random() < 0.5:  # 50% chance to include each mod
                offspring.prompt_modifications.append(copy.deepcopy(mod))
        
        # Merge specializations
        offspring.specialization = list(set(parent1.specialization + parent2.specialization))
        
        # Reset performance metrics
        offspring.performance_metrics.invocation_count = 0
        offspring.performance_metrics.success_count = 0
        offspring.performance_metrics.avg_duration = 0.0
        offspring.performance_metrics.avg_quality_score = 0.0
        offspring.performance_metrics.avg_reward = 0.0
        offspring.task_type_performance = {}
        
        return offspring
    
    def evolutionary_search(
        self,
        agent_name: str,
        task_type: str,
        population_size: int = 5,
        generations: int = 10,
        mutation_rate: float = 0.3,
        elite_size: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Evolutionary algorithm to discover optimal variants.
        
        Process:
        1. Initialize population (existing variants + mutations)
        2. Evaluate fitness (Q-values)
        3. Select top performers (elitism)
        4. Generate offspring (mutations + crossover)
        5. Repeat for N generations
        
        Args:
            agent_name: Agent name
            task_type: Task type to optimize for
            population_size: Population size per generation
            generations: Number of generations
            mutation_rate: Probability of mutation (0-1)
            elite_size: Number of elite variants to preserve
        
        Returns:
            List of best variants with fitness scores
        """
        # Initialize population with existing variants
        existing_variants = self.agent_basis.list_variants(agent_name)
        
        if not existing_variants:
            return []
        
        population = existing_variants[:population_size]
        
        evolution_history = []
        
        for gen in range(generations):
            # Evaluate fitness (Q-values for this task type)
            fitness = {}
            
            for variant_id in population:
                q_value = self.q_learning.get_q_value(agent_name, task_type, variant_id)
                visits = self.q_learning.get_visit_count(agent_name, task_type, variant_id)
                
                # Fitness = Q-value (penalize unvisited variants)
                if visits == 0:
                    fitness[variant_id] = 0.0
                else:
                    fitness[variant_id] = q_value
            
            # Sort by fitness
            sorted_population = sorted(population, key=lambda v: fitness.get(v, 0.0), reverse=True)
            
            # Record generation stats
            generation_stats = {
                "generation": gen,
                "best_variant": sorted_population[0],
                "best_fitness": fitness.get(sorted_population[0], 0.0),
                "avg_fitness": sum(fitness.values()) / len(fitness) if fitness else 0.0
            }
            evolution_history.append(generation_stats)
            
            # Select elite variants
            elite = sorted_population[:elite_size]
            
            # Generate offspring
            offspring = []
            
            while len(offspring) < population_size - elite_size:
                # Tournament selection
                parent = self._tournament_selection(sorted_population, fitness, k=3)
                
                # Mutation or crossover
                if random.random() < mutation_rate:
                    # Mutation
                    mutation_type = random.choice(["parameter", "prompt", "model"])
                    mutated = self.mutate_variant(agent_name, parent, mutation_type, strength=0.2)
                    
                    if mutated:
                        # Save mutated variant
                        self.agent_basis.save_variant(mutated)
                        offspring.append(mutated.variant_id)
                else:
                    # Crossover
                    parent2 = self._tournament_selection(sorted_population, fitness, k=3)
                    if parent != parent2:
                        combined = self.combine_variants(agent_name, parent, parent2)
                        if combined:
                            # Save combined variant
                            self.agent_basis.save_variant(combined)
                            offspring.append(combined.variant_id)
            
            # New population = elite + offspring
            population = elite + offspring
        
        # Return best variants from final generation
        final_fitness = {}
        for variant_id in population:
            q_value = self.q_learning.get_q_value(agent_name, task_type, variant_id)
            final_fitness[variant_id] = q_value
        
        best_variants = sorted(
            [{"variant_id": v, "fitness": final_fitness[v]} for v in population],
            key=lambda x: x["fitness"],
            reverse=True
        )
        
        return best_variants[:elite_size]
    
    def _tournament_selection(
        self,
        population: List[str],
        fitness: Dict[str, float],
        k: int = 3
    ) -> str:
        """
        Tournament selection: select best from k random individuals.
        
        Args:
            population: List of variant IDs
            fitness: Fitness scores
            k: Tournament size
        
        Returns:
            Selected variant ID
        """
        tournament = random.sample(population, min(k, len(population)))
        return max(tournament, key=lambda v: fitness.get(v, 0.0))


def main():
    """Example usage of variant mutator."""
    print("=" * 60)
    print("Variant Mutator Demo")
    print("=" * 60)
    print()
    
    # Initialize mutator
    mutator = VariantMutator()
    
    agent_name = "backend-architect"
    existing_variants = mutator.agent_basis.list_variants(agent_name)
    
    if not existing_variants:
        print("No existing variants found. Create some variants first.")
        return
    
    base_variant = existing_variants[0]
    
    print(f"Base variant: {base_variant}")
    print()
    
    # Example 1: Parameter mutation
    print("1. Parameter Mutation")
    print("-" * 60)
    
    mutated_param = mutator.mutate_variant(
        agent_name, base_variant, "parameter", strength=0.2
    )
    
    if mutated_param:
        print(f"Created: {mutated_param.variant_id}")
        print(f"Temperature: {mutated_param.temperature:.2f}")
        print()
    
    # Example 2: Prompt mutation
    print("2. Prompt Mutation")
    print("-" * 60)
    
    mutated_prompt = mutator.mutate_variant(
        agent_name, base_variant, "prompt", strength=0.3
    )
    
    if mutated_prompt:
        print(f"Created: {mutated_prompt.variant_id}")
        print(f"Prompt mods: {len(mutated_prompt.prompt_modifications)}")
        print()
    
    # Example 3: Model tier mutation
    print("3. Model Tier Mutation")
    print("-" * 60)
    
    mutated_model = mutator.mutate_variant(
        agent_name, base_variant, "model"
    )
    
    if mutated_model:
        print(f"Created: {mutated_model.variant_id}")
        print(f"Model tier: {mutated_model.model_tier}")
        print()
    
    # Example 4: Combination
    if len(existing_variants) >= 2:
        print("4. Variant Combination")
        print("-" * 60)
        
        combined = mutator.combine_variants(
            agent_name, existing_variants[0], existing_variants[1]
        )
        
        if combined:
            print(f"Created: {combined.variant_id}")
            print(f"Parents: {existing_variants[0]} + {existing_variants[1]}")
            print(f"Specializations: {combined.specialization}")
            print()
    
    print("=" * 60)


if __name__ == "__main__":
    main()
