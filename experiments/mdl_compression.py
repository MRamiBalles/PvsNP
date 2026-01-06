"""
MDL Compression Experiment - SCO v6.5
Status: PROTOTYPE
Theory: Kolmogorov Complexity & Minimum Description Length.

Hard instances have incompressible solution traces.
Easy instances have compressible (structured) traces.

We use multiple compression algorithms as approximators of K(trace).
"""

import sys
sys.path.insert(0, 'd:/PvsNP')

import zlib
import lzma
import bz2
import numpy as np
from engines.physics.phase_detector import SpinGlassPhaseDetector
from engines.sat.instrumented_solver import InstrumentedSATSolver


def compress_trace(trace_bytes, algorithm='zlib'):
    """Compress using specified algorithm."""
    if algorithm == 'zlib':
        return zlib.compress(trace_bytes, level=9)
    elif algorithm == 'lzma':
        return lzma.compress(trace_bytes, preset=9)
    elif algorithm == 'bz2':
        return bz2.compress(trace_bytes, compresslevel=9)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")


def trace_to_bytes(trace):
    """Convert a trace list to a byte sequence for compression."""
    # Serialize trace events to a string
    parts = []
    for event in trace:
        parts.append(f"{event.event_type.value}:{event.level}:{event.variable}:{event.assignment}")
    
    trace_str = "|".join(parts)
    return trace_str.encode('utf-8')


def algorithmic_hardness(raw_size, compressed_size):
    """H_alg = CompressedSize / RawSize. H_alg ~ 1 means incompressible."""
    if raw_size == 0:
        return 0.0
    return compressed_size / raw_size


def run_mdl_experiment(n_vars=40):
    print("\n" + "="*80)
    print("SCO v6.5 - MDL COMPRESSION EXPERIMENT (Kolmogorov Approximation)")
    print("="*80)
    
    detector = SpinGlassPhaseDetector()
    solver = InstrumentedSATSolver()
    alphas = [2.0, 3.0, 4.0, 4.26, 5.0]
    
    print(f"{'Alpha':>6} | {'Trace Len':>10} | {'ZLIB Ratio':>12} | {'LZMA Ratio':>12} | {'BZ2 Ratio':>12} | {'Verdict':>12}")
    print("-"*80)
    
    for alpha in alphas:
        # Average over 3 instances
        ratios_zlib = []
        ratios_lzma = []
        ratios_bz2 = []
        trace_lens = []
        
        for _ in range(3):
            instance = detector.generate_random_3sat(n_vars=n_vars, alpha=alpha)
            result = solver.solve_with_trace(instance)
            
            trace = solver.trace
            trace_bytes = trace_to_bytes(trace)
            raw_size = len(trace_bytes)
            trace_lens.append(len(trace))
            
            if raw_size > 0:
                comp_zlib = len(compress_trace(trace_bytes, 'zlib'))
                comp_lzma = len(compress_trace(trace_bytes, 'lzma'))
                comp_bz2 = len(compress_trace(trace_bytes, 'bz2'))
                
                ratios_zlib.append(algorithmic_hardness(raw_size, comp_zlib))
                ratios_lzma.append(algorithmic_hardness(raw_size, comp_lzma))
                ratios_bz2.append(algorithmic_hardness(raw_size, comp_bz2))
        
        avg_len = np.mean(trace_lens)
        avg_zlib = np.mean(ratios_zlib) if ratios_zlib else 0
        avg_lzma = np.mean(ratios_lzma) if ratios_lzma else 0
        avg_bz2 = np.mean(ratios_bz2) if ratios_bz2 else 0
        
        # Best compression ratio (lowest = most structure)
        best = min(avg_zlib, avg_lzma, avg_bz2)
        
        if best < 0.3:
            verdict = "COMPRESSIBLE"
        elif best < 0.6:
            verdict = "STRUCTURED"
        else:
            verdict = "RANDOM"
        
        print(f"{alpha:>6.2f} | {avg_len:>10.0f} | {avg_zlib:>12.4f} | {avg_lzma:>12.4f} | {avg_bz2:>12.4f} | {verdict:>12}")

    print("-"*80)
    print("Interpretation:")
    print("- COMPRESSIBLE (< 0.3): Trace has exploitable structure (P-like).")
    print("- STRUCTURED (0.3-0.6): Moderate structure.")
    print("- RANDOM (> 0.6): Trace is incompressible (Brute force, NP-like).")


if __name__ == "__main__":
    run_mdl_experiment()
