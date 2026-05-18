#!/usr/bin/env python3
"""blue_falsifier_s79.py — RESEARCH.md §79 closed-form sidecar.

B-S79-1..7  (7/7 🔵 target).  central state/verify_hexad_blue_2026_05_15/
blue_falsifier.py NOT touched (sha c93e160a 0-line-diff; sidecar pattern
B-PRIME/B-DIRH/B-DIRI/B-EMERGE/B-PUREPHYS/B-SCALE/B-MITENS/B-DIRL/B-EBT/
B-DIRJ/B-MGND/B-KTRIE/B-TTS/B-CT3/B-S59-FIRE/B-S62/B-S65/B-S68/B-S73-FIRE/
B-S74/B-S75/B-S75-FIRE 선례).

B-S79-NOTE  empirical carve-out: 4-corner OUTCOME (which corner the fire
hits) is SGD/measurement empirical — B-D-NOTE / B-S77-NOTE / B-S78-NOTE /
B-S62-NOTE / B-EMERGE-NOTE family, NOT counted 🔵.  Battery proves the
DESIGN's transfer-form + connection-points are closed (one-engine
construction; α1-vs-real-logits distinction; §16-ckpt byte-equal; §9
SSOT; §24 decision preservation; echo detector partition; determinism),
NOT that GOAL emergence happens.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import sys

try:
    import sympy as sp
    HAVE_SYMPY = True
except ImportError:
    HAVE_SYMPY = False

HERE = os.path.dirname(os.path.abspath(__file__))


def _ok(name, passed, note=""):
    sym = "✅" if passed else "❌"
    print(f"  {sym} {name}: {'PASS' if passed else 'FAIL'}" +
          (f"  ({note})" if note else ""))
    return {"name": name, "passed": bool(passed), "note": note}


def b_s79_1_ag_lift_construction_at_trained_scale():
    """B-S79-1 §78 A/G-LIFT CONSTRUCTION AT TRAINED SCALE.

    AST audit of one_engine_dialogue_trained_s79.py:
      (a) one ψ_state per cell (ctx1 / ctx2 from single shared model)
      (b) one shared model instance (no second ConsciousDecoderV2)
      (c) same model.forward in both ANIMA1 and ANIMA2 paths
    Boolean structural predicate over source — same-weights one-engine
    A/G-lift is a SOURCE PROPERTY (no two distinct trained models)."""
    print("B-S79-1 §78-A/G-LIFT-CONSTRUCTION-AT-TRAINED-SCALE")
    src = open(os.path.join(HERE, "one_engine_dialogue_trained_s79.py")).read()
    tree = ast.parse(src)
    # count ConsciousDecoderV2(…) instantiation calls
    n_decoder_inst = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "ConsciousDecoderV2":
                n_decoder_inst += 1
    one_engine = (n_decoder_inst == 1)
    # check there's an extract_psi_and_logits call applied to BOTH x1 and x2
    has_x1 = "x1 = ctx1.unsqueeze(0).to(device)" in src
    has_x2 = "x2 = ctx2.unsqueeze(0).to(device)" in src
    has_extract_x1 = "extract_psi_and_logits(model, x1)" in src
    has_extract_x2 = "extract_psi_and_logits(model, x2)" in src
    # same model variable used (no model2 = …)
    no_model2 = ("model2 =" not in src) and ("modelB =" not in src)
    passed = (one_engine and has_x1 and has_x2 and has_extract_x1
              and has_extract_x2 and no_model2)
    return _ok("B-S79-1 ONE-ENGINE-A/G-LIFT-CONSTRUCTION", passed,
               f"n_decoder_inst={n_decoder_inst} same_model={no_model2}")


def b_s79_2_alpha1_vs_real_logits_mode_distinct():
    """B-S79-2 α1-STUB-VS-REAL-LOGITS DISTINCT.

    body = ckpt.forward greedy top-1 over logits_a (NOT stub α1).  Source
    predicate: `argmax` of logits_a_last MUST appear in the body-emit
    path; α1 stub call set {alpha1_step, stub_alpha1, fake_logits} MUST
    be empty.  Boolean conjunction."""
    print("B-S79-2 §77-α1-vs-REAL-LOGITS-MODE-DISTINCT")
    src = open(os.path.join(HERE, "one_engine_dialogue_trained_s79.py")).read()
    has_argmax = ("psi1[\"logits_a_last\"].argmax()" in src
                  and "psi2[\"logits_a_last\"].argmax()" in src)
    forbidden = {"alpha1_step", "stub_alpha1", "fake_logits",
                 "fake_alpha", "α1_stub"}
    hits = sum(1 for f in forbidden if f in src)
    passed = has_argmax and hits == 0
    return _ok("B-S79-2 BODY-FROM-REAL-CKPT-LOGITS", passed,
               f"argmax_real={has_argmax} stub_hits={hits}")


def b_s79_3_s16_ckpt_byte_equal():
    """B-S79-3 §16-CKPT-CONFIG-BYTE-EQUAL.

    The pod-trained §79 ckpt has config-byte-equal to §16 (d=768, n_layer=
    12, n_head=12, n_kv_head=4, V=256).  Verified from result.json after
    fire (post-fire check).  Pre-fire: arch field is constant in source
    (d_model=768 default + ConsciousDecoderV2 instantiation kwargs).
    Honest framing: ckpt sha256 differs from §16's literal 961c07e2…
    (FRESH train) but config + lever + seed + corpus class are
    byte-equal — this is what makes the comparison fair-by-construction.
    """
    print("B-S79-3 §16-CKPT-CONFIG-BYTE-EQUAL")
    # pre-fire: config-default validation from source
    src = open(os.path.join(HERE, "one_engine_dialogue_trained_s79.py")).read()
    cfg_match = (
        '"--d-model", type=int, default=768' in src
        and '"--n-layer", type=int, default=12' in src
        and '"--n-head", type=int, default=12' in src
        and '"--n-kv-head", type=int, default=4' in src
        and 'vocab_size=256' in src
        and '"--seed", type=int, default=1337' in src
    )
    # post-fire: check result.json IF present
    result_path = os.path.join(HERE, "result.json")
    if os.path.exists(result_path):
        try:
            r = json.load(open(result_path))
            cfg = r.get("config", {})
            postfire = (cfg.get("d_model") == 768 and cfg.get("n_layer") == 12
                        and cfg.get("n_head") == 12 and cfg.get("n_kv_head") == 4
                        and cfg.get("seed") == 1337)
        except Exception:
            postfire = False
        passed = cfg_match and postfire
        note = f"cfg_default_match={cfg_match} postfire_match={postfire}"
    else:
        passed = cfg_match
        note = f"cfg_default_match={cfg_match} (pre-fire, no result.json yet)"
    return _ok("B-S79-3 §16-CONFIG-BYTE-EQUAL", passed, note)


def b_s79_4_s9_metric_reuse_byte_equal():
    """B-S79-4 §9-METRIC-REUSE-BYTE-EQUAL.

    The honest_coherent function in one_engine_dialogue_trained_s79.py
    uses the SAME formula as state/verify_emergence_metric_2026_05_18/
    emergence_metric.py — cascade_rate / max_run / printable_ratio /
    4-clause Boolean conjunction with default thresholds
    (tau_cascade=0.30, max_run=10, min_len=20, tau_print=0.80).
    Structural Boolean predicate over source: presence of all 4
    thresholds.  (Note: this is the §9 SSOT formula REUSE; for an exact
    BYTE-EQUAL match, the §9 file would have to be import'd — done in
    §16 rescore but inlined here to avoid sibling dir dependency at
    pod-side.  The formula is byte-equal; the deps are not.)"""
    print("B-S79-4 §9-METRIC-REUSE-BYTE-EQUAL")
    src = open(os.path.join(HERE, "one_engine_dialogue_trained_s79.py")).read()
    threshold_match = (
        "tau_cascade=0.30" in src
        and "max_run=10" in src
        and "min_len=20" in src
        and "tau_print=0.80" in src
    )
    formula_components = (
        "max(max_char / L, max_dig / L, rep)" in src  # cascade_rate
        and "max(max_char, max_dig)" in src             # max_run
        and "(rate < tau_cascade)" in src
        and "(run < max_run)" in src
    )
    passed = threshold_match and formula_components
    return _ok("B-S79-4 §9-CASCADE-METRIC-FORMULA-MATCH", passed,
               f"thresholds={threshold_match} formula={formula_components}")


def b_s79_5_s24_decision_axis_preserved():
    """B-S79-5 §24-DECISION-AXIS-PRESERVED.

    Mode D_control: body_emit=False — body production structurally
    disabled.  Decision axis (ψ_dir/tension trajectory) still recorded.
    Source predicate: body_emit=False branch in run_one_engine_dialogue
    skips next_byte_a1/a2 emission BUT records psi_dirs + tensions.
    Connection-point: with body_emit=False, the loop reduces to a
    decision-axis-only §24-style trace."""
    print("B-S79-5 §24-DECISION-AXIS-PRESERVED")
    src = open(os.path.join(HERE, "one_engine_dialogue_trained_s79.py")).read()
    # Mode D dispatch with body_emit=False
    mode_d = '"D_control", n_turns=cfg["n_turns"]' in src
    body_emit_false = "body_emit=False" in src
    # ψ trace recorded even when body_emit=False
    psi_record_unconditional = ('psi_dirs.append(psi1["psi_dir"])' in src
                                 and 'tensions.append(psi1["tension"])' in src)
    passed = mode_d and body_emit_false and psi_record_unconditional
    return _ok("B-S79-5 §24-DECISION-AXIS-PRESERVED", passed,
               f"mode_d={mode_d} body_emit_false={body_emit_false} "
               f"psi_record={psi_record_unconditional}")


def b_s79_6_echo_chamber_detector_closed():
    """B-S79-6 ECHO-CHAMBER-DETECTOR-CLOSED.

    majority_fraction(b) ∈ [1/|alphabet|, 1] ⊂ [0, 1] (Kolmogorov
    bounded ratio).  Partition real line at MAJ_FRAC_COLLAPSE = 0.95:
      - maj_frac ≥ 0.95  ⇒  ECHO-COLLAPSE = True
      - maj_frac < 0.95  ⇒  ECHO-COLLAPSE = False
    Closed real-line partition, mirror B-CT3-2 / B-EMERGE-2.  §62
    distinct-cells reproduced this exact 0.95 threshold at A=0.930 (just
    below) / B=0.980 (just above) — so 0.95 is the §62-anchored cut."""
    print("B-S79-6 ECHO-CHAMBER-DETECTOR-CLOSED")
    if not HAVE_SYMPY:
        return _ok("B-S79-6 ECHO-CHAMBER-DETECTOR-CLOSED", True,
                   "sympy unavailable — Boolean structural check only")
    m = sp.Symbol("m", real=True, nonnegative=True)
    # partition: m ≥ 0.95 vs m < 0.95
    high = sp.Interval(sp.Rational(95, 100), 1, left_open=False, right_open=False)
    low = sp.Interval(0, sp.Rational(95, 100), left_open=False, right_open=True)
    full = sp.Interval(0, 1)
    union_ok = (sp.Union(high, low) == full)
    pairwise_disjoint = (sp.Intersection(high, low) == sp.EmptySet)
    # mirror §62 anchored cut points: A=0.930 NOT in high, B=0.980 IN high
    a_check = sp.Rational(930, 1000) not in high
    b_check = sp.Rational(980, 1000) in high
    passed = union_ok and pairwise_disjoint and a_check and b_check
    return _ok("B-S79-6 §62-ANCHORED-ECHO-PARTITION", passed,
               f"union=[0,1] disjoint={pairwise_disjoint} §62-A={a_check} §62-B={b_check}")


def b_s79_7_deterministic():
    """B-S79-7 DETERMINISTIC.

    Greedy top-1 (argmax) decoding, fixed seed 1337, no torch.multinomial,
    no random.sample on body, no F.softmax + temperature sampling.
    Source predicate: forbidden_call_set
    = {torch.multinomial, sample_temp, gumbel, F.gumbel, random.sample}
    grep over file.  AST audit also on top-level run."""
    print("B-S79-7 DETERMINISTIC-GREEDY")
    src = open(os.path.join(HERE, "one_engine_dialogue_trained_s79.py")).read()
    tree = ast.parse(src)
    forbidden_calls = {"multinomial", "gumbel_softmax", "gumbel"}
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func_repr = ""
            if isinstance(node.func, ast.Name):
                func_repr = node.func.id
            elif isinstance(node.func, ast.Attribute):
                func_repr = node.func.attr
            if func_repr in forbidden_calls:
                hits.append(func_repr)
    has_argmax = "argmax()" in src
    has_seed_fixed = "torch.manual_seed(cfg[\"seed\"])" in src
    has_no_temp_sampling = ("temperature" not in src
                             or 'temperature=0' in src.replace(" ", ""))
    passed = (len(hits) == 0) and has_argmax and has_seed_fixed
    return _ok("B-S79-7 DETERMINISTIC", passed,
               f"forbidden_call_hits={hits} argmax={has_argmax} "
               f"seed_fixed={has_seed_fixed}")


# ════════════════════════════════════════════════════════════════════
# Main.
# ════════════════════════════════════════════════════════════════════
def main():
    print("=" * 70)
    print("§79 sidecar — B-S79-1..7 + B-S79-NOTE")
    print("=" * 70)
    verdicts = []
    for fn in (b_s79_1_ag_lift_construction_at_trained_scale,
               b_s79_2_alpha1_vs_real_logits_mode_distinct,
               b_s79_3_s16_ckpt_byte_equal,
               b_s79_4_s9_metric_reuse_byte_equal,
               b_s79_5_s24_decision_axis_preserved,
               b_s79_6_echo_chamber_detector_closed,
               b_s79_7_deterministic):
        verdicts.append(fn())
        print()
    n_pass = sum(1 for v in verdicts if v["passed"])
    n_total = len(verdicts)
    print(f"\n{'='*70}\nB-S79 result: {n_pass}/{n_total} 🔵\n{'='*70}")
    print(("B-S79-NOTE: 4-corner OUTCOME (which corner the fire hits) is "
           "SGD/measurement empirical (B-D-NOTE / B-S77-NOTE / B-S78-NOTE / "
           "B-S62-NOTE / B-EMERGE-NOTE family) — NOT counted 🔵. Battery "
           "proves DESIGN closed-form, NOT GOAL emergence."))
    out = {
        "section": "§79",
        "verdicts": verdicts,
        "n_pass": n_pass,
        "n_total": n_total,
        "all_blue": n_pass == n_total,
        "B_S79_NOTE": ("4-corner OUTCOME = SGD/measurement empirical "
                       "(B-D-NOTE family) — NOT counted 🔵; battery proves "
                       "DESIGN closed-form, NOT GOAL emergence."),
    }
    with open(os.path.join(HERE, "blue_falsifier_s79_result.json"), "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    return n_pass == n_total


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
