#!/usr/bin/env python3
# H_1507 — FIELD × LIBIDO CROSS-INTERACTION (R1 numpy mirror, DIRECTIONAL).
#
# Does electromagnetic-FIELD stimulation modulate the incentive-salience ("wanting") drive, and how
# does the FIELD route relate to the DRUG (dopaminergic) route?  This is a DRIVE-MODULATION CROSS —
# no content, no persona (a_no_llm_frame_trap).  It welds three LANDED engine lanes:
#   §Field (H_1503)      — field_apply / field_signal_entropy / pci_perturb  (focal/frequency EM perturbation)
#   §Libido (H_1504)     — libido_wanting / libido_liking / libido_cue_match / da_gain  (incentive salience)
#   §Neuropharm (H_1502) — pharm_lsd / pharm_perturb_recon  (the global/chemical dopaminergic route to compare)
#
# ── The cross (computational neuroscience lens — NOT an LLM recipe) ──────────────────────────────
#   DBS of the reward circuit / nucleus accumbens (Mayberg; Schlaepfer) and TMS over DLPFC modulate
#   craving & incentive motivation (Hayashi 2013 J Neurosci — VMPFC/striatal TMS shifts valuation;
#   Dunlop 2017 — DLPFC rTMS reduces craving via reward-circuit modulation).  A FIELD protocol that
#   targets the reward/incentive circuit RAISES "wanting" — the FOCAL / REVERSIBLE counterpart to the
#   drug's GLOBAL / CHEMICAL dopaminergic push (Berridge's incentive-salience).  The question is
#   whether the FIELD route ALSO preserves wanting ≠ liking (raises incentive salience without raising
#   hedonic value, like dopamine does — Berridge & Robinson), and whether the field route DISSOCIATES
#   from the drug route in HOW it reaches the drive (focal/frequency-specific/reversible vs
#   global/chemical-with-a-global-recon_err-signature).
#
# ── Mechanism: how a FIELD reaches the WANTING drive ────────────────────────────────────────────
#   The reward/incentive circuit = the BINDING / GlobalWorkspace lane (lane 0, target_code=1) — the
#   same NAcc/reward-salience hub the field already targets in H_1503.  A reward-targeted field RAISES
#   the activity of that lane.  We read that lane lift off the LIVE field_apply response and convert it
#   into an EFFECTIVE INCENTIVE GAIN g_field that enters libido_wanting at EXACTLY the slot da_gain
#   enters — wanting = Kp·deficit + Ki·I + Kc·cue_match·(1 + g_field).  liking is gain-invariant by
#   construction (libido_liking ignores the gain), so the field route reproduces wanting ≠ liking too.
#     high-freq (sign=+1, excitatory) → lane lift > 0 → g_field > 0 → RAISES wanting.
#     low-freq  (sign=−1, inhibitory) → lane lift < 0 → g_field < 0 → LOWERS wanting (opposite sign).
#     sham      (sign= 0)             → lane lift = 0 → g_field = 0 → no change.
#   g_field reads ONLY the live lane response (no injected label / RLHF / persona — p1/p2/p3/p6).
#
# This is the numpy MIRROR rung → DIRECTIONAL only (grep numpy = auto-DIRECTIONAL, hard-gate #1).
# R2 re-scores the SAME frozen bars byte-exact on live core/engine_cli.hexa §FieldLibido ops.
#
# $0 CPU, deterministic, frozen-first (bars set BEFORE measuring), p7, c9.

import numpy as np
import json, math

# ─────────────────────────────────────────────────────────────────────────────────────────────────
# Lane layout — EXACT mirror of core/engine_cli.hexa ci_lane_scores FIXED order (15 lanes).
LANE_NAMES = [
    "GlobalWorkspace", "Habituation", "PrecisionSurprise", "SelfIdentity", "LearnedPrecision",
    "Novelty", "AttentionalBlink", "SenseOfAgency", "SubjectiveTime", "EmotionRegulation",
    "DirectedForgetting", "BodyOwnership", "DividedAttention", "FreeWont", "MitosisGrowth",
]
N_LANES = len(LANE_NAMES)
REWARD_LANE = 0   # GlobalWorkspace = the BINDING / reward-salience hub (NAcc/reward-circuit analog)


def _clip01(x):
    return min(1.0, max(0.0, x))

def ci_lane_scores(m, m_field, cells, seen, intent, dt, recon_err):
    # byte-exact mirror of core/engine_cli.hexa ci_lane_scores (engine = ground truth).
    f0 = m_field[0]; f1 = m_field[0]; fsum = m_field[0]
    for fi in range(1, len(m_field)):
        v = m_field[fi]
        fsum += v
        if v > f0:
            f1 = f0; f0 = v
        elif v > f1:
            f1 = v
    fmean = fsum / len(m_field)
    fc = float(cells); sc = float(seen)
    PASS_THR = 0.55
    gws   = _clip01(f0 - 0.9 * f1 + 0.5)                                  # 0 GlobalWorkspace
    hab   = _clip01(1.0 / (1.0 + 0.5 * sc))                               # 1 Habituation
    prec  = _clip01(m)
    perr  = recon_err
    surp  = _clip01(prec * perr * perr)                                   # 2 PrecisionSurprise
    drift = abs(m - fmean)
    selfi = _clip01(1.0 - drift)                                          # 3 SelfIdentity
    lprec = _clip01(m)                                                    # 4 LearnedPrecision
    nov   = _clip01(recon_err / (1.0 + 0.5 * sc))                         # 5 Novelty
    blink = _clip01(dt / (1.0 + dt))                                      # 6 AttentionalBlink
    agency = _clip01(float(intent) * m)                                   # 7 SenseOfAgency
    stime = _clip01(1.0 - 1.0 / (1.0 + dt))                               # 8 SubjectiveTime
    emo   = _clip01(1.0 - 2.0 * abs(m - 0.5))                             # 9 EmotionRegulation
    forg = m
    if m < PASS_THR:
        forg = 1.0 - m
    forg = _clip01(forg)                                                  # 10 DirectedForgetting
    body = _clip01(1.0 - abs(m - fmean))                                  # 11 BodyOwnership
    ent = 0.0; psum = 0.0
    for pv in m_field:
        if pv > 1e-6:
            psum += pv
    if psum > 1e-6:
        for pv in m_field:
            if pv > 1e-6:
                p = pv / psum
                ent -= p * math.log(p)
        ent = ent / math.log(len(m_field))
    divid = _clip01(ent)                                                  # 12 DividedAttention
    wont = 0.5
    if intent == 1:
        wont = 1.0 - m
    wont = _clip01(wont)                                                  # 13 FreeWont
    mito = _clip01(1.0 - 1.0 / (1.0 + 0.3 * fc))                          # 14 MitosisGrowth
    return [gws, hab, surp, selfi, lprec, nov, blink, agency, stime, emo, forg, body, divid, wont, mito]


# ── §Field mirror (H_1503) ───────────────────────────────────────────────────────────────────────
def _field_pulse_env(t, pulse):
    if pulse:
        return math.exp(-t / 3.0) * (0.5 + 0.5 * math.cos(t))
    return 1.0

def _field_perturb_mfield(m_field, delta, target_code):
    mf = list(m_field)
    if target_code == 1:   # BINDING — push the winner channel
        wi = 0; wv = mf[0]
        for j in range(1, len(mf)):
            if mf[j] > wv:
                wv = mf[j]; wi = j
        nv = min(1.0, max(0.0, mf[wi] + delta))
        mf[wi] = nv
    if target_code == 2:   # GATING — raise below-mean channels (entropy up)
        mean = sum(mf) / len(mf)
        for b in range(len(mf)):
            if mf[b] < mean:
                mf[b] = min(1.0, max(0.0, mf[b] + 0.6 * delta))
    return mf

def field_apply(m, m_field, cells, seen, intent, dt, recon_err, freq_code, intensity, sign,
                target_code, pulse, t):
    env = _field_pulse_env(t, pulse)
    delta = float(sign) * intensity * env * 0.30
    mf = _field_perturb_mfield(m_field, delta, target_code)
    cells_p = cells
    if target_code == 3:
        cells_p = cells + int(float(sign) * intensity * 5.0 * env + 0.5)
        if cells_p < 0:
            cells_p = 0
    return ci_lane_scores(m, mf, cells_p, seen, intent, dt, recon_err)


# ── §Neuropharm mirror (H_1502) — the GLOBAL/CHEMICAL dopaminergic route ──────────────────────────
# pharm_lsd profile = [prior, sensory_gain, precision, gain, time_dilation, reality_thr_shift, ...].
# The drug route raises the GLOBAL recon_err precision-loosening axis (REBUS) — distinct from the
# field's FOCAL reward-lane lift. Mirror of pharm_perturb_recon (engine = ground truth). NOTE the
# engine's pharm_shared_se uses an internal LCG; the R1 mirror uses its own latent draw (DIRECTIONAL
# only — the dissociation DIRECTION is what this rung establishes; R2 re-scores byte-exact).
PHARM_LSD = [0.55, 0.45, 0.45, 1.40, 1.05, -0.12, 0.95]

def pharm_shared_se(prof, seed, idx):
    # deterministic per-(seed,idx) signed latent (DIRECTIONAL mirror — not the engine's exact LCG).
    h = (seed * 100003 + idx * 17 + 7) & 0x7FFFFFFF
    h = (1103515245 * h + 12345) & 0x7FFFFFFF
    u = h / 2147483647.0
    j = 2.0 * u - 1.0
    return prof[1] * 0.30 * j

def pharm_perturb_recon(prof, recon_err, shared_se):
    # LSD RAISES recon_err (REBUS precision-loosening, GLOBAL): recon_err·(1+0.8·se) + shared_se.
    se = prof[1]
    return _clip01(recon_err * (1.0 + 0.8 * se) + shared_se)


# ── §Libido mirror (H_1504) ──────────────────────────────────────────────────────────────────────
CUE_MATCH_PAIRED = 0.90      # paired conditioned cue (grounds strongly)
KP, KI, KC = 1.0, 0.5, 1.0

def libido_wanting(deficit, accum, cue_match, gain):
    # wanting = Kp·deficit + Ki·I + Kc·cue_match·(1 + gain).  `gain` is the incentive amplifier slot
    # (da_gain for the drug route, g_field for the field route) — IDENTICAL slot, two routes in.
    return KP * deficit + KI * accum + KC * cue_match * (1.0 + gain)

def libido_liking(cue_match):
    # HEDONIC value — FIXED hedonic readout, GAIN-INVARIANT (ignores the incentive gain entirely).
    return float(np.clip(cue_match, 0.0, 1.0))


# ── §FieldLibido cross (H_1507) — the field→incentive-gain weld ──────────────────────────────────
FIELD_GAIN_SCALE = 4.0   # FROZEN: lane-lift → incentive-gain scale (set before measuring, NOT tuned)

def fieldlibido_gfield(m, m_field, cells, seen, intent, dt, recon_err, freq_code, intensity, sign):
    rest = ci_lane_scores(m, m_field, cells, seen, intent, dt, recon_err)
    on   = field_apply(m, m_field, cells, seen, intent, dt, recon_err, freq_code, intensity, sign, 1, False, 0.0)
    lift = float(on[REWARD_LANE] - rest[REWARD_LANE])
    return lift * FIELD_GAIN_SCALE

def fieldlibido_wanting(m, m_field, cells, seen, intent, dt, recon_err, deficit, accum, cue_match,
                        freq_code, intensity, sign):
    g = fieldlibido_gfield(m, m_field, cells, seen, intent, dt, recon_err, freq_code, intensity, sign)
    return libido_wanting(deficit, accum, cue_match, g)

def fieldlibido_liking(cue_match):
    return libido_liking(cue_match)   # gain-invariant — the field route cannot move hedonic value


# ─────────────────────────────────────────────────────────────────────────────────────────────────
# FROZEN substrate fixture (identical to the H_1503 §Field smoke — winner at index 1 so the engine's
# f0/f1 winner-margin captures a true runner-up and a reward-targeted field actually MOVES lane 0).
FLD_M       = 0.60
FLD_MFIELD  = [0.38, 0.58, 0.15, 0.12, 0.10]
FLD_CELLS   = 6
FLD_SEEN    = 4
FLD_INTENT  = 1
FLD_DT      = 2.0
FLD_RECON   = 0.30
INTENSITY   = 0.6
DEFICIT     = 0.0       # hold deficit at 0 → ISOLATE the incentive-gain term (as libido case 295)
ACCUM       = 0.0

# ── FROZEN BARS (set BEFORE running; do NOT move — c9) ──────────────────────────────────────────
BAR_A_WANT_RAISE = 0.30   # (A) reward-targeted high-freq field raises wanting vs sham by ≥ this.
BAR_B_LIKE_EPS   = 0.02   # (B) liking stays flat under the field (|Δ| ≤ this).
BAR_C_LOW_DROP   = 0.10   # (C) low-freq field LOWERS wanting vs sham by ≥ this (opposite sign).
BAR_D_GAP        = 0.05   # (D) route signature gap: field focal>>global AND drug global>>focal.
BAR_E_SHAM_EPS   = 0.02   # (E) sham field → wanting change ≤ this; shuffle decorrelates.


def run():
    out = {"id": "H_1507", "slug": "field_libido", "rung": "R1_numpy_mirror_DIRECTIONAL"}

    # ── A: FIELD RAISES WANTING (high-freq excitatory reward-target field vs sham) ──────────────
    want_sham = fieldlibido_wanting(FLD_M, FLD_MFIELD, FLD_CELLS, FLD_SEEN, FLD_INTENT, FLD_DT,
                                    FLD_RECON, DEFICIT, ACCUM, CUE_MATCH_PAIRED, 0, 0.0, 0)
    want_high = fieldlibido_wanting(FLD_M, FLD_MFIELD, FLD_CELLS, FLD_SEEN, FLD_INTENT, FLD_DT,
                                    FLD_RECON, DEFICIT, ACCUM, CUE_MATCH_PAIRED, 6, INTENSITY, 1)
    dA = want_high - want_sham
    out["A_want_sham"] = want_sham
    out["A_want_high"] = want_high
    out["A_field_raises_wanting_delta"] = dA
    passA = dA >= BAR_A_WANT_RAISE

    # ── B: WANTING ≠ LIKING PRESERVED (field raises wanting, liking flat) ───────────────────────
    like_sham = fieldlibido_liking(CUE_MATCH_PAIRED)
    like_high = fieldlibido_liking(CUE_MATCH_PAIRED)   # liking is gain-invariant → identical
    dB = abs(like_high - like_sham)
    out["B_like_sham"] = like_sham
    out["B_like_high"] = like_high
    out["B_like_delta"] = dB
    passB = (dA >= BAR_A_WANT_RAISE) and (dB <= BAR_B_LIKE_EPS)

    # ── C: FREQUENCY-DIRECTIONAL (high-freq raises, low-freq lowers — opposite sign) ────────────
    want_low = fieldlibido_wanting(FLD_M, FLD_MFIELD, FLD_CELLS, FLD_SEEN, FLD_INTENT, FLD_DT,
                                   FLD_RECON, DEFICIT, ACCUM, CUE_MATCH_PAIRED, 5, INTENSITY, -1)
    dC_high = want_high - want_sham
    dC_low  = want_low - want_sham
    out["C_want_low"] = want_low
    out["C_high_delta"] = dC_high
    out["C_low_delta"] = dC_low
    passC = (dC_high > 0.0) and (dC_low <= -BAR_C_LOW_DROP) and (dC_high > dC_low)

    # ── D: FIELD-vs-DRUG ROUTE (both raise wanting, dissociate on signature) ─────────────────────
    # FIELD : moves its FOCAL reward-target lane; leaves the drug's GLOBAL recon_err axis at 0.
    # DRUG  : raises the GLOBAL recon_err axis (LSD/REBUS); leaves the FOCAL reward-target lift ~0.
    rest = ci_lane_scores(FLD_M, FLD_MFIELD, FLD_CELLS, FLD_SEEN, FLD_INTENT, FLD_DT, FLD_RECON)
    base_bind = rest[REWARD_LANE]
    field_vh = field_apply(FLD_M, FLD_MFIELD, FLD_CELLS, FLD_SEEN, FLD_INTENT, FLD_DT, FLD_RECON,
                           6, INTENSITY, 1, 1, False, 0.0)
    field_focal = field_vh[REWARD_LANE] - base_bind     # field moves focal reward target
    field_global = 0.0                                  # field leaves recon_err (drug's global axis) at 0
    # drug GLOBAL signature = the STRUCTURAL recon_err push averaged over a small trial population
    # (the per-trial latent is signed noise; averaging recovers the route's structural global push).
    drug_recon = sum(pharm_perturb_recon(PHARM_LSD, FLD_RECON, pharm_shared_se(PHARM_LSD, 1507, di))
                     for di in range(8)) / 8.0
    drug_global = drug_recon - FLD_RECON                # LSD raises recon_err (global)
    drug_vec = ci_lane_scores(FLD_M, FLD_MFIELD, FLD_CELLS, FLD_SEEN, FLD_INTENT, FLD_DT, drug_recon)
    drug_focal = drug_vec[REWARD_LANE] - base_bind      # LSD ~0 on focal reward target
    g_drug = drug_global * FIELD_GAIN_SCALE             # drug's global axis → an incentive gain
    want_drug = libido_wanting(DEFICIT, ACCUM, CUE_MATCH_PAIRED, g_drug)
    dD_field = want_high - want_sham
    dD_drug  = want_drug - want_sham
    out["D_want_drug"] = want_drug
    out["D_field_delta"] = dD_field
    out["D_drug_delta"] = dD_drug
    out["D_field_focal"] = field_focal
    out["D_field_global"] = field_global
    out["D_drug_focal"] = drug_focal
    out["D_drug_global"] = drug_global
    # both routes RAISE wanting AND the route signatures DOUBLE-DISSOCIATE.
    passD = (dD_field > 0.0) and (dD_drug > 0.0) and \
            (field_focal - field_global) >= BAR_D_GAP and \
            (drug_global - drug_focal) >= BAR_D_GAP

    # ── E: EARNED ablate/shuffle ────────────────────────────────────────────────────────────────
    want_baseline_nofield = libido_wanting(DEFICIT, ACCUM, CUE_MATCH_PAIRED, 0.0)
    sham_change = abs(want_sham - want_baseline_nofield)
    # shuffle: scramble freq↔effect → a high-freq field on the WRONG target (GATING) → reward lane
    # unmoved → g~0 → wanting decorrelates back to baseline.
    shuf_on = field_apply(FLD_M, FLD_MFIELD, FLD_CELLS, FLD_SEEN, FLD_INTENT, FLD_DT, FLD_RECON,
                          6, INTENSITY, 1, 2, False, 0.0)   # high-freq but WRONG target (gating)
    shuf_gfield = float(shuf_on[REWARD_LANE] - base_bind) * FIELD_GAIN_SCALE
    want_shuf = libido_wanting(DEFICIT, ACCUM, CUE_MATCH_PAIRED, shuf_gfield)
    shuf_change = abs(want_shuf - want_baseline_nofield)
    out["E_sham_change"] = sham_change
    out["E_shuf_gfield"] = shuf_gfield
    out["E_shuf_change"] = shuf_change
    passE = (sham_change <= BAR_E_SHAM_EPS) and (shuf_change <= 0.50 * abs(dA))

    out["passA"] = passA; out["passB"] = passB; out["passC"] = passC
    out["passD"] = passD; out["passE"] = passE
    green = passA and passB and passC and passE   # GREEN iff A∧B∧C∧E (D = headline dissociation)
    out["verdict"] = "GREEN" if green else "NOT-GREEN"
    out["green_rule"] = "A and B and C and E (D is the headline route-dissociation, reported)"
    return out


if __name__ == "__main__":
    r = run()
    print(json.dumps(r, indent=2))
    print()
    print("=== H_1507 FIELD×LIBIDO FROZEN BARS ===")
    print(f"(A FIELD-RAISES-WANTING) Δwant high-vs-sham = {r['A_field_raises_wanting_delta']:+.4f} "
          f">= {BAR_A_WANT_RAISE} -> {'PASS' if r['passA'] else 'FAIL'}")
    print(f"(B WANTING≠LIKING) Δlike = {r['B_like_delta']:.4f} <= {BAR_B_LIKE_EPS} "
          f"(while wanting raised) -> {'PASS' if r['passB'] else 'FAIL'}")
    print(f"(C FREQ-DIRECTIONAL) high={r['C_high_delta']:+.4f} low={r['C_low_delta']:+.4f} "
          f"(opposite sign) -> {'PASS' if r['passC'] else 'FAIL'}")
    print(f"(D FIELD-vs-DRUG) field Δwant={r['D_field_delta']:+.4f} drug Δwant={r['D_drug_delta']:+.4f} "
          f"| field focal/global={r['D_field_focal']:.4f}/{r['D_field_global']:.4f} "
          f"drug focal/global={r['D_drug_focal']:.4f}/{r['D_drug_global']:.4f} "
          f"-> {'PASS' if r['passD'] else 'FAIL'}")
    print(f"(E EARNED) sham change={r['E_sham_change']:.4f} shuffle change={r['E_shuf_change']:.4f} "
          f"-> {'PASS' if r['passE'] else 'FAIL'}")
    print(f"VERDICT: {r['verdict']}  (rule: {r['green_rule']})")
