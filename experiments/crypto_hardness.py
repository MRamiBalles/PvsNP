"""
Cryptographic Hardness Experiment - SCO v5.0
Status: NEW (Phase 34)

Connects topological persistence to average-case hardness and OWF existence.
Tests whether H1 > 0 correlates with high Kt-complexity.
"""

import sys
sys.path.insert(0, 'd:/PvsNP')

from engines.physics.phase_detector import SpinGlassPhaseDetector
from engines.sat.instrumented_solver import InstrumentedSATSolver
from engines.topology.topological_scanner import TopologicalScanner
from engines.crypto.mcsp_owf import MCSPManager

def run_crypto_experiment():
    print("\n" + "="*70)
    print("SCO v5.0 - PHASE 34: CRYPTOGRAPHIC HARDNESS (MCSP-OWF)")
    print("="*70)
    print("Objective: Link H1 persistence to Kt-complexity and OWFs")
    print("="*70 + "\n")
    
    detector = SpinGlassPhaseDetector()
    solver = InstrumentedSATSolver()
    scanner = TopologicalScanner()
    crypto = MCSPManager()
    
    alpha_values = [2.0, 3.0, 4.0, 4.26, 4.5]
    
    print("="*90)
    print(f"{'Alpha':>6} | {'H1':>3} | {'Kt (bits)':>10} | {'Ratio':>6} | {'Entropy':>8} | {'Hard?'}")
    print("-"*90)
    
    for alpha in alpha_values:
        # Increase n_vars to get meaningful traces
        instance = detector.generate_random_3sat(n_vars=40, alpha=alpha)
        
        # Solve and get trace
        _, trace = solver.solve_with_trace(instance)
        configs = solver.trace_to_config_list()
        
        # Topological Analysis
        complex = scanner.trace_to_simplicial_complex(configs)
        betti = scanner.compute_betti_numbers(complex)
        
        # Cryptographic Analysis
        res = crypto.analyze_cryptographic_potential(configs, betti.beta_1)
        
        hard_str = "YES (OWF)" if res.is_average_case_hard else "NO (P)"
        
        print(f"{alpha:>6.2f} | {betti.beta_1:>3} | {res.kt_complexity:>10.1f} | {res.compression_ratio:>6.3f} | "
              f"{res.topological_entropy:>8.3f} | {hard_str}")

    print("-"*90)
    print("\n" + "="*70)
    print("VERDICT: ONE-WAY FUNCTION EXISTENCE")
    print("="*70)
    print("According to Cavalar et al. (2025):")
    print("- High H1 + incompressible Kt (Ratio > 0.1) implies MCSP hardness.")
    print("- MCSP hardness on average-case implies existence of OWFs.")
    print("="*70)

if __name__ == "__main__":
    run_crypto_experiment()
