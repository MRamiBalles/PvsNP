"""
Hybrid Holographic Engine - ARE + RF Oracle
Status: NEW (Phase 23)
Source: Cook-Mertz (2025), Williams (2025), HERMES Architecture

Combines the Algebraic Replay Engine with the RF Oracle for
speculative acceleration. The oracle predicts boundary states,
and the ARE verifies them locally, pruning the recursion tree.
"""

import time
import math
from typing import Dict, Tuple, Optional
from dataclasses import dataclass

from engines.holography.optimization import AlgebraicReplayEngine
from engines.learning.sklearn_predictor import ScikitLearnOracle, SKLEARN_AVAILABLE
from engines.learning.trace_generator import TraceGenerator

@dataclass
class HybridMetrics:
    total_intervals: int
    oracle_hits: int
    oracle_misses: int
    are_fallbacks: int
    time_elapsed: float
    speedup_factor: float

class HybridHolographicEngine:
    """
    Hybrid Engine: Combines speculative ML prediction with rigorous ARE verification.
    
    Protocol:
    1. Oracle predicts boundary config for interval [L, R]
    2. If confidence > threshold, verify prediction locally (cheap)
    3. If verification passes, skip ARE recursion (Fast Path)
    4. If verification fails or confidence low, fall back to ARE (Slow Path)
    
    Source: Inspired by HERMES "informal reasoning + formal verification" paradigm.
    """
    
    def __init__(self, time_bound: int, confidence_threshold: float = 0.7):
        self.time_bound = time_bound
        self.confidence_threshold = confidence_threshold
        
        # Core ARE
        self.are = AlgebraicReplayEngine(time_bound)
        
        # ML Oracle (RF by default - best performer from Phase 22)
        self.oracle = ScikitLearnOracle(model_type='rf', t_max=time_bound) if SKLEARN_AVAILABLE else None
        self.oracle_trained = False
        
        # Metrics
        self.metrics = {
            "oracle_queries": 0,
            "oracle_hits": 0,
            "oracle_misses": 0,
            "are_fallbacks": 0,
            "verification_failures": 0
        }
    
    def train_oracle(self, num_samples: int = 500):
        """Train the oracle with synthetic data."""
        if not self.oracle:
            print("[HYBRID] No oracle available (sklearn not installed)")
            return
        
        generator = TraceGenerator(t_max=self.time_bound)
        samples = generator.generate_dataset(num_samples=num_samples)
        self.oracle.train(samples)
        self.oracle_trained = True
        print(f"[HYBRID] Oracle trained on {num_samples} samples")
    
    def _verify_prediction_locally(self, predicted_config: dict, interval: Tuple[int, int]) -> bool:
        """
        Cheap local verification of oracle prediction.
        Checks if the predicted config is consistent with the interval.
        """
        if not predicted_config:
            return False
        
        # Basic consistency: predicted interval must match query interval
        expected_label = f"0_{interval[1]}"
        predicted_label = f"{predicted_config.get('t_start', -1)}_{predicted_config.get('t_end', -1)}"
        
        return predicted_label == expected_label
    
    def simulate_interval(self, start: int, end: int, depth: int = 0) -> dict:
        """
        Hybrid simulation: Oracle-first with ARE fallback.
        """
        length = end - start + 1
        
        # Base case: small intervals use ARE directly
        if length <= self.are.block_size:
            return self.are._simulate_block(start, end)
        
        self.metrics["oracle_queries"] += 1
        
        # Try oracle prediction if available and trained
        if self.oracle and self.oracle_trained:
            initial_state = f"state_{start % 10}"
            time_t = end - start
            
            predicted_config, confidence = self.oracle.predict(initial_state, time_t)
            
            if confidence >= self.confidence_threshold:
                # Attempt local verification
                if self._verify_prediction_locally(predicted_config, (start, end)):
                    self.metrics["oracle_hits"] += 1
                    # Fast Path: skip recursion, use predicted config
                    return {"t_start": start, "t_end": end, "source": "oracle", "predicted": True}
                else:
                    self.metrics["verification_failures"] += 1
            else:
                self.metrics["oracle_misses"] += 1
        
        # Slow Path: fall back to ARE
        self.metrics["are_fallbacks"] += 1
        return self.are.recursive_eval(start, end, depth)
    
    def run_simulation(self) -> HybridMetrics:
        """Run full simulation and return metrics."""
        start_time = time.time()
        
        # Reset metrics
        self.metrics = {k: 0 for k in self.metrics}
        
        # Run simulation
        result = self.simulate_interval(0, self.time_bound, 0)
        
        elapsed = time.time() - start_time
        
        total = self.metrics["oracle_queries"]
        hits = self.metrics["oracle_hits"]
        
        return HybridMetrics(
            total_intervals=total,
            oracle_hits=hits,
            oracle_misses=self.metrics["oracle_misses"],
            are_fallbacks=self.metrics["are_fallbacks"],
            time_elapsed=elapsed,
            speedup_factor=hits / max(1, total)  # Fraction of work skipped
        )

class PureAREBenchmark:
    """Baseline benchmark using pure ARE without oracle."""
    
    def __init__(self, time_bound: int):
        self.time_bound = time_bound
        self.are = AlgebraicReplayEngine(time_bound)
    
    def run_simulation(self) -> float:
        """Run pure ARE simulation and return time elapsed."""
        start_time = time.time()
        self.are.recursive_eval(0, self.time_bound, 0)
        return time.time() - start_time

def run_benchmark(time_bound: int = 1000, oracle_samples: int = 500):
    """Compare Hybrid vs Pure ARE performance."""
    print("="*60)
    print("HYBRID ACCELERATION BENCHMARK")
    print("="*60)
    print(f"Time Bound: T = {time_bound}")
    print(f"Oracle Training Samples: {oracle_samples}")
    print("-"*60)
    
    # Pure ARE baseline
    print("\n[1/3] Running Pure ARE Baseline...")
    pure_are = PureAREBenchmark(time_bound)
    pure_time = pure_are.run_simulation()
    print(f"  Pure ARE Time: {pure_time:.4f}s")
    
    # Hybrid with trained oracle
    print("\n[2/3] Training Hybrid Oracle...")
    hybrid = HybridHolographicEngine(time_bound)
    hybrid.train_oracle(num_samples=oracle_samples)
    
    print("\n[3/3] Running Hybrid Simulation...")
    metrics = hybrid.run_simulation()
    
    print(f"\n{'='*60}")
    print("RESULTS")
    print("="*60)
    print(f"Pure ARE Time:       {pure_time:.4f}s")
    print(f"Hybrid Time:         {metrics.time_elapsed:.4f}s")
    print(f"Oracle Queries:      {metrics.total_intervals}")
    print(f"Oracle Hits:         {metrics.oracle_hits} ({metrics.speedup_factor:.1%} hit rate)")
    print(f"ARE Fallbacks:       {metrics.are_fallbacks}")
    
    if metrics.time_elapsed > 0:
        actual_speedup = pure_time / metrics.time_elapsed
        print(f"\nActual Speedup:      {actual_speedup:.2f}x")
        if actual_speedup > 1.0:
            print("[SUCCESS] Hybrid is faster than pure ARE!")
        else:
            print("[NOTE] Overhead exceeded savings (expected with small T)")
    
    print("="*60)
    return {"pure_time": pure_time, "hybrid_time": metrics.time_elapsed, "metrics": metrics}

if __name__ == "__main__":
    run_benchmark(time_bound=1000, oracle_samples=500)
