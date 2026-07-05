#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""σ·schema (Ψ-SOMA REFLECT) — rung-2 ENGINE-NATIVE (real engine_cli.py §AttentionSchema op).

Ψ-SOMA Phase-2 pattern (2nd engine-native σ axis after σ·witness): wrap the WIRED §AttentionSchema lane
`attn_schema_report(true_focus, reported, schema_on)` into a σ collapse-Δ verdict. σ·schema (Graziano AST)
= does the substrate hold an internal model of its OWN attention (report its focus), and is that self-model
EARNED (collapses when the schema is off)?

  intact  : schema_on=True, reported = true_focus (the schema accurately models its own focus) → op≈1.0.
  ablate  : schema_on=False (no self-model)                                                    → op=0.125.
  shuffle : schema_on=True but reported = permuted focus (report decoupled from focus)          → op=0.125.

Frozen bars (pre-registered · p7): B1 intact>=0.75 · B2 intact-ablate>=0.30 · B3 intact-shuffle>=0.30.
PASS=B1∧B2∧B3. engine-native (real op) → rung-2 TERMINAL-eligible (a_eval_py_canonical).
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "core"))
import engine_cli as E

N_TRIAL, K_FOCI = 120, 8

def run(seed=7):
    rng = np.random.RandomState(seed)
    focus = rng.randint(0, K_FOCI, N_TRIAL)                       # the true attended target per trial
    # intact: self-model reports its own focus accurately
    intact = float(np.mean([E.attn_schema_report(int(focus[i]), int(focus[i]), True) for i in range(N_TRIAL)]))
    # ablate: schema off → no self-model
    ablate = float(np.mean([E.attn_schema_report(int(focus[i]), int(focus[i]), False) for i in range(N_TRIAL)]))
    # shuffle: schema on but report decoupled from focus (permuted)
    perm = rng.permutation(N_TRIAL)
    shuffle = float(np.mean([E.attn_schema_report(int(focus[i]), int(focus[perm[i]]), True) for i in range(N_TRIAL)]))
    bars = {
        "B1_INTACT>=0.75": intact >= 0.75,
        "B2_INTACT-ABLATE>=0.30": (intact - ablate) >= 0.30,
        "B3_INTACT-SHUF>=0.30": (intact - shuffle) >= 0.30,
    }
    verdict = ("ENGINE-NATIVE-VALID(rung2 · σ·schema earned)" if all(bars.values())
               else "PARTIAL" if bars["B1_INTACT>=0.75"] else "FLOOR")
    out = {"probe": "σ·schema rung-2 ENGINE-NATIVE (real engine_cli.py §AttentionSchema attn_schema_report)",
           "engine_native": True, "n_trial": N_TRIAL, "k_foci": K_FOCI,
           "metrics": {"intact": round(intact,3), "ablate": round(ablate,3), "shuffle": round(shuffle,3),
                       "delta_intact_ablate": round(intact-ablate,3),
                       "delta_intact_shuffle": round(intact-shuffle,3)},
           "bars": {k: bool(v) for k,v in bars.items()}, "verdict": verdict}
    json.dump(out, open(os.path.join(HERE, "SIGMA_SCHEMA_RUNG2_RESULT.json"), "w"), ensure_ascii=False, indent=1)
    for k,v in out["metrics"].items(): print(f"  {k:22s} = {v}")
    print("  " + "  ".join(("✓" if v else "✗")+k.split('_')[1].split('>')[0] for k,v in bars.items()))
    print(f"\nσ·schema rung-2 VERDICT: {verdict}")
    return out

if __name__ == "__main__":
    run()
