
"""
Grokking Test - Neural Generalization Experiment
Status: NEW (Phase 22)
Source: Power et al. (2022) "Grokking", DeepSeek-Prover

Measures accuracy curves to detect non-linear jumps in learning.
Compares RandomForest (memorization) vs MLP (potential generalization).
"""

from typing import List, Dict, Tuple
import sys
sys.path.insert(0, 'd:/PvsNP')

from engines.learning.trace_generator import TraceGenerator
from engines.learning.sklearn_predictor import ScikitLearnOracle, SKLEARN_AVAILABLE

class GrokkingExperiment:
    """
    Experiment to detect "grokking" - delayed generalization in neural networks.
    
    Protocol:
    1. Train on increasing dataset sizes
    2. Evaluate on held-out test set
    3. Plot accuracy curve
    4. Look for S-shaped curve (grokking signature)
    """
    
    def __init__(self, t_max: int = 50):
        self.t_max = t_max
        self.generator = TraceGenerator(t_max=t_max)
        
    def run_experiment(self, 
                       model_type: str = 'rf',
                       training_sizes: List[int] = None,
                       test_size: int = 100) -> List[Tuple[int, float]]:
        """
        Run grokking experiment with specified model type.
        
        Returns: List of (train_size, accuracy) tuples
        """
        if not SKLEARN_AVAILABLE:
            print("[ERROR] scikit-learn not available")
            return []
        
        if training_sizes is None:
            training_sizes = [20, 50, 100, 200, 300, 500]
        
        print("="*60)
        print(f"GROKKING EXPERIMENT - {model_type.upper()}")
        print("="*60)
        print(f"Training sizes: {training_sizes}")
        print(f"Test set size: {test_size}")
        print("-"*60)
        
        results = []
        
        # Generate fixed test set
        test_samples = self.generator.generate_dataset(num_samples=test_size)
        
        for train_size in training_sizes:
            # Generate training data
            train_samples = self.generator.generate_dataset(num_samples=train_size)
            
            # Train model
            oracle = ScikitLearnOracle(model_type=model_type, t_max=self.t_max)
            oracle.train(train_samples)
            
            # Evaluate
            eval_result = oracle.evaluate(test_samples)
            accuracy = eval_result['accuracy']
            
            results.append((train_size, accuracy))
            print(f"Train Size: {train_size:4d} | Test Accuracy: {accuracy:.1%}")
        
        print("-"*60)
        
        # Detect grokking (jump from <50% to >80%)
        prev_acc = 0
        grokking_detected = False
        for train_size, accuracy in results:
            if prev_acc < 0.5 and accuracy > 0.8:
                print(f"[GROKKING] Jump detected at {train_size} samples!")
                grokking_detected = True
                break
            prev_acc = accuracy
        
        if not grokking_detected:
            # Check for gradual learning (baseline)
            final_acc = results[-1][1] if results else 0
            if final_acc > 0.8:
                print(f"[LEARNING] Gradual learning achieved. Final: {final_acc:.1%}")
            else:
                print(f"[PLATEAU] Model plateaued at {final_acc:.1%}")
        
        print("="*60)
        return results

    def compare_models(self, training_sizes: List[int] = None, test_size: int = 100):
        """Compare RF vs MLP to find which generalizes better."""
        print("\n" + "="*60)
        print("MODEL COMPARISON: Random Forest vs MLP")
        print("="*60)
        
        rf_results = self.run_experiment('rf', training_sizes, test_size)
        mlp_results = self.run_experiment('mlp', training_sizes, test_size)
        
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"{'Size':<8} | {'RF Acc':<10} | {'MLP Acc':<10} | {'Winner':<10}")
        print("-"*45)
        
        for (size, rf_acc), (_, mlp_acc) in zip(rf_results, mlp_results):
            winner = "RF" if rf_acc > mlp_acc else "MLP" if mlp_acc > rf_acc else "TIE"
            print(f"{size:<8} | {rf_acc:.1%}      | {mlp_acc:.1%}      | {winner}")
        
        print("="*60)
        return {"rf": rf_results, "mlp": mlp_results}

if __name__ == "__main__":
    experiment = GrokkingExperiment(t_max=50)
    
    # Run comparison
    experiment.compare_models(
        training_sizes=[20, 50, 100, 150, 200, 300],
        test_size=100
    )
