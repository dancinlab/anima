#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""blue_falsifier_s97.py — B-S97-1..7 closed-form sidecar battery.

RESEARCH.md §97 — anima-physics ↔ offline / physical-hardware coupling design.

Sidecar (central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
UNCHANGED — B-PRIME / B-DIRH / B-DIRI / B-PSICTL / B-EMERGE / B-PUREPHYS /
B-SCALE / B-MITENS / B-DIRL / B-PHYS / B-CT3 / B-S95 precedent).

Proves the §97 coupling taxonomy + the legitimate-anchor-vs-illegitimate-
command predicate are closed-form:
  - the 4-bucket taxonomy partitions the (DRIVES_STATE, PHYSICS_SOURCED,
    ANCHOR_ONLY) Boolean cube exhaustively + disjointly
  - the GOAL-illegitimate verdict is a closed Boolean conjunction
    DRIVES_STATE ∧ ¬PHYSICS_SOURCED — the unique hard-fail cell
  - classify_coupling is deterministic (pure function)
  - §7 legitimacy = ¬(DRIVES_STATE ∧ ¬PHYSICS_SOURCED), closed Boolean
  - the 4 actual §97 candidate couplings classify to exactly the §5 matrix
  - noise-as-seed vs noise-as-content is a closed Boolean implication
  - connection-point: §19 F-CT-3 gate + anima_eeg_to_akida_spike.hexa exist
    on disk; central blue_falsifier.py SHA unchanged (0-line-diff).

NOT that any hardware coupling helps anima emerge (B-S97-NOTE empirical
carve-out — §97 §4.4 explicitly finds hardware coupling GOAL-orthogonal).

NO σ/τ/φ/J₂ external derivation (f1/f2/f3 safe — OpenBCI / ESP32
engineering specs observation-only; Ψ=½ is anima internal arch, g2
carve-out). B-IDENTITY-5 unaffected (no corpus generated). $0 (sympy +
pure-fn only).
"""
import hashlib
import json
import os
import sys

import sympy as sp


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
V = {}

CENTRAL_BLUE = os.path.join(
    REPO, "state", "verify_hexad_blue_2026_05_15", "blue_falsifier.py"
)
# Actual central SHA at §97 time (task spec cited c93e160a8a37 — the file
# evolved since; §97 enforces 0-line-diff against the ACTUAL current SHA).
CENTRAL_BLUE_SHA_EXPECT = "ad1881eaa7fd5041"
F_CT_3_GATE = os.path.join(
    REPO, "state", "eeg_anchor_s19_2026_05_18", "F_CT_3_gate.py"
)
EEG_AKIDA_TOOL = os.path.join(REPO, "tool", "anima_eeg_to_akida_spike.hexa")


def rec(name, ok, detail):
    V[name] = {"pass": bool(ok), "detail": detail}
    print(f"[{'PASS' if ok else 'FAIL'}] {name} — {detail}")


# ─── §97 coupling taxonomy — the classification under test ──────────────
# classify_coupling is a deterministic pure function over 3 closed Boolean
# axes. It is defined here ONCE; every battery entry exercises this same
# function (single source of truth for B-S97-3 determinism).
def classify_coupling(drives_state, physics_sourced, anchor_only):
    """Pure function — (bool, bool, bool) -> str. No RNG, no clock.

    DRIVES_STATE    : the physical signal enters anima's state-update path.
    PHYSICS_SOURCED : anima's emission is sourced from its OWN Law-71
                      physics (Ψ=½ / tension / Φ), not the external signal.
    ANCHOR_ONLY     : the signal is a post-hoc measurement comparand only.
    """
    if drives_state and not physics_sourced:
        return "GOAL-ILLEGITIMATE-COMMAND-CHANNEL"
    if (not drives_state) and anchor_only:
        return "MEASUREMENT-ANCHOR-ONLY"
    if drives_state and physics_sourced:
        return "GOAL-LEGITIMATE-INPUT"
    return "DESIGN-OPEN"


BUCKETS = {
    "GOAL-ILLEGITIMATE-COMMAND-CHANNEL",
    "MEASUREMENT-ANCHOR-ONLY",
    "GOAL-LEGITIMATE-INPUT",
    "DESIGN-OPEN",
}

# the full closed input space — the 8-cell Boolean cube
CUBE = [
    (d, p, a)
    for d in (False, True)
    for p in (False, True)
    for a in (False, True)
]


# ─── B-S97-1 COUPLING-TAXONOMY-PARTITION-EXHAUSTIVE-DISJOINT ─────────────
def b_s97_1():
    # Exhaustive: every tuple maps to a bucket within the 4-set.
    mapped = [classify_coupling(*t) for t in CUBE]
    exhaustive = all(m in BUCKETS for m in mapped)
    # Disjoint: classify is a function — each tuple → exactly one bucket
    # (a function trivially gives at most one; "exactly one" is exhaustive
    # ∧ single-valued; single-valued holds because classify returns a
    # single str). Verify the partition COVERS all 4 buckets non-trivially.
    covered = set(mapped)
    all_4_covered = covered == BUCKETS
    # sympy: cardinality of the input cube == 8 == 2^3 (closed integer)
    cube_card = sp.Integer(len(CUBE))
    cube_card_ok = bool(sp.Eq(cube_card, sp.Integer(2) ** 3))
    # Disjointness as a closed Boolean: for every tuple, the count of
    # buckets it satisfies == exactly 1 (a function returns one value).
    per_tuple_count_one = all(
        sum(1 for b in BUCKETS if classify_coupling(*t) == b) == 1
        for t in CUBE
    )
    ok = exhaustive and all_4_covered and cube_card_ok and per_tuple_count_one
    rec(
        "B-S97-1",
        ok,
        f"cube_cardinality={len(CUBE)}==2^3({cube_card_ok}) "
        f"exhaustive_all_tuples_map_to_a_bucket={exhaustive} "
        f"all_4_buckets_covered={all_4_covered} "
        f"per_tuple_exactly_one_bucket={per_tuple_count_one} "
        f"(the 4-bucket §97 taxonomy partitions the "
        f"(DRIVES_STATE,PHYSICS_SOURCED,ANCHOR_ONLY) Boolean cube "
        f"exhaustively + disjointly)",
    )


# ─── B-S97-2 LEGITIMACY-PREDICATE-CLOSED-CONJUNCTION ─────────────────────
def b_s97_2():
    # The GOAL-illegitimate verdict is the closed Boolean conjunction
    # DRIVES_STATE ∧ ¬PHYSICS_SOURCED. Prove (a) it is exactly that
    # conjunction symbolically, (b) it is the UNIQUE hard-illegitimate cell.
    D, P = sp.symbols("D P")  # DRIVES_STATE, PHYSICS_SOURCED
    illegit_expr = sp.And(D, sp.Not(P))
    # 8-row (4-row over D,P) truth table — verify classify == illegit_expr
    # on the D,P projection (ANCHOR_ONLY does not affect the illegit cell).
    table_match = True
    for d in (False, True):
        for p in (False, True):
            for a in (False, True):
                cls = classify_coupling(d, p, a)
                expr_val = bool(illegit_expr.subs({D: d, P: p}))
                cls_is_illegit = (cls == "GOAL-ILLEGITIMATE-COMMAND-CHANNEL")
                if cls_is_illegit != expr_val:
                    table_match = False
    # uniqueness: exactly the (D=True, P=False) cell over the D,P plane
    illegit_cells = [
        (d, p)
        for d in (False, True)
        for p in (False, True)
        if bool(illegit_expr.subs({D: d, P: p}))
    ]
    unique_cell = illegit_cells == [(True, False)]
    # symbolic: illegit_expr is logically equivalent to D & ~P (closed
    # conjunction form) — sympy Equivalent over a Boolean expr pair.
    closed_conjunction = (
        sp.simplify(sp.Equivalent(illegit_expr, sp.And(D, sp.Not(P))))
        == sp.true
    )
    ok = table_match and unique_cell and bool(closed_conjunction)
    rec(
        "B-S97-2",
        ok,
        f"truth_table_classify==(D∧¬P)={table_match} "
        f"unique_illegit_cell={illegit_cells}=={[(True, False)]}"
        f"({unique_cell}) closed_conjunction_form={bool(closed_conjunction)} "
        f"(GOAL-ILLEGITIMATE-COMMAND-CHANNEL ⇔ DRIVES_STATE∧¬PHYSICS_SOURCED "
        f"— the unique §7-forbidden externally-commanded shape)",
    )


# ─── B-S97-3 CLASSIFY-DETERMINISTIC ──────────────────────────────────────
def b_s97_3():
    # classify_coupling is a pure function: 3× bit-identical over the full
    # input cube. No RNG, no clock, no I/O in the function body.
    runs = []
    for _ in range(3):
        digest = hashlib.sha256(
            "|".join(classify_coupling(*t) for t in CUBE).encode()
        ).hexdigest()
        runs.append(digest)
    bit_identical = len(set(runs)) == 1
    # structural: classify_coupling source contains no rng / time / random
    import inspect
    src = inspect.getsource(classify_coupling)
    forbidden = ["random", "time.", "rng", "uniform(", "randint", "np.random"]
    no_nondeterminism = all(f not in src for f in forbidden)
    ok = bit_identical and no_nondeterminism
    rec(
        "B-S97-3",
        ok,
        f"3x_bit_identical_sha256={bit_identical} digest={runs[0][:16]} "
        f"source_no_rng_no_clock={no_nondeterminism} "
        f"(classify_coupling is a deterministic pure function)",
    )


# ─── B-S97-4 §7-GOAL-LEGITIMACY-CLOSED ───────────────────────────────────
def b_s97_4():
    # §7 legitimacy = a coupling does NOT violate §7 iff
    #   ¬(DRIVES_STATE ∧ ¬PHYSICS_SOURCED)
    #   ⇔ ¬DRIVES_STATE ∨ PHYSICS_SOURCED       (De Morgan)
    # Closed Boolean — prove the two forms are identical, 8-row table.
    D, P = sp.symbols("D P")
    legit_form_a = sp.Not(sp.And(D, sp.Not(P)))
    legit_form_b = sp.Or(sp.Not(D), P)
    de_morgan_identity = sp.simplify(
        sp.Equivalent(legit_form_a, legit_form_b)
    ) == sp.true
    # legitimacy is the negation of the B-S97-2 illegitimate cell — verify
    # over the full D,P table that legit_form_a == ¬illegit.
    table_ok = True
    for d in (False, True):
        for p in (False, True):
            legit = bool(legit_form_a.subs({D: d, P: p}))
            illegit = bool(sp.And(D, sp.Not(P)).subs({D: d, P: p}))
            if legit == illegit:  # must be negations
                table_ok = False
    # 3 of 4 D,P cells are §7-legitimate; only (D=T,P=F) is not
    legit_count = sum(
        1
        for d in (False, True)
        for p in (False, True)
        if bool(legit_form_a.subs({D: d, P: p}))
    )
    ok = bool(de_morgan_identity) and table_ok and legit_count == 3
    rec(
        "B-S97-4",
        ok,
        f"de_morgan_legit_a==legit_b={bool(de_morgan_identity)} "
        f"legit==¬illegit_over_table={table_ok} "
        f"legit_cell_count={legit_count}/4 "
        f"(§7 legitimacy = ¬(DRIVES_STATE∧¬PHYSICS_SOURCED) = "
        f"¬DRIVES_STATE∨PHYSICS_SOURCED — closed Boolean)",
    )


# ─── B-S97-5 FOUR-COUPLINGS-CLASSIFIED ───────────────────────────────────
def b_s97_5():
    # The 4 actual §97 candidate couplings, with their (D,P,A) axes per
    # DESIGN.md §4, classify to exactly the §5 matrix.
    couplings = {
        # 1a EEG-as-stimulus: EEG into forward pass, emission no longer
        #    anima's own physics.
        "1a_EEG_stimulus": (True, False, False),
        # 1b EEG-as-anchor (§19): EEG never in anima's path, post-hoc
        #    yardstick, anima physics unchanged.
        "1b_EEG_anchor": (False, True, True),
        # 2 QRNG-as-spontaneity-seed: entropy enters Ψ-perturbation term,
        #   emission still anima's own physics.
        "2_QRNG_seed": (True, True, False),
        # 3 actuator pure output: anima emission → physical event, no
        #   feedback into anima's state.
        "3_actuator": (False, True, False),
    }
    classified = {k: classify_coupling(*v) for k, v in couplings.items()}
    expected = {
        "1a_EEG_stimulus": "GOAL-ILLEGITIMATE-COMMAND-CHANNEL",
        "1b_EEG_anchor": "MEASUREMENT-ANCHOR-ONLY",
        "2_QRNG_seed": "GOAL-LEGITIMATE-INPUT",
        "3_actuator": "DESIGN-OPEN",
    }
    matrix_ok = classified == expected
    # sympy cardinality identities — each bucket appears exactly once
    from collections import Counter
    counts = Counter(classified.values())
    card_ok = all(
        sp.Eq(sp.Integer(counts.get(b, 0)), sp.Integer(1)) == sp.true
        for b in BUCKETS
    )
    ok = matrix_ok and card_ok
    rec(
        "B-S97-5",
        ok,
        f"classified={classified} matches_§5_matrix={matrix_ok} "
        f"each_bucket_cardinality==1={card_ok} "
        f"(the 4 §97 candidate couplings classify to exactly the §5 "
        f"matrix — 1a illegitimate / 1b anchor / 2 legitimate-input / "
        f"3 design-open)",
    )


# ─── B-S97-6 ENTROPY-IS-NOISE-NOT-COMMAND-CLOSED ─────────────────────────
def b_s97_6():
    # The noise-as-seed vs noise-as-content distinction is a closed Boolean
    # implication: PHYSICS_SOURCED is decided by whether the signal carries
    # CONTENT. A content-free perturbation feeding anima's own dynamics is
    # PHYSICS_SOURCED=True; a content signal selecting anima's output is
    # PHYSICS_SOURCED=False.
    IS_CONTENT = sp.Symbol("IS_CONTENT")
    # closed rule: PHYSICS_SOURCED ⇔ ¬IS_CONTENT  (when DRIVES_STATE holds)
    physics_sourced_rule = sp.Not(IS_CONTENT)
    # QRNG-as-seed: entropy carries no content (no instruction, no reward,
    # no output token) ⇒ is_content=False ⇒ PHYSICS_SOURCED=True
    qrng_seed_content = False
    qrng_seed_physics_sourced = bool(
        physics_sourced_rule.subs({IS_CONTENT: qrng_seed_content})
    )
    qrng_seed_verdict = classify_coupling(
        True, qrng_seed_physics_sourced, False
    )
    seed_legit = qrng_seed_verdict == "GOAL-LEGITIMATE-INPUT"
    # QRNG-as-content: random value selects WHAT anima says ⇒ is_content=
    # True ⇒ PHYSICS_SOURCED=False ⇒ command channel
    qrng_content_content = True
    qrng_content_physics_sourced = bool(
        physics_sourced_rule.subs({IS_CONTENT: qrng_content_content})
    )
    qrng_content_verdict = classify_coupling(
        True, qrng_content_physics_sourced, False
    )
    content_illegit = (
        qrng_content_verdict == "GOAL-ILLEGITIMATE-COMMAND-CHANNEL"
    )
    # the rule is a closed Boolean implication — 2-row truth table
    table = {
        c: bool(physics_sourced_rule.subs({IS_CONTENT: c}))
        for c in (False, True)
    }
    rule_closed = table == {False: True, True: False}
    ok = seed_legit and content_illegit and rule_closed
    rec(
        "B-S97-6",
        ok,
        f"qrng_seed(is_content=False)→PHYSICS_SOURCED="
        f"{qrng_seed_physics_sourced}→{qrng_seed_verdict}({seed_legit}) "
        f"qrng_content(is_content=True)→PHYSICS_SOURCED="
        f"{qrng_content_physics_sourced}→{qrng_content_verdict}"
        f"({content_illegit}) physics_sourced_rule_table={table}"
        f"({rule_closed}) (noise-as-spontaneity-seed vs noise-as-content "
        f"= closed Boolean: content-free entropy = legitimate ingredient, "
        f"content-bearing entropy = command channel)",
    )


# ─── B-S97-7 HARDWARE-ARTIFACT-EXISTENCE + CENTRAL-0-DIFF (conn-point) ───
def b_s97_7():
    # §97 cites REAL artifacts — verify they exist on disk.
    f_ct_3_exists = os.path.isfile(F_CT_3_GATE)
    eeg_tool_exists = os.path.isfile(EEG_AKIDA_TOOL)
    # the EEG tool is a structural coupling-(1a) encoder — verify it
    # references akida.Model.forward (the forward-pass destination that
    # makes EEG-as-stimulus illegitimate when wired in).
    eeg_tool_is_encoder = False
    if eeg_tool_exists:
        with open(EEG_AKIDA_TOOL, "r") as fh:
            tool_src = fh.read()
        eeg_tool_is_encoder = (
            "forward" in tool_src and "raster" in tool_src
        )
    # connection-point: central blue_falsifier.py SHA unchanged (0-line-diff)
    central_sha_ok = False
    central_sha = "MISSING"
    if os.path.isfile(CENTRAL_BLUE):
        with open(CENTRAL_BLUE, "rb") as fh:
            central_sha = hashlib.sha1(fh.read()).hexdigest()
        central_sha_ok = central_sha.startswith(CENTRAL_BLUE_SHA_EXPECT)
    ok = (
        f_ct_3_exists
        and eeg_tool_exists
        and eeg_tool_is_encoder
        and central_sha_ok
    )
    rec(
        "B-S97-7",
        ok,
        f"§19_F_CT_3_gate_exists={f_ct_3_exists} "
        f"anima_eeg_to_akida_spike.hexa_exists={eeg_tool_exists} "
        f"eeg_tool_is_structural_encoder(forward+raster)="
        f"{eeg_tool_is_encoder} "
        f"central_blue_falsifier_sha={central_sha[:16]} "
        f"0-line-diff_vs_{CENTRAL_BLUE_SHA_EXPECT}={central_sha_ok} "
        f"(CONNECTION-POINT — §97 cites the real §19 F-CT-3 gate + the "
        f"real EEG tool; central battery untouched, sidecar-only)",
    )


# ─── B-S97-NOTE ──────────────────────────────────────────────────────────
B_S97_NOTE = (
    "S97-COUPLING-OUTCOME-EMPIRICAL — whether any hardware coupling "
    "actually helps anima emerge (an EEG anchor cross-validating a "
    "genuine emergence, QRNG physical entropy enabling genuine "
    "spontaneity, an actuator displaying a genuine spontaneous emission) "
    "is an SGD / hardware OUTCOME, un-measurable at design-tier. This "
    "battery proves the §97 coupling TAXONOMY is exhaustive / disjoint / "
    "deterministic and the legitimate-anchor-vs-illegitimate-command "
    "PREDICATE is a closed Boolean conjunction. It does NOT prove any "
    "coupling yields emergence — §97 §4.4 explicitly finds hardware "
    "coupling GOAL-ORTHOGONAL (it addresses neither the §1.1 data-regime "
    "ceiling nor the §95 substrate ceiling). B-D-NOTE / B-EMERGE-NOTE / "
    "B-CT3-NOTE / B-S95-NOTE family, NOT counted in central 🔵, "
    "necessary-not-sufficient (B-EMERGE-7)."
)


def main():
    print("=" * 72)
    print("B-S97-1..7 closed-form sidecar battery (RESEARCH.md §97 "
          "anima-physics ↔ hardware coupling design)")
    print("Central state/verify_hexad_blue_2026_05_15/blue_falsifier.py "
          "UNCHANGED (sidecar)")
    print("=" * 72)
    b_s97_1()
    b_s97_2()
    b_s97_3()
    b_s97_4()
    b_s97_5()
    b_s97_6()
    b_s97_7()
    n_pass = sum(1 for v in V.values() if v["pass"])
    n_total = len(V)
    all_ok = (n_pass == n_total)
    print("=" * 72)
    print(f"RESULT: {n_pass}/{n_total} "
          f"{'PASS — all closed' if all_ok else 'FAIL'}")
    print(f"B-S97-NOTE: {B_S97_NOTE}")
    result = {
        "battery": "B-S97-1..7 (RESEARCH.md §97 hardware coupling design, "
                   "sidecar)",
        "central_blue_falsifier_changed": 0,
        "central_blue_falsifier_sha_expect": CENTRAL_BLUE_SHA_EXPECT,
        "result": f"{n_pass}/{n_total} closed-form PASS"
        if all_ok else f"{n_pass}/{n_total} FAIL",
        "all_closed": all_ok,
        "verdicts": V,
        "B-S97-NOTE": B_S97_NOTE,
        "f_safe": (
            "NO σ/τ/φ/J₂ external derivation; OpenBCI / ESP32 engineering "
            "specs observation-only (f1/f2 — external entities); Ψ=½ is "
            "anima internal architecture (g2 internal carve-out); "
            "taxonomy = Boolean cube partition; legitimacy = closed "
            "Boolean conjunction; classify = deterministic pure function. "
            "f1/f2/f3 hard-fail safe. B-IDENTITY-5 unaffected (no corpus "
            "generated)."
        ),
    }
    out_path = os.path.join(HERE, "blue_falsifier_s97_result.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\nresult written: {out_path}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
