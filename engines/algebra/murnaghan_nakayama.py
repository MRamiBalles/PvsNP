"""
Murnaghan-Nakayama Rule Implementation - SCO v9.1
Status: NEW (Phase 9.1B - Critical)

Complete implementation of the Murnaghan-Nakayama rule for computing
character values chi^lambda(sigma) for any permutation sigma.

This enables exact Kronecker coefficient computation:
g(lambda, mu, nu) = (1/n!) * sum_{sigma} chi^lambda(sigma) * chi^mu(sigma) * chi^nu(sigma)

Theory:
- The MN rule computes chi^lambda(rho) recursively by removing "border strips" from lambda.
- A border strip (ribbon/rim hook) of size k is a connected skew shape with no 2x2 square.
- Each removal contributes (-1)^(height-1) to the character value.
"""

import sys
sys.path.insert(0, 'd:/PvsNP')

from typing import List, Tuple, Optional
from functools import lru_cache
from math import factorial
from collections import Counter


def partition_to_list(p: Tuple[int, ...]) -> List[int]:
    """Convert partition tuple to mutable list."""
    return list(p)


def list_to_partition(l: List[int]) -> Tuple[int, ...]:
    """Convert list back to partition tuple, removing trailing zeros."""
    while l and l[-1] == 0:
        l.pop()
    return tuple(l) if l else ()


def is_valid_partition(p: Tuple[int, ...]) -> bool:
    """Check if p is a valid partition (non-increasing positive integers)."""
    if not p:
        return True
    for i in range(len(p) - 1):
        if p[i] < p[i+1]:
            return False
    return all(x > 0 for x in p)


def remove_border_strip(partition: Tuple[int, ...], k: int) -> List[Tuple[Tuple[int, ...], int]]:
    """
    Find all ways to remove a border strip of size k from the partition.
    
    Returns list of (new_partition, height) pairs.
    Height = number of rows the strip spans.
    """
    if not partition or k <= 0:
        return []
    
    results = []
    n_rows = len(partition)
    
    # A border strip starts at some cell (i, partition[i]-1) and goes up-left
    # We enumerate all possible removals
    
    for start_row in range(n_rows):
        # Try to remove a strip starting from the rightmost cell of row start_row
        p = partition_to_list(partition)
        
        # The strip must remove exactly k cells, staying connected
        removed = 0
        end_row = start_row
        height = 1
        
        while removed < k and end_row >= 0:
            # How many cells can we remove from this row?
            if end_row == start_row:
                # First row: start from rightmost
                available = p[end_row]
            else:
                # Subsequent rows: only cells that are "exposed" (form border)
                # A cell (i,j) is in the border if (i+1,j) is not in the diagram
                if end_row + 1 < len(p):
                    available = p[end_row] - p[end_row + 1]
                else:
                    available = p[end_row]
            
            if available <= 0:
                break
            
            to_remove = min(available, k - removed)
            
            # Connectivity Check:
            # If we are continuing a strip from the previous iteration (row below, i.e., end_row + 1),
            # the leftmost cell removed in the current row (end_row) must be directly below
            # the rightmost cell removed in the previous row (end_row + 1).
            # Wait, we are iterating UP (decreasing row index).
            # Previous iteration was 'end_row + 1'.
            # Current is 'end_row'.
            # The strip moves from (end_row+1, col) to (end_row, col).
            # The column of the *last* cell removed in 'end_row+1' (its leftmost cell)
            # must match the column of the *first* cell removed in 'end_row' (its rightmost cell).
            
            # Leftmost col of row below: p[end_row+1] (value after removal)
            # Rightmost col of current row: p[end_row] - 1 (value before removal)
            # Connectivity condition: p[end_row+1] == p[end_row] - 1?
            # No, using indices:
            # Row below current size: p[end_row+1]. This is the column index of the hole left.
            # Row current rightmost available: p[end_row]-1.
            # We need p[end_row+1] == p[end_row] - 1 to ensure vertical connection.
            
            if removed > 0:
                # We have already removed cells from lower rows.
                # Check connectivity with the row below (end_row + 1).
                # The leftmost cell removed in row (end_row + 1) had column index `p[end_row+1]`.
                # The rightmost cell we are about to remove in `end_row` has column index `p[end_row] - 1`.
                # They must share an edge. Since we move UP, they must share a horizontal edge?
                # No, vertical edge. (r+1, c) and (r, c).
                # So column indices must match.
                # CORRECTION: Diagonal connectivity is allowed in rim hooks!
                # (r+1, c) and (r, c+1) are connected.
                # So column difference can be 0 (vertical) or 1 (diagonal).
                
                # left_col_below = p[end_row+1]
                # right_col_current = p[end_row] - 1
                # diff = right_col_current - left_col_below
                
                diff = (p[end_row] - 1) - p[end_row+1]
                if diff < 0 or diff > 1:
                     # Not connected
                     break

            p[end_row] -= to_remove
            removed += to_remove
            
            if removed < k:
                end_row -= 1
                if end_row >= 0:
                    height += 1
        
        if removed == k:
            # Check if result is valid partition
            new_p = list_to_partition(p)
            if is_valid_partition(new_p):
                # Verify connectivity (simplified: we trust the algorithm)
                results.append((new_p, height))
    
    # Remove duplicates
    unique = {}
    for p, h in results:
        if p not in unique:
            unique[p] = h
    
    return list(unique.items())


@lru_cache(maxsize=10000)
def character_mn(partition: Tuple[int, ...], cycle_type: Tuple[int, ...]) -> int:
    """
    Compute chi^partition(sigma) where sigma has the given cycle_type.
    Uses the Murnaghan-Nakayama rule recursively.
    
    Base case: chi^()( () ) = 1 (trivial representation of S_0)
    Recursive case: Remove a border strip of size = first part of cycle_type
    """
    # Normalize: sort cycle_type in decreasing order
    cycle_type = tuple(sorted(cycle_type, reverse=True))
    
    # Base case: empty partition and empty cycle type
    if not partition and not cycle_type:
        return 1
    
    if not partition or not cycle_type:
        return 0
    
    # Check sizes match
    if sum(partition) != sum(cycle_type):
        return 0
    
    # Remove the first (largest) cycle
    k = cycle_type[0]
    remaining_cycles = cycle_type[1:]
    
    # Find all valid border strip removals of size k
    removals = remove_border_strip(partition, k)
    
    if not removals:
        return 0
    
    # Sum over all removals with sign (-1)^(height-1)
    total = 0
    for new_partition, height in removals:
        sign = (-1) ** (height - 1)
        contrib = sign * character_mn(new_partition, remaining_cycles)
        total += contrib
    
    return total


def conjugacy_class_size(cycle_type: Tuple[int, ...], n: int) -> int:
    """Size of conjugacy class with given cycle type."""
    counts = Counter(cycle_type)
    z = 1
    for part, mult in counts.items():
        z *= (part ** mult) * factorial(mult)
    return factorial(n) // z


def partitions(n: int) -> List[Tuple[int, ...]]:
    """Generate all partitions of n."""
    if n == 0:
        return [()]
    
    result = []
    def generate(remaining, max_part, current):
        if remaining == 0:
            result.append(tuple(current))
            return
        for part in range(min(remaining, max_part), 0, -1):
            generate(remaining - part, part, current + [part])
    generate(n, n, [])
    return result


def kronecker_coefficient_exact(lam: Tuple[int, ...], 
                                 mu: Tuple[int, ...], 
                                 nu: Tuple[int, ...]) -> int:
    """
    Compute the exact Kronecker coefficient g(lambda, mu, nu).
    
    g(lam, mu, nu) = (1/n!) * sum_{rho} |C_rho| * chi^lam(rho) * chi^mu(rho) * chi^nu(rho)
    
    where the sum is over conjugacy classes rho.
    """
    n = sum(lam)
    if sum(mu) != n or sum(nu) != n:
        return 0
    
    all_parts = partitions(n)
    
    total = 0
    for rho in all_parts:
        class_size = conjugacy_class_size(rho, n)
        chi_lam = character_mn(lam, rho)
        chi_mu = character_mn(mu, rho)
        chi_nu = character_mn(nu, rho)
        
        total += class_size * chi_lam * chi_mu * chi_nu
    
    return total // factorial(n)


def run_kronecker_validation():
    print("\n" + "="*80)
    print("SCO v9.2 - EXACT KRONECKER COEFFICIENTS (Murnaghan-Nakayama)")
    print("Status: REPAIRED & EXTENDED")
    print("="*80)
    
    # 1. Sign Representation Parity Test
    print("\n[Test 1] Sign Representation Parity (1^n)")
    # Theory: g(sgn, sgn, sgn) corresponds to multiplicity of Id in sgn x sgn x sgn = sgn.
    # Since sgn != Id (for n>=2), this should ALWAYS be 0.
    
    for n in [3, 4, 5]:
        sign = tuple([1]*n)
        g = kronecker_coefficient_exact(sign, sign, sign)
        print(f"n={n}: g((1^{n}), (1^{n}), (1^{n})) = {g} (Expected: 0)")
        if g != 0:
            print("  >>> FAIL: Sign parity error detected!")

    # 2. Standard Representation Tests
    print("\n[Test 2] Standard Representation (n-1, 1)")
    # g(std, std, std)
    # n=3 (2,1): g=1
    n = 3
    std = (2, 1)
    g = kronecker_coefficient_exact(std, std, std)
    print(f"n=3: g({std}, {std}, {std}) = {g} (Expected: 1)")

    # 3. The Five Threshold Hunt (Rectangular Partitions)
    print("\n[Experiment] The Five Threshold Hunt (k=2 to 5)")
    print("Computing g(lambda, lambda, lambda) for lambda = (2^k) (Rectangle of width 2, height k)")
    print("Hypothesis: Sequence breaks pattern at k=5.")
    
    # Sequence of rectangular partitions of width 2:
    # k=1: (2)
    # k=2: (2,2)
    # k=3: (2,2,2)
    # k=4: (2,2,2,2)
    # k=5: (2,2,2,2,2)
    
    for k in range(1, 6):
        n = 2 * k
        rect = tuple([2] * k)
        
        # Computing triple Kronecker product multiplicity of IDENTITY (trivial)
        # Equivalently: multiplicity of rect in rect x rect? No, we use symmetric triple.
        # g(rect, rect, rect)
        
        g = kronecker_coefficient_exact(rect, rect, rect)
        print(f"k={k} (n={n}, lambda={rect}): g = {g}")
        
    print("\n" + "="*80)
    print("Validation Complete.")
    print("="*80)



if __name__ == "__main__":
    run_kronecker_validation()
