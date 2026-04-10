"""
exact_diag.py
-------------
Exact diagonalisation of the TFIM Hamiltonian using NumPy/SciPy.

Used to benchmark VQE results.

H = -J * sum_i Z_i Z_{i+1}  -  h * sum_i X_i
"""

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh


# Pauli matrices
_I = np.eye(2)
_X = np.array([[0, 1], [1, 0]], dtype=float)
_Z = np.array([[1, 0], [0, -1]], dtype=float)


def _kron_op(op, site, n_qubits):
    """Embed a single-site operator at `site` in the full 2^n Hilbert space."""
    ops = [_I] * n_qubits
    ops[site] = op
    result = ops[0]
    for m in ops[1:]:
        result = np.kron(result, m)
    return result


def build_matrix(n_qubits: int, J: float = 1.0, h: float = 1.0, periodic: bool = False):
    """Return the full TFIM Hamiltonian as a dense numpy matrix."""
    dim = 2 ** n_qubits
    H = np.zeros((dim, dim))

    # ZZ terms
    for i in range(n_qubits - 1):
        Zi = _kron_op(_Z, i, n_qubits)
        Zj = _kron_op(_Z, i + 1, n_qubits)
        H -= J * (Zi @ Zj)

    if periodic:
        # TODO: add boundary term between site n_qubits-1 and site 0
        pass

    # Transverse field terms
    for i in range(n_qubits):
        H -= h * _kron_op(_X, i, n_qubits)

    return H


def ground_state_energy(n_qubits: int, J: float = 1.0, h: float = 1.0, periodic: bool = False):
    """Return the exact ground state energy (and state vector)."""
    H = build_matrix(n_qubits, J=J, h=h, periodic=periodic)

    # TODO: use np.linalg.eigh for small systems, eigsh (sparse) for larger
    eigenvalues, eigenvectors = np.linalg.eigh(H)

    E0 = eigenvalues[0]
    psi0 = eigenvectors[:, 0]
    return E0, psi0


def scan_energies(n_qubits: int, h_values, J: float = 1.0):
    """Return exact ground state energies for an array of h values."""
    return np.array([ground_state_energy(n_qubits, J=J, h=h)[0] for h in h_values])


if __name__ == "__main__":
    n = 6
    for h in [0.5, 1.0, 1.5]:
        E0, _ = ground_state_energy(n, J=1.0, h=h)
        print(f"n={n}, h={h:.1f}  ->  E0 = {E0:.6f}  (per site: {E0/n:.6f})")
