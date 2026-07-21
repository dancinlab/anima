#!/usr/bin/env python3
"""H_003 verdict collector — reads train_result_full.json, applies the frozen
falsifiers F1/F2/F6, emits SUPPORTED / PARTIAL / FALSIFIED (deterministic, $0).

Run this AFTER the training driver writes train_result_full.json. It does not
train anything; it applies the pre-registered thresholds to the measured d_acc.

Pre-registered rules (frozen 2026-07-16, H_003 card):
  F2 liveness : f1'(A-atom) >= 0.85 on BOTH seeds, else measurement DEAD (no verdict).
  F1 primary  : Δ = d_acc(A-atom,f2') − d_acc(A-shat,f2').
                SUPPORTED iff Δ >= 0.15 at BOTH seeds; DEAD iff Δ < 0.05 at both; else PARTIAL.
  F6 placebo  : if d_acc(A-atom,f2') − d_acc(C-plc,f2') > 0.05 at either seed, the F1
                pass is VOID (generic-disruption, not atomicity).
  F3 leak     : f2'(C-scaf) > 0.60 ⇒ grid leaks (reported).
  F4 harness  : f2'(C-perm) ∉ [0.40, 0.60] ⇒ harness/label leak (reported).

Run:  python3 state/h003_atomicity_fixed_codec_drill_2026-07-16/collect_verdict.py
"""

from __future__ import annotations

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_RESULT = os.path.join(_HERE, "train_result_full.json")

F2_LIVENESS_FLOOR = 0.85
F1_SUPPORTED = 0.15
F1_DEAD = 0.05
F6_PLACEBO_MAX = 0.05
F3_SCAF_MAX = 0.60
F4_PERM_BAND = (0.40, 0.60)


def _g(results, arm, seed, panel):
    return results.get(f"{arm}.s{seed}", {}).get(panel)


def main() -> int:
    if not os.path.exists(_RESULT):
        print(f"NO RESULT YET — {_RESULT} does not exist. Run train_h003.py first "
              "(the ~6-8h full run). This collector applies the frozen falsifiers once it lands.")
        return 2
    data = json.load(open(_RESULT, encoding="utf-8"))
    results = data["results"]
    seeds = sorted({int(k.split(".s")[1]) for k in results})

    per_seed = {}
    for s in seeds:
        a_at = _g(results, "A-atom", s, "f2prime")
        a_sh = _g(results, "A-shat", s, "f2prime")
        a_plc = _g(results, "C-plc", s, "f2prime")
        a_scaf = _g(results, "C-scaf", s, "f2prime")
        a_perm = _g(results, "C-perm", s, "f2prime")
        live = _g(results, "A-atom", s, "f1prime")
        d = None if (a_at is None or a_sh is None) else round(a_at - a_sh, 4)
        plc_gap = None if (a_at is None or a_plc is None) else round(a_at - a_plc, 4)
        per_seed[s] = {
            "f1_delta": d, "liveness_f1prime": live, "placebo_gap": plc_gap,
            "C_scaf_f2": a_scaf, "C_perm_f2": a_perm,
            "A_atom_f2": a_at, "A_shat_f2": a_sh, "C_plc_f2": a_plc,
        }

    # F2 liveness — both seeds must clear 0.85 or the measurement is DEAD
    live_ok = all(per_seed[s]["liveness_f1prime"] is not None
                  and per_seed[s]["liveness_f1prime"] >= F2_LIVENESS_FLOOR for s in seeds)
    # F6 placebo — any seed with gap > 0.05 voids
    placebo_void = any(per_seed[s]["placebo_gap"] is not None
                       and per_seed[s]["placebo_gap"] > F6_PLACEBO_MAX for s in seeds)
    deltas = [per_seed[s]["f1_delta"] for s in seeds if per_seed[s]["f1_delta"] is not None]

    if not live_ok:
        verdict = "DEAD (F2 liveness) — f1'(A-atom) < 0.85; measurement invalid, escalate to GPU d=1024"
    elif placebo_void:
        verdict = "VOID (F6 placebo) — A-atom−C-plc > 0.05; effect is generic disruption, not atomicity"
    elif deltas and all(x >= F1_SUPPORTED for x in deltas):
        verdict = "SUPPORTED — Δd_acc ≥ 0.15 at both seeds AND placebo clean AND liveness alive"
    elif deltas and all(x < F1_DEAD for x in deltas):
        verdict = "FALSIFIED — Δd_acc < 0.05 at both seeds; atomicity does NOT cause held-out recombination"
    else:
        verdict = "PARTIAL — Δd_acc between 0.05 and 0.15 (or seed-inconsistent); weak/uncertain effect"

    print("=" * 74)
    print("H_003 verdict — frozen falsifiers on the measured run")
    print("=" * 74)
    print(f"seeds: {seeds}  ·  config: {data.get('config')}")
    for s in seeds:
        r = per_seed[s]
        print(f"\n[seed {s}]")
        print(f"  A-atom f2'={r['A_atom_f2']}  A-shat f2'={r['A_shat_f2']}  →  F1 Δ={r['f1_delta']}")
        print(f"  liveness f1'(A-atom)={r['liveness_f1prime']} (F2 floor {F2_LIVENESS_FLOOR})")
        print(f"  C-plc f2'={r['C_plc_f2']}  →  F6 placebo gap={r['placebo_gap']} (max {F6_PLACEBO_MAX})")
        print(f"  C-scaf f2'={r['C_scaf_f2']} (F3 leak > {F3_SCAF_MAX})  ·  "
              f"C-perm f2'={r['C_perm_f2']} (F4 band {F4_PERM_BAND})")
    print()
    print("F2 liveness OK :", live_ok)
    print("F6 placebo void:", placebo_void)
    print("F1 deltas      :", deltas)
    print()
    print("VERDICT:", verdict)

    out = {"verdict": verdict, "per_seed": per_seed, "live_ok": live_ok,
           "placebo_void": placebo_void, "f1_deltas": deltas}
    with open(os.path.join(_HERE, "verdict.json"), "w") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print("\nwrote verdict.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
