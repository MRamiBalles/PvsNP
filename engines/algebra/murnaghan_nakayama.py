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


def is_valid_border_strip(original: Tuple[int, ...], result: Tuple[int, ...]) -> bool:
    """
    Check if the skew shape (original / result) is a valid border strip.
    A border strip (rim hook) CANNOT contain a 2x2 square.
    
    The skew shape has a 2x2 square if there exist adjacent rows i and i+1
    where both rows have at least 2 cells in the removed portion AND
    they overlap by at least 2 columns.
    """
    if not original:
        return False
    
    # Pad result to match length of original
    result_list = list(result) + [0] * (len(original) - len(result))
    
    # Calculate removed cells per row
    # removed[i] = original[i] - result[i], cells removed from row i
    # The interval of removed cells in row i is [result[i], original[i]-1]
    
    for i in range(len(original) - 1):
        # Row i: removed cells are columns [result_list[i], original[i]-1]
        # Row i+1: removed cells are columns [result_list[i+1], original[i+1]-1]
        
        removed_i_start = result_list[i]
        removed_i_end = original[i] - 1
        removed_i_count = original[i] - result_list[i]
        
        removed_i1_start = result_list[i+1]
        removed_i1_end = original[i+1] - 1 if i+1 < len(original) else -1
        removed_i1_count = original[i+1] - result_list[i+1] if i+1 < len(original) else 0
        
        # Check for 2x2 square: both rows have >=2 cells removed AND overlap >=2 columns
        if removed_i_count >= 2 and removed_i1_count >= 2:
            # Calculate column overlap
            overlap_start = max(removed_i_start, removed_i1_start)
            overlap_end = min(removed_i_end, removed_i1_end)
            overlap_width = overlap_end - overlap_start + 1
            
            if overlap_width >= 2:
                # Found a 2x2 square!
                return False
    
    return True


def remove_border_strip(partition: Tuple[int, ...], k: int) -> List[Tuple[Tuple[int, ...], int]]:
    """
    Find all ways to remove a border strip of size k from the partition.
    Returns list of (new_partition, height) pairs.
    Uses DFS to explore all valid rim hooks (branching between moving left or up).
    """
    if not partition or k <= 0:
        return []
    
    results = []
    p_mutable = list(partition)
    
    def dfs(current_p, start_row, current_row, k_left, prev_interval):
        # Base case: successfully removed k cells
        if k_left == 0:
            # Height is (start_row - end_row + 1)
            # current_row here is the *last* row from which cells were removed.
            results.append((list_to_partition(current_p), start_row - current_row + 1))
            return

        # Cannot go below row 0
        if current_row < 0:
            return

        # Calculate available cells in current_row (exposed on rim)
        if current_row + 1 < len(current_p):
            available = current_p[current_row] - current_p[current_row + 1]
        else:
            available = current_p[current_row]
            
        if available <= 0:
            return

        limit = min(available, k_left)
        
        for n in range(1, limit + 1):
            # Proposed interval for this row
            curr_end = current_p[current_row] - 1
            curr_start = current_p[current_row] - n
            
            valid_connection = True
            if prev_interval is not None:
                prev_start, prev_end = prev_interval
                # Interval overlap check
                overlap_start = max(curr_start, prev_start)
                overlap_end = min(curr_end, prev_end)
                if overlap_start > overlap_end:
                    valid_connection = False
            
            if valid_connection:
                # Execute removal
                new_p = list(current_p)
                new_p[current_row] -= n
                
                # Recurse
                if k_left - n == 0:
                     # Finished
                     h_calc = start_row - current_row + 1
                     results.append((list_to_partition(new_p), h_calc))
                else:
                     # Must continue UP
                     dfs(new_p, start_row, current_row - 1, k_left - n, (curr_start, curr_end))

    # Iterate over all possible starting rows
    for r in range(len(partition)):
        dfs(p_mutable, r, r, k, None)

    # Filter: remove any result where the skew shape contains a 2x2 square
    valid_results = []
    for new_p, h in results:
        if is_valid_border_strip(partition, new_p):
            valid_results.append((new_p, h))
    
    # Dedup
    unique_results = []
    seen = set()
    for p, h in valid_results:
        if (p, h) not in seen:
            seen.add((p, h))
            unique_results.append((p, h))
            
    return unique_results


@lru_cache(maxsize=10000)
def character_mn(partition: Tuple[int, ...], cycle_type: Tuple[int, ...]) -> int:
    """
    Compute chi^partition(sigma).
    """
    # Normalize
    cycle_type = tuple(sorted(cycle_type, reverse=True))
    
    # Base case
    if not partition and not cycle_type:
        return 1
    
    if not partition or not cycle_type:
        return 0
    
    if sum(partition) != sum(cycle_type):
        return 0
    
    k = cycle_type[0]
    remaining_cycles = cycle_type[1:]
    
    removals = remove_border_strip(partition, k)
    
    # Debug trace for specific problematic case
    # checking (1,1,1) or sub-partitions
    trace = False
    # if sum(partition) <= 3 and k==1:
    #    if partition == (1,1,1) or partition == (2,1):
    #         trace = True
    
    total = 0
    for new_partition, height in removals:
        sign = (-1) ** (height - 1)
        sub_val = character_mn(new_partition, remaining_cycles)
        contrib = sign * sub_val
        total += contrib
        
        if trace:
            print(f"TRACE: p={partition} k={k} -> new_p={new_partition} h={height} s={sign} sub={sub_val} contrib={contrib}")
            
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
                                 nu: Tuple[int, ...],
                                 debug: bool = False) -> int:
    """
    Compute the exact Kronecker coefficient g(lambda, mu, nu).
    """
    n = sum(lam)
    if sum(mu) != n or sum(nu) != n:
        return 0
    
    all_parts = partitions(n)
    
    total = 0
    if debug:
        print(f"DEBUG: Kronecker for n={n}, lam={lam}, mu={mu}, nu={nu}")
        print(f"{'Class':>15} | {'Size':>6} | {'X_lam':>6} | {'X_mu':>6} | {'X_nu':>6} | {'Contrib':>8}")
    
    for rho in all_parts:
        class_size = conjugacy_class_size(rho, n)
        chi_lam = character_mn(lam, rho)
        chi_mu = character_mn(mu, rho)
        chi_nu = character_mn(nu, rho)
        
        contrib = class_size * chi_lam * chi_mu * chi_nu
        total += contrib
        
        if debug:
            print(f"{str(rho):>15} | {class_size:>6} | {chi_lam:>6} | {chi_mu:>6} | {chi_nu:>6} | {contrib:>8}")
    
    result = total // factorial(n)
    if debug:
        print(f"Total Sum: {total}. Factorial(n): {factorial(n)}. Result: {result}")
    return result


def run_kronecker_validation():
    print("\n" + "="*80)
    print("SCO v9.2 - EXACT KRONECKER COEFFICIENTS (Murnaghan-Nakayama)")
    print("Status: DEBUG MODE")
    print("="*80)
    
    # 1. Sign Representation Parity Test (Debug n=3)
    print("\n[Test 1] Sign Representation Parity (1^3)")
    n = 3
    sign = tuple([1]*n)
    g = kronecker_coefficient_exact(sign, sign, sign, debug=True)
    print(f"n={n}: g((1^{n}), (1^{n}), (1^{n})) = {g} (Expected: 0)")
    
    # 2. Standard Representation Tests (Debug n=3)
    print("\n[Test 2] Standard Representation (2, 1)")
    std = (2, 1)
    g = kronecker_coefficient_exact(std, std, std, debug=True)
    print(f"n=3: g({std}, {std}, {std}) = {g} (Expected: 1)")

    # 3. The Five Threshold Hunt (Rectangular Partitions)
    print("\n[Experiment] The Five Threshold Hunt (k=1 to 5)")
    print("Computing g(lambda, lambda, lambda) for lambda = (2^k) (Rectangle of width 2, height k)")
    
    for k in range(1, 6):
        n = 2 * k
        rect = tuple([2] * k)
        # Using debug=False for production run
        g = kronecker_coefficient_exact(rect, rect, rect, debug=False)
        print(f"k={k} (n={n}, lambda={rect}): g = {g}")
        
    print("\n" + "="*80)
    print("Validation Complete.")
    print("="*80)



if __name__ == "__main__":
    run_kronecker_validation()
