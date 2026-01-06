"""
Trace Generator - Synthetic Dataset for Oracle Training
Status: NEW (Phase 21)
Source: DeepSeek-Prover Expert Iteration, Lean Workbook

Generates (initial_state, time) -> boundary_hash pairs for training
the HERMES Oracle to predict holographic boundaries.
"""

import json
import random
import hashlib
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict

@dataclass
class TrainingSample:
    initial_state: str
    time_t: int
    boundary_hash: str
    block_size: int

class TraceGenerator:
    """
    Generates synthetic training data by running the ARE
    and recording ground truth boundary hashes.
    """
    
    def __init__(self, t_max: int = 100):
        self.t_max = t_max
        # Import here to avoid circular dependency
        from engines.holography.optimization import AlgebraicReplayEngine
        self.ARE = AlgebraicReplayEngine
        
    def _compute_boundary_hash(self, initial_state: str, time_t: int) -> Tuple[str, int]:
        """
        Run ARE simulation and compute the boundary hash.
        Returns (hash, block_size) tuple.
        """
        engine = self.ARE(time_t)
        
        # Simulate the computation
        summary = engine.recursive_eval(0, time_t, 0)
        
        # Create deterministic hash from state + time + summary
        hash_input = f"{initial_state}_{time_t}_{summary['t_start']}_{summary['t_end']}"
        boundary_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]
        
        return boundary_hash, engine.block_size
    
    def generate_dataset(self, num_samples: int = 500, output_file: str = None) -> List[TrainingSample]:
        """
        Generate a dataset of training samples.
        
        Each sample contains:
        - initial_state: Configuration at t=0
        - time_t: Target time
        - boundary_hash: Ground truth hash of σ(0, time_t)
        """
        samples = []
        
        print(f"[GENERATOR] Generating {num_samples} training samples...")
        
        for i in range(num_samples):
            # Vary initial state (simplified: use index as state identifier)
            initial_state = f"state_{i % 10}"
            
            # Vary time (within bounds)
            time_t = random.randint(10, self.t_max)
            
            # Compute ground truth
            boundary_hash, block_size = self._compute_boundary_hash(initial_state, time_t)
            
            sample = TrainingSample(
                initial_state=initial_state,
                time_t=time_t,
                boundary_hash=boundary_hash,
                block_size=block_size
            )
            samples.append(sample)
            
            if (i + 1) % 100 == 0:
                print(f"  Generated {i + 1}/{num_samples} samples")
        
        # Optionally save to JSONL
        if output_file:
            with open(output_file, 'w') as f:
                for sample in samples:
                    f.write(json.dumps(asdict(sample)) + '\n')
            print(f"[GENERATOR] Saved dataset to {output_file}")
        
        return samples

    def load_dataset(self, input_file: str) -> List[TrainingSample]:
        """Load a previously generated dataset."""
        samples = []
        with open(input_file, 'r') as f:
            for line in f:
                data = json.loads(line)
                samples.append(TrainingSample(**data))
        return samples

if __name__ == "__main__":
    generator = TraceGenerator(t_max=100)
    samples = generator.generate_dataset(num_samples=200, output_file="training_data.jsonl")
    print(f"[GENERATOR] Generated {len(samples)} samples")
    print(f"  Sample: {samples[0]}")
