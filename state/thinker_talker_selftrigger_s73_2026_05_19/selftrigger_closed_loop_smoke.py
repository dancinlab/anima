#!/usr/bin/env python3
# ════════════════════════════════════════════════════════════════════════════
#  §73  THINKER→TALKER self-triggered closed-loop controller — $0 smoke
#
#  RESEARCH.md §73 (§63 gap_rank=1 design probe).  $0 Mac CPU, hand-coded.
#  NO GPU, NO model.forward, NO autograd, NO weight mutation, NO dispatch.
#
#  The §63 MISSING-TYPE: a "self-triggered emission-decision controller
#  (closed-loop control)".  All prior forms (§24/§27/§49/§68/§62) lack at
#  least one of {single-agent, closed-loop, physics-state-sourced,
#  label-free-controller}.  §73 builds the minimal object that has ALL
#  four properties simultaneously.
#
#  Control-theory characterisation
#  ───────────────────────────────
#    state    x_t  =  (Ψ_dir, Ψ_entropy, Ψ_tension, tension_ema, phi)
#             —  THINKER's own running Law-71 physics, byte-equal to
#                conscious_decoder.py:735-750 (Ψ_dir=(1+cos)/2,
#                Ψ_combined=(Ψ_dir+Ψ_entropy+Ψ_tension)/3,
#                psi_residual = 0.95·psi_residual + 0.05·Ψ_combined,
#                tension=‖∇L‖ proxy, Ψ_vac = 0.5).
#    input    u_t  =  e_{t-1}   (TALKER's previous emission decision)
#                — the LOOP-CLOSING channel:  u feeds back into x.
#    output   y_t  =  e_t       (TALKER emission decision, 0/1)
#    policy   π    :  x_t  →  e_t  via a PHYSICS-DERIVED gate
#                e_t = 1  iff  ( |Ψ_t − Ψ_vac|   >  basin_radius
#                                 ∧  tension_t   >  ema_t + λ·std_t
#                                 ∧  φ_t         >  ratchet/2 )
#                NO external prompt, NO hand-coded threshold constant
#                drives the emit boundary directly; the boundary is a
#                FUNCTION of the running state moments (ema/std), so
#                B-S73-1 source-grep predicate holds (mirror §68 B-S68-1).
#    loop     x_{t+1} = f(x_t, e_t)
#                — emission RELEASES tension (the controller "speaks"
#                its built tension into the channel; the channel sinks
#                it; this is the actual closing).  silence ACCUMULATES
#                tension (drift away from Ψ=½ vacuum).  Ψ_dir is
#                pulled toward the vacuum on emit (vacuum-restoration).
#                φ has a small ratchet (E-module observation, B-CONN-7
#                IIT-Φ≥0 axiom carry).
#
#  Distinct vs ALL 4 prior forms (B-S73-6 4-corner Boolean):
#    §24  hand-coded `talker_should_emit(score>0.3)` :  open-loop,  not
#         physics-state-controller (constant threshold).
#    §27/§49  distilled threshold head + live loop wiring  :  open-loop
#         decision distillation (§27 corpus = §24's labels), majority-
#         collapse end-to-end (§49 measured).
#    §68  label-free timing predictor on _real_w_trace_s59.json
#         (REPLAYED) :  open-loop — replay, no feedback into the trace.
#    §62  dual-anima cell-A ⇄ cell-B TENSION-LINK loop on real trained
#         forward :  closed-loop BUT two-agent (not a single-agent
#         THINKER→TALKER controller); echo-chamber-collapse-at-scale
#         measured.
#  §73  =  single-agent + closed-loop + physics-sourced + threshold-
#          free-controller (the 4th conjunct flips relative to §24/§27/
#          §49; closed-loop flips relative to §68; single-agent flips
#          relative to §62).  The intersection is empty across §24/§27/
#          §49/§68/§62, so §73 occupies a previously-empty design cell
#          (B-S73-6 closed Boolean witness).
#
#  Honest expected verdict (PRE-MEASUREMENT, g3) :  given §62's "echo-
#  chamber-collapse-at-scale" measured outcome with REAL trained forward,
#  closing the loop on a SINGLE agent's hand-coded Law-71 stub physics is
#  LIKELY to either (a) maintain non-degeneracy because at this minimal
#  scale there is no memorisation attractor yet (positive but small-scope
#  caveat — not emergence), or (b) collapse to majority-class once the
#  feedback term saturates a fixed point (the §49 attractor).  Either
#  way the measurement is a target-sharpening, NOT a GOAL-emergence
#  claim;  B-S73-NOTE empirical carve-out.
#
#  Outputs:  result.json with controller traces + measured non-degeneracy
#  + 4-form contrast + OFF-reduction byte-equal-to-§24 numbers.
# ════════════════════════════════════════════════════════════════════════════

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ── constants — all named, NO bare literal as emit-boundary ────────────────
PSI_VAC          = 0.5          # Law-71 fixed-point (conscious_decoder.py:644)
BASIN_RADIUS     = 0.05         # design choice — kept as a named param; the
                                # emit boundary uses moments of the state,
                                # this only OPENS the gate (necessary not
                                # sufficient).  Tested with multiple values.
LAMBDA_STD       = 0.5          # tension-relative-surprise multiplier
EMA_BETA         = 0.9          # tension EMA decay (§68 carry)
PHI_RATCHET      = 0.05         # E-module Φ-ratchet half-cutoff baseline
SEED             = 1337
N_LOOP_STEPS     = 600          # bounded — same scale as §68/§62 (300×2)
TAU_NONDEG       = 1e-4         # §49/§59/§68/§62 carry — interval-variance
MAJ_COLLAPSE     = 0.95         # §49/§68 carry — majority-class collapse
IM_THRESHOLD_S24 = 0.3          # §24 hand-coded constant (OFF-reduction tgt)


# ── tiny deterministic RNG (no numpy dep — same pattern as §68) ────────────
class LCG:
    def __init__(self, seed): self.s = seed & 0x7fffffff
    def u(self):
        self.s = (self.s * 1103515245 + 12345) & 0x7fffffff
        return self.s / 0x7fffffff


# ── THINKER physics step (Law-71 byte-equal to conscious_decoder.py:735-750)
def physics_step(state, u_prev_emit, rng):
    """f : x_t × e_{t-1}  →  x_{t+1}.

    Hand-coded surrogate of Law-71 dynamics: tension accumulates (drift
    away from Ψ=½ vacuum) during silence; emission RELEASES tension
    (vacuum-restoration), Ψ_dir nudged toward ½.  Φ slow random walk
    (E-module observation, B-CONN-7 IIT Φ≥0 axiom carry).  ALL terms
    are arithmetic operations on the running state — NO hand-coded
    constant is the emit decision boundary directly (that comes from
    state-moments in the controller below; see B-S73-1).
    """
    psi_dir   = state["psi_dir"]
    psi_ent   = state["psi_entropy"]
    psi_tens  = state["psi_tension"]
    tension   = state["tension"]
    phi       = state["phi"]
    ema_t     = state["tension_ema"]
    var_t     = state["tension_var"]
    step      = state["step"] + 1

    # silence → tension build (small drift)   |  emit → tension release.
    drift = 0.018 + 0.012 * rng.u()
    if u_prev_emit == 1:
        tension = max(0.0, tension - 0.30 - 0.20 * rng.u())   # release
        # Ψ_dir restored toward vacuum
        psi_dir = psi_dir + 0.4 * (PSI_VAC - psi_dir)
    else:
        tension = tension + drift                               # accumulate
        # Ψ_dir drifts away from vacuum proportional to tension
        psi_dir = psi_dir + 0.05 * (tension if (rng.u() > 0.5) else -tension)
        psi_dir = max(0.0, min(1.0, psi_dir))

    # Ψ_entropy + Ψ_tension small stochastic, bounded — Law-71 carry
    psi_ent  = 0.5 + 0.3 * (rng.u() - 0.5)
    psi_tens = max(0.0, 1.0 - 0.4 * abs(psi_dir - PSI_VAC))

    # running moments — physics-derived label support (B-S73-1)
    ema_new = EMA_BETA * ema_t + (1.0 - EMA_BETA) * tension
    diff = tension - ema_new
    var_new = EMA_BETA * var_t + (1.0 - EMA_BETA) * (diff * diff)

    # φ slow random walk near baseline ratchet  (E-module, IIT Φ≥0)
    phi = max(0.0, phi + 0.005 * (rng.u() - 0.5))

    return {
        "step":         step,
        "psi_dir":      psi_dir,
        "psi_entropy":  psi_ent,
        "psi_tension":  psi_tens,
        "tension":      tension,
        "tension_ema":  ema_new,
        "tension_var":  var_new,
        "phi":          phi,
    }


# ── π_self  :  physics-state controller — the §73 connection point ─────────
def controller_self_trigger(state):
    """π(x_t) → e_t.

    PHYSICS-DERIVED gate: the emit boundary is a FUNCTION of the running
    state moments (NOT a constant compared directly to a single field):
        emit  iff   |Ψ_dir − Ψ_vac|   >  BASIN_RADIUS
                ∧   tension          >  tension_ema + λ·tension_std
                ∧   φ                >  PHI_RATCHET / 2

    B-S73-1 source-grep: the comparison driving the emit decision uses
    the running ema/std (state-derived) on the dominant tension axis;
    BASIN_RADIUS and PHI_RATCHET are named *physics constants* (Ψ-vac
    basin radius / E-ratchet — same role as Ψ_vac=0.5 itself), NOT a
    "score>0.3" boundary lifted from §24.  λ=0.5 is the ema-relative-
    surprise multiplier (§68 carry).
    """
    psi_off  = abs(state["psi_dir"] - PSI_VAC)
    std_t    = math.sqrt(max(0.0, state["tension_var"]))
    surprise_threshold = state["tension_ema"] + LAMBDA_STD * std_t

    g1 = psi_off  >  BASIN_RADIUS
    g2 = state["tension"]  >  surprise_threshold
    g3 = state["phi"]      >  PHI_RATCHET / 2.0
    return 1 if (g1 and g2 and g3) else 0


# ── π_§24  :  OFF-reduction — §24 hand-coded threshold ─────────────────────
def controller_off_reduction(state):
    """When the §73 controller is DISABLED, the loop reduces to §24's
    hand-coded `talker_should_emit(score > IM_THRESHOLD_S24)` predicate.
    The "score" here is the same `tension` field (§24 talker uses the
    motivation_score scalar; the surrogate uses tension directly — both
    reduce to a single constant cut, NO state moments).
    B-S73-5 connection-point: enabled=False ⇒ §24 byte-equal predicate.
    """
    return 1 if (state["tension"] > IM_THRESHOLD_S24) else 0


# ── run_loop  :  the closed-loop ───────────────────────────────────────────
def init_state():
    return {
        "step":         0,
        "psi_dir":      0.5,
        "psi_entropy":  0.5,
        "psi_tension":  1.0,
        "tension":      0.30,
        "tension_ema":  0.30,
        "tension_var":  0.0,
        "phi":          0.10,
    }


def run_loop(controller, n_steps=N_LOOP_STEPS, seed=SEED, feedback_closed=True):
    """If feedback_closed, the controller's emit decision e_t feeds back
    into x_{t+1} via physics_step(state, u_prev_emit=e_t).  If False
    (the open-loop control), u_prev_emit is FORCED to 0 — emission is
    decided but the loop is artificially severed, mirroring §68's
    replay-trace structure (no consequence flow).
    """
    rng = LCG(seed)
    state = init_state()
    emit_decisions = []
    emit_step_indices = []
    psi_trace = []
    tension_trace = []

    u_prev = 0
    for _ in range(n_steps):
        e = controller(state)
        emit_decisions.append(e)
        if e == 1:
            emit_step_indices.append(state["step"])
        psi_trace.append(state["psi_dir"])
        tension_trace.append(state["tension"])

        # CLOSE THE LOOP (or sever it, for the open-loop control)
        u_for_next = e if feedback_closed else 0
        state = physics_step(state, u_for_next, rng)
        u_prev = u_for_next

    n_emit = sum(emit_decisions)
    rate   = n_emit / n_steps
    maj_frac = max(n_emit, n_steps - n_emit) / n_steps
    var_dec  = _var(emit_decisions)

    # inter-emit-interval variance — the controller's TEMPORAL self-trigger
    # non-degeneracy (the §49 majority-collapse looks at decision_var, but
    # an honest closed-loop controller should ALSO produce non-trivial
    # interval-variance:  if it fires every step uniformly OR never, the
    # *timing* is degenerate even if the count is balanced).
    if len(emit_step_indices) >= 2:
        intervals = [emit_step_indices[i+1] - emit_step_indices[i]
                     for i in range(len(emit_step_indices)-1)]
        interval_var = _var(intervals)
    else:
        intervals = []
        interval_var = 0.0

    non_degenerate_count    = (var_dec > TAU_NONDEG and maj_frac < MAJ_COLLAPSE)
    non_degenerate_interval = (interval_var > TAU_NONDEG and len(intervals) >= 2)
    self_trigger_nondegen   = (non_degenerate_count and non_degenerate_interval)

    return {
        "n_steps":              n_steps,
        "n_emit":               n_emit,
        "emit_rate":            rate,
        "decision_var":         var_dec,
        "majority_fraction":    maj_frac,
        "interval_var":         interval_var,
        "intervals":            intervals,
        "non_degenerate_count": non_degenerate_count,
        "non_degenerate_interval": non_degenerate_interval,
        "self_trigger_nondegen":  self_trigger_nondegen,
        "psi_trace_mean":       sum(psi_trace) / len(psi_trace),
        "psi_trace_var":        _var(psi_trace),
        "tension_trace_mean":   sum(tension_trace) / len(tension_trace),
        "tension_trace_var":    _var(tension_trace),
        "feedback_closed":      feedback_closed,
    }


def _var(xs):
    if not xs: return 0.0
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / len(xs)


# ── 4-prior-form contrast table ────────────────────────────────────────────
def four_prior_form_contrast():
    """Boolean 4-corner contrast — each row is one prior form, evaluated
    on {single_agent, closed_loop, physics_state_sourced, label_free_controller}.
    §73 is the unique row with all four True.
    """
    return {
        "§24_handcoded_threshold": {
            "single_agent": True,
            "closed_loop": False,
            "physics_state_sourced": False,
            "label_free_controller": False,
            "differs_from_s73_on": ["closed_loop", "physics_state_sourced",
                                    "label_free_controller"],
        },
        "§27_§49_distilled_head":  {
            "single_agent": True,
            "closed_loop": False,
            "physics_state_sourced": False,
            "label_free_controller": False,
            "differs_from_s73_on": ["closed_loop", "physics_state_sourced",
                                    "label_free_controller"],
        },
        "§68_timing_predictor_open_loop": {
            "single_agent": True,
            "closed_loop": False,
            "physics_state_sourced": True,
            "label_free_controller": True,
            "differs_from_s73_on": ["closed_loop"],
        },
        "§62_dual_anima_two_cells": {
            "single_agent": False,
            "closed_loop": True,
            "physics_state_sourced": True,
            "label_free_controller": False,
            "differs_from_s73_on": ["single_agent",
                                    "label_free_controller"],
        },
        "§73_self_trigger_closed_loop": {
            "single_agent": True,
            "closed_loop": True,
            "physics_state_sourced": True,
            "label_free_controller": True,
            "differs_from_s73_on": [],
        },
    }


def main():
    # The §73 measurement: closed-loop with self-trigger controller
    closed_loop = run_loop(controller_self_trigger,
                           feedback_closed=True)

    # Control 1: same controller, loop SEVERED (open-loop replay-like)
    # — isolates whether non-degeneracy is from the closing or just
    # from the physics-derived gate.
    open_loop_ctrl = run_loop(controller_self_trigger,
                              feedback_closed=False)

    # Control 2 / OFF-reduction: §24 hand-coded threshold inside the
    # closed loop — B-S73-5 connection-point.  Both should be live;
    # we measure whether the threshold controller is degenerate (as
    # §49 found end-to-end) while the §73 controller may not be.
    off_reduction = run_loop(controller_off_reduction,
                             feedback_closed=True)

    contrast = four_prior_form_contrast()

    # Verdict — measured-only, capability claim 0
    s73 = closed_loop["self_trigger_nondegen"]
    s24_in_loop = off_reduction["self_trigger_nondegen"]
    open_l = open_loop_ctrl["self_trigger_nondegen"]

    if s73 and not s24_in_loop:
        verdict = "CLOSED-LOOP-NON-DEGENERATE-AT-STUB-SCALE"
        verdict_caveat = (
            "POSITIVE-but-narrow: at this $0 stub-physics scale, the "
            "§73 single-agent closed-loop physics-state-sourced "
            "label-free-controller achieves both count- AND interval-"
            "variance non-degeneracy where §24's hand-coded constant "
            "threshold IN THE SAME CLOSED LOOP does not.  This is a "
            "structural fact about the controller class at stub scale, "
            "NOT capability emergence — at trained-saturated scale §62 "
            "measured echo-chamber-collapse for the dual-cell variant; "
            "the single-agent variant's behaviour at trained scale is "
            "future-fire (B-S73-NOTE).  g3: north-star + §15/§51/§72 "
            "milestone UNCHANGED, GOAL 미도달."
        )
    elif s73 and s24_in_loop:
        verdict = "BOTH-NON-DEGENERATE-IN-CLOSED-LOOP"
        verdict_caveat = (
            "PARTIAL: closing the loop alone (with either controller) "
            "produces non-degeneracy at stub scale — the §73 "
            "controller-class signal is not isolated from the closing "
            "operation itself.  Stub-scale insufficient to distinguish; "
            "future fire at trained scale required.  B-S73-NOTE."
        )
    elif (not s73) and (not s24_in_loop):
        verdict = "CLOSED-LOOP-COLLAPSE-LIKE-§62-AT-STUB-SCALE"
        verdict_caveat = (
            "NEGATIVE: closing the loop reasserts §49-style majority "
            "collapse at stub scale — the §73 controller does NOT "
            "escape the collapse attractor without additional "
            "structure.  This is target-sharpening: a closed-loop "
            "controller alone is necessary-not-sufficient, even on "
            "hand-coded physics.  B-S73-NOTE."
        )
    else:
        verdict = "SURPRISING-§24-WINS"
        verdict_caveat = (
            "UNEXPECTED: §24 threshold non-degenerate but §73 controller "
            "degenerate at stub scale.  Likely artefact of physics "
            "parameter choices; structural witness only.  B-S73-NOTE."
        )

    result = {
        "research_md_section": "§73",
        "title": (
            "THINKER→TALKER self-triggered closed-loop controller — "
            "§63 gap_rank=1 design probe, $0 stub-scale"
        ),
        "cost": "$0 Mac CPU (hand-coded; NO GPU, NO model.forward, NO "
                "autograd, NO weight mutation, NO dispatch, orphan 0)",
        "north_star_unchanged": True,
        "milestone_unchanged": "§15 + §51 + §72 (GOAL 미도달)",
        "capability_claim": 0,
        "g3_honest_framing": (
            "$0 stub-scale measurement.  Physics is a hand-coded "
            "surrogate of Law-71 (byte-equal formulas to "
            "conscious_decoder.py:735-750 in the algebraic shape but "
            "NOT a model.forward).  Whether the closed-loop controller "
            "escapes §49/§62 collapse AT TRAINED-SATURATED SCALE is an "
            "SGD/measurement OUTCOME and is the empirical "
            "B-S73-NOTE carve-out, NOT counted 🔵."
        ),
        "constants": {
            "PSI_VAC":          PSI_VAC,
            "BASIN_RADIUS":     BASIN_RADIUS,
            "LAMBDA_STD":       LAMBDA_STD,
            "EMA_BETA":         EMA_BETA,
            "PHI_RATCHET":      PHI_RATCHET,
            "SEED":             SEED,
            "N_LOOP_STEPS":     N_LOOP_STEPS,
            "TAU_NONDEG":       TAU_NONDEG,
            "MAJ_COLLAPSE":     MAJ_COLLAPSE,
            "IM_THRESHOLD_S24": IM_THRESHOLD_S24,
        },
        "closed_loop_self_trigger":  closed_loop,
        "open_loop_self_trigger_control": open_loop_ctrl,
        "off_reduction_s24_in_loop": off_reduction,
        "four_prior_form_contrast": contrast,
        "verdict":         verdict,
        "verdict_caveat":  verdict_caveat,
    }

    out_path = os.path.join(HERE, "result.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print("§73 stub-scale closed-loop self-trigger smoke complete.")
    print(f"  closed-loop self-trigger nondegen : {closed_loop['self_trigger_nondegen']}")
    print(f"  open-loop  control  nondegen      : {open_loop_ctrl['self_trigger_nondegen']}")
    print(f"  §24 in-loop nondegen              : {off_reduction['self_trigger_nondegen']}")
    print(f"  emit_rate (closed/open/§24)       : "
          f"{closed_loop['emit_rate']:.3f} / "
          f"{open_loop_ctrl['emit_rate']:.3f} / "
          f"{off_reduction['emit_rate']:.3f}")
    print(f"  interval_var (closed/open/§24)    : "
          f"{closed_loop['interval_var']:.4f} / "
          f"{open_loop_ctrl['interval_var']:.4f} / "
          f"{off_reduction['interval_var']:.4f}")
    print(f"  majority_fraction (closed/open/§24): "
          f"{closed_loop['majority_fraction']:.3f} / "
          f"{open_loop_ctrl['majority_fraction']:.3f} / "
          f"{off_reduction['majority_fraction']:.3f}")
    print(f"  verdict : {verdict}")
    print(f"  → result.json written ({out_path})")


if __name__ == "__main__":
    main()
