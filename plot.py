"""
plot.py
-------
Visualise the sweep results.

Figures produced
----------------
1. energy_vs_h.png      — VQE vs exact ground state energy as a function of h/J
2. observables_vs_h.png — transverse magnetisation <X> and ZZ correlation vs h/J
3. convergence.png      — VQE energy convergence for a single h/J value
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


RESULTS_FILE = "results/sweep.json"
FIGURES_DIR = Path("figures")


def load_results(path: str = RESULTS_FILE):
    with open(path) as f:
        return json.load(f)


def plot_energy(results: dict, save: bool = True):
    h_values = np.array(results["h_values"])
    J = results["J"]
    x = h_values / J  # dimensionless ratio h/J

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(x, results["exact_energies"], "k-", label="Exact", linewidth=2)
    ax.plot(x, results["vqe_energies"], "ro--", label="VQE", markersize=5)
    ax.axvline(1.0, color="gray", linestyle=":", label="Phase transition (h/J=1)")
    ax.set_xlabel("h / J")
    ax.set_ylabel("Ground state energy")
    ax.set_title("TFIM Ground State Energy")
    ax.legend()
    fig.tight_layout()

    if save:
        FIGURES_DIR.mkdir(exist_ok=True)
        fig.savefig(FIGURES_DIR / "energy_vs_h.png", dpi=150)
        print("Saved figures/energy_vs_h.png")
    return fig


def plot_observables(results: dict, save: bool = True):
    h_values = np.array(results["h_values"])
    J = results["J"]
    x = h_values / J

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Transverse magnetisation
    axes[0].plot(x, results["magnetisation_x"], "b-o", markersize=5)
    axes[0].axvline(1.0, color="gray", linestyle=":", label="h/J=1")
    axes[0].set_xlabel("h / J")
    axes[0].set_ylabel(r"$\langle X \rangle$")
    axes[0].set_title("Transverse Magnetisation")
    axes[0].legend()

    # ZZ correlation
    axes[1].plot(x, results["correlation_zz"], "g-o", markersize=5)
    axes[1].axvline(1.0, color="gray", linestyle=":", label="h/J=1")
    axes[1].set_xlabel("h / J")
    axes[1].set_ylabel(r"$\langle Z_i Z_{i+1} \rangle$")
    axes[1].set_title("Nearest-Neighbour ZZ Correlation")
    axes[1].legend()

    fig.tight_layout()

    if save:
        FIGURES_DIR.mkdir(exist_ok=True)
        fig.savefig(FIGURES_DIR / "observables_vs_h.png", dpi=150)
        print("Saved figures/observables_vs_h.png")
    return fig


def plot_convergence(history: list, h: float, save: bool = True):
    """Plot VQE energy vs optimisation step for a single run."""
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(history, "b-")
    ax.set_xlabel("Optimisation step")
    ax.set_ylabel("Energy")
    ax.set_title(f"VQE Convergence  (h/J = {h:.2f})")
    fig.tight_layout()

    if save:
        FIGURES_DIR.mkdir(exist_ok=True)
        fig.savefig(FIGURES_DIR / "convergence.png", dpi=150)
        print("Saved figures/convergence.png")
    return fig


if __name__ == "__main__":
    results = load_results()
    plot_energy(results)
    plot_observables(results)
    plt.show()
