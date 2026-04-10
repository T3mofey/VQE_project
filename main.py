"""
main.py
-------
Entry point. Runs a single VQE, then optionally the full sweep.

Usage
-----
  python main.py              # single run at h/J = 1.0
  python main.py --sweep      # full h/J sweep (slow, ~10-30 min)
  python main.py --plot-only  # load saved results and plot
"""

import argparse
from vqe import run_vqe
from exact_diag import ground_state_energy
from sweep import run_sweep
from plot import load_results, plot_energy, plot_observables, plot_convergence
import matplotlib.pyplot as plt


def single_run(n_qubits=6, h=1.0):
    print(f"\n{'='*50}")
    print(f"VQE single run  |  n={n_qubits}, h/J={h}")
    print("="*50)

    exact_E0, _ = ground_state_energy(n_qubits, J=1.0, h=h)
    print(f"Exact ground state energy: {exact_E0:.6f}")

    vqe_energy, params, history = run_vqe(
        n_qubits=n_qubits,
        h=h,
        n_layers=3,
        n_steps=300,
        verbose=True,
    )

    error = abs(vqe_energy - exact_E0)
    print(f"\nVQE energy  : {vqe_energy:.6f}")
    print(f"Exact energy: {exact_E0:.6f}")
    print(f"Error       : {error:.2e}  ({100*error/abs(exact_E0):.3f}%)")

    plot_convergence(history, h=h)
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="VQE for the Transverse-Field Ising Model")
    parser.add_argument("--sweep", action="store_true", help="Run the full h/J sweep")
    parser.add_argument("--plot-only", action="store_true", help="Plot previously saved results")
    parser.add_argument("--n-qubits", type=int, default=6)
    parser.add_argument("--h", type=float, default=1.0, help="Transverse field (single run)")
    args = parser.parse_args()

    if args.plot_only:
        results = load_results()
        plot_energy(results)
        plot_observables(results)
        plt.show()

    elif args.sweep:
        results = run_sweep(n_qubits=args.n_qubits)
        plot_energy(results)
        plot_observables(results)
        plt.show()

    else:
        single_run(n_qubits=args.n_qubits, h=args.h)


if __name__ == "__main__":
    main()
