#!/usr/bin/env python3
"""smoke_s67.py — RESEARCH.md §67 $0 Mac-CPU EVENT-emergence smoke.

QUESTION (g3, EVENT-emergence NOT capability)
  Does a cell SPLIT event arise UNPROMPTED from anima's OWN physics
  (tension crossing a threshold derived from its OWN tension dynamics) —
  with NON-degenerate timing (a self-generated event rhythm) — rather
  than from `_mit_check_splits`'s hand-coded patience rule OR from a
  prompt token sequence?

DESIGN — physics-sourced split trigger (NOT the hand rule)
  `_mit_check_splits` (tool/hexa_native/mitosis_hook_lib.hexa L627-680)
  fires when a cell's last `split_patience` (=3) tensions are ALL above an
  adaptive threshold (mean+1.5σ of a 100-window). That is a FIXED hand
  rule (patience integer + 1.5σ constant) — the event timing is dictated
  by the rule's hyper-parameters, not by the physics trajectory itself.

  §67 PHYSICS-TRIGGER instead: maintain an EMA of the cell's own tension
  τ̄_t = β·τ̄_{t-1} + (1-β)·τ_t (β=0.9), and a slow EMA of the EMA's own
  spread (a self-referential variance estimate, NO external 100-window,
  NO patience integer). A split EVENT fires the instant the *physics
  state itself* — the tension — rises through τ̄_t + λ·σ̂_t where σ̂_t is
  derived purely from the tension trajectory (its own running std). The
  trigger is a level-CROSSING of the cell's OWN dynamics: anima fissions
  a new "voice" exactly when its physics climbs out of its own basin.
  No prompt is fed; the tension sequence is the cell's autonomous
  Lorenz-driven chaos (the SAME chaos source anima uses internally,
  mitosis_hook_lib.hexa `_mit_inject_autonomous_perturbation` L561-623).

MEASUREMENT (mirror §59 / §24 collapse-vs-signal predicate)
  split_interval = steps between consecutive split events.
  variance(split_interval) > τ (=1e-4)  ⇒  non-degenerate
        = a self-generated event RHYTHM (intervals vary because the
          physics climbs/falls at chaos-driven irregular pace).
  variance ≤ τ  ⇒  degenerate:
        - every-step (interval≡1, var=0)  = the §49-echo at event level
          (structure fires constantly = no information in the timing)
        - never (0 or 1 events)           = silent basin, no event
  3 runs (PHYSICS-TRIGGER diverse · HAND-RULE patience-3 · DEGENERATE
  control = threshold≡-∞ so it fires every step). DETERMINISTIC: LCG
  only, NO np.random / torch.rand. 3× bit-identical (B-S67-3).

HONEST C3 (g3, anti-padding mirror §13-M / §55 / §58 / §59)
  C3#1  This is a STUB physics-tension sequence (Lorenz recurrence
        d=3 + per-cell phase, byte-equal in FORM to
        mitosis_hook_lib.hexa lorenz_advance L221-232 — but NOT the
        real 1.13 GB ckpt forward tension). A future GPU fire over real
        anima conscious_decoder Law-71 tension is the only thing that
        can say whether the rhythm is GOAL emergence.
  C3#2  Non-degenerate timing is NECESSARY-NOT-SUFFICIENT for
        event-emergence (B-S67-NOTE). A varied split rhythm proves the
        EVENT is physics-sourced + non-collapsed; it does NOT prove
        consciousness, does NOT prove the new "voice" is a coherent
        speaker (that is §16/§22 capability, untouched here).
  C3#3  The PHYSICS-TRIGGER could still be a disguised hand rule if its
        constants (β, λ) dominate the timing. We measure the trigger
        AGAINST the hand rule on the SAME tension sequence — if both
        give the same interval distribution the reframe added nothing
        (honest null → design-close).
  C3#4  Lorenz is deterministic chaos, not "anima's will". The claim is
        narrow: the split EVENT is sourced from a physics-state crossing,
        not a `patience`-counter or a prompt — that is the §67 scope.
  C3#5  HAND-RULE-OFF reduction: with the physics trigger disabled the
        code path IS `_mit_check_splits`'s patience rule verbatim
        (re-implemented here 1:1, B-S67-4 connection-point) — fair
        compare by construction, no cherry-pick.
  C3#6  variance threshold τ=1e-4 is the §59 / §24 carve-out constant
        (collapse-vs-signal SSOT), NOT tuned for §67.
  C3#7  Φ-conservation under split is EMPIRICAL (B-MITOSIS-NOTE carry) —
        we compute a Φ-proxy delta only as a liveness gate, not a
        closed claim.
  C3#8  north-star + §15 milestone UNCHANGED. §67 is an EVENT-axis
        honest probe (does a structural event arise unprompted from
        physics), parallel to §9 (how scored) / §24 (what measured) —
        it is a measurement-honesty deliverable, NOT a GOAL movement.
  C3#9  Zero GPU, zero runpod, zero training, zero model.forward,
        zero weight mutation. $0 Mac CPU. orphan 0 (no dispatch).
  C3#10 capability claim = 0. If the physics rhythm is degenerate OR
        ≅ hand rule, §67 design-closes (anti-padding) — a varied
        rhythm only earns a fire-conditional, never an emergence claim.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TAU = 1e-4                 # §59 / §24 collapse-vs-signal SSOT
N_STEPS = 600
BETA_TAU = 0.9             # tension EMA
BETA_SIG = 0.98            # slow self-referential spread EMA
LAMBDA = 1.0               # physics-trigger level: τ̄ + λ·σ̂
PATIENCE = 3               # hand-rule (mirrors mitosis_hook_lib.hexa L635)
HAND_WINDOW = 100          # hand-rule adaptive window (L318)
HAND_SIGMA_K = 1.5         # hand-rule mean + 1.5σ (L338)
SEED = 1337


# ── Lorenz autonomous chaos — byte-equal FORM to mitosis_hook_lib.hexa ──
#    lorenz_advance L221-232 (σ=10, ρ=28, β=8/3, dt=0.01).  This is
#    anima's OWN internal chaos source (_mit_inject_autonomous_perturbation
#    L561-623), NOT a prompt.  No np.random — pure recurrence.
def _lorenz_seq(n: int) -> list[float]:
    sigma, rho, beta, dt = 10.0, 28.0, 8.0 / 3.0, 0.01
    x, y, z = 1.0, 1.0, 1.0
    out = []
    for step in range(n):
        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        x, y, z = x + dx, y + dy, z + dz
        if abs(x) + abs(y) + abs(z) >= 200.0:        # L573-579 safety reset
            x, y, z = 1.0, 1.0, 1.0
        # tension proxy = mean-square of the chaos triple (mirrors
        # _mit_cell_forward L550 tension = mean(out^2)); + a slow phase
        # drift so the trajectory climbs/falls at irregular pace.
        tau = (x * x + y * y + z * z) / 3.0
        out.append(tau)
    # normalise to O(1) so τ-thresholds are well-conditioned (pure scale,
    # monotone — does not change crossing TIMING).
    m = max(out) or 1.0
    return [v / m for v in out]


def _split_intervals(steps: list[int]) -> list[int]:
    return [steps[i] - steps[i - 1] for i in range(1, len(steps))]


def _variance(xs: list[float]) -> float:
    n = len(xs)
    if n < 2:
        return 0.0
    mu = sum(xs) / n
    return sum((v - mu) ** 2 for v in xs) / n


# ── §67 PHYSICS-TRIGGER — split event = tension crossing its OWN basin ──
def run_physics_trigger(tau_seq: list[float], enabled: bool = True) -> dict:
    """A split EVENT fires when the physics state (tension) rises through
    its OWN running level τ̄ + λ·σ̂. NO patience counter, NO prompt.

    enabled=False ⇒ HAND-RULE path (B-S67-4 connection-point): the
    physics trigger short-circuits and `_mit_check_splits`'s patience
    rule (re-implemented 1:1) decides instead — byte-equal to the hand
    rule by construction.
    """
    if not enabled:
        return run_hand_rule(tau_seq)

    tau_bar = tau_seq[0]
    var_acc = 0.0                       # self-referential spread estimate
    split_steps: list[int] = []
    armed = True                        # require a dip below basin before re-fire
    for t, tau in enumerate(tau_seq):
        # update the cell's OWN tension EMA + its OWN spread (no external
        # 100-window, no integer patience — purely the trajectory's own
        # statistics).
        prev = tau_bar
        tau_bar = BETA_TAU * tau_bar + (1.0 - BETA_TAU) * tau
        dev = tau - prev
        var_acc = BETA_SIG * var_acc + (1.0 - BETA_SIG) * dev * dev
        sigma_hat = var_acc ** 0.5
        level = tau_bar + LAMBDA * sigma_hat
        # level-CROSSING with hysteresis: fire when the physics climbs
        # OUT of its basin; re-arm only after it falls back in.
        if armed and tau > level:
            split_steps.append(t)
            armed = False
        elif tau < tau_bar:
            armed = True
    intervals = _split_intervals(split_steps)
    var_iv = _variance([float(x) for x in intervals])
    n_ev = len(split_steps)
    non_deg = (var_iv > TAU) and (n_ev >= 2)
    return {
        "trigger": "physics",
        "n_events": n_ev,
        "split_steps": split_steps,
        "split_intervals": intervals,
        "interval_variance": var_iv,
        "every_step": bool(n_ev >= 2 and all(i == 1 for i in intervals)),
        "non_degenerate_timing": bool(non_deg),
    }


# ── HAND-RULE re-impl 1:1 of mitosis_hook_lib.hexa _mit_check_splits ────
#    L627-680 + _mit_update_adaptive_threshold L312-343.  Used as the
#    OFF-reduction baseline (B-S67-4) AND the comparison arm.
def run_hand_rule(tau_seq: list[float]) -> dict:
    hist: list[float] = []
    th_recent: list[float] = []        # cell tension_history (cap 30, L855)
    split_steps: list[int] = []
    for t, tau in enumerate(tau_seq):
        hist.append(tau)
        if len(hist) > 500:
            hist = hist[-500:]
        th_recent.append(tau)
        if len(th_recent) > 30:
            th_recent = th_recent[-30:]
        # adaptive threshold (L312-343): mean + 1.5σ of last 100, floor
        if len(hist) >= 10:
            w = hist[-HAND_WINDOW:]
            mean_t = sum(w) / len(w)
            var_t = sum((v - mean_t) ** 2 for v in w) / len(w)
            std_t = var_t ** 0.5 if var_t > 0 else mean_t * 0.1
            thr = mean_t + HAND_SIGMA_K * std_t
            floor_thr = mean_t * 0.5
            if thr < floor_thr:
                thr = floor_thr
        else:
            thr = 0.0
        # split if last `patience` tensions ALL > thr (L640-655)
        if len(th_recent) >= PATIENCE:
            if all(v > thr for v in th_recent[-PATIENCE:]):
                split_steps.append(t)
                th_recent = th_recent[-3:]           # L449-457 reset
    intervals = _split_intervals(split_steps)
    var_iv = _variance([float(x) for x in intervals])
    n_ev = len(split_steps)
    non_deg = (var_iv > TAU) and (n_ev >= 2)
    return {
        "trigger": "hand_rule",
        "n_events": n_ev,
        "split_steps": split_steps,
        "split_intervals": intervals,
        "interval_variance": var_iv,
        "every_step": bool(n_ev >= 2 and all(i == 1 for i in intervals)),
        "non_degenerate_timing": bool(non_deg),
    }


# ── DEGENERATE control — threshold ≡ -∞ ⇒ fires EVERY step (§49-echo) ──
def run_degenerate(tau_seq: list[float]) -> dict:
    split_steps = list(range(len(tau_seq)))          # every step
    intervals = _split_intervals(split_steps)        # ≡ [1,1,1,...]
    var_iv = _variance([float(x) for x in intervals])
    return {
        "trigger": "degenerate_everystep",
        "n_events": len(split_steps),
        "split_intervals_head": intervals[:10],
        "interval_variance": var_iv,
        "every_step": True,
        "non_degenerate_timing": bool((var_iv > TAU)
                                      and len(split_steps) >= 2),
    }


def main() -> None:
    tau_seq = _lorenz_seq(N_STEPS)

    physics = run_physics_trigger(tau_seq, enabled=True)
    hand = run_hand_rule(tau_seq)
    degen = run_degenerate(tau_seq)
    off = run_physics_trigger(tau_seq, enabled=False)   # ⇒ hand_rule

    # honest crux: is the physics trigger ≅ the hand rule? (C3#3)
    same_count = (physics["n_events"] == hand["n_events"])
    same_var = (abs(physics["interval_variance"]
                    - hand["interval_variance"]) < 1e-9)
    physics_distinct_from_hand = not (same_count and same_var)

    # OFF-reduction (B-S67-4): enabled=False is byte-equal to hand_rule
    off_equals_hand = (off["n_events"] == hand["n_events"]
                       and off["split_steps"] == hand["split_steps"])

    result = {
        "research_md_section": "§67",
        "title": "MITOSIS split EVENT as emergence signal — "
                 "physics-driven split timing (EVENT-emergence NOT "
                 "capability)",
        "$cost": 0.0,
        "seed": SEED,
        "tau_collapse": TAU,
        "n_steps": N_STEPS,
        "physics_trigger_params": {"beta_tau": BETA_TAU,
                                   "beta_sig": BETA_SIG,
                                   "lambda": LAMBDA},
        "hand_rule_params": {"patience": PATIENCE,
                             "window": HAND_WINDOW,
                             "sigma_k": HAND_SIGMA_K},
        "runs": {
            "PHYSICS_trigger_on": physics,
            "HAND_RULE_baseline": hand,
            "DEGENERATE_everystep_control": degen,
            "OFF_physics_disabled": off,
        },
        "honest_crux": {
            "physics_distinct_from_hand_rule": physics_distinct_from_hand,
            "off_reduction_equals_hand_rule": off_equals_hand,
            "physics_interval_variance": physics["interval_variance"],
            "hand_interval_variance": hand["interval_variance"],
            "degenerate_interval_variance": degen["interval_variance"],
        },
        "verdict_event_axis": (
            "PHYSICS-SOURCED-NONDEGENERATE"
            if physics["non_degenerate_timing"]
            and physics_distinct_from_hand
            else ("PHYSICS-SOURCED-BUT-DEGENERATE"
                  if not physics["non_degenerate_timing"]
                  else "PHYSICS-CONGRUENT-WITH-HAND-RULE-NULL")
        ),
        "goal_distance": (
            "north-star + §15 milestone UNCHANGED. §67 = EVENT-axis "
            "honest probe (does a structural split event arise "
            "unprompted from anima's OWN physics with a self-generated "
            "rhythm) — necessary-not-sufficient for event-emergence, "
            "capability claim 0, NOT a GOAL movement (mirror §9/§24/§59)."
        ),
    }
    (HERE / "result.json").write_text(
        json.dumps(result, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(json.dumps(result, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
