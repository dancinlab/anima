#!/usr/bin/env python3
"""
VQE H2 ground-state via qiskit-nature + Aer simulator + SciPy minimize.


Spec:
  - Geometry: H2 at R=0.735 Angstrom (equilibrium)
  - Basis: STO-3G
  - Mapper: Bravyi-Kitaev
  - Tapering: Z2 symmetry reduction -> 2 qubits
  - Ansatz: TwoLocal RY+CX (1 rep, 4 params for 2 qubits)
  - Optimizer: SciPy COBYLA (gradient-free, robust on noisy energy surface)
  - Exact reference: NumPyMinimumEigensolver on the same tapered operator
  - FCI literature value: -1.137 hartree
  - Falsifier F-VQE-1: |E_VQE - E_FCI_exact| < 1e-3 hartree
"""

import json
import socket
import sys
import time
from pathlib import Path

import numpy as np
# numpy 2.x compat shim for qiskit-nature 0.7.2 (uses removed np.in1d)
if not hasattr(np, "in1d"):
    np.in1d = np.isin  # type: ignore[attr-defined]
from scipy.optimize import minimize

OUT = Path("/tmp/qmirror_vqe_h2_2026_05_03")
OUT.mkdir(parents=True, exist_ok=True)

HOST = socket.gethostname()
if "aiden" not in HOST and "ubu" not in HOST:
    sys.exit(1)

t0 = time.time()

# ---------------------------------------------------------------------------
# 1. Build H2 fermionic Hamiltonian via PySCF, map to qubits via Bravyi-Kitaev
# ---------------------------------------------------------------------------
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import BravyiKitaevMapper, TaperedQubitMapper
from qiskit_nature.units import DistanceUnit

driver = PySCFDriver(
    atom="H 0 0 0; H 0 0 0.735",
    basis="sto3g",
    charge=0,
    spin=0,
    unit=DistanceUnit.ANGSTROM,
)
problem = driver.run()
nuclear_repulsion = float(problem.nuclear_repulsion_energy)

mapper = BravyiKitaevMapper()
fer_op = problem.hamiltonian.second_q_op()
qubit_op_full = mapper.map(fer_op)

# Z2 symmetry tapering -> 2-qubit reduced Hamiltonian (canonical for H2 BK)
tapered = TaperedQubitMapper(mapper)
tapered = problem.get_tapered_mapper(mapper)
qubit_op = tapered.map(fer_op)

print(f"[setup] nuclear_repulsion={nuclear_repulsion:.6f} ha")
print(f"[setup] full BK Hamiltonian: num_qubits={qubit_op_full.num_qubits}, "
      f"terms={len(qubit_op_full)}")
print(f"[setup] tapered Hamiltonian: num_qubits={qubit_op.num_qubits}, "
      f"terms={len(qubit_op)}")

# Spec said "2-qubit ansatz" but qiskit-nature 0.7 finds full Z2 symmetry
# group and tapers to 1 qubit; both are correct ground-state-preserving
# reductions of the 4-qubit BK Hamiltonian. Accept whichever the mapper produces.
assert qubit_op.num_qubits in (1, 2), \
    f"expected 1 or 2 qubits after tapering, got {qubit_op.num_qubits}"
n_qubits_active = qubit_op.num_qubits

# ---------------------------------------------------------------------------
# 2. Exact diagonalization via NumPy (ground-truth reference)
# ---------------------------------------------------------------------------
from qiskit_algorithms import NumPyMinimumEigensolver

exact_solver = NumPyMinimumEigensolver()
exact_result = exact_solver.compute_minimum_eigenvalue(qubit_op)
e_electronic_exact = float(np.real(exact_result.eigenvalue))
e_fci_exact = e_electronic_exact + nuclear_repulsion
print(f"[exact] electronic={e_electronic_exact:.8f} ha  total={e_fci_exact:.8f} ha")

# ---------------------------------------------------------------------------
# 3. Build TwoLocal ansatz (RY rotations + linear CX entangler, 1 rep)
# ---------------------------------------------------------------------------
from qiskit.circuit.library import TwoLocal

if n_qubits_active >= 2:
    ansatz = TwoLocal(
        num_qubits=n_qubits_active,
        rotation_blocks="ry",
        entanglement_blocks="cx",
        entanglement="linear",
        reps=1,
        insert_barriers=False,
    )
    ansatz_label = f"TwoLocal(ry, cx, linear, reps=1, n_qubits={n_qubits_active})"
else:
    # Single-qubit case: TwoLocal with no entangler -> just RY rotations
    ansatz = TwoLocal(
        num_qubits=1,
        rotation_blocks="ry",
        entanglement_blocks=None,
        reps=1,
        insert_barriers=False,
    )
    ansatz_label = "TwoLocal(ry, no entangler, reps=1, n_qubits=1)"
n_params = ansatz.num_parameters
print(f"[ansatz] {ansatz_label} -> {n_params} parameters")

# ---------------------------------------------------------------------------
# 4. Aer Estimator (statevector, deterministic)
# ---------------------------------------------------------------------------
from qiskit_aer.primitives import Estimator as AerEstimator

estimator = AerEstimator(
    backend_options={"method": "statevector", "seed_simulator": SEED},
    run_options={"shots": None, "seed": SEED},  # exact expectation
    approximation=True,
)

trajectory = []  # (iter, params, energy_electronic, energy_total)
iter_counter = {"n": 0}


def cost_fn(params):
    job = estimator.run([ansatz], [qubit_op], [params])
    e_elec = float(job.result().values[0])
    e_total = e_elec + nuclear_repulsion
    iter_counter["n"] += 1
    trajectory.append({
        "iter": iter_counter["n"],
        "params": [float(p) for p in params],
        "e_electronic": e_elec,
        "e_total": e_total,
    })
    return e_elec


# ---------------------------------------------------------------------------
# 5. SciPy COBYLA optimization
# ---------------------------------------------------------------------------
rng = np.random.default_rng(SEED)
x0 = rng.uniform(-np.pi, np.pi, size=n_params)
print(f"[opt] x0={x0.tolist()}")

opt_result = minimize(
    cost_fn,
    x0,
    method="COBYLA",
    options={"maxiter": 500, "rhobeg": 0.5, "disp": False},
)

e_vqe_electronic = float(opt_result.fun)
e_vqe_total = e_vqe_electronic + nuclear_repulsion
delta = abs(e_vqe_total - e_fci_exact)
delta_lit = abs(e_vqe_total - (-1.137))

# F-VQE-1 falsifier: |E_VQE - E_FCI_exact| < 1e-3 hartree
F_VQE_1 = bool(delta < 1e-3)

elapsed = time.time() - t0

verdict = {
    "schema": "anima/qmirror/vqe_h2/1",
    "ts_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "host": HOST,
    "molecule": "H2",
    "geometry_angstrom": "H 0 0 0; H 0 0 0.735",
    "basis": "STO-3G",
    "mapper": "BravyiKitaev + Z2-tapered",
    "num_qubits_full": int(qubit_op_full.num_qubits),
    "num_qubits_tapered": int(qubit_op.num_qubits),
    "num_pauli_terms_tapered": int(len(qubit_op)),
    "ansatz": ansatz_label,
    "n_params": int(n_params),
    "optimizer": "scipy.optimize.minimize(method=COBYLA, maxiter=500)",
    "estimator": "qiskit_aer.primitives.Estimator(statevector, exact, seed=1729)",
    "seed": SEED,
    "nuclear_repulsion_ha": nuclear_repulsion,
    "e_electronic_exact_ha": e_electronic_exact,
    "e_fci_exact_total_ha": e_fci_exact,
    "e_vqe_electronic_ha": e_vqe_electronic,
    "e_vqe_total_ha": e_vqe_total,
    "delta_vs_exact_ha": delta,
    "delta_vs_literature_minus_1_137_ha": delta_lit,
    "n_cost_evals": iter_counter["n"],
    "scipy_nfev": int(opt_result.nfev) if hasattr(opt_result, "nfev") else None,
    "scipy_status": int(opt_result.status) if hasattr(opt_result, "status") else None,
    "scipy_success": bool(opt_result.success),
    "scipy_message": str(opt_result.message),
    "F_VQE_1": {
        "criterion": "|E_VQE - E_FCI_exact| < 1e-3 ha",
        "delta_ha": delta,
        "threshold_ha": 1e-3,
        "verdict": "PASS" if F_VQE_1 else "FAIL",
    },
    "elapsed_seconds": elapsed,
}

with open(OUT / "verdict.json", "w") as f:
    json.dump(verdict, f, indent=2)

with open(OUT / "energy_trajectory.json", "w") as f:
    json.dump({
        "schema": "anima/qmirror/vqe_h2_trajectory/1",
        "n_evals": iter_counter["n"],
        "nuclear_repulsion_ha": nuclear_repulsion,
        "trajectory": trajectory,
    }, f, indent=2)

print()
print("=" * 60)
print(f"E_VQE_total      = {e_vqe_total:+.8f} ha")
print(f"E_FCI_exact      = {e_fci_exact:+.8f} ha")
print(f"|delta vs exact| = {delta:.2e} ha")
print(f"|delta vs -1.137|= {delta_lit:.2e} ha")
print(f"F-VQE-1          = {'PASS' if F_VQE_1 else 'FAIL'} (threshold 1e-3 ha)")
print(f"cost evals       = {iter_counter['n']}")
print(f"elapsed          = {elapsed:.2f} s")
print("=" * 60)
print(f"verdict: {OUT / 'verdict.json'}")
print(f"trajectory: {OUT / 'energy_trajectory.json'}")
