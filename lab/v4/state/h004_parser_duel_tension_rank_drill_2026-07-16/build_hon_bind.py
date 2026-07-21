#!/usr/bin/env python3
"""H_004 G-0 — HON-BIND panel builder + F7 audit (pre-training don't-run gate, $0).

Implements SPEC_hon_bind_panel_fable5.md verbatim. Deterministic, stdlib-only, no
`random` — fixed nested loops (pairs -> verbs -> tails -> cells).

The panel makes SUBJECT-HONORIFIC BINDING visible: a prenominal relative clause
`{V-adn(±시)} {N1}의 {N2}도 {TAIL}` is attachment-ambiguous, and ONLY the honorific
-시- (agreeing categorically with an honorable, 님-marked subject) disambiguates which
noun the RC modifies. Answer is a POSITION token 앞 (RC modifies N1) / 뒤 (N2).

    gold_flip = 1 ^ honorific_present ^ (honored_position - 1)      # 0 = 앞/N1, 1 = 뒤/N2

The XOR's two inputs live at opposite string ends (±시 in the initial verb eojeol;
position only by locating the 님-noun mid-string), so every single-feature and every
contiguous-window reader sees at most one input -> pinned to 0.5. F7 verifies that
closed-form BEFORE any arm trains. Metric is d_acc (chance 0.5); f1/f2 are PANEL names.

Run:  python3 state/h004_parser_duel_tension_rank_drill_2026-07-16/build_hon_bind.py
Exit: 0 iff F7 PASS (panel heuristic-neutral, arms may be built).
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


# --- FROZEN inventory (SPEC §1) -------------------------------------------------
# RC verbs: (dict_stem, plain_adnominal, honorific_adnominal). All clean -(으)시-,
# subject-gap, class-neutral semantics; suppletive/ㄹ-final/ㄷ-irregular excluded.
VERBS_F2 = [  # SPEC §1c drill + f2'
    ("웃", "웃는", "웃으시는"),
    ("오", "오는", "오시는"),
    ("떠나", "떠나는", "떠나시는"),
]
VERBS_F1 = [  # drill + f1'
    ("쉬", "쉬는", "쉬시는"),
    ("달리", "달리는", "달리시는"),
    ("노래하", "노래하는", "노래하시는"),
    ("춤추", "춤추는", "춤추시는"),
]

TAILS_F2 = ["기다렸다", "기다렸어요"]   # SPEC §1d drill + f2'
TAIL_F1 = "기다렸네요"                    # held-out register -> f1' only

# SPEC §1e held-out genitive pairs (HON, PLAIN); each lexeme in exactly 2 pairs.
PAIRS_F2 = [
    ("어머님", "조카"), ("어머님", "후배"),
    ("회장님", "비서"), ("회장님", "후배"),
    ("스승님", "제자"), ("스승님", "조카"),
    ("박사님", "비서"), ("박사님", "제자"),
]
PAIRS_F1 = [  # drilled pairs
    ("선생님", "아이"), ("교수님", "학생"),
    ("사장님", "직원"), ("아버님", "친구"),
]

# The four design cells (SPEC §2). Each entry: (cell, honorific_present, honored_position,
# use_honorific_form, honored_is_n1). honored_position: 1 = N1, 2 = N2.
CELLS = [
    ("SI_N1", 1, 1, True, True),    # {V+시} H의 P도  -> honored at N1
    ("SI_N2", 1, 2, True, False),   # {V+시} P의 H도  -> honored at N2
    ("PL_N1", 0, 1, False, True),   # {V-시} H의 P도  -> honored at N1
    ("PL_N2", 0, 2, False, False),  # {V-시} P의 H도  -> honored at N2
]

_ANS = ("앞", "뒤")   # gold_flip 0 -> 앞 (N1), 1 -> 뒤 (N2)
_NEG_STRINGS = ["않", "아니", " 안 ", " 못 "]   # SPEC §0: must be absent everywhere


def _gold_flip(hp: int, honored_position: int) -> int:
    return 1 ^ hp ^ (honored_position - 1)


def item(panel, cell, hp, honored_position, verb_stem, verb_form, hon, plain, tail):
    """Build one panel item (SPEC §6 schema). honored noun is `hon` (님-marked)."""
    n1, n2 = (hon, plain) if honored_position == 1 else (plain, hon)
    surface = f"{verb_form} {n1}의 {n2}도 {tail} => "
    template = f"{verb_form} ⟨N⟩의 ⟨N⟩도 {tail} => "
    gf = _gold_flip(hp, honored_position)
    it = {
        "panel": panel,
        "cell": cell,
        "surface": surface,
        "template": template,
        "honorific_present": hp,
        "honored_position": honored_position,
        "attachment_gold": gf + 1,
        "gold_flip": gf,
        "gold_token": _ANS[gf],
        "hon_lexeme": hon,
        "plain_lexeme": plain,
        "n1_lexeme": n1,
        "n2_lexeme": n2,
        "verb_stem": verb_stem,
        "verb_form": verb_form,
        "tail": tail,
        "eojeol_len": len(surface.split(" => ")[0].split()),
        "char_len": len(surface),
    }
    # SPEC §6 per-item consistency asserts
    assert it["gold_flip"] == (1 ^ hp ^ (honored_position - 1))
    assert it["gold_token"] == _ANS[gf]
    assert hon.endswith("님") and not plain.endswith("님")
    assert (n1 == hon) ^ (n2 == hon)
    assert surface.startswith(verb_form)
    assert surface.endswith("도 " + tail + " => ")
    assert not any(neg in surface for neg in _NEG_STRINGS)
    return it


def build_panel(panel, pairs, verbs, tails):
    items = []
    for (hon, plain) in pairs:
        for (stem, plain_form, hon_form) in verbs:
            for tail in tails:
                for (cell, hp, pos, use_hon, _hon_is_n1) in CELLS:
                    vf = hon_form if use_hon else plain_form
                    items.append(item(panel, cell, hp, pos, stem, vf, hon, plain, tail))
    return items


# --- HON-BIND heuristic scorers (SPEC §4; kept local until stable, §6) ----------

def _majority_by_key(items, keyfn):
    """Fraction correct for the best per-group constant guess (max(maj,1-maj) within
    each group, summed). An anti-correlated cue counts as leaky as a correlated one."""
    by = defaultdict(list)
    for it in items:
        by[keyfn(it)].append(it["gold_flip"])
    correct = 0
    for flips in by.values():
        ones = sum(flips)
        correct += max(ones, len(flips) - ones)
    return correct / len(items)


def presence_attach(items):   # §4.1 — group by honorific_present
    return _majority_by_key(items, lambda it: it["honorific_present"])


def locality(items):          # §4.2 — RC is adjacent to N1 on every item -> constant guess
    return _majority_by_key(items, lambda it: 0)


def lexical_lookup_max(items):  # §4.3 — max over 6 lexical groupings
    keys = ["hon_lexeme", "plain_lexeme", "n1_lexeme", "n2_lexeme", "verb_stem", "tail"]
    return max(_majority_by_key(items, (lambda k: (lambda it: it[k]))(k)) for k in keys)


def marker_position(items):   # §4.4 — group by which slot holds the 님-noun
    return _majority_by_key(items, lambda it: it["honored_position"])


def verbform_prefix_leak(items):  # §4.6 gated form — group by per-item verb-eojeol window
    return _majority_by_key(items, lambda it: it["verb_form"])


def charlen_majority(items):  # §4.8
    return _majority_by_key(items, lambda it: it["char_len"])


def fixedL_prefix_curve(items, max_len=10):  # §4.6 report-only (NOT gated)
    curve = {}
    for L in range(1, max_len + 1):
        curve[L] = round(_majority_by_key(items, (lambda L: (lambda it: it["surface"][:L]))(L)), 4)
    return curve


def task_conjunction_sanity(items):  # §4.9 — must be 1.0 or the gold formula is wrong
    return _majority_by_key(items, lambda it: (it["honorific_present"], it["honored_position"]))


# --- F7 audit (SPEC §7) ---------------------------------------------------------

def _band(x):
    return 0.48 <= x <= 0.52


def audit(h, items, panel_name):
    presence = presence_attach(items)
    loc = locality(items)
    lex = lexical_lookup_max(items)
    marker = marker_position(items)
    templ = h.template_heuristic_score(items)
    suffix = h.worst_suffix_leak(items, max_len=10)["worst_suffix_score"]
    prefix = verbform_prefix_leak(items)
    charlen = charlen_majority(items)
    sanity = task_conjunction_sanity(items)

    # structural (== , not toleranced)
    cell_counts = defaultdict(int)
    for it in items:
        cell_counts[it["cell"]] += 1
    per_cell_equal = len(set(cell_counts.values())) == 1
    eojeol_single = len({it["eojeol_len"] for it in items}) == 1
    particle_const = all(("도 " + it["tail"] + " => ") == it["surface"][-len("도 " + it["tail"] + " => "):] for it in items)
    no_ans_in_surface = all(("앞" not in it["surface"] and "뒤" not in it["surface"]) for it in items)
    no_neg = all(not any(neg in it["surface"] for neg in _NEG_STRINGS) for it in items)

    # gold balance == 0.5 on every stratum (§7)
    def _bal(keyfn):
        by = defaultdict(list)
        for it in items:
            by[keyfn(it)].append(it["gold_flip"])
        return {k: sum(v) / len(v) for k, v in by.items()}

    balances = {
        "overall": sum(it["gold_flip"] for it in items) / len(items),
        "per_hp": _bal(lambda it: it["honorific_present"]),
        "per_pos": _bal(lambda it: it["honored_position"]),
        "per_hon_lexeme": _bal(lambda it: it["hon_lexeme"]),
        "per_plain_lexeme": _bal(lambda it: it["plain_lexeme"]),
        "per_verb": _bal(lambda it: it["verb_stem"]),
        "per_tail": _bal(lambda it: it["tail"]),
    }
    all_half = abs(balances["overall"] - 0.5) < 1e-9 and all(
        abs(v - 0.5) < 1e-9
        for grp in ("per_hp", "per_pos", "per_hon_lexeme", "per_plain_lexeme", "per_verb", "per_tail")
        for v in balances[grp].values()
    )

    heuristics = {
        "presence_attach": round(presence, 4),
        "locality": round(loc, 4),
        "lexical_lookup_max": round(lex, 4),
        "marker_position": round(marker, 4),
        "template_heuristic": round(templ, 4),
        "worst_suffix_leak_L10": round(suffix, 4),
        "verbform_prefix_leak": round(prefix, 4),
        "charlen_majority": round(charlen, 4),
    }
    heur_ok = all(_band(v) for v in heuristics.values())
    struct_ok = (per_cell_equal and eojeol_single and particle_const and no_ans_in_surface
                 and no_neg and all_half and abs(sanity - 1.0) < 1e-9)
    ok = heur_ok and struct_ok
    return {
        "panel": panel_name,
        "n": len(items),
        "cell_counts": dict(cell_counts),
        "heuristics": heuristics,
        "heuristics_in_band": heur_ok,
        "structural": {
            "per_cell_equal": per_cell_equal,
            "eojeol_len_single": eojeol_single,
            "particle_const_도": particle_const,
            "answer_tokens_absent": no_ans_in_surface,
            "negators_absent": no_neg,
            "all_strata_balanced_0.5": all_half,
            "task_conjunction_sanity": round(sanity, 4),
        },
        "structural_ok": struct_ok,
        "balances": balances,
        "fixedL_prefix_curve_reportonly": fixedL_prefix_curve(items),
        "F7_pass": ok,
    }


def _drill_disjointness():
    """Reported PENDING until drill_grid.json exists (SPEC §5/§7)."""
    drill_path = os.path.join(_HERE, "drill_grid.json")
    held = ["어머님", "회장님", "스승님", "박사님", "조카", "후배", "제자", "비서", TAIL_F1]
    if not os.path.exists(drill_path):
        return {"status": "PENDING", "note": "drill_grid.json not built yet", "held_out": held}
    drill = json.load(open(drill_path, encoding="utf-8"))
    surfaces = " ".join(d.get("surface", "") for d in (drill if isinstance(drill, list) else drill.get("items", [])))
    collisions = [x for x in held if x in surfaces]
    return {"status": "PASS" if not collisions else "FAIL", "collisions": collisions, "held_out": held}


def main() -> int:
    h = _harness()
    f2 = build_panel("f2prime", PAIRS_F2, VERBS_F2, TAILS_F2)
    f1 = build_panel("f1prime", PAIRS_F1, VERBS_F1, [TAIL_F1])

    rep_f2 = audit(h, f2, "f2prime")
    rep_f1 = audit(h, f1, "f1prime")

    # union check (§7): template + suffix on f2 ∪ f1 must stay in band
    union = f2 + f1
    union_templ = round(h.template_heuristic_score(union), 4)
    union_suffix = round(h.worst_suffix_leak(union, max_len=10)["worst_suffix_score"], 4)
    union_ok = _band(union_templ) and _band(union_suffix)

    disjoint = _drill_disjointness()

    sigma = round(h.binom_sigma(0.5, len(f2)), 4)
    ok = rep_f2["F7_pass"] and rep_f1["F7_pass"] and union_ok

    print("=" * 74)
    print("H_004 G-0 — HON-BIND F7 panel audit (pre-training don't-run gate)")
    print("=" * 74)
    for r in (rep_f2, rep_f1):
        print(f"\n[{r['panel']}]  n={r['n']}  cells={r['cell_counts']}")
        for k, v in r["heuristics"].items():
            flag = "" if _band(v) else "  <-- OUT OF BAND"
            print(f"  {k:24s}= {v}{flag}")
        s = r["structural"]
        print(f"  structural: cell_equal={s['per_cell_equal']} eojeol_single={s['eojeol_len_single']} "
              f"도_const={s['particle_const_도']} ans_absent={s['answer_tokens_absent']} "
              f"neg_absent={s['negators_absent']} strata_0.5={s['all_strata_balanced_0.5']} "
              f"sanity={s['task_conjunction_sanity']}")
        print(f"  F7 {'PASS' if r['F7_pass'] else 'FAIL'}")
    print(f"\nunion(f2∪f1): template={union_templ} suffix_L10={union_suffix} -> {'ok' if union_ok else 'OUT'}")
    print(f"f2' σ(0.5,192) = {sigma}  (F3 leak floor 0.60 = chance + {round((0.60-0.5)/sigma,2)}σ)")
    print(f"drill disjointness: {disjoint['status']}"
          + (f" (collisions {disjoint['collisions']})" if disjoint.get("collisions") else ""))
    print("\nF7 VERDICT:", "PASS — panel is heuristic-neutral, arms may be built"
          if ok else "FAIL — panel leaks a countable cue, DO NOT TRAIN")

    manifest = {
        "hon_heldout": ["어머님", "회장님", "스승님", "박사님"],
        "plain_heldout": ["조카", "후배", "제자", "비서"],
        "tail_heldout": TAIL_F1,
        "f2_pairs": PAIRS_F2, "f1_pairs": PAIRS_F1,
        "verbs_f2": [v[0] for v in VERBS_F2], "verbs_f1": [v[0] for v in VERBS_F1],
        "tails_f2": TAILS_F2,
    }
    out = {"F7_pass": ok, "f2prime": rep_f2, "f1prime": rep_f1,
           "union": {"template": union_templ, "suffix_L10": union_suffix, "ok": union_ok},
           "drill_disjointness": disjoint, "sigma_f2": sigma}
    with open(os.path.join(_HERE, "f7_audit.json"), "w") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    with open(os.path.join(_HERE, "panel_f2prime.json"), "w") as fh:
        json.dump(f2, fh, indent=2, ensure_ascii=False)
    with open(os.path.join(_HERE, "panel_f1prime.json"), "w") as fh:
        json.dump(f1, fh, indent=2, ensure_ascii=False)
    with open(os.path.join(_HERE, "heldout_manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
    # REVIEW_surfaces.tsv for the G-1 native pass (one line per distinct surface)
    seen = {}
    for it in f2 + f1:
        seen.setdefault(it["surface"], it)
    with open(os.path.join(_HERE, "REVIEW_surfaces.tsv"), "w") as fh:
        fh.write("surface\tcell\tgold\tpanel\n")
        for surf, it in seen.items():
            fh.write(f"{surf}\t{it['cell']}\t{it['gold_token']}\t{it['panel']}\n")
    print("\nwrote f7_audit.json · panel_f2prime.json · panel_f1prime.json · "
          "heldout_manifest.json · REVIEW_surfaces.tsv")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
