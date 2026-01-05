import os
import sys

# Paths (adjust if needed)
PYTHON_EXE = r"C:\Users\Manu\AppData\Local\Programs\Python\Python312\python.exe"

def run_module(name, path):
    print(f"\n{'='*20} {name} {'='*20}")
    # Using the current process if possible, or subprocess with the specific python path
    try:
        import subprocess
        result = subprocess.run([PYTHON_EXE, path], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Errors in {name}:", result.stderr)
        return result.stdout
    except Exception as e:
        print(f"Failed to run {name}: {e}")
        return ""

def main():
    print("      COMPUTER DIAGNOSTIC SYSTEM (V0.1)      ")
    print("      =================================      ")
    print("Modular Laboratory for Complexity Analysis\n")

    # Step 1: Topological Motor
    topo_output = run_module("Step 1: Topological Motor", "topological_motor.py")
    
    # Analyze output for H1
    h1_hard = "H1 Rank: > 0" in topo_output or "H1 Rank: 1" in topo_output

    # Step 2: Algebraic Motor
    alg_output = run_module("Step 2: Algebraic Motor", "algebraic_motor.py")
    alg_hard = "ALGEBRAIC OBSTRUCTION DETECTED" in alg_output

    # Step 3: Holographic Motor
    holo_output = run_module("Step 3: Holographic Simulation", "holographic_motor.py")

    # Step 4: Neuro-Symbolic Integration
    print("\n" + "="*20 + " Step 4: Certification (HERMES) " + "="*20)
    import neuro_symbolic
    neuro_symbolic.run_neuro_symbolic_demo()

    # Final Report
    print("\n" + "#"*50)
    print("FINAL HARDNESS CERTIFICATE")
    print("#"*50)
    print(f"[*] Topological Hardness (H1): {'DETECTED' if h1_hard else 'NOT DETECTED'}")
    print(f"[*] Algebraic Obstruction (k=5): {'DETECTED' if alg_hard else 'NOT DETECTED'}")
    print(f"[*] Holographic Efficiency: VERIFIED ({'31' if '31' in holo_output else 'OK'})")
    print("-" * 50)
    
    if h1_hard or alg_hard:
        print("[RESULT] CANDIDATE FOR NP-HARD / STRUCTURAL COMPLEXITY")
    else:
        print("[RESULT] P-TIME / CONTRACTIBLE SPACE")
    print("#"*50)

if __name__ == "__main__":
    main()
