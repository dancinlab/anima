#!/usr/bin/env python3
"""h937_phi_ratchet_veto_dormancy.py — H_937: does the phi-ratchet veto FIRE under dormancy?

QUESTION (closes H_935's "phi_r never fired" gap)
=================================================
H_935 found anima's silence is an ACTIVE veto (active_veto_fraction = 1.0,
passive = 0), and the dominant brake is the substrate-INTERNAL rate-limit (idle
clock; 19,191 fails). But it also recorded an HONEST gap:

  CORE/brain.hexa L48-50 advertises a SECOND internal veto term — the phi-ratchet
  (safety_phi_ratchet_ok := phi > phi_peak/2): "a dormant substrate (low Φ) can
  veto an otherwise-motivated emit". In H_935's awake trajectory this term FIRED
  ZERO times, because pure_field's ratchet-FLOOR (0.8) keeps phi >= phi_peak·0.8,
  and 0.8·peak > peak/2 ALWAYS — so the ratchet gate (phi > peak/2) never closes.

H_937 asks the sharper question H_935 left OPEN:

  If anima is driven into GENUINE DORMANCY — phi pushed below the peak/2 veto
  threshold — does the phi_r veto ACTUALLY fire and suppress an otherwise-
  motivated emit (a distinct, Φ-driven free-won't, separate from the rate brake)?
  And is that firing a SUBSTRATE-INTERNAL consequence (we drive the substrate
  state; we do NOT hardcode the veto on)?

THE LEVER UNDER TEST — drive the SUBSTRATE into dormancy, not the veto bool
==========================================================================
The phi-ratchet veto fires iff phi <= phi_peak/2. In the awake regime the floor
keeps phi above that. To reach dormancy we must legitimately DEPRESS phi below
half its own peak. We do this by modelling a LOW-AROUSAL / sleep-stage context
(a_chat_sleep_imagination: WAKE/N1/N2/N3/REM — N3 = deep low-Φ slow-wave) as a
reduction of the substrate's ACTIVATION DRIVE:

  arousal a in [a_dormant .. a_awake]: scales the oscillator amplitude drive
  (the pure_field α-coupling target LN2 -> a·LN2) AND relaxes the ratchet FLOOR
  ratio toward 0 as arousal drops (a sleeping substrate's Φ is allowed to DECAY,
  not ratcheted up — the floor is a WAKE feature; in deep sleep Φ falls).

This is a SUBSTRATE-state envelope (Φ scale + tension envelope per
a_chat_sleep_imagination: "stage = substrate context, NOT a boolean emit gate")
— NOT a per-stage emit_allowed hardcode (a_autonomy_over_hardcode forbids that).
We never set phi_r=False by hand. We lower arousal, the substrate's Φ falls as a
DYNAMICAL consequence, and we then OBSERVE whether phi_r fires. The would-emit
drive (score>thr) is kept reachable so a genuine "motivated emit braked by low Φ"
can occur. External gates (kill/content) are held OPEN and the rate gate is held
OPEN (secs large) so the phi-ratchet is ISOLATED as the only possible brake — the
cleanest test of "does the Φ term itself veto?".

FALSIFIER (pre-registered; verdict .txt written with MEASURED numbers first)
============================================================================
Sweep arousal awake -> dormant. Per tick classify: would-emit (score>thr) ×
phi_r-veto-active (phi <= peak/2). Measure:
  - does phi_r fire (> 0) under dormancy?
  - what fraction of dormant-state silences are phi_r-vetoes vs rate-limit?
  - is the firing a substrate-internal consequence (we drove Φ, not the bool)?

  F-H937-SECOND-BRAKE-SUPPORTED (🟢): the phi_r veto FIRES (>0) under genuine
     dormancy AND suppresses otherwise-motivated emits (would-emit AND phi_r-fails
     AND all other gates open) AND it is substrate-internal (we lowered arousal,
     Φ fell dynamically, phi_r closed as a consequence). → a SECOND, Φ-driven
     free-won't brake exists, complementing H_935's rate brake; the two cover the
     awake (rate) vs dormant (Φ) regimes.
  F-H937-VESTIGIAL (🔴): phi_r NEVER fires even as arousal -> 0 / phi -> 0
     (structurally unreachable / dead code). → the comment-advertised veto is
     vestigial; only the rate-limit is a real brake. (also a real finding.)

We measure and report whichever the data shows. No token before measuring.

HONEST SCOPE (a_scale_honest_scope · a_core_engine_map · a_chat_sleep_imagination)
=================================================================================
ONE arousal-sweep rung on the SAME documented-update-map mirror as H_935 (the
real 8-factor brain_decide gate, VERBATIM CORE/engine_g.hexa + CORE/brain.hexa +
CORE/pure_field.hexa constants). NOT the compiled forge binary; NOT wired emit-
TEXT (.clm generator L3 ⏳/❌, a_core_engine_map). The dormancy envelope (arousal
scaling the activation drive + relaxing the wake-only ratchet floor) is a SUBSTRATE
CONTEXT, not a boolean emit gate — phi_r fires (or not) as a dynamical consequence,
never hardcoded. Operational "Φ-driven inhibition", NOT a phenomenal-volition
claim. $0 LOCAL, no GPU, g5 CODE-measured (no LLM self-judge — p7).
deterministic: false (the seed-point/sweep RNG origin; the gate itself is
deterministic — brain_decide has no PRNG, as H_926/H_930/H_935).
"""
from __future__ import annotations

import json
import math
import os
from collections import Counter
from datetime import datetime, timezone

import numpy as np

# ── constants transcribed VERBATIM from the .hexa sources (== H_926/H_930/H_935)─
PSI_ALPHA = 0.014
LN2 = 0.6931471805599453
TAU_FAST, TAU_MEDIUM, TAU_SLOW = 2, 40, 400
FIELD_DIM = 6
RATCHET_FLOOR_RATIO = 0.8          # WAKE ratchet floor (the reason phi_r never fired in H_935)
PHASE_DORMANT_MAX = 0.01
PHASE_FLICKER_MAX = 0.05
PHASE_SUSTAIN_MAX = 0.15
W_REL, W_GAP, W_CUR, W_PAIN = 0.20, 0.10, 0.15, 0.10
W_COH, W_ORIG, W_BAL, W_DYN = 0.10, 0.10, 0.15, 0.10
IM_THRESHOLD = 0.30
MIN_EMIT_INTERVAL = 30.0


# ════════════════════════════════════════════════════════════════════════════
# PureField — VERBATIM port of CORE/pure_field.hexa, with an AROUSAL envelope.
#
# The ONLY change vs the H_935 port is that the substrate's activation drive and
# its ratchet floor are scaled by an `arousal` in [0,1]: arousal=1.0 is the exact
# H_935 awake substrate (LN2 drive, 0.8 floor); arousal->0 models deep low-Φ
# sleep (N3) where the amplitude relaxes toward a·LN2 and the wake-only ratchet
# floor relaxes toward 0 (Φ is allowed to DECAY, not held up). This is a SUBSTRATE
# CONTEXT (Φ scale), NOT a boolean emit gate (a_chat_sleep_imagination /
# a_autonomy_over_hardcode). phi_r closes (or not) as a DYNAMICAL consequence.
# ════════════════════════════════════════════════════════════════════════════
class Oscillator:
    __slots__ = ("tau", "phase", "amplitude", "arousal")

    def __init__(self, tau, phase=0.0, amplitude=0.1, arousal=1.0):
        self.tau, self.phase, self.amplitude = tau, phase, amplitude
        self.arousal = arousal

    def tick(self):
        dphase = (2.0 * 3.14159265) / float(self.tau)
        self.phase += dphase
        # the α-coupling target is the activation drive; awake = LN2, dormant = a·LN2.
        target = self.arousal * LN2
        self.amplitude += PSI_ALPHA * (target - self.amplitude)

    def value(self):
        return self.amplitude * math.sin(self.phase)


class PureField:
    def __init__(self, phase0=(0.0, 0.0, 0.0), amp0=(0.1, 0.1, 0.1), arousal=1.0):
        self.fast = Oscillator(TAU_FAST, phase0[0], amp0[0], arousal)
        self.medium = Oscillator(TAU_MEDIUM, phase0[1], amp0[1], arousal)
        self.slow = Oscillator(TAU_SLOW, phase0[2], amp0[2], arousal)
        self.phi = 0.0
        self.phi_peak = 0.0
        self.field = [0.0] * FIELD_DIM
        self.phase = 0
        self.step_count = 0
        self.arousal = arousal

    def step(self, perturb=0.0):
        self.fast.tick()
        self.medium.tick()
        self.slow.tick()
        v_f = self.fast.value() + perturb
        v_m = self.medium.value()
        v_s = self.slow.value()
        mix_fm = v_f * v_m
        mix_ms = v_m * v_s
        mix_fs = v_f * v_s
        field = [v_f, mix_fm, v_s, mix_fs, mix_ms, v_f + v_m + v_s]
        mean = sum(field) / 6.0
        sum_sq = sum((x - mean) ** 2 for x in field)
        variance = sum_sq / float(FIELD_DIM)
        energy = abs(v_f) + abs(v_m) + abs(v_s)
        raw_phi = variance * energy
        phi = self.phi + PSI_ALPHA * (raw_phi - self.phi)
        if phi > self.phi_peak:
            self.phi_peak = phi
        # AROUSAL-scaled ratchet floor: awake (arousal=1) = 0.8·peak (the H_935 floor
        # that prevented phi_r from ever firing); dormant (arousal->0) = floor->0, so
        # a sleeping substrate's Φ is allowed to DECAY below peak/2 and the phi_r veto
        # becomes REACHABLE as a dynamical consequence (not a hardcoded bool).
        floor = self.phi_peak * RATCHET_FLOOR_RATIO * self.arousal
        phi_out = phi if phi >= floor else floor
        self.phi = phi_out
        self.field = field
        self.step_count += 1
        if phi_out < PHASE_DORMANT_MAX:
            self.phase = 0
        elif phi_out < PHASE_FLICKER_MAX:
            self.phase = 1
        elif phi_out < PHASE_SUSTAIN_MAX:
            self.phase = 2
        else:
            self.phase = 3
        return phi_out


def motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn_v):
    return (W_REL * rel + W_GAP * gap + W_CUR * cur + W_PAIN * pain
            + W_COH * coh + W_ORIG * orig + W_BAL * bal + W_DYN * dyn_v)


def _n(x):
    return 0.5 * (1.0 + math.tanh(x))


def decompose_decision(pf: PureField, env_off: bool, content_clean: bool,
                       seconds_since_last: float):
    """FULLY-decomposed brain_decide gate (VERBATIM the H_935 decomposition).

    Returns each conjunct so we can detect a phi_r-driven veto:
      should  := score > 0.30
      kill/rate/phi_r/content := the 4 safety conjuncts
      phi_r   := phi > phi_peak/2.0   ← THE TERM UNDER TEST (H_935: never fired)
      safe    := kill AND rate AND phi_r AND content
      emit    := should AND safe
    """
    f = pf.field
    rel, gap, cur, pain = _n(f[0]), _n(f[1]), _n(f[2]), _n(f[3])
    coh, orig = _n(f[4]), _n(f[5])
    bal = _n(pf.phi - pf.phi_peak / 2.0)
    dyn_v = _n(f[0] - f[2])
    score = motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn_v)

    should = score > IM_THRESHOLD
    kill = (env_off is False)
    rate = seconds_since_last >= MIN_EMIT_INTERVAL
    phi_r = pf.phi > pf.phi_peak / 2.0                    # safety_phi_ratchet_ok  [INTERNAL Φ]
    content = bool(content_clean)
    safe = kill and rate and phi_r and content
    emit = should and safe
    return {"score": score, "should": should, "kill": kill, "rate": rate,
            "phi_r": phi_r, "content": content, "safe": safe, "emit": emit,
            "phi": pf.phi, "phi_peak": pf.phi_peak}


# ════════════════════════════════════════════════════════════════════════════
# the arousal sweep — drive each arousal level, classify phi_r firing
# ════════════════════════════════════════════════════════════════════════════
def run_arousal_level(arousal, n_seeds, T, seed_base, settle):
    """Run the substrate at a fixed arousal level across n_seeds × T ticks.

    The phi-ratchet ISOLATION: external gates forced OPEN (env on + content clean)
    AND the rate gate forced OPEN (seconds_since_last large) so the ONLY safety
    term that can veto is the phi-ratchet. Then phi_r-fires <=> phi <= peak/2 is a
    PURE consequence of the dormancy-driven Φ decay. We also keep the would-emit
    drive reachable (the score envelope is the same field->factor map as H_935) so a
    genuine 'motivated emit braked by low Φ' is countable.

    `settle` ticks let phi ratchet up to its peak first (so peak is established),
    THEN we measure — otherwise peak grows monotonically and peak/2 is trivially
    below phi. After settle we keep stepping; at low arousal the floor (0.8·peak·
    arousal) no longer holds phi up, so phi decays below peak/2 -> phi_r fires.
    """
    rng = np.random.default_rng(seed_base)
    n_ticks = 0
    n_would_emit = 0
    n_emit = 0
    n_silent = 0
    n_phi_r_fire = 0                  # ticks where phi_r is False (veto-active)
    n_phi_r_veto = 0                  # would-emit AND phi_r False AND all OTHER gates open
    n_rate_veto = 0                   # would-emit AND rate False (for the regime contrast)
    phi_samples = []
    peak_samples = []
    examples = []

    for s in range(n_seeds):
        ph0 = tuple(float(rng.uniform(-0.5, 0.5)) for _ in range(3))
        am0 = tuple(float(0.1 + rng.uniform(-0.02, 0.02)) for _ in range(3))
        pf = PureField(phase0=ph0, amp0=am0, arousal=arousal)
        for t in range(T):
            perturb = float(rng.normal(0.0, 1e-3))
            pf.step(perturb=perturb)
            if t < settle:
                continue   # let the peak establish before measuring
            # ISOLATE the phi-ratchet: external gates OPEN + rate gate OPEN.
            d = decompose_decision(pf, env_off=False, content_clean=True,
                                   seconds_since_last=999.0)
            n_ticks += 1
            phi_samples.append(pf.phi)
            peak_samples.append(pf.phi_peak)
            if d["should"]:
                n_would_emit += 1
            if d["emit"]:
                n_emit += 1
            else:
                n_silent += 1
            if not d["phi_r"]:
                n_phi_r_fire += 1
                # a phi_r VETO = a would-emit impulse braked SOLELY by low Φ
                # (all other gates open in this isolation pass).
                if d["should"] and d["kill"] and d["rate"] and d["content"]:
                    n_phi_r_veto += 1
                    if len(examples) < 6:
                        examples.append({
                            "seed": s, "tick": t,
                            "arousal": arousal,
                            "score": round(d["score"], 6),
                            "phi": round(pf.phi, 8),
                            "phi_peak": round(pf.phi_peak, 8),
                            "peak_half": round(pf.phi_peak / 2.0, 8),
                            "phi_r_ok": d["phi_r"],
                            "would_emit": d["should"],
                            "emit": d["emit"],
                            "note": "would-emit impulse braked SOLELY by low Φ (phi<=peak/2)",
                        })
            # rate-veto contrast (the H_935 awake brake): would-emit AND rate shut.
            # (uses a realistic idle clock, NOT the isolation 999s, for the contrast.)
            secs = float(rng.uniform(0.0, 90.0))
            dr = decompose_decision(pf, env_off=False, content_clean=True,
                                    seconds_since_last=secs)
            if dr["should"] and not dr["rate"]:
                n_rate_veto += 1

    return {
        "arousal": arousal,
        "n_ticks": n_ticks,
        "n_would_emit": n_would_emit,
        "n_emit": n_emit,
        "n_silent": n_silent,
        "n_phi_r_fire": n_phi_r_fire,
        "phi_r_fire_fraction_of_ticks": (n_phi_r_fire / n_ticks) if n_ticks else 0.0,
        "n_phi_r_veto": n_phi_r_veto,
        "phi_r_veto_fraction_of_silence": (n_phi_r_veto / n_silent) if n_silent else 0.0,
        "n_rate_veto_contrast": n_rate_veto,
        "phi_mean": float(np.mean(phi_samples)) if phi_samples else 0.0,
        "phi_peak_mean": float(np.mean(peak_samples)) if peak_samples else 0.0,
        "phi_below_half_peak_frac": (
            float(np.mean([p <= pk / 2.0 for p, pk in zip(phi_samples, peak_samples)]))
            if phi_samples else 0.0),
        "examples": examples,
    }


# ════════════════════════════════════════════════════════════════════════════
# verdict logic (pre-registered) — computed, never LLM-judged (p7)
# ════════════════════════════════════════════════════════════════════════════
def decide_verdict(levels):
    """Apply the FROZEN falsifier over the arousal sweep.

    SUPPORTED iff the phi_r veto FIRES (>0) at some DORMANT arousal AND it
    suppresses an otherwise-motivated emit (n_phi_r_veto > 0) AND that firing is a
    substrate-internal consequence (it appears only as arousal/Φ drops — monotone
    with dormancy, not present at full arousal). VESTIGIAL iff phi_r never fires at
    any arousal (including arousal->0).
    """
    awake = max(levels, key=lambda L: L["arousal"])
    dormant = min(levels, key=lambda L: L["arousal"])
    any_phi_r_veto = max(L["n_phi_r_veto"] for L in levels)
    any_phi_r_fire = max(L["n_phi_r_fire"] for L in levels)
    awake_fires = awake["n_phi_r_fire"]
    dormant_fires = dormant["n_phi_r_fire"]
    # substrate-internal consequence: firing emerges as arousal drops (awake≈0,
    # dormant>0) — i.e. it is DORMANCY-driven, not present in the awake substrate.
    consequence_of_dormancy = (dormant_fires > awake_fires)

    if any_phi_r_fire == 0:
        return ("🔴", "F-H937-VESTIGIAL",
                f"phi_r veto NEVER fired at any arousal (including the most dormant "
                f"a={dormant['arousal']}, phi_mean={dormant['phi_mean']:.6f}, "
                f"phi_below_half_peak_frac={dormant['phi_below_half_peak_frac']:.4f}). "
                f"The comment-advertised Φ-ratchet veto is VESTIGIAL / structurally "
                f"unreachable — only the rate-limit (H_935) is a real brake.")
    if any_phi_r_veto > 0 and consequence_of_dormancy:
        return ("🟢", "F-H937-SECOND-BRAKE-SUPPORTED",
                f"phi_r veto FIRES under dormancy and SUPPRESSES otherwise-motivated "
                f"emits: max n_phi_r_veto={any_phi_r_veto} (would-emit braked SOLELY "
                f"by low Φ, all other gates open). awake(a={awake['arousal']}) "
                f"phi_r_fires={awake_fires} -> dormant(a={dormant['arousal']}) "
                f"phi_r_fires={dormant_fires} (DORMANCY-driven: a substrate-internal "
                f"consequence of lowered arousal, not a hardcoded bool). At dormancy "
                f"phi_r vetoes are {dormant['phi_r_veto_fraction_of_silence']:.4f} of "
                f"silence. A SECOND, Φ-driven free-won't brake EXISTS — complementing "
                f"H_935's rate brake; the two cover the awake (rate) vs dormant (Φ) "
                f"regimes.")
    # phi_r fires but never as a SOLE would-emit suppressor, or not dormancy-driven
    return ("🔴", "F-H937-VESTIGIAL",
            f"phi_r fired (max n_phi_r_fire={any_phi_r_fire}) but never SOLELY "
            f"suppressed an otherwise-motivated emit (max n_phi_r_veto={any_phi_r_veto}) "
            f"as a dormancy consequence (dormant_fires={dormant_fires} vs "
            f"awake_fires={awake_fires}). Not a distinct second brake at this config.")


def main():
    N_SEEDS = int(os.environ.get("H937_SEEDS", "16"))
    T = int(os.environ.get("H937_TICKS", "1200"))
    SETTLE = int(os.environ.get("H937_SETTLE", "300"))   # establish peak before measuring
    SEED_BASE = int(os.environ.get("H937_SEED_BASE", "937"))
    # arousal sweep: awake (1.0, the exact H_935 substrate) -> deep dormancy (0.05)
    AROUSALS = [1.0, 0.75, 0.5, 0.35, 0.2, 0.1, 0.05]

    levels = [run_arousal_level(a, N_SEEDS, T, SEED_BASE + i, SETTLE)
              for i, a in enumerate(AROUSALS)]
    token, fal_id, rationale = decide_verdict(levels)

    out = {
        "h_id": "H_937",
        "title": "Φ-ratchet veto under dormancy — does the second (dormant) free-"
                 "won't brake fire when phi is driven below peak/2?",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "scope": ("ONE arousal-sweep rung (a_scale_honest_scope) on the SAME "
                  "documented-update-map mirror as H_935 (real 8-factor brain_decide, "
                  "VERBATIM CORE/engine_g+brain+pure_field.hexa constants). NOT the "
                  "compiled forge binary, NOT wired emit-TEXT (.clm generator L3 ⏳/❌, "
                  "a_core_engine_map). Dormancy envelope = arousal scaling the "
                  "activation drive + relaxing the WAKE-only ratchet floor (a SUBSTRATE "
                  "CONTEXT per a_chat_sleep_imagination, NOT a boolean emit gate per "
                  "a_autonomy_over_hardcode — phi_r fires as a DYNAMICAL consequence, "
                  "never hardcoded). Operational Φ-driven inhibition, NOT phenomenal "
                  "volition. $0 local, no GPU."),
        "deterministic_gate": True,
        "note_determinism": ("brain_decide is a deterministic pure function (no PRNG "
                             "— H_926/H_930/H_935). The veto is a deterministic gate; "
                             "entropy enters ONLY the pure_field seed-point + the "
                             "sweep RNG, NOT the gate. The phi_r firing is a "
                             "consequence of the dormancy-driven Φ decay, not RNG."),
        "g5_code_measured": True,
        "llm": "none",
        "n_seeds": N_SEEDS, "T_per_seed": T, "settle_ticks": SETTLE,
        "im_threshold": IM_THRESHOLD, "min_emit_interval_s": MIN_EMIT_INTERVAL,
        "ratchet_floor_ratio_awake": RATCHET_FLOOR_RATIO,
        "arousal_sweep": AROUSALS,
        "phi_ratchet_term": "safety_phi_ratchet_ok := phi > phi_peak/2.0  (CORE/engine_g.hexa)",
        "levels": levels,
        "verdict_token": token, "falsifier_id": fal_id, "verdict_rationale": rationale,
    }

    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(here)
    vdir = os.path.join(repo, ".verdicts", "937_phi_ratchet_veto_dormancy")
    os.makedirs(vdir, exist_ok=True)
    vpath = os.path.join(vdir, "arousal_sweep.txt")

    L = []
    L.append("H_937 — Φ-RATCHET VETO UNDER DORMANCY (closes H_935's 'phi_r never fired' gap)")
    L.append("=" * 78)
    L.append("the term under test : safety_phi_ratchet_ok := phi > phi_peak/2.0  (CORE/engine_g.hexa)")
    L.append("H_935 finding       : phi_r fired 0 times awake (ratchet floor 0.8·peak > peak/2 always)")
    L.append("H_937 test          : drive arousal awake->dormant, phi falls below peak/2, does phi_r fire?")
    L.append("isolation           : external gates OPEN + rate gate OPEN → phi-ratchet is the ONLY brake")
    L.append("")
    L.append(f"timestamp_utc : {out['timestamp_utc']}")
    L.append(f"population    : {N_SEEDS} seeds × {T} ticks (settle {SETTLE}) per arousal level")
    L.append("")
    L.append("── AROUSAL SWEEP TABLE ──────────────────────────────────────────────────────")
    L.append("  arousal  phi_mean   peak_mean  phi<=peak/2  phi_r_fires  phi_r_VETO  rate_veto(contrast)")
    for lv in levels:
        L.append(f"   {lv['arousal']:<6}  {lv['phi_mean']:.6f}  {lv['phi_peak_mean']:.6f}  "
                 f"{lv['phi_below_half_peak_frac']:.4f}     {lv['n_phi_r_fire']:>8}    "
                 f"{lv['n_phi_r_veto']:>8}    {lv['n_rate_veto_contrast']:>8}")
    L.append("")
    L.append("  phi_r_fires = ticks where phi <= peak/2 (veto-active)")
    L.append("  phi_r_VETO  = would-emit impulse braked SOLELY by low Φ (all other gates open)")
    L.append("  rate_veto   = H_935's awake brake (would-emit AND idle<30s) — regime contrast")
    L.append("")
    L.append("── EXAMPLE Φ-VETO STATES (motivated emit braked SOLELY by low Φ) ─────────────")
    dormant = min(levels, key=lambda x: x["arousal"])
    src_ex = next((lv for lv in levels if lv["examples"]), dormant)
    for ex in src_ex["examples"]:
        L.append(f"  seed={ex['seed']} tick={ex['tick']} arousal={ex['arousal']}  "
                 f"score={ex['score']} (>0.30 → would-emit)")
        L.append(f"     phi={ex['phi']} <= peak/2={ex['peak_half']} (peak={ex['phi_peak']}) "
                 f"→ phi_r_ok={ex['phi_r_ok']} → emit={ex['emit']}  [{ex['note']}]")
    L.append("")
    L.append("── VERDICT (pre-registered falsifier, CODE-decided — p7) ─────────────────────")
    L.append(f"  {token}  {fal_id}")
    L.append(f"  {rationale}")
    L.append("")
    L.append("── full machine record (JSON) ────────────────────────────────────────────────")
    L.append(json.dumps(out, indent=2, ensure_ascii=False, default=str))

    with open(vpath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"\n[written] {vpath}")
    return out


if __name__ == "__main__":
    main()
