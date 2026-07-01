#!/usr/bin/env python3
"""tensionlink_dim_time.py — benchmark the anima TENSION-LINK optimal dimension
and add a TIME AXIS.

This is the anima 5-ch tension-link parallel of the KOSMOS dimension work
(PR #1768 / #1772) and the #1763 "time enters via the derivative" finding,
applied to anima's own meta-telepathy channel (§97: tension-link = anima's
own channel).

THE OBJECT UNDER TEST
---------------------
The TENSION-LINK (HEXAD/TENSION-LINK/README.md) is anima's 5-CHANNEL
meta-fingerprint exchanged between two ConsciousMind cells:

  | Channel       | Role  | Dims     | Encoding                                  |
  |---------------|-------|----------|-------------------------------------------|
  | Concept       | what  | 16 float | normalize(engine_a - engine_g)            |
  | Context       | when  |  8 float | time phase + tension trend                |
  | Meaning       | why   | 16 float | engine_a * engine_g interaction           |
  | Authenticity  | trust |  1 float | Dedekind chain (variance / direction)     |
  | Sender        | who   |  4 float | [a_sig, g_sig, a*g, tension]              |
  |               |       | =45 total (sopfr(6)=5 channel GROUPS)     |

The "is 5 right?" question is about the 5 CHANNEL-GROUPS (sopfr(6)=5),
not the 45 raw floats. We reduce each 45-dim fingerprint to its natural
5-channel SUMMARY VECTOR (one scalar magnitude per channel group) — that
is the 5-ch tension vector that travels the link, the direct analogue of
the generator.hexa [alpha,theta,gamma,1-delta,beta] 5-ch literal.

DATA SOURCE (real vs synthetic — flagged in results.json)
---------------------------------------------------------
We drive each cell's OWN physics from the REAL §59-FIRE anima W-state trace
(_real_w_trace_s59.json, 300 steps: tension / psi_dir / psi_entropy / phi).
The fingerprint_5ch transfer law is the byte-faithful §65 code copied
verbatim from dual_anima_tension_link_smoke.py (the B-S65 4/4 BLUE-verified
5-channel spec). So:
  - tension TRAJECTORY shape           = REAL (s59 anima fire trace)
  - engine_a/engine_g latent + 5ch map = byte-faithful §65 transfer law
We label the COMBINED stream "real-shape-driven (synthetic-engine map)".
A second 3-regime synthetic set (diverse / majority / flat) is the control
ladder. No GPU, no pods, CPU/$0. numpy only (no sklearn / no torch).

PHASES
------
P1  intrinsic dim of the 5-ch tension stream X (T x 5):
    PCA explained-variance per PC, participation ratio, effective rank
    (entropy of the eigenvalue spectrum), channel correlation matrix.
    Per-channel independence: shuffle each channel alone, measure the
    drop in linear reconstruction of the held-out channels + the drop
    in stage/state decode. Projection ladder k=1..5 reconstruction R^2.
    Probe a 6th synthetic channel for independence.
P2  add a TIME AXIS:  [5ch] -> [5ch + dF/dt(5ch)]  (#1763 derivative form).
    The shuffle CONTROL: time-scramble the stream. A dF/dt-aware
    representation MUST degrade under scramble; the static-marginal
    representation MUST NOT (its per-row marginals are permutation
    invariant). Stage/state decode with vs without the time axis.

3 seeds. Verbatim verdicts; no rounding of the headline ratios.
"""

import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ── §65 byte-faithful transfer-law constants (verbatim from the smoke) ──
SEED_PHYS = 1337
ENGINE_DIM = 16
CH_CONCEPT = 16
CH_CONTEXT = 8
CH_MEANING = 16
CH_AUTH = 1
CH_SENDER = 4
FP_DIM = CH_CONCEPT + CH_CONTEXT + CH_MEANING + CH_AUTH + CH_SENDER  # 45
CHANNEL_NAMES = ["concept", "context", "meaning", "auth", "sender"]
# channel slice boundaries in the 45-dim fp (fp = concept+context+meaning+[auth]+sender)
CH_SLICES = {
    "concept": (0, 16),
    "context": (16, 24),
    "meaning": (24, 40),
    "auth": (40, 41),
    "sender": (41, 45),
}


# ──────────────────────────────────────────────────────────────────────
# §65 byte-faithful linear algebra + fingerprint (verbatim)
# ──────────────────────────────────────────────────────────────────────
def _seeded_vec(tag, dim):
    out = []
    s = 0x9E3779B9 ^ SEED_PHYS
    for b in tag.encode("utf-8"):
        s = (s * 1103515245 + 12345 + b) & 0xFFFFFFFF
    for i in range(dim):
        s = (s * 1103515245 + 12345 + i) & 0xFFFFFFFF
        out.append((s / 0xFFFFFFFF) * 2.0 - 1.0)
    return out


def _norm(v):
    return math.sqrt(sum(x * x for x in v)) or 1.0


def _unit(v):
    n = _norm(v)
    return [x / n for x in v]


def _l2(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def sender_physics(cell_id, engine_a, engine_g, intent):
    base = _seeded_vec(cell_id + "|a", ENGINE_DIM)
    pert = _seeded_vec(intent, ENGINE_DIM)
    a = [b + 0.5 * p for b, p in zip(base, pert)]
    bg = _seeded_vec(cell_id + "|g", ENGINE_DIM)
    g = [b - 0.5 * p for b, p in zip(bg, pert)]
    tension = _l2(a, g)
    return a, g, tension


def fingerprint_5ch(engine_a, engine_g, tension):
    """Verbatim §65 fingerprint_5ch (45-dim) — the BLUE-verified transfer law."""
    a, g = engine_a, engine_g
    concept = _unit([x - y for x, y in zip(a, g)])
    meaning = [x * y for x, y in zip(a, g)]
    mn = _norm(meaning)
    meaning = [x / mn for x in meaning]
    a_sig = sum(a) / len(a)
    g_sig = sum(g) / len(g)
    sender = [a_sig, g_sig, a_sig * g_sig, tension]
    t = tension
    context = [math.tanh(t), math.tanh(t / 2.0), math.cos(t), math.sin(t),
               math.tanh(a_sig), math.tanh(g_sig), 0.0, 0.0]
    var_a = sum((x - a_sig) ** 2 for x in a) / len(a)
    var_g = sum((x - g_sig) ** 2 for x in g) / len(g)
    auth = 1.0 / (1.0 + math.exp(-(var_a + var_g - 1.0)))
    fp = concept + context + meaning + [auth] + sender
    assert len(fp) == FP_DIM, (len(fp), FP_DIM)
    return fp


def channel_summary(fp):
    """Reduce a 45-dim fp to its 5-channel SUMMARY VECTOR — one scalar
    per channel group = the L2 magnitude of that group's slice. This is
    the 5-ch tension vector that semantically travels the link (the
    [alpha,theta,gamma,1-delta,beta] analogue).

    HONEST CAVEAT (p7): the §65 spec L2-NORMALIZES the concept and meaning
    channels (concept=_unit(a-g), meaning=meaning/||meaning||), so their
    *magnitude* is identically 1.0 every step — a magnitude-summary of those
    two channels is degenerate (zero temporal variance) BY CONSTRUCTION, not
    because the channel is redundant. The DIRECTION of those channels still
    carries info. We therefore report intrinsic dim on BOTH the 5-scalar
    magnitude-summary (this fn) AND the full 45-dim fingerprint stream, and
    never conflate 'magnitude-summary degenerate' with 'channel redundant'."""
    out = []
    for name in CHANNEL_NAMES:
        lo, hi = CH_SLICES[name]
        seg = fp[lo:hi]
        out.append(math.sqrt(sum(x * x for x in seg)))
    return out


# ──────────────────────────────────────────────────────────────────────
# stream builders
# ──────────────────────────────────────────────────────────────────────
class _LCG:
    def __init__(self, seed):
        self.s = seed & 0xFFFFFFFF

    def u(self):
        self.s = (1103515245 * self.s + 12345) & 0x7FFFFFFF
        return self.s / 0x7FFFFFFF


def load_real_w_trace():
    p = os.path.join(HERE, "_real_w_trace_s59.json")
    if not os.path.exists(p):
        # fallback to the canonical state copy
        p = os.path.join(HERE, "..", "state",
                         "dual_anima_tension_link_s61_2026_05_18",
                         "_real_w_trace_s59.json")
    with open(p) as fh:
        raw = json.load(fh)
    return [{"t": t, "tension": float(r["tension"]),
             "psi_dir": float(r["psi_dir"]),
             "psi_entropy": float(r["psi_entropy"]),
             "phi": float(r["phi"])} for t, r in enumerate(raw)]


def synth_stream(regime, n, seed):
    rng = _LCG(seed)
    seq = []
    tension = 0.05
    for t in range(n):
        if regime == "diverse":
            drive = 0.18 * math.sin(t / 7.0) + 0.10 * (rng.u() - 0.5)
            tension = max(0.0, 0.72 * tension + 0.28 * (0.20 + drive) + 0.04 * rng.u())
        elif regime == "majority":
            if rng.u() < 0.05:
                tension = 0.55 + 0.30 * rng.u()
            else:
                tension = 0.04 + 0.015 * (rng.u() - 0.5)
        elif regime == "flat":
            tension = 0.10
        else:
            raise ValueError(regime)
        psi_dir = 0.5 + 0.30 * math.tanh(2.0 * (tension - 0.25))
        psi_entropy = 0.5 + 0.20 * math.cos(t / 5.0) * (0.5 + 0.5 * tension)
        phi = 0.40 + 0.50 * tension
        seq.append({"t": t, "tension": tension, "psi_dir": psi_dir,
                    "psi_entropy": psi_entropy, "phi": phi})
    return seq


def build_5ch_stream(physics_seq, cell_id, seed):
    """Map a physics trajectory -> T x 5 channel-summary matrix + the engine
    tension trace + a derived STAGE label per step.

    The intent strings vary per-step (so the fingerprint actually moves with
    the trace, not a constant), keyed off the trace shape + a per-seed offset
    so the 3 seeds are genuinely distinct realizations."""
    rng = _LCG(seed ^ 0x5bd1e995)
    X = []
    fulls = []
    tens = []
    stages = []
    for rec in physics_seq:
        t_phys = rec["tension"]
        # intent string driven by the trace shape + seed (deterministic)
        bucket = int(min(9, max(0, math.floor(t_phys * 10.0))))
        intent = f"{cell_id}|topic{bucket}|s{seed}|p{int(rec['phi']*10)}"
        a, g, eng_tension = sender_physics(cell_id, None, None, intent)
        # fold the REAL trace tension into the engine tension (the trace is
        # the load-bearing shape; the transfer law gives the 5ch geometry)
        eng_tension = 0.5 * eng_tension + 0.5 * (t_phys * 4.0)
        fp = fingerprint_5ch(a, g, eng_tension)
        X.append(channel_summary(fp))
        fulls.append(fp)
        tens.append(t_phys)
        # 5-stage ultradian label from the trace (WAKE/N1/N2/N3/REM proxy)
        # via phi + tension — this is the engine STATE the link should decode
        stages.append(stage_label(rec))
    return (np.array(X, dtype=float), np.array(tens, dtype=float),
            np.array(stages), np.array(fulls, dtype=float))


def stage_label(rec):
    """5-state proxy (WAKE=0 N1=1 N2=2 N3=3 REM=4) from phi+tension.
    Deterministic, derived from the trace — the engine STATE the temporal
    trajectory should predict."""
    phi = rec["phi"]
    t = rec["tension"]
    score = 0.6 * phi + 0.4 * t
    if score > 0.55:
        return 0  # WAKE (high integration + tension)
    if score > 0.40:
        return 4  # REM (high phi, moderate)
    if score > 0.28:
        return 1  # N1
    if score > 0.18:
        return 2  # N2
    return 3      # N3 (deep, low)


# ──────────────────────────────────────────────────────────────────────
# linear algebra utilities (numpy only — no sklearn)
# ──────────────────────────────────────────────────────────────────────
def zscore(X):
    mu = X.mean(axis=0)
    sd = X.std(axis=0)
    sd = np.where(sd < 1e-12, 1.0, sd)
    return (X - mu) / sd, mu, sd


def pca_spectrum(X):
    """Return eigenvalues (variance per PC, descending) of the covariance of
    the z-scored X, plus explained-variance ratio."""
    Z, _, _ = zscore(X)
    C = np.cov(Z, rowvar=False)
    w = np.linalg.eigvalsh(C)
    w = np.clip(w[::-1], 0.0, None)  # descending, non-negative
    total = w.sum()
    evr = w / total if total > 0 else w
    return w, evr


def participation_ratio(eigs):
    """PR = (sum lambda)^2 / sum(lambda^2). Continuous effective-dim count."""
    s1 = eigs.sum()
    s2 = (eigs ** 2).sum()
    return (s1 * s1) / s2 if s2 > 0 else 0.0


def effective_rank(eigs):
    """erank = exp(H) where H = -sum p log p, p = eig/sum(eig). (Roy & Vetterli)"""
    s = eigs.sum()
    if s <= 0:
        return 0.0
    p = eigs / s
    p = p[p > 1e-15]
    H = -(p * np.log(p)).sum()
    return math.exp(H)


def corr_matrix(X):
    return np.corrcoef(X, rowvar=False)


def ridge_fit(A, b, lam=1e-3):
    """Closed-form ridge regression coefficients."""
    n_feat = A.shape[1]
    G = A.T @ A + lam * np.eye(n_feat)
    return np.linalg.solve(G, A.T @ b)


def r2_score(y_true, y_pred):
    ss_res = ((y_true - y_pred) ** 2).sum()
    ss_tot = ((y_true - y_true.mean()) ** 2).sum()
    return 1.0 - ss_res / ss_tot if ss_tot > 1e-15 else 0.0


def design(X):
    """add intercept column."""
    return np.hstack([np.ones((X.shape[0], 1)), X])


def linear_decode_acc(X, y, train_frac=0.6, n_classes=5):
    """One-vs-rest ridge classifier accuracy on a held-out tail.
    Pure numpy. Deterministic split (temporal: first frac = train)."""
    n = X.shape[0]
    cut = int(n * train_frac)
    Xtr, Xte = X[:cut], X[cut:]
    ytr, yte = y[:cut], y[cut:]
    Atr, Ate = design(Xtr), design(Xte)
    scores = np.zeros((Xte.shape[0], n_classes))
    for c in range(n_classes):
        tgt = (ytr == c).astype(float)
        if tgt.sum() == 0:
            scores[:, c] = -1e9  # class absent in train
            continue
        w = ridge_fit(Atr, tgt, lam=1e-2)
        scores[:, c] = Ate @ w
    pred = scores.argmax(axis=1)
    return float((pred == yte).mean())


def reconstruct_r2_from_projection(X, k):
    """z-score, project to top-k PCs, reconstruct, return mean per-channel R^2."""
    Z, _, _ = zscore(X)
    C = np.cov(Z, rowvar=False)
    w, V = np.linalg.eigh(C)
    idx = np.argsort(w)[::-1]
    Vk = V[:, idx[:k]]
    Zrec = Z @ Vk @ Vk.T
    r2s = [r2_score(Z[:, j], Zrec[:, j]) for j in range(Z.shape[1])]
    return float(np.mean(r2s)), r2s


def per_channel_shuffle_drop(X, y, seed):
    """For each channel, shuffle it ALONE (in time) and measure (a) the drop
    in reconstructing the OTHER 4 channels from it via ridge, and (b) the
    drop in stage-decode accuracy. A channel carrying isolated info -> large
    drop. A duplicative channel -> ~0 drop."""
    rng = np.random.default_rng(seed)
    n, d = X.shape
    base_acc = linear_decode_acc(X, y)
    out = {}
    for j in range(d):
        Xs = X.copy()
        Xs[:, j] = X[rng.permutation(n), j]
        # (a) reconstruction of the held-out 4 channels from this channel
        others = [c for c in range(d) if c != j]
        # how well does channel j (original) linearly predict the others?
        A = design(X[:, [j]])
        r2_orig = np.mean([r2_score(X[:, c], A @ ridge_fit(A, X[:, c]))
                           for c in others])
        As = design(Xs[:, [j]])
        r2_shuf = np.mean([r2_score(X[:, c], As @ ridge_fit(As, X[:, c]))
                           for c in others])
        # (b) stage decode with this channel shuffled
        acc_shuf = linear_decode_acc(Xs, y)
        out[CHANNEL_NAMES[j]] = {
            "predicts_others_r2": float(r2_orig),
            "predicts_others_r2_shuffled": float(r2_shuf),
            "decode_acc_drop": float(base_acc - acc_shuf),
        }
    out["_base_decode_acc"] = float(base_acc)
    return out


# ──────────────────────────────────────────────────────────────────────
# PHASE 2 — time axis
# ──────────────────────────────────────────────────────────────────────
def add_time_axis(X):
    """[5ch] -> [5ch + dF/dt(5ch)] (#1763: time enters via the derivative).
    dF/dt = forward difference (first row repeated)."""
    dX = np.diff(X, axis=0)
    dX = np.vstack([dX[0:1], dX])  # pad to match length
    return np.hstack([X, dX])


def time_scramble(X, seed):
    """Permute the ROWS (time order) — destroys all dynamics, preserves the
    per-row marginal SET. A static-marginal representation is invariant to
    this; a dF/dt representation is NOT."""
    rng = np.random.default_rng(seed)
    return X[rng.permutation(X.shape[0])]


def dynamics_energy(X):
    """Total dF/dt energy (sum of squared first differences) — a scalar that
    a dynamics-aware rep can see and a static-marginal rep cannot."""
    dX = np.diff(X, axis=0)
    return float((dX ** 2).sum())


# ──────────────────────────────────────────────────────────────────────
# RUN
# ──────────────────────────────────────────────────────────────────────
def run_seed(seed, physics_real, n_synth=300):
    """Run all probes for one seed; return a results dict."""
    res = {"seed": seed}

    # build the REAL-shape-driven 5ch stream (cell A)
    Xr, tens_r, stages_r, Xfull = build_5ch_stream(physics_real, "cellA", seed)
    # synthetic control ladder
    syn = {}
    for reg in ["diverse", "majority", "flat"]:
        seq = synth_stream(reg, n_synth, seed + hash(reg) % 1000)
        Xs, _, st, _f = build_5ch_stream(seq, "cellA", seed)
        syn[reg] = (Xs, st)

    # ── P1: intrinsic dim on the REAL-shape stream ──
    eigs, evr = pca_spectrum(Xr)
    pr = participation_ratio(eigs)
    er = effective_rank(eigs)
    corr = corr_matrix(Xr)
    ladder = {k: reconstruct_r2_from_projection(Xr, k)[0] for k in range(1, 6)}
    shuf = per_channel_shuffle_drop(Xr, stages_r, seed)

    # full 45-dim fingerprint intrinsic dim — the representation that
    # PRESERVES concept/meaning DIRECTION (not just magnitude). This is the
    # honest counterweight to the magnitude-summary degeneracy.
    eigs_full, evr_full = pca_spectrum(Xfull)
    pr_full = participation_ratio(eigs_full)
    er_full = effective_rank(eigs_full)
    # 90% / 95% variance dimension on the full fp
    cum = np.cumsum(evr_full)
    dim90 = int(np.searchsorted(cum, 0.90) + 1)
    dim95 = int(np.searchsorted(cum, 0.95) + 1)

    # 6th synthetic channel probe: is an independent extra channel even
    # available? Add a genuinely independent gaussian channel and an
    # already-derivable one (concept-meaning product), compare PR gain.
    rng = np.random.default_rng(seed ^ 0xABCDEF)
    indep = rng.standard_normal(Xr.shape[0])
    derivable = Xr[:, 0] * Xr[:, 2]  # concept*meaning — derivable from existing
    X6_indep = np.hstack([Xr, indep[:, None]])
    X6_deriv = np.hstack([Xr, derivable[:, None]])
    e6i, _ = pca_spectrum(X6_indep)
    e6d, _ = pca_spectrum(X6_deriv)
    pr6_indep = participation_ratio(e6i)
    pr6_deriv = participation_ratio(e6d)

    res["P1"] = {
        "source": "real-shape-driven (s59 trace) + byte-faithful §65 transfer",
        "T_x_5_shape": list(Xr.shape),
        "pca_eigs_desc": [float(x) for x in eigs],
        "explained_var_ratio_desc": [float(x) for x in evr],
        "participation_ratio": float(pr),
        "effective_rank": float(er),
        "corr_matrix": [[float(c) for c in row] for row in corr],
        "channel_order": CHANNEL_NAMES,
        "projection_ladder_recon_r2": {str(k): float(v) for k, v in ladder.items()},
        "per_channel_shuffle": shuf,
        "sixth_channel_probe": {
            "pr_base_5ch": float(pr),
            "pr_with_independent_6th": float(pr6_indep),
            "pr_with_derivable_6th": float(pr6_deriv),
            "indep_gain": float(pr6_indep - pr),
            "deriv_gain": float(pr6_deriv - pr),
        },
        "full_fp_45dim": {
            "note": "intrinsic dim of the full 45-float fingerprint (preserves "
                    "concept/meaning DIRECTION; magnitude-summary degeneracy absent)",
            "participation_ratio": float(pr_full),
            "effective_rank": float(er_full),
            "dim_for_90pct_var": dim90,
            "dim_for_95pct_var": dim95,
            "top5_explained_var_ratio": [float(x) for x in evr_full[:5]],
        },
    }

    # ── P2: time axis ──
    Xt = add_time_axis(Xr)
    # decode WITH vs WITHOUT time axis
    acc_static = linear_decode_acc(Xr, stages_r)
    acc_time = linear_decode_acc(Xt, stages_r)

    # shuffle CONTROL: time-scramble, recompute a dynamics-sensitive statistic
    # vs a static-marginal statistic.
    Xr_scram = time_scramble(Xr, seed)
    dyn_orig = dynamics_energy(Xr)
    dyn_scram = dynamics_energy(Xr_scram)
    # static-marginal stat = sorted column means (permutation invariant) ->
    # measure as the column-mean vector L2 (must be ~identical pre/post)
    static_orig = float(np.linalg.norm(Xr.mean(axis=0)))
    static_scram = float(np.linalg.norm(Xr_scram.mean(axis=0)))

    # decode on scrambled stream: time-axis decode should COLLAPSE toward
    # the static decode (the derivative channels are now noise), while the
    # static decode is invariant (rows unchanged, only reordered -> but the
    # train/test temporal split changes, so we instead compare the
    # dynamics-detectability directly).
    Xt_scram = add_time_axis(Xr_scram)
    # The clean test: does the dF/dt block carry signal that the scramble
    # destroys? Predict the current stage from ONLY the dF/dt block.
    dblock = Xt[:, 5:]
    dblock_scram = Xt_scram[:, 5:]
    acc_dblock = linear_decode_acc(dblock, stages_r)
    # scrambled dblock against scrambled stages (the matched control)
    stages_scram = stages_r[time_scramble_idx(Xr, seed)]
    acc_dblock_scram = linear_decode_acc(dblock_scram, stages_scram)

    # ── the DYNAMICS-NECESSARY label (the decisive P2 test) ──
    # The stage label above is a per-step function of phi+tension, so a static
    # snapshot trivially decodes it (ceiling -> zero headroom for time). To
    # test whether the TIME axis captures dynamics the static rep CANNOT, use
    # a label that is provably NOT a function of a single snapshot: the
    # RISING/FALLING direction of the underlying tension (sign of dF/dt).
    # A static 5-ch snapshot at time t is identical whether tension is on its
    # way up or down through that value -> static decode must sit near chance;
    # the dF/dt-augmented rep should recover it.
    dyn_label = (np.diff(tens_r) > 0).astype(int)        # 1=rising 0=falling
    dyn_label = np.concatenate([dyn_label[:1], dyn_label])
    acc_static_dyn = linear_decode_acc(Xr, dyn_label, n_classes=2)
    acc_time_dyn = linear_decode_acc(Xt, dyn_label, n_classes=2)
    # matched shuffle control (the FALSIFIER): permute the (row, label) PAIRS
    # together so each snapshot still carries its own true rising/falling
    # label (static info intact), but the TEMPORAL ORDER is destroyed -> the
    # dF/dt computed on the reordered stream no longer reflects each row's
    # real neighbour, so the derivative block is noise. A genuine
    # dynamics-reading rep must lose its gain (collapse to ~static); if it
    # held its gain, the gain would be an artifact rather than real dynamics.
    perm = time_scramble_idx(Xr, seed)
    Xt_scram_paired = add_time_axis(Xr[perm])      # derivative now meaningless
    dyn_label_paired = dyn_label[perm]             # label rides with the row
    acc_time_dyn_scram = linear_decode_acc(Xt_scram_paired, dyn_label_paired, n_classes=2)
    base_rate_dyn = float(max(dyn_label.mean(), 1.0 - dyn_label.mean()))

    res["P2"] = {
        "stage_label_decode": {
            "note": "stage label = f(phi,tension) per-step -> static at ceiling, "
                    "no headroom (expected). Reported for completeness.",
            "decode_acc_static_5ch": float(acc_static),
            "decode_acc_time_aug_10ch": float(acc_time),
            "decode_acc_gain_from_time": float(acc_time - acc_static),
        },
        "rising_falling_decode": {
            "note": "DYNAMICS-NECESSARY label = sign(dF/dt tension). NOT a "
                    "function of a single snapshot -> the decisive time-axis test.",
            "majority_base_rate": base_rate_dyn,
            "decode_acc_static_5ch": float(acc_static_dyn),
            "decode_acc_time_aug_10ch": float(acc_time_dyn),
            "decode_acc_gain_from_time": float(acc_time_dyn - acc_static_dyn),
            "decode_acc_time_aug_scrambled": float(acc_time_dyn_scram),
        },
        "shuffle_control": {
            "dynamics_energy_orig": dyn_orig,
            "dynamics_energy_scrambled": dyn_scram,
            "static_marginal_L2_orig": static_orig,
            "static_marginal_L2_scrambled": static_scram,
            "static_marginal_invariant": bool(abs(static_orig - static_scram) < 1e-9),
            "dF_dt_block_stage_decode_acc": float(acc_dblock),
            "dF_dt_block_stage_decode_acc_scrambled": float(acc_dblock_scram),
        },
    }

    # synthetic ladder check (does the dim verdict transfer across regimes?)
    res["P1_synth"] = {}
    for reg, (Xs, _st) in syn.items():
        es, _ = pca_spectrum(Xs)
        res["P1_synth"][reg] = {
            "participation_ratio": float(participation_ratio(es)),
            "effective_rank": float(effective_rank(es)),
        }
    return res


# global cache so time_scramble and its index share the SAME permutation
_SCRAMBLE_IDX = {}


def time_scramble_idx(X, seed):
    key = (id(X), seed)
    if key not in _SCRAMBLE_IDX:
        rng = np.random.default_rng(seed)
        _SCRAMBLE_IDX[key] = rng.permutation(X.shape[0])
    return _SCRAMBLE_IDX[key]


def time_scramble(X, seed):  # noqa: F811 (override to use cached idx)
    return X[time_scramble_idx(X, seed)]


def main():
    physics_real = load_real_w_trace()
    seeds = [1, 7, 42]
    all_res = [run_seed(s, physics_real) for s in seeds]

    # aggregate
    pr_vals = [r["P1"]["participation_ratio"] for r in all_res]
    er_vals = [r["P1"]["effective_rank"] for r in all_res]
    evr_top1 = [r["P1"]["explained_var_ratio_desc"][0] for r in all_res]
    indep_gain = [r["P1"]["sixth_channel_probe"]["indep_gain"] for r in all_res]
    deriv_gain = [r["P1"]["sixth_channel_probe"]["deriv_gain"] for r in all_res]
    pr_full = [r["P1"]["full_fp_45dim"]["participation_ratio"] for r in all_res]
    er_full = [r["P1"]["full_fp_45dim"]["effective_rank"] for r in all_res]
    dim90 = [r["P1"]["full_fp_45dim"]["dim_for_90pct_var"] for r in all_res]
    dim95 = [r["P1"]["full_fp_45dim"]["dim_for_95pct_var"] for r in all_res]

    # decisive rising/falling (dynamics-necessary) P2 metrics
    rf_static = [r["P2"]["rising_falling_decode"]["decode_acc_static_5ch"] for r in all_res]
    rf_time = [r["P2"]["rising_falling_decode"]["decode_acc_time_aug_10ch"] for r in all_res]
    rf_gain = [r["P2"]["rising_falling_decode"]["decode_acc_gain_from_time"] for r in all_res]
    rf_scram = [r["P2"]["rising_falling_decode"]["decode_acc_time_aug_scrambled"] for r in all_res]
    rf_base = [r["P2"]["rising_falling_decode"]["majority_base_rate"] for r in all_res]
    dblock = [r["P2"]["shuffle_control"]["dF_dt_block_stage_decode_acc"] for r in all_res]
    dblock_s = [r["P2"]["shuffle_control"]["dF_dt_block_stage_decode_acc_scrambled"] for r in all_res]
    dyn_o = [r["P2"]["shuffle_control"]["dynamics_energy_orig"] for r in all_res]
    dyn_s = [r["P2"]["shuffle_control"]["dynamics_energy_scrambled"] for r in all_res]

    summary = {
        "n_seeds": len(seeds),
        "seeds": seeds,
        "P1_magnitude_summary_5ch": {
            "participation_ratio_mean": float(np.mean(pr_vals)),
            "participation_ratio_per_seed": pr_vals,
            "effective_rank_mean": float(np.mean(er_vals)),
            "effective_rank_per_seed": er_vals,
            "top1_explained_var_mean": float(np.mean(evr_top1)),
            "caveat": "concept+meaning magnitude is constant 1.0 by spec "
                      "(L2-normalized) -> 2 of 5 PCs structurally zero; "
                      "magnitude-summary effective dim ~2.5-3 is partly a "
                      "summary-choice artifact, NOT proof those channels are "
                      "redundant (their DIRECTION carries info; see full_fp).",
        },
        "P1_full_fp_45dim": {
            "participation_ratio_mean": float(np.mean(pr_full)),
            "participation_ratio_per_seed": pr_full,
            "effective_rank_mean": float(np.mean(er_full)),
            "dim_for_90pct_var_per_seed": dim90,
            "dim_for_95pct_var_per_seed": dim95,
        },
        "P1_sixth_indep_gain_mean": float(np.mean(indep_gain)),
        "P1_sixth_deriv_gain_mean": float(np.mean(deriv_gain)),
        "P2_rising_falling_static_acc_mean": float(np.mean(rf_static)),
        "P2_rising_falling_time_acc_mean": float(np.mean(rf_time)),
        "P2_rising_falling_gain_mean": float(np.mean(rf_gain)),
        "P2_rising_falling_gain_per_seed": rf_gain,
        "P2_rising_falling_time_scrambled_acc_mean": float(np.mean(rf_scram)),
        "P2_rising_falling_base_rate_mean": float(np.mean(rf_base)),
        "P2_dF_dt_block_stage_acc_mean": float(np.mean(dblock)),
        "P2_dF_dt_block_stage_acc_scrambled_mean": float(np.mean(dblock_s)),
        "P2_dynamics_energy_orig_mean": float(np.mean(dyn_o)),
        "P2_dynamics_energy_scrambled_mean": float(np.mean(dyn_s)),
    }
    out = {"per_seed": all_res, "summary": summary,
           "data_source": {
               "real_trace": "_real_w_trace_s59.json (§59-FIRE anima W-state, 300 steps)",
               "transfer_law": "byte-faithful §65 fingerprint_5ch (B-S65 4/4 BLUE)",
               "flag": "real-shape-driven; engine latent + 5ch map = synthetic transfer law",
               "compute": "CPU / $0 / numpy-only (no torch, no sklearn, no GPU/pods)",
           }}
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
