"""
Transient Chaos Experiment - SCO v6.5
Status: PROTOTYPE
Theory: Analog Ising Machines exhibit transient chaos before settling.

We simulate the Hopfield-Tank neural network dynamics for SAT, treating each
variable as a continuous "spin" in [-1, +1] that evolves according to a Gradient
Flow on the energy landscape.

Hardness Conjecture: Difficult instances spend exponentially longer in transient
chaos (positive Lyapunov exponent) before converging.
"""

import sys
sys.path.insert(0, 'd:/PvsNP')

import numpy as np
from scipy.integrate import odeint
from engines.physics.phase_detector import SpinGlassPhaseDetector


def sat_energy(spins, clauses):
    """
    Compute a continuous 'energy' for a SAT instance.
    Energy = sum over clauses (1 - max_i{ satisfied_i })
    where satisfied_i = (1 - s_j * sign_j) / 2 for each literal.
    A satisfied clause contributes 0, unsatisfied contributes ~ 1.
    """
    E = 0.0
    for clause in clauses:
        # Compute 'softmax' satisfaction for the clause
        clause_sat = 1.0  # Product of unsatisfied (0 if any is sat)
        for lit in clause:
            var = abs(lit) - 1  # 0-indexed
            sign = 1 if lit > 0 else -1
            # Literal satisfied if spin * sign > 0
            # Satisfaction degree: (1 + sign * spin) / 2 in [0, 1]
            sat_degree = (1 + sign * spins[var]) / 2
            clause_sat *= (1 - sat_degree)  # All literals must fail for clause to fail
        E += clause_sat
    return E


def gradient_flow(spins, t, clauses, beta=5.0):
    """
    Compute gradient of energy w.r.t. spins.
    Dynamics: d(spin)/dt = -grad(E) + noise
    The 'beta' parameter controls steepness (annealing).
    """
    n = len(spins)
    grad = np.zeros(n)
    eps = 1e-6
    
    for i in range(n):
        spins_plus = spins.copy()
        spins_minus = spins.copy()
        spins_plus[i] += eps
        spins_minus[i] -= eps
        
        # Numerical gradient
        grad[i] = (sat_energy(spins_plus, clauses) - sat_energy(spins_minus, clauses)) / (2 * eps)
    
    # Gradient descent with soft constraint to [-1, 1]
    dsdt = -beta * grad - 0.1 * spins * (np.abs(spins) - 1) * (np.abs(spins) > 1)
    return dsdt


def estimate_lyapunov(trajectory, dt=0.01):
    """
    Estimate max Lyapunov exponent from trajectory divergence.
    Simplified: measure how quickly nearby points diverge.
    """
    diffs = np.diff(trajectory, axis=0)
    norms = np.linalg.norm(diffs, axis=1)
    
    # Avoid log(0)
    norms = norms[norms > 1e-10]
    if len(norms) < 2:
        return 0.0
        
    # Estimate divergence rate
    log_norms = np.log(norms + 1e-10)
    lyap = np.mean(np.diff(log_norms)) / dt
    return lyap


def run_chaos_experiment(n_vars=20):
    print("\n" + "="*70)
    print("SCO v6.5 - TRANSIENT CHAOS EXPERIMENT (Ising ODE)")
    print("="*70)
    
    detector = SpinGlassPhaseDetector()
    alphas = [2.0, 3.0, 4.0, 4.26, 5.0]
    
    print(f"{'Alpha':>6} | {'Converged':>10} | {'Lyapunov (Est)':>16} | {'Time to Converge':>18}")
    print("-"*70)
    
    for alpha in alphas:
        instance = detector.generate_random_3sat(n_vars=n_vars, alpha=alpha)
        
        # Initial random spins in [-1, 1]
        spins_init = np.random.uniform(-1, 1, n_vars)
        
        # Time evolution
        t = np.linspace(0, 50, 500)  # Longer time for harder instances
        
        trajectory = odeint(gradient_flow, spins_init, t, args=(instance.clauses,))
        
        # Check convergence: final spins should be near +/-1
        final_spins = trajectory[-1]
        converged = np.all(np.abs(final_spins) > 0.9)
        
        # Lyapunov exponent
        lyap = estimate_lyapunov(trajectory)
        
        # Time to "settle" (spins reach +/-0.9)
        settled_mask = np.all(np.abs(trajectory) > 0.9, axis=1)
        if np.any(settled_mask):
            settle_idx = np.argmax(settled_mask)
            settle_time = t[settle_idx]
        else:
            settle_time = float('inf')
        
        status = "YES" if converged else "NO"
        print(f"{alpha:>6.2f} | {status:>10} | {lyap:>16.4f} | {settle_time:>18.2f}")

    print("-"*70)
    print("Interpretation:")
    print("- Positive Lyapunov: Chaotic transient (Butterfly Effect in search).")
    print("- Long Settle Time: Analog solver struggles to escape chaotic attractor.")


if __name__ == "__main__":
    run_chaos_experiment()
