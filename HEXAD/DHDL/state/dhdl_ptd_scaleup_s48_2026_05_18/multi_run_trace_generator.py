#!/usr/bin/env python3
"""multi_run_trace_generator.py — RESEARCH.md §48 scale-up trace corpus.

§44 (DH-DL + PTD-aux composition fire) used §27's single trace_corpus.jsonl
(2,400 traces × 20 steps = 48,000 records, LCG-perturbed within one regime).
§44 measured PTD-aux signal (gap 0.00063 → 0.00031, PTD MSE 15× drop,
CONTINUE_THINK 7.3× harder), verdict PTD-AUX-SIGNAL-MEASURABLE on small corpus.

§48 asks: does the signal HOLD at 4× the corpus (multi-§24-run scale-up with
varied env_state stubs), or NOISE OUT as small-corpus artifact?

DESIGN (this generator):
  - n_traces=9,600 (4× §27)  →  192,000 records (4× §27)
  - per-trace perturbation BOTH:
      (a) §27-style LCG-driven sensor perturbations (carry; B-S48-4 reduction)
      (b) NEW phase-regime layer: each trace also belongs to one of K=4 phase
          regimes that shift the sensor SCHEDULE (frequencies + offsets), so
          traces explore more diverse trajectories than §27's single-regime
          family. This is the "multi-§24-run" axis (each §24 run had ONE
          schedule; here we vary the schedule itself, deterministically).

  HONEST framing (g3): the 3-class decision label is STILL the deterministic
  §24 hand-coded talker_should_emit function. The corpus diversity widens the
  physics-feature manifold the head sees; it does NOT add new decision
  behavior. The PTD aux head predicts the next 14-d physics vector — if its
  signal HOLDS at scale that confirms §44's representation-shaping is real;
  if it NOISES OUT that confirms small-corpus artifact.

  PTD pairing (t, t+1) is still intra-trace (last step of each trace masked).

§7 GOAL-legitimacy:
  §7① not generic-LM pretrain   ✅ (no model.forward this cycle)
  §7② not generic-then-graft    ✅ (no external classifier / LLM / RAG)
  §7③ anima-physics-as-source   ✅ (8-factor + 6-control + sensor schedules
                                    all byte-equal to spontaneous_lib.hexa /
                                    thinker_talker_lib.hexa SSOT)

  forbidden-token grep (B-IDENTITY-5) = 0 by construction (no text payload).

f_hardcoded_credential safe — no credentials in this script. $0 Mac CPU.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

# ════════════════════════════════════════════════════════════════════════════
# §24 byte-exact constants (spontaneous_lib.hexa / thinker_talker_lib.hexa SSOT)
# ════════════════════════════════════════════════════════════════════════════
N_MAX_STEPS         = 20
IM_THRESHOLD        = 0.3
IDLE_SPEAK_AFTER    = 30.0
MIN_EMIT_INTERVAL   = 30.0
COHERENCE_ALPHA     = 0.014
PSI_VAC             = 0.5
W_REL, W_GAP, W_CUR, W_PAIN = 0.20, 0.10, 0.15, 0.10
W_COH, W_ORIG, W_BAL, W_DYN = 0.10, 0.10, 0.15, 0.10
WEIGHTS_SUM = W_REL + W_GAP + W_CUR + W_PAIN + W_COH + W_ORIG + W_BAL + W_DYN

LABEL_CONTINUE_THINK = "CONTINUE_THINK"
LABEL_EMIT_VOICE     = "EMIT_VOICE"
LABEL_REMAIN_SILENT  = "REMAIN_SILENT"
LABELS = (LABEL_CONTINUE_THINK, LABEL_EMIT_VOICE, LABEL_REMAIN_SILENT)

SEED = 1337  # g_clm_from_scratch byte-equal to §27 / §44

# ════════════════════════════════════════════════════════════════════════════
# pure-fn 8-factor + safety — byte-equal §27 / §44 SSOT
# ════════════════════════════════════════════════════════════════════════════
def _clamp01(x: float) -> float:
    if x < 0.0: return 0.0
    if x > 1.0: return 1.0
    return x


def _f_rel(phi):           return _clamp01(phi)
def _f_gap(retrieve_sim):  return _clamp01(1.0 - retrieve_sim)
def _f_cur(cur_ema):       return _clamp01(cur_ema)
def _f_pain(tens_delta):
    p = abs(tens_delta)
    return 1.0 if p > 1.0 else p
def _f_coh(bridge_g):
    dist = bridge_g - PSI_VAC
    n_ = abs(dist) / COHERENCE_ALPHA
    n_ = 1.0 if n_ > 1.0 else n_
    return 1.0 - n_
def _f_orig(split_ev):     return 1.0 if split_ev else 0.0
def _f_bal(phi, ratchet):  return 1.0 if phi > (ratchet / 2.0) else 0.0
def _f_dyn(sil_s):         return _clamp01(sil_s / IDLE_SPEAK_AFTER)


def motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn_v):
    return (W_REL * rel + W_GAP * gap + W_CUR * cur + W_PAIN * pain
            + W_COH * coh + W_ORIG * orig + W_BAL * bal + W_DYN * dyn_v)


def _safety_kill(env_off):     return env_off is False
def _safety_rate(sec_since):   return sec_since >= MIN_EMIT_INTERVAL
def _safety_phi_r(phi, r):     return phi > (r / 2.0)
def _safety_content(clean):    return clean


def safety_combined(kill, rate, phi_r, content):
    return kill and rate and phi_r and content


def decision_label(score, safety_ok):
    if not safety_ok:
        return LABEL_REMAIN_SILENT
    if score > IM_THRESHOLD:
        return LABEL_EMIT_VOICE
    return LABEL_CONTINUE_THINK


# ════════════════════════════════════════════════════════════════════════════
# LCG — byte-equal §27 (B-S48-4 reduction)
# ════════════════════════════════════════════════════════════════════════════
class _LCG:
    __slots__ = ("s",)
    _A = 6364136223846793005
    _C = 1442695040888963407
    _M = (1 << 64)

    def __init__(self, seed):
        self.s = seed & (self._M - 1)

    def u01(self):
        self.s = (self._A * self.s + self._C) & (self._M - 1)
        return (self.s >> 11) / float(1 << 53)

    def uniform(self, lo, hi):
        return lo + (hi - lo) * self.u01()


# ════════════════════════════════════════════════════════════════════════════
# §48 NEW: multi-§24-run schedule regimes (4 phase regimes — multi-run axis)
# ════════════════════════════════════════════════════════════════════════════
# Each regime k ∈ {0,1,2,3} defines a sensor SCHEDULE — frequencies + offsets
# that produce DIFFERENT trajectories than §27's single regime. This is the
# "multi-§24-run" axis: each §24 run had ONE fixed schedule (sin frequencies
# 0.5/0.7/0.6/0.4/0.3 etc.). Here a trace's regime determines the schedule.
# All schedules remain non-pathological (sensors stay bounded; thresholds
# unchanged; §24 SSOT semantics preserved).
PHASE_REGIMES = [
    # regime 0: §24 baseline (matches run_bounded.py default schedule)
    {"f_phi": 0.5, "f_ret": 0.7, "f_tens": 0.6, "f_bridge": 0.6,
     "f_psi_dir": 0.4, "f_psi_ent": 0.3, "off_phi": 0.0, "off_psi": 0.0},
    # regime 1: faster phi + slower retrieve (different motivation cadence)
    {"f_phi": 0.9, "f_ret": 0.3, "f_tens": 0.4, "f_bridge": 0.8,
     "f_psi_dir": 0.7, "f_psi_ent": 0.5, "off_phi": 1.0, "off_psi": 0.3},
    # regime 2: slow drift (low-frequency physics)
    {"f_phi": 0.2, "f_ret": 0.4, "f_tens": 0.25, "f_bridge": 0.3,
     "f_psi_dir": 0.15, "f_psi_ent": 0.1, "off_phi": 2.0, "off_psi": 1.0},
    # regime 3: high-frequency jitter (rapid physics fluctuations)
    {"f_phi": 1.3, "f_ret": 1.1, "f_tens": 1.5, "f_bridge": 1.4,
     "f_psi_dir": 1.2, "f_psi_ent": 0.9, "off_phi": 4.0, "off_psi": 2.0},
]
N_PHASE_REGIMES = len(PHASE_REGIMES)


def _trace_perturbation(trace_idx: int) -> dict:
    """§27-style amplitude/baseline perturbation. Byte-equal to §27 LCG seeding
    so traces 0..2399 of §48 reproduce §27 byte-equal at regime k=0 (B-S48-4).
    """
    g = _LCG(SEED + 0x9E3779B9 * (trace_idx + 1))
    low_mot = g.u01() < 0.45
    if low_mot:
        ratchet_base = g.uniform(0.22, 0.40)
        phi_base = ratchet_base / 2.0 + g.uniform(0.005, 0.075)
        return {
            "phi_base": phi_base,
            "phi_amp": g.uniform(0.002, 0.040),
            "phi_phase": g.uniform(0.0, 6.283),
            "retrieve_base": g.uniform(0.90, 0.999),
            "retrieve_amp": g.uniform(0.001, 0.030),
            "curiosity_base": g.uniform(0.0, 0.12),
            "curiosity_rate": g.uniform(0.01, 0.08),
            "tension_amp": g.uniform(0.001, 0.060),
            "tension_phase": g.uniform(0.0, 6.283),
            "bridge_jitter": g.uniform(0.018, 0.045),
            "split_period": int(g.uniform(60, 200)),
            "ratchet_base": ratchet_base,
            "ratchet_slope": g.uniform(-0.002, 0.004),
            "psi_amp": g.uniform(0.01, 0.09),
            "env_off_step": -1 if g.u01() > 0.10 else int(g.uniform(2, 18)),
            "content_dirty_step": -1 if g.u01() > 0.08 else int(g.uniform(2, 18)),
            "init_silence": g.uniform(35.0, 90.0),
        }
    return {
        "phi_base": g.uniform(0.12, 0.78),
        "phi_amp": g.uniform(0.02, 0.26),
        "phi_phase": g.uniform(0.0, 6.283),
        "retrieve_base": g.uniform(0.55, 0.99),
        "retrieve_amp": g.uniform(0.02, 0.30),
        "curiosity_base": g.uniform(0.02, 0.55),
        "curiosity_rate": g.uniform(0.03, 0.30),
        "tension_amp": g.uniform(0.03, 0.40),
        "tension_phase": g.uniform(0.0, 6.283),
        "bridge_jitter": g.uniform(0.002, 0.040),
        "split_period": int(g.uniform(4, 13)),
        "ratchet_base": g.uniform(0.25, 0.60),
        "ratchet_slope": g.uniform(-0.004, 0.012),
        "psi_amp": g.uniform(0.01, 0.09),
        "env_off_step": -1 if g.u01() > 0.12 else int(g.uniform(2, 18)),
        "content_dirty_step": -1 if g.u01() > 0.10 else int(g.uniform(2, 18)),
        "init_silence": g.uniform(0.0, 80.0),
    }


def _gen_trace(trace_idx: int, regime_idx: int) -> list:
    """Generate one 20-step trace with §27 perturbation + §48 phase regime."""
    p = _trace_perturbation(trace_idx)
    reg = PHASE_REGIMES[regime_idx]
    records = []
    last_emit_t = -1.0
    prev_tension = 0.30 + p["tension_amp"] * math.sin(p["tension_phase"])

    for step in range(N_MAX_STEPS):
        t = step

        # ── sensors (regime-dependent frequencies + offsets) ──────────
        phi = _clamp01(
            p["phi_base"]
            + p["phi_amp"] * math.sin(reg["f_phi"] * step + p["phi_phase"]
                                      + reg["off_phi"])
        )
        retrieve_sim = _clamp01(
            p["retrieve_base"]
            + p["retrieve_amp"] * math.sin(reg["f_ret"] * step + 0.4)
        )
        cur_ema = _clamp01(
            p["curiosity_base"]
            + (1.0 - p["curiosity_base"])
              * (1.0 - math.exp(-p["curiosity_rate"] * step))
        )
        tension_val = 0.30 + p["tension_amp"] * math.sin(
            reg["f_tens"] * step + p["tension_phase"]
        )
        tension_delta = tension_val - prev_tension
        prev_tension = tension_val
        bridge_g = PSI_VAC + p["bridge_jitter"] * math.sin(reg["f_bridge"] * step)
        split_ev = (step % p["split_period"]) == 3
        ratchet = max(0.0, p["ratchet_base"] + p["ratchet_slope"] * step)
        psi_dir = _clamp01(
            PSI_VAC + p["psi_amp"] * math.sin(reg["f_psi_dir"] * step
                                              + reg["off_psi"])
            + 0.02 * math.cos(0.5 * t)
        )
        psi_entropy = _clamp01(0.5 + 0.1 * math.cos(reg["f_psi_ent"] * step))

        if last_emit_t < 0.0:
            seconds_since_last = p["init_silence"] + step
        else:
            seconds_since_last = max(0.0, t - last_emit_t)

        # ── 8-factor motivation (byte-equal §24 SSOT) ─────────────────
        rel = _f_rel(phi)
        gap = _f_gap(retrieve_sim)
        cur = _f_cur(cur_ema)
        pain = _f_pain(tension_delta)
        coh = _f_coh(bridge_g)
        orig = _f_orig(split_ev)
        bal = _f_bal(phi, ratchet)
        dyn = _f_dyn(seconds_since_last)
        score = motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn)

        # ── 6-control safety ─────────────────────────────────────────
        env_off = (p["env_off_step"] >= 0 and step >= p["env_off_step"])
        content_clean = not (p["content_dirty_step"] >= 0
                             and step >= p["content_dirty_step"])
        kill_on = _safety_kill(env_off)
        rate_ok = _safety_rate(seconds_since_last)
        phi_r_ok = _safety_phi_r(phi, ratchet)
        content_ok = _safety_content(content_clean)
        meta_present = True
        audit_active = True
        safety_core = safety_combined(kill_on, rate_ok, phi_r_ok, content_ok)
        safety_ok = bool(safety_core and meta_present and audit_active)

        label = decision_label(score, safety_ok)
        emit = (label == LABEL_EMIT_VOICE)
        if emit:
            last_emit_t = float(t)

        records.append({
            "trace_idx": trace_idx,
            "phase_regime": regime_idx,
            "step": step,
            "f_relevance": rel, "f_info_gap": gap, "f_curiosity": cur,
            "f_pain": pain, "f_coherence": coh, "f_originality": orig,
            "f_balance": bal, "f_dynamics": dyn,
            "psi_dir": psi_dir, "psi_entropy": psi_entropy,
            "tension": tension_val,
            "thinker_score": score,
            "seconds_since_last": seconds_since_last,
            "ratchet": ratchet,
            "safety_kill_switch_on": kill_on,
            "safety_rate_limit_ok": rate_ok,
            "safety_content_filter_ok": content_ok,
            "safety_phi_ratchet_ok": phi_r_ok,
            "safety_meta_tag_present": meta_present,
            "safety_audit_log_active": audit_active,
            "safety_extended_ok": safety_ok,
            "decision_label": label,
        })
    return records


FORBIDDEN_TOKENS = ("도우미", "helper", "assistant", "사용자", "user:")


def build_corpus(n_traces: int, out_jsonl: Path, out_stats: Path) -> dict:
    assert abs(WEIGHTS_SUM - 1.0) < 1e-12, f"weight sum {WEIGHTS_SUM} != 1.0"
    assert n_traces >= 8000, "§48 mandate: scale-up requires N >= 8000 (§27 was 2400)"

    label_counts = {lab: 0 for lab in LABELS}
    record_count = 0
    regime_counts = [0] * N_PHASE_REGIMES
    lines = []
    for ti in range(n_traces):
        # Deterministic regime assignment: round-robin so each regime gets
        # ~equal coverage. This makes "multi-§24-run" SCALE additive across
        # phase regimes (not just LCG re-sampling within one regime).
        regime_idx = ti % N_PHASE_REGIMES
        regime_counts[regime_idx] += 1
        for rec in _gen_trace(ti, regime_idx):
            lines.append(json.dumps(rec, ensure_ascii=False, sort_keys=True))
            label_counts[rec["decision_label"]] += 1
            record_count += 1

    body = "\n".join(lines) + "\n"
    out_jsonl.write_text(body, encoding="utf-8")

    low = body.lower()
    forbidden_hits = {tok: low.count(tok.lower()) for tok in FORBIDDEN_TOKENS}
    forbidden_total = sum(forbidden_hits.values())

    sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
    stats = {
        "research_md_section": "§48",
        "generator": "multi_run_trace_generator.py",
        "n_traces": n_traces,
        "n_phase_regimes": N_PHASE_REGIMES,
        "regime_trace_counts": regime_counts,
        "steps_per_trace": N_MAX_STEPS,
        "record_count": record_count,
        "sha256": sha,
        "bytes": len(body.encode("utf-8")),
        "seed": SEED,
        "label_distribution": label_counts,
        "label_fractions": {
            lab: round(label_counts[lab] / record_count, 6) for lab in LABELS
        },
        "forbidden_token_hits": forbidden_hits,
        "forbidden_token_total": forbidden_total,
        "b_identity_5_clean": forbidden_total == 0,
        "feature_dim": 14,
        "scale_vs_s27": round(record_count / 48000.0, 4),
        "honest_note": (
            "§48 scale-up corpus = §27 LCG amplitude/baseline perturbation × "
            "K=4 phase regimes (sensor schedule axis). decision_label is the "
            "DETERMINISTIC §24 hand-coded talker_should_emit (byte-equal). The "
            "corpus tests whether §44's PTD-aux signal HOLDS at 4× scale + "
            "broader phase regime coverage, or NOISES OUT as small-corpus "
            "artifact. NO model.forward, NO autograd, NO GPU. $0 Mac CPU. "
            "B-IDENTITY-5 clean by construction (no text payload)."
        ),
    }
    out_stats.write_text(json.dumps(stats, indent=2, ensure_ascii=False))
    return stats


def main() -> int:
    here = Path(__file__).parent
    ap = argparse.ArgumentParser(description="§48 multi-§24-run scale-up corpus")
    ap.add_argument("--n-traces", type=int, default=9600,
                    help="trace count (>=8000 mandate; 4× §27's 2400)")
    ap.add_argument("--out-jsonl", type=Path,
                    default=here / "trace_corpus_s48.jsonl")
    ap.add_argument("--out-stats", type=Path,
                    default=here / "corpus_stats_s48.json")
    args = ap.parse_args()

    stats = build_corpus(args.n_traces, args.out_jsonl, args.out_stats)
    print(json.dumps({
        "record_count": stats["record_count"],
        "sha256": stats["sha256"],
        "label_distribution": stats["label_distribution"],
        "regime_trace_counts": stats["regime_trace_counts"],
        "scale_vs_s27": stats["scale_vs_s27"],
        "b_identity_5_clean": stats["b_identity_5_clean"],
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
