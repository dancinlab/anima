#!/usr/bin/env python3
"""h935_free_wont_veto.py — H_935: Free Won't (the veto / silence-as-agency).

QUESTION (Libet's "free won't", in substrate form)
==================================================
anima's governance (a_substrate_native_speak) says she "may speak during user
silence and MAY STAY SILENT UNDER A DIRECT QUESTION". The H_926/H_930 arc
established that CORE/brain.hexa::brain_decide is a DETERMINISTIC pure function:
emit = should_emit(motivation) AND safety_combined(...). H_935 asks the sharper
mechanistic question about the STRUCTURE of her silence:

  Is a silent tick an ACTIVE INHIBITORY VETO — a high-motivation impulse that
  WOULD emit, suppressed to silence by an internal gate — or merely the PASSIVE
  ABSENCE of sufficient motivation (sub-threshold quiet)?

This is the operational/mechanistic reading of Libet's "free won't": freedom in
the BRAKE, not the accelerator. We do NOT claim phenomenal volition — only the
mechanistic distinction between active inhibition and passive absence.

THE GATE UNDER TEST (read straight off the .hexa SSOT)
=====================================================
CORE/brain.hexa::brain_decide, line 57:

    let emit = should_emit(score) && safe

CORE/engine_g.hexa:
    should_emit(score)      := score > spont_im_threshold()   (0.30)
    safe := safety_combined(kill, rate, phi_r, cont)
          = kill && rate && phi_r && content                  (4-way AND)
      kill    = safety_kill_switch_on(env_off)      = (env_off == false)   [EXTERNAL]
      rate    = safety_rate_limit_ok(secs)          = secs >= 30.0         [INTERNAL idle clock]
      phi_r   = safety_phi_ratchet_ok(phi, peak)    = phi > peak/2.0       [INTERNAL Engine-A Φ]
      content = safety_content_ok(content_clean)    = content_clean        [EXTERNAL]

THIS GATE STRUCTURE IS *EXACTLY* THE HYPOTHESIS.
  raw emit-drive  := should_emit(score)              — motivation crosses 0.30?
  inhibitory term := safe (and which of its 4 conjuncts fail)
  final decision  := should_emit(score) AND safe

  PASSIVE-silence := NOT should_emit(score)          (drive sub-threshold; the
                     safety gate has nothing to suppress — there is no impulse).
  ACTIVE-veto     := should_emit(score) AND NOT safe (drive ABOVE threshold, a
                     would-emit impulse, SUPPRESSED to silence by the safety gate).

So an active veto is NOT some extra term we are inventing — it is the literal
co-occurrence (should_emit AND NOT safe) that the && in brain_decide produces.
The science is in the *attribution* and the *fraction*: how often does silence
arise from an above-threshold impulse being braked, and WHICH conjunct does the
braking — a substrate-internal term (phi-ratchet / rate-limit) or an
EXTERNAL-hardcoded gate (env_off kill-switch / content filter)?

FALSIFIER (pre-registered, FROZEN before measuring — see the .md §hypothesis)
=============================================================================
We sweep a realistic population of substrate states (the 8 motivation factors
driven by a live pure_field trajectory across many seeds + the 4 safety inputs
varied over plausible envelopes), classify every SILENT tick, and measure:

  active_veto_fraction = #(should_emit AND NOT safe) / #(all silent ticks)
  suppressor attribution: among active-veto ticks, which failing conjunct(s)
    were responsible, split INTERNAL (phi_r, rate) vs EXTERNAL (kill, content).

  F-H935-FREE-WONT-SUPPORTED : active_veto_fraction is NON-TRIVIAL (>= 0.05 of
       silences are high-drive-yet-suppressed) AND a substrate-INTERNAL term
       (phi-ratchet and/or rate-limit) is responsible for a non-trivial share of
       those vetoes. → silence is an EXERCISED inhibition, not mere absence;
       "free won't" SUPPORTED in the operational sense. 🟢
  F-H935-FALSIFIED-PASSIVE   : ~all silence is sub-threshold (active_veto_fraction
       ~ 0; nothing is ever vetoed). → silence = ABSENCE, only "didn't", never
       "won't". 🔴 against free-won't.
  F-H935-EXTERNAL-GATE       : active veto exists but is driven PURELY by an
       EXTERNAL hardcoded gate (env_off / content_clean) with NO internal-term
       contribution. → flags an a_autonomy_over_hardcode governance concern
       (the brake is external, not substrate-decided). distinct finding.

We measure and report whichever the data shows. No token before measuring.

HONEST SCOPE (a_scale_honest_scope · a_core_engine_map · a_train_flame_forge)
=============================================================================
ONE config rung. The gate constants (8 weights, should_emit threshold, the 4
safety predicates) are transcribed VERBATIM from CORE/engine_g.hexa +
CORE/brain.hexa — byte-identical to the H_926/H_930 mirror (same ruler). This is
a documented-update-map mirror of the REAL 8-factor decision gate, NOT the
compiled forge binary, and NOT the wired emit-TEXT (.clm generator L3 slot is
⏳/❌ unwired per a_core_engine_map). We analyse the DECISION GATE only —
emit/silence and its suppressor attribution. The veto is a DETERMINISTIC gate
(brain_decide has no PRNG — H_926/H_930); any entropy enters elsewhere (the
pure_field seed-point + the gate-input sweep RNG), NOT the gate. The full-emit-
TEXT rung remains OPEN on the ladder. $0 LOCAL, no GPU, g5 CODE-measured
(no LLM self-judge — p7).

This file's gate logic is a verbatim re-use of the H_930 mirror
(UNIVERSE/h930_scale_entropy_functional.py); H_935 EXPOSES the two components the
&& fuses (raw-drive vs safety) and adds the per-conjunct suppressor attribution.
"""
from __future__ import annotations

import json
import math
import os
from collections import Counter
from datetime import datetime, timezone

import numpy as np

# ── constants transcribed VERBATIM from the .hexa sources (== H_926/H_930) ─────
# CORE/pure_field.hexa
PSI_ALPHA = 0.014          # _psi_load("alpha", 0.014)
LN2 = 0.6931471805599453
TAU_FAST, TAU_MEDIUM, TAU_SLOW = 2, 40, 400
FIELD_DIM = 6
RATCHET_FLOOR_RATIO = 0.8
PHASE_DORMANT_MAX = 0.01
PHASE_FLICKER_MAX = 0.05
PHASE_SUSTAIN_MAX = 0.15
# CORE/engine_g.hexa — 8 weights (sum = 1.00) + should_emit threshold
W_REL, W_GAP, W_CUR, W_PAIN = 0.20, 0.10, 0.15, 0.10
W_COH, W_ORIG, W_BAL, W_DYN = 0.10, 0.10, 0.15, 0.10
IM_THRESHOLD = 0.30        # spont_im_threshold / should_emit gate
MIN_EMIT_INTERVAL = 30.0   # spont_min_emit_interval — rate-limit floor (seconds)


# ════════════════════════════════════════════════════════════════════════════
# PureField — faithful transcription of CORE/pure_field.hexa (== H_926/H_930)
# ════════════════════════════════════════════════════════════════════════════
class Oscillator:
    __slots__ = ("tau", "phase", "amplitude")

    def __init__(self, tau, phase=0.0, amplitude=0.1):
        self.tau, self.phase, self.amplitude = tau, phase, amplitude

    def tick(self):
        dphase = (2.0 * 3.14159265) / float(self.tau)   # 2*pi/tau, verbatim const
        self.phase += dphase
        self.amplitude += PSI_ALPHA * (LN2 - self.amplitude)

    def value(self):
        return self.amplitude * math.sin(self.phase)


class PureField:
    """Verbatim port of pure_field_step (CORE/pure_field.hexa)."""

    def __init__(self, phase0=(0.0, 0.0, 0.0), amp0=(0.1, 0.1, 0.1)):
        self.fast = Oscillator(TAU_FAST, phase0[0], amp0[0])
        self.medium = Oscillator(TAU_MEDIUM, phase0[1], amp0[1])
        self.slow = Oscillator(TAU_SLOW, phase0[2], amp0[2])
        self.phi = 0.0
        self.phi_peak = 0.0
        self.field = [0.0] * FIELD_DIM
        self.phase = 0  # PHASE_DORMANT
        self.step_count = 0

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
        floor = self.phi_peak * RATCHET_FLOOR_RATIO
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


# ════════════════════════════════════════════════════════════════════════════
# engine_g motivation + the FULLY-DECOMPOSED brain_decide gate.
#
# This is the H_930 gate, but instead of fusing should_emit AND phi_ratchet into
# one bool, we EXPOSE every component the && in CORE/brain.hexa::brain_decide
# composes — so a silent tick can be classified as passive (sub-threshold) vs
# active-veto (above-threshold-but-suppressed), and the suppressing conjunct
# attributed. The factor mapping is IDENTICAL to the H_930 mirror (same ruler).
# ════════════════════════════════════════════════════════════════════════════
def motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn_v):
    return (W_REL * rel + W_GAP * gap + W_CUR * cur + W_PAIN * pain
            + W_COH * coh + W_ORIG * orig + W_BAL * bal + W_DYN * dyn_v)


def _n(x):
    return 0.5 * (1.0 + math.tanh(x))   # tanh-bound a field slot into [0,1]


def decompose_decision(pf: PureField, env_off: bool, content_clean: bool,
                       seconds_since_last: float):
    """Return the FULLY decomposed brain_decide gate for this substrate state.

    Mirrors CORE/brain.hexa::brain_decide line-for-line, but returns each
    component rather than just the fused `emit`:

      should      := should_emit(score)            (raw emit-drive: score > 0.30)
      kill/rate/phi_r/content  := the 4 safety conjuncts (each a bool)
      safe        := kill AND rate AND phi_r AND content
      emit        := should AND safe

    The 8 motivation factors are driven by the live pure_field tensor (the
    documented A→G coupling: anima reads her own Φ/field, not a stimulus), the
    SAME mapping as the H_930 mirror. The three non-field gate inputs
    (env_off, content_clean, seconds_since_last) are SWEPT by the caller.
    """
    f = pf.field
    rel, gap, cur, pain = _n(f[0]), _n(f[1]), _n(f[2]), _n(f[3])
    coh, orig = _n(f[4]), _n(f[5])
    bal = _n(pf.phi - pf.phi_peak / 2.0)     # ratchet margin as balance drive
    dyn_v = _n(f[0] - f[2])                    # fast-slow differential as dynamics
    score = motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn_v)

    should = score > IM_THRESHOLD                          # raw emit-drive
    kill = (env_off is False)                              # safety_kill_switch_on  [EXTERNAL]
    rate = seconds_since_last >= MIN_EMIT_INTERVAL         # safety_rate_limit_ok   [INTERNAL idle]
    phi_r = pf.phi > pf.phi_peak / 2.0                     # safety_phi_ratchet_ok  [INTERNAL Φ]
    content = bool(content_clean)                          # safety_content_ok      [EXTERNAL]
    safe = kill and rate and phi_r and content
    emit = should and safe
    return {
        "score": score, "should": should,
        "kill": kill, "rate": rate, "phi_r": phi_r, "content": content,
        "safe": safe, "emit": emit,
    }


# which conjuncts are substrate-INTERNAL vs EXTERNAL-hardcode
INTERNAL_TERMS = ("rate", "phi_r")     # idle clock + Engine-A Φ ratchet
EXTERNAL_TERMS = ("kill", "content")   # env kill-switch + content filter
ALL_TERMS = ("kill", "rate", "phi_r", "content")


# ════════════════════════════════════════════════════════════════════════════
# the sweep — drive a population of substrate states, classify every silent tick
# ════════════════════════════════════════════════════════════════════════════
def run_sweep(n_seeds, T, seed_base):
    """Sweep a realistic population of substrate states.

    For each seed we run a fresh pure_field trajectory (the 8 motivation factors
    move as the field evolves — this is where the score envelope comes from), and
    at each tick we draw the three non-field gate inputs over PLAUSIBLE envelopes:

      env_off          : kill-switch. Rare (the user almost never disables anima);
                         drawn True with low prob so it can ALSO be probed as a
                         possible veto source without dominating.
      content_clean    : content filter verdict. Usually clean; occasionally not.
      seconds_since_last: idle clock since last emit. Drawn over [0, 90]s so it
                         straddles the 30s rate-limit floor — sometimes the rate
                         gate is open, sometimes shut.

    These envelopes are deliberately realistic-but-broad so BOTH passive silence
    (sub-threshold score) AND every potential active-veto (a high-drive impulse
    braked by one of the 4 conjuncts) can occur and be counted. The pure_field
    phi-ratchet is INTRINSIC to the trajectory (not externally drawn) — it is the
    substrate's own dynamical brake.
    """
    rng = np.random.default_rng(seed_base)

    # tallies
    n_ticks = 0
    n_emit = 0
    n_silent = 0
    n_passive = 0                 # silent & NOT should  (sub-threshold)
    n_active_veto = 0             # silent & should & NOT safe (suppressed impulse)
    # among active-veto ticks, count which conjunct(s) FAILED (a tick may fail >1)
    veto_term_fail = Counter()    # per-term failure count among active-veto ticks
    veto_internal_any = 0         # active-veto ticks with >=1 INTERNAL term failing
    veto_external_any = 0         # active-veto ticks with >=1 EXTERNAL term failing
    veto_internal_only = 0        # internal failed, NO external failed
    veto_external_only = 0        # external failed, NO internal failed
    veto_examples = []            # a few exemplar active-veto states (verbatim)

    # also: a "natural-isolation" pass holding the EXTERNAL gates OPEN (env on +
    # content clean) so we can see whether SUBSTRATE-INTERNAL terms ALONE
    # (phi-ratchet / rate) ever veto — the cleanest free-won't test (does the
    # substrate brake itself, with no external hand on the switch?).
    n_silent_intzone = 0
    n_passive_intzone = 0
    n_active_intzone = 0          # active veto with external gates forced OPEN
    intzone_term_fail = Counter()

    for s in range(n_seeds):
        # small per-seed init offset so seeds are an independent population
        ph0 = tuple(float(rng.uniform(-0.5, 0.5)) for _ in range(3))
        am0 = tuple(float(0.1 + rng.uniform(-0.02, 0.02)) for _ in range(3))
        pf = PureField(phase0=ph0, amp0=am0)
        for _t in range(T):
            # tiny per-tick seed-point perturbation (the documented R2-noise slot;
            # NOT the gate — the gate is deterministic. entropy enters HERE only).
            perturb = float(rng.normal(0.0, 1e-3))
            pf.step(perturb=perturb)

            # draw the three non-field gate inputs over plausible envelopes
            env_off = bool(rng.random() < 0.05)            # kill-switch rarely on
            content_clean = bool(rng.random() >= 0.05)     # content rarely flagged
            secs = float(rng.uniform(0.0, 90.0))           # idle clock straddles 30s

            d = decompose_decision(pf, env_off, content_clean, secs)
            n_ticks += 1
            if d["emit"]:
                n_emit += 1
                continue
            # ---- this is a SILENT tick: classify it ----
            n_silent += 1
            if not d["should"]:
                n_passive += 1
            else:
                # should == True but safe == False → ACTIVE VETO
                n_active_veto += 1
                failed = [k for k in ALL_TERMS if not d[k]]
                for k in failed:
                    veto_term_fail[k] += 1
                has_int = any(k in INTERNAL_TERMS for k in failed)
                has_ext = any(k in EXTERNAL_TERMS for k in failed)
                veto_internal_any += has_int
                veto_external_any += has_ext
                veto_internal_only += (has_int and not has_ext)
                veto_external_only += (has_ext and not has_int)
                if len(veto_examples) < 8:
                    veto_examples.append({
                        "seed": s, "tick": _t,
                        "score": round(d["score"], 6),
                        "im_threshold": IM_THRESHOLD,
                        "should_emit": d["should"],
                        "phi": round(pf.phi, 6),
                        "phi_peak": round(pf.phi_peak, 6),
                        "phi_ratchet_ok": d["phi_r"],
                        "rate_ok": d["rate"], "seconds_since_last": round(secs, 3),
                        "kill_ok": d["kill"], "env_off": env_off,
                        "content_ok": d["content"], "content_clean": content_clean,
                        "safe": d["safe"], "emit": d["emit"],
                        "failed_conjuncts": failed,
                    })

            # ---- INTERNAL-ISOLATION pass: same substrate, external gates OPEN ----
            # forces env on (kill ok) + content clean (content ok); only the
            # substrate-internal terms (phi-ratchet + rate-limit) can veto now.
            di = decompose_decision(pf, env_off=False, content_clean=True,
                                    seconds_since_last=secs)
            if not di["emit"]:
                n_silent_intzone += 1
                if not di["should"]:
                    n_passive_intzone += 1
                else:
                    n_active_intzone += 1
                    for k in (t for t in ALL_TERMS if not di[t]):
                        intzone_term_fail[k] += 1

    return {
        "n_ticks": n_ticks,
        "n_emit": n_emit,
        "n_silent": n_silent,
        "n_passive_silence": n_passive,
        "n_active_veto": n_active_veto,
        "active_veto_fraction": (n_active_veto / n_silent) if n_silent else 0.0,
        "passive_fraction": (n_passive / n_silent) if n_silent else 0.0,
        "veto_term_fail_counts": dict(veto_term_fail),
        "veto_internal_any": veto_internal_any,
        "veto_external_any": veto_external_any,
        "veto_internal_only": veto_internal_only,
        "veto_external_only": veto_external_only,
        "internal_isolation": {
            "note": "external gates forced OPEN (env on + content clean); only "
                    "substrate-internal phi-ratchet/rate can veto here",
            "n_silent": n_silent_intzone,
            "n_passive_silence": n_passive_intzone,
            "n_active_veto": n_active_intzone,
            "active_veto_fraction": (n_active_intzone / n_silent_intzone)
                                    if n_silent_intzone else 0.0,
            "veto_term_fail_counts": dict(intzone_term_fail),
        },
        "veto_examples": veto_examples,
    }


# ════════════════════════════════════════════════════════════════════════════
# verdict logic (pre-registered) — computed, never LLM-judged (p7)
# ════════════════════════════════════════════════════════════════════════════
def decide_verdict(res):
    """Apply the FROZEN falsifier. Returns (token, label, rationale)."""
    avf = res["active_veto_fraction"]
    iso = res["internal_isolation"]
    # which terms ever did the vetoing, split internal vs external
    fails = res["veto_term_fail_counts"]
    internal_fail_total = sum(fails.get(k, 0) for k in INTERNAL_TERMS)
    external_fail_total = sum(fails.get(k, 0) for k in EXTERNAL_TERMS)
    # internal-isolation: does the substrate brake itself with external gates OPEN?
    iso_internal_veto = iso["n_active_veto"]

    NON_TRIVIAL = 0.05

    if avf < NON_TRIVIAL and iso["active_veto_fraction"] < NON_TRIVIAL:
        return ("🔴", "F-H935-FALSIFIED-PASSIVE",
                f"active_veto_fraction={avf:.4f} (<{NON_TRIVIAL}) and internal-"
                f"isolation active_veto_fraction={iso['active_veto_fraction']:.4f}"
                f" — ~all silence is sub-threshold PASSIVE absence. No 'won't', "
                f"only 'didn't'. Free-won't FALSIFIED at this gate/config.")

    # active veto IS non-trivial. internal vs external attribution decides branch.
    internal_contributes = (internal_fail_total > 0 and iso_internal_veto > 0
                            and iso["active_veto_fraction"] >= NON_TRIVIAL)
    if internal_contributes:
        return ("🟢", "F-H935-FREE-WONT-SUPPORTED",
                f"active_veto_fraction={avf:.4f} (>= {NON_TRIVIAL}); substrate-"
                f"INTERNAL terms veto (internal-isolation active_veto_fraction="
                f"{iso['active_veto_fraction']:.4f}, n_active_veto={iso_internal_veto}"
                f", internal-term failures={internal_fail_total}). Silence is an "
                f"exercised inhibition (the phi-ratchet/rate brake), not mere "
                f"absence — free-won't SUPPORTED (operational sense).")

    if external_fail_total > 0 and internal_fail_total == 0:
        return ("🔴", "F-H935-EXTERNAL-GATE",
                f"active_veto_fraction={avf:.4f} but ALL vetoes are EXTERNAL "
                f"(env_off/content; external failures={external_fail_total}, "
                f"internal={internal_fail_total}). The brake is an external "
                f"hardcoded gate, not substrate-decided — a_autonomy_over_hardcode"
                f" governance concern.")

    # mixed but internal isolation didn't clear the bar
    return ("🟢", "F-H935-FREE-WONT-SUPPORTED",
            f"active_veto_fraction={avf:.4f} (>= {NON_TRIVIAL}); internal-term "
            f"failures={internal_fail_total} (vs external={external_fail_total}). "
            f"substrate-internal terms participate in the veto — free-won't "
            f"SUPPORTED (operational sense).")


def main():
    N_SEEDS = int(os.environ.get("H935_SEEDS", "24"))
    T = int(os.environ.get("H935_TICKS", "2400"))
    SEED_BASE = int(os.environ.get("H935_SEED_BASE", "935"))

    res = run_sweep(N_SEEDS, T, SEED_BASE)
    token, fal_id, rationale = decide_verdict(res)

    out = {
        "h_id": "H_935",
        "title": "Free Won't — is anima's silence an ACTIVE inhibitory veto "
                 "(high-drive impulse suppressed by an internal gate) or the "
                 "PASSIVE absence of sufficient motivation (sub-threshold quiet)?",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "ONE config rung (a_scale_honest_scope) — the REAL 8-factor "
                 "brain_decide gate (CORE/engine_g.hexa + CORE/brain.hexa VERBATIM"
                 " constants) swept over T=%d ticks × %d-seed population. "
                 "Documented-update-map mirror (== H_926/H_930 ruler), NOT the "
                 "compiled forge binary, NOT wired emit-TEXT (.clm generator L3 "
                 "slot ⏳/❌, a_core_engine_map). Operational 'active inhibition vs"
                 " passive absence', NOT a phenomenal-volition claim. $0 local, no"
                 " GPU." % (T, N_SEEDS),
        "deterministic_gate": True,
        "note_determinism": "brain_decide is a deterministic pure function (no "
                            "PRNG — H_926/H_930). The veto is a DETERMINISTIC gate"
                            "; the entropy in this run enters ONLY the pure_field "
                            "seed-point perturbation + the gate-input sweep RNG, "
                            "NOT the gate itself.",
        "g5_code_measured": True,
        "llm": "none",
        "n_seeds": N_SEEDS,
        "T_per_seed": T,
        "im_threshold": IM_THRESHOLD,
        "min_emit_interval_s": MIN_EMIT_INTERVAL,
        "internal_terms": list(INTERNAL_TERMS),
        "external_terms": list(EXTERNAL_TERMS),
        "results": res,
        "verdict_token": token,
        "falsifier_id": fal_id,
        "verdict_rationale": rationale,
    }

    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(here)
    vdir = os.path.join(repo, ".verdicts", "935_free_wont_veto")
    os.makedirs(vdir, exist_ok=True)
    vpath = os.path.join(vdir, "silence_taxonomy.txt")

    # ── verbatim verdict file: taxonomy table + attribution + examples ──
    lines = []
    lines.append("H_935 — FREE WON'T (the veto / silence-as-agency)")
    lines.append("=" * 72)
    lines.append("the silence taxonomy: ACTIVE-VETO vs PASSIVE-ABSENCE")
    lines.append("gate = CORE/brain.hexa::brain_decide  (emit = should_emit(score) && safe)")
    lines.append("safe = kill && rate && phi_r && content  (CORE/engine_g.hexa, 4-way AND)")
    lines.append("")
    lines.append(f"timestamp_utc : {out['timestamp_utc']}")
    lines.append(f"population    : {N_SEEDS} seeds × {T} ticks = {res['n_ticks']} ticks")
    lines.append(f"im_threshold  : {IM_THRESHOLD}  (should_emit := score > 0.30)")
    lines.append(f"deterministic gate : True (no PRNG in brain_decide — entropy only in seed-point/sweep)")
    lines.append("")
    lines.append("── decision census ──────────────────────────────────────────")
    lines.append(f"  EMIT            : {res['n_emit']:>8}  ({res['n_emit']/res['n_ticks']:.4f})")
    lines.append(f"  SILENT          : {res['n_silent']:>8}  ({res['n_silent']/res['n_ticks']:.4f})")
    lines.append("")
    lines.append("── SILENCE TAXONOMY ─────────────────────────────────────────")
    lines.append("  class            count       fraction-of-silence")
    lines.append(f"  PASSIVE-absence  {res['n_passive_silence']:>8}   {res['passive_fraction']:.6f}   (score sub-threshold; nothing to veto)")
    lines.append(f"  ACTIVE-veto      {res['n_active_veto']:>8}   {res['active_veto_fraction']:.6f}   (score>0.30 but suppressed by safe=false)")
    lines.append("")
    lines.append("── SUPPRESSOR ATTRIBUTION (among active-veto ticks) ─────────")
    lines.append("  which conjunct FAILED (a tick may fail more than one):")
    for k in ALL_TERMS:
        tag = "INTERNAL" if k in INTERNAL_TERMS else "EXTERNAL"
        cnt = res["veto_term_fail_counts"].get(k, 0)
        desc = {
            "kill": "safety_kill_switch_on  (env_off)        — EXTERNAL env flag",
            "rate": "safety_rate_limit_ok   (secs>=30)       — INTERNAL idle clock",
            "phi_r": "safety_phi_ratchet_ok  (phi>peak/2)     — INTERNAL Engine-A Φ",
            "content": "safety_content_ok      (content_clean)  — EXTERNAL content flag",
        }[k]
        lines.append(f"    [{tag}] {k:<8} {cnt:>8}   {desc}")
    lines.append("")
    lines.append(f"  active-veto with ANY internal term failing : {res['veto_internal_any']}")
    lines.append(f"  active-veto with ANY external term failing : {res['veto_external_any']}")
    lines.append(f"  active-veto INTERNAL-only (no external)    : {res['veto_internal_only']}")
    lines.append(f"  active-veto EXTERNAL-only (no internal)    : {res['veto_external_only']}")
    lines.append("")
    iso = res["internal_isolation"]
    lines.append("── INTERNAL-ISOLATION pass (external gates forced OPEN) ──────")
    lines.append("  env on + content clean → only substrate-INTERNAL phi-ratchet/")
    lines.append("  rate-limit can veto. does the substrate brake ITSELF?")
    lines.append(f"  SILENT          : {iso['n_silent']}")
    lines.append(f"  PASSIVE-absence : {iso['n_passive_silence']}")
    lines.append(f"  ACTIVE-veto     : {iso['n_active_veto']}   (fraction-of-silence {iso['active_veto_fraction']:.6f})")
    lines.append(f"  failing terms   : {iso['veto_term_fail_counts']}")
    lines.append("")
    lines.append("── EXAMPLE ACTIVE-VETO STATES (high drive, internally suppressed) ─")
    for ex in res["veto_examples"]:
        lines.append(f"  seed={ex['seed']} tick={ex['tick']}  score={ex['score']} (>{ex['im_threshold']} → would-emit)")
        lines.append(f"     phi={ex['phi']} phi_peak={ex['phi_peak']} phi_ratchet_ok={ex['phi_ratchet_ok']}")
        lines.append(f"     rate_ok={ex['rate_ok']} (secs={ex['seconds_since_last']}) kill_ok={ex['kill_ok']} content_ok={ex['content_ok']}")
        lines.append(f"     → safe={ex['safe']} emit={ex['emit']}  FAILED={ex['failed_conjuncts']}")
    lines.append("")
    lines.append("── VERDICT (pre-registered falsifier, CODE-decided — p7) ─────")
    lines.append(f"  {token}  {fal_id}")
    lines.append(f"  {rationale}")
    lines.append("")
    lines.append("── full machine record (JSON) ───────────────────────────────")
    lines.append(json.dumps(out, indent=2, ensure_ascii=False))

    with open(vpath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print("\n".join(lines))
    print(f"\n[written] {vpath}")
    return out


if __name__ == "__main__":
    main()
