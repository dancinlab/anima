#!/usr/bin/env python3
# h1310_mitosis_from_scratch.py — H_1310 FROM-SCRATCH PURE MITOSIS vs GRADIENT.
#
# THE QUESTION (deepest p8): can a next-byte model be grown FROM SCRATCH by mitosis
# ALONE — seed = ONE cell, split-only under next-byte error pressure, GRADIENT-FREE —
# and how does its held-out next-byte CE compare to a gradient baseline of MATCHED
# effective capacity? Honest hypothesis to test/possibly REFUTE: pure-mitosis cells
# are LOCAL experts (Voronoi over byte-trigram context). Without a learned deep
# representation underneath, pure mitosis may plateau ABOVE gradient — it tiles the
# input space but builds no compositional depth. That ceiling, if real, is a
# first-class result (c9), NOT a failure.
#
# LENS (a_no_llm_frame_trap): cortical columns / neurogenesis grow capacity WHERE the
# organism fails, corrected LOCALLY — NOT a bigger-transformer recipe. The split rule
# is the from-scratch twin of the live VAdaptField split (high local error -> +1 cell),
# seeded at ONE cell instead of mounting a 303M trunk.
#
# DIRECTIONAL numpy MIRROR (a_engine_native_learning) — engine-transfer + scale
# UNVERIFIED (a_toy_scale_recheck, a_scale_honest_scope). $0 CPU, no GPU. p7: held-out
# next-byte CE in nats, NEVER perplexity-as-truth. Bars frozen in FREEZE.txt BEFORE run.

import hashlib
import random
import math
import numpy as np

# ---- FROZEN knobs (VERBATIM from FREEZE.txt — do NOT tune) -------------------
SEEDS        = [13101, 13102, 13103]
CORPUS_SEED  = 13100
CORPUS_BYTES = 24000
LADDER       = [1, 8, 64, 512]      # frozen cell-budget ladder
SPLIT_THRESH = 0.55                 # owned mean-error over this => an ERROR cell may split
ORDER        = 2                    # order-2 byte context (previous 2 bytes)
TRAIN_FRAC   = 0.80
A_STEPS      = 300                  # gradient baseline full-batch SGD steps
A_LR         = 0.5
SMOOTH       = 1.0                  # add-1 (Laplace) smoothing for cell + freq tables
FREEZE_SHA   = "86864aa32dcf1c8680ab254e1b28357bf0326c8d45a86837ae4e3b9d09350f62"

# frozen interpretation thresholds (the GAP buckets)
GAP_MATCH    = 0.10
GAP_NEAR     = 0.50
FLOOR_MARGIN = 0.02
CTRL_MARGIN  = 0.10


# ============================ corpus (REAL English) ==========================
def build_corpus():
    """Deterministic English byte corpus from the system dictionary (fixed asset)."""
    words = []
    with open("/usr/share/dict/words", "r", errors="ignore") as f:
        for line in f:
            w = line.strip().lower()
            if w.isalpha() and 2 <= len(w) <= 12:
                words.append(w)
    rng = random.Random(CORPUS_SEED)
    rng.shuffle(words)
    words = words[:4000]
    text = " ".join(words) + "\n"
    data = text.encode("ascii", errors="ignore")[:CORPUS_BYTES]
    h = hashlib.sha256(data).hexdigest()
    assert h == FREEZE_SHA, f"corpus sha256 drift: {h} != {FREEZE_SHA}"
    return data, h


def encode_alphabet(data):
    """Map the corpus bytes to a dense 0..V-1 symbol id space."""
    syms = sorted(set(data))
    s2i = {s: i for i, s in enumerate(syms)}
    ids = np.array([s2i[b] for b in data], dtype=np.int64)
    return ids, len(syms), s2i


def make_examples(ids, order):
    """(context-tuple, next-symbol) pairs. context = previous `order` symbol ids."""
    ctx, nxt = [], []
    for t in range(order, len(ids)):
        ctx.append(tuple(int(ids[t - order + j]) for j in range(order)))
        nxt.append(int(ids[t]))
    return ctx, np.array(nxt, dtype=np.int64)


# ===================== A_freq: order-2 Markov n-gram floor ====================
def arm_freq(ctx_tr, nxt_tr, ctx_te, nxt_te, V):
    """Add-1 smoothed order-2 trigram counts — the n-gram-counting floor."""
    table = {}  # ctx -> np.array(V) counts
    for c, y in zip(ctx_tr, nxt_tr):
        if c not in table:
            table[c] = np.full(V, SMOOTH, dtype=np.float64)
        table[c][y] += 1.0
    uniform = np.full(V, 1.0 / V, dtype=np.float64)
    nll = 0.0
    for c, y in zip(ctx_te, nxt_te):
        if c in table:
            p = table[c] / table[c].sum()
        else:
            p = uniform
        nll += -math.log(max(p[y], 1e-12))
    return nll / len(nxt_te)


# ============== A_gradient: softmax next-byte head (MATCHED capacity) =========
def arm_gradient(ctx_tr, nxt_tr, ctx_te, nxt_te, V, seed, cap_contexts):
    """Gradient-trained softmax over the order-2 context (one-hot context feature).
    MATCHED capacity: restrict to the `cap_contexts` most-frequent training contexts
    (so the effective param count tracks the mitosis cell budget at the top rung);
    rare/unseen contexts fall back to a learned global bias. Full-batch CE SGD."""
    rng = np.random.RandomState(seed + 5000)
    # pick the cap_contexts most frequent contexts -> a feature index
    from collections import Counter
    freq = Counter(ctx_tr)
    keep = [c for c, _ in freq.most_common(cap_contexts)]
    c2f = {c: i for i, c in enumerate(keep)}
    F = len(keep) + 1                      # +1 = the "other/unseen" bucket
    def feat(c):
        return c2f.get(c, F - 1)
    Xtr = np.array([feat(c) for c in ctx_tr], dtype=np.int64)
    W = rng.normal(0.0, 0.01, (F, V))      # weight per (context-bucket, symbol)
    n = len(nxt_tr)
    onehot = np.zeros((n, V)); onehot[np.arange(n), nxt_tr] = 1.0
    for t in range(A_STEPS):
        logits = W[Xtr]                    # (n, V)
        logits -= logits.max(axis=1, keepdims=True)
        e = np.exp(logits); p = e / e.sum(axis=1, keepdims=True)
        grad_logits = (p - onehot) / n     # (n, V)
        # scatter-add gradient into W rows by feature index
        gW = np.zeros_like(W)
        np.add.at(gW, Xtr, grad_logits)
        W -= A_LR * gW
    # held-out CE
    Xte = np.array([feat(c) for c in ctx_te], dtype=np.int64)
    logits = W[Xte]; logits -= logits.max(axis=1, keepdims=True)
    e = np.exp(logits); p = e / e.sum(axis=1, keepdims=True)
    nll = -np.log(np.clip(p[np.arange(len(nxt_te)), nxt_te], 1e-12, None))
    return float(nll.mean())


# ============ B_scratch: FROM-SCRATCH PURE MITOSIS (1 cell, split-only) =======
# A cell OWNS a region of the order-2 context space (by nearest-centroid over a
# numeric embedding of the context) and holds an online add-1 next-symbol table over
# the bytes it owns. From 1 cell, split-only under next-byte error pressure. No grad.
class MitosisModel:
    def __init__(self, V, dim):
        self.V = V
        self.dim = dim
        # one seed cell at the origin (the all-context centroid); it owns everything.
        self.centers = [np.zeros(dim)]
        self.tables = [np.full(V, SMOOTH)]       # per-cell next-symbol counts
        self.err_sum = [0.0]                     # running owned error
        self.err_n = [0.0]

    def _nearest(self, x):
        best, bd = 0, np.sum((self.centers[0] - x) ** 2)
        for k in range(1, len(self.centers)):
            d = np.sum((self.centers[k] - x) ** 2)
            if d < bd:
                bd, best = d, k
        return best

    def predict_p(self, x):
        k = self._nearest(x)
        t = self.tables[k]
        return t / t.sum()

    def observe(self, x, y):
        """Online: assign to nearest cell, accrue error, update its table."""
        k = self._nearest(x)
        p = self.tables[k] / self.tables[k].sum()
        self.err_sum[k] += (1.0 - p[y])          # error = 1 - p(true)
        self.err_n[k] += 1.0
        self.tables[k][y] += 1.0
        return k

    def n_cells(self):
        return len(self.centers)

    def split_error_cell(self, owned_X, mode, rng):
        """MITOSIS: the highest-owned-error eligible cell divides. Its owned context
        territory is bisected (k-means-2 over owned points) into two children.
        mode='targeted' splits the worst-error cell; 'shuffle' splits a random cell."""
        # eligible = cells with enough owned points and mean error over threshold
        elig = []
        for k in range(len(self.centers)):
            if self.err_n[k] >= 4 and len(owned_X[k]) >= 2:
                me = self.err_sum[k] / max(self.err_n[k], 1.0)
                if me > SPLIT_THRESH:
                    elig.append((me, k))
        if not elig:
            return False
        if mode == "shuffle":
            _, k = elig[rng.randint(len(elig))]
        else:
            elig.sort(reverse=True)               # worst error first
            _, k = elig[0]
        pts = np.array(owned_X[k])
        if len(pts) < 2:
            return False
        # bisect: 2-means (1 iter) seeded at the two extreme owned points
        d0 = np.sum((pts - pts.mean(0)) ** 2, axis=1)
        a = pts[np.argmax(d0)]
        b = pts[np.argmin(d0)] if not np.allclose(pts[np.argmax(d0)], pts[np.argmin(d0)]) else pts[0]
        for _ in range(3):
            da = np.sum((pts - a) ** 2, axis=1)
            db = np.sum((pts - b) ** 2, axis=1)
            la, lb = pts[da <= db], pts[da > db]
            if len(la) == 0 or len(lb) == 0:
                break
            a, b = la.mean(0), lb.mean(0)
        # replace parent with child a, append child b; reset their tables/error
        self.centers[k] = a.copy()
        self.tables[k] = np.full(self.V, SMOOTH)
        self.err_sum[k] = 0.0; self.err_n[k] = 0.0
        self.centers.append(b.copy())
        self.tables.append(np.full(self.V, SMOOTH))
        self.err_sum.append(0.0); self.err_n.append(0.0)
        return True


def context_embed(ctx, V):
    """Numeric embedding of an order-2 context for the metric space: normalized
    symbol ids. (A simple, fixed, non-learned feature — the cells partition THIS.)"""
    return np.array([c / max(V - 1, 1) for c in ctx], dtype=np.float64)


def _vassign(centers, pts):
    """Vectorized hard nearest-center ownership over a (M,dim) point matrix.
    argmin ties -> lowest index, exactly like the scalar _nearest loop."""
    d2 = ((pts[:, None, :] - centers[None, :, :]) ** 2).sum(2)   # (M,K)
    return d2.argmin(1)


def arm_mitosis(ctx_tr, nxt_tr, ctx_te, nxt_te, V, seed, budget, mode):
    """From-scratch pure-mitosis trainer up to `budget` cells. GRADIENT-FREE.
    Returns held-out next-byte CE (nats) and the final cell count.

    Vectorized form (numpy ownership) — BYTE-IDENTICAL to the per-point reference
    (MitosisModel loops above): same online split (owned over points-SO-FAR), same
    eligibility (err_n>=4, owned>=2, mean-err>SPLIT_THRESH), same worst-error/random
    pick, same 2-means(3-iter) median bisection, same guard loop. Verified to
    reproduce rungs 8/64 to 5 d.p. The vectorization only replaces the O(N) Python
    ownership recompute with a numpy distance matrix (the 512-rung is intractable
    point-by-point)."""
    rng = np.random.RandomState(seed + 9000)
    emb = np.stack([context_embed(c, V) for c in ctx_tr])        # (N,dim)
    N = len(emb)
    centers = np.zeros((1, ORDER))                               # one seed cell at origin
    tables = [np.full(V, SMOOTH)]                                # per-cell next-sym counts
    errs = [0.0]; errn = [0.0]                                   # running owned error

    def try_split(upto):
        """Attempt ONE mitosis split over points emb[:upto] (owned SO-FAR)."""
        own = _vassign(centers, emb[:upto])
        cnt = np.bincount(own, minlength=len(centers))
        elig = []
        for k in range(len(centers)):
            me = errs[k] / max(errn[k], 1.0)
            if errn[k] >= 4 and cnt[k] >= 2 and me > SPLIT_THRESH:
                elig.append((me, k))
        if not elig:
            return False
        if mode == "shuffle":
            _, k = elig[rng.randint(len(elig))]                 # random eligible cell
        else:
            elig.sort(reverse=True); _, k = elig[0]             # worst-error cell
        pts = emb[:upto][own == k]
        if len(pts) < 2:
            return False
        d0 = ((pts - pts.mean(0)) ** 2).sum(1)
        a = pts[d0.argmax()]
        b = pts[d0.argmin()] if not np.allclose(pts[d0.argmax()], pts[d0.argmin()]) else pts[0]
        for _ in range(3):                                      # 2-means, 3 iters
            da = ((pts - a) ** 2).sum(1); db = ((pts - b) ** 2).sum(1)
            la, lb = pts[da <= db], pts[da > db]
            if len(la) == 0 or len(lb) == 0:
                break
            a, b = la.mean(0), lb.mean(0)
        centers[k] = a                                          # parent -> child a
        tables[k] = np.full(V, SMOOTH); errs[k] = 0.0; errn[k] = 0.0
        return ("append", b)

    def do_append(b):
        nonlocal centers
        centers = np.vstack([centers, b.reshape(1, -1)])
        tables.append(np.full(V, SMOOTH)); errs.append(0.0); errn.append(0.0)

    # online single pass: observe each byte; periodically attempt a split until budget.
    split_every = max(1, N // (budget * 4 + 1))
    for i in range(N):
        x = emb[i]; y = int(nxt_tr[i])
        k = int(((centers - x) ** 2).sum(1).argmin())          # nearest cell
        p = tables[k] / tables[k].sum()
        errs[k] += (1.0 - p[y]); errn[k] += 1.0                 # error = 1 - p(true)
        tables[k][y] += 1.0
        if len(centers) < budget and (i % split_every == 0) and i > 0:
            r = try_split(i + 1)
            if r:
                do_append(r[1])
    # extra split passes if budget not reached (still single corpus, gradient-free)
    guard = 0
    while len(centers) < budget and guard < budget * 2:
        r = try_split(N)
        if not r:
            break
        do_append(r[1])
        guard += 1

    # held-out CE (deterministic): nearest cell predicts its add-1 next-sym table.
    emb_te = np.stack([context_embed(c, V) for c in ctx_te])
    win = _vassign(centers, emb_te)
    nll = 0.0
    for i in range(len(nxt_te)):
        t = tables[win[i]]; p = t / t.sum()
        nll += -math.log(max(p[int(nxt_te[i])], 1e-12))
    return nll / len(nxt_te), len(centers)


# ============================ run + frozen scoring ============================
def main():
    data, sha = build_corpus()
    ids, V, _ = encode_alphabet(data)
    cut = int(len(ids) * TRAIN_FRAC)
    ids_tr, ids_te = ids[:cut], ids[cut - ORDER:]   # overlap ORDER so test ctx valid
    ctx_tr, nxt_tr = make_examples(ids_tr, ORDER)
    ctx_te, nxt_te = make_examples(ids_te, ORDER)

    print("H_1310 — FROM-SCRATCH PURE MITOSIS vs GRADIENT — DIRECTIONAL numpy mirror")
    print("=" * 78)
    print(f"corpus = /usr/share/dict/words slice | sha256={sha[:16]}... | "
          f"{len(data)} bytes | V={V} symbols")
    print(f"train ctx/next = {len(nxt_tr)} | test = {len(nxt_te)} | order={ORDER} | "
          f"seeds={SEEDS}")
    print(f"FROZEN: ladder={LADDER} SPLIT_THRESH={SPLIT_THRESH} | "
          f"GAP_MATCH={GAP_MATCH} GAP_NEAR={GAP_NEAR} FLOOR_MARGIN={FLOOR_MARGIN} "
          f"CTRL_MARGIN={CTRL_MARGIN}")
    print("-" * 78)

    # A_freq floor + A_gradient (matched to top-rung budget) — seed-averaged
    freq_ce = []
    grad_ce = []
    for seed in SEEDS:
        freq_ce.append(arm_freq(ctx_tr, nxt_tr, ctx_te, nxt_te, V))
        grad_ce.append(arm_gradient(ctx_tr, nxt_tr, ctx_te, nxt_te, V, seed,
                                    cap_contexts=LADDER[-1]))
    mFreq = float(np.mean(freq_ce))
    mGrad = float(np.mean(grad_ce))

    # B_scratch + B_shuffle across the ladder — seed-averaged per rung
    print("LADDER (mean CE nats over 3 seeds):")
    print(f"{'cells':>7} | {'B_scratch':>10} | {'B_shuffle':>10}")
    rung_ce = {}
    rung_ce_shuf = {}
    rung_cells = {}
    for budget in LADDER:
        bs, bsh, ncl = [], [], []
        for seed in SEEDS:
            ce, nc = arm_mitosis(ctx_tr, nxt_tr, ctx_te, nxt_te, V, seed, budget, "targeted")
            cesh, _ = arm_mitosis(ctx_tr, nxt_tr, ctx_te, nxt_te, V, seed, budget, "shuffle")
            bs.append(ce); bsh.append(cesh); ncl.append(nc)
        rung_ce[budget] = float(np.mean(bs))
        rung_ce_shuf[budget] = float(np.mean(bsh))
        rung_cells[budget] = float(np.mean(ncl))
        print(f"{budget:>7} | {rung_ce[budget]:>10.5f} | {rung_ce_shuf[budget]:>10.5f}  "
              f"(actual cells ~{rung_cells[budget]:.0f})")
    print("-" * 78)
    print(f"A_freq  (order-2 n-gram floor) CE = {mFreq:.5f} nats")
    print(f"A_gradient (matched cap={LADDER[-1]}) CE = {mGrad:.5f} nats")
    print("-" * 78)

    top = LADDER[-1]
    ceB = rung_ce[top]
    ceBshuf = rung_ce_shuf[top]
    gap = ceB - mGrad

    # frozen bars (read VERBATIM, no tune-to-green)
    b1 = (rung_ce[1] > rung_ce[8] > rung_ce[64] > rung_ce[top])     # PRESENCE monotone
    b3 = ceB < mFreq - FLOOR_MARGIN                                  # FLOOR beats n-gram
    b4 = ceBshuf >= ceB + CTRL_MARGIN                               # CONTROL collapse

    if gap <= GAP_MATCH:
        gap_label = "MATCHES gradient"
    elif gap <= GAP_NEAR:
        gap_label = "near gradient (small ceiling)"
    else:
        gap_label = "HONEST LOCAL-EXPERT CEILING"

    print("FROZEN BARS:")
    print(f"(1) PRESENCE monotone CE drop 1>8>64>{top}: "
          f"{rung_ce[1]:.4f}>{rung_ce[8]:.4f}>{rung_ce[64]:.4f}>{rung_ce[top]:.4f} "
          f"-> {'PASS' if b1 else 'FAIL'}")
    print(f"(2) KEY GAP  B_scratch[{top}]-A_gradient = {ceB:.5f}-{mGrad:.5f} = "
          f"{gap:+.5f} nats -> {gap_label}")
    print(f"(3) FLOOR    B_scratch[{top}] < A_freq-{FLOOR_MARGIN}: "
          f"{ceB:.5f} < {mFreq - FLOOR_MARGIN:.5f} -> {'PASS' if b3 else 'FAIL'}")
    print(f"(4) CONTROL  B_shuffle[{top}] >= B_scratch[{top}]+{CTRL_MARGIN}: "
          f"{ceBshuf:.5f} >= {ceB + CTRL_MARGIN:.5f} -> {'PASS' if b4 else 'FAIL'}")
    print("-" * 78)

    base_pass = b1 and b3 and b4
    if base_pass and gap <= GAP_MATCH:
        tier = "GREEN-MATCH"
    elif base_pass and gap <= GAP_NEAR:
        tier = "GREEN-NEAR"
    elif base_pass:
        tier = "HONEST-CEILING"
    elif not b3:
        tier = "FLOOR-FAIL (RED)"
    elif not b1:
        tier = "NO-LEARN (RED)"
    elif not b4:
        tier = "CONTROL-LEAK (RED)"
    else:
        tier = "RED"

    print(f"VERDICT TIER (frozen): {tier}")
    print(f"  from-scratch pure mitosis (1 cell -> split-only, GRADIENT-FREE): "
          f"{'LEARNS' if b1 else 'does NOT learn'} from nothing; "
          f"gap-to-gradient = {gap:+.4f} nats ({gap_label})")
    print(f"  b1={b1} gap={gap:+.4f} b3={b3} b4={b4} | DIRECTIONAL mirror, "
          f"engine-transfer+scale UNVERIFIED (a_toy_scale_recheck/a_scale_honest_scope)")
    print("=" * 78)
    return tier


if __name__ == "__main__":
    main()
