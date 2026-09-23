# Implementation of Deutsch's algorithm for use with qiskit.
# We use state vectors and do not require access to a quantum
# simulator or backend-computer.
# Our goal is to make this as simple as possible such that users
# can have an easy first interaction with quantum algorithms.
import sys

from qiskit import *
from qiskit.quantum_info import Statevector


def main():
    chl = ["f(x) = 0", "f(x) = 1", "f(x) = x", "f(x) = not_x"]
    print(f"""
    The Deutsch algorithm will be challenged to classify a
    binary-input binary-output function. It will use only one
    call to the quantum implementation of the function (oracle).
    The following functions are available:
    0: {chl[0]}
    1: {chl[1]}
    2: {chl[2]}
    3: {chl[3]}
    """)
    c_str = input(f"Provide your input as an index between 0 and {len(chl) - 1}: ")
    try:
        c = int(c_str)
    except ValueError:
        print("Invalid input: enter a number.")
        sys.exit(1)

    if not 0 <= c < len(chl):
        print(f"Invalid input: enter a number between 0 and {len(chl) - 1}")
        sys.exit(1)

    qc = QuantumCircuit(2)

    # Prepare qubits in |0> and |1> state, resp.

    qc.x(1)

    # Create superposition |+> and |-> by sending both through Hadamard-gates

    qc.h(0)
    qc.h(1)

    # The oracle function serves as the quantum implementation of the function
    # provided in the challenge. Based on user's choice, we prepare the oracle
    # and include it into the circuit.
    oracle = create_oracle(c)
    qc.compose(oracle, inplace=True)

    # Transform to |0> and |1>, depending on oracle's output
    qc.h(0)

    sv = Statevector(qc)
    probs = sv.probabilities_dict()

    p0 = sum(v for k, v in probs.items() if k[1] == "0")  # first qubit

    if p0 > 0.99:  # Check is zero-state has probability \approx 1.
        print(f"Function {chl[c]} has constant output.")
    else:
        print(f"Function {chl[c]} has balanced output.")


def create_oracle(challenge: int) -> QuantumCircuit:
    o = QuantumCircuit(2)
    if challenge == 0:  # f(x) = 0
        o.id(1)
    elif challenge == 1:  # f(x) = 1
        o.x(1)
    elif challenge == 2:  # f(x) = x
        o.cx(0, 1)
    elif challenge == 3:  # f(x) = not(x)
        o.x(0)
        o.cx(0, 1)
        o.x(0)
    else:
        print("Oracle not implemented")
    return o


if __name__ == "__main__":
    main()
