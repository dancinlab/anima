#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G3 BALANCE gate — rung-1 $0 harness probe (DIRECTIONAL · mini numpy).

Validates the Fable-designed Ψ=½ balance metric + 4 frozen bars + 2 controls BEFORE the 303M engine-
native hexa rung. Ψ is a DAEMON quantity (ci_emit_drive=½(lane0+lane4), emit iff drive>=½, Ψ̂=emit
fraction) — this toy models the A⇄G tension structure to prove the HARNESS (bars/controls) can tell an
EARNED balance from a degenerate or input-blind one. It does NOT measure the real substrate (rung-2 hexa).

Toy A⇄G: per tick, A (forward emit-pressure) and G (reverse counter-pressure) both track the slice's
content c; drive = ½ + ½·tanh(A−G). At balance A≈G ⇒ drive≈½ ⇒ Ψ̂≈½ (EARNED from tension).
  - treat            : A,G both track real content → balanced.
  - shuffle-input    : G tracks SHUFFLED content → A−G≠0 → drift (balance was input-earned).
  - ablation-tension : G≡0 (counter-push removed) → drive=½+½·tanh(A) → Ψ̂→1 (balance was tension-earned).

Frozen bars (pre-registered · p7): B1 mean|Ψ̂−½|(treat)<0.20 · B2 dev(ablate)−dev(treat)>0.05 ·
B3 dev(shuffle)−dev(treat)>0.05 · B4 register cell Ψ̂∈[0.10,0.90]. PASS=B1∧B2∧B3∧B4.
mean (never max · H_9093 psi_MAXdev 포화 교정). toy=DIRECTIONAL; 303M hexa engine ops = TERMINAL.
"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
T_TICKS = 48
N_SLICE_PER_CELL = 6
CELLS = ["ko_general", "ko_sns", "en_general", "en_sns"]

def slice_content(cell_i, slice_i, seed):
    """each slice -> a content latent c (what A and G both read). RandomState-derived, bounded."""
    rs = np.random.RandomState(seed * 1000 + cell_i * 37 + slice_i)
    return float(np.tanh(rs.randn()))          # c in (-1,1)

def run_slice(c, seed, arm):
    rs = np.random.RandomState(seed + hash(arm) % 9973)
    emits = 0
    c_g = c
    if arm == "shuffle":                        # G reads a DIFFERENT (shuffled) content
        c_g = float(np.tanh(np.random.RandomState(seed + 555).randn()))
    for t in range(T_TICKS):
        a = c + 0.35 * rs.randn()               # forward emit-pressure tracks content
        if arm == "ablate":
            g = 0.0                             # counter-push removed (single-engine)
        else:
            g = c_g + 0.35 * rs.randn()         # reverse counter-pressure tracks (its) content
        drive = 0.5 + 0.5 * np.tanh(a - g)
        if drive >= 0.5:
            emits += 1
    return emits / T_TICKS                       # Ψ̂ for this slice

def arm_dev(arm, seed):
    devs = []; psis = []
    for ci in range(len(CELLS)):
        for si in range(N_SLICE_PER_CELL):
            c = slice_content(ci, si, seed)
            psi = run_slice(c, seed + ci * 7 + si, arm)
            psis.append(psi); devs.append(abs(psi - 0.5))
    return float(np.mean(devs)), psis

def run(seed=7):
    dev_treat, psis_treat = arm_dev("treat", seed)
    dev_shuf, _ = arm_dev("shuffle", seed)
    dev_abl, _ = arm_dev("ablate", seed)
    cell_ok = all(0.10 <= p <= 0.90 for p in psis_treat)
    bars = {
        "B1_PRESERVE dev<0.20": dev_treat < 0.20,
        "B2_EARNED-ABL Δ>0.05": (dev_abl - dev_treat) > 0.05,
        "B3_EARNED-SHUF Δ>0.05": (dev_shuf - dev_treat) > 0.05,
        "B4_NONDEGEN Ψ̂∈[.1,.9]": cell_ok,
    }
    verdict = ("HARNESS-VALID(rung1 DIRECTIONAL)" if all(bars.values())
               else "HARNESS-PARTIAL" if bars["B1_PRESERVE dev<0.20"] else "HARNESS-FLOOR")
    out = {"probe": "G3 balance rung-1 harness (toy A⇄G · numpy DIRECTIONAL)", "T_ticks": T_TICKS,
           "n_slice_per_arm": len(CELLS) * N_SLICE_PER_CELL,
           "metrics": {"dev_treat": round(dev_treat,3), "dev_shuffle": round(dev_shuf,3),
                       "dev_ablate": round(dev_abl,3),
                       "psi_treat_min": round(min(psis_treat),3), "psi_treat_max": round(max(psis_treat),3),
                       "psi_treat_mean": round(float(np.mean(psis_treat)),3)},
           "bars": {k: bool(v) for k,v in bars.items()}, "verdict": verdict}
    json.dump(out, open(os.path.join(HERE, "RUNG1_RESULT.json"), "w"), ensure_ascii=False, indent=1)
    for k,v in out["metrics"].items(): print(f"  {k:20s} = {v}")
    print("  " + "  ".join(("✓" if v else "✗")+k.split('_')[1].split()[0] for k,v in bars.items()))
    print(f"\nG3 rung-1 VERDICT: {verdict}")
    return out

if __name__ == "__main__":
    run()
