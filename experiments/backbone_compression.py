"""
Backbone Compression Experiment - SCO v6.6
Status: NEW (Refined Hypothesis)
Theory: Hardness resides in the SOLUTION SPACE topology, not the search trace.

Instead of compressing the solver trace (which is algorithmically regular),
we compress the SOLUTION STATES themselves.

Hypothesis:
- Easy instances: Solutions are structured/correlated (high mutual info, compressible).
- Hard instances: Solutions are fragmented into incompressible, mutually exclusive clusters.
"""

import sys
sys.path.insert(0, 'd:/PvsNP')

import zlib
import numpy as np
from pysat.solvers import Solver
from engines.physics.phase_detector import SpinGlassPhaseDetector


def solution_to_bytes(model, n_vars):
    """Convert a SAT model (list of literals) to a compact byte representation."""
    bits = np.zeros(n_vars, dtype=np.uint8)
    for lit in model:
        var = abs(lit) - 1
        bits[var] = 1 if lit > 0 else 0
    return bits.tobytes()


def get_multiple_solutions(clauses, n_solutions=10, timeout_per=1.0):
    """
    Attempt to find multiple distinct solutions using blocking clauses.
    Returns list of models.
    """
    solutions = []
    
    with Solver(name='m22', bootstrap_with=clauses) as s:
        for _ in range(n_solutions):
            if s.solve():
                model = s.get_model()
                solutions.append(model)
                
                # Add blocking clause to exclude this solution
                blocking = [-lit for lit in model]
                s.add_clause(blocking)
            else:
                break  # No more solutions
    
    return solutions


def compute_mutual_information_proxy(solutions, n_vars):
    """
    Compute a proxy for mutual information between solutions.
    High correlation = structured (easy), low = fragmented (hard).
    """
    if len(solutions) < 2:
        return 0.0
    
    # Convert to bit arrays
    bit_arrays = []
    for sol in solutions:
        bits = np.zeros(n_vars, dtype=np.int8)
        for lit in sol:
            var = abs(lit) - 1
            bits[var] = 1 if lit > 0 else -1
        bit_arrays.append(bits)
    
    # Compute average pairwise correlation
    correlations = []
    for i in range(len(bit_arrays)):
        for j in range(i+1, len(bit_arrays)):
            # Fraction of variables with same value
            agreement = np.mean(bit_arrays[i] == bit_arrays[j])
            correlations.append(agreement)
    
    return np.mean(correlations) if correlations else 0.0


def backbone_fraction(solutions, n_vars):
    """
    Compute the fraction of variables that are "frozen" (same value in all solutions).
    High backbone = rigid structure.
    """
    if len(solutions) < 2:
        return 1.0  # Single solution = fully frozen
    
    # For each variable, check if it has the same value across all solutions
    frozen_count = 0
    
    for var in range(1, n_vars + 1):
        values = set()
        for sol in solutions:
            # Find the literal for this variable
            for lit in sol:
                if abs(lit) == var:
                    values.add(lit > 0)
                    break
        
        if len(values) == 1:
            frozen_count += 1
    
    return frozen_count / n_vars


def run_backbone_experiment(n_vars=40):
    print("\n" + "="*80)
    print("SCO v6.6 - BACKBONE COMPRESSION EXPERIMENT (Solution Space Analysis)")
    print("="*80)
    
    detector = SpinGlassPhaseDetector()
    alphas = [2.0, 3.0, 3.5, 4.0, 4.26, 4.5, 5.0]
    
    print(f"{'Alpha':>6} | {'#Solutions':>10} | {'Backbone %':>12} | {'Correlation':>12} | {'Compress Ratio':>14}")
    print("-"*80)
    
    for alpha in alphas:
        # Average over 3 instances
        backbones = []
        correlations = []
        compress_ratios = []
        sol_counts = []
        
        for _ in range(3):
            instance = detector.generate_random_3sat(n_vars=n_vars, alpha=alpha)
            solutions = get_multiple_solutions(instance.clauses, n_solutions=20)
            
            if not solutions:
                continue
            
            sol_counts.append(len(solutions))
            
            # Backbone analysis
            bb = backbone_fraction(solutions, n_vars)
            backbones.append(bb)
            
            # Correlation analysis
            mi = compute_mutual_information_proxy(solutions, n_vars)
            correlations.append(mi)
            
            # Compress the solution itself (not the trace)
            sol_bytes = solution_to_bytes(solutions[0], n_vars)
            compressed = zlib.compress(sol_bytes, level=9)
            ratio = len(compressed) / len(sol_bytes) if len(sol_bytes) > 0 else 0
            compress_ratios.append(ratio)
        
        if sol_counts:
            avg_sols = np.mean(sol_counts)
            avg_bb = np.mean(backbones)
            avg_corr = np.mean(correlations)
            avg_ratio = np.mean(compress_ratios)
            
            print(f"{alpha:>6.2f} | {avg_sols:>10.1f} | {avg_bb:>12.2%} | {avg_corr:>12.4f} | {avg_ratio:>14.4f}")
        else:
            print(f"{alpha:>6.2f} | {'UNSAT':>10} | {'-':>12} | {'-':>12} | {'-':>14}")

    print("-"*80)
    print("Interpretation:")
    print("- High Backbone %: Rigid structure (frozen variables across solutions).")
    print("- Low Correlation: Solutions are in disjoint clusters (shattering).")
    print("- High Compress Ratio: Solution bits are random/incompressible.")


if __name__ == "__main__":
    run_backbone_experiment()
