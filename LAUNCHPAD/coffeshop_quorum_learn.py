#!/usr/bin/env python3
"""coffeshop_quorum_learn.py - PLASTICITY learning lane for COFFESHOP emit-quorum.

LAUNCHPAD milestone (PLASTICITY lane): the emit-quorum used by the COFFESHOP
closed loop (coffeshop_akida.py) is not a fixed constant -- it ADAPTS per
stim_type via on-chip edge learning, so anima's interrupt sensitivity changes
with context (e.g. it grows pickier on `private_prompt`, more eager on
`silence`). This is the LEARNING sibling of the (deterministic) inference lane.

ROUTING (AKIDA-first, HW-first switch SSOT):
  AKIDA/akida_backend.hexa::akida_backend_resolve_graceful (default "hw").
    HW reachable   -> on-chip AkidaUnsupervised Hebbian over per-stim spike
                      patterns (SUB_ENGINES/AKIDA/scripts/edge_learn_probe.py
                      interface: InputData input_bits=1 -> FullyConnected
                      units=10 weights_bits=1, model.compile(AkidaUnsupervised),
                      model.fit(x)). provenance "akida-learn-hw".
    HW unreachable -> SW: a FIXED quorum (no adaptation) + an explicit
                      non-equivalence marker. provenance "akida-learn-sw-approx".

  HONEST 🔴 CLOSED-NEGATIVE (p7 . a_blue_closed): the SW path is NOT a
  byte-identical replacement for HW learning. Unlike the inference DECODER lane
  (akida_sw_lif, byte-identical), the PLASTICITY learning lane is intrinsically
  NON-DETERMINISTIC and silicon-specific (1-bit integer weights, on-chip
  competition / pruning / packet-order / refractory timing). The SW fallback
  here is a FIXED-quorum baseline, never a HW substitute. Adaptation is a
  FUNCTION, not a reproduction target -- we do NOT claim SW == HW.

The learned object is small + bounded: a per-stim_type quorum DELTA in
[-Q_DELTA_MAX, +Q_DELTA_MAX] applied to the base quorum (6). On-chip, the
winning-unit count over a stim's spike pattern drives the delta direction;
the exact converged value is non-deterministic (chip state) and is reported
verbatim, never faked.
"""
from __future__ import annotations

import os

import numpy as np

# honest provenance / verdict constants (mirror PLASTICITY/plasticity_sw_approx.py)
PROVENANCE_HW = "akida-learn-hw"
PROVENANCE_SW = "akida-learn-sw-approx"
EQUIVALENCE_VERDICT = "CLOSED-NEGATIVE"   # SW fixed-quorum != HW on-chip learning
EQUIVALENCE_EMOJI = "RED"

BASE_QUORUM = 6              # coffeshop_akida.QUORUM_DEFAULT
Q_DELTA_MAX = 3             # bounded learned delta: quorum in [3, 9]
IN_DIM = 16
N_UNITS = 10
SEED = 42                   # edge_learn_probe rng seed (interface parity only)

# COFFESHOP stim_type set (COFFESHOP.md section 4)
STIM_TYPES = ("direct_mention", "indirect_topic", "silence",
              "private_prompt", "group_drift")


def akida_backend_resolve(arg: str = "") -> str:
    """Mirror of AKIDA/akida_backend.hexa::akida_backend_resolve (default hw)."""
    if arg in ("hw", "sw"):
        return arg
    e = os.environ.get("AKIDA_BACKEND", "")
    if e in ("hw", "sw"):
        return e
    return "hw"


def _try_akida():
    try:
        import importlib
        ak = importlib.import_module("akida")
        devs = ak.devices()
        return (ak, devs[0]) if devs else (ak, None)
    except Exception:
        return (None, None)


def _clamp_quorum(q: int) -> int:
    lo, hi = BASE_QUORUM - Q_DELTA_MAX, BASE_QUORUM + Q_DELTA_MAX
    return max(lo, min(hi, int(q)))


def _stim_spike_patterns(stim_type: str, n_samples: int = 8) -> np.ndarray:
    """Per-stim binary spike patterns (the on-chip learner's training input).
    Density encodes the stim's substrate salience: high-salience stims
    (direct_mention/silence-break) drive denser patterns -> the learner shifts
    quorum down (more eager); restraint stims (private_prompt) -> sparser ->
    quorum up (pickier). The pattern density is a closed design map; the LEARNED
    delta is what the chip computes (non-deterministic on HW)."""
    rng = np.random.default_rng(SEED + hash(stim_type) % 1000)
    density = {"direct_mention": 0.55, "silence": 0.50, "indirect_topic": 0.40,
               "group_drift": 0.35, "private_prompt": 0.20}.get(stim_type, 0.4)
    return (rng.random((n_samples, 1, 1, IN_DIM)) < density).astype(np.uint8)


class QuorumLearnerHW:
    """On-chip AkidaUnsupervised learner of a per-stim quorum delta."""
    provenance = PROVENANCE_HW

    def __init__(self, ak, dev):
        self._ak, self._dev = ak, dev
        m = ak.Model()
        m.add(ak.InputData(input_shape=(1, 1, IN_DIM), input_bits=1, name="in"))
        m.add(ak.FullyConnected(units=N_UNITS, name="fc", weights_bits=1,
                                activation=True))
        m.map(dev)
        m.compile(optimizer=ak.AkidaUnsupervised(num_weights=2,
                                                 learning_competition=0.1))
        self._model = m

    def learn_quorum(self, stim_type: str) -> dict:
        x = _stim_spike_patterns(stim_type)
        self._model.fit(x)                      # on-chip Hebbian (non-det)
        y = self._model.forward(x)              # winning-unit activity
        win = float(np.mean(y > 0))             # on-chip winner density [0,1]
        # denser winners (salient stim) -> lower quorum (more eager to emit)
        delta = int(round((0.5 - win) * 2 * Q_DELTA_MAX))
        q = _clamp_quorum(BASE_QUORUM + delta)
        return {"stim_type": stim_type, "quorum": q, "winner_density": round(win, 4),
                "provenance": self.provenance, "deterministic": False,
                "equivalence": EQUIVALENCE_VERDICT}


class QuorumLearnerSW:
    """SW fallback: FIXED quorum (no adaptation) + honest non-equivalence."""
    provenance = PROVENANCE_SW

    def learn_quorum(self, stim_type: str) -> dict:
        return {"stim_type": stim_type, "quorum": BASE_QUORUM,
                "winner_density": None, "provenance": self.provenance,
                "deterministic": True,          # fixed -> trivially deterministic
                "equivalence": EQUIVALENCE_VERDICT,
                "note": "SW fixed-quorum baseline; NOT HW on-chip learning "
                        "(🔴 CLOSED-NEGATIVE non-equivalence)."}


def build_learner(arg: str = ""):
    """AKIDA-first factory. backend hw (default) -> on-chip learner; on any
    failure flip to SW fixed-quorum with explicit provenance (never fake HW)."""
    backend = akida_backend_resolve(arg)
    if backend == "hw":
        ak, dev = _try_akida()
        if ak is not None and dev is not None:
            try:
                return QuorumLearnerHW(ak, dev)
            except Exception as e:
                print(f"[quorum_learn] HW learn unreachable ({e!r}) -> SW fixed",
                      flush=True)
        else:
            print("[quorum_learn] akida pkg/device absent -> SW fixed", flush=True)
    return QuorumLearnerSW()


def learn_all(arg: str = "") -> dict:
    """Learn a quorum per COFFESHOP stim_type. Returns {stim_type: record}."""
    learner = build_learner(arg)
    return {st: learner.learn_quorum(st) for st in STIM_TYPES}


if __name__ == "__main__":
    import json
    import sys
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    out = learn_all(arg)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    prov = next(iter(out.values()))["provenance"]
    print(f"\nlane provenance: {prov} · equivalence: "
          f"{EQUIVALENCE_EMOJI} {EQUIVALENCE_VERDICT} "
          f"(SW fixed-quorum != HW on-chip learning)")
