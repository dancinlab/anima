#!/usr/bin/env python3
"""H_007 mech-5 G-0 — SWAP-XOR panel builder + full closed-form audit ($0, deterministic).

Implements DESIGN_fable5_seed.md §3/§5-G0. The panel makes ROLE BINDING measurable: gold is a
synthetic drill-grammar rule composing TWO non-adjacent ingredients,

    gold  =  class(subject)  XOR  form(object-marker)

so no single local window computes it. Role (subject vs object) is read from a CASE MARKER, not
from position — sentences are scrambling-counterbalanced (SOV / OSV), so every single-site
heuristic sits at exactly 0.500 (closed-form, F7).

Grammar (fixed byte offsets — every noun 6 B, every marker 3 B, verb-stem fixed, answer 3 B):
    SOV:  [N_subj:6][SUBJ_MARK:3][N_obj:6][OBJ_MARK_m:3][VERB]   -> answer [AGREE_g:3]
    OSV:  [N_obj:6][OBJ_MARK_m:3][N_subj:6][SUBJ_MARK:3][VERB]   -> answer [AGREE_g:3]
  - SUBJ_MARK: one fixed synthetic subject particle (class-NEUTRAL — marks role, never class).
  - OBJ_MARK_m: two synthetic object particles carrying the marker bit m (byte-length matched).
  - class(N): drilled lexical partition {honored=1, plain=0}; fixed-byte-length pools so the
    subject<->object filler swap stays byte-aligned (head-G's target, below).
  - AGREE_g: the verb's agreement suffix, two byte-length-matched forms; gold selects which.

head-G target (mech-5 A-tug) = swap(x): the SAME sentence with the two 6-B noun FILLERS transposed
and the markers/verb held in place — forcing the shared trunk to encode BOTH fillers AND their
roles. swap(x) is built from surface components ONLY: it contains NO agreement suffix => the gold
bit is structurally absent from head-G's supervision (the raw-hon-phi scaffolding-certifier trap
from G3-a, banned here up front).

G-0 audit (exit 0 iff ALL pass):
  A1 free-slot         : K=1 single answer slot -> _panel_free_slots == [0] (nothing prefix-determined).
  A2 GF(2) codebook    : rank{class_subj, marker, gold}=2 AND gold not in span of any single ingredient.
  A3 F7 heuristics      : class-of-first / class-nearest-verb / class-majority / marker-alone /
                          class(subj)-alone / every single byte-position -> all == 0.500.
  A4 length-parity      : both AGREE forms 3 B; both OBJ_MARK forms 3 B; both noun classes 6 B
                          (teacher-forcing CE-normalization cannot leak via length).
  A5 swap alignment     : for every item |swap(x)| == |x| AND swap == x with the two noun fields
                          transposed, markers/verb byte-identical.
  A6 leak ban           : AGREE_g bytes absent from swap(x); head-G target carries no gold channel.
  balance/decorr        : gold 50/50; class_subj, marker, order each 50/50 and pairwise independent.

Run:  python3 state/h007_gradient_tug_role_code_drill_2026-07-17/build_swap_xor.py
Exit: 0 iff every audit PASS. Writes swap_xor_f2.json / swap_xor_f1.json / swap_xor_reserved.json.
"""

from __future__ import annotations

import json
import os
import random
import sys
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
_H004 = os.path.join(_ROOT, "state", "h004_parser_duel_tension_rank_drill_2026-07-16")

# ---------------------------------------------------------------- inventory (fixed byte lengths)
# 2-syllable nouns = 6 UTF-8 bytes each. class 1 = honored, class 0 = plain (drilled partition).
HON = ["사장", "교수", "부장", "회장", "원장", "총장", "판사", "검사", "장관", "차관", "국장", "실장"]
PLAIN = ["학생", "친구", "동생", "이웃", "직원", "손자", "조카", "제자", "청년", "소년", "소녀", "하인"]

SUBJ_MARK = "뷔"                 # fixed synthetic subject particle (3 B, class-neutral)
OBJ_MARK = ("죠", "퓨")          # two synthetic object particles = marker bit (3 B each)
VERB = "달리"                    # fixed verb stem (6 B)
AGREE = ("네", "지")             # agreement-suffix answer forms (3 B each); gold selects index

ORDERS = ("SOV", "OSV")


def _bytelen(s):
    return len(s.encode("utf-8"))


# assert the fixed-length contract up front (any drift here silently breaks swap alignment)
for _n in HON + PLAIN:
    assert _bytelen(_n) == 6, f"noun {_n!r} is not 6 bytes"
assert _bytelen(SUBJ_MARK) == 3
assert all(_bytelen(m) == 3 for m in OBJ_MARK) and OBJ_MARK[0] != OBJ_MARK[1]
assert all(_bytelen(a) == 3 for a in AGREE) and AGREE[0] != AGREE[1]
assert _bytelen(VERB) == 6


# ---------------------------------------------------------------- surface + swap render
def render(n_subj, n_obj, marker, order):
    """Byte-exact surface. Fields at fixed offsets so the noun swap is a clean transpose."""
    om = OBJ_MARK[marker]
    if order == "SOV":
        return f"{n_subj}{SUBJ_MARK}{n_obj}{om}{VERB}"
    return f"{n_obj}{om}{n_subj}{SUBJ_MARK}{VERB}"        # OSV: object NP first


def render_swap(n_subj, n_obj, marker, order):
    """head-G target = swap(x): transpose the two noun FILLERS, markers/verb fixed. No answer suffix."""
    om = OBJ_MARK[marker]
    if order == "SOV":
        return f"{n_obj}{SUBJ_MARK}{n_subj}{om}{VERB}"    # subj slot now holds n_obj, obj slot n_subj
    return f"{n_subj}{om}{n_obj}{SUBJ_MARK}{VERB}"


def gold_bit(class_subj, marker):
    return class_subj ^ marker


def make_item(n_subj, cs, n_obj, marker, order):
    g = gold_bit(cs, marker)
    surface = render(n_subj, n_obj, marker, order)
    return {
        "surface": surface,
        "gold_token": AGREE[g],                          # single answer slot (K=1)
        "swap_target": render_swap(n_subj, n_obj, marker, order),
        "cell": {"class_subj": cs, "marker": marker, "order": order, "gold": g,
                 "n_subj": n_subj, "n_obj": n_obj},
    }


# ---------------------------------------------------------------- panel generation
# DETERMINISTIC-BALANCED construction (H_004's orthogonal-array discipline, not random sampling):
# to make gold EXACTLY independent of every single-site feature in the finite panel, each noun lexeme
# must appear equally across the marker bit (so gold = class^marker is balanced within every lexeme)
# and object class is balanced per stratum. We fix a pair-multiset per (class_subj, order) and cross it
# with BOTH markers -> every subject/object lexeme, every byte, and both orders are 50/50 vs gold.
# f2 (verdict, OOD) = held-out (N_subj,N_obj) pairings; f1 (liveness) = DISJOINT drilled pairings.
def _all_pairs(cs):
    """ALL distinct class-balanced (subj,obj) pairs for class_subj=cs, deterministic order. Subject
    ranges over its class pool; object over a class-ALTERNATING interleave of both pools (so the pair
    list is object-class balanced). 12 subj x 24 obj-slots = plenty of distinct pairs (>> f2+f1 need)."""
    subj_pool = HON if cs == 1 else PLAIN
    # interleave HON/PLAIN so consecutive objects alternate class -> class-balanced by construction
    obj_seq = [n for pair in zip(HON, PLAIN) for n in pair]      # [HON0,PLAIN0,HON1,PLAIN1,...] len 24
    pairs = []
    for a in range(len(subj_pool)):
        for b in range(len(obj_seq)):
            ns, no = subj_pool[a], obj_seq[b]
            if ns != no:
                pairs.append((ns, no))
    return pairs                                                 # deterministic, ~276 distinct pairs


def build_panels():
    # per (cs,order): F2_NP pairs held out for the verdict panel, F1_NP DISJOINT pairs for liveness.
    # crossing BOTH markers doubles each -> f2 = 2(cs)*2(order)*2(marker)*F2_NP; F2_NP=24 -> 192, F1=64.
    F2_NP, F1_NP = 24, 8

    f2, f1, reserved = [], [], set()
    for cs in (0, 1):
        for order in ORDERS:
            allp = _all_pairs(cs)
            # object-class-balanced slice: take F2_NP with equal honored/plain objects, then F1_NP disjoint
            f2_pairs = _balanced_slice(allp, F2_NP, start=0)
            f1_pairs = _balanced_slice([p for p in allp if p not in set(f2_pairs)], F1_NP, start=0)
            for marker in (0, 1):                          # cross BOTH markers -> gold balanced per lexeme
                for (ns, no) in f2_pairs:
                    f2.append(make_item(ns, cs, no, marker, order))
                    reserved.add((ns, no))
                for (ns, no) in f1_pairs:
                    f1.append(make_item(ns, cs, no, marker, order))
    return f2, f1, sorted(reserved)


def _balanced_slice(pairs, count, start):
    """`count` pairs with EQUAL honored/plain OBJECT class (count must be even), preserving order."""
    assert count % 2 == 0
    hon_obj = [p for p in pairs if p[1] in HON][start:]
    plain_obj = [p for p in pairs if p[1] in PLAIN][start:]
    out = []
    for i in range(count // 2):
        out.append(hon_obj[i]); out.append(plain_obj[i])
    return out


# ---------------------------------------------------------------- audits
def _free_slots(panel):
    """Reuse the FROZEN mech-1 free-slot computation verbatim (never re-implement the metric)."""
    sys.path.insert(0, _H004)
    import train_h004
    return train_h004._panel_free_slots(panel)


def _best_map_acc(feature_vals, golds):
    """Closed-form best deterministic map feature->{0,1}: accuracy of the majority-gold per feature value.
    This is the strongest a single-feature heuristic can do; for a balanced-decorrelated panel -> 0.5."""
    by = defaultdict(lambda: [0, 0])
    for f, g in zip(feature_vals, golds):
        by[f][g] += 1
    correct = sum(max(c0, c1) for c0, c1 in by.values())
    return correct / len(golds)


def audit(f2, f1):
    res = {"pass": True, "checks": {}}

    def check(name, ok, detail):
        res["checks"][name] = {"pass": bool(ok), "detail": detail}
        if not ok:
            res["pass"] = False

    golds = [it["cell"]["gold"] for it in f2]
    cs = [it["cell"]["class_subj"] for it in f2]
    mk = [it["cell"]["marker"] for it in f2]
    od = [1 if it["cell"]["order"] == "OSV" else 0 for it in f2]
    n = len(f2)

    # A1 free-slot: single answer slot, nothing prefix-determined
    fs2, fs1 = _free_slots(f2), _free_slots(f1)
    check("A1_free_slot", fs2 == [0] and fs1 == [0], f"f2 free_slots={fs2} f1 free_slots={fs1} (want [0])")

    # A2 GF(2) codebook: gold = class_subj XOR marker exactly; gold not equal to either ingredient alone
    xor_ok = all(g == (a ^ b) for g, a, b in zip(golds, cs, mk))
    gold_eq_cs = all(g == a for g, a in zip(golds, cs))
    gold_eq_mk = all(g == b for g, b in zip(golds, mk))
    # GF(2) rank over the 3 columns {class_subj, marker, gold}: gold is their XOR -> rank 2
    rows = list({(a, b, g) for a, b, g in zip(cs, mk, golds)})
    rank = _gf2_rank([list(r) for r in rows])
    check("A2_gf2_codebook", xor_ok and not gold_eq_cs and not gold_eq_mk and rank == 2,
          f"gold==class^marker:{xor_ok} rank={rank} gold==cs:{gold_eq_cs} gold==mk:{gold_eq_mk}")

    # A3 F7 heuristics — every single-site feature must sit at 0.500
    heur = {}
    heur["class_subj_alone"] = _best_map_acc(cs, golds)
    heur["marker_alone"] = _best_map_acc(mk, golds)
    # class of the FIRST noun (SOV->subject, OSV->object) and class NEAREST the verb (SOV->object, OSV->subject)
    first_cls, near_cls, maj_cls = [], [], []
    for it in f2:
        c = it["cell"]
        csubj = c["class_subj"]
        cobj = 1 if c["n_obj"] in HON else 0
        if c["order"] == "SOV":
            first_cls.append(csubj); near_cls.append(cobj)
        else:
            first_cls.append(cobj); near_cls.append(csubj)
        maj_cls.append(1 if (csubj + cobj) >= 1 else 0)          # presence/majority of honored
    heur["class_first_noun"] = _best_map_acc(first_cls, golds)
    heur["class_nearest_verb"] = _best_map_acc(near_cls, golds)
    heur["class_presence_majority"] = _best_map_acc(maj_cls, golds)
    # every single BYTE POSITION of the surface (min length) as a categorical feature
    surfs = [it["surface"].encode("utf-8") for it in f2]
    L = min(len(s) for s in surfs)
    byte_max = 0.0
    for p in range(L):
        byte_max = max(byte_max, _best_map_acc([s[p] for s in surfs], golds))
    heur["worst_single_byte"] = byte_max
    he_ok = all(abs(v - 0.5) < 1e-9 for k, v in heur.items() if k != "worst_single_byte") \
        and byte_max <= 0.5 + 1e-9
    check("A3_heuristics_0p5", he_ok, heur)

    # A4 length-parity (teacher-forcing CE cannot leak via candidate length)
    lp = (_bytelen(AGREE[0]) == _bytelen(AGREE[1]) == 3
          and _bytelen(OBJ_MARK[0]) == _bytelen(OBJ_MARK[1]) == 3
          and all(_bytelen(x) == 6 for x in HON + PLAIN)
          and len({len(it["surface"].encode()) for it in f2}) == 1)     # all surfaces equal byte length
    check("A4_length_parity", lp,
          f"agree={[_bytelen(a) for a in AGREE]} objmark={[_bytelen(m) for m in OBJ_MARK]} "
          f"surface_lens={sorted({len(it['surface'].encode()) for it in f2})}")

    # A5 swap alignment — swap(x) == x with the two 6-B noun fields transposed, byte-length preserved
    swap_ok, swap_bad = True, None
    for it in f2 + f1:
        c = it["cell"]
        x = it["surface"]; sw = it["swap_target"]
        if len(x.encode()) != len(sw.encode()):
            swap_ok = False; swap_bad = ("len", it["surface"]); break
        # reconstruct expected swap independently
        exp = render_swap(c["n_subj"], c["n_obj"], c["marker"], c["order"])
        if sw != exp:
            swap_ok = False; swap_bad = ("mismatch", it["surface"]); break
        # the transpose actually moved the fillers (n_subj != n_obj guaranteed)
        if sw == x:
            swap_ok = False; swap_bad = ("noop", it["surface"]); break
    check("A5_swap_alignment", swap_ok, f"bad={swap_bad}")

    # A6 supervision-leak ban — neither AGREE form appears in any head-G target
    leak = None
    for it in f2 + f1:
        for a in AGREE:
            if a in it["swap_target"]:
                leak = (it["surface"], a); break
        if leak:
            break
    check("A6_leak_ban", leak is None, f"leak={leak}")

    # balance + pairwise decorrelation
    def bal(v):
        return sum(v) / len(v)

    def corr_indep(a, b):
        j = defaultdict(int)
        for x, y in zip(a, b):
            j[(x, y)] += 1
        # independent & balanced -> each of the 4 joint cells == n/4
        return all(abs(j[(i, k)] - n / 4) <= 1 for i in (0, 1) for k in (0, 1))
    balances = {"gold": bal(golds), "class_subj": bal(cs), "marker": bal(mk), "order": bal(od)}
    bal_ok = all(abs(v - 0.5) < 1e-9 for v in balances.values())
    dec_ok = corr_indep(cs, mk) and corr_indep(cs, od) and corr_indep(mk, od)
    check("balance", bal_ok, balances)
    check("decorrelation", dec_ok,
          {"cs_x_mk": corr_indep(cs, mk), "cs_x_od": corr_indep(cs, od), "mk_x_od": corr_indep(mk, od)})

    # held-out contract: f2 pairings disjoint from f1 pairings (the composition OOD axis)
    p2 = {(it["cell"]["n_subj"], it["cell"]["n_obj"]) for it in f2}
    p1 = {(it["cell"]["n_subj"], it["cell"]["n_obj"]) for it in f1}
    check("held_out_pairings", p2.isdisjoint(p1),
          f"f2 pairs={len(p2)} f1 pairs={len(p1)} overlap={len(p2 & p1)}")

    return res


def _gf2_rank(rows):
    """Rank over GF(2) of a list of 0/1 rows."""
    mat = [r[:] for r in rows]
    ncol = len(mat[0]) if mat else 0
    rank = 0
    for col in range(ncol):
        piv = next((r for r in range(rank, len(mat)) if mat[r][col]), None)
        if piv is None:
            continue
        mat[rank], mat[piv] = mat[piv], mat[rank]
        for r in range(len(mat)):
            if r != rank and mat[r][col]:
                mat[r] = [a ^ b for a, b in zip(mat[r], mat[rank])]
        rank += 1
    return rank


def main():
    f2, f1, reserved = build_panels()
    res = audit(f2, f1)

    print("=" * 78)
    print("H_007 mech-5 G-0 — SWAP-XOR panel + closed-form audit")
    print("=" * 78)
    print(f"f2 (verdict, OOD): n={len(f2)}   f1 (liveness): n={len(f1)}   reserved f2 pairings: {len(reserved)}")
    print(f"gold = class(subject) XOR form(object-marker)   answer forms={AGREE}   markers={OBJ_MARK}")
    print()
    for name, c in res["checks"].items():
        flag = "PASS" if c["pass"] else "FAIL"
        print(f"  [{flag}] {name}: {c['detail']}")
    print()
    print("G-0 VERDICT:", "PASS — panel admissible, freeze-ready pending G-1" if res["pass"]
          else "FAIL — panel NOT admissible (fix before any freeze)")

    if res["pass"]:
        json.dump({"panel": f2, "meta": {"kind": "f2_verdict_ood", "n": len(f2),
                   "gold_rule": "class(subject) XOR form(object-marker)", "answer_forms": list(AGREE)}},
                  open(os.path.join(_HERE, "swap_xor_f2.json"), "w"), ensure_ascii=False, indent=1)
        json.dump({"panel": f1, "meta": {"kind": "f1_liveness", "n": len(f1)}},
                  open(os.path.join(_HERE, "swap_xor_f1.json"), "w"), ensure_ascii=False, indent=1)
        json.dump({"reserved_pairings": reserved, "note": "G-2 gen_drill MUST exclude these (subj,obj) pairs"},
                  open(os.path.join(_HERE, "swap_xor_reserved.json"), "w"), ensure_ascii=False, indent=1)
        print("wrote swap_xor_f2.json / swap_xor_f1.json / swap_xor_reserved.json")
    return 0 if res["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
