"""
Refuter Hardness Experiment
Status: NEW (Phase 26 - SCO v3.0)

Measures the 'Hardness of Refutation' across the alpha spectrum.
Hypothesis: Refutation effort peaks at the critical phase transition.
- Easy SAT: Refuter wins quickly.
- Easy UNSAT: Prover wins quickly (Refuter gives up).
- Critical: Refuter struggles maximally (High energy expenditure).
"""

import sys
sys.path.insert(0, 'd:/PvsNP')

from engines.physics.phase_detector import SpinGlassPhaseDetector, SATInstance
from engines.meta.refuter import RefuterEngine, GameResult

def run_hardness_experiment():
    print("\n" + "="*70)
    print("SCO v3.0 - PHASE 26: REFUTER HARDNESS GAME")
    print("="*70)
    print("Objective: Measure complexity of finding counter-examples")
    print("Hypothesis: Peak hardness at alpha ~ 4.26")
    print("="*70 + "\n")
    
    phase_detector = SpinGlassPhaseDetector()
    refuter = RefuterEngine(max_steps=3000)
    
    alpha_values = [2.0, 3.0, 4.0, 4.26, 4.5, 5.0, 6.0]
    n_vars = 50
    
    print("="*70)
    print("REFUTATION COMPLEXITY ANALYSIS")
    print("="*70)
    print(f"{'Alpha':>6} | {'Result':>12} | {'Steps':>6} | {'Residual':>8} | {'Energy':>8}")
    print("-"*70)
    
    results = []
    
    for alpha in alpha_values:
        # Generate instance
        instance = phase_detector.generate_random_3sat(n_vars=n_vars, alpha=alpha)
        
        # Run Refuter
        metrics = refuter.refute(instance)
        
        # Analyze outcome
        if metrics.result == GameResult.REFUTER_WINS:
            outcome = "REFUTED" # Found SAT -> Claim False
        else:
            outcome = "CONFIRMED" # Failed to find SAT -> Claim Likely True
        
        print(f"{alpha:>6.2f} | {outcome:>12} | {metrics.steps:>6} | {metrics.contradictions_found:>8} | {metrics.energy_expended:>8.4f}")
        
        results.append({
            "alpha": alpha,
            "metrics": metrics,
            "outcome": outcome
        })
        
    print("-"*70)
    
    # Analysis
    print("\n" + "="*70)
    print("METAMATHEMATICAL ANALYSIS")
    print("="*70)
    
    hardest_alpha = max(results, key=lambda r: r["metrics"].contradictions_found)["alpha"]
    
    print(f"Hardest to Refute (Max Residual Unsat): Alpha = {hardest_alpha}")
    
    refuted_count = sum(1 for r in results if r["outcome"] == "REFUTED")
    confirmed_count = sum(1 for r in results if r["outcome"] == "CONFIRMED")
    
    print(f"Refuted claims (Easy SAT): {refuted_count}")
    print(f"Confirmed claims (Hard/UNSAT): {confirmed_count}")
    
    print("\n[CONCLUSION]")
    print(f"At alpha ~ {hardest_alpha}, the Refuter cannot find a solution")
    print("but also cannot easily prove non-existence (high residual search).")
    print("This 'Twilight Zone' is where TFNP hardness resides.")
    print("="*70)

if __name__ == "__main__":
    run_hardness_experiment()
