#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
§108-Q5-reconcile — blue falsifier (sidecar)

Closed-form / Boolean battery for the §108 Q5 A3-axis predicate split.

What this proves:
  - the split predicate's two sub-clauses (A3_genuine_freeze, A3_low_spread)
    are mutually DISJOINT, and together with A3_PASS form an EXHAUSTIVE cover;
  - §107-RETRY's actually-measured (RESP, SPREAD_OK) lands in EXACTLY ONE cell;
  - that cell is A3_low_spread (NOT A3_genuine_freeze, NOT A3_PASS);
  - the §11-B genuine-freeze condition is a DIFFERENT cell from §107-RETRY's;
  - the corrected Q5 tree leaves the §108 fire-decision UNDETERMINED for
    §107-RETRY's cell (a tree-coverage gap), i.e. neither auto-GO nor auto-FALSE.

What this does NOT prove (B-S108Q5-NOTE):
  - that anima emerges / that the §108 fire would succeed or fail.
  - This battery proves the dispatch-LOGIC reconciliation is well-formed;
    the GOAL outcome stays empirical, necessary-not-sufficient (B-EMERGE-7).

NO GPU / NO fire / NO model.forward / $0. Pure Boolean + arithmetic.
central state/verify_hexad_blue_2026_05_15/blue_falsifier.py is 0-line-diff.
"""

import json
import os
import itertools

HERE = os.path.dirname(os.path.abspath(__file__))

# ── §107-RETRY measured A3 fields (the settled measurement — never re-fired) ──
# verbatim from state/dataregime_threshold_fire_s107_2026_05_19/result.json
# block "Q2_A3_physics_responsive_held_out".
S107_PHYSICS_RESPONSIVE = True
S107_PSI_STD_H          = 0.0165725780299372
S107_PSI_SPREAD_AVG_H   = 0.05609576078131795
S107_THRESHOLD_SPREAD   = 0.20
S107_A3_PASS_RECORDED   = False   # result.json Q2_A3...["PASS"]

# τ liveness floor (§17 physics-channel probe — channel_not_collapsed threshold)
TAU_LIVENESS = 1e-4

# ── §11-B PURE-PHYSICS genuine-freeze anchor (cited as its own measurement) ──
# §11-B: no-CE → degenerate; Ψ std = 0; §17 probe: purephysics RESPONSIVE=False.
S11B_PHYSICS_RESPONSIVE = False
S11B_PSI_STD            = 0.0


# ── the split predicate (the §108-Q5-reconcile deliverable) ──────────────────
def a3_genuine_freeze(resp: bool) -> bool:
    """Cell 1: physics channel collapsed. Defined as ¬RESP — see DESIGN §1.1
    (the (RESP=F, SPREAD_OK=T) corner is measurement-unreachable and folds here)."""
    return not resp


def a3_low_spread(resp: bool, spread_ok: bool) -> bool:
    """Cell 2: physics ALIVE but Ψ_dir spread below the 0.20 emergence bar."""
    return resp and (not spread_ok)


def a3_pass(resp: bool, spread_ok: bool) -> bool:
    """Cell 3: physics alive AND spread >= 0.20 (== original conflated A3_PASS)."""
    return resp and spread_ok


def spread_ok(psi_spread_avg: float, threshold: float) -> bool:
    return psi_spread_avg >= threshold


# ── battery ──────────────────────────────────────────────────────────────────
RESULTS = []


def check(name, passed, detail):
    RESULTS.append({"id": name, "PASS": bool(passed), "detail": detail})
    return passed


# B-S108Q5-1 — the three cells PAIRWISE DISJOINT over {T,F}^2.
def b_s108q5_1():
    corners = list(itertools.product([True, False], repeat=2))  # (RESP, SPREAD_OK)
    overlaps = []
    for resp, sok in corners:
        f = a3_genuine_freeze(resp)
        l = a3_low_spread(resp, sok)
        p = a3_pass(resp, sok)
        # count how many cells claim this corner
        n_true = sum([f, l, p])
        if n_true > 1:
            overlaps.append((resp, sok, f, l, p))
    ok = (len(overlaps) == 0)
    return check("B-S108Q5-1-CELLS-PAIRWISE-DISJOINT", ok,
                 f"no (RESP,SPREAD_OK) corner satisfies >1 cell; overlaps={overlaps}")


# B-S108Q5-2 — the three cells EXHAUSTIVE (every corner hits exactly one).
def b_s108q5_2():
    corners = list(itertools.product([True, False], repeat=2))
    bad = []
    for resp, sok in corners:
        n_true = sum([a3_genuine_freeze(resp),
                      a3_low_spread(resp, sok),
                      a3_pass(resp, sok)])
        if n_true != 1:
            bad.append((resp, sok, n_true))
    ok = (len(bad) == 0)
    return check("B-S108Q5-2-CELLS-EXHAUSTIVE-EXACTLY-ONE", ok,
                 f"every one of 4 corners satisfies exactly 1 cell; violations={bad}")


# B-S108Q5-3 — §107-RETRY's measured (RESP, SPREAD_OK) is computed correctly,
#              and the recorded A3_PASS == our derived A3_PASS (consistency).
def b_s108q5_3():
    resp = S107_PHYSICS_RESPONSIVE
    sok = spread_ok(S107_PSI_SPREAD_AVG_H, S107_THRESHOLD_SPREAD)
    derived_pass = a3_pass(resp, sok)
    consistent = (derived_pass == S107_A3_PASS_RECORDED)
    # spread sub-clause: 0.0561 >= 0.20 is False
    sok_correct = (sok is False) and (S107_PSI_SPREAD_AVG_H < S107_THRESHOLD_SPREAD)
    # liveness: Ψ std 0.0166 >> τ=1e-4 ⇒ channel alive ⇒ RESP True is honest
    alive = S107_PSI_STD_H > TAU_LIVENESS
    ok = consistent and sok_correct and alive and (resp is True)
    return check("B-S108Q5-3-S107RETRY-RESP-SPREAD-DERIVED-CONSISTENT", ok,
                 f"RESP={resp} SPREAD_OK={sok} (0.0561<0.20) derived A3_PASS="
                 f"{derived_pass}==recorded {S107_A3_PASS_RECORDED}; "
                 f"alive(std {S107_PSI_STD_H:.4g}>{TAU_LIVENESS})={alive}")


# B-S108Q5-4 — §107-RETRY lands in EXACTLY ONE cell, and that cell is
#              A3_low_spread (not freeze, not pass).
def b_s108q5_4():
    resp = S107_PHYSICS_RESPONSIVE
    sok = spread_ok(S107_PSI_SPREAD_AVG_H, S107_THRESHOLD_SPREAD)
    cells = {
        "A3_genuine_freeze": a3_genuine_freeze(resp),
        "A3_low_spread":     a3_low_spread(resp, sok),
        "A3_pass":           a3_pass(resp, sok),
    }
    n_true = sum(cells.values())
    landed = [k for k, v in cells.items() if v]
    ok = (n_true == 1) and (landed == ["A3_low_spread"])
    return check("B-S108Q5-4-S107RETRY-LANDS-IN-A3-LOW-SPREAD-CELL", ok,
                 f"cells={cells} ⇒ n_true={n_true} landed={landed} "
                 f"(expected exactly ['A3_low_spread'])")


# B-S108Q5-5 — the (RESP=F, SPREAD_OK=T) corner folds into the freeze cell,
#              keeping the partition a TOTAL cover with no phantom 4th cell.
def b_s108q5_5():
    # the four corners and which named cell each maps to
    mapping = {}
    for resp, sok in itertools.product([True, False], repeat=2):
        if a3_genuine_freeze(resp):
            mapping[(resp, sok)] = "A3_genuine_freeze"
        elif a3_low_spread(resp, sok):
            mapping[(resp, sok)] = "A3_low_spread"
        elif a3_pass(resp, sok):
            mapping[(resp, sok)] = "A3_pass"
        else:
            mapping[(resp, sok)] = "UNCOVERED"
    # the (F,T) corner must map to A3_genuine_freeze (folded, per DESIGN §1.1)
    ft_folds = mapping[(False, True)] == "A3_genuine_freeze"
    # no corner uncovered ⇒ total cover, no phantom 4th cell
    no_uncovered = "UNCOVERED" not in mapping.values()
    ok = ft_folds and no_uncovered
    return check("B-S108Q5-5-FT-CORNER-FOLDS-TOTAL-COVER", ok,
                 f"(RESP=F,SPREAD_OK=T)→{mapping[(False,True)]}; "
                 f"corner-map={mapping}; no UNCOVERED corner={no_uncovered}")


# B-S108Q5-6 — §11-B genuine-freeze is a DIFFERENT cell from §107-RETRY:
#              §11-B → A3_genuine_freeze; §107-RETRY → A3_low_spread; disjoint.
def b_s108q5_6():
    # §11-B: RESPONSIVE=False, Ψ std = 0 ⇒ freeze cell
    s11b_resp = S11B_PHYSICS_RESPONSIVE
    s11b_cell_freeze = a3_genuine_freeze(s11b_resp)
    s11b_frozen = (S11B_PSI_STD == 0.0) and (s11b_resp is False)
    # §107-RETRY: RESPONSIVE=True, Ψ std 0.0166 ⇒ low_spread cell
    s107_resp = S107_PHYSICS_RESPONSIVE
    s107_sok = spread_ok(S107_PSI_SPREAD_AVG_H, S107_THRESHOLD_SPREAD)
    s107_cell_lowspread = a3_low_spread(s107_resp, s107_sok)
    s107_not_freeze = not a3_genuine_freeze(s107_resp)
    # the two ckpts occupy different cells; freeze ∩ low_spread = ∅ (B-S108Q5-1)
    different_cell = s11b_cell_freeze and s107_cell_lowspread and s107_not_freeze
    # and they differ measurably on the Ψ-std axis (not a definitional split)
    measurably_apart = abs(S107_PSI_STD_H - S11B_PSI_STD) > TAU_LIVENESS
    ok = s11b_frozen and different_cell and measurably_apart
    return check("B-S108Q5-6-S11B-FREEZE-IS-A-DIFFERENT-CELL", ok,
                 f"§11-B frozen(std=0,RESP=False)={s11b_frozen}→A3_genuine_freeze; "
                 f"§107-RETRY→A3_low_spread, not freeze={s107_not_freeze}; "
                 f"Ψ-std apart by {abs(S107_PSI_STD_H - S11B_PSI_STD):.4g}>{TAU_LIVENESS}")


# B-S108Q5-7 — corrected Q5 tree walk: §107-RETRY's bits dispatch to
#              UNDETERMINED (Sub-case A1 freeze does NOT fire; A2 low_spread
#              fires → fall through; B/C/D/E all gated on A3_PASS==True →
#              none fire). NOT auto-GO, NOT auto-FALSE.
def b_s108q5_7():
    # §107-RETRY measured bits
    THRESHOLD_CROSSED = False
    A1 = False  # routing  r_H 0/16
    A2 = False  # coherence c_H 0/16
    A4 = False  # emit-len-indep r_emit_late 0.0
    resp = S107_PHYSICS_RESPONSIVE
    sok = spread_ok(S107_PSI_SPREAD_AVG_H, S107_THRESHOLD_SPREAD)
    A3_freeze = a3_genuine_freeze(resp)
    A3_low    = a3_low_spread(resp, sok)
    A3_PASS   = a3_pass(resp, sok)

    # corrected Case 2 tree (THRESHOLD_CROSSED == False)
    assert THRESHOLD_CROSSED is False
    # Sub-case A1: genuine freeze → DISPATCH False (substrate pivot)
    subA1_fires = A3_freeze
    # Sub-case A2: low_spread → UNDETERMINED-BY-A3, fall through
    subA2_fires = A3_low
    # Sub-cases B/C/D/E: ALL gated on A3_PASS == True
    bcde_eligible = A3_PASS
    # Sub-case F: A4==False with A1/A2/A3 *mixed* — here A1,A2 fail & A3_PASS F
    # ⇒ NOT "mixed/healthy", F's rationale inapplicable
    a_axes_mixed = not (A1 is False and A2 is False and A3_PASS is False)
    subF_clean_fires = (A4 is False) and a_axes_mixed

    # the corrected outcome:
    if subA1_fires:
        outcome = "DISPATCH_False_substrate_pivot"
    elif subA2_fires and not bcde_eligible and not subF_clean_fires:
        outcome = "UNDETERMINED"
    elif bcde_eligible:
        outcome = "BCDE_capacity_path"
    else:
        outcome = "OTHER"

    # assertions: §107-RETRY ⇒ A1 freeze does NOT fire, A2 fires, BCDE NOT
    # eligible, F NOT clean ⇒ outcome == UNDETERMINED ⇒ neither auto-GO
    # ("True") nor auto-FALSE-by-freeze.
    not_auto_go = (outcome != "BCDE_capacity_path")
    not_auto_substrate = (outcome != "DISPATCH_False_substrate_pivot")
    is_undetermined = (outcome == "UNDETERMINED")
    ok = ((subA1_fires is False) and (subA2_fires is True)
          and (bcde_eligible is False) and (subF_clean_fires is False)
          and is_undetermined and not_auto_go and not_auto_substrate)
    return check("B-S108Q5-7-CORRECTED-TREE-LEAVES-S108-UNDETERMINED", ok,
                 f"A3_freeze={A3_freeze} A3_low={A3_low} A3_PASS={A3_PASS}; "
                 f"subA1_fires={subA1_fires} subA2_fires={subA2_fires} "
                 f"bcde_eligible={bcde_eligible} subF_clean={subF_clean_fires} "
                 f"⇒ outcome={outcome} (not auto-GO={not_auto_go}, "
                 f"not auto-substrate={not_auto_substrate})")


def main():
    b_s108q5_1()
    b_s108q5_2()
    b_s108q5_3()
    b_s108q5_4()
    b_s108q5_5()
    b_s108q5_6()
    b_s108q5_7()

    n_pass = sum(1 for r in RESULTS if r["PASS"])
    n_total = len(RESULTS)
    all_pass = (n_pass == n_total)

    note = ("B-S108Q5-NOTE — this battery proves the §108 Q5 A3-axis predicate "
            "split is well-formed (disjoint + exhaustive cells), that §107-RETRY's "
            "measurement lands in exactly the A3_low_spread cell, that the §11-B "
            "genuine-freeze is a different cell, and that the corrected Q5 tree "
            "leaves the §108 fire-decision UNDETERMINED. It does NOT prove anima "
            "emerges, NOR that the §108 fire would succeed/fail — capability claim "
            "0, GOAL outcome empirical, necessary-not-sufficient (B-EMERGE-7). "
            "design ≠ fire ≠ emergence; WALL-A measured-but-not-crossed carry.")

    out = {
        "section": "§108-Q5-reconcile",
        "date": "2026-05-19",
        "battery": "B-S108Q5-1..7",
        "n_pass": n_pass,
        "n_total": n_total,
        "all_pass": all_pass,
        "verdict": ("ALL 7 🔵 PASS — split predicate disjoint+exhaustive; "
                    "§107-RETRY lands in A3_low_spread; §108 fire-decision "
                    "GENUINELY UNDETERMINED under the corrected tree"
                    if all_pass else "FAIL — see results"),
        "results": RESULTS,
        "B-S108Q5-NOTE": note,
        "central_blue_sha_prefix": "c93e160a8a376a94 (0-line-diff, sidecar-only)",
    }
    with open(os.path.join(HERE, "blue_falsifier_s108q5_result.json"), "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    for r in RESULTS:
        mark = "🔵 PASS" if r["PASS"] else "❌ FAIL"
        print(f"{mark}  {r['id']}")
        print(f"        {r['detail']}")
    print(f"\n{'='*60}")
    print(f"B-S108Q5  {n_pass}/{n_total} {'🔵 ALL PASS' if all_pass else '❌ FAIL'}")
    print(note)
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
