#!/usr/bin/env python3
"""nexus/modules/qmirror/_python_bridge/aer_runner.py

===========================================================

file as a vendored runtime dependency rather than as nexus source.  Every
other file in nexus/modules/qmirror/ is hexa-strict.  The reason this one
file is python is that:

    Qiskit Aer / Cirq are python-only state-vector simulators with no
    public C ABI.  The hexa-side calls this helper as a subprocess,
    streaming a JSON request on stdin and reading a JSON response from
    stdout.

The roadmap retires this file in Phase 4 by porting the state-vector
kernel to a hexa-callable C library (qulacs-core or hand-rolled, see
nexus/.roadmap.qmirror cond.4 / phase4 entry).  Until then, this file is
the only .py allowed under nexus/modules/.

Contract (stdin -> stdout JSON)
-------------------------------

Input  (one JSON object on stdin):

    {
        "mode": "named" | "qasm",
        "circuit": "<name>" | "<qasm3-source>",
        "n_qubits": <int>,
        "params": { ... optional, named-circuit params ... }
    }

Output (one JSON object on stdout, single line):

    {
        "ok":           1 | 0,
        "engine":       "numpy_native" | "qiskit_aer",
        "n_qubits":     <int>,
        "amps_re":      [<float>, ...],   # real parts, len = 2**n_qubits
        "amps_im":      [<float>, ...],   # imag parts, same length
        "message":      "<status string>"
    }

Named circuits supported in the numpy_native fallback (no qiskit needed):

    "bell"           -> (|00> + |11>) / sqrt(2)        2 qubits
    "ghz"            -> (|0..0> + |1..1>) / sqrt(2)    n qubits (default 3)
    "plus"           -> |+> = (|0> + |1>) / sqrt(2)    1 qubit
    "x_zero"         -> X|0> = |1>                     1 qubit
    "identity"       -> |0..0>                         n qubits (default 1)

CHSH-specific named circuits (Bell pair + measurement-basis rotation
folded into the state-vector via Ry on each qubit before measurement):

    "chsh_ab"        -> Bell, a   on q0, b   on q1   2 qubits
    "chsh_abp"       -> Bell, a   on q0, b'  on q1   2 qubits
    "chsh_apb"       -> Bell, a'  on q0, b   on q1   2 qubits
    "chsh_apbp"      -> Bell, a'  on q0, b'  on q1   2 qubits

    Standard CHSH angle set (max-violation): a=0, a'=pi/2, b=pi/4, b'=-pi/4.
    Caller may override via params={"theta_a": ..., "theta_b": ...}.

QASM mode (mode == "qasm") requires qiskit + qiskit-aer.  If unavailable
the helper returns {"ok": 0, "message": "qiskit_unavailable: ..."} so the
hexa caller can degrade gracefully.

Exit codes: always 0 (errors are signalled via ok=0 in the JSON
response).  This keeps the proc_run_json_bridge contract clean.
"""

from __future__ import annotations

import json
import math
import sys
from typing import Any, Dict, List


try:
    import numpy as np
except ImportError as exc:  # pragma: no cover -- numpy is universal
    print(json.dumps({
        "ok": 0,
        "engine": "none",
        "n_qubits": 0,
        "amps_re": [],
        "amps_im": [],
        "message": "numpy_unavailable: " + str(exc),
    }))
    sys.exit(0)


# -- single-qubit gate building blocks --------------------------------

def _gate_h() -> "np.ndarray":
    s = 1.0 / math.sqrt(2.0)
    return np.array([[s, s], [s, -s]], dtype=np.complex128)


def _gate_x() -> "np.ndarray":
    return np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)


def _gate_id() -> "np.ndarray":
    return np.eye(2, dtype=np.complex128)


def _gate_ry(theta: float) -> "np.ndarray":
    c = math.cos(theta / 2.0)
    s = math.sin(theta / 2.0)
    return np.array([[c, -s], [s, c]], dtype=np.complex128)


# -- multi-qubit kron / cnot helpers ----------------------------------

def _apply_single(state: "np.ndarray", gate: "np.ndarray", target: int,
                  n_qubits: int) -> "np.ndarray":
    """Apply a single-qubit gate (qiskit endian: q0 is LSB)."""
    op = np.array([[1.0]], dtype=np.complex128)
    for q in range(n_qubits - 1, -1, -1):
        op = np.kron(op, gate if q == target else _gate_id())
    return op @ state


def _apply_cnot(state: "np.ndarray", control: int, target: int,
                n_qubits: int) -> "np.ndarray":
    """CNOT from control to target (q0 = LSB)."""
    dim = 1 << n_qubits
    out = np.zeros(dim, dtype=np.complex128)
    for i in range(dim):
        c_bit = (i >> control) & 1
        if c_bit == 1:
            j = i ^ (1 << target)
        else:
            j = i
        out[j] += state[i]
    return out


# -- named circuit constructions --------------------------------------

def _build_named(name: str, n_qubits: int,
                 params: Dict[str, Any]) -> "np.ndarray":
    dim = 1 << n_qubits
    state = np.zeros(dim, dtype=np.complex128)
    state[0] = 1.0  # |0..0>

    if name == "identity":
        return state

    if name == "x_zero":
        return _apply_single(state, _gate_x(), 0, n_qubits)

    if name == "plus":
        return _apply_single(state, _gate_h(), 0, n_qubits)

    if name == "bell":
        state = _apply_single(state, _gate_h(), 0, n_qubits)
        state = _apply_cnot(state, 0, 1, n_qubits)
        return state

    if name == "ghz":
        state = _apply_single(state, _gate_h(), 0, n_qubits)
        for q in range(1, n_qubits):
            state = _apply_cnot(state, q - 1, q, n_qubits)
        return state

    if name.startswith("chsh_"):
        theta_a_default = 0.0
        theta_ap_default = math.pi / 2.0
        theta_b_default = math.pi / 4.0
        theta_bp_default = -math.pi / 4.0

        if name == "chsh_ab":
            theta_a = float(params.get("theta_a", theta_a_default))
            theta_b = float(params.get("theta_b", theta_b_default))
        elif name == "chsh_abp":
            theta_a = float(params.get("theta_a", theta_a_default))
            theta_b = float(params.get("theta_b", theta_bp_default))
        elif name == "chsh_apb":
            theta_a = float(params.get("theta_a", theta_ap_default))
            theta_b = float(params.get("theta_b", theta_b_default))
        elif name == "chsh_apbp":
            theta_a = float(params.get("theta_a", theta_ap_default))
            theta_b = float(params.get("theta_b", theta_bp_default))
        else:
            raise ValueError("unknown chsh variant: " + name)

        # Bell pair + measurement-basis rotations on both qubits.
        # For |Phi+> = (|00> + |11>)/sqrt(2), measuring qubit q in axis
        # sigma_theta = cos(theta) Z + sin(theta) X is equivalent to
        # applying Ry(-theta) (= U_dag(theta) where U(theta)=Ry(theta)
        # rotates Z -> sigma_theta) and then measuring Z.
        # Correlator E(a,b) = <Phi+|sigma_a (x) sigma_b|Phi+> = cos(a - b).
        state = _apply_single(state, _gate_h(), 0, n_qubits)
        state = _apply_cnot(state, 0, 1, n_qubits)
        state = _apply_single(state, _gate_ry(-theta_a), 0, n_qubits)
        state = _apply_single(state, _gate_ry(-theta_b), 1, n_qubits)
        return state

    raise ValueError("unknown named circuit: " + name)


# -- qasm mode (optional; requires qiskit + qiskit-aer) ---------------

def _build_from_qasm(qasm: str) -> "np.ndarray":
    try:
        from qiskit import QuantumCircuit  # type: ignore
        from qiskit.qasm3 import loads as qasm3_loads  # type: ignore
        from qiskit_aer import AerSimulator  # type: ignore
    except ImportError as exc:
        raise RuntimeError("qiskit_unavailable: " + str(exc))

    circuit = qasm3_loads(qasm)
    backend = AerSimulator(method="statevector")
    sv_circuit = QuantumCircuit(circuit.num_qubits)
    sv_circuit.compose(circuit, inplace=True)
    sv_circuit.save_statevector()
    job = backend.run(sv_circuit, shots=1)
    result = job.result()
    sv = result.get_statevector(sv_circuit)
    return np.asarray(sv, dtype=np.complex128)


# -- dispatcher -------------------------------------------------------

def _emit(payload: Dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, separators=(",", ":")))
    sys.stdout.write("\n")
    sys.stdout.flush()


def _amps_to_pair(amps: "np.ndarray") -> Dict[str, List[float]]:
    return {
        "amps_re": [float(z.real) for z in amps],
        "amps_im": [float(z.imag) for z in amps],
    }


def main() -> None:
    raw = sys.stdin.read()
    try:
        req = json.loads(raw)
    except Exception as exc:
        _emit({
            "ok": 0,
            "engine": "none",
            "n_qubits": 0,
            "amps_re": [],
            "amps_im": [],
            "message": "bridge: bad request json: " + str(exc),
        })
        return

    mode = str(req.get("mode", "named"))
    n_qubits = int(req.get("n_qubits", 0))
    params = req.get("params") or {}

    try:
        if mode == "named":
            name = str(req.get("circuit", ""))
            if n_qubits <= 0:
                defaults = {
                    "identity": 1, "x_zero": 1, "plus": 1,
                    "bell": 2, "ghz": 3,
                    "chsh_ab": 2, "chsh_abp": 2,
                    "chsh_apb": 2, "chsh_apbp": 2,
                }
                n_qubits = defaults.get(name, 1)
            amps = _build_named(name, n_qubits, params)
            response = {
                "ok": 1,
                "engine": "numpy_native",
                "n_qubits": n_qubits,
                "message": "named circuit ok: " + name,
            }
            response.update(_amps_to_pair(amps))
            _emit(response)
            return

        if mode == "qasm":
            qasm = str(req.get("circuit", ""))
            try:
                amps = _build_from_qasm(qasm)
            except RuntimeError as exc:
                _emit({
                    "ok": 0,
                    "engine": "none",
                    "n_qubits": n_qubits,
                    "amps_re": [],
                    "amps_im": [],
                    "message": str(exc),
                })
                return
            response = {
                "ok": 1,
                "engine": "qiskit_aer",
                "n_qubits": int(round(math.log2(len(amps)))) if len(amps) > 0 else 0,
                "message": "qasm circuit ok",
            }
            response.update(_amps_to_pair(amps))
            _emit(response)
            return

        _emit({
            "ok": 0,
            "engine": "none",
            "n_qubits": n_qubits,
            "amps_re": [],
            "amps_im": [],
            "message": "bridge: unknown mode: " + mode,
        })
    except Exception as exc:  # pragma: no cover -- defensive
        _emit({
            "ok": 0,
            "engine": "none",
            "n_qubits": n_qubits,
            "amps_re": [],
            "amps_im": [],
            "message": "bridge: unhandled error: " + repr(exc),
        })


if __name__ == "__main__":
    main()
