import numpy as np
import sys
import os

# Ensure we can import from the root
sys.path.append(os.getcwd())

from future.ising_molecule import IsingMolecule

def test_2sat_vs_3sat_physics():
    print("\n--- Physics Control: 2-SAT vs 3-SAT (AMC Frustration) ---")
    
    # 2-SAT Simulation: Symmetric/Non-Frustrated interactions
    print("\n[Simulating 2-SAT Landscape]")
    mol_2sat = IsingMolecule(size=(4, 4, 2))
    # Override J to be +1 (Ferromagnetic = No Frustration)
    for u, v in mol_2sat.graph.edges():
        mol_2sat.graph[u][v]['J'] = 1
    
    frust_2sat = mol_2sat.detect_frustration()
    
    # 3-SAT Simulation: Random/Frustrated interactions
    print("\n[Simulating 3-SAT Landscape]")
    mol_3sat = IsingMolecule(size=(4, 4, 2))
    # Random J in {-1, 1} creates frustration
    for u, v in mol_3sat.graph.edges():
        mol_3sat.graph[u][v]['J'] = np.random.choice([-1, 1])
        
    frust_3sat = mol_3sat.detect_frustration()
    
    print("\n" + "="*50)
    print(f"2-SAT Frustration Index: {frust_2sat}")
    print(f"3-SAT Frustration Index: {frust_3sat}")
    
    # Success Criteria: 2-SAT must be significantly lower than 3-SAT
    if frust_2sat < 0.1 and frust_3sat > 0.2:
        print("[PASSED] Physics correctly distinguishes 2-SAT vs 3-SAT.")
        return True
    else:
        print("[FAILED] Physics Indistinguishability detected (Aaronson-Tao Trap).")
        return False

if __name__ == "__main__":
    test_2sat_vs_3sat_physics()
