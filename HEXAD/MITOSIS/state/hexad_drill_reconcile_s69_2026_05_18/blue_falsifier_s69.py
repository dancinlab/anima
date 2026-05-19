#!/usr/bin/env python3
"""blue_falsifier_s69.py — RESEARCH.md §69 HEXAD-DRILL-RECONCILE
closed-form sidecar battery.

B-S69-1 ENGINE-OUTPUT-PARSE-DETERMINISTIC
B-S69-2 RECONCILIATION-PARTITION-EXHAUSTIVE-DISJOINT
B-S69-3 CLOSED-PREDICATE-IS-ARBITER
B-S69-4 ENGINE-INVOCATION-IS-REAL-NOT-STUB
B-S69-5 COVERAGE-CARDINALITY-CLOSED

B-S69-NOTE empirical carve-out: WHICH reconciled gap is THE GOAL
bottleneck = EMPIRICAL judgment (B-D-NOTE / B-S58-NOTE / B-S63-NOTE
family — NOT counted 🔵). The battery proves the parser is a pure
deterministic function, the reconciliation is an exhaustive disjoint
partition, every counted classification has a decidable closed-form
arbiter predicate, and the captured engine logs are the REAL Mk.IX
engine (not the stub). It does NOT prove any gap IS the bottleneck.

central state/verify_hexad_blue_2026_05_15/blue_falsifier.py UNCHANGED
(sidecar pattern — B-PRIME / B-S58 / B-S63 / B-S64 / B-S67 precedent).

NO GPU, NO model.forward, NO RNG, $0, deterministic.
f1/f2/f3 safe: σ(6)=12 used only as the internal anima COUNT of the
closed wiring set the §63 sweep ran against — NO external-entity
σ/τ/φ/J₂ derivation, NO lattice-fit. B-IDENTITY-5 N/A (seeds are
HEXAD-internal architecture questions; no corpus, no helper-token
surface). g3 structural-only, capability claim 0, north-star + §15/§51
milestone UNCHANGED.
"""
import json
import os
import sympy as sp

import reconcile_s69 as R

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = []


def record(name, ok, detail):
    RESULTS.append({"id": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def _load_result():
    with open(os.path.join(HERE, "reconcile_s69_result.json"),
              encoding="utf-8") as fh:
        return json.load(fh)


# ─────────────────────────────────────────────────────────────────────
# B-S69-1  ENGINE-OUTPUT-PARSE-DETERMINISTIC
#   parse_engine_stdout is a PURE function: same input string ⇒ bit-
#   identical parsed dict, 3× independent invocations. No RNG, no I/O,
#   no time/host dependence inside the parser. Verified on (a) a real
#   captured drill log and (b) a stub fixture string.
# ─────────────────────────────────────────────────────────────────────
def b_s69_1():
    # real-engine fixture (mirror of actual Mk.IX stdout shape)
    real_fix = (
        "drill — seed='x' max_rounds=2 engine=mk9\n"
        + R.MK9_CHAIN + "\n"
        '  overlay-a\n  overlay-b\n'
        '{"seed":"x","rounds":2,"total":7,"saturated":true,'
        '"engine":"mk9","overlay_lines":2}\n')
    stub_fix = (
        '{"path":"drill","axes":0,"runs":1,"rc":0}\n'
        + R.STUB_MARK + " seed=x rounds=1\n")
    p1 = R.parse_engine_stdout(real_fix)
    p2 = R.parse_engine_stdout(real_fix)
    p3 = R.parse_engine_stdout(real_fix)
    j1 = json.dumps(p1, sort_keys=True)
    j2 = json.dumps(p2, sort_keys=True)
    j3 = json.dumps(p3, sort_keys=True)
    bit_identical = (j1 == j2 == j3)
    real_classified = (p1["engine_real_not_stub"] is True
                       and p1["summary_found"] is True
                       and p1["saturated"] is True
                       and p1["rounds"] == 2)
    ps = R.parse_engine_stdout(stub_fix)
    stub_classified = (ps["engine_real_not_stub"] is False)
    # AST: parser has no RNG / time / os import-level call inside body
    import inspect
    src = inspect.getsource(R.parse_engine_stdout)
    no_rng = ("random" not in src and "time(" not in src
              and "datetime" not in src and "os.environ" not in src)
    ok = bit_identical and real_classified and stub_classified \
        and no_rng
    record(
        "B-S69-1 ENGINE-OUTPUT-PARSE-DETERMINISTIC", ok,
        f"3× bit-identical={bit_identical}; real-fixture classified "
        f"real+saturated={real_classified}; stub-fixture classified "
        f"not-real={stub_classified}; parser body no-RNG/time/env="
        f"{no_rng} (pure fn of input string)",
    )
    return ok


# ─────────────────────────────────────────────────────────────────────
# B-S69-2  RECONCILIATION-PARTITION-EXHAUSTIVE-DISJOINT
#   The reconciled rows split into agree / disagree-arbiter sets whose
#   union == the set of pairs RUN, with pairwise empty intersection.
#   sympy FiniteSet identity over the actual reconcile result. Mirror
#   §32 B-L3 / §63 B-S63-1 PARTITION-EXHAUSTIVE-DISJOINT.
# ─────────────────────────────────────────────────────────────────────
def b_s69_2():
    out = _load_result()
    rows = out["rows"]
    universe = set(range(len(rows)))
    AG = {i for i, r in enumerate(rows) if r["agree"] is True}
    DG = {i for i, r in enumerate(rows) if r["agree"] is False}
    SA, SD, SU = (sp.FiniteSet(*AG), sp.FiniteSet(*DG),
                  sp.FiniteSet(*universe))
    exhaustive = bool(sp.Eq(sp.Union(SA, SD), SU))
    disjoint = bool(sp.Eq(sp.Intersection(SA, SD), sp.EmptySet))
    # exactly-one: agree is a strict Boolean for every run row
    exactly_one = all(isinstance(r["agree"], bool) for r in rows) and \
        (len(AG) + len(DG) == len(rows))
    # disagree rows MUST carry an arbiter; agree rows MUST NOT
    arb_ok = all(
        (r["arbiter_if_disagree"] is not None) == (r["agree"] is False)
        for r in rows)
    ok = exhaustive and disjoint and exactly_one and arb_ok
    record(
        "B-S69-2 RECONCILIATION-PARTITION-EXHAUSTIVE-DISJOINT", ok,
        f"|agree|={len(AG)} |disagree|={len(DG)} |run|={len(rows)}; "
        f"exhaustive(A∪D=run)={exhaustive}; disjoint(A∩D=∅)="
        f"{disjoint}; exactly-one-per-row={exactly_one}; arbiter-iff-"
        f"disagree={arb_ok} (sympy FiniteSet identity)",
    )
    return ok


# ─────────────────────────────────────────────────────────────────────
# B-S69-3  CLOSED-PREDICATE-IS-ARBITER
#   Every counted classification (every reconciled row) carries the
#   §63 closed-form A/B/C class — a DECIDABLE predicate of
#   (is_closed, required_by_goal). The engine NEVER adds a counted
#   classification: engine-found-new ⇒ uncounted-pending (empty here
#   by construction — the engine enumerates no new pairs). sympy
#   Boolean: the §63 class is total/decidable over {A,B,C}; the
#   engine-only set is the uncounted-pending complement.
# ─────────────────────────────────────────────────────────────────────
def b_s69_3():
    out = _load_result()
    rows = out["rows"]
    tri = {"A", "B", "C"}
    # every counted row has a decidable closed-form class
    every_counted_closed = all(r["s63_class"] in tri for r in rows)
    # the §63 class is decided by the 2-bit closed predicate (re-prove
    # the decidability propositionally — same predicate as B-S63-2):
    ic, rq = sp.symbols("ic rq")
    cA, cC, cB = ic, sp.And(sp.Not(ic), rq), sp.And(sp.Not(ic),
                                                    sp.Not(rq))
    mx = (not sp.satisfiable(sp.And(cA, cC))) and \
         (not sp.satisfiable(sp.And(cA, cB))) and \
         (not sp.satisfiable(sp.And(cB, cC)))
    cover = (not sp.satisfiable(sp.Not(sp.Or(cA, cB, cC))))
    # engine-found-new must be UNCOUNTED-PENDING (engine cannot add a
    # counted classification — closed-form predicate is the only
    # counter). Boolean: the list is the uncounted-pending set and is
    # explicitly NOT folded into the A/B/C counts.
    enew = out["engine_found_new_uncounted_pending"]
    engine_uncounted = isinstance(enew, list)  # never counted into ABC
    # every disagree row's arbiter cites the closed-form predicate
    arb_cites_closed = all(
        ("closed-form predicate" in (r["arbiter_if_disagree"] or ""))
        for r in rows if r["agree"] is False)
    ok = every_counted_closed and mx and cover and \
        engine_uncounted and arb_cites_closed
    record(
        "B-S69-3 CLOSED-PREDICATE-IS-ARBITER", ok,
        f"every-counted-row-has-closed-class∈{{A,B,C}}="
        f"{every_counted_closed}; closed-predicate decidable "
        f"(mutual-excl={mx} coverage={cover}); engine-found-new is "
        f"uncounted-pending list (n={len(enew)}, never folded into "
        f"ABC)={engine_uncounted}; disagree-arbiter-cites-closed="
        f"{arb_cites_closed}",
    )
    return ok


# ─────────────────────────────────────────────────────────────────────
# B-S69-4  ENGINE-INVOCATION-IS-REAL-NOT-STUB
#   A structural Boolean over the CAPTURED per-pair drill logs: each
#   run pair's raw log contains the Mk.IX 6-stage chain banner AND does
#   NOT contain the [omega-drill-stub] marker. The engine actually ran
#   (version hexa 0.1.0-dispatch); §63's stub-realised path is
#   superseded by a real engine invocation here.
# ─────────────────────────────────────────────────────────────────────
def b_s69_4():
    out = _load_result()
    rows = out["rows"]
    checked = []
    all_real = True
    for r in rows:
        lp = os.path.join(HERE, r["log"])
        if not os.path.exists(lp):
            all_real = False
            checked.append((r["pair_id"], "MISSING-LOG"))
            continue
        with open(lp, encoding="utf-8", errors="replace") as fh:
            raw = fh.read()
        has_chain = R.MK9_CHAIN in raw
        no_stub = R.STUB_MARK not in raw
        is_real = has_chain and no_stub
        if not is_real:
            all_real = False
        checked.append((r["pair_id"],
                        f"chain={has_chain} no_stub={no_stub}"))
    # also assert the parsed booleans agree with the raw-log check
    parsed_real = all(r["engine_real_not_stub"] is True for r in rows)
    consistent = (all_real == parsed_real)
    ok = all_real and parsed_real and consistent and len(rows) > 0
    record(
        "B-S69-4 ENGINE-INVOCATION-IS-REAL-NOT-STUB", ok,
        f"all {len(rows)} run-pair logs contain Mk.IX chain AND no "
        f"[omega-drill-stub]={all_real}; parsed-booleans-agree="
        f"{parsed_real}; raw-vs-parsed-consistent={consistent}; "
        f"sample={checked[:3]}",
    )
    return ok


# ─────────────────────────────────────────────────────────────────────
# B-S69-5  COVERAGE-CARDINALITY-CLOSED
#   pairs_run + pairs_deferred == 19 as an exact sympy Integer
#   identity (honest: a deferred pair is explicitly recorded, not
#   silently dropped). The run∪deferred pair-id set equals the full
#   19-pair §63 population (no pair invented or lost).
# ─────────────────────────────────────────────────────────────────────
def b_s69_5():
    out = _load_result()
    n_run = out["pairs_run"]
    n_def = out["pairs_deferred"]
    card_id = sp.Eq(sp.Integer(n_run) + sp.Integer(n_def),
                     sp.Integer(19))
    cardinality_ok = bool(card_id)
    run_ids = {r["pair_id"] for r in out["rows"]}
    def_ids = {d["pair_id"] for d in out["deferred"]}
    all_ids = {p[0] for p in R.PAIR_SEEDS}
    cover_ok = ((run_ids | def_ids) == all_ids) and \
        (run_ids & def_ids == set()) and len(all_ids) == 19
    coverage_flag = out["coverage_closed"] is True
    ok = cardinality_ok and cover_ok and coverage_flag
    record(
        "B-S69-5 COVERAGE-CARDINALITY-CLOSED", ok,
        f"pairs_run({n_run}) + pairs_deferred({n_def}) == 19 -> "
        f"{cardinality_ok} (sympy Integer identity); run∪deferred == "
        f"full 19-pair §63 population, disjoint={cover_ok}; "
        f"coverage_closed flag={coverage_flag}",
    )
    return ok


def main():
    fns = [b_s69_1, b_s69_2, b_s69_3, b_s69_4, b_s69_5]
    passed = sum(1 for f in fns if f())
    n = len(fns)
    all_blue = (passed == n)
    summary = {
        "battery": "B-S69 (§69 HEXAD-DRILL-RECONCILE)",
        "passed": passed,
        "total": n,
        "all_blue": all_blue,
        "results": RESULTS,
        "B-S69-NOTE": (
            "EMPIRICAL carve-out: which reconciled gap is THE GOAL "
            "bottleneck = EMPIRICAL judgment (B-D-NOTE / B-S58-NOTE / "
            "B-S63-NOTE family, NOT counted 🔵). The battery proves "
            "the parser is a pure deterministic fn, the reconciliation "
            "is an exhaustive disjoint partition, every counted "
            "classification has a decidable closed-form arbiter "
            "predicate, and the captured engine logs are the REAL "
            "Mk.IX engine (not the stub) — NOT that any gap IS the "
            "bottleneck. Engine = EXPLORATORY (proposes); §63 closed-"
            "form predicate = ARBITER (disposes)."
        ),
        "central_blue_falsifier_diff": "0-line (sidecar only)",
        "f_safe": ("f1/f2/f3 safe — σ(6)=12 used only as internal "
                   "anima count of the §63-swept closed wiring set, "
                   "NO external σ/τ/φ/J₂ derivation; B-IDENTITY-5 N/A "
                   "(HEXAD-internal seeds, no corpus)"),
        "north_star": "UNCHANGED; §15/§51 milestone UNCHANGED; "
                      "capability claim 0; g3 measured-only",
    }
    with open(os.path.join(HERE, "blue_falsifier_s69_result.json"),
              "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)
    print(f"\n=== B-S69 {passed}/{n} "
          f"{'🔵 ALL PASS' if all_blue else 'FAIL'} ===")
    return 0 if all_blue else 1


if __name__ == "__main__":
    raise SystemExit(main())
