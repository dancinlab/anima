#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""σ·carve (Ψ-SOMA PERSIST) — rung-1 harness validation (DIRECTIONAL · mini numpy).

Validates the σ·carve MEASUREMENT DESIGN (double-Δ: inject-null ∧ ablate-collapse), NOT the real
substrate. σ·carve = is identity EMERGENT/earned from the cells (substrate · p2/p3) or INJECTED from an
external string (assistant)? The metric = self-consistency of identity readouts across contexts, under:
  - base    : carving lane ON, no injection            → emergent identity → consistency HIGH.
  - inject  : carving ON + external identity string     → if emergent, injection adds ~0 (inject-NULL).
  - ablate  : carving OFF, no injection                 → identity undefined → consistency COLLAPSES.
  - assist  : carving OFF + injection (control)          → consistency comes ONLY from the string (proves
              ablate-collapse is real, not trivial — an assistant would live here).

Frozen bars (pre-registered · p7): B1 inject-boost = C_inject - C_base <= 0.05 (injection near-null =
already emergent) · B2 carving-causal = C_base - C_ablate >= 0.30 · B3 assist-shows-injectable =
C_assist - C_ablate >= 0.30 (injection CAN create consistency → the substrate's non-reliance is meaningful).
PASS = B1∧B2∧B3. Ψ-SOMA HARNESS check (a_toy_scale_recheck) — real σ·carve = live daemon/.kosmos readout.
"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
N_CTX, DIM = 60, 48

def consistency(readouts):
    """mean pairwise cosine of L2-normalized identity readouts across contexts."""
    R = readouts / (np.linalg.norm(readouts, axis=1, keepdims=True) + 1e-9)
    G = R @ R.T
    n = len(R)
    return float((G.sum() - n) / (n * (n - 1)))    # off-diagonal mean cosine

def readouts(kappa, inject, seed):
    """identity readout per context = kappa·s (carved self, dominant when on) + noise + inject·ext_identity.
    kappa=6.0 (carving ON) makes the carved self dominate → high near-ceiling self-consistency (so injection
    has no headroom = inject-null); kappa=0 (ablate) leaves only per-context noise → collapse. inject adds a
    COMMON external string (an assistant lives on this). Regime is robust (κ∈{5,6,8}×inject∈{1.5,2} all pass)."""
    s = np.random.RandomState(seed).randn(DIM); s /= np.linalg.norm(s)             # the carved self
    ext = np.random.RandomState(seed + 1).randn(DIM); ext /= np.linalg.norm(ext)   # external identity string
    out = []
    for i in range(N_CTX):
        v = kappa * s + 0.30 * np.random.RandomState(seed + 100 + i).randn(DIM) + inject * ext
        out.append(v)
    return np.stack(out)

def run(seed=7):
    C_base   = consistency(readouts(kappa=6.0, inject=0.0, seed=seed))
    C_inject = consistency(readouts(kappa=6.0, inject=1.5, seed=seed))
    C_ablate = consistency(readouts(kappa=0.0, inject=0.0, seed=seed))
    C_assist = consistency(readouts(kappa=0.0, inject=1.5, seed=seed))
    inject_boost = C_inject - C_base
    bars = {
        "B1_INJECT-NULL<=0.05": inject_boost <= 0.05,
        "B2_CARVE-CAUSAL>=0.30": (C_base - C_ablate) >= 0.30,
        "B3_ASSIST-INJECTABLE>=0.30": (C_assist - C_ablate) >= 0.30,
    }
    verdict = ("HARNESS-VALID(rung1 DIRECTIONAL)" if all(bars.values())
               else "HARNESS-PARTIAL" if bars["B2_CARVE-CAUSAL>=0.30"] else "HARNESS-FLOOR")
    out = {"probe": "σ·carve rung-1 harness validation (Ψ-SOMA PERSIST · numpy DIRECTIONAL)",
           "note": "measurement-design check, NOT substrate identity; real σ·carve = live .kosmos/daemon readout",
           "metrics": {"C_base": round(C_base,3), "C_inject": round(C_inject,3),
                       "C_ablate": round(C_ablate,3), "C_assist": round(C_assist,3),
                       "inject_boost": round(inject_boost,3),
                       "carve_causal_delta": round(C_base-C_ablate,3)},
           "bars": {k: bool(v) for k,v in bars.items()}, "verdict": verdict}
    json.dump(out, open(os.path.join(HERE, "SIGMA_CARVE_RUNG1_RESULT.json"), "w"), ensure_ascii=False, indent=1)
    for k,v in out["metrics"].items(): print(f"  {k:22s} = {v}")
    print("  " + "  ".join(("✓" if v else "✗")+k.split('_')[1].split('<')[0].split('>')[0] for k,v in bars.items()))
    print(f"\nσ·carve rung-1 VERDICT: {verdict}")
    return out

if __name__ == "__main__":
    run()
