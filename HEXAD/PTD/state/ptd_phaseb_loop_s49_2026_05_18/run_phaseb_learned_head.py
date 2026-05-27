#!/usr/bin/env python3
"""run_phaseb_learned_head.py — RESEARCH.md §49.

§24 SPONTANEOUS Phase B bounded-run loop, but the emission decision is the
§48-scale-validated PTD-aux DH-DL learned head's argmax INSTEAD OF the
§24 hand-coded `talker_should_emit(score, safety_ok)` threshold.

The §48 head (state/dhdl_ptd_scaleup_s48_2026_05_18/dhdl_ptd_head_s48_lam03.json)
is `shared trunk 14->32` + `decision head 32->16->3` over the 14 §24 feature
keys. Its argmax over {CONTINUE_THINK, EMIT_VOICE, REMAIN_SILENT} replaces the
scalar threshold. **Safety still overrides** — the 6-control safety
conjunction (B-S49-1 connection-point, mirror §27 B-DHDL-4) gates the head
output: if not safety_extended_ok ⇒ NO emit regardless of head argmax.

What this measures (§49):
  - unprompted_emission_rate: learned-head loop vs threshold loop
  - per-step decision divergence: steps where learned-head ≠ threshold IN
    THE LIVE LOOP (under identical env_state stub sequence)
  - capability-vs-distillation: is any divergence something the threshold
    CANNOT produce, or is it distillation approximation noise?

g3 honest (stated up front, before measuring): this is almost certainly
DISTILLATION-level. The §48 head was supervised to imitate the §24
hand-coded threshold (§27/§38/§44/§48: decision label IS the threshold's
output). A faithful distillation should mostly AGREE with the threshold;
divergences are approximation noise, not new capability. §27 measured a
threshold-distillation gap of 0.00063 (head under-fits in 6/9598 records).
This cycle tests whether that residual gap manifests as a DIFFERENT
emission pattern IN THE LIVE LOOP. NOT GOAL emergence. north-star unchanged.

Hard guards / scope identical to §24 run_bounded.py: step ≤ N_MAX,
outer wall, top-of-loop kill_check, NO user input (unprompted), NO body
production, NO model.forward, NO GPU. $0 Mac CPU numpy head + pure-fn loop.

Usage: python3 run_phaseb_learned_head.py [--head PATH] [--mode head|threshold]
"""
from __future__ import annotations
import argparse
import json
import math
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import numpy as np

# Reuse §24 SSOT machinery byte-equal (sensors, 8-factor, 6-control safety,
# audit logger). The §24 run_bounded.py is the SSOT for the protocol.
_S24 = Path(__file__).resolve().parents[1] / "spontaneous_phase_b_run_2026_05_18"
sys.path.insert(0, str(_S24))
import run_bounded as s24  # noqa: E402  (§24 SSOT)
from audit_logger import (  # noqa: E402
    AuditLogger, iso8601_now,
    ACTION_THINK_ONLY, ACTION_EMIT, ACTION_SAFETY_BLOCK,
)

# §48 scale-validated head canonical path
HEAD_DEFAULT = (
    Path(__file__).resolve().parents[1]
    / "dhdl_ptd_scaleup_s48_2026_05_18" / "dhdl_ptd_head_s48_lam03.json"
)

# §48 feature ordering (decision label space, head input vector)
FEATURE_KEYS = (
    "f_relevance", "f_info_gap", "f_curiosity", "f_pain",
    "f_coherence", "f_originality", "f_balance", "f_dynamics",
    "psi_dir", "psi_entropy", "tension", "thinker_score",
    "seconds_since_last", "ratchet",
)
LABELS = ("CONTINUE_THINK", "EMIT_VOICE", "REMAIN_SILENT")
EMIT_IDX = 1  # LABELS.index("EMIT_VOICE")


# ════════════════════════════════════════════════════════════════════════════
# §48 LEARNED HEAD — pure numpy forward (shared trunk + decision head only)
# ════════════════════════════════════════════════════════════════════════════
class LearnedHead:
    """Pure-fn forward of the §48 DH-DL shared trunk + decision head.

    NO training, NO weight mutation, NO backward — inference read-out only
    (mirror §27 B-DHDL: head is the learned imitation of the §24 threshold).
    """

    def __init__(self, head_json: dict):
        h = head_json["head"]
        self.W1 = np.asarray(h["shared"]["W1"], dtype=np.float64)
        self.b1 = np.asarray(h["shared"]["b1"], dtype=np.float64)
        self.Wd2 = np.asarray(h["decision"]["W2"], dtype=np.float64)
        self.bd2 = np.asarray(h["decision"]["b2"], dtype=np.float64)
        self.Wd3 = np.asarray(h["decision"]["W3"], dtype=np.float64)
        self.bd3 = np.asarray(h["decision"]["b3"], dtype=np.float64)
        self.mean = np.asarray(head_json["feature_mean"], dtype=np.float64)
        self.std = np.asarray(head_json["feature_std"], dtype=np.float64)
        self.std[self.std == 0.0] = 1.0
        self.feature_keys = tuple(head_json["feature_keys"])
        assert self.feature_keys == FEATURE_KEYS, (
            f"head feature_keys mismatch: {self.feature_keys}")

    def decide(self, feat: dict) -> tuple[int, list]:
        x = np.asarray([float(feat[k]) for k in FEATURE_KEYS],
                        dtype=np.float64)
        xn = (x - self.mean) / self.std
        a1 = np.maximum(xn @ self.W1 + self.b1, 0.0)
        ad2 = np.maximum(a1 @ self.Wd2 + self.bd2, 0.0)
        z = ad2 @ self.Wd3 + self.bd3
        z = z - z.max()
        e = np.exp(z)
        p = e / e.sum()
        return int(np.argmax(p)), p.tolist()


# ════════════════════════════════════════════════════════════════════════════
# BOUNDED RUN — §24 loop with learned-head OR threshold decision (mode toggle)
# ════════════════════════════════════════════════════════════════════════════
@dataclass
class LoopResult:
    mode: str
    n_max_steps: int
    actual_steps: int = 0
    wall_elapsed_sec: float = 0.0
    killed: bool = False
    kill_reason: Optional[str] = None
    emission_count: int = 0
    motivation_trace: List[float] = field(default_factory=list)
    psi_dir_trace: List[float] = field(default_factory=list)
    tension_trace: List[float] = field(default_factory=list)
    safety_trace: List[bool] = field(default_factory=list)
    # per-step decision record (both decisions computed every step for the
    # divergence comparison — only the active mode's decision drives emit)
    threshold_decision: List[bool] = field(default_factory=list)
    head_decision: List[bool] = field(default_factory=list)
    head_argmax: List[int] = field(default_factory=list)
    action_counts: dict = field(default_factory=dict)


def run_loop(
    head: LearnedHead,
    mode: str,
    n_max_steps: int = s24.N_MAX_STEPS_DEFAULT,
    t_max_wall_sec: float = s24.T_MAX_WALL_SEC_DEFAULT,
    think_interval_sec: float = s24.THINK_INTERVAL_TEST_SEC,
    audit_log_path: Optional[Path] = None,
    content_clean_dryrun: bool = True,
) -> LoopResult:
    """§24 bounded loop. mode ∈ {head, threshold}.

    Both the threshold decision (§24 talker_should_emit) AND the learned-head
    argmax are computed every step (identical env_state stub sequence), so
    per-step divergence is measurable. The `mode` selects which one drives
    the actual emit + audit action. Safety conjunction OVERRIDES both
    (B-S49-1 connection-point — 6-control AND, mirror §27 B-DHDL-4).
    """
    assert mode in ("head", "threshold"), mode
    if audit_log_path is None:
        audit_log_path = Path(__file__).parent / f"audit_log_{mode}.jsonl"
    assert abs(s24.WEIGHTS_SUM - 1.0) < 1e-12

    res = LoopResult(
        mode=mode, n_max_steps=n_max_steps,
        action_counts={ACTION_THINK_ONLY: 0, ACTION_EMIT: 0,
                       ACTION_SAFETY_BLOCK: 0},
    )
    t_start = time.time()
    last_emit_t = -math.inf

    with AuditLogger(audit_log_path) as logger:
        step = 0
        while step < n_max_steps:
            wall_elapsed = time.time() - t_start
            if wall_elapsed > t_max_wall_sec:
                res.killed = True
                res.kill_reason = "wall_timer"
                break
            if s24._kill_check_env_off():
                res.killed = True
                res.kill_reason = "kill_switch_env_off"
                logger.write_step({
                    "timestamp_iso8601": iso8601_now(), "step": step,
                    "thinker_score": 0.0,
                    "motivation_components": {k: 0.0 for k in
                        ["relevance", "info_gap", "curiosity", "pain",
                         "coherence", "originality", "balance", "dynamics"]},
                    "psi_dir": 0.0, "psi_entropy": 0.0, "tension": 0.0,
                    "safety_flags": {
                        "kill_switch_on": False, "rate_limit_ok": False,
                        "content_filter_ok": False, "phi_ratchet_ok": False,
                        "meta_tag_present": True, "audit_log_active": True},
                    "talker_decision": False, "action": ACTION_SAFETY_BLOCK,
                })
                res.action_counts[ACTION_SAFETY_BLOCK] += 1
                break

            time.sleep(think_interval_sec)
            t_now = time.time() - t_start

            # ── §24 sensors → 8-factor motivation (byte-equal SSOT) ──────
            silence_s = s24._silence_seconds(step, t_now, last_emit_t)
            phi = s24._sensor_phi(step, t_now)
            retrieve_sim = s24._sensor_retrieve_sim(step, t_now)
            cur_ema = s24._sensor_curiosity_ema(step, t_now)
            tens_delta = s24._sensor_tension_delta(step, t_now)
            bridge_g = s24._sensor_bridge_gate(step, t_now)
            split_ev = s24._sensor_split_event(step)
            ratch = s24._sensor_ratchet(step)
            score, comps = s24.thinker_step(
                phi, retrieve_sim, cur_ema, tens_delta, bridge_g,
                split_ev, ratch, silence_s)

            psi_dir = s24._sensor_psi_dir(step, t_now)
            psi_ent = s24._sensor_psi_entropy(step)
            tens_val = s24._sensor_tension_value(step, t_now)
            res.motivation_trace.append(score)
            res.psi_dir_trace.append(psi_dir)
            res.tension_trace.append(tens_val)

            # ── §24 6-control safety (byte-equal SSOT) ───────────────────
            env_off = s24._kill_check_env_off()
            seconds_since_last = (
                t_now - last_emit_t if last_emit_t != -math.inf else 1e6)
            kill_on = s24._safety_kill_switch_on(env_off)
            rate_ok = s24._safety_rate_limit_ok(seconds_since_last)
            phi_r_ok = s24._safety_phi_ratchet_ok(phi, ratch)
            content_ok = s24._safety_content_ok(content_clean_dryrun)
            safety_core = s24.safety_combined(
                kill_on, rate_ok, phi_r_ok, content_ok)
            meta_present = True
            audit_active = True
            safety_ok = safety_core and meta_present and audit_active
            res.safety_trace.append(safety_ok)

            # ── DECISION (both computed every step) ──────────────────────
            # threshold: §24 talker_should_emit(score, safety_ok)
            thr_emit = s24.talker_should_emit(score, safety_ok)
            # head: §48 argmax → EMIT iff argmax==EMIT_VOICE AND safety_ok
            #       (B-S49-1: 6-control safety conjunction OVERRIDES head;
            #        mirror §27 B-DHDL-4 SAFETY-OVERRIDE-CLOSED)
            feat = {
                "f_relevance": comps["relevance"],
                "f_info_gap": comps["info_gap"],
                "f_curiosity": comps["curiosity"],
                "f_pain": comps["pain"],
                "f_coherence": comps["coherence"],
                "f_originality": comps["originality"],
                "f_balance": comps["balance"],
                "f_dynamics": comps["dynamics"],
                "psi_dir": psi_dir, "psi_entropy": psi_ent,
                "tension": tens_val, "thinker_score": score,
                "seconds_since_last": seconds_since_last,
                "ratchet": ratch,
            }
            argmax, _probs = head.decide(feat)
            head_emit = bool(argmax == EMIT_IDX and safety_ok)

            res.threshold_decision.append(bool(thr_emit))
            res.head_decision.append(head_emit)
            res.head_argmax.append(argmax)

            active_emit = head_emit if mode == "head" else bool(thr_emit)

            if not safety_ok:
                action = ACTION_SAFETY_BLOCK
            elif active_emit:
                action = ACTION_EMIT
                res.emission_count += 1
                last_emit_t = t_now
            else:
                action = ACTION_THINK_ONLY
            res.action_counts[action] += 1

            logger.write_step({
                "timestamp_iso8601": iso8601_now(), "step": step,
                "thinker_score": score, "motivation_components": comps,
                "psi_dir": psi_dir, "psi_entropy": psi_ent,
                "tension": tens_val,
                "safety_flags": {
                    "kill_switch_on": kill_on, "rate_limit_ok": rate_ok,
                    "content_filter_ok": content_ok,
                    "phi_ratchet_ok": phi_r_ok,
                    "meta_tag_present": meta_present,
                    "audit_log_active": audit_active},
                "talker_decision": bool(active_emit),
                "action": action,
            })
            step += 1

        res.actual_steps = step
        res.wall_elapsed_sec = time.time() - t_start
    return res


def _summarise(res: LoopResult) -> dict:
    n_eff = max(res.n_max_steps, 1)
    return {
        "mode": res.mode,
        "unprompted_emission_rate": res.emission_count / n_eff,
        "emission_count": res.emission_count,
        "actual_steps": res.actual_steps,
        "wall_elapsed_sec": round(res.wall_elapsed_sec, 4),
        "killed": res.killed, "kill_reason": res.kill_reason,
        "action_counts": res.action_counts,
        "threshold_decision": res.threshold_decision,
        "head_decision": res.head_decision,
        "head_argmax": res.head_argmax,
        "safety_trace": res.safety_trace,
        "motivation_trace": res.motivation_trace,
        "psi_dir_trace": res.psi_dir_trace,
        "tension_trace": res.tension_trace,
    }


def main() -> int:
    here = Path(__file__).parent
    ap = argparse.ArgumentParser(description="§49 PTD-aux head ↔ §24 loop")
    ap.add_argument("--head", type=Path, default=HEAD_DEFAULT)
    ap.add_argument("--mode", choices=["head", "threshold"], default="head")
    ap.add_argument("--n-max", type=int, default=s24.N_MAX_STEPS_DEFAULT)
    ap.add_argument("--out", type=Path,
                    default=here / "loop_result.json")
    args = ap.parse_args()

    head_json = json.loads(Path(args.head).read_text(encoding="utf-8"))
    head = LearnedHead(head_json)
    res = run_loop(head, args.mode, n_max_steps=args.n_max,
                   audit_log_path=here / f"audit_log_{args.mode}.jsonl")
    out = _summarise(res)
    out["head_path"] = str(args.head)
    out["head_section"] = head_json.get("research_md_section", "?")
    out["head_lambda_ptd"] = head_json.get("lambda_ptd")
    args.out.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps({k: out[k] for k in (
        "mode", "unprompted_emission_rate", "emission_count",
        "actual_steps")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
