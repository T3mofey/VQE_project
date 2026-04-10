"""
sweep.py
--------
Sweep the transverse field h/J from 0 to 3 and collect:
  - VQE ground state energy
  - Exact ground state energy
  - Transverse magnetisation  <X> = (1/n) * sum_i <X_i>
  - Nearest-neighbour ZZ correlation  <ZZ> = (1/n) * sum_i <Z_i Z_{i+1}>

The quantum phase transition of the TFIM occurs at h/J = 1.
"""

import numpy as np
import json
from pathlib import Path

from hamiltonian import build_hamiltonian
from ansatz import ansatz, random_params
from vqe import run_vqe
from exact_diag import scan_energies

import pennylane as qml


def measure_observables(params, n_qubits: int, n_layers: int):
    """
    Measure transverse magnetisation and ZZ correlations
    using the optimised VQE parameters.

    Returns
    -------
    mag_x : float   — mean <X_i>
    corr_zz : float — mean <Z_i Z_{i+1}>
    """
    dev = qml.device("default.qubit", wires=n_qubits)

    # Transverse magnetisation  (1/n) sum_i <X_i>
    X_ops = qml.Hamiltonian(
        [1 / n_qubits] * n_qubits,
        [qml.PauliX(i) for i in range(n_qubits)],
    )

    # ZZ correlations  (1/(n-1)) sum_i <Z_i Z_{i+1}>
    ZZ_ops = qml.Hamiltonian(
        [1 / (n_qubits - 1)] * (n_qubits - 1),
        [qml.PauliZ(i) @ qml.PauliZ(i + 1) for i in range(n_qubits - 1)],
    )

    @qml.qnode(dev)
    def circuit_x(params):
        ansatz(params, n_qubits, n_layers)
        return qml.expval(X_ops)

    @qml.qnode(dev)
    def circuit_zz(params):
        ansatz(params, n_qubits, n_layers)
        return qml.expval(ZZ_ops)

    # TODO: call circuit_x and circuit_zz with the optimised params
    mag_x = float(circuit_x(params))
    corr_zz = float(circuit_zz(params))
    return mag_x, corr_zz


def run_sweep(
    n_qubits: int = 6,
    J: float = 1.0,
    h_min: float = 0.1,
    h_max: float = 3.0,
    n_points: int = 20,
    n_layers: int = 3,
    n_steps: int = 300,
    save_path: str = "results/sweep.json",
):
    """
    Run the full h/J sweep and save results to a JSON file.
    """
    h_values = np.linspace(h_min, h_max, n_points)

    print("Computing exact energies...")
    exact_energies = scan_energies(n_qubits, h_values, J=J)

    vqe_energies = []
    mag_x_list = []
    corr_zz_list = []

    for idx, h in enumerate(h_values):
        print(f"\n[{idx+1}/{n_points}]  h/J = {h/J:.3f}")
        energy, params, _ = run_vqe(
            n_qubits=n_qubits,
            J=J,
            h=h,
            n_layers=n_layers,
            n_steps=n_steps,
            verbose=False,
        )
        vqe_energies.append(energy)

        mag_x, corr_zz = measure_observables(params, n_qubits, n_layers)
        mag_x_list.append(mag_x)
        corr_zz_list.append(corr_zz)
        print(f"  VQE energy={energy:.4f}  exact={exact_energies[idx]:.4f}  "
              f"<X>={mag_x:.4f}  <ZZ>={corr_zz:.4f}")

    results = {
        "n_qubits": n_qubits,
        "J": J,
        "h_values": h_values.tolist(),
        "vqe_energies": vqe_energies,
        "exact_energies": exact_energies.tolist(),
        "magnetisation_x": mag_x_list,
        "correlation_zz": corr_zz_list,
    }

    Path(save_path).parent.mkdir(exist_ok=True)
    with open(save_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {save_path}")
    return results


if __name__ == "__main__":
    run_sweep()
