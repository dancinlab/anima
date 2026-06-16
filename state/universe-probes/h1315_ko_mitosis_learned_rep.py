#!/usr/bin/env python3
# h1315_ko_mitosis_learned_rep.py — does gradient-free Korean mitosis over the 303M TRUNK's
# LEARNED HIDDEN REPRESENTATION break the ~2.9 nat/byte raw-byte ceiling that H_1311 (#2215) could
# not? (the surviving lever named by H_1311's REFUTATION.)
#
# THE THREAD (resolved by this rung):
#   H_1307 (#2213) scaled engine-native Korean mitosis (gradient-free, p8 — cells only SPLIT) to a
#     50x real-KO corpus → held-out KO next-byte CE floors at ~2.9 nat/byte (CTX=4 raw-byte substrate
#     SATURATES). The ceiling.
#   H_1311 (#2215, 🔴 HONEST-NEGATIVE) tested whether a RICHER RAW-BYTE substrate breaks 2.9 — longer
#     raw-byte context (ctx8/16/32) and a per-cell ridge head. EVERY richer rung was WORSE (curse-of-dim
#     on the L2/Voronoi partition over raw bytes; ridge collapses). VERDICT: the bottleneck is the
#     L2-Voronoi-partition-over-RAW-BYTES *geometry*, not the per-cell readout. The named surviving
#     lever: partition over a LEARNED representation instead of raw bytes.
#
# H_1315 THE QUESTION (frozen-first, likely DECISIVE — closes the axis either way):
#   Does the SAME gradient-free Korean mitosis (grow-op + cell budget held FIXED, verbatim H_1306/
#   H_1307/H_1311) — but partitioning over the MOUNTED 303M TRUNK's hidden representation at each byte
#   position (ckpt h1129c_chat.pt, forward = GRADIENT-FREE, just READ the hidden, NO backprop) — push
#   held-out KO CE BELOW 2.9, while raw-byte mitosis (G0) can't?
#   Honest hypothesis: the 303M trunk PROVIDES the learned representation raw-byte mitosis can't build
#   → mitosis = grow-under-pressure ON TOP OF a learned rep (structure-over-learned-rep).
#
# ARMS (same REAL KO/EN R2 corpus window as H_1307/H_1311, sha-asserted byte-identical; same grow-op
#   + cell budget GROW_MAX; ONLY the partition INPUT varies; 3 seeds; held-out DETERMINISTIC next-byte CE):
#   G0  raw-byte ctx4 (the 2.9 ceiling ref — the H_1307/H_1311 S0 substrate, count-MLE head).
#   G1  partition over the 303M TRUNK HIDDEN REP (ln_f(x) at position i-1, the learned embedding that
#       predicts byte i), projected to PROJ_DIM by a FIXED seeded random projection (gradient-free).
#       SAME grow-op, SAME cell budget, count-MLE head.
#   CONTROL random-embed = the SAME PROJ_DIM, but the hidden states come from a RANDOMLY-INITIALISED
#       (untrained) trunk of the IDENTICAL architecture (same seed for the projection). Isolates
#       "LEARNED rep" from "just a higher-D non-byte space of the same width" — if G1 only ties this,
#       the lift is capacity/dim, NOT the learned representation.
#   CONTROL shuffle = G1's trunk hidden states with the hidden->byte ALIGNMENT shuffled (each position's
#       feature row permuted away from its label byte) -> leakage / partition-handle check. A real
#       learned-rep gain must DIE under shuffle.
#
# FROZEN bars (pre-registered .verdicts/1315_ko_mitosis_learned_rep/FREEZE.txt BEFORE scoring; c9/p7;
#   held-out DETERMINISTIC next-byte CROSS-ENTROPY; NO perplexity-as-truth; NO tune-to-green):
#   (B1 BREAK-2.9)  does G1 push held-out KO CE BELOW the H_1307 ceiling 2.9475? report the drop.
#   (B2 LEARNED)    does G1 beat BOTH controls by >= MARGIN (random-embed AND shuffle)? -> lift is the
#                   LEARNED rep, not capacity/dim/leakage.
#   (B3 RETENTION)  EN CE under G1 <= EN CE[G1 2-cell seed] + 0.05 (no catastrophic forgetting).
#   DECISIVE: G1 breaks 2.9 AND beats both controls -> the ceiling is REPRESENTATION-bound, the 303M
#     trunk supplies the representation raw-byte mitosis can't build (mitosis = structure-over-learned-
#     rep). G1 fails / ties controls -> raw-mitosis genuinely ceilings even with the trunk rep at this
#     scale (terminal axis-closure: the Korean depth needs gradient learning, not gradient-free grow-on-
#     top, at this scale).
#
# FROZEN knobs (verbatim H_1306/H_1307/H_1311, NOT moved): V=256, GROW_MAX, SPLIT_THRESH_CE, MIN_OWNED,
#   LAPLACE; even/odd train/test split; H_1307 RUN A stride/window. NEW frozen-before-run knobs:
#   PROJ_DIM (random-projection target width), PROJ_SEED, TRUNK_CTX (bytes of left-context fed to the
#   trunk forward for each hidden read), HIDDEN_LAYER = ln_f output (the trunk's final representation).
#
# REAL Korean only (NO synthetic, p1-p8): the SAME anima-7b R2 web corpus windows as H_1307/H_1311
#   (r2://phanes/anima-7b/web/{kor,eng}/shard0000.bytes), boto3 range GET; the KO/EN window sha256 is
#   asserted == the H_1307 RUN A manifest hashes so the corpus is provably identical. Secrets (R2 keys)
#   read from ENV ONLY at fetch time, never echoed/logged/committed (c7).
#
# SCALE-HONEST (a_scale_honest_scope, a_toy_scale_recheck): toy/DIRECTIONAL — summer GPU; the mitosis
#   grow-op is a numpy/torch mirror (engine-transfer to live hexa = follow-on); NO fluency claim.

import argparse
import hashlib
import json
import os
import sys
import time

import numpy as np

try:
    import torch
    import torch.nn as nn
except Exception as e:  # pragma: no cover
    print("FATAL: torch import failed:", e)
    sys.exit(2)

# -- FROZEN knobs (verbatim H_1306 / H_1307 / H_1311) ---------------------------
V = 256
GROW_MAX = 40
SPLIT_THRESH_CE = 0.05
MIN_OWNED = 8
LAPLACE = 1.0
# H_1307 RUN A (stride-300, 30MB) ceiling this rung must break:
H1307_CEILING_KO_CE = 2.9475
H1307_KO_SHA = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
H1307_EN_SHA = "31b4a5430441cfdbb496b59f392150e4aa748cde2ed1b7cedad10960f0bcaf73"

R2_KO_KEY = "anima-7b/web/kor/shard0000.bytes"
R2_EN_KEY = "anima-7b/web/eng/shard0000.bytes"

# -- NEW frozen-before-run knobs (H_1315) ---------------------------------------
PROJ_DIM = 16            # random-projection target width for the trunk hidden (matched G1 vs control)
PROJ_SEED = 1313         # fixed projection seed (SAME for G1 + random-embed control)
TRUNK_CTX = 64           # bytes of left-context fed to the trunk forward to read each hidden state
MARGIN = 0.02            # nats/byte -- a real (not noise) drop; FROZEN
CKPT = "/tmp/h1156_mount/h1129c_chat.pt"


def log(*a):
    print(*a, flush=True)


# -- the EXACT H_1129 / H_1156 ByteGPT block (gradient-free forward; we read ln_f(x)) ---------------
class Block(nn.Module):
    def __init__(s, d, h, p=0.0):
        super().__init__()
        s.ln1 = nn.LayerNorm(d)
        s.attn = nn.MultiheadAttention(d, h, dropout=p, batch_first=True)
        s.ln2 = nn.LayerNorm(d)
        s.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d), nn.Dropout(p))

    def forward(s, x, m):
        h = s.ln1(x)
        a, _ = s.attn(h, h, h, attn_mask=m, need_weights=False)
        x = x + a
        return x + s.mlp(s.ln2(x))


class ByteGPT(nn.Module):
    def __init__(s, vocab=256, d=1024, n_layer=24, n_head=16, block=512, p=0.0):
        super().__init__()
        s.block = block; s.n_head = n_head; s.d = d; s.n_layer = n_layer; s.vocab = vocab
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d); s.drop = nn.Dropout(p)
        s.blocks = nn.ModuleList([Block(d, n_head, p) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight

    def hidden(s, idx):
        """Return ln_f(x) -- the trunk's FINAL learned hidden representation at every position."""
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        for b in s.blocks:
            x = b(x, mask)
        return s.ln_f(x)  # [B, T, d]


def load_trunk(dev, randomized=False, rand_seed=0):
    ck = torch.load(CKPT, map_location="cpu", weights_only=False)
    cfg = ck["config"]
    m = ByteGPT(**cfg)
    if randomized:
        torch.manual_seed(rand_seed)  # untrained trunk: fresh random init of the IDENTICAL arch
    else:
        m.load_state_dict(ck["model"])
    m.eval()
    m.to(dev)
    for p in m.parameters():
        p.requires_grad_(False)
    return m, cfg


# -- trunk hidden-state extraction for each byte position (gradient-free, batched windows) ----------
@torch.no_grad()
def trunk_hidden_at_positions(model, byte_arr, positions, trunk_ctx, dev, proj, batch=2048):
    """For each target position i in `positions`, build the TRUNK_CTX left-context window ending at i-1,
    forward it, and read ln_f at the LAST window position = the learned rep that predicts byte i.
    Then project to PROJ_DIM via the fixed random projection `proj` [d, PROJ_DIM]. Gradient-free."""
    out = np.zeros((len(positions), proj.shape[1]), dtype=np.float64)
    bt = torch.from_numpy(byte_arr.astype(np.int64))
    for s0 in range(0, len(positions), batch):
        chunk = positions[s0:s0 + batch]
        rows = []
        for i in chunk:
            lo = max(0, i - trunk_ctx)
            ctx = bt[lo:i]                              # bytes [lo, i) -- predicts byte i
            if ctx.shape[0] < trunk_ctx:               # left-pad with 0 to TRUNK_CTX
                pad = torch.zeros(trunk_ctx - ctx.shape[0], dtype=torch.int64)
                ctx = torch.cat([pad, ctx])
            rows.append(ctx)
        idx = torch.stack(rows, 0).to(dev)             # [b, TRUNK_CTX]
        h = model.hidden(idx)[:, -1, :]                # [b, d] last-pos hidden
        hp = (h.double() @ proj)                       # [b, PROJ_DIM]
        out[s0:s0 + len(chunk)] = hp.cpu().numpy()
    return out


# -- engine-native mitosis (BYTE-FAITHFUL to the H_1306/H_1307/H_1311 _grow_on; dimension-agnostic) --
def assign_all(centers_t, X_t):
    d2 = torch.cdist(X_t, centers_t, p=2)
    return torch.argmin(d2, dim=1)


def all_heads(Y_t, owner, K, ntr, dev):
    Hmat = torch.full((K, V), LAPLACE, dtype=torch.float64, device=dev)
    own = owner[:ntr]; y = Y_t[:ntr]
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


def grow_on(centers, X_tr, Y_tr, ntr, dev, grow_max):
    """Faithful port of the H_1306/H_1307/H_1311 hexa _grow_on (gradient-free, cells only SPLIT -- p8).
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
        pick = elig[0]; bestce = local_ce[elig[0]]
        for k in elig[1:]:
            if local_ce[k] > bestce:
                bestce = local_ce[k]; pick = k
        if len(centers) + 1 > grow_max:
            break
        pmask = (owntr == pick)
        pts = X_tr[:ntr][pmask]
        if pts.shape[0] == 0:
            break
        var = pts.var(dim=0, unbiased=False)
        ax = int(torch.argmax(var).item())
        col = pts[:, ax]; m = col.shape[0]
        scol, _ = torch.sort(col)
        med = scol[m // 2].item() if m % 2 == 1 else ((scol[m // 2 - 1] + scol[m // 2]) / 2.0).item()
        lo_mask = col <= med; hi_mask = col > med
        if int(lo_mask.sum().item()) == 0 or int(hi_mask.sum().item()) == 0:
            break
        c_lo = pts[lo_mask].mean(dim=0).cpu().numpy().tolist()
        c_hi = pts[hi_mask].mean(dim=0).cpu().numpy().tolist()
        centers = [centers[i] for i in range(len(centers)) if i != pick] + [c_lo, c_hi]
    return centers


def utf8_cont_depth(arr_u8):
    is_cont = (arr_u8 >= 0x80) & (arr_u8 <= 0xBF)
    depth = np.zeros(len(arr_u8), dtype=np.float64)
    d = 0
    for i in range(len(arr_u8)):
        d = d + 1 if is_cont[i] else 0
        depth[i] = d
    return depth


def make_pairs_s0(byte_arr):
    """G0 raw-byte ctx4 substrate (verbatim H_1307/H_1311 S0): FEAT=[last/255, second/255, cont/3]."""
    n = len(byte_arr)
    cont = utf8_cont_depth(byte_arr)
    idx = np.arange(4, n - 1)
    last = byte_arr[idx - 1].astype(np.float64) / 255.0
    second = byte_arr[idx - 2].astype(np.float64) / 255.0
    cdep = cont[idx - 1] / 3.0
    X = np.stack([last, second, cdep], axis=1)
    Y = byte_arr[idx].astype(np.int64)
    return X, Y, idx


def seed_centers_for_dim(d, lo=0.3, hi=0.7):
    a = [0.5] * d; b = [0.5] * d
    a[0], b[0] = lo, hi
    a[-1], b[-1] = 0.0, 0.5
    return [a, b]


def seed_centers_from_data(X):
    """For the learned-rep space (arbitrary scale), seed two cells at the data's per-axis 25/75
    quantiles so the first split is meaningful. Deterministic. (frozen choice before run)"""
    lo = np.quantile(X, 0.25, axis=0)
    hi = np.quantile(X, 0.75, axis=0)
    return [lo.tolist(), hi.tolist()]


def split_even_odd_idx(npts, stride):
    keep = np.arange(0, npts, stride)
    pos = np.arange(keep.shape[0])
    tr = keep[pos % 2 == 0]; te = keep[pos % 2 == 1]
    return tr, te


def run_arm(name, Xtr, Ytr, Xte, Yte, Xen, Yen, dev, grow_max, seed_centers, results):
    d = Xtr.shape[1]
    Xtr_t = torch.tensor(Xtr, dtype=torch.float64, device=dev)
    Ytr_t = torch.tensor(Ytr, dtype=torch.int64, device=dev)
    Xte_t = torch.tensor(Xte, dtype=torch.float64, device=dev)
    Yte_t = torch.tensor(Yte, dtype=torch.int64, device=dev)
    Xen_t = torch.tensor(Xen, dtype=torch.float64, device=dev)
    Yen_t = torch.tensor(Yen, dtype=torch.int64, device=dev)
    n = Xtr.shape[0]
    seed_t = torch.tensor(seed_centers, dtype=torch.float64, device=dev)
    nb1 = max(2, n // 3)
    en_seed = score_ce(seed_t, Xtr_t, Ytr_t, nb1, Xen_t, Yen_t, dev)
    t0 = time.time()
    c = grow_on(seed_centers, Xtr_t, Ytr_t, n, dev, grow_max)
    grow_wall = time.time() - t0
    ct = torch.tensor(c, dtype=torch.float64, device=dev)
    ko_ce = score_ce(ct, Xtr_t, Ytr_t, n, Xte_t, Yte_t, dev)
    en_ce = score_ce(ct, Xtr_t, Ytr_t, n, Xen_t, Yen_t, dev)
    torch.cuda.synchronize()
    npairs = Xtr.shape[0] + Xte.shape[0] + Xen.shape[0]
    rec = {
        "arm": name, "feat_dim": d, "cells": len(c),
        "ko_ce": round(ko_ce, 5), "en_ce": round(en_ce, 5), "en_seed_ce": round(en_seed, 5),
        "grow_wall_s": round(grow_wall, 2),
        "throughput_pairs_per_s": round(npairs / max(grow_wall, 1e-9), 1),
    }
    log("  [arm] " + json.dumps(rec))
    return rec


def main():
    _t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--ko-window", type=int, default=30_000_000)
    ap.add_argument("--en-window", type=int, default=10_000_000)
    ap.add_argument("--ko-stride", type=int, default=300)
    ap.add_argument("--en-stride", type=int, default=600)
    ap.add_argument("--rep-pairs", type=int, default=24000)   # total KO pairs (train+test) for G1/controls
    ap.add_argument("--en-rep-pairs", type=int, default=8000)
    ap.add_argument("--proj-dim", type=int, default=PROJ_DIM)
    ap.add_argument("--trunk-ctx", type=int, default=TRUNK_CTX)
    ap.add_argument("--grow-max", type=int, default=GROW_MAX)
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--out", default="/tmp/h1315_out")
    ap.add_argument("--ko-cache", default="/tmp/h1311_ko_raw.bytes")  # reuse H_1311 cache (same corpus)
    ap.add_argument("--en-cache", default="/tmp/h1311_en_raw.bytes")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    assert torch.cuda.is_available(), "CUDA not available -- REFUSING CPU (a_train_flame_forge)"
    dev = torch.device("cuda")
    cap = torch.cuda.get_device_capability(0)
    log(f"=== H_1315 -- mitosis over 303M LEARNED REP vs the H_1311 raw-byte 2.9 ceiling (RTX 5070 sm_{cap[0]}{cap[1]}) ===")
    log(f"device={torch.cuda.get_device_name(0)} cap={cap} torch={torch.__version__}")
    _s = (torch.randn(1024, 1024, device=dev) @ torch.randn(1024, 1024, device=dev)).sum().item()
    torch.cuda.synchronize()
    log(f"sm_{cap[0]}{cap[1]} kernel launch OK (sentinel {_s:.1f})")

    def fetch_r2_range(key, nbytes):
        import boto3
        from botocore.config import Config
        acct = os.environ["R2_ACCOUNT_ID"]; bucket = os.environ["R2_BUCKET"]
        s3 = boto3.client("s3", endpoint_url=f"https://{acct}.r2.cloudflarestorage.com",
                          aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
                          aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
                          config=Config(signature_version="s3v4", retries={"max_attempts": 5}))
        obj = s3.get_object(Bucket=bucket, Key=key, Range=f"bytes=0-{nbytes - 1}")
        return obj["Body"].read()

    def trim_utf8(b):
        for cut in range(0, 4):
            try:
                b[: len(b) - cut].decode("utf-8"); return b[: len(b) - cut]
            except Exception:
                continue
        return b

    if os.path.exists(args.ko_cache) and os.path.getsize(args.ko_cache) >= args.ko_window:
        ko_raw = open(args.ko_cache, "rb").read()[: args.ko_window + 8]
        log(f"[corpus] KO from cache {args.ko_cache}")
    else:
        log(f"[corpus] fetching {args.ko_window} REAL KO bytes from r2")
        ko_raw = fetch_r2_range(R2_KO_KEY, args.ko_window + 8); open(args.ko_cache, "wb").write(ko_raw)
    if os.path.exists(args.en_cache) and os.path.getsize(args.en_cache) >= args.en_window:
        en_raw = open(args.en_cache, "rb").read()[: args.en_window + 8]
        log(f"[corpus] EN from cache {args.en_cache}")
    else:
        log(f"[corpus] fetching {args.en_window} REAL EN bytes from r2")
        en_raw = fetch_r2_range(R2_EN_KEY, args.en_window + 8); open(args.en_cache, "wb").write(en_raw)

    ko_win = trim_utf8(ko_raw[: args.ko_window]); en_win = trim_utf8(en_raw[: args.en_window])
    ko_sha = hashlib.sha256(ko_win).hexdigest(); en_sha = hashlib.sha256(en_win).hexdigest()
    same_ko = (ko_sha == H1307_KO_SHA); same_en = (en_sha == H1307_EN_SHA)
    log(f"[corpus] KO {len(ko_win)}B sha={ko_sha[:16]}...  EN {len(en_win)}B sha={en_sha[:16]}...")
    log(f"[corpus] identical-to-H_1307-RUN-A: KO={same_ko} EN={same_en}")

    ko_arr = np.frombuffer(ko_win, dtype=np.uint8).astype(np.int64)
    en_arr = np.frombuffer(en_win, dtype=np.uint8).astype(np.int64)

    results = []

    # -- G0 raw-byte ctx4 (full H_1307/H_1311 S0; the 2.9 ref) --
    Xko0, Yko0, _ = make_pairs_s0(ko_arr)
    Xen0, Yen0, _ = make_pairs_s0(en_arr)
    ktr0, kte0 = split_even_odd_idx(Xko0.shape[0], args.ko_stride)
    en0 = np.arange(0, Xen0.shape[0], args.en_stride)
    Xktr0, Yktr0 = Xko0[ktr0], Yko0[ktr0]
    Xkte0, Ykte0 = Xko0[kte0], Yko0[kte0]
    Xen0s, Yen0s = Xen0[en0], Yen0[en0]
    log(f"[G0] KO train={Xktr0.shape[0]} test={Xkte0.shape[0]} EN test={Xen0s.shape[0]}")
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    g0_recs = []
    for sd in seeds:
        r = run_arm(f"G0_rawbyte_ctx4_seed{sd}", Xktr0, Yktr0, Xkte0, Ykte0, Xen0s, Yen0s, dev,
                    args.grow_max, seed_centers_for_dim(3), results)
        r["seed"] = sd; r["group"] = "G0"; results.append(r); g0_recs.append(r)
    g0_ko = float(np.mean([r["ko_ce"] for r in g0_recs]))
    log(f"[G0] mean KO CE over seeds = {g0_ko:.5f}  (H_1307 RUN A ceiling 2.9475 -- port check)")

    # -- learned-rep pair index (subsample positions to ~rep_pairs) --
    n_ko = ko_arr.shape[0]
    ko_targets_all = np.arange(args.trunk_ctx, n_ko - 1)
    ko_sub_stride = max(1, ko_targets_all.shape[0] // args.rep_pairs)
    ko_targets = ko_targets_all[::ko_sub_stride][: args.rep_pairs]
    n_en = en_arr.shape[0]
    en_targets_all = np.arange(args.trunk_ctx, n_en - 1)
    en_sub_stride = max(1, en_targets_all.shape[0] // args.en_rep_pairs)
    en_targets = en_targets_all[::en_sub_stride][: args.en_rep_pairs]
    Yko_rep = ko_arr[ko_targets].astype(np.int64)
    Yen_rep = en_arr[en_targets].astype(np.int64)
    ko_pos = np.arange(ko_targets.shape[0])
    ko_tr_m, ko_te_m = (ko_pos % 2 == 0), (ko_pos % 2 == 1)
    log(f"[REP] KO rep pairs={ko_targets.shape[0]} (train={int(ko_tr_m.sum())} test={int(ko_te_m.sum())}) "
        f"EN rep pairs={en_targets.shape[0]} trunk_ctx={args.trunk_ctx} proj_dim={args.proj_dim}")

    rng_proj = np.random.default_rng(PROJ_SEED)
    d_model = 1024
    proj_np = rng_proj.standard_normal((d_model, args.proj_dim)) / np.sqrt(d_model)
    proj = torch.tensor(proj_np, dtype=torch.float64, device=dev)

    def extract(model, byte_arr, targets):
        return trunk_hidden_at_positions(model, byte_arr, targets, args.trunk_ctx, dev, proj)

    # -- G1: TRAINED trunk hidden rep --
    log("[G1] loading TRAINED 303M trunk + extracting hidden rep (gradient-free forward)...")
    t_ex = time.time()
    trunk, cfg = load_trunk(dev, randomized=False)
    Hko = extract(trunk, ko_arr, ko_targets)
    Hen = extract(trunk, en_arr, en_targets)
    log(f"[G1] trunk hidden extracted in {time.time()-t_ex:.1f}s  cfg={cfg}")
    del trunk; torch.cuda.empty_cache()

    # -- CONTROL random-embed: UNTRAINED trunk hidden rep (same arch, same projection) --
    log("[CTRL-rand] loading RANDOM-INIT trunk + extracting hidden rep...")
    rtrunk, _ = load_trunk(dev, randomized=True, rand_seed=PROJ_SEED)
    Rko = extract(rtrunk, ko_arr, ko_targets)
    Ren = extract(rtrunk, en_arr, en_targets)
    del rtrunk; torch.cuda.empty_cache()

    def run_rep_group(group, Hko_m, Hen_m, Yko_m, Yen_m, shuffle_align=False):
        recs = []
        for sd in seeds:
            rng = np.random.default_rng(1000 + sd)
            Hk = Hko_m.copy(); Yk = Yko_m.copy()
            if shuffle_align:
                perm = rng.permutation(Hk.shape[0])
                Hk = Hk[perm]   # labels Yk stay -> each rep now predicts a RANDOM byte (leakage check)
            Xtr, Ytr = Hk[ko_tr_m], Yk[ko_tr_m]
            Xte, Yte = Hk[ko_te_m], Yk[ko_te_m]
            sc = seed_centers_from_data(Xtr)
            r = run_arm(f"{group}_seed{sd}", Xtr, Ytr, Xte, Yte, Hen_m, Yen_m, dev, args.grow_max, sc, results)
            r["seed"] = sd; r["group"] = group; results.append(r); recs.append(r)
        return recs

    log("[G1] growing mitosis over TRAINED trunk rep...")
    g1_recs = run_rep_group("G1_trunk_rep", Hko, Hen, Yko_rep, Yen_rep, shuffle_align=False)
    log("[CTRL-rand] growing mitosis over UNTRAINED trunk rep...")
    cr_recs = run_rep_group("CTRL_random_embed", Rko, Ren, Yko_rep, Yen_rep, shuffle_align=False)
    log("[CTRL-shuf] growing mitosis over TRAINED rep with SHUFFLED hidden->byte alignment...")
    cs_recs = run_rep_group("CTRL_shuffle_align", Hko, Hen, Yko_rep, Yen_rep, shuffle_align=True)

    def mean_ko(recs): return float(np.mean([r["ko_ce"] for r in recs]))
    def mean_en(recs): return float(np.mean([r["en_ce"] for r in recs]))
    def mean_en_seed(recs): return float(np.mean([r["en_seed_ce"] for r in recs]))
    g1_ko = mean_ko(g1_recs); cr_ko = mean_ko(cr_recs); cs_ko = mean_ko(cs_recs)
    g1_en = mean_en(g1_recs); g1_en_seed = mean_en_seed(g1_recs)

    # -- FROZEN VERDICT logic --
    b1_break = bool(g1_ko < H1307_CEILING_KO_CE)
    beats_rand = (cr_ko - g1_ko) >= MARGIN
    beats_shuf = (cs_ko - g1_ko) >= MARGIN
    b2_learned = bool(beats_rand and beats_shuf)
    b3_retain = bool(g1_en <= g1_en_seed + 0.05)
    decisive_rep_bound = bool(b1_break and b2_learned)
    if decisive_rep_bound:
        verdict = "REPRESENTATION-bound (the 303M trunk rep breaks 2.9 -> mitosis=structure-over-learned-rep)"
    elif b1_break and not b2_learned:
        verdict = "AMBIGUOUS-capacity (G1 below 2.9 but ties a control -> lift is dim/capacity, not learned rep)"
    else:
        verdict = "TERMINAL (even the 303M trunk rep does NOT break 2.9 with gradient-free mitosis at this scale)"

    total_wall = time.time() - _t0
    summary = {
        "id": "H_1315",
        "device": torch.cuda.get_device_name(0), "sm": f"{cap[0]}{cap[1]}", "torch": torch.__version__,
        "ckpt": CKPT, "trunk_config": cfg,
        "ko_window_bytes": len(ko_win), "en_window_bytes": len(en_win),
        "ko_window_sha256": ko_sha, "en_window_sha256": en_sha,
        "corpus_identical_to_H1307_runA": bool(same_ko and same_en),
        "ko_stride": args.ko_stride, "en_stride": args.en_stride,
        "rep_pairs": int(ko_targets.shape[0]), "en_rep_pairs": int(en_targets.shape[0]),
        "proj_dim": args.proj_dim, "proj_seed": PROJ_SEED, "trunk_ctx": args.trunk_ctx,
        "grow_max": args.grow_max, "seeds": seeds, "margin_nats": MARGIN,
        "h1307_ceiling_ko_ce": H1307_CEILING_KO_CE,
        "mean_ko_ce": {"G0_rawbyte": round(g0_ko, 5), "G1_trunk_rep": round(g1_ko, 5),
                       "CTRL_random_embed": round(cr_ko, 5), "CTRL_shuffle_align": round(cs_ko, 5)},
        "g1_minus_g0": round(g1_ko - g0_ko, 5),
        "g1_below_2.9_ceiling": b1_break,
        "g1_beats_random_embed_by": round(cr_ko - g1_ko, 5), "beats_random_embed": bool(beats_rand),
        "g1_beats_shuffle_by": round(cs_ko - g1_ko, 5), "beats_shuffle": bool(beats_shuf),
        "b1_break_2.9": b1_break, "b2_learned_rep": b2_learned, "b3_en_retention": b3_retain,
        "en_g1_mean": round(g1_en, 5), "en_g1_seed_mean": round(g1_en_seed, 5),
        "verdict": verdict, "decisive_representation_bound": decisive_rep_bound,
        "ladder": results,
        "total_wall_s": round(total_wall, 2),
    }
    with open(os.path.join(args.out, "h1315_summary.json"), "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    with open(os.path.join(args.out, "h1315_metrics.jsonl"), "w") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    manifest = {
        "ko_source": f"r2://{os.environ.get('R2_BUCKET','phanes')}/{R2_KO_KEY} bytes[0:{args.ko_window}] trimmed[:{len(ko_win)}]",
        "en_source": f"r2://{os.environ.get('R2_BUCKET','phanes')}/{R2_EN_KEY} bytes[0:{args.en_window}] trimmed[:{len(en_win)}]",
        "ko_window_bytes": len(ko_win), "en_window_bytes": len(en_win),
        "ko_window_sha256": ko_sha, "en_window_sha256": en_sha,
        "identical_to_H1307_runA": bool(same_ko and same_en),
        "ckpt": CKPT, "ckpt_sha256_note": "see h1315_ckpt_sha.txt (computed on summer)",
        "trunk_config": cfg, "proj_dim": args.proj_dim, "proj_seed": PROJ_SEED,
        "trunk_ctx": args.trunk_ctx, "rep_pairs": int(ko_targets.shape[0]),
        "en_rep_pairs": int(en_targets.shape[0]), "V": V, "grow_max": args.grow_max,
    }
    with open(os.path.join(args.out, "h1315_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    log("-------------------------------------------------------------------------------")
    log("mean held-out KO next-byte CE (nats/byte), 3 seeds:")
    log(f"  G0 raw-byte ctx4       = {g0_ko:.5f}   (the 2.9475 ceiling ref)")
    log(f"  G1 303M trunk rep      = {g1_ko:.5f}   dvs_G0={g1_ko-g0_ko:+.5f}  below2.9={b1_break}")
    log(f"  CTRL random-embed      = {cr_ko:.5f}   (G1 beats by {cr_ko-g1_ko:+.5f}, >={MARGIN}? {beats_rand})")
    log(f"  CTRL shuffle-align     = {cs_ko:.5f}   (G1 beats by {cs_ko-g1_ko:+.5f}, >={MARGIN}? {beats_shuf})")
    log(f"EN retention: G1 EN={g1_en:.5f} vs seed {g1_en_seed:.5f}  ok={b3_retain}")
    log("-------------------------------------------------------------------------------")
    log(f"(B1) G1 below 2.9?  {b1_break}")
    log(f"(B2) G1 lift = LEARNED rep (beats BOTH controls >={MARGIN})?  {b2_learned}")
    log(f"(B3) EN retained?  {b3_retain}")
    log(f"VERDICT: {verdict}")
    log("  engine-transfer to live hexa DIRECTIONAL (re-confirm on CORE/*.hexa = follow-on). NO fluency claim.")
    log("[done]")


if __name__ == "__main__":
    main()
