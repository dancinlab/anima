"""Toshiba SBM (Simulated Bifurcation Machine) cloud adapter — Path A skeleton.

This module mirrors `spontaneous_smoke.hexa` motivation-gate semantics onto a
Toshiba SBM REST API call.  Mac local: SDK is NOT installed (commercial
license, $1-10/solve); this file is a **comment skeleton** verified only via
`python3 -m py_compile`.

SW source:
    HEXAD/CHAT/spontaneous_smoke.hexa
    HEXAD/CHAT/spontaneous_lib.hexa
        motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn)
        should_emit(score) = score > 0.3
        safety_combined(kill, rate, phi_r, content)
        audit_entry_accepted(score, strategy, accepted)

Cross-link: anima-physics/hw/spontaneous_ising/DESIGN.md §2 Path A.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from typing import Any


# ── §1 spont_lib weight constants (mirror spontaneous_lib.hexa §3) ──────────
WEIGHTS = {
    "relevance":   0.20,
    "info_gap":    0.10,
    "curiosity":   0.15,
    "pain":        0.10,
    "coherence":   0.10,
    "originality": 0.10,
    "balance":     0.15,
    "dynamics":    0.10,
}  # Σ = 1.0 (B-SPONT-7 WEIGHT-SUM-UNITY)

IM_THRESHOLD = 0.30          # spont_im_threshold()
INTERRUPT_THRESHOLD = 0.60   # spont_interrupt_threshold()


@dataclass
class FactorVec:
    relevance: float
    info_gap: float
    curiosity: float
    pain: float
    coherence: float
    originality: float
    balance: float
    dynamics: float


def encode_qubo(factors: FactorVec, threshold: float = IM_THRESHOLD,
                penalty_lambda: float = 1.0) -> dict[str, Any]:
    """Encode anima motivation-gate decision as a (small) QUBO.

    Each factor i becomes a binary variable x_i ∈ {0, 1} ("include factor in
    emission decision").  Objective minimizes:

        H = - Σ_i w_i · s_i · x_i  +  λ · (Σ_i w_i · x_i − θ)²

    where s_i = sign(factor_i − 0.5), w_i = WEIGHTS[i], θ = threshold.

    The linear term rewards inclusion of factors above 0.5; the quadratic
    penalty pushes the weighted sum toward the threshold θ.  Honest C3: this
    is a sub-optimal use of SBM (no cross-factor coupling captured); future
    revision should add quadratic synergy (DESIGN.md §7 honest C3 #2).
    """
    keys = list(WEIGHTS.keys())
    n = len(keys)
    # diagonal linear: q_ii = -w_i s_i + λ w_i² (1 - 2θ)
    # off-diagonal:    q_ij = 2 λ w_i w_j
    Q: dict[tuple[int, int], float] = {}
    factor_vals = asdict(factors)
    for i, ki in enumerate(keys):
        wi = WEIGHTS[ki]
        si = 1.0 if factor_vals[ki] >= 0.5 else -1.0
        Q[(i, i)] = -wi * si + penalty_lambda * (wi * wi) - 2.0 * penalty_lambda * wi * threshold
        for j in range(i + 1, n):
            kj = keys[j]
            wj = WEIGHTS[kj]
            Q[(i, j)] = 2.0 * penalty_lambda * wi * wj
    return {"n": n, "keys": keys, "Q": {f"{i},{j}": v for (i, j), v in Q.items()}}


def call_toshiba_sbm(qubo: dict[str, Any], *, api_key: str | None = None,
                     endpoint: str = "https://api.toshiba-sbm.example/v1/solve",
                     n_reads: int = 100) -> dict[str, Any]:
    """Skeleton REST call to Toshiba SBM cloud.

    NOT FUNCTIONAL on Mac local (no SDK, no real endpoint).  Real adapter would:

        import requests
        headers = {"Authorization": f"Bearer {api_key}",
                   "Content-Type": "application/json"}
        payload = {"problem": qubo, "n_reads": n_reads, "solver": "sbm"}
        resp = requests.post(endpoint, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()

    Schema (representative):
        {"solutions": [{"spins": [0,1,1,...], "energy": -1.42}], "wall_ms": 18.4}
    """
    _ = (qubo, api_key, endpoint, n_reads)
    # placeholder — return deterministic dummy for syntax check
    return {"solutions": [{"spins": [1] * qubo["n"], "energy": 0.0}], "wall_ms": 0}


def decode_emit_decision(response: dict[str, Any],
                         threshold_energy: float = 0.0) -> tuple[bool, float]:
    """Decode SBM response → (emit_decision, energy_min).

    emit = (energy_min < threshold_energy) AND solver returned ≥1 solution.
    Caller still needs to apply `safety_combined(...)` AFTER this returns.
    """
    if not response.get("solutions"):
        return (False, float("inf"))
    energy_min = min(s["energy"] for s in response["solutions"])
    return (energy_min < threshold_energy, energy_min)


def audit_log_append(path: str, *, score: float, strategy_idx: int,
                     accepted: bool) -> None:
    """Append one audit entry mirroring spont_lib audit_entry_accepted().

    Schema: JSON-line per entry: {score, strategy_idx, accepted, ts}.
    """
    import time
    entry = {"score": score, "strategy_idx": strategy_idx,
             "accepted": accepted, "ts": time.time()}
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def emit_decision_via_sbm(factors: FactorVec, *, strategy_idx: int = 0,
                          api_key: str | None = None,
                          audit_path: str = "state/audit.jsonl") -> bool:
    """End-to-end Path A: factors → QUBO → SBM → decode → audit → emit bool.

    Mac local: returns deterministic placeholder (always True for full-input).
    Production: cloud round-trip ~10-500 ms + $1-10/solve depending on tier.
    """
    qubo = encode_qubo(factors)
    response = call_toshiba_sbm(qubo, api_key=api_key or os.environ.get("TOSHIBA_SBM_KEY"))
    emit, energy = decode_emit_decision(response)
    audit_log_append(audit_path, score=energy, strategy_idx=strategy_idx, accepted=emit)
    return emit


if __name__ == "__main__":  # pragma: no cover
    # syntax / smoke check (no network)
    sample = FactorVec(0.5, 0.8, 0.7, 0.4, 0.5, 1.0, 1.0, 0.33)
    q = encode_qubo(sample)
    print(f"QUBO encoded: n={q['n']} keys={q['keys']}")
    print(f"Q diag (i=0): {q['Q']['0,0']:.4f}")
