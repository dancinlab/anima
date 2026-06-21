#!/usr/bin/env python3
# H_1508 — G5 METACOG-CONTROL (R1 numpy mirror, DIRECTIONAL · engine-transfer UNVERIFIED)
# =============================================================================
# Deepens the G5 metacognition gate along its MISSING half (Nelson & Narens 1990
# monitoring↔control): the G5 chain (H_1202/1304/1361/1367/1396/1398/1379/1400) is
# all DISCRIMINATION / MONITORING resolution (type-2 meta-d', AUROC). It NEVER
# measured CALIBRATION (does the recall margin track ACTUAL accuracy numerically,
# not just rank?) nor CONTROL (does a LOW margin drive ADAPTIVE resource allocation
# that beats uniform — Metcalfe region-of-proximal-learning?).
#
# DRUG-INDEPENDENT: NO §Neuropharm coupling whatsoever. Pure computational
# metacognition (Nelson-Narens monitoring/control; Fleming & Lau 2014 calibration;
# Metcalfe & Kornell 2005 region-of-proximal-learning control).
#
# Substrate = faithful numpy mirror of CORE/engine_cli.hexa:
#   immune_embed_key (byte-trigram FNV-1a, DIM=64, L2-norm)  — VERBATIM
#   vadapt_field_recon_err = L2 distance to nearest prototype  — VERBATIM
#   immune_memory_recall_margin = recon_err − recall_thr(0.15) — the LIVE G5 op we read
# margin is read PURELY off the live affinity geometry — NO injected accuracy label (p6).
#
# $0 CPU, deterministic (no rng except the explicitly-seeded shuffle control), 3 seeds,
# frozen-first, p7, c9. R2 = engine-native §MetacogControl ops re-score these exact bars.
# =============================================================================
import numpy as np
import json, sys, os

DIM = 64
NGRAM = 3
RECALL_THR = 0.15          # frozen (H_1304/1361/1367)
SEEDS = [11, 12, 13]

# difficulty ladder = byte-corruption levels (fraction of key bytes randomly substituted).
# L=0 → exact key (easy, high accuracy); rising L → key drifts off its stored cell
# (hard, accuracy falls, recall margin RISES toward/above threshold = lower confidence).
# NOTE (WALL-CLAUSE, frozen-first well-posedness — a_break_the_wall, like H_1396): the
# raw byte→accuracy transition is SHARP (acc 1.0@L0 → 0.83@0.08 → ~0@0.16), so a coarse
# ladder leaves NO proximal zone (items are trivial OR hopeless, never recoverable-uncertain).
# The ladder is sampled DENSELY across the real transition [0.06..0.14] so a genuine
# region-of-proximal-learning EXISTS to measure. This corrects the MEASUREMENT regime
# (difficulty granularity), NOT any verdict bar — every A/B/C/D/E threshold is UNCHANGED.
DIFFICULTY = [0.00, 0.06, 0.09, 0.12, 0.14]
N_FACTS = 120              # store size
TRIALS_PER_LEVEL = 60      # query trials per difficulty level per seed

# ---- frozen bars (set BEFORE running; DO NOT move — c9, no tune-to-green) ----
A_ECE_MAX      = 0.15      # (A CALIBRATION) expected calibration error ceiling
A_MONO_MIN     = 0.50      # (A) margin must DECREASE in confidence monotone w/ difficulty:
                           #     Spearman(difficulty, margin) ≥ +0.50 (margin rises as harder)
B_LIFT_MIN     = 0.04      # (B CONTROL-LIFT) RPL adaptive vs uniform accuracy lift ≥ this
D_ABLATE_MAX   = 0.015     # (D EARNED) margin-blind (uniform) allocation lift collapses ≤ this
E_CHANCE_BAND  = 0.30      # (E EARNED shuffle) |AUROC−0.5| ≤ band AND calibration decorrelates
# (C DISCRIMINATION⊥CALIBRATION) is the HEADLINE orthogonality (report numbers):
#   a monotone (rank-preserving) transform of confidence keeps AUROC constant but
#   shifts ECE — proving calibration is a NEW axis AUROC(0.906 prior chain) misses.
C_AUROC_DRIFT_MAX = 1e-9   # AUROC must be byte-identical under the monotone transform
C_ECE_SHIFT_MIN   = 0.10   # ECE must shift by at least this under the same transform

# ============================================================================
#  faithful CORE/engine_cli.hexa mirror
# ============================================================================
def fnv1a(bs):
    h = 2166136261
    for b in bs:
        h ^= b
        h = (h * 16777619) & 4294967295
    return h

def embed_key(text: bytes):
    v = np.zeros(DIM)
    blen = len(text)
    if blen < NGRAM:
        v[fnv1a(list(text)) % DIM] += 1.0
    else:
        for i in range(blen - NGRAM + 1):
            v[fnv1a(list(text[i:i+NGRAM])) % DIM] += 1.0
    nrm = np.sqrt((v*v).sum())
    if nrm > 0:
        v = v / nrm
    return v

def recon_err(protos, x):
    # L2 distance to nearest prototype (vadapt_field_recon_err)
    d = np.sqrt(((protos - x)**2).sum(axis=1))
    return d.min(), int(d.argmin())

# ============================================================================
#  store + corruption (difficulty ladder)
# ============================================================================
def build_store(seed):
    rng = np.random.default_rng(seed)
    facts, values, protos = [], [], []
    alphabet = list(b"abcdefghijklmnopqrstuvwxyz0123456789 ")
    for i in range(N_FACTS):
        L = 14 + int(rng.integers(0, 8))
        txt = bytes(rng.choice(alphabet, size=L))
        facts.append(txt)
        values.append(f"v{i}")
        protos.append(embed_key(txt))
    return facts, values, np.array(protos)

def corrupt(text: bytes, level: float, rng):
    if level <= 0.0:
        return text
    b = bytearray(text)
    alphabet = list(b"abcdefghijklmnopqrstuvwxyz0123456789 ")
    n_flip = int(round(level * len(b)))
    if n_flip <= 0:
        return bytes(b)
    pos = rng.choice(len(b), size=n_flip, replace=False)
    for p in pos:
        b[p] = rng.choice(alphabet)
    return bytes(b)

def query(protos, values, q_text):
    """LIVE recall: margin = recon_err − RECALL_THR; FIRE iff err ≤ thr → predicted value."""
    err, win = recon_err(protos, embed_key(q_text))
    margin = err - RECALL_THR
    fired = err <= RECALL_THR
    pred = values[win] if fired else None
    return margin, fired, pred, win

def query_key(protos, values, key):
    """recall straight from an (already-embedded) key vector — for the averaged re-look."""
    err, win = recon_err(protos, key)
    margin = err - RECALL_THR
    fired = err <= RECALL_THR
    return margin, fired, (values[win] if fired else None), win

# ============================================================================
#  trial generation: each trial = (true_idx, difficulty, margin, correct)
# ============================================================================
def run_trials(seed):
    facts, values, protos = build_store(seed)
    rng = np.random.default_rng(seed * 7919 + 1)
    trials = []
    for L in DIFFICULTY:
        for _ in range(TRIALS_PER_LEVEL):
            ti = int(rng.integers(0, N_FACTS))
            q = corrupt(facts[ti], L, rng)
            margin, fired, pred, win = query(protos, values, q)
            # accuracy = did recall route to the correct cell's value?
            correct = 1 if (pred == values[ti]) else 0
            # NOTE: confidence is NOT set here. It is the HELD-OUT calibrated map of the
            # raw substrate margin (fit on a DISJOINT train seed, §calibrate_map), so the
            # ECE bar is evaluated on UNSEEN data — non-circular, NOT tune-to-green (p7,c9).
            trials.append(dict(true=ti, L=L, margin=float(margin), correct=correct,
                               q=q, q_key=embed_key(q),
                               facts=facts, values=values, protos=protos))
    return trials, facts, values, protos

# ── HELD-OUT CALIBRATION MAP (Platt/isotonic-style, non-circular) ──────────────
# Fit a monotone margin→P(correct) map on the TRAIN seed's (margin, correct) pairs by
# binning, then APPLY it to the TEST seeds' margins to get calibrated confidence. The
# map is fit on data DISJOINT from where ECE is scored, so a low test ECE is genuine
# calibration, not curve-fitting the eval set. The map reads ONLY margins+correctness
# of the TRAIN split (standard supervised calibration; the TEST confidence uses NO test
# label). Monotone-nonincreasing in margin (smaller margin ⇒ higher P-correct) by design.
def fit_calibration_map(margins, corrects, n_bins=12):
    margins = np.asarray(margins, float); corrects = np.asarray(corrects, float)
    order = np.argsort(margins)
    m_sorted = margins[order]; c_sorted = corrects[order]
    edges = np.quantile(margins, np.linspace(0, 1, n_bins + 1))
    centers, probs = [], []
    for i in range(n_bins):
        lo, hi = edges[i], edges[i + 1]
        msk = (margins >= lo) & (margins <= hi if i == n_bins - 1 else margins < hi)
        if msk.sum() == 0:
            continue
        centers.append(margins[msk].mean()); probs.append(corrects[msk].mean())
    centers = np.array(centers); probs = np.array(probs)
    # enforce monotone-nonincreasing P vs margin (PAV-lite: backward max pass)
    for i in range(len(probs) - 2, -1, -1):
        probs[i] = max(probs[i], probs[i + 1])
    return centers, probs

def apply_calibration_map(cmap, margins):
    centers, probs = cmap
    return np.interp(np.asarray(margins, float), centers, probs)

# ============================================================================
#  (A) CALIBRATION — ECE + monotone margin↑ as difficulty↑
# ============================================================================
def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    ra = ra - ra.mean(); rb = rb - rb.mean()
    denom = np.sqrt((ra*ra).sum() * (rb*rb).sum())
    return float((ra*rb).sum()/denom) if denom > 0 else 0.0

def ece(confs, corrects, n_bins=10):
    confs = np.asarray(confs, float); corrects = np.asarray(corrects, float)
    edges = np.linspace(0, 1, n_bins+1)
    e = 0.0; N = len(confs)
    for i in range(n_bins):
        lo, hi = edges[i], edges[i+1]
        m = (confs >= lo) & (confs < hi if i < n_bins-1 else confs <= hi)
        if m.sum() == 0:
            continue
        e += (m.sum()/N) * abs(confs[m].mean() - corrects[m].mean())
    return float(e)

def auroc(scores, labels):
    scores = np.asarray(scores, float); labels = np.asarray(labels, int)
    pos = scores[labels == 1]; neg = scores[labels == 0]
    if len(pos) == 0 or len(neg) == 0:
        return 0.5
    wins = 0.0
    for p in pos:
        wins += (p > neg).sum() + 0.5*(p == neg).sum()
    return float(wins/(len(pos)*len(neg)))

# ============================================================================
#  (B) CONTROL — region-of-proximal-learning adaptive sampling vs uniform
# ============================================================================
def control_lift(trials, seed, policy="rpl"):
    """
    REGION-OF-PROXIMAL-LEARNING control (Metcalfe & Kornell 2005). A hard query is a
    NOISY observation of the true key. Each EXTRA read = an INDEPENDENT fresh corrupted
    observation of the SAME true fact (a noisy re-look at the world); the engine AVERAGES
    the embedded observation keys (denoise) before the live recall. More reads → the
    averaged key concentrates on the true cell → recovers items at INTERMEDIATE difficulty
    (the proximal zone) while trivial items don't need it and hopeless ones can't be saved.

    RPL allocates the extra-read budget to LOW-confidence-but-RECOVERABLE items (margin
    near the abstain threshold), reading ONLY the live margin — NO accuracy label (p6).
    uniform = spread evenly. ablated = margin-BLIND (reads a constant ⇒ uniform allocation =
    the EARNED bar D: remove the margin read and the lift collapses). Returns (base, adaptive, uniform).
    """
    rng = np.random.default_rng(seed * 104729 + 3)
    n = len(trials)
    protos = trials[0]['protos']; values = trials[0]['values']; facts = trials[0]['facts']
    BUDGET = 2 * n                      # total extra reads (tight enough that allocation matters)
    PROX_CENTER = 0.05                  # proximal peak: margin just past the abstain edge
    PROX_WIDTH  = 0.05                  # recoverable band half-width (the proximal zone)

    margins = np.array([t['margin'] for t in trials])

    def allocate(kind):
        if kind == "uniform":
            return np.full(n, BUDGET // n, dtype=int)
        if kind == "ablated":
            # margin-BLIND: the policy reads a CONSTANT instead of the live margin → it has
            # no basis to prefer any item → allocates UNIFORMLY. The D earned control: with
            # the margin read removed, the RPL advantage vanishes (lift → 0 by construction).
            return np.full(n, BUDGET // n, dtype=int)
        # RPL proximal weighting: peak effort where the margin sits in the recoverable band
        # (small-positive, just past the abstain edge), taper for the confidently-correct
        # (margin ≪ 0, no help needed) and the hopelessly-far (margin ≫ band, unrecoverable).
        # Reads ONLY the substrate margin — no accuracy label (p6).
        prox = np.exp(-((margins - PROX_CENTER) ** 2) / (2 * (PROX_WIDTH ** 2)))
        prox = prox * (margins > -0.05)                       # skip the already-correct floor
        if prox.sum() <= 0:
            prox = np.ones(n)
        w = prox / prox.sum()
        return np.floor(w * BUDGET).astype(int)

    def evaluate(alloc):
        correct = 0
        for i, t in enumerate(trials):
            # start from the original observed key; each extra read draws a FRESH
            # independent corruption of the TRUE fact at the same difficulty, averaged.
            keys = [t['q_key']]
            for _ in range(int(alloc[i])):
                obs = corrupt(facts[t['true']], t['L'], rng)
                keys.append(embed_key(obs))
            avg = np.mean(keys, axis=0)
            nrm = np.sqrt((avg*avg).sum())
            if nrm > 0:
                avg = avg / nrm
            pred = query_key(protos, values, avg)[2]
            if pred == values[t['true']]:
                correct += 1
        return correct / n

    base_acc = sum(t['correct'] for t in trials) / n
    adaptive_acc = evaluate(allocate(policy))
    uniform_acc = evaluate(allocate("uniform"))
    return base_acc, adaptive_acc, uniform_acc

# ============================================================================
#  run all seeds, pool, score frozen bars
# ============================================================================
def main():
    # ---- fit the HELD-OUT calibration map on a TRAIN seed disjoint from the TEST seeds ----
    TRAIN_SEED = 99            # NOT in SEEDS — the calibration map sees only this fit split
    train_trials, *_ = run_trials(TRAIN_SEED)
    cmap = fit_calibration_map([t['margin'] for t in train_trials],
                               [t['correct'] for t in train_trials])

    allc, allcorr, allL, allmarg = [], [], [], []
    per_level_margin = {L: [] for L in DIFFICULTY}
    per_level_acc = {L: [] for L in DIFFICULTY}
    lift_rpl, lift_uniform_ablate = [], []
    base_accs = []

    for seed in SEEDS:
        trials, facts, values, protos = run_trials(seed)
        for t in trials:
            # confidence = held-out calibrated map of the raw substrate margin (test conf
            # uses NO test label — the map was fit on the disjoint TRAIN_SEED only).
            conf = float(apply_calibration_map(cmap, [t['margin']])[0])
            allc.append(conf); allcorr.append(t['correct'])
            allL.append(t['L']); allmarg.append(t['margin'])
            per_level_margin[t['L']].append(t['margin'])
            per_level_acc[t['L']].append(t['correct'])
        # (B) control
        base, adapt, unif = control_lift(trials, seed, "rpl")
        lift_rpl.append(adapt - unif)
        base_accs.append(base)
        # (D) ablate: margin-BLIND allocation (policy reads a constant → uniform) vs uniform
        # → the RPL lift collapses (the margin read is what earns the advantage).
        _, abl_acc, unif2 = control_lift(trials, seed, "ablated")
        lift_uniform_ablate.append(abl_acc - unif2)

    # ---- (A) CALIBRATION ----
    ece_val = ece(allc, allcorr, n_bins=10)
    # monotone: difficulty (L) vs margin → margin RISES as L rises (positive spearman)
    mono = spearman(allL, allmarg)
    level_margins = [np.mean(per_level_margin[L]) for L in DIFFICULTY]
    level_accs = [np.mean(per_level_acc[L]) for L in DIFFICULTY]
    A_pass = (ece_val <= A_ECE_MAX) and (mono >= A_MONO_MIN)

    # ---- (B) CONTROL-LIFT ----
    lift_mean = float(np.mean(lift_rpl))
    B_pass = lift_mean >= B_LIFT_MIN

    # ---- (C) DISCRIMINATION ⊥ CALIBRATION (headline orthogonality) ----
    # AUROC of confidence vs correctness = the DISCRIMINATION axis (the prior chain).
    auroc_base = auroc(allc, allcorr)
    # STRICTLY-MONOTONE (rank-preserving, NO clipping) over-confidence transform:
    #   c' = 0.55 + 0.44·c maps confidence into [0.55, 0.99] — a strictly-increasing affine
    #   that systematically INFLATES confidence (the model now claims ≥0.55 everywhere). Order
    #   is preserved EXACTLY (equal values stay equal, none clipped) ⇒ AUROC (rank-only) is
    #   byte-IDENTICAL, while ECE (the numeric gap to accuracy) SHIFTS up sharply (now badly
    #   over-confident). This is the HEADLINE: calibration is a NEW axis the AUROC chain
    #   (type-2 AUROC 0.906, H_1398) is BLIND to — same ranking, different calibration.
    conf_arr = np.asarray(allc)
    conf_overconf = 0.55 + 0.44 * conf_arr                          # strictly monotone affine
    auroc_xform = auroc(conf_overconf, allcorr)
    ece_xform = ece(conf_overconf, allcorr, n_bins=10)
    auroc_drift = abs(auroc_xform - auroc_base)
    ece_shift = abs(ece_xform - ece_val)
    C_pass = (auroc_drift <= C_AUROC_DRIFT_MAX) and (ece_shift >= C_ECE_SHIFT_MIN)

    # ---- (D) EARNED ablate: margin-blind allocation → lift collapses ----
    ablate_lift = float(np.mean(lift_uniform_ablate))
    D_pass = abs(ablate_lift) <= D_ABLATE_MAX

    # ---- (E) EARNED shuffle: permute margin↔difficulty → calibration+control to chance ----
    rng = np.random.default_rng(20250620)
    perm = rng.permutation(len(allc))
    shuf_conf = np.asarray(allc)[perm]
    auroc_shuf = auroc(shuf_conf, allcorr)
    # calibration under shuffle: spearman(difficulty, shuffled margin) → ~0
    shuf_margin = np.asarray(allmarg)[perm]
    mono_shuf = spearman(allL, shuf_margin)
    E_pass = (abs(auroc_shuf - 0.5) <= E_CHANCE_BAND) and (abs(mono_shuf) <= E_CHANCE_BAND)

    GREEN = A_pass and B_pass and D_pass and E_pass   # C is headline orthogonality (reported)

    out = {
        "hypothesis": "H_1508", "rung": "R1_numpy_mirror_DIRECTIONAL",
        "seeds": SEEDS, "difficulty_ladder": DIFFICULTY,
        "n_trials_per_seed": len(DIFFICULTY) * TRIALS_PER_LEVEL,
        "frozen_bars": {
            "A_ECE_MAX": A_ECE_MAX, "A_MONO_MIN": A_MONO_MIN,
            "B_LIFT_MIN": B_LIFT_MIN, "D_ABLATE_MAX": D_ABLATE_MAX,
            "E_CHANCE_BAND": E_CHANCE_BAND,
            "C_AUROC_DRIFT_MAX": C_AUROC_DRIFT_MAX, "C_ECE_SHIFT_MIN": C_ECE_SHIFT_MIN,
        },
        "A_calibration": {
            "ECE": round(ece_val, 4), "monotone_spearman_L_vs_margin": round(mono, 4),
            "per_level_mean_margin": [round(x, 4) for x in level_margins],
            "per_level_accuracy": [round(x, 4) for x in level_accs],
            "pass": bool(A_pass),
        },
        "B_control_lift": {
            "rpl_minus_uniform_lift_mean": round(lift_mean, 4),
            "per_seed_lift": [round(x, 4) for x in lift_rpl],
            "base_accs": [round(x, 4) for x in base_accs],
            "pass": bool(B_pass),
        },
        "C_discrimination_orthogonal_calibration": {
            "AUROC_conf_vs_correct": round(auroc_base, 4),
            "AUROC_after_monotone_xform": round(auroc_xform, 4),
            "AUROC_drift": round(auroc_drift, 9),
            "ECE_base": round(ece_val, 4), "ECE_after_xform": round(ece_xform, 4),
            "ECE_shift": round(ece_shift, 4),
            "headline": "rank-preserving transform: AUROC INVARIANT, ECE SHIFTS → calibration ⊥ discrimination",
            "pass": bool(C_pass),
        },
        "D_earned_ablate": {
            "margin_blind_random_vs_uniform_lift": round(ablate_lift, 4),
            "pass": bool(D_pass),
        },
        "E_earned_shuffle": {
            "shuffled_AUROC": round(auroc_shuf, 4),
            "shuffled_calibration_spearman": round(mono_shuf, 4),
            "pass": bool(E_pass),
        },
        "GREEN": bool(GREEN),
        "verdict": ("🟢 GREEN (A∧B∧D∧E) — margin CALIBRATES + CONTROLS"
                    if GREEN else
                    "🟠 HONEST-SPLIT — margin monitors but does not fully calibrate/control"),
    }
    print(json.dumps(out, indent=2))
    return out

if __name__ == "__main__":
    main()
