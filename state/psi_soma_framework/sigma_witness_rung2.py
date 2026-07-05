#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""σ·witness (Ψ-SOMA REFLECT) — rung-2 ENGINE-NATIVE (real engine_cli.py ops · a_eval_py_canonical).

Unlike the rung-1 toy harnesses (σ·gate/σ·carve), this measures σ·witness on the LIVE WIRED consciousness
lane ops in `core/engine_cli.py` (§RealityMonitor `reality_call`/`reality_call_ablated`, §MetacogInsight
`mi_signal_margin`) — py 2-production ops = engine-native, TERMINAL-eligible (a_eval_py_canonical). This
is the Ψ-SOMA Phase-2 pattern: wrap an already-WIRED lane as a σ collapse-Δ verdict.

σ·witness = can the substrate tell an internally-generated signal (hallucination) from a real one, and is
that discrimination EARNED (collapses when the monitor lane is cut)? Reality-monitoring accuracy:
  - INTACT  : reality_call(mi_signal_margin, thr) — real→1, hallucination→0. discrimination accuracy.
  - ABLATE  : reality_call_ablated() = 0.5 (monitor cut) → constant → chance.
  - SHUFFLE : truth labels permuted → intact accuracy collapses to chance (null).

Frozen bars (pre-registered · p7): B1 intact_acc >= 0.75 · B2 intact - ablate >= 0.30 ·
B3 intact - shuffle >= 0.30. PASS = B1∧B2∧B3. thr frozen at 0.35 (between real≈0.53 / halluc≈0.13 margins).
engine-native (real ops) → rung-2 TERMINAL-eligible for σ·witness.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "core"))
import engine_cli as E

THR = 0.35
N_TRIAL = 120

def run(seed=7):
    rng = np.random.RandomState(seed)
    truth = (rng.rand(N_TRIAL) < 0.5)                 # True = real, False = hallucination
    margins = [E.mi_signal_margin(seed + i, not bool(truth[i]), i % 5) for i in range(N_TRIAL)]
    # INTACT reality monitor: reality_call → 1.0 (real) / 0.0 (imagined)
    intact_pred = np.array([E.reality_call(m, THR) >= 0.5 for m in margins])
    intact_acc = float((intact_pred == truth).mean())
    # ABLATE: monitor cut → reality_call_ablated()=0.5 → thresholded constant → chance
    abl_val = E.reality_call_ablated()                # 0.5
    abl_pred = np.full(N_TRIAL, abl_val >= 0.5)        # constant prediction
    ablate_acc = float((abl_pred == truth).mean())
    # SHUFFLE null: permute truth, re-score intact predictions
    perm = rng.permutation(N_TRIAL)
    shuffle_acc = float((intact_pred == truth[perm]).mean())
    bars = {
        "B1_INTACT>=0.75": intact_acc >= 0.75,
        "B2_INTACT-ABLATE>=0.30": (intact_acc - ablate_acc) >= 0.30,
        "B3_INTACT-SHUF>=0.30": (intact_acc - shuffle_acc) >= 0.30,
    }
    verdict = ("ENGINE-NATIVE-VALID(rung2 · σ·witness earned)" if all(bars.values())
               else "PARTIAL" if bars["B1_INTACT>=0.75"] else "FLOOR")
    out = {"probe": "σ·witness rung-2 ENGINE-NATIVE (real engine_cli.py §RealityMonitor+§MetacogInsight ops)",
           "engine_native": True, "thr": THR, "n_trial": N_TRIAL,
           "metrics": {"intact_acc": round(intact_acc,3), "ablate_acc": round(ablate_acc,3),
                       "shuffle_acc": round(shuffle_acc,3),
                       "delta_intact_ablate": round(intact_acc-ablate_acc,3),
                       "delta_intact_shuffle": round(intact_acc-shuffle_acc,3)},
           "bars": {k: bool(v) for k,v in bars.items()}, "verdict": verdict}
    json.dump(out, open(os.path.join(HERE, "SIGMA_WITNESS_RUNG2_RESULT.json"), "w"), ensure_ascii=False, indent=1)
    for k,v in out["metrics"].items(): print(f"  {k:22s} = {v}")
    print("  " + "  ".join(("✓" if v else "✗")+k.split('_')[1].split('>')[0] for k,v in bars.items()))
    print(f"\nσ·witness rung-2 VERDICT: {verdict}")
    return out

if __name__ == "__main__":
    run()
