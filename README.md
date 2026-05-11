# Variational Quantum Eigensolver for the Transverse-Field Ising Model

##  Overview

This project implements a **Variational Quantum Eigensolver (VQE)** to approximate the ground state of the **Transverse-Field Ising Model (TFIM)** - a canonical model in quantum many-body physics.

The project combines:

* quantum simulation (PennyLane)
* classical optimisation
* exact diagonalisation benchmarking

and studies how the system evolves across a **quantum phase transition**.

---

##  Physical Model

We consider a 1D spin chain described by the Hamiltonian:

H = -J Σ ZᵢZᵢ₊₁ - h Σ Xᵢ

Where:

* J - nearest-neighbour interaction strength
* h - transverse magnetic field
* Z, X - Pauli operators

###  Physical Interpretation

* The **interaction term (ZZ)** favours aligned spins -> ordered phase
* The **field term (X)** induces quantum fluctuations -> disordered phase

At the critical point:

 **h / J = 1**

the system undergoes a **quantum phase transition**, where the structure of the ground state changes qualitatively and the energy gap closes.

---

##  Method: Variational Quantum Eigensolver (VQE)

VQE is a hybrid quantum-classical algorithm:

1. Prepare a parameterized quantum state (ansatz)
2. Measure the energy <ψ(θ)|H|ψ(θ)>
3. Optimise parameters θ to minimise energy

By the variational principle:

E(θ) ≥ E₀

---

##  Ansatz

A hardware-efficient ansatz is used:

* Single-qubit rotations (RY gates)
* Entangling CNOT ladder

This enables:

* superposition (via rotations)
* entanglement (via CNOT)

and allows approximation of correlated many-body quantum states.

---

##  Features

*  VQE implementation using PennyLane
*  Exact diagonalisation (NumPy/SciPy) for validation
*  Parameter sweep over h/J
*  Computation of observables:

  * Ground state energy
  * Transverse magnetisation ⟨X⟩
  * Nearest-neighbour correlations ⟨ZᵢZᵢ₊₁⟩
*  Visualisation of phase transition behaviour

---

##  Parameter Sweep (Key Idea)

The transverse field h is varied over a range:

h ∈ [0, 3]

For each value:

* VQE is run to approximate the ground state
* Observables are computed
* Results are compared with exact solutions

This allows reconstruction of the **phase diagram** of the system.

---

##  Results

The project reproduces key physical behaviour:

###  Ordered phase (h/J < 1)

* Strong spin alignment along Z
* High ⟨ZᵢZᵢ₊₁⟩
* Low ⟨X⟩

###  Disordered phase (h/J > 1)

* Spins align with transverse field
* High <X>
* Reduced correlations

###  Critical point (h/J ≈ 1)

* Rapid change in observables
* Closing of the energy gap
* Signatures of a quantum phase transition

VQE results show good agreement with exact diagonalisation for small system sizes.

###  Interpreting results

###  Ground state energy 

VQE tracks the exact solution well for h/J < 1. The divergence after h/J ≈ 1 may be explained by the ansatz being not expressive enough to capture the ground state in the paramagnetic phase (h/J > 1), where the state structure changes significantly after the phase transition. The jumps suggest the optimizer is getting stuck in local minima.

<img width="699" height="399" alt="image" src="https://github.com/user-attachments/assets/019c377e-1407-4dd8-bdf4-778a764f92e1" />

###  Transverse Magnetisation ⟨X⟩ (left)

This should smoothly increase from 0 to 1 as h/J goes from zero to infinity. The dotted line at h/J = 1 marks the phase transition. Curve shows the right trend up to h/J = 1.2, then instability kicks in. The exact result should be a smooth S-curve - the jumps again point to optimizer/ansatz issues in the high-field regime.

###  Nearest-Neighbour ZZ Correlation ⟨Z_i Z_{i+1}⟩ (right)

This should decay from 1 toward 0 as the field dominates and spins align with X rather than Z. Curve shows the correct qualitative decay, again with instability past h/J ≈ 1.2.

<img width="1199" height="399" alt="image" src="https://github.com/user-attachments/assets/77025654-9ced-4647-85ff-0ef230a836c9" />


---

##  Usage

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run a single VQE simulation

```bash
python main.py
```

### Run full parameter sweep

```bash
python main.py --sweep
```

### Plot results

```bash
python main.py --plot-only
```

---

##  Limitations

* Exponential scaling limits exact diagonalisation
* Hardware-efficient ansatz may not fully capture correlations
* Optimisation may suffer from:

  * local minima
  * barren plateaus (for larger systems)

---

##  Future Work

* Implement periodic boundary conditions
* Explore problem-inspired ansatz
* Study scaling with system size and circuit depth
* Analyse optimisation landscape and gradient behaviour
* Compare optimisers and training strategies

---

##  Technologies Used

* Python
* PennyLane
* NumPy / SciPy
* Matplotlib

---

##  Author

Timofey Kotov
MSc Artificial Intelligence for Science and Technology
University of Milano-Bicocca

---

##  Notes

This project was developed as a research-oriented exploration of:

* quantum computing
* variational algorithms
* quantum many-body systems

It demonstrates the use of hybrid quantum-classical methods to study fundamental physical phenomena.
