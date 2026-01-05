import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engines.algebraic.kronecker import KroneckerMotor

def test_k5_anomaly():
    print("Executing Test: k=5 Algebraic Anomaly Detection...")
    km = KroneckerMotor()
    
    # Check k=4 (Stable)
    is_obs4, act4, pred4 = km.analyze_threshold(4)
    if is_obs4:
        print("[FAILURE] False positive at k=4")
        return False
        
    # Check k=5 (Anomaly)
    is_obs5, act5, pred5 = km.analyze_threshold(5)
    if is_obs5 and act5 == 260 and pred5 == 231:
        print("[SUCCESS] Detected +29 Correction (Lee 2025).")
        return True
    else:
        print("[FAILURE] Failed to detect k=5 structural deviation.")
        return False

if __name__ == "__main__":
    test_k5_anomaly()
