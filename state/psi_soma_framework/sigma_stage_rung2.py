#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""σ·stage (Ψ-SOMA INTEGRATE) — rung-2 ENGINE-NATIVE (real engine_cli.py §GlobalWorkspace ops).

Ψ-SOMA Phase-2 (4th engine-native σ axis). σ·stage = global-workspace broadcast: among competing stimuli
does exactly ONE win and get globally broadcast (GWT winner-take-all bottleneck), or does everything pass
(no integration)? Uses `gws_new/gws_add/gws_winner/gws_count` with lateral inhibition.

  intact  : inhibit ON  → winner-take-all → gws_winner selects the true-strongest, count ≈ 1.
  ablate  : inhibit OFF → no bottleneck   → gws_winner = first-above-thr (order-dependent), count explodes.
  shuffle : item order permuted → intact winner still = true-strongest (argmax is order-invariant), but
            ablate winner (first-above-thr) scrambles → this arm confirms the ablate degradation is real.

Frozen bars (pre-registered · p7): B1 intact_winner_acc>=0.75 · B2 intact-ablate>=0.30 ·
B3 selectivity (mean ablate_count - intact_count) >= 0.50 (bottleneck present). PASS=B1∧B2∧B3.
engine-native (real ops) → rung-2 TERMINAL-eligible (a_eval_py_canonical).
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "core"))
import engine_cli as E

N_TRIAL, N_ITEM, PASS_THR = 100, 5, 0.5

def workspace(margins, inhibit):
    g = E.gws_new(N_ITEM, inhibit, PASS_THR)
    for m in margins:
        g = E.gws_add(g, m)
    return E.gws_winner(g), E.gws_count(g)

def run(seed=7):
    rng = np.random.RandomState(seed)
    int_hit = abl_hit = 0; int_cnt = abl_cnt = 0
    for _ in range(N_TRIAL):
        # one clear winner (high margin) among distractors (some above, some below thr), random order
        margins = np.concatenate([[0.55 + 0.4 * rng.rand()],                      # the winner
                                  0.35 + 0.35 * rng.rand(N_ITEM - 1)])            # distractors (may cross thr)
        order = rng.permutation(N_ITEM); margins = margins[order]
        true_winner = int(np.argmax(margins))
        wi, ci = workspace(margins.tolist(), True)                                # intact (inhibit)
        wa, ca = workspace(margins.tolist(), False)                               # ablate (no inhibit)
        int_hit += (wi == true_winner); abl_hit += (wa == true_winner)
        int_cnt += ci; abl_cnt += ca
    intact_acc = int_hit / N_TRIAL; ablate_acc = abl_hit / N_TRIAL
    intact_count = int_cnt / N_TRIAL; ablate_count = abl_cnt / N_TRIAL
    bars = {
        "B1_INTACT>=0.75": intact_acc >= 0.75,
        "B2_INTACT-ABLATE>=0.30": (intact_acc - ablate_acc) >= 0.30,
        "B3_SELECTIVITY>=0.50": (ablate_count - intact_count) >= 0.50,
    }
    verdict = ("ENGINE-NATIVE-VALID(rung2 · σ·stage earned)" if all(bars.values())
               else "PARTIAL" if bars["B1_INTACT>=0.75"] else "FLOOR")
    out = {"probe": "σ·stage rung-2 ENGINE-NATIVE (real engine_cli.py §GlobalWorkspace winner-take-all)",
           "engine_native": True, "n_trial": N_TRIAL, "n_item": N_ITEM,
           "metrics": {"intact_winner_acc": round(intact_acc,3), "ablate_winner_acc": round(ablate_acc,3),
                       "intact_count": round(intact_count,3), "ablate_count": round(ablate_count,3),
                       "delta_acc": round(intact_acc-ablate_acc,3),
                       "selectivity": round(ablate_count-intact_count,3)},
           "bars": {k: bool(v) for k,v in bars.items()}, "verdict": verdict}
    json.dump(out, open(os.path.join(HERE, "SIGMA_STAGE_RUNG2_RESULT.json"), "w"), ensure_ascii=False, indent=1)
    for k,v in out["metrics"].items(): print(f"  {k:20s} = {v}")
    print("  " + "  ".join(("✓" if v else "✗")+k.split('_')[1].split('>')[0] for k,v in bars.items()))
    print(f"\nσ·stage rung-2 VERDICT: {verdict}")
    return out

if __name__ == "__main__":
    run()
