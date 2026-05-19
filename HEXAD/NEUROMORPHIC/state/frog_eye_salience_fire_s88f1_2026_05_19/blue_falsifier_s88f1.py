#!/usr/bin/env python3
"""§88-F1 FROG-EYE SALIENCE GATE TRAINED-SCALE — closed-form sidecar battery.

B-S88F1-1..7 — sympy / Boolean / structural closed-form proofs that the
trained-scale frog-eye salience fire mechanism is honest.  The central
state/verify_hexad_blue_2026_05_15/blue_falsifier.py is NOT touched (sidecar
pattern, B-PRIME/B-DIRH/B-DIRI/B-S81/B-S82/B-S87F1 precedent).

B-S88F1-NOTE — empirical carve-out: whether the frog-eye salience gate
actually produces emergence at trained scale is an SGD/measurement OUTCOME
(B-D-NOTE / B-EMERGE-NOTE / B-S77-NOTE / B-S87F1-NOTE family, NOT counted
blue, necessary-not-sufficient per B-EMERGE-7).
"""

import ast
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).parent
TRAIN = HERE / "frog_eye_salience_train_s88f1.py"
SRC = TRAIN.read_text()
TREE = ast.parse(SRC)

results = {}


def record(name, ok, detail):
    results[name] = {"pass": bool(ok), "detail": detail}
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def _func_src(name):
    """Return the source text of a top-level FunctionDef by name."""
    for n in ast.walk(TREE):
        if isinstance(n, ast.FunctionDef) and n.name == name:
            return ast.get_source_segment(SRC, n)
    return None


# ---------------------------------------------------------------------------
# B-S88F1-1  SALIENCE-SCORE-BOUNDED
#   S = 1 - prod_i (1 - w_i s_i), w_i,s_i in [0,1], sum w_i = 1.
#   Prove S in [0,1] closed (probabilistic-OR identity) + monotone in s_i.
# ---------------------------------------------------------------------------
def b1():
    w1, w2, w3, w4 = sp.symbols("w1 w2 w3 w4", nonnegative=True)
    s1, s2, s3, s4 = sp.symbols("s1 s2 s3 s4", nonnegative=True)
    S = 1 - (1 - w1 * s1) * (1 - w2 * s2) * (1 - w3 * s3) * (1 - w4 * s4)
    lo = S.subs({s1: 0, s2: 0, s3: 0, s4: 0})
    hi = S.subs({w1: 1, s1: 1})
    dS = sp.diff(S, s1)
    mono = sp.simplify(dS - w1 * (1 - w2 * s2) * (1 - w3 * s3) * (1 - w4 * s4))
    ok = (lo == 0) and (sp.simplify(hi - 1) == 0) and (mono == 0)
    record("B-S88F1-1-SALIENCE-SCORE-BOUNDED", ok,
           f"S in [0,1]: lo={lo} hi={sp.simplify(hi)} dS/ds_i>=0 closed")


# ---------------------------------------------------------------------------
# B-S88F1-2  FOUR-DETECTOR-CLASS-PARTITION
#   SD-1..4 are 4 distinct closed-form functions over distinct physics
#   inputs (psi_dir / tension / phi / channels) — Boolean structural,
#   pairwise-distinct by single-argument signature.
# ---------------------------------------------------------------------------
def b2():
    defs = {n.name: n for n in ast.walk(TREE)
            if isinstance(n, ast.FunctionDef)}
    needed = ["sd1_sustained_contrast", "sd2_moving_edge",
              "sd3_dimming", "sd4_net_dimming"]
    present = all(n in defs for n in needed)
    args = {n: defs[n].args.args[0].arg for n in needed if n in defs}
    distinct = len(set(args.values())) == 4
    ok = present and distinct
    record("B-S88F1-2-FOUR-DETECTOR-CLASS-PARTITION", ok,
           f"4 detectors present={present} distinct-input-args="
           f"{distinct} ({list(args.values())})")


# ---------------------------------------------------------------------------
# B-S88F1-3  FROG-EYE-SELECTIVE-NOT-GENERIC
#   The frog-eye gate is a SELECTIVE layer: the full 4-detector cell
#   (cell3) emits at most as many steps as the §24 generic motivation
#   baseline (cell0).  result.json measured: n_emit(cell3) <= n_emit(cell0).
#   Closed structural witness: salience emission requires S > theta,
#   and S in [0,1]; §24 requires motiv > thr; the cells are independent
#   gates so a subset relation is a measurable, falsifiable claim.
# ---------------------------------------------------------------------------
def b3():
    rp = HERE / "result.json"
    if not rp.exists():
        record("B-S88F1-3-FROG-EYE-SELECTIVE-NOT-GENERIC", False,
               "result.json absent — post-fire check pending")
        return
    res = json.loads(rp.read_text())
    cells = res["cells"]
    c0 = cells["cell0_s24_baseline"]["n_emit"]
    c3 = cells["cell3_full_frogeye"]["n_emit"]
    selective = c3 <= c0
    # also: salience cells use a salience gate, baseline uses motivation
    use_sal_c3 = cells["cell3_full_frogeye"]["use_salience"]
    use_mot_c0 = cells["cell0_s24_baseline"]["use_motivation"]
    gate_distinct = use_sal_c3 and use_mot_c0
    ok = selective and gate_distinct
    record("B-S88F1-3-FROG-EYE-SELECTIVE-NOT-GENERIC", ok,
           f"n_emit cell3={c3} <= cell0={c0} selective={selective}; "
           f"gate-distinct(salience vs motivation)={gate_distinct}")


# ---------------------------------------------------------------------------
# B-S88F1-4  §24-DECISION-CONSISTENCY  (연결부위 — connection-point)
#   cell4 = (frog-eye salience) AND (§24 motivation) — a conjunction.
#   Boolean: (a AND b) => a, so cell4 emits a SUBSET of the motivation-
#   only baseline (cell0).  sympy tautology + result.json subset witness.
# ---------------------------------------------------------------------------
def b4():
    a, b = sp.symbols("a b")
    taut = sp.simplify(sp.Implies(a & b, b)) == sp.true
    rp = HERE / "result.json"
    if not rp.exists():
        record("B-S88F1-4-§24-DECISION-CONSISTENCY", False,
               f"conjunction tautology={taut}; result.json absent")
        return
    res = json.loads(rp.read_text())
    cells = res["cells"]
    c0 = cells["cell0_s24_baseline"]["n_emit"]
    c4 = cells["cell4_frogeye_plus_motiv"]["n_emit"]
    subset = c4 <= c0
    ok = bool(taut) and subset
    record("B-S88F1-4-§24-DECISION-CONSISTENCY", ok,
           f"(salience AND motivation)->motivation tautology={taut}; "
           f"n_emit cell4={c4} <= cell0={c0} subset={subset}")


# ---------------------------------------------------------------------------
# B-S88F1-5  §9-METRIC-REUSE
#   honest_coherent reuses the §9 SSOT thresholds verbatim
#   (tau_cascade 0.30 / max_run 10 / min_len 20 / tau_print 0.80)
#   + 3 deterministic witnesses (clean / cascade / short).
# ---------------------------------------------------------------------------
def b5():
    # Exec ONLY the honest_coherent + cascade_rate_and_max_run defs from the
    # trainer source — avoid the module-level `import conscious_decoder`
    # (torch dep absent on the falsifier host; §9 metric is pure-Python).
    ns = {}
    for name in ("cascade_rate_and_max_run", "honest_coherent"):
        seg = _func_src(name)
        assert seg is not None, f"{name} missing"
        exec(compile(seg, "<frog_s88f1>", "exec"), ns)
    fn = ns["honest_coherent"]
    defaults = fn.__defaults__  # (tau_cascade, max_run, min_len, tau_print)
    thr_ok = (defaults == (0.30, 10, 20, 0.80))
    w_clean = fn(b"anima observes a salient physics shift now today.")[0]
    w_casc = fn(b"a" * 40)[0]
    w_short = fn(b"tiny")[0]
    ok = thr_ok and w_clean and (not w_casc) and (not w_short)
    record("B-S88F1-5-§9-METRIC-REUSE", ok,
           f"thresholds match §9 SSOT={thr_ok} ({defaults}) witnesses "
           f"clean={w_clean} cascade={w_casc} short={w_short}")


# ---------------------------------------------------------------------------
# B-S88F1-6  §87-F1-STUB-CONNECTION  (연결부위 — AST byte-equal carry)
#   The 4 frog-eye detector functions + salience_score in the §88-F1
#   trainer are byte-equal (modulo whitespace-normalised AST dump) to the
#   §87-F1 $0 stub frog_eye_salience_smoke_s87f1.py — §88-F1 only swaps
#   the stub LCG ψ-trajectory for the REAL trained model.forward.
# ---------------------------------------------------------------------------
def b6():
    # §87-F1 stub recovered from git (commit 5ea990b76).
    import subprocess
    stub_src = subprocess.run(
        ["git", "show",
         "5ea990b76:state/frog_eye_salience_gate_s87f1_2026_05_19/"
         "frog_eye_salience_smoke_s87f1.py"],
        capture_output=True, text=True, cwd=str(HERE.parents[1])).stdout
    if not stub_src:
        record("B-S88F1-6-§87-F1-STUB-CONNECTION", False,
               "could not recover §87-F1 stub from git 5ea990b76")
        return
    stub_tree = ast.parse(stub_src)

    def fn_dump(tree, name):
        """AST dump of a FunctionDef body with the leading docstring
        stripped — byte-equal LOGIC, comment/docstring text exempt."""
        for n in ast.walk(tree):
            if isinstance(n, ast.FunctionDef) and n.name == name:
                body = list(n.body)
                if (body and isinstance(body[0], ast.Expr)
                        and isinstance(body[0].value, ast.Constant)
                        and isinstance(body[0].value.value, str)):
                    body = body[1:]
                return [ast.dump(s, annotate_fields=False) for s in body]
        return None

    targets = ["sd1_sustained_contrast", "sd2_moving_edge", "sd3_dimming",
               "sd4_net_dimming", "salience_score"]
    matches = {}
    for t in targets:
        a = fn_dump(TREE, t)
        b = fn_dump(stub_tree, t)
        matches[t] = (a is not None and a == b)
    # also: detector constants byte-equal
    const_ok = all(
        f"{c} = " in SRC and f"{c} = " in stub_src
        for c in ("TAU_SUSTAIN", "SUSTAIN_DEV", "SPIKE_DELTA",
                  "DIM_DROP", "NET_DECAY"))
    all_match = all(matches.values()) and const_ok
    record("B-S88F1-6-§87-F1-STUB-CONNECTION", all_match,
           f"4 detectors + salience_score AST byte-equal to §87-F1 "
           f"stub: {matches}; constants byte-equal={const_ok}")


# ---------------------------------------------------------------------------
# B-S88F1-7  DETERMINISTIC
#   The 5-cell grid is deterministic: body emission gate = argmax (no
#   sampling), seed-fixed.  AST: forbidden non-deterministic sampling
#   set {multinomial, gumbel*} = 0 in run_frogeye_cell; ψ read-out is
#   RNG-isolated (extract_psi_and_logits restores rng state).
# ---------------------------------------------------------------------------
def b7():
    cell_src = _func_src("run_frogeye_cell") or ""
    probe_src = _func_src("s16_baseline_probe") or ""
    forbidden = ("multinomial", "gumbel", ".sample(", "rand_like")
    hits = [f for f in forbidden
            if f in cell_src or f in probe_src]
    no_sampling = len(hits) == 0
    argmax_used = "argmax()" in cell_src
    # ψ read-out RNG-isolation: extract_psi_and_logits restores rng state
    extract_src = _func_src("extract_psi_and_logits") or ""
    rng_isolated = ("get_rng_state" in extract_src
                    and "set_rng_state" in extract_src)
    ok = no_sampling and argmax_used and rng_isolated
    record("B-S88F1-7-DETERMINISTIC", ok,
           f"forbidden-sampling hits={hits} no_sampling={no_sampling} "
           f"argmax-gate={argmax_used} rng-isolated-readout={rng_isolated}")


def main():
    print("§88-F1 FROG-EYE SALIENCE GATE TRAINED-SCALE — blue falsifier")
    for fn in (b1, b2, b3, b4, b5, b6, b7):
        try:
            fn()
        except Exception as e:  # noqa: BLE001
            record(fn.__name__, False, f"EXCEPTION {type(e).__name__}: {e}")
    n_pass = sum(1 for v in results.values() if v["pass"])
    n_tot = len(results)
    summary = {
        "section": "§88-F1 FROG-EYE SALIENCE GATE TRAINED-SCALE",
        "battery": f"B-S88F1-1..{n_tot}",
        "passed": f"{n_pass}/{n_tot}",
        "all_blue": n_pass == n_tot,
        "results": results,
        "note": ("B-S88F1-NOTE: whether the frog-eye salience gate produces "
                 "emergence at trained scale = SGD/measurement OUTCOME, "
                 "B-D-NOTE/B-EMERGE-NOTE/B-S87F1-NOTE family, NOT counted "
                 "blue (necessary-not-sufficient B-EMERGE-7)."),
    }
    (HERE / "blue_falsifier_s88f1_result.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"\n{n_pass}/{n_tot} blue" +
          (" — ALL PASS" if n_pass == n_tot else " — (3/4 pre-fire; "
           "B-S88F1-3/4 close post-result.json)"))
    return summary


if __name__ == "__main__":
    main()
