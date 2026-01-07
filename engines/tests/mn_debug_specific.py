"""
Targeted debug of chi^(2,2)((4)) - the ONLY failing case.

Expected: 0
Got: -1

Let's trace the border strip removal for partition (2,2) with k=4.
"""

import sys
sys.path.insert(0, 'd:/PvsNP')

from engines.algebra.murnaghan_nakayama import remove_border_strip, character_mn

print("="*80)
print("DEBUGGING chi^(2,2)((4))")
print("="*80)

partition = (2, 2)
k = 4

print(f"\nPartition: {partition}")
print(f"Removing border strips of size k={k}")
print()

# Get all border strip removals
removals = remove_border_strip(partition, k)

print(f"Found {len(removals)} border strip removal(s):")
for new_p, height in removals:
    sign = (-1) ** (height - 1)
    print(f"  -> new_partition={new_p}, height={height}, sign=(-1)^{height-1}={sign}")

print()

# Manual analysis:
# Partition (2,2) looks like:
#   [ ][ ]
#   [ ][ ]
#
# A border strip of size 4 must remove all 4 cells.
# But is there ONE valid border strip, or NONE?
#
# Border strip definition: connected skew shape with no 2x2 square.
# The skew shape (2,2) / () = the entire (2,2) diagram.
# Does (2,2) itself contain a 2x2 square? YES! It IS a 2x2 square!
#
# Therefore, the ENTIRE (2,2) partition is NOT a valid border strip.
# There should be ZERO valid removals!

print("ANALYSIS:")
print("The partition (2,2) IS a 2x2 square.")
print("A border strip cannot contain a 2x2 square.")
print("Therefore, there are NO valid border strips of size 4 in (2,2).")
print("The algorithm should return chi^(2,2)((4)) = 0 (sum over empty set).")
print()

if len(removals) == 0:
    print(">>> CORRECT: No border strips found. <<<")
else:
    print(">>> BUG: Algorithm incorrectly found border strip(s). <<<")
    print("    The 2x2 square check is missing!")
