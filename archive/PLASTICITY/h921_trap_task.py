#!/usr/bin/env python3
"""h921_trap_task.py — H_921 local-minimum trap few-shot task + falsifier design check.

PURPOSE (M1, design-validation ONLY — NOT the verdict):
  Before spending the single-tenant AKD1000, confirm the H_921 falsifier is SOUND:
    (a) the deterministic SW-det learner collapses to ONE solution (diversity == 1)
        and gets STUCK in a winner-collapse trap  -> the control behaves as claimed.
    (b) a non-deterministic learner (here a numpy tie-break SHADOW) CAN escape the
        trap (diversity > 1, escape_rate > 0) -> the task is SENSITIVE to
        non-determinism, so the falsifier is not trivially un-passable.

⚠ HONEST BOUNDARY (p7 · H_679 closed-negative): the numpy non-det SHADOW below is
   NOT the AKD1000 result. It only proves the TASK can distinguish det vs non-det.
   The real arm-HW (AkidaUnsupervised on-chip, chip-RNG tie-break) runs on pi5-akida
   in M2 and is the ONLY thing that earns the H_921 verdict. SW shadow != HW.

THE TRAP (winner-collapse degeneracy):
  N near-degenerate binary patterns are fed to a winner-take-all Hebbian sweep over
  K units from a fixed init. With deterministic argmax tie-breaking (lowest index),
  every pattern routes to unit 0 -> mode-collapse: all mass on one unit (the trap).
  A learner whose tie-break is non-deterministic distributes winners across units
  -> escapes collapse. "diversity" = unique winner-assignment tuples across episodes;
  "escape" = an episode using > 1 distinct winner unit.
"""
from __future__ import annotations

import hashlib
import json

import numpy as np

IN_DIM = 16
N_UNITS = 10
N_PATTERNS = 12
N_EPISODES = 16
LR = 0.05


def make_trap_patterns(seed: int = 7) -> np.ndarray:
    """Near-degenerate patterns: a shared core (drives a tie) + tiny per-pattern bit.

    The shared core makes every unit's activation near-equal at the first step, so
    the argmax winner is decided by tie-breaking — deterministic tie-break -> always
    unit 0 (collapse); non-deterministic tie-break -> spread.
    """
    rng = np.random.default_rng(seed)
    core = np.zeros(IN_DIM, dtype=np.uint8)
    core[:8] = 1  # shared dominant core -> near-degenerate activations
    pats = np.tile(core, (N_PATTERNS, 1))
    # one distinguishing bit per pattern in the tail (weak signal, doesn't break tie)
    for i in range(N_PATTERNS):
        pats[i, 8 + (i % 8)] = 1
    return pats.astype(np.uint8)


def _winner(act: np.ndarray, tiebreak: str, rng) -> int:
    """argmax with a configurable tie-break among near-equal activations."""
    top = float(np.max(act))
    ties = np.flatnonzero(act >= top - 1e-6)
    if tiebreak == "det":
        return int(ties[0])            # deterministic: lowest index -> collapse
    return int(rng.choice(ties))       # non-det shadow: random among ties -> spread


def run_episode(x: np.ndarray, *, tiebreak: str, init_seed: int, tb_seed: int) -> dict:
    """One few-shot edge-learn episode. Fixed init (init_seed shared across arms);
    only the tie-break source differs (det vs non-det shadow).

    Faithful to AKD1000 weights_bits=1: integer (binary) weights -> integer dot
    activations -> exact ties are NATURAL. Init is IDENTICAL across units (the
    degenerate trap): step-1 every unit is exactly tied, so the FIRST winner is
    decided purely by the tie-break source. Deterministic tie-break -> always
    unit 0 -> every episode collapses to the SAME unit (diversity 1, the trap).
    Non-det tie-break -> a different seed unit per episode -> diversity > 1."""
    init_rng = np.random.default_rng(init_seed)          # SHARED fixed init
    w0 = (init_rng.random(IN_DIM) < 0.5).astype(np.int32)  # one binary row...
    W = np.tile(w0, (N_UNITS, 1))                        # ...broadcast to ALL units (tie)
    tb_rng = np.random.default_rng(tb_seed)              # tie-break RNG (shadow only)
    winners = []
    for row in x.astype(np.int32):
        win = _winner((W @ row).astype(np.float64), tiebreak, tb_rng)
        winners.append(win)
        W[win] = ((W[win] + row) > 0).astype(np.int32)   # binary Hebbian set-bit
    assign = tuple(winners)
    n_distinct = len(set(winners))
    return {
        "winners": assign,
        "n_distinct_units": n_distinct,
        "escaped_collapse": n_distinct > 1,
        "assign_hash": hashlib.sha256(repr(assign).encode()).hexdigest()[:12],
    }


def bootstrap_ci(vals, n_boot=2000, seed=1):
    rng = np.random.default_rng(seed)
    arr = np.asarray(vals, dtype=np.float64)
    boots = [rng.choice(arr, size=len(arr), replace=True).mean() for _ in range(n_boot)]
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return float(lo), float(hi)


def main():
    x = make_trap_patterns()
    fixed_init = 187  # SHARED across both arms — only tie-break source varies

    # arm-SW-det: deterministic tie-break -> the single trap solution (diversity 1)
    det = [run_episode(x, tiebreak="det", init_seed=fixed_init, tb_seed=0)
           for _ in range(N_EPISODES)]
    det_hashes = {e["assign_hash"] for e in det}
    trap_hash = det[0]["assign_hash"]                    # THE deterministic trap solution
    det_escape = [int(e["assign_hash"] != trap_hash) for e in det]  # escape = differ from trap

    # arm-SW-nondet SHADOW (NOT HW): random tie-break -> diversity>1, escapes the trap
    nd = [run_episode(x, tiebreak="nondet", init_seed=fixed_init, tb_seed=1000 + i)
          for i in range(N_EPISODES)]
    nd_hashes = {e["assign_hash"] for e in nd}
    nd_escape = [int(e["assign_hash"] != trap_hash) for e in nd]   # escape = differ from det trap
    nd_ci = bootstrap_ci(nd_escape)

    out = {
        "task": "h921_winner_collapse_trap",
        "n_episodes": N_EPISODES,
        "n_patterns": N_PATTERNS,
        "fixed_init_seed": fixed_init,
        "arm_sw_det": {
            "diversity": len(det_hashes),         # expect 1 (deterministic)
            "escape_rate": float(np.mean(det_escape)),
            "trapped": len(det_hashes) == 1 and sum(det_escape) == 0,
        },
        "arm_sw_nondet_shadow": {
            "diversity": len(nd_hashes),          # expect > 1
            "escape_rate": float(np.mean(nd_escape)),
            "escape_ci95": nd_ci,
            "NOT_HW": "numpy tie-break shadow — design check only, != AKD1000 (H_679)",
        },
        "design_check": {
            "det_collapses_to_one": len(det_hashes) == 1,
            "task_sensitive_to_nondet": len(nd_hashes) > 1 and nd_ci[0] > 0,
            "falsifier_sound": (len(det_hashes) == 1) and (len(nd_hashes) > 1) and (nd_ci[0] > 0),
        },
        "honest_note": ("M1 design-validation. arm-HW (AkidaUnsupervised on-chip, "
                        "chip-RNG tie-break) runs on pi5-akida in M2 and is the ONLY "
                        "arm that earns the verdict. SW shadow proves the task can "
                        "distinguish det vs non-det; it does NOT predict the HW result."),
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
