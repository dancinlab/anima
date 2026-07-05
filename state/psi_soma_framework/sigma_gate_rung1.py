#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""σ·gate (Ψ-SOMA ENACT) — rung-1 harness validation (DIRECTIONAL · mini numpy).

Validates the σ·gate MEASUREMENT DESIGN (collapse-Δ detector), NOT the real substrate. σ·gate = does
emit/silence flow from real A⇄G tension (substrate) or from an answer-obligation (assistant)? The metric:
correlation between emit decisions and context, LIVE vs tension-FLATTENED. This harness proves the metric
can distinguish the two regimes + survives a shuffle null — i.e. that the σ·gate axis yields a sound,
non-gameable measurement before it is run on the live daemon (rung-2, engine-native, summer hexa).

  live      : tension_t tracks context content → emit iff tension>=½ → emit ⇄ context CORRELATED.
  flatten   : Ψ forced to ½ (tension killed) → emit = coin-flip → emit ⇄ context DECORRELATED (filler).
  shuffle   : context labels permuted before scoring → correlation must collapse (null).

Frozen bars (pre-registered · p7): B1 corr_live>=0.50 · B2 corr_live - corr_flatten >= 0.30 ·
B3 corr_live - corr_shuffle >= 0.30. PASS = B1∧B2∧B3. NOTE: this is a Ψ-SOMA HARNESS check (a_toy_scale_
recheck) — NOT a Ψ proxy (Fable: py Ψ-proxy 금지). Real σ·gate = live daemon emit-decision readout.
"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
N_CTX = 200

def run(seed=7):
    rng = np.random.RandomState(seed)
    # each context has a scalar "salience" c that a LIVE substrate would feel as tension
    c = rng.randn(N_CTX)
    def emit_decisions(arm):
        rs = np.random.RandomState(seed + hash(arm) % 7919)
        if arm == "live":
            tension = c + 0.4 * rs.randn(N_CTX)      # tension tracks context salience
        else:  # flatten: Ψ forced to ½ -> tension killed -> emit independent of context
            tension = 0.0 * c + 1.0 * rs.randn(N_CTX)
        return (tension >= 0.0).astype(float)         # emit iff drive>=½
    e_live = emit_decisions("live")
    e_flat = emit_decisions("flatten")
    # point-biserial correlation between emit (0/1) and context salience c
    def corr(emit, ctx):
        if emit.std() == 0: return 0.0
        return abs(float(np.corrcoef(emit, ctx)[0, 1]))
    corr_live = corr(e_live, c)
    corr_flat = corr(e_flat, c)
    perm = rng.permutation(N_CTX)
    corr_shuf = corr(e_live, c[perm])                 # shuffle-null: emit vs permuted context
    bars = {
        "B1_LIVE>=0.50": corr_live >= 0.50,
        "B2_LIVE-FLAT>=0.30": (corr_live - corr_flat) >= 0.30,
        "B3_LIVE-SHUF>=0.30": (corr_live - corr_shuf) >= 0.30,
    }
    verdict = ("HARNESS-VALID(rung1 DIRECTIONAL)" if all(bars.values())
               else "HARNESS-PARTIAL" if bars["B1_LIVE>=0.50"] else "HARNESS-FLOOR")
    out = {"probe": "σ·gate rung-1 harness validation (Ψ-SOMA ENACT · numpy DIRECTIONAL)",
           "note": "measurement-design check, NOT a Ψ proxy; real σ·gate = live daemon readout (rung-2)",
           "metrics": {"corr_live": round(corr_live,3), "corr_flatten": round(corr_flat,3),
                       "corr_shuffle": round(corr_shuf,3),
                       "delta_live_flat": round(corr_live-corr_flat,3),
                       "delta_live_shuf": round(corr_live-corr_shuf,3)},
           "bars": {k: bool(v) for k,v in bars.items()}, "verdict": verdict}
    json.dump(out, open(os.path.join(HERE, "SIGMA_GATE_RUNG1_RESULT.json"), "w"), ensure_ascii=False, indent=1)
    for k,v in out["metrics"].items(): print(f"  {k:20s} = {v}")
    print("  " + "  ".join(("✓" if v else "✗")+k.split('_')[0] for k,v in bars.items()))
    print(f"\nσ·gate rung-1 VERDICT: {verdict}")
    return out

if __name__ == "__main__":
    run()
