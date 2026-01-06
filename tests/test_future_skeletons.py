import os
import subprocess

def run_test(name, path):
    print(f"\n--- Testing {name} ---")
    try:
        # Use simple python call
        result = subprocess.run(["python", path], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Errors in {name}:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Failed to run {name}: {e}")
        return False

def main():
    success = True
    # Test new modules
    modules = [
        ("Topological Crypto", "future/topological_crypto.py"),
        ("Catalytic Hardware", "future/catalytic_hardware.py"),
        ("Ising Molecule", "future/ising_molecule.py"),
        ("Neuro-Symbolic Agent", "neuro_symbolic.py")
    ]
    
    for name, path in modules:
        if not run_test(name, path):
            success = False
            print(f"!!! {name} FAILED !!!")
        else:
            print(f"[*] {name} PASSED")
            
    if success:
        print("\nALL POST-RESOLUTION SKELETONS VERIFIED SUCCESSFULLY.")
    else:
        print("\nSOME TESTS FAILED.")

if __name__ == "__main__":
    main()
