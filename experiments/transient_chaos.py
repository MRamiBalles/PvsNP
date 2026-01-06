"""
Transient Chaos Experiment v2 - SCO v6.6
Status: REFINED
Theory: Analog Ising Machines exhibit transient chaos before settling.

UPGRADE: Using solve_ivp with RK45 adaptive stepping for numerical stability.
"""

import sys
sys.path.insert(0, 'd:/PvsNP')

import numpy as np
from scipy.integrate import solve_ivp
from engines.physics.phase_detector import SpinGlassPhaseDetector


def sat_energy(spins, clauses):
    """Compute continuous 'energy' for a SAT instance."""
    E = 0.0
    for clause in clauses:
        clause_sat = 1.0
        for lit in clause:
            var = abs(lit) - 1
            sign = 1 if lit > 0 else -1
            sat_degree = (1 + sign * spins[var]) / 2
            clause_sat *= (1 - sat_degree)
        E += clause_sat
    return E


def gradient_flow_rk45(t, spins, clauses, beta=5.0):
    """Gradient dynamics compatible with solve_ivp (t, y order)."""
    n = len(spins)
    grad = np.zeros(n)
    eps = 1e-6
    
    for i in range(n):
        spins_plus = spins.copy()
        spins_minus = spins.copy()
        spins_plus[i] += eps
        spins_minus[i] -= eps
        grad[i] = (sat_energy(spins_plus, clauses) - sat_energy(spins_minus, clauses)) / (2 * eps)
    
    # Gradient descent with soft constraint to [-1, 1]
    # Added damping term for stability
    dsdt = -beta * grad - 0.5 * spins * (np.abs(spins) - 1) * (np.abs(spins) > 0.95)
    
    # Clip to prevent explosion
    dsdt = np.clip(dsdt, -10, 10)
    return dsdt


def estimate_lyapunov_improved(trajectory, times):
    """Improved Lyapunov estimation using time-weighted divergence."""
    if len(trajectory) < 10:
        return 0.0
    
    diffs = np.diff(trajectory, axis=0)
    norms = np.linalg.norm(diffs, axis=1)
    dt = np.diff(times)
    
    # Filter valid data
    valid = (norms > 1e-10) & (dt > 1e-10)
    if np.sum(valid) < 5:
        return 0.0
    
    norms = norms[valid]
    dt = dt[valid]
    
    # Cumulative divergence rate
    log_norms = np.log(norms)
    lyap = np.mean(np.diff(log_norms) / dt[:-1]) if len(dt) > 1 else 0.0
    return lyap


def run_chaos_experiment_v2(n_vars=15):
    print("\n" + "="*70)
    print("SCO v6.6 - TRANSIENT CHAOS EXPERIMENT (RK45 Adaptive)")
    print("="*70)
    
    detector = SpinGlassPhaseDetector()
    alphas = [2.0, 3.0, 4.0, 4.26, 5.0]
    
    print(f"{'Alpha':>6} | {'Final Energy':>14} | {'Lyapunov (Est)':>16} | {'Steps (Adaptive)':>18}")
    print("-"*70)
    
    for alpha in alphas:
        instance = detector.generate_random_3sat(n_vars=n_vars, alpha=alpha)
        
        # Initial random spins in [-0.5, 0.5] (closer to origin for stability)
        spins_init = np.random.uniform(-0.5, 0.5, n_vars)
        
        # RK45 with adaptive stepping
        t_span = (0, 30)
        
        try:
            sol = solve_ivp(
                gradient_flow_rk45,
                t_span,
                spins_init,
                method='RK45',
                args=(instance.clauses,),
                max_step=0.5,
                rtol=1e-6,
                atol=1e-8
            )
            
            trajectory = sol.y.T  # Shape: (n_times, n_vars)
            times = sol.t
            
            # Final energy
            final_spins = trajectory[-1] if len(trajectory) > 0 else spins_init
            final_energy = sat_energy(final_spins, instance.clauses)
            
            # Lyapunov
            lyap = estimate_lyapunov_improved(trajectory, times)
            
            n_steps = len(times)
            
        except Exception as e:
            final_energy = float('nan')
            lyap = float('nan')
            n_steps = 0
        
        print(f"{alpha:>6.2f} | {final_energy:>14.4f} | {lyap:>16.4f} | {n_steps:>18}")

    print("-"*70)
    print("Interpretation:")
    print("- High Lyapunov (> 0): Chaotic transient (trajectory divergence).")
    print("- Many Adaptive Steps: Solver struggles with stiff/chaotic dynamics.")
    print("- High Final Energy: Failed to find satisfying assignment.")


if __name__ == "__main__":
    run_chaos_experiment_v2()
