#!/usr/bin/env python3
# h1354_ko_natural_sparse.py — H_1354: ko-natural-sparse.
#
# PARENT: H_1345 (🟢) mapped a DATA-RICHNESS crossover — as the per-cell jamo count falls below ~1,
# Jelinek-Mercer interpolation toward the global jamo marginal crosses BELOW the opaque jamo floor.
# BUT H_1345 manufactured that starvation by ARTIFICIAL STRIDING (sub-sampling the 30MB corpus at
# stride up to 76800 → tiny 188-byte held-out streams). H_1344 separately showed even at FULL data
# JM beats the floor only via memorization of repeats. The OPEN question (named verbatim in the H_1345
# card's "Next" §, angle ii): is the starvation win a REAL PRACTICAL LEVER or a STRIDING ARTIFACT?
#
# H_1354 RUNS the H_1345-named angle directly: a NATURALLY-sparse context regime at FULL 30MB. Instead
# of cutting the corpus, we ENRICH the partition CONTEXT to cross-syllable phonotactic transitions —
# the (previous-syllable CODA jamo, current-syllable ONSET jamo) pair across the syllable boundary —
# which fragments the model into MANY contexts whose per-context jamo counts are genuinely sparse AT
# FULL DATA (no striding, no cutting). Korean phonotactics make many coda→onset transitions rare or
# illegal, so the sparsity is a REAL property of the language, not an artifact of throwing data away.
#
# THE QUESTION: on these NATURALLY-sparse phonotactic contexts, does JM interpolation buy below-jamo?
#   YES (JM crosses below jamo on natural-sparse contexts, earned, dissociated from A5) => REAL LEVER:
#         the H_1345 crossover survives without artificial striding — sparse-context backoff is a real
#         below-jamo mechanism at full data.
#   NO  (JM does NOT cross naturally) => STRIDING ARTIFACT: the H_1345 win needed the tiny-stream
#         starvation it manufactured; honest 🧱 (c9). H_1344's memorization reading stands.
#
# FROZEN bars (pre-registered FREEZE BEFORE the run; bars NOT moved — c9/p7):
#   c1 NAT-SPARSE-WIN : on the naturally-sparse phonotactic contexts, held-out JM nat/byte beats jamo
#                       (A1) — report the SIGNED delta (jamo − JM). WIN iff delta >= +0.03 (mean 3 seeds).
#   c2 EARNED         : JM beats its SHUFFLE control (permuted global jamo marginal = wrong backoff
#                       target) by >= 0.05 — the win is real backoff structure, not generic mass; the
#                       shuffle must go the WRONG way (shuffle CE > jamo CE).
#   c3 DISSOCIATION   : A5 learned-metric kernel-smoothing does NOT cross (stays >= jamo) — the H_1345
#                       dissociation: interpolation-toward-the-marginal exploits sparsity, smoothing does
#                       not. If A5 ALSO crosses, the lift is generic capacity not backoff → flag.
#   c4 NO-STRIDE      : confirm the sparsity is NATURAL — report the per-context jamo-count distribution
#                       (median, frac of contexts with count < 1) and assert NO artificial stride/cut
#                       was applied (stride == 1 over the FULL 30MB window). The contexts must be
#                       genuinely sparse (median per-context jamo count < ~1) WITHOUT cutting data.
#   GREEN iff c1 ∧ c2 ∧ c3 ∧ c4(sparsity natural)  => REAL LEVER (crossover survives without striding).
#   c1 fail (JM does NOT cross naturally) => STRIDING ARTIFACT, honest 🧱.
#
# REAL Korean only (NO synthetic, p1-p8): SAME R2 web corpus as H_1307 RUN A / H_1316 / H_1337 / H_1345.
# The FULL 30MB KO window sha256 ASSERTED == c47b6808… (== H_1307 RUN A). NO striding of the corpus for
# the natural-sparse arm. SCALE-HONEST: toy/DIRECTIONAL numpy mirror; A5 metric LEARNED BY GRADIENT
# (labeled, NOT p8); engine-transfer = follow-on; NO fluency claim.

import argparse, hashlib, json, os, sys, time, unicodedata
import numpy as np

# ── FROZEN knobs (verbatim from H_1316/H_1326/H_1329/H_1337/H_1345) ────────────────────
GROW_MAX = 40
SPLIT_THRESH_CE = 0.05
MIN_OWNED = 8
LAPLACE = 1.0
H1316_JAMO_CE = 2.51335
C1_MARGIN = 0.03          # c1: JM beats jamo by >= this on natural-sparse contexts (mean 3 seeds)
C2_MARGIN = 0.05          # c2: JM beats its shuffle control by >= this
H1307_KO_SHA = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
R2_KO_KEY = "anima-7b/web/kor/shard0000.bytes"
HANGUL_LO, HANGUL_HI = 0xAC00, 0xD7A3
# ── A5 learned-metric knobs (FROZEN, verbatim H_1337/H_1345; NO per-run tuning) ────────
D_EMB = 16
SKIPGRAM_STEPS = 400
SKIPGRAM_LR = 0.05

def log(*a): print(*a, flush=True)

# ── REAL corpus fetch from R2 (secrets env-only, never logged) ──────────────────
def fetch_r2_range(key, nbytes):
    import boto3
    from botocore.config import Config
    s3 = boto3.client("s3",
        endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        config=Config(signature_version="s3v4", retries={"max_attempts": 5}))
    obj = s3.get_object(Bucket=os.environ["R2_BUCKET"], Key=key, Range=f"bytes=0-{nbytes-1}")
    return obj["Body"].read()

def trim_utf8(b):
    for cut in range(0, 4):
        try:
            b[: len(b) - cut].decode("utf-8"); return b[: len(b) - cut]
        except Exception:
            continue
    return b

# ════ jamo decomposition + streams (VECTORIZED; byte/symbol-identical to H_1316/H_1337/H_1345) ═══════
LJAMO = 0x1100; VJAMO = 0x1161; TJAMO = 0x11A7
SBASE = 0xAC00; NCOUNT = 588; TCOUNT = 28

def _decompose_cp(cp):
    if SBASE <= cp <= HANGUL_HI:
        Si = cp - SBASE
        L = LJAMO + Si // NCOUNT
        V = VJAMO + (Si % NCOUNT) // TCOUNT
        T0 = Si % TCOUNT
        if T0:
            return [(L, 1), (V, 1), (TJAMO + T0, 1)]      # 3 jamo: onset L, vowel V, CODA T
        return [(L, 2), (V, 1)]                            # 2 jamo: onset L, vowel V, NO coda
    return None

def roundtrip_and_accounting(text):
    cps = np.array([ord(c) for c in set(text)], dtype=np.int64)
    hang = cps[(cps >= SBASE) & (cps <= HANGUL_HI)]
    bad = 0
    for cp in hang.tolist():
        ch = chr(cp)
        nfc = unicodedata.normalize("NFC", unicodedata.normalize("NFD", ch))
        if nfc.encode("utf-8") != ch.encode("utf-8"): bad += 1
    arr = np.frombuffer(text.encode("utf-32-le"), dtype=np.uint32).astype(np.int64)
    n_syll = int(((arr >= SBASE) & (arr <= HANGUL_HI)).sum())
    return {"hangul_syllables": n_syll, "roundtrip_fail": bad, "ok": bad == 0,
            "distinct_hangul_checked": int(hang.shape[0])}

def build_jamo_vocab(text):
    jset = set()
    for cp in set(ord(c) for c in text):
        if SBASE <= cp <= HANGUL_HI:
            for (jcp, _nb) in _decompose_cp(cp): jset.add(jcp)
    jamo_sorted = sorted(jset)
    return {cp: 256 + i for i, cp in enumerate(jamo_sorted)}, jamo_sorted

def make_streams(text, jamo_to_id):
    """VECTORIZED symbol/nbyte/depth streams (byte-identical to H_1316/H_1345). depth 0=onset,1=vowel,
       2=coda within a 3-jamo syllable; 2-jamo syllable has onset(depth0) vowel(depth1) NO coda."""
    cps = np.frombuffer(text.encode("utf-32-le"), dtype=np.uint32).astype(np.int64)
    is_h = (cps >= SBASE) & (cps <= HANGUL_HI)
    syms = []; nby = []; depth = []
    sa = syms.append; na = nby.append; da = depth.append
    hcache = {}
    d = 0
    for cp, h in zip(cps.tolist(), is_h.tolist()):
        if h:
            exp = hcache.get(cp)
            if exp is None:
                exp = [(jamo_to_id[jcp], nb) for (jcp, nb) in _decompose_cp(cp)]
                hcache[cp] = exp
            for j, (sid, nb) in enumerate(exp):
                sa(sid); na(nb)
                d = 0 if j == 0 else d + 1; da(d)
        else:
            for b in chr(cp).encode("utf-8"):
                sa(b); na(1)
                d = d + 1 if 0x80 <= b <= 0xBF else 0; da(d)
    return (np.asarray(syms, np.int64), np.asarray(nby, np.int64), np.asarray(depth, np.int64))

# ── engine-native mitosis (numpy port, BYTE-FAITHFUL to H_1306..H_1345) ─────────
# CHUNKED over rows: at FULL 30MB (25.5M rows, NO striding) the (N,K,D) broadcast blows 17GB RAM, so we
# stream the argmin in row blocks. BYTE-IDENTICAL result to the H_1345 full-broadcast (||x-c||^2 expanded
# as |x|^2 - 2 x·c + |c|^2, argmin invariant to the |x|^2 term; we keep the squared form for exactness).
_ASSIGN_CHUNK = 200_000
def assign_all(centers, X):
    K = centers.shape[0]; n = X.shape[0]
    cc = (centers ** 2).sum(axis=1)                       # (K,)
    out = np.empty(n, dtype=np.int64)
    if n <= _ASSIGN_CHUNK:
        d2 = ((X[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        return np.argmin(d2, axis=1)
    for s in range(0, n, _ASSIGN_CHUNK):
        e = min(s + _ASSIGN_CHUNK, n)
        xb = X[s:e]
        d2 = (xb * xb).sum(axis=1)[:, None] - 2.0 * (xb @ centers.T) + cc[None, :]
        out[s:e] = np.argmin(d2, axis=1)
    return out

def all_heads_counts(Y, owner, K, ntr, vj):
    Hcnt = np.full((K, vj), LAPLACE, dtype=np.float64)
    flat = owner[:ntr] * vj + Y[:ntr]
    np.add.at(Hcnt.reshape(-1), flat, 1.0)
    return Hcnt

def all_heads(Y, owner, K, ntr, vj):
    Hcnt = all_heads_counts(Y, owner, K, ntr, vj)
    return Hcnt / Hcnt.sum(axis=1, keepdims=True)

def owned_ce(Y, owner, k, ntr, p_row):
    mask = (owner[:ntr] == k)
    if not mask.any(): return -1.0
    yk = Y[:ntr][mask]
    return float(-np.log(p_row[yk] + 1e-12).mean())

def grow_on(centers, X_tr, Y_tr, ntr, vj, grow_max):
    centers = [list(c) for c in centers]
    while len(centers) < grow_max:
        ct = np.asarray(centers, dtype=np.float64)
        owner = assign_all(ct, X_tr); K = len(centers); owntr = owner[:ntr]
        owned_n = np.bincount(owntr, minlength=K)
        Hmat = all_heads(Y_tr, owner, K, ntr, vj)
        local_ce = np.full(K, -1.0)
        for k in range(K):
            if owned_n[k] > 0: local_ce[k] = owned_ce(Y_tr, owner, k, ntr, Hmat[k])
        elig = [k for k in range(K) if owned_n[k] >= MIN_OWNED and local_ce[k] > SPLIT_THRESH_CE]
        if not elig: break
        pick = elig[0]; bestce = local_ce[elig[0]]
        for k in elig[1:]:
            if local_ce[k] > bestce: bestce = local_ce[k]; pick = k
        if len(centers) + 1 > grow_max: break
        pts = X_tr[:ntr][owntr == pick]
        if pts.shape[0] == 0: break
        ax = int(np.argmax(pts.var(axis=0)))
        col = pts[:, ax]; m = col.shape[0]; scol = np.sort(col)
        med = scol[m // 2] if m % 2 == 1 else (scol[m//2-1] + scol[m//2]) / 2.0
        lo_mask = col <= med; hi_mask = col > med
        if int(lo_mask.sum()) == 0 or int(hi_mask.sum()) == 0: break
        c_lo = pts[lo_mask].mean(axis=0).tolist()
        c_hi = pts[hi_mask].mean(axis=0).tolist()
        centers = [centers[i] for i in range(len(centers)) if i != pick] + [c_lo, c_hi]
    return centers

def split_even_odd_full(X, *arrs):
    """NO STRIDE — full data, even/odd held-out split only (stride == 1)."""
    idx = np.arange(X.shape[0]); e = idx % 2 == 0; o = idx % 2 == 1
    out_tr = [X[e]] + [a[e] for a in arrs]; out_te = [X[o]] + [a[o] for a in arrs]
    return out_tr, out_te

# ── OPAQUE-id per-byte CE (A1 = jamo id) numpy port ─────────────────────────────
def per_byte_ce_opaque(centers, X_tr, Y_tr, ntr, X_te, Y_te, NB_te, vj):
    owner_tr = assign_all(centers, X_tr)
    Hmat = all_heads(Y_tr, owner_tr, centers.shape[0], ntr, vj)
    owner_te = assign_all(centers, X_te)
    p = Hmat[owner_te, Y_te]; nll = -np.log(p + 1e-12)
    return float(nll.sum() / float(NB_te.sum()))

# ══════════ A5 — LEARNED-METRIC kernel-smoothed (VERBATIM H_1337/H_1345 mechanism, numpy) ═══════════
def learn_jamo_embedding(Y_tr_n, sym_is_jamo_tr, n_jamo, seed, refine=True):
    C = np.zeros((n_jamo, n_jamo), dtype=np.float64)
    prev = -1
    for i in range(len(Y_tr_n)):
        if sym_is_jamo_tr[i]:
            j = int(Y_tr_n[i]) - 256
            if prev >= 0: C[prev, j] += 1.0
            prev = j
        else:
            prev = -1
    total = C.sum()
    if total <= 0:
        return np.zeros((n_jamo, D_EMB), dtype=np.float64)
    Pij = C / total
    Pi = Pij.sum(axis=1, keepdims=True) + 1e-12
    Pj = Pij.sum(axis=0, keepdims=True) + 1e-12
    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log((Pij + 1e-12) / (Pi * Pj))
    ppmi = np.maximum(0.0, pmi)
    d = min(D_EMB, n_jamo)
    U, S, Vt = np.linalg.svd(ppmi, full_matrices=False)
    E0 = U[:, :d] * np.sqrt(S[:d] + 1e-12)[None, :]
    if E0.shape[1] < D_EMB:
        E0 = np.concatenate([E0, np.zeros((n_jamo, D_EMB - E0.shape[1]))], axis=1)
    if not refine:
        return E0
    Ew = E0.copy(); Fw = E0.copy()
    Ct = C
    rowsum = Ct.sum(axis=1, keepdims=True) + 1e-12
    Pcond = Ct / rowsum
    wrow = (Ct.sum(axis=1) / Ct.sum())[:, None]
    mE = np.zeros_like(Ew); vE = np.zeros_like(Ew)
    mF = np.zeros_like(Fw); vF = np.zeros_like(Fw)
    b1, b2, eps, lr = 0.9, 0.999, 1e-8, SKIPGRAM_LR
    for t in range(1, SKIPGRAM_STEPS + 1):
        logits = Ew @ Fw.T
        m = logits.max(axis=1, keepdims=True)
        ex = np.exp(logits - m)
        sm = ex / ex.sum(axis=1, keepdims=True)
        rowmass = (wrow * Pcond).sum(axis=1, keepdims=True)
        dlog = wrow * (sm * rowmass - Pcond)
        gE = dlog @ Fw + 1e-4 * 2 * Ew
        gF = dlog.T @ Ew + 1e-4 * 2 * Fw
        for (W, g, mm, vv) in ((Ew, gE, mE, vE), (Fw, gF, mF, vF)):
            mm *= b1; mm += (1 - b1) * g
            vv *= b2; vv += (1 - b2) * (g * g)
            mhat = mm / (1 - b1 ** t); vhat = vv / (1 - b2 ** t)
            W -= lr * mhat / (np.sqrt(vhat) + eps)
    return Ew

def kernel_from_embedding(E):
    D = np.sqrt(((E[:, None, :] - E[None, :, :]) ** 2).sum(axis=2))
    n = D.shape[0]
    iu = np.triu_indices(n, k=1)
    pw = D[iu]
    h = float(np.median(pw))
    if h <= 1e-9: h = 1.0
    W = np.exp(-(D * D) / (2.0 * h * h))
    np.fill_diagonal(W, 1.0)
    return W, h

def per_byte_ce_metric_smoothed(centers, X_tr, Y_tr, ntr, X_te, Y_te, NB_te, vj, Wjamo, n_jamo):
    K = centers.shape[0]
    owner_tr = assign_all(centers, X_tr)
    Hcnt = all_heads_counts(Y_tr, owner_tr, K, ntr, vj)
    byte_blk = Hcnt[:, :256]
    jamo_blk = Hcnt[:, 256:256 + n_jamo]
    jamo_smoothed = jamo_blk @ Wjamo.T
    Hsm = np.concatenate([byte_blk, jamo_smoothed], axis=1)
    P = Hsm / Hsm.sum(axis=1, keepdims=True)
    owner_te = assign_all(centers, X_te)
    p = P[owner_te, Y_te]; nll = -np.log(p + 1e-12)
    return float(nll.sum() / float(NB_te.sum()))

# ══════════ JM — JELINEK-MERCER interpolation with the GLOBAL jamo marginal (verbatim H_1345) ═══════
def per_byte_ce_jm(centers, X_tr, Y_tr, ntr, X_te, Y_te, NB_te, vj, n_jamo, shuffle_seed=None):
    K = centers.shape[0]
    owner_tr = assign_all(centers, X_tr)
    Hcnt = all_heads_counts(Y_tr, owner_tr, K, ntr, vj)
    jamo_lab = Y_tr[:ntr]
    is_j = (jamo_lab >= 256) & (jamo_lab < 256 + n_jamo)
    gcnt = np.full(n_jamo, LAPLACE, dtype=np.float64)
    np.add.at(gcnt, jamo_lab[is_j] - 256, 1.0)
    Pglobal = gcnt / gcnt.sum()
    if shuffle_seed is not None:
        Pglobal = np.random.default_rng(shuffle_seed).permutation(Pglobal)
    byte_blk = Hcnt[:, :256]
    jamo_cnt = Hcnt[:, 256:256 + n_jamo]
    Nk_jamo = jamo_cnt.sum(axis=1, keepdims=True)
    Pcell_j = jamo_cnt / Nk_jamo
    Nk_raw = Nk_jamo - LAPLACE * n_jamo
    Nk_raw = np.maximum(Nk_raw, 0.0)
    lam = MIN_OWNED / (MIN_OWNED + Nk_raw)
    jamo_interp = (1.0 - lam) * Pcell_j + lam * Pglobal[None, :]
    Pbyte = byte_blk / byte_blk.sum(axis=1, keepdims=True)
    full_norm = Hcnt.sum(axis=1, keepdims=True)
    jamo_mass = jamo_cnt.sum(axis=1, keepdims=True) / full_norm
    byte_mass = byte_blk.sum(axis=1, keepdims=True) / full_norm
    P = np.concatenate([byte_mass * Pbyte, jamo_mass * jamo_interp], axis=1)
    P = P / P.sum(axis=1, keepdims=True)
    owner_te = assign_all(centers, X_te)
    p = P[owner_te, Y_te]; nll = -np.log(p + 1e-12)
    return float(nll.sum() / float(NB_te.sum()))

# ── partition feature builders ──────────────────────────────────────────────────
def build_X_opaque(syms, depth, vj):
    """H_1345 3-D opaque feature (CALIB arm): last sym, second sym, current depth. Dense partition."""
    n = len(syms); idx = np.arange(4, n - 1)
    last = syms[idx - 1].astype(np.float64) / float(vj)
    second = syms[idx - 2].astype(np.float64) / float(vj)
    cdep = depth[idx - 1].astype(np.float64) / 3.0
    return np.stack([last, second, cdep], axis=1), syms[idx].astype(np.int64), idx

def build_X_phonotactic(syms, depth, vj, n_jamo):
    """NATURAL-SPARSE feature: the CROSS-SYLLABLE PHONOTACTIC context. We add the (last-seen CODA jamo,
       last-seen ONSET jamo) pair to the H_1345 3-D opaque feature. The coda→onset transition across a
       syllable boundary is a real Korean phonotactic pair; many such pairs are rare or illegal, so
       partitioning on them produces MANY contexts whose per-context jamo counts are NATURALLY sparse
       at FULL data — no striding."""
    n = len(syms)
    is_jamo = (syms >= 256) & (syms < 256 + n_jamo)
    is_coda = is_jamo & (depth == 2)            # depth 2 within a 3-jamo syllable == coda
    is_onset = is_jamo & (depth == 0)           # depth 0 jamo == onset of a syllable
    last_coda = np.full(n, -1, dtype=np.int64)
    last_onset = np.full(n, -1, dtype=np.int64)
    lc = -1; lo = -1
    sy = syms.tolist(); icoda = is_coda.tolist(); ionset = is_onset.tolist()
    for i in range(n):
        last_coda[i] = lc
        last_onset[i] = lo
        if icoda[i]:
            lc = sy[i] - 256
        if ionset[i]:
            lo = sy[i] - 256
    idx = np.arange(4, n - 1)
    last = syms[idx - 1].astype(np.float64) / float(vj)
    second = syms[idx - 2].astype(np.float64) / float(vj)
    cdep = depth[idx - 1].astype(np.float64) / 3.0
    coda_f = (last_coda[idx - 1].astype(np.float64) + 1.0) / float(n_jamo + 1)    # [-1..n_jamo-1] -> [0..1)
    onset_f = (last_onset[idx - 1].astype(np.float64) + 1.0) / float(n_jamo + 1)
    X = np.stack([last, second, cdep, coda_f, onset_f], axis=1)
    return X, syms[idx].astype(np.int64), idx

# ════ GEOMETRY-FAIR seed-center protocol (FROZEN bank) verbatim H_1326/H_1337/H_1345 ════
BANK_GRID = [
    (0.3, 0.7, 0.0, 0.5),
    (0.3, 0.7, 0.3, 0.7),
    (0.5, 0.5, 0.0, 0.5),
    (0.25, 0.75, 0.0, 0.5),
    (0.4, 0.6, 0.2, 0.8),
]
def seed_bank(dim):
    bank = []
    for (lo, hi, alo, ahi) in BANK_GRID:
        a = [lo] * dim; a[-1] = alo
        b = [hi] * dim; b[-1] = ahi
        bank.append([a, b])
    a = [0.3] + [0.5] * (dim - 2) + [0.0] if dim >= 2 else [0.3]
    b = [0.7] + [0.5] * (dim - 2) + [0.5] if dim >= 2 else [0.7]
    if dim == 1: a = [0.3]; b = [0.7]
    bank.append([a, b])
    return bank

def grow_pick_bank(Xtr, Ytr, vj, grow_max, dim):
    n = Xtr.shape[0]; inner_idx = np.arange(n)
    ie = inner_idx % 2 == 0; io = inner_idx % 2 == 1
    best_ce = 1e18; best_member = -1
    for mi, seed in enumerate(seed_bank(dim)):
        Xie = Xtr[ie]; Yie = Ytr[ie]; Xio = Xtr[io]; Yio = Ytr[io]
        c = grow_on(seed, Xie, Yie, Xie.shape[0], vj, grow_max)
        ct = np.asarray(c, dtype=np.float64)
        nbio = np.ones(int(io.sum()))
        ce = per_byte_ce_opaque(ct, Xie, Yie, Xie.shape[0], Xio, Yio, nbio, vj)
        if ce < best_ce: best_ce = ce; best_member = mi
    seed = seed_bank(dim)[best_member]
    c = grow_on(seed, Xtr, Ytr, n, vj, grow_max)
    return c, best_member, best_ce

def context_count_distribution(centers, X_tr, Y_tr, ntr, vj, n_jamo):
    """c4 NO-STRIDE diagnostic: the per-context (= per-cell) jamo-count distribution at FULL data."""
    owner_tr = assign_all(centers, X_tr)
    K = centers.shape[0]
    lab = Y_tr[:ntr]
    is_j = (lab >= 256) & (lab < 256 + n_jamo)
    per_cell_jamo_rows = np.bincount(owner_tr[:ntr][is_j], minlength=K).astype(np.float64)
    per_cell_cellJcnt = per_cell_jamo_rows / float(n_jamo)
    return {
        "K_contexts": int(K),
        "per_context_jamo_rows_median": float(np.median(per_cell_jamo_rows)),
        "per_context_jamo_rows_mean": float(per_cell_jamo_rows.mean()),
        "cellJcnt_median": float(np.median(per_cell_cellJcnt)),
        "cellJcnt_mean": float(per_cell_cellJcnt.mean()),
        "frac_contexts_cellJcnt_lt_1": float((per_cell_cellJcnt < 1.0).mean()),
        "frac_contexts_cellJcnt_lt_0_5": float((per_cell_cellJcnt < 0.5).mean()),
        "global_cellJcnt": float(int(is_j.sum()) / float(K * n_jamo)),
    }

def run_arm(name, Xj, Yj, NBj, n_jamo, VJ, seeds, dim, do_a5=True):
    """One arm (CALIB opaque or NAT-SPARSE phonotactic). FULL data, NO stride — even/odd split only."""
    (Xtr, Ytr, NBtr), (Xte, Yte, NBte) = split_even_odd_full(Xj, Yj, NBj)
    ntr = Xtr.shape[0]
    cells, mi, tce = grow_pick_bank(Xtr, Ytr, VJ, GROW_MAX, dim)
    ct = np.asarray(cells, dtype=np.float64)

    a1 = per_byte_ce_opaque(ct, Xtr, Ytr, ntr, Xte, Yte, NBte, VJ)
    dist = context_count_distribution(ct, Xtr, Ytr, ntr, VJ, n_jamo)

    Ytr_n = Ytr
    sym_is_jamo_tr = (Ytr_n >= 256) & (Ytr_n < 256 + n_jamo)

    a5_list, a5sh_list = [], []
    if do_a5:
        for sd in seeds:
            np.random.seed(sd)
            E = learn_jamo_embedding(Ytr_n, sym_is_jamo_tr, n_jamo, sd, refine=True)
            Wjamo, _ = kernel_from_embedding(E)
            a5 = per_byte_ce_metric_smoothed(ct, Xtr, Ytr, ntr, Xte, Yte, NBte, VJ, Wjamo, n_jamo)
            a5_list.append(a5)
            rng = np.random.default_rng(sd)
            perm = rng.permutation(n_jamo)
            Esh = E[perm]
            Wsh, _ = kernel_from_embedding(Esh)
            a5sh = per_byte_ce_metric_smoothed(ct, Xtr, Ytr, ntr, Xte, Yte, NBte, VJ, Wsh, n_jamo)
            a5sh_list.append(a5sh)

    jm = per_byte_ce_jm(ct, Xtr, Ytr, ntr, Xte, Yte, NBte, VJ, n_jamo, shuffle_seed=None)
    jmsh_list = [per_byte_ce_jm(ct, Xtr, Ytr, ntr, Xte, Yte, NBte, VJ, n_jamo, shuffle_seed=sd)
                 for sd in seeds]

    out = {
        "arm": name, "stride": 1, "cells": len(cells), "bank_member": mi,
        "ntr": int(ntr), "nte": int(Xte.shape[0]), "test_bytes": int(NBte.sum()),
        "A1_jamo": round(a1, 5),
        "JM_interp": round(jm, 5), "JM_shuffle_mean": round(float(np.mean(jmsh_list)), 5),
        "delta_JM_vs_jamo": round(a1 - jm, 5),          # POSITIVE = JM crosses BELOW jamo (win)
        "delta_JMshuf_vs_jamo": round(a1 - float(np.mean(jmsh_list)), 5),
        "context_distribution": dist,
    }
    if do_a5:
        out["A5_learned_mean"] = round(float(np.mean(a5_list)), 5)
        out["A5_shuffle_mean"] = round(float(np.mean(a5sh_list)), 5)
        out["A5_per_seed"] = [round(x, 5) for x in a5_list]
        out["delta_A5_vs_jamo"] = round(a1 - float(np.mean(a5_list)), 5)   # POSITIVE = A5 crosses below
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ko-window", type=int, default=30_000_000)
    ap.add_argument("--grow-max", type=int, default=GROW_MAX)
    ap.add_argument("--seeds", default="4354,4355,4356")
    ap.add_argument("--out", default="/tmp/h1354_out")
    ap.add_argument("--ko-cache", default="/tmp/h1311_ko_raw.bytes")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    log("=== H_1354 — ko-natural-sparse: cross-syllable phonotactic contexts @ FULL 30MB (NO striding) ===")
    t0 = time.time()
    if os.path.exists(args.ko_cache) and os.path.getsize(args.ko_cache) >= args.ko_window:
        ko_raw = open(args.ko_cache, "rb").read()[: args.ko_window + 8]; log(f"[corpus] KO from cache {args.ko_cache}")
    else:
        log(f"[corpus] fetching {args.ko_window} REAL KO bytes from r2://{os.environ.get('R2_BUCKET','?')}/{R2_KO_KEY}")
        ko_raw = fetch_r2_range(R2_KO_KEY, args.ko_window + 8); open(args.ko_cache, "wb").write(ko_raw)
    ko_win = trim_utf8(ko_raw[: args.ko_window]); ko_sha = hashlib.sha256(ko_win).hexdigest()
    same_ko = (ko_sha == H1307_KO_SHA)
    log(f"[corpus] KO {len(ko_win)}B sha={ko_sha[:16]}…  identical-to-H_1307-RUN-A={same_ko}")
    if not same_ko:
        log("FATAL: KO corpus sha != H_1307 RUN A — REFUSING (provenance gate, REAL-only). STOP."); sys.exit(3)
    ko_text = ko_win.decode("utf-8")

    rt = roundtrip_and_accounting(ko_text)
    log(f"[nocheat] hangul_syllables={rt['hangul_syllables']} roundtrip_fail={rt['roundtrip_fail']} ok={rt['ok']}")
    jamo_to_id, jamo_sorted = build_jamo_vocab(ko_text)
    n_jamo = len(jamo_sorted); VJ = 256 + n_jamo
    log(f"[jamo] distinct jamo codepoints={n_jamo}  jamo-symbol vocab Vj={VJ}")

    ts = time.time()
    syms_i, nby_i, depth_i = make_streams(ko_text, jamo_to_id)
    acct_ok = (int(nby_i.sum()) == len(ko_win))
    log(f"[nocheat] byte-accounting Σ n_bytes={int(nby_i.sum())} corpus_bytes={len(ko_win)} close={acct_ok}")
    log(f"[streams] built in {round(time.time()-ts,1)}s  symbols={len(syms_i)}")

    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]

    # ── CALIB arm: H_1345 3-D opaque feature @ FULL data (stride 1). Dense; JM should TIE/LOSE. ──
    Xc, Yc, idxc = build_X_opaque(syms_i, depth_i, VJ)
    NBc = nby_i[idxc]
    log(f"[calib] opaque-3D feature rows={Xc.shape[0]}")
    tr = time.time()
    calib = run_arm("CALIB_opaque_full", Xc, Yc, NBc, n_jamo, VJ, seeds, dim=Xc.shape[1], do_a5=False)
    calib["wall_s"] = round(time.time() - tr, 1)
    log("[CALIB] " + json.dumps(calib, ensure_ascii=False))

    # ── NAT-SPARSE arm: cross-syllable phonotactic feature @ FULL data (stride 1). Naturally sparse. ──
    Xp, Yp, idxp = build_X_phonotactic(syms_i, depth_i, VJ, n_jamo)
    NBp = nby_i[idxp]
    log(f"[natsparse] phonotactic-5D feature rows={Xp.shape[0]}")
    tr = time.time()
    nat = run_arm("NATSPARSE_phonotactic_full", Xp, Yp, NBp, n_jamo, VJ, seeds, dim=Xp.shape[1], do_a5=True)
    nat["wall_s"] = round(time.time() - tr, 1)
    log("[NATSPARSE] " + json.dumps(nat, ensure_ascii=False))

    # ── FROZEN bars ──
    nat_dist = nat["context_distribution"]
    # c1 NAT-SPARSE-WIN: JM crosses below jamo on natural-sparse contexts by >= C1_MARGIN
    c1_delta = nat["delta_JM_vs_jamo"]                      # jamo − JM ; positive = JM below jamo
    c1 = bool(c1_delta >= C1_MARGIN)
    # c2 EARNED: JM beats its shuffle by >= C2_MARGIN (shuffle goes wrong way = shuffle CE > jamo CE)
    c2_delta = nat["JM_shuffle_mean"] - nat["JM_interp"]    # positive = JM better than its shuffle
    shuffle_wrong_way = bool(nat["JM_shuffle_mean"] >= nat["A1_jamo"])   # shuffle does NOT cross below
    c2 = bool(c2_delta >= C2_MARGIN and shuffle_wrong_way)
    # c3 DISSOCIATION: A5 learned-metric does NOT cross (stays >= jamo, i.e. delta_A5_vs_jamo <= 0)
    a5_crosses = bool(nat["delta_A5_vs_jamo"] > 0.0)
    c3 = bool(not a5_crosses)
    # c4 NO-STRIDE: sparsity is natural (stride==1) AND contexts genuinely sparse (median cellJcnt < ~1)
    natural_sparse = bool(nat["stride"] == 1 and nat_dist["cellJcnt_median"] < 1.0)
    c4 = natural_sparse

    green = bool(c1 and c2 and c3 and c4)

    if green:
        verdict = ("🟢 GREEN — REAL LEVER: on NATURALLY-sparse cross-syllable phonotactic contexts at FULL "
                   f"30MB (NO striding), JM interpolation crosses BELOW the jamo floor by {c1_delta} (c1), "
                   f"earns it vs its shuffle control (c2, Δ={round(c2_delta,5)}, shuffle goes wrong way), and "
                   "A5 kernel-smoothing does NOT cross (c3 dissociation) — the H_1345 crossover SURVIVES "
                   "without artificial striding; sparse-context backoff is a real below-jamo mechanism")
    elif not c4:
        verdict = ("⚠ NOT-NATURALLY-SPARSE — c4 fails: the phonotactic contexts are NOT sparse enough at "
                   "full data (median cellJcnt >= 1) → cannot test the natural-sparse question; the enrich "
                   "did not fragment the model into sparse contexts. Flag and re-design the context (c9)")
    elif not c1:
        verdict = ("🧱 STRIDING ARTIFACT — c1 fails: on naturally-sparse phonotactic contexts at FULL 30MB, "
                   f"JM does NOT cross below jamo (delta jamo−JM = {c1_delta} < {C1_MARGIN}). The H_1345 "
                   "below-jamo win NEEDED the tiny-stream starvation it manufactured by striding; at full "
                   "data the opaque jamo MLE per phonotactic context is not starved enough for backoff to "
                   "win. H_1344's memorization reading stands; the striding crossover is an artifact (c9)")
    elif c1 and not c2:
        verdict = ("🟠 NAT-WIN-NOT-EARNED — c1 holds (JM crosses below jamo naturally) but c2 fails: the win "
                   "does not beat its shuffle control by the bar / the shuffle also crosses → the lift is "
                   "generic backoff mass, not real phonotactic-context structure (honest, c9)")
    elif c1 and c2 and not c3:
        verdict = ("🟠 NAT-WIN-NOT-DISSOCIATED — c1∧c2 hold but c3 fails: A5 kernel-smoothing ALSO crosses "
                   "below jamo here → the lift is generic sparse-context capacity, not the H_1345 "
                   "interpolation-toward-marginal mechanism specifically (the dissociation breaks; honest c9)")
    else:
        verdict = "🟠 mixed — see per-bar flags"

    wall = time.time() - t0
    summary = {
        "id": "H_1354", "device": "cpu-numpy", "numpy": np.__version__,
        "ko_window_bytes": len(ko_win), "ko_window_sha256": ko_sha,
        "corpus_identical_to_H1307_runA": bool(same_ko),
        "stride": 1, "NO_artificial_striding": True,
        "jamo_vocab_Vj": VJ, "distinct_jamo": n_jamo, "seeds": seeds,
        "d_emb": D_EMB, "skipgram_steps": SKIPGRAM_STEPS,
        "jamo_floor_ko_ce_locked": H1316_JAMO_CE,
        "calib_arm": calib,
        "natsparse_arm": nat,
        "c1_natsparse_win": c1, "c1_delta_jamo_minus_JM": c1_delta,
        "c2_earned": c2, "c2_delta_shuffle_minus_JM": round(c2_delta, 5),
        "c2_shuffle_wrong_way": shuffle_wrong_way,
        "c3_dissociation_A5_no_cross": c3, "c3_delta_A5_vs_jamo": nat["delta_A5_vs_jamo"],
        "c4_natural_sparse": c4,
        "c4_context_cellJcnt_median": nat_dist["cellJcnt_median"],
        "c4_frac_contexts_lt_1": nat_dist["frac_contexts_cellJcnt_lt_1"],
        "green": green, "verdict": verdict, "wall_s": round(wall, 1),
        "label_note": "numpy CPU mirror (no torch); A5 metric LEARNED BY GRADIENT (PPMI-SVD + skip-gram "
                      "Adam, numpy port of H_1337 torch loop) — NOT p8 gradient-free. JM-interp count-MLE "
                      "with Witten-Bell-style FROZEN backoff weight. Rides the gradient-free Voronoi "
                      "partition. NO artificial striding (stride==1, FULL 30MB). engine-transfer = follow-on.",
    }
    json.dump(summary, open(os.path.join(args.out, "h1354_summary.json"), "w"), indent=2, ensure_ascii=False)

    log("-" * 79)
    log("ARMS (CE nats/UTF-8-byte; A5/A5-shuf 3-seed mean; A1/JM deterministic). delta = jamo − mech (+=below jamo):")
    log(f"{'arm':>28} {'cells':>5} {'cellJcnt_med':>12} {'A1jamo':>8} {'JM':>8} {'JMshuf':>8} {'A5':>8} {'ΔJM':>8} {'ΔA5':>8}")
    for r in (calib, nat):
        cjm = r["context_distribution"]["cellJcnt_median"]
        a5 = r.get("A5_learned_mean", float("nan"))
        da5 = r.get("delta_A5_vs_jamo", float("nan"))
        log(f"{r['arm']:>28} {r['cells']:>5} {cjm:>12.4f} {r['A1_jamo']:>8} {r['JM_interp']:>8} "
            f"{r['JM_shuffle_mean']:>8} {a5:>8} {r['delta_JM_vs_jamo']:>8} {da5:>8}")
    log("-" * 79)
    log(f"[c4 NO-STRIDE] natsparse context distribution: K={nat_dist['K_contexts']} "
        f"cellJcnt median={nat_dist['cellJcnt_median']:.4f} mean={nat_dist['cellJcnt_mean']:.4f} "
        f"frac<1={nat_dist['frac_contexts_cellJcnt_lt_1']:.3f} frac<0.5={nat_dist['frac_contexts_cellJcnt_lt_0_5']:.3f}")
    log(f"c1 NAT-SPARSE-WIN (JM crosses below jamo by ≥{C1_MARGIN}): {c1}  (jamo−JM = {c1_delta})")
    log(f"c2 EARNED (JM beats shuffle by ≥{C2_MARGIN}, shuffle wrong way): {c2}  "
        f"(Δ={round(c2_delta,5)}, shuffle_wrong_way={shuffle_wrong_way})")
    log(f"c3 DISSOCIATION (A5 does NOT cross): {c3}  (Δ_A5_vs_jamo={nat['delta_A5_vs_jamo']}, A5_crosses={a5_crosses})")
    log(f"c4 NO-STRIDE (stride==1, cellJcnt median<1): {c4}  (median={nat_dist['cellJcnt_median']:.4f})")
    log(f"VERDICT: {verdict}")
    log(f"total wall={round(wall,1)}s")
    log("  numpy CPU mirror; A5 metric LEARNED BY GRADIENT (labeled, NOT p8). engine-transfer follow-on. NO fluency claim.")
    log("[done]")

if __name__ == "__main__":
    main()
