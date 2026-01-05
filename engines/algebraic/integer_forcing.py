from .kronecker import KroneckerMotor

def run_integer_forcing():
    print("--- Algebraic Motor: Integer Forcing & Obstruction Detection ---")
    motor = KroneckerMotor()
    
    for k in range(1, 6):
        is_obstruction, actual, predicted = motor.analyze_threshold(k)
        if is_obstruction:
            print(f"k={k}: STRONG ALGEBRAIC OBSTRUCTION FOUND.")
        else:
            print(f"k={k}: Structural pattern stable.")

if __name__ == "__main__":
    run_integer_forcing()
