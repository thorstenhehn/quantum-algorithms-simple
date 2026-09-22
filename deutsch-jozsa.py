# Implementation of Deutsch-Jozsa's algorithm for use with qiskit.
# We use state vectors and do not require access to a quantum
# simulator or backend-computer.
# Our goal is to make this as simple as possible such that users
# can have an easy first interaction with quantum algorithms.

from qiskit import *
from qiskit.quantum_info import Statevector
import sys


def main():
    chl = [
        "f(x0, x1) = 0",
        "f(x0, x1) = 1",
        "f(x0, x1) = x0",
        "f(x0, x1) = x1",
        "f(x0, x1) = not x0",
        "f(x0, x1) = not x1",
        "f(x0, x1) = x0 xor x1",
        "f(x0, x1) = not(x0 xor x1)",
    ]
    print(f"""
    The Deutsch-Jozsa algorithm will be challenged to classify a
    binary-input binary-output function. It will use only one
    call to the quantum implementation of the function (oracle).
    The following functions are available:
    0: {chl[0]}
    1: {chl[1]}
    2: {chl[2]}
    3: {chl[3]}
    4: {chl[4]}
    5: {chl[5]}
    6: {chl[6]}
    7: {chl[7]}
    """)
    c_str = input(f"Provide your input as an index between 0 and {len(chl) - 1}: ")
    try:
        c = int(c_str)
        assert c < len(chl)
    except:
        print("Invalid input.")
        sys.exit(1)

    qc = QuantumCircuit(3)

    # Prepare qubits in |0> and |1> state, resp.

    qc.x(2)

    # Create superposition |+>, |+>, and |-> by sending all through Hadamard.

    qc.h(0)
    qc.h(1)
    qc.h(2)

    # The oracle function serves as the quantum implementation of the function
    # provided in the challenge. Based on user's choice, we prepare the oracle
    # and include it into the circuit.
    oracle = create_oracle(c)
    qc.compose(oracle, inplace=True)

    # Transform to |0> and |1>, depending on oracle's output
    qc.h(0)
    qc.h(1)

    sv = Statevector(qc)
    probs = sv.probabilities_dict()

    p00 = sum(v for k, v in probs.items() if k[-2:] == "00")  # first two qubits
    if p00 > 0.99:
        print(f"Function {chl[c]} has constant output.")
    else:
        print(f"Function {chl[c]} has balanced output.")


def create_oracle(challenge: int) -> QuantumCircuit:
    o = QuantumCircuit(3)
    if challenge == 0:  # f(x0,x1) = 0
        o.id(2)
    elif challenge == 1:  # f(x0,x1) = 1
        o.x(2)
    elif challenge == 2:  # f(x0,x1) = x0
        o.cx(0, 2)
    elif challenge == 3:  # f(x0,x1) = x1
        o.cx(1, 2)
    elif challenge == 4:  # f(x0,x1) = not x0
        o.x(0)
        o.cx(0, 2)
        o.x(0)
    elif challenge == 5:  # f(x0,x1) = not x1
        o.x(1)
        o.cx(1, 2)
        o.x(1)
    elif challenge == 6:  # f(x0,x1) = x0 xor x1
        o.cx(0, 2)
        o.cx(1, 2)
    elif challenge == 7:  # f(x0,x1) = not (x0 xor x1)
        o.cx(0, 2)
        o.cx(1, 2)
        o.x(2)
    else:
        print("Oracle not implemented")
    return o


if __name__ == "__main__":
    main()
