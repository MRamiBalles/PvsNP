"""
Arithmetizer - SCO v5.0
Status: NEW (Phase 32)
Source: Aaronson & Wigderson, "Algebrization: A New Barrier"

Transforms Boolean CNF instances into polynomial representations over Finite Fields.
Used to test if topological invariants are specific to the Boolean structure.
"""

import numpy as np
from typing import List, Tuple

class Arithmetizer:
    """
    Handles the 'lifting' of SAT instances to polynomials.
    """
    
    def __init__(self, field_size: int = 127):
        self.q = field_size # Prime for GF(q)
        
    def arithmetize_clause(self, clause: List[int]) -> callable:
        """Returns a function representing the polynomial of the clause."""
        def p(assignment: dict):
            prod = 1
            for lit in clause:
                var = abs(lit)
                val = assignment.get(var, 0)
                v_poly = val if lit > 0 else (1 - val)
                prod = (prod * (1 - v_poly)) % self.q
            return (1 - prod) % self.q
        return p

    def arithmetize_instance(self, clauses: List[List[int]]) -> callable:
        """Returns the full polynomial P(x) = Product of clauses."""
        def full_p(assignment: dict):
            res = 1
            for clause in clauses:
                c_poly = self.arithmetize_clause(clause)
                res = (res * c_poly(assignment)) % self.q
            return res
        return full_p

    def additive_arithmetize_instance(self, clauses: List[List[int]]) -> callable:
        """Returns the 'Energy' polynomial E(x) = Sum of clauses."""
        def energy_p(assignment: dict):
            res = 0
            for clause in clauses:
                c_poly = self.arithmetize_clause(clause)
                res = (res + c_poly(assignment)) % self.q
            return res
        return energy_p

    def trace_polynomial_evaluation(self, clauses: List[List[int]], path: List[dict], mode: str = "multiplicative") -> List[dict]:
        """
        Generates a trace of evaluating the polynomial extension along a computational path.
        """
        poly_trace = []
        poly_func = self.arithmetize_instance(clauses) if mode == "multiplicative" else self.additive_arithmetize_instance(clauses)
        
        for state in path:
            assignment = state.get("assignment", {})
            step_data = {"assignment": assignment.copy()}
            step_data["val"] = poly_func(assignment)
            poly_trace.append(step_data)
        return poly_trace
