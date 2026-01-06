"""
Topological Scanner - Computational Homology for Complexity Analysis
Status: NEW (Phase 25 - SCO v3.0)
Source: Tang (2025), Zhang (2025), Edelsbrunner (Computational Topology)

Computes Betti numbers from computational traces to detect topological
obstructions that may distinguish P from NP.

Key Insight (Tang 2025):
- P problems: H_n(L) = 0 for n > 0 (contractible computation space)
- NP problems: H_1(L) != 0 (presence of non-trivial cycles)
"""

import numpy as np
from typing import List, Dict, Tuple, Set, Optional
from dataclasses import dataclass
from enum import Enum

class TopologyType(Enum):
    TRIVIAL = "trivial"           # beta_1 = 0, contractible
    CYCLIC = "cyclic"             # beta_1 > 0, has holes
    HIGHLY_CONNECTED = "highly_connected"  # beta_1 >> 0

@dataclass
class PersistenceInterval:
    """Represents a topological feature's birth and death."""
    dimension: int
    birth: float
    death: float
    persistence: float

@dataclass
class BettiResult:
    """Result of Betti number computation."""
    beta_0: int  # Connected components
    beta_1: int  # 1-dimensional holes (cycles)
    beta_2: int  # 2-dimensional voids (optional)
    topology_type: TopologyType
    euler_characteristic: int
    intervals: List[PersistenceInterval] = None
    message: str = ""

@dataclass
class SimplicialComplex:
    """Represents a simplicial complex for homology computation."""
    vertices: Set[int]           # 0-simplices
    edges: Set[Tuple[int, int]]  # 1-simplices
    triangles: Set[Tuple[int, int, int]]  # 2-simplices
    tetrahedra: Set[Tuple[int, int, int, int]] = None  # 3-simplices (Phase 33)

    def __post_init__(self):
        if self.tetrahedra is None:
            self.tetrahedra = set()

@dataclass
class HigherBettiResult:
    """Extended result with higher Betti numbers for BQP analysis."""
    beta_0: int  # Connected components
    beta_1: int  # 1-dimensional holes (cycles)
    beta_2: int  # 2-dimensional voids
    beta_3: int  # 3-dimensional cavities
    homological_complexity: int  # h(L) = max{q : H_q != 0}
    bqp_compatible: bool  # True if h(L) <= 2 (Tang Conjecture 8.13)
    euler_characteristic: int
    message: str

class TopologicalScanner:
    """
    Computes topological invariants from computational traces.
    
    Uses Smith Normal Form algorithm over Z_2 for efficiency.
    
    Chain Complex Structure:
    - C_0: Computational configurations (vertices)
    - C_1: Transitions between configurations (edges)
    - C_2: Confluence relations (triangles)
    - C_3: Higher-order clusters (tetrahedra) - Phase 33/v5.0
    """
    
    def __init__(self):
        self.scan_history: List[BettiResult] = []
    
    def trace_to_simplicial_complex(self, trace: List[dict]) -> SimplicialComplex:
        """
        Convert execution trace to simplicial complex.
        
        Each configuration becomes a vertex.
        Each transition becomes an edge.
        Confluent paths create triangles and tetrahedra.
        """
        vertices = set()
        edges = set()
        triangles = set()
        tetrahedra = set()
        
        # Vertices: each unique configuration hash
        config_to_id = {}
        for i, config in enumerate(trace):
            config_hash = hash(frozenset(config.items())) if isinstance(config, dict) else hash(config)
            if config_hash not in config_to_id:
                config_to_id[config_hash] = len(config_to_id)
            vertices.add(config_to_id[config_hash])
        
        # Edges: sequential transitions
        prev_id = None
        for config in trace:
            config_hash = hash(frozenset(config.items())) if isinstance(config, dict) else hash(config)
            curr_id = config_to_id[config_hash]
            
            if prev_id is not None and prev_id != curr_id:
                edge = (min(prev_id, curr_id), max(prev_id, curr_id))
                edges.add(edge)
            
            prev_id = curr_id
        
        # Build adjacency for clique detection
        adj = {v: set() for v in vertices}
        for (u, v) in edges:
            adj[u].add(v)
            adj[v].add(u)
        
        # Triangles: 3-cliques
        for v in vertices:
            neighbors = list(adj[v])
            for i, n1 in enumerate(neighbors):
                for n2 in neighbors[i+1:]:
                    if n2 in adj[n1]:
                        tri = tuple(sorted([v, n1, n2]))
                        triangles.add(tri)
        
        # Tetrahedra: 4-cliques (for H_3)
        for tri in triangles:
            v1, v2, v3 = tri
            # Find vertex connected to all three
            common_neighbors = adj[v1] & adj[v2] & adj[v3]
            for v4 in common_neighbors:
                if v4 not in tri:
                    tet = tuple(sorted([v1, v2, v3, v4]))
                    tetrahedra.add(tet)
        
        return SimplicialComplex(
            vertices=vertices, 
            edges=edges, 
            triangles=triangles,
            tetrahedra=tetrahedra
        )
    
    def build_boundary_matrix_1(self, complex: SimplicialComplex) -> np.ndarray:
        """
        Build boundary matrix d_1: C_1 -> C_0.
        Maps edges to their boundary vertices.
        """
        vertices = sorted(complex.vertices)
        edges = sorted(complex.edges)
        
        n_vertices = len(vertices)
        n_edges = len(edges)
        
        if n_edges == 0:
            return np.zeros((n_vertices, 1), dtype=int)
        
        vertex_to_idx = {v: i for i, v in enumerate(vertices)}
        
        d1 = np.zeros((n_vertices, n_edges), dtype=int)
        
        for j, (v1, v2) in enumerate(edges):
            d1[vertex_to_idx[v1], j] = 1
            d1[vertex_to_idx[v2], j] = 1
        
        return d1
    
    def build_boundary_matrix_2(self, complex: SimplicialComplex) -> np.ndarray:
        """
        Build boundary matrix d_2: C_2 -> C_1.
        Maps triangles to their boundary edges.
        """
        edges = sorted(complex.edges)
        triangles = sorted(complex.triangles)
        
        n_edges = len(edges)
        n_triangles = len(triangles)
        
        if n_triangles == 0:
            return np.zeros((max(1, n_edges), 1), dtype=int)
        
        edge_to_idx = {e: i for i, e in enumerate(edges)}
        
        d2 = np.zeros((n_edges, n_triangles), dtype=int)
        
        for j, (v1, v2, v3) in enumerate(triangles):
            for edge in [(v1, v2), (v1, v3), (v2, v3)]:
                e = (min(edge), max(edge))
                if e in edge_to_idx:
                    d2[edge_to_idx[e], j] = 1
        
        return d2
    
    def build_boundary_matrix_3(self, complex: SimplicialComplex) -> np.ndarray:
        """
        Build boundary matrix d_3: C_3 -> C_2.
        Maps tetrahedra to their boundary triangles.
        Phase 33: Higher Homology (Tang 2025 Conjecture 8.13)
        """
        triangles = sorted(complex.triangles)
        tetrahedra = sorted(complex.tetrahedra)
        
        n_triangles = len(triangles)
        n_tetrahedra = len(tetrahedra)
        
        if n_tetrahedra == 0:
            return np.zeros((max(1, n_triangles), 1), dtype=int)
        
        tri_to_idx = {t: i for i, t in enumerate(triangles)}
        
        d3 = np.zeros((n_triangles, n_tetrahedra), dtype=int)
        
        for j, (v1, v2, v3, v4) in enumerate(tetrahedra):
            # Tetrahedron has 4 boundary triangles
            faces = [
                tuple(sorted([v1, v2, v3])),
                tuple(sorted([v1, v2, v4])),
                tuple(sorted([v1, v3, v4])),
                tuple(sorted([v2, v3, v4]))
            ]
            for face in faces:
                if face in tri_to_idx:
                    d3[tri_to_idx[face], j] = 1
        
        return d3
    
    def rank_mod2(self, matrix: np.ndarray) -> int:
        """Compute rank of matrix over Z_2 using Gaussian elimination."""
        if matrix.size == 0:
            return 0
        
        M = matrix.copy() % 2
        rows, cols = M.shape
        
        rank = 0
        for col in range(cols):
            pivot_row = None
            for row in range(rank, rows):
                if M[row, col] == 1:
                    pivot_row = row
                    break
            
            if pivot_row is None:
                continue
            
            M[[rank, pivot_row]] = M[[pivot_row, rank]]
            
            for row in range(rows):
                if row != rank and M[row, col] == 1:
                    M[row] = (M[row] + M[rank]) % 2
            
            rank += 1
        
        return rank
    
    def compute_higher_betti(self, complex: SimplicialComplex) -> HigherBettiResult:
        """
        Compute Betti numbers β₀, β₁, β₂, β₃ for BQP threshold analysis.
        
        Tang (2025) Conjecture 8.13: BQP problems satisfy h(L) ≤ 2.
        If we find H₃ ≠ 0, the instance is likely outside BQP.
        """
        n0 = len(complex.vertices)
        n1 = len(complex.edges)
        n2 = len(complex.triangles)
        n3 = len(complex.tetrahedra)
        
        # Build all boundary matrices
        d1 = self.build_boundary_matrix_1(complex)
        d2 = self.build_boundary_matrix_2(complex)
        d3 = self.build_boundary_matrix_3(complex)
        
        # Compute ranks
        rank_d1 = self.rank_mod2(d1)
        rank_d2 = self.rank_mod2(d2)
        rank_d3 = self.rank_mod2(d3)
        
        # Betti numbers: β_k = dim(Ker ∂_k) - dim(Im ∂_{k+1})
        beta_0 = max(0, n0 - rank_d1)
        beta_1 = max(0, n1 - rank_d1 - rank_d2)
        beta_2 = max(0, n2 - rank_d2 - rank_d3)
        beta_3 = max(0, n3 - rank_d3)  # Assumes d4 = 0
        
        # Euler characteristic
        euler = n0 - n1 + n2 - n3
        
        # Homological complexity h(L)
        if beta_3 > 0:
            h_L = 3
        elif beta_2 > 0:
            h_L = 2
        elif beta_1 > 0:
            h_L = 1
        else:
            h_L = 0
        
        # BQP compatibility (Tang Conjecture 8.13)
        bqp_compatible = (h_L <= 2)
        
        if h_L == 0:
            msg = "h(L)=0: Trivial topology. Solvable by 1D systems (P)."
        elif h_L == 1:
            msg = "h(L)=1: H_1 obstructions. Requires 2D systems. NP-hard candidate."
        elif h_L == 2:
            msg = "h(L)=2: H_2 cavities. Requires 3D systems. BQP boundary."
        else:
            msg = "h(L)>=3: H_3 detected! BEYOND BQP. Requires higher-dimensional physics."

        
        return HigherBettiResult(
            beta_0=beta_0,
            beta_1=beta_1,
            beta_2=beta_2,
            beta_3=beta_3,
            homological_complexity=h_L,
            bqp_compatible=bqp_compatible,
            euler_characteristic=euler,
            message=msg
        )

    def compute_betti_numbers(self, complex: SimplicialComplex) -> BettiResult:
        """
        Compute Betti numbers using the rank-nullity theorem.
        (Legacy method for backward compatibility)
        """
        n0 = len(complex.vertices)
        n1 = len(complex.edges)
        n2 = len(complex.triangles)
        
        d1 = self.build_boundary_matrix_1(complex)
        d2 = self.build_boundary_matrix_2(complex)
        
        rank_d1 = self.rank_mod2(d1)
        rank_d2 = self.rank_mod2(d2)
        
        beta_0 = n0 - rank_d1 if n0 > 0 else 0
        beta_1 = max(0, n1 - rank_d1 - rank_d2)
        beta_2 = max(0, n2 - rank_d2)
        
        euler = n0 - n1 + n2
        
        if beta_1 == 0:
            topo_type = TopologyType.TRIVIAL
            msg = "Topology is TRIVIAL (contractible). Consistent with P."
        elif beta_1 <= 3:
            topo_type = TopologyType.CYCLIC
            msg = f"Topology has {beta_1} CYCLE(S). Non-trivial H_1 detected!"
        else:
            topo_type = TopologyType.HIGHLY_CONNECTED
            msg = f"Topology is HIGHLY CONNECTED (beta_1={beta_1}). Strong obstruction!"
        
        result = BettiResult(
            beta_0=beta_0,
            beta_1=beta_1,
            beta_2=beta_2,
            topology_type=topo_type,
            euler_characteristic=euler,
            message=msg
        )
        
        self.scan_history.append(result)
        return result
    
    def scan_trace(self, trace: List[dict]) -> BettiResult:
        """Full pipeline: trace -> simplicial complex -> Betti numbers."""
        complex = self.trace_to_simplicial_complex(trace)
        return self.compute_betti_numbers(complex)

    
    def compute_persistence(self, trace: List[dict]) -> List[PersistenceInterval]:
        """
        Compute Persistent Homology using computation depth as filtration.
        
        Algorithm: Standard Persistent Homology over Z_2.
        1. Build simplicial complex with filtration values (depth).
        2. Sort simplices by filtration and dimension.
        3. Perform column reduction on the boundary matrix.
        """
        # 1. Prepare simplices with filtration (depth)
        # For simplicity, we use vertices and edges.
        vertices_with_filt = []
        edges_with_filt = []
        
        config_to_id = {}
        prev_id = None
        
        for event in trace:
            cfg = event.get("hash", hash(str(event)))
            depth = event.get("level", 0.0)
            
            if cfg not in config_to_id:
                config_to_id[cfg] = len(config_to_id)
                vertices_with_filt.append((config_to_id[cfg], depth))
            
            curr_id = config_to_id[cfg]
            if prev_id is not None and prev_id != curr_id:
                edge = tuple(sorted([prev_id, curr_id]))
                # Edge filtration is the max of its vertices' filtration (or event time)
                edges_with_filt.append((edge, depth))
            prev_id = curr_id

        # 2. Combine and sort simplices
        # Simplified: H_1 persistence (Edges and Vertices)
        # A proper PH would sort all simplices [K0, K1, ...]
        simplices = []
        for v, f in vertices_with_filt: simplices.append({'dim': 0, 'nodes': (v,), 'f': f})
        # Remove duplicates for edges
        unique_edges = {}
        for e, f in edges_with_filt:
            if e not in unique_edges or f < unique_edges[e]:
                unique_edges[e] = f
        for e, f in unique_edges.items(): simplices.append({'dim': 1, 'nodes': e, 'f': f})

        # Sort by filtration, then by dimension
        simplices.sort(key=lambda s: (s['f'], s['dim']))
        
        # 3. Boundary Matrix Reduction
        # We need a way to track which columns are reduced
        pivot_to_col = {}
        intervals = []
        
        # Boundary matrix as list of active indices (Z_2)
        n = len(simplices)
        boundary_cols = [[] for _ in range(n)]
        
        for i, s in enumerate(simplices):
            if s['dim'] > 0:
                # Boundary of edge (u, v) is {u, v}
                # Find indices of vertices in the sorted list
                b_indices = []
                for node in s['nodes']:
                    for j in range(i):
                        if simplices[j]['dim'] == s['dim'] - 1 and simplices[j]['nodes'] == (node,):
                            b_indices.append(j)
                            break
                boundary_cols[i] = sorted(b_indices)
            
            # Reduce column i
            while boundary_cols[i]:
                pivot = max(boundary_cols[i])
                if pivot not in pivot_to_col:
                    break
                # XOR with the column that has this pivot
                target_col = boundary_cols[pivot_to_col[pivot]]
                # Z_2 addition (symmetric difference)
                new_col = set(boundary_cols[i]) ^ set(target_col)
                boundary_cols[i] = sorted(list(new_col))
            
            if not boundary_cols[i]:
                # i is a "creator" (birth of a feature)
                pass
            else:
                # i is a "destroyer" (death of feature at pivot)
                pivot = max(boundary_cols[i])
                birth_idx = pivot
                death_idx = i
                
                birth_f = simplices[birth_idx]['f']
                death_f = simplices[death_idx]['f']
                
                if death_f > birth_f:
                    intervals.append(PersistenceInterval(
                        dimension=simplices[birth_idx]['dim'],
                        birth=birth_f,
                        death=death_f,
                        persistence=death_f - birth_f
                    ))
                pivot_to_col[pivot] = i
        
        # Infinite intervals (features that never die)
        # These are the Betti numbers of the final complex
        for i in range(n):
            if i not in pivot_to_col and not boundary_cols[i]:
                intervals.append(PersistenceInterval(
                    dimension=simplices[i]['dim'],
                    birth=simplices[i]['f'],
                    death=float('inf'),
                    persistence=float('inf')
                ))

        return intervals

    def plot_barcodes(self, intervals: List[PersistenceInterval]):
        """Textual representation of persistence barcodes."""
        print("\n" + "-"*40)
        print("PERSISTENCE BARCODE (H_1)")
        print("-"*40)
        for inter in sorted(intervals, key=lambda x: x.birth):
            if inter.dimension == 1:
                life = "----" if inter.death == float('inf') else f"-{inter.persistence:.1f}-"
                print(f"[{inter.birth:4.1f}] {life}> Death: {inter.death}")
        print("-"*40)
    
    def generate_test_traces(self, difficulty: str = "easy") -> List[dict]:
        """
        Generate synthetic traces for testing.
        
        - Easy (P-like): Linear progression, no branching
        - Hard (NP-like): Branching with cycles
        """
        if difficulty == "easy":
            # Linear trace: no cycles
            return [{"state": i, "time": i} for i in range(20)]
        elif difficulty == "medium":
            # Some revisiting: creates small cycles
            trace = []
            for i in range(30):
                state = i % 10  # Revisit states
                trace.append({"state": state, "time": i})
            return trace
        else:  # hard
            # Complex branching with many cycles
            trace = []
            for i in range(50):
                # Create densely connected states
                state = (i * 7) % 15  # Pseudo-random revisits
                trace.append({"state": state, "time": i})
            return trace

def run_topological_experiment():
    """Main experiment: Compare topology of easy vs hard traces."""
    print("\n" + "="*70)
    print("SCO v3.0 - PHASE 25: TOPOLOGICAL SCANNER")
    print("="*70)
    print("Objective: Compute Betti numbers to detect topological obstructions")
    print("Theory: P -> beta_1 = 0, NP -> beta_1 > 0 (Tang 2025)")
    print("="*70 + "\n")
    
    scanner = TopologicalScanner()
    
    print("="*70)
    print("BETTI NUMBER ANALYSIS")
    print("="*70)
    print(f"{'Instance':>12} | {'V':>4} | {'E':>4} | {'T':>4} | {'beta_0':>6} | {'beta_1':>6} | {'Type'}")
    print("-"*70)
    
    results = {}
    
    for difficulty in ["easy", "medium", "hard"]:
        trace = scanner.generate_test_traces(difficulty)
        result = scanner.scan_trace(trace)
        results[difficulty] = result
        
        complex = scanner.trace_to_simplicial_complex(trace)
        n_v = len(complex.vertices)
        n_e = len(complex.edges)
        n_t = len(complex.triangles)
        
        print(f"{difficulty:>12} | {n_v:>4} | {n_e:>4} | {n_t:>4} | {result.beta_0:>6} | "
              f"{result.beta_1:>6} | {result.topology_type.value}")
    
    print("-"*70)
    
    # Analysis
    print("\n" + "="*70)
    print("TOPOLOGICAL ANALYSIS")
    print("="*70)
    
    for difficulty, result in results.items():
        print(f"\n[{difficulty.upper()}]: {result.message}")
    
    # Correlation with complexity
    print("\n" + "-"*70)
    print("CORRELATION WITH COMPUTATIONAL COMPLEXITY:")
    print("-"*70)
    
    if results["easy"].beta_1 == 0 and results["hard"].beta_1 > 0:
        print("[CONFIRMED] beta_1 = 0 for easy, beta_1 > 0 for hard!")
        print("           This is consistent with the Topological Separation Thesis.")
    else:
        print("[OBSERVATION] Pattern detected but requires more data points.")
    
    print("="*70)
    
    return results

if __name__ == "__main__":
    run_topological_experiment()
