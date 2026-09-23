# Implementation of Quantum Phase Estimation for use with qiskit.
# We use state vectors and do not require access to a quantum
# simulator or backend-computer.
# Our goal is to make this as simple as possible such that users
# can have an easy first interaction with quantum algorithms.
import sys

import numpy as np
from qiskit import *
from qiskit.quantum_info import Statevector


def main():
    print("""
    Single-qubit Quantum Phase Estimation (QPE) using state vector probabilities.
    """)
    ang_str = input("Provide your input as an angle between 0 and pi: ")

    try:
        ang = float(ang_str)
    except ValueError:
        print("Invalid input: enter a number.")
        sys.exit(1)

    if not 0 <= ang < np.pi:
        print(f"Invalid input: enter a number between 0 and {np.pi}")
        sys.exit(1)

    qc = QuantumCircuit(2)
    qc.h(0)
    # Prepare second qubit as |1> to allow for phase kickback
    qc.x(1)

    # Apply controlled phase to second qubit
    qc.cp(ang, 0, 1)
    qc.h(0)

    sv = Statevector(qc)
    probs = sv.probabilities_dict()
    p0 = sum(v for k, v in probs.items() if k[-1:] == "0")  # first qubit

    # Two .h() and one .cp() yield P(0) = |0.5 * (1 + exp(i*ang)|^2
    # Use exp(i*x) = cos(x) + i*sin(x) to solve for ang.
    ang_est = np.arccos(2 * p0 - 1)

    print(f"Estimated angle: {ang_est}")


if __name__ == "__main__":
    main()
