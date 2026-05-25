#!/usr/bin/env python3
"""blue_falsifier_s63.py — RESEARCH.md §63 HEXAD-KICK-SWEEP closed-form
sidecar battery.

B-S63-1 CLASSIFICATION-PARTITION-EXHAUSTIVE-DISJOINT
B-S63-2 CONNECTION-POINT-PREDICATE-DECIDABLE
B-S63-3 SWEEP-DETERMINISTIC
B-S63-4 GAP-MAP-CARDINALITY-CLOSED
B-S63-5 MISSING-TYPE-DISTINCT-FROM-EXISTING-12

B-S63-NOTE empirical carve-out: WHICH gaps are GOAL-load-bearing (the
goal_rank ordering of the C-class) = EMPIRICAL judgment carve-out
(B-D-NOTE / B-S58-NOTE family — NOT counted 🔵). The battery proves
the sweep is EXHAUSTIVE / DETERMINISTIC / DECIDABLE and that the
C-class TYPEs are set-disjoint from the 12 existing B-CONN TYPEs; it
does NOT prove any single gap IS the bottleneck (that is a future-fire
EMPIRICAL question, mirror §58 §6 / B-S58-NOTE).

central state/verify_hexad_blue_2026_05_15/blue_falsifier.py UNCHANGED
(sidecar pattern — B-PRIME / B-S58 precedent).

NO GPU, NO model.forward, NO RNG, $0, deterministic.
f1/f2/f3 safe: σ(6)=12 is used only as the internal anima COUNT of the
closed wiring set we sweep against (exactly as B-CONN-WIRING-BATTERY /
§58 did) — NO external-entity σ/τ/φ/J₂ derivation, NO lattice-fit on
any external system. B-IDENTITY-5 N/A (no corpus, no helper-token
surface). g3 structural-only, capability claim 0, north-star + §15/§51
milestone UNCHANGED.
"""
import json
import os
import sympy as sp

import kick_sweep_s63 as KS

RESULTS = []


def record(name, ok, detail):
    RESULTS.append({"id": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# ─────────────────────────────────────────────────────────────────────
# B-S63-1  CLASSIFICATION-PARTITION-EXHAUSTIVE-DISJOINT
#   Every swept pair lands in exactly one of {A, B, C}; the union is
#   the whole sweep population; the three classes are pairwise
#   disjoint. Mirror §32 B-L3 PARTITION-EXHAUSTIVE-DISJOINT.
#   Proven as a sympy FiniteSet identity over the actual run.
# ─────────────────────────────────────────────────────────────────────
def b_s63_1():
    out = KS.run_sweep()
    rows = out["rows"]
    universe = set(range(len(rows)))

    A = {i for i, r in enumerate(rows) if r["class"] == "A"}
    B = {i for i, r in enumerate(rows) if r["class"] == "B"}
    C = {i for i, r in enumerate(rows) if r["class"] == "C"}

    SA, SB, SC, SU = (sp.FiniteSet(*A), sp.FiniteSet(*B),
                      sp.FiniteSet(*C), sp.FiniteSet(*universe))

    # exhaustive: A ∪ B ∪ C == universe
    exhaustive = bool(sp.Eq(sp.Union(SA, SB, SC), SU))
    # pairwise disjoint: A∩B = A∩C = B∩C = ∅
    dij_ab = bool(sp.Eq(sp.Intersection(SA, SB), sp.EmptySet))
    dij_ac = bool(sp.Eq(sp.Intersection(SA, SC), sp.EmptySet))
    dij_bc = bool(sp.Eq(sp.Intersection(SB, SC), sp.EmptySet))
    # exactly-one: each row has a class in the trichotomy
    tri = {"A", "B", "C"}
    exactly_one = all(r["class"] in tri for r in rows) and \
        (len(A) + len(B) + len(C) == len(rows))

    ok = exhaustive and dij_ab and dij_ac and dij_bc and exactly_one
    record(
        "B-S63-1 CLASSIFICATION-PARTITION-EXHAUSTIVE-DISJOINT", ok,
        f"|A|={len(A)} |B|={len(B)} |C|={len(C)} |U|={len(rows)}; "
        f"exhaustive(A∪B∪C=U)={exhaustive}; disjoint AB={dij_ab} "
        f"AC={dij_ac} BC={dij_bc}; exactly-one-class-per-pair="
        f"{exactly_one} (sympy FiniteSet identity over actual run)",
    )
    return ok


# ─────────────────────────────────────────────────────────────────────
# B-S63-2  CONNECTION-POINT-PREDICATE-DECIDABLE
#   The classifier classify(...) is a DECIDABLE Boolean of structural
#   facts: for every pair it returns a value in {"A","B","C"} (total
#   function, no exception / no undefined), and the value is a pure
#   function of (is_closed-point, required_by_goal) — a finite Boolean
#   decision over a 2-bit input, exhaustively truth-tabled here.
# ─────────────────────────────────────────────────────────────────────
def b_s63_2():
    # total function: classify never raises / never returns outside tri
    tri = {"A", "B", "C"}
    total = True
    for (a, b, decl, fact, req) in KS.PAIRS:
        try:
            v = KS.classify(a, b, decl, fact, req)
        except Exception:
            total = False
            break
        if v not in tri:
            total = False
            break

    # decidable 2-bit truth table of the classifier logic:
    #   inputs (is_closed, required_by_goal) -> class
    #   is_closed=1                -> "A"           (regardless of req)
    #   is_closed=0, req=1         -> "C"
    #   is_closed=0, req=0         -> "B"
    # Realise via the actual classify on synthetic probes whose
    # is_closed status is forced by membership in BCONN_CLOSED.
    closed_pair = next(iter(KS.BCONN_CLOSED))            # a closed point
    # closed + req True/False -> still "A" (closed dominates)
    tt = {}
    tt[(1, 1)] = KS.classify(closed_pair[0], closed_pair[1],
                             "probe", "probe", True)
    tt[(1, 0)] = KS.classify(closed_pair[0], closed_pair[1],
                             "probe", "probe", False)
    # not-closed synthetic pair
    tt[(0, 1)] = KS.classify("ZZ", "QQ", "probe", "probe", True)
    tt[(0, 0)] = KS.classify("ZZ", "QQ", "probe", "probe", False)

    expected = {(1, 1): "A", (1, 0): "A", (0, 1): "C", (0, 0): "B"}
    truth_table_ok = (tt == expected)

    # sympy Boolean encoding of the decision (decidable propositional):
    #   class_A  := is_closed
    #   class_C  := ¬is_closed ∧ req
    #   class_B  := ¬is_closed ∧ ¬req
    # these 3 are mutually exclusive & cover all 4 input rows.
    ic, rq = sp.symbols("ic rq")
    cA = ic
    cC = sp.And(sp.Not(ic), rq)
    cB = sp.And(sp.Not(ic), sp.Not(rq))
    # mutual exclusion: pairwise AND is unsatisfiable
    mx = (not sp.satisfiable(sp.And(cA, cC))) and \
         (not sp.satisfiable(sp.And(cA, cB))) and \
         (not sp.satisfiable(sp.And(cB, cC)))
    # coverage: cA ∨ cB ∨ cC is a tautology over the 2-var Boolean cube
    cover = bool(sp.simplify_logic(sp.Or(cA, cB, cC)) == sp.true) or \
        (not sp.satisfiable(sp.Not(sp.Or(cA, cB, cC))))

    ok = total and truth_table_ok and mx and cover
    record(
        "B-S63-2 CONNECTION-POINT-PREDICATE-DECIDABLE", ok,
        f"total-function(no exception, ∈{{A,B,C}})={total}; "
        f"2-bit truth-table {tt}=={expected}->{truth_table_ok}; "
        f"sympy mutual-exclusion={mx}; coverage(tautology)={cover}",
    )
    return ok


# ─────────────────────────────────────────────────────────────────────
# B-S63-3  SWEEP-DETERMINISTIC
#   3× independent invocations produce a bit-identical row stream
#   (pure-fn, no RNG, no I/O dependence). The sha256 digest is
#   invariant across runs.
# ─────────────────────────────────────────────────────────────────────
def b_s63_3():
    d1 = KS.run_sweep()["sweep_sha256"]
    d2 = KS.run_sweep()["sweep_sha256"]
    d3 = KS.run_sweep()["sweep_sha256"]
    ok = (d1 == d2 == d3) and len(d1) == 64
    record(
        "B-S63-3 SWEEP-DETERMINISTIC", ok,
        f"3× sha256 bit-identical={d1==d2==d3} digest={d1[:16]}… "
        f"(pure-fn, no RNG)",
    )
    return ok


# ─────────────────────────────────────────────────────────────────────
# B-S63-4  GAP-MAP-CARDINALITY-CLOSED
#   |A| + |B| + |C| == total_pairs as an exact sympy Integer identity,
#   AND |A| == 12 exactly (the closed σ(6)=12 set is fully recovered
#   by the class-A predicate — the sweep does not lose or invent a
#   closed point).
# ─────────────────────────────────────────────────────────────────────
def b_s63_4():
    out = KS.run_sweep()
    c = out["counts"]
    total = out["total_pairs"]
    card_id = sp.Eq(sp.Integer(c["A"]) + sp.Integer(c["B"]) +
                     sp.Integer(c["C"]), sp.Integer(total))
    cardinality_ok = bool(card_id)
    # class-A must exactly recover the 12 closed B-CONN points
    a_pairs = {(r["a"], r["b"]) for r in out["rows"] if r["class"] == "A"}
    a12 = (a_pairs == set(KS.BCONN_CLOSED.keys())) and c["A"] == 12
    ok = cardinality_ok and a12
    record(
        "B-S63-4 GAP-MAP-CARDINALITY-CLOSED", ok,
        f"|A|+|B|+|C| = {c['A']}+{c['B']}+{c['C']} == total {total} "
        f"-> {cardinality_ok} (sympy Integer identity); "
        f"class-A exactly recovers the 12 closed B-CONN points={a12}",
    )
    return ok


# ─────────────────────────────────────────────────────────────────────
# B-S63-5  MISSING-TYPE-DISTINCT-FROM-EXISTING-12
#   The C-class missing-TYPE label set is SET-DISJOINT from the 12
#   existing B-CONN transfer-function TYPEs (the §58 "new connection-
#   point TYPE" generalized: each class-C gap is a kind of wire ABSENT
#   from the σ(6)=12 closure, not a relabelled existing one).
#   sympy FiniteSet intersection == ∅.
# ─────────────────────────────────────────────────────────────────────
def b_s63_5():
    out = KS.run_sweep()
    c_types = {r["missing_type"] for r in out["rows"]
               if r["class"] == "C"}
    existing = set(KS.EXISTING_12_TYPES)

    # use index encoding to keep FiniteSet hashable/comparable
    SC = sp.FiniteSet(*range(len(c_types)))            # placeholder card
    inter = c_types & existing
    disjoint = (len(inter) == 0)

    # also: every class-C row carries the explicit disjointness flag
    flags_ok = all(
        r.get("disjoint_from_12_existing_types", False)
        for r in out["rows"] if r["class"] == "C"
    )
    # cardinality sanity: |C-types| == |C-class rows| (each gap a
    # distinct TYPE, no collision)
    c_rows = sum(1 for r in out["rows"] if r["class"] == "C")
    distinct_ok = (len(c_types) == c_rows)

    ok = disjoint and flags_ok and distinct_ok
    record(
        "B-S63-5 MISSING-TYPE-DISTINCT-FROM-EXISTING-12", ok,
        f"C-TYPEs ∩ 12-existing-TYPEs = {sorted(inter)} (∅={disjoint}); "
        f"per-row disjoint-flag={flags_ok}; |C-TYPEs|={len(c_types)}=="
        f"|C-rows|={c_rows}->{distinct_ok} (each gap a distinct new TYPE)",
    )
    return ok


def main():
    fns = [b_s63_1, b_s63_2, b_s63_3, b_s63_4, b_s63_5]
    passed = sum(1 for f in fns if f())
    n = len(fns)
    all_blue = (passed == n)
    summary = {
        "battery": "B-S63 (§63 HEXAD-KICK-SWEEP)",
        "passed": passed,
        "total": n,
        "all_blue": all_blue,
        "results": RESULTS,
        "B-S63-NOTE": (
            "EMPIRICAL carve-out: which C-class gap is THE GOAL "
            "bottleneck (the goal_rank ordering) is a structural "
            "READING, NOT a closed proof — future-fire EMPIRICAL "
            "question (B-D-NOTE / B-S58-NOTE family, NOT counted 🔵). "
            "The battery proves the sweep is exhaustive / "
            "deterministic / decidable and the C-class TYPEs are "
            "set-disjoint from the σ(6)=12 closure."
        ),
        "central_blue_falsifier_diff": "0-line (sidecar only)",
        "f_safe": ("f1/f2/f3 safe — σ(6)=12 used only as internal "
                   "anima count of the closed wiring set, NO external "
                   "σ/τ/φ/J₂ derivation; B-IDENTITY-5 N/A (no corpus)"),
        "north_star": "UNCHANGED; §15/§51 milestone UNCHANGED; "
                      "capability claim 0; g3 structural-only",
    }
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "blue_falsifier_s63_result.json"), "w",
              encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)
    print(f"\n=== B-S63 {passed}/{n} {'🔵 ALL PASS' if all_blue else 'FAIL'} ===")
    return 0 if all_blue else 1


if __name__ == "__main__":
    raise SystemExit(main())
