#!/usr/bin/env python3
# ════════════════════════════════════════════════════════════════════════════
#  §75  Controller-class sub-axis decomposition — $0 Mac CPU
#
#  RESEARCH.md §75 (earned by §73-FIRE C3#6: SEVER-FEEDBACK also non-degen,
#  so loop-closing is NOT isolated; the "physics-state-sourced controller
#  class" itself is the load-bearing signal vs §24 majority-collapse).
#
#  §75 decomposes "physics-state-sourced" into 3 distinguishable properties
#  and runs a 4-cell grid in the SAME closed-loop infrastructure as §73
#  (byte-equal port of physics_step + run_loop) to identify the load-bearing
#  sub-axis.
#
#  3 properties:
#    A  STATE-DERIVED   :  controller INPUT is the running state tuple
#                           (Ψ_dir, tension, φ)  vs.  a single scalar.
#    B  MOMENT-BASED    :  boundary is a STATISTIC of state
#                           (tension_ema + λ·tension_std)  vs.  a fixed
#                           scalar value compared directly to a field.
#    C  TIME-VARYING    :  that statistic UPDATES per step from fresh state
#                           vs.  computed once over a warmup window then
#                           HELD constant for the rest of the run.
#
#  4 cells:
#    cell0  §24-baseline  :  ¬A ¬B ¬C   tension > 0.3                 (control)
#    cell1  §73-A-only    :   A ¬B ¬C   gate uses state tuple INPUT but
#                                       compared to FROZEN scalar
#                                       (warmup-mean of tension).
#    cell2  §73-AB        :   A  B ¬C   state inputs, MOMENT-BASED boundary
#                                       (ema+λstd) but FROZEN after warmup
#                                       (held constant for steps>warmup_n).
#    cell3  §73-ABC       :   A  B  C   full §73 controller (byte-equal port
#                                       of state/thinker_talker_selftrigger_
#                                       s73_2026_05_19/selftrigger_closed_
#                                       loop_smoke.py:controller_self_trigger).
#
#  All 4 cells share IDENTICAL physics_step / run_loop / init_state / LCG /
#  constants — byte-equal port from §73 stub (B-S75-5 structural).  Only the
#  controller-gate function differs.
#
#  Honest predictions registered AHEAD of measurement (g3):
#    cell0  expected COLLAPSE     (control — re-confirm §73 stub §24-in-loop
#                                  shape; §73 stub measured int_var=0.47
#                                  ON but B-S73 augmented predicate evaluates
#                                  also against MAJ_COLLAPSE).
#    cell3  expected NON-DEGEN    (re-confirm §73 stub baseline 35.02).
#    cell1, cell2  =  the OPEN question.  Three honest verdict buckets:
#      (a) Full ABC required  ⇒  cell1 + cell2 both collapse → lever is
#          irreducible; the FULL physics-state-sourced statistic IS the
#          load-bearing unit (NOT decomposable).
#      (b) A-only sufficient  ⇒  cell1 survives → lever is mere state-
#          derivation; B and C are not independently load-bearing.
#      (c) AB needed but not C ⇒  cell2 survives but cell1 collapses →
#          state-derivation + moment-basedness suffice; time-variance is
#          not independently load-bearing.
#      (d) Partial / mixed.
#
#  Outputs:  result.json with the 4-cell decomposition table + each cell's
#  full augmented-predicate measurement + the load-bearing-sub-axis verdict.
#
#  $0  Mac CPU local · NO GPU · NO model.forward · NO autograd · NO dispatch
#       · orphan 0 · g_clm_from_scratch unaffected (no training) ·
#       g_fire_autonomous unaffected (no fire).
# ════════════════════════════════════════════════════════════════════════════

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ── constants — byte-equal to §73 stub ─────────────────────────────────────
PSI_VAC          = 0.5
BASIN_RADIUS     = 0.05
LAMBDA_STD       = 0.5
EMA_BETA         = 0.9
PHI_RATCHET      = 0.05
SEED             = 1337
N_LOOP_STEPS     = 600
TAU_NONDEG       = 1e-4
MAJ_COLLAPSE     = 0.95
IM_THRESHOLD_S24 = 0.3

# ── §75 NEW: warmup window for cell1 + cell2 (frozen moments captured here)
#  N_WARMUP = 100 ≈ 1/6 of N_LOOP_STEPS — long enough that LCG-driven drift
#  has built a non-trivial tension trace; short enough that 5/6 of the run
#  uses the FROZEN moment.  This is the same shape as §16-FIRE's "first
#  forward batch is the seed" pattern but inverted: the warmup CAPTURES the
#  moment, then the rest of the run HOLDS it (NOT updates it).
N_WARMUP         = 100


# ── tiny deterministic RNG — byte-equal to §73 stub ────────────────────────
class LCG:
    def __init__(self, seed): self.s = seed & 0x7fffffff
    def u(self):
        self.s = (self.s * 1103515245 + 12345) & 0x7fffffff
        return self.s / 0x7fffffff


# ── THINKER physics step — byte-equal to §73 stub ──────────────────────────
def physics_step(state, u_prev_emit, rng):
    """f : x_t × e_{t-1}  →  x_{t+1}.   BYTE-EQUAL to §73 stub's physics_step.
    """
    psi_dir   = state["psi_dir"]
    psi_ent   = state["psi_entropy"]
    psi_tens  = state["psi_tension"]
    tension   = state["tension"]
    phi       = state["phi"]
    ema_t     = state["tension_ema"]
    var_t     = state["tension_var"]
    step      = state["step"] + 1

    drift = 0.018 + 0.012 * rng.u()
    if u_prev_emit == 1:
        tension = max(0.0, tension - 0.30 - 0.20 * rng.u())
        psi_dir = psi_dir + 0.4 * (PSI_VAC - psi_dir)
    else:
        tension = tension + drift
        psi_dir = psi_dir + 0.05 * (tension if (rng.u() > 0.5) else -tension)
        psi_dir = max(0.0, min(1.0, psi_dir))

    psi_ent  = 0.5 + 0.3 * (rng.u() - 0.5)
    psi_tens = max(0.0, 1.0 - 0.4 * abs(psi_dir - PSI_VAC))

    ema_new = EMA_BETA * ema_t + (1.0 - EMA_BETA) * tension
    diff = tension - ema_new
    var_new = EMA_BETA * var_t + (1.0 - EMA_BETA) * (diff * diff)

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


# ── cell0  §24-baseline  :  ¬A ¬B ¬C  ──────────────────────────────────────
#  Input is single scalar (tension), boundary is fixed constant (0.3) — NO
#  state-derivation, NO moments, NO time-variance.  Byte-equal to §73 stub's
#  `controller_off_reduction`.
def make_controller_cell0_baseline():
    def controller(state, frozen=None):
        return 1 if (state["tension"] > IM_THRESHOLD_S24) else 0
    return controller, {"freeze_after_warmup": False, "needs_warmup": False}


# ── cell1  §73-A-only  :   A ¬B ¬C  ────────────────────────────────────────
#  Input IS the state tuple (Ψ_dir, tension, φ) — but the boundary is a
#  FROZEN SCALAR (warmup-mean of tension), NOT a moment combination.  This
#  isolates "STATE-DERIVED inputs" alone.
def make_controller_cell1_A_only(frozen_scalar):
    def controller(state, frozen=None):
        # STATE-DERIVED:  uses Ψ_dir / tension / φ  (full state tuple)
        psi_off = abs(state["psi_dir"] - PSI_VAC)
        g1 = psi_off > BASIN_RADIUS                       # state input
        g2 = state["tension"] > frozen_scalar             # frozen SCALAR — not moment
        g3 = state["phi"]    > PHI_RATCHET / 2.0          # state input
        return 1 if (g1 and g2 and g3) else 0
    return controller, {"freeze_after_warmup": True, "needs_warmup": True,
                        "what_freezes": "scalar (warmup-mean of tension)"}


# ── cell2  §73-AB  :   A  B ¬C  ────────────────────────────────────────────
#  Input IS state tuple, boundary IS a MOMENT (ema + λ·std) — but the
#  moment is computed ONCE over the warmup window and HELD CONSTANT for
#  the rest of the run.  Time-variance is removed; state-derivation +
#  moment-basedness are preserved.
def make_controller_cell2_AB(frozen_ema, frozen_std):
    frozen_threshold = frozen_ema + LAMBDA_STD * frozen_std
    def controller(state, frozen=None):
        psi_off = abs(state["psi_dir"] - PSI_VAC)
        g1 = psi_off > BASIN_RADIUS                       # state input
        g2 = state["tension"] > frozen_threshold          # frozen MOMENT
        g3 = state["phi"]    > PHI_RATCHET / 2.0          # state input
        return 1 if (g1 and g2 and g3) else 0
    return controller, {"freeze_after_warmup": True, "needs_warmup": True,
                        "what_freezes": "moment (ema + λ·std at end of warmup)",
                        "frozen_threshold": frozen_threshold}


# ── cell3  §73-ABC  :   A  B  C  ───────────────────────────────────────────
#  Full §73 controller — byte-equal port of §73 stub's controller_self_trigger.
def make_controller_cell3_ABC():
    def controller(state, frozen=None):
        psi_off = abs(state["psi_dir"] - PSI_VAC)
        std_t   = math.sqrt(max(0.0, state["tension_var"]))
        surprise_threshold = state["tension_ema"] + LAMBDA_STD * std_t
        g1 = psi_off > BASIN_RADIUS
        g2 = state["tension"] > surprise_threshold
        g3 = state["phi"]    > PHI_RATCHET / 2.0
        return 1 if (g1 and g2 and g3) else 0
    return controller, {"freeze_after_warmup": False, "needs_warmup": False}


# ── _var  :  byte-equal to §73 stub ────────────────────────────────────────
def _var(xs):
    if not xs: return 0.0
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / len(xs)


# ── warmup pass — captures tension series under a no-emit drift, computes
#   the moment(s) that cell1/cell2 will FREEZE.  Uses a separate RNG seeded
#   identically to the main run so the warmup is deterministic and shares
#   the same drift shape that the main run starts with.
def warmup_capture(n=N_WARMUP, seed=SEED):
    rng = LCG(seed)
    state = init_state()
    tensions = []
    for _ in range(n):
        tensions.append(state["tension"])
        state = physics_step(state, 0, rng)   # no-emit warmup
    mean_t = sum(tensions) / len(tensions)
    var_t  = _var(tensions)
    std_t  = math.sqrt(max(0.0, var_t))
    return {
        "n_warmup":     n,
        "tension_mean": mean_t,
        "tension_var":  var_t,
        "tension_std":  std_t,
        "ema_at_warmup_end": state["tension_ema"],
        "var_at_warmup_end": state["tension_var"],
    }


# ── run_loop — same closed-loop infra as §73 stub.  feedback_closed=True
#   for §75 (all 4 cells run in the same closing topology so the only
#   variable IS the controller-gate function — fair-compare by construction).
def run_loop(controller, n_steps=N_LOOP_STEPS, seed=SEED):
    rng = LCG(seed)
    state = init_state()
    emit_decisions = []
    emit_step_indices = []
    psi_trace = []
    tension_trace = []

    for _ in range(n_steps):
        e = controller(state)
        emit_decisions.append(e)
        if e == 1:
            emit_step_indices.append(state["step"])
        psi_trace.append(state["psi_dir"])
        tension_trace.append(state["tension"])
        state = physics_step(state, e, rng)        # CLOSE THE LOOP

    n_emit = sum(emit_decisions)
    rate = n_emit / n_steps
    maj_frac = max(n_emit, n_steps - n_emit) / n_steps
    var_dec = _var(emit_decisions)

    if len(emit_step_indices) >= 2:
        intervals = [emit_step_indices[i+1] - emit_step_indices[i]
                     for i in range(len(emit_step_indices)-1)]
        interval_var = _var(intervals)
    else:
        intervals = []
        interval_var = 0.0

    # B-S73 augmented predicate (byte-equal):
    #   count_var > τ ∧ maj_frac < 0.95 ∧ interval_var > τ ∧ ≥2 emits
    non_deg_count    = (var_dec > TAU_NONDEG and maj_frac < MAJ_COLLAPSE)
    non_deg_interval = (interval_var > TAU_NONDEG and len(intervals) >= 2)
    non_degenerate   = (non_deg_count and non_deg_interval)

    return {
        "n_steps":              n_steps,
        "n_emit":               n_emit,
        "emit_rate":            rate,
        "decision_var":         var_dec,
        "majority_fraction":    maj_frac,
        "interval_var":         interval_var,
        "n_intervals":          len(intervals),
        "non_deg_count":        non_deg_count,
        "non_deg_interval":     non_deg_interval,
        "non_degenerate":       non_degenerate,
        "psi_trace_mean":       sum(psi_trace) / len(psi_trace),
        "psi_trace_var":        _var(psi_trace),
        "tension_trace_mean":   sum(tension_trace) / len(tension_trace),
        "tension_trace_var":    _var(tension_trace),
    }


def main():
    # 1.  Warmup pass — capture the frozen moments for cell1/cell2.
    wu = warmup_capture()

    # 2.  Build controllers, RUN each in same closed-loop infra.
    c0, info0 = make_controller_cell0_baseline()
    c1, info1 = make_controller_cell1_A_only(frozen_scalar=wu["tension_mean"])
    c2, info2 = make_controller_cell2_AB(
        frozen_ema=wu["ema_at_warmup_end"],
        frozen_std=math.sqrt(max(0.0, wu["var_at_warmup_end"])),
    )
    c3, info3 = make_controller_cell3_ABC()

    r0 = run_loop(c0)
    r1 = run_loop(c1)
    r2 = run_loop(c2)
    r3 = run_loop(c3)

    # 3.  Sanity gate — §24-baseline MUST collapse for the decomposition to
    #     be valid (B-S75-4).  If r0 is non-degen, the closed-loop topology
    #     itself is already disrupting the §24 boundary in a way that
    #     wasn't true at §73-FIRE trained scale — the stub scale's §24
    #     emit_rate WAS already lower (0.07) than trained-scale (1.00), so
    #     the augmented predicate may evaluate True on a different
    #     mechanism.  Report TRUTHFULLY; verdict logic accounts for it.
    s24_collapsed_as_expected = (not r0["non_degenerate"]) or \
                                (r0["majority_fraction"] >= 0.95)

    # 4.  Decomposition verdict (g3 — read off measured outcomes).
    abc = r3["non_degenerate"]
    ab  = r2["non_degenerate"]
    a   = r1["non_degenerate"]
    s24 = r0["non_degenerate"]

    # Verdict bucket logic
    if abc and not ab and not a:
        load_bearing = "FULL-ABC-IRREDUCIBLE"
        verdict_note = (
            "Only the FULL time-varying state-moment statistic survives. "
            "A-only AND AB both collapse like §24. The lever is "
            "irreducible: physics-state-sourced controller class IS a "
            "tight conjunction of all 3 properties; the unit is not "
            "decomposable.  Refines §73-FIRE's mechanism reframe: the "
            "load-bearing sub-axis is the FULL combination, not any "
            "single property.  (Verdict bucket (a))"
        )
    elif a and not s24:
        load_bearing = "A-ONLY-SUFFICIENT"
        verdict_note = (
            "Mere STATE-DERIVATION of the controller inputs (A) is "
            "sufficient for non-degeneracy; B and C are not independently "
            "load-bearing at this scale.  §73-FIRE's mechanism reframe "
            "refines further: physics-state-AS-INPUT is the lever, the "
            "specific statistic form (moment vs scalar, frozen vs running) "
            "is not load-bearing.  (Verdict bucket (b))"
        )
    elif ab and not a and not s24:
        load_bearing = "AB-NEEDED-NOT-C"
        verdict_note = (
            "STATE-DERIVATION + MOMENT-BASEDNESS together suffice for "
            "non-degeneracy; TIME-VARIANCE (C) is not independently "
            "load-bearing.  Loop-closing-like reframe at the controller "
            "level: a frozen moment-based boundary works.  (Verdict "
            "bucket (c))"
        )
    elif abc and ab and a and s24:
        load_bearing = "ALL-CELLS-NONDEG-AT-STUB-SCALE-INDETERMINATE"
        verdict_note = (
            "Every cell INCLUDING §24-baseline reaches the B-S73 augmented "
            "non-degeneracy predicate at this $0 stub scale.  Stub scale "
            "insufficient to distinguish sub-axes: §73-FIRE's trained "
            "scale was where §24 collapsed (interval_var 0.00); §75 stub "
            "scale's §24 already had interval_var 0.47.  Trained-scale "
            "re-run required (B-S75-NOTE).  Mixed verdict (d), "
            "INDETERMINATE-AT-STUB-SCALE sub-case."
        )
    else:
        load_bearing = "PARTIAL-OR-MIXED"
        verdict_note = (
            f"Mixed pattern not in the canonical buckets: "
            f"§24={s24}, A-only={a}, AB={ab}, ABC={abc}.  "
            "Verdict bucket (d).  See decomposition_table for raw numbers."
        )

    # 5.  Decomposition table — the §75 deliverable.
    decomp_table = {
        "cell0_§24_baseline_no_A_no_B_no_C": {
            "controller_class":     "§24 hand-coded constant scalar threshold",
            "A_state_derived":      False,
            "B_moment_based":       False,
            "C_time_varying":       False,
            "what_freezes":         "n/a — no moments at all",
            "emit_rate":            r0["emit_rate"],
            "majority_fraction":    r0["majority_fraction"],
            "interval_var":         r0["interval_var"],
            "n_intervals":          r0["n_intervals"],
            "non_degenerate":       r0["non_degenerate"],
            "raw":                  r0,
        },
        "cell1_§73_A_only":  {
            "controller_class":     "state tuple inputs, FROZEN scalar threshold (warmup-mean of tension)",
            "A_state_derived":      True,
            "B_moment_based":       False,
            "C_time_varying":       False,
            "what_freezes":         info1["what_freezes"],
            "frozen_scalar_value":  wu["tension_mean"],
            "emit_rate":            r1["emit_rate"],
            "majority_fraction":    r1["majority_fraction"],
            "interval_var":         r1["interval_var"],
            "n_intervals":          r1["n_intervals"],
            "non_degenerate":       r1["non_degenerate"],
            "raw":                  r1,
        },
        "cell2_§73_AB":       {
            "controller_class":     "state tuple inputs, FROZEN moment (ema+λstd captured at end of warmup, HELD)",
            "A_state_derived":      True,
            "B_moment_based":       True,
            "C_time_varying":       False,
            "what_freezes":         info2["what_freezes"],
            "frozen_threshold":     info2["frozen_threshold"],
            "emit_rate":            r2["emit_rate"],
            "majority_fraction":    r2["majority_fraction"],
            "interval_var":         r2["interval_var"],
            "n_intervals":          r2["n_intervals"],
            "non_degenerate":       r2["non_degenerate"],
            "raw":                  r2,
        },
        "cell3_§73_ABC_full": {
            "controller_class":     "full §73 controller — running ema/std updated per step (byte-equal port of §73 stub controller_self_trigger)",
            "A_state_derived":      True,
            "B_moment_based":       True,
            "C_time_varying":       True,
            "what_freezes":         "nothing — moment updates each step from fresh state",
            "emit_rate":            r3["emit_rate"],
            "majority_fraction":    r3["majority_fraction"],
            "interval_var":         r3["interval_var"],
            "n_intervals":          r3["n_intervals"],
            "non_degenerate":       r3["non_degenerate"],
            "raw":                  r3,
        },
    }

    result = {
        "research_md_section": "§75",
        "title": ("Controller-class sub-axis decomposition — §73-FIRE "
                  "C3#6 earned (which property of physics-state-sourced "
                  "is load-bearing?)"),
        "cost": "$0 Mac CPU local (hand-coded; NO GPU, NO model.forward, "
                "NO autograd, NO weight mutation, NO dispatch, orphan 0)",
        "north_star_unchanged": True,
        "milestone_unchanged": "§15 + §51 + §72 (GOAL 미도달)",
        "capability_claim": 0,
        "g3_honest_framing": (
            "§75 = mechanism-property identification at $0 stub scale.  "
            "The decomposition isolates WHICH sub-axis (A state-derivation, "
            "B moment-basedness, C time-variance) survives where §24 "
            "constant-scalar fails.  Stub-scale §24 is itself a different "
            "regime from §73-FIRE's trained-scale §24 (interval_var 0.47 "
            "vs 0.00 collapse), so the augmented predicate may evaluate "
            "True for §24-baseline at stub scale — this is reported "
            "truthfully and the verdict accounts for it.  Trained-scale "
            "validation of the load-bearing sub-axis is empirical "
            "future-fire (B-S75-NOTE)."
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
            "N_WARMUP":         N_WARMUP,
        },
        "warmup_capture":               wu,
        "decomposition_table":          decomp_table,
        "s24_collapsed_as_expected":    s24_collapsed_as_expected,
        "load_bearing_sub_axis":        load_bearing,
        "verdict_note":                 verdict_note,
        "s73_stub_reference": {
            "closed_loop_int_var":      35.0229,
            "off_reduction_int_var":    0.4739,
            "verdict":                  "BOTH-NON-DEGENERATE-IN-CLOSED-LOOP",
        },
        "s73_fire_reference": {
            "closed_loop_int_var":      38.0699,
            "sever_feedback_int_var":   57.0491,
            "off_reduction_int_var":    0.0,
            "off_reduction_emit_rate":  1.0,
            "verdict":                  "CONTROLLER-SURVIVES-AT-TRAINED-SCALE",
        },
    }

    out_path = os.path.join(HERE, "result.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("§75 controller-class sub-axis decomposition complete.")
    print(f"  warmup tension_mean = {wu['tension_mean']:.4f}, std = {wu['tension_std']:.4f}")
    print()
    print(f"  {'cell':<25s} {'emit_rate':>10s} {'maj_frac':>10s} {'int_var':>10s} {'nondeg':>8s}")
    print(f"  {'-'*25:<25s} {'-'*10:>10s} {'-'*10:>10s} {'-'*10:>10s} {'-'*8:>8s}")
    for name, row in decomp_table.items():
        print(f"  {name:<25s} "
              f"{row['emit_rate']:>10.4f} "
              f"{row['majority_fraction']:>10.4f} "
              f"{row['interval_var']:>10.4f} "
              f"{str(row['non_degenerate']):>8s}")
    print()
    print(f"  load-bearing sub-axis : {load_bearing}")
    print(f"  s24 collapsed as expected : {s24_collapsed_as_expected}")
    print(f"  → result.json written ({out_path})")


if __name__ == "__main__":
    main()
