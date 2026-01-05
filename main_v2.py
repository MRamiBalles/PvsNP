import os
import sys

# Add root to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

PYTHON_EXE = r"C:\Users\Manu\AppData\Local\Programs\Python\Python312\python.exe"

def run_test(path):
    import subprocess
    print(f"\nRunning {os.path.basename(path)}...")
    result = subprocess.run([PYTHON_EXE, path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("ERROR:", result.stderr)
    return result.returncode == 0

def main():
    print("="*60)
    print("   SYSTEMA DE DIAGN\u00d3STICO COMPUTACIONAL - FASE 2: ESCALAMIENTO")
    print("="*60)
    
    tests = [
        "tests/test_memory_restore.py",
        "tests/test_k5_anomaly.py",
        "tests/test_refuter_rwphp.py"
    ]
    
    all_passed = True
    for test in tests:
        if not run_test(test):
            all_passed = False
            
    print("\n" + "#"*60)
    if all_passed:
        print("PHASE 2 CERTIFICATION: VERIFIED")
        print("M\u00d3DULOS HOLOGR\u00c1FICO, ALGEBRAICO Y METAMATEM\u00c1TICO OPERATIVOS")
    else:
        print("PHASE 2 CERTIFICATION: FAILED")
    print("#"*60)

if __name__ == "__main__":
    main()
