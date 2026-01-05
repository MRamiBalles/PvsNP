"""
Homology Computation Module
Calculates H_1 using Smith Normal Form over Z_2.
Based on Tang (2025): Topological Obstructions in Computational Complexity.
"""

import numpy as np
from scipy.sparse import csr_matrix
import networkx as nx


def smith_normal_form_z2(matrix):
    """
    Compute the Smith Normal Form of a matrix over Z_2.
    
    Returns the rank (number of 1s on diagonal after reduction).
    This is equivalent to Gaussian elimination over GF(2).
    """
    if matrix.size == 0:
        return 0
    
    A = matrix.copy() % 2
    nrows, ncols = A.shape
    rank = 0
    pivot_row = 0
    
    for col in range(ncols):
        if pivot_row >= nrows:
            break
        
        # Find pivot in current column
        pivot = -1
        for row in range(pivot_row, nrows):
            if A[row, col] == 1:
                pivot = row
                break
        
        if pivot == -1:
            continue  # No pivot in this column
        
        # Swap rows
        A[[pivot_row, pivot]] = A[[pivot, pivot_row]]
        
        # Eliminate other entries in this column
        for row in range(nrows):
            if row != pivot_row and A[row, col] == 1:
                A[row] = (A[row] + A[pivot_row]) % 2
        
        pivot_row += 1
        rank += 1
    
    return rank


def compute_kernel_dimension(matrix):
    """
    Compute dim(ker(matrix)) = #columns - rank(matrix).
    """
    if matrix.size == 0:
        return 0
    rank = smith_normal_form_z2(matrix)
    return matrix.shape[1] - rank


def compute_image_dimension(matrix):
    """
    Compute dim(im(matrix)) = rank(matrix).
    """
    if matrix.size == 0:
        return 0
    return smith_normal_form_z2(matrix)


class HomologyCalculator:
    """
    Computes homology groups of computation complexes.
    
    H_n = ker(d_n) / im(d_{n+1})
    dim(H_n) = dim(ker(d_n)) - dim(im(d_{n+1}))
    """
    
    def __init__(self, vertices, edges, faces=None):
        self.vertices = vertices
        self.edges = edges
        self.faces = faces if faces else []
        self.num_vertices = len(vertices)
        self.num_edges = len(edges)
        
    def _build_d1_matrix(self):
        """Build boundary matrix d_1: C_1 -> C_0."""
        if self.num_edges == 0:
            return np.array([]).reshape(self.num_vertices, 0)
        
        matrix = np.zeros((self.num_vertices, self.num_edges), dtype=np.int8)
        for j, edge in enumerate(self.edges):
            matrix[edge[0], j] = 1
            matrix[edge[1], j] = 1
        return matrix % 2
    
    def _build_d2_matrix(self):
        """
        Build boundary matrix d_2: C_2 -> C_1.
        
        For faces stored as edge lists, each face contributes 1 to its boundary edges.
        """
        if not self.faces:
            return np.array([]).reshape(self.num_edges, 0)
        
        edge_index = {tuple(sorted(e)): i for i, e in enumerate(self.edges)}
        num_faces = len(self.faces)
        
        matrix = np.zeros((self.num_edges, num_faces), dtype=np.int8)
        for f_idx, face in enumerate(self.faces):
            for edge in face:
                e_key = tuple(sorted(edge))
                if e_key in edge_index:
                    matrix[edge_index[e_key], f_idx] += 1
        
        return matrix % 2
    
    def compute_h0(self):
        """
        Compute H_0 = number of connected components.
        """
        G = nx.Graph()
        G.add_nodes_from(range(self.num_vertices))
        G.add_edges_from(self.edges)
        return nx.number_connected_components(G)
    
    def compute_h1(self):
        """
        Compute H_1 = ker(d_1) / im(d_2).
        
        dim(H_1) = dim(ker(d_1)) - dim(im(d_2))
        
        For connected graph:
        dim(ker(d_1)) = |E| - |V| + #components
        """
        # Number of connected components
        num_components = self.compute_h0()
        
        # dim(ker(d_1)) using rank-nullity
        # rank(d_1) = |V| - #components (for connected components)
        dim_ker_d1 = self.num_edges - (self.num_vertices - num_components)
        
        # dim(im(d_2))
        d2 = self._build_d2_matrix()
        dim_im_d2 = compute_image_dimension(d2)
        
        return max(0, dim_ker_d1 - dim_im_d2)
    
    def is_contractible(self):
        """Check if the complex is contractible (H_1 = 0)."""
        return self.compute_h1() == 0
    
    def detect_obstruction(self):
        """
        Detect topological obstruction to polynomial-time computation.
        
        Returns True if H_1 != 0 (non-trivial cycles exist).
        """
        h1 = self.compute_h1()
        if h1 > 0:
            return True, h1
        return False, 0


def test_homology():
    """Test homology computation on simple examples."""
    print("--- Homology Calculator Test ---")
    
    # Test 1: Square (4 vertices, 4 edges) - should have H_1 = 1 if missing face
    print("\nTest 1: Square without face (should have H_1 = 1)")
    vertices = [0, 1, 2, 3]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    faces = []  # No face -> cycle is not a boundary
    
    calc = HomologyCalculator(vertices, edges, faces)
    h1 = calc.compute_h1()
    print(f"H_1 = {h1} (Expected: 1)")
    
    # Test 2: Square with face - should have H_1 = 0
    print("\nTest 2: Square with face (should have H_1 = 0)")
    faces = [[(0, 1), (1, 2), (2, 3), (3, 0)]]
    calc = HomologyCalculator(vertices, edges, faces)
    h1 = calc.compute_h1()
    print(f"H_1 = {h1} (Expected: 0)")
    
    # Test obstruction detection
    print("\nTest 3: Obstruction Detection")
    is_obs, rank = calc.detect_obstruction()
    print(f"Obstruction: {is_obs}, Rank: {rank}")


if __name__ == "__main__":
    test_homology()
