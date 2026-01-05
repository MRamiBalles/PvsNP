import numpy as np
import networkx as nx
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

def get_boundary_matrix_z2(nodes, edges, faces):
    """
    Computes the boundary matrix d1 (faces to edges) or d0 (edges to nodes) over Z2.
    For d1: rows are edges, cols are faces.
    """
    if len(faces) == 0:
        return csr_matrix((len(edges), 0))
    
    # d1: rows = edges, cols = faces
    # Over Z2, we just check if an edge is in a face.
    data = []
    row_ind = []
    col_ind = []
    
    edge_to_idx = {tuple(sorted(e)): i for i, e in enumerate(edges)}
    
    for f_idx, face in enumerate(faces):
        # A face (cycle) in our context is a list of edges
        for edge in face:
            e_key = tuple(sorted(edge))
            if e_key in edge_to_idx:
                data.append(1)
                row_ind.append(edge_to_idx[e_key])
                col_ind.append(f_idx)
                
    return csr_matrix((data, (row_ind, col_ind)), shape=(len(edges), len(faces)), dtype=int)

def rank_z2(matrix):
    """
    Computes the rank of a binary matrix over Z2 using Gaussian elimination.
    """
    if matrix.shape[0] == 0 or matrix.shape[1] == 0:
        return 0
    
    # Convert to dense for small matrices (typical for our SAT examples)
    A = matrix.toarray() % 2
    nrows, ncols = A.shape
    rank = 0
    pivot_row = 0
    for j in range(ncols):
        if pivot_row >= nrows:
            break
        # Find pivot
        pivot = -1
        for i in range(pivot_row, nrows):
            if A[i, j] == 1:
                pivot = i
                break
        
        if pivot != -1:
            # Swap rows
            A[[pivot_row, pivot]] = A[[pivot, pivot_row]]
            # Eliminate
            for i in range(nrows):
                if i != pivot_row and A[i, j] == 1:
                    A[i] = (A[i] + A[pivot_row]) % 2
            pivot_row += 1
            rank += 1
    return rank

def compute_h1_rank(edges, faces, nodes_count):
    """
    H1 = Ker(d0) / Im(d1)
    dim(H1) = dim(Ker(d0)) - dim(Im(d1))
    dim(Ker(d0)) = |Edges| - rank(d0)
    rank(d0) = |Nodes| - (number of connected components)
    So dim(H1) = |Edges| - (|Nodes| - CC) - rank(d1)
    """
    # Number of connected components
    G = nx.Graph()
    G.add_edges_from(edges)
    # Ensure all nodes are included even if isolated
    G.add_nodes_from(range(nodes_count))
    cc = nx.number_connected_components(G)
    
    dim_ker_d0 = len(edges) - (nodes_count - cc)
    
    d1 = get_boundary_matrix_z2(None, edges, faces)
    dim_im_d1 = rank_z2(d1)
    
    return dim_ker_d0 - dim_im_d1

def sat_to_config_graph(variables, clauses):
    """
    Generates a configuration graph for small SAT.
    Nodes: 2^n possible assignments.
    Edges: Transitions between assignments differing by one bit (optional)
    or more specifically for Tang: transitions that maintain some partial satisfaction?
    
    Let's use the standard configuration graph: nodes are assignments, 
    edges connect assignments differing by 1 bit flip.
    """
    n = len(variables)
    nodes = list(range(2**n))
    edges = []
    for i in range(2**n):
        for bit in range(n):
            j = i ^ (1 << bit)
            if i < j:
                edges.append((i, j))
    
    # Faces: For a simple configuration graph (hypercube), 
    # faces are the 4-cycles.
    faces = []
    for i in range(2**n):
        for b1 in range(n):
            for b2 in range(b1 + 1, n):
                # 4-cycle: i -> i^2^b1 -> i^2^b1^2^b2 -> i^2^b2 -> i
                n1 = i ^ (1 << b1)
                n2 = n1 ^ (1 << b2)
                n3 = i ^ (1 << b2)
                faces.append([(i, n1), (n1, n2), (n2, n3), (n3, i)])
                
    return nodes, edges, faces

if __name__ == "__main__":
    print("--- Topological Motor: H1 Homology Detector ---")
    
    # Test 1: Simple 2-variable system (Square graph)
    print("\nTest 1: 2-variable hypercube (Square)")
    nodes, edges, faces = sat_to_config_graph(['x', 'y'], [])
    h1 = compute_h1_rank(edges, faces, len(nodes))
    print(f"Nodes: {len(nodes)}, Edges: {len(edges)}, Faces: {len(faces)}")
    print(f"H1 Rank: {h1} (Expect 0 for contractible space)")

    # Test 2: Simulating "H1 > 0" by removing a face (creating a hole)
    print("\nTest 2: Square with a hole (Removed face)")
    h1_hole = compute_h1_rank(edges, faces[:-1], len(nodes))
    print(f"H1 Rank: {h1_hole} (Expect 1)")
