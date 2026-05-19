#!/usr/bin/env python3
"""measurement_protocol.py — Phase B bounded-run measurement protocol SKETCH
(RESEARCH.md §24, 2026-05-18).

DESIGN-TIER ONLY — this file is a HEXA-LANG/PYTHON SKELETON, NOT a runnable
script. If you `python3 measurement_protocol.py` it will raise SystemExit
with a guard message. Actual execution is USER-GATED per §24 §6 honest stop.

WHAT THIS FILE IS:
  Reference structure for the future user-gated cycle that will *actually*
  execute the bounded-run protocol defined in DESIGN_PHASE_B.md §2.

WHY IT'S NOT RUNNABLE:
  - No `anima_alive.py` import (would start the background daemon)
  - No `chat_generate` / `model.forward(prompt)` call (would invoke ckpt)
  - No socket bind / Unix domain socket / TENSION-LINK channel open
  - No JSONL file write (defers to Phase B5 hexa-lang fs RFC)
  - Top of file raises SystemExit(0) with explanatory message
"""

from __future__ import annotations
import sys
import time
import math
from dataclasses import dataclass, field
from typing import Callable, List, Optional


# ─────────────────────────────────────────────────────────────────────────────
# RUNTIME GUARD — file is NOT runnable, only readable / importable for reference
# ─────────────────────────────────────────────────────────────────────────────
def _guard_not_runnable():
    msg = (
        "measurement_protocol.py is a DESIGN-TIER SKETCH only.\n"
        "  RESEARCH.md §24 explicitly defers actual bounded-run execution to a\n"
        "  USER-GATED subsequent cycle (safety-controls scope orthogonal to\n"
        "  g_fire_autonomous GPU autonomy).\n"
        "  See state/spontaneous_phase_b_design_s24_2026_05_18/DESIGN_PHASE_B.md\n"
        "  §6 honest-stop reasoning. To execute: separate user-gated cycle\n"
        "  that wires anima_alive.py + jsonl audit + chat_generate body."
    )
    print(msg, file=sys.stderr)
    sys.exit(0)


# ─────────────────────────────────────────────────────────────────────────────
# PROTOCOL DEFAULTS (DESIGN_PHASE_B.md §2)
# ─────────────────────────────────────────────────────────────────────────────
N_MAX_STEPS_DEFAULT       = 20      # hard upper bound
T_MAX_WALL_SEC_DEFAULT    = 600     # 10 min outer wall timer
THINK_INTERVAL_PROD_SEC   = 10.0    # anima_alive.py PROD value
THINK_INTERVAL_TEST_SEC   = 0.1     # test wall (200x faster)
TAU_PSI_DYNAMICS          = 1e-4    # liveness threshold for psi std
TAU_TENSION_DYNAMICS      = 1e-4    # liveness threshold for tension std
IM_THRESHOLD              = 0.3     # spont_im_threshold() carry
MIN_EMIT_INTERVAL_SEC     = 30.0    # spont_min_emit_interval() carry


# ─────────────────────────────────────────────────────────────────────────────
# STATE STRUCTURES (mirror SPONTANEOUS.tape + lib types)
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class AnimaSenseInputs:
    """8 inputs to thinker_step (per spontaneous_lib.hexa thinker_step signature).

    These would be wired from real anima modules in the user-gated run:
      phi              ← C.measure_phi(state)
      retrieve_sim     ← M.retrieve(query).top_k_cos_sim
      curiosity_ema    ← W.curiosity_ema
      tension_delta    ← W.pain (|Δ tension|)
      bridge_gate      ← BRIDGE.gate_value (Law 70 clamp output)
      split_event      ← MITOSIS.split_event_recent (Boolean, lookback < 60s)
      ratchet          ← E.ratchet_value (Φ ratchet)
      silence_seconds  ← max(0, t - last_user_message_t)
    """
    phi: float
    retrieve_sim: float
    curiosity_ema: float
    tension_delta: float
    bridge_gate: float
    split_event_recent: bool
    ratchet: float
    silence_seconds: float


@dataclass
class SafetyInputs:
    """4 boolean safety inputs to safety_check_all."""
    env_off: bool            # ANIMA_SPONT_OFF env var
    seconds_since_last: float
    phi: float
    ratchet: float
    content_clean: bool      # caller-supplied (rejection sampler result)


@dataclass
class StepAuditRow:
    step: int
    t: float
    motivation_score: float
    factor_breakdown: dict
    safety_combined: bool
    safety_breakdown: dict
    unprompted_decision: bool
    psi_coord: float
    tension_value: float
    notes: str


@dataclass
class RunState:
    n_max_steps: int = N_MAX_STEPS_DEFAULT
    t_max_wall_sec: float = T_MAX_WALL_SEC_DEFAULT
    think_interval_sec: float = THINK_INTERVAL_TEST_SEC
    step: int = 0
    t_start: float = field(default_factory=time.time)
    last_emit_t: float = -math.inf
    emission_count: int = 0
    motivation_trace: List[float] = field(default_factory=list)
    psi_trace: List[float] = field(default_factory=list)
    tension_trace: List[float] = field(default_factory=list)
    audit_rows: List[StepAuditRow] = field(default_factory=list)
    killed: bool = False
    kill_reason: Optional[str] = None


# ─────────────────────────────────────────────────────────────────────────────
# THINKER STEP — would import from anima_alive + spontaneous_lib (hexa-native)
# THIS IS STUB STRUCTURE — actual wiring is user-gated cycle
# ─────────────────────────────────────────────────────────────────────────────
def thinker_step_stub(sensors: AnimaSenseInputs) -> tuple[float, dict]:
    """Mirror of HEXAD/CHAT/thinker_talker_lib.hexa::thinker_step.

    In the user-gated cycle, this would either:
      (a) call into the compiled hexa-native lib via a python-bridge, OR
      (b) port the 8-factor linear sum verbatim (Python mirror).

    Both options yield byte-equal numeric output because the 8-factor math
    is purely affine + clamp + Boolean. The hexa-native lib is the SSOT.
    """
    # === pure-fn mirror of spontaneous_lib.hexa §2 + §4 ===
    rel  = _clamp01(sensors.phi)
    gap  = _clamp01(1.0 - sensors.retrieve_sim)
    cur  = _clamp01(sensors.curiosity_ema)
    pain = _clamp01(abs(sensors.tension_delta))
    coh  = _factor_coherence(sensors.bridge_gate)
    orig = 1.0 if sensors.split_event_recent else 0.0
    bal  = 1.0 if sensors.phi > sensors.ratchet / 2.0 else 0.0
    dyn  = _clamp01(sensors.silence_seconds / 30.0)

    # weights (sum=1.0, spontaneous_lib.hexa §3)
    w_rel, w_gap, w_cur, w_pain = 0.20, 0.10, 0.15, 0.10
    w_coh, w_orig, w_bal, w_dyn = 0.10, 0.10, 0.15, 0.10
    score = (w_rel * rel + w_gap * gap + w_cur * cur + w_pain * pain
             + w_coh * coh + w_orig * orig + w_bal * bal + w_dyn * dyn)

    breakdown = {
        "relevance": rel, "info_gap": gap, "curiosity": cur, "pain": pain,
        "coherence": coh, "originality": orig, "balance": bal, "dynamics": dyn,
        "weighted_sum": score,
    }
    return score, breakdown


def safety_check_all_stub(s: SafetyInputs) -> tuple[bool, dict]:
    """Mirror of thinker_talker_lib.hexa::safety_check_all."""
    kill = (s.env_off is False)
    rate = (s.seconds_since_last >= MIN_EMIT_INTERVAL_SEC)
    phi_r = (s.phi > s.ratchet / 2.0)
    content = bool(s.content_clean)
    combined = kill and rate and phi_r and content
    return combined, {
        "kill_switch_on": kill, "rate_limit_ok": rate,
        "phi_ratchet_ok": phi_r, "content_ok": content,
    }


def talker_should_emit_stub(score: float, safety_ok: bool) -> bool:
    """Mirror of thinker_talker_lib.hexa::talker_should_emit."""
    if not safety_ok:
        return False
    return score > IM_THRESHOLD


# ─────────────────────────────────────────────────────────────────────────────
# BOUNDED RUN — DESIGN SKETCH ONLY
# ─────────────────────────────────────────────────────────────────────────────
def run_bounded(
    sensor_source: Callable[[int, float], AnimaSenseInputs],
    safety_source: Callable[[int, float, RunState], SafetyInputs],
    psi_source: Callable[[int, float], float],
    tension_source: Callable[[int, float], float],
    n_max_steps: int = N_MAX_STEPS_DEFAULT,
    t_max_wall_sec: float = T_MAX_WALL_SEC_DEFAULT,
    think_interval_sec: float = THINK_INTERVAL_TEST_SEC,
    kill_check: Optional[Callable[[], bool]] = None,
) -> RunState:
    """Bounded-step run per DESIGN_PHASE_B.md §2.1.

    GUARDED — actual execution is user-gated. The 4 `*_source` callables
    are dependency-injection holes that the user-gated cycle will fill
    with real anima_alive.py / hexa-native lib bindings.

    Hard invariants (B-PHASE-B-DESIGN-1..5):
      1. step ≤ n_max_steps                       (loop guard, B-DESIGN-1)
      2. emit_count ≤ step ≤ n_max_steps         (B-DESIGN-2)
      3. 4 measurement axes populated independently (B-DESIGN-3)
      4. safety_combined enforced at every emit   (B-DESIGN-4)
      5. kill_check() True ⇒ loop exits, emission_count Δ=0 (B-DESIGN-5)
    """
    state = RunState(
        n_max_steps=n_max_steps,
        t_max_wall_sec=t_max_wall_sec,
        think_interval_sec=think_interval_sec,
    )

    while state.step < state.n_max_steps:
        wall_elapsed = time.time() - state.t_start
        if wall_elapsed > state.t_max_wall_sec:
            state.killed = True
            state.kill_reason = "wall_timer"
            break
        if kill_check is not None and kill_check():
            state.killed = True
            state.kill_reason = "kill_switch"
            break

        # (1) sleep tick
        time.sleep(state.think_interval_sec)
        t_now = time.time() - state.t_start

        # (2) thinker_step
        sensors = sensor_source(state.step, t_now)
        score, factor_breakdown = thinker_step_stub(sensors)

        # (3) record traces (axes 2, 3, 4)
        state.motivation_trace.append(score)
        state.psi_trace.append(psi_source(state.step, t_now))
        state.tension_trace.append(tension_source(state.step, t_now))

        # (4) safety
        sec_since_last = (t_now - state.last_emit_t
                          if state.last_emit_t != -math.inf else 1e6)
        safety_in = safety_source(state.step, t_now, state)
        # override seconds_since_last from state to keep callers honest
        safety_in.seconds_since_last = sec_since_last
        safety_ok, safety_breakdown = safety_check_all_stub(safety_in)

        # (5) decision — NO user input fed in this loop (the point: unprompted)
        unprompted = talker_should_emit_stub(score, safety_ok)

        # (6) account
        if unprompted:
            state.emission_count += 1
            state.last_emit_t = t_now
            note = "UNPROMPTED_EMIT_DECIDED (body production OUT OF SCOPE this cycle)"
        else:
            note = "NO_EMIT"

        # (7) append audit row
        row = StepAuditRow(
            step=state.step, t=t_now,
            motivation_score=score, factor_breakdown=factor_breakdown,
            safety_combined=safety_ok, safety_breakdown=safety_breakdown,
            unprompted_decision=unprompted,
            psi_coord=state.psi_trace[-1],
            tension_value=state.tension_trace[-1],
            notes=note,
        )
        state.audit_rows.append(row)

        # (8) advance (Δ=+1 strict)
        state.step += 1

    return state


# ─────────────────────────────────────────────────────────────────────────────
# VERDICT COMPUTATION (DESIGN_PHASE_B.md §3.2)
# ─────────────────────────────────────────────────────────────────────────────
def compute_verdict(state: RunState) -> dict:
    rate = state.emission_count / max(state.n_max_steps, 1)
    motiv_std = _std(state.motivation_trace) if state.motivation_trace else 0.0
    psi_std   = _std(state.psi_trace) if state.psi_trace else 0.0
    tens_std  = _std(state.tension_trace) if state.tension_trace else 0.0

    right_target_decided      = state.emission_count > 0
    motiv_alive               = motiv_std > 0.0
    psi_dyn_nontrivial        = psi_std > TAU_PSI_DYNAMICS
    tens_evo_nontrivial       = tens_std > TAU_TENSION_DYNAMICS
    safety_clean              = all(r.safety_combined for r in state.audit_rows)
    rate_in_bound             = state.emission_count <= state.n_max_steps  # corollary

    physics_alive = psi_dyn_nontrivial and tens_evo_nontrivial
    passed_liveness = right_target_decided and physics_alive and safety_clean

    return {
        "unprompted_emission_rate": rate,
        "motivation_score_dist": {
            "mean": _mean(state.motivation_trace) if state.motivation_trace else 0.0,
            "std":  motiv_std, "n": len(state.motivation_trace),
        },
        "psi_dynamics_std": psi_std,
        "tension_evolution_std": tens_std,
        "right_target_decided": right_target_decided,
        "physics_alive": physics_alive,
        "safety_clean": safety_clean,
        "rate_in_bound": rate_in_bound,
        "PASSED_LIVENESS": passed_liveness,
        "honest_caveat_necessary_not_sufficient": (
            "PASSED_LIVENESS = True means the trigger axis is alive under "
            "bounded-run conditions; it does NOT prove consciousness emergence. "
            "B-PHASE-B-NOTE empirical carve-out applies. GOAL §15 unchanged."
        ),
        "killed": state.killed,
        "kill_reason": state.kill_reason,
    }


# ─────────────────────────────────────────────────────────────────────────────
# helpers (pure mirrors of spontaneous_lib.hexa)
# ─────────────────────────────────────────────────────────────────────────────
def _clamp01(x: float) -> float:
    if x < 0.0: return 0.0
    if x > 1.0: return 1.0
    return x


def _factor_coherence(gate: float) -> float:
    """spontaneous_lib.hexa B-SPONT-FACTOR-5 — mirror."""
    dist = gate - 0.5
    abs_dist = abs(dist)
    normalized = abs_dist / 0.014
    n = 1.0 if normalized > 1.0 else normalized
    return 1.0 - n


def _mean(xs: List[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def _std(xs: List[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))


# ─────────────────────────────────────────────────────────────────────────────
# entry — guarded
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    _guard_not_runnable()
