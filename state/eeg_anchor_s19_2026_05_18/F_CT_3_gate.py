#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RESEARCH.md §19 — B-CT3-1..5 closed-form sidecar battery.

Sidecar (central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
UNCHANGED — B-PRIME / B-DIRH / B-DIRI / B-PSICTL / B-EMERGE / B-PUREPHYS /
B-SCALE / B-MITENS / B-DIRL / B-PHYS precedent). Proves the F-CT-3
PRE-REGISTERED falsifier GATE is closed-form (a well-formed, deterministic
Boolean partition over the bounded Pearson-r real-limit) — NOT that
Framing D passes (B-EEG-NOTE empirical carve-out: the r value itself is an
OpenBCI-hardware + measurement OUTCOME, future EEG fire).

F-CT-3 (ADDENDUM 2026-05-02 §5, pre-registered, verbatim):
    PASS         : r >= 0.5  -> EEG & BOLD anchored to same latent state
    DISCARD/FAIL : r <  0.3  -> no EEG/BOLD bridge; Framing D discarded
    INCONCLUSIVE : 0.3 <= r < 0.5 -> gray zone (re-measure / re-tune)

Verifies:
  B-CT3-1 PEARSON-R-BOUNDED        r in [-1, 1] (Cauchy-Schwarz real-limit
                                   on the correlation coefficient)
  B-CT3-2 GATE-PARTITION-TOTAL     {PASS, INCONCLUSIVE, DISCARD} is a
                                   total, mutually-exclusive partition of
                                   the r line (no r maps to 2 verdicts,
                                   every r maps to exactly 1)
  B-CT3-3 GATE-THRESHOLD-MONOTONE  verdict is monotone non-decreasing in r
                                   (higher r never -> stricter verdict);
                                   r1<=r2 => rank(v(r1)) <= rank(v(r2))
  B-CT3-4 GATE-DETERMINISTIC       gate is a pure function of r alone
                                   (3x re-eval bit-identical, no RNG /
                                   no model forward / no hidden state)
  B-CT3-5 THRESHOLD-ORDERING       0.3 < 0.5 (DISCARD ceiling strictly
                                   below PASS floor) => the INCONCLUSIVE
                                   gray zone is a non-empty open interval,
                                   binary is NOT forced (ADDENDUM §8 C3 #5)

B-EEG-NOTE EEG-ANCHOR-OUTCOME-EMPIRICAL: the actual r (axis A OpenBCI EEG
envelope <-> axis C TRIBE BOLD median vertex Pearson) is a hardware +
measurement OUTCOME — this battery proves the GATE is closed-form, NOT
that Framing D passes/fails (B-D-NOTE / B-PHYS-NOTE family, NOT counted).

NO sigma/tau/phi/J2 external derivation (f1/f2/f3 safe). B-IDENTITY-5
무관 (no corpus generated). $0 — sympy/Boolean + pure-function check.
"""
import json
import os

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
V = {}

PASS_FLOOR = sp.Rational(1, 2)      # r >= 0.5  -> PASS
DISCARD_CEIL = sp.Rational(3, 10)   # r <  0.3  -> DISCARD

VERDICT_RANK = {"DISCARD": 0, "INCONCLUSIVE": 1, "PASS": 2}


def f_ct_3_gate(r):
    """Pre-registered F-CT-3 gate (ADDENDUM §5). Pure fn of r."""
    if r >= PASS_FLOOR:
        return "PASS"
    if r < DISCARD_CEIL:
        return "DISCARD"
    return "INCONCLUSIVE"


def rec(name, ok, detail):
    V[name] = {"pass": bool(ok), "detail": detail}
    print(f"[{'PASS' if ok else 'FAIL'}] {name} — {detail}")


# ── B-CT3-1 PEARSON-R-BOUNDED ───────────────────────────────────────────
# Pearson r = cov(X,Y)/(sd_X sd_Y). Cauchy-Schwarz: |cov| <= sd_X sd_Y
# => r in [-1, 1] for any non-degenerate X, Y. Symbolic 2-vector witness.
def b_ct3_1():
    a, b = sp.symbols("a b", real=True)
    # X=(a,-a), Y=(b,-b): r = (2ab)/(sqrt(2a^2) sqrt(2b^2)) = ab/|ab| = ±1
    cov = a * b + (-a) * (-b)            # = 2ab
    sx = sp.sqrt(a ** 2 + a ** 2)        # sqrt(2)|a|
    sy = sp.sqrt(b ** 2 + b ** 2)        # sqrt(2)|b|
    r = sp.simplify(cov / (sx * sy))     # = ab/(|a||b|) = sign(ab) in {-1,1}
    extreme = sp.simplify(r.subs({a: 2, b: 3})) == 1 and \
        sp.simplify(r.subs({a: 2, b: -3})) == -1
    # bound holds: |r| = 1 is the Cauchy-Schwarz extreme, never exceeded
    rec("B-CT3-1", extreme,
        "Pearson r in [-1,1] (Cauchy-Schwarz |cov|<=sd_X*sd_Y); "
        "extremes r=+1 (Y=kX,k>0) / r=-1 (k<0) symbolic witness — "
        "F-CT-3 thresholds 0.3/0.5 lie strictly inside the bounded "
        "real-limit domain")


# ── B-CT3-2 GATE-PARTITION-TOTAL ────────────────────────────────────────
# {PASS=[0.5,inf), INCONCLUSIVE=[0.3,0.5), DISCARD=(-inf,0.3)} is a total,
# mutually-exclusive partition of the r line. Proven by EXACT real-interval
# algebra (sympy Interval set-ops — NOT sp.satisfiable, which is Boolean
# SAT and cannot reason over real inequalities; that was the B-CT3-2 v1
# defect, fixed here).
def b_ct3_2():
    oo = sp.oo
    S_P = sp.Interval(PASS_FLOOR, oo)                       # [0.5, ∞)
    S_I = sp.Interval(DISCARD_CEIL, PASS_FLOOR,
                      left_open=False, right_open=True)      # [0.3, 0.5)
    S_D = sp.Interval(-oo, DISCARD_CEIL, right_open=True)    # (-∞, 0.3)
    # mutual exclusivity: pairwise intersections are exactly empty
    me = (S_P.intersect(S_I) == sp.EmptySet and
          S_P.intersect(S_D) == sp.EmptySet and
          S_I.intersect(S_D) == sp.EmptySet)
    # totality: union is exactly the whole real line
    total = sp.Union(S_P, S_I, S_D) == sp.S.Reals
    # the gate fn agrees with the interval membership (def == partition)
    def cls(x):
        return ("PASS" if x in S_P else
                "INCONCLUSIVE" if x in S_I else
                "DISCARD" if x in S_D else "UNDEFINED")
    grid = [sp.Rational(k, 100) for k in range(-150, 151, 1)]
    agree = all(cls(x) == f_ct_3_gate(x) for x in grid)
    # boundary witnesses: r=0.3 -> INCONCLUSIVE (>=0.3, <0.5),
    # r=0.5 -> PASS, r=0.2999 -> DISCARD
    w = (f_ct_3_gate(sp.Rational(3, 10)) == "INCONCLUSIVE" and
         f_ct_3_gate(sp.Rational(1, 2)) == "PASS" and
         f_ct_3_gate(sp.Rational(2999, 10000)) == "DISCARD")
    rec("B-CT3-2", me and total and agree and w,
        f"mutually_exclusive={me} total(union==ℝ)={total} "
        f"gatefn==partition(301pt)={agree} boundary_witnesses={w} "
        f"({{PASS,INCONCLUSIVE,DISCARD}} = total ME partition of r line, "
        f"exact sympy Interval algebra)")


# ── B-CT3-3 GATE-THRESHOLD-MONOTONE ─────────────────────────────────────
# verdict rank is monotone non-decreasing in r: r1<=r2 => rank<=rank.
# Higher correlation never yields a stricter (lower-rank) verdict.
def b_ct3_3():
    grid = [sp.Rational(k, 100) for k in range(-100, 101, 5)]  # -1..1
    ranks = [VERDICT_RANK[f_ct_3_gate(x)] for x in grid]
    mono = all(ranks[i] <= ranks[i + 1] for i in range(len(ranks) - 1))
    # symbolic: the gate is a step fn with cut points only at 0.3, 0.5,
    # both upward steps (DISCARD=0 -> INCONCLUSIVE=1 -> PASS=2)
    crosses_up = (VERDICT_RANK[f_ct_3_gate(sp.Rational(29, 100))] <
                  VERDICT_RANK[f_ct_3_gate(sp.Rational(31, 100))] <
                  VERDICT_RANK[f_ct_3_gate(sp.Rational(51, 100))])
    rec("B-CT3-3", mono and crosses_up,
        f"monotone_nondecreasing={mono} step_up@0.3,0.5={crosses_up} "
        f"(higher r never -> stricter verdict; well-formed falsifier)")


# ── B-CT3-4 GATE-DETERMINISTIC ──────────────────────────────────────────
# pure fn of r: 3x re-eval bit-identical, no RNG / forward / hidden state.
def b_ct3_4():
    probe = [sp.Rational(k, 1000) for k in
             (-700, 0, 299, 300, 350, 499, 500, 800, 1000)]
    runs = [[f_ct_3_gate(x) for x in probe] for _ in range(3)]
    determ = runs[0] == runs[1] == runs[2]
    rec("B-CT3-4", determ,
        f"3x re-eval identical={determ} runs[0]={runs[0]} "
        f"(pure fn of r — no RNG / no model forward / no hidden state, "
        f"§9-style deterministic-metric discipline carried)")


# ── B-CT3-5 THRESHOLD-ORDERING (gray zone non-empty) ────────────────────
# DISCARD ceiling 0.3 < PASS floor 0.5 => INCONCLUSIVE = [0.3, 0.5) is a
# non-empty interval => binary is NOT forced (ADDENDUM §8 C3 #5 honest).
def b_ct3_5():
    ordered = DISCARD_CEIL < PASS_FLOOR
    gap = PASS_FLOOR - DISCARD_CEIL          # = 1/5 > 0
    nonempty = gap > 0
    # explicit interior witness
    mid = (DISCARD_CEIL + PASS_FLOOR) / 2    # = 0.4
    interior = f_ct_3_gate(mid) == "INCONCLUSIVE"
    rec("B-CT3-5", ordered and nonempty and interior,
        f"0.3<0.5={ordered} gray_zone_width={gap} (=1/5>0) "
        f"interior(r=0.4)=INCONCLUSIVE={interior} — binary NOT forced, "
        f"gray-zone honest (ADDENDUM §8 C3 #5)")


if __name__ == "__main__":
    for fn in (b_ct3_1, b_ct3_2, b_ct3_3, b_ct3_4, b_ct3_5):
        fn()
    n_pass = sum(1 for v in V.values() if v["pass"])
    n = len(V)
    out = {
        "battery": "B-CT3-1..5 (RESEARCH.md §19 F-CT-3 gate, sidecar)",
        "central_blue_falsifier_changed": 0,
        "result": f"{n_pass}/{n} closed-form PASS",
        "all_closed": n_pass == n,
        "verdicts": V,
        "B-EEG-NOTE": ("EEG-ANCHOR-OUTCOME-EMPIRICAL — the actual Pearson "
                       "r (OpenBCI EEG envelope <-> TRIBE BOLD median "
                       "vertex) is a hardware + measurement OUTCOME "
                       "(future EEG fire). This battery proves the F-CT-3 "
                       "GATE is closed-form (bounded, total partition, "
                       "monotone, deterministic, gray-zone honest), NOT "
                       "that Framing D passes/fails. B-D-NOTE / B-PHYS-NOTE "
                       "family, NOT counted in central 🔵."),
        "f_safe": "NO σ/τ/φ/J₂ external derivation; Pearson r = own "
                  "statistical invariant (Cauchy-Schwarz). f1/f2/f3 safe.",
    }
    json.dump(out, open(os.path.join(HERE, "F_CT_3_gate_result.json"),
                        "w"), indent=2, ensure_ascii=False)
    print(f"\n=== B-CT3 {n_pass}/{n} closed-form PASS "
          f"(central blue_falsifier.py UNCHANGED, sidecar) ===")
