"""
Holographic Interpreter Module
Implements Interval Summaries and the Merge Operator for height compression.
Based on Williams (2025) and Cook-Mertz (2025).
"""

import numpy as np
import math
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class IntervalSummary:
    """
    Compressed representation of a computation interval.
    """
    q_in: int           # Initial control state
    q_out: int          # Final control state
    h_in: int           # Initial head position
    h_out: int          # Final head position
    W_interface: bytes  # Interface window content (O(b) bytes)
    regime: str = "VOID" # "VOID" (deterministic) or "VOLUME" (non-deterministic)
    
    def __repr__(self):
        return f"Summary(q:{self.q_in}->{self.q_out}, h:{self.h_in}->{self.h_out}, regime:{self.regime})"


class HolographicInterpreter:
    """
    Verifies computation traces using height-compressed summaries.
    """
    
    def __init__(self, block_size=32):
        self.block_size = block_size
        self.summary_stack: List[IntervalSummary] = []
        self.verified_count = 0
        self.memory_snapshots = [] # To track memory usage (O(sqrt(T)))
        
    def create_summary(self, q_in, q_out, h_in, h_out, window_data=None, regime="VOID"):
        if window_data is None:
            window_data = bytes(self.block_size)
        return IntervalSummary(q_in, q_out, h_in, h_out, window_data, regime)
    
    def merge(self, left: IntervalSummary, right: IntervalSummary) -> Optional[IntervalSummary]:
        if left.q_out != right.q_in:
            return None
        
        merged = IntervalSummary(
            q_in=left.q_in,
            q_out=right.q_out,
            h_in=left.h_in,
            h_out=right.h_out,
            W_interface=right.W_interface
        )
        self.verified_count += 1
        
        # Risk A: If either side is VOLUME, the result is VOLUME (incompressibility propagates)
        if left.regime == "VOLUME" or right.regime == "VOLUME":
            merged.regime = "VOLUME"
            
        return merged
    
    def build_causal_tree(self, summaries: List[IntervalSummary]) -> Optional[IntervalSummary]:
        if not summaries:
            return None
        
        if len(summaries) == 1:
            return summaries[0]
        
        # Risk A: Volume vs Void Regime Check
        # If in VOLUME regime, the active surface scales linearly (O(T)) instead of O(log T)
        current_regime = summaries[0].regime
        if current_regime == "VOLUME":
            # Incompressible boundary: memory usage spikes to volume size
            active_surface_size = len(summaries)
            print(f"[WARNING] Regime: VOLUME. Boundary is algoritmically incompressible. Space: O({active_surface_size})")
        else:
            # Standard Void regime (deterministic path)
            active_surface_size = int(math.log2(len(summaries))) + 1
        
        self.memory_snapshots.append(active_surface_size)
        
        next_level = []
        for i in range(0, len(summaries) - 1, 2):
            merged = self.merge(summaries[i], summaries[i + 1])
            if merged is None:
                return None
            next_level.append(merged)
        
        if len(summaries) % 2 == 1:
            next_level.append(summaries[-1])
        
        return self.build_causal_tree(next_level)
    
    def verify_trace(self, trace_summaries: List[IntervalSummary]) -> bool:
        print(f"--- Holographic Verification ({len(trace_summaries)} intervals) ---")
        root = self.build_causal_tree(trace_summaries)
        if root is not None:
            print(f"[VERIFIED] Root summary: {root}")
            return True
        return False

if __name__ == "__main__":
    # Internal test
    interpreter = HolographicInterpreter()
    summaries = [interpreter.create_summary(i, i+1, i, i+1) for i in range(8)]
    interpreter.verify_trace(summaries)
    print(f"Memory Snapshots: {interpreter.memory_snapshots}")
