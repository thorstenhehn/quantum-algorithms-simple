# Implementation of Quantum Fourier Transformation for use with qiskit.
# We use state vectors and do not require access to a quantum
# simulator or backend-computer.
# Our goal is to make this as simple as possible such that users
# can have an easy first interaction with quantum algorithms.
import sys

import numpy as np
from qiskit import *
from qiskit.quantum_info import Statevector


def main():
    inp = [
        "Amplitude spike |0001>",
        "Amplitude spike |0010>",
        "Uniform superposition with phase ramp, step size 2*pi*x*1 / 2**n",
        "Uniform superposition with phase ramp, step size 2*pi*x*2 / 2**n",
    ]
    out = [
        "Phase wave, phase increase 2*pi*k/(2**n) per step, k = 1",
        "Phase wave, phase increase 2*pi*k/(2**n) per step, k = 2",
        "Amplitude spike",
        "Amplitude spike",
    ]
    print(f"""
    Quantum Fourier Transformation (QFT) with n = 4 qubits and N = 16 states.
    The following input signals are available for demonstration (MSB left):
    0: {inp[0]}
    1: {inp[1]}
    2: {inp[2]}
    3: {inp[3]}
    """)
    idx_str = input(f"Provide your input as an index between 0 and {len(inp) - 1}: ")
    try:
        idx = int(idx_str)
    except ValueError:
        print("Invalid input: enter a number.")
        sys.exit(1)

    if not 0 <= idx < len(inp):
        print(f"Invalid input: enter a number between 0 and {len(inp) - 1}")
        sys.exit(1)

    n = 4  # Use n = 4, N = 16 for demonstration purposes

    print(f"Chosen input: {inp[idx]}\nExpected Output: {out[idx]}\n")

    qc = QuantumCircuit(n)

    # Create input signal
    s = create_input(n, idx)
    qc.compose(s, inplace=True)

    # Print input signals
    print("State vector of QFT input:")
    print_sv(qc)

    # QFT
    qft = create_qft(n, swap=True)
    qc.compose(qft, inplace=True)

    # Print output signals
    print("\nState vector of QFT output:")
    print_sv(qc)


def create_qft(n: int, swap=False) -> QuantumCircuit:

    qft = QuantumCircuit(n)
    for i in reversed(range(n)):
        qft.h(i)
        for j in range(i):
            qft.cp(2 * np.pi / (2 ** (i - j + 1)), j, i)

    # swap qubits, if enabled
    if swap == False:
        return qft
    for i in range(n // 2):  # floor(n/2)
        qft.swap(i, n - i - 1)
    return qft


def create_input(n: int, choice: int) -> QuantumCircuit:
    if choice == 0:
        s = create_amplitude_spike(n, 0)  # Set zero-th qubit for k = 1
    if choice == 1:
        s = create_amplitude_spike(n, 1)  # Set first qubit for k = 2
    if choice == 2:
        s = create_phase_ramp(n, 1)
    if choice == 3:
        s = create_phase_ramp(n, 2)
    return s


def create_phase_ramp(n: int, k: int) -> QuantumCircuit:
    s = QuantumCircuit(n)

    # Put all qubits in superposition
    for i in range(n):
        s.h(i)

    # Apply phase ramp: exp(2 pi i k x / 2^n)
    for i in range(n):
        angle = 2 * np.pi * k * 2 ** (i - n)
        s.p(angle, i)

    return s


def create_amplitude_spike(n: int, k: int) -> QuantumCircuit:
    s = QuantumCircuit(n)
    s.x(k)
    return s


def print_sv(qc: QuantumCircuit):
    sv = Statevector(qc)
    for i, amp in enumerate(sv.data):
        mag = np.abs(amp)
        phase = np.angle(amp) % (2 * np.pi)
        print(f"|{i:04b}> (|{i:02d}>): |amp| = {mag:.3f}, phase = {phase:.3f}")


if __name__ == "__main__":
    main()
