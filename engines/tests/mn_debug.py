"""
MN Emergency Debug - Verifying against known S_4 character table.

S_4 Character Table (standard):
Cycle Types:  (1^4)  (2,1^2) (2^2)   (3,1)   (4)
----------------------------------------------
(4)             1      1       1       1      1
(3,1)           3      1      -1       0     -1
(2,2)           2      0       2      -1      0
(2,1,1)         3     -1      -1       0      1
(1,1,1,1)       1     -1       1       1     -1

Key tests:
- chi^(4)( (1,1,1,1) ) = 1  (trivial rep on identity)
- chi^(2,2)( (1,1,1,1) ) = 2  (dimension of rep)
- chi^(2,2)( (4) ) = 0  (on 4-cycle)
- chi^(3,1)( (4) ) = -1  (on 4-cycle)
"""

import sys
sys.path.insert(0, 'd:/PvsNP')

from engines.algebra.murnaghan_nakayama import character_mn, kronecker_coefficient_exact

print("="*80)
print("S_4 CHARACTER TABLE VERIFICATION")
print("="*80)

# Expected S_4 character table
# Rows: partitions (representations)
# Cols: cycle types (conjugacy classes)
expected = {
    # chi^(4) - trivial rep
    ((4,), (1,1,1,1)): 1,
    ((4,), (2,1,1)): 1,
    ((4,), (2,2)): 1,
    ((4,), (3,1)): 1,
    ((4,), (4,)): 1,
    
    # chi^(3,1) - standard rep
    ((3,1), (1,1,1,1)): 3,
    ((3,1), (2,1,1)): 1,
    ((3,1), (2,2)): -1,
    ((3,1), (3,1)): 0,
    ((3,1), (4,)): -1,
    
    # chi^(2,2) - two-dimensional rep
    ((2,2), (1,1,1,1)): 2,
    ((2,2), (2,1,1)): 0,
    ((2,2), (2,2)): 2,
    ((2,2), (3,1)): -1,
    ((2,2), (4,)): 0,
    
    # chi^(2,1,1) - another 3-dim rep
    ((2,1,1), (1,1,1,1)): 3,
    ((2,1,1), (2,1,1)): -1,
    ((2,1,1), (2,2)): -1,
    ((2,1,1), (3,1)): 0,
    ((2,1,1), (4,)): 1,
    
    # chi^(1,1,1,1) - sign rep
    ((1,1,1,1), (1,1,1,1)): 1,
    ((1,1,1,1), (2,1,1)): -1,
    ((1,1,1,1), (2,2)): 1,
    ((1,1,1,1), (3,1)): 1,
    ((1,1,1,1), (4,)): -1,
}

print(f"{'Partition':>15} | {'Cycle':>12} | {'Expected':>8} | {'Got':>8} | {'Status':>8}")
print("-"*60)

errors = 0
for (partition, cycle_type), exp_val in expected.items():
    got_val = character_mn(partition, cycle_type)
    status = "OK" if got_val == exp_val else "FAIL"
    if got_val != exp_val:
        errors += 1
    print(f"{str(partition):>15} | {str(cycle_type):>12} | {exp_val:>8} | {got_val:>8} | {status:>8}")

print("-"*60)
print(f"Total Errors: {errors} / {len(expected)}")

if errors > 0:
    print("\n>>> CHARACTER TABLE MISMATCH DETECTED! <<<")
    print("The MN algorithm is producing incorrect character values.")
else:
    print("\n>>> CHARACTER TABLE VERIFIED! <<<")
    print("Proceeding to Kronecker coefficient verification...")
    
    # Now test Kronecker
    print("\n" + "="*80)
    print("KRONECKER COEFFICIENT TESTS (S_4)")
    print("="*80)
    
    # g(lambda, mu, nu) should always be >= 0
    from itertools import product
    
    partitions_4 = [(4,), (3,1), (2,2), (2,1,1), (1,1,1,1)]
    
    print("Checking all g(lambda, lambda, lambda) for S_4...")
    for lam in partitions_4:
        g = kronecker_coefficient_exact(lam, lam, lam)
        status = "OK" if g >= 0 else "NEGATIVE!"
        print(f"g({lam}, {lam}, {lam}) = {g}  [{status}]")
