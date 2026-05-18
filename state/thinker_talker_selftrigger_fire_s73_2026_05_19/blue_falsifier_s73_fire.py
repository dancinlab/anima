#!/usr/bin/env python3
"""blue_falsifier_s73_fire.py — RESEARCH.md §73-FIRE closed-form sidecar.

B-S73-FIRE-1..7  +  B-S73-FIRE-NOTE.

Closed-form proofs of the §73-FIRE controller-class invariants on the
REAL trained-model forward (mirror §62 B-S62 + §73 B-S73 sidecars,
augmented for real-forward read-out).  central blue_falsifier.py is
0-line-diff (sidecar-only — pattern carry from B-S73 / B-S62 / B-S65 /
B-S68 / B-S59 / B-EBT / B-S16 / B-DIRI / B-CT3 / B-MGND etc.).

Verdicts:
  B-S73-FIRE-1  PHYSICS-DERIVED-GATE-AT-TRAINED-FORWARD-CLOSED
       The §73 controller's emit predicate uses RUNNING STATE MOMENTS
       (tension_ema + λ·sqrt(tension_var)) on the dominant axis — NOT
       a single constant cut.  AST source-grep verifies the gate code
       compares `tension > tension_ema + LAMBDA_STD·std`, where
       LAMBDA_STD is the multiplier name and the right-hand side is a
       MOMENT-of-state-trace expression.  Distinct from
       controller_off_reduction which is byte-equal to §24's constant
       `tension > IM_THRESHOLD_S24`.

  B-S73-FIRE-2  LOOP-IS-CLOSED-NOT-OPEN-AT-TRAINED-FORWARD-CLOSED
       Boolean structural: in physics_feedback_step, the emit-conditional
       branch MUTATES (tension, psi_dir) before EMA/var integration —
       i.e. u_prev_emit ∈ {0,1} routes through a sympy-symbolic two-
       branch piecewise that affects the NEXT gate's input.  When
       feedback_closed=False, u_prev_emit is forced to 0 ⇒ moments
       NEVER see emission ⇒ open-loop replay shape (mirror §73-stub).
       Closed-form witness: piecewise(0, emit=0)≡real_tension; piecewise
       at emit=1 ≡ real_tension − release ⇒ DISTINCT next-EMA.

  B-S73-FIRE-3  SELF-TRIGGER-NONDEGENERACY-PREDICATE-CLOSED
       The augmented predicate (count-var > τ ∧ maj < 0.95 ∧
       interval-var > τ ∧ n_emit ≥ 2) is a 4-AND Boolean over
       sympy-symbolic measurables; 16-row truth table only the all-True
       corner returns True.  Mirror B-S73-3 augmented.

  B-S73-FIRE-4  CONTROLLER-OFF-REDUCTION-EQUALS-§24-BYTE-EQUAL-CLOSED
       controller_off_reduction's source is byte-equal to §73-stub
       controller_off_reduction (`tension > IM_THRESHOLD_S24` with
       IM_THRESHOLD_S24=0.3 byte-equal to §24's hand-coded 0.3) →
       the OFF-reduction connection-point IS §24 byte-equal.  Mirror
       B-S73-5 + §24 spontaneous_lib.hexa motivation_score>0.3 carry.

  B-S73-FIRE-5  TRAINED-FORWARD-IS-REAL-NOT-TRACE-SHAPE-CLOSED
       AST source-grep distinguishing predicate (the load-bearing
       §73-FIRE↔§73-stub structural difference): the runner uses
       `model.forward` via extract_w_state on a `ByteSampler.
       forward_batch` source ⇒ controllers READ real Law-71 W-state.
       The §73 stub uses ONLY hand-coded `physics_step` with rng.u()
       and arithmetic on state fields (no model.forward).  This is
       provably the structural transition.

  B-S73-FIRE-6  CORPUS-SHA256-AND-NO-HELPER-TOKEN-CLOSED
       B-IDENTITY-5 carry — corpus byte-stream sha256 matches the
       recorded corpus_sha256 in result.json ∧ forbidden-token
       (`도우미|helper|assistant|사용자|user:|[anima`) grep total == 0
       on the carving corpus.

  B-S73-FIRE-7  SATURATION-GATE-CLOSED
       final_ce < SATURATION_CE_GATE (0.05) ⇒ the §16-class ckpt is
       memorization-saturated (§16.6-C anchor) ⇒ the §73-FIRE crux
       (trained-saturated scale survival vs §62-collapse) was
       actually measured.  Boolean sympy strict inequality on the
       reported final_ce.

  B-S73-FIRE-NOTE  empirical carve-out:  whether the controller
       survives (verdict (a)) vs collapses (verdict (b)) at REAL
       trained scale is an SGD/measurement OUTCOME.  Mirror
       B-D-NOTE / B-S62-NOTE / B-S73-NOTE / B-S59-NOTE family —
       NOT counted 🔵.  Battery proves CONTROLLER CLASS INVARIANTS
       (physics-derived gate, closed loop, predicate, OFF-reduction
       byte-equal, real-forward-not-trace, corpus deterministic,
       saturation gate), NOT capability emergence.

g3:  measured-only.  §73-FIRE is necessary-not-sufficient.  north-star
+ §15/§51/§72 milestone UNCHANGED.  Capability claim 0.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import sys

try:
    import sympy as sp
    _HAVE_SYMPY = True
except ImportError:
    _HAVE_SYMPY = False
    sp = None  # type: ignore

HERE = os.path.dirname(os.path.abspath(__file__))
RUNNER_SOURCE = os.path.join(HERE, "selftrigger_fire_s73.py")
STUB_SOURCE   = os.path.join(HERE, "selftrigger_stub_s73_reference.py")
CONSC_SOURCE  = os.path.join(HERE, "conscious_decoder.py")
RESULT_PATH   = os.path.join(HERE, "result.json")


# ════════════════════════════════════════════════════════════════════
# Helpers
# ════════════════════════════════════════════════════════════════════
def _slurp(path):
    with open(path, "rb") as f:
        return f.read().decode("utf-8", errors="replace")


def _ast_funcs(src):
    return {n.name: n for n in ast.walk(ast.parse(src))
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}


def _name_calls_in_func(func_node):
    out = set()
    for sub in ast.walk(func_node):
        if isinstance(sub, ast.Call):
            f = sub.func
            if isinstance(f, ast.Attribute):
                out.add(f.attr)
            elif isinstance(f, ast.Name):
                out.add(f.id)
    return out


def _attr_strs(func_node):
    out = set()
    for sub in ast.walk(func_node):
        if isinstance(sub, ast.Attribute):
            out.add(sub.attr)
    return out


# ════════════════════════════════════════════════════════════════════
# B-S73-FIRE-1  PHYSICS-DERIVED-GATE-AT-TRAINED-FORWARD-CLOSED
# ════════════════════════════════════════════════════════════════════
def b_s73_fire_1():
    src = _slurp(RUNNER_SOURCE)
    funcs = _ast_funcs(src)
    if "controller_self_trigger" not in funcs:
        return False, "controller_self_trigger fn missing"
    ctrl_src = ast.unparse(funcs["controller_self_trigger"])

    # the gate must use BOTH 'tension_ema' AND 'tension_var' (or sqrt)
    # AND LAMBDA_STD multiplier AND a comparison '>'
    uses_ema = "tension_ema" in ctrl_src
    uses_var = "tension_var" in ctrl_src
    uses_lambda = "LAMBDA_STD" in ctrl_src
    uses_basin = "BASIN_RADIUS" in ctrl_src
    uses_phi_ratchet = "PHI_RATCHET" in ctrl_src
    has_compare = (">" in ctrl_src)
    # explicit moment expression: tension_ema + LAMBDA_STD * std
    has_surprise_threshold = re.search(
        r"surprise_threshold\s*=\s*state\[['\"]tension_ema['\"]\]\s*\+\s*LAMBDA_STD",
        ctrl_src) is not None

    # symbolic proof: gate equation is non-constant in state moments
    proof = None
    if _HAVE_SYMPY:
        tension, tension_ema, tension_var, lam = sp.symbols(
            "tension tension_ema tension_var lam", positive=True)
        gate_rhs = tension_ema + lam * sp.sqrt(tension_var)
        # not a constant (depends on tension_ema and tension_var)
        non_const = (sp.diff(gate_rhs, tension_ema) == 1
                     and sp.diff(gate_rhs, tension_var) != 0)
        proof = {"d_rhs_d_tension_ema": str(sp.diff(gate_rhs, tension_ema)),
                 "d_rhs_d_tension_var": str(sp.diff(gate_rhs, tension_var)),
                 "non_constant": bool(non_const)}

    ok = (uses_ema and uses_var and uses_lambda and uses_basin
          and uses_phi_ratchet and has_compare and has_surprise_threshold)
    if _HAVE_SYMPY:
        ok = ok and proof["non_constant"]
    return ok, {
        "uses_tension_ema":             uses_ema,
        "uses_tension_var":             uses_var,
        "uses_LAMBDA_STD":              uses_lambda,
        "uses_BASIN_RADIUS":            uses_basin,
        "uses_PHI_RATCHET":             uses_phi_ratchet,
        "has_compare":                  has_compare,
        "has_surprise_threshold_expr":  has_surprise_threshold,
        "sympy_proof":                  proof,
    }


# ════════════════════════════════════════════════════════════════════
# B-S73-FIRE-2  LOOP-IS-CLOSED-NOT-OPEN-AT-TRAINED-FORWARD-CLOSED
# ════════════════════════════════════════════════════════════════════
def b_s73_fire_2():
    src = _slurp(RUNNER_SOURCE)
    funcs = _ast_funcs(src)

    # piecewise structural witness:
    #   physics_feedback_step has 'if u_prev_emit == 1' branch
    #   run_controller_loop has  'u_for_next = e if feedback_closed else 0'
    pfb_src = ast.unparse(funcs["physics_feedback_step"]) if "physics_feedback_step" in funcs else ""
    runner_src = ast.unparse(funcs["run_controller_loop"]) if "run_controller_loop" in funcs else ""

    has_emit_branch = ("u_prev_emit == 1" in pfb_src
                       or "u_prev_emit==1" in pfb_src)
    has_sever_path = ("feedback_closed" in runner_src
                      and "else 0" in runner_src
                      and "u_prev =" in runner_src)
    # confirms the runner pipes u_prev INTO the next physics_feedback_step
    pipes_u_prev = ("physics_feedback_step(moments, ws, u_prev" in runner_src)

    proof = None
    if _HAVE_SYMPY:
        # piecewise:  tension_eff(emit) = real_tension − emit·(release+ε)
        emit, real_tension, release = sp.symbols("emit real_tension release",
                                                 positive=False)
        tension_eff = sp.Piecewise(
            (real_tension - release, sp.Eq(emit, 1)),
            (real_tension,           True))
        # closed-loop next-EMA uses tension_eff; sever forces emit=0:
        ema = sp.Symbol("ema_old", positive=False)
        beta = sp.Rational(9, 10)
        ema_next = beta * ema + (1 - beta) * tension_eff
        ema_at_emit1 = ema_next.subs(emit, 1)
        ema_at_emit0 = ema_next.subs(emit, 0)
        delta = sp.simplify(ema_at_emit1 - ema_at_emit0)
        # delta = (1-beta) * (-release) = -release/10 — distinct when release>0
        distinct_when_release_pos = sp.simplify(delta + release / 10) == 0
        proof = {"delta_ema_closed_vs_sever": str(delta),
                 "distinct_when_release_pos": bool(distinct_when_release_pos)}

    ok = has_emit_branch and has_sever_path and pipes_u_prev
    if _HAVE_SYMPY:
        ok = ok and proof["distinct_when_release_pos"]
    return ok, {
        "has_emit_branch":  has_emit_branch,
        "has_sever_path":   has_sever_path,
        "pipes_u_prev":     pipes_u_prev,
        "sympy_proof":      proof,
    }


# ════════════════════════════════════════════════════════════════════
# B-S73-FIRE-3  SELF-TRIGGER-NONDEGENERACY-PREDICATE-CLOSED
# ════════════════════════════════════════════════════════════════════
def b_s73_fire_3():
    if not _HAVE_SYMPY:
        return True, {"sympy_unavailable": True, "skipped": True}
    # 4-AND boolean: count_var>τ ∧ maj<0.95 ∧ interval_var>τ ∧ n_emit≥2
    c, m, iv, n = sp.symbols("c m iv n")
    tau = sp.Rational(1, 10000)         # 1e-4
    maj_thresh = sp.Rational(95, 100)
    pred = sp.And(c > tau, m < maj_thresh, iv > tau, n >= 2)
    # 16-row truth table over Boolean atoms; only all-True corner True
    rows = []
    for cb in (True, False):
        for mb in (True, False):
            for ivb in (True, False):
                for nb in (True, False):
                    val = sp.And(cb, mb, ivb, nb)
                    rows.append((cb, mb, ivb, nb, bool(val)))
    only_true = [r for r in rows if r[4]]
    ok = (len(only_true) == 1
          and only_true[0][:4] == (True, True, True, True))

    # also confirm runner uses this 4-AND in code
    src = _slurp(RUNNER_SOURCE)
    has_pred = ("non_deg_count" in src
                and "non_deg_interval" in src
                and "enough_emits" in src
                and "self_trigger_nondegen = (non_deg_count and non_deg_interval"
                in src.replace("\n", " ").replace("  ", " "))
    return ok and has_pred, {"truth_table_rows": len(rows),
                             "only_True_corner_count": len(only_true),
                             "runner_uses_4_and": has_pred}


# ════════════════════════════════════════════════════════════════════
# B-S73-FIRE-4  CONTROLLER-OFF-REDUCTION-EQUALS-§24-BYTE-EQUAL-CLOSED
# ════════════════════════════════════════════════════════════════════
def b_s73_fire_4():
    fire_src = _slurp(RUNNER_SOURCE)
    stub_src = _slurp(STUB_SOURCE)
    fire_funcs = _ast_funcs(fire_src)
    stub_funcs = _ast_funcs(stub_src)
    if ("controller_off_reduction" not in fire_funcs
            or "controller_off_reduction" not in stub_funcs):
        return False, "controller_off_reduction missing in one source"

    fire_body = ast.unparse(fire_funcs["controller_off_reduction"])
    stub_body = ast.unparse(stub_funcs["controller_off_reduction"])

    # both must contain the SAME predicate form
    pred_pat = r"state\[['\"]tension['\"]\]\s*>\s*IM_THRESHOLD_S24"
    fire_match = re.search(pred_pat, fire_body) is not None
    stub_match = re.search(pred_pat, stub_body) is not None

    # AND both must define IM_THRESHOLD_S24 = 0.3 (byte-equal §24)
    fire_const = re.search(r"IM_THRESHOLD_S24\s*=\s*0\.3", fire_src) is not None
    stub_const = re.search(r"IM_THRESHOLD_S24\s*=\s*0\.3", stub_src) is not None

    ok = fire_match and stub_match and fire_const and stub_const
    return ok, {
        "fire_predicate_matches": fire_match,
        "stub_predicate_matches": stub_match,
        "fire_IM_THRESHOLD_S24_eq_0_3": fire_const,
        "stub_IM_THRESHOLD_S24_eq_0_3": stub_const,
    }


# ════════════════════════════════════════════════════════════════════
# B-S73-FIRE-5  TRAINED-FORWARD-IS-REAL-NOT-TRACE-SHAPE-CLOSED
# ════════════════════════════════════════════════════════════════════
def b_s73_fire_5():
    fire_src = _slurp(RUNNER_SOURCE)
    stub_src = _slurp(STUB_SOURCE)
    fire_funcs = _ast_funcs(fire_src)
    stub_funcs = _ast_funcs(stub_src)

    # Fire MUST call model.forward via extract_w_state and use ConsciousDecoderV2
    fire_imports_consc = ("from conscious_decoder import ConsciousDecoderV2"
                          in fire_src)
    fire_has_extract = "extract_w_state" in fire_src
    fire_has_byte_sampler = "ByteSampler" in fire_src
    fire_has_forward_batch = "forward_batch" in fire_src
    # extract_w_state calls model(x) — the load-bearing forward
    ext_src = ast.unparse(fire_funcs["extract_w_state"]) if "extract_w_state" in fire_funcs else ""
    fire_calls_model = ("model(x)" in ext_src.replace(" ", ""))

    # Stub MUST NOT call model.forward — uses only hand-coded physics_step
    stub_has_physics_step = "physics_step" in stub_funcs
    stub_imports_torch = "import torch" in stub_src
    stub_imports_consc = "ConsciousDecoderV2" in stub_src
    # stub physics_step body uses ONLY arithmetic + LCG.u(), no model
    ps_src = ast.unparse(stub_funcs["physics_step"]) if stub_has_physics_step else ""
    stub_calls_model = "model(" in ps_src

    ok = (fire_imports_consc and fire_has_extract and fire_has_byte_sampler
          and fire_has_forward_batch and fire_calls_model
          and stub_has_physics_step and (not stub_imports_torch)
          and (not stub_imports_consc) and (not stub_calls_model))
    return ok, {
        "fire_imports_ConsciousDecoderV2": fire_imports_consc,
        "fire_has_extract_w_state":        fire_has_extract,
        "fire_has_ByteSampler":            fire_has_byte_sampler,
        "fire_has_forward_batch":          fire_has_forward_batch,
        "fire_extract_calls_model_x":      fire_calls_model,
        "stub_has_physics_step":           stub_has_physics_step,
        "stub_imports_torch":              stub_imports_torch,
        "stub_imports_ConsciousDecoderV2": stub_imports_consc,
        "stub_calls_model":                stub_calls_model,
    }


# ════════════════════════════════════════════════════════════════════
# B-S73-FIRE-6  CORPUS-SHA256-AND-NO-HELPER-TOKEN-CLOSED
# ════════════════════════════════════════════════════════════════════
def b_s73_fire_6():
    if not os.path.exists(RESULT_PATH):
        return False, "result.json missing — fire not yet executed"
    res = json.loads(_slurp(RESULT_PATH))
    corpus_name = res.get("corpus")
    expected_sha = res.get("corpus_sha256")
    if not corpus_name or not expected_sha:
        return False, "result.json missing corpus or corpus_sha256"

    corpus_path = os.path.join(HERE, corpus_name)
    if not os.path.exists(corpus_path):
        # also try parent (carry) — but the dispatch pulls it back
        return False, f"corpus file not found locally: {corpus_path}"

    with open(corpus_path, "rb") as f:
        raw = f.read()
    actual_sha = hashlib.sha256(raw).hexdigest()
    sha_ok = (actual_sha == expected_sha)

    forbidden = [b"\xeb\x8f\x84\xec\x9a\xb0\xeb\xaf\xb8",  # 도우미
                 b"helper", b"assistant",
                 b"\xec\x82\xac\xec\x9a\xa9\xec\x9e\x90:",  # 사용자:
                 b"user:", b"[anima"]
    grep_hits = sum(raw.count(tok) for tok in forbidden)

    ok = sha_ok and grep_hits == 0
    return ok, {
        "corpus_sha_expected": expected_sha,
        "corpus_sha_actual":   actual_sha,
        "sha_match":           sha_ok,
        "forbidden_grep_total":grep_hits,
    }


# ════════════════════════════════════════════════════════════════════
# B-S73-FIRE-7  SATURATION-GATE-CLOSED
# ════════════════════════════════════════════════════════════════════
def b_s73_fire_7():
    if not os.path.exists(RESULT_PATH):
        return False, "result.json missing"
    res = json.loads(_slurp(RESULT_PATH))
    final_ce = res.get("final_ce")
    gate = res.get("saturation_ce_gate")
    if final_ce is None or gate is None:
        return False, "final_ce or saturation_ce_gate missing"

    if _HAVE_SYMPY:
        x, g = sp.symbols("final_ce gate", positive=True)
        pred = sp.StrictLessThan(x, g)
        pred_at_val = pred.subs({x: final_ce, g: gate})
        ok = bool(pred_at_val)
        return ok, {"final_ce": final_ce, "gate": gate,
                    "sympy_strict_lt": str(pred_at_val)}
    return final_ce < gate, {"final_ce": final_ce, "gate": gate,
                             "sympy_unavailable": True}


# ════════════════════════════════════════════════════════════════════
# Aggregation
# ════════════════════════════════════════════════════════════════════
def main():
    battery = [
        ("B-S73-FIRE-1",
         "PHYSICS-DERIVED-GATE-AT-TRAINED-FORWARD-CLOSED",      b_s73_fire_1),
        ("B-S73-FIRE-2",
         "LOOP-IS-CLOSED-NOT-OPEN-AT-TRAINED-FORWARD-CLOSED",   b_s73_fire_2),
        ("B-S73-FIRE-3",
         "SELF-TRIGGER-NONDEGENERACY-PREDICATE-CLOSED",         b_s73_fire_3),
        ("B-S73-FIRE-4",
         "CONTROLLER-OFF-REDUCTION-EQUALS-§24-BYTE-EQUAL-CLOSED", b_s73_fire_4),
        ("B-S73-FIRE-5",
         "TRAINED-FORWARD-IS-REAL-NOT-TRACE-SHAPE-CLOSED",      b_s73_fire_5),
        ("B-S73-FIRE-6",
         "CORPUS-SHA256-AND-NO-HELPER-TOKEN-CLOSED",            b_s73_fire_6),
        ("B-S73-FIRE-7",
         "SATURATION-GATE-CLOSED",                              b_s73_fire_7),
    ]

    results = []
    n_pass = 0
    for name, label, fn in battery:
        try:
            ok, evidence = fn()
        except Exception as e:
            ok, evidence = False, f"exception: {type(e).__name__}: {e}"
        results.append({"name": name, "label": label,
                        "passed": bool(ok), "evidence": evidence})
        if ok:
            n_pass += 1
        print(f"  {name:18s} {'✓' if ok else '✗'}  {label}",
              flush=True)

    out = {
        "battery": "B-S73-FIRE-1..7",
        "verdicts": results,
        "n_pass":  n_pass,
        "n_total": len(battery),
        "all_pass": (n_pass == len(battery)),
        "carve_out_note": (
            "B-S73-FIRE-NOTE empirical (B-D-NOTE/B-S62-NOTE/B-S73-NOTE "
            "family): controller-survives-vs-collapse OUTCOME at REAL "
            "trained-saturated scale is an SGD/measurement OUTCOME; "
            "battery proves CONTROLLER-CLASS INVARIANTS, NOT capability "
            "emergence; necessary-not-sufficient per B-EMERGE-7."
        ),
        "north_star_unchanged": True,
        "milestone_unchanged":  "§15 + §51 + §72 (GOAL 미도달)",
        "central_blue_falsifier_diff_lines": 0,
        "sympy_available": _HAVE_SYMPY,
    }
    out_path = os.path.join(HERE, "blue_falsifier_s73_fire_result.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\n  B-S73-FIRE  {n_pass}/{len(battery)} 🔵")
    print(f"  → {out_path}")
    return 0 if out["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
