#!/usr/bin/env python3
"""H_003 drill-grid generator — the training data (held-out 못 = 0 occurrences).

The drill teaches the negation→polarity-flip RULE using the DRILLED negators
(안 / 않 / 아니) across the 16 verbs, in the SAME sentence frames as the eval
panels (so the panels are structurally in-distribution). The held-out negator 못
appears ZERO times here — the whole test is whether an atomic-negator model
generalises the drilled rule to 못 (A-atom) while a shattered-negator model cannot
(A-shat). Reuses build_panels' verbs + renderers (one source of truth).

Each drill item is (surface, gold_sent). gold_sent = pol(V) XOR (drilled-neg parity).
Depth-parity is preserved: filler slot = no flip (D1-analog), drilled 안 slot in an
않-scaffold = 2 negators = no flip, etc. — but for TRAINING we simply teach the rule
across single- and double-negation, so the model learns to count negation, not to
memorise a surface→label map.

Output: drill_grid.json (raw text; encoded per arm by the training driver later).
Verifies 못 = 0 before writing (the held-out invariant).

Run:  python3 state/h003_atomicity_fixed_codec_drill_2026-07-16/gen_drill.py
"""

from __future__ import annotations

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import build_panels as bp  # reuse VERBS + renderers (one source of truth)

# Drilled negators the drill may teach with (못 is HELD OUT — never here).
# Slot fillers (no-flip) reuse build_panels' register fillers.
DRILLED_SLOTS = ["안"]              # free pre-verb drilled negator for the slot
BOUND_SCAFFOLD = ("않", "지는 않았")  # the 않-scaffold is itself one drilled negator


def gold_sent(pol, neg_count):
    return "긍정." if (pol ^ (neg_count % 2)) else "부정."


def build_drill():
    """One item per (verb, register, slot-variant). The 않-scaffold (render_A)
    already carries one drilled negator (않); the slot adds a filler (no extra
    negator) or 안 (one more → depth-2). The 아니-cleft (render_K) carries 아니."""
    items = []
    for v in bp.VERBS:
        pol = v[0]
        # 않-scaffold family (already 1 negator = 않)
        for tail, filler in bp.REG_A:
            # slot = filler → 1 negator (않) → flip
            items.append((bp.render_A(v, filler, tail), gold_sent(pol, 1)))
            # slot = 안 → 2 negators (안 + 않) → no flip
            items.append((bp.render_A(v, "안", tail), gold_sent(pol, 2)))
        # 아니-cleft family (already 1 negator = 아니)
        for tail, filler in bp.REG_K:
            items.append((bp.render_K(v, filler, tail), gold_sent(pol, 1)))
            items.append((bp.render_K(v, "안", tail), gold_sent(pol, 2)))
        # base D0 (no negation at all) so the model sees the un-negated polarity too
        # rendered as a plain declarative with the filler, no scaffold negator
        for tail, filler in bp.REG_A:
            base = tail.replace("않", "").replace("았", "았")  # keep a clean positive tail
        # a clean positive frame: `이 영화 [filler] {V}었다` (no negator) => pol
        for _tail, filler in bp.REG_A:
            stem = v[2] if v[1] == "s" else v[2] + " " + v[3]
            items.append((f"이 영화 {filler} {stem}었다 => ", gold_sent(pol, 0)))
    return items


def main() -> int:
    items = build_drill()
    surfaces = [s for s, _ in items]

    # HELD-OUT INVARIANT: 못 must appear zero times in the drill.
    mot_count = sum(s.count("못") for s in surfaces)
    # DRILLED present: 안/않/아니 must appear (the rule is teachable)
    drilled_present = sum(1 for s in surfaces if ("안" in s or "않" in s or "아니" in s))
    # label balance
    pos = sum(1 for _, g in items if g == "긍정.")
    neg = len(items) - pos

    print("=" * 70)
    print("H_003 drill-grid generator — held-out 못 invariant")
    print("=" * 70)
    print(f"drill items      : {len(items)}")
    print(f"못 occurrences   : {mot_count}   (MUST be 0 — held out)")
    print(f"drilled-negator lines: {drilled_present}/{len(items)}")
    print(f"label balance    : 긍정 {pos} / 부정 {neg}")
    print("sample:")
    for s, g in items[:6]:
        print(f"   {s}{g}")
    ok = (mot_count == 0) and drilled_present > 0
    print()
    print("VERDICT:", "drill grid OK — 못 held out, negation rule teachable"
          if ok else "BROKEN — held-out invariant violated (못 present) or no drilled negation")

    out = {"n_items": len(items), "mot_occurrences": mot_count,
           "drilled_lines": drilled_present, "pos": pos, "neg": neg,
           "held_out_ok": ok, "items": [{"surface": s, "gold": g} for s, g in items]}
    with open(os.path.join(_HERE, "drill_grid.json"), "w") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print("wrote drill_grid.json")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
