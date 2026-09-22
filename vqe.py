# Implementation of Variational Quantum Eigensolver for use with qiskit.
# We use state vectors and do not require access to a quantum
# simulator or backend-computer.
# Our goal is to make this as simple as possible such that users
# can have an easy first interaction with quantum algorithms.

from qiskit import *
from qiskit.quantum_info import Statevector
import numpy as np
import sys

PAULI = {
    "I": np.array([[1, 0], [0, 1]]),
    "X": np.array([[0, 1], [1, 0]]),
    "Y": np.array([[0, -1j], [1j, 0]]),
    "Z": np.array([[1, 0], [0, -1]]),
}


def main():
    print("""
    Simple demonstration of Variational Quantum Eigensolver (VQE).
    Limitations:
    - Up to 3 qubits
    - Random search
    """)

    n, H_terms = get_user_input()

    H = build_hamiltonian(H_terms)

    is_complex = contains_Y(H_terms)

    # Exact solution
    eigvals, _ = np.linalg.eigh(H)
    exact_energy = np.min(eigvals)

    print(f"\nExact ground state energy: {exact_energy:.6f}")

    # VQE
    best_theta = None
    best_energy = 1e9

    iterations = 10000

    if is_complex:
        print("\nRunning VQE for complex-valued Hamiltonians.")
    else:
        print("\nRunning VQE restricted to real-valued Hamiltonians.")

    for i in range(iterations):
        if is_complex:
            theta = np.random.uniform(-np.pi, np.pi, 4 * n)
        else:
            theta = np.random.uniform(-np.pi, np.pi, 2 * n)
        e = energy(theta, H, n, is_complex)

        if e < best_energy:
            best_energy = e
            best_theta = theta

        # progress print
        if i % 500 == 0:
            print(f"Iteration {i}: best_energy = {best_energy:.6f}")

    print(f"\nVQE energy:     {best_energy:.6f}")
    print(f"Exact energy:   {exact_energy:.6f}")
    print(f"""\nRelative Error:
    {100 * abs(best_energy - exact_energy) / abs(exact_energy):.6f} %
    """)

    # Final state
    qc = create_ansatz(n, best_theta, is_complex)
    sv = Statevector(qc)

    print("\nFinal statevector:")
    print(sv)

    print("\nProbabilities:")
    probs = np.abs(sv.data) ** 2
    for i, p in enumerate(probs):
        print(f"|{i:0{n}b}>: {p:.4f}")


def build_hamiltonian(terms):
    n = len(terms[0][1])
    dim = 2**n

    H = np.zeros((dim, dim), dtype=complex)

    for coeff, pstring in terms:
        op = PAULI[pstring[0]]
        for p in pstring[1:]:
            op = np.kron(op, PAULI[p])

        H += coeff * op

    return H


def create_ansatz(n, theta, is_complex):
    qc = QuantumCircuit(n)

    if is_complex:
        # Layer 1
        for i in range(n):
            qc.ry(theta[i], i)
            qc.rz(theta[n + i], i)

        # Entanglement
        for i in range(n - 1):
            qc.cx(i, i + 1)

        # Layer 2
        for i in range(n):
            qc.ry(theta[2 * n + i], i)
            qc.rz(theta[3 * n + i], i)

    else:
        # Layer 1
        for i in range(n):
            qc.ry(theta[i], i)

        # Entanglement
        for i in range(n - 1):
            qc.cx(i, i + 1)

        # Layer 2
        for i in range(n):
            qc.ry(theta[n + i], i)

    return qc


def energy(theta, H, n, is_complex):
    qc = create_ansatz(n, theta, is_complex)
    sv = Statevector(qc)
    svd = sv.data
    return np.real(np.conj(svd) @ (H @ svd))


def get_user_input():
    try:
        n = int(input("Number of qubits (e.g. 3): "))
        assert 0 < n <= 3
    except:
        print("Invalid number of qubits.")
        sys.exit(1)

    try:
        num_terms = int(input("Number of Hamiltonian terms (e.g. 2): "))
        assert num_terms > 0
    except:
        print("Invalid number of terms.")
        sys.exit(1)

    terms = []

    for i in range(num_terms):
        print(f"\nTerm {i + 1}")

        try:
            coeff = float(input("  Coefficient: "))
        except:
            print("Invalid coefficient.")
            sys.exit(1)

        pstring = input(f"  Pauli string (length {n}, e.g. ZIX): ").upper()

        if len(pstring) != n or any(p not in "IXYZ" for p in pstring):
            print("Invalid Pauli string.")
            sys.exit(1)

        terms.append((coeff, pstring))

    return n, terms


def contains_Y(terms):
    return any("Y" in p for _, p in terms)


if __name__ == "__main__":
    main()
