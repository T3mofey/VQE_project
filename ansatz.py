"""
ansatz.py
---------
Hardware-efficient ansatz for the TFIM ground state.

Structure per layer:
  1. RY(theta_i) on every qubit
  2. CNOT ladder:  0->1, 1->2, ..., (n-2)->(n-1)

Total parameters: n_qubits * n_layers  (+ optional final RY layer)
"""

import pennylane as qml
from pennylane import numpy as np


def ansatz(params, n_qubits: int, n_layers: int):
    """
    Apply the hardware-efficient ansatz to the current circuit.

    Parameters
    ----------
    params   : array of shape (n_layers, n_qubits)
    n_qubits : int
    n_layers : int
    """
    # TODO: implement the layered structure
    # For each layer l in range(n_layers):
    #   - apply RY(params[l, i]) to qubit i  for all i
    #   - apply CNOT(i, i+1)                 for i in range(n_qubits - 1)
    for l in range(n_layers):
        for i in range(n_qubits):
            qml.RY(params[l, i], wires=i)
        for i in range(n_qubits - 1):
            qml.CNOT(wires=[i, i + 1])


def param_shape(n_qubits: int, n_layers: int):
    """Return the shape of the parameter array."""
    return (n_layers, n_qubits)


def random_params(n_qubits: int, n_layers: int, seed: int = 42):
    """Initialise parameters uniformly in [0, 2*pi)."""
    rng = np.random.default_rng(seed)
    return rng.uniform(0, 2 * np.pi, param_shape(n_qubits, n_layers))


if __name__ == "__main__":
    n_qubits, n_layers = 4, 2
    dev = qml.device("default.qubit", wires=n_qubits)
    params = random_params(n_qubits, n_layers)

    @qml.qnode(dev)
    def circuit(params):
        ansatz(params, n_qubits, n_layers)
        return qml.state()

    print(qml.draw(circuit)(params))
