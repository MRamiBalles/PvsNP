import sys
import os

# Adjust path to import from engines
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engines.holographic.catalytic_tape import CatalyticTape

def test_memory_restore():
    print("Executing Test: Memory Invariant Restoration...")
    tape = CatalyticTape(100)
    initial = tape.get_state()
    
    # Simulate a deep computation chain
    for i in range(10):
        val = random_val = i * 7
        tape.write(i, val)
        # ... logic ...
        tape.write(i, val) # Reversible XOR
        
    if tape.check_restoration():
        print("[SUCCESS] Catalytic Invariant Maintained.")
        return True
    else:
        print("[FAILURE] Memory Leak / Corruption Detected!")
        return False

if __name__ == "__main__":
    test_memory_restore()
