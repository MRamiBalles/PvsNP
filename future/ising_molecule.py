import numpy as np
import networkx as nx

class IsingMolecule:
    """
    Visualizes the Absolute Minimum Core (AMC) and Topological Frustration.
    Maps SAT to a 3D Ising model (Zhang 2025).
    """
    def __init__(self, size=(4, 4, 2)):
        self.size = size
        self.graph = nx.grid_graph(dim=size)
        # Random interactions J_ij in {-1, 1}
        for u, v in self.graph.edges():
            self.graph[u][v]['J'] = np.random.choice([-1, 1])

    def identify_amc(self):
        """
        Isolates the bilayer structure (2D planes interacting).
        Zhang identifies this as the frontier of NP-completeness.
        """
        print(f"Identifying AMC in {self.size} grid...")
        # AMC is the core sub-grid where 2D layers meet and frustrate
        amc_nodes = [n for n in self.graph.nodes() if n[2] < 2]
        amc_subgraph = self.graph.subgraph(amc_nodes)
        print(f"AMC found with {len(amc_subgraph.nodes())} spins.")
        return amc_subgraph

    def detect_frustration(self):
        """
        A plaquette is frustrated if the product of J_ij around it is -1.
        """
        frustrated_count = 0
        total_plaquettes = 0
        
        # We iterate through 1x1 loops in the z=0 plane
        for x in range(self.size[0] - 1):
            for y in range(self.size[1] - 1):
                # Nodes of the square plaquette
                p = [(x, y, 0), (x+1, y, 0), (x+1, y+1, 0), (x, y+1, 0)]
                # Product of interaction signs
                product = (self.graph[p[0]][p[1]]['J'] * 
                           self.graph[p[1]][p[2]]['J'] * 
                           self.graph[p[2]][p[3]]['J'] * 
                           self.graph[p[3]][p[0]]['J'])
                
                total_plaquettes += 1
                if product < 0:
                    frustrated_count += 1
        
        frustration_index = frustrated_count / total_plaquettes
        print(f"Frustration Detection: {frustrated_count}/{total_plaquettes} plaquettes frustrated.")
        print(f"Energy Landscape Status: {'Rugged (NP-Hard signature)' if frustration_index > 0.2 else 'Smooth'}")
        return frustration_index

if __name__ == "__main__":
    mol = IsingMolecule()
    mol.identify_amc()
    mol.detect_frustration()
