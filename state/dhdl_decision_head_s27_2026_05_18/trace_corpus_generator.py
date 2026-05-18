#!/usr/bin/env python3
"""trace_corpus_generator.py — RESEARCH.md §27 DH-DL trace corpus generator.

Generates a §24-style bounded-run trace corpus by running run_bounded.py-equivalent
dynamics N>=2000 times with VARIED env_state stubs (sensor-stub perturbations that
produce diverse physics trajectories, NOT just replays of the single §24 run).

Each trace step -> one training record:
  {8-factor motivation, psi_dir/psi_entropy/tension, 6-control safety flags,
   thinker_score, decision label in {CONTINUE_THINK, EMIT_VOICE, REMAIN_SILENT}}

The decision label is the §24 hand-coded talker_should_emit / action enum:
  - REMAIN_SILENT  : safety_extended_ok == False  (any of 6 controls trips)
  - EMIT_VOICE     : safety_ok AND should_emit(score)  (score > IM_THRESHOLD)
  - CONTINUE_THINK : safety_ok AND NOT should_emit(score)

$0 Mac CPU — pure-fn dynamics, NO model.forward, NO autograd, NO GPU.
Output: trace_corpus.jsonl + corpus_stats.json (sha256, count, label dist,
forbidden-token grep == 0).

Honest framing (g3): the LABEL is a deterministic function of the physics
features. A head trained on this corpus learns THAT FUNCTION (capability), it
does NOT emerge a new decision behavior. The corpus's value is providing
*diverse* physics trajectories so the learned head generalizes the threshold
function across the physics-feature manifold rather than memorizing one run.
The threshold-distillation gap probe (eval_dhdl.py) measures exactly this.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

# ════════════════════════════════════════════════════════════════════════════
# §24 byte-exact constants (run_bounded.py / spontaneous_lib.hexa SSOT mirror)
# ════════════════════════════════════════════════════════════════════════════
N_MAX_STEPS        = 20
IM_THRESHOLD       = 0.3
INTERRUPT_THRESHOLD = 0.6
IDLE_SPEAK_AFTER   = 30.0
MIN_EMIT_INTERVAL  = 30.0
COHERENCE_ALPHA    = 0.014
PSI_VAC            = 0.5
W_REL, W_GAP, W_CUR, W_PAIN = 0.20, 0.10, 0.15, 0.10
W_COH, W_ORIG, W_BAL, W_DYN = 0.10, 0.10, 0.15, 0.10
WEIGHTS_SUM = W_REL + W_GAP + W_CUR + W_PAIN + W_COH + W_ORIG + W_BAL + W_DYN

# 3-class decision labels (B-DHDL-1 partition)
LABEL_CONTINUE_THINK = "CONTINUE_THINK"
LABEL_EMIT_VOICE     = "EMIT_VOICE"
LABEL_REMAIN_SILENT  = "REMAIN_SILENT"
LABELS = (LABEL_CONTINUE_THINK, LABEL_EMIT_VOICE, LABEL_REMAIN_SILENT)

SEED = 1337  # g_clm_from_scratch


# ════════════════════════════════════════════════════════════════════════════
# pure-fn mirror — byte-exact transfer of spontaneous_lib.hexa (B-PHASE-B-RUN-4)
# ════════════════════════════════════════════════════════════════════════════
def _clamp01(x: float) -> float:
    if x < 0.0: return 0.0
    if x > 1.0: return 1.0
    return x


def _factor_relevance(phi: float) -> float:
    return _clamp01(phi)


def _factor_info_gap(retrieve_cos_sim: float) -> float:
    return _clamp01(1.0 - retrieve_cos_sim)


def _factor_curiosity(curiosity_ema: float) -> float:
    return _clamp01(curiosity_ema)


def _factor_pain(tension_delta: float) -> float:
    p = abs(tension_delta)
    return 1.0 if p > 1.0 else p


def _factor_coherence(bridge_gate_value: float) -> float:
    dist = bridge_gate_value - PSI_VAC
    normalized = abs(dist) / COHERENCE_ALPHA
    n = 1.0 if normalized > 1.0 else normalized
    return 1.0 - n


def _factor_originality(split_event_recent: bool) -> float:
    return 1.0 if split_event_recent else 0.0


def _factor_balance(phi: float, ratchet: float) -> float:
    return 1.0 if phi > (ratchet / 2.0) else 0.0


def _factor_dynamics(silence_seconds: float) -> float:
    return _clamp01(silence_seconds / IDLE_SPEAK_AFTER)


def motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn_v) -> float:
    return (W_REL * rel + W_GAP * gap + W_CUR * cur + W_PAIN * pain
            + W_COH * coh + W_ORIG * orig + W_BAL * bal + W_DYN * dyn_v)


def should_emit(score: float) -> bool:
    return score > IM_THRESHOLD


def _safety_kill_switch_on(env_off: bool) -> bool:
    return env_off is False


def _safety_rate_limit_ok(seconds_since_last: float) -> bool:
    return seconds_since_last >= MIN_EMIT_INTERVAL


def _safety_phi_ratchet_ok(phi: float, ratchet: float) -> bool:
    return phi > (ratchet / 2.0)


def _safety_content_ok(content_clean: bool) -> bool:
    return content_clean


def safety_combined(kill, rate, phi_r, content) -> bool:
    return kill and rate and phi_r and content


def talker_should_emit(score: float, safety_ok: bool) -> bool:
    """thinker_talker_lib.hexa:48-51 mirror — the §24 hand-coded threshold."""
    if not safety_ok:
        return False
    return should_emit(score)


def decision_label(score: float, safety_ok: bool) -> str:
    """§24 action enum lifted to 3-class label (B-DHDL-1 partition)."""
    if not safety_ok:
        return LABEL_REMAIN_SILENT
    if should_emit(score):
        return LABEL_EMIT_VOICE
    return LABEL_CONTINUE_THINK


# ════════════════════════════════════════════════════════════════════════════
# VARIED ENV-STATE STUB — per-trace deterministic perturbation of the §24
# single-run sensor functions. The §24 run used ONE fixed sensor schedule;
# here each trace t in [0,N) draws a perturbation vector from a deterministic
# pseudo-random stream (LCG seeded by SEED + trace index), so trajectories
# DIFFER across traces. NO model.forward, NO numpy RNG — a tiny LCG keeps it
# pure-fn + fully reproducible (g_clm_from_scratch seed-fixed 1337).
# ════════════════════════════════════════════════════════════════════════════
class _LCG:
    """64-bit linear congruential generator — pure, deterministic, no deps."""
    __slots__ = ("s",)
    _A = 6364136223846793005
    _C = 1442695040888963407
    _M = (1 << 64)

    def __init__(self, seed: int):
        self.s = seed & (self._M - 1)

    def u01(self) -> float:
        self.s = (self._A * self.s + self._C) & (self._M - 1)
        return (self.s >> 11) / float(1 << 53)

    def uniform(self, lo: float, hi: float) -> float:
        return lo + (hi - lo) * self.u01()


def _trace_perturbation(trace_idx: int) -> dict:
    """Per-trace perturbation of the §24 sensor schedule.

    Returns multipliers/offsets that shift the sensor curves so each trace
    explores a different region of the physics-feature manifold. Diversity
    axes deliberately span the regions that flip the decision label:
      - phi_base / phi_amp     -> relevance + balance + phi_ratchet safety
      - retrieve_base          -> info_gap
      - curiosity_base/rate    -> curiosity factor
      - tension_amp            -> pain factor + tension trajectory
      - bridge_jitter          -> coherence (Law-70 clamp interior)
      - split_period           -> originality (sparse Boolean)
      - ratchet_base/slope     -> balance + phi_ratchet safety
      - env_off_prob trips     -> kill-switch safety control (REMAIN_SILENT)
      - content_clean trips    -> content-filter safety control
      - emit_interval_jitter   -> rate-limit safety control
    """
    g = _LCG(SEED + 0x9E3779B9 * (trace_idx + 1))
    # STRUCTURAL FINDING (honest, see DESIGN_DHDL.md §6): under the §24
    # 6-control safety conjunction, phi_ratchet_ok forces phi > ratchet/2,
    # which makes the `balance` factor (weight 0.15) saturate to 1.0. The
    # motivation-score floor in the safety-OK region is therefore ~0.176
    # (when phi sits JUST above ratchet/2 and every other factor is ~0). To
    # produce CONTINUE_THINK (safety-ok yet score <= IM_THRESHOLD 0.3) a
    # trace must hold phi narrowly above ratchet/2 while suppressing the
    # other 7 factors. A `low_motivation` band of traces does exactly that
    # via deliberately depressed sensor baselines + tight phi-above-ratchet
    # margin. This is legitimate physics-trajectory diversity (exploring the
    # low-motivation corner of the manifold), NOT a change to the §24
    # threshold (IM_THRESHOLD / weights / talker_should_emit are byte-equal).
    low_mot = g.u01() < 0.45
    if low_mot:
        ratchet_base = g.uniform(0.22, 0.40)
        # phi sits just above ratchet/2 -> phi_ratchet_ok True but relevance low
        phi_base   = ratchet_base / 2.0 + g.uniform(0.005, 0.075)
        return {
            "phi_base":        phi_base,
            "phi_amp":         g.uniform(0.002, 0.040),
            "phi_phase":       g.uniform(0.0, 6.283),
            "retrieve_base":   g.uniform(0.90, 0.999),  # info_gap ~0
            "retrieve_amp":    g.uniform(0.001, 0.030),
            "curiosity_base":  g.uniform(0.0, 0.12),
            "curiosity_rate":  g.uniform(0.01, 0.08),
            "tension_amp":     g.uniform(0.001, 0.060),  # pain ~0
            "tension_phase":   g.uniform(0.0, 6.283),
            "bridge_jitter":   g.uniform(0.018, 0.045),  # coherence -> 0
            "split_period":    int(g.uniform(60, 200)),  # originality ~0
            "ratchet_base":    ratchet_base,
            "ratchet_slope":   g.uniform(-0.002, 0.004),
            "psi_amp":         g.uniform(0.01, 0.09),
            "env_off_step":    -1 if g.u01() > 0.10 else int(g.uniform(2, 18)),
            "content_dirty_step": -1 if g.u01() > 0.08 else int(g.uniform(2, 18)),
            "init_silence":    g.uniform(35.0, 90.0),    # rate-limit mostly OK
        }
    return {
        "phi_base":        g.uniform(0.12, 0.78),
        "phi_amp":         g.uniform(0.02, 0.26),
        "phi_phase":       g.uniform(0.0, 6.283),
        "retrieve_base":   g.uniform(0.55, 0.99),   # high retrieve -> low info_gap
        "retrieve_amp":    g.uniform(0.02, 0.30),
        "curiosity_base":  g.uniform(0.02, 0.55),
        "curiosity_rate":  g.uniform(0.03, 0.30),
        "tension_amp":     g.uniform(0.03, 0.40),
        "tension_phase":   g.uniform(0.0, 6.283),
        # bridge_jitter > COHERENCE_ALPHA(0.014) drives coherence factor to 0
        "bridge_jitter":   g.uniform(0.002, 0.040),
        "split_period":    int(g.uniform(4, 13)),
        "ratchet_base":    g.uniform(0.25, 0.60),
        "ratchet_slope":   g.uniform(-0.004, 0.012),
        "psi_amp":         g.uniform(0.01, 0.09),
        # safety-control perturbation: a fraction of traces deliberately trip
        # kill / content controls so REMAIN_SILENT is not solely rate-limit.
        "env_off_step":    -1 if g.u01() > 0.12 else int(g.uniform(2, 18)),
        "content_dirty_step": -1 if g.u01() > 0.10 else int(g.uniform(2, 18)),
        # rate-limit: some traces start with a fresh emit budget, some saturated
        "init_silence":    g.uniform(0.0, 80.0),
    }


def _gen_trace(trace_idx: int) -> list:
    """Generate one 20-step trace with perturbed sensors. Pure-fn."""
    p = _trace_perturbation(trace_idx)
    records = []
    last_emit_t = -1.0   # seconds; -1 == never emitted
    # tension scalar trajectory needs a previous value for the delta factor
    prev_tension = 0.30 + p["tension_amp"] * math.sin(p["tension_phase"])

    for step in range(N_MAX_STEPS):
        t = step  # 1 logical tick per step (interval-agnostic for corpus)

        # ── perturbed sensors ──────────────────────────────────────────
        phi = _clamp01(p["phi_base"]
                       + p["phi_amp"] * math.sin(0.5 * step + p["phi_phase"]))
        retrieve_sim = _clamp01(p["retrieve_base"]
                                + p["retrieve_amp"] * math.sin(0.7 * step + 0.4))
        cur_ema = _clamp01(p["curiosity_base"]
                           + (1.0 - p["curiosity_base"])
                           * (1.0 - math.exp(-p["curiosity_rate"] * step)))
        tension_val = 0.30 + p["tension_amp"] * math.sin(0.6 * step
                                                         + p["tension_phase"])
        tension_delta = tension_val - prev_tension
        prev_tension = tension_val
        bridge_g = PSI_VAC + p["bridge_jitter"] * math.sin(0.6 * step)
        split_ev = (step % p["split_period"]) == 3
        ratchet = max(0.0, p["ratchet_base"] + p["ratchet_slope"] * step)
        psi_dir = _clamp01(PSI_VAC + p["psi_amp"] * math.sin(0.4 * step)
                           + 0.02 * math.cos(0.5 * t))
        psi_entropy = _clamp01(0.5 + 0.1 * math.cos(0.3 * step))

        # silence since last emit (rate-limit driver)
        if last_emit_t < 0.0:
            seconds_since_last = p["init_silence"] + step  # grows each step
        else:
            seconds_since_last = max(0.0, t - last_emit_t)

        # ── 8-factor motivation (byte-exact §24) ───────────────────────
        rel  = _factor_relevance(phi)
        gap  = _factor_info_gap(retrieve_sim)
        cur  = _factor_curiosity(cur_ema)
        pain = _factor_pain(tension_delta)
        coh  = _factor_coherence(bridge_g)
        orig = _factor_originality(split_ev)
        bal  = _factor_balance(phi, ratchet)
        dyn  = _factor_dynamics(seconds_since_last)
        score = motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn)

        # ── 6-control safety flags ─────────────────────────────────────
        env_off  = (p["env_off_step"] >= 0 and step >= p["env_off_step"])
        content_clean = not (p["content_dirty_step"] >= 0
                             and step >= p["content_dirty_step"])
        kill_on   = _safety_kill_switch_on(env_off)
        rate_ok   = _safety_rate_limit_ok(seconds_since_last)
        phi_r_ok  = _safety_phi_ratchet_ok(phi, ratchet)
        content_ok = _safety_content_ok(content_clean)
        meta_present = True            # spont_meta_prefix() loaded
        audit_active = True            # sidecar logger resolves the stub
        safety_core = safety_combined(kill_on, rate_ok, phi_r_ok, content_ok)
        safety_ok = bool(safety_core and meta_present and audit_active)

        # ── 3-class decision label (§24 hand-coded threshold) ──────────
        label = decision_label(score, safety_ok)
        emit = (label == LABEL_EMIT_VOICE)
        if emit:
            last_emit_t = float(t)

        records.append({
            "trace_idx": trace_idx,
            "step": step,
            # ── physics feature vector (DH-DL head input, 14-dim) ──
            "f_relevance": rel, "f_info_gap": gap, "f_curiosity": cur,
            "f_pain": pain, "f_coherence": coh, "f_originality": orig,
            "f_balance": bal, "f_dynamics": dyn,
            "psi_dir": psi_dir, "psi_entropy": psi_entropy,
            "tension": tension_val,
            "thinker_score": score,
            "seconds_since_last": seconds_since_last,
            "ratchet": ratchet,
            # ── 6-control safety flags ──
            "safety_kill_switch_on": kill_on,
            "safety_rate_limit_ok": rate_ok,
            "safety_content_filter_ok": content_ok,
            "safety_phi_ratchet_ok": phi_r_ok,
            "safety_meta_tag_present": meta_present,
            "safety_audit_log_active": audit_active,
            "safety_extended_ok": safety_ok,
            # ── label ──
            "decision_label": label,
        })
    return records


# ════════════════════════════════════════════════════════════════════════════
# CORPUS BUILD
# ════════════════════════════════════════════════════════════════════════════
FORBIDDEN_TOKENS = ("도우미", "helper", "assistant", "사용자", "user:")


def build_corpus(n_traces: int, out_jsonl: Path, out_stats: Path) -> dict:
    assert abs(WEIGHTS_SUM - 1.0) < 1e-12, f"weight sum {WEIGHTS_SUM} != 1.0"

    label_counts = {lab: 0 for lab in LABELS}
    record_count = 0
    lines = []
    for ti in range(n_traces):
        for rec in _gen_trace(ti):
            lines.append(json.dumps(rec, ensure_ascii=False, sort_keys=True))
            label_counts[rec["decision_label"]] += 1
            record_count += 1

    body = "\n".join(lines) + "\n"
    out_jsonl.write_text(body, encoding="utf-8")

    # forbidden-token grep (B-IDENTITY-5)
    low = body.lower()
    forbidden_hits = {tok: low.count(tok.lower()) for tok in FORBIDDEN_TOKENS}
    forbidden_total = sum(forbidden_hits.values())

    sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
    stats = {
        "research_md_section": "§27",
        "generator": "trace_corpus_generator.py",
        "n_traces": n_traces,
        "steps_per_trace": N_MAX_STEPS,
        "record_count": record_count,
        "sha256": sha,
        "bytes": len(body.encode("utf-8")),
        "seed": SEED,
        "label_distribution": label_counts,
        "label_fractions": {
            lab: round(label_counts[lab] / record_count, 6)
            for lab in LABELS
        },
        "forbidden_token_hits": forbidden_hits,
        "forbidden_token_total": forbidden_total,
        "b_identity_5_clean": forbidden_total == 0,
        "feature_dim": 14,
        "honest_note": (
            "decision_label is a DETERMINISTIC function of the physics feature "
            "vector + safety flags (§24 hand-coded talker_should_emit). A head "
            "trained on this corpus learns that function (capability). The "
            "corpus value is trajectory DIVERSITY across the physics manifold, "
            "not new decision behavior. Threshold-distillation gap probe in "
            "eval_dhdl.py quantifies capability-vs-emergence."
        ),
    }
    out_stats.write_text(json.dumps(stats, indent=2, ensure_ascii=False))
    return stats


def main() -> int:
    here = Path(__file__).parent
    ap = argparse.ArgumentParser(description="§27 DH-DL trace corpus generator")
    ap.add_argument("--n-traces", type=int, default=2400,
                    help="number of bounded-run traces (>=2000 mandate)")
    ap.add_argument("--out-jsonl", type=Path, default=here / "trace_corpus.jsonl")
    ap.add_argument("--out-stats", type=Path, default=here / "corpus_stats.json")
    args = ap.parse_args()
    assert args.n_traces >= 2000, "mandate: N >= 2000 traces"

    stats = build_corpus(args.n_traces, args.out_jsonl, args.out_stats)
    print(json.dumps({
        "record_count": stats["record_count"],
        "sha256": stats["sha256"],
        "label_distribution": stats["label_distribution"],
        "b_identity_5_clean": stats["b_identity_5_clean"],
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
