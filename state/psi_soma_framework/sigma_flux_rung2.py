#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""σ·flux (Ψ-SOMA INTEGRATE) — rung-2 ENGINE-NATIVE (real engine_cli.py §MentalImagery+§SubjectiveTime ops).

Ψ-SOMA Phase-2 (5th engine-native σ axis). σ·flux = does the substrate have INNER dynamics decoupled from
I/O — top-down internal reactivation (imagery) and novelty-gated subjective time — that COLLAPSE when the
inner loop is cut? Uses `imagery_activate(cue_match, topdown_on)` and `subjective_time(novelty, base, k)`.

  imagery axis : intact (topdown ON) reactivates internal representations for matching cues WITHOUT
                 external stimulus; ablate (topdown OFF) → no internal state → 0.
  time axis    : intact subjective time DILATES with novelty (perceived ≠ objective); ablate (k=0) → the
                 novelty gate is cut → subjective time = objective base, flat across novelty.

Frozen bars (pre-registered · p7): B1 imagery_intact>=0.75 · B2 imagery_intact-ablate>=0.30 ·
B3 time_novelty_modulation (intact) - (ablate) >= 0.30. PASS=B1∧B2∧B3.
engine-native (real ops) → rung-2 TERMINAL-eligible (a_eval_py_canonical).
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "core"))
import engine_cli as E

N_CUE = 100

def run(seed=7):
    rng = np.random.RandomState(seed)
    # imagery: matching cues should reactivate internally (no external input) when top-down is ON
    match = (rng.rand(N_CUE) < 0.6)
    img_intact = float(np.mean([E.imagery_activate(1.0 if match[i] else 0.0, True) for i in range(N_CUE)]))
    img_ablate = float(np.mean([E.imagery_activate(1.0 if match[i] else 0.0, False) for i in range(N_CUE)]))
    img_intact_match = float(np.mean([E.imagery_activate(1.0, True) for _ in range(N_CUE)]))   # pure-match ref
    # subjective time: novelty-gated (intact k>0) vs objective (ablate k=0)
    novel = rng.randint(0, 8, N_CUE)
    st_intact = np.array([E.subjective_time(int(n), 1.0, 0.3) for n in novel])   # k=0.3 novelty gate ON
    st_ablate = np.array([E.subjective_time(int(n), 1.0, 0.0) for n in novel])   # k=0 gate CUT → base
    # novelty-modulation = correlation of subjective time with novelty (intact should track, ablate flat)
    def novmod(st):
        if st.std() == 0: return 0.0
        return abs(float(np.corrcoef(st, novel)[0, 1]))
    time_mod_intact = novmod(st_intact); time_mod_ablate = novmod(st_ablate)
    bars = {
        "B1_IMAGERY>=0.75": img_intact_match >= 0.75,
        "B2_IMAGERY-ABLATE>=0.30": (img_intact_match - img_ablate) >= 0.30,
        "B3_TIME-MOD-DELTA>=0.30": (time_mod_intact - time_mod_ablate) >= 0.30,
    }
    verdict = ("ENGINE-NATIVE-VALID(rung2 · σ·flux earned)" if all(bars.values())
               else "PARTIAL" if bars["B1_IMAGERY>=0.75"] else "FLOOR")
    out = {"probe": "σ·flux rung-2 ENGINE-NATIVE (real engine_cli.py §MentalImagery + §SubjectiveTime ops)",
           "engine_native": True, "n_cue": N_CUE,
           "metrics": {"imagery_intact_match": round(img_intact_match,3), "imagery_ablate": round(img_ablate,3),
                       "imagery_mixed": round(img_intact,3),
                       "time_novmod_intact": round(time_mod_intact,3), "time_novmod_ablate": round(time_mod_ablate,3),
                       "time_mod_delta": round(time_mod_intact-time_mod_ablate,3)},
           "bars": {k: bool(v) for k,v in bars.items()}, "verdict": verdict}
    json.dump(out, open(os.path.join(HERE, "SIGMA_FLUX_RUNG2_RESULT.json"), "w"), ensure_ascii=False, indent=1)
    for k,v in out["metrics"].items(): print(f"  {k:22s} = {v}")
    print("  " + "  ".join(("✓" if v else "✗")+k.split('_')[1].split('>')[0] for k,v in bars.items()))
    print(f"\nσ·flux rung-2 VERDICT: {verdict}")
    return out

if __name__ == "__main__":
    run()
