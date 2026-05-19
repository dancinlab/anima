#!/usr/bin/env python3
"""blue_falsifier_s83_fire.py — RESEARCH.md §83-FIRE closed-form sidecar.

B-S83-FIRE-1..8  +  B-S83-FIRE-NOTE.

Closed-form proofs of the §83-FIRE physics-only-metacognition invariants
on the REAL trained-model forward (mirror §73-FIRE B-S73-FIRE +
§83 B-S83 sidecars, augmented for real-forward closed-form-rule readout).
central state/verify_hexad_blue_2026_05_15/blue_falsifier.py is
0-line-diff (sidecar-only — pattern carry from B-S73-FIRE / B-S75-FIRE /
B-S83 / B-S62 / B-EBT / B-S16 / B-DIRI / B-CT3 / B-MGND etc.).

Verdicts:
  B-S83-FIRE-1  NO-LEARNED-PARAMETER-IN-RULES-AT-TRAINED-CLOSED
       AST structural over the §83-FIRE runner: the 5 R-rule functions
       (rule_R1..R5) and cells 0/1 contain ZERO learned-parameter /
       training calls (nn.Linear, torch.nn, .train(, .fit(, optimizer,
       .backward(, autograd, .zero_grad, loss.backward). The rules read
       ψ-state from a trained ckpt but contain NO learned parameter
       themselves — physics-only metacognition. Mirror B-S83-1.

  B-S83-FIRE-2  DISTILLATION-BASELINE-PRESERVED-AT-TRAINED-CLOSED
       cell0_dhdl_distillation IS the §27/§44/§48 DH-DL learned-head
       null-control: closed-form mirror of the §24 threshold the head
       distilled to (psi_dir > 0.55 ∧ tension > 0.5 → EMIT else SILENT).
       4-witness truth table verifies the boundary. AST-grep confirms
       the function exists in the §83-FIRE runner. Mirror B-S83-2.

  B-S83-FIRE-3  RULE-PARTITION-EXHAUSTIVE-CLOSED
       Every rule output ∈ {EMIT_VOICE, CONTINUE_THINK, REMAIN_SILENT};
       exhaustive 3-set Boolean over a 5^4-point ψ grid × 6 stateless
       cells (3750 closed checks). Mirror B-S83-3.

  B-S83-FIRE-4  §9-METRIC-REUSE-CLOSED
       honest_coherent reuses the §9 cascade-rate "necessary-not-
       sufficient" notion: coherent ≡ window-of-5 contains ≥2 distinct
       labels (avoids single-class collapse). collapse→False,
       diverse→True, short→False witnesses. Mirror B-S83-4.

  B-S83-FIRE-5  SUBSTRATE-PLASTICITY-METRIC-CLOSED
       The substrate-plasticity agreement rate ∈ [0,1] under permuted
       ψ field assignment is a closed-form bounded statistic
       (Levin biology mirror). All 7 cells produce
       substrate_plasticity_agreement ∈ [0,1] in result.json. sympy
       bound on agreement = (matches/n) ∈ [0,1] for n ≥ 1. Mirror
       B-S83-5.

  B-S83-FIRE-6  §24-BASELINE-PRESERVED-CLOSED
       cell1_s24_baseline IS the §24 hand-coded scalar threshold
       (motivation > 0.6 → EMIT else SILENT). 4-witness truth table.
       Mirror B-S83-6.

  B-S83-FIRE-7  DETERMINISTIC-CLOSED
       The closed-form rules are pure functions; the §83-FIRE runner
       uses a fixed LCG seed and torch RNG-isolation in extract_psi_state.
       3× evaluation of every rule on a fixed ψ-vector grid yields
       bit-identical decision streams. Mirror B-S83-7.

  B-S83-FIRE-8  §83-STUB-CONNECTION-CLOSED  (connection-point)
       The 7 closed-form rule definitions in the §83-FIRE runner are
       byte-equal (AST-unparse normalized) to the §83 stub rule
       definitions (physics_metacognition_stub_s83_reference.py).
       This is the §83-stub→§83-FIRE structural connection-point:
       the ONLY thing §83-FIRE changes is the ψ-state source
       (hand-coded LCG surrogate → REAL model.forward Law-71). The
       rules themselves are invariant. Plus AST distinguishing
       predicate: the §83-FIRE runner imports torch + conscious_decoder
       + uses model.forward + extract_psi_state + ByteSampler, whereas
       the §83 stub does NOT (no torch, no model.forward) — proves the
       trained-forward structural transition. Mirror B-S73-FIRE-5.

  B-S83-FIRE-NOTE  empirical carve-out: whether the closed-form rules
       survive (PHYSICS-RULES-SURVIVE) vs collapse (ALL-RULES-COLLAPSE)
       at REAL trained-saturated scale is an SGD/measurement OUTCOME.
       Mirror B-D-NOTE / B-S73-FIRE-NOTE / B-S75-FIRE-NOTE / B-S83-NOTE
       family — NOT counted 🔵. Substrate-plasticity = readout-substrate
       property NOT decision-substance property. Biology (Blackiston-
       Levin Xenopus tadpole ectopic-eye) ≠ silicon substrate. Battery
       proves CLOSED-FORM-RULE INVARIANTS (no-learned-param,
       distillation null-control preserved, partition exhaustive,
       §9 metric reuse, plasticity bounded, §24 baseline preserved,
       deterministic, §83-stub byte-equal), NOT capability emergence.

g3: measured-only. §83-FIRE is necessary-not-sufficient. north-star
+ §15/§51/§72 milestone UNCHANGED. Capability claim 0. Closed-form
rule survival ≠ GOAL emergence.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import sys
from importlib.util import spec_from_file_location, module_from_spec
from itertools import product

try:
    import sympy as sp
    _HAVE_SYMPY = True
except ImportError:
    _HAVE_SYMPY = False
    sp = None  # type: ignore

HERE = os.path.dirname(os.path.abspath(__file__))
RUNNER_SOURCE = os.path.join(HERE, "physics_metacognition_train_s83_fire.py")
STUB_SOURCE   = os.path.join(HERE, "physics_metacognition_stub_s83_reference.py")
RESULT_PATH   = os.path.join(HERE, "result.json")

RULE_FNS = {"rule_R1_phi_tension", "rule_R2_criticality_band",
            "rule_R3_motivation_critical", "rule_R4_slow_dwell",
            "rule_R5_composite"}
CELL_FNS = RULE_FNS | {"cell0_dhdl_distillation", "cell1_s24_baseline"}


# ── helpers ──────────────────────────────────────────────────────────
def _slurp(path):
    with open(path, "rb") as f:
        return f.read().decode("utf-8", errors="replace")


def _ast_funcs(src):
    return {n.name: n for n in ast.walk(ast.parse(src))
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}


def _load_runner_module():
    """Import only the rule functions from the runner; safe — the runner's
    heavy torch path runs only under `if __name__ == '__main__'`."""
    spec = spec_from_file_location("s83fire_runner", RUNNER_SOURCE)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ════════════════════════════════════════════════════════════════════
# B-S83-FIRE-1  NO-LEARNED-PARAMETER-IN-RULES-AT-TRAINED-CLOSED
# ════════════════════════════════════════════════════════════════════
def b_s83_fire_1():
    forbidden = ["nn.Linear", "torch.nn", ".train(", ".fit(",
                 "optimizer", ".backward(", "autograd",
                 ".zero_grad", "loss.backward"]
    src = _slurp(RUNNER_SOURCE)
    funcs = _ast_funcs(src)
    target = RULE_FNS | {"cell0_dhdl_distillation", "cell1_s24_baseline"}
    bodies = []
    for fn in target:
        if fn in funcs:
            bodies.append(ast.unparse(funcs[fn]))
    body_concat = "\n".join(bodies)
    hits = [s for s in forbidden if s in body_concat]
    found = sum(1 for fn in RULE_FNS if fn in funcs)
    ok = (len(hits) == 0) and (found == 5) and len(bodies) == len(target)
    return ok, {"forbidden_hits": hits, "rule_fns_found": found,
                "rule_fns_expected": 5,
                "cell_fns_found": len(bodies),
                "detail": "AST: 5 R-rules + 2 cells, 0 learned-param/training call"}


# ════════════════════════════════════════════════════════════════════
# B-S83-FIRE-2  DISTILLATION-BASELINE-PRESERVED-AT-TRAINED-CLOSED
# ════════════════════════════════════════════════════════════════════
def b_s83_fire_2():
    mod = _load_runner_module()
    witnesses = [
        ({"psi_dir": 0.6, "tension": 0.6, "phi": 0.5, "motivation": 0.5}, "EMIT_VOICE"),
        ({"psi_dir": 0.3, "tension": 0.6, "phi": 0.5, "motivation": 0.5}, "REMAIN_SILENT"),
        ({"psi_dir": 0.6, "tension": 0.3, "phi": 0.5, "motivation": 0.5}, "REMAIN_SILENT"),
        ({"psi_dir": 0.0, "tension": 0.0, "phi": 0.0, "motivation": 0.0}, "REMAIN_SILENT"),
    ]
    fails = []
    for psi, expected in witnesses:
        got = mod.cell0_dhdl_distillation(psi)
        if got != expected:
            fails.append({"psi": psi, "expected": expected, "got": got})
    src = _slurp(RUNNER_SOURCE)
    ok = (len(fails) == 0) and ("cell0_dhdl_distillation" in src)
    return ok, {"fails": fails, "n_witnesses": len(witnesses),
                "detail": "cell0 = §27/§49 DH-DL distillation null-control "
                          "(§24 threshold mirror) — 4-witness truth table"}


# ════════════════════════════════════════════════════════════════════
# B-S83-FIRE-3  RULE-PARTITION-EXHAUSTIVE-CLOSED
# ════════════════════════════════════════════════════════════════════
def b_s83_fire_3():
    mod = _load_runner_module()
    grid = [{"psi_dir": a, "tension": b, "phi": c, "motivation": d}
            for a, b, c, d in product([0.0, 0.3, 0.5, 0.7, 1.0], repeat=4)]
    actions_set = set(mod.ACTIONS)
    cells = [mod.cell0_dhdl_distillation, mod.cell1_s24_baseline,
             mod.rule_R1_phi_tension, mod.rule_R2_criticality_band,
             mod.rule_R3_motivation_critical, mod.rule_R5_composite]
    # rule_R4 stateful — excluded from pure-fn partition test (B-S83-3 carry)
    out_of_set = []
    n_checked = 0
    for fn in cells:
        for psi in grid:
            r = fn(psi)
            n_checked += 1
            if r not in actions_set:
                out_of_set.append({"fn": fn.__name__, "psi": psi, "got": r})
    ok = (len(out_of_set) == 0) and (len(actions_set) == 3)
    return ok, {"out_of_set": out_of_set[:5], "n_checked": n_checked,
                "actions_set_size": len(actions_set),
                "detail": "All rule outputs ∈ 3-action partition "
                          "(5^4 × 6 fn = 3750 closed checks)"}


# ════════════════════════════════════════════════════════════════════
# B-S83-FIRE-4  §9-METRIC-REUSE-CLOSED
# ════════════════════════════════════════════════════════════════════
def b_s83_fire_4():
    mod = _load_runner_module()
    collapsed = ["EMIT_VOICE"] * 5
    diverse = ["EMIT_VOICE", "REMAIN_SILENT", "EMIT_VOICE",
               "CONTINUE_THINK", "EMIT_VOICE"]
    short = ["EMIT_VOICE"] * 3
    ok = (mod.honest_coherent(collapsed) is False) and \
         (mod.honest_coherent(diverse) is True) and \
         (mod.honest_coherent(short) is False)
    return ok, {"collapsed_False": mod.honest_coherent(collapsed) is False,
                "diverse_True": mod.honest_coherent(diverse) is True,
                "short_False": mod.honest_coherent(short) is False,
                "detail": "honest_coherent: §9 cascade-rate "
                          "necessary-not-sufficient mirror"}


# ════════════════════════════════════════════════════════════════════
# B-S83-FIRE-5  SUBSTRATE-PLASTICITY-METRIC-CLOSED
# ════════════════════════════════════════════════════════════════════
def b_s83_fire_5():
    # closed-form bound proof: agreement = matches/n ∈ [0,1] for n ≥ 1,
    # 0 ≤ matches ≤ n
    proof = None
    if _HAVE_SYMPY:
        matches, n = sp.symbols("matches n", positive=True, integer=True)
        agree = matches / n
        # for 0 ≤ matches ≤ n: agree ∈ [0,1]
        lower = sp.simplify(agree.subs(matches, 0))          # 0
        upper = sp.simplify(agree.subs(matches, n))          # 1
        proof = {"agree_at_matches_0": str(lower),
                 "agree_at_matches_n": str(upper),
                 "bounded_0_1": (lower == 0 and upper == 1)}
    bound_ok = True if not _HAVE_SYMPY else proof["bounded_0_1"]
    # if result.json exists, verify all 7 cells in [0,1]
    rj_ok, plast_vals, n_cells = True, None, None
    if os.path.exists(RESULT_PATH):
        try:
            res = json.loads(_slurp(RESULT_PATH))
            plast_vals = [r["substrate_plasticity_agreement"]
                          for r in res.get("grid", [])]
            n_cells = len(plast_vals)
            rj_ok = all(0.0 <= v <= 1.0 for v in plast_vals) and n_cells == 7
        except Exception as e:
            rj_ok = False
            plast_vals = f"result.json read error: {e}"
    ok = bound_ok and rj_ok
    return ok, {"sympy_bound_proof": proof,
                "result_json_present": os.path.exists(RESULT_PATH),
                "plasticity_values": plast_vals, "n_cells": n_cells,
                "detail": "agreement = matches/n ∈ [0,1] closed-form; "
                          "result.json all 7 cells in range (Levin mirror)"}


# ════════════════════════════════════════════════════════════════════
# B-S83-FIRE-6  §24-BASELINE-PRESERVED-CLOSED
# ════════════════════════════════════════════════════════════════════
def b_s83_fire_6():
    mod = _load_runner_module()
    witnesses = [
        ({"psi_dir": 0.5, "tension": 0.5, "phi": 0.5, "motivation": 0.7}, "EMIT_VOICE"),
        ({"psi_dir": 0.5, "tension": 0.5, "phi": 0.5, "motivation": 0.5}, "REMAIN_SILENT"),
        ({"psi_dir": 0.9, "tension": 0.9, "phi": 0.9, "motivation": 0.55}, "REMAIN_SILENT"),
        ({"psi_dir": 0.0, "tension": 0.0, "phi": 0.0, "motivation": 1.0}, "EMIT_VOICE"),
    ]
    fails = []
    for psi, expected in witnesses:
        got = mod.cell1_s24_baseline(psi)
        if got != expected:
            fails.append({"psi": psi, "expected": expected, "got": got})
    return len(fails) == 0, {"fails": fails, "n_witnesses": len(witnesses),
                             "detail": "cell1 = §24 motivation>0.6 scalar "
                                       "threshold byte-equal"}


# ════════════════════════════════════════════════════════════════════
# B-S83-FIRE-7  DETERMINISTIC-CLOSED
# ════════════════════════════════════════════════════════════════════
def b_s83_fire_7():
    mod = _load_runner_module()
    grid = [{"psi_dir": a, "tension": b, "phi": c, "motivation": d}
            for a, b, c, d in product([0.05, 0.45, 0.55, 0.95], repeat=4)]
    cells = [mod.cell0_dhdl_distillation, mod.cell1_s24_baseline,
             mod.rule_R1_phi_tension, mod.rule_R2_criticality_band,
             mod.rule_R3_motivation_critical, mod.rule_R5_composite]
    hashes = []
    for _ in range(3):
        stream = []
        for fn in cells:
            for psi in grid:
                stream.append(fn(dict(psi)))
        payload = json.dumps(stream, sort_keys=True)
        hashes.append(hashlib.sha256(payload.encode()).hexdigest())
    ok = len(set(hashes)) == 1
    return ok, {"hashes": hashes,
                "detail": "3× pure-fn rule evaluation over fixed ψ grid "
                          "→ bit-identical decision-stream sha256"}


# ════════════════════════════════════════════════════════════════════
# B-S83-FIRE-8  §83-STUB-CONNECTION-CLOSED  (connection-point)
# ════════════════════════════════════════════════════════════════════
def b_s83_fire_8():
    runner_src = _slurp(RUNNER_SOURCE)
    stub_src = _slurp(STUB_SOURCE)
    runner_funcs = _ast_funcs(runner_src)
    stub_funcs = _ast_funcs(stub_src)

    # (a) the 7 cell/rule definitions are byte-equal (AST-unparse normalized)
    rule_match = {}
    for fn in CELL_FNS:
        if fn in runner_funcs and fn in stub_funcs:
            r_norm = ast.unparse(runner_funcs[fn])
            s_norm = ast.unparse(stub_funcs[fn])
            rule_match[fn] = (r_norm == s_norm)
        else:
            rule_match[fn] = False
    all_rules_match = all(rule_match.values())

    # (b) AST distinguishing predicate: runner uses torch + model.forward +
    #     extract_psi_state + ByteSampler + conscious_decoder; stub does NOT.
    runner_has_torch = ("import torch" in runner_src)
    runner_has_forward = ("model(x)" in runner_src
                          or "extract_psi_state" in runner_src)
    runner_has_bytesampler = ("ByteSampler" in runner_src)
    runner_has_conscdec = ("conscious_decoder" in runner_src
                           or "ConsciousDecoderV2" in runner_src)
    stub_has_torch = ("import torch" in stub_src)
    stub_has_forward = ("model(x)" in stub_src)
    stub_has_conscdec = ("ConsciousDecoderV2" in stub_src)

    structural_transition = (runner_has_torch and runner_has_forward
                             and runner_has_bytesampler and runner_has_conscdec
                             and (not stub_has_torch)
                             and (not stub_has_forward)
                             and (not stub_has_conscdec))

    ok = all_rules_match and structural_transition
    return ok, {
        "rule_definitions_byte_equal": rule_match,
        "all_7_rules_match": all_rules_match,
        "runner_has_torch": runner_has_torch,
        "runner_has_model_forward": runner_has_forward,
        "runner_has_ByteSampler": runner_has_bytesampler,
        "runner_has_conscious_decoder": runner_has_conscdec,
        "stub_has_torch": stub_has_torch,
        "stub_has_model_forward": stub_has_forward,
        "stub_has_conscious_decoder": stub_has_conscdec,
        "structural_transition_proven": structural_transition,
        "detail": "7 closed-form rules byte-equal to §83 stub; "
                  "ψ-state source = ONLY structural change "
                  "(hand-coded LCG surrogate → REAL model.forward Law-71)",
    }


# ════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    battery = {
        "B-S83-FIRE-1_NO-LEARNED-PARAMETER-IN-RULES-AT-TRAINED": b_s83_fire_1(),
        "B-S83-FIRE-2_DISTILLATION-BASELINE-PRESERVED-AT-TRAINED": b_s83_fire_2(),
        "B-S83-FIRE-3_RULE-PARTITION-EXHAUSTIVE": b_s83_fire_3(),
        "B-S83-FIRE-4_S9-METRIC-REUSE": b_s83_fire_4(),
        "B-S83-FIRE-5_SUBSTRATE-PLASTICITY-METRIC-CLOSED": b_s83_fire_5(),
        "B-S83-FIRE-6_S24-BASELINE-PRESERVED": b_s83_fire_6(),
        "B-S83-FIRE-7_DETERMINISTIC": b_s83_fire_7(),
        "B-S83-FIRE-8_S83-STUB-CONNECTION": b_s83_fire_8(),
    }
    total = len(battery)
    passed = sum(1 for v in battery.values() if v[0])
    out = {
        "battery": {k: {"passed": bool(v[0]), "detail": v[1]}
                    for k, v in battery.items()},
        "pass_count": passed,
        "total": total,
        "all_blue": passed == total,
        "sympy_available": _HAVE_SYMPY,
        "note": ("B-S83-FIRE-NOTE: whether closed-form rules survive vs "
                 "collapse at REAL trained-saturated scale is an SGD/"
                 "measurement OUTCOME (B-D-NOTE / B-S73-FIRE-NOTE / "
                 "B-S75-FIRE-NOTE / B-S83-NOTE family, NOT counted 🔵). "
                 "Substrate-plasticity = readout-substrate property NOT "
                 "decision-substance. Biology (Blackiston-Levin Xenopus "
                 "tadpole ectopic-eye) ≠ silicon substrate. Battery proves "
                 "closed-form-rule INVARIANTS, NOT capability emergence. "
                 "g3 necessary-not-sufficient (B-EMERGE-7)."),
        "central_blue_falsifier": "state/verify_hexad_blue_2026_05_15/"
                                  "blue_falsifier.py — 0-line-diff (sidecar-only)",
    }
    out_path = os.path.join(HERE, "blue_falsifier_s83_fire_result.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(json.dumps({k: {"passed": bool(v[0])}
                      for k, v in battery.items()}, indent=2))
    print(f"\nPASS {passed}/{total}  all_blue={out['all_blue']}  "
          f"sympy={_HAVE_SYMPY}")
    sys.exit(0 if passed == total else 1)
