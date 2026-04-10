"""
vqe.py
------
VQE optimisation loop using PennyLane + Adam optimiser.

Returns the optimised parameters and the energy convergence history.
"""

import pennylane as qml
from pennylane import numpy as np

from hamiltonian import build_hamiltonian
from ansatz import ansatz, random_params


def make_cost_fn(H, n_qubits: int, n_layers: int):
    """
    Build and return the VQE cost function (energy expectation value).

    The returned function maps params -> <H>.
    """
    dev = qml.device("default.qubit", wires=n_qubits)

    @qml.qnode(dev, interface="autograd")
    def cost(params):
        ansatz(params, n_qubits, n_layers)
        return qml.expval(H)

    return cost


def run_vqe(
    n_qubits: int = 6,
    J: float = 1.0,
    h: float = 1.0,
    n_layers: int = 3,
    n_steps: int = 300,
    step_size: float = 0.05,
    seed: int = 42,
    verbose: bool = True,
):
    """
    Run VQE and return (best_energy, optimised_params, history).

    Parameters
    ----------
    n_qubits  : number of spins
    J         : ZZ coupling
    h         : transverse field
    n_layers  : ansatz depth
    n_steps   : optimisation steps
    step_size : Adam learning rate
    seed      : RNG seed for reproducibility
    verbose   : print progress every 50 steps
    """
    H = build_hamiltonian(n_qubits, J=J, h=h)
    cost = make_cost_fn(H, n_qubits, n_layers)

    params = random_params(n_qubits, n_layers, seed=seed)

    # TODO: choose optimiser — Adam is a good default
    # opt = qml.AdamOptimizer(stepsize=step_size)
    opt = qml.AdamOptimizer(stepsize=step_size)

    history = []

    for step in range(n_steps):
        # TODO: update params with opt.step(cost, params)
        params, energy = opt.step_and_cost(cost, params)
        history.append(float(energy))

        if verbose and (step % 50 == 0 or step == n_steps - 1):
            print(f"  step {step:4d}  |  energy = {energy:.6f}")

    best_energy = history[-1]
    return best_energy, params, history


if __name__ == "__main__":
    energy, params, history = run_vqe(n_qubits=6, h=1.0, verbose=True)
    print(f"\nFinal VQE energy: {energy:.6f}")
