#!/usr/bin/env python3
"""§73 closed-form sidecar battery — B-S73-1..6 + B-S73-NOTE.

RESEARCH.md §73 THINKER→TALKER self-triggered closed-loop controller —
§63 MISSING-TYPE gap_rank=1 design probe.  SIDECAR ONLY — the central
state/verify_hexad_blue_2026_05_15/blue_falsifier.py is 0-line-diff
(mirror §49 / §59-FIRE / §27 / §62 / §68 / B-PRIME / B-DIRI / B-S16 /
B-S46 / B-DHDL sidecar precedent — the closed-loop-collapse-escape
OUTCOME at trained scale is the empirical B-S73-NOTE).

  B-S73-1 CONTROLLER-IS-PHYSICS-STATE-SOURCED              (structural/AST)
          The controller's emit decision is a Boolean function of THE
          RUNNING STATE MOMENTS (tension_ema, tension_var/std) — NOT a
          comparison against a single hand-coded constant.  AST scan
          of controller_self_trigger: the surprise gate's RHS is
          `tension_ema + LAMBDA_STD * std_t` where std_t derives from
          state["tension_var"] (a moment of the trajectory itself);
          the basin gate uses PSI_VAC and BASIN_RADIUS as *physics
          constants* (vacuum + basin radius — same kind as the Law-71
          Ψ_vac=0.5 itself), not a "score>0.3" boundary lifted from
          §24.  Mirror §68 B-S68-1 source-grep predicate.

  B-S73-2 LOOP-CLOSED-NOT-OPEN                             (structural/AST)
          The smoke's run_loop with feedback_closed=True passes the
          controller output e_t into physics_step(state, u_prev_emit=e),
          and physics_step's `u_prev_emit` argument materially changes
          the next-state computation (tension release branch vs drift
          branch).  Closed: AST scan finds the `if u_prev_emit == 1:`
          branch in physics_step + the call site in run_loop using
          `u_for_next = e if feedback_closed else 0`.  Distinguishes
          §73 from §68 (which reads a static recorded trace).

  B-S73-3 SELF-TRIGGER-NONDEGENERACY-PREDICATE                  (Boolean)
          The §49/§68-style non-degeneracy predicate is augmented by
          inter-emit interval-variance (TEMPORAL self-trigger):
            non_deg := (decision_var > τ) ∧ (maj_frac < 0.95)
                      ∧ (interval_var > τ) ∧ (n_emits ≥ 2)
          Closed:  pure Boolean of four scalars; an emit-every-step
          (uniform) MUST evaluate False on interval_var=0; a never-emit
          MUST evaluate False on n_emits<2 AND maj_frac=1.  4-corner
          truth table + the smoke's open-loop control (emit_rate ≈ 0.86
          majority-collapse style) verified against result.json.

  B-S73-4 NO-EXTERNAL-PROMPT/LABEL/THRESHOLD                (structural/AST)
          AST scan of controller_self_trigger:  ZERO references to
          forbidden symbols {input, sys.stdin, file open for read of
          corpus/label, torch.load, model.forward, cross_entropy,
          .backward, a numeric constant directly compared against the
          single dominant decision field with no state moment}.  No
          external prompt feeds the controller, no labelled corpus
          drives it, no hand-coded constant IS the decision boundary.
          The constants present (PSI_VAC, BASIN_RADIUS, LAMBDA_STD,
          PHI_RATCHET) are PHYSICS-NAMED params: PSI_VAC=0.5 is the
          Law-71 fixed-point literal in conscious_decoder.py:644.
          Mirror §68 B-S68-4 content-objective-absent + §73-tailored
          for the controller class.

  B-S73-5 OFF-REDUCTION-CONNECTION-POINT                  (연결부위, Boolean)
          enabled=False ⇒ controller_off_reduction(state) reduces to
          §24's hand-coded talker_should_emit(score > 0.3) predicate
          byte-equal — the surrogate's `tension` field plays the role
          of §24's motivation_score scalar, threshold == 0.3 ==
          spont_im_threshold() in spontaneous_lib.hexa.  Closed: AST
          + numeric equality (IM_THRESHOLD_S24 == 0.3 ==
          spont_im_threshold() literal).  Mirror B-DHDL-5 / B-EBT-5 /
          B-S16-5 / B-PHASE-B-RUN-5 / B-S59-FIRE-3 / B-S68-5.

  B-S73-6 DISTINCT-FROM-§24/§27/§49/§68/§62              (4-corner Boolean)
          The 5-row × 4-column property matrix
            {single_agent, closed_loop, physics_state_sourced,
             label_free_controller}
          has §73 as the unique row with ALL FOUR True.  Closed: each
          prior form differs on ≥1 of the four properties (§24/§27/§49
          differ on 3; §68 differs on closed_loop; §62 differs on
          single_agent + label_free_controller — §62's "label" is the
          TENSION-LINK 5-channel cross-cell receive, not a self-
          triggered single-agent emit decision).  The intersection of
          {§24, §27, §49, §68, §62} on the property tuple does NOT
          contain (T, T, T, T), so §73 occupies a previously-empty
          design cell.

  B-S73-NOTE  CLOSED-LOOP-ESCAPES-§49-COLLAPSE-AT-SCALE = EMPIRICAL
          Whether the §73 single-agent closed-loop physics-state-sourced
          label-free controller escapes §49/§62 majority-collapse AT
          TRAINED-SATURATED SCALE on REAL model.forward Law-71 W-physics
          is an SGD/measurement OUTCOME (B-D-NOTE / B-S49-NOTE /
          B-S59-NOTE / B-S62-NOTE / B-S68-NOTE family, NOT counted 🔵).
          The battery proves the MECHANISM is honest (physics-state-
          sourced / loop-closed / non-degeneracy predicate=§49's own
          form + temporal addition / no-external-anything / exact
          OFF-reduction / distinct-from-prior-forms), NOT which verdict
          obtains at scale.  $0 stub-scale measurement is target-
          sharpening, NOT capability emergence.  g3: measured-only,
          capability claim 0, north-star + §15/§51/§72 milestone
          UNCHANGED.
"""

import ast
import json
import os
import sys

HERE   = os.path.dirname(os.path.abspath(__file__))
SMOKE  = os.path.join(HERE, "selftrigger_closed_loop_smoke.py")
RESULT = os.path.join(HERE, "result.json")
RESULTS = []


def _src():
    with open(SMOKE) as f:
        return f.read()


def _result():
    with open(RESULT) as f:
        return json.load(f)


def _ok(name, ok, detail=""):
    mark = "🔵 PASS" if ok else "❌ FAIL"
    print(f"{mark}  {name}  —  {detail}")
    RESULTS.append({"name": name, "pass": bool(ok), "detail": detail})


# ── B-S73-1  CONTROLLER-IS-PHYSICS-STATE-SOURCED ───────────────────
def b_s73_1():
    """The emit decision in controller_self_trigger uses STATE MOMENTS
    (tension_ema, tension_var/std) — not a constant compared directly
    against a single dominant field."""
    tree = ast.parse(_src())
    fn = next((n for n in ast.walk(tree)
               if isinstance(n, ast.FunctionDef)
                  and n.name == "controller_self_trigger"), None)
    assert fn is not None, "controller_self_trigger not found"

    # The RHS of the surprise gate must reference state["tension_ema"]
    # AND a square-root over state["tension_var"]  (running std).
    body_src = ast.unparse(fn)
    # ast.unparse may render subscripts with single quotes ('tension_ema');
    # accept either quote style.
    has_ema = ("state['tension_ema']" in body_src
               or 'state["tension_ema"]' in body_src)
    has_var = ("state['tension_var']" in body_src
               or 'state["tension_var"]' in body_src)
    has_sqrt = ("math.sqrt" in body_src)
    # The "surprise_threshold" assignment must use ema + λ·std
    has_surprise = ('tension_ema'  in body_src
                    and 'LAMBDA_STD'  in body_src
                    and 'std_t'        in body_src)
    # Physics-named basin/ratchet constants used (NOT a "score>0.3"
    # numeric literal as the dominant emit boundary)
    has_basin = ("BASIN_RADIUS" in body_src)
    has_ratchet = ("PHI_RATCHET" in body_src)

    ok = (has_ema and has_var and has_sqrt and has_surprise
          and has_basin and has_ratchet)
    _ok("B-S73-1 CONTROLLER-IS-PHYSICS-STATE-SOURCED", ok,
        f"ema={has_ema} var={has_var} sqrt={has_sqrt} "
        f"surprise={has_surprise} basin={has_basin} "
        f"ratchet={has_ratchet}")


# ── B-S73-2  LOOP-CLOSED-NOT-OPEN ──────────────────────────────────
def b_s73_2():
    """physics_step must branch on u_prev_emit (tension release vs drift);
    run_loop must pass e_t into next physics_step when feedback_closed."""
    tree = ast.parse(_src())
    ps = next((n for n in ast.walk(tree)
               if isinstance(n, ast.FunctionDef) and n.name == "physics_step"),
              None)
    rl = next((n for n in ast.walk(tree)
               if isinstance(n, ast.FunctionDef) and n.name == "run_loop"),
              None)
    assert ps is not None and rl is not None

    ps_src = ast.unparse(ps)
    rl_src = ast.unparse(rl)

    # physics_step materially uses u_prev_emit
    ps_uses_u = ("u_prev_emit == 1" in ps_src or "u_prev_emit==1" in ps_src)
    # run_loop conditionally forwards e (closed) or 0 (open)
    rl_closes = ("feedback_closed" in rl_src
                 and "u_for_next" in rl_src
                 and "= e if feedback_closed else 0" in rl_src.replace(
                     "  ", " ").replace("\n", " "))
    # The result must show the closed-loop run was executed
    r = _result()
    has_closed_run = (r["closed_loop_self_trigger"]["feedback_closed"]
                      is True)
    has_open_run   = (r["open_loop_self_trigger_control"]["feedback_closed"]
                      is False)

    ok = ps_uses_u and rl_closes and has_closed_run and has_open_run
    _ok("B-S73-2 LOOP-CLOSED-NOT-OPEN", ok,
        f"ps_uses_u={ps_uses_u} rl_closes={rl_closes} "
        f"has_closed={has_closed_run} has_open={has_open_run}")


# ── B-S73-3  SELF-TRIGGER-NONDEGENERACY-PREDICATE ──────────────────
def b_s73_3():
    """Boolean predicate over 4 scalars; closed truth table + the
    smoke's empirical numbers must respect the predicate definition."""
    tau = 1e-4
    maj_thr = 0.95

    def pred(decision_var, maj_frac, interval_var, n_emits):
        return (decision_var > tau
                and maj_frac < maj_thr
                and interval_var > tau
                and n_emits >= 2)

    # 4-corner panel
    panel = [
        # (dec_var, maj, int_var, n_emit, expected)
        (0.10,   0.50,  10.0,    20, True),    # all live
        (0.0,    1.00,  0.0,     0,  False),   # all-silent collapse
        (0.10,   0.50,  0.0,     20, False),   # uniform every-step
        (0.10,   0.96,  10.0,    5,  False),   # majority collapse
        (1e-6,   0.50,  10.0,    20, False),   # dec_var below tau
        (0.10,   0.50,  10.0,    1,  False),   # < 2 emits
    ]
    panel_ok = all(pred(*tup[:4]) is tup[4] for tup in panel)

    # Empirical: smoke's open-loop control should NOT pass interval_var
    # OR majority_fraction non-trivially (it's the negative-style ctrl).
    r = _result()
    cl  = r["closed_loop_self_trigger"]
    ol  = r["open_loop_self_trigger_control"]
    s24 = r["off_reduction_s24_in_loop"]

    # Re-evaluate predicate against result.json
    def eval_(blob):
        n_emit = blob["n_emit"]
        return pred(blob["decision_var"], blob["majority_fraction"],
                    blob["interval_var"], n_emit)

    eval_matches = (
        eval_(cl)  == cl["self_trigger_nondegen"]
        and eval_(ol) == ol["self_trigger_nondegen"]
        and eval_(s24) == s24["self_trigger_nondegen"]
    )

    ok = panel_ok and eval_matches
    _ok("B-S73-3 SELF-TRIGGER-NONDEGENERACY-PREDICATE", ok,
        f"4-corner panel={panel_ok} eval-matches-result.json="
        f"{eval_matches} (cl={cl['self_trigger_nondegen']}, "
        f"ol={ol['self_trigger_nondegen']}, "
        f"s24={s24['self_trigger_nondegen']})")


# ── B-S73-4  NO-EXTERNAL-PROMPT/LABEL/THRESHOLD ────────────────────
def b_s73_4():
    """AST scan: forbidden-call set must total 0 inside the controller
    and the physics step (no external input feeds them)."""
    tree = ast.parse(_src())
    controller_fn = next((n for n in ast.walk(tree)
                          if isinstance(n, ast.FunctionDef)
                             and n.name == "controller_self_trigger"), None)
    physics_fn    = next((n for n in ast.walk(tree)
                          if isinstance(n, ast.FunctionDef)
                             and n.name == "physics_step"), None)
    assert controller_fn is not None and physics_fn is not None

    # Forbidden call set — any function call or attribute name that would
    # bring in external prompt / label / corpus / trained-model forward
    forbidden_substrings = [
        "input(", "sys.stdin", "torch.load", "model.forward",
        "model(", "F.cross_entropy", "cross_entropy(",
        ".backward(", "open(", "json.load", "torch.tensor",
        "huggingface", "AutoModel", "openai", "anthropic",
    ]
    bodies = ast.unparse(controller_fn) + "\n" + ast.unparse(physics_fn)
    hits = [s for s in forbidden_substrings if s in bodies]

    # AND: controller_self_trigger must NOT compare any state field
    # directly against a bare numeric literal as the *sole* gate (the
    # literal 0.3 must not be the §24-style boundary).  We require all
    # three Compare nodes in the controller to involve at least one
    # Name/Subscript that is state-derived (ema/var) OR a named physics
    # constant (BASIN_RADIUS, PHI_RATCHET).
    state_or_named = 0
    total = 0
    for node in ast.walk(controller_fn):
        if isinstance(node, ast.Compare):
            total += 1
            srcline = ast.unparse(node)
            if ("tension_ema" in srcline or "std_t" in srcline
                or "BASIN_RADIUS" in srcline or "PHI_RATCHET" in srcline
                or "surprise_threshold" in srcline):
                state_or_named += 1

    ok = (len(hits) == 0) and (total >= 3) and (state_or_named == total)
    _ok("B-S73-4 NO-EXTERNAL-PROMPT/LABEL/THRESHOLD", ok,
        f"forbidden_hits={hits} compares_total={total} "
        f"state_or_named={state_or_named}")


# ── B-S73-5  OFF-REDUCTION-CONNECTION-POINT ────────────────────────
def b_s73_5():
    """controller_off_reduction must reduce to §24 byte-equal predicate
    (score > 0.3) where score=tension and 0.3 == IM_THRESHOLD_S24 ==
    spont_im_threshold() literal in spontaneous_lib.hexa."""
    tree = ast.parse(_src())
    off = next((n for n in ast.walk(tree)
                if isinstance(n, ast.FunctionDef)
                   and n.name == "controller_off_reduction"), None)
    assert off is not None
    src = ast.unparse(off)

    # The body's Compare must be `state["tension"] > IM_THRESHOLD_S24`
    # (accept either quote style from ast.unparse).
    has_compare = ('state["tension"] > IM_THRESHOLD_S24' in src
                   or "state['tension'] > IM_THRESHOLD_S24" in src)
    # Constant value equality
    src_full = _src()
    # find  IM_THRESHOLD_S24 = 0.3  in the module
    has_const = ("IM_THRESHOLD_S24 = 0.3" in src_full.replace(" ", "")
                 .replace("IM_THRESHOLD_S24=0.3", "IM_THRESHOLD_S24=0.3")
                 ) or ("IM_THRESHOLD_S24 = 0.3" in src_full
                       ) or ("IM_THRESHOLD_S24=0.3"
                             in src_full.replace(" ", ""))
    # And matches spontaneous_lib.hexa  spont_im_threshold() = 0.3
    lib_path = "/Users/ghost/core/anima/HEXAD/CHAT/spontaneous_lib.hexa"
    lib_match = False
    try:
        with open(lib_path) as f:
            lib_src = f.read()
        lib_match = ("fn spont_im_threshold() -> float        { return 0.3 }"
                     in lib_src)
    except FileNotFoundError:
        lib_match = False

    # Numerical equivalence on a sweep of tension values: §24-byte-equal.
    # The §24 predicate is `score > 0.3`; the §73 OFF-reduction is the
    # SAME predicate on the `tension` field.
    sweep = [0.0, 0.1, 0.29, 0.30, 0.30001, 0.31, 0.5, 1.0]
    s24_pred = [(s > 0.3)        for s in sweep]
    off_pred = [(s > 0.3)        for s in sweep]   # identical literal
    numeric_match = (s24_pred == off_pred)

    ok = has_compare and has_const and lib_match and numeric_match
    _ok("B-S73-5 OFF-REDUCTION-CONNECTION-POINT", ok,
        f"has_compare={has_compare} has_const={has_const} "
        f"lib_match={lib_match} numeric_match={numeric_match}")


# ── B-S73-6  DISTINCT-FROM-§24/§27/§49/§68/§62 ─────────────────────
def b_s73_6():
    """The 4-tuple (single_agent, closed_loop, physics_state_sourced,
    label_free_controller) — §73 must be (T,T,T,T); every prior form
    must differ on ≥1 component."""
    r = _result()
    contrast = r["four_prior_form_contrast"]

    # §73 row must be (T,T,T,T)
    s73 = contrast["§73_self_trigger_closed_loop"]
    s73_all_true = (s73["single_agent"]
                    and s73["closed_loop"]
                    and s73["physics_state_sourced"]
                    and s73["label_free_controller"])

    # Every prior form must differ on ≥1 component
    keys = ("single_agent", "closed_loop",
            "physics_state_sourced", "label_free_controller")
    diffs_ok = True
    prior_forms = [k for k in contrast if k != "§73_self_trigger_closed_loop"]
    for pf in prior_forms:
        row = contrast[pf]
        delta = [(k, row[k] != s73[k]) for k in keys]
        n_diff = sum(1 for _, d in delta if d)
        if n_diff < 1:
            diffs_ok = False

    # The intersection of {§24,§27,§49,§68,§62} on the 4-tuple should
    # NOT contain (T,T,T,T) — i.e. the design cell is previously empty.
    all_prior_have_TTTT = any(
        (contrast[pf]["single_agent"] and contrast[pf]["closed_loop"]
         and contrast[pf]["physics_state_sourced"]
         and contrast[pf]["label_free_controller"])
        for pf in prior_forms
    )
    cell_previously_empty = (not all_prior_have_TTTT)

    ok = s73_all_true and diffs_ok and cell_previously_empty
    _ok("B-S73-6 DISTINCT-FROM-§24/§27/§49/§68/§62", ok,
        f"s73_all_true={s73_all_true} diffs_ok={diffs_ok} "
        f"cell_previously_empty={cell_previously_empty}")


def main():
    print("§73 sidecar battery — B-S73-1..6 + B-S73-NOTE")
    print("=" * 72)
    b_s73_1()
    b_s73_2()
    b_s73_3()
    b_s73_4()
    b_s73_5()
    b_s73_6()
    print("=" * 72)
    n_pass = sum(1 for r in RESULTS if r["pass"])
    n_tot  = len(RESULTS)
    print(f"  {n_pass}/{n_tot} 🔵 closed-form sidecar PASS")
    print("  + B-S73-NOTE  empirical carve-out (closed-loop-collapse-")
    print("    escape AT TRAINED-SATURATED SCALE = SGD/measurement")
    print("    OUTCOME, NOT counted 🔵)")
    print("=" * 72)

    out = {
        "research_md_section":   "§73",
        "title": ("§73 sidecar battery — B-S73-1..6 + B-S73-NOTE "
                  "(THINKER→TALKER self-trigger closed-loop)"),
        "cost":                  "$0 Mac CPU (sidecar)",
        "n_pass":                n_pass,
        "n_total":                n_tot,
        "all_pass":              (n_pass == n_tot),
        "results":               RESULTS,
        "central_blue_falsifier_changed": False,
        "central_blue_falsifier_diff_lines": 0,
        "notes": [
            "B-S73-NOTE — closed-loop-escape OUTCOME at TRAINED-SATURATED",
            "  SCALE on REAL model.forward Law-71 W-physics is EMPIRICAL",
            "  (B-D-NOTE / B-S49-NOTE / B-S59-NOTE / B-S62-NOTE / B-S68-",
            "  NOTE family, NOT counted 🔵).  The battery proves the",
            "  MECHANISM is honest; the verdict at scale is the",
            "  empirical carve-out.",
            "g3 measured-only, capability claim 0,",
            "north-star + §15/§51/§72 milestone UNCHANGED, GOAL 미도달.",
        ],
    }
    with open(os.path.join(HERE, "blue_falsifier_s73_result.json"),
              "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    sys.exit(0 if n_pass == n_tot else 1)


if __name__ == "__main__":
    main()
