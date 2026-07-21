#!/usr/bin/env python3
"""H_003 panel builder + F7 audit — v3 (SLOT-CONTRAST), the pre-training don't-run gate.

History: v1 leaked via unique tails (template heuristic 1.0). v2 fixed the tails but
let a DRILLED negator (안) carry the depth-2 bit in one family, so a drilled-only
reader recovered parity without touching 못 (held_out_blind 0.25). v3 removes the
whole possibility class:

SLOT-CONTRAST — every minimal pair holds the drilled scaffold CONSTANT (않- or 아니-,
exactly one drilled negator per item) and varies ONLY a pre-verbal slot eojeol:
held-out 못 (depth-2) vs a 1-syllable sentiment-neutral filler 잘/더/꽤 (depth-1).
Closed-form consequences:
  * presence   : a negator is present in every item, D1:D2 = 50:50   -> 0.5
  * held_out_blind: drilled_negator_count == 1 on every item          -> 0.5 exactly
  * tails      : byte-identical within a pair (incl. the verb eojeol) -> 0.5
  * eojeol count: the filler fills the slot in D1, so pair lengths match -> 0.5
  * slot char length: fillers are 1 syllable, like 못                  -> uninformative
The ONLY discriminator left inside a pair is the identity of the slot eojeol —
못 vs a transparent adverb — i.e. exactly the individuation the hypothesis is about.
The filler side of that coin (knowing 잘/더/꽤 are NOT negators) is arm-SYMMETRIC:
fillers are never in the shatter list, so their encoding is identical in A-atom and
A-shat, and any arm delta still routes through 못's encoding alone.

PURE-못 (depth-2 as double 못: `못 {V}지 못했다`) was REJECTED as ungrammatical —
Korean forbids same-negator doubling (*안 가지 않았다 / *못 가지 못했다).

Bound 못 (`-지 못하-`) cannot be a clean sole discriminator: it drags the -지
scaffold and an extra eojeol in with it (a 지-reader or eojeol-counter recovers the
depth bit without individuating 못). So f2' verdicts FREE 못 only; a bound
diagnostic panel f2b rides along NON-VERDICT (documented length leak; its use is the
arm CONTRAST per cell, sign-gated across seeds, F5 becomes directional-only).

worst_suffix_leak is reported capped at L=10: past the shared pair-region it groups
singleton (verb,cell) surfaces and returns 1.0 mechanically, and it would score
detecting the target token itself as a leak — held_out_blind_score supersedes it as
the gate (see its docstring in tool/anima_v4.py). Gates per panel:
  f2prime : presence + held_out_blind + template + suffix(<=10) + eojeol-length
            + per-cell SENTIMENT balance -> ALL 0.5 +/- 0.02 -> verdict panel
  f1prime : same minus held_out_blind (drilled-solvable BY DESIGN — liveness/ceiling
            panel; blind score reported, expected 1.0)
  f2b     : report-only, verdict_eligible=false

Run:  python3 state/h003_atomicity_fixed_codec_drill_2026-07-16/build_panels.py
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


# --- FROZEN inventory -----------------------------------------------------------
#
# Verbs: 8 positive + 8 negative review-sentiment stems, every one 못-compatible
# (volitional) in EVERY cell. kind "s" = simple stem (slot pre-posed: `잘/못 {V}`);
# kind "c" = N + light-verb compound (slot split: `{N} 잘/못 {LV}` — the prescriptive
# short-negation form, and it keeps pair eojeol-counts equal). adn = past adnominal
# for the 아니-cleft family. `?` = flagged for the G-1 operator grammar pass.
# NOTE vs v2 inventory: 하품하/후회하/실망하/지루해하/짜증내 were re-audited for
# 못-compatibility; non-volitional reactions dropped, volitional review actions in
# (돌려보/건너뛰). G-1 minimum-12 rule applies unchanged.
# G-1 PROVISIONAL (LLM first-pass, pending native operator confirm): the three ?-flagged
# verbs were swapped for clearly volitional + 못-compatible review actions —
# 기대하→감상하 (stative→appreciate), 졸→야유하 (non-volitional→jeer), 끄→참 (odd→endure).
# This narrows the human gate to CONFIRMING these three, not judging borderline cases.
VERBS = [
    # (polarity, kind, N-or-stem, LV-or-adn, [LV-adn])
    (1, "s", "즐기", "즐긴"),
    (1, "s", "웃", "웃은"),
    (1, "c", "몰입", "하", "한"),
    (1, "c", "집중", "하", "한"),
    (1, "c", "공감", "하", "한"),
    (1, "c", "추천", "하", "한"),
    (1, "c", "이해", "하", "한"),
    (1, "c", "감상", "하", "한"),      # 감상하다=appreciate/view (G-1 PASS · volitional +못-compat)
    (0, "c", "야유", "하", "한"),      # 야유하다=jeer (G-1 PASS · volitional negative)
    (0, "s", "참", "참은"),            # 참다=endure, 못 참다=couldn't bear (G-1 PASS)
    (0, "s", "돌려보", "돌려본"),
    (0, "s", "건너뛰", "건너뛴"),
    (0, "c", "딴짓", "하", "한"),
    (0, "c", "딴생각", "하", "한"),
    (0, "c", "딴청", "부리", "부린"),
    (0, "c", "짜증", "내", "낸"),
]

# Fillers: 1-syllable (matches 못's char length), CPT-frequent, drill-absent,
# no ㅁ-initial jamo (막 rejected: shares onset ㅁ with 못). Bound to the register so
# every verb crosses every filler and filler||flip independence is exact.
# A-family register tails / K-family register tails, each with its filler.
REG_A = [("않았다", "잘"), ("않았어요", "더"), ("않았음", "꽤")]
REG_K = [("아니다", "잘"), ("아니에요", "더"), ("아님", "꽤")]
REG_A_LIVE = [("않았네요", "잘")]   # f1' held-out 4th register
REG_K_LIVE = [("아니네요", "잘")]


def render_A(v, slot, tail):
    """않-scaffold family: `이 영화 [SLOT] {V}지는 않았-REG`."""
    if v[1] == "s":
        return f"이 영화 {slot} {v[2]}지는 {tail} => "
    return f"이 영화 {v[2]} {slot} {v[3]}지는 {tail} => "


def render_K(v, slot, tail):
    """아니-cleft family: `이 영화 [SLOT] {V-adn} 것은 아니-REG`."""
    if v[1] == "s":
        return f"이 영화 {slot} {v[3]} 것은 {tail} => "
    return f"이 영화 {v[2]} {slot} {v[4]} 것은 {tail} => "


def render_Kb1(v, tail):
    """bound-diagnostic D1: plain 아니-cleft, no slot."""
    if v[1] == "s":
        return f"이 영화 {v[3]} 것은 {tail} => "
    return f"이 영화 {v[2]}{v[4]} 것은 {tail} => "


def render_Kb2(v, tail):
    """bound-diagnostic D2: BOUND 못 (`-지 못한`) under the 아니-cleft."""
    stem = v[2] if v[1] == "s" else v[2] + v[3]
    return f"이 영화 {stem}지 못한 것은 {tail} => "


def item(cell, v, surface, template, heldout, drilled):
    total = heldout + drilled
    flip = total % 2
    return {
        "cell": cell,
        "verb": v[2] if v[1] == "s" else v[2] + v[3],
        "verb_polarity": v[0],
        "template": template,
        "negator_count": total,
        "drilled_negator_count": drilled,
        "heldout_negator_count": heldout,
        "gold_flip": flip,
        "gold_sent": v[0] ^ flip,
        "eojeol_len": len(surface.split()),
        "surface": surface,
    }


def build_f2prime():
    items = []
    for v in VERBS:
        for tail, filler in REG_A:
            t = f"지는 {tail} => "
            items.append(item("A1", v, render_A(v, filler, tail), t, 0, 1))
            items.append(item("A2", v, render_A(v, "못", tail), t, 1, 1))
        for tail, filler in REG_K:
            t = f"것은 {tail} => "
            items.append(item("K1", v, render_K(v, filler, tail), t, 0, 1))
            items.append(item("K2", v, render_K(v, "못", tail), t, 1, 1))
    return items


def build_f1prime():
    items = []
    for v in VERBS:
        for tail, filler in REG_A_LIVE:
            t = f"지는 {tail} => "
            items.append(item("L1", v, render_A(v, filler, tail), t, 0, 1))
            items.append(item("L2", v, render_A(v, "안", tail), t, 0, 2))
        for tail, filler in REG_K_LIVE:
            t = f"것은 {tail} => "
            items.append(item("L3", v, render_K(v, filler, tail), t, 0, 1))
            items.append(item("L4", v, render_K(v, "안", tail), t, 0, 2))
    return items


def build_f2b():
    items = []
    for v in VERBS:
        for tail, _f in REG_K:
            t = f"것은 {tail} => "
            items.append(item("Kb1", v, render_Kb1(v, tail), t, 0, 1))
            items.append(item("Kb2", v, render_Kb2(v, tail), t, 1, 1))
    return items


def majority_score(items, key):
    """Best majority-guess strategy over groups of `key` — same machinery as the
    harness template heuristic, applied to an arbitrary grouping."""
    g = defaultdict(list)
    for it in items:
        g[key(it)].append(it["gold_flip"])
    correct = 0
    for flips in g.values():
        maj = 1 if sum(flips) * 2 >= len(flips) else 0
        correct += sum(1 for f in flips if f == maj)
    return correct / len(items)


def audit(h, items, gate_blind=True, gated=True):
    presence = h.presence_heuristic_score(items)
    blind = h.held_out_blind_score(items)
    template = h.template_heuristic_score(items)
    suffix = h.worst_suffix_leak(items, max_len=10)
    length = majority_score(items, lambda it: it["eojeol_len"])
    sent_bal = {}
    by_c = defaultdict(list)
    for it in items:
        by_c[it["cell"]].append(it["gold_sent"])
    for c, v in sorted(by_c.items()):
        sent_bal[c] = sum(v) / len(v)
    d1 = sum(1 for it in items if it["negator_count"] == 1)
    d2 = sum(1 for it in items if it["negator_count"] == 2)
    checks = [
        abs(presence - 0.5) <= 0.02,
        abs(template - 0.5) <= 0.02,
        abs(suffix["worst_suffix_score"] - 0.5) <= 0.02,
        abs(length - 0.5) <= 0.02,
        all(abs(b - 0.5) <= 0.02 for b in sent_bal.values()),
        d1 == d2,
    ]
    if gate_blind:
        checks.append(abs(blind - 0.5) <= 0.02)
    ok = all(checks) if gated else False
    return {
        "n": len(items),
        "presence_heuristic": round(presence, 4),
        "held_out_blind": round(blind, 4),
        "held_out_blind_gated": gate_blind,
        "template_heuristic": round(template, 4),
        "worst_suffix_leak_L<=10": suffix,
        "eojeol_length_heuristic": round(length, 4),
        "sentiment_balance_per_cell": {k: round(x, 4) for k, x in sent_bal.items()},
        "depth_split_D1_D2": [d1, d2],
        "F7_pass": ok,
        "verdict_eligible": gated,
    }


def main() -> int:
    h = _harness()
    f2 = build_f2prime()
    f1 = build_f1prime()
    f2b = build_f2b()

    report = {
        "f2prime": audit(h, f2, gate_blind=True, gated=True),
        "f1prime": audit(h, f1, gate_blind=False, gated=True),
        "f2b_bound_diagnostic": audit(h, f2b, gate_blind=True, gated=False),
    }
    # cross-panel union: at eval one model sees all panels — no tail may leak
    # across panel boundaries either (f2b shares the 아니-cleft tails with K cells).
    union_template = h.template_heuristic_score(f2 + f1 + f2b)
    report["union_template_heuristic"] = round(union_template, 4)

    ok = (report["f2prime"]["F7_pass"] and report["f1prime"]["F7_pass"]
          and abs(union_template - 0.5) <= 0.02)

    print("=" * 74)
    print("H_003 F7 panel audit v3 (SLOT-CONTRAST) — pre-training don't-run gate")
    print("=" * 74)
    for name in ("f2prime", "f1prime", "f2b_bound_diagnostic"):
        r = report[name]
        print()
        print(f"[{name}] n={r['n']}  D1:D2={r['depth_split_D1_D2']}"
              f"  verdict_eligible={r['verdict_eligible']}")
        print(f"  presence-heuristic       = {r['presence_heuristic']}")
        print(f"  held_out_blind (max s,1-s)= {r['held_out_blind']}"
              f"  (gated: {r['held_out_blind_gated']})")
        print(f"  template-heuristic       = {r['template_heuristic']}")
        print(f"  worst-suffix leak (L<=10) = {r['worst_suffix_leak_L<=10']}")
        print(f"  eojeol-length heuristic  = {r['eojeol_length_heuristic']}")
        print(f"  sentiment balance / cell = {r['sentiment_balance_per_cell']}")
        print(f"  F7 {'PASS' if r['F7_pass'] else ('n/a (diagnostic, non-verdict)' if not r['verdict_eligible'] else 'FAIL')}")
    print()
    print(f"union template heuristic (f2'+f1'+f2b) = {report['union_template_heuristic']}")
    print("F7 VERDICT:", "PASS — panel is heuristic-neutral, arms may be built"
          if ok else "FAIL — panel leaks a countable cue, DO NOT TRAIN")

    out = {"F7_pass": ok, "panels": report,
           "strategy": "SLOT-CONTRAST v3 — drilled scaffold constant within pair; "
                       "slot eojeol = held-out 못 (D2) vs 1-syllable filler 잘/더/꽤 (D1)",
           "note": "gold_flip audited here = negator parity; sentiment gold = pol XOR flip at eval"}
    with open(os.path.join(_HERE, "f7_audit.json"), "w") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    with open(os.path.join(_HERE, "panel_f2prime.json"), "w") as fh:
        json.dump(f2, fh, indent=2, ensure_ascii=False)
    with open(os.path.join(_HERE, "panel_f1prime.json"), "w") as fh:
        json.dump(f1, fh, indent=2, ensure_ascii=False)
    with open(os.path.join(_HERE, "panel_f2b_bound_diagnostic.json"), "w") as fh:
        json.dump(f2b, fh, indent=2, ensure_ascii=False)
    print()
    print("wrote f7_audit.json, panel_f2prime.json, panel_f1prime.json,"
          " panel_f2b_bound_diagnostic.json")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
