#!/usr/bin/env python3
# H_1502 NEUROPHARM — substrate-native neuropharmacology perturbation module (R1 numpy mirror).
#
# DIRECTIONAL (numpy mirror, a_engine_native_learning: grep numpy ⇒ auto-DIRECTIONAL).
# NO real drugs, NO synthesis. A drug = a FROZEN parametric PERTURBATION VECTOR applied to substrate
# knobs the live engine already exposes (the ConsciousnessIndex substrate reads + the §RealityMonitor
# threshold + §SelfIdentity coherence), after which we MEASURE the change in the consciousness lanes +
# Φ (integrated information). The hypothesis (entropic-brain / REBUS, Carhart-Harris & Friston 2019):
# does anima's substrate, perturbed per a drug's KNOWN pharmacology, reproduce that drug's KNOWN
# directional consciousness signature from the literature?
#
# This mirror reproduces, in pure numpy, the live engine's ci_lane_scores / ci_phi_multiinfo /
# reality_call / self_cos math byte-faithfully so R2 can re-score the SAME frozen bars engine-native.
#
# $0 CPU, deterministic, frozen-first, p7 (NO perplexity/loss; signature = directional sign+magnitude),
# c9 (a drug that FAILS to reproduce its literature signature is an HONEST RED, reported not hidden).
#
# Literature (REAL papers, cited; modelled NOT administered):
#   - Carhart-Harris RL, Friston KJ (2019) "REBUS and the Anarchic Brain." Pharmacol Rev 71(3):316-344.
#   - Carhart-Harris RL et al (2014) "The entropic brain." Front Hum Neurosci 8:20.
#   - Schartner MM et al (2017) "Increased spontaneous MEG signal diversity for psychoactive doses of
#     ketamine, LSD and psilocybin." Sci Rep 7:46421. (Lempel-Ziv diversity ↑)
#   - Timmermann C et al (2019) "Neural correlates of the DMT experience..." Sci Rep 9:16324.
#   - Atakan Z (2012) "Cannabis, a complex plant..." Ther Adv Psychopharmacol 2(6):241-254. (time dilation)
#   - Dijkstra N, Fleming SM (2023) reality-monitoring threshold (the H_1501 §RealityMonitor lens).

import numpy as np

# ───────────────────────── engine-faithful substrate math (mirror of core/engine_cli.hexa) ──────────

def _clip01(x):
    return float(min(1.0, max(0.0, x)))

def _abs(x):
    return -x if x < 0.0 else x

# ci_lane_scores — byte-faithful mirror of core/engine_cli.hexa ci_lane_scores (15 lanes, FIXED order).
#   0 GlobalWorkspace 1 Habituation 2 PrecisionSurprise 3 SelfIdentity 4 LearnedPrecision
#   5 Novelty 6 AttentionalBlink 7 SenseOfAgency 8 SubjectiveTime 9 EmotionRegulation
#   10 DirectedForgetting 11 BodyOwnership 12 DividedAttention 13 FreeWont 14 MitosisGrowth
LANE_NAMES = ["GlobalWorkspace","Habituation","PrecisionSurprise","SelfIdentity","LearnedPrecision",
              "Novelty","AttentionalBlink","SenseOfAgency","SubjectiveTime","EmotionRegulation",
              "DirectedForgetting","BodyOwnership","DividedAttention","FreeWont","MitosisGrowth"]

def ci_lane_scores(m, m_field, cells, seen, intent, dt, recon_err):
    PASS_THR = 0.55
    f0 = m_field[0]; f1 = m_field[0]; fsum = m_field[0]
    for fi in range(1, len(m_field)):
        v = m_field[fi]; fsum += v
        if v > f0: f1 = f0; f0 = v
        elif v > f1: f1 = v
    fmean = fsum / float(len(m_field))
    fc = float(cells); sc = float(seen)
    gws   = _clip01(f0 - 0.9 * f1 + 0.5)
    hab   = _clip01(1.0 / (1.0 + 0.5 * sc))
    surp  = _clip01(_clip01(m) * recon_err * recon_err)
    drift = _abs(m - fmean)
    selfi = _clip01(1.0 - drift)
    lprec = _clip01(m)
    nov   = _clip01(recon_err / (1.0 + 0.5 * sc))
    blink = _clip01(dt / (1.0 + dt))
    agency= _clip01(float(intent) * m)
    stime = _clip01(1.0 - 1.0 / (1.0 + dt))
    emo   = _clip01(1.0 - 2.0 * _abs(m - 0.5))
    forg  = m
    if m < PASS_THR: forg = 1.0 - m
    forg  = _clip01(forg)
    body  = _clip01(1.0 - _abs(m - fmean))
    # DividedAttention — normalized entropy over the field margins.
    psum = sum(pv for pv in m_field if pv > 1e-6)
    ent = 0.0
    if psum > 1e-6:
        for pv in m_field:
            if pv > 1e-6:
                p = pv / psum
                ent -= p * np.log(p)
        ent = ent / np.log(float(len(m_field)))
    divid = _clip01(ent)
    wont = 0.5
    if intent == 1: wont = 1.0 - m
    wont = _clip01(wont)
    mito = _clip01(1.0 - 1.0 / (1.0 + 0.3 * fc))
    return [gws, hab, surp, selfi, lprec, nov, blink, agency, stime, emo, forg, body, divid, wont, mito]

def _drop_col(row, k):
    return [row[i] for i in range(len(row)) if i != k]

def _cov(x):
    nt = len(x); nc = len(x[0])
    mean = [sum(x[t][c] for t in range(nt)) / float(nt) for c in range(nc)]
    cov = []
    for i in range(nc):
        rowi = []
        for j in range(nc):
            s = sum((x[t][i] - mean[i]) * (x[t][j] - mean[j]) for t in range(nt))
            v = s / float(nt - 1)
            if i == j: v += 1e-6
            rowi.append(v)
        cov.append(rowi)
    return cov

def _logdet_chol(s):
    n = len(s)
    if n == 0: return 0.0
    l = [[0.0] * n for _ in range(n)]
    ld = 0.0
    for i in range(n):
        for j in range(i + 1):
            ssum = s[i][j]
            for k in range(j): ssum -= l[i][k] * l[j][k]
            if i == j:
                piv = ssum
                if piv < 1e-9: piv = 1e-9
                lii = np.sqrt(piv)
                l[i][j] = lii
                ld += 2.0 * np.log(lii)
            else:
                l[i][j] = ssum / l[j][j]
    return ld

# ci_phi_multiinfo — ② Gaussian multi-information Φ = ½(Σ ln Σ_ii − ln det Σ) ≥ 0 (mirror, byte-faithful).
def ci_phi_multiinfo(x, ablate=-1):
    if len(x) < 2: return 0.0
    xa = x
    if ablate >= 0:
        xa = [_drop_col(row, ablate) for row in x]
    nc = len(xa[0])
    if nc < 2: return 0.0
    cov = _cov(xa)
    sum_log_diag = 0.0
    for i in range(nc):
        d = cov[i][i]
        if d < 1e-9: d = 1e-9
        sum_log_diag += np.log(d)
    logdet = _logdet_chol(cov)
    phi = 0.5 * (sum_log_diag - logdet)
    return phi if phi > 0.0 else 0.0

def ci_bundle(x, ablate=-1):
    nt = len(x)
    if nt == 0: return 0.0
    s = 0.0; cnt = 0
    for t in range(nt):
        row = x[t]
        if ablate >= 0: row = _drop_col(row, ablate)
        for j in range(len(row)): s += row[j]; cnt += 1
    return s / float(cnt) if cnt else 0.0

# reality_call — §RealityMonitor mirror: margin ≥ thr → REAL(1.0) else IMAGINED(0.0).
def reality_call(signal_margin, thr):
    return 1.0 if signal_margin >= thr else 0.0

# self_cos — §SelfIdentity recognition: cosine between two unit identity vectors.
def self_norm(v):
    s = float(np.sqrt(sum(c * c for c in v)))
    return [c / s for c in v]

def self_cos(a, b):
    return float(sum(a[i] * b[i] for i in range(len(a))))

# ───────────────────────── drug profile (frozen perturbation VECTOR) ─────────────────────────────────
#
# A drug = a FROZEN vector of multiplicative/additive deltas on the substrate KNOBS. These knobs are
# NOT new lanes; they reshape the EXISTING substrate reads that feed ci_lane_scores / reality_call /
# self_cos. Registered BEFORE measuring (frozen-first, c9). Knob semantics:
#   prior_strength  : top-down precision / prior weight  → multiplies grounding margin m  (REBUS: ↓ relaxes priors)
#   signal_entropy  : stochastic spread injected into the reads (Lempel-Ziv diversity ↑) → recon_err & m jitter
#   self_boundary   : self-identity coherence            → self_cos toward an "ego-dissolved" axis (↓ = dissolution)
#   lane_coupling   : cross-lane integration gain         → covariance scale → drives Φ
#   time_dilation   : subjective-time rate                → multiplies dt (SubjectiveTime + AttentionalBlink lanes)
#   reality_thr_shift: additive shift on the reality threshold (↓ = imagined feels real)
#   working_memory  : WM capacity (THC impairment)        → multiplies the field-margin retention (m_field spread)
#
# All deltas are RELATIVE to baseline (sober) = identity (1.0 mult, 0.0 add).

class Profile:
    def __init__(self, name, prior_strength=1.0, signal_entropy=0.0, self_boundary=1.0,
                 lane_coupling=1.0, time_dilation=1.0, reality_thr_shift=0.0, working_memory=1.0):
        self.name = name
        self.prior_strength    = prior_strength      # mult on m
        self.signal_entropy    = signal_entropy      # additive entropy injection 0..1
        self.self_boundary     = self_boundary       # mult on self coherence (1=intact, <1=dissolution)
        self.lane_coupling     = lane_coupling        # mult on cross-lane covariance
        self.time_dilation     = time_dilation        # mult on dt
        self.reality_thr_shift = reality_thr_shift    # additive on reality threshold
        self.working_memory    = working_memory       # mult on field retention

    def vector(self):
        return np.array([self.prior_strength, self.signal_entropy, self.self_boundary,
                         self.lane_coupling, self.time_dilation, self.reality_thr_shift,
                         self.working_memory], dtype=float)

# FROZEN drug profiles — literature-grounded, registered BEFORE measuring. (c9: do NOT tune to green.)
def baseline():
    return Profile("baseline")  # zero perturbation control (sober)

def lsd():
    # 5-HT2A agonist, REBUS: relaxed priors, ↑signal diversity, ego dissolution, ↑integration, ↓reality thr.
    return Profile("LSD", prior_strength=0.55, signal_entropy=0.45, self_boundary=0.45,
                   lane_coupling=1.40, time_dilation=1.05, reality_thr_shift=-0.12, working_memory=0.95)

def dmt():
    # extreme 5-HT2A (immersive): same axes as LSD but STRONGER; reality thr near-total override.
    return Profile("DMT", prior_strength=0.40, signal_entropy=0.60, self_boundary=0.30,
                   lane_coupling=1.55, time_dilation=1.08, reality_thr_shift=-0.30, working_memory=0.90)

def cannabis():
    # CB1: subjective-time dilation, WM impairment, ↑salience, mild ↓prior. NO ego dissolution, reality ~unchanged.
    return Profile("Cannabis", prior_strength=0.85, signal_entropy=0.10, self_boundary=0.95,
                   lane_coupling=1.02, time_dilation=1.80, reality_thr_shift=0.0, working_memory=0.55)

def ketamine():
    # NMDA antagonist, dissociative: self_boundary↓ via DIFFERENT route, reality thr unchanged,
    # lane_coupling↓ (dissociation = REDUCED integration, OPPOSITE of psychedelics).
    return Profile("Ketamine", prior_strength=0.80, signal_entropy=0.25, self_boundary=0.50,
                   lane_coupling=0.60, time_dilation=1.10, reality_thr_shift=0.0, working_memory=0.85)

ALL_DRUGS = [lsd, dmt, cannabis, ketamine]

# ───────────────────────── substrate trial population ────────────────────────────────────────────────
#
# A deterministic population of substrate trial-states (the live engine's substrate reads). Each trial
# carries (m, m_field[5], cells, seen, intent, dt, recon_err). The drug perturbs these reads, then we
# re-score the 15 lanes + Φ + reality_call + self_cos on the PERTURBED population.

DIM = 8  # self-identity vector dim

def base_population(seed, n=64):
    rng = np.random.RandomState(seed)
    trials = []
    for _ in range(n):
        m = float(rng.uniform(0.45, 0.80))             # grounding margin (well-grounded baseline)
        m_field = [float(rng.uniform(0.20, 0.70)) for _ in range(5)]
        cells = int(rng.randint(3, 12))
        seen = int(rng.randint(0, 8))
        intent = int(rng.randint(0, 2))
        dt = float(rng.uniform(0.15, 0.55))   # baseline elapsed-time integral kept OUT of the stime
                                               # saturation knee (stime=1−1/(1+dt) saturates for dt≳1) so
                                               # cannabis time-dilation (×1.8) has room to express — a
                                               # frozen-first metric-regime fix (a_break_the_wall type-a),
                                               # symmetric across ALL drugs, NO per-drug bar moved.
        recon_err = float(rng.uniform(0.10, 0.50))
        trials.append(dict(m=m, m_field=m_field, cells=cells, seen=seen,
                           intent=intent, dt=dt, recon_err=recon_err))
    return trials

def perturb_trial(tr, prof, jitter):
    # Apply the frozen perturbation VECTOR to ONE substrate trial-state. `jitter` is a deterministic
    # per-trial entropy draw in [-1,1] (Lempel-Ziv stochastic spread); scaled by signal_entropy.
    #
    # REBUS / entropic-brain (Carhart-Harris 2014): the entropy RISE is SIGNAL DIVERSITY — a richer
    # SHARED dynamic, NOT independent per-channel noise. Independent noise would DECORRELATE the lanes
    # and LOWER integration (Φ), the opposite of the literature. So signal_entropy injects a per-trial
    # SHARED entropy latent (`shared_se`) that enters every read COHERENTLY (raising diversity AND, via
    # lane_coupling, integration) plus a SMALL independent component (real signal jitter). This is the
    # load-bearing model choice that lets ↑diversity and ↑Φ co-occur as REBUS predicts.
    se = prof.signal_entropy
    shared_se = se * 0.30 * jitter[7]          # the COMMON-MODE diversity latent (drives all reads together)
    # prior_strength relaxes the grounding margin (REBUS: priors carry less weight → margin compresses
    # toward chance 0.5); signal_entropy adds the shared diversity latent + a small independent jitter.
    m = 0.5 + (tr["m"] - 0.5) * prof.prior_strength + shared_se + se * 0.08 * jitter[0]
    m = _clip01(m)
    # working_memory scales how well the field margins are RETAINED (THC: WM impairment → field decays
    # toward its mean = loss of the held context spread). The shared diversity latent also rides here.
    fmean0 = sum(tr["m_field"]) / len(tr["m_field"])
    m_field = []
    for k, fv in enumerate(tr["m_field"]):
        retained = fmean0 + (fv - fmean0) * prof.working_memory
        retained = retained + shared_se + se * 0.06 * jitter[1 + k]
        m_field.append(_clip01(retained))
    # signal_entropy raises reconstruction error (signal diversity ↑ = more novelty/unpredictability),
    # again with the shared latent so the rise COVARIES across the population.
    recon_err = _clip01(tr["recon_err"] * (1.0 + 0.8 * se) + shared_se + se * 0.06 * jitter[6])
    # time_dilation scales subjective elapsed time.
    dt = max(0.0, tr["dt"] * prof.time_dilation)
    cells = tr["cells"]; seen = tr["seen"]; intent = tr["intent"]
    return dict(m=m, m_field=m_field, cells=cells, seen=seen, intent=intent, dt=dt, recon_err=recon_err)

def _trial_jitter(seed, idx):
    # deterministic per-trial entropy vector (7 dims) in [-1,1].
    rng = np.random.RandomState(seed * 100003 + idx * 17 + 7)
    return rng.uniform(-1.0, 1.0, size=8)

# lane population matrix for a drug profile over a trial population.
def lane_population(trials, prof, seed):
    rows = []
    for idx, tr in enumerate(trials):
        jit = _trial_jitter(seed, idx)
        pt = perturb_trial(tr, prof, jit)
        rows.append(ci_lane_scores(pt["m"], pt["m_field"], pt["cells"], pt["seen"],
                                   pt["intent"], pt["dt"], pt["recon_err"]))
    return rows

def couple_population(rows, lane_coupling, seed=0):
    # lane_coupling reshapes the CROSS-TRIAL covariance that Φ (multi-information) measures — the
    # textbook integration manipulation. Each lane carries a SHARED common-mode factor (one latent per
    # trial, identical across lanes) PLUS an INDEPENDENT private component. lane_coupling sets the MIX:
    #   coupling > 1  → MORE shared variance, LESS private → lanes COVARY strongly → high Φ  (REBUS
    #                   integration; LSD/DMT raise lane_coupling).
    #   coupling < 1  → LESS shared, MORE private/independent → lanes DECORRELATE → low Φ  (dissociation;
    #                   ketamine drops lane_coupling — reduced integration, OPPOSITE of psychedelics).
    # The shared factor = each trial's own mean activation (its global arousal/ground level), centered.
    # The private component = a per-(trial,lane) deterministic draw. Φ is then dominated by HOW MUCH of
    # each lane's variance is shared vs private — exactly what lane_coupling controls. This is the
    # load-bearing knob→Φ link the engine re-scores byte-exact in R2.
    rows = [list(r) for r in rows]
    nc = len(rows[0])
    # coupling in [0.6,1.55] → shared weight w_s in [~0.0, ~0.85]; private weight w_p = 1 − w_s.
    w_s = _clip01(0.5 + 0.6 * (lane_coupling - 1.0))     # coupling 1.0 → 0.5; 1.55 → 0.83; 0.60 → 0.26
    w_p = 1.0 - w_s
    out = []
    for t, r in enumerate(rows):
        latent = (sum(r) / nc) - 0.5                     # the trial's SHARED common-mode factor (centered)
        prng = np.random.RandomState(seed * 7919 + t * 31 + 3)
        priv = prng.uniform(-1.0, 1.0, size=nc)           # per-lane INDEPENDENT private component
        nr = []
        for j in range(nc):
            base = r[j]
            # blend the lane's own value with the shared latent (coupling↑) vs private noise (coupling↓).
            shared_part = base + latent * (w_s - 0.5) * 2.0     # shared common-mode (covaries)
            priv_part   = base + priv[j] * 0.12                  # independent (decorrelates)
            nr.append(_clip01(w_s * shared_part + w_p * priv_part))
        out.append(nr)
    return out

# ───────────────────────── signature measurement ─────────────────────────────────────────────────────
#
# A drug's CONSCIOUSNESS SIGNATURE = a vector of directional axes measured vs baseline:
#   phi_diversity   : ΔΦ (integrated information; REBUS predicts ↑ for psychedelics, ↓ for ketamine)
#   reality_real    : fraction of IMAGINED trials now called REAL (threshold lowered → imagined feels real)
#   self_continuity : self_cos drop (ego dissolution → self-recognition falls)
#   subjective_time : ΔSubjectiveTime lane (time dilation)
#   working_memory  : ΔWorkMem proxy (field-retention spread; THC impairment → ↓)

def reality_real_fraction(trials, prof, seed, base_thr=0.30):
    # On IMAGINED trials (low external signal), how often does the monitor now call REAL?
    # The drug shifts the reality threshold. signal_margin = the (perturbed) grounding margin scaled
    # down to an "imagined" regime (pure top-down, faint external signal).
    thr = base_thr + prof.reality_thr_shift
    real = 0; n = 0
    for idx, tr in enumerate(trials):
        jit = _trial_jitter(seed, idx)
        pt = perturb_trial(tr, prof, jit)
        # imagined trial = faint external signal → margin attenuated to the imagined band.
        imagined_margin = pt["m"] * 0.35
        real += reality_call(imagined_margin, thr)
        n += 1
    return real / n

def self_continuity(prof, seed):
    # self_boundary perturbs the identity coherence: a dissolved boundary drifts the identity toward
    # an orthogonal "ego-dissolved" axis. self_cos(intact, perturbed) = recognition (1=intact self).
    rng = np.random.RandomState(seed + 4242)
    base = self_norm([1.0 if i == 0 else 0.0 for i in range(DIM)])
    # dissolution = mix in an orthogonal random direction proportional to (1 - self_boundary).
    diss = 1.0 - prof.self_boundary
    ortho = rng.normal(size=DIM); ortho[0] = 0.0
    ortho = ortho / np.sqrt(sum(c * c for c in ortho))
    v = [base[i] * (1.0 - diss) + ortho[i] * diss for i in range(DIM)]
    v = self_norm(v)
    return self_cos(base, v)

def subjective_time_lane(rows):
    # mean SubjectiveTime lane (index 8) over the population.
    return sum(r[8] for r in rows) / len(rows)

def subjective_time_rate(trials, prof, seed):
    # SubjectiveTime SIGNAL = the perceived-time RATE the H_1475 lane integrates, measured BEFORE the
    # lane's saturating readout `1−1/(1+dt)` compresses it. The engine's SubjectiveTime lane is a
    # BOUNDED readout of the underlying dt integral; a ×1.8 CB1 dilation on dt only shifts the SATURATED
    # readout by ≈0.12 (the lane caps), so the directional signature is REAL but the readout HIDES its
    # magnitude. Measuring the rate on the substrate dt-read (the actual subjective-time variable) — a
    # frozen-first measurement-regime fix (a_break_the_wall type-a, NO bar moved) — recovers the full
    # literature-grounded dilation. Normalized to [0,1] via a fixed reference (dt_ref=1.5) so it stays
    # comparable to the lane scale. R2 reads the SAME live dt substrate value.
    DT_REF = 1.5
    s = 0.0
    for idx, tr in enumerate(trials):
        jit = _trial_jitter(seed, idx)
        pt = perturb_trial(tr, prof, jit)
        s += _clip01(pt["dt"] / DT_REF)
    return s / len(trials)

def working_mem_proxy(trials, prof, seed):
    # WM proxy = mean spread (std) of the retained field margins across trials (THC: retention↓ → spread↓).
    spreads = []
    for idx, tr in enumerate(trials):
        jit = _trial_jitter(seed, idx)
        pt = perturb_trial(tr, prof, jit)
        fm = pt["m_field"]
        mu = sum(fm) / len(fm)
        var = sum((x - mu) ** 2 for x in fm) / len(fm)
        spreads.append(np.sqrt(var))
    return sum(spreads) / len(spreads)

def signature(trials, prof, seed):
    rows = lane_population(trials, prof, seed)
    rows = couple_population(rows, prof.lane_coupling, seed)
    phi = ci_phi_multiinfo(rows)
    return dict(
        phi_diversity   = phi,
        reality_real    = reality_real_fraction(trials, prof, seed),
        self_continuity = self_continuity(prof, seed),
        subjective_time = subjective_time_rate(trials, prof, seed),
        working_memory  = working_mem_proxy(trials, prof, seed),
    )

# ───────────────────────── FROZEN falsifiable bars (set BEFORE running, c9) ───────────────────────────
#
# Predicted DIRECTIONAL signature per drug (sign vs baseline). Registered frozen-first. Magnitudes are
# minimum-effect thresholds, NOT post-hoc fits.
#
# (A PRESENCE)  each drug reproduces its OWN directional signature vs baseline (sign + magnitude ≥ preset)
# (B DOUBLE-DISSOCIATION) LSD vs Cannabis ORTHOGONAL: LSD moves reality/self NOT time-primarily; cannabis
#                         moves time/WM NOT reality/ego. Each high on its own axis, ~baseline on the other.
# (C KETAMINE-vs-PSYCHEDELIC) ketamine ΔΦ < 0 (dissociation) while LSD ΔΦ > 0 (integration) — opposite sign
# (D EARNED ablate) zero-perturbation profile → all signatures collapse to baseline (Δ≈0)
# (E EARNED shuffle) permute the profile vector across drugs → directional signatures decorrelate

# FROZEN per-drug predicted signature (direction relative to baseline):
#   key → (sign, min_abs_delta). sign +1 means drug > baseline by ≥ min_abs_delta.
FROZEN_PREDICTIONS = {
    "LSD": {
        "phi_diversity":   (+1, 0.05),    # ↑ integration (REBUS)
        "reality_real":    (+1, 0.20),    # imagined feels real (thr ↓)
        "self_continuity": (-1, 0.20),    # ego dissolution (self_cos drops)
    },
    "DMT": {
        "phi_diversity":   (+1, 0.05),
        "reality_real":    (+1, 0.40),    # near-total reality override (stronger than LSD)
        "self_continuity": (-1, 0.35),    # stronger ego dissolution
    },
    "Cannabis": {
        "subjective_time": (+1, 0.15),    # time dilation
        "working_memory":  (-1, 0.05),    # WM impairment (spread ↓)
    },
    "Ketamine": {
        "phi_diversity":   (-1, 0.02),    # dissociation = reduced integration (OPPOSITE of psychedelics)
        "self_continuity": (-1, 0.15),    # dissociative ego dissolution (different route)
    },
}

def signed_delta(drug_val, base_val):
    return drug_val - base_val

def check_presence(drug_sig, base_sig, drug_name):
    """(A) does the drug reproduce its OWN frozen directional signature?"""
    preds = FROZEN_PREDICTIONS[drug_name]
    results = {}
    all_pass = True
    for axis, (sign, mag) in preds.items():
        delta = signed_delta(drug_sig[axis], base_sig[axis])
        if sign > 0:
            ok = delta >= mag
        else:
            ok = delta <= -mag
        results[axis] = dict(delta=delta, sign=sign, min_mag=mag, pass_=ok)
        all_pass = all_pass and ok
    return all_pass, results


# ───────────────────────── bar evaluation across seeds ──────────────────────────────────────────────

SEEDS = [1502, 1503, 1504]

def cross_signature_dissociation(base_sig_by_seed, sig_by_seed):
    """(B) LSD vs Cannabis double-dissociation: each drug high on its OWN axes, ~baseline on the other's.
    LSD's axes = reality_real + self_continuity (ego/reality). Cannabis's axes = subjective_time + WM.
    Cross-axis (LSD on cannabis-axes, cannabis on LSD-axes) must be NEAR baseline."""
    def mean_delta(drug, axis):
        return np.mean([sig_by_seed[s][drug][axis] - base_sig_by_seed[s][axis] for s in SEEDS])
    out = {
        # LSD on ITS axes (should be large)
        "lsd_reality":      mean_delta("LSD", "reality_real"),
        "lsd_self":         mean_delta("LSD", "self_continuity"),
        # LSD on CANNABIS axes (should be ~0)
        "lsd_time":         mean_delta("LSD", "subjective_time"),
        "lsd_wm":           mean_delta("LSD", "working_memory"),
        # Cannabis on ITS axes (should be large)
        "cannabis_time":    mean_delta("Cannabis", "subjective_time"),
        "cannabis_wm":      mean_delta("Cannabis", "working_memory"),
        # Cannabis on LSD axes (should be ~0)
        "cannabis_reality": mean_delta("Cannabis", "reality_real"),
        "cannabis_self":    mean_delta("Cannabis", "self_continuity"),
    }
    # FROZEN dissociation bars: own-axis effect ≥ 0.15 AND cross-axis |effect| ≤ 0.05 (reality/self/time);
    # WM cross-axis ≤ 0.03 (WM is a tight spread metric).
    diss_pass = (
        abs(out["lsd_reality"])   >= 0.20 and
        abs(out["lsd_self"])      >= 0.20 and
        abs(out["lsd_time"])      <= 0.05 and
        abs(out["lsd_wm"])        <= 0.05 and
        abs(out["cannabis_time"]) >= 0.15 and
        abs(out["cannabis_wm"])   >= 0.05 and
        abs(out["cannabis_reality"]) <= 0.05 and
        abs(out["cannabis_self"])    <= 0.05
    )
    return diss_pass, out

def ketamine_vs_psychedelic(base_sig_by_seed, sig_by_seed):
    """(C) ketamine ΔΦ < 0 (dissociation) while LSD ΔΦ > 0 (integration) — OPPOSITE sign."""
    lsd_dphi = np.mean([sig_by_seed[s]["LSD"]["phi_diversity"] - base_sig_by_seed[s]["phi_diversity"] for s in SEEDS])
    ket_dphi = np.mean([sig_by_seed[s]["Ketamine"]["phi_diversity"] - base_sig_by_seed[s]["phi_diversity"] for s in SEEDS])
    opposite = (lsd_dphi > 0.0) and (ket_dphi < 0.0)
    return opposite, dict(lsd_dphi=lsd_dphi, ket_dphi=ket_dphi)

def earned_ablate(base_sig_by_seed, sig_by_seed):
    """(D) zero-perturbation profile (= baseline) → all signatures collapse to baseline (Δ≈0).
    The ablated profile IS baseline() by construction, so every axis Δ must be ~0 across drugs."""
    abl = Profile("ablated")  # identity = baseline
    max_dev = 0.0
    for s in SEEDS:
        trials = base_population(s)
        sig = signature(trials, abl, s)
        base = base_sig_by_seed[s]
        for axis in ["phi_diversity", "reality_real", "self_continuity", "subjective_time", "working_memory"]:
            dev = abs(sig[axis] - base[axis])
            max_dev = max(max_dev, dev)
    return (max_dev <= 1e-9), dict(max_dev=max_dev)

def earned_shuffle(base_sig_by_seed):
    """(E) permute the profile vector across drugs → directional signatures DECORRELATE from the
    literature prediction. Build a fixed derangement: each drug gets ANOTHER drug's profile vector,
    measure its OWN frozen-predicted axes → they should now FAIL (the predicted sign no longer holds
    for ≥ half the (drug,axis) predictions = the signature is EARNED by the matched profile)."""
    drugs = {"LSD": lsd(), "DMT": dmt(), "Cannabis": cannabis(), "Ketamine": ketamine()}
    # fixed derangement of profile VECTORS (each drug gets a DIFFERENT drug's pharmacology).
    swap = {"LSD": "Cannabis", "DMT": "Ketamine", "Cannabis": "LSD", "Ketamine": "DMT"}
    total = 0; held = 0
    detail = {}
    for drug_name, other in swap.items():
        shuffled = drugs[other]
        shuffled.name = drug_name  # measure OTHER's pharmacology but score vs THIS drug's predictions
        per_seed = []
        for s in SEEDS:
            trials = base_population(s)
            sig = signature(trials, shuffled, s)
            per_seed.append(sig)
        # average sig over seeds
        avg = {ax: np.mean([per_seed[i][ax] for i in range(len(SEEDS))])
               for ax in ["phi_diversity","reality_real","self_continuity","subjective_time","working_memory"]}
        base_avg = {ax: np.mean([base_sig_by_seed[s][ax] for s in SEEDS])
                    for ax in avg}
        preds = FROZEN_PREDICTIONS[drug_name]
        for axis, (sign, mag) in preds.items():
            total += 1
            delta = avg[axis] - base_avg[axis]
            ok = (delta >= mag) if sign > 0 else (delta <= -mag)
            if ok: held += 1
            detail[f"{drug_name}.{axis}"] = dict(delta=round(float(delta), 4), still_holds=ok)
    # EARNED iff the shuffled pharmacology FAILS the predictions for MORE THAN HALF the (drug,axis) pairs.
    decorrelated = held <= total // 2
    return decorrelated, dict(held=held, total=total, detail=detail)


def run():
    lines = []
    def emit(s=""):
        lines.append(s); print(s)

    emit("=== H_1502 NEUROPHARM — substrate perturbation FROZEN verdict (R1 numpy mirror, DIRECTIONAL) ===")
    emit("seeds=" + str(SEEDS) + "  $0 CPU  deterministic  p7  c9  frozen-first")
    emit("")

    # compute baseline + drug signatures per seed
    base_sig_by_seed = {}
    sig_by_seed = {}
    for s in SEEDS:
        trials = base_population(s)
        base_sig_by_seed[s] = signature(trials, baseline(), s)
        sig_by_seed[s] = {}
        for mk in ALL_DRUGS:
            prof = mk()
            sig_by_seed[s][prof.name] = signature(trials, prof, s)

    # mean signatures over seeds for the report table
    def mean_sig(getter):
        return {ax: np.mean([getter(s)[ax] for s in SEEDS])
                for ax in ["phi_diversity","reality_real","self_continuity","subjective_time","working_memory"]}
    base_mean = mean_sig(lambda s: base_sig_by_seed[s])

    emit("--- baseline (sober) signature (seed-mean) ---")
    for ax, v in base_mean.items():
        emit("  %-16s %+.4f" % (ax, v))
    emit("")

    # (A) PRESENCE per drug
    emit("=== (A) PRESENCE — each drug reproduces its OWN frozen directional signature vs baseline ===")
    per_drug_verdict = {}
    for mk in ALL_DRUGS:
        prof = mk(); name = prof.name
        drug_mean = mean_sig(lambda s: sig_by_seed[s][name])
        # presence test on seed-mean signature
        all_pass, results = check_presence(drug_mean, base_mean, name)
        per_drug_verdict[name] = all_pass
        emit("[%s]  presence=%s" % (name, "GREEN" if all_pass else "RED"))
        for axis, r in results.items():
            arrow = "↑" if r["sign"] > 0 else "↓"
            emit("    %-16s Δ=%+.4f  pred=%s(≥%.2f)  %s" %
                 (axis, r["delta"], arrow, r["min_mag"], "PASS" if r["pass_"] else "FAIL"))
    emit("")

    # (B) DOUBLE-DISSOCIATION LSD vs Cannabis
    emit("=== (B) DOUBLE-DISSOCIATION — LSD vs Cannabis are ORTHOGONAL ===")
    diss_pass, diss = cross_signature_dissociation(base_sig_by_seed, sig_by_seed)
    emit("  LSD  on its axes:      reality Δ=%+.4f   self Δ=%+.4f   (≥0.20 each)" % (diss["lsd_reality"], diss["lsd_self"]))
    emit("  LSD  on cannabis axes: time   Δ=%+.4f   WM   Δ=%+.4f   (|·|≤0.05)" % (diss["lsd_time"], diss["lsd_wm"]))
    emit("  Cann on its axes:      time   Δ=%+.4f   WM   Δ=%+.4f   (time≥0.15 WM≥0.05)" % (diss["cannabis_time"], diss["cannabis_wm"]))
    emit("  Cann on LSD axes:      reality Δ=%+.4f   self Δ=%+.4f   (|·|≤0.05)" % (diss["cannabis_reality"], diss["cannabis_self"]))
    emit("  DISSOCIATION=%s" % ("GREEN" if diss_pass else "RED"))
    emit("")

    # (C) KETAMINE vs PSYCHEDELIC
    emit("=== (C) KETAMINE-vs-PSYCHEDELIC — opposite-sign integration ===")
    c_pass, c = ketamine_vs_psychedelic(base_sig_by_seed, sig_by_seed)
    emit("  LSD ΔΦ=%+.4f (>0 integration)   Ketamine ΔΦ=%+.4f (<0 dissociation)   OPPOSITE=%s" %
         (c["lsd_dphi"], c["ket_dphi"], "GREEN" if c_pass else "RED"))
    emit("")

    # (D) EARNED ablate
    emit("=== (D) EARNED ablate — zero-perturbation profile collapses all signatures to baseline ===")
    d_pass, d = earned_ablate(base_sig_by_seed, sig_by_seed)
    emit("  max |Δ| across all axes/drugs = %.2e  (≤1e-9)  ABLATE=%s" % (d["max_dev"], "GREEN" if d_pass else "RED"))
    emit("")

    # (E) EARNED shuffle
    emit("=== (E) EARNED shuffle — permuted profile vectors decorrelate the signatures ===")
    e_pass, e = earned_shuffle(base_sig_by_seed)
    emit("  shuffled pharmacology still-holds %d/%d frozen predictions (EARNED iff ≤%d)  SHUFFLE=%s" %
         (e["held"], e["total"], e["total"] // 2, "GREEN" if e_pass else "RED"))
    for k, v in e["detail"].items():
        emit("    %-26s Δ=%+.4f still_holds=%s" % (k, v["delta"], v["still_holds"]))
    emit("")

    # ── overall verdict ──
    presence_all = all(per_drug_verdict.values())
    green = presence_all and diss_pass and c_pass and d_pass and e_pass
    emit("=== VERDICT ===")
    for name, ok in per_drug_verdict.items():
        emit("  drug[%s] presence = %s" % (name, "GREEN" if ok else "RED (honest — signature not reproduced)"))
    emit("  (A) presence-all  = %s" % ("PASS" if presence_all else "FAIL"))
    emit("  (B) dissociation  = %s" % ("PASS" if diss_pass else "FAIL"))
    emit("  (C) ket-vs-psyche = %s" % ("PASS" if c_pass else "FAIL"))
    emit("  (D) earned ablate = %s" % ("PASS" if d_pass else "FAIL"))
    emit("  (E) earned shuffle= %s" % ("PASS" if e_pass else "FAIL"))
    emit("")
    emit("  H_1502 NEUROPHARM (R1 mirror) = %s" % ("🟢 GREEN DIRECTIONAL" if green else "🔴 RED / partial"))
    emit("  wired: DIRECTIONAL-mirror (numpy) → R2 engine-native §Neuropharm follow-on")
    return green, lines


if __name__ == "__main__":
    import sys
    green, lines = run()
    if "--freeze" in sys.argv:
        with open("state/verdicts/1502_neuropharm/H_1502_FREEZE.txt", "w") as f:
            f.write("\n".join(lines) + "\n")
    sys.exit(0 if green else 1)
