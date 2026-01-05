"""
Complex Builder Module
Constructs computation complexes from machine configurations.
Based on Tang (2025): Topological Obstructions in Computational Complexity.
"""

import numpy as np
from itertools import combinations

class ComputationChain:
    """
    Represents a chain in the computation complex.
    
    A chain is a formal sum of simplices with coefficients in Z_2.
    For computational purposes, we represent chains as sets of simplices.
    """
    def __init__(self, simplices=None):
        self.simplices = set(simplices) if simplices else set()
    
    def __add__(self, other):
        # Over Z_2, addition is symmetric difference (XOR)
        return ComputationChain(self.simplices ^ other.simplices)
    
    def __repr__(self):
        return f"Chain({self.simplices})"


class ComplexBuilder:
    """
    Builds the computation complex K(M) for a machine M.
    
    The complex captures the topology of the computation space:
    - 0-simplices: configurations
    - 1-simplices: valid transitions
    - n-simplices: computation paths
    """
    
    def __init__(self):
        self.vertices = []      # C_0: configurations
        self.edges = []         # C_1: transitions
        self.faces = []         # C_2: 2-paths (triangles)
        self.vertex_index = {}  # configuration -> index mapping
        
    def add_configuration(self, config):
        """Add a 0-simplex (configuration) to the complex."""
        if config not in self.vertex_index:
            idx = len(self.vertices)
            self.vertices.append(config)
            self.vertex_index[config] = idx
        return self.vertex_index[config]
    
    def add_transition(self, config_from, config_to):
        """Add a 1-simplex (transition) to the complex."""
        idx_from = self.add_configuration(config_from)
        idx_to = self.add_configuration(config_to)
        edge = (idx_from, idx_to)
        if edge not in self.edges:
            self.edges.append(edge)
        return edge
    
    def add_path(self, path):
        """Add an n-simplex (computation path) to the complex."""
        indices = [self.add_configuration(c) for c in path]
        # Add all edges along the path
        for i in range(len(indices) - 1):
            self.add_transition(path[i], path[i+1])
        # If path length >= 3, record as a face
        if len(indices) >= 3:
            for i in range(len(indices) - 2):
                face = (indices[i], indices[i+1], indices[i+2])
                if face not in self.faces:
                    self.faces.append(face)
        return tuple(indices)
    
    def build_from_sat(self, num_vars, clauses):
        """
        Build complex from a SAT formula.
        
        Vertices are truth assignments (2^n configurations).
        Edges connect assignments differing by one bit.
        Faces are 4-cycles in the hypercube (for 2D slices).
        """
        n = num_vars
        num_configs = 2 ** n
        
        # Add all configurations
        for i in range(num_configs):
            assignment = tuple((i >> j) & 1 for j in range(n))
            self.add_configuration(assignment)
        
        # Add edges (single bit flips)
        for i in range(num_configs):
            for bit in range(n):
                j = i ^ (1 << bit)
                if i < j:
                    config_i = tuple((i >> k) & 1 for k in range(n))
                    config_j = tuple((j >> k) & 1 for k in range(n))
                    self.add_transition(config_i, config_j)
        
        # Add faces (4-cycles from 2-bit flips)
        for i in range(num_configs):
            for b1 in range(n):
                for b2 in range(b1 + 1, n):
                    # Square: i -> i^b1 -> i^b1^b2 -> i^b2 -> i
                    v0 = i
                    v1 = i ^ (1 << b1)
                    v2 = v1 ^ (1 << b2)
                    v3 = i ^ (1 << b2)
                    # Store as list of edge indices for boundary computation
                    c0 = tuple((v0 >> k) & 1 for k in range(n))
                    c1 = tuple((v1 >> k) & 1 for k in range(n))
                    c2 = tuple((v2 >> k) & 1 for k in range(n))
                    c3 = tuple((v3 >> k) & 1 for k in range(n))
                    face_edges = [
                        (self.vertex_index[c0], self.vertex_index[c1]),
                        (self.vertex_index[c1], self.vertex_index[c2]),
                        (self.vertex_index[c2], self.vertex_index[c3]),
                        (self.vertex_index[c3], self.vertex_index[c0])
                    ]
                    self.faces.append(face_edges)
        
        return self
    
    def get_boundary_matrix_d1(self):
        """
        Compute the boundary matrix d_1: C_1 -> C_0.
        
        Entry (i, j) is 1 if vertex i is a boundary of edge j.
        Over Z_2, each edge has exactly 2 boundary vertices.
        """
        num_vertices = len(self.vertices)
        num_edges = len(self.edges)
        
        matrix = np.zeros((num_vertices, num_edges), dtype=np.int8)
        for j, (v_from, v_to) in enumerate(self.edges):
            matrix[v_from, j] = 1
            matrix[v_to, j] = 1
        
        return matrix % 2
    
    def get_stats(self):
        return {
            "vertices": len(self.vertices),
            "edges": len(self.edges),
            "faces": len(self.faces)
        }


if __name__ == "__main__":
    print("--- Complex Builder Test ---")
    
    # Build complex for 2-variable SAT (hypercube)
    builder = ComplexBuilder()
    builder.build_from_sat(2, [])
    
    stats = builder.get_stats()
    print(f"Vertices (C_0): {stats['vertices']}")
    print(f"Edges (C_1): {stats['edges']}")
    print(f"Faces (C_2): {stats['faces']}")
    
    d1 = builder.get_boundary_matrix_d1()
    print(f"Boundary Matrix d_1 shape: {d1.shape}")
