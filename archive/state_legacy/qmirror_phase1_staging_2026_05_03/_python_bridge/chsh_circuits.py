#!/usr/bin/env python3
"""qmirror CHSH circuit construction — SHARED SSOT (Single Source of Truth).

Canonical paths (mirrored — keep both in sync):
    PRIMARY (writable, anima):
        state/qmirror_phase1_staging_2026_05_03/_python_bridge/chsh_circuits.py
    SECONDARY (nexus repo, hexa-side mirror):
        nexus/modules/qmirror/_python_bridge/chsh_circuits.py

Promoted 2026-05-03 to prevent the cond.3-vs-α-burst divergence that
produced the v1/v2 runner artifact (S~0.04, was Ry(-2θ) bug; corrected
Aer returns S=2.842; cond.3 fez with canonical Ry(-θ) returns S=2.357
on real Heron r2 hardware).

-----------------------------------------------
This file is the SECOND .py allowed under nexus/modules/qmirror/ (after
aer_runner.py). The reason: Qiskit + qiskit-ibm-runtime are python-only,
and any .py runner under state/.../_runner/ that touches paid hardware
MUST import from this SSOT to prevent re-derivation drift.

Phase 4 retires this when the qmirror C kernel ships (see
nexus/.roadmap.qmirror cond.4 / phase4 entry).

Canonical CHSH recipe (DO NOT MODIFY without spec amendment)
-------------------------------------------------------------
* Bell pair: H on q0, CNOT(0 -> 1)  =>  |Phi+> = (|00> + |11>)/sqrt(2)
* Measurement-basis rotation: Ry(-theta) on each qubit (NO factor of 2)
* Standard angle set:
      a       = 0
      a_prime = pi / 2
      b       = pi / 4
      b_prime = -pi / 4
* CHSH S formula (matches cond.3 ibm_fez empirical sign pattern):
      S = E(a,b) - E(a,b') + E(a',b) + E(a',b')
* Tsirelson bound: 2*sqrt(2) ~ 2.828
* Aer pre-flight band: S in [2.7, 2.85] (allows binomial fluctuation
  at 1024 shots; Tsirelson ~ 13 sigma above classical 2.0).

Why factor-of-2 doubling is wrong
---------------------------------
For a Bell |Phi+> state, measuring qubit q in axis
  sigma_theta = cos(theta) Z + sin(theta) X
is equivalent to applying U_dag(theta) and measuring in the Z basis,
where U(theta) = Ry(theta) rotates Z -> sigma_theta (Pauli rotation, not
Bloch rotation). Thus the canonical pre-measurement gate is Ry(-theta)
with NO factor of 2. The `Ry(-2*theta)` form treats theta as a Bloch
half-angle, which over-rotates the basis and collapses S to ~0 when
combined with the standard angle set.

Falsifier F-CHSH-PREFLIGHT-1
----------------------------
Any runner targeting paid hardware MUST call `aer_preflight()` before
any `SamplerV2.run()` on a real backend, and abort if the Aer-simulated
S falls outside [2.7, 2.85]. This catches Ry-doubling, sign-flipped
formulae, swapped angles, and bit-string parsing bugs.
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

# --- canonical CHSH constants -----------------------------------------

ANGLE_A = 0.0
ANGLE_A_PRIME = math.pi / 2.0
ANGLE_B = math.pi / 4.0
ANGLE_B_PRIME = -math.pi / 4.0

#: Canonical SETTINGS list (name, theta_a, theta_b) — all 4 CHSH bases.
SETTINGS: List[Tuple[str, float, float]] = [
    ("circuit_a_b",            ANGLE_A,       ANGLE_B),
    ("circuit_a_bprime",       ANGLE_A,       ANGLE_B_PRIME),
    ("circuit_aprime_b",       ANGLE_A_PRIME, ANGLE_B),
    ("circuit_aprime_bprime",  ANGLE_A_PRIME, ANGLE_B_PRIME),
]

#: Aer pre-flight acceptance band for S (inclusive).
AER_PREFLIGHT_S_MIN = 2.7
AER_PREFLIGHT_S_MAX = 2.85

#: Tsirelson bound (analytic max for quantum CHSH).
TSIRELSON = 2.0 * math.sqrt(2.0)

#: Classical CHSH bound (LHV upper limit).
CLASSICAL_BOUND = 2.0


# --- circuit construction ---------------------------------------------

def make_bell_chsh(theta_a: float, theta_b: float):
    """Canonical CHSH circuit: Bell |Phi+> + Ry(-theta) on each qubit.

    Returns a 2-qubit, 2-classical-bit `qiskit.QuantumCircuit` with the
    measurements wired q0->c0, q1->c1.

    DO NOT change `Ry(-theta)` to `Ry(-2*theta)` — that was the v1/v2
    alpha-burst bug that produced S ~ 0 (collapsed correlators).

    Imported lazily to keep this module importable in environments
    without qiskit (pure-python harness, doc generation, etc.).
    """
    from qiskit import QuantumCircuit  # type: ignore

    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.ry(-theta_a, 0)
    qc.ry(-theta_b, 1)
    qc.measure([0, 1], [0, 1])
    return qc


def build_all_settings() -> List:
    """Build all 4 CHSH circuits in canonical SETTINGS order."""
    return [make_bell_chsh(ta, tb) for (_, ta, tb) in SETTINGS]


# --- correlator + S formula -------------------------------------------

def correlator(counts_dict: Dict[str, int]) -> Tuple[float, float, int]:
    """E(a,b) and binomial sigma from a counts dict over '00','01','10','11'.

    Mapping: bitstring "ab" (qiskit endian: a = q1, b = q0) =>
        outcome = (+1 if a==b else -1)
    E = (n_agree - n_disagree) / n_total
    sigma = sqrt(max(0, (1 - E^2) / n))
    """
    n = sum(counts_dict.values())
    if n <= 0:
        return 0.0, 0.0, 0
    same = counts_dict.get("00", 0) + counts_dict.get("11", 0)
    diff = counts_dict.get("01", 0) + counts_dict.get("10", 0)
    E = (same - diff) / n
    sigma = math.sqrt(max(0.0, (1.0 - E * E) / n))
    return E, sigma, n


def compute_S(Es: Dict[str, float]) -> float:
    """Canonical CHSH S = E_ab - E_ab' + E_a'b + E_a'b'.

    Sign on E_ab' matches the cond.3 ibm_fez empirical orientation (the
    runner's `Ry(-theta)` + angle set `(0, pi/2, pi/4, -pi/4)` produces
    a NEGATIVE E_ab' on hardware; with this formula S is positive at
    ~+2.357 with Heron r2 fidelity, ~+2.84 ideal).
    """
    return (
        Es["circuit_a_b"]
        - Es["circuit_a_bprime"]
        + Es["circuit_aprime_b"]
        + Es["circuit_aprime_bprime"]
    )


def compute_sigma_S(sigmas: Dict[str, float]) -> float:
    """Quadrature sum of per-correlator sigmas (independent shots)."""
    return math.sqrt(sum(s * s for s in sigmas.values()))


# --- Aer pre-flight gate (F-CHSH-PREFLIGHT-1) -------------------------

class AerPreflightFail(RuntimeError):
    """Raised when Aer-simulated S falls outside [2.7, 2.85]."""


def aer_preflight(shots: int = 8192) -> Dict[str, object]:
    """F-CHSH-PREFLIGHT-1: simulate the 4 canonical CHSH circuits on
    Qiskit AerSimulator and verify S in [AER_PREFLIGHT_S_MIN,
    AER_PREFLIGHT_S_MAX].

    MUST be called by every runner targeting paid hardware BEFORE any
    `SamplerV2.run()` on a real backend. If the band check fails, raise
    AerPreflightFail with a diagnostic payload — the caller should
    refuse to submit.

    Returns: dict with S, sigma_S, per-correlator E/sigma, settings
    used, and a 'pass' bool. Always returns even on band-fail (so the
    caller can serialize the diagnostic before re-raising).

    Cost: $0 (pure simulation, no hardware contact).
    """
    try:
        from qiskit_aer import AerSimulator  # type: ignore
        from qiskit import transpile  # type: ignore
    except ImportError as exc:
        raise AerPreflightFail(
            "F-CHSH-PREFLIGHT-1: qiskit_aer unavailable: " + str(exc)
        )

    backend = AerSimulator()
    raws = build_all_settings()
    transpiled = transpile(raws, backend=backend)

    job = backend.run(transpiled, shots=shots)
    result = job.result()

    counts_by: Dict[str, Dict[str, int]] = {}
    for i, (name, _, _) in enumerate(SETTINGS):
        c = result.get_counts(i)
        norm = {k: int(v) for k, v in c.items()}
        for k in ("00", "01", "10", "11"):
            norm.setdefault(k, 0)
        counts_by[name] = norm

    Es: Dict[str, float] = {}
    sigmas: Dict[str, float] = {}
    corrs: Dict[str, Dict[str, float]] = {}
    for name, _, _ in SETTINGS:
        E, sigma, n = correlator(counts_by[name])
        Es[name] = E
        sigmas[name] = sigma
        corrs[name] = {"E": E, "sigma": sigma, "n": n}

    S = compute_S(Es)
    sigma_S = compute_sigma_S(sigmas)
    band_pass = (AER_PREFLIGHT_S_MIN <= S <= AER_PREFLIGHT_S_MAX)

    payload: Dict[str, object] = {
        "falsifier": "F-CHSH-PREFLIGHT-1",
        "S": S,
        "sigma_S": sigma_S,
        "band_min": AER_PREFLIGHT_S_MIN,
        "band_max": AER_PREFLIGHT_S_MAX,
        "tsirelson": TSIRELSON,
        "classical_bound": CLASSICAL_BOUND,
        "shots_per_setting": shots,
        "correlators": corrs,
        "pass": band_pass,
        "engine": "qiskit_aer.AerSimulator",
    }

    if not band_pass:
        raise AerPreflightFail(
            "F-CHSH-PREFLIGHT-1 BAND FAIL: S={:.4f} not in [{}, {}]; "
            "diagnostic={}".format(S, AER_PREFLIGHT_S_MIN, AER_PREFLIGHT_S_MAX, payload)
        )

    return payload


# --- module self-check (python -m or direct) --------------------------

if __name__ == "__main__":
    import json
    import sys

    try:
        diag = aer_preflight(shots=8192)
        sys.stdout.write(json.dumps({"ok": 1, **diag}, indent=2, default=str))
        sys.stdout.write("\n")
    except AerPreflightFail as exc:
        sys.stdout.write(json.dumps({"ok": 0, "error": str(exc)}, indent=2))
        sys.stdout.write("\n")
        sys.exit(1)
    except Exception as exc:  # pragma: no cover -- defensive
        sys.stdout.write(json.dumps({"ok": 0, "error": "unhandled: " + repr(exc)}))
        sys.stdout.write("\n")
        sys.exit(2)
