# Implementation of Deutsch-Jozsa's algorithm to the
# Bernstein-Vazirani problem for use with qiskit.  We use state
# vectors and do not require access to a quantum simulator or
# backend-computer.  Our goal is to make this as simple as possible
# such that users can have an easy first interaction with quantum
# algorithms.

from qiskit import *
from qiskit.quantum_info import Statevector
import sys


def main():
    print(f""" The Bernstein-Vazirani problem recovers a secret
    bitstring s by using the Deutsch-Jozsa algorithm. It will use only
    one query to the oracle, with f(x) chosen as
    f(x) = xor_over_i x_i * s_i .  """)

    s = input(f"Provide the secret s as a string of 0s and 1s: ")
    if s and set(s) <= {"0", "1"}:
        # Valid input
        pass
    else:
        print("Invalid input.")
        sys.exit(1)

    l = len(s)
    qc = QuantumCircuit(l + 1)

    # Prepare qubits in |0> (input registers) and |1> (aux register) state, resp.

    qc.x(l)

    # Create superposition |+> and |-> by sending all through Hadamard.

    for i in range(l + 1):
        qc.h(i)

    # The oracle function serves as the quantum implementation of the function
    # provided in the challenge. Based on user's choice, we prepare the oracle
    # and include it into the circuit.
    oracle = create_oracle(s)
    qc.compose(oracle, inplace=True)

    # Send outputs 0 to l-1 (corresponding to input bits) through Hadamard.
    for i in range(l):
        qc.h(i)
    # The input registers now contain the hidden string s.

    sv = Statevector(qc)
    p = sv.probabilities_dict()

    # Sum over auxiliary qubit as it remains in superposition
    input_p = {}
    for k, v in p.items():
        input_bits = k[-l:]  # extract input register
        input_p[input_bits] = input_p.get(input_bits, 0) + v

    # Find state with probability \approx 1
    result = max(input_p, key=input_p.get)

    # Reverse qiskit's bit order and output to user
    s_est = result[::-1]
    print(f"Bernstein-Vazirani algorithm recovered secret string: {s_est}.")


def create_oracle(s: str) -> QuantumCircuit:
    l = len(s)
    o = QuantumCircuit(l + 1)
    for i in range(l):
        if s[i] == "1":
            o.cx(i, l)
    return o


if __name__ == "__main__":
    main()
