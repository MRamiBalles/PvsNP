"""
Survey Propagation (SP) Engine - Cavity Method for Random K-SAT
Status: NEW (Phase 28 - SCO v4.0)
Source: Mézard, Parisi, Zecchina (2002); Braunstein, Mézard, Zecchina (2005)

Implements the Survey Propagation algorithm to detect "frozen" variables
in the backbone of hard SAT instances. 

Key Insight: 
SP calculates the probability (survey) that a variable is constrained
to a specific value across various clusters of solutions.
Fills the "Backbone Anomaly" gap where local search (WalkSAT) failed.
"""

import numpy as np
from typing import List, Dict, Tuple, Set, Optional
import random

class SurveyPropagationEngine:
    """
    Implementation of the Survey Propagation message-passing algorithm.
    
    Variables:
    - eta[i -> j]: Survey from clause i to variable j.
    - bias_pos[j]: Probability that variable j is forced to True.
    - bias_neg[j]: Probability that variable j is forced to False.
    - bias_star[j]: Probability that variable j is unconstrained.
    """
    
    def __init__(self, epsilon: float = 1e-3, max_iter: int = 100, damping: float = 0.5):
        self.epsilon = epsilon
        self.max_iter = max_iter
        self.damping = damping
        
    def solve(self, instance) -> Dict[int, Dict[str, float]]:
        """
        Run SP message passing to compute variable biases.
        Returns a dictionary mapping var_id -> {pos, neg, star, backbone_strength}.
        """
        n = instance.num_variables
        clauses = instance.clauses
        
        # Build adjacency maps
        # var_to_clauses[j] = [(clause_idx, literal_sign), ...]
        var_to_clauses = {j: [] for j in range(1, n + 1)}
        # clause_to_vars[i] = [(var_id, literal_sign), ...]
        clause_to_vars = {i: [] for i, _ in enumerate(clauses)}
        
        for i, clause in enumerate(clauses):
            for lit in clause:
                var = abs(lit)
                sign = 1 if lit > 0 else -1
                var_to_clauses[var].append((i, sign))
                clause_to_vars[i].append((var, sign))
        
        # Initialize surveys eta[i -> j] randomly in [0, 1]
        # Maps (clause_idx, var_id) -> probability
        eta = {}
        for i, clause in enumerate(clauses):
            for lit in clause:
                var = abs(lit)
                eta[(i, var)] = random.random()
        
        # Message Passing (Survey Updates)
        converged = False
        for iteration in range(self.max_iter):
            max_diff = 0
            new_eta = {}
            
            # For each clause i and variable j in it
            for i, clause in enumerate(clauses):
                for lit in clause:
                    j = abs(lit)
                    
                    # Compute eta[i -> j]
                    # This is the prob that all OTHER vars in clause i are NOT 
                    # satisfied by THEIR other clauses.
                    
                    prod_term = 1.0
                    for lit_k in clause:
                        k = abs(lit_k)
                        if k == j:
                            continue
                        
                        # Contribution of variable k to clause i
                        # Probability that k is NOT satisfying clause i
                        # (either because it's unconstrained or forced to the wrong value)
                        
                        # Prob that k is satisfying some OTHER clause that forces it
                        # to the OPPOSITE value of what clause i needs.
                        
                        # We need the bias of k excluding clause i
                        phi_pos, phi_neg, phi_star = self._compute_local_biases(k, i, eta, var_to_clauses)
                        
                        # Prob that k provides NO support to clause i:
                        # If clause i needs k=True (lit_k > 0), support is pos.
                        # No support = (phi_neg + phi_star) / (phi_pos + phi_neg + phi_star)
                        if lit_k > 0:
                            term = (phi_neg) / (phi_pos + phi_neg + phi_star + 1e-12)
                        else:
                            term = (phi_pos) / (phi_pos + phi_neg + phi_star + 1e-12)
                        
                        prod_term *= term
                    
                    val = prod_term
                    diff = abs(eta[(i, j)] - val)
                    max_diff = max(max_diff, diff)
                    
                    # Apply damping
                    new_eta[(i, j)] = (1 - self.damping) * val + self.damping * eta[(i, j)]
            
            eta = new_eta
            if max_diff < self.epsilon:
                converged = True
                break
        
        # Compute Final Biases
        results = {}
        for j in range(1, n + 1):
            p_pos, p_neg, p_star = self._compute_local_biases(j, None, eta, var_to_clauses)
            
            total = p_pos + p_neg + p_star + 1e-12
            bias_pos = p_pos / total
            bias_neg = p_neg / total
            bias_star = p_star / total
            
            # Backbone strength: how "non-star" is this variable?
            # Or specifically, if it's very clearly polar
            backbone_strength = max(bias_pos, bias_neg) if bias_star < 0.2 else 0.0
            
            results[j] = {
                "pos": bias_pos,
                "neg": bias_neg,
                "star": bias_star,
                "strength": backbone_strength
            }
            
        return results

    def _compute_local_biases(self, j: int, exclude_clause_idx: Optional[int], 
                             eta: Dict[Tuple[int, int], float], 
                             var_to_clauses: Dict[int, List[Tuple[int, int]]]) -> Tuple[float, float, float]:
        """
        Compute the survey biases for variable j.
        If exclude_clause_idx is provided, ignores that clause (for message update).
        """
        # Product of (1 - eta_i) for clauses where j appears positive
        prod_pos = 1.0
        # Product of (1 - eta_i) for clauses where j appears negative
        prod_neg = 1.0
        
        for i, sign in var_to_clauses[j]:
            if i == exclude_clause_idx:
                continue
            
            e_val = eta.get((i, j), 0.0)
            if sign == 1:
                prod_pos *= (1.0 - e_val)
            else:
                prod_neg *= (1.0 - e_val)
        
        # Equations from Mezard/Zecchina:
        # P_pos = (1 - prod_pos) * prod_neg
        # P_neg = (1 - prod_neg) * prod_pos
        # P_star = prod_pos * prod_neg
        
        p_pos = (1.0 - prod_pos) * prod_neg
        p_neg = (1.0 - prod_neg) * prod_pos
        p_star = prod_pos * prod_neg
        
        return p_pos, p_neg, p_star

    def get_backbone_fraction(self, sp_results: Dict[int, Dict[str, float]], threshold: float = 0.8) -> float:
        """Calculate the percentage of variables in the backbone."""
        n = len(sp_results)
        if n == 0: return 0.0
        
        count = sum(1 for res in sp_results.values() if res["strength"] > threshold)
        return count / n
