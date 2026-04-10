"""
hamiltonian.py
--------------
Build the Transverse-Field Ising Model (TFIM) Hamiltonian as a PennyLane operator.

H = -J * sum_i Z_i Z_{i+1}  -  h * sum_i X_i

Parameters
----------
n_qubits : int   — number of spins
J        : float — ZZ coupling strength  (default 1.0)
h        : float — transverse field strength
periodic : bool  — periodic boundary conditions (default False)
"""

import pennylane as qml
from pennylane import numpy as np


def build_hamiltonian(n_qubits: int, J: float = 1.0, h: float = 1.0, periodic: bool = False):
    """Return the TFIM Hamiltonian as a qml.Hamiltonian."""
    coeffs = []
    ops = []

    # --- ZZ interaction terms ---
    # TODO: loop over neighbouring pairs (i, i+1)
    # Hint: use qml.PauliZ(i) @ qml.PauliZ(i+1)
    # If periodic=True, also add the (n_qubits-1, 0) pair
    for i in range(n_qubits - 1):
        coeffs.append(-J)
        ops.append(qml.PauliZ(i) @ qml.PauliZ(i + 1))

    if periodic:
        # TODO: add the boundary term
        pass

    # --- Transverse field terms ---
    # TODO: loop over all sites i, add -h * X_i
    for i in range(n_qubits):
        coeffs.append(-h)
        ops.append(qml.PauliX(i))

    return qml.Hamiltonian(coeffs, ops)


if __name__ == "__main__":
    H = build_hamiltonian(n_qubits=4, J=1.0, h=1.0)
    print(H)
