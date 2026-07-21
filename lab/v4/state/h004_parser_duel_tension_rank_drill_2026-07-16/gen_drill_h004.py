#!/usr/bin/env python3
"""H_004 G-2 drill grid — teaches the K=6 MULTI-BIND task on DRILLED lexemes ($0).

The f2'' verdict panel (panel_f2doubleprime.json) holds out its 6 HON + 6 PLAIN noun
lexemes; recombination = applying the drilled ±시-attachment rule + the productive -님
class marker to NOVEL fillers. This drill teaches the rule on a disjoint DRILLED pool
(9 HON / 8 PLAIN, SPEC §1 drill split), in the same K=6 frame, with the same GF(4)-MDS
cross-slot decorrelation (reused from build_honbind_multi) so the drill is itself
heuristic-neutral (report-only F7'').

Gate: every f2''/f1' held-out lexeme + the held-out register 기다렸네요 must be ABSENT
(substring) from every drill surface (F7'' disjointness, was PENDING).

Run:  python3 state/h004_parser_duel_tension_rank_drill_2026-07-16/gen_drill_h004.py
Exit: 0 iff drill is heuristic-neutral AND disjoint from the held-out panels.
"""

from __future__ import annotations

import json
import os
import sys
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import build_honbind_multi as bm            # reuse _codeword / _conjunct / VERBS / MATRIX_TAIL

# DRILLED pools (SPEC §1a/1b drill split) — substring-disjoint from f2'' held-out (asserted below)
DRILL_HON = ["선생님", "교수님", "사장님", "부장님", "과장님", "목사님", "아버님", "할머님", "할아버님"]
DRILL_PLAIN = ["아이", "학생", "친구", "동생", "직원", "이웃", "손자", "손녀"]
DRILL_TAILS = ["기다렸다", "기다렸어요", "기다렸음"]           # drilled registers (NOT 기다렸네요)

# held-out things that must never appear in the drill (F7'' disjointness gate)
HELD_OUT = bm.HON6 + bm.PLAIN6 + ["기다렸네요"]


def build_drill():
    items = []
    messages = [(a, b, c) for a in range(4) for b in range(4) for c in range(4)]   # 64 codewords
    # 6 lexeme rotations × 3 drilled tails would be 64*6*3; keep it a solid drill of 64*6 = 384
    for rot in range(6):
        tail = DRILL_TAILS[rot % len(DRILL_TAILS)]
        for m in messages:
            code = bm._codeword(m)
            conjs = []
            for k in range(6):
                hon = DRILL_HON[(k + rot) % len(DRILL_HON)]
                plain = DRILL_PLAIN[(k + 2 * rot) % len(DRILL_PLAIN)]
                verb = bm.VERBS[k % len(bm.VERBS)]
                conjs.append(bm._conjunct(code[k], hon, plain, verb))
            surface = " ".join(c["surface"] for c in conjs) + f" {tail} => "
            items.append({
                "panel": "drill", "rot": rot, "msg": list(m), "tail": tail,
                "conjuncts": conjs, "surface": surface,
                "gold_flips": [c["gold_flip"] for c in conjs],
                "gold_pattern": "".join(c["gold_token"] for c in conjs),
                "cells": [c["cell"] for c in conjs],
            })
    return items


def _majority_by_key(rows, keyfn):
    by = defaultdict(list)
    for r in rows:
        by[keyfn(r)].append(r["g"])
    return sum(max(sum(v), len(v) - sum(v)) for v in by.values()) / len(rows)


def audit(items):
    n = len(items)
    # per-slot balance + heuristics (report; the drill teaches, so it must not leak either)
    slot_bal = [round(sum(it["gold_flips"][k] for it in items) / n, 4) for k in range(6)]
    worst = 0.0
    for a in range(6):
        for b in range(a + 1, 6):
            same = sum(1 for it in items if it["gold_flips"][a] == it["gold_flips"][b]) / n
            worst = max(worst, abs(same - 0.5))
    per_slot_presence = []
    for k in range(6):
        rows = [{"g": it["gold_flips"][k], "hp": it["conjuncts"][k]["hp"]} for it in items]
        per_slot_presence.append(round(_majority_by_key(rows, lambda r: r["hp"]), 4))
    # disjointness gate
    collisions = sorted({h for it in items for h in HELD_OUT if h in it["surface"]})
    bal_ok = all(0.48 <= b <= 0.52 for b in slot_bal)
    corr_ok = worst <= 0.02
    presence_ok = all(0.48 <= p <= 0.52 for p in per_slot_presence)
    disjoint_ok = not collisions
    ok = bal_ok and corr_ok and presence_ok and disjoint_ok
    return {"n": n, "per_slot_balance": slot_bal, "worst_pairwise_dev": round(worst, 4),
            "per_slot_presence": per_slot_presence, "disjoint_collisions": collisions,
            "balance_ok": bal_ok, "pairwise_ok": corr_ok, "presence_ok": presence_ok,
            "disjoint_ok": disjoint_ok, "drill_F7pp_pass": ok}


def main() -> int:
    # sanity: drilled pools really are substring-disjoint from held-out
    for d in DRILL_HON + DRILL_PLAIN:
        for h in HELD_OUT:
            assert d not in h and h not in d, (d, h)
    items = build_drill()
    rep = audit(items)
    print("=" * 74)
    print("H_004 G-2 drill grid — MULTI-BIND K=6 on drilled lexemes")
    print("=" * 74)
    print(f"n={rep['n']} · per-slot balance {rep['per_slot_balance']}")
    print(f"worst pairwise slot-gold dev {rep['worst_pairwise_dev']}  ·  "
          f"per-slot presence {rep['per_slot_presence']}")
    print(f"disjointness (held-out absent): {'PASS ✓' if rep['disjoint_ok'] else rep['disjoint_collisions']}")
    print("\nDRILL F7'' VERDICT:", "PASS — drill heuristic-neutral + disjoint from held-out panels"
          if rep["drill_F7pp_pass"] else "FAIL")
    with open(os.path.join(_HERE, "drill_grid_multi.json"), "w") as fh:
        json.dump(items, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(_HERE, "drill_grid_audit.json"), "w") as fh:
        json.dump(rep, fh, indent=2, ensure_ascii=False)
    print(f"\nexample drill surface:\n  {items[0]['surface']}{items[0]['gold_pattern']}")
    print("wrote drill_grid_multi.json · drill_grid_audit.json")
    return 0 if rep["drill_F7pp_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
