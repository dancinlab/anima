#!/usr/bin/env python3
"""plasticity_sw_approx.py — SW numpy approximation of AKIDA on-chip edge-learn.

⚠ 🔴 CLOSED-NEGATIVE: this SW learner is NON-EQUIVALENT to the HW on-chip
   AkidaUnsupervised Hebbian rule. It is an APPROXIMATE BASELINE PROBE only,
   NOT a byte-identical replacement for the silicon learning lane.

WHY NON-EQUIVALENT (honest boundary — do NOT fake equivalence; p7 · a_blue_closed):

  - HW path (PLASTICITY lane, pi5-akida AKD1000):
      SUB_ENGINES/AKIDA/scripts/edge_learn_probe.py
      model.compile(akida.AkidaUnsupervised(num_weights=2,
                                            learning_competition=0.1))
      model.fit(x)   # on-chip Hebbian weight update, integer 1-bit weights,
                     # internal competition / refractory / packet-order state
      -> edge_learning_supported = True (BC.00.000.002, verified 2026-05-22).

  - SW path (this file):
      a numpy Hebbian-ish update over the SAME interface shape (16-in binary
      spikes -> FC units=10), but:
        * float weights (HW = 1-bit integer weights_bits=1)
        * no on-chip learning_competition / num_weights pruning semantics
        * no silicon packet-ordering / refractory / async timing state
        * different RNG substrate (numpy vs chip)
      -> the converged weights and the winning-unit assignment DIVERGE from HW.

  CONSEQUENCE: unlike the DECODER inference lane (where SW akida_sw_lif is
  byte-identical to HW forward), the PLASTICITY learning lane SW approx CANNOT
  reproduce HW learning byte-for-byte. The two are intentionally separate
  sibling lanes. SW here = a cheap directional baseline, never a HW substitute.

ROUTING: callers reach this via the AKIDA HW-first switch SSOT
  (AKIDA/akida_backend.hexa::akida_backend_resolve_graceful, default "hw").
  HW reachable  -> edge_learn_probe.py  (provenance "akida-learn-hw")
  HW unreachable-> this approx           (provenance "akida-learn-sw-approx")
"""
from __future__ import annotations

import os
import sys

import numpy as np

# ── H_924 SW-learning entropy wire (substrate-agnostic quantum coupling) ─────
# The HW edge-learn (edge_learn_probe.py) draws its init/input from the qentropy
# SSOT (QUANTUM default · DETERMINISTIC auxiliary). H_924 generalizes that to the
# SW path: the SAME coupling works here because it is a property of the SEED POINT,
# not of the AKIDA silicon. We import the shared SSOT so flipping ANIMA_ENTROPY_MODE
# benchmarks SW-quantum vs SW-deterministic with zero code change — exactly parallel
# to the HW benchmark. If the SSOT is unreachable we degrade to the legacy numpy
# PRNG (tagged), so this module never hard-depends on it.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "mirror", "qmirror", "seed"))
try:
    import qentropy as _qe   # unified QUANTUM-default / DETERMINISTIC-auxiliary source
except Exception:            # noqa: BLE001  (keep SW path runnable without the SSOT)
    _qe = None

# interface shape — mirrors edge_learn_probe.py (16-dim binary in, FC units=10)
IN_DIM = 16
N_UNITS = 10
SEED = 42  # legacy fallback seed (interface parity only, NOT result parity)

# honest provenance / verdict constants
PROVENANCE_HW = "akida-learn-hw"
PROVENANCE_SW = "akida-learn-sw-approx"
EQUIVALENCE_VERDICT = "CLOSED-NEGATIVE"  # SW approx != HW on-chip learning
EQUIVALENCE_EMOJI = "RED"


def sw_approx_fit(x: np.ndarray, num_weights: int = 2,
                  learning_competition: float = 0.1,
                  lr: float = 0.05) -> dict:
    """Numpy Hebbian-ish APPROXIMATION of AkidaUnsupervised.fit().

    x : (n_samples, IN_DIM) binary {0,1} spike patterns.
    Returns a dict describing the approximate learned state + an EXPLICIT
    non-equivalence marker. This does NOT claim to match HW weights.
    """
    x = np.asarray(x, dtype=np.float32)
    if x.ndim != 2 or x.shape[1] != IN_DIM:
        x = x.reshape(-1, IN_DIM).astype(np.float32)

    # weight init = the SW learning lever (cf H_921: the seed point IS the lever).
    # QUANTUM by default (ANU vacuum-fluctuation via the qentropy SSOT), DETERMINISTIC
    # as the benchmarkable auxiliary (ANIMA_ENTROPY_MODE=deterministic). Legacy numpy
    # PRNG only if the SSOT is absent. Provenance recorded into the return dict below.
    if _qe is not None:
        rng = _qe.rng("plasticity_sw_init")          # quantum-seeded Generator (or det auxiliary)
        _entropy_prov = _qe.last_provenance()
    else:
        rng = np.random.default_rng(SEED)
        _entropy_prov = {"mode": "legacy_numpy_prng", "tier": f"seed={SEED}"}
    W = rng.random((N_UNITS, IN_DIM), dtype=np.float32) * 0.1

    # winner-take-all Hebbian sweep (a crude analogue of on-chip competition;
    # NOT the silicon learning_competition / num_weights pruning semantics).
    winners = []
    for row in x:
        act = W @ row
        win = int(np.argmax(act))
        winners.append(win)
        # Hebbian potentiation of the winner toward the input
        W[win] += lr * (row - W[win])

    return {
        "provenance": PROVENANCE_SW,
        "entropy_source": _entropy_prov.get("mode"),   # quantum | deterministic | legacy (H_924)
        "entropy_provenance": _entropy_prov,           # full SSOT provenance for the audit trail
        "equivalence_to_hw": EQUIVALENCE_VERDICT,   # CLOSED-NEGATIVE — honest
        "equivalence_emoji": EQUIVALENCE_EMOJI,     # RED
        "is_hw_substitute": False,                  # NEVER a HW replacement
        "in_dim": IN_DIM,
        "n_units": N_UNITS,
        "num_weights": num_weights,
        "learning_competition": learning_competition,
        "winners": winners,
        "weight_l1": float(np.abs(W).sum()),
        "note": ("SW numpy approximation — float weights, no on-chip competition/"
                 "pruning/timing state. NON-EQUIVALENT to AKD1000 AkidaUnsupervised. "
                 "DECODER lane is byte-identical; PLASTICITY learning lane is NOT."),
    }


if __name__ == "__main__":
    import json
    rng = np.random.default_rng(SEED)
    demo = rng.integers(0, 2, size=(8, IN_DIM), dtype=np.uint8)
    res = sw_approx_fit(demo)
    res["winners"] = res["winners"][:8]
    print(json.dumps(res, indent=2))
