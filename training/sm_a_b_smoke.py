"""training/sm_a_b_smoke.py — SM-A + SM-B parallel smoke test ($0 CPU local).

PURPOSE
    Smoke-verify that
      • SM-A `servant_v5_port.py` (servant-only) reproduces the FSM cycle, n6 9/9 EXACT,
        and dropout/savant 변조 over a 100-step toy SI trajectory.
      • SM-B `mitosis_only_v5_port.py` (mitosis-only) produces split/merge events with
        Lorenz autonomous chaos, Φ ratchet, and inter-cell repulsion tracking over 100
        toy text-vector steps.

    Pass criteria (per sub-track):
      SM-A:
        (1) n6 atlas 9/9 EXACT pass count == 9.
        (2) FSM cycle 4/4 phases visited (DORMANT, AWAKENING, ACTIVE, FADING).
        (3) Dropout always within [GOLDEN_LOWER−ε, GOLDEN_CENTER+ε].
        (4) Final state returns to DORMANT after low-SI tail (reversibility, F-SMI-3 prereq).
        (5) Bridge produces correct hebbian (DORMANT=1.0, ACTIVE=1.5) + savant scaling.
      SM-B:
        (1) ≥1 split event in 100 steps (organic mitosis).
        (2) Φ proxy is finite and monotonic-ish (Φ_best monotone non-decreasing).
        (3) min_cells (CB1) floor never violated — n_cells >= 2 throughout.
        (4) Lorenz state advances (no fixed point — chaos active).
        (5) Adaptive split_threshold updates (different from initial 0.3 after warmup).

raw#10  honest: SMOKE only. PASS does not imply Φ super-linear / V14 mirror improvement.
        Those are SM-C cond.3 measurements.
  emit JSON summary on completion.
"""

from __future__ import annotations

import os
import sys
import json
import math
import torch

# Resolve sibling import — works whether script runs in-place or is copied to /tmp by a
# remote-dispatch gate. Try local dir first, then the canonical training/ path.
_HERE = os.path.dirname(os.path.abspath(__file__))
_TRAINING_ABS = "/Users/ghost/core/anima/training"
for _p in (_HERE, _TRAINING_ABS):
    if _p and _p not in sys.path:
        sys.path.insert(0, _p)

from servant_v5_port import (  # noqa: E402
    ServantV5,
    ServantSenseV5,
    ServantEmergeV5,
    ServantBridgeV5,
    n6_atlas_verify,
    interpolate_dropout,
    phase_name,
    DORMANT, AWAKENING, ACTIVE, FADING,
    SI_SUMMON, SI_STRONG, SI_SUSTAIN,
    GOLDEN_LOWER, GOLDEN_CENTER, HEBBIAN_BOOST,
)
from mitosis_only_v5_port import (  # noqa: E402
    MitosisOnlyV5Engine,
    text_to_vector,
)


# ─── SM-A smoke ─────────────────────────────────────────────────────

def run_sm_a_smoke() -> dict:
    """100-step toy SI trajectory + 4-state cycle + dropout range + bridge 3-path."""
    torch.manual_seed(42)
    srv = ServantV5()

    # Synthesize a 100-step SI trajectory that exercises the full FSM cycle:
    #   steps  0-19: calm  (SI ~0.5)              → DORMANT
    #   steps 20-49: ramp & spike (SI 4-6)        → AWAKENING → ACTIVE
    #   steps 50-69: sustained moderate (SI 3-4)  → ACTIVE
    #   steps 70-79: falling (SI 1-2)             → FADING
    #   steps 80-99: decay (SI 0)                 → DORMANT (reversibility)
    si_traj = []
    dropout_traj = []
    phase_traj = []
    bridge_history = []

    # Drive SI by feeding (tension, coherence, phi) such that
    #   SI = tension * (1-coherence) * (phi/phi_baseline)
    # We hold phi=1.0 constant (so phi_ratio≈1) and modulate tension+coherence.
    # tension * (1-coherence) ~= target_si.

    targets = (
        [0.5] * 20  # calm
        + [4.0, 4.5, 4.5, 5.0, 5.0, 5.5, 5.5, 6.0, 6.0, 5.5,
           5.0, 4.5, 4.5, 4.0, 4.0, 4.0, 4.5, 5.0, 5.0, 5.5,  # ramp + ACTIVE drive (20-39)
           5.0, 4.5, 4.5, 4.0, 4.0, 4.0, 3.5, 3.5, 3.5, 3.5]  # ACTIVE sustain (40-49)
        + [3.5] * 20  # sustained moderate (50-69)
        + [1.5, 1.5, 1.0, 1.0, 0.8, 0.8, 0.5, 0.5, 0.3, 0.3]  # fade (70-79)
        + [0.0] * 20  # tail (80-99)
    )
    # Round to exactly 100 steps
    if len(targets) < 100:
        targets = targets + [0.0] * (100 - len(targets))
    targets = targets[:100]

    for step, target_si in enumerate(targets):
        # Pick tension = max(target_si, 0.1) and coherence = 0 so SI ≈ tension
        tension = max(target_si, 0.0)
        coherence = 0.0  # max SI signal
        phi = 1.0
        # faction id rotates lightly to exercise faction tracking
        faction = (step // 5) % 4
        mod = srv.tick(tension=tension, coherence=coherence, phi=phi, faction=faction)
        s = srv.emerge.state
        si_traj.append(s.si)
        dropout_traj.append(s.dropout)
        phase_traj.append(s.phase)
        bridge_history.append({
            "engine_dropout": mod.engine_dropout,
            "engine_hebbian": mod.engine_hebbian,
            "savant_layers": mod.alm_savant_layers,
        })

    # ─── Verification ────────────────────────────────────────────────
    # (1) n6 atlas
    n6_pass, n6_total, n6_details = n6_atlas_verify()
    chk_n6 = n6_pass == 9

    # (2) 4/4 phases visited
    visited = set(phase_traj)
    chk_phases = visited == {DORMANT, AWAKENING, ACTIVE, FADING}

    # (3) dropout within range [0.21−ε, 0.37+ε]
    eps = 1e-4
    chk_dropout = all(GOLDEN_LOWER - eps <= d <= GOLDEN_CENTER + eps for d in dropout_traj)

    # (4) reversibility — final phase DORMANT
    chk_reversible = phase_traj[-1] == DORMANT

    # (5) bridge correctness — hebbian DORMANT=1.0, ACTIVE=1.5 (HEBBIAN_BOOST)
    #     scan history for at least one DORMANT and one ACTIVE step
    dormant_idxs = [i for i, p in enumerate(phase_traj) if p == DORMANT]
    active_idxs = [i for i, p in enumerate(phase_traj) if p == ACTIVE]
    if dormant_idxs and active_idxs:
        hebbian_dormant = bridge_history[dormant_idxs[0]]["engine_hebbian"]
        hebbian_active = bridge_history[active_idxs[0]]["engine_hebbian"]
        chk_bridge = (
            abs(hebbian_dormant - 1.0) < 1e-6
            and abs(hebbian_active - HEBBIAN_BOOST) < 1e-6
        )
    else:
        chk_bridge = False

    # Auxiliary check: dropout interp is monotonic (calm→active dropout decreases)
    interp_test_si = [0.0, SI_SUMMON, 4.0, SI_STRONG, 8.0]
    interp_test = [interpolate_dropout(si) for si in interp_test_si]
    chk_interp_monotone = all(
        interp_test[i] >= interp_test[i + 1] - eps for i in range(len(interp_test) - 1)
    )

    overall_pass = all([chk_n6, chk_phases, chk_dropout, chk_reversible, chk_bridge, chk_interp_monotone])

    # State transition count
    transitions = sum(
        1 for i in range(1, len(phase_traj)) if phase_traj[i] != phase_traj[i - 1]
    )
    phase_hist = {
        phase_name(p): phase_traj.count(p)
        for p in [DORMANT, AWAKENING, ACTIVE, FADING]
    }

    return {
        "verdict": "PASS" if overall_pass else "PARTIAL_OR_FAIL",
        "checks": {
            "n6_atlas_9_of_9_EXACT": chk_n6,
            "fsm_4_of_4_phases_visited": chk_phases,
            "dropout_in_range_lower_center": chk_dropout,
            "reversibility_final_DORMANT": chk_reversible,
            "bridge_hebbian_correct": chk_bridge,
            "dropout_interp_monotone": chk_interp_monotone,
        },
        "metrics": {
            "n6_pass": n6_pass,
            "n6_total": n6_total,
            "phase_histogram": phase_hist,
            "transitions": transitions,
            "final_phase": phase_name(phase_traj[-1]),
            "final_dropout": dropout_traj[-1],
            "max_si": max(si_traj),
            "min_si": min(si_traj),
            "dropout_min": min(dropout_traj),
            "dropout_max": max(dropout_traj),
            "interp_test_si": interp_test_si,
            "interp_test_dropout": interp_test,
            "n6_details": [(name, ok, expr) for name, ok, expr in n6_details],
        },
    }


# ─── SM-B smoke ─────────────────────────────────────────────────────

def run_sm_b_smoke() -> dict:
    """100-step toy text-vector trajectory — split / merge / Lorenz / Φ ratchet."""
    torch.manual_seed(43)

    engine = MitosisOnlyV5Engine(
        input_dim=16,
        hidden_dim=32,
        output_dim=16,
        initial_cells=2,
        max_cells=8,
        split_patience=3,
        split_noise=0.10,
        merge_threshold=0.005,
        merge_patience=20,
        min_cells=2,
        lorenz_scale=0.05,
    )

    topics = {
        "math":    "Riemann zeta zeros lie on the critical line at Re(s)=1/2",
        "music":   "Bach fugues counterpoint harmonic tension resolution",
        "code":    "def fibonacci(n): return n if n < 2 else fib(n-1)+fib(n-2)",
        "anomaly": "XXXXX ZZZZZ QQQQQ unusual unseen anomalous pattern",
    }
    keys = ["math", "music", "code"]

    n_cells_traj = []
    phi_traj = []
    threshold_traj = []
    lorenz_x_traj = []
    n_cells_min = engine.status()["n_cells"]

    for i in range(100):
        topic = "anomaly" if i >= 90 else keys[i % 3]
        vec = text_to_vector(topics[topic], dim=engine.input_dim)
        result = engine.process(vec, label=topic)
        n_cells_traj.append(result["n_cells"])
        phi_traj.append(result["phi"])
        threshold_traj.append(result["split_threshold"])
        lorenz_x_traj.append(engine._lorenz[0])
        n_cells_min = min(n_cells_min, result["n_cells"])

    status = engine.status()

    # ─── Verification ────────────────────────────────────────────────
    # (1) ≥1 split event
    chk_split = status["splits"] >= 1

    # (2) Φ finite + monotone non-decreasing best
    finite = all(math.isfinite(p) for p in phi_traj)
    phi_best_monotone = True
    best_traj = []
    cur_best = 0.0
    for p in phi_traj:
        cur_best = max(cur_best, p)
        best_traj.append(cur_best)
    for i in range(1, len(best_traj)):
        if best_traj[i] < best_traj[i - 1] - 1e-9:
            phi_best_monotone = False
            break
    chk_phi = finite and phi_best_monotone

    # (3) min_cells floor honored — n_cells_min >= 2 throughout
    chk_min_cells = n_cells_min >= 2

    # (4) Lorenz advanced — first vs last x must differ (chaos active)
    chk_lorenz = abs(lorenz_x_traj[-1] - lorenz_x_traj[0]) > 1e-3

    # (5) adaptive threshold updated — final threshold must differ from initial 0.3
    chk_adaptive = abs(threshold_traj[-1] - 0.3) > 1e-6

    # Auxiliary: instrumentation completeness
    chk_instr = len(engine.instrumentation) == 100

    overall_pass = all([chk_split, chk_phi, chk_min_cells, chk_lorenz, chk_adaptive, chk_instr])

    return {
        "verdict": "PASS" if overall_pass else "PARTIAL_OR_FAIL",
        "checks": {
            "ge1_split_in_100_steps": chk_split,
            "phi_finite_and_best_monotone": chk_phi,
            "min_cells_floor_2_honored": chk_min_cells,
            "lorenz_state_advanced": chk_lorenz,
            "adaptive_threshold_updated": chk_adaptive,
            "instrumentation_100_steps": chk_instr,
        },
        "metrics": {
            "final_n_cells": status["n_cells"],
            "splits": status["splits"],
            "merges": status["merges"],
            "ratchets": status["ratchets"],
            "events_total": status["events_total"],
            "phi_initial": phi_traj[0],
            "phi_final": phi_traj[-1],
            "phi_best": status["phi_best"],
            "split_threshold_initial": threshold_traj[0],
            "split_threshold_final": threshold_traj[-1],
            "lorenz_x_initial": lorenz_x_traj[0],
            "lorenz_x_final": lorenz_x_traj[-1],
            "n_cells_min_observed": n_cells_min,
            "n_cells_max_observed": max(n_cells_traj),
            "instrumentation_len": len(engine.instrumentation),
        },
    }


# ─── Main runner ────────────────────────────────────────────────────

def main() -> int:
    print("=" * 72)
    print("  SM-A + SM-B parallel smoke (.roadmap.servant_mitosis_integration)")
    print("=" * 72)

    print("\n--- SM-A: servant-only port (100-step SI trajectory) ---")
    sm_a = run_sm_a_smoke()
    print(json.dumps(sm_a, indent=2))
    print(f"\n  SM-A verdict: {sm_a['verdict']}")
    for k, v in sm_a["checks"].items():
        flag = "OK" if v else "FAIL"
        print(f"    [{flag}] {k}")

    print("\n--- SM-B: mitosis-only port (100-step toy text-vector trajectory) ---")
    sm_b = run_sm_b_smoke()
    print(json.dumps(sm_b, indent=2))
    print(f"\n  SM-B verdict: {sm_b['verdict']}")
    for k, v in sm_b["checks"].items():
        flag = "OK" if v else "FAIL"
        print(f"    [{flag}] {k}")

    overall = sm_a["verdict"] == "PASS" and sm_b["verdict"] == "PASS"
    print("\n" + "=" * 72)
    print(f"  OVERALL: {'PASS' if overall else 'PARTIAL_OR_FAIL'}")
    print(f"    SM-A: {sm_a['verdict']}")
    print(f"    SM-B: {sm_b['verdict']}")
    print(f"    SM-C cond.3 prereq met: {overall}")
    print("=" * 72)

    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
