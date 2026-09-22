# Implementation of Quantum Phase Estimation for use with qiskit.
# We use state vectors and do not require access to a quantum
# simulator or backend-computer.
# Our goal is to make this as simple as possible such that users
# can have an easy first interaction with quantum algorithms.

from qiskit import *
from qiskit.quantum_info import Statevector
import numpy as np
import sys


def main():
    print(f"""
    Single-qubit Quantum Phase Estimation (QPE) using state vector probabilities.
    """)
    ang_str = input(f"Provide your input as an angle between 0 and pi: ")
    try:
        ang = float(ang_str)
        assert 0 <= ang < np.pi
    except:
        print("Invalid input.")
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
