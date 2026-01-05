import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engines.metemath.refuter_game import RefuterGame

def test_refuter_rwphp():
    print("Executing Test: Refuter Game rwPHP(PLS) Collision Search...")
    # Small size for deterministic collision
    game = RefuterGame(5)
    
    # In a mapping from [6] -> [5], a collision MUST exist (Pigeonhole Principle)
    success, errors = game.propose_proof("Candidate-Proof-002")
    
    if success and len(errors) > 0:
        print(f"[SUCCESS] Collision found: {errors[0]}")
        return True
    else:
        print("[FAILURE] No collision found in a guaranteed space.")
        return False

if __name__ == "__main__":
    test_refuter_rwphp()
