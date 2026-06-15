#!/usr/bin/env python3
# h1311_ko_richer_substrate.py — does a RICHER SUBSTRATE break the H_1307 ~2.9 nat/byte ceiling?
#
# H_1307 (#2213, 🟢 GREEN @ 30MB + 🟠 honest saturation) scaled the engine-native Korean mitosis
# grow-op (gradient-free, p8 — cells only SPLIT, error-targeted Voronoi) to a 50x real-KO corpus
# and found: MORE Korean data drops held-out KO next-byte CE to ~2.95, but then the CTX=4 / 3-D
# BYTE substrate SATURATES at a ~2.9 nat/byte ceiling (learning-curve flattens, EN drifts at
# 250k-pair density). The H_1307 NEXT pointer names this lever:
#   "does a RICHER substrate (longer context window / a learned per-cell head instead of raw
#    byte-trigram MLE) break past ~2.9? Is the ceiling capacity-bound or substrate-bound?"
#
# H_1311 holds the corpus + the mitosis grow-op FIXED (the verified H_1306/H_1307 _grow_on:
# error-targeted highest-owned-CE eligible cell → hi-var-axis owned-median split → two
# half-centroids; net +1 cell; gradient-free; cells only SPLIT) and varies ONLY the SUBSTRATE
# richness on a frozen ladder:
#   S0 = the H_1307 baseline substrate: FEAT = [last/255, second/255, cont_depth/3] (3-D), per-cell
#        raw next-byte count-MLE head (add-Laplace). The ~2.9 ceiling.
#   S1 = LONGER CONTEXT: FEAT = the last CTXk bytes (each /255) + cont_depth/3, for CTXk in {8,16,32}.
#        More bytes of history feed the Voronoi partition. SAME grow-op, SAME count-MLE head.
#        (the grow-op is dimension-agnostic — cdist/argmin over arbitrary FEAT_DIM — so this is a
#         pure substrate-richness change, no mechanism change.)
#   S2 = LEARNED PER-CELL HEAD: replace the raw count-MLE head with a per-cell CLOSED-FORM ridge
#        readout (gradient-free, Gauss-Jordan / normal-equations like H_1300 — NOT global backprop,
#        NOT per-cell SGD). Each cell fits p(next_byte | feat) = softmax over a ridge-regressed
#        score; still gradient-free per-cell closed-form. SAME grow-op, S0 features.
#
# This is the SAME deep hypothesis the from-scratch lane shares: is the ~2.9 ceiling CAPACITY-bound
# (only cell-count matters; a richer representation per cell does NOT help → the ceiling is the
# byte-task itself at this density) or SUBSTRATE-bound (a richer representation breaks 2.9 → the
# depth needs representation, matching the capability-vs-scale thesis)?
#
# FROZEN-FIRST bars (pre-registered .verdicts/1311_ko_richer_substrate/FREEZE.txt BEFORE the run,
# NOT moved — c9/p7; held-out DETERMINISTIC next-byte CROSS-ENTROPY, NO perplexity-as-truth, NO
# tune-to-green):
#   (Q1 BREAK-2.9)   does ANY richer substrate (S1/S2) push held-out KO CE BELOW the H_1307 ceiling
#                    2.9475 (RUN A) — report the drop per rung. (the headline.)
#   (R RETENTION)    EN CE under each richer substrate <= EN CE[that substrate's 2-cell seed] + 0.05
#                    (no catastrophic forgetting; the H_1300/H_1306/H_1307 property).
#   (C CONTROL)      SHUFFLE the ADDED context bytes (S1: permute the extra history columns across
#                    rows; S2: permute the feature rows fed to the ridge fit) → if KO CE STILL drops
#                    below S0, the gain was CAPACITY (more columns = more partition handles), NOT the
#                    richer REPRESENTATION (honest, anti-Goodhart). A richer substrate "really helps"
#                    ONLY if the intact richer substrate beats both S0 AND its shuffled control.
#   (T THROUGHPUT)   report final cells + GPU pairs/s per rung.
# VERDICT: ceiling is SUBSTRATE-bound IFF some intact richer substrate beats S0 by a real margin
#   AND beats its own shuffle control (representation, not capacity). Else CAPACITY-bound / byte-task
#   ceiling (richer substrate does NOT help, or only the shuffle-surviving capacity helps).
#
# FROZEN knobs (verbatim from H_1306/H_1307, NOT moved): V=256, GROW_MAX, SPLIT_THRESH_CE, MIN_OWNED,
#   LAPLACE; seed 2-cell centers from the H_1307 SEED_CENTERS pattern (extended per FEAT_DIM); even/odd
#   train/test split; ridge lambda fixed BEFORE the run.
#
# REAL Korean only (NO synthetic, p1-p8): the SAME anima-7b R2 web corpus windows as H_1307
# (r2://phanes/anima-7b/web/{kor,eng}/shard0000.bytes), pulled via boto3 range GET; the KO/EN window
# sha256 is asserted == the H_1307 RUN A manifest hashes so the corpus is provably identical. Secrets
# (R2 keys) are read from ENV ONLY at fetch time, never echoed/logged/committed (c7).
#
# SCALE-HONEST (a_scale_honest_scope, a_toy_scale_recheck): toy/DIRECTIONAL — same simple byte
# substrate family, summer GPU, engine-transfer to live hexa is a follow-on. NO fluency claim.

import argparse
import hashlib
import json
import os
import sys
import time

import numpy as np

try:
    import torch
except Exception as e:  # pragma: no cover
    print("FATAL: torch import failed:", e)
    sys.exit(2)

# ── FROZEN knobs (verbatim from H_1306 / H_1307) ───────────────────────────────
V = 256
GROW_MAX = 40
SPLIT_THRESH_CE = 0.05
MIN_OWNED = 8
LAPLACE = 1.0
RIDGE_LAMBDA = 1.0          # S2 per-cell ridge regularizer — FROZEN before the run
# H_1307 RUN A (stride-300, 30MB) is the ceiling this rung must break:
H1307_CEILING_KO_CE = 2.9475
# H_1307 RUN A corpus window hashes — assert the corpus is IDENTICAL (provenance, p7):
H1307_KO_SHA = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
H1307_EN_SHA = "31b4a5430441cfdbb496b59f392150e4aa748cde2ed1b7cedad10960f0bcaf73"

R2_KO_KEY = "anima-7b/web/kor/shard0000.bytes"
R2_EN_KEY = "anima-7b/web/eng/shard0000.bytes"


def log(*a):
    print(*a, flush=True)


# ── REAL corpus fetch from R2 (boto3 range GET; secrets env-only, never logged) ─
def fetch_r2_range(key, nbytes):
    import boto3
    from botocore.config import Config
    acct = os.environ["R2_ACCOUNT_ID"]
    bucket = os.environ["R2_BUCKET"]
    s3 = boto3.client(
        "s3",
        endpoint_url=f"https://{acct}.r2.cloudflarestorage.com",
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        config=Config(signature_version="s3v4", retries={"max_attempts": 5}),
    )
    obj = s3.get_object(Bucket=bucket, Key=key, Range=f"bytes=0-{nbytes - 1}")
    return obj["Body"].read()


def trim_utf8(b):
    for cut in range(0, 4):
        try:
            b[: len(b) - cut].decode("utf-8")
            return b[: len(b) - cut]
        except Exception:
            continue
    return b


def utf8_cont_depth(arr_u8):
    is_cont = (arr_u8 >= 0x80) & (arr_u8 <= 0xBF)
    depth = np.zeros(len(arr_u8), dtype=np.float64)
    d = 0
    for i in range(len(arr_u8)):
        d = d + 1 if is_cont[i] else 0
        depth[i] = d
    return depth


# ── SUBSTRATE feature builders — the LADDER (S0 baseline, S1 longer ctx, S2 same-as-S0 for ridge) ──
def make_pairs_s0(byte_arr):
    """H_1307 baseline substrate: FEAT=[last/255, second/255, cont_depth/3] (3-D)."""
    n = len(byte_arr)
    cont = utf8_cont_depth(byte_arr)
    idx = np.arange(4, n - 1)            # CTX=4 window start (verbatim H_1307)
    last = byte_arr[idx - 1].astype(np.float64) / 255.0
    second = byte_arr[idx - 2].astype(np.float64) / 255.0
    cdep = cont[idx - 1] / 3.0
    X = np.stack([last, second, cdep], axis=1)
    Y = byte_arr[idx].astype(np.int64)
    return X, Y


def make_pairs_ctxk(byte_arr, ctxk):
    """S1 LONGER CONTEXT: FEAT = [b[i-1]/255, ..., b[i-ctxk]/255, cont_depth[i-1]/3]  (ctxk+1 dims).
    More bytes of real history feeding the Voronoi partition. ctxk>=2 superset of S0's last+second."""
    n = len(byte_arr)
    cont = utf8_cont_depth(byte_arr)
    idx = np.arange(ctxk, n - 1)
    cols = []
    for j in range(1, ctxk + 1):
        cols.append(byte_arr[idx - j].astype(np.float64) / 255.0)
    cols.append(cont[idx - 1] / 3.0)
    X = np.stack(cols, axis=1)            # [N, ctxk+1]
    Y = byte_arr[idx].astype(np.int64)
    return X, Y


def shuffle_extra_cols(X, base_dims, seed):
    """CONTROL for S1: permute (across rows, independently per column) the ADDED history columns
    beyond the S0 base (cols [2 .. ctxk-1]; col 0=last, col 1=second kept; last col=cont kept).
    If KO CE still drops with the extra history DESTROYED row-wise, the gain was capacity (more
    columns = more partition handles), not the richer representation."""
    Xs = X.copy()
    rng = np.random.default_rng(seed)
    n = Xs.shape[0]
    last_col = Xs.shape[1] - 1            # cont depth column — keep aligned
    for c in range(base_dims, last_col):  # the ADDED history bytes
        Xs[:, c] = Xs[rng.permutation(n), c]
    return Xs


# ── engine-native mitosis (BYTE-FAITHFUL to the H_1306/H_1307 _grow_on; dimension-agnostic) ─────
def assign_all(centers_t, X_t):
    d2 = torch.cdist(X_t, centers_t, p=2)
    return torch.argmin(d2, dim=1)


def all_heads(Y_t, owner, K, ntr, dev):
    Hmat = torch.full((K, V), LAPLACE, dtype=torch.float64, device=dev)
    own = owner[:ntr]
    y = Y_t[:ntr]
    flat = own * V + y
    ones = torch.ones(flat.shape[0], dtype=torch.float64, device=dev)
    Hmat.view(-1).index_add_(0, flat, ones)
    Hmat = Hmat / Hmat.sum(dim=1, keepdim=True)
    return Hmat


def owned_ce(Y_t, owner, k, ntr, p_row):
    mask = (owner[:ntr] == k)
    if not mask.any():
        return -1.0
    yk = Y_t[:ntr][mask]
    return -torch.log(p_row[yk] + 1e-12).mean().item()


def score_ce(centers_t, X_tr, Y_tr, ntr, X_te, Y_te, dev):
    owner_tr = assign_all(centers_t, X_tr)
    K = centers_t.shape[0]
    Hmat = all_heads(Y_tr, owner_tr, K, ntr, dev)
    owner_te = assign_all(centers_t, X_te)
    p = Hmat[owner_te, Y_te]
    return -torch.log(p + 1e-12).mean().item()


# ── S2 LEARNED PER-CELL HEAD: per-cell closed-form RIDGE readout (gradient-free, Gauss-Jordan) ──
def ridge_heads_fit(centers_t, X_tr, Y_tr, ntr, dev, lam):
    """For each cell, fit a CLOSED-FORM ridge multinomial readout:
        W_k = (Phi^T Phi + lam I)^-1 Phi^T Onehot(Y)   over the cell's owned train rows,
    where Phi = [X | 1] (augmented). p(y|x) = softmax(W_k^T phi). Gradient-free normal-equations
    (the H_1300 closed-form lens), NOT backprop / SGD. Returns list of W_k tensors [d+1, V]."""
    owner = assign_all(centers_t, X_tr)[:ntr]
    K = centers_t.shape[0]
    Xt = X_tr[:ntr]
    Yt = Y_tr[:ntr]
    d = Xt.shape[1]
    ones = torch.ones((Xt.shape[0], 1), dtype=torch.float64, device=dev)
    Phi_all = torch.cat([Xt, ones], dim=1)         # [ntr, d+1]
    Iaug = torch.eye(d + 1, dtype=torch.float64, device=dev) * lam
    Ws = []
    for k in range(K):
        m = (owner == k)
        if int(m.sum().item()) < 2:
            Ws.append(None)
            continue
        Phi = Phi_all[m]                            # [nk, d+1]
        yk = Yt[m]
        Yoh = torch.zeros((Phi.shape[0], V), dtype=torch.float64, device=dev)
        Yoh[torch.arange(Phi.shape[0], device=dev), yk] = 1.0
        A = Phi.t() @ Phi + Iaug                    # [d+1, d+1]
        B = Phi.t() @ Yoh                           # [d+1, V]
        W = torch.linalg.solve(A, B)                # closed-form normal equations
        Ws.append(W)
    return Ws, owner


def ridge_score_ce(centers_t, X_tr, Y_tr, ntr, X_te, Y_te, dev, lam):
    Ws, _ = ridge_heads_fit(centers_t, X_tr, Y_tr, ntr, dev, lam)
    owner_te = assign_all(centers_t, X_te)
    ones = torch.ones((X_te.shape[0], 1), dtype=torch.float64, device=dev)
    Phi_te = torch.cat([X_te, ones], dim=1)
    # fallback count-MLE for cells the ridge couldn't fit (too few owned) — keep it well-defined
    Hmat = all_heads(Y_tr, assign_all(centers_t, X_tr), centers_t.shape[0], ntr, dev)
    nll = torch.zeros(X_te.shape[0], dtype=torch.float64, device=dev)
    for k in range(centers_t.shape[0]):
        m = (owner_te == k)
        if not m.any():
            continue
        if Ws[k] is None:
            p = Hmat[k][Y_te[m]]
            nll[m] = -torch.log(p + 1e-12)
        else:
            logits = Phi_te[m] @ Ws[k]              # [nk_te, V]
            logp = logits - torch.logsumexp(logits, dim=1, keepdim=True)
            nll[m] = -logp[torch.arange(int(m.sum().item()), device=dev), Y_te[m]]
    return nll.mean().item()


def grow_on(centers, X_tr, Y_tr, ntr, dev, grow_max):
    """Faithful port of the H_1306/H_1307 hexa _grow_on (gradient-free, cells only SPLIT — p8).
    Dimension-agnostic: works for any FEAT_DIM (the partition is L2 over whatever features)."""
    centers = [list(c) for c in centers]
    while len(centers) < grow_max:
        ct = torch.tensor(centers, dtype=torch.float64, device=dev)
        owner = assign_all(ct, X_tr)
        K = len(centers)
        owntr = owner[:ntr]
        owned_n = torch.bincount(owntr, minlength=K).cpu().numpy()
        Hmat = all_heads(Y_tr, owner, K, ntr, dev)
        local_ce = np.full(K, -1.0)
        for k in range(K):
            if owned_n[k] > 0:
                local_ce[k] = owned_ce(Y_tr, owner, k, ntr, Hmat[k])
        elig = [k for k in range(K) if owned_n[k] >= MIN_OWNED and local_ce[k] > SPLIT_THRESH_CE]
        if not elig:
            break
        pick = elig[0]
        bestce = local_ce[elig[0]]
        for k in elig[1:]:
            if local_ce[k] > bestce:
                bestce = local_ce[k]
                pick = k
        if len(centers) + 1 > grow_max:
            break
        pmask = (owntr == pick)
        pts = X_tr[:ntr][pmask]
        if pts.shape[0] == 0:
            break
        var = pts.var(dim=0, unbiased=False)
        ax = int(torch.argmax(var).item())
        col = pts[:, ax]
        m = col.shape[0]
        scol, _ = torch.sort(col)
        if m % 2 == 1:
            med = scol[m // 2].item()
        else:
            med = ((scol[m // 2 - 1] + scol[m // 2]) / 2.0).item()
        lo_mask = col <= med
        hi_mask = col > med
        if int(lo_mask.sum().item()) == 0 or int(hi_mask.sum().item()) == 0:
            break
        c_lo = pts[lo_mask].mean(dim=0).cpu().numpy().tolist()
        c_hi = pts[hi_mask].mean(dim=0).cpu().numpy().tolist()
        new_centers = [centers[i] for i in range(len(centers)) if i != pick] + [c_lo, c_hi]
        centers = new_centers
    return centers


def seed_centers_for_dim(d):
    """Extend the H_1307 SEED_CENTERS [[0.3,0.5,0.0],[0.7,0.5,0.5]] to FEAT_DIM=d: two seed cells,
    first feature 0.3/0.7 (the byte-history split), the rest at the H_1307 mid pattern 0.5 / 0.5,
    last (cont) col 0.0 / 0.5. Deterministic, fixed before the run."""
    a = [0.5] * d
    b = [0.5] * d
    a[0], b[0] = 0.3, 0.7
    a[-1], b[-1] = 0.0, 0.5
    return [a, b]


def split_even_odd(X, Y, stride):
    X, Y = X[::stride], Y[::stride]
    idx = np.arange(X.shape[0])
    return X[idx % 2 == 0], Y[idx % 2 == 0], X[idx % 2 == 1], Y[idx % 2 == 1]


def run_substrate(name, Xtr, Ytr, Xte, Yte, Xen, Yen, dev, grow_max, head, lam, base_dims=None):
    """Grow on a 3-point curve, score held-out KO + EN. head in {"mle","ridge"}."""
    d = Xtr.shape[1]
    seed = seed_centers_for_dim(d)
    Xtr_t = torch.tensor(Xtr, dtype=torch.float64, device=dev)
    Ytr_t = torch.tensor(Ytr, dtype=torch.int64, device=dev)
    Xte_t = torch.tensor(Xte, dtype=torch.float64, device=dev)
    Yte_t = torch.tensor(Yte, dtype=torch.int64, device=dev)
    Xen_t = torch.tensor(Xen, dtype=torch.float64, device=dev)
    Yen_t = torch.tensor(Yen, dtype=torch.int64, device=dev)
    n = Xtr.shape[0]
    nb1, nb3 = n // 3, n
    seed_t = torch.tensor(seed, dtype=torch.float64, device=dev)

    def sce(ct, ntr, Xq, Yq):
        if head == "ridge":
            return ridge_score_ce(ct, Xtr_t, Ytr_t, ntr, Xq, Yq, dev, lam)
        return score_ce(ct, Xtr_t, Ytr_t, ntr, Xq, Yq, dev)

    en_seed = sce(seed_t, nb1, Xen_t, Yen_t)
    t0 = time.time()
    c = grow_on(seed, Xtr_t, Ytr_t, n, dev, grow_max)
    grow_wall = time.time() - t0
    ct = torch.tensor(c, dtype=torch.float64, device=dev)
    ko_ce = sce(ct, n, Xte_t, Yte_t)
    en_ce = sce(ct, n, Xen_t, Yen_t)
    torch.cuda.synchronize()
    npairs = Xtr.shape[0] + Xte.shape[0] + Xen.shape[0]
    rec = {
        "substrate": name, "feat_dim": d, "head": head, "cells": len(c),
        "ko_ce": round(ko_ce, 5), "en_ce": round(en_ce, 5), "en_seed_ce": round(en_seed, 5),
        "grow_wall_s": round(grow_wall, 2),
        "throughput_pairs_per_s": round(npairs / max(grow_wall, 1e-9), 1),
    }
    log("  [substrate] " + json.dumps(rec))
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ko-window", type=int, default=30_000_000)
    ap.add_argument("--en-window", type=int, default=10_000_000)
    ap.add_argument("--ko-stride", type=int, default=300)   # H_1307 RUN A stride (same corpus density)
    ap.add_argument("--en-stride", type=int, default=600)
    ap.add_argument("--grow-max", type=int, default=GROW_MAX)
    ap.add_argument("--ctxk-ladder", default="8,16,32")
    ap.add_argument("--out", default="/tmp/h1311_out")
    ap.add_argument("--ko-cache", default="/tmp/h1311_ko_raw.bytes")
    ap.add_argument("--en-cache", default="/tmp/h1311_en_raw.bytes")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    assert torch.cuda.is_available(), "CUDA not available — REFUSING CPU (a_train_flame_forge)"
    dev = torch.device("cuda")
    cap = torch.cuda.get_device_capability(0)
    log(f"=== H_1311 — RICHER SUBSTRATE vs the H_1307 ~2.9 ceiling (RTX 5070 sm_{cap[0]}{cap[1]}) ===")
    log(f"device={torch.cuda.get_device_name(0)} cap={cap} torch={torch.__version__}")
    _t = (torch.randn(1024, 1024, device=dev) @ torch.randn(1024, 1024, device=dev)).sum().item()
    torch.cuda.synchronize()
    log(f"sm_{cap[0]}{cap[1]} kernel launch OK (sentinel {_t:.1f})")

    t0 = time.time()
    if os.path.exists(args.ko_cache) and os.path.getsize(args.ko_cache) >= args.ko_window:
        ko_raw = open(args.ko_cache, "rb").read()[: args.ko_window + 8]
        log(f"[corpus] KO from cache {args.ko_cache}")
    else:
        log(f"[corpus] fetching {args.ko_window} REAL KO bytes from r2://{os.environ.get('R2_BUCKET','?')}/{R2_KO_KEY}")
        ko_raw = fetch_r2_range(R2_KO_KEY, args.ko_window + 8)
        open(args.ko_cache, "wb").write(ko_raw)
    if os.path.exists(args.en_cache) and os.path.getsize(args.en_cache) >= args.en_window:
        en_raw = open(args.en_cache, "rb").read()[: args.en_window + 8]
        log(f"[corpus] EN from cache {args.en_cache}")
    else:
        log(f"[corpus] fetching {args.en_window} REAL EN bytes from r2://{os.environ.get('R2_BUCKET','?')}/{R2_EN_KEY}")
        en_raw = fetch_r2_range(R2_EN_KEY, args.en_window + 8)
        open(args.en_cache, "wb").write(en_raw)

    ko_win = trim_utf8(ko_raw[: args.ko_window])
    en_win = trim_utf8(en_raw[: args.en_window])
    ko_sha = hashlib.sha256(ko_win).hexdigest()
    en_sha = hashlib.sha256(en_win).hexdigest()
    log(f"[corpus] KO {len(ko_win)}B sha={ko_sha[:16]}…  EN {len(en_win)}B sha={en_sha[:16]}…")
    # provenance gate: SAME corpus as H_1307 RUN A (the ceiling we compare against)
    same_ko = (ko_sha == H1307_KO_SHA)
    same_en = (en_sha == H1307_EN_SHA)
    log(f"[corpus] identical-to-H_1307-RUN-A: KO={same_ko} EN={same_en} (gate for a clean ceiling comparison)")

    ko_arr = np.frombuffer(ko_win, dtype=np.uint8).astype(np.int64)
    en_arr = np.frombuffer(en_win, dtype=np.uint8).astype(np.int64)

    ctxk_ladder = [int(x) for x in args.ctxk_ladder.split(",") if x.strip()]
    results = []

    # ── S0 baseline (must reproduce the H_1307 RUN A ~2.95 ceiling = port check) ──
    Xko0, Yko0 = make_pairs_s0(ko_arr)
    Xen0, Yen0 = make_pairs_s0(en_arr)
    Xktr0, Yktr0, Xkte0, Ykte0 = split_even_odd(Xko0, Yko0, args.ko_stride)
    Xen0s, Yen0s = Xen0[:: args.en_stride], Yen0[:: args.en_stride]
    log(f"[S0] KO train={Xktr0.shape[0]} test={Xkte0.shape[0]} EN test={Xen0s.shape[0]}")
    r0 = run_substrate("S0_ctx4_mle", Xktr0, Yktr0, Xkte0, Ykte0, Xen0s, Yen0s, dev, args.grow_max, "mle", RIDGE_LAMBDA)
    results.append(r0)
    s0_ko = r0["ko_ce"]

    # ── S1 LONGER CONTEXT (intact) + its SHUFFLE control, per ctxk ──
    for ck in ctxk_ladder:
        Xko, Yko = make_pairs_ctxk(ko_arr, ck)
        Xen, Yen = make_pairs_ctxk(en_arr, ck)
        Xktr, Yktr, Xkte, Ykte = split_even_odd(Xko, Yko, args.ko_stride)
        Xens, Yens = Xen[:: args.en_stride], Yen[:: args.en_stride]
        r = run_substrate(f"S1_ctx{ck}_mle", Xktr, Yktr, Xkte, Ykte, Xens, Yens, dev, args.grow_max, "mle", RIDGE_LAMBDA, base_dims=2)
        r["delta_vs_s0"] = round(r["ko_ce"] - s0_ko, 5)
        r["below_ceiling"] = bool(r["ko_ce"] < H1307_CEILING_KO_CE)
        results.append(r)
        # CONTROL: shuffle the ADDED history columns (cols 2..ck-1; keep last+second+cont)
        Xktr_sh = shuffle_extra_cols(Xktr, 2, seed=1311 + ck)
        Xkte_sh = shuffle_extra_cols(Xkte, 2, seed=2311 + ck)
        Xens_sh = shuffle_extra_cols(Xens, 2, seed=3311 + ck)
        rc = run_substrate(f"S1_ctx{ck}_mle_SHUFFLE", Xktr_sh, Yktr, Xkte_sh, Ykte, Xens_sh, Yens, dev, args.grow_max, "mle", RIDGE_LAMBDA, base_dims=2)
        rc["delta_vs_s0"] = round(rc["ko_ce"] - s0_ko, 5)
        rc["control_for"] = f"S1_ctx{ck}_mle"
        results.append(rc)

    # ── S2 LEARNED PER-CELL RIDGE HEAD on S0 features (intact) + SHUFFLE control ──
    r2 = run_substrate("S2_ctx4_ridge", Xktr0, Yktr0, Xkte0, Ykte0, Xen0s, Yen0s, dev, args.grow_max, "ridge", RIDGE_LAMBDA)
    r2["delta_vs_s0"] = round(r2["ko_ce"] - s0_ko, 5)
    r2["below_ceiling"] = bool(r2["ko_ce"] < H1307_CEILING_KO_CE)
    results.append(r2)
    # CONTROL for S2: shuffle the FEATURE ROWS fed to the ridge fit (destroy feat<->label coupling
    # while keeping the partition) — if ridge CE still beats S0 count-MLE, the gain is capacity/Voronoi
    # not the learned readout's use of the features.
    rngc = np.random.default_rng(4311)
    perm = rngc.permutation(Xktr0.shape[0])
    Xktr0_sh = Xktr0[perm]               # features permuted vs labels Yktr0 (label kept in place)
    r2c = run_substrate("S2_ctx4_ridge_SHUFFLE", Xktr0_sh, Yktr0, Xkte0, Ykte0, Xen0s, Yen0s, dev, args.grow_max, "ridge", RIDGE_LAMBDA)
    r2c["delta_vs_s0"] = round(r2c["ko_ce"] - s0_ko, 5)
    r2c["control_for"] = "S2_ctx4_ridge"
    results.append(r2c)

    # ── VERDICT logic ──
    total_wall = time.time() - t0
    intact = [r for r in results if "control_for" not in r and r["substrate"] != "S0_ctx4_mle"]
    # a substrate "really breaks the ceiling by representation" iff: below 2.9 ceiling AND beats S0
    # by a real margin AND beats its OWN shuffle control by a real margin.
    MARGIN = 0.02   # frozen, nats/byte — a real (not noise) drop
    by_name = {r["substrate"]: r for r in results}
    breakers = []
    for r in intact:
        sh = by_name.get(r["substrate"] + "_SHUFFLE")
        beats_s0 = (s0_ko - r["ko_ce"]) >= MARGIN
        below_ceil = r["ko_ce"] < H1307_CEILING_KO_CE
        beats_shuffle = (sh is not None) and ((sh["ko_ce"] - r["ko_ce"]) >= MARGIN)
        retain = r["en_ce"] <= r["en_seed_ce"] + 0.05
        r["beats_s0"] = bool(beats_s0)
        r["beats_shuffle"] = bool(beats_shuffle)
        r["retention_ok"] = bool(retain)
        r["representation_break"] = bool(below_ceil and beats_s0 and beats_shuffle and retain)
        if r["representation_break"]:
            breakers.append(r["substrate"])
    # any below-ceiling at all (even if capacity)?
    any_below = any(r.get("below_ceiling") for r in intact)
    # capacity-only signal: a shuffle control ALSO beats S0 (gain survives destroying the rep)
    capacity_signal = any(
        (by_name.get(r["substrate"] + "_SHUFFLE") is not None) and
        ((s0_ko - by_name[r["substrate"] + "_SHUFFLE"]["ko_ce"]) >= MARGIN)
        for r in intact
    )
    substrate_bound = len(breakers) > 0
    verdict = "SUBSTRATE-bound" if substrate_bound else "capacity-bound"

    summary = {
        "id": "H_1311",
        "device": torch.cuda.get_device_name(0), "sm": f"{cap[0]}{cap[1]}", "torch": torch.__version__,
        "ko_window_bytes": len(ko_win), "en_window_bytes": len(en_win),
        "ko_window_sha256": ko_sha, "en_window_sha256": en_sha,
        "corpus_identical_to_H1307_runA": bool(same_ko and same_en),
        "ko_stride": args.ko_stride, "en_stride": args.en_stride, "grow_max": args.grow_max,
        "ridge_lambda": RIDGE_LAMBDA, "ctxk_ladder": ctxk_ladder,
        "h1307_ceiling_ko_ce": H1307_CEILING_KO_CE,
        "s0_ko_ce": s0_ko,
        "ladder": results,
        "any_below_ceiling": bool(any_below),
        "representation_breakers": breakers,
        "capacity_signal_present": bool(capacity_signal),
        "ceiling_is": verdict,
        "margin_nats": MARGIN,
        "total_wall_s": round(total_wall, 2),
    }
    with open(os.path.join(args.out, "h1311_summary.json"), "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    with open(os.path.join(args.out, "h1311_metrics.jsonl"), "w") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    manifest = {
        "ko_source": f"r2://{os.environ.get('R2_BUCKET','phanes')}/{R2_KO_KEY} bytes[0:{args.ko_window}] trimmed[:{len(ko_win)}]",
        "en_source": f"r2://{os.environ.get('R2_BUCKET','phanes')}/{R2_EN_KEY} bytes[0:{args.en_window}] trimmed[:{len(en_win)}]",
        "ko_window_bytes": len(ko_win), "en_window_bytes": len(en_win),
        "ko_window_sha256": ko_sha, "en_window_sha256": en_sha,
        "identical_to_H1307_runA": bool(same_ko and same_en),
        "ko_stride": args.ko_stride, "en_stride": args.en_stride,
        "ctxk_ladder": ctxk_ladder, "ridge_lambda": RIDGE_LAMBDA, "V": V,
    }
    with open(os.path.join(args.out, "h1311_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    log("-------------------------------------------------------------------------------")
    log(f"S0 baseline (CTX=4, 3-D, count-MLE): KO CE={s0_ko}  (H_1307 RUN A was 2.9475 — port check)")
    log("substrate ladder (held-out KO next-byte CE, nats/byte):")
    for r in results:
        tag = ""
        if "control_for" in r:
            tag = f"  [SHUFFLE control for {r['control_for']}]"
        elif r["substrate"] != "S0_ctx4_mle":
            tag = f"  Δvs_s0={r.get('delta_vs_s0')} below2.9={r.get('below_ceiling')} repBreak={r.get('representation_break')}"
        log(f"  {r['substrate']:<26} dim={r['feat_dim']:<3} cells={r['cells']:<3} KO={r['ko_ce']:<8} EN={r['en_ce']:<8} {tag}")
    log("-------------------------------------------------------------------------------")
    log(f"(Q1) any richer substrate BELOW the 2.9 ceiling? {any_below}")
    log(f"     representation-breakers (below 2.9 AND beat S0≥{MARGIN} AND beat own shuffle≥{MARGIN} AND EN held): {breakers}")
    log(f"(C)  capacity-signal (a shuffle control ALSO beats S0 ≥{MARGIN})? {capacity_signal}")
    log(f"VERDICT: the ~2.9 ceiling is {verdict}.")
    if substrate_bound:
        log("  → richer representation breaks 2.9 (depth needs representation; matches capability-vs-scale thesis).")
    else:
        log("  → only cell-count / capacity matters (or nothing helps); the ~2.9 ceiling is the byte-task itself.")
    log(f"total wall={total_wall:.1f}s")
    log("  engine-transfer to live hexa DIRECTIONAL (re-confirm on CORE/*.hexa = follow-on). NO fluency claim.")
    log("[done]")


if __name__ == "__main__":
    main()
