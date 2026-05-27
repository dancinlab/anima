#!/usr/bin/env python3
"""run_bounded_emergence.py — §77 emergence-axis direct probe runner.

Extends §24 run_bounded.py with body-production hook + §9 honest_coherent
gate. Runs a 7-cell grid (5 α paths + 1 β cascade control + 1 §24 baseline)
on identical env_state stub (deterministic) for fair head-to-head.

For each cell, per step:
  - thinker_step (8-factor → motivation, byte-equal §24)
  - safety_combined (6/6 controls — same as §24, env_off=False here for
    body-production measurement; kill-switch closed-form tested in §24 B-PHASE-B-RUN-5)
  - talker_should_emit decision
  - if EMIT: produce body via dispatched path; score §9 honest_coherent
  - record physics traces (axis3 psi_dir, axis4 tension)

4-axis verdict per cell:
  axis1 emit_count / n_max
  axis2 motivation dist {mean, std, n}
  axis3 psi_dir std > 1e-4
  axis4 tension std > 1e-4
  axis_new_5 body §9 honest_coherent pass count / pass rate (over emits)
  cell_verdict ∈ {EMERGENCE-AXIS-DIRECTIONAL-POSITIVE,
                  MECHANISM-CONTENT-SPLIT,
                  DECISION-DEAD-NULL,
                  NO-EMIT-N/A}

Necessary-not-sufficient (B-EMERGE-7, B-PHASE-B-RUN-NOTE, B-S77-NOTE):
  stub body §9 pass ≠ trained body §9 pass ≠ GOAL emergence.

NO RNG (env stub is deterministic per-step sinusoidal). NO ckpt forward.
NO GPU. $0 Mac CPU. Wall ~2-3s for 7 cells × 20 steps.
"""
from __future__ import annotations
import argparse
import json
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
# import §24 protocol pure-fn mirrors (deterministic, byte-equal)
sys.path.insert(0, str(HERE.parent / "spontaneous_phase_b_run_2026_05_18"))
from run_bounded import (  # type: ignore
    thinker_step,
    safety_combined, talker_should_emit,
    _safety_kill_switch_on, _safety_rate_limit_ok,
    _safety_phi_ratchet_ok, _safety_content_ok,
    _sensor_phi, _sensor_retrieve_sim, _sensor_curiosity_ema,
    _sensor_tension_delta, _sensor_bridge_gate, _sensor_split_event,
    _sensor_ratchet, _sensor_psi_dir, _sensor_psi_entropy,
    _sensor_tension_value, _silence_seconds,
    N_MAX_STEPS_DEFAULT, IDLE_SPEAK_AFTER,
)

# import §9 honest cascade-rate metric (single SSOT, byte-equal)
sys.path.insert(0, str(HERE.parent / "verify_emergence_metric_2026_05_18"))
from emergence_metric import honest_coherent  # type: ignore

# body stubs
sys.path.insert(0, str(HERE))
from body_production_stubs import (  # noqa: E402
    PATH_NAMES, produce_body, b_identity_5_check_all_emissions,
)


# ════════════════════════════════════════════════════════════════════════════
# 7-cell grid bounded run
# ════════════════════════════════════════════════════════════════════════════

def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0

def _std(xs):
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))


def run_cell(path_name: str, n_max: int = 20) -> dict:
    """Run one path bounded loop. Returns per-cell metrics dict.

    Deterministic (no RNG, no sleep — math.sin/cos closed-form).
    """
    # state
    last_emit_t = -math.inf
    emit_count = 0
    body_pass_count = 0
    body_emits = []        # list of emitted body strings
    body_metrics = []      # list of §9 metric dicts
    mot_trace = []
    psi_trace = []
    tens_trace = []
    safety_trace = []

    # NOTE: no sleep — we use step as "time" proxy for deterministic measurement.
    # Wall-time independence is intentional (B-S77 deterministic invariant).
    for step in range(n_max):
        # simulated t monotonic — derived from step (no time.time())
        t_now = step * 0.1

        # sensors (byte-equal §24 mirror)
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

        # physics traces
        psi_dir = _sensor_psi_dir(step, t_now)
        tens_val = _sensor_tension_value(step, t_now)
        mot_trace.append(score)
        psi_trace.append(psi_dir)
        tens_trace.append(tens_val)

        # safety (env_off=False — kill-switch closed-form in §24 B-PHASE-B-RUN-5)
        env_off = False
        seconds_since_last = (
            t_now - last_emit_t if last_emit_t != -math.inf else 1e6
        )
        kill_on = _safety_kill_switch_on(env_off)
        rate_ok = _safety_rate_limit_ok(seconds_since_last)
        phi_r_ok = _safety_phi_ratchet_ok(phi, ratch)
        content_ok = _safety_content_ok(True)  # dry-run flag
        safety_core = safety_combined(kill_on, rate_ok, phi_r_ok, content_ok)
        meta_present = True
        audit_active = True
        safety_extended = safety_core and meta_present and audit_active
        safety_trace.append(safety_extended)

        unprompted_emit = talker_should_emit(score, safety_extended)

        if unprompted_emit:
            emit_count += 1
            last_emit_t = t_now
            # produce body via dispatched path
            body = produce_body(
                path_name,
                tension=tens_val, psi_dir=psi_dir, phi=phi,
                factors=components, step=step,
            )
            body_emits.append(body)
            # §9 honest_coherent gate
            ok, metrics = honest_coherent(body)
            body_metrics.append(metrics)
            if ok:
                body_pass_count += 1

    # 4-axis (§24 carry) + body axis (§77 new)
    n_eff = max(n_max, 1)
    axis1_rate = emit_count / n_eff
    psi_std = _std(psi_trace)
    tens_std = _std(tens_trace)

    physics_alive = (psi_std > 1e-4) and (tens_std > 1e-4)
    right_target_decided = emit_count > 0
    safety_clean_every_step = all(safety_trace) if safety_trace else False

    # body axis 5 — §9 pass rate over emits (well-defined only if emit > 0)
    body_pass_rate = (
        (body_pass_count / emit_count) if emit_count > 0 else 0.0
    )

    # cell_verdict 4-corner
    if not right_target_decided:
        cell_verdict = "DECISION-DEAD-NULL"  # could be regression or by design (§24 baseline emits 1)
    else:
        if path_name == "s24_baseline_no_body":
            # baseline = decision-only by design
            cell_verdict = "BASELINE-DECISION-ONLY"
        elif body_pass_count >= 1:
            cell_verdict = "EMERGENCE-AXIS-DIRECTIONAL-POSITIVE"
        else:
            cell_verdict = "MECHANISM-CONTENT-SPLIT"

    return {
        "path_name": path_name,
        "n_max_steps": n_max,
        "axis1_emit_count": emit_count,
        "axis1_emit_rate": axis1_rate,
        "axis2_motivation_mean": _mean(mot_trace),
        "axis2_motivation_std": _std(mot_trace),
        "axis2_motivation_n": len(mot_trace),
        "axis3_psi_std": psi_std,
        "axis3_psi_nontrivial": psi_std > 1e-4,
        "axis4_tension_std": tens_std,
        "axis4_tension_nontrivial": tens_std > 1e-4,
        "physics_alive": physics_alive,
        "safety_clean_every_step": safety_clean_every_step,
        "right_target_decided": right_target_decided,
        "axis5_body_pass_count": body_pass_count,
        "axis5_body_pass_rate": body_pass_rate,
        "axis5_body_emits_total": len(body_emits),
        "body_emits": body_emits,
        "body_metrics": body_metrics,
        "cell_verdict": cell_verdict,
    }


def run_grid(n_max: int = 20) -> dict:
    """Run all 7 cells. Returns overall grid result with corner verdict."""
    t_start = time.time()
    cells = {}
    all_emissions = []
    for p in PATH_NAMES:
        cell = run_cell(p, n_max)
        cells[p] = cell
        all_emissions.extend(cell["body_emits"])

    # B-IDENTITY-5 audit across ALL emissions
    id5 = b_identity_5_check_all_emissions(all_emissions)

    # 4-corner overall verdict
    alpha_paths = [p for p in PATH_NAMES if p.startswith("alpha")]
    beta_path = "beta_cascade_control"
    baseline = "s24_baseline_no_body"

    any_alpha_pos = any(
        cells[p]["cell_verdict"] == "EMERGENCE-AXIS-DIRECTIONAL-POSITIVE"
        for p in alpha_paths
    )
    beta_correctly_fails = (cells[beta_path]["axis5_body_pass_count"] == 0)
    baseline_emits = cells[baseline]["axis1_emit_count"]

    if any_alpha_pos and beta_correctly_fails:
        overall = "DIRECTIONAL-POSITIVE-WITH-CONTROL"
    elif any_alpha_pos and not beta_correctly_fails:
        overall = "POSITIVE-BUT-CONTROL-COMPROMISED"   # metric/stub broken — INVALID
    elif (not any_alpha_pos) and beta_correctly_fails:
        overall = "NEGATIVE-SUBSTRATE-PHYSICS-INSUFFICIENT"
    else:
        overall = "FULL-NULL"

    wall = time.time() - t_start

    return {
        "research_md_section": "§77",
        "design_ref": "state/emergence_axis_direct_s77_2026_05_19/DESIGN_FINDINGS.md",
        "n_max_steps_per_cell": n_max,
        "wall_elapsed_sec": round(wall, 3),
        "b_identity_5": id5,
        "cells": cells,
        "overall_verdict": overall,
        "alpha_pass_counts": {
            p: cells[p]["axis5_body_pass_count"] for p in alpha_paths
        },
        "beta_pass_count": cells[beta_path]["axis5_body_pass_count"],
        "baseline_emit_count": baseline_emits,
        "honest_c3": [
            "C3 #1 — Bodies are NOT model outputs. Stub bodies are substrate-physics-derived "
                "closed-form bytes. This probe measures the EMERGENCE-AXIS MEASUREMENT MECHANISM, "
                "NOT a trained-anima emergence claim.",
            "C3 #2 — α-paths may pass §9 by stub-construction tautology. The discriminating "
                "value is (i) β control properly FAILS §9 (sanity); (ii) α-variant differential "
                "pass-rate as mechanism profile; (iii) §24 baseline regression-free.",
            "C3 #3 — necessary-not-sufficient at every layer (B-EMERGE-7, B-PHASE-B-RUN-NOTE, "
                "B-S77-NOTE). §9 pass on stub body ≠ trained body §9 pass ≠ GOAL emergence.",
            "C3 #4 — env_state stub is deterministic sinusoidal — same across all 7 cells, "
                "so axis1/2/3/4 are INTENTIONALLY IDENTICAL per cell (only axis5 body varies "
                "by path). Fair head-to-head by construction.",
            "C3 #5 — α1 high-tension branch (>0.4) intentionally emits digit-cascade as honest "
                "test that §9 catches substrate-physics-driven cascade. If §9 misses it, the "
                "metric is broken (in this run, max tension ~0.45 may briefly hit this branch).",
            "C3 #6 — α3 low-Φ branch (<0.5) intentionally produces len<20 body to test §9 "
                "MIN_LEN gate. Expected to FAIL §9 by design — this is honest measurement of "
                "the gate, not a §77 weakness.",
            "C3 #7 — §24 baseline (s24_baseline_no_body) emits decision but produces empty "
                "body — §9 pass count must be 0 by construction. cell_verdict='BASELINE-"
                "DECISION-ONLY' is correct (not regression).",
            "C3 #8 — rate_limit (30s) under deterministic step*0.1s simulated time means at "
                "most 1 emit per 20-step cell (well below cap). axis1_emit_rate is therefore "
                "structurally ≤ 1/20; not a path differentiator.",
            "C3 #9 — β cascade control (s16 saturated byte-attractor template) MUST §9-FAIL "
                "to validate the metric. If β passes, the run is INVALID and either §9 or "
                "the cascade templates are broken (closed-form B-S77 falsifier asserts).",
            "C3 #10 — GOAL §15/§51/§72 milestone UNCHANGED. §77 = emergence-axis DIRECT "
                "MEASUREMENT MECHANISM design; trained-scale GPU fire is a separate future "
                "cycle (cost-bearing) gated on this $0 stub showing valid measurement.",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="§77 emergence-axis direct probe runner")
    ap.add_argument("--n-max", type=int, default=N_MAX_STEPS_DEFAULT)
    ap.add_argument("--result-json", type=Path, default=HERE / "result.json")
    args = ap.parse_args()

    res = run_grid(n_max=args.n_max)
    args.result_json.write_text(json.dumps(res, indent=2, ensure_ascii=False))

    # short summary print
    print(json.dumps({
        "overall_verdict": res["overall_verdict"],
        "alpha_pass_counts": res["alpha_pass_counts"],
        "beta_pass_count": res["beta_pass_count"],
        "baseline_emit_count": res["baseline_emit_count"],
        "b_identity_5_clean": res["b_identity_5"]["clean"],
        "wall_sec": res["wall_elapsed_sec"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
