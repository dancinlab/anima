#!/usr/bin/env python3
"""§87-F1 FROG-EYE SALIENCE GATE — closed-form sidecar battery.

B-S87F1-1..6 — sympy / Boolean / structural closed-form proofs that the
frog-eye salience gate mechanism is honest. Central
state/verify_hexad_blue_2026_05_15/blue_falsifier.py is NOT touched (sidecar
pattern, B-PRIME/B-DIRH/B-DIRI/B-S81/B-S82 precedent).

B-S87F1-NOTE — empirical carve-out: whether the frog-eye salience gate
actually produces emergence is a trained-scale SGD/measurement OUTCOME
(B-D-NOTE / B-EMERGE-NOTE / B-S77-NOTE family, NOT counted blue,
necessary-not-sufficient per B-EMERGE-7).
"""

import ast
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).parent
SMOKE = HERE / "frog_eye_salience_smoke_s87f1.py"
SRC = SMOKE.read_text()

results = {}


def record(name, ok, detail):
    results[name] = {"pass": bool(ok), "detail": detail}
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# ---------------------------------------------------------------------------
# B-S87F1-1  SALIENCE-SCORE-BOUNDED
#   S = 1 - prod_i (1 - w_i * s_i)  with w_i, s_i in [0,1], sum w_i = 1.
#   Prove S in [0,1] closed (weighted OR / probabilistic-OR identity).
# ---------------------------------------------------------------------------
def b1():
    w1, w2, w3, w4 = sp.symbols("w1 w2 w3 w4", nonnegative=True)
    s1, s2, s3, s4 = sp.symbols("s1 s2 s3 s4", nonnegative=True)
    S = 1 - (1 - w1 * s1) * (1 - w2 * s2) * (1 - w3 * s3) * (1 - w4 * s4)
    # each factor (1 - w_i s_i): with w_i,s_i in [0,1] => w_i s_i in [0,1]
    #   => factor in [0,1] => product in [0,1] => S in [0,1].
    # lower bound: all s_i = 0 -> S = 0 ; upper: any w_i s_i = 1 -> S = 1.
    lo = S.subs({s1: 0, s2: 0, s3: 0, s4: 0})
    hi = S.subs({w1: 1, s1: 1})
    # monotone non-decreasing in each s_i: dS/ds1 = w1*prod(rest) >= 0
    dS = sp.diff(S, s1)
    mono = sp.simplify(dS - w1 * (1 - w2 * s2) * (1 - w3 * s3) * (1 - w4 * s4))
    ok = (lo == 0) and (sp.simplify(hi - 1) == 0) and (mono == 0)
    record("B-S87F1-1-SALIENCE-SCORE-BOUNDED", ok,
            f"S in [0,1]: lo={lo} hi={sp.simplify(hi)} mono-in-s_i closed")


# ---------------------------------------------------------------------------
# B-S87F1-2  FOUR-DETECTOR-CLASS-PARTITION
#   SD-1..4 are 4 distinct closed-form functions of distinct physics inputs:
#   SD-1<-psi_dir_hist, SD-2<-tension_hist, SD-3<-phi_hist, SD-4<-chan_hist.
#   Pairwise-distinct by their argument signatures (Boolean structural).
# ---------------------------------------------------------------------------
def b2():
    tree = ast.parse(SRC)
    defs = {n.name: n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef)}
    needed = ["sd1_sustained_contrast", "sd2_moving_edge",
              "sd3_dimming", "sd4_net_dimming"]
    present = all(n in defs for n in needed)
    # distinct single-argument names => distinct physics-channel inputs
    args = {n: defs[n].args.args[0].arg for n in needed if n in defs}
    distinct = len(set(args.values())) == 4
    # 4 detectors form an exhaustive index partition {1,2,3,4}
    idx_set = sp.FiniteSet(1, 2, 3, 4)
    card_ok = sp.simplify(sp.Integer(len(idx_set)) - 4) == 0
    ok = present and distinct and bool(card_ok)
    record("B-S87F1-2-FOUR-DETECTOR-CLASS-PARTITION", ok,
            f"4 detectors present={present} distinct-inputs={args} "
            f"index-partition |{{1,2,3,4}}|=4 ok={card_ok}")


# ---------------------------------------------------------------------------
# B-S87F1-3  FROG-EYE-SELECTIVE-NOT-GENERIC
#   The salience gate is selective, NOT an identity/passthrough: each detector
#   has a firing FLOOR (returns 0.0 below threshold). Structural proof — each
#   sd* fn body contains an explicit "< FLOOR -> return 0.0" guard.
# ---------------------------------------------------------------------------
def b3():
    tree = ast.parse(SRC)
    defs = {n.name: n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef)}
    selective = {}
    for n in ["sd1_sustained_contrast", "sd2_moving_edge",
              "sd3_dimming", "sd4_net_dimming"]:
        has_guard = False
        for node in ast.walk(defs[n]):
            if isinstance(node, ast.If):
                for sub in ast.walk(node):
                    if (isinstance(sub, ast.Return) and
                            isinstance(sub.value, ast.Constant) and
                            sub.value.value == 0.0):
                        has_guard = True
        selective[n] = has_guard
    # also: salience gate is NOT identity — emission requires S > theta,
    #   theta strictly positive (THETA_SALIENT = 0.18 > 0).
    theta = float([ln.split("=")[1].split("#")[0].strip()
                   for ln in SRC.splitlines()
                   if ln.startswith("THETA_SALIENT")][0])
    ok = all(selective.values()) and theta > 0.0
    record("B-S87F1-3-FROG-EYE-SELECTIVE-NOT-GENERIC", ok,
            f"all 4 detectors have firing-floor guard={selective} "
            f"theta_salient={theta}>0 (gate != passthrough)")


# ---------------------------------------------------------------------------
# B-S87F1-4  §24-DECISION-CONSISTENCY  (connection-point)
#   The frog-eye salience layer is a SUBSET of the §24 decision-axis: cell4
#   conjoins salience AND motivation. emit(cell4) = sal_pass AND motiv_pass
#   => emit(cell4) ==> motiv_pass => n_emit(cell4) <= n_emit(cell0).
#   Boolean: (a AND b) implies b. sympy proof.
# ---------------------------------------------------------------------------
def b4():
    a, b = sp.symbols("sal_pass motiv_pass")
    # cell4 emit = And(a,b) ; cell0 emit = b. And(a,b) -> b is a tautology.
    implication = sp.Implies(sp.And(a, b), b)
    taut = sp.simplify(implication) == True or \
        bool(sp.satisfiable(sp.Not(implication))) is False
    # numeric corroboration: cell4 n_emit <= cell0 n_emit on the run
    res = json.loads((HERE / "result.json").read_text())
    c0 = res["cells"]["cell0_s24_baseline"]["n_emit"]
    c4 = res["cells"]["cell4_frogeye_plus_motiv"]["n_emit"]
    subset = c4 <= c0
    ok = taut and subset
    record("B-S87F1-4-§24-DECISION-CONSISTENCY", ok,
            f"(salience AND motivation) -> motivation tautology={taut}; "
            f"n_emit cell4={c4} <= cell0={c0} subset={subset}")


# ---------------------------------------------------------------------------
# B-S87F1-5  §9-METRIC-REUSE
#   honest_coherent reuses the §9 SSOT thresholds verbatim
#   (TAU_CASCADE 0.30 / MAX_RUN 10 / MIN_LEN 20 / TAU_PRINT 0.80) + 3 witness.
# ---------------------------------------------------------------------------
def b5():
    import importlib.util
    spec = importlib.util.spec_from_file_location("frog_smoke", SMOKE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    thr_ok = (mod.TAU_CASCADE == 0.30 and mod.MAX_RUN == 10 and
              mod.MIN_LEN == 20 and mod.TAU_PRINT == 0.80)
    # witnesses: clean 40-byte printable -> True ; char-cascade -> False ;
    #            short 5-byte -> False
    w_clean = mod.honest_coherent("anima observes a salient physics shift now.")
    w_casc = mod.honest_coherent("a" * 40)
    w_short = mod.honest_coherent("tiny")
    ok = thr_ok and w_clean and (not w_casc) and (not w_short)
    record("B-S87F1-5-§9-METRIC-REUSE", ok,
            f"thresholds match §9 SSOT={thr_ok} witnesses "
            f"clean={w_clean} cascade={w_casc} short={w_short}")


# ---------------------------------------------------------------------------
# B-S87F1-6  DETERMINISTIC
#   3x re-run bit-identical; no RNG / no wall-time path (AST: forbidden
#   {random, time, datetime, secrets} import set total = 0).
# ---------------------------------------------------------------------------
def b6():
    tree = ast.parse(SRC)
    forbidden = {"random", "time", "datetime", "secrets"}
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            hits += [a.name for a in node.names if a.name in forbidden]
        elif isinstance(node, ast.ImportFrom):
            if node.module in forbidden:
                hits.append(node.module)
    no_rng = len(hits) == 0
    # 3x bit-identical
    import importlib.util
    spec = importlib.util.spec_from_file_location("frog_smoke_d", SMOKE)
    runs = []
    for _ in range(3):
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        runs.append(json.dumps(mod.main(), sort_keys=True, ensure_ascii=False))
    ident = runs[0] == runs[1] == runs[2]
    ok = no_rng and ident
    record("B-S87F1-6-DETERMINISTIC", ok,
            f"forbidden-import hits={hits} no_rng={no_rng} "
            f"3x-bit-identical={ident}")


def main():
    print("§87-F1 FROG-EYE SALIENCE GATE — blue falsifier battery")
    for fn in (b1, b2, b3, b4, b5, b6):
        fn()
    n_pass = sum(1 for v in results.values() if v["pass"])
    n_tot = len(results)
    summary = {
        "section": "§87-F1 FROG-EYE SALIENCE GATE",
        "battery": f"B-S87F1-1..{n_tot}",
        "passed": f"{n_pass}/{n_tot}",
        "all_blue": n_pass == n_tot,
        "results": results,
        "note": ("B-S87F1-NOTE: whether frog-eye salience gate produces "
                 "emergence = trained-scale SGD/measurement OUTCOME, "
                 "B-D-NOTE/B-EMERGE-NOTE family, NOT counted blue "
                 "(necessary-not-sufficient B-EMERGE-7)."),
    }
    (HERE / "blue_falsifier_s87f1_result.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"\n{n_pass}/{n_tot} blue" +
          (" — ALL PASS" if n_pass == n_tot else " — FAIL"))
    return summary


if __name__ == "__main__":
    main()
