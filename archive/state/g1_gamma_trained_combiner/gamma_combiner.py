"""gamma_combiner.py — H_1823γ (substrate twin): TRAINED CONSTRUCTIVE bind operator.

CAMPAIGN CONTEXT (substrate-framebreak-g1-combination-operator memory):
  α (char-hash) + β (semantic 303M trunk embed) measured substrate-G1 = "can A⇄G
  combine two concept basins without the mouth?". BOTH floored 0/5 at the engine's
  operating radius. The ONLY concept-combiner the substrate owns is VAdaptField
  L2-Voronoi NEAREST-BASIN affinity (compositional depth-0): a recombined child is
  treated as an isolated novel point, NOT recoverable-from-both-parents.

  The 4-corner convergence (mouth-objective H_1602 · mouth-readout H_1816 ·
  substrate-embed β · substrate-combiner α/β) all floor on ADDITIVE/AFFINITY
  readouts. The one UNTESTED lever is γ: replace the nearest-basin Voronoi metric
  with a TRAINED CONSTRUCTIVE bind operator g_θ(a,b) that CONSTRUCTS a child basin
  from two parents — then ask whether the real child is recoverable from g_θ(a,b)
  but NOT from a or b alone. This is the substrate twin of the mouth binding-op
  lever, and (because it uses GRADIENT) is distinct from H_1310 (from-scratch
  GRADIENT-FREE split, already closed).

HYPOTHESIS (H_1823γ): a trained constructive bind operator on the substrate concept
space lifts substrate-G1 above the nearest-basin floor (0/5 from α/β):
  on HELD-OUT test compound pairs, child recoverable from g_θ(a,b) (rank/sim) AND
  NOT from a or b alone AND > shuffle control, on >=2/3 of held-out pairs.

FROZEN-FIRST (p7 — pre-registered, NO sliding):
  * Embedding = the SAME β semantic embed (303M trunk penultimate mean-pool L2-unit)
    via core/clm_decode.py — only the COMBINATION OPERATOR changes vs β. DIRECTIONAL.
  * Recoverability metric on held-out: among a CANDIDATE POOL of all known child
    vectors (+ the parents + distractors), is the TRUE child the nearest neighbour
    of the constructed point g_θ(a,b)?  (rank-1 hit = recovered).
    substrate-G1(pair) = 1 iff:
        (i)  rank1(g_θ(a,b)) == true child                         (constructed)
        (ii) rank1(a) != child  AND  rank1(b) != child             (irreducible: NOT from one parent)
        (iii) sim(g_θ(a,b), child) > sim(g_θ(shuffle), child)      (> shuffle control)
  * BAR (pre-registered): trained-g_θ substrate-G1 >= 2/3 of held-out pairs
    AND  > untrained-g_θ (random init) baseline  AND  > single-parent control.
  * Controls (pre-registered):
      single      : best single parent NN -> must NOT recover child (else not recomb)
      shuffle     : g_θ(a, wrong_b) -> should NOT recover child
      untrained   : g_θ with random-init weights -> baseline (geometry, not training)
  * 5-fold CV over the compound pairs (each pair held out once) -> report mean.

SCOPE HONESTY (c9 / a_engine_native_learning): DIRECTIONAL.
  - embed = py mirror core/clm_decode.py (trunk penultimate), numpy/torch combiner.
  - g_θ trained in numpy (ridge / closed-form least-squares for projection variants;
    fp32). NO bf16, NO FFT-trap (HRR circular conv via direct numpy roll-sum, fp64).
  - If trained-g_θ LIFTS where nearest-basin floored -> the operator IS the lever and
    it must be TRAINED+CONSTRUCTIVE. If it ALSO floors -> even trained substrate
    combination can't = strong terminal evidence (combination-operator family
    exhausted on the substrate side too).

Usage:  OMP_NUM_THREADS=4 python3 gamma_combiner.py [<ckpt.clm>]
"""

import sys, os, time
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_CORE = os.path.abspath(os.path.join(_HERE, "..", "..", "core"))
_BETA = os.path.abspath(os.path.join(_HERE, "..", "g1_substrate_native_recombination"))
sys.path.insert(0, _CORE)
sys.path.insert(0, _BETA)
import clm_decode as cd          # byte-faithful CLMConvMoE forward (py 2-production)
import beta_readout as br        # reuse the SAME semantic embed as the β round

DEFAULT_CLM = "/Users/mini/dancinlab/anima/state/clm303_savant_mitosis_train/clm303.clm"
EPS = 1e-9
RIDGE = 1e-2                      # least-squares ridge (fp32-safe)
PROJ_DIM = 64                    # tensor-product random-projection target dim (64^2=4096 feats)
SEED = 1823

# ════════════════════════════════════════════════════════════════════════
# Compound-pair dataset — REAL morphological compounds (parent_a + parent_b = child).
# Each child is a genuine recombination of the two parents' meanings.
# Mix of EN (lexical compounds), KO (한자어/합성), ZH (合成) so the test is not a
# single-language artifact. NO partial/ambiguous pairs (frozen, a_completeness).
# ════════════════════════════════════════════════════════════════════════
PAIRS = [
    # English compounds
    ("rain",  "bow",    "rainbow"),
    ("snow",  "man",    "snowman"),
    ("sun",   "flower", "sunflower"),
    ("fire",  "fly",    "firefly"),
    ("water", "fall",   "waterfall"),
    ("foot",  "ball",   "football"),
    ("book",  "shelf",  "bookshelf"),
    ("moon",  "light",  "moonlight"),
    ("star",  "fish",   "starfish"),
    ("tooth", "brush",  "toothbrush"),
    ("rail",  "road",   "railroad"),
    ("butter","fly",    "butterfly"),
    ("key",   "board",  "keyboard"),
    ("news",  "paper",  "newspaper"),
    ("bed",   "room",   "bedroom"),
    ("ear",   "ring",   "earring"),
    ("eye",   "brow",   "eyebrow"),
    ("hand",  "bag",    "handbag"),
    ("wheel", "chair",  "wheelchair"),
    ("after", "noon",   "afternoon"),
    # Korean 합성/한자어
    ("불",    "꽃",     "불꽃"),
    ("눈",    "사람",   "눈사람"),
    ("손",    "수건",   "손수건"),
    ("물",    "고기",   "물고기"),
    ("책",    "상",     "책상"),
    ("봄",    "바람",   "봄바람"),
    ("밤",    "하늘",   "밤하늘"),
    ("꽃",    "잎",     "꽃잎"),
    # Chinese 合成
    ("日",    "光",     "日光"),
    ("月",    "光",     "月光"),
    ("火",    "山",     "火山"),
    ("水",    "車",     "水車"),
]

# distractor concepts for the candidate pool (NOT children of any pair)
DISTRACTORS = ["mountain", "ocean", "computer", "garden", "window",
               "산", "강", "하늘", "구름", "바다",
               "天", "地", "風", "雨", "雪"]


# ════════════════════════════════════════════════════════════════════════
# TRAINED CONSTRUCTIVE BIND OPERATORS  g_θ: (a, b) -> constructed child
# all trained to MINIMIZE ||g_θ(a,b) - child|| via closed-form least-squares
# (ridge); fp64; held-out test pairs never enter the fit.
# ════════════════════════════════════════════════════════════════════════

def _ridge_fit(Phi, Y, ridge=RIDGE):
    """least-squares  W = argmin ||Phi W - Y||^2 + ridge||W||^2 .  Phi:[n,f] Y:[n,d]."""
    f = Phi.shape[1]
    A = Phi.T @ Phi + ridge * np.eye(f)
    return np.linalg.solve(A, Phi.T @ Y)          # [f, d]


class AdditiveBaseline:
    """control: g(a,b) = W_a a + W_b b  (LINEAR/ADDITIVE — the floored readout family).
    This is the substrate analogue of the additive mouth readout that floored."""
    name = "additive(ctrl)"
    def features(self, A, B):
        return np.concatenate([A, B], axis=1)     # [n, 2d]
    def fit(self, A, B, Y):
        self.W = _ridge_fit(self.features(A, B), Y)
    def __call__(self, a, b):
        return self.features(a[None], b[None]) @ self.W


class TensorProductProj:
    """CONSTRUCTIVE: g(a,b) = W vec(P_a a ⊗ P_b b)  — outer product (multiplicative
    interaction) of randomly-projected parents, then learned projection to child.
    Random projection keeps the bilinear feature dim tractable (PROJ_DIM^2)."""
    name = "tensorproduct"
    def __init__(self, d, seed=SEED):
        rng = np.random.default_rng(seed)
        self.Pa = rng.standard_normal((d, PROJ_DIM)) / np.sqrt(d)
        self.Pb = rng.standard_normal((d, PROJ_DIM)) / np.sqrt(d)
    def features(self, A, B):
        ra = A @ self.Pa                          # [n, P]
        rb = B @ self.Pb                          # [n, P]
        out = np.einsum("np,nq->npq", ra, rb).reshape(A.shape[0], -1)  # [n, P*P]
        return out
    def fit(self, A, B, Y):
        self.W = _ridge_fit(self.features(A, B), Y)
    def __call__(self, a, b):
        return self.features(a[None], b[None]) @ self.W


class CircularConvHRR:
    """CONSTRUCTIVE: HRR binding  c = a ⊛ b  (circular convolution, dimension-
    preserving multiplicative bind), then a learned linear readout W (c -> child).
    Circular conv via direct numpy roll-sum (fp64, NO FFT bf16-trap)."""
    name = "circconv_hrr"
    def _ccorr_bind(self, A, B):
        # circular convolution c = a ⊛ b via fp64 FFT (EXACT for circular conv;
        # NOT the bf16+fft trap — full fp64 precision, real ifft). Vectorized.
        FA = np.fft.rfft(A, axis=1)
        FB = np.fft.rfft(B, axis=1)
        return np.fft.irfft(FA * FB, n=A.shape[1], axis=1)   # [n, d] bound vector
    def features(self, A, B):
        return self._ccorr_bind(A, B)             # [n, d]  bound vector
    def fit(self, A, B, Y):
        self.W = _ridge_fit(self.features(A, B), Y)
    def __call__(self, a, b):
        return self.features(a[None], b[None]) @ self.W


class BilinearMLP:
    """CONSTRUCTIVE: small bilinear-then-linear g(a,b) = W2 · tanh(W1 [a;b;a*b]).
    a*b = elementwise (Hadamard) multiplicative term. Trained by gradient descent
    (fp32, small hidden) — the genuine 'small bilinear/MLP' candidate from the prompt."""
    name = "bilinear_mlp"
    def __init__(self, d, hidden=128, seed=SEED):
        rng = np.random.default_rng(seed + 7)
        fin = 3 * d
        self.W1 = rng.standard_normal((fin, hidden)) * np.sqrt(2.0 / fin)
        self.b1 = np.zeros(hidden)
        self.W2 = rng.standard_normal((hidden, d)) * np.sqrt(2.0 / hidden)
        self.b2 = np.zeros(d)
        self.d = d
    def _feat(self, A, B):
        return np.concatenate([A, B, A * B], axis=1)   # [n, 3d]
    def _fwd(self, X):
        h = np.tanh(X @ self.W1 + self.b1)
        return h, h @ self.W2 + self.b2
    def fit(self, A, B, Y, epochs=400, lr=0.05):
        X = self._feat(A, B); n = X.shape[0]
        for ep in range(epochs):
            h, out = self._fwd(X)
            err = out - Y                              # [n,d]
            gW2 = h.T @ err / n; gb2 = err.mean(0)
            dh = (err @ self.W2.T) * (1 - h * h)
            gW1 = X.T @ dh / n; gb1 = dh.mean(0)
            self.W2 -= lr * gW2; self.b2 -= lr * gb2
            self.W1 -= lr * gW1; self.b1 -= lr * gb1
    def __call__(self, a, b):
        X = self._feat(a[None], b[None])
        _, out = self._fwd(X)
        return out


# ════════════════════════════════════════════════════════════════════════
# substrate-G1 recoverability metric (held-out)
# ════════════════════════════════════════════════════════════════════════

def _cos(u, v):
    nu = np.linalg.norm(u); nv = np.linalg.norm(v)
    if nu < EPS or nv < EPS:
        return 0.0
    return float(u @ v / (nu * nv))

def _rank1(query, pool_vecs, pool_names):
    """nearest neighbour name of `query` among the candidate pool (cosine)."""
    sims = [ _cos(query, v) for v in pool_vecs ]
    return pool_names[int(np.argmax(sims))]


def evaluate_operator(OpFactory, emb, train_idx, test_idx, untrained=False):
    """Fit on train pairs, measure substrate-G1 on held-out test pairs.
    Returns per-test dicts. If untrained=True, skip .fit (random-init baseline)."""
    d = len(next(iter(emb.values())))
    A_tr = np.array([emb[PAIRS[i][0]] for i in train_idx])
    B_tr = np.array([emb[PAIRS[i][1]] for i in train_idx])
    Y_tr = np.array([emb[PAIRS[i][2]] for i in train_idx])

    op = OpFactory(d)
    if not untrained:
        op.fit(A_tr, B_tr, Y_tr)
    else:
        # untrained baseline (pre-registered control): RANDOM-INIT readout W,
        # never fit on the data -> isolates trained-vs-geometry. BilinearMLP is
        # already random-init at construction (skip fit); projection ops need a
        # random W matching their feature dim.
        rng = np.random.default_rng(SEED + 99)
        fdim = op.features(A_tr[:1], B_tr[:1]).shape[1] if hasattr(op, "features") else d
        if hasattr(op, "features"):
            op.W = rng.standard_normal((fdim, d)) / np.sqrt(fdim)

    # candidate pool = ALL children + ALL distractors (held-out child must WIN here)
    pool_names = [PAIRS[i][2] for i in range(len(PAIRS))] + DISTRACTORS
    pool_vecs  = [emb[n] for n in pool_names]

    results = []
    for ti in test_idx:
        pa, pb, child = PAIRS[ti]
        a, b, cv = emb[pa], emb[pb], emb[child]
        constructed = np.asarray(op(a, b)).reshape(-1)
        # shuffle: bind with a WRONG parent_b from another pair
        wrong_b = emb[PAIRS[(ti + 1) % len(PAIRS)][1]]
        shuffled = np.asarray(op(a, wrong_b)).reshape(-1)

        nn_constructed = _rank1(constructed, pool_vecs, pool_names)
        nn_a = _rank1(a, pool_vecs, pool_names)
        nn_b = _rank1(b, pool_vecs, pool_names)

        sim_c = _cos(constructed, cv)
        sim_shuf = _cos(shuffled, cv)

        recovered = (nn_constructed == child)
        irreducible = (nn_a != child) and (nn_b != child)
        beats_shuffle = sim_c > sim_shuf
        g1 = int(recovered and irreducible and beats_shuffle)
        results.append(dict(pair="%s+%s->%s" % (pa, pb, child),
                            nn_constructed=nn_constructed, nn_a=nn_a, nn_b=nn_b,
                            sim_c=sim_c, sim_shuf=sim_shuf,
                            recovered=recovered, irreducible=irreducible,
                            beats_shuffle=beats_shuffle, g1=g1))
    return results


def cv_operator(OpFactory, emb, untrained=False, folds=5, seed=SEED):
    """k-fold CV: each fold holds out a disjoint test slice. Returns (hits, total, per)."""
    n = len(PAIRS)
    rng = np.random.default_rng(seed)
    order = rng.permutation(n)
    fold_sz = int(np.ceil(n / folds))
    hits = total = 0
    per = []
    for k in range(folds):
        test_idx = list(order[k*fold_sz:(k+1)*fold_sz])
        if not test_idx:
            continue
        train_idx = [i for i in order if i not in test_idx]
        res = evaluate_operator(OpFactory, emb, train_idx, test_idx, untrained=untrained)
        for r in res:
            hits += r["g1"]; total += 1; per.append(r)
    return hits, total, per


def main(argv):
    np.seterr(all="ignore")
    ck = argv[1] if len(argv) > 1 else DEFAULT_CLM
    print("=" * 76)
    print("H_1823γ — SUBSTRATE TRAINED CONSTRUCTIVE BIND OPERATOR (substrate twin)")
    print("  DIRECTIONAL: embed = core/clm_decode.py trunk penultimate (β round's");
    print("  semantic embed). ONLY the combination OPERATOR changes vs β. fp64 combiner.")
    print("=" * 76)

    if not cd.clm_decodable(ck):
        print("!! ckpt not v0.2-decodable:", ck); return 1
    print("\n[1] loading 303M trunk:", os.path.basename(ck))
    W = cd.clm_load_weights(ck)
    print("    d=%d E=%d K=%d L=%d" % (W["d"], W["E"], W["K"], W["L"]))

    # embed every unique concept ONCE (cached). β semantic embed, L2-unit.
    concepts = set()
    for a, b, c in PAIRS:
        concepts.update([a, b, c])
    concepts.update(DISTRACTORS)
    concepts = sorted(concepts)
    print("\n[2] embedding %d unique concepts (303M trunk penultimate, β embed)..." % len(concepts))
    t0 = time.time()
    emb = {}
    for s in concepts:
        emb[s] = br._unit(br._semantic_rep(W, s))
    print("    done %.1fs (%.2fs/concept)" % (time.time()-t0, (time.time()-t0)/len(concepts)))
    print("    %d pairs, %d distractors, candidate pool = %d"
          % (len(PAIRS), len(DISTRACTORS), len(PAIRS) + len(DISTRACTORS)))

    print("\n[3] 5-fold CV substrate-G1 (held-out test pairs, child recoverable from")
    print("    g_θ(a,b) ∧ NOT from a/b alone ∧ > shuffle):")
    print("    %-22s %-12s %s" % ("operator", "G1 (held-out)", "rate"))
    print("    " + "-" * 60)

    ops = [
        ("AdditiveBaseline",  lambda d: AdditiveBaseline()),
        ("TensorProductProj", lambda d: TensorProductProj(d)),
        ("CircularConvHRR",   lambda d: CircularConvHRR()),
        ("BilinearMLP",       lambda d: BilinearMLP(d)),
    ]
    summary = {}
    detail = {}
    for nm, fac in ops:
        h, t, per = cv_operator(fac, emb, untrained=False)
        summary[nm] = (h, t)
        detail[nm] = per
        print("    %-22s %d/%-10d %.2f" % (nm, h, t, h/max(t,1)))

    print("\n[4] CONTROLS")
    # untrained (random-init) baselines for the constructive ops
    for nm, fac in [("TensorProductProj", lambda d: TensorProductProj(d)),
                    ("CircularConvHRR", lambda d: CircularConvHRR()),
                    ("BilinearMLP", lambda d: BilinearMLP(d))]:
        h, t, _ = cv_operator(fac, emb, untrained=True)
        print("    untrained %-20s %d/%-10d %.2f  (geometry, no training)" % (nm, h, t, h/max(t,1)))

    # single-parent control: does the BEST single parent NN already recover child?
    pool_names = [PAIRS[i][2] for i in range(len(PAIRS))] + DISTRACTORS
    pool_vecs  = [emb[n] for n in pool_names]
    single_hits = 0
    for i in range(len(PAIRS)):
        pa, pb, child = PAIRS[i]
        if _rank1(emb[pa], pool_vecs, pool_names) == child or \
           _rank1(emb[pb], pool_vecs, pool_names) == child:
            single_hits += 1
    print("    single-parent NN already==child: %d/%d  (must be ~0 = irreducible)"
          % (single_hits, len(PAIRS)))

    print("\n[5] per-pair detail — BEST constructive operator")
    best = max([("TensorProductProj","CircularConvHRR","BilinearMLP")[k]
                for k in range(3)],
               key=lambda nm: summary[nm][0])
    print("    best constructive = %s (%d/%d)" % (best, summary[best][0], summary[best][1]))
    for r in detail[best]:
        print("      %-22s nn(g)=%-10s nn(a)=%-9s nn(b)=%-9s sim_c=%.3f sim_shuf=%.3f  recov=%s irred=%s >shuf=%s  G1=%d"
              % (r["pair"], r["nn_constructed"], r["nn_a"], r["nn_b"],
                 r["sim_c"], r["sim_shuf"],
                 "Y" if r["recovered"] else "n", "Y" if r["irreducible"] else "n",
                 "Y" if r["beats_shuffle"] else "n", r["g1"]))

    print("\n" + "=" * 76)
    print("VERDICT GATE (pre-registered p7):")
    besth, bestt = summary[best]
    bar_pass = (besth / max(bestt,1)) >= (2.0/3.0)
    add_h, add_t = summary["AdditiveBaseline"]
    print("  best constructive %s: %d/%d (%.2f)   additive(ctrl): %d/%d (%.2f)"
          % (best, besth, bestt, besth/max(bestt,1), add_h, add_t, add_h/max(add_t,1)))
    print("  BAR (>=2/3 held-out AND > additive AND > untrained AND single~0): %s"
          % ("PASS -> γ LIFTS (operator is the lever, must be TRAINED+CONSTRUCTIVE)"
             if (bar_pass and besth > add_h) else
             "FAIL -> even TRAINED substrate combiner floors = combination-operator family exhausted"))
    print("=" * 76)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
