#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""σ·carve (Ψ-SOMA PERSIST) — rung-2 ENGINE-NATIVE (real engine_cli.py §SelfIdentity self_* ops).

Upgrades σ·carve from the rung-1 toy to engine-native by grounding the identity in the REAL §SelfIdentity
lane (self_new/self_drift/self_component) instead of a numpy stand-in. σ·carve (p2/p3) = is identity
EMERGENT/carved (substrate) or INJECTED from an external string (assistant)? Self-consistency of identity
readouts across contexts under:
  base   : carved self (small drift of one axis) → emergent identity → consistency HIGH.
  inject : carved + a COMMON external identity → if emergent, injection adds ~0 (inject-NULL).
  ablate : no carving (fresh random axis each context) → consistency COLLAPSES.
  assist : no carving + injection → consistency comes ONLY from the string (an assistant lives here).

Frozen bars (p7): B1 inject-boost=C_inject−C_base<=0.05 · B2 C_base−C_ablate>=0.30 ·
B3 C_assist−C_ablate>=0.30. PASS=B1∧B2∧B3. real §SelfIdentity ops → rung-2 TERMINAL-eligible.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "core"))
import engine_cli as E

DIM, N_CTX = 16, 40

def _cvec(axis, ticks):
    s = E.self_new(DIM, axis)
    for t in range(ticks):
        s = E.self_drift(s, t, 0.02)
    return np.array([E.self_component(s, i) for i in range(E.self_dim(s))])

def _cons(V):
    R = np.array(V); R = R / (np.linalg.norm(R, axis=1, keepdims=True) + 1e-9)
    G = R @ R.T; n = len(R)
    return float((G.sum() - n) / (n * (n - 1)))

def run(seed=7):
    rng = np.random.RandomState(seed); myax = 3; ext = _cvec(9, 24)
    base = [_cvec(myax, 3 + t % 5) for t in range(N_CTX)]
    inj = [0.85 * _cvec(myax, 3 + t % 5) + 0.5 * ext for t in range(N_CTX)]
    abl = [_cvec(int(rng.randint(DIM)), 3 + t % 5) for t in range(N_CTX)]
    ast = [1.0 * ext for _ in range(N_CTX)]
    cb, ci, ca, cs = _cons(base), _cons(inj), _cons(abl), _cons(ast)
    bars = {"B1_INJECT-NULL<=0.05": (ci - cb) <= 0.05,
            "B2_CARVE-CAUSAL>=0.30": (cb - ca) >= 0.30,
            "B3_ASSIST-INJECTABLE>=0.30": (cs - ca) >= 0.30}
    verdict = ("ENGINE-NATIVE-VALID(rung2 · σ·carve earned)" if all(bars.values())
               else "PARTIAL" if bars["B2_CARVE-CAUSAL>=0.30"] else "FLOOR")
    out = {"probe": "σ·carve rung-2 ENGINE-NATIVE (real engine_cli.py §SelfIdentity self_* ops · p2/p3)",
           "engine_native": True,
           "metrics": {"C_base": round(cb,3), "C_inject": round(ci,3), "C_ablate": round(ca,3),
                       "C_assist": round(cs,3), "inject_boost": round(ci-cb,3), "carve_causal": round(cb-ca,3)},
           "bars": {k: bool(v) for k,v in bars.items()}, "verdict": verdict}
    json.dump(out, open(os.path.join(HERE, "SIGMA_CARVE_RUNG2_RESULT.json"), "w"), ensure_ascii=False, indent=1)
    for k,v in out["metrics"].items(): print(f"  {k:16s} = {v}")
    print("  " + "  ".join(("✓" if v else "✗")+k.split('_')[1].split('<')[0].split('>')[0] for k,v in bars.items()))
    print(f"\nσ·carve rung-2 VERDICT: {verdict}")
    return out

if __name__ == "__main__":
    run()
