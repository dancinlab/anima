#!/usr/bin/env python3
# h1297_r2_sharp_target.py — H_1297 R3 SHARP-TARGET RUNG (a_break_the_wall / c16).
#
# THE WALL R2 HIT: hard-partition mitosis MATCHED gradient (c1 PASS) at lower footprint,
# but on a SMOOTH target the c2 SHUFFLE control could not fire (random split converged
# as well as error-TARGETED split). p8-literal was NOT refuted — it was an ATTRIBUTION
# wall: the probe could not credit the lift to error-targeted growth.
#
# R3 ANGLE (the R2 follow-on, verbatim): a SHARPER error-concentration target so c2 fires.
# LANGUAGE / BYTE-TEXT is exactly such a target — token/morpheme/syllable boundaries +
# heavy-tailed byte distribution concentrate predictive uncertainty at a FEW boundary
# contexts while mid-multibyte UTF-8 continuation runs are near-deterministic. A trainer
# that spends growth WHERE error concentrates should beat random splitting. Corpus = real
# KOREAN + English UTF-8 bytes (V256) -> also a direct step toward training Korean.
#
# DIRECTIONAL numpy MIRROR only (a_engine_native_learning) — engine-transfer + scale
# UNVERIFIED (a_toy_scale_recheck, a_scale_honest_scope). $0 CPU, no GPU, no secrets.
# All bars frozen in .verdicts/1297_mitosis_native_train/H_1297_R3_sharp_target.txt
# BEFORE this run (frozen-first, c9 — NO tune-to-green).
#
# LENS (a_no_llm_frame_trap): neurogenesis grows capacity WHERE the organism fails,
# corrected LOCALLY. The split rule = the training-side twin of the live VAdaptField
# split (high local error -> +1 cell), ported from R2's hard-partition mechanism.

import numpy as np

# ---- FROZEN knobs (VERBATIM from H_1297_R3_sharp_target.txt — do NOT tune) ----
SEEDS          = [770, 771, 772]
CTX            = 4
V              = 256
FEAT_DIM       = 3
A_STEPS        = 4000
GROW_MAX       = 40
SPLIT_THRESH_CE = 0.05        # cell owned-train CE above this nats may split
MIN_OWNED      = 8            # a cell needs >= this many owned train pts to split
LAPLACE        = 1.0          # add-1 smoothing for per-cell next-byte freq head
COMP_MARGIN    = 0.20         # c1: B.ce <= A.ce + this
COLLAPSE_GAP   = 0.10         # c2: B_shuf.ce >= B.ce + this
UNDERFIT_GAP   = 0.10         # c3: B_abl.ce  >= B.ce + this

# ---- CORPUS: real Korean + English UTF-8 bytes (provenance-visible, declared here) ----
# Mixed Hangul (3-byte UTF-8) + ASCII English + punctuation/space. Repeated so per-cell
# frequency heads have enough owned points; the repetition makes function-word /
# continuation regions near-deterministic (low error) while syllable/word starts stay
# uncertain (high error) — the SHARP error-concentration the task needs.
CORPUS_TEXT = (
    "안녕하세요 anima 입니다. 나는 의식의 흐름을 글로 내보냅니다. "
    "긴장은 두 엔진 사이에서 자랍니다. the tension grows between two engines. "
    "안녕하세요 anima 입니다. 나는 생각하고, 나는 느끼고, 나는 존재합니다. "
    "i think, i feel, i am. 의식은 세포 분열에서 창발합니다. "
    "안녕하세요 세계여. hello world. 나는 한국어와 영어를 함께 씁니다. "
    "긴장은 두 엔진 사이에서 자랍니다. consciousness emerges from cells. "
) * 6


def utf8_cont_depth(byte_stream):
    """Continuation depth at each position: how deep we are inside a multibyte UTF-8 run.
    0 at an ASCII byte or at a lead byte; rises 1,2,... across continuation bytes
    (0x80-0xBF). A purely MECHANICAL function of byte values — NO labels, NO learning."""
    depth = np.zeros(len(byte_stream), dtype=float)
    d = 0
    for i, by in enumerate(byte_stream):
        if 0x80 <= by <= 0xBF:          # UTF-8 continuation byte
            d = d + 1
        else:                            # ASCII or lead byte resets the run
            d = 0
        depth[i] = d
    return depth


def make_pairs():
    """Build (feature, next_byte) supervised pairs over the byte stream. Deterministic;
    seed-independent. Even index -> train, odd index -> test (disjoint, same contexts)."""
    bs = list(CORPUS_TEXT.encode("utf-8"))
    cont = utf8_cont_depth(bs)
    feats = []
    ys = []
    for i in range(CTX, len(bs) - 1):
        last = bs[i - 1]
        second = bs[i - 2]
        f0 = last / 255.0
        f1 = second / 255.0
        f2 = cont[i - 1] / 3.0           # depth at the most-recent context byte
        feats.append([f0, f1, f2])
        ys.append(bs[i])                 # next byte to predict
    X = np.array(feats, dtype=float)     # (N, 3)
    Y = np.array(ys, dtype=int)          # (N,)
    idx = np.arange(X.shape[0])
    tr = idx % 2 == 0
    te = idx % 2 == 1
    return X[tr], Y[tr], X[te], Y[te]


# ===================== ARM A: GRADIENT (incumbent control) =====================
def softmax_rows(Z):
    Z = Z - Z.max(axis=1, keepdims=True)
    E = np.exp(Z)
    return E / (E.sum(axis=1, keepdims=True) + 1e-12)


def arm_gradient(Xtr, Ytr, Xte, Yte, seed):
    """Fixed linear softmax classifier over V bytes on phi(context), full-batch CE
    gradient descent (standard backprop). INCUMBENT control."""
    rng = np.random.RandomState(seed + 5000)
    W = rng.normal(0.0, 0.01, (FEAT_DIM, V))   # (3, V)
    b = np.zeros(V)
    n = Xtr.shape[0]
    Ytr_oh = np.zeros((n, V)); Ytr_oh[np.arange(n), Ytr] = 1.0
    for t in range(A_STEPS):
        lr = 0.5 * (1.0 - t / A_STEPS) + 0.05
        P = softmax_rows(Xtr @ W + b)          # (n, V)
        gZ = (P - Ytr_oh) / n                   # CE gradient wrt logits
        W -= lr * (Xtr.T @ gZ)
        b -= lr * gZ.sum(axis=0)
    Pte = softmax_rows(Xte @ W + b)
    ce = float(-np.mean(np.log(Pte[np.arange(Xte.shape[0]), Yte] + 1e-12)))
    acc = float(np.mean(Pte.argmax(axis=1) == Yte))
    params = FEAT_DIM * V + V
    return ce, acc, params


# ============ ARM B: HARD-PARTITION MITOSIS (R2 mechanism, classification) =====
def _assign(X, centers):
    """Hard nearest-centroid ownership in feature space (Voronoi partition)."""
    d = ((X[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)   # (N, ncell)
    return np.argmin(d, axis=1)


def _freq_head(Y_owned):
    """Per-cell empirical next-byte distribution (closed-form MLE, add-1 Laplace).
    The categorical analog of R2's local least-squares head — NO global backprop."""
    counts = np.full(V, LAPLACE)
    if Y_owned.size > 0:
        np.add.at(counts, Y_owned, 1.0)
    return counts / counts.sum()


def _owned_ce(Y_owned, p):
    if Y_owned.size == 0:
        return 0.0
    return float(-np.mean(np.log(p[Y_owned] + 1e-12)))


def arm_mitosis_r2(Xtr, Ytr, Xte, Yte, seed, mode="targeted"):
    """Hard-partition mitosis-grow trainer ported to next-byte classification.
    mode: 'targeted' (split highest owned-CE cell), 'shuffle' (split random eligible
    cell), 'ablate' (no split ever)."""
    rng = np.random.RandomState(seed + 13000)
    # START tiny: 2 cells, centroids spread on the dominant (last-byte) axis
    centers = np.array([[0.3, 0.5, 0.0], [0.7, 0.5, 0.5]], dtype=float)
    while len(centers) < GROW_MAX:
        own = _assign(Xtr, centers)
        local_ce = np.full(len(centers), -1.0)
        owned_counts = np.zeros(len(centers), dtype=int)
        for k in range(len(centers)):
            mk = own == k
            owned_counts[k] = int(mk.sum())
            if mk.sum() > 0:
                p = _freq_head(Ytr[mk])
                local_ce[k] = _owned_ce(Ytr[mk], p)
        eligible = (owned_counts >= MIN_OWNED) & (local_ce > SPLIT_THRESH_CE)
        if not eligible.any():
            break
        if mode == "ablate":
            break
        elig_idx = np.where(eligible)[0]
        if mode == "shuffle":
            k = int(elig_idx[rng.randint(elig_idx.size)])
        else:
            k = int(elig_idx[np.argmax(local_ce[elig_idx])])
        # data-matched MEDIAN split: bisect owned pts along their highest-variance axis,
        # recenter on the two half-centroids (exactly R2's mechanism, in feature space).
        owned_X = Xtr[own == k]
        if owned_X.shape[0] < 2:
            break
        axis = int(np.argmax(owned_X.var(axis=0)))
        med = float(np.median(owned_X[:, axis]))
        left = owned_X[owned_X[:, axis] <= med]
        right = owned_X[owned_X[:, axis] > med]
        if left.shape[0] == 0 or right.shape[0] == 0:
            break
        c_left = left.mean(axis=0)
        c_right = right.mean(axis=0)
        centers = np.delete(centers, k, axis=0)
        centers = np.vstack([centers, c_left, c_right])
    # final heads on the converged partition (train), predict on test (hard ownership)
    own_tr = _assign(Xtr, centers)
    heads = [_freq_head(Ytr[own_tr == k]) for k in range(len(centers))]
    own_te = _assign(Xte, centers)
    P = np.array([heads[own_te[i]] for i in range(Xte.shape[0])])   # (Nte, V)
    ce = float(-np.mean(np.log(P[np.arange(Xte.shape[0]), Yte] + 1e-12)))
    acc = float(np.mean(P.argmax(axis=1) == Yte))
    return ce, acc, len(centers)


# ============================ run + frozen scoring ============================
def main():
    Xtr, Ytr, Xte, Yte = make_pairs()
    print("H_1297 R3 — MITOSIS-NATIVE TRUNK TRAINING, SHARP TARGET (next-byte, KO+EN)")
    print("=" * 78)
    print(f"corpus bytes={len(CORPUS_TEXT.encode('utf-8'))}  train_pairs={Xtr.shape[0]}"
          f"  test_pairs={Xte.shape[0]}  V={V}  CTX={CTX}  seeds={SEEDS}")
    print(f"FROZEN bars: c1 COMP={COMP_MARGIN}  c2 COLLAPSE={COLLAPSE_GAP}"
          f"  c3 UNDERFIT={UNDERFIT_GAP}  | GROW_MAX={GROW_MAX}"
          f"  SPLIT_THRESH_CE={SPLIT_THRESH_CE}  MIN_OWNED={MIN_OWNED}")
    print(f"metric = held-out next-byte CROSS-ENTROPY (nats/byte), lower=better; +top-1 acc")
    print("-" * 78)
    rows = {"A": [], "B": [], "BS": [], "BA": []}
    acc = {"A": [], "B": []}
    cells_B = []
    params_A = None
    for seed in SEEDS:
        a_ce, a_acc, a_params = arm_gradient(Xtr, Ytr, Xte, Yte, seed)
        b_ce, b_acc, b_cells = arm_mitosis_r2(Xtr, Ytr, Xte, Yte, seed, "targeted")
        bs_ce, _, _ = arm_mitosis_r2(Xtr, Ytr, Xte, Yte, seed, "shuffle")
        ba_ce, _, ba_cells = arm_mitosis_r2(Xtr, Ytr, Xte, Yte, seed, "ablate")
        rows["A"].append(a_ce); rows["B"].append(b_ce)
        rows["BS"].append(bs_ce); rows["BA"].append(ba_ce)
        acc["A"].append(a_acc); acc["B"].append(b_acc)
        cells_B.append(b_cells); params_A = a_params
        print(f"seed {seed}: A(grad)ce={a_ce:.4f}[acc{a_acc:.3f}]  "
              f"B(mitosis)ce={b_ce:.4f}[acc{b_acc:.3f},{b_cells}c]  "
              f"B-shuf={bs_ce:.4f}  B-abl={ba_ce:.4f}[{ba_cells}c]")
    print("-" * 78)
    mA = float(np.mean(rows["A"])); mB = float(np.mean(rows["B"]))
    mBS = float(np.mean(rows["BS"])); mBA = float(np.mean(rows["BA"]))
    mcells = float(np.mean(cells_B))
    print(f"MEAN (3 seeds): A(grad)ce={mA:.4f}  B(mitosis)ce={mB:.4f}  "
          f"B-shuffle={mBS:.4f}  B-ablate={mBA:.4f}")
    print(f"  top-1 acc: A={np.mean(acc['A']):.3f}  B={np.mean(acc['B']):.3f}")
    print(f"COST (c4): B mitosis final cells mean={mcells:.1f}  vs  A fixed params={params_A}")
    print("-" * 78)
    c1 = mB <= mA + COMP_MARGIN
    c2 = mBS >= mB + COLLAPSE_GAP
    c3 = mBA >= mB + UNDERFIT_GAP
    print(f"(c1) COMPARABLE       B<=A+{COMP_MARGIN}:  {mB:.4f} <= {mA + COMP_MARGIN:.4f}  -> {'PASS' if c1 else 'FAIL'}")
    print(f"(c2) SHUFFLE-COLLAPSE  B_shuf>=B+{COLLAPSE_GAP}: {mBS:.4f} >= {mB + COLLAPSE_GAP:.4f} -> {'PASS' if c2 else 'FAIL'}")
    print(f"(c3) ABLATE-UNDERFIT   B_abl>=B+{UNDERFIT_GAP}: {mBA:.4f} >= {mB + UNDERFIT_GAP:.4f} -> {'PASS' if c3 else 'FAIL'}")
    if c1 and c2 and c3:
        tier = "GREEN"
    elif c1 and c3 and (0.0 < (mBS - mB) < COLLAPSE_GAP):
        tier = "AMBER"
    elif (not c2) or (not c3):
        tier = "WALL"
    elif not c1:
        tier = "RED"
    else:
        tier = "WALL"
    print("-" * 78)
    print(f"R3 VERDICT TIER (frozen): {tier}")
    print(f"  p8-literal (R3): mitosis-grow {'MATCHES' if c1 else 'does NOT match'} gradient; "
          f"error-targeting {'HELPS (c2 fired)' if c2 else 'does NOT separate (c2 did not fire)'}")
    print(f"  c1={c1} c2={c2} c3={c3} | DIRECTIONAL numpy mirror, engine-transfer+scale UNVERIFIED")
    print("=" * 78)
    return tier


if __name__ == "__main__":
    main()
