"""
Holographic Monitor - Real-Time Visualization
Status: NEW (Phase 18)
Validates Computational Area Law: S(t) <= O(sqrt(t))

Visualizes the "Holographic Boundary" of the Algebraic Replay Engine.
"""

import math
import sys
import time
from engines.holography.optimization import AlgebraicReplayEngine

class HolographicMonitor:
    def __init__(self, time_bound_t):
        self.t = time_bound_t
        self.max_space_observed = 0
        self.history = []
        self.engine = AlgebraicReplayEngine(self.t, telemetry_callback=self.on_telemetry_event)

    def on_telemetry_event(self, stack_depth, block_size):
        """
        Callback from the engine.
        Total Space = Active Screen Area (b) + Stack Depth (log T)
        """
        current_space = block_size + stack_depth
        self.max_space_observed = max(self.max_space_observed, current_space)
        self.history.append(current_space)
        
        # Optional: Print real-time status (can be noisy for large T)
        # print(f"Stack: {stack_depth}, TotalSpace: {current_space}")

    def run_simulation(self):
        print(f"\n[MONITOR] Starting Holographic Simulation (T={self.t})...")
        print(f"[MONITOR] Theoretical Bound sqrt(T) = {math.sqrt(self.t):.2f}")
        
        start_time = time.time()
        self.engine.height_compression_schedule(0, self.engine.T)
        duration = time.time() - start_time
        
        print(f"[MONITOR] Simulation Complete in {duration:.4f}s.")
        self.visualize_results()

    def visualize_results(self):
        print("\n" + "="*50)
        print("COMPUTATIONAL AREA LAW VISUALIZATION")
        print("="*50)
        
        theoretical_bound = 2 * math.sqrt(self.t) # Conservative bound 2*sqrt(t)
        
        print(f"Max Space Observed: {self.max_space_observed}")
        print(f"Theoretical Bound:  {theoretical_bound:.2f}")
        print("-" * 50)
        
        # ASCII Plot of Space Usage over "Time" (Recursion Steps)
        # Downsample history to fit screen width
        width = 60
        step = max(1, len(self.history) // width)
        sampled_history = self.history[::step]
        
        print("Space Usage Profile:")
        max_val = max(self.history) if self.history else 1
        
        for i, val in enumerate(sampled_history):
            # Bar height modeled by val
            bar_len = int((val / max_val) * 20)
            bar = "#" * bar_len
            print(f"t={i*step:<4} | {bar} ({val})")
            
        print("-" * 50)
        if self.max_space_observed <= theoretical_bound:
            print("[SUCCESS] VALID: Space stayed within Holographic Boundary.")
        else:
            print("[WARNING] VIOLATION: Space exceeded bound!")
        print("="*50)

if __name__ == "__main__":
    # Test cases
    monitor = HolographicMonitor(time_bound_t=1000)
    monitor.run_simulation()
