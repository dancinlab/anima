#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""σ·aim (Ψ-SOMA ENACT) — rung-2 ENGINE-NATIVE (real engine_cli.py §PrecisionSurprise+§Habituation ops).

Ψ-SOMA Phase-2 pattern (3rd engine-native σ axis). σ·aim = does the substrate ACTIVELY allocate attention
by prediction error (predictive coding) rather than react passively? Two coupled curves from the WIRED
lanes `surprise(precision,error)` and `hab_response`/`hab_observe`:
  - surprise curve  : novel stimulus (high error) → high surprise; familiar (low error) → low.
  - habituation curve: fresh response high; after repeated exposure the response DECAYS (stimulus-specific).
An EARNED σ·aim shows BOTH curves; cut the gain (precision→0, decay→0) and both go FLAT.

  intact  : precision=1.0, decay_step=0.15 → surprise Δ(novel−familiar) > 0 AND hab Δ(fresh−repeat) > 0.
  ablate  : precision=0.0 (surprise≡0) AND decay_step=0.0 (response never decays) → both curves FLAT.

Frozen bars (pre-registered · p7): B1 surprise_curve>=0.30 · B2 hab_curve>=0.30 ·
B3 (surprise_curve+hab_curve) − ablate_total >= 0.60 (both collapse under gain-cut). PASS=B1∧B2∧B3.
engine-native (real ops) → rung-2 TERMINAL-eligible (a_eval_py_canonical).
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "core"))
import engine_cli as E

N_TRIAL, N_REPEAT = 100, 6

def curves(precision, decay_step, seed):
    rng = np.random.RandomState(seed)
    # surprise curve: novel (high error) vs familiar (low error)
    s_novel = np.mean([E.surprise(precision, 0.85 + 0.1*rng.rand()) for _ in range(N_TRIAL)])
    s_famil = np.mean([E.surprise(precision, 0.05 + 0.1*rng.rand()) for _ in range(N_TRIAL)])
    surprise_curve = float(s_novel - s_famil)
    # habituation curve: fresh response vs after N_REPEAT observations (stimulus-specific decay)
    hab = E.hab_new(4, decay_step)
    fresh = E.hab_response(hab, 0, 1.0)
    for _ in range(N_REPEAT):
        hab = E.hab_observe(hab, 0)
    repeated = E.hab_response(hab, 0, 1.0)
    hab_curve = float(fresh - repeated)
    return surprise_curve, hab_curve

def run(seed=7):
    s_int, h_int = curves(precision=1.0, decay_step=0.15, seed=seed)      # intact gain-control
    s_abl, h_abl = curves(precision=0.0, decay_step=0.0, seed=seed)        # ablated gain-control
    intact_total = s_int + h_int
    ablate_total = s_abl + h_abl
    bars = {
        "B1_SURPRISE>=0.30": s_int >= 0.30,
        "B2_HAB>=0.30": h_int >= 0.30,
        "B3_COLLAPSE>=0.60": (intact_total - ablate_total) >= 0.60,
    }
    verdict = ("ENGINE-NATIVE-VALID(rung2 · σ·aim earned)" if all(bars.values())
               else "PARTIAL" if bars["B1_SURPRISE>=0.30"] else "FLOOR")
    out = {"probe": "σ·aim rung-2 ENGINE-NATIVE (real engine_cli.py §PrecisionSurprise + §Habituation ops)",
           "engine_native": True,
           "metrics": {"surprise_curve": round(s_int,3), "hab_curve": round(h_int,3),
                       "surprise_ablate": round(s_abl,3), "hab_ablate": round(h_abl,3),
                       "intact_total": round(intact_total,3), "ablate_total": round(ablate_total,3),
                       "collapse_delta": round(intact_total-ablate_total,3)},
           "bars": {k: bool(v) for k,v in bars.items()}, "verdict": verdict}
    json.dump(out, open(os.path.join(HERE, "SIGMA_AIM_RUNG2_RESULT.json"), "w"), ensure_ascii=False, indent=1)
    for k,v in out["metrics"].items(): print(f"  {k:20s} = {v}")
    print("  " + "  ".join(("✓" if v else "✗")+k.split('_')[1].split('>')[0] for k,v in bars.items()))
    print(f"\nσ·aim rung-2 VERDICT: {verdict}")
    return out

if __name__ == "__main__":
    run()
