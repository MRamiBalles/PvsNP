import numpy as np

class CatalyticTape:
    """
    Implements a 'dirty' memory tape that uses XOR operations for 
    reversible data storage. The core invariant is that any subrutine
    must restore the tape to its exact original state.
    """
    def __init__(self, size, initial_data=None):
        self.size = size
        if initial_data is not None:
            self.tape = np.array(initial_data, dtype=np.uint8)
        else:
            # Simulate 'dirty' memory with random data
            self.tape = np.random.randint(0, 256, size, dtype=np.uint8)
        self.initial_state = self.tape.copy()

    def write(self, index, value):
        """XOR writing: reversible if you XOR the same value again."""
        self.tape[index] ^= np.uint8(value)

    def read(self, index):
        return self.tape[index]

    def check_restoration(self):
        """Verifies if the tape has been returned to its original state."""
        return np.array_equal(self.tape, self.initial_state)

    def get_state(self):
        return self.tape.copy()

if __name__ == "__main__":
    print("--- Catalytic Tape Functional Test ---")
    tape = CatalyticTape(10)
    print(f"Initial State: {tape.get_state()}")
    
    # Simulate computation
    val = 42
    tape.write(0, val)
    print(f"Intermediate State: {tape.get_state()}")
    
    # Restore
    tape.write(0, val)
    print(f"Restored State: {tape.get_state()}")
    print(f"Restoration OK: {tape.check_restoration()}")
