from qiskit import *
from qiskit.quantum_info import Statevector
import numpy as np
import sys


def main():
    print(f"""
    The Amplitude Amplification algorithm will be challenged to find a
    secret good state s. It will use an oracle marking the good state
    and diffusion in a loop with a maximum number of iterations and
    a threshold-based early stopping criteria.
    """)

    s = input(f"Provide the secret s as a string of 0s and 1s: ")
    if s and set(s) <= {"0", "1"}:
        # Valid input
        pass
    else:
        print("Invalid input.")
        sys.exit(1)

    # Main parameters
    n = len(s)
    max_iter = 25
    thr = 0.99  # Threshold for early stopping criteria

    qc = QuantumCircuit(n)
    oracle = create_oracle(s)
    diffusion = create_diffusion(n)

    # Step 0: uniform superposition
    qc.h(range(n))
    sv = Statevector(qc)
    print_state("Initial state", n, sv, 0)

    for i in range(1, max_iter + 1):
        # Step 1: Marking by oracle
        qc.compose(oracle, inplace=True)

        # Step 2: Diffusion operator
        qc.compose(diffusion, inplace=True)
        sv = Statevector(qc)
        print_state("Diffusion (amplitude amplification)", n, sv, i)

        # Early stopping and iteration counting
        p = sv.probabilities_dict()
        max_value = max(p.values())
        if max_value > thr:
            print(f"Stopping after {i} iterations - threshold {thr} reached.")
            break


def create_oracle(target):
    n = len(target)
    qc = QuantumCircuit(n)

    for i, bit in enumerate(target):
        if bit == "0":
            qc.x(n - 1 - i)

    qc.compose(mcz(n), inplace=True)

    for i, bit in enumerate(target):
        if bit == "0":
            qc.x(n - 1 - i)

    return qc


def mcz(n):
    qc = QuantumCircuit(n)

    # Apply Z = HXH on qubit n-1. Use control structure from mcx().
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)

    return qc


def create_diffusion(n):
    qc = QuantumCircuit(n)

    # Basis transformation before reflection
    qc.h(range(n))
    qc.x(range(n))

    # MCZ (reflection around |0..0>)
    qc.compose(mcz(n), inplace=True)

    # Undo transformation
    qc.x(range(n))
    qc.h(range(n))

    return qc


def print_state(label, n, sv, i):
    probs = np.abs(sv.data) ** 2

    print(f"\nProbabilities after {label}, iteration {i}")
    for idx, p in enumerate(probs):
        print(f"|{idx:0{n}b}>: {p:.3f}")


if __name__ == "__main__":
    main()
