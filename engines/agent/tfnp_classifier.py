"""
TFNP Classifier - Metamathematical Strategy Advisor
Based on: Li et al. (2024) - TFNP complexity hierarchy

This module links the theoretical TFNP classification to the agent's
proof strategy, enabling targeted tactic selection based on problem class.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict

@dataclass
class TFNPClassification:
    problem_class: str
    recommended_tactics: List[str]
    difficulty_estimate: str
    metamath_notes: str

class TFNPClassifier:
    """
    Phase 16: Links TFNP theory to agent proof strategies.
    Based on: Li et al. (2024) - Metamathematical scaling
    
    When the agent encounters a goal, this classifier determines
    which TFNP class it likely belongs to and recommends strategies.
    """
    
    def __init__(self):
        # TFNP class -> recommended tactics/strategies
        self.class_strategies = {
            "PLS": {
                "tactics": ["induction", "well_founded_rec", "decreasing"],
                "difficulty": "medium",
                "notes": "PLS = Polynomial Local Search. Use induction on potential functions."
            },
            "PPA": {
                "tactics": ["cases", "match", "parity_arg"],
                "difficulty": "medium",
                "notes": "PPA = Polynomial Parity Argument. Try case analysis on graph structures."
            },
            "PPP": {
                "tactics": ["pigeonhole", "exists_collision", "funext"],
                "difficulty": "hard",
                "notes": "PPP = Polynomial Pigeonhole Principle. NOT Turing-closed under black-box."
            },
            "PPAD": {
                "tactics": ["fixed_point", "brouwer", "sperner"],
                "difficulty": "hard",
                "notes": "PPAD = Polynomial Path Argument Directed. Fixed-point existence."
            },
            "TFZPP": {
                "tactics": ["random_res", "tree_eval", "compression"],
                "difficulty": "hard",
                "notes": "TFZPP = Total FZP Problems. BLACK_BOX ONLY hardness."
            },
            "rwPHP_PLS": {
                "tactics": ["random_restriction", "resolution_refutation"],
                "difficulty": "expert",
                "notes": "Random Resolution lower bounds. Very sparse rewards."
            }
        }
        
        # Keyword-based classification heuristics
        self.keywords = {
            "local minimum": "PLS",
            "potential function": "PLS",
            "parity": "PPA",
            "odd degree": "PPA",
            "pigeonhole": "PPP",
            "collision": "PPP",
            "fixed point": "PPAD",
            "equilibrium": "PPAD",
            "random oracle": "TFZPP",
            "resolution": "rwPHP_PLS"
        }
    
    def classify(self, goal: str) -> TFNPClassification:
        """
        Classify a goal into a TFNP class and recommend strategies.
        """
        print(f"\n--- TFNP Classification ---")
        print(f"[TFNP] Analyzing: {goal[:60]}...")
        
        # Keyword-based classification
        goal_lower = goal.lower()
        detected_class = "UNKNOWN"
        
        for keyword, tfnp_class in self.keywords.items():
            if keyword in goal_lower:
                detected_class = tfnp_class
                print(f"[TFNP] Keyword '{keyword}' detected -> {tfnp_class}")
                break
        
        if detected_class == "UNKNOWN":
            # Default to PLS for most induction-style proofs
            detected_class = "PLS"
            print(f"[TFNP] No specific keywords, defaulting to PLS")
        
        strategy = self.class_strategies.get(detected_class, {
            "tactics": ["simp", "ring", "aesop"],
            "difficulty": "unknown",
            "notes": "Generic tactics"
        })
        
        result = TFNPClassification(
            problem_class=detected_class,
            recommended_tactics=strategy["tactics"],
            difficulty_estimate=strategy["difficulty"],
            metamath_notes=strategy["notes"]
        )
        
        print(f"[TFNP] Classification: {result.problem_class}")
        print(f"[TFNP] Recommended tactics: {result.recommended_tactics}")
        print(f"[TFNP] Difficulty: {result.difficulty_estimate}")
        
        return result
    
    def get_strategy_hint(self, classification: TFNPClassification) -> str:
        """Generate a natural language strategy hint for the agent."""
        hints = {
            "PLS": "Try induction with a decreasing measure. Look for invariants.",
            "PPA": "Use case analysis. The problem likely involves parity arguments.",
            "PPP": "Apply pigeonhole principle. Find a collision point.",
            "PPAD": "Look for fixed-point theorems. Try Brouwer or Sperner.",
            "TFZPP": "Warning: Only hard under black-box access. Check oracle opacity.",
            "rwPHP_PLS": "Expert level. Use random restrictions on resolution proofs."
        }
        return hints.get(classification.problem_class, "Use generic proof search.")

if __name__ == "__main__":
    classifier = TFNPClassifier()
    
    # Test classifications
    classifier.classify("Prove that every function has a local minimum")
    classifier.classify("Show that there exists a collision in the hash function")
    classifier.classify("Find a fixed point of the continuous function f")
    classifier.classify("Prove the sum of first n numbers equals n*(n+1)/2")
