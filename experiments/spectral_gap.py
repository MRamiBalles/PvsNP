"""
Spectral Gap Experiment - SCO v6.0
Status: DISCOVERY
Theory: Hard instances correspond to "bad expanders" (or disconnected clusters) in the energy landscape.

This script constructs the Configuration Graph for small N (due to 2^N complexity)
and computes the Spectral Gap (2nd smallest eigenvalue of Laplacian).

Hypothesis: 
- Easy (P): High spectral gap (Fast mixing, single component).
- Hard (NP): Low spectral gap (Slow mixing, multiple clusters).
"""

import sys
sys.path.insert(0, 'd:/PvsNP')

import numpy as np
import networkx as nx
from scipy.sparse import csgraph
from scipy.linalg import eigh
from engines.physics.phase_detector import SpinGlassPhaseDetector

def get_energy(assignment, clauses):
    """Calculate number of violated clauses."""
    energy = 0
    for clause in clauses:
        satisfied = False
        for lit in clause:
            var = abs(lit)
            val = assignment.get(var, False) # Boolean
            if (lit > 0 and val) or (lit < 0 and not val):
                satisfied = True
                break
        if not satisfied:
            energy += 1
    return energy

def bit_flip_neighbors(config_int, n_vars):
    """Generate neighbors by flipping 1 bit."""
    neighbors = []
    for i in range(n_vars):
        neighbor = config_int ^ (1 << i)
        neighbors.append(neighbor)
    return neighbors

def run_spectral_analysis(n_vars=12):
    print("\n" + "="*70)
    print(f"SCO v6.0 - SPECTRAL GAP DISCOVERY (n={n_vars})")
    print("="*70)
    
    detector = SpinGlassPhaseDetector()
    alphas = [2.0, 4.26, 6.0]
    
    print(f"{'Alpha':>6} | {'Nodes (Sublevel)':>16} | {'Components':>10} | {'Spectral Gap (L2)':>18} | {'Mixing Time (Est)':>18}")
    print("-"*80)
    
    for alpha in alphas:
        # 1. Generate Instance
        instance = detector.generate_random_3sat(n_vars=n_vars, alpha=alpha)
        
        # 2. Build Sublevel Graph (Low Energy States)
        # We look at states with Energy <= Threshold (e.g., 2 violations)
        # to see the landscape topology "near" solutions.
        threshold = 2 
        
        # Brute force all 2^n states (feasible for n=12 -> 4096)
        states = []
        state_map = {}
        
        for i in range(2**n_vars):
            # Decode assignment
            assignment = {}
            for v in range(n_vars):
                assignment[v+1] = bool((i >> v) & 1)
            
            E = get_energy(assignment, instance.clauses)
            if E <= threshold:
                state_map[i] = len(states)
                states.append(i)
        
        # 3. Build Adjacency
        G = nx.Graph()
        for s_int in states:
            u = state_map[s_int]
            G.add_node(u)
            
            neighbors = bit_flip_neighbors(s_int, n_vars)
            for n_int in neighbors:
                if n_int in state_map:
                    v = state_map[n_int]
                    G.add_edge(u, v)
        
        # 4. Analysis
        if G.number_of_nodes() == 0:
            print(f"{alpha:>6.2f} | {'0':>16} | {'-':>10} | {'-':>18} | {'-':>18}")
            continue
            
        # Connected Components
        n_comps = nx.number_connected_components(G)
        
        # Spectral Gap (Laplacian Eigenvalues)
        if n_comps == 1 and G.number_of_nodes() > 2:
            L = nx.normalized_laplacian_matrix(G).todense()
            evals = eigh(L, eigvals_only=True)
            # Sort and take 2nd smallest (lambda_2)
            evals = np.sort(evals)
            lambda_2 = evals[1] if len(evals) > 1 else 0.0
            mixing_time = 1 / lambda_2 if lambda_2 > 1e-9 else float('inf')
        else:
            lambda_2 = 0.0 # Disconnected
            mixing_time = float('inf')
            
        print(f"{alpha:>6.2f} | {G.number_of_nodes():>16} | {n_comps:>10} | {lambda_2:>18.4f} | {mixing_time:>18.2f}")

    print("-"*80)
    print("Interpretation:")
    print("- High Gap (L2 > 0): Fast mixing, easy to navigate (P).")
    print("- Zero Gap (L2 =~ 0): Disconnected or bottlenecked (NP/Hard).")

if __name__ == "__main__":
    run_spectral_analysis()
