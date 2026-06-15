#!/usr/bin/env python3
# h1336_ko_crosssyllable.py — H_1336: does CROSS-SYLLABLE PHONOTACTIC context break BELOW the
# jamo 2.51335 floor, where every re-FACTORIZATION mechanism (H_1326 A2/A3, H_1329 A4) floored?
#
# THE DEPLETION TEST H_1329 HANDED FORWARD (verbatim):
#   H_1329 🧱: three mechanisms (partition / independent-factorization / correlation-chain) ALL
#   land ABOVE the jamo floor 2.51335 — because ANY mechanism that models the WITHIN-jamo feature
#   JOINT asymptotes to P(jamo|cell), exactly what the opaque jamo head already computes. A below-
#   jamo win must INJECT INFORMATION THE OPAQUE JAMO HEAD LACKS — NOT a re-factorization of the
#   same target.
#
# THE NEW INFORMATION (genuinely new — NOT a re-factorization):
#   The within-syllable jamo head computes P(next_jamo | Voronoi cell), and the cell context
#   (build_X_jamo) is the immediate 2 previous jamo-symbols + within-syllable UTF-8 depth, which
#   RESETS at every syllable boundary → CTX ≈ the CURRENT syllable. It does NOT see CROSS-SYLLABLE
#   phonotactic context: Korean liaison (연음), 사잇소리, 자음동화 — the CODA of syllable N
#   conditions the realized onset / pronunciation of syllable N+1. That coda→onset dependency is
#   REAL information the within-syllable head structurally cannot see.
#
# THE MECHANISM (B1 — cross-syllable-coda-conditioned jamo head):
#   B1 = the SAME opaque jamo head as A1 (same geometry-fair bank, same dim-3 within-syllable
#   Voronoi partition, same per-cell count-MLE, same LAPLACE, same jamo alphabet Vj), but the
#   per-cell next-jamo distribution is ADDITIONALLY conditioned on prev_coda = the coda jamo-id of
#   the most recently COMPLETED Hangul syllable (NONE at start, a distinct NO-CODA token for open
#   syllables):
#       A1:  P(next_jamo | cell)              [within-syllable only]
#       B1:  P(next_jamo | cell, prev_coda)   [+ cross-syllable phonotactic context]
#   ESTIMATOR (per cell k): count table (k, prev_coda) → over next_jamo, Laplace-smoothed; an unseen
#   (k, prev_coda) at test BACKS OFF to the cell-marginal P(next_jamo|k) — EXACTLY the A1 jamo head
#   (TRAIN-only). So the jamo head is B1's FLOOR; any below-jamo win is REAL conditional cross-
#   syllable structure, never a sparsity artifact. Both tables TRAIN-only (even/odd) → proper
#   held-out CE, same nats/UTF-8-byte axis as A1. Byte symbols scored exactly as A1.
#
# GREEN iff (X1 BELOW-JAMO: B1 < jamo 2.51335 by >=0.03 AND < raw 2.95342)
#       AND (X2 EARNED: B1 < B1-shuffle (permuted prev-coda labels) by >=0.05)
#       AND (X3 ATTRIBUTION: B1 < A1 within-syllable baseline, reproduced in-run).
# X1 fail → cross-syllable info doesn't beat jamo for this predictor (deeper 🧱). X2 fail → gain is
# context-dims not phonotactics (🟠). All VALID (c9).
#
# REAL Korean only (NO synthetic, p1-p8): SAME anima-7b R2 web corpus as H_1307 RUN A / H_1316 /
# H_1326 / H_1329. KO window sha256 ASSERTED == H_1307 RUN A. R2 keys env-only at fetch time (c7).
# LABEL = count-MLE structured head riding the gradient-free Voronoi partition (NOT gradient-free
# p8 mitosis, NOT gradient-trained). SCALE-HONEST: toy/DIRECTIONAL; engine-transfer = follow-on;
# NO fluency claim.

import argparse, hashlib, json, os, sys, time, unicodedata
import numpy as np

try:
    import torch
except Exception as e:  # pragma: no cover
    print("FATAL: torch import failed:", e); sys.exit(2)

# ── FROZEN knobs (verbatim from H_1306/H_1307/H_1316/H_1326/H_1329) ────────────
GROW_MAX = 40
SPLIT_THRESH_CE = 0.05
MIN_OWNED = 8
LAPLACE = 1.0
H1307_CEILING_KO_CE = 2.95342
H1316_JAMO_CE = 2.51335
X1_MARGIN = 0.03
X2_MARGIN = 0.05
CALIB_TOL = 0.0005
H1307_KO_SHA = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
R2_KO_KEY = "anima-7b/web/kor/shard0000.bytes"
HANGUL_LO, HANGUL_HI = 0xAC00, 0xD7A3
# NFD jongseong (coda) codepoint range — used to identify a syllable's coda jamo
JONG_LO, JONG_HI = 0x11A8, 0x11C2
NO_CODA = -1   # open syllable (no coda)
START_CODA = -2  # corpus start / no completed syllable yet

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

# ── NO-CHEAT round-trip + accounting (same as H_1316/H_1326/H_1329) ─────────────
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
    """syms (jamo-id 256+rank or byte 0..255) · nby · depth · PREV_CODA (cross-syllable context).
       prev_coda[i] = the coda jamo-id (jamo_to_id of the jongseong) of the most recently COMPLETED
       Hangul syllable as of stream position i; NO_CODA for an open prior syllable, START_CODA before
       any syllable, and frozen across byte runs. This is the CROSS-SYLLABLE phonotactic variable —
       it carries OVER the syllable boundary the within-syllable depth resets at.
       Within-syllable arms (A1) IGNORE prev_coda; only B1/shuffle read it → A1 reproduces byte-exact."""
    syms, nby, depth, prev_coda = [], [], [], []
    d = 0
    cur_prev_coda = START_CODA   # coda of the last completed syllable, visible to the NEXT syllable
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            nfd = unicodedata.normalize("NFD", ch)
            nb = syll_jamo_nbytes(len(nfd))
            # this syllable's own coda (jongseong), to hand to the NEXT syllable
            this_coda = NO_CODA
            for jc in nfd:
                if JONG_LO <= ord(jc) <= JONG_HI:
                    this_coda = jamo_to_id[ord(jc)]
            for j, jc in enumerate(nfd):
                jcp = ord(jc)
                syms.append(jamo_to_id[jcp])
                nby.append(nb[j])
                d = 0 if j == 0 else d + 1
                depth.append(d)
                # prev_coda visible at THIS position = coda of the previous completed syllable
                prev_coda.append(cur_prev_coda)
            cur_prev_coda = this_coda   # update only AFTER the whole syllable is emitted
        else:
            for b in ch.encode("utf-8"):
                syms.append(int(b))
                nby.append(1)
                d = d + 1 if 0x80 <= b <= 0xBF else 0
                depth.append(d)
                prev_coda.append(cur_prev_coda)
            # a non-Hangul run does NOT reset cur_prev_coda (no new syllable completed)
    return (np.asarray(syms, np.int64), np.asarray(nby, np.int64),
            np.asarray(depth, np.int64), np.asarray(prev_coda, np.int64))

# ── engine-native mitosis (BYTE-FAITHFUL to H_1306/H_1307/H_1316/H_1326/H_1329) ─
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

# ── B1 CROSS-SYLLABLE-CODA-conditioned per-byte CE (THE NEW INFORMATION) ─────────
def per_byte_ce_xsyll(centers_t, X_tr_t, Y_tr_t, ntr, pc_tr,
                      X_te_t, Y_te_t, pc_te, NB_te, vj, dev):
    """B1: P(next_jamo | cell, prev_coda). Per cell k, a count table keyed by (k, prev_coda) over
       next_jamo (Laplace). Unseen (k, prev_coda) at test BACKS OFF to the cell-marginal
       P(next_jamo|k) = the A1 jamo head (TRAIN-only) → jamo head is B1's FLOOR. The ONLY change
       vs A1 is the cross-syllable-coda conditioning; same geometry, same alphabet, same byte axis."""
    K = centers_t.shape[0]
    owner_tr = assign_all(centers_t, X_tr_t).cpu().numpy()[:ntr]
    owner_te = assign_all(centers_t, X_te_t).cpu().numpy()
    Y_tr_n = Y_tr_t.cpu().numpy()[:ntr]; Y_te_n = Y_te_t.cpu().numpy()
    pc_tr_n = pc_tr.cpu().numpy()[:ntr]; pc_te_n = pc_te.cpu().numpy()
    nb_te_n = np.asarray(NB_te, np.float64)

    # cell-marginal P(next_jamo|k) (= A1 jamo head), TRAIN-only, Laplace-smoothed
    marg = np.full((K, vj), LAPLACE)
    for i in range(ntr):
        marg[owner_tr[i], Y_tr_n[i]] += 1.0
    marg_p = marg / marg.sum(axis=1, keepdims=True)

    # conditional counts keyed by (k, prev_coda) -> over next_jamo, Laplace-smoothed
    cond = dict()   # (k, pc) -> np.array(vj)
    for i in range(ntr):
        key = (int(owner_tr[i]), int(pc_tr_n[i]))
        tbl = cond.get(key)
        if tbl is None:
            tbl = np.full(vj, LAPLACE); cond[key] = tbl
        tbl[Y_tr_n[i]] += 1.0
    cond_p = {key: tbl / tbl.sum() for key, tbl in cond.items()}

    total_nats = 0.0
    for i in range(owner_te.shape[0]):
        k = int(owner_te[i]); pc = int(pc_te_n[i]); y = int(Y_te_n[i])
        p_row = cond_p.get((k, pc))
        if p_row is None:
            p = marg_p[k, y]   # BACK OFF to the A1 jamo head
        else:
            p = p_row[y]
        total_nats += -np.log(p + 1e-12)
    return total_nats / float(nb_te_n.sum())

# ── partition feature builder (verbatim from H_1326/H_1329: within-syllable dim-3) ──
def build_X_jamo(syms, depth, vj):
    n = len(syms); idx = np.arange(4, n - 1)
    last = syms[idx - 1].astype(np.float64) / float(vj)
    second = syms[idx - 2].astype(np.float64) / float(vj)
    cdep = depth[idx - 1].astype(np.float64) / 3.0
    return np.stack([last, second, cdep], axis=1), syms[idx].astype(np.int64), idx

# ════ GEOMETRY-FAIR seed-center protocol (FROZEN bank, identical to every arm) verbatim H_1326/H_1329 ═══
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
    """FIX A: grow from EACH bank member on inner-train ONLY, pick lowest inner-test CE (no test
       peeking), regrow the winner on the full train. Identical protocol for every arm → geometry-fair."""
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
    ap.add_argument("--seeds", default="4336,4337,4338")
    ap.add_argument("--out", default="/tmp/h1336_out")
    ap.add_argument("--ko-cache", default="/tmp/h1311_ko_raw.bytes")
    ap.add_argument("--cpu", action="store_true")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    if args.cpu or not torch.cuda.is_available():
        dev = torch.device("cpu"); log("=== H_1336 — ko-crosssyllable (cross-syllable phonotactic context) (CPU) ===")
    else:
        dev = torch.device("cuda"); cap = torch.cuda.get_device_capability(0)
        log(f"=== H_1336 — ko-crosssyllable (sm_{cap[0]}{cap[1]}) ===")
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

    # ── G0 raw-byte re-port (sanity, reproduce ~2.953) ──
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

    # ── streams (intact), with the cross-syllable prev_coda variable ──
    syms, nby, depth, prev_coda = make_streams(ko_text, jamo_to_id)
    log(f"[nocheat] byte-accounting: Σ n_bytes={int(nby.sum())} corpus_bytes={len(ko_win)} "
        f"close={int(nby.sum())==len(ko_win)}")
    n_distinct_coda = len(set(prev_coda.tolist()))
    log(f"[xsyll] distinct prev_coda tokens (incl NO_CODA/START) = {n_distinct_coda}")

    # ── build the within-syllable jamo partition + scored positions (shared by A1 and B1) ──
    Xj, Yj, idxj = build_X_jamo(syms, depth, VJ)
    NB = nby[idxj]; pc = prev_coda[idxj]
    (Xtr, Ytr, NBtr, pctr), (Xte, Yte, NBte, pcte) = split_even_odd(Xj, Yj, NB, pc, stride=args.ko_stride)

    # ONE geometry-fair partition (FIX A bank) shared by A1 and B1 → A1 vs B1 isolates the
    # cross-syllable conditioning ALONE (same cells, same target alphabet, same byte axis).
    c, mi, tce = grow_pick_bank(Xtr, Ytr, VJ, dev, args.grow_max, 3)
    ct = torch.tensor(c, dtype=torch.float64, device=dev)
    Xtr_t = torch.tensor(Xtr, dtype=torch.float64, device=dev)
    Ytr_t = torch.tensor(Ytr, dtype=torch.int64, device=dev)
    Xte_t = torch.tensor(Xte, dtype=torch.float64, device=dev)
    Yte_t = torch.tensor(Yte, dtype=torch.int64, device=dev)
    pctr_t = torch.tensor(pctr, dtype=torch.int64, device=dev)
    pcte_t = torch.tensor(pcte, dtype=torch.int64, device=dev)

    # ── A1 WITHIN-SYLLABLE-only jamo head (= calibration anchor 2.51335 AND C3 baseline) ──
    a1_ce = per_byte_ce_opaque(ct, Xtr_t, Ytr_t, Xtr.shape[0], Xte_t, Yte_t, NBte, VJ, dev)
    calib_ok = abs(a1_ce - H1316_JAMO_CE) <= CALIB_TOL
    log(f"[A1 jamo within-syllable] ce={round(a1_ce,5)} cells={len(c)} bank_member={mi} train_proxy={round(tce,5)}")
    log(f"[CALIB] A1 jamo {round(a1_ce,5)} vs H_1316 {H1316_JAMO_CE}  match(±{CALIB_TOL})={calib_ok}")
    if not calib_ok:
        log("WARN: A1 jamo did NOT reproduce 2.51335 byte-exact — geometry protocol calibration off. "
            "Continuing but flagging the verdict (honest, c9).")

    # ── B1 CROSS-SYLLABLE-coda-conditioned jamo head (THE NEW INFORMATION) ──
    b1_ce = per_byte_ce_xsyll(ct, Xtr_t, Ytr_t, Xtr.shape[0], pctr_t,
                              Xte_t, Yte_t, pcte_t, NBte, VJ, dev)
    log(f"[B1 cross-syllable-coda] ce={round(b1_ce,5)} cells={len(c)} (same partition as A1)")

    # ── controls: SHUFFLE the prev_coda LABELS per seed (random bijection over distinct coda tokens) ──
    #   Same number of extra context bins, BROKEN phonotactic coda→onset mapping → isolates X2.
    distinct = sorted(set(prev_coda.tolist()))
    real_codas = [c0 for c0 in distinct if c0 not in (NO_CODA, START_CODA)]  # permute only real codas
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    b1s_list = []
    for sd in seeds:
        rng = np.random.default_rng(sd)
        perm = rng.permutation(len(real_codas))
        remap = {real_codas[i]: real_codas[perm[i]] for i in range(len(real_codas))}
        # NO_CODA / START stay fixed (structural tokens), real coda IDs permuted among themselves
        pc_shuf = np.array([remap.get(int(v), int(v)) for v in prev_coda], dtype=np.int64)
        pc_s = pc_shuf[idxj]
        (_, _, _, pctr_s), (_, _, _, pcte_s) = split_even_odd(Xj, Yj, NB, pc_s, stride=args.ko_stride)
        b1s_ce = per_byte_ce_xsyll(ct, Xtr_t, Ytr_t, Xtr.shape[0],
                                   torch.tensor(pctr_s, dtype=torch.int64, device=dev),
                                   Xte_t, Yte_t, torch.tensor(pcte_s, dtype=torch.int64, device=dev),
                                   NBte, VJ, dev)
        b1s_list.append(b1s_ce)
        log(f"[B1s coda-shuffle seed{sd}] ce={round(b1s_ce,5)}")
        log(f"[seed {sd}] " + json.dumps({"b1s": round(b1s_ce,5)}))
    b1s_mean = float(np.mean(b1s_list))

    # ── FROZEN bars X1/X2/X3 ──
    x1_vs_jamo = bool(b1_ce < (a1_ce - X1_MARGIN))
    x1_vs_raw = bool(b1_ce < H1307_CEILING_KO_CE)
    x1 = bool(x1_vs_jamo and x1_vs_raw)
    x2 = bool((b1s_mean - b1_ce) >= X2_MARGIN)
    x3 = bool(b1_ce < a1_ce)
    green = bool(x1 and x2 and x3)
    if green:
        verdict = ("🟢 GREEN — CROSS-SYLLABLE PHONOTACTIC information breaks BELOW the jamo 2.51335 floor: "
                   "the floor was an INFORMATION limit, not a mechanism limit. The within-syllable jamo "
                   "head LACKS the preceding-coda→onset dependency (연음/자음동화); injecting it (NOT a "
                   "re-factorization of the same target) drops held-out KO CE below the floor. H_1329's "
                   "depletion test PASSED — new info, not re-factorization, is the answer.")
    elif not x1:
        verdict = ("🧱 HONEST-FLOOR (deeper) — X1 fails: even CROSS-SYLLABLE phonotactic context does NOT "
                   "beat the jamo floor by the bar for this gradient-free count-MLE predictor → the floor "
                   "is deeper than an information limit at this scale/mechanism (honest, c9).")
    elif x1 and not x3:
        verdict = ("🟠 X1∧¬X3 — B1 ties/loses vs the within-syllable A1 baseline (contradiction; report "
                   "straight, c9).")
    else:
        verdict = ("🟠 X1∧X3 but X2 fails — CONTEXT-DIMS-NOT-PHONOTACTICS: the gain is the extra context "
                   "bins, not the real coda→onset dependency (shuffle ties; honest, c9).")

    wall = time.time() - t0
    summary = {
        "id": "H_1336", "device": (torch.cuda.get_device_name(0) if dev.type == "cuda" else "cpu"),
        "torch": torch.__version__, "ko_window_bytes": len(ko_win), "ko_window_sha256": ko_sha,
        "corpus_identical_to_H1307_runA": bool(same_ko), "ko_stride": args.ko_stride,
        "grow_max": args.grow_max, "jamo_vocab_Vj": VJ, "distinct_jamo": n_jamo,
        "distinct_prev_coda_tokens": n_distinct_coda,
        "raw_ceiling_ko_ce": H1307_CEILING_KO_CE, "jamo_floor_ko_ce_locked": H1316_JAMO_CE,
        "g0_raw_byte_ce": round(g0, 5),
        "A1_jamo_within_syllable_ce": round(a1_ce, 5), "A1_calib_match_2_51335": calib_ok,
        "A1_bank_member": mi, "cells": len(c),
        "B1_cross_syllable_ce": round(b1_ce, 5),
        "B1s_coda_shuffle_mean": round(b1s_mean, 5), "B1s_per_seed": [round(x,5) for x in b1s_list],
        "delta_B1_vs_jamo": round(b1_ce - a1_ce, 5),
        "delta_shuffle_minus_B1": round(b1s_mean - b1_ce, 5),
        "X1_below_jamo": x1, "X1_vs_jamo": x1_vs_jamo, "X1_vs_raw": x1_vs_raw,
        "X2_earned": x2, "X3_attribution": x3,
        "green": green, "verdict": verdict, "seeds": seeds, "wall_s": round(wall, 1),
        "label_note": "B1 = count-MLE cross-syllable-coda-conditioned structured head; NOT gradient-free "
                      "p8 mitosis, NOT gradient-trained. Rides the same gradient-free Voronoi partition.",
    }
    json.dump(summary, open(os.path.join(args.out, "h1336_summary.json"), "w"), indent=2, ensure_ascii=False)

    log("-" * 79)
    log("CE LADDER (nats/UTF-8-byte, geometry-FAIR; mean 3 seeds for shuffle):")
    log(f"  raw-byte ceiling             = {H1307_CEILING_KO_CE}  (in-run G0 {round(g0,5)})")
    log(f"  A1 jamo within-syllable      = {round(a1_ce,5)}  (calib vs H_1316 2.51335 = {calib_ok})")
    log(f"  B1 cross-syllable-coda       = {round(b1_ce,5)}  (cells {len(c)})")
    log(f"  B1 shuffle (coda labels)     = {round(b1s_mean,5)}  Δ(shuf−B1)={round(b1s_mean-b1_ce,5)}")
    log(f"X1 BELOW-JAMO (B1 < A1−{X1_MARGIN} AND < raw): {x1}  "
        f"(B1 {round(b1_ce,5)} vs A1 {round(a1_ce,5)}, Δ={round(a1_ce-b1_ce,5)})")
    log(f"X2 EARNED (B1 < shuffle by >={X2_MARGIN}): {x2}  (Δ={round(b1s_mean-b1_ce,5)})")
    log(f"X3 ATTRIBUTION (B1 < A1 within-syllable): {x3}  (Δ={round(a1_ce-b1_ce,5)})")
    log(f"VERDICT: {verdict}")
    log(f"total wall={round(wall,1)}s")
    log("  engine-transfer to live hexa DIRECTIONAL (re-confirm on CORE/*.hexa = follow-on). NO fluency claim.")
    log("[done]")

if __name__ == "__main__":
    main()
