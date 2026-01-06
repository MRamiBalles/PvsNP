"""
HERMES Oracle - Trainable Boundary Predictor
Status: UPGRADED (Phase 21)
Source: Williams (2025) Sec. 6.4, DeepSeek-Prover Expert Iteration

Now includes a TrainablePredictor that learns from synthetic data,
replacing the mock random oracle with a pattern-matching model.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Tuple, List
import hashlib

@dataclass
class BoundaryPrediction:
    interval: Tuple[int, int]
    predicted_hash: str
    confidence: float
    reasoning_trace: str

class TrainablePredictor:
    """
    A simple pattern-matching predictor that learns from training data.
    Uses memoization + similarity matching for predictions.
    
    In a production system, this would be replaced by an LLM or neural network.
    """
    
    def __init__(self):
        # Lookup table: (initial_state, time_t) -> boundary_hash
        self.memory: Dict[Tuple[str, int], str] = {}
        # Pattern cache for approximate matching
        self.pattern_cache: Dict[str, List[Tuple[int, str]]] = {}
        self.training_samples = 0
        
    def train(self, samples: List):
        """
        Train the predictor on a dataset of samples.
        Each sample should have: initial_state, time_t, boundary_hash
        """
        for sample in samples:
            key = (sample.initial_state, sample.time_t)
            self.memory[key] = sample.boundary_hash
            
            # Build pattern cache for approximate matching
            if sample.initial_state not in self.pattern_cache:
                self.pattern_cache[sample.initial_state] = []
            self.pattern_cache[sample.initial_state].append(
                (sample.time_t, sample.boundary_hash)
            )
        
        self.training_samples = len(samples)
        print(f"[PREDICTOR] Trained on {self.training_samples} samples")
        print(f"  Unique states: {len(self.pattern_cache)}")
        print(f"  Memory entries: {len(self.memory)}")
    
    def predict(self, initial_state: str, time_t: int) -> Tuple[str, float]:
        """
        Predict the boundary hash for a given state and time.
        
        Returns: (predicted_hash, confidence)
        """
        # Exact match (highest confidence)
        key = (initial_state, time_t)
        if key in self.memory:
            return self.memory[key], 1.0
        
        # Approximate match: find closest time for same state
        if initial_state in self.pattern_cache:
            patterns = self.pattern_cache[initial_state]
            # Find closest time
            closest = min(patterns, key=lambda x: abs(x[0] - time_t))
            closest_t, closest_hash = closest
            
            # Confidence decreases with time distance
            time_distance = abs(closest_t - time_t)
            confidence = max(0.3, 1.0 - (time_distance / 50))
            
            # Interpolate hash (simplified: modify last char based on delta)
            delta = time_t - closest_t
            interpolated = closest_hash[:-2] + format(abs(delta) % 256, '02x')
            
            return interpolated, confidence
        
        # No match: fall back to deterministic pseudo-random
        fallback_input = f"{initial_state}_{time_t}_fallback"
        fallback_hash = hashlib.sha256(fallback_input.encode()).hexdigest()[:16]
        return fallback_hash, 0.1  # Very low confidence

class HERMESOracle:
    """
    Neural Oracle for Holographic Boundary Prediction.
    
    Now uses TrainablePredictor for learned predictions instead of random hashes.
    """
    
    def __init__(self, use_trained: bool = True):
        self.predictor = TrainablePredictor() if use_trained else None
        self.prediction_cache = {}
        self.accuracy_log = []
        self.is_trained = False
        
    def train_from_file(self, dataset_path: str):
        """Train the predictor from a JSONL dataset file."""
        from engines.learning.trace_generator import TraceGenerator
        
        generator = TraceGenerator()
        samples = generator.load_dataset(dataset_path)
        self.predictor.train(samples)
        self.is_trained = True
        
    def train_from_samples(self, samples: List):
        """Train directly from sample objects."""
        self.predictor.train(samples)
        self.is_trained = True
        
    def predict_boundary(self, start_state: Dict, interval: Tuple[int, int]) -> BoundaryPrediction:
        """
        Predict the holographic boundary for a given interval.
        Uses trained predictor if available, otherwise falls back to mock.
        """
        t_start, t_end = interval
        initial_state = start_state.get("state", f"t_{t_start}")
        time_t = t_end - t_start
        
        if self.predictor and self.is_trained:
            # Use trained predictor
            predicted_hash, confidence = self.predictor.predict(initial_state, time_t)
            reasoning = f"Trained prediction for {initial_state}@t={time_t}"
        else:
            # Fallback to mock (random-ish)
            prediction_input = f"{start_state}_{t_start}_{t_end}"
            predicted_hash = hashlib.sha256(prediction_input.encode()).hexdigest()[:16]
            confidence = 0.1
            reasoning = "Mock prediction (untrained)"
        
        prediction = BoundaryPrediction(
            interval=interval,
            predicted_hash=predicted_hash,
            confidence=confidence,
            reasoning_trace=reasoning
        )
        
        self.prediction_cache[interval] = prediction
        print(f"[ORACLE] Predicted sigma({t_start},{t_end}) = {predicted_hash[:8]}... (conf: {confidence:.2f})")
        
        return prediction

    def report_accuracy(self, interval: Tuple[int, int], was_correct: bool):
        """Log prediction accuracy for learning feedback."""
        self.accuracy_log.append({
            "interval": interval,
            "correct": was_correct
        })
        
        if len(self.accuracy_log) >= 10:
            accuracy = sum(1 for x in self.accuracy_log if x["correct"]) / len(self.accuracy_log)
            print(f"[ORACLE] Rolling accuracy: {accuracy:.1%}")

if __name__ == "__main__":
    # Demo: generate data and train
    from engines.learning.trace_generator import TraceGenerator
    
    print("=== HERMES Oracle Training Demo ===\n")
    
    # Generate training data
    generator = TraceGenerator(t_max=50)
    samples = generator.generate_dataset(num_samples=100)
    
    # Train oracle
    oracle = HERMESOracle()
    oracle.train_from_samples(samples)
    
    # Test predictions
    print("\n=== Testing Predictions ===")
    test_cases = [
        ({"state": "state_0"}, (0, 25)),
        ({"state": "state_1"}, (0, 30)),
        ({"state": "state_5"}, (0, 45)),
    ]
    
    for state, interval in test_cases:
        pred = oracle.predict_boundary(state, interval)
        print(f"  {interval}: {pred.predicted_hash[:12]}... (conf: {pred.confidence:.2f})")
