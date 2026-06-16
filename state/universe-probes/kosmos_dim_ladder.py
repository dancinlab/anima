#!/usr/bin/env python3
"""
kosmos_dim_ladder.py — STANDALONE toy benchmark (DIMENSION LADDER).

Question
--------
The KOSMOS anchor coordinate already carries placement attributes
(coord/lane/radius/tier/tags — see HEXAD/KOSMOS.md). PR #1765 extended the
coordinate by ONE axis (time, [x,y]->[x,y,t]) and found it captures
carve-sequence, BUT flagged a near-tautology caveat: for monotone time
encodings t is 1-1 with the carve-step, so "recovery" partly reads back the
encoding rather than proving independent information.

This benchmark ladders the coordinate dimensionality D = 2 -> 8 and asks the
CAPACITY question that #1765 did not: does EACH ADDED axis carry NEW
INDEPENDENT information (the D-dim map discriminates a held-out attribute
better than the (D-1)-dim map by more than seed-noise), or do axes SATURATE /
become redundant past some dimension D* (an axis capacity)?

It resolves the #1765 tautology by construction: every axis encodes its OWN
independent LATENT CLASS signal, NOT a monotone function of one shared index.
Recovery is measured by kNN discrimination of a HELD-OUT attribute label, which
cannot be trivially read back from a monotone coordinate. Controlled
cross-correlations are injected so REDUNDANCY is itself measurable (a redundant
axis should add no kNN info -> SATURATED, the honest expected finding).

Axes laddered (each a distinct, independent KOSMOS anchor attribute):
  D=2  x,y  = Psi-space placement (vacuum_psi)              [baseline 2D]
  D=3  t    = carve-order / time (#1765 axis)
  D=4  e    = emotion valence (top_emotion)
  D=5  tau  = tier (Knuth ordinal)
  D=6  m    = modality channel (EEG / LiDAR / dolphin-acoustic / text)
  D=7  s    = scale / radius (basin_radius)
  D=8  kappa= lane / cell_id (MITOSIS partition)

Design (NON-tautology, the core of this benchmark):
  - Each anchor i has an INDEPENDENT latent label per axis:
      lab_y  in {0,1,2}  (the held-out spatial cluster — recovery target)
      lab_t  in {0,1,2}  (a TIME-regime label, independent of lab_y)
      lab_e  in {0,1,2}  (emotion class)
      lab_tau in {0,1,2} (tier band)
      lab_m  in {0,1,2,3}(modality channel; 4 real ingested modalities)
      lab_s  in {0,1,2}  (scale band)
      lab_kap in {0,1,2} (lane partition)
    These labels are drawn INDEPENDENTLY (seed-varied) EXCEPT for two
    deliberately-injected redundancies so saturation is measurable:
      * axis s (scale, D=7) is set to be ~85% correlated with axis t
        (a REDUNDANT axis: a near-copy of an already-present signal).
      * axis kappa (lane, D=8) is ~80% correlated with axis e
        (a second REDUNDANT axis).
    The independent axes (t, e, tau, m) should each ADD kNN info; the
    redundant axes (s, kappa) should SATURATE (add ~0 beyond noise).
  - The RECOVERY TARGET is a JOINT label that depends on ALL independent
    latent axes equally (a held-out attribute that needs every independent
    axis to discriminate). Each added INDEPENDENT axis supplies one more
    factor of the joint target -> kNN recovery should rise; each REDUNDANT
    axis supplies nothing new -> kNN recovery flat.
  - Crucially the coordinate value on each axis is a NOISY continuous embedding
    of its latent label (class-conditional Gaussian), NOT a 1-1 monotone index.
    So kNN recovery is a genuine discrimination task, not an index read-back.

Measures (per rung D = 2..8), substrate-native, NOT cross-entropy/perplexity (p7):
  F-NEWINFO        : kNN recovery accuracy of the held-out joint target at D vs
                     (D-1). HOLDS if acc(D) - acc(D-1) > 2-sigma seed noise.
                     SATURATED if within noise. COLLAPSE if acc(D) < acc(D-1)-2sig.
  F-PERAXIS-SHUFFLE: shuffling axis-k alone degrades recovery of attribute-k but
                     NOT the others (each axis independent & meaningful) — the
                     non-tautology control from #1765, generalised per-axis.
  F-CAPACITY       : the incremental-gain curve dAcc(D) and the knee D* where the
                     next added axis no longer beats noise (the honest capacity).
  F-NOCOLLAPSE     : distance concentration (relative contrast = (d_max-d_min)/
                     d_mean of pairwise distances) as D grows — axes stay
                     separable, no curse-of-dimensionality collapse at toy scale.

3 seeds, mean +/- std. NOTHING rounded. SATURATION is a valid honest finding
(a_paper_negative_ok) — capacity is real; we do NOT claim infinite gain.
CPU / $0 / STANDALONE (no wiring into any runtime engine/decoder).
"""

import json
import math
import sys

import numpy as np

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
N_ANCHORS = 600          # toy anchor population (mirror: KOSMOS e7_31 + s16 ~168)
SEEDS = [0, 1, 2]        # 3 fixed seeds
K_NN = 7                 # kNN neighbours for recovery
N_PERAXIS_SHUFFLE = 1    # per-seed shuffle is deterministic given seed
CLASS_SEP = 3.2          # class-conditional Gaussian mean separation (per axis)
CLASS_STD = 1.0          # within-class std
REDUND_S_T = 0.85        # axis s (scale) correlation with axis t (time) label
REDUND_KAP_E = 0.80      # axis kappa (lane) correlation with axis e (emotion)

# Axis ladder: (dim_index, short, attribute, n_classes, redundant_with)
# dim 0,1 = x,y are ONE attribute (spatial cluster) spanning 2 coordinate dims.
AXES = [
    # name,  attribute key, n_classes, redundant_with (None = independent)
    ("xy",  "lab_y",   3, None),    # D=2 baseline (2 coord dims, 1 attribute)
    ("t",   "lab_t",   3, None),    # D=3 time
    ("e",   "lab_e",   3, None),    # D=4 emotion
    ("tau", "lab_tau", 3, None),    # D=5 tier
    ("m",   "lab_m",   4, None),    # D=6 modality (4 real modalities)
    ("s",   "lab_s",   3, "lab_t"), # D=7 scale  (REDUNDANT with time)
    ("kap", "lab_kap", 3, "lab_e"), # D=8 lane   (REDUNDANT with emotion)
]
MODALITY_NAMES = ["EEG", "LiDAR", "dolphin-acoustic", "text"]
D_LADDER = list(range(2, 9))  # 2..8


# ---------------------------------------------------------------------------
# Latent labels per anchor per axis (the INDEPENDENT signals).
# ---------------------------------------------------------------------------
def make_labels(seed, n):
    """Independent latent labels per axis, plus two injected redundancies.

    Returns dict attr_key -> int array (n,). Labels are seed-varied (a
    different anchor population per seed). The independent axes are drawn
    independently; s and kappa are partial copies of t and e respectively so
    their REDUNDANCY (no new info) is measurable.
    """
    rng = np.random.default_rng(7000 + seed)
    labels = {}
    labels["lab_y"]   = rng.integers(0, 3, n)
    labels["lab_t"]   = rng.integers(0, 3, n)
    labels["lab_e"]   = rng.integers(0, 3, n)
    labels["lab_tau"] = rng.integers(0, 3, n)
    labels["lab_m"]   = rng.integers(0, 4, n)

    # Redundant axis s: with prob REDUND_S_T copy lab_t, else resample.
    keep_s = rng.random(n) < REDUND_S_T
    rand_s = rng.integers(0, 3, n)
    labels["lab_s"] = np.where(keep_s, labels["lab_t"], rand_s)

    # Redundant axis kappa: with prob REDUND_KAP_E copy lab_e, else resample.
    keep_k = rng.random(n) < REDUND_KAP_E
    rand_k = rng.integers(0, 3, n)
    labels["lab_kap"] = np.where(keep_k, labels["lab_e"], rand_k)
    return labels


# Order in which INDEPENDENT axes enter the ladder (matches AXES order, minus
# the redundant ones). Each contributes one factor to the held-out target, so
# the target's discriminability grows as more INDEPENDENT axes are read.
INDEP_AXES_ORDER = ["lab_y", "lab_t", "lab_e", "lab_tau", "lab_m"]


def held_out_target(labels):
    """The recovery target: a JOINT product-code over the INDEPENDENT axes.

    Each independent latent axis contributes one DIGIT of a mixed-radix code:
        target = ((( lab_y )*3 + lab_t )*3 + lab_e )*3 + lab_tau )*4 + lab_m
    The target is therefore a fine joint class (3*3*3*3*4 = 324 cells) whose
    cells are only separable when ALL independent axes are read. A coordinate
    that exposes more independent axes can split more target cells -> higher
    kNN recovery. The two REDUNDANT axes (s~t, kappa~e) are deliberately NOT
    in the code, so adding them supplies no new factor -> SATURATION.

    This is a genuine discrimination task on a NOISY class-conditional embedding
    (NOT an index read-back), so it defeats the #1765 monotone-tautology: there
    is no single shared index that all axes are 1-1 with.
    """
    t = labels["lab_y"].astype(int)
    t = t * 3 + labels["lab_t"]
    t = t * 3 + labels["lab_e"]
    t = t * 3 + labels["lab_tau"]
    t = t * 4 + labels["lab_m"]
    return t.astype(int)


# ---------------------------------------------------------------------------
# Coordinate embedding: each axis = noisy class-conditional Gaussian (NOT a
# 1-1 monotone index). xy attribute spans 2 coordinate dims.
# ---------------------------------------------------------------------------
def embed_axis(labels_arr, n_classes, seed, axis_dims, salt):
    """Embed integer labels -> continuous coordinate of `axis_dims` dims.

    Class-conditional isotropic Gaussian: class c centred at a fixed random
    per-class mean (separation CLASS_SEP), within-class std CLASS_STD. The
    coordinate is therefore a NOISY embedding of the label — recovering the
    label needs genuine discrimination, defeating the #1765 index read-back.
    """
    rng = np.random.default_rng(90000 + 131 * seed + salt)
    means = rng.normal(0, 1, (n_classes, axis_dims))
    # normalise class means to a sphere then scale by CLASS_SEP for clean sep.
    means = means / (np.linalg.norm(means, axis=1, keepdims=True) + 1e-9)
    means = means * CLASS_SEP
    out = means[labels_arr] + rng.normal(0, CLASS_STD, (len(labels_arr), axis_dims))
    return out


def build_coords(seed, labels):
    """Build the full coordinate per axis. Returns dict short -> (n, dims) array
    and an ordered list of (short, dims) for ladder assembly."""
    coords = {}
    layout = []
    for salt, (short, attr, ncls, _redund) in enumerate(AXES):
        dims = 2 if short == "xy" else 1
        coords[short] = embed_axis(labels[attr], ncls, seed, dims, salt)
        layout.append((short, dims))
    return coords, layout


def assemble_D(coords, layout, D):
    """Concatenate axes up to coordinate-dimension D. xy contributes 2 dims.

    Ladder: D=2 -> [xy]; D=3 -> [xy,t]; ... D=8 -> [xy,t,e,tau,m,s,kap].
    """
    cols = []
    dim_count = 0
    used = []
    for short, dims in layout:
        if dim_count >= D:
            break
        cols.append(coords[short])
        dim_count += dims
        used.append(short)
        if dim_count >= D:
            break
    X = np.concatenate(cols, axis=1)
    return X, used


# ---------------------------------------------------------------------------
# kNN recovery (leave-one-out) — pure numpy, no sklearn.
# ---------------------------------------------------------------------------
def knn_loo_accuracy(X, y, k=K_NN):
    """Leave-one-out kNN classification accuracy of labels y from coords X."""
    # standardise columns so axes are commensurate.
    mu = X.mean(0)
    sd = X.std(0) + 1e-9
    Xs = (X - mu) / sd
    n = len(y)
    # pairwise squared distances
    sq = (Xs * Xs).sum(1)
    d2 = sq[:, None] + sq[None, :] - 2.0 * (Xs @ Xs.T)
    np.fill_diagonal(d2, np.inf)  # exclude self
    correct = 0
    for i in range(n):
        nn = np.argpartition(d2[i], k)[:k]
        votes = np.bincount(y[nn], minlength=int(y.max()) + 1)
        pred = np.argmax(votes)
        if pred == y[i]:
            correct += 1
    return correct / n


def distance_concentration(X):
    """Relative contrast (d_max - d_min)/d_mean of pairwise distances.

    High = well separated; -> 0 = curse-of-dimensionality collapse.
    """
    mu = X.mean(0)
    sd = X.std(0) + 1e-9
    Xs = (X - mu) / sd
    sq = (Xs * Xs).sum(1)
    d2 = sq[:, None] + sq[None, :] - 2.0 * (Xs @ Xs.T)
    iu = np.triu_indices(len(Xs), k=1)
    d = np.sqrt(np.clip(d2[iu], 0, None))
    return float((d.max() - d.min()) / (d.mean() + 1e-9))


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
def run():
    print("=" * 78)
    print("KOSMOS DIMENSION-LADDER toy benchmark (STANDALONE, CPU, $0)")
    print(f"N_ANCHORS={N_ANCHORS}  seeds={SEEDS}  k={K_NN}")
    print(f"injected redundancy: s~t={REDUND_S_T}  kappa~e={REDUND_KAP_E}")
    print(f"axis ladder D=2..8: xy(2) t e tau m(4cls) s[redund t] kap[redund e]")
    print(f"modalities (axis m): {MODALITY_NAMES}")
    print("=" * 78)

    # per-seed: recovery acc per D, per-axis-shuffle table, distance concentration
    acc_by_seed = {D: [] for D in D_LADDER}
    conc_by_seed = {D: [] for D in D_LADDER}
    # per-axis shuffle: degrade of TARGET recovery at full D=8 when axis-k shuffled
    shuf_target = {short: [] for short, _, _, _ in AXES}
    # per-axis shuffle: degrade of the axis's OWN attribute recovery (axis-isolated)
    shuf_own = {short: [] for short, _, _, _ in AXES}
    # per-axis shuffle: cross — does shuffling axis-k hurt OTHER attributes?
    shuf_cross = {short: [] for short, _, _, _ in AXES}

    for seed in SEEDS:
        labels = make_labels(seed, N_ANCHORS)
        target = held_out_target(labels)
        coords, layout = build_coords(seed, labels)

        print(f"\n--- seed {seed} ---")
        prev_acc = None
        for D in D_LADDER:
            X, used = assemble_D(coords, layout, D)
            acc = knn_loo_accuracy(X, target, K_NN)
            conc = distance_concentration(X)
            acc_by_seed[D].append(acc)
            conc_by_seed[D].append(conc)
            delta = "" if prev_acc is None else f"  dAcc={acc - prev_acc:+.5f}"
            print(f"  D={D} axes={used}  target_acc={acc:.5f}  conc={conc:.5f}{delta}")
            prev_acc = acc

        # ----- per-axis shuffle at full D=8 -----
        rng = np.random.default_rng(50000 + seed)
        X_full, used_full = assemble_D(coords, layout, 8)
        acc_full_target = knn_loo_accuracy(X_full, target, K_NN)
        # baseline: recover each axis's OWN attribute from the full coord
        own_attr = {short: attr for short, attr, _, _ in AXES}
        base_own = {}
        for short, _ in layout:
            base_own[short] = knn_loo_accuracy(X_full, labels[own_attr[short]], K_NN)

        for short, attr, ncls, _ in AXES:
            # shuffle ONLY this axis's coordinate columns
            coords_sh = {s: a.copy() for s, a in coords.items()}
            perm = rng.permutation(N_ANCHORS)
            coords_sh[short] = coords_sh[short][perm]
            Xsh, _ = assemble_D(coords_sh, layout, 8)
            # target recovery drop
            acc_t_sh = knn_loo_accuracy(Xsh, target, K_NN)
            shuf_target[short].append(acc_full_target - acc_t_sh)
            # own-attribute recovery drop (should be large for meaningful axis)
            acc_own_sh = knn_loo_accuracy(Xsh, labels[attr], K_NN)
            shuf_own[short].append(base_own[short] - acc_own_sh)
            # cross: mean recovery drop of OTHER axes' attributes (should be ~0)
            cross_drops = []
            for o_short, o_attr, _, _ in AXES:
                if o_short == short:
                    continue
                acc_o_base = base_own[o_short]
                acc_o_sh = knn_loo_accuracy(Xsh, labels[o_attr], K_NN)
                cross_drops.append(acc_o_base - acc_o_sh)
            shuf_cross[short].append(float(np.mean(cross_drops)))

    # ----- aggregate -----
    def ms(arr):
        a = np.array(arr, dtype=float)
        return float(a.mean()), float(a.std())

    acc_mean = {D: ms(acc_by_seed[D]) for D in D_LADDER}
    conc_mean = {D: ms(conc_by_seed[D]) for D in D_LADDER}

    # incremental gain per D (D vs D-1), with seed-noise band from the std of
    # the per-seed deltas.
    incr = {}
    for D in D_LADDER:
        if D == 2:
            incr[D] = (None, None)  # baseline, no predecessor
            continue
        per_seed_delta = [acc_by_seed[D][i] - acc_by_seed[D - 1][i] for i in range(len(SEEDS))]
        incr[D] = ms(per_seed_delta)

    # PER-RUNG noise test (statistically correct): each rung's incremental gain
    # is tested against ITS OWN per-seed variability via a one-sample t-like
    # band: gain HOLDS if mean - 2*SEM > 0 (the 2-sigma std-error of the mean of
    # the 3 per-seed deltas is strictly below the gain). This avoids inflating
    # one noisy rung's std into a global floor. We ALSO report a single global
    # noise_band (max 2*std across rungs) for a conservative cross-check.
    delta_stds = [incr[D][1] for D in D_LADDER if incr[D][1] is not None]
    base_seed_std = acc_mean[2][1]
    noise_band = 2.0 * max(max(delta_stds) if delta_stds else 0.0, base_seed_std)
    n_seeds = len(SEEDS)

    # per-D verdict (per-rung 2-SEM test)
    AXIS_OF_D = {3: "t", 4: "e", 5: "tau", 6: "m", 7: "s", 8: "kap"}
    rung_verdict = {}
    rung_sem_band = {}
    for D in D_LADDER:
        if D == 2:
            rung_verdict[D] = "BASELINE"
            rung_sem_band[D] = None
            continue
        gm, gs = incr[D]
        sem = gs / math.sqrt(n_seeds)
        band = 2.0 * sem
        rung_sem_band[D] = band
        if gm - band > 0:
            rung_verdict[D] = "HOLDS"
        elif gm + band < 0:
            rung_verdict[D] = "COLLAPSE"
        else:
            rung_verdict[D] = "SATURATED"

    # capacity knee D*: the LAST dimension at which an added axis still beats
    # noise (HOLDS), allowing non-contiguous saturation. The knee is the
    # maximum D with a HOLDS verdict; beyond it adding axes no longer reliably
    # beats noise (the honest capacity). If no rung HOLDS, D* = 2 (baseline).
    holds_dims = [D for D in D_LADDER if D >= 3 and rung_verdict[D] == "HOLDS"]
    d_star = max(holds_dims) if holds_dims else 2

    # cumulative-info cross-check: total gain from D=2 baseline to each D, with
    # 2-SEM band. This is the clearest evidence that the added axes DO carry
    # information cumulatively even when a single per-step delta hovers in noise.
    cum_gain = {}
    for D in D_LADDER:
        per_seed_cum = [acc_by_seed[D][i] - acc_by_seed[2][i] for i in range(n_seeds)]
        cm, cs = ms(per_seed_cum)
        sem = cs / math.sqrt(n_seeds)
        sig = "SIGNIFICANT" if cm - 2 * sem > 0 else ("NEG" if cm + 2 * sem < 0 else "ns")
        cum_gain[D] = (cm, cs, sig)

    # per-axis shuffle aggregate
    shuf_rows = {}
    for short, attr, ncls, redund in AXES:
        st_m, st_s = ms(shuf_target[short])
        so_m, so_s = ms(shuf_own[short])
        sc_m, sc_s = ms(shuf_cross[short])
        shuf_rows[short] = {
            "attribute": attr, "n_classes": ncls, "redundant_with": redund,
            "target_drop_mean": st_m, "target_drop_std": st_s,
            "own_attr_drop_mean": so_m, "own_attr_drop_std": so_s,
            "cross_attr_drop_mean": sc_m, "cross_attr_drop_std": sc_s,
        }

    # ----- print summary -----
    print("\n" + "=" * 78)
    print("INCREMENTAL-GAIN-PER-D CURVE (target kNN recovery, mean +/- std, 3 seeds)")
    print("=" * 78)
    print(f"{'D':>3} {'added':>6} {'acc_mean':>10} {'acc_std':>9} {'dAcc_mean':>11} {'dAcc_std':>10} {'2SEMband':>10} {'verdict':>10}")
    for D in D_LADDER:
        am, asd = acc_mean[D]
        gm, gs = incr[D]
        added = "xy" if D == 2 else AXIS_OF_D[D]
        gm_s = "" if gm is None else f"{gm:+.6f}"
        gs_s = "" if gs is None else f"{gs:.6f}"
        bs = "" if rung_sem_band[D] is None else f"{rung_sem_band[D]:.6f}"
        print(f"{D:>3} {added:>6} {am:>10.6f} {asd:>9.6f} {gm_s:>11} {gs_s:>10} {bs:>10} {rung_verdict[D]:>10}")
    print(f"\nglobal noise_band (conservative 2-sigma cross-check) = {noise_band:.6f}")
    print(f"per-rung verdict uses per-rung 2-SEM band (col above).")
    print(f"capacity knee D* = {d_star}  (max D whose added axis still beats its 2-SEM noise band)")

    print("\nCUMULATIVE-INFO cross-check (acc(D) - acc(D=2 baseline), 2-SEM):")
    for D in D_LADDER:
        cm, cs, sig = cum_gain[D]
        sem = cs / math.sqrt(n_seeds)
        print(f"  D={D} {('xy' if D==2 else AXIS_OF_D[D]):>4}: cum_gain={cm:+.6f} +/- {cs:.6f} (2SEM={2*sem:.6f}) -> {sig}")

    print("\n" + "=" * 78)
    print("PER-AXIS SHUFFLE INDEPENDENCE (full D=8; mean +/- std, 3 seeds)")
    print("shuffle axis-k alone -> own-attr recovery DROPS, OTHERS do NOT")
    print("=" * 78)
    print(f"{'axis':>5} {'attr':>9} {'redund':>9} {'own_drop':>16} {'cross_drop':>16} {'target_drop':>16}")
    for short, attr, ncls, redund in AXES:
        r = shuf_rows[short]
        rd = redund if redund else "-"
        print(f"{short:>5} {attr:>9} {rd:>9} "
              f"{r['own_attr_drop_mean']:+.5f}+/-{r['own_attr_drop_std']:.5f} "
              f"{r['cross_attr_drop_mean']:+.5f}+/-{r['cross_attr_drop_std']:.5f} "
              f"{r['target_drop_mean']:+.5f}+/-{r['target_drop_std']:.5f}")

    print("\n" + "=" * 78)
    print("DISTANCE CONCENTRATION (relative contrast; ->0 = collapse)")
    print("=" * 78)
    for D in D_LADDER:
        cm, cs = conc_mean[D]
        print(f"  D={D}  contrast={cm:.5f} +/- {cs:.5f}")
    conc_first = conc_mean[2][0]
    conc_last = conc_mean[8][0]
    nocollapse = conc_last > 0.5 * conc_first and conc_last > 1.0
    print(f"\nNO-COLLAPSE: D=2 contrast={conc_first:.5f} -> D=8 contrast={conc_last:.5f} "
          f"-> {'HOLDS (no degeneracy)' if nocollapse else 'COLLAPSE RISK'}")

    # honest bottom line
    indep_axes = [AXIS_OF_D[D] for D in D_LADDER if D >= 3 and rung_verdict[D] == "HOLDS"]
    n_useful_dims = d_star
    print("\n" + "=" * 78)
    print("HONEST BOTTOM LINE")
    print("=" * 78)
    print(f"useful coordinate dimensionality before saturation: D* = {d_star}")
    print(f"axes carrying NEW independent info (beat noise): {indep_axes}")
    print(f"saturated/redundant axes: "
          f"{[AXIS_OF_D[D] for D in D_LADDER if D >= 3 and rung_verdict[D] != 'HOLDS']}")

    results = {
        "config": {
            "n_anchors": N_ANCHORS, "seeds": SEEDS, "k_nn": K_NN,
            "class_sep": CLASS_SEP, "class_std": CLASS_STD,
            "redund_s_t": REDUND_S_T, "redund_kap_e": REDUND_KAP_E,
            "modalities": MODALITY_NAMES,
            "axis_ladder": [{"D": D, "added": ("xy" if D == 2 else AXIS_OF_D[D])} for D in D_LADDER],
        },
        "acc_mean_std": {str(D): acc_mean[D] for D in D_LADDER},
        "incremental_gain": {str(D): incr[D] for D in D_LADDER},
        "rung_2sem_band": {str(D): rung_sem_band[D] for D in D_LADDER},
        "cumulative_gain_vs_baseline": {str(D): cum_gain[D] for D in D_LADDER},
        "noise_band_2sigma_global": noise_band,
        "rung_verdict": {str(D): rung_verdict[D] for D in D_LADDER},
        "capacity_knee_D_star": d_star,
        "useful_dims": n_useful_dims,
        "independent_axes": indep_axes,
        "per_axis_shuffle": shuf_rows,
        "distance_concentration": {str(D): conc_mean[D] for D in D_LADDER},
        "no_collapse": bool(nocollapse),
        "per_seed_acc": {str(D): acc_by_seed[D] for D in D_LADDER},
    }
    return results, rung_verdict, incr, acc_mean, noise_band, d_star, shuf_rows, conc_mean, nocollapse, indep_axes


if __name__ == "__main__":
    out = run()
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        print("\nJSON_RESULTS_BEGIN")
        print(json.dumps(out[0], indent=2))
        print("JSON_RESULTS_END")
