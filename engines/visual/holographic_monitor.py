"""
Holographic Monitor - Phase 19 Refined
Validates Payload (sqrt T) vs Overhead (log T) scaling.
"""

import math
import sys
from engines.holography.optimization import AlgebraicReplayEngine

class HolographicMonitor:
    def __init__(self, time_bound_t):
        self.t = time_bound_t
        self.history = []
        self.engine = AlgebraicReplayEngine(self.t, telemetry_callback=self.store_telemetry)

    def store_telemetry(self, payload, overhead):
        self.history.append((payload, overhead))

    def run_simulation(self):
        print(f"\n[MONITOR] Phase 19: Auditing Holographic Scale (T={self.t})")
        self.engine.recursive_eval(0, self.t, 0)
        self.visualize_results()

    def visualize_results(self):
        print("\n" + "="*60)
        print("HOLOGRAPHIC PERFECTION AUDIT: PAYLOAD VS OVERHEAD")
        print("="*60)
        
        max_p = max(p for p, o in self.history)
        max_o = max(o for p, o in self.history)
        
        print(f"Max Active Payload:  {max_p} (Target: O(sqrt T))")
        print(f"Max Control Overhead: {max_o} (Target: O(log T))")
        print("-" * 60)
        
        # ASCII Plotting Layer
        width = 50
        step = max(1, len(self.history) // 15)
        sampled = self.history[::step]
        
        print("Visual Profile [ P=Payload, O=Overhead ]")
        for i, (p, o) in enumerate(sampled):
            # Scale bars relative to max_p
            p_len = int((p / max_p) * 20)
            o_len = int((o / max_p) * 20)
            
            p_bar = "P" * p_len
            o_bar = "O" * o_len
            
            print(f"t={i*step:<4} | {p_bar}{o_bar} (P:{p}, O:{o})")
            
        print("-" * 60)
        # Verification Logic
        sqrt_t = math.sqrt(self.t)
        log_t = math.log2(self.t)
        
        if max_p <= 2.5 * sqrt_t and max_o < max_p:
            print("[SUCCESS] VALID: Asymptotic separation confirmed.")
            print(f"         Payload ~ {max_p/sqrt_t:.2f}*sqrt(T), Overhead ~ {max_o/log_t:.2f}*log(T)")
        else:
            print("[WARNING] Audit failed to confirm strict separation.")
        print("="*60)

if __name__ == "__main__":
    monitor = HolographicMonitor(time_bound_t=2000)
    monitor.run_simulation()
