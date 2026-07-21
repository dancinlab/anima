#!/usr/bin/env python3
"""H_005 G3-a verdict collector — reads g3a_result_full.json, applies the frozen G3-a falsifiers,
emits SUPPORTED / PARTIAL / FALSIFIED (deterministic, $0). Free-slot d_acc throughout.

  precond : drill d_acc(A-χ̂) ≥ 0.95 BOTH seeds, else WIRING FAILURE (the arm did not fit its drill).
  F2 live : f1′(A-χ̂) ≥ 0.85 BOTH, else DEAD.
  F3      : f2″(C-scaf) > 0.60 ⇒ grid leaks ⇒ no verdict.
  harness : f2″(C-perm) ∉ [0.45,0.55] ⇒ harness broken.
  F4      : A-χ̂ F4_offtop < 0.20 BOTH ⇒ R reads ≤ rank-1 shadow ⇒ DEAD.
  F5      : A-χ̂ dCE < 0.01 AND d_dacc < 0.05 BOTH ⇒ VALUES don't matter (strip resolution = same) ⇒ DEAD.
  F1a     : Δ = f2″(A-χ̂) − f2″(C-χ̂plc). SUPPORTED iff Δ ≥ 0.15 BOTH; DEAD iff < 0.05 both. (C-χ̂plc = placebo)
  F1a′    : f2″(A-χ̂) ≥ f2″(A-hand) − 0.05 BOTH (non-inferiority; learned values ≈ hand values).

SUPPORTED here is SCOPED (honest-limit): G3-0d probe φ→hon = 1.0 ⇒ the claim is 'concord recoverable
from trunk representations on the drill register', NOT a strong natural-text or learned-SUPPORT claim.
"""
from __future__ import annotations

import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_R = os.path.join(_HERE, "g3a_result_full.json")


def _g(res, arm, s, key="f2doubleprime"):
    return res.get(f"{arm}.s{s}", {}).get(key)


def main() -> int:
    if not os.path.exists(_R):
        print(f"NO RESULT YET — {_R} does not exist. Run train_g3a.py (the d=384 run) first.")
        return 2
    data = json.load(open(_R, encoding="utf-8"))
    res = data["results"]
    seeds = sorted({int(k.split(".s")[1]) for k in res})

    per = {}
    for s in seeds:
        chi = _g(res, "A-χ̂", s); plc = _g(res, "C-χ̂plc", s); hand = _g(res, "A-hand", s)
        scaf = _g(res, "C-scaf", s); perm = _g(res, "C-perm", s)
        live = _g(res, "A-χ̂", s, "f1prime"); drill = _g(res, "A-χ̂", s, "drill_dacc")
        f4 = _g(res, "A-χ̂", s, "F4_offtop"); f5 = _g(res, "A-χ̂", s, "F5_union") or {}
        f1a = None if (chi is None or plc is None) else round(chi - plc, 4)
        f1ap = None if (chi is None or hand is None) else round(chi - hand, 4)
        per[s] = {"f1a_delta": f1a, "f1aprime_margin": f1ap, "A_chi": chi, "C_chiplc": plc,
                  "A_hand": hand, "C_scaf": scaf, "C_perm": perm, "liveness": live, "drill_dacc": drill,
                  "F4_offtop": f4, "F5_dCE": f5.get("dCE"), "F5_d_dacc": f5.get("d_dacc")}

    def _all(p):
        return all(p(per[s]) for s in seeds)

    precond_ok = _all(lambda r: r["drill_dacc"] is not None and r["drill_dacc"] >= 0.95)
    live_ok = _all(lambda r: r["liveness"] is not None and r["liveness"] >= 0.85)
    f3_leak = any(per[s]["C_scaf"] is not None and per[s]["C_scaf"] > 0.60 for s in seeds)
    harness_bad = any(per[s]["C_perm"] is not None and not (0.45 <= per[s]["C_perm"] <= 0.55) for s in seeds)
    f4_dead = _all(lambda r: r["F4_offtop"] is not None and r["F4_offtop"] < 0.20)
    f5_dead = _all(lambda r: r["F5_dCE"] is not None and r["F5_d_dacc"] is not None
                   and r["F5_dCE"] < 0.01 and r["F5_d_dacc"] < 0.05)
    f1a_deltas = [per[s]["f1a_delta"] for s in seeds if per[s]["f1a_delta"] is not None]
    f1ap_ok = _all(lambda r: r["f1aprime_margin"] is not None and r["f1aprime_margin"] >= -0.05)

    if not precond_ok:
        verdict = "WIRING FAILURE — drill d_acc(A-χ̂) < 0.95; the arm did not fit its own drill (not a verdict)"
    elif not live_ok:
        verdict = "DEAD (F2 liveness) — f1′(A-χ̂) < 0.85; measurement invalid"
    elif f3_leak:
        verdict = "NO VERDICT (F3) — f2″(C-scaf) > 0.60; the grid leaks, field cannot be isolated"
    elif harness_bad:
        verdict = "HARNESS BROKEN — f2″(C-perm) outside [0.45,0.55]"
    elif f4_dead:
        verdict = "DEAD (F4 eff-rank) — R reads ≤ a rank-1 shadow of T̂ (offtop < 0.20)"
    elif f5_dead:
        verdict = "DEAD (F5 union) — stripping the learned resolution leaves d_acc unchanged; the VALUES are epiphenomenal"
    elif f1a_deltas and all(x >= 0.15 for x in f1a_deltas) and f1ap_ok:
        verdict = ("SUPPORTED (SCOPED) — Δd_acc(A-χ̂−C-χ̂plc) ≥ 0.15 both seeds, F1a′ non-inferior, "
                   "F2/F3/F4/F5/harness clean. A LEARNED concord χ̂=g(φ) on the fixed support reproduces the "
                   "hand field's causal power. SCOPE (G3-0d probe φ→hon=1.0): the concord is recoverable from "
                   "TRUNK REPRESENTATIONS ON THE DRILL REGISTER — NOT a natural-text claim, NOT learned SUPPORT.")
    elif f1a_deltas and all(x >= 0.15 for x in f1a_deltas) and not f1ap_ok:
        verdict = "PARTIAL — F1a ≥ 0.15 both but F1a′ fails (A-χ̂ materially below A-hand): the cost of removing the hand"
    elif f1a_deltas and all(x < 0.05 for x in f1a_deltas):
        verdict = "FALSIFIED — Δd_acc(A-χ̂−C-χ̂plc) < 0.05 both seeds; learned values work equally on WRONG support = capacity, not binding"
    else:
        verdict = "PARTIAL — Δd_acc(A-χ̂−C-χ̂plc) between 0.05 and 0.15 (or seed-inconsistent)"

    print("=" * 78 + "\nH_005 G3-a verdict — frozen falsifiers on the measured learned-χ̂ run\n" + "=" * 78)
    print(f"seeds: {seeds}  ·  config: {data.get('config')}")
    for s in seeds:
        r = per[s]
        print(f"\n[seed {s}]")
        print(f"  A-χ̂ f2″={r['A_chi']}  C-χ̂plc f2″={r['C_chiplc']}  →  F1a Δ={r['f1a_delta']}  "
              f"(A-hand f2″={r['A_hand']} · F1a′ margin={r['f1aprime_margin']})")
        print(f"  liveness f1′={r['liveness']} (≥0.85) · drill={r['drill_dacc']} (≥0.95) · "
              f"C-scaf={r['C_scaf']} (<0.60) · C-perm={r['C_perm']} ([.45,.55])")
        print(f"  F4 offtop={r['F4_offtop']} (≥0.20) · F5 dCE={r['F5_dCE']} d_dacc={r['F5_d_dacc']}")
    print(f"\nprecond_ok={precond_ok} live_ok={live_ok} F3_leak={f3_leak} harness_bad={harness_bad} "
          f"F4_dead={f4_dead} F5_dead={f5_dead} F1a′_ok={f1ap_ok} · F1a deltas={f1a_deltas}")
    print("\nVERDICT:", verdict)

    out = {"verdict": verdict, "per_seed": per, "precond_ok": precond_ok, "live_ok": live_ok,
           "F3_leak": f3_leak, "harness_bad": harness_bad, "F4_dead": f4_dead, "F5_dead": f5_dead,
           "F1aprime_ok": f1ap_ok, "f1a_deltas": f1a_deltas}
    json.dump(out, open(os.path.join(_HERE, "verdict_g3a.json"), "w"), indent=2, ensure_ascii=False)
    print("\nwrote verdict_g3a.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
