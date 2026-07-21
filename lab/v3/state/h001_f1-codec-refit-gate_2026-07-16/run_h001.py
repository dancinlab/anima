"""H_001 — f1-codec-refit-gate. Run of the 5 pre-registered falsifiers G-1..G-5.

Verdict is about the RIG, not about F1: LICENSED (H_002 may run as pre-registered)
or REFUSED (H_002 blocked until the named defect is repaired).

Card: HYPOTHESES/cards/H_001_f1-codec-refit-gate.md (frozen 2026-07-16)
Run:  python3 state/h001_f1-codec-refit-gate_2026-07-16/run_h001.py

Deterministic, stdlib only, no network, $0.
"""

from __future__ import annotations

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tool"))

from anima_v3 import (
    Falsifier,
    binom_two_sided_p,
    chance_band,
    evaluate,
    two_proportion_n,
)

# ---------------------------------------------------------------------------
# Pre-registered inputs (frozen in the card 2026-07-16).
# ---------------------------------------------------------------------------
ALPHA = 0.01
POWER = 0.99
DELTA_MIN = 0.15          # half of MORPH-ATOM's measured +0.291
CONF = 0.99

# ---------------------------------------------------------------------------
# G-5 OUTPUT — the H_9288 protocol, recovered 2026-07-16 from the v1 repo
# (`anima`), which the campaign kept as the evidence trail. It was never lost;
# it was simply never restated in THIS repo. Source of record:
#   anima/HYPOTHESES/cards/H_9288_morpheme_atomicity_lever.md
#   anima/state/verdicts/9288_morpheme_atomicity/VERDICT.md
# ---------------------------------------------------------------------------
PROTOCOL = {
    "name": "H_9288 MORPH-ATOM stage-2 S1 held-out flip panel",
    "task": "synthetic XOR negation drill (NBIND grid), Korean negation stems",
    "metric": "F2 = held-out flip accuracy on the stem never seen in the drill",
    "format": "FORCED CHOICE (binary flip: affirmative vs negated)",
    "chance_p0": 0.5,
    "n_items": 120,
    "drilled_stems": ["안", "않", "못"],
    "held_out_stem": "아니",
    "sanity_metric": "F1 = drilled-stem accuracy (must be ~1.0 or the arm never learned the drill)",
    "arms": {
        "M": "MORPH-2B codec (BPE-on-jamo, atomicity without identity)",
        "C1": "raw utf-8 baseline, identical drill — the control",
        "C2": "held-out stem ablated from the codec",
        "C3": "shared-<NEG> token — the leak ceiling / liveness arm",
    },
    "v1_pass_rule": "F2(M)>=0.70 & delta(M-C1)>=0.15 & C3>=0.90 & C2<=0.55 & F1(M)>=0.75",
    "seeds": 1,
    "seed": 4302,
    "harness": "custom morphatom_eval.py (NOT canonical anima-py evaluate)",
}

# Measured scores, from the sealed v1 verdict (2026-07-13, pod 44611459).
# Counts are exact integers over n=120 — the published rates reproduce them
# exactly, which is how n was recovered.
SCORES = {
    "M_f2": 109 / 120,      # 0.9083 — codec arm, held-out flip
    "C1_f2": 74 / 120,      # 0.6167 — raw utf-8 control, held-out flip
    "C3_f2": 110 / 120,     # 0.9167 — leak-ceiling liveness arm
    "M_f2_k": 109,
    "C1_f2_k": 74,
    "C3_f2_k": 110,
}

# ---------------------------------------------------------------------------
# The rig anima-v3 would build. It does not exist yet — that is a measurement,
# not an excuse.
# ---------------------------------------------------------------------------
GENERATOR_EXISTS = os.path.isdir(os.path.join(_ROOT, "src", "generator"))


def main() -> int:
    m = {}

    print("=" * 78)
    print("H_001 — f1-codec-refit-gate · verdict = rig LICENSED or REFUSED")
    print("=" * 78)

    # --- G-5 protocol reconstruction -------------------------------------
    print("\n[G-5] protocol reconstruction")
    m["protocol_recovered"] = True
    m["protocol"] = PROTOCOL
    print(f"  RECOVERED from the v1 repo (`anima`) — the campaign's evidence trail.")
    print(f"    metric      : {PROTOCOL['metric']}")
    print(f"    format      : {PROTOCOL['format']}")
    print(f"    chance p0   : {PROTOCOL['chance_p0']}   <- NOT an F-score; a forced-choice rate")
    print(f"    n_items     : {PROTOCOL['n_items']}")
    print(f"    seeds       : {PROTOCOL['seeds']} (seed {PROTOCOL['seed']})")
    print(f"    harness     : {PROTOCOL['harness']}")

    # --- G-4 salvage bounds check ----------------------------------------
    print("\n[G-4] salvage bounds check — is MORPH-ATOM above the chance floor?")
    n = PROTOCOL["n_items"]
    p0 = PROTOCOL["chance_p0"]
    lo, hi = chance_band(n, p0, CONF)
    m["chance_band_99"] = [lo, hi]
    m["n_items"] = n
    m["chance_p0"] = p0

    c1_p = binom_two_sided_p(SCORES["C1_f2_k"], n, p0)
    m_p = binom_two_sided_p(SCORES["M_f2_k"], n, p0)
    c3_p = binom_two_sided_p(SCORES["C3_f2_k"], n, p0)
    m["C1_inside_band"] = lo <= SCORES["C1_f2"] <= hi
    m["M_inside_band"] = lo <= SCORES["M_f2"] <= hi
    m["C1_two_sided_p"] = c1_p
    m["M_two_sided_p"] = m_p
    m["C3_two_sided_p"] = c3_p
    m["delta_M_C1"] = SCORES["M_f2"] - SCORES["C1_f2"]

    print(f"  exact 99% chance band at n={n}, p0={p0}: [{lo:.4f}, {hi:.4f}]")
    print(f"    C1 control  = {SCORES['C1_f2_k']}/{n} = {SCORES['C1_f2']:.4f}  "
          f"inside_band={m['C1_inside_band']}  two-sided p={c1_p:.4f}")
    print(f"    M  codec    = {SCORES['M_f2_k']}/{n} = {SCORES['M_f2']:.4f}  "
          f"inside_band={m['M_inside_band']}  two-sided p={m_p:.3e}")
    print(f"    C3 liveness = {SCORES['C3_f2_k']}/{n} = {SCORES['C3_f2']:.4f}  "
          f"two-sided p={c3_p:.3e}")
    print(f"    delta(M-C1) = {m['delta_M_C1']:+.4f}")

    # --- G-2 closed-form power -------------------------------------------
    print("\n[G-2] closed-form power")
    p_ctrl = SCORES["C1_f2"]
    p_treat = p_ctrl + DELTA_MIN
    n_req = two_proportion_n(p_ctrl, p_treat, ALPHA, POWER)
    m["n_required"] = n_req
    m["power_operating_point"] = [p_ctrl, p_treat]
    m["v1_anchor_n"] = n
    m["v1_anchor_underpowered"] = n < n_req
    print(f"  two-proportion, alpha={ALPHA}, power={POWER}, delta_min={DELTA_MIN}")
    print(f"    operating point p1={p_ctrl:.4f} -> p2={p_treat:.4f}")
    print(f"    N required per arm = {n_req}")
    print(f"    the v1 anchor run used n={n} -> underpowered={m['v1_anchor_underpowered']} "
          f"(v1's own card admits this)")
    print(f"    anima-v3's generator can emit N>={n_req}? UNKNOWN — generator does not exist")

    # --- G-3 estimator fixtures ------------------------------------------
    print("\n[G-3] estimator fixtures (positive control on the instruments)")
    rc = os.system(f"python3 {os.path.join(_ROOT, 'tool', 'test_anima_v3.py')} > /dev/null 2>&1")
    m["fixtures_pass"] = (rc == 0)
    print(f"  tool/test_anima_v3.py exit={rc >> 8} -> fixtures_pass={m['fixtures_pass']}")

    # --- G-1 drift existence ---------------------------------------------
    print("\n[G-1] drift existence")
    m["generator_exists"] = GENERATOR_EXISTS
    m["boundary_shift_rate"] = None
    print(f"  generator_exists={GENERATOR_EXISTS} -> boundary-shift rate is NOT MEASURABLE.")
    print(f"  G-1 cannot be evaluated: the jamo-drill generator this card presupposes")
    print(f"  has not been built. An unevaluable gate cannot return PASS.")

    # --- ledger -----------------------------------------------------------
    falsifiers = [
        Falsifier("G-1 drift existence",
                  lambda x: not x["generator_exists"],
                  "generator absent -> the lever's existence is unmeasured"),
        Falsifier("G-2 closed-form power",
                  lambda x: not x["generator_exists"],
                  "cannot confirm the generator emits N>=n_required items"),
        Falsifier("G-3 estimator fixtures",
                  lambda x: not x["fixtures_pass"],
                  "an estimator is blind"),
        Falsifier("G-4 salvage bounds check",
                  lambda x: x["C1_inside_band"],
                  "control indistinguishable from chance at 99%"),
        Falsifier("G-5 protocol reconstruction",
                  lambda x: not x["protocol_recovered"],
                  "metric not restatable"),
    ]

    ledger = evaluate(m, falsifiers)
    licensed = ledger["all_pass"]
    m["rig"] = "LICENSED" if licensed else "REFUSED"

    print("\n" + "=" * 78)
    print("FALSIFIER LEDGER")
    print("=" * 78)
    for r in ledger["falsifiers"]:
        print(f"  {r['status']:4s}  {r['name']}")
    print(f"\n  {ledger['n_pass']}/{ledger['n_total']} PASS")
    print(f"\n  VERDICT: rig = {m['rig']}")

    out = os.path.join(_HERE, "result.json")
    with open(out, "w") as f:
        json.dump({"metrics": m, "falsifiers": ledger["falsifiers"],
                   "n_pass": ledger["n_pass"], "n_total": ledger["n_total"],
                   "rig": m["rig"]}, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"\n  artifacts: {os.path.relpath(out, _ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
