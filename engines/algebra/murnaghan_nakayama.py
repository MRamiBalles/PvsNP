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
        # Cells must be removed from right to left.
        # Rightmost available is at col p[current_row]-1.
        # How many can we remove?
        # Limited by the row below (it supports cells).
        # We can remove cells as long as we don't eat into the support of row+1.
        # But wait, available logic is: p[row] - p[row+1].
        # These are the cells that extend beyond the row below.
        
        if current_row + 1 < len(current_p):
            available = current_p[current_row] - current_p[current_row + 1]
        else:
            available = current_p[current_row]
            
        if available <= 0:
            return

        # Try removing n cells from this row
        # n can be from 1 to min(available, k_left)
        # BUT: If we are not at the start_row (strips connect upwards),
        # we MUST ensure connectivity with the previous interval.
        # Since we are peeling a continuous strip, if we move UP to this row,
        # we must connect to the strip segment in current_row+1.
        
        # Determine valid range of n
        # If we are continuing a strip, we must satisfy overlap connectivity.
        # The 'prev_interval' (from row+1) was [prev_start, prev_end].
        # The interval we remove here will be [p[row]-n, p[row]-1].
        # They must overlap.
        
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
                     # print(f"DFS FINISH: start={start_row} curr={current_row} h={h_calc} p={new_p}")
                     results.append((list_to_partition(new_p), h_calc))
                else:
                     # Must continue UP
                     dfs(new_p, start_row, current_row - 1, k_left - n, (curr_start, curr_end))

    # Iterate over all possible starting rows
    for r in range(len(partition)):
        # Start a strip at row r
        # Must remove at least 1 cell from row r
        # print(f"DFS START: r={r} p={p_mutable}")
        dfs(p_mutable, r, r, k, None)

    # Dedup results (same partition might be reached via different paths? 
    # Actually MN says "sum over all border strips". If multiple strips yield same partition, sum them? 
    # Usually border strip is unique for a given set of cells.
    # Different sets of cells might yield same partition?
    # No, $\lambda \setminus S = \mu$. Since S is determined by $\lambda$ and $\mu$, they are unique.
    # So deduplication involves same (partition, height) tuples.
    
    unique_results = []
    seen = set()
    for p, h in results:
        # p is tuple from list_to_partition
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
