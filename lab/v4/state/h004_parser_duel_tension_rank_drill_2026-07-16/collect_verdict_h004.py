#!/usr/bin/env python3
"""H_004 G-2 verdict collector — reads train_result_full.json, applies the frozen falsifiers
F1/F2/F3/F4/F5/F6 + harness, emits SUPPORTED / PARTIAL / FALSIFIED (deterministic, $0).

Run AFTER train_h004.py writes train_result_full.json. Applies the pre-registered thresholds
(DESIGN_g2_training_fable5.md §4) to the measured d_acc; does not train.

  F2 liveness : f1′(A-duel) ≥ 0.85 BOTH seeds, else DEAD (no verdict; FM-3b frame-transfer caveat).
  precond     : d_acc(A-duel, drill) ≥ 0.95 BOTH seeds, else the run is a wiring failure.
  F3 not-free : f2″(C-scaf) > 0.60 ⇒ grid leaks (surface solves it) ⇒ no verdict.
  harness     : f2″(C-perm) ∉ [0.45,0.55] ⇒ harness broken.
  F6 placebo  : f2″(A-duel) − f2″(C-plc) ≤ 0.05 ⇒ void (no SUPPORTED).
  F4 eff-rank : A-duel F4_offtop < 0.20 ⇒ R reads ≤ a rank-1 shadow ⇒ DEAD.
  F5 union    : A-duel F5_union dCE < 0.01 AND d_dacc < 0.05 ⇒ decoder didn't need resolution ⇒ DEAD.
  F1 primary  : Δ = f2″(A-duel) − f2″(A-rank1). SUPPORTED iff Δ ≥ 0.15 BOTH seeds; DEAD iff <0.05 both.
"""

from __future__ import annotations

import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_R = os.path.join(_HERE, "train_result_full.json")


def _g(res, arm, s, key="f2doubleprime"):
    return res.get(f"{arm}.s{s}", {}).get(key)


def main() -> int:
    if not os.path.exists(_R):
        print(f"NO RESULT YET — {_R} does not exist. Run train_h004.py (the ~5h d=384 run) first.")
        return 2
    data = json.load(open(_R, encoding="utf-8"))
    res = data["results"]
    seeds = sorted({int(k.split(".s")[1]) for k in res})

    per = {}
    for s in seeds:
        duel = _g(res, "A-duel", s); rank1 = _g(res, "A-rank1", s)
        plc = _g(res, "C-plc", s); scaf = _g(res, "C-scaf", s); perm = _g(res, "C-perm", s)
        live = _g(res, "A-duel", s, "f1prime")
        drill = _g(res, "A-duel", s, "drill_dacc")
        f4 = _g(res, "A-duel", s, "F4_offtop")
        f5 = _g(res, "A-duel", s, "F5_union") or {}
        d = None if (duel is None or rank1 is None) else round(duel - rank1, 4)
        per[s] = {"f1_delta": d, "A_duel": duel, "A_rank1": rank1, "C_plc": plc,
                  "C_scaf": scaf, "C_perm": perm, "liveness_f1prime": live, "drill_dacc": drill,
                  "F4_offtop": f4, "F5_dCE": f5.get("dCE"), "F5_d_dacc": f5.get("d_dacc"),
                  "placebo_gap": None if (duel is None or plc is None) else round(duel - plc, 4)}

    def _all(pred):
        return all(pred(per[s]) for s in seeds)

    live_ok = _all(lambda r: r["liveness_f1prime"] is not None and r["liveness_f1prime"] >= 0.85)
    precond_ok = _all(lambda r: r["drill_dacc"] is not None and r["drill_dacc"] >= 0.95)
    f3_leak = any(per[s]["C_scaf"] is not None and per[s]["C_scaf"] > 0.60 for s in seeds)
    harness_bad = any(per[s]["C_perm"] is not None and not (0.45 <= per[s]["C_perm"] <= 0.55)
                      for s in seeds)
    f6_void = any(per[s]["placebo_gap"] is not None and per[s]["placebo_gap"] <= 0.05 for s in seeds)
    f4_dead = _all(lambda r: r["F4_offtop"] is not None and r["F4_offtop"] < 0.20)
    f5_dead = _all(lambda r: r["F5_dCE"] is not None and r["F5_d_dacc"] is not None
                   and r["F5_dCE"] < 0.01 and r["F5_d_dacc"] < 0.05)
    deltas = [per[s]["f1_delta"] for s in seeds if per[s]["f1_delta"] is not None]

    if not precond_ok:
        verdict = "WIRING FAILURE — d_acc(A-duel, drill) < 0.95; the run did not fit its own drill (not a verdict)"
    elif not live_ok:
        verdict = "DEAD (F2 liveness) — f1′(A-duel) < 0.85; measurement invalid (check FM-3b frame transfer)"
    elif f3_leak:
        verdict = "NO VERDICT (F3) — f2″(C-scaf) > 0.60; the surface alone solves it, field cannot be isolated"
    elif harness_bad:
        verdict = "HARNESS BROKEN — f2″(C-perm) outside [0.45,0.55]"
    elif f4_dead:
        verdict = "DEAD (F4 eff-rank) — trained R reads ≤ a rank-1 shadow of T (offtop < 0.20)"
    elif f5_dead:
        verdict = "DEAD (F5 union) — decoder scores the same on the resolution-stripped skeleton"
    elif f6_void:
        verdict = "VOID (F6 placebo) — A-duel − C-plc ≤ 0.05; the effect is any-tensor capacity, not edge-aligned content"
    elif deltas and all(x >= 0.15 for x in deltas):
        verdict = ("SUPPORTED — Δd_acc(A-duel−A-rank1) ≥ 0.15 both seeds, F2/F3/F4/F5/F6/harness clean. "
                   "The parse-tension FIELD FORMAT (edge-aligned) causes held-out binding beyond its rank-1 "
                   "summary. SCOPE: licenses building the learned-duel stage; does NOT claim a trained parser "
                   "pair produces this field (χ hand-computed).")
    elif deltas and all(x < 0.05 for x in deltas):
        verdict = "FALSIFIED — Δd_acc < 0.05 both seeds; the field format buys nothing over its rank-1 summary"
    else:
        verdict = "PARTIAL — Δd_acc between 0.05 and 0.15 (or seed-inconsistent)"

    print("=" * 76)
    print("H_004 G-2 verdict — frozen falsifiers on the measured run")
    print("=" * 76)
    print(f"seeds: {seeds}  ·  config: {data.get('config')}")
    for s in seeds:
        r = per[s]
        print(f"\n[seed {s}]")
        print(f"  A-duel f2″={r['A_duel']}  A-rank1 f2″={r['A_rank1']}  →  F1 Δ={r['f1_delta']}")
        print(f"  liveness f1′(A-duel)={r['liveness_f1prime']} (≥0.85) · drill d_acc={r['drill_dacc']} (≥0.95 precond)")
        print(f"  C-scaf f2″={r['C_scaf']} (F3 >0.60 leak) · C-perm f2″={r['C_perm']} (harness [0.45,0.55])")
        print(f"  C-plc f2″={r['C_plc']} → F6 gap={r['placebo_gap']} (>0.05) · F4 offtop={r['F4_offtop']} (≥0.20) · "
              f"F5 dCE={r['F5_dCE']} d_dacc={r['F5_d_dacc']}")
    print(f"\nprecond_ok={precond_ok} live_ok={live_ok} F3_leak={f3_leak} harness_bad={harness_bad} "
          f"F4_dead={f4_dead} F5_dead={f5_dead} F6_void={f6_void} · F1 deltas={deltas}")
    print("\nVERDICT:", verdict)

    out = {"verdict": verdict, "per_seed": per, "precond_ok": precond_ok, "live_ok": live_ok,
           "F3_leak": f3_leak, "harness_bad": harness_bad, "F4_dead": f4_dead, "F5_dead": f5_dead,
           "F6_void": f6_void, "f1_deltas": deltas}
    with open(os.path.join(_HERE, "verdict.json"), "w") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print("\nwrote verdict.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
