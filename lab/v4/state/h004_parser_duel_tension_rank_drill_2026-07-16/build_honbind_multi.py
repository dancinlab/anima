#!/usr/bin/env python3
"""H_004 G-0/redesign — MULTI-BIND K=6 panel builder + F7'' audit ($0, deterministic).

Implements DESIGN_g1_core_fable5.md §7. The single-bind HON-BIND frame has exactly ONE
parser-contested edge, so its tension field collapses to T = s*M (rank-1) — F4-DEAD
(g1_core_check.py, off-top 0.000). The fix is to STACK K=6 independent HON-BIND
conjuncts in one sentence, giving T = sum_k c_k*M_k of per-item rank 6:

    frame:  [V_k-adn(±시_k) N_k1의 N_k2도] ×6  기다렸다 =>
    answer: 6 position tokens (앞/뒤 per conjunct), d_acc = mean over the 6 forced choices
    gold_k: hp_k ⊕ 1[honored noun of conjunct k at N_k1]   (per-conjunct XOR)

Cross-slot decorrelation (F7'' requires pairwise slot-gold correlation 0) is achieved by
a strength-2 ORTHOGONAL ARRAY: the 6 conjunct cells per sentence are a codeword of the
[6,3] MDS (Reed-Solomon/Vandermonde) code over GF(4). MDS ⇒ any 2 of the 6 coordinates
are jointly uniform ⇒ every slot balanced AND every slot-pair independent, exactly. The
64 codewords (4^3 messages) are each instantiated 3× with rotated lexeme pairings → n=192.

Run:  python3 state/h004_parser_duel_tension_rank_drill_2026-07-16/build_honbind_multi.py
Exit: 0 iff F7'' PASS.
"""

from __future__ import annotations

import json
import os
import sys
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))


def _harness():
    sys.path.insert(0, os.path.join(_ROOT, "tool"))
    import anima_v4

    return anima_v4


# --- GF(4) arithmetic (poly x^2+x+1) -------------------------------------------
_GF_MUL = [
    [0, 0, 0, 0],
    [0, 1, 2, 3],
    [0, 2, 3, 1],
    [0, 3, 1, 2],
]


def _gadd(a, b):
    return a ^ b            # GF(4) addition = bitwise XOR on 2-bit reps


def _gmul(a, b):
    return _GF_MUL[a][b]


# [6,3] MDS generator G = [I3 | A], A = Vandermonde over points {1,2,3}:
#   A[i][j] = point_j ^ i   (i = 0..2 rows, j = 0..2 cols; point = {1,2,3})
# columns of A: col0=(1,1,1), col1=(1,2,3), col2=(1,3,2). Any 2 of the 6 columns
# of G are linearly independent (Vandermonde ⇒ MDS) ⇒ strength-2 OA.
_A_COLS = [(1, 1, 1), (1, 2, 3), (1, 3, 2)]


def _codeword(m):
    """m = (m0,m1,m2) in GF(4)^3 → 6-vector codeword over GF(4)."""
    parity = []
    for col in _A_COLS:
        acc = 0
        for mk, ak in zip(m, col):
            acc = _gadd(acc, _gmul(mk, ak))
        parity.append(acc)
    return list(m) + parity          # [I | A] : first 3 = message, last 3 = parity


# --- HON-BIND cell inventory (per conjunct) ------------------------------------
# GF(4) elem -> cell (hp, honored_position). Reuses build_hon_bind's gold logic:
#   gold_flip = 1 ^ hp ^ (honored_position - 1)   (0 = 앞/N1, 1 = 뒤/N2)
_CELL_BY_GF = {
    0: ("SI_N1", 1, 1),   # +시, honored at N1
    1: ("SI_N2", 1, 2),   # +시, honored at N2
    2: ("PL_N1", 0, 1),   # -시, honored at N1
    3: ("PL_N2", 0, 2),   # -시, honored at N2
}
_ANS = ("앞", "뒤")


def _gold_flip(hp, honored_position):
    return 1 ^ hp ^ (honored_position - 1)


# f2'' held-out pools EXPANDED 4→6 (DESIGN §7 item c; the +2/+2 are G-1-flagged `?`)
HON6 = ["어머님", "회장님", "스승님", "박사님", "원장님", "총장님"]     # 원장님/총장님 = ?-flag
PLAIN6 = ["조카", "후배", "제자", "비서", "조수", "신입"]               # 조수/신입 = ?-flag
FLAGS = {"원장님", "총장님", "조수", "신입"}

# clean RC verbs (plain adnominal, honorific adnominal) — reuse f2 verbs, cycled per conjunct
VERBS = [("웃", "웃는", "웃으시는"), ("오", "오는", "오시는"), ("떠나", "떠나는", "떠나시는")]
MATRIX_TAIL = "기다렸다"


def _conjunct(cell_gf, hon, plain, verb):
    cell, hp, pos = _CELL_BY_GF[cell_gf]
    stem, plain_form, hon_form = verb
    vf = hon_form if hp == 1 else plain_form
    n1, n2 = (hon, plain) if pos == 1 else (plain, hon)
    surface = f"{vf} {n1}의 {n2}도"
    gf = _gold_flip(hp, pos)
    return {
        "cell": cell, "hp": hp, "honored_position": pos,
        "surface": surface, "verb_form": vf, "verb_stem": stem,
        "hon_lexeme": hon, "plain_lexeme": plain, "n1_lexeme": n1, "n2_lexeme": n2,
        "gold_flip": gf, "gold_token": _ANS[gf],
    }


def build_panel():
    items = []
    messages = [(a, b, c) for a in range(4) for b in range(4) for c in range(4)]  # 64
    assert len(messages) == 64
    for rot in range(3):                       # 3 lexeme rotations → 64×3 = 192
        for mi, m in enumerate(messages):
            code = _codeword(m)                # 6 GF(4) cells
            conjs = []
            for k in range(6):
                hon = HON6[k]
                plain = PLAIN6[(k + rot) % 6]   # rotate pairing so lexemes vary across items
                verb = VERBS[k % len(VERBS)]
                conjs.append(_conjunct(code[k], hon, plain, verb))
            surface = " ".join(c["surface"] for c in conjs) + f" {MATRIX_TAIL} => "
            gold_tokens = [c["gold_token"] for c in conjs]
            items.append({
                "panel": "f2doubleprime",
                "rot": rot, "msg": list(m),
                "conjuncts": conjs,
                "surface": surface,
                "gold_flips": [c["gold_flip"] for c in conjs],
                "gold_pattern": "".join(gold_tokens),
                "cells": [c["cell"] for c in conjs],
            })
    return items


# --- F7'' audit (DESIGN §7 additions) ------------------------------------------

def _slot_view(items, k, field):
    return [{"gold_flip": it["gold_flips"][k], field: it["conjuncts"][k][field]} for it in items]


def _majority_by_key(rows, keyfn):
    by = defaultdict(list)
    for r in rows:
        by[keyfn(r)].append(r["gold_flip"])
    correct = 0
    for flips in by.values():
        ones = sum(flips)
        correct += max(ones, len(flips) - ones)
    return correct / len(rows)


def _slot_heuristics(items, k):
    rows = [{
        "gold_flip": it["gold_flips"][k],
        "hp": it["conjuncts"][k]["hp"],
        "honored_position": it["conjuncts"][k]["honored_position"],
        "hon_lexeme": it["conjuncts"][k]["hon_lexeme"],
        "plain_lexeme": it["conjuncts"][k]["plain_lexeme"],
        "n1_lexeme": it["conjuncts"][k]["n1_lexeme"],
        "verb_stem": it["conjuncts"][k]["verb_stem"],
        "verb_form": it["conjuncts"][k]["verb_form"],
    } for it in items]
    presence = _majority_by_key(rows, lambda r: r["hp"])                # presence-attach
    locality = _majority_by_key(rows, lambda r: 0)                      # nearest-noun const
    marker = _majority_by_key(rows, lambda r: r["honored_position"])    # marker-position
    lexmax = max(_majority_by_key(rows, (lambda kk: (lambda r: r[kk]))(kk))
                 for kk in ("hon_lexeme", "plain_lexeme", "n1_lexeme", "verb_stem", "verb_form"))
    return {"presence_attach": round(presence, 4), "locality": round(locality, 4),
            "marker_position": round(marker, 4), "lexical_lookup_max": round(lexmax, 4)}


def _pairwise_corr(items):
    """Max |P(gold_a=gold_b) - 0.5| over all slot pairs (0 ⇒ independent)."""
    worst = 0.0
    worst_pair = None
    for a in range(6):
        for b in range(a + 1, 6):
            same = sum(1 for it in items if it["gold_flips"][a] == it["gold_flips"][b])
            frac = same / len(items)
            dev = abs(frac - 0.5)
            if dev > worst:
                worst, worst_pair = dev, (a, b)
    return round(worst, 4), worst_pair


def audit(h, items):
    n = len(items)
    per_slot = [_slot_heuristics(items, k) for k in range(6)]
    slot_balance = [round(sum(it["gold_flips"][k] for it in items) / n, 4) for k in range(6)]
    corr, corr_pair = _pairwise_corr(items)
    # answer-pattern majority: can the 6-token pattern be guessed constant? (per-slot 0.5 already)
    patt = _majority_by_key(
        [{"gold_flip": 0} for _ in items], lambda r: 0)  # trivially 0.5-safe placeholder
    # real answer-pattern heuristic: majority over the whole 6-tuple (should be ~1/64 groups → report)
    by_patt = defaultdict(int)
    for it in items:
        by_patt[it["gold_pattern"]] += 1
    patt_majority = max(by_patt.values()) / n
    # 도-boundary constancy: every conjunct surface ends with '도', matrix tail constant
    boundary_ok = all(c["surface"].endswith("도") for it in items for c in it["conjuncts"])
    tail_ok = all(it["surface"].endswith(f"{MATRIX_TAIL} => ") for it in items)
    no_neg = all(not any(x in it["surface"] for x in ["않", "아니", " 안 ", " 못 "]) for it in items)

    def _band(x):
        return 0.48 <= x <= 0.52

    heur_ok = all(_band(v) for s in per_slot for v in s.values())
    balance_ok = all(_band(b) for b in slot_balance)
    corr_ok = corr <= 0.02
    struct_ok = boundary_ok and tail_ok and no_neg
    ok = heur_ok and balance_ok and corr_ok and struct_ok
    return {
        "n": n, "K": 6, "n_nodes": 20,
        "per_slot_heuristics": per_slot,
        "per_slot_gold_balance": slot_balance,
        "worst_pairwise_slot_gold_dev": corr, "worst_pair": corr_pair,
        "answer_pattern_majority": round(patt_majority, 4),
        "distinct_patterns": len(by_patt),
        "structural": {"도_boundary_const": boundary_ok, "matrix_tail_const": tail_ok,
                       "negators_absent": no_neg},
        "heuristics_in_band": heur_ok, "balance_in_band": balance_ok,
        "pairwise_independent": corr_ok,
        "F7pp_pass": ok,
    }


def main() -> int:
    h = _harness()
    items = build_panel()
    rep = audit(h, items)

    print("=" * 74)
    print("H_004 MULTI-BIND K=6 — F7'' panel audit (redesign after single-bind F4-DEAD)")
    print("=" * 74)
    print(f"n={rep['n']} sentences · K={rep['K']} conjuncts · nodes={rep['n_nodes']} · "
          f"distinct answer-patterns={rep['distinct_patterns']}")
    print(f"\nper-slot gold balance : {rep['per_slot_gold_balance']}")
    print(f"worst pairwise slot-gold deviation from 0.5: {rep['worst_pairwise_slot_gold_dev']} "
          f"(pair {rep['worst_pair']})  [OA strength-2 ⇒ expect 0.0]")
    print(f"answer-pattern majority: {rep['answer_pattern_majority']} "
          f"(over {rep['distinct_patterns']} patterns)")
    print("\nper-slot heuristics (each must be 0.48–0.52):")
    for k, s in enumerate(rep["per_slot_heuristics"]):
        print(f"  slot {k}: presence={s['presence_attach']} locality={s['locality']} "
              f"marker={s['marker_position']} lexmax={s['lexical_lookup_max']}")
    st = rep["structural"]
    print(f"\nstructural: 도_boundary={st['도_boundary_const']} matrix_tail={st['matrix_tail_const']} "
          f"neg_absent={st['negators_absent']}")
    print(f"heuristics_in_band={rep['heuristics_in_band']} balance_in_band={rep['balance_in_band']} "
          f"pairwise_independent={rep['pairwise_independent']}")
    print("\nF7'' VERDICT:", "PASS — MULTI-BIND panel heuristic-neutral + cross-slot independent, "
          "run G-0/G-1 tension on it" if rep["F7pp_pass"]
          else "FAIL — a slot/pair leaks, DO NOT PROCEED")

    with open(os.path.join(_HERE, "panel_f2doubleprime.json"), "w") as fh:
        json.dump(items, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(_HERE, "f7pp_audit.json"), "w") as fh:
        json.dump(rep, fh, indent=2, ensure_ascii=False)
    # one worked surface for the reviewer
    print("\nexample surface (item 0):\n  " + items[0]["surface"] + items[0]["gold_pattern"])
    print("\nwrote panel_f2doubleprime.json · f7pp_audit.json")
    return 0 if rep["F7pp_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
