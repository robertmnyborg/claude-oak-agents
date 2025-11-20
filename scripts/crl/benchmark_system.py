#!/usr/bin/env python3
"""
Benchmark CRL system performance.

Measures:
- Selection time per algorithm
- Memory usage
- Throughput (requests/second)
- Learning convergence speed
"""

import time
import sys
import random
from pathlib import Path
from typing import List, Dict, Any
import statistics

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from core.q_learning import QLearningEngine
from core.bandits import UCB1, ThompsonSampling
from core.contextual_bandits import LinUCB
from core.task_classifier import TaskClassifier
from core.domain_router import DomainRouter


def benchmark_selection_algorithms(iterations: int = 1000) -> Dict[str, Any]:
    """
    Compare selection time: Q-learning vs UCB1 vs Thompson vs LinUCB.
    
    Args:
        iterations: Number of selections to perform
    
    Returns:
        Benchmark results dictionary
    """
    print("=" * 80)
    print(f"Benchmarking Selection Algorithms ({iterations} iterations)")
    print("=" * 80)
    print()
    
    # Setup
    agent_name = "backend-architect"
    task_type = "api-design"
    variants = ["default", "api-optimized", "database-focused"]
    
    results = {}
    
    # Benchmark Q-learning
    print("Testing Q-learning...")
    q_engine = QLearningEngine()
    start = time.time()
    for _ in range(iterations):
        q_engine.select_variant(agent_name, task_type, variants)
    q_time = time.time() - start
    results['q_learning'] = {
        'total_time': q_time,
        'avg_time_ms': (q_time / iterations) * 1000,
        'throughput': iterations / q_time
    }
    print(f"  Time: {q_time:.3f}s | Avg: {results['q_learning']['avg_time_ms']:.2f}ms")
    
    # Benchmark UCB1
    print("Testing UCB1...")
    ucb1 = UCB1()
    start = time.time()
    for _ in range(iterations):
        ucb1.select_variant(agent_name, task_type, variants)
    ucb1_time = time.time() - start
    results['ucb1'] = {
        'total_time': ucb1_time,
        'avg_time_ms': (ucb1_time / iterations) * 1000,
        'throughput': iterations / ucb1_time
    }
    print(f"  Time: {ucb1_time:.3f}s | Avg: {results['ucb1']['avg_time_ms']:.2f}ms")
    
    # Benchmark Thompson Sampling
    print("Testing Thompson Sampling...")
    thompson = ThompsonSampling()
    start = time.time()
    for _ in range(iterations):
        thompson.select_variant(agent_name, task_type, variants)
    thompson_time = time.time() - start
    results['thompson'] = {
        'total_time': thompson_time,
        'avg_time_ms': (thompson_time / iterations) * 1000,
        'throughput': iterations / thompson_time
    }
    print(f"  Time: {thompson_time:.3f}s | Avg: {results['thompson']['avg_time_ms']:.2f}ms")
    
    # Benchmark LinUCB
    print("Testing LinUCB...")
    linucb = LinUCB(context_dim=10)
    context = [random.random() for _ in range(10)]
    start = time.time()
    for _ in range(iterations):
        linucb.select_variant(agent_name, task_type, variants, context)
    linucb_time = time.time() - start
    results['linucb'] = {
        'total_time': linucb_time,
        'avg_time_ms': (linucb_time / iterations) * 1000,
        'throughput': iterations / linucb_time
    }
    print(f"  Time: {linucb_time:.3f}s | Avg: {results['linucb']['avg_time_ms']:.2f}ms")
    
    print()
    print("Summary:")
    print("-" * 80)
    for algo, stats in results.items():
        print(f"{algo:20s}: {stats['avg_time_ms']:6.2f}ms | "
              f"{stats['throughput']:8.1f} req/s")
    
    return results


def benchmark_task_classification(iterations: int = 100) -> Dict[str, Any]:
    """
    Measure task classification performance.
    
    Args:
        iterations: Number of classifications to perform
    
    Returns:
        Benchmark results
    """
    print()
    print("=" * 80)
    print(f"Benchmarking Task Classification ({iterations} iterations)")
    print("=" * 80)
    print()
    
    classifier = TaskClassifier()
    
    test_requests = [
        "Create REST API endpoints for user management",
        "Fix database migration for analytics table",
        "Review authentication security vulnerabilities",
        "Optimize slow API query performance",
        "Build React dashboard component"
    ]
    
    times = []
    
    for i in range(iterations):
        request = random.choice(test_requests)
        files = ["src/example.ts"]
        
        start = time.time()
        task_type, confidence, scores = classifier.classify_with_confidence(request, files)
        duration = time.time() - start
        
        times.append(duration)
    
    avg_time = statistics.mean(times)
    median_time = statistics.median(times)
    p95_time = sorted(times)[int(len(times) * 0.95)]
    
    print(f"Average time: {avg_time * 1000:.2f}ms")
    print(f"Median time: {median_time * 1000:.2f}ms")
    print(f"P95 time: {p95_time * 1000:.2f}ms")
    print(f"Throughput: {iterations / sum(times):.1f} classifications/s")
    
    return {
        'avg_time_ms': avg_time * 1000,
        'median_time_ms': median_time * 1000,
        'p95_time_ms': p95_time * 1000,
        'throughput': iterations / sum(times)
    }


def benchmark_domain_routing(iterations: int = 100) -> Dict[str, Any]:
    """
    Measure domain routing performance.
    
    Args:
        iterations: Number of routing operations
    
    Returns:
        Benchmark results
    """
    print()
    print("=" * 80)
    print(f"Benchmarking Domain Routing ({iterations} iterations)")
    print("=" * 80)
    print()
    
    # Test with CRL enabled
    router_crl = DomainRouter(crl_enabled=True)
    
    test_cases = [
        ("Create React component", ["src/components/Button.tsx"]),
        ("Deploy Lambda function", ["infrastructure/lambda-stack.ts"]),
        ("Fix SQL injection vulnerability", ["src/auth/db.ts"]),
        ("Optimize database queries", ["src/models/user.ts"]),
        ("Create API endpoints", ["src/routes/api.ts"])
    ]
    
    times_crl = []
    times_no_crl = []
    
    # Benchmark with CRL
    print("Testing with CRL enabled...")
    for i in range(iterations):
        request, files = random.choice(test_cases)
        
        start = time.time()
        routing = router_crl.route_request(request, files)
        duration = time.time() - start
        
        times_crl.append(duration)
    
    # Benchmark without CRL
    print("Testing with CRL disabled...")
    router_no_crl = DomainRouter(crl_enabled=False)
    for i in range(iterations):
        request, files = random.choice(test_cases)
        
        start = time.time()
        routing = router_no_crl.route_request(request, files)
        duration = time.time() - start
        
        times_no_crl.append(duration)
    
    print()
    print("CRL Enabled:")
    print(f"  Average: {statistics.mean(times_crl) * 1000:.2f}ms")
    print(f"  P95: {sorted(times_crl)[int(len(times_crl) * 0.95)] * 1000:.2f}ms")
    
    print()
    print("CRL Disabled:")
    print(f"  Average: {statistics.mean(times_no_crl) * 1000:.2f}ms")
    print(f"  P95: {sorted(times_no_crl)[int(len(times_no_crl) * 0.95)] * 1000:.2f}ms")
    
    overhead = (statistics.mean(times_crl) - statistics.mean(times_no_crl)) * 1000
    print()
    print(f"CRL Overhead: {overhead:.2f}ms")
    
    return {
        'crl_enabled_avg_ms': statistics.mean(times_crl) * 1000,
        'crl_disabled_avg_ms': statistics.mean(times_no_crl) * 1000,
        'overhead_ms': overhead
    }


def benchmark_memory_usage():
    """
    Measure memory footprint of CRL components.
    
    Note: Requires psutil package for accurate memory measurement.
    """
    print()
    print("=" * 80)
    print("Memory Usage Benchmark")
    print("=" * 80)
    print()
    
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        # Baseline memory
        baseline = process.memory_info().rss / 1024 / 1024
        print(f"Baseline memory: {baseline:.2f} MB")
        
        # Load Q-learning engine
        q_engine = QLearningEngine()
        q_memory = process.memory_info().rss / 1024 / 1024
        print(f"After Q-learning: {q_memory:.2f} MB (+{q_memory - baseline:.2f} MB)")
        
        # Load task classifier
        classifier = TaskClassifier()
        classifier_memory = process.memory_info().rss / 1024 / 1024
        print(f"After classifier: {classifier_memory:.2f} MB (+{classifier_memory - q_memory:.2f} MB)")
        
        # Load domain router with CRL
        router = DomainRouter(crl_enabled=True)
        router_memory = process.memory_info().rss / 1024 / 1024
        print(f"After router: {router_memory:.2f} MB (+{router_memory - classifier_memory:.2f} MB)")
        
        print()
        print(f"Total CRL overhead: {router_memory - baseline:.2f} MB")
        
    except ImportError:
        print("psutil not installed - skipping memory benchmark")
        print("Install with: pip install psutil")


def main():
    """Run all benchmarks."""
    print()
    print("CRL SYSTEM PERFORMANCE BENCHMARKS")
    print()
    
    # Run benchmarks
    selection_results = benchmark_selection_algorithms(iterations=1000)
    classification_results = benchmark_task_classification(iterations=100)
    routing_results = benchmark_domain_routing(iterations=100)
    benchmark_memory_usage()
    
    # Summary
    print()
    print("=" * 80)
    print("BENCHMARK SUMMARY")
    print("=" * 80)
    print()
    print("Target: CRL overhead < 20ms")
    print(f"Actual: {routing_results['overhead_ms']:.2f}ms")
    
    if routing_results['overhead_ms'] < 20:
        print("✅ PERFORMANCE TARGET MET")
    else:
        print("❌ PERFORMANCE TARGET NOT MET")
    
    print()


if __name__ == "__main__":
    main()
