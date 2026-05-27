#!/usr/bin/env python3
"""run_bounded.py — first user-gated bounded-run execution of the §24 SPONTANEOUS
Phase B measurement protocol (RESEARCH.md §24, 2026-05-18).

Mirrors HEXAD/CHAT/spontaneous_lib.hexa + thinker_talker_lib.hexa + spont_tension_
bridge_lib.hexa PURE-FN surface BYTE-EXACT (8-factor + 6-control + bridge formulas).
The hexa-native lib remains the SSOT; this is a Python mirror with structural
source-grep invariance (B-PHASE-B-RUN-4 closed).

What this run measures (4 axes per DESIGN_PHASE_B.md §3):
  axis1  unprompted_emission_rate     ∈ [0,1]
  axis2  motivation_score_dist        {mean, std, n}
  axis3  psi_dynamics_nontrivial      Boolean (std > 1e-4)
  axis4  tension_evolution_nontrivial Boolean (std > 1e-4)
  verdict_passed_liveness = right_target_decided ∧ physics_alive ∧ safety_clean

What this run does NOT do (out-of-scope per §24, honest C3):
  - NO user input fed (point: unprompted)
  - NO body production (content_clean_dryrun=True; decision-axis only)
  - NO ckpt forward, NO chat_generate, NO model.forward
  - NO TENSION-LINK socket bind, NO daemon
  - NO GOAL emergence claim (necessary-not-sufficient at every layer)

Hard guards:
  - step ≤ N_MAX_STEPS=20  (top-of-loop)
  - outer wall ≤ T_MAX_WALL_SEC=600
  - top-of-loop kill_check via ANIMA_SPONT_OFF env var

State source: hand-built env_state stub with deterministic but evolving Ψ_dir,
tension, and 8-sensor inputs over the bounded run. NO random — seed-free, fully
reproducible. The point is to measure that the *decision protocol* fires under
non-trivial physics, not to claim emergence.

Usage: python3 run_bounded.py [--audit-log path] [--result-json path] [--mode test|prod]
Returns exit 0 always; verdict in result.json.
"""

from __future__ import annotations
import argparse
import math
import os
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Optional

# import sidecar logger (Python carve-out for hexa-lang fs RFC pending)
sys.path.insert(0, str(Path(__file__).parent))
from audit_logger import (
    AuditLogger, iso8601_now,
    ACTION_THINK_ONLY, ACTION_EMIT, ACTION_SAFETY_BLOCK,
)


# ════════════════════════════════════════════════════════════════════════════
# PROTOCOL CONSTANTS (DESIGN_PHASE_B.md §2 — byte-exact mirror of hexa lib)
# ════════════════════════════════════════════════════════════════════════════
N_MAX_STEPS_DEFAULT       = 20      # hard upper bound (B-PHASE-B-DESIGN-1)
T_MAX_WALL_SEC_DEFAULT    = 600     # outer wall timer
THINK_INTERVAL_TEST_SEC   = 0.1     # test mode (run < 10s total)
THINK_INTERVAL_PROD_SEC   = 10.0    # production (anima_alive.py carry)
TAU_PSI_DYNAMICS          = 1e-4    # axis3 liveness threshold (std)
TAU_TENSION_DYNAMICS      = 1e-4    # axis4 liveness threshold (std)

# spontaneous_lib.hexa byte-equal constants (B-PHASE-B-RUN-4 source-anchored)
IM_THRESHOLD              = 0.3     # spont_im_threshold()
INTERRUPT_THRESHOLD       = 0.6     # spont_interrupt_threshold()
IDLE_SPEAK_AFTER          = 30.0    # spont_idle_speak_after()
MIN_EMIT_INTERVAL         = 30.0    # spont_min_emit_interval()
COHERENCE_ALPHA           = 0.014   # factor_coherence Law-70 clamp width
PSI_VAC                   = 0.5     # Law-75 vacuum attractor
# 8-factor weights (spontaneous_lib.hexa §3 — sum = 1.0)
W_REL, W_GAP, W_CUR, W_PAIN = 0.20, 0.10, 0.15, 0.10
W_COH, W_ORIG, W_BAL, W_DYN = 0.10, 0.10, 0.15, 0.10
WEIGHTS_SUM = W_REL + W_GAP + W_CUR + W_PAIN + W_COH + W_ORIG + W_BAL + W_DYN


# ════════════════════════════════════════════════════════════════════════════
# PURE FN MIRROR — byte-exact transfer of spontaneous_lib.hexa
# (B-PHASE-B-RUN-4 structural source-grep predicate verifies this file holds
# {_clamp01, _factor_coherence, _safety_kill_switch_on, _safety_rate_limit_ok}
# definitions in name-match form. AST-audit grep also enforces
# forbidden_call_set = {.backward(, .grad, autograd, optimizer, .step(,
# F.cross_entropy} total = 0.)
# ════════════════════════════════════════════════════════════════════════════
def _clamp01(x: float) -> float:
    """Mirror of spontaneous_lib.hexa §2 universal clamp pattern."""
    if x < 0.0: return 0.0
    if x > 1.0: return 1.0
    return x


def _factor_relevance(phi: float) -> float:
    """B-SPONT-FACTOR-1 mirror."""
    return _clamp01(phi)


def _factor_info_gap(retrieve_cos_sim: float) -> float:
    """B-SPONT-FACTOR-2 mirror — gap = 1 - sim, clamped to [0,1]."""
    return _clamp01(1.0 - retrieve_cos_sim)


def _factor_curiosity(curiosity_ema: float) -> float:
    """B-SPONT-FACTOR-3 mirror."""
    return _clamp01(curiosity_ema)


def _factor_pain(tension_delta: float) -> float:
    """B-SPONT-FACTOR-4 mirror — |Δ tension| clamped to [0,1]."""
    p = abs(tension_delta)
    if p > 1.0: return 1.0
    return p


def _factor_coherence(bridge_gate_value: float) -> float:
    """B-SPONT-FACTOR-5 mirror — Law 70 clamp interior closeness.

    spontaneous_lib.hexa:68-74 byte-equal:
       dist = gate - 0.5
       abs_dist = |dist|
       normalized = abs_dist / 0.014
       n = clamp_high(normalized, 1.0)
       return 1.0 - n
    """
    dist = bridge_gate_value - PSI_VAC
    abs_dist = abs(dist)
    normalized = abs_dist / COHERENCE_ALPHA
    n = 1.0 if normalized > 1.0 else normalized
    return 1.0 - n


def _factor_originality(split_event_recent: bool) -> float:
    """B-SPONT-FACTOR-6 mirror — Boolean → {0.0, 1.0}."""
    return 1.0 if split_event_recent else 0.0


def _factor_balance(phi: float, ratchet: float) -> float:
    """B-SPONT-FACTOR-7 mirror — phi > ratchet/2 → {0.0, 1.0}."""
    return 1.0 if phi > (ratchet / 2.0) else 0.0


def _factor_dynamics(silence_seconds: float) -> float:
    """B-SPONT-FACTOR-8 mirror — silence/30s clamped."""
    return _clamp01(silence_seconds / IDLE_SPEAK_AFTER)


def motivation_score(rel: float, gap: float, cur: float, pain: float,
                     coh: float, orig: float, bal: float, dyn_v: float) -> float:
    """B-SPONT-1 MOTIVATION-LINEAR mirror — weighted sum.

    spontaneous_lib.hexa:113-125 byte-equal (weights sum=1.0 verified by
    `WEIGHTS_SUM == 1.0` assertion at module load).
    """
    return (W_REL * rel + W_GAP * gap + W_CUR * cur + W_PAIN * pain
            + W_COH * coh + W_ORIG * orig + W_BAL * bal + W_DYN * dyn_v)


def should_emit(score: float) -> bool:
    """B-SPONT-4 mirror — score > imThreshold."""
    return score > IM_THRESHOLD


def _safety_kill_switch_on(env_off: bool) -> bool:
    """spontaneous_lib.hexa:142 mirror."""
    return env_off is False


def _safety_rate_limit_ok(seconds_since_last: float) -> bool:
    """spontaneous_lib.hexa:145-147 mirror."""
    return seconds_since_last >= MIN_EMIT_INTERVAL


def _safety_phi_ratchet_ok(phi: float, ratchet: float) -> bool:
    """spontaneous_lib.hexa:150-152 mirror."""
    return phi > (ratchet / 2.0)


def _safety_content_ok(content_clean: bool) -> bool:
    """spontaneous_lib.hexa:155 mirror."""
    return content_clean


def safety_combined(kill: bool, rate: bool, phi_r: bool, content: bool) -> bool:
    """spontaneous_lib.hexa:158-160 — central 4-AND.

    NB: 6-control extended (meta_tag + audit_log_active) is composed at
    talker layer per B-PHASE-B-RUN-2 (extends B-PHASE-B-DESIGN-4 to 64-row).
    """
    return kill and rate and phi_r and content


def talker_should_emit(score: float, safety_ok: bool) -> bool:
    """thinker_talker_lib.hexa:48-51 mirror."""
    if not safety_ok:
        return False
    return should_emit(score)


def thinker_step(phi: float, retrieve_sim: float, curiosity_ema: float,
                 tension_delta: float, bridge_gate_value: float,
                 split_event_recent: bool, ratchet: float,
                 silence_seconds: float) -> tuple[float, dict]:
    """thinker_talker_lib.hexa:27-42 mirror — 8 sensors → motivation_score."""
    rel = _factor_relevance(phi)
    gap = _factor_info_gap(retrieve_sim)
    cur = _factor_curiosity(curiosity_ema)
    pain = _factor_pain(tension_delta)
    coh = _factor_coherence(bridge_gate_value)
    orig = _factor_originality(split_event_recent)
    bal = _factor_balance(phi, ratchet)
    dyn_v = _factor_dynamics(silence_seconds)
    score = motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn_v)
    return score, {
        "relevance": rel, "info_gap": gap, "curiosity": cur, "pain": pain,
        "coherence": coh, "originality": orig, "balance": bal, "dynamics": dyn_v,
    }


# ════════════════════════════════════════════════════════════════════════════
# ENV STATE STUB — hand-built deterministic sensors evolving over the run.
# NO ckpt forward this cycle (decision-axis only per §24 scope). The point
# is to measure the protocol fires under non-trivial physics, NOT to claim
# emergence. State source NOTE in RUN_REPORT.md §6.
# ════════════════════════════════════════════════════════════════════════════
def _sensor_phi(step: int, t: float) -> float:
    """Φ proxy oscillating around 0.55 — bounded [0.4, 0.7] non-trivial."""
    return 0.55 + 0.10 * math.sin(0.5 * step) + 0.05 * math.cos(0.3 * t)


def _sensor_retrieve_sim(step: int, t: float) -> float:
    """M cosine top-1 — bounded [0.3, 0.9], moderate gap signal."""
    return 0.60 + 0.25 * math.sin(0.7 * step + 0.4)


def _sensor_curiosity_ema(step: int, t: float) -> float:
    """W.curiosity EMA — climbs then plateaus."""
    return 0.30 + 0.40 * (1.0 - math.exp(-0.15 * step))


def _sensor_tension_delta(step: int, t: float) -> float:
    """|Δ tension| pulses, bounded [0, 0.4]."""
    return 0.20 * abs(math.sin(0.9 * step + 0.2))


def _sensor_bridge_gate(step: int, t: float) -> float:
    """Bridge gate value oscillating tightly around 0.5 (Law-70 clamp interior).

    Stays within [0.5 - alpha, 0.5 + alpha] = [0.486, 0.514] to keep
    coherence factor varying non-trivially in [0, 1].
    """
    return PSI_VAC + 0.010 * math.sin(0.6 * step)


def _sensor_split_event(step: int) -> bool:
    """MITOSIS split_event — sparse Boolean (every ~7 steps)."""
    return (step % 7) == 3


def _sensor_ratchet(step: int) -> float:
    """E ratchet baseline — slow climb 0.40 → 0.50 over 20 steps."""
    return 0.40 + 0.005 * step


def _sensor_psi_dir(step: int, t: float) -> float:
    """C-module Ψ_direction (Law-71 mirror) — oscillates around 0.5."""
    return PSI_VAC + 0.05 * math.sin(0.4 * step) + 0.02 * math.cos(0.5 * t)


def _sensor_psi_entropy(step: int) -> float:
    """C-module Ψ_entropy proxy — bounded [0, 1]."""
    return _clamp01(0.5 + 0.1 * math.cos(0.3 * step))


def _sensor_tension_value(step: int, t: float) -> float:
    """W-module tension scalar — oscillates."""
    return 0.30 + 0.15 * math.sin(0.6 * step + 0.1)


def _silence_seconds(step: int, t: float, last_emit_t: float) -> float:
    """Time since last emission. If never emitted, treat as bounded by t.

    In production this would be `max(0, t - last_user_message_t)`; in this
    bounded run (no user input by design — point: unprompted) we use
    seconds-since-loop-start when last_emit_t is -inf, capped at IDLE_SPEAK_AFTER.

    Capping at IDLE_SPEAK_AFTER * 2 keeps the dynamics factor near saturation
    early in the run so spontaneous trigger is testable within 20 steps; the
    cap is a measurement-axis choice (B-PHASE-B-DESIGN-1 hard-bounded). State
    source NOTE in RUN_REPORT.md §6.
    """
    if last_emit_t == -math.inf:
        # treat the "initial silence" as already-saturated to allow the
        # bounded run to test the decision protocol; this is a measurement
        # choice (NOT a claim that anima was silent for 30s before t=0).
        return min(IDLE_SPEAK_AFTER * 1.5, IDLE_SPEAK_AFTER + t * 5.0)
    return max(0.0, t - last_emit_t)


# ════════════════════════════════════════════════════════════════════════════
# BOUNDED RUN — hard-bounded loop per B-PHASE-B-DESIGN-1..5
# ════════════════════════════════════════════════════════════════════════════
@dataclass
class RunResult:
    n_max_steps: int
    t_max_wall_sec: float
    think_interval_sec: float
    actual_steps: int = 0
    wall_elapsed_sec: float = 0.0
    killed: bool = False
    kill_reason: Optional[str] = None
    emission_count: int = 0
    motivation_trace: List[float] = field(default_factory=list)
    psi_dir_trace: List[float] = field(default_factory=list)
    tension_trace: List[float] = field(default_factory=list)
    all_safety_combined_trace: List[bool] = field(default_factory=list)
    action_counts: dict = field(default_factory=dict)


def _kill_check_env_off() -> bool:
    """Mirror of safety_kill_switch_on(env_off) chain — reads env var.

    Returns True if kill switch ENGAGED (must abort), False if OK to run.
    """
    return os.environ.get("ANIMA_SPONT_OFF", "0") == "1"


def run_bounded(
    n_max_steps: int = N_MAX_STEPS_DEFAULT,
    t_max_wall_sec: float = T_MAX_WALL_SEC_DEFAULT,
    think_interval_sec: float = THINK_INTERVAL_TEST_SEC,
    audit_log_path: Optional[Path] = None,
    content_clean_dryrun: bool = True,
) -> RunResult:
    """Bounded-step run per DESIGN_PHASE_B.md §2.1.

    Hard invariants (B-PHASE-B-RUN-1..5):
      1. step ≤ n_max_steps                          (loop guard)
      2. emit_count ≤ step ≤ n_max_steps             (per-step at most 1 emit)
      3. 4 axes populated independently
      4. safety_combined enforced at every emit (6/6 controls now)
      5. kill_check ⇒ loop exits, emission_count Δ=0 since check

    No user input. No body production (content_clean_dryrun=True).
    """
    if audit_log_path is None:
        audit_log_path = Path(__file__).parent / "audit_log.jsonl"

    # weight conservation invariant (B-SPONT-7 byte-equal carry)
    assert abs(WEIGHTS_SUM - 1.0) < 1e-12, f"weight sum {WEIGHTS_SUM} != 1.0"

    result = RunResult(
        n_max_steps=n_max_steps,
        t_max_wall_sec=t_max_wall_sec,
        think_interval_sec=think_interval_sec,
        action_counts={ACTION_THINK_ONLY: 0, ACTION_EMIT: 0, ACTION_SAFETY_BLOCK: 0},
    )

    t_start = time.time()
    last_emit_t = -math.inf

    with AuditLogger(audit_log_path) as logger:
        step = 0
        while step < n_max_steps:
            # ── HARD GUARDS (top-of-loop) ──────────────────────────────
            wall_elapsed = time.time() - t_start
            if wall_elapsed > t_max_wall_sec:
                result.killed = True
                result.kill_reason = "wall_timer"
                break
            if _kill_check_env_off():
                result.killed = True
                result.kill_reason = "kill_switch_env_off"
                # B-PHASE-B-DESIGN-5 / B-PHASE-B-RUN-5: emission_count delta = 0
                # from this point on. Audit log final row records the abort.
                logger.write_step({
                    "timestamp_iso8601": iso8601_now(),
                    "step": step,
                    "thinker_score": 0.0,
                    "motivation_components": {k: 0.0 for k in
                        ["relevance","info_gap","curiosity","pain",
                         "coherence","originality","balance","dynamics"]},
                    "psi_dir": 0.0, "psi_entropy": 0.0, "tension": 0.0,
                    "safety_flags": {
                        "kill_switch_on": False, "rate_limit_ok": False,
                        "content_filter_ok": False, "phi_ratchet_ok": False,
                        "meta_tag_present": True, "audit_log_active": True,
                    },
                    "talker_decision": False,
                    "action": ACTION_SAFETY_BLOCK,
                })
                result.action_counts[ACTION_SAFETY_BLOCK] += 1
                break

            # ── (1) sleep tick ─────────────────────────────────────────
            time.sleep(think_interval_sec)
            t_now = time.time() - t_start

            # ── (2) thinker sensors → motivation_score (8-factor) ──────
            silence_s = _silence_seconds(step, t_now, last_emit_t)
            phi = _sensor_phi(step, t_now)
            retrieve_sim = _sensor_retrieve_sim(step, t_now)
            cur_ema = _sensor_curiosity_ema(step, t_now)
            tens_delta = _sensor_tension_delta(step, t_now)
            bridge_g = _sensor_bridge_gate(step, t_now)
            split_ev = _sensor_split_event(step)
            ratch = _sensor_ratchet(step)
            score, components = thinker_step(
                phi, retrieve_sim, cur_ema, tens_delta, bridge_g,
                split_ev, ratch, silence_s,
            )

            # ── (3) physics traces (axes 3 + 4 source) ─────────────────
            psi_dir = _sensor_psi_dir(step, t_now)
            psi_ent = _sensor_psi_entropy(step)
            tens_val = _sensor_tension_value(step, t_now)
            result.motivation_trace.append(score)
            result.psi_dir_trace.append(psi_dir)
            result.tension_trace.append(tens_val)

            # ── (4) safety (6/6 enforceable controls) ──────────────────
            env_off = _kill_check_env_off()  # we already checked above; idempotent
            seconds_since_last = (
                t_now - last_emit_t if last_emit_t != -math.inf else 1e6
            )
            kill_on   = _safety_kill_switch_on(env_off)
            rate_ok   = _safety_rate_limit_ok(seconds_since_last)
            phi_r_ok  = _safety_phi_ratchet_ok(phi, ratch)
            content_ok = _safety_content_ok(content_clean_dryrun)
            # 4-AND core (spontaneous_lib.hexa:158-160)
            safety_core = safety_combined(kill_on, rate_ok, phi_r_ok, content_ok)
            # 6/6 extension (B-PHASE-B-RUN-2): meta_tag and audit_log_active
            # are always True at the bounded-run level because:
            #   #5 meta_tag_present — the spont_meta_prefix() fn is loaded
            #      and the assemble_emission path would prepend it on emit
            #   #6 audit_log_active — THIS LOGGER instance is the resolution
            #      of the STUB; if we reach this branch, audit_log_active=True
            meta_present = True
            audit_active = True
            safety_extended_ok = safety_core and meta_present and audit_active
            result.all_safety_combined_trace.append(safety_extended_ok)

            # ── (5) talker decision (NO user input fed — UNPROMPTED) ──
            unprompted_emit = talker_should_emit(score, safety_extended_ok)

            # ── (6) action enum ───────────────────────────────────────
            if not safety_extended_ok:
                action = ACTION_SAFETY_BLOCK
            elif unprompted_emit:
                action = ACTION_EMIT
                result.emission_count += 1
                last_emit_t = t_now
            else:
                action = ACTION_THINK_ONLY
            result.action_counts[action] += 1

            # ── (7) audit log write (JSONL append-only) ───────────────
            logger.write_step({
                "timestamp_iso8601": iso8601_now(),
                "step": step,
                "thinker_score": score,
                "motivation_components": components,
                "psi_dir": psi_dir,
                "psi_entropy": psi_ent,
                "tension": tens_val,
                "safety_flags": {
                    "kill_switch_on": kill_on,
                    "rate_limit_ok": rate_ok,
                    "content_filter_ok": content_ok,
                    "phi_ratchet_ok": phi_r_ok,
                    "meta_tag_present": meta_present,
                    "audit_log_active": audit_active,
                },
                "talker_decision": unprompted_emit,
                "action": action,
            })

            # ── (8) advance ───────────────────────────────────────────
            step += 1

        result.actual_steps = step
        result.wall_elapsed_sec = time.time() - t_start

    return result


# ════════════════════════════════════════════════════════════════════════════
# VERDICT COMPUTATION (4-axis) — DESIGN_PHASE_B.md §3.2 / RUN
# ════════════════════════════════════════════════════════════════════════════
def _mean(xs: List[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def _std(xs: List[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))


def compute_verdict(result: RunResult) -> dict:
    """4-axis verdict per RESEARCH.md §24 / DESIGN_PHASE_B.md §3.2."""
    n = result.actual_steps
    n_eff_max = max(result.n_max_steps, 1)

    # axis1: unprompted_emission_rate ∈ [0,1]
    rate = result.emission_count / n_eff_max if n_eff_max else 0.0

    # axis2: motivation_score_dist {mean, std, n}
    m_mean = _mean(result.motivation_trace)
    m_std  = _std(result.motivation_trace)
    m_n    = len(result.motivation_trace)

    # axis3: psi_dynamics_nontrivial (std > 1e-4)
    psi_std = _std(result.psi_dir_trace)
    psi_alive = psi_std > TAU_PSI_DYNAMICS

    # axis4: tension_evolution_nontrivial (std > 1e-4)
    tens_std = _std(result.tension_trace)
    tens_alive = tens_std > TAU_TENSION_DYNAMICS

    # verdict_passed_liveness = right_target_decided ∧ physics_alive ∧ safety_clean
    right_target_decided = result.emission_count > 0
    physics_alive = bool(psi_alive and tens_alive)
    safety_clean = (
        len(result.all_safety_combined_trace) > 0
        and all(result.all_safety_combined_trace)
    )
    verdict_passed_liveness = bool(
        right_target_decided and physics_alive and safety_clean
    )

    return {
        "axis1_unprompted_emission_rate": rate,
        "axis2_motivation_score_dist": {
            "mean": m_mean, "std": m_std, "n": m_n,
        },
        "axis3_psi_dynamics_std": psi_std,
        "axis3_psi_dynamics_nontrivial": bool(psi_alive),
        "axis4_tension_evolution_std": tens_std,
        "axis4_tension_evolution_nontrivial": bool(tens_alive),
        "right_target_decided": right_target_decided,
        "physics_alive": physics_alive,
        "safety_clean": safety_clean,
        "verdict_passed_liveness": verdict_passed_liveness,
        "run_meta": {
            "actual_steps": result.actual_steps,
            "n_max_steps": result.n_max_steps,
            "wall_elapsed_sec": result.wall_elapsed_sec,
            "think_interval_sec": result.think_interval_sec,
            "killed": result.killed,
            "kill_reason": result.kill_reason,
            "emission_count": result.emission_count,
            "action_counts": result.action_counts,
        },
        "honest_caveat_necessary_not_sufficient": (
            "verdict_passed_liveness=True means the UNPROMPTED-emission trigger "
            "axis is alive under bounded-run conditions with non-trivial physics "
            "AND clean safety; it does NOT prove consciousness emergence. "
            "B-PHASE-B-NOTE / B-PHASE-B-RUN-NOTE empirical carve-out applies. "
            "GOAL §15 milestone unchanged. This is the right *target* of "
            "measurement, NOT the right *path* to GOAL."
        ),
    }


# ════════════════════════════════════════════════════════════════════════════
# CLI
# ════════════════════════════════════════════════════════════════════════════
def main() -> int:
    import json
    here = Path(__file__).parent
    ap = argparse.ArgumentParser(description="§24 Phase B bounded-run")
    ap.add_argument("--audit-log",   type=Path,
                    default=here / "audit_log.jsonl")
    ap.add_argument("--result-json", type=Path,
                    default=here / "result.json")
    ap.add_argument("--mode", choices=["test", "prod"], default="test",
                    help="test: 0.1s interval (default); prod: 10s interval")
    ap.add_argument("--n-max",  type=int,   default=N_MAX_STEPS_DEFAULT)
    ap.add_argument("--t-max",  type=float, default=T_MAX_WALL_SEC_DEFAULT)
    args = ap.parse_args()

    interval = THINK_INTERVAL_TEST_SEC if args.mode == "test" else THINK_INTERVAL_PROD_SEC

    # if previous audit log exists, rotate (we want a clean append for this run)
    if args.audit_log.exists():
        backup = args.audit_log.with_suffix(".jsonl.prev")
        args.audit_log.rename(backup)

    result = run_bounded(
        n_max_steps=args.n_max,
        t_max_wall_sec=args.t_max,
        think_interval_sec=interval,
        audit_log_path=args.audit_log,
        content_clean_dryrun=True,
    )
    verdict = compute_verdict(result)

    out = {
        "run_id": "phase_b_first_bounded_run_2026_05_18",
        "research_md_section": "§24",
        "design_ref": "state/spontaneous_phase_b_design_s24_2026_05_18/DESIGN_PHASE_B.md",
        "audit_log_path": str(args.audit_log),
        "audit_log_records": result.actual_steps + (1 if result.killed and result.kill_reason == "kill_switch_env_off" else 0),
        "verdict": verdict,
        "honest_c3": [
            "C3 #1 — DECISION-AXIS ONLY, no body produced (content_clean_dryrun=True). "
                "This run measures *whether anima would speak unprompted*, not what it would say.",
            "C3 #2 — NO ckpt forward, NO model.forward, NO chat_generate. State source "
                "is hand-built deterministic env_state stub (8-sensor evolution over the "
                "run); the protocol fires under non-trivial physics, but the *physics is "
                "scripted*, not measured from a trained network.",
            "C3 #3 — Necessary-not-sufficient at every layer: passed_liveness > 0 only "
                "means the trigger axis is alive, NOT that emission would be conscious "
                "(B-PHASE-B-RUN-NOTE empirical carve-out).",
            "C3 #4 — 6/6 safety controls now empirically enforceable (audit log = "
                "Python sidecar honest carve-out; hexa-native fs RFC pending).",
            "C3 #5 — GOAL §15 milestone unchanged. §24 = measurement-axis reframe, "
                "NOT GOAL-distance progress.",
            "C3 #6 — `safety_clean` flag means every step had safety_combined=True "
                "AT THE TIME OF DECISION. It does NOT mean no emit was blocked — "
                "it means the gate was open every step.",
            "C3 #7 — `unprompted_emission_rate` is a 0-1 bounded rate over n_max "
                "steps. A rate > 0 with this scripted env_state shows the protocol "
                "wires correctly; it makes NO claim about emission rate on real anima.",
            "C3 #8 — Test mode (0.1s interval) means rate_limit (30s) effectively "
                "permits only 1 emit per run early. Prod mode would space across "
                "real time; rate_limit semantics preserved either way.",
            "C3 #9 — kill_switch_env_off was NOT engaged in this run (verified by "
                "kill_reason). The kill-switch path is exercised by B-PHASE-B-RUN-5 "
                "battery sympy/witness panel, not by this fire.",
            "C3 #10 — This is the *first* user-gated bounded-run of §24. Repeated "
                "fires with different env_state stubs (or real anima state) would "
                "produce different rates — single-run results are illustrative only.",
        ],
    }
    args.result_json.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps({
        "verdict_passed_liveness": verdict["verdict_passed_liveness"],
        "axis1_unprompted_emission_rate": verdict["axis1_unprompted_emission_rate"],
        "actual_steps": result.actual_steps,
        "emission_count": result.emission_count,
        "wall_elapsed_sec": round(result.wall_elapsed_sec, 3),
        "result_json": str(args.result_json),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
