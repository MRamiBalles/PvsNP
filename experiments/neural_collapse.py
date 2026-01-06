"""
Neural Collapse Experiment
Status: NEW (Phase 21)
Source: DeepSeek-Prover, Interpretability Literature

Measures how many training samples are needed for the HERMES Oracle
to achieve accurate boundary predictions (Fast Path).
"""

import random
from typing import List, Tuple
from engines.learning.trace_generator import TraceGenerator, TrainingSample
from engines.agent.hermes_oracle import HERMESOracle
from engines.holography.optimization import AlgebraicReplayEngine
import hashlib

class NeuralCollapseExperiment:
    """
    Experiment to measure the "Neural Collapse" phenomenon:
    At what point does the oracle learn the dynamics well enough
    to predict boundaries without simulation?
    """
    
    def __init__(self, t_max: int = 50):
        self.t_max = t_max
        self.generator = TraceGenerator(t_max=t_max)
        
    def _compute_ground_truth(self, initial_state: str, time_t: int) -> str:
        """Compute actual boundary hash via ARE."""
        engine = AlgebraicReplayEngine(time_t)
        summary = engine.recursive_eval(0, time_t, 0)
        hash_input = f"{initial_state}_{time_t}_{summary['t_start']}_{summary['t_end']}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]
    
    def run_experiment(self, training_sizes: List[int] = None, test_size: int = 50):
        """
        Run the collapse experiment with varying training sizes.
        
        Measures accuracy at each training size to find the "collapse point"
        where accuracy jumps from ~0% to >80%.
        """
        if training_sizes is None:
            training_sizes = [10, 25, 50, 100, 200, 500]
        
        print("="*60)
        print("NEURAL COLLAPSE EXPERIMENT")
        print("="*60)
        print(f"Testing training sizes: {training_sizes}")
        print(f"Test set size: {test_size}")
        print("-"*60)
        
        results = []
        
        for train_size in training_sizes:
            # Generate training data
            train_samples = self.generator.generate_dataset(num_samples=train_size)
            
            # Train oracle
            oracle = HERMESOracle()
            oracle.train_from_samples(train_samples)
            
            # Generate test data (different samples)
            test_samples = self.generator.generate_dataset(num_samples=test_size)
            
            # Evaluate
            correct = 0
            for sample in test_samples:
                state = {"state": sample.initial_state}
                interval = (0, sample.time_t)
                
                prediction = oracle.predict_boundary(state, interval)
                ground_truth = sample.boundary_hash
                
                if prediction.predicted_hash == ground_truth:
                    correct += 1
            
            accuracy = correct / test_size
            results.append((train_size, accuracy))
            
            print(f"Training Size: {train_size:4d} | Accuracy: {accuracy:.1%} ({correct}/{test_size})")
        
        print("-"*60)
        
        # Detect collapse point
        collapse_point = None
        for train_size, accuracy in results:
            if accuracy >= 0.8:
                collapse_point = train_size
                break
        
        if collapse_point:
            print(f"[COLLAPSE] Neural Collapse detected at {collapse_point} samples!")
        else:
            print("[COLLAPSE] No collapse detected. Model needs more data or better architecture.")
        
        print("="*60)
        return results

if __name__ == "__main__":
    experiment = NeuralCollapseExperiment(t_max=50)
    results = experiment.run_experiment(training_sizes=[10, 25, 50, 100, 150, 200])
