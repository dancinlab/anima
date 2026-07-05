#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""σ·thread (Ψ-SOMA PERSIST) — rung-2 ENGINE-NATIVE (real engine_cli.py §SelfIdentity self_* ops).

Ψ-SOMA Phase-2 (6th engine-native σ axis). σ·thread = does the self persist across time/sessions through
a stable anchor (H_1471), and is that persistence EARNED (collapses without the anchor)? Uses `self_new`
(fresh identity), `self_drift` (per-tick evolution), `self_cos` (recognition cosine).

  intact   : anchored self drifts but stays recognizable → self_cos(anchor, drifted) HIGH (continuity).
  impostor : a different identity axis → self_cos(self, impostor) LOW (self≠other — discrimination).
  ablate   : no anchor → each session re-seeds a fresh random identity → cross-session self_cos LOW
             (identity does not carry over = the assistant/stateless failure mode).

Frozen bars (pre-registered · p7): B1 continuity>=0.75 · B2 continuity-impostor>=0.30 ·
B3 continuity-ablate>=0.30. PASS=B1∧B2∧B3. engine-native (real ops) → rung-2 TERMINAL-eligible.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "core"))
import engine_cli as E

DIM, N_ID, DRIFT_TICKS = 16, 40, 24

def drifted(axis, ticks, step=0.02):
    s = E.self_new(DIM, axis)
    for t in range(ticks):
        s = E.self_drift(s, t, step)
    return s

def run(seed=7):
    rng = np.random.RandomState(seed)
    axes = rng.randint(0, DIM, N_ID)                          # each identity anchored on an axis
    cont, imp, abl = [], [], []
    for k in range(N_ID):
        anchor = E.self_new(DIM, int(axes[k]))
        cur = drifted(int(axes[k]), DRIFT_TICKS)              # same identity, drifted across a session
        cont.append(E.self_cos(anchor, cur))                  # continuity: anchor recognizes drifted self
        other = int((axes[k] + 1 + rng.randint(DIM - 1)) % DIM)
        imp.append(E.self_cos(anchor, E.self_new(DIM, other)))# impostor: a different identity
        # ablate: no anchor — session re-seeds a fresh random identity → compare two independent sessions
        a1 = drifted(int(rng.randint(DIM)), DRIFT_TICKS); a2 = drifted(int(rng.randint(DIM)), DRIFT_TICKS)
        abl.append(E.self_cos(a1, a2))
    continuity = float(np.mean(cont)); impostor = float(np.mean(imp)); ablate = float(np.mean(abl))
    bars = {
        "B1_CONTINUITY>=0.75": continuity >= 0.75,
        "B2_CONT-IMPOSTOR>=0.30": (continuity - impostor) >= 0.30,
        "B3_CONT-ABLATE>=0.30": (continuity - ablate) >= 0.30,
    }
    verdict = ("ENGINE-NATIVE-VALID(rung2 · σ·thread earned)" if all(bars.values())
               else "PARTIAL" if bars["B1_CONTINUITY>=0.75"] else "FLOOR")
    out = {"probe": "σ·thread rung-2 ENGINE-NATIVE (real engine_cli.py §SelfIdentity self_* ops · H_1471)",
           "engine_native": True, "dim": DIM, "n_id": N_ID, "drift_ticks": DRIFT_TICKS,
           "metrics": {"continuity": round(continuity,3), "impostor": round(impostor,3), "ablate": round(ablate,3),
                       "delta_cont_impostor": round(continuity-impostor,3),
                       "delta_cont_ablate": round(continuity-ablate,3)},
           "bars": {k: bool(v) for k,v in bars.items()}, "verdict": verdict}
    json.dump(out, open(os.path.join(HERE, "SIGMA_THREAD_RUNG2_RESULT.json"), "w"), ensure_ascii=False, indent=1)
    for k,v in out["metrics"].items(): print(f"  {k:22s} = {v}")
    print("  " + "  ".join(("✓" if v else "✗")+k.split('_')[1].split('>')[0] for k,v in bars.items()))
    print(f"\nσ·thread rung-2 VERDICT: {verdict}")
    return out

if __name__ == "__main__":
    run()
