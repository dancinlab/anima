#!/usr/bin/env python3
# h1337_ko_jamo_metric.py — H_1337: does a LEARNED jamo metric / embedding (learned from REAL corpus
# co-occurrence, jamo2vec-style) break BELOW the jamo 2.51335 floor, by letting the gradient-free
# predictor SHARE statistical strength across metric-near jamo (kernel-smoothing) — INJECTING info the
# OPAQUE one-hot jamo head LACKS (the H_1329 depletion criterion)?
#
# THE H_1329 DEPLETION TEST THIS LANE ANSWERS (H_1329 🧱, cross-mechanism HONEST-FLOOR):
#   raw 2.95342 · A1 jamo 2.51335 (FLOOR) · A2 partition 2.73046 · A3 indep-factor 3.07295 ·
#   A4 conditional-chain (joint) 2.75109.
#   H_1329 proved any mechanism modeling the within-jamo feature JOINT asymptotes to P(jamo|cell) =
#   the opaque head → ties, stays ABOVE jamo. H_1329's depletion test: a below-jamo win must INJECT
#   INFO THE OPAQUE JAMO HEAD LACKS. The opaque head treats jamo as 51 OPAQUE atoms (one-hot, no
#   similarity — does NOT know ㄱ~ㅋ). A LEARNED jamo metric lets similar jamo SHARE strength = NEW info.
#
# THE NEW MECHANISM (A5 — learned-jamo-metric kernel-smoothed head; FREEZE-justified):
#   A5 = the SAME per-cell OPAQUE-jamo count head as A1 (identical alphabet/axis, SAME Fix-A bank,
#   SAME gradient-free Voronoi partition) but each per-cell next-jamo distribution is KERNEL-SMOOTHED
#   over a LEARNED jamo metric, so a count for jamo j ALSO lends partial strength to metric-near jamo j'.
#   The opaque head (A1) has NO notion that ㄱ~ㅋ, so any lift A5 buys over A1 is exactly the
#   LEARNED-METRIC INFORMATION the opaque head LACKS (the depletion criterion, met by construction).
#
#   Learned metric (TRAIN-ONLY, learned BY GRADIENT — labeled, NOT p8 gradient-free):
#     (1) jamo×jamo directed bigram co-occurrence C over the TRAIN stream (Hangul jamo only).
#     (2) PPMI(C) = max(0, log P(i,j)/(P(i)P(j))) — jamo2vec association weighting.
#     (3) low-dim embedding E (D_EMB=16) = truncated SVD of PPMI (E=U_D·sqrt(S_D)); THEN refined by a
#         FIXED number of skip-gram log-bilinear gradient steps (Adam, TRAIN-ONLY) seeded from the SVD
#         embedding → a genuinely GRADIENT-LEARNED jamo embedding (jamo2vec). metric = Euclidean in E.
#     (4) kernel w(j,j') = exp(-dist^2 / (2 h^2)), bandwidth h = MEDIAN pairwise train-jamo distance
#         (Silverman-style FIXED heuristic, NO per-run tuning). self-weight w(j,j)=1.
#   Smoothed head: ñ_k[j] = Σ_{j'} w(j,j') n_k[j'] ; P_k(j) = ñ_k[j]/Σ ñ_k.  byte symbols scored
#   EXACTLY as A1 (no smoothing) → ONLY diff A5-vs-A1 = the jamo-space kernel smoothing over the
#   learned metric, isolating the learned-metric information.
#
# GREEN iff (M1 BELOW-JAMO: A5 < jamo 2.51335 by >=0.03 AND < raw 2.95342)
#       AND (M2 EARNED: A5 < RANDOM-metric control by >=0.05 — win is LEARNED structure not smoothing)
#       AND (M3 ATTRIBUTION: A5 < A1 opaque baseline — gain is the learned-metric info opaque lacks).
# M1 fail → even a learned metric does not beat the opaque head (deeper floor, 🧱).
# M2 fail → the gain is smoothing not learned structure (random metric pools as well, 🟠).
#
# REAL Korean only (NO synthetic, p1-p8): SAME R2 web corpus as H_1307 RUN A / H_1316 / H_1326 / H_1329.
# KO window sha256 ASSERTED == H_1307 RUN A. R2 keys env-only at fetch time (c7). SCALE-HONEST:
# toy/DIRECTIONAL; metric learned BY GRADIENT (labeled, not p8); engine-transfer = follow-on; NO fluency claim.

import argparse, hashlib, json, os, sys, time, unicodedata
import numpy as np

try:
    import torch
except Exception as e:  # pragma: no cover
    print("FATAL: torch import failed:", e); sys.exit(2)

# ── FROZEN knobs (verbatim from H_1306/H_1307/H_1316/H_1326/H_1329) ─────────────
GROW_MAX = 40
SPLIT_THRESH_CE = 0.05
MIN_OWNED = 8
LAPLACE = 1.0
H1307_CEILING_KO_CE = 2.95342
H1316_JAMO_CE = 2.51335
M1_MARGIN = 0.03
M2_MARGIN = 0.05
CALIB_TOL = 0.0005
H1307_KO_SHA = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
R2_KO_KEY = "anima-7b/web/kor/shard0000.bytes"
HANGUL_LO, HANGUL_HI = 0xAC00, 0xD7A3
# ── A5 learned-metric knobs (FROZEN in FREEZE; NO per-run tuning) ───────────────
D_EMB = 16            # embedding dim (< distinct jamo ~51 → genuine compression)
SKIPGRAM_STEPS = 400  # FIXED gradient refine steps (skip-gram log-bilinear, Adam, TRAIN-ONLY)
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

# ════ jamo decomposition + streams (verbatim from H_1316/H_1326/H_1329) ══════════
def roundtrip_and_accounting(text):
    bad = 0; n_syll = 0
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            n_syll += 1
            nfc = unicodedata.normalize("NFC", unicodedata.normalize("NFD", ch))
            if nfc.encode("utf-8") != ch.encode("utf-8"): bad += 1
    return {"hangul_syllables": n_syll, "roundtrip_fail": bad, "ok": bad == 0}

def build_jamo_vocab(text):
    jset = set()
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            for jc in unicodedata.normalize("NFD", ch): jset.add(ord(jc))
    jamo_sorted = sorted(jset)
    return {cp: 256 + i for i, cp in enumerate(jamo_sorted)}, jamo_sorted

def syll_jamo_nbytes(njamo):
    if njamo == 3: return [1, 1, 1]
    if njamo == 2: return [2, 1]
    if njamo == 1: return [3]
    out = [1] * njamo; out[0] += (3 - njamo) if njamo < 3 else 0; return out

def make_streams(text, jamo_to_id):
    """syms (jamo-id 256+rank or byte 0..255) · nby · depth. Verbatim jamo decomposition from H_1316."""
    syms, nby, depth = [], [], []
    d = 0
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            nfd = unicodedata.normalize("NFD", ch)
            nb = syll_jamo_nbytes(len(nfd))
            for j, jc in enumerate(nfd):
                jcp = ord(jc)
                syms.append(jamo_to_id[jcp]); nby.append(nb[j])
                d = 0 if j == 0 else d + 1; depth.append(d)
        else:
            for b in ch.encode("utf-8"):
                syms.append(int(b)); nby.append(1)
                d = d + 1 if 0x80 <= b <= 0xBF else 0; depth.append(d)
    return (np.asarray(syms, np.int64), np.asarray(nby, np.int64), np.asarray(depth, np.int64))

# ── engine-native mitosis (BYTE-FAITHFUL to H_1306..H_1329) ─────────────────────
def assign_all(centers_t, X_t):
    return torch.argmin(torch.cdist(X_t, centers_t, p=2), dim=1)

def all_heads(Y_t, owner, K, ntr, vj, dev):
    Hmat = torch.full((K, vj), LAPLACE, dtype=torch.float64, device=dev)
    flat = owner[:ntr] * vj + Y_t[:ntr]
    Hmat.view(-1).index_add_(0, flat, torch.ones(flat.shape[0], dtype=torch.float64, device=dev))
    return Hmat / Hmat.sum(dim=1, keepdim=True)

def owned_ce(Y_t, owner, k, ntr, p_row):
    mask = (owner[:ntr] == k)
    if not mask.any(): return -1.0
    return -torch.log(p_row[Y_t[:ntr][mask]] + 1e-12).mean().item()

def grow_on(centers, X_tr, Y_tr, ntr, vj, dev, grow_max):
    centers = [list(c) for c in centers]
    while len(centers) < grow_max:
        ct = torch.tensor(centers, dtype=torch.float64, device=dev)
        owner = assign_all(ct, X_tr); K = len(centers); owntr = owner[:ntr]
        owned_n = torch.bincount(owntr, minlength=K).cpu().numpy()
        Hmat = all_heads(Y_tr, owner, K, ntr, vj, dev)
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
        ax = int(torch.argmax(pts.var(dim=0, unbiased=False)).item())
        col = pts[:, ax]; m = col.shape[0]; scol, _ = torch.sort(col)
        med = scol[m // 2].item() if m % 2 == 1 else ((scol[m//2-1] + scol[m//2]) / 2.0).item()
        lo_mask = col <= med; hi_mask = col > med
        if int(lo_mask.sum().item()) == 0 or int(hi_mask.sum().item()) == 0: break
        c_lo = pts[lo_mask].mean(dim=0).cpu().numpy().tolist()
        c_hi = pts[hi_mask].mean(dim=0).cpu().numpy().tolist()
        centers = [centers[i] for i in range(len(centers)) if i != pick] + [c_lo, c_hi]
    return centers

def split_even_odd(X, *arrs, stride):
    X = X[::stride]; arrs = [a[::stride] for a in arrs]
    idx = np.arange(X.shape[0]); e = idx % 2 == 0; o = idx % 2 == 1
    out_tr = [X[e]] + [a[e] for a in arrs]; out_te = [X[o]] + [a[o] for a in arrs]
    return out_tr, out_te

# ── OPAQUE-id per-byte CE (A1 target = jamo id) verbatim from H_1326/H_1329 ──────
def per_byte_ce_opaque(centers_t, X_tr_t, Y_tr_t, ntr, X_te_t, Y_te_t, NB_te, vj, dev):
    owner_tr = assign_all(centers_t, X_tr_t)
    Hmat = all_heads(Y_tr_t, owner_tr, centers_t.shape[0], ntr, vj, dev)
    owner_te = assign_all(centers_t, X_te_t)
    p = Hmat[owner_te, Y_te_t]; nll = -torch.log(p + 1e-12)
    nb = torch.tensor(NB_te, dtype=torch.float64, device=dev)
    return nll.sum().item() / float(nb.sum().item())

# ══════════ A5 — LEARNED-METRIC kernel-smoothed per-byte CE (THE NEW MECHANISM) ═══════════
def learn_jamo_embedding(Y_tr_n, sym_is_jamo_tr, n_jamo, seed, dev, refine=True):
    """Learn a jamo embedding from TRAIN bigram co-occurrence: PPMI → SVD init → skip-gram gradient
       refine (Adam, TRAIN-ONLY). Returns E (n_jamo × D_EMB) numpy. jamo-id = sym-256 (rank).
       The metric = Euclidean distance in E. LEARNED BY GRADIENT (labeled NOT p8 gradient-free)."""
    # directed bigram counts over consecutive jamo positions (both endpoints Hangul jamo)
    C = np.zeros((n_jamo, n_jamo), dtype=np.float64)
    prev = -1
    for i in range(len(Y_tr_n)):
        if sym_is_jamo_tr[i]:
            j = int(Y_tr_n[i]) - 256
            if prev >= 0:
                C[prev, j] += 1.0
            prev = j
        else:
            prev = -1
    # PPMI
    total = C.sum()
    if total <= 0:
        return np.zeros((n_jamo, D_EMB), dtype=np.float64)
    Pij = C / total
    Pi = Pij.sum(axis=1, keepdims=True) + 1e-12
    Pj = Pij.sum(axis=0, keepdims=True) + 1e-12
    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log((Pij + 1e-12) / (Pi * Pj))
    ppmi = np.maximum(0.0, pmi)
    # truncated SVD init
    d = min(D_EMB, n_jamo)
    U, S, Vt = np.linalg.svd(ppmi, full_matrices=False)
    E0 = U[:, :d] * np.sqrt(S[:d] + 1e-12)[None, :]
    if E0.shape[1] < D_EMB:
        E0 = np.concatenate([E0, np.zeros((n_jamo, D_EMB - E0.shape[1]))], axis=1)
    if not refine:
        return E0
    # skip-gram log-bilinear gradient refine (Adam) on the train bigrams, TRAIN-ONLY, FIXED steps.
    # objective: maximize Σ_ij C[i,j] log σ(E_i·F_j) + negative sampling — implemented as a small
    # torch optimization seeded from E0 (this is the literal "learned by gradient" embedding).
    dev_e = dev
    Ew = torch.tensor(E0, dtype=torch.float64, device=dev_e, requires_grad=True)
    Fw = torch.tensor(E0.copy(), dtype=torch.float64, device=dev_e, requires_grad=True)
    Ct = torch.tensor(C, dtype=torch.float64, device=dev_e)
    rowsum = Ct.sum(dim=1, keepdim=True) + 1e-12
    Pcond = Ct / rowsum                                  # P(j|i) empirical, TRAIN-only
    wrow = (Ct.sum(dim=1) / Ct.sum())                    # P(i) weighting
    opt = torch.optim.Adam([Ew, Fw], lr=SKIPGRAM_LR)
    g = torch.Generator(device="cpu").manual_seed(seed)  # only affects nothing here; refine is det.
    for _ in range(SKIPGRAM_STEPS):
        opt.zero_grad()
        logits = Ew @ Fw.t()                              # n×n
        logp = torch.log_softmax(logits, dim=1)
        # cross-entropy of the empirical conditional bigram dist (TRAIN), P(i)-weighted
        loss = -(wrow[:, None] * Pcond * logp).sum()
        loss = loss + 1e-4 * (Ew.pow(2).sum() + Fw.pow(2).sum())  # L2 reg (FIXED)
        loss.backward(); opt.step()
    return Ew.detach().cpu().numpy()

def kernel_from_embedding(E, dev):
    """Gaussian kernel over Euclidean distance in E; bandwidth h = MEDIAN pairwise distance (FIXED)."""
    Et = torch.tensor(E, dtype=torch.float64, device=dev)
    D = torch.cdist(Et, Et, p=2)                          # n×n distances
    n = D.shape[0]
    iu = torch.triu_indices(n, n, offset=1, device=dev)
    pw = D[iu[0], iu[1]]
    h = torch.median(pw).item()
    if h <= 1e-9: h = 1.0
    W = torch.exp(-(D * D) / (2.0 * h * h))
    W.fill_diagonal_(1.0)
    return W, h

def per_byte_ce_metric_smoothed(centers_t, X_tr_t, Y_tr_t, ntr, X_te_t, Y_te_t, NB_te, vj, dev,
                                Wjamo, n_jamo):
    """A5: per-cell OPAQUE-jamo Laplace count head (identical to A1) but the JAMO sub-block of each
       cell's count vector is KERNEL-SMOOTHED over the learned metric: ñ_k[j]=Σ_j' W[j,j'] n_k[j'].
       byte symbols (id<256) scored exactly as A1 (no smoothing). isolates the learned-metric info."""
    K = centers_t.shape[0]
    owner_tr = assign_all(centers_t, X_tr_t)
    # raw Laplace counts per cell over the FULL vj alphabet (jamo ids are 256..256+n_jamo-1)
    Hcnt = torch.full((K, vj), LAPLACE, dtype=torch.float64, device=dev)
    flat = owner_tr[:ntr] * vj + Y_tr_t[:ntr]
    Hcnt.view(-1).index_add_(0, flat, torch.ones(flat.shape[0], dtype=torch.float64, device=dev))
    # split byte block [0:256] (untouched) and jamo block [256:256+n_jamo] (kernel-smoothed)
    byte_blk = Hcnt[:, :256]
    jamo_blk = Hcnt[:, 256:256 + n_jamo]                  # K × n_jamo raw Laplace counts
    # ñ_k[j] = Σ_j' W[j,j'] n_k[j']  →  (K×n_jamo) @ (n_jamo×n_jamo)^T ; W symmetric
    jamo_smoothed = jamo_blk @ Wjamo.t()
    Hsm = torch.cat([byte_blk, jamo_smoothed], dim=1)
    P = Hsm / Hsm.sum(dim=1, keepdim=True)
    owner_te = assign_all(centers_t, X_te_t)
    p = P[owner_te, Y_te_t]; nll = -torch.log(p + 1e-12)
    nb = torch.tensor(NB_te, dtype=torch.float64, device=dev)
    return nll.sum().item() / float(nb.sum().item())

# ── partition feature builder (opaque-id 3-D, verbatim from H_1326/H_1329) ───────
def build_X_jamo(syms, depth, vj):
    n = len(syms); idx = np.arange(4, n - 1)
    last = syms[idx - 1].astype(np.float64) / float(vj)
    second = syms[idx - 2].astype(np.float64) / float(vj)
    cdep = depth[idx - 1].astype(np.float64) / 3.0
    return np.stack([last, second, cdep], axis=1), syms[idx].astype(np.int64), idx

# ════ GEOMETRY-FAIR seed-center protocol (FROZEN bank) verbatim H_1326/H_1329 ════
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

def grow_pick_bank(Xtr, Ytr, vj, dev, grow_max, dim):
    Xtr_t = torch.tensor(Xtr, dtype=torch.float64, device=dev)
    Ytr_t = torch.tensor(Ytr, dtype=torch.int64, device=dev)
    n = Xtr.shape[0]; inner_idx = np.arange(n)
    ie = inner_idx % 2 == 0; io = inner_idx % 2 == 1
    best_ce = 1e18; best_member = -1
    for mi, seed in enumerate(seed_bank(dim)):
        Xie = torch.tensor(Xtr[ie], dtype=torch.float64, device=dev)
        Yie = torch.tensor(Ytr[ie], dtype=torch.int64, device=dev)
        Xio = torch.tensor(Xtr[io], dtype=torch.float64, device=dev)
        Yio = torch.tensor(Ytr[io], dtype=torch.int64, device=dev)
        c = grow_on(seed, Xie, Yie, Xie.shape[0], vj, dev, grow_max)
        ct = torch.tensor(c, dtype=torch.float64, device=dev)
        nbio = np.ones(int(io.sum()))
        ce = per_byte_ce_opaque(ct, Xie, Yie, Xie.shape[0], Xio, Yio, nbio, vj, dev)
        if ce < best_ce: best_ce = ce; best_member = mi
    seed = seed_bank(dim)[best_member]
    c = grow_on(seed, Xtr_t, Ytr_t, n, vj, dev, grow_max)
    return c, best_member, best_ce

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ko-window", type=int, default=30_000_000)
    ap.add_argument("--ko-stride", type=int, default=300)
    ap.add_argument("--grow-max", type=int, default=GROW_MAX)
    ap.add_argument("--seeds", default="4337,4338,4339")
    ap.add_argument("--out", default="/tmp/h1337_out")
    ap.add_argument("--ko-cache", default="/tmp/h1311_ko_raw.bytes")
    ap.add_argument("--cpu", action="store_true")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    if args.cpu or not torch.cuda.is_available():
        dev = torch.device("cpu"); log("=== H_1337 — ko-jamo-metric (learned-metric kernel-smoothed) (CPU) ===")
    else:
        dev = torch.device("cuda"); cap = torch.cuda.get_device_capability(0)
        log(f"=== H_1337 — ko-jamo-metric (sm_{cap[0]}{cap[1]}) ===")
        log(f"device={torch.cuda.get_device_name(0)} torch={torch.__version__}")
        _ = (torch.randn(256, 256, device=dev) @ torch.randn(256, 256, device=dev)).sum().item()
        torch.cuda.synchronize()

    t0 = time.time()
    # ── REAL corpus, BYTE-IDENTICAL to H_1307 RUN A / H_1316 / H_1326 / H_1329 ──
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

    # ── G0 raw-byte re-port (sanity) ──
    ko_bytes = np.frombuffer(ko_win, dtype=np.uint8).astype(np.int64)
    is_cont = (ko_bytes >= 0x80) & (ko_bytes <= 0xBF)
    raw_depth = np.zeros(len(ko_bytes), np.int64); d = 0
    for i in range(len(ko_bytes)):
        d = d + 1 if is_cont[i] else 0; raw_depth[i] = d
    Xr, Yr, idxr = build_X_jamo(ko_bytes, raw_depth, 256)
    NBr = np.ones(len(ko_bytes), np.int64)[idxr]
    (Xtr_r, Ytr_r, NBtr_r), (Xte_r, Yte_r, NBte_r) = split_even_odd(Xr, Yr, NBr, stride=args.ko_stride)
    cr, mr, _ = grow_pick_bank(Xtr_r, Ytr_r, 256, dev, args.grow_max, 3)
    ctr = torch.tensor(cr, dtype=torch.float64, device=dev)
    g0 = per_byte_ce_opaque(ctr, torch.tensor(Xtr_r, dtype=torch.float64, device=dev),
                            torch.tensor(Ytr_r, dtype=torch.int64, device=dev), Xtr_r.shape[0],
                            torch.tensor(Xte_r, dtype=torch.float64, device=dev),
                            torch.tensor(Yte_r, dtype=torch.int64, device=dev), NBte_r, 256, dev)
    log(f"[G0 raw-byte] ce={round(g0,5)} cells={len(cr)} member={mr}  (H_1316 reproduced 2.95342)")

    # ── jamo streams + partition (intact opaque-id, the A1 geometry) ──
    syms_i, nby_i, depth_i = make_streams(ko_text, jamo_to_id)
    log(f"[nocheat] byte-accounting: Σ n_bytes={int(nby_i.sum())} corpus_bytes={len(ko_win)} "
        f"close={int(nby_i.sum())==len(ko_win)}")
    Xj, Yj, idxj = build_X_jamo(syms_i, depth_i, VJ)
    NBj = nby_i[idxj]
    (Xtr, Ytr, NBtr), (Xte, Yte, NBte) = split_even_odd(Xj, Yj, NBj, stride=args.ko_stride)
    # geometry-fair grown cells (SHARED by A1 and A5 — identical partition, isolates the head)
    cells, mi, tce = grow_pick_bank(Xtr, Ytr, VJ, dev, args.grow_max, Xj.shape[1])
    ct = torch.tensor(cells, dtype=torch.float64, device=dev)
    Xtr_t = torch.tensor(Xtr, dtype=torch.float64, device=dev)
    Ytr_t = torch.tensor(Ytr, dtype=torch.int64, device=dev)
    Xte_t = torch.tensor(Xte, dtype=torch.float64, device=dev)
    Yte_t = torch.tensor(Yte, dtype=torch.int64, device=dev)
    ntr = Xtr.shape[0]

    # ── A1 jamo opaque-id (CALIBRATION anchor = 2.51335; M3 baseline) ──
    a1_ce = per_byte_ce_opaque(ct, Xtr_t, Ytr_t, ntr, Xte_t, Yte_t, NBte, VJ, dev)
    calib_ok = abs(a1_ce - H1316_JAMO_CE) <= CALIB_TOL
    log(f"[A1 jamo opaque-id] ce={round(a1_ce,5)} cells={len(cells)} member={mi} "
        f"calib-vs-2.51335(±{CALIB_TOL})={calib_ok}")
    if not calib_ok:
        log("WARN: A1 jamo did NOT reproduce 2.51335 byte-exact — geometry protocol calibration off. "
            "Continuing but flagging the verdict (honest, c9).")

    # ── learned jamo metric (TRAIN-ONLY) + A5 smoothed head; per seed ──
    Ytr_n = Ytr  # numpy int64 jamo-id stream (train)
    sym_is_jamo_tr = (Ytr_n >= 256) & (Ytr_n < 256 + n_jamo)
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]

    a5_list, a5rand_list = [], []
    emb_med_h = None
    for sd in seeds:
        torch.manual_seed(sd); np.random.seed(sd)
        # LEARNED metric: PPMI→SVD→skip-gram gradient refine (TRAIN-ONLY)
        E = learn_jamo_embedding(Ytr_n, sym_is_jamo_tr, n_jamo, sd, dev, refine=True)
        Wjamo, h_learn = kernel_from_embedding(E, dev)
        a5_ce = per_byte_ce_metric_smoothed(ct, Xtr_t, Ytr_t, ntr, Xte_t, Yte_t, NBte, VJ, dev,
                                            Wjamo, n_jamo)
        a5_list.append(a5_ce); emb_med_h = round(h_learn, 4)
        # RANDOM-metric control: random embedding of SAME dim (kernel + median-bandwidth rule identical)
        rng = np.random.default_rng(sd)
        Erand = rng.standard_normal((n_jamo, D_EMB))
        Wrand, h_rand = kernel_from_embedding(Erand, dev)
        a5r_ce = per_byte_ce_metric_smoothed(ct, Xtr_t, Ytr_t, ntr, Xte_t, Yte_t, NBte, VJ, dev,
                                             Wrand, n_jamo)
        a5rand_list.append(a5r_ce)
        log(f"[seed {sd}] " + json.dumps({"A5_learned_metric": round(a5_ce,5),
                                          "A5_random_metric": round(a5r_ce,5),
                                          "h_learn": round(h_learn,4), "h_rand": round(h_rand,4)}))

    a5_mean = float(np.mean(a5_list)); a5rand_mean = float(np.mean(a5rand_list))

    # ── FROZEN bars M1/M2/M3 ──
    m1_vs_jamo = bool(a5_mean < (a1_ce - M1_MARGIN))
    m1_vs_raw = bool(a5_mean < H1307_CEILING_KO_CE)
    m1 = bool(m1_vs_jamo and m1_vs_raw)
    m2 = bool((a5rand_mean - a5_mean) >= M2_MARGIN)
    m3 = bool(a5_mean < a1_ce)
    green = bool(m1 and m2 and m3)
    if green:
        verdict = ("🟢 GREEN — a LEARNED jamo metric breaks BELOW the jamo 2.51335 floor: the floor was "
                   "the OPAQUE-ATOM info limit (one-hot, no similarity); learned between-jamo similarity "
                   "is NEW info the opaque head LACKS, and it crosses below jamo (overturns the H_1329 "
                   "floor as an opaque-atom limit, not a terminal decomposition floor)")
    elif not m1:
        verdict = ("🧱 HONEST-FLOOR (opaque-atom limit) — M1 fails: even a LEARNED jamo metric does NOT "
                   "beat the jamo floor by the bar → the opaque per-cell jamo MLE is already information-"
                   "optimal at this scale; learned between-jamo similarity adds no exploitable below-jamo "
                   "signal (a deeper 🧱 than H_1329 — the floor is the opaque-atom info limit, confirmed "
                   "by a learned metric, not just re-factorization)")
    elif m1 and not m3:
        verdict = ("🟠 SMOOTHING-NOT-INFO — M1 holds but M3 fails: A5 ties/loses vs the opaque A1 baseline; "
                   "any gain is generic smoothing, not learned-metric info the opaque head lacks (c9)")
    else:
        verdict = ("🟠 SMOOTHING-NOT-STRUCTURE — M1∧M3 but M2 fails: a RANDOM metric pools just as well → "
                   "the gain is smoothing/over-pooling, NOT the LEARNED structure (honest, c9)")

    wall = time.time() - t0
    summary = {
        "id": "H_1337", "device": (torch.cuda.get_device_name(0) if dev.type == "cuda" else "cpu"),
        "torch": torch.__version__, "ko_window_bytes": len(ko_win), "ko_window_sha256": ko_sha,
        "corpus_identical_to_H1307_runA": bool(same_ko), "ko_stride": args.ko_stride,
        "grow_max": args.grow_max, "jamo_vocab_Vj": VJ, "distinct_jamo": n_jamo,
        "d_emb": D_EMB, "skipgram_steps": SKIPGRAM_STEPS, "skipgram_lr": SKIPGRAM_LR,
        "kernel_bandwidth_h_learned_lastseed": emb_med_h,
        "raw_ceiling_ko_ce": H1307_CEILING_KO_CE, "jamo_floor_ko_ce_locked": H1316_JAMO_CE,
        "g0_raw_byte_ce": round(g0, 5),
        "A1_jamo_opaque_ce": round(a1_ce, 5), "A1_calib_match_2_51335": calib_ok, "A1_bank_member": mi,
        "A5_learned_metric_ce_mean": round(a5_mean, 5), "A5_per_seed": [round(x,5) for x in a5_list],
        "A5_random_metric_ce_mean": round(a5rand_mean, 5), "A5rand_per_seed": [round(x,5) for x in a5rand_list],
        "delta_A5_vs_jamo": round(a5_mean - a1_ce, 5),
        "delta_random_minus_A5": round(a5rand_mean - a5_mean, 5),
        "M1_below_jamo": m1, "M1_vs_jamo": m1_vs_jamo, "M1_vs_raw": m1_vs_raw,
        "M2_earned": m2, "M3_attribution": m3,
        "green": green, "verdict": verdict, "seeds": seeds, "wall_s": round(wall, 1),
        "label_note": "A5 metric LEARNED BY GRADIENT (PPMI-SVD init + skip-gram Adam refine, TRAIN-ONLY) "
                      "— NOT p8 gradient-free; the smoothed count head is count-MLE. Rides the same "
                      "gradient-free Voronoi partition as A1 (identical cells). engine-transfer = follow-on.",
    }
    json.dump(summary, open(os.path.join(args.out, "h1337_summary.json"), "w"), indent=2, ensure_ascii=False)

    log("-" * 79)
    log("CE LADDER (nats/UTF-8-byte, geometry-FAIR; learned/random metric mean 3 seeds):")
    log(f"  raw-byte ceiling             = {H1307_CEILING_KO_CE}  (in-run G0 {round(g0,5)})")
    log(f"  A1 jamo (Fix-A protocol)     = {round(a1_ce,5)}  (calib vs H_1316 2.51335 = {calib_ok})")
    log(f"  A5 learned-metric smoothed   = {round(a5_mean,5)}  per-seed {[round(x,5) for x in a5_list]}")
    log(f"  A5 RANDOM-metric control     = {round(a5rand_mean,5)}  Δ(rand−A5)={round(a5rand_mean-a5_mean,5)}")
    log(f"M1 BELOW-JAMO (A5 < A1−{M1_MARGIN} AND < raw): {m1}  "
        f"(A5 {round(a5_mean,5)} vs A1 {round(a1_ce,5)}, Δ={round(a1_ce-a5_mean,5)})")
    log(f"M2 EARNED (A5 < random-metric by >={M2_MARGIN}): {m2}  (Δ={round(a5rand_mean-a5_mean,5)})")
    log(f"M3 ATTRIBUTION (A5 < A1 opaque): {m3}  (Δ={round(a1_ce-a5_mean,5)})")
    log(f"VERDICT: {verdict}")
    log(f"total wall={round(wall,1)}s")
    log("  metric LEARNED BY GRADIENT (labeled, NOT p8). engine-transfer DIRECTIONAL (follow-on). NO fluency claim.")
    log("[done]")

if __name__ == "__main__":
    main()
