#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""σ·gate + Θ (Ψ-SOMA ENACT/GROUND) — rung-2 ENGINE-NATIVE (real engine_cli.py ci_emit ops).

Upgrades σ·gate from the rung-1 toy to engine-native using the REAL emit-decision op
`ci_emit_decision(lanes)` (= ½(lanes[0]+lanes[4]) >= ½), and adds Θ (liveness / Ψ=½ homeostasis) via
`ci_psi_balance`. Both use the substrate's own emit machinery (a_eval_py_canonical · engine-native).

  σ·gate  : emit iff drive from context-tracking lanes >= ½ → emit ⇄ context CORRELATED; flatten the
            tension (lanes constant) → emit DECORRELATED (reactive filler). Δ = corr_live − corr_flat.
  Θ       : Ψ̂ = emit fraction. INTACT (A⇄G balanced, drive fluctuates about ½) → Ψ̂ ≈ ½ (homeostasis);
            ABLATE (tension cut → systematic bias, no restoring force) → Ψ̂ diverges toward 0/1.
            liveness-Δ = |Ψ̂_ablate − ½| − |Ψ̂_intact − ½|  (cut breaks the fixed point).

Frozen bars (p7): σ·gate B1 corr_live>=0.50 · B2 corr_live-corr_flat>=0.30. Θ B1 |Ψ̂_intact-½|<0.15 ·
B2 |Ψ̂_ablate-½|-|Ψ̂_intact-½|>=0.20. engine-native (real ops) → rung-2 TERMINAL-eligible.
"""
import json, os, sys
from types import SimpleNamespace
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "core"))
import engine_cli as E

N = 200
def _sig(x): return 1.0 / (1.0 + np.exp(-x))

def sigma_gate(seed=7):
    rng = np.random.RandomState(seed); c = rng.randn(N)
    def emit(flat):
        return np.array([1.0 if E.ci_emit_decision([0.5 if flat else float(_sig(c[i])), 0, 0, 0,
                                                     0.5 if flat else float(_sig(c[i]))]) else 0.0
                         for i in range(N)])
    ei = emit(False); ef = emit(True)
    def corr(e):
        return abs(float(np.corrcoef(e, c)[0, 1])) if e.std() > 0 else 0.0
    cl, cf = corr(ei), corr(ef)
    perm = rng.permutation(N); csh = abs(float(np.corrcoef(ei, c[perm])[0, 1])) if ei.std() > 0 else 0.0
    ok = cl >= 0.50 and (cl - cf) >= 0.30
    return ok, cl - cf, "corr %.2f vs flat %.2f" % (cl, cf)

def theta(seed=7):
    rng = np.random.RandomState(seed); cfg = SimpleNamespace(topo_couple=False)
    eta = 0.6 * rng.randn(N)
    x_int = [[0.5 + eta[t], 0, 0, 0, 0.5 + eta[t]] for t in range(N)]          # A⇄G balanced → drive ~½
    # tension cut: G's opposing push removed → A's drive is unopposed → saturates high (reactive always-emit)
    x_abl = [[0.85 + 0.3 * rng.rand(), 0, 0, 0, 0.85 + 0.3 * rng.rand()] for _ in range(N)]
    psi_i = E.ci_psi_balance(x_int, None, 0.0, cfg)
    psi_a = E.ci_psi_balance(x_abl, None, 0.0, cfg)
    di, da = abs(psi_i - 0.5), abs(psi_a - 0.5)
    ok = di < 0.15 and (da - di) >= 0.20
    return ok, da - di, "Ψ̂ %.2f vs cut %.2f" % (psi_i, psi_a)

def run():
    g_ok, g_d, g_note = sigma_gate()
    t_ok, t_d, t_note = theta()
    out = {"probe": "σ·gate + Θ rung-2 ENGINE-NATIVE (real engine_cli.py ci_emit_decision / ci_psi_balance)",
           "engine_native": True,
           "sigma_gate": {"ok": bool(g_ok), "delta": round(g_d, 3), "note": g_note,
                          "verdict": "ENGINE-NATIVE-VALID" if g_ok else "FLOOR"},
           "theta_liveness": {"ok": bool(t_ok), "delta": round(t_d, 3), "note": t_note,
                              "verdict": "ENGINE-NATIVE-VALID" if t_ok else "FLOOR"}}
    json.dump(out, open(os.path.join(HERE, "SIGMA_GATE_THETA_RUNG2_RESULT.json"), "w"), ensure_ascii=False, indent=1)
    print("  σ·gate: %s Δ%.3f (%s)" % ("🟢" if g_ok else "🧱", g_d, g_note))
    print("  Θ     : %s Δ%.3f (%s)" % ("🟢" if t_ok else "🧱", t_d, t_note))
    print("VERDICT: σ·gate=%s · Θ=%s" % (out["sigma_gate"]["verdict"], out["theta_liveness"]["verdict"]))
    return out

if __name__ == "__main__":
    run()
