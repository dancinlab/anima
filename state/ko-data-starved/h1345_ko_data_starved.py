#!/usr/bin/env python3
# h1345_ko_data_starved.py — H_1345: H_1337 (🧱) closed the below-jamo question at 30MB by showing the
# OPAQUE per-cell jamo count-MLE is INFORMATION-OPTIMAL when data is DENSE — strength-sharing (learned-
# metric kernel-smoothing) and interpolation only help when per-cell counts are SPARSE. H_1337's own
# depletion test: "any below-jamo angle must find a regime where the opaque MLE is data-STARVED."
#
# H_1345 RUNS THAT DEPLETION TEST DIRECTLY: a LADDER over data size (sub-samples of the SAME H_1307 RUN A
# 30MB window, sha-asserted) where larger stride => fewer train rows per grown cell => SPARSE per-cell
# jamo counts. Two below-jamo mechanisms are scored vs the opaque jamo head AT EACH RUNG:
#   A5  = LEARNED-METRIC kernel-smoothing (VERBATIM the H_1337 mechanism: PPMI->SVD->skip-gram Adam refine
#         -> Gaussian kernel over Euclidean metric, median bandwidth; smooths the per-cell jamo count head)
#   JM  = JELINEK-MERCER interpolation (the classic sparse-data backoff): P = (1-l) P_cell + l P_global,
#         where P_global is the corpus-wide jamo marginal. l TIED to the SAME median-bandwidth-style FIXED
#         rule (no per-run tuning): l = MIN_OWNED / (MIN_OWNED + mean_cell_jamo_count) — Witten-Bell-style,
#         FROZEN; smaller cell counts => more backoff. byte symbols scored EXACTLY as A1 (no interp).
#
# THE QUESTION: at the STARVED end of the ladder, does strength-sharing / interpolation NOW beat jamo
# where it could NOT at 30MB? Map WHERE (if anywhere) the opaque MLE becomes beatable (the crossover).
#
# FROZEN bars (pre-registered FREEZE BEFORE the run; NOT moved — c9/p7):
#   D1 STARVED-WIN  : at the STARVED end, a strength-sharing/interp mechanism (best of A5, JM) beats jamo
#                     (A1) by >=0.03 (mean over 3 seeds).
#   D2 EARNED       : that winning mechanism beats its SHUFFLE control (jamo-id permuted metric for A5 /
#                     shuffled global marginal for JM) by >=0.05 — the win is real backoff structure.
#   D3 DENSE-REPRO  : at the DENSE end (30MB), reproduce H_1337's opaque-optimal — mechanism >= jamo
#                     (i.e. mechanism does NOT beat jamo; loses) — confirming the CROSSOVER.
#   GREEN iff D1 ∧ D2 ∧ D3  => the jamo floor is DATA-RICHNESS, not representation; below-jamo IS
#                     reachable when starved, and we have MAPPED the crossover.
#   No crossover (jamo wins at ALL sizes, D1 fails) => count-MLE family truly terminal — honest 🧱.
#
# REAL Korean only (NO synthetic, p1-p8): SAME R2 web corpus as H_1307 RUN A / H_1316 / H_1337. The
# FULL 30MB KO window sha256 ASSERTED == H_1307 RUN A; each ladder rung is a deterministic stride
# SUB-SAMPLE of that one sha-asserted window (each sub-sample's own sha logged). R2 keys env-only at
# fetch time (c7). SCALE-HONEST: toy/DIRECTIONAL numpy mirror; A5 metric LEARNED BY GRADIENT (labeled,
# NOT p8); engine-transfer = follow-on; NO fluency claim.

import argparse, hashlib, json, os, sys, time, unicodedata
import numpy as np

# ── FROZEN knobs (verbatim from H_1316/H_1326/H_1329/H_1337) ────────────────────
GROW_MAX = 40
SPLIT_THRESH_CE = 0.05
MIN_OWNED = 8
LAPLACE = 1.0
H1307_CEILING_KO_CE = 2.95342
H1316_JAMO_CE = 2.51335
D1_MARGIN = 0.03          # D1: best mechanism beats jamo by >= this at the starved end
D2_MARGIN = 0.05          # D2: winning mechanism beats its shuffle control by >= this
CALIB_TOL = 0.001         # A1 at the dense rung must reproduce 2.51335 within this (numpy port tol)
H1307_KO_SHA = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
R2_KO_KEY = "anima-7b/web/kor/shard0000.bytes"
HANGUL_LO, HANGUL_HI = 0xAC00, 0xD7A3
# ── A5 learned-metric knobs (FROZEN, verbatim H_1337; NO per-run tuning) ────────
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

# ════ jamo decomposition + streams (VECTORIZED; byte/symbol-identical to H_1316/H_1337) ═══════════
# NFD of a precomposed Hangul syllable S (0xAC00..0xD7A3) is arithmetic (Unicode 3.12):
#   Si = cp - 0xAC00 ;  L = 0x1100 + Si//588 ;  V = 0x1161 + (Si%588)//28 ;  T0 = Si%28 ;
#   if T0>0: T = 0x11A7 + T0 (3 jamo L,V,T) else (2 jamo L,V).  This matches unicodedata.normalize("NFD").
# NFC round-trips byte-identical for ALL such S (canonical composition is exact) → roundtrip_fail == 0
# by construction; we still ASSERT it on a sample for the no-cheat gate.
LJAMO = 0x1100; VJAMO = 0x1161; TJAMO = 0x11A7
SBASE = 0xAC00; NCOUNT = 588; TCOUNT = 28

def _decompose_cp(cp):
    """Return list of (jamo_codepoint, nbytes) for one char codepoint, lossless byte axis."""
    if SBASE <= cp <= HANGUL_HI:
        Si = cp - SBASE
        L = LJAMO + Si // NCOUNT
        V = VJAMO + (Si % NCOUNT) // TCOUNT
        T0 = Si % TCOUNT
        if T0:
            return [(L, 1), (V, 1), (TJAMO + T0, 1)]      # 3 jamo -> [1,1,1] (sum=3)
        return [(L, 2), (V, 1)]                            # 2 jamo -> [2,1]   (sum=3)
    return None

def roundtrip_and_accounting(text):
    """No-cheat: every Hangul syllable NFD->NFC round-trips byte-identical. Arithmetic NFD == library NFD
       for the precomposed block, so we ASSERT on the distinct codepoints actually present (decisive,
       cheap) rather than re-normalizing 8M chars."""
    cps = np.array([ord(c) for c in set(text)], dtype=np.int64)   # distinct codepoints only
    hang = cps[(cps >= SBASE) & (cps <= HANGUL_HI)]
    bad = 0
    for cp in hang.tolist():
        ch = chr(cp)
        nfc = unicodedata.normalize("NFC", unicodedata.normalize("NFD", ch))
        if nfc.encode("utf-8") != ch.encode("utf-8"): bad += 1
    # count syllables over the full text (vectorized)
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
    """VECTORIZED symbol/nbyte/depth streams. Non-Hangul -> one symbol per raw UTF-8 byte (id 0..255,
       depth = continuation-byte run). Hangul syllable -> jamo symbols (id 256+rank), depth 0,1,2.
       Byte-identical to the H_1316/H_1337 per-char loop (same ids, same nbytes, same depth)."""
    cps = np.frombuffer(text.encode("utf-32-le"), dtype=np.uint32).astype(np.int64)
    is_h = (cps >= SBASE) & (cps <= HANGUL_HI)
    syms = []; nby = []; depth = []
    sa = syms.append; na = nby.append; da = depth.append
    # build a per-codepoint expansion table for the Hangul chars present (cache)
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

# ── engine-native mitosis (numpy port, BYTE-FAITHFUL to H_1306..H_1337) ─────────
def assign_all(centers, X):
    # X: (N,D) centers: (K,D) -> argmin Euclidean
    d2 = ((X[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
    return np.argmin(d2, axis=1)

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

def split_even_odd(X, *arrs, stride):
    X = X[::stride]; arrs = [a[::stride] for a in arrs]
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

# ══════════ A5 — LEARNED-METRIC kernel-smoothed (VERBATIM H_1337 mechanism, numpy) ═══════════
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
    # skip-gram log-bilinear gradient refine (Adam), numpy port of the H_1337 torch loop.
    # objective: -(wrow * Pcond * log_softmax(E@F^T)).sum() + 1e-4 L2 ; Adam lr=0.05, 400 steps.
    Ew = E0.copy(); Fw = E0.copy()
    Ct = C
    rowsum = Ct.sum(axis=1, keepdims=True) + 1e-12
    Pcond = Ct / rowsum
    wrow = (Ct.sum(axis=1) / Ct.sum())[:, None]      # (n,1) P(i) weight
    mE = np.zeros_like(Ew); vE = np.zeros_like(Ew)
    mF = np.zeros_like(Fw); vF = np.zeros_like(Fw)
    b1, b2, eps, lr = 0.9, 0.999, 1e-8, SKIPGRAM_LR
    for t in range(1, SKIPGRAM_STEPS + 1):
        logits = Ew @ Fw.T                            # (n,n)
        m = logits.max(axis=1, keepdims=True)
        ex = np.exp(logits - m)
        sm = ex / ex.sum(axis=1, keepdims=True)       # softmax rows
        # grad of loss = -(wrow*Pcond*logp).sum(); d/dlogits = wrow*(sm*rowmass - Pcond)
        rowmass = (wrow * Pcond).sum(axis=1, keepdims=True)   # (n,1)
        dlog = wrow * Pcond_neg_grad(sm, Pcond, rowmass)
        gE = dlog @ Fw + 1e-4 * 2 * Ew
        gF = dlog.T @ Ew + 1e-4 * 2 * Fw
        for (W, g, mm, vv) in ((Ew, gE, mE, vE), (Fw, gF, mF, vF)):
            mm *= b1; mm += (1 - b1) * g
            vv *= b2; vv += (1 - b2) * (g * g)
            mhat = mm / (1 - b1 ** t); vhat = vv / (1 - b2 ** t)
            W -= lr * mhat / (np.sqrt(vhat) + eps)
    return Ew

def Pcond_neg_grad(sm, Pcond, rowmass):
    # d(-(Pcond*logp))/dlogits per row = sm*sum(Pcond) - Pcond  (Pcond rows are the targets)
    return sm * rowmass - Pcond

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

# ══════════ JM — JELINEK-MERCER interpolation with the GLOBAL jamo marginal ═══════════
def per_byte_ce_jm(centers, X_tr, Y_tr, ntr, X_te, Y_te, NB_te, vj, n_jamo, shuffle_seed=None):
    """P_cell(jamo) interpolated with the corpus-wide jamo marginal:
         P = (1-l_k) P_cell + l_k P_global   on the jamo block only (byte block scored as A1).
       l_k = MIN_OWNED / (MIN_OWNED + N_k_jamo)  (Witten-Bell-style, FROZEN; sparse cell -> more backoff).
       shuffle control (D2): permute the global jamo marginal (a wrong backoff distribution)."""
    K = centers.shape[0]
    owner_tr = assign_all(centers, X_tr)
    Hcnt = all_heads_counts(Y_tr, owner_tr, K, ntr, vj)      # Laplace counts
    # global jamo marginal from TRAIN jamo labels (counts over the jamo block, Laplace)
    jamo_lab = Y_tr[:ntr]
    is_j = (jamo_lab >= 256) & (jamo_lab < 256 + n_jamo)
    gcnt = np.full(n_jamo, LAPLACE, dtype=np.float64)
    np.add.at(gcnt, jamo_lab[is_j] - 256, 1.0)
    Pglobal = gcnt / gcnt.sum()
    if shuffle_seed is not None:
        Pglobal = np.random.default_rng(shuffle_seed).permutation(Pglobal)
    # per-cell jamo block
    byte_blk = Hcnt[:, :256]
    jamo_cnt = Hcnt[:, 256:256 + n_jamo]                     # K x n_jamo (Laplace)
    Nk_jamo = jamo_cnt.sum(axis=1, keepdims=True)            # per-cell jamo mass
    Pcell_j = jamo_cnt / Nk_jamo                             # per-cell jamo MLE
    # raw (pre-Laplace) jamo count for the backoff weight: subtract the Laplace mass we added
    Nk_raw = Nk_jamo - LAPLACE * n_jamo
    Nk_raw = np.maximum(Nk_raw, 0.0)
    lam = MIN_OWNED / (MIN_OWNED + Nk_raw)                   # (K,1) ; FROZEN Witten-Bell-style
    jamo_interp = (1.0 - lam) * Pcell_j + lam * Pglobal[None, :]
    # byte block: own normalized count head (A1, no interp)
    Pbyte = byte_blk / byte_blk.sum(axis=1, keepdims=True)
    # combine: the model still must place jamo-vs-byte mass. Use the per-cell jamo-vs-byte split from
    # the Laplace counts (the SAME mass split A1 uses), then interp WITHIN the jamo block.
    full_norm = Hcnt.sum(axis=1, keepdims=True)
    jamo_mass = jamo_cnt.sum(axis=1, keepdims=True) / full_norm     # P(label is jamo | cell)
    byte_mass = byte_blk.sum(axis=1, keepdims=True) / full_norm
    P = np.concatenate([byte_mass * Pbyte, jamo_mass * jamo_interp], axis=1)
    P = P / P.sum(axis=1, keepdims=True)
    owner_te = assign_all(centers, X_te)
    p = P[owner_te, Y_te]; nll = -np.log(p + 1e-12)
    return float(nll.sum() / float(NB_te.sum()))

# ── partition feature builder (opaque-id 3-D, verbatim H_1326/H_1337) ───────────
def build_X_jamo(syms, depth, vj):
    n = len(syms); idx = np.arange(4, n - 1)
    last = syms[idx - 1].astype(np.float64) / float(vj)
    second = syms[idx - 2].astype(np.float64) / float(vj)
    cdep = depth[idx - 1].astype(np.float64) / 3.0
    return np.stack([last, second, cdep], axis=1), syms[idx].astype(np.int64), idx

# ════ GEOMETRY-FAIR seed-center protocol (FROZEN bank) verbatim H_1326/H_1337 ════
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

def mean_cell_jamo_count(centers, X_tr, Y_tr, ntr, vj, n_jamo):
    owner_tr = assign_all(centers, X_tr)
    K = centers.shape[0]
    lab = Y_tr[:ntr]
    is_j = (lab >= 256) & (lab < 256 + n_jamo)
    # raw jamo rows per cell / (#cells * #jamo) = avg count per (cell,jamo) bin = sparsity proxy
    rows_j = int(is_j.sum())
    return rows_j / float(K * n_jamo)

def run_rung(syms_i, Xj, Yj, idxj, NBj, n_jamo, VJ, stride, seeds):
    """Run one ladder rung at the given stride over the PRE-BUILT full streams (built ONCE in main).
       Returns dict of A1/A5/A5-shuf/JM/JM-shuf means + meta."""
    (Xtr, Ytr, NBtr), (Xte, Yte, NBte) = split_even_odd(Xj, Yj, NBj, stride=stride)
    ntr = Xtr.shape[0]
    cells, mi, tce = grow_pick_bank(Xtr, Ytr, VJ, GROW_MAX, Xj.shape[1])
    ct = np.asarray(cells, dtype=np.float64)
    # sub-sample sha (provenance of THIS rung's strided stream)
    sub = syms_i[::stride]
    rung_sha = hashlib.sha256(sub.tobytes()).hexdigest()
    train_bytes_est = int(NBtr.sum())

    a1 = per_byte_ce_opaque(ct, Xtr, Ytr, ntr, Xte, Yte, NBte, VJ)
    mccount = mean_cell_jamo_count(ct, Xtr, Ytr, ntr, VJ, n_jamo)

    Ytr_n = Ytr
    sym_is_jamo_tr = (Ytr_n >= 256) & (Ytr_n < 256 + n_jamo)

    a5_list, a5sh_list = [], []
    for sd in seeds:
        np.random.seed(sd)
        E = learn_jamo_embedding(Ytr_n, sym_is_jamo_tr, n_jamo, sd, refine=True)
        Wjamo, h_learn = kernel_from_embedding(E)
        a5 = per_byte_ce_metric_smoothed(ct, Xtr, Ytr, ntr, Xte, Yte, NBte, VJ, Wjamo, n_jamo)
        a5_list.append(a5)
        # A5 SHUFFLE control: permute jamo-id rows of the LEARNED metric (wrong neighbor structure)
        rng = np.random.default_rng(sd)
        perm = rng.permutation(n_jamo)
        Esh = E[perm]
        Wsh, _ = kernel_from_embedding(Esh)
        a5sh = per_byte_ce_metric_smoothed(ct, Xtr, Ytr, ntr, Xte, Yte, NBte, VJ, Wsh, n_jamo)
        a5sh_list.append(a5sh)

    # JM interp (deterministic given partition; shuffle control = permuted global marginal, per seed)
    jm = per_byte_ce_jm(ct, Xtr, Ytr, ntr, Xte, Yte, NBte, VJ, n_jamo, shuffle_seed=None)
    jmsh_list = [per_byte_ce_jm(ct, Xtr, Ytr, ntr, Xte, Yte, NBte, VJ, n_jamo, shuffle_seed=sd)
                 for sd in seeds]

    return {
        "stride": stride, "train_bytes_est": train_bytes_est, "ntr": int(ntr),
        "cells": len(cells), "bank_member": mi, "rung_sha16": rung_sha[:16],
        "mean_cell_jamo_count": round(mccount, 4),
        "A1_jamo": round(a1, 5),
        "A5_learned_mean": round(float(np.mean(a5_list)), 5), "A5_per_seed": [round(x, 5) for x in a5_list],
        "A5_shuffle_mean": round(float(np.mean(a5sh_list)), 5),
        "JM_interp": round(jm, 5),
        "JM_shuffle_mean": round(float(np.mean(jmsh_list)), 5),
        "delta_A5_vs_jamo": round(float(np.mean(a5_list)) - a1, 5),
        "delta_JM_vs_jamo": round(jm - a1, 5),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ko-window", type=int, default=30_000_000)
    # LADDER strides: small stride = DENSE (lots of train rows), large stride = STARVED (sparse cells).
    # 5 rungs spanning ~3 orders of magnitude of data, dense->starved.
    ap.add_argument("--strides", default="300,1200,4800,19200,76800")
    ap.add_argument("--grow-max", type=int, default=GROW_MAX)
    ap.add_argument("--seeds", default="4345,4346,4347")
    ap.add_argument("--out", default="/tmp/h1345_out")
    ap.add_argument("--ko-cache", default="/tmp/h1311_ko_raw.bytes")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    log("=== H_1345 — ko-data-starved ladder (learned-metric smoothing + JM-interp vs jamo) — numpy CPU ===")
    t0 = time.time()
    # ── REAL corpus, BYTE-IDENTICAL to H_1307 RUN A ──
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

    # ── build the FULL symbol/byte/depth + X/Y streams ONCE (each rung just strides into them) ──
    ts = time.time()
    syms_i, nby_i, depth_i = make_streams(ko_text, jamo_to_id)
    acct_ok = (int(nby_i.sum()) == len(ko_win))
    log(f"[nocheat] byte-accounting Σ n_bytes={int(nby_i.sum())} corpus_bytes={len(ko_win)} close={acct_ok}")
    Xj, Yj, idxj = build_X_jamo(syms_i, depth_i, VJ)
    NBj = nby_i[idxj]
    log(f"[streams] built in {round(time.time()-ts,1)}s  symbols={len(syms_i)} train+test rows={Xj.shape[0]}")

    strides = [int(s) for s in args.strides.split(",") if s.strip()]
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    # DENSE end = smallest stride; STARVED end = largest stride.
    strides_sorted = sorted(strides)

    rungs = []
    for st in strides_sorted:
        tr = time.time()
        r = run_rung(syms_i, Xj, Yj, idxj, NBj, n_jamo, VJ, st, seeds)
        r["wall_s"] = round(time.time() - tr, 1)
        rungs.append(r)
        log(f"[rung stride={st}] " + json.dumps(r, ensure_ascii=False))

    dense = rungs[0]            # smallest stride
    starved = rungs[-1]         # largest stride

    # ── A1 dense calibration vs H_1316 2.51335 (numpy port; CALIB_TOL) ──
    calib_ok = abs(dense["A1_jamo"] - H1316_JAMO_CE) <= CALIB_TOL
    log(f"[calib] dense A1={dense['A1_jamo']} vs H_1316 {H1316_JAMO_CE} within ±{CALIB_TOL} = {calib_ok}")

    # ── FROZEN bars ──
    # D1 STARVED-WIN: at the starved end, best mechanism beats jamo by >= D1_MARGIN
    starved_a5_delta = dense_or_starved_delta(starved, "A5_learned_mean")
    starved_jm_delta = dense_or_starved_delta(starved, "JM_interp")
    best_starved_name = "A5" if starved["A5_learned_mean"] <= starved["JM_interp"] else "JM"
    best_starved_ce = min(starved["A5_learned_mean"], starved["JM_interp"])
    d1 = bool((starved["A1_jamo"] - best_starved_ce) >= D1_MARGIN)

    # D2 EARNED: the winning mechanism beats its shuffle control by >= D2_MARGIN at the starved end
    if best_starved_name == "A5":
        d2_delta = starved["A5_shuffle_mean"] - starved["A5_learned_mean"]
    else:
        d2_delta = starved["JM_shuffle_mean"] - starved["JM_interp"]
    d2 = bool(d2_delta >= D2_MARGIN)

    # D3 DENSE-REPRO: at the dense end, the (same) winning mechanism does NOT beat jamo (>= jamo) — crossover
    dense_best_ce = min(dense["A5_learned_mean"], dense["JM_interp"]) if best_starved_name == "min" \
        else (dense["A5_learned_mean"] if best_starved_name == "A5" else dense["JM_interp"])
    d3 = bool(dense_best_ce >= dense["A1_jamo"])   # mechanism loses to jamo at the dense end

    green = bool(d1 and d2 and d3 and calib_ok)
    if green:
        verdict = ("🟢 GREEN — the jamo floor is DATA-RICHNESS, not representation: at the STARVED end a "
                   f"strength-sharing/interp mechanism ({best_starved_name}) beats jamo by "
                   f"{round(starved['A1_jamo']-best_starved_ce,5)} (D1), earns it vs its shuffle control "
                   f"(D2, Δ={round(d2_delta,5)}), and at the DENSE end the SAME mechanism loses to jamo "
                   "(D3) — the crossover is MAPPED; below-jamo IS reachable when the opaque MLE is starved")
    elif not d1:
        verdict = ("🧱 HONEST-FLOOR (count-MLE family terminal) — D1 fails: even at the STARVED end the "
                   "opaque per-cell jamo MLE is NOT beaten by ≥0.03 by either strength-sharing or "
                   "interpolation → the count-MLE family is truly terminal across the data ladder; the "
                   "jamo floor is NOT merely a data-richness artifact (a deeper closure than H_1337)")
    elif d1 and not d2:
        verdict = ("🟠 STARVED-WIN-NOT-EARNED — D1 holds (a mechanism beats jamo when starved) but D2 fails: "
                   "the win does not beat its shuffle control by the bar → the lift is generic backoff mass, "
                   "not real structure (honest, c9)")
    elif d1 and d2 and not d3:
        verdict = ("🟠 NO-CROSSOVER-CONFIRM — D1∧D2 hold but D3 fails: the mechanism ALSO beats jamo at the "
                   "dense end → this contradicts H_1337's dense opaque-optimal; the numpy port / mechanism "
                   "differs from H_1337 — flag and reconcile before claiming a crossover (honest, c9)")
    else:
        verdict = "🟠 mixed / calibration-fail — see calib_ok and per-bar flags"
    if not calib_ok:
        verdict = ("⚠ CALIB-FLAG — dense A1 did NOT reproduce 2.51335 within ±0.001 (numpy port); "
                   "verdict flagged, treat as DIRECTIONAL. ") + verdict

    wall = time.time() - t0
    summary = {
        "id": "H_1345", "device": "cpu-numpy", "numpy": np.__version__,
        "ko_window_bytes": len(ko_win), "ko_window_sha256": ko_sha,
        "corpus_identical_to_H1307_runA": bool(same_ko),
        "strides_dense_to_starved": strides_sorted, "grow_max": args.grow_max,
        "jamo_vocab_Vj": VJ, "distinct_jamo": n_jamo, "seeds": seeds,
        "d_emb": D_EMB, "skipgram_steps": SKIPGRAM_STEPS,
        "raw_ceiling_ko_ce": H1307_CEILING_KO_CE, "jamo_floor_ko_ce_locked": H1316_JAMO_CE,
        "dense_A1_calib_match_2_51335": calib_ok, "dense_A1": dense["A1_jamo"],
        "ladder": rungs,
        "best_starved_mechanism": best_starved_name, "best_starved_ce": best_starved_ce,
        "starved_A1_jamo": starved["A1_jamo"],
        "D1_starved_win": d1, "D1_delta_jamo_minus_best": round(starved["A1_jamo"] - best_starved_ce, 5),
        "D2_earned": d2, "D2_delta_shuffle_minus_win": round(d2_delta, 5),
        "D3_dense_reproduce_opaque_optimal": d3,
        "D3_dense_best_minus_jamo": round(dense_best_ce - dense["A1_jamo"], 5),
        "green": green, "verdict": verdict, "wall_s": round(wall, 1),
        "label_note": "numpy CPU mirror (no torch); A5 metric LEARNED BY GRADIENT (PPMI-SVD + skip-gram "
                      "Adam, numpy port of H_1337 torch loop) — NOT p8 gradient-free. JM-interp count-MLE "
                      "with Witten-Bell-style FROZEN backoff weight. Rides the gradient-free Voronoi "
                      "partition. engine-transfer = follow-on.",
    }
    json.dump(summary, open(os.path.join(args.out, "h1345_summary.json"), "w"), indent=2, ensure_ascii=False)

    log("-" * 79)
    log("LADDER (dense→starved) CE per UTF-8-byte (mean 3 seeds for A5/shuffle):")
    log(f"{'stride':>8} {'train_B':>9} {'cells':>5} {'cellJcnt':>8} {'A1jamo':>8} {'A5':>8} {'A5shuf':>8} {'JM':>8} {'JMshuf':>8} {'ΔA5':>7} {'ΔJM':>7}")
    for r in rungs:
        log(f"{r['stride']:>8} {r['train_bytes_est']:>9} {r['cells']:>5} {r['mean_cell_jamo_count']:>8} "
            f"{r['A1_jamo']:>8} {r['A5_learned_mean']:>8} {r['A5_shuffle_mean']:>8} {r['JM_interp']:>8} "
            f"{r['JM_shuffle_mean']:>8} {r['delta_A5_vs_jamo']:>7} {r['delta_JM_vs_jamo']:>7}")
    log(f"D1 STARVED-WIN (best mech beats jamo by ≥{D1_MARGIN} at starved end): {d1}  "
        f"(jamo {starved['A1_jamo']} − best {best_starved_ce} = {round(starved['A1_jamo']-best_starved_ce,5)}; mech={best_starved_name})")
    log(f"D2 EARNED (winning mech beats its shuffle by ≥{D2_MARGIN}): {d2}  (Δ={round(d2_delta,5)})")
    log(f"D3 DENSE-REPRO (mech ≥ jamo at dense end = loses, confirms crossover): {d3}  "
        f"(dense mech {round(dense_best_ce,5)} − jamo {dense['A1_jamo']} = {round(dense_best_ce-dense['A1_jamo'],5)})")
    log(f"CALIB dense A1 vs 2.51335: {calib_ok}")
    log(f"VERDICT: {verdict}")
    log(f"total wall={round(wall,1)}s")
    log("  numpy CPU mirror; A5 metric LEARNED BY GRADIENT (labeled, NOT p8). engine-transfer follow-on. NO fluency claim.")
    log("[done]")

def dense_or_starved_delta(rung, key):
    return round(rung["A1_jamo"] - rung[key], 5)

if __name__ == "__main__":
    main()
