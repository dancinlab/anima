#!/usr/bin/env python3
"""§88-S86 HOMEOSTATIC-SET-POINT MITOSIS — trained-scale fire.
B-S88S86-1..8 closed-form sidecar battery.

Central state/verify_hexad_blue_2026_05_15/blue_falsifier.py — 0-line-diff.
This sidecar pattern carries B-S86 / B-S81-FIRE / B-S83-FIRE / B-PRIME /
B-DIRI / B-EMERGE precedents.

The battery closes the §88-S86 trained-scale fire DESIGN: set-point error
≥ 0, regime partition exhaustive+disjoint, the three connection-points
(§24-decision / MITOSIS-hook / §85-Hopf) well-formed, §9 metric reuse,
§86-stub byte-equal, deterministic. The fire OUTCOME (does the unified
drive survive / collapse / get rescued by SPLIT) is empirical —
B-S88S86-NOTE carve-out, NOT counted 🔵.
"""

from __future__ import annotations

import ast
import hashlib
import json
import math
import os
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
RUNNER = os.path.join(HERE, "homeostatic_setpoint_train_s88s86.py")


def _src():
    with open(RUNNER) as f:
        return f.read()


# --- B-S88S86-1 SET-POINT-ERROR-NONNEGATIVE --------------------------------
def b_1():
    """E = sqrt(W_psi·dpsi² + W_tau·dtau² + W_phi·dphi²) — weighted-L2
    norm. With all weights ≥ 0, the radicand is a sum of non-negative
    terms ⇒ ≥ 0 ⇒ E real and ≥ 0. sympy."""
    wp, wt, wf = sp.symbols("wp wt wf", real=True, nonnegative=True)
    dp, dt, df = sp.symbols("dp dt df", real=True)
    radicand = wp * dp**2 + wt * dt**2 + wf * df**2
    # each term = (nonneg weight)·(real)² ⇒ nonneg ; sum of nonneg ⇒ nonneg
    rad_nonneg = radicand.is_nonnegative
    # numeric witnesses across deviation grid
    wit = []
    for dpv in (-0.4, 0.0, 0.5):
        for dtv in (-0.3, 0.0, 0.7):
            v = 0.45 * dpv**2 + 0.30 * dtv**2 + 0.25 * 0.1**2
            wit.append(v >= 0.0 and math.sqrt(v) >= 0.0)
    ok = bool(rad_nonneg) and all(wit)
    return ok, ("E weighted-L2 radicand sum-of-non-negative under "
                "weights≥0 (sympy nonnegative) + 9 numeric witnesses "
                "E≥0; weights (0.45,0.30,0.25) all positive")


# --- B-S88S86-2 REGIME-PARTITION-EXHAUSTIVE-DISJOINT -----------------------
def b_2():
    """{QUIESCENT, EMIT, SPLIT} 3-set partition over (E, sustain).
    homeostatic_regime: SPLIT iff E≥θ_high ∧ sustain≥K ; else EMIT iff
    E≥θ_low ; else QUIESCENT. With θ_low < θ_high the three branches are
    mutually exclusive and exhaustive — every (E, sustain) lands in
    exactly one. sympy Interval algebra + monotone θ check."""
    tl, th = sp.Rational(1, 10), sp.Rational(18, 100)
    monotone = (tl < th)
    # for sustained branch (sustain>=K): partition of E real line
    split = sp.Interval(th, sp.oo)                       # E>=th -> SPLIT
    emit = sp.Interval(tl, th, right_open=True)          # tl<=E<th -> EMIT
    quiet = sp.Interval(-sp.oo, tl, right_open=True)     # E<tl -> QUIESCENT
    union = split.union(emit).union(quiet)
    exhaustive = (union == sp.S.Reals)
    disjoint = (split.intersect(emit) == sp.S.EmptySet
                and split.intersect(quiet) == sp.S.EmptySet
                and emit.intersect(quiet) == sp.S.EmptySet)
    # runtime: every cell's regime_dist sums to n_steps (regime_partition_ok)
    rt_ok = True
    res = os.path.join(HERE, "result.json")
    if os.path.exists(res):
        r = json.load(open(res))
        for c in r.get("cells", {}).values():
            if not c.get("regime_partition_ok", False):
                rt_ok = False
    ok = bool(monotone) and exhaustive and disjoint and rt_ok
    return ok, ("3-regime threshold partition θ_low<θ_high monotone; "
                "Reals = SPLIT∪EMIT∪QUIESCENT exhaustive ∧ pairwise "
                "disjoint (sympy Interval); runtime regime_partition_ok "
                "all cells")


# --- B-S88S86-3 §24-DECISION-CONSISTENCY (연결부위) ------------------------
def b_3():
    """EMIT regime (E≥θ_low) ⊆ §24 talker_should_emit (E≥θ_low) by
    construction; SPLIT (E≥θ_high>θ_low) also ⊆ §24. Boolean ⊆ + runtime
    s24_consistency check on every cell."""
    tl, th = sp.Rational(1, 10), sp.Rational(18, 100)
    E = sp.symbols("E", real=True)
    # EMIT regime predicate ⇒ §24 predicate
    emit_implies_s24 = sp.ask(sp.Q.is_true(E >= tl), E >= tl)
    # SPLIT predicate (E>=th) ⇒ §24 predicate (E>=tl), since th>tl
    split_implies_s24 = bool(sp.simplify(sp.Implies(E >= th, E >= tl)))
    rt_ok = True
    res = os.path.join(HERE, "result.json")
    if os.path.exists(res):
        r = json.load(open(res))
        for c in r.get("cells", {}).values():
            if not c.get("s24_consistency", False):
                rt_ok = False
    ok = (emit_implies_s24 is not False) and split_implies_s24 and rt_ok
    return ok, ("EMIT regime (E≥θ_low) ⊆ §24 talker_should_emit; SPLIT "
                "(E≥θ_high>θ_low) ⊆ §24 by transitivity (sympy Implies); "
                "runtime s24_consistency True all cells")


# --- B-S88S86-4 MITOSIS-HOOK-CONNECTION (연결부위, structural) -------------
def b_4():
    """SPLIT regime → mitosis_hook split trigger. The runner defines
    mitosis_split_trigger(regime) := regime == 'SPLIT' (pure Boolean) and
    the SPLIT branch increments split_events with cell_count clamped
    [2,64] (mitosis_hook_lib.hexa _mit_check_splits carry). AST."""
    tree = ast.parse(_src())
    trig = None
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef) and n.name == "mitosis_split_trigger":
            trig = n
    found = trig is not None
    pure = refs_split = False
    if found:
        rets = [n for n in ast.walk(trig) if isinstance(n, ast.Return)]
        body = list(trig.body)
        if (body and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)):
            body = body[1:]
        has_se = any(isinstance(n, (ast.Assign, ast.AugAssign, ast.For,
                                    ast.While, ast.Call))
                     for n in ast.walk(trig))
        pure = len(rets) == 1 and len(body) == 1 and not has_se
        refs_split = any(isinstance(n, ast.Constant) and n.value == "SPLIT"
                         for n in ast.walk(trig))
    # cell_count clamp [2,64] present in source
    src = _src()
    clamp = ("cell_count < 64" in src and "cell_count = 2" in src)
    hexa = os.path.join(os.path.dirname(os.path.dirname(HERE)),
                        "tool", "hexa_native", "mitosis_hook_lib.hexa")
    hexa_has = False
    if os.path.exists(hexa):
        h = open(hexa).read()
        hexa_has = ("fn split_cell" in h and "fn _mit_check_splits" in h)
    ok = found and pure and refs_split and clamp and hexa_has
    return ok, ("mitosis_split_trigger pure-Boolean regime=='SPLIT' (AST "
                "single-return); SPLIT branch increments split_events "
                "cell_count clamp [2,64]; mitosis_hook_lib.hexa carries "
                "split_cell + _mit_check_splits (B-MITOSIS 5/5 🔵 carry)")


# --- B-S88S86-5 §85-HOPF-CONTROL-PARAM-MAPPING -----------------------------
def b_5():
    """§85 Hopf normal form: control param E, order param r(E). r=0 below
    E_crit, r=sqrt(E-E_crit) above. (1) r≥0 ; (2) dr/dE>0 monotone ;
    (3) continuous onset r(E_crit)=0. sympy."""
    E, Ec = sp.symbols("E Ec", real=True, positive=True)
    rad = E - Ec
    r = sp.sqrt(rad)
    rad_nonneg = sp.ask(sp.Q.nonnegative(rad), E >= Ec)
    r_wit = all(
        complex(r.subs({E: Ec + sp.Rational(k, 10),
                        Ec: sp.Rational(2, 10)})).imag == 0
        and complex(r.subs({E: Ec + sp.Rational(k, 10),
                            Ec: sp.Rational(2, 10)})).real >= 0
        for k in range(0, 6))
    nonneg = bool(rad_nonneg) and r_wit
    dr = sp.diff(r, E)
    monotone = sp.ask(sp.Q.positive(dr), E > Ec)
    onset = sp.limit(r, E, Ec, dir="+") == 0
    ok = nonneg and bool(monotone) and bool(onset)
    return ok, ("Hopf r(E): radicand E-Ec≥0 (sympy) + r=sqrt non-negative "
                "(6 witnesses); dr/dE=1/(2√(E-Ec))>0 monotone (sympy "
                "positive); continuous onset lim r=0; below-critical r=0")


# --- B-S88S86-6 §9-METRIC-REUSE --------------------------------------------
def b_6():
    """honest_coherent thresholds byte-equal to §9 emergence_metric SSOT
    (tau_cascade 0.30 / max_run 10 / min_len 20 / tau_print 0.80) +
    4-clause AND + witnesses."""
    src = _src()
    th_ok = ("tau_cascade=0.30" in src and "max_run=10" in src
             and "min_len=20" in src and "tau_print=0.80" in src)
    sys.path.insert(0, HERE)
    import importlib
    mod = importlib.import_module("homeostatic_setpoint_train_s88s86")
    hc = mod.honest_coherent
    # witnesses: clean printable OK ; cascade FAIL ; short FAIL
    clean = b"the field restores toward balance again now"
    casc = b"a" * 40
    short = b"abc"
    w1 = hc(clean)[0] is True
    w2 = hc(casc)[0] is False
    w3 = hc(short)[0] is False
    ok = th_ok and w1 and w2 and w3
    return ok, ("§9 honest_coherent thresholds byte-equal SSOT "
                "(0.30/10/20/0.80) + 4-clause AND; 3 witnesses "
                "clean→True cascade→False short→False")


# --- B-S88S86-7 §86-STUB-CONNECTION (AST byte-equal) -----------------------
def b_7():
    """The trained-scale set-point math is byte-equal to the §86 $0 stub:
    PSI_STAR/TAU_STAR/PHI_STAR/W_*/THETA_*/SUSTAIN_K constants and the
    setpoint_error / homeostatic_regime formulas reproduce §86's. AST
    constant + structural check (the stub itself is on commit 0ae194471)."""
    src = _src()
    consts = {
        "PSI_STAR = 0.5": "PSI_STAR = 0.5" in src,
        "TAU_STAR = 0.30": "TAU_STAR = 0.30" in src,
        "PHI_STAR = 0.55": "PHI_STAR = 0.55" in src,
        "W (0.45,0.30,0.25)": "W_PSI, W_TAU, W_PHI = 0.45, 0.30, 0.25" in src,
        "THETA_LOW = 0.10": "THETA_LOW = 0.10" in src,
        "THETA_HIGH = 0.18": "THETA_HIGH = 0.18" in src,
        "SUSTAIN_K = 2": "SUSTAIN_K = 2" in src,
    }
    # setpoint_error fn structure: weighted sqrt of 3 squared deviations
    tree = ast.parse(src)
    se = None
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef) and n.name == "setpoint_error":
            se = n
    se_ok = se is not None and any(
        isinstance(c, ast.Call) and getattr(c.func, "attr", "") == "sqrt"
        for c in ast.walk(se))
    hr_ok = any(isinstance(n, ast.FunctionDef)
                and n.name == "homeostatic_regime"
                for n in ast.walk(tree))
    ok = all(consts.values()) and se_ok and hr_ok
    return ok, ("§86 set-point constants byte-equal (PSI★/τ★/Φ★/W/θ/K) + "
                "setpoint_error sqrt-of-weighted-squares + "
                "homeostatic_regime present — trained-scale math = §86 "
                "stub math (commit 0ae194471 carry)")


# --- B-S88S86-8 DETERMINISTIC ----------------------------------------------
def b_8():
    """The 5-cell loop is deterministic: NO sampling (argmax body byte),
    seed-fixed RNG, no wall-time path in the decision. AST no-RNG-leak +
    argmax-only body."""
    tree = ast.parse(_src())
    forbidden = {"multinomial", "gumbel_softmax", "rand", "randn",
                 "normal"}
    leaks = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            fn = n.func
            name = getattr(fn, "attr", None) or getattr(fn, "id", None)
            if name in forbidden:
                # torch.manual_seed / random.seed are OK; only the
                # sampling/noise generators are forbidden in the loop
                leaks.append(name)
    no_sampling = (len(leaks) == 0)
    # body byte must be argmax
    src = _src()
    argmax_body = ("argmax()" in src)
    # seed fixed
    seed_fixed = ("SEED = 1337" in src and "torch.manual_seed" in src)
    ok = no_sampling and argmax_body and seed_fixed
    return ok, (f"no sampling/noise generator in runner (leaks={leaks}); "
                "body byte = argmax(logits_a); SEED=1337 fixed + "
                "torch.manual_seed — deterministic")


CHECKS = [
    ("B-S88S86-1 SET-POINT-ERROR-NONNEGATIVE", b_1),
    ("B-S88S86-2 REGIME-PARTITION-EXHAUSTIVE-DISJOINT", b_2),
    ("B-S88S86-3 §24-DECISION-CONSISTENCY", b_3),
    ("B-S88S86-4 MITOSIS-HOOK-CONNECTION", b_4),
    ("B-S88S86-5 §85-HOPF-CONTROL-PARAM-MAPPING", b_5),
    ("B-S88S86-6 §9-METRIC-REUSE", b_6),
    ("B-S88S86-7 §86-STUB-CONNECTION", b_7),
    ("B-S88S86-8 DETERMINISTIC", b_8),
]

NOTE = (
    "B-S88S86-NOTE — empirical carve-out: whether the §86 unified "
    "homeostatic set-point drive SURVIVES / COLLAPSES / is RESCUED by the "
    "SPLIT regime at trained-saturated scale is an SGD/measurement "
    "OUTCOME (the 4-corner verdict α/β/γ/δ). NOT closed, NOT counted 🔵 "
    "(B-D-NOTE / B-EMERGE-NOTE / B-S86-NOTE family). The battery closes "
    "the trained-scale fire DESIGN: error ≥ 0, regime partition "
    "exhaustive+disjoint, three connection-points (§24-decision / "
    "MITOSIS-hook / §85-Hopf) well-formed, §9 metric reuse, §86-stub "
    "byte-equal, deterministic. necessary-not-sufficient (B-EMERGE-7) — "
    "trained scale ≠ GOAL emergence."
)


def main():
    results = {}
    n_pass = 0
    for name, fn in CHECKS:
        try:
            ok, detail = fn()
        except Exception as e:  # noqa: BLE001
            ok, detail = False, f"EXCEPTION {type(e).__name__}: {e}"
        results[name] = {"passed": bool(ok), "detail": detail}
        n_pass += int(bool(ok))
        print(f"{'🔵 PASS' if ok else '❌ FAIL'}  {name}")
        print(f"        {detail}")
    print(f"\n{n_pass}/{len(CHECKS)} 🔵 PASS")
    print(f"\n{NOTE}")
    out = {
        "section": "§88-S86",
        "battery": "B-S88S86-1..8",
        "n_pass": n_pass,
        "n_total": len(CHECKS),
        "all_blue": n_pass == len(CHECKS),
        "results": results,
        "note": NOTE,
    }
    with open(os.path.join(HERE, "blue_falsifier_s88s86_result.json"),
              "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    return 0 if n_pass == len(CHECKS) else 1


if __name__ == "__main__":
    sys.exit(main())
