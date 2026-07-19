"""core/mi_compress.py — COMPRESSION-MI measurement lane (H_9806), CORE-owned SSOT.

WHY THIS EXISTS, in one line: production anima had ZERO compression-based mutual-information
estimators, so every "does this stream carry information across a boundary" question had to be
answered by a forward pass through a model — which conflates what the STREAM carries with what
the MODEL can reach. This module measures a property of the stream itself, at $0, stdlib-only,
with no GPU and no ckpt.

Two instruments, absorbed from the lab/v3 campaign (H_005 · H_009) and re-implemented here
against the production `core/` idiom. Both landed as PROPOSED instruments — a lab number is
never a production verdict; only `anima-py` output on this code may be cemented.

────────────────────────────────────────────────────────────────────────────────────────────
A — CROSS-BOUNDARY CONDITIONAL-bpb BATTERY  (`stream_mi`, lab H_005 lineage)
────────────────────────────────────────────────────────────────────────────────────────────
For an ordered stream of segments s_0..s_{n-1} (a "day" of a git history, a document, a
session), ask: does segment t carry information about segment t+1 BEYOND what the last W bytes
of t already supply?

    ceiling(t) = bpb(P_{t+1} | tail_t) − bpb(P_{t+1} | tail_t + body_t)

where tail_t = last W bytes of segment t (the proxy for a model's in-context reach), P_{t+1} =
first P bytes of segment t+1 (the predicted quantity), body_t = everything in segment t BEFORE
the tail (the upper bound on any bottlenecked summary of it — if the FULL body does not lift
bpb, no k-byte extract of it will; conservative toward the kill).

THREE INDEPENDENT ESTIMATORS, because a single compressor's blind spot reads as a substrate
fact (this is exactly how the lab's gzip-only first pass produced a PENDING):
  · gzip    — LZ77. Blind to a lone long-range token beyond its 32KB window.
  · ppm     — multi-order (1..k) adaptive byte model with backoff. Unbounded context reach.
  · markov6 — single order-6 sparse byte Markov. Order-aware, scales where high-order PPM does not.
A reading is only read when the order-aware pair AGREES in sign; the strict bar is all three
over the floor.

★ THE FLOOR IS DERIVED, NEVER ASSUMED. `ceiling` is a raw value and a raw value is not a
signal (measurement-metalaw: the signal is collapse-Δ vs a control). The floor is recomputed
from the SAME realized segments with adjacency deterministically broken — same segment lengths,
same byte statistics, same estimator, same number of pairs; only the ORDER is destroyed. The
reported quantity is `over_floor = ceiling − shuffle_floor`, per estimator, per stream.

────────────────────────────────────────────────────────────────────────────────────────────
B — FEATURE-SPACE SHIFT-NULL LOO CAPTURE  (`shift_null_loo_capture`, lab H_009 lineage)
────────────────────────────────────────────────────────────────────────────────────────────
The byte battery is instrument-BLIND to an abstract code: gzip/ppm/markov are literal byte
models with no decoder, so appending a rendered k-float vector reads ≈0 regardless of truth.
To ask "how much of the cross-boundary information survives a rank-k continuous summary" the
measurement must move into feature space.

    align_X = median_δ err_X(δ) − err_X(0)       (δ = a cyclic misalignment of the queries)
    capture(k) = align_s(k) / align_full

`err_X` is a leave-one-out K-NN prediction error of tomorrow's feature vector from code X.
The shift null is the load-bearing trick: a K-NN estimator's variance penalty is IDENTICAL in
the aligned and the misaligned run, so it CANCELS in the difference. (The lab's first attempt
used a constant-mean denominator and read estimator variance as substrate — a negative capture
on a live stream. The shift null dissolves that failure mode by construction.)

Two structural defects are excluded by construction, not by hope:
  · VALID-k ONLY — when k ≥ n_train−1 the top-k axes span the whole training subspace, so a
    test query's orthogonal residual is a per-query CONSTANT that cancels in the K-NN argmin,
    making capture ≡ 1.0 MECHANICALLY. We drop any k > (n_train−1)//2 or with 2k > numeric rank.
  · LEAKAGE — K-NN candidates exclude |i−j| < 2, so a pair may never be predicted by a
    neighbour that shares a segment with it.

TOPIC FLOOR. A code that merely identifies WHICH topic a segment is about would score well
without carrying anything segment-specific. The topic arm queries with the summary of the
topically-NEAREST OTHER segment (excluding t−1, t, t+1). The honest test is not the aggregate
margin but the PER-PAIR SIGN count, and its threshold is DERIVED from the realized pair count
by exact binomial tail (never a copied 28/43).

────────────────────────────────────────────────────────────────────────────────────────────
CERTIFICATION SHIPS WITH THE INSTRUMENT (the hard rule)
────────────────────────────────────────────────────────────────────────────────────────────
A null control alone NEVER proves an instrument can see anything — it only proves it is not
hallucinating. Every entry point in this module runs its POSITIVE plant before it will report
a substrate number, and refuses to emit a verdict if the plant does not fire:

  battery : `plant_crossboundary()` — a synthetic stream whose segment t+1 prefix IS segment
            t's high-entropy block, placed BEYOND the tail so it is readable only from the
            body. Must read ceiling ≫ ε.  Paired with `plant_null_stream()` — identical
            construction with the carry-over REMOVED — which must NOT clear the floor.
  capture : the three-arm buried-delay-line certification (`capture_liveness`):
            HIGH `plant_weak`   — a real but weak ceiling the top-k axes DO span → capture ≥ 0.8
            LOW  `plant_buried` — 20 delay taps of one logistic scalar (flat covariance
                                  spectrum, exactly 1·I) buried under 8 higher-variance iid
                                  decoys: the FULL code sees it (gate PASS) but the top-k axes
                                  are decoy-dominated → capture ≤ 0.25. This arm is what makes
                                  capture(k) NOT silently inflatable. Certifiable only at
                                  n ≳ 100; below that the decoy sample-eigenvalue spread leaks
                                  signal into the top-8 and the arm is INFORMATIONAL, which
                                  this module reports rather than hides.
            FAIL `plant_iid`    — pure noise → the ceiling gate MUST fail.

DISJOINT (a_substrate_disjoint): its own file, stdlib only, imported by nothing in the decode
path. It touches no weights, no ckpt, no frozen panel; `--stream-mi` / `--capture-anchor` are
purely ADDITIVE flags. No numpy, no torch, no import from `archive/` or `lab/`.
"""

from __future__ import annotations

import gzip
import heapq as _heapq
import math
import os

# ── frozen defaults (an instrument's constants are part of its identity) ───────────────────
W_TAIL = 4096        # in-context reach proxy: the summary must beat what the tail already gives
P_PRED = 2048        # predicted prefix of the next segment
EPS_BPB = 0.02       # decoration guard in bpb — below this an over-floor lift is not read
MIN_PAIRS = 20       # under-powered below this; reported as such, never silently averaged

D_FEAT = 256         # hashed n-gram buckets
K_CANDIDATES = (2, 4, 8, 16)
PRIMARY_K = 8
KNN = 5
EPS_FRAC = 0.075     # capture-margin decoration guard (fraction units)
CAPTURE_ANCHOR = 0.25
RANK_GATE = 2        # aligned run must rank <= this among the shifted runs
TRAIN_FRAC = 0.60    # axis-fit split ONLY; evaluation is LOO over all pairs
LOW_CAP_MAX = 0.25   # LOW liveness arm ceiling
LOW_CERT_N = 100     # below this the LOW arm is informational, not gating (measured limit)


# ═══════════════════════════════════════════════════════════════════════════════════════════
# A — conditional bits-per-byte estimators
# ═══════════════════════════════════════════════════════════════════════════════════════════

def _gz(b: bytes) -> int:
    """Compressed size in bytes at a FIXED level — determinism is the whole point."""
    return len(gzip.compress(b, compresslevel=9))


def cond_bpb_gzip(x: bytes, y: bytes) -> float:
    """NCD-style conditional bpb of x given context y: [|gz(y+x)| − |gz(y)|]·8/|x|.

    Needs no training and no model. Its known blind spot: the LZ window is 32KB, so a single
    day-specific long-range token beyond that window is invisible to it. That blind spot is
    why this estimator is never read alone."""
    if not x:
        return 0.0
    return (_gz(y + x) - _gz(y)) * 8.0 / len(x)


def cond_bpb_ppm(x: bytes, y: bytes, order: int = 4) -> float:
    """Order-1..k adaptive byte model with longest-match backoff, primed on y, scoring x.

    Unlike gzip this has an UNBOUNDED context reach (counts, not a sliding window), so it is
    sensitive to exactly the lone long-range token gzip misses. Laplace-smoothed over the 256
    byte alphabet; updates online while scoring, so it never sees x's future. Deterministic."""
    if not x:
        return 0.0
    ctx_counts: dict = {}

    for i in range(len(y)):
        for k in range(1, order + 1):
            if i - k < 0:
                continue
            d = ctx_counts.setdefault(y[i - k:i], [0] * 256)
            d[y[i]] += 1

    total_bits = 0.0
    hist = bytearray(y[-order:])
    for byte in x:
        p = None
        for k in range(order, 0, -1):            # back off from the longest context with counts
            if len(hist) < k:
                continue
            d = ctx_counts.get(bytes(hist[-k:]))
            if d:
                tot = sum(d)
                if tot > 0:
                    p = (d[byte] + 1) / (tot + 256)
                    break
        if p is None:
            p = 1.0 / 256
        total_bits += -math.log(p, 2)
        for k in range(1, order + 1):
            if len(hist) >= k:
                dd = ctx_counts.setdefault(bytes(hist[-k:]), [0] * 256)
                dd[byte] += 1
        hist.append(byte)
    return total_bits / len(x)


def cond_bpb_markov(x: bytes, y: bytes, order: int = 6) -> float:
    """Single order-k sparse byte Markov model — the third, tie-breaking estimator.

    O(|y|+|x|) with dict-of-dict counts, so it reaches an order where a multi-order PPM is
    intractable. Backs off to a primed unigram when the order-k context is unseen. It is
    order-AWARE (unlike gzip) and single-order (unlike ppm), so agreement between it and ppm
    is a genuine second opinion rather than a re-reading of the same statistic."""
    if not x:
        return 0.0
    x, y = bytes(x), bytes(y)
    ctx: dict = {}
    uni = [0] * 256
    for i in range(len(y)):
        uni[y[i]] += 1
        if i >= order:
            ctx.setdefault(y[i - order:i], {})
            d = ctx[y[i - order:i]]
            d[y[i]] = d.get(y[i], 0) + 1
    uni_tot = sum(uni) or 1
    bits = 0.0
    hist = bytearray(y[-order:])
    for b in x:
        key = bytes(hist[-order:]) if len(hist) >= order else None
        d = ctx.get(key) if key is not None else None
        if d:
            p = (d.get(b, 0) + 1) / (sum(d.values()) + 256)
        else:
            p = (uni[b] + 1) / (uni_tot + 256)
        bits += -math.log(p, 2)
        if key is not None:
            dd = ctx.setdefault(key, {})
            dd[b] = dd.get(b, 0) + 1
        uni[b] += 1
        uni_tot += 1
        hist.append(b)
    return bits / len(x)


ESTIMATORS = (("gzip", cond_bpb_gzip), ("ppm", cond_bpb_ppm), ("markov6", cond_bpb_markov))
ORDER_AWARE = ("ppm", "markov6")


# ═══════════════════════════════════════════════════════════════════════════════════════════
# segmentation + the derived floor
# ═══════════════════════════════════════════════════════════════════════════════════════════

def segments_from_path(path: str, win: int = W_TAIL, span: int = P_PRED) -> tuple:
    """Read an ordered stream of segments from disk. Returns (segments, how).

    A DIRECTORY  → one segment per file, ordered by filename (a stable, inspectable order).
    A FILE       → split on a blank-line separator, b"\\n\\n\\n" first, then b"\\n\\n".

    Segments shorter than win+span are DROPPED, not padded: a segment with no body beyond its
    tail cannot express the quantity being measured, and padding one would manufacture the
    answer. The count of dropped segments is returned so a caller can see the attrition."""
    if os.path.isdir(path):
        blobs, names = [], sorted(os.listdir(path))
        for nm in names:
            fp = os.path.join(path, nm)
            if os.path.isfile(fp):
                with open(fp, "rb") as fh:
                    blobs.append((nm, fh.read()))
        how = "dir:%d files" % len(blobs)
    else:
        with open(path, "rb") as fh:
            raw = fh.read()
        sep = b"\n\n\n" if raw.count(b"\n\n\n") >= MIN_PAIRS else b"\n\n"
        parts = [p for p in raw.split(sep) if p.strip()]
        blobs = [("seg%04d" % i, p) for i, p in enumerate(parts)]
        how = "file:sep=%r → %d segments" % (sep, len(parts))
    keep = [(nm, b) for nm, b in blobs if len(b) >= win + span]
    return keep, "%s · %d/%d usable (>= %dB)" % (how, len(keep), len(blobs), win + span)


def break_adjacency(segments: list) -> list:
    """The DERIVED floor's construction: same segments, same lengths, adjacency destroyed.

    Deterministic (no RNG — a floor that moves between runs is not a floor): interleave the
    even and odd positions then reverse. Every original neighbour pair is separated, while the
    multiset of segments, their byte statistics, and the number of measured pairs are all
    preserved exactly. What differs from the real arm is ONLY the order — which is precisely
    the thing the ceiling claims to measure."""
    return (segments[::2] + segments[1::2])[::-1]


def _median(xs: list) -> float:
    s = sorted(xs)
    n = len(s)
    if n == 0:
        return 0.0
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def measure_pairs(segments: list, estimator, win: int = W_TAIL, span: int = P_PRED) -> dict:
    """Ceiling + segment-specificity over consecutive (t, t+1) pairs under one estimator."""
    ceilings, specs, base = [], [], []
    n = len(segments)
    for i in range(n - 1):
        cur = segments[i][1]
        nxt = segments[i + 1][1]
        tail = cur[-win:]
        pref = nxt[:span]
        body = cur[:-win] if len(cur) > win else b""
        # the swap control: a NON-adjacent segment's body, matched in role and roughly in size
        j = i - 2 if i - 2 >= 0 else i + 2
        wrong = segments[j][1][:-win] if 0 <= j < n and len(segments[j][1]) > win else b""

        b_tail = estimator(pref, tail)
        b_body = estimator(pref, tail + body)
        b_swap = estimator(pref, tail + wrong) if wrong else b_body
        ceilings.append(b_tail - b_body)
        specs.append(b_swap - b_body)
        base.append(b_tail)
    return {
        "n_pairs": len(ceilings),
        "ceiling_med": _median(ceilings),
        "ceiling_mean": (sum(ceilings) / len(ceilings)) if ceilings else 0.0,
        "specificity_med": _median(specs),
        "base_bpb_med": _median(base),
    }


def stream_mi(segments: list, win: int = W_TAIL, span: int = P_PRED,
              eps: float = EPS_BPB, estimators=ESTIMATORS) -> dict:
    """The full battery on one stream: per-estimator ceiling, DERIVED shuffle floor, over_floor.

    Never returns a bare ceiling as the headline. `over_floor` is the reported quantity, and
    `anchored_strict` requires ALL THREE estimators over the floor by eps (no gzip exemption —
    exempting the estimator that disagrees is how a tune-to-green happens)."""
    shuf = break_adjacency(segments)
    row = {"n_segments": len(segments), "win": win, "span": span, "eps": eps,
           "underpowered": (len(segments) - 1) < MIN_PAIRS}
    for name, est in estimators:
        real = measure_pairs(segments, est, win, span)
        floor = measure_pairs(shuf, est, win, span)
        row[name] = {"ceiling": real["ceiling_med"], "shuffle_floor": floor["ceiling_med"],
                     "over_floor": real["ceiling_med"] - floor["ceiling_med"],
                     "specificity": real["specificity_med"],
                     "base_bpb": real["base_bpb_med"], "n_pairs": real["n_pairs"]}
    names = [n for n, _ in estimators]
    row["anchored_strict"] = all(row[n]["over_floor"] > eps for n in names)
    oa = [n for n in ORDER_AWARE if n in row]
    row["anchored_order_aware"] = bool(oa) and all(row[n]["over_floor"] > eps for n in oa)
    row["order_aware_agree"] = (len(oa) < 2) or \
        ((row[oa[0]]["over_floor"] > 0) == (row[oa[1]]["over_floor"] > 0))
    return row


# ── the battery's shipped controls ─────────────────────────────────────────────────────────

class _LCG:
    """Deterministic LCG. A seeded stdlib `random` would still be deterministic, but this is
    explicit about carrying no global state a parallel caller could disturb."""

    def __init__(self, seed: int):
        self.s = seed & 0x7FFFFFFF

    def i(self) -> int:
        self.s = (1103515245 * self.s + 12345) & 0x7FFFFFFF
        return self.s

    def u(self) -> float:
        return self.i() / 0x7FFFFFFF

    def n(self) -> float:      # ~N(0, 0.5) via 6-uniform CLT
        return sum(self.u() for _ in range(6)) - 3.0

    def g(self) -> float:      # ~N(0, 1) via 12-uniform CLT
        return sum(self.u() for _ in range(12)) - 6.0


def plant_crossboundary(n_days: int = 30, seed: int = 3,
                        win: int = W_TAIL, span: int = P_PRED) -> list:
    """POSITIVE CONTROL — a stream with a KNOWN, quantified cross-boundary signal.

    Each segment carries a fresh high-entropy `block` at its START (so it lands in the BODY,
    beyond the tail), and the NEXT segment's prefix is exactly that block. The information is
    therefore readable from segment t's body and from nowhere else — precisely the quantity
    `ceiling` claims to measure. If this reads ≈0 the instrument is blind and no reading taken
    with it is interpretable, whatever it says about a real stream."""
    rng = _LCG(seed)
    out, prev = [], None
    for d in range(n_days):
        block = bytes([(rng.i() % 94) + 33 for _ in range(span)])
        filler = bytes([(rng.i() % 26) + 97 for _ in range(win + 1000)])
        out.append(("plant%03d" % d, (prev if prev else block) + block + filler))
        prev = block
    return out


def plant_null_stream(n_days: int = 30, seed: int = 5,
                      win: int = W_TAIL, span: int = P_PRED) -> list:
    """NEGATIVE CONTROL — byte-for-byte the same construction with the CARRY-OVER REMOVED.

    Same lengths, same alphabets, same high-entropy block, same filler; the only difference is
    that segment t+1's prefix is its OWN fresh block instead of yesterday's. So it has the
    identical marginal statistics and ZERO cross-boundary information. It must NOT clear the
    floor. (The positive plant proves the instrument can see; this proves it is not seeing
    things that are not there. Neither alone is a certification.)"""
    rng = _LCG(seed)
    out = []
    for d in range(n_days):
        block = bytes([(rng.i() % 94) + 33 for _ in range(span)])
        own = bytes([(rng.i() % 94) + 33 for _ in range(span)])
        filler = bytes([(rng.i() % 26) + 97 for _ in range(win + 1000)])
        out.append(("null%03d" % d, own + block + filler))
    return out


def battery_liveness(n_days: int = 30, win: int = W_TAIL, span: int = P_PRED,
                     eps: float = EPS_BPB, estimators=ESTIMATORS) -> dict:
    """Run BOTH shipped controls and decide whether the battery may be read at all."""
    pos = stream_mi(plant_crossboundary(n_days, win=win, span=span), win, span, eps, estimators)
    neg = stream_mi(plant_null_stream(n_days, win=win, span=span), win, span, eps, estimators)
    names = [n for n, _ in estimators]
    pos_fires = all(pos[n]["over_floor"] > 5 * eps for n in names)
    neg_refuses = not any(neg[n]["over_floor"] > eps for n in names)
    return {"plant": pos, "null": neg, "plant_fires": pos_fires,
            "null_refuses": neg_refuses, "certified": bool(pos_fires and neg_refuses)}


# ═══════════════════════════════════════════════════════════════════════════════════════════
# B — feature space: hashing, axes, shift-null LOO capture
# ═══════════════════════════════════════════════════════════════════════════════════════════

def fnv1a(b: bytes) -> int:
    h = 0x811C9DC5
    for byte in b:
        h ^= byte
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def hashed_ngram_features(seg: bytes, dim: int = D_FEAT, log_weight: bool = True) -> list:
    """Hashed char-n-gram (n ∈ {1,2,3}) counts → dim buckets → log1p → L2-normalised.

    HONEST LIMIT, stated where it is created: bag-of-n-grams destroys ORDER, and hashing tens
    of thousands of trigrams into 256 buckets crushes the representation hard. Both are
    CONSERVATIVE toward a false negative — a capture read here is a lower bound on what a
    sequence-aware learned code could hold, never an upper bound."""
    counts = [0] * dim
    n = len(seg)
    for size in (1, 2, 3):
        for i in range(n - size + 1):
            counts[fnv1a(seg[i:i + size]) % dim] += 1
    vec = [math.log1p(c) if log_weight else float(c) for c in counts]
    nrm = math.sqrt(sum(v * v for v in vec))
    return [v / nrm for v in vec] if nrm > 0 else vec


def _jacobi(mat: list, tol: float = 1e-12, max_sweeps: int = 100) -> tuple:
    """Eigen-decomposition of a real symmetric matrix by cyclic Jacobi. Deterministic,
    stdlib-only, no numpy. Returns (eigenvalues desc, eigenvectors as rows)."""
    n = len(mat)
    a = [list(map(float, r)) for r in mat]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(max_sweeps):
        off = math.fsum(a[p][q] ** 2 for p in range(n) for q in range(n) if p != q)
        if off <= tol:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) <= 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                sgn = 1.0 if theta >= 0.0 else -1.0
                t = sgn / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    order = sorted(range(n), key=lambda i: a[i][i], reverse=True)
    return [a[i][i] for i in order], [[v[r][i] for r in range(n)] for i in order]


def _centered(rows: list) -> tuple:
    n, dim = len(rows), len(rows[0])
    mean = [sum(r[j] for r in rows) / n for j in range(dim)]
    return [[r[j] - mean[j] for j in range(dim)] for r in rows], mean


def spectrum(rows: list) -> list:
    """Singular values of the observation set (rows = observations).

    Computed through the n×n GRAM matrix X·Xᵀ, not the dim×dim covariance. Same non-zero
    spectrum (a mathematical identity), but n ≈ 30–100 while dim = 256, so the Jacobi cost
    drops by ~(256/n)³ and the numeric rank comes out exactly bounded by n−1 — which is what
    the valid-k guard actually needs to know."""
    x, _ = _centered(rows)
    n = len(x)
    g = [[math.fsum(x[i][t] * x[j][t] for t in range(len(x[0]))) for j in range(n)]
         for i in range(n)]
    ev, _ = _jacobi(g)
    return [math.sqrt(max(0.0, e)) for e in ev]


def principal_axes(rows: list, k: int) -> tuple:
    """Top-k unit principal axes (as rows) + the column mean, via the same Gram trick:
    an eigenvector u of X·Xᵀ maps to the feature-space axis Xᵀu / ‖Xᵀu‖."""
    x, mean = _centered(rows)
    n, dim = len(x), len(x[0])
    g = [[math.fsum(x[i][t] * x[j][t] for t in range(dim)) for j in range(n)]
         for i in range(n)]
    ev, evec = _jacobi(g)
    axes = []
    for idx in range(min(k, n)):
        if ev[idx] <= 1e-18:
            break
        u = evec[idx]
        ax = [math.fsum(u[i] * x[i][t] for i in range(n)) for t in range(dim)]
        nrm = math.sqrt(math.fsum(a * a for a in ax))
        if nrm <= 1e-15:
            break
        axes.append([a / nrm for a in ax])
    return axes, mean


def project(f: list, mean: list, axes: list, k: int) -> list:
    c = [f[i] - mean[i] for i in range(len(f))]
    return [math.fsum(c[i] * ax[i] for i in range(len(ax))) for ax in axes[:k]]


def _sqdist(a: list, b: list) -> float:
    return math.fsum((a[i] - b[i]) ** 2 for i in range(len(a)))


def binom_sf(k: int, n: int, p: float = 0.5) -> float:
    """Exact upper tail P(X ≥ k), summed term-by-term in log space.

    Not a normal approximation: near a threshold the exact and approximate answers straddle
    the band, and then the verdict is a property of the estimator rather than of the data."""
    if not (0 <= k <= n):
        raise ValueError("k must be in [0,n]")

    def pmf(i):
        if p <= 0.0:
            return 1.0 if i == 0 else 0.0
        if p >= 1.0:
            return 1.0 if i == n else 0.0
        return math.exp(math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1)
                        + i * math.log(p) + (n - i) * math.log1p(-p))
    return math.fsum(pmf(i) for i in range(k, n + 1))


def sign_threshold(n_pairs: int, alpha: float = 0.05) -> int:
    """DERIVE the per-pair sign-test bar from the REALIZED number of pairs.

    Chance is re-derived per metric from the realized split (chance-level-must-be-derived):
    the smallest k with P(X ≥ k | n, ½) < alpha. Copying a threshold computed for a different
    n is how a bar silently moves."""
    for k in range(n_pairs + 1):
        if binom_sf(k, n_pairs, 0.5) < alpha:
            return k
    return n_pairs + 1


def _shift_errors(queries: list, cands: list, targets: list, shifts: list, kk: int = KNN) -> tuple:
    """LOO K-NN error of predicting each target from a (possibly cyclically shifted) query.

    For target i under shift δ the query is queries[(i+δ) % P]; candidates are all j with
    |i−j| ≥ 2 (excludes self AND any neighbour sharing a segment with i — the leakage guard).
    Returns ({δ: summed error}, per-pair errors at δ=0). The estimator's variance penalty is
    identical across δ, so it cancels in align = median_{δ≠0} err(δ) − err(0)."""
    P = len(targets)
    dim_t = len(targets[0])
    cand_of = [[j for j in range(P) if abs(i - j) >= 2] for i in range(P)]
    dm = [[_sqdist(queries[q], cands[c]) for c in range(P)] for q in range(P)]
    errs, pp0 = {}, None
    for d in shifts:
        tot, pp = 0.0, []
        for i in range(P):
            row = dm[(i + d) % P]
            nn = _heapq.nsmallest(kk, cand_of[i], key=lambda j: (row[j], j))
            pred = [math.fsum(targets[j][t] for j in nn) / len(nn) for t in range(dim_t)]
            e = _sqdist(targets[i], pred)
            tot += e
            pp.append(e)
        errs[d] = tot
        if d == 0:
            pp0 = pp
    return errs, pp0


def _summarize(errs: dict, nz: list) -> dict:
    e0 = errs[0]
    med = _median([errs[d] for d in nz])
    rank = sum(1 for d in nz if errs[d] <= e0)
    return {"e0": e0, "median_shift": med, "align": med - e0, "rank": rank,
            "p": (rank / len(nz)) if nz else 1.0, "n_shifts": len(nz)}


def shift_null_loo_capture(feats: list, primary_k: int = PRIMARY_K,
                           k_candidates=K_CANDIDATES, knn: int = KNN,
                           train_frac: float = TRAIN_FRAC, alpha: float = 0.05) -> dict:
    """How much of the cross-boundary predictive information survives a rank-k linear code?

    `feats` — an ORDERED list of per-segment feature vectors (all the same width).

    Returns capture(k) = align_s(k)/align_full for every VALID k, the ceiling gate, the
    topic-matched floor and its per-pair sign count with a DERIVED threshold. A hindsight
    linear projection is an upper bound on a learned code of the same rank, so a null here
    bounds the learned case; a positive does NOT establish the learned case."""
    n_days = len(feats)
    if n_days < 6:
        return {"error": "need >= 6 segments, got %d" % n_days, "n_days": n_days}
    dim = len(feats[0])
    n_train = max(2, int(round(n_days * train_frac)))
    train = feats[:n_train]

    svs = spectrum(train)
    smax = max(svs) if svs else 0.0
    numrank = sum(1 for s in svs if s > 1e-9 * smax) if smax > 0 else 0
    # VALID-k guard: k >= n_train-1 makes capture === 1.0 MECHANICALLY (the top-k axes span
    # the whole training subspace, so the test query's orthogonal residual is a per-query
    # constant that cancels in the argmin). Refusing those k is not conservatism, it is the
    # difference between a measurement and a tautology.
    valid_ks = [k for k in k_candidates if k <= (n_train - 1) // 2 and 2 * k <= numrank]
    if not valid_ks:
        return {"error": "no valid k (n_train=%d numrank=%d) — the split cannot support a "
                         "non-tautological rank-k code" % (n_train, numrank),
                "n_days": n_days, "n_train": n_train, "numrank": numrank}
    pk = primary_k if primary_k in valid_ks else max(valid_ks)
    axes, mean = principal_axes(train, max(valid_ks))
    if len(axes) < max(valid_ks):
        valid_ks = [k for k in valid_ks if k <= len(axes)]
        if not valid_ks:
            return {"error": "axis fit produced only %d axes" % len(axes), "n_days": n_days}
        pk = primary_k if primary_k in valid_ks else max(valid_ks)

    P = n_days - 1
    shifts = [0] + list(range(3, P - 3))
    nz = shifts[1:]
    if len(nz) < 4:
        return {"error": "only %d shift-null draws (need >= 4) — the misalignment floor is "
                         "not estimable at n_days=%d" % (len(nz), n_days), "n_days": n_days}
    targets = [feats[i + 1] for i in range(P)]

    fk = [feats[i] for i in range(P)]
    errs_full, pp_full = _shift_errors(fk, fk, targets, shifts, knn)
    sf = _summarize(errs_full, nz)

    summ = {k: [project(feats[j], mean, axes, k) for j in range(n_days)] for k in valid_ks}
    cap, s_stats, pp_s = {}, {}, {}
    for k in valid_ks:
        sk = [summ[k][i] for i in range(P)]
        errs_s, pp = _shift_errors(sk, sk, targets, shifts, knn)
        ss = _summarize(errs_s, nz)
        s_stats[k], pp_s[k] = ss, pp
        cap[k] = (ss["align"] / sf["align"]) if sf["align"] > 1e-12 else None

    def cos(a, b):
        na = math.sqrt(math.fsum(x * x for x in a))
        nb = math.sqrt(math.fsum(x * x for x in b))
        return math.fsum(a[i] * b[i] for i in range(len(a))) / (na * nb) if na and nb else 0.0

    topic_of = []
    for i in range(P):
        excl = {i - 1, i, i + 1}
        best, bc = 0, -2.0
        for u in range(n_days):
            if u in excl:
                continue
            c = cos(feats[i], feats[u])
            if c > bc:
                bc, best = c, u
        topic_of.append(best)
    tq = [summ[pk][topic_of[i]] for i in range(P)]
    tc = [summ[pk][j] for j in range(P)]
    errs_t, pp_t = _shift_errors(tq, tc, targets, shifts, knn)
    st = _summarize(errs_t, nz)
    topic_cap = (st["align"] / sf["align"]) if sf["align"] > 1e-12 else None

    sign_cnt = sum(1 for a, b in zip(pp_t, pp_s[pk]) if a > b)
    need = sign_threshold(P, alpha)
    # monotonicity: a rank-k code cannot carry LESS than a rank-(k-1) one except by artifact
    running, mono_ok = -1e18, True
    for k in valid_ks:
        v = cap[k]
        if v is None:
            continue
        if v < running - 0.05:
            mono_ok = False
        running = max(running, v)

    return {
        "n_days": n_days, "n_train": n_train, "numrank": numrank, "n_pairs": P,
        "n_shifts": sf["n_shifts"], "valid_ks": valid_ks, "primary_k": pk, "dim": dim,
        "full": sf, "s": {str(k): s_stats[k] for k in valid_ks}, "topic": st,
        "capture": {str(k): cap[k] for k in valid_ks},
        "capture_primary": cap[pk], "topic_capture_primary": topic_cap,
        "capture_margin": (None if (cap[pk] is None or topic_cap is None)
                           else cap[pk] - topic_cap),
        "gate_ok": sf["rank"] <= RANK_GATE,
        "monotonic_ok": mono_ok,
        "sign_topic_gt_s": sign_cnt, "sign_needed": need, "sign_alpha": alpha,
        "sign_ok": sign_cnt >= need,
    }


# ── the capture instrument's shipped three-arm certification ───────────────────────────────

def _unit(rng: _LCG, dim: int) -> list:
    v = [rng.n() for _ in range(dim)]
    nrm = math.sqrt(sum(x * x for x in v))
    return [x / nrm for x in v]


def _norm(v: list) -> list:
    nrm = math.sqrt(sum(x * x for x in v))
    return [x / nrm for x in v] if nrm > 0 else v


def plant_weak(n_days: int, seed: int = 11, dim: int = D_FEAT,
               R: int = 8, alpha: float = 0.80) -> list:
    """LIVENESS-HIGH. R topic directions; segment t is a mixture with weights w_t, and
    w_{t+1} = α·shift(w_t) + (1−α)·fresh. Tomorrow's weights are largely determined by
    today's, and the R topic directions dominate the variance, so the top-8 axes ARE the
    weights. capture(8) must read HIGH — if it does not, the instrument cannot see a real
    ceiling that a rank-k code demonstrably spans."""
    rng = _LCG(seed)
    topics = [_unit(rng, dim) for _ in range(R)]
    w = [rng.u() + 0.2 for _ in range(R)]
    out = []
    for _ in range(n_days):
        base = [math.fsum(w[c] * topics[c][j] for c in range(R)) for j in range(dim)]
        out.append(_norm([base[j] + 0.05 * rng.n() for j in range(dim)]))
        w = [alpha * w[(c - 1) % R] + (1 - alpha) * (rng.u() + 0.2) for c in range(R)]
    return out


def plant_buried(n_days: int, dim: int = D_FEAT, n_sig: int = 20, n_dec: int = 8,
                 sig_amp: float = math.sqrt(2.0), dec_amp: float = 2.0) -> list:
    """LIVENESS-LOW — the BURIED DELAY-LINE, and the reason `capture` is not inflatable.

    The arm needs a stream whose cross-boundary information the FULL code can see (so the
    ceiling gate passes) but which the top-k axes MISS (so capture must read low). Two obvious
    constructions fail: a single orthogonal direction contributes a vanishing share of a
    Euclidean K-NN distance, so the full code goes blind too and the ceiling dies with it;
    independent latents make the attractor too high-dimensional for the neighbour count.

    The escape is MANY sub-threshold dimensions driven by ONE deterministic core:
      · signal — n_sig delay TAPS of a single logistic scalar x_{i+1} = 4x_i(1−x_i); tap j is
        √2·(1−2·x[idx−j]), whose per-dim variance is 1.0 and whose Chebyshev orthogonality
        makes the tap covariance EXACTLY 1·I — a flat spectrum with zero lag-correlation, so
        no single direction sticks up for PCA to find.
      · decoy — n_dec fresh iid dimensions at variance 4.0, sitting ON TOP of the spectrum.
    The full K-NN sees the signal block's 20/(20+8·4) = 38.5% distance share and the attractor
    is 1-dimensional, so the gate passes; the top-8 SAMPLE axes are decoy-dominated, so the
    rank-k code misses it and capture(k ≤ 8) is low BY CONSTRUCTION at every valid k."""
    x0 = 0.6180339887 if n_days < 100 else 0.3819660113
    N = 119 + n_days
    x = [0.0] * N
    x[0] = x0
    for i in range(N - 1):
        xi = 4.0 * x[i] * (1.0 - x[i])
        x[i + 1] = min(1.0 - 1e-12, max(1e-12, xi))
    rng = _LCG(20260720 + n_days)
    out = []
    for t in range(n_days):
        it = 119 + t
        v = [0.0] * dim
        for j in range(n_sig):
            v[j] = sig_amp * (1.0 - 2.0 * x[it - j])
        for i in range(n_dec):
            v[n_sig + i] = dec_amp * rng.g()
        out.append(_norm(v))
    return out


def plant_iid(n_days: int, seed: int = 37, dim: int = D_FEAT) -> list:
    """LIVENESS-FAIL — iid segments, no cross-boundary structure at all. The ceiling gate MUST
    fail here. If it passes, the gate is reading estimator variance and every capture number
    taken with this instrument is void."""
    rng = _LCG(seed)
    return [_norm([rng.n() for _ in range(dim)]) for _ in range(n_days)]


def capture_liveness(n_days: int, primary_k: int = PRIMARY_K) -> dict:
    """Three-arm certification, run BEFORE any substrate capture number may be read.

    HIGH must fire · FAIL must refuse · LOW must stay under LOW_CAP_MAX.

    RESOLUTION LIMIT, reported rather than hidden: the LOW arm is certifiable only at
    n ≳ LOW_CERT_N. Below that the decoy sample-eigenvalue SPREAD over a small training set
    leaks signal combinations into the top-8 and capture cannot be driven under the bar
    without starving the gate. At n < LOW_CERT_N the arm is INFORMATIONAL and the run is
    REPLICATION-grade, not PRIMARY — which is a statement about power, not about substrate."""
    hi = shift_null_loo_capture(plant_weak(n_days), primary_k)
    lo = shift_null_loo_capture(plant_buried(n_days), primary_k)
    fa = shift_null_loo_capture(plant_iid(n_days), primary_k)

    high_ok = bool(hi.get("gate_ok") and (hi.get("capture_primary") or 0.0) >= 0.8)
    fail_ok = bool(not fa.get("gate_ok", True))
    locap = lo.get("capture", {}) or {}
    lo_ks = [k for k in lo.get("valid_ks", []) if k <= 8]
    lo_vals = [locap.get(str(k)) for k in lo_ks]
    low_ok = bool(lo.get("full", {}).get("rank") == 0 and lo_vals
                  and all(v is not None and v <= LOW_CAP_MAX for v in lo_vals))
    gating = n_days >= LOW_CERT_N
    return {
        "n_days": n_days, "high": hi, "low": lo, "fail": fa,
        "high_ok": high_ok, "low_ok": low_ok, "fail_ok": fail_ok,
        "low_is_gating": gating,
        "certified": bool(high_ok and fail_ok and (low_ok or not gating)),
        "grade": "PRIMARY" if (gating and low_ok) else "REPLICATION",
    }
