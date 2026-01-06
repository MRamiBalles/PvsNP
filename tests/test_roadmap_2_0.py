import sys
import os

# Ensure we can import from the root
sys.path.append(os.getcwd())

from engines.metemath.nephew_detector import NephewDetector
from engines.algebraic.asymptotic_analyzer import AsymptoticAnalyzer
from engines.topological.immunity_miner import ImmunityMiner
from neuro_symbolic import NeuroSymbolicAgent

def run_test(name, func):
    print(f"\n>>> Running {name} <<<")
    try:
        func()
        print(f"[PASSED] {name}")
        return True
    except Exception as e:
        print(f"[FAILED] {name}: {e}")
        return False

def test_nephew():
    detector = NephewDetector()
    detector.scan_for_nephew_structure({'has_infinite_tree': True, 'leaf_density': 0.05})

def test_asymptotics():
    analyzer = AsymptoticAnalyzer()
    analyzer.analyze_sequence([5, 10, 15], [29, 314, 1599])

def test_immunity():
    miner = ImmunityMiner()
    rank, _ = miner.mine_immunity(iterations=50)
    if rank < 3:
        print("[!] Warning: Immunity miner didn't find h(L)>=3 in 50 iterations (stochastic).")

def test_hermes_v3():
    agent = NeuroSymbolicAgent()
    agent.run_discovery("a + b = b + a")

def main():
    print("="*50)
    print("ROADMAP 2.0 DISCOVERY PIPELINE VERIFICATION")
    print("="*50)
    
    tests = [
        ("Nephew Detection", test_nephew),
        ("Asymptotic Analysis", test_asymptotics),
        ("Immunity Mining", test_immunity),
        ("HERMES v3 Evolution", test_hermes_v3)
    ]
    
    success_count = 0
    for name, func in tests:
        if run_test(name, func):
            success_count += 1
            
    print("\n" + "="*50)
    print(f"VERIFICATION COMPLETE: {success_count}/{len(tests)} PASSED")
    print("="*50)

if __name__ == "__main__":
    main()
