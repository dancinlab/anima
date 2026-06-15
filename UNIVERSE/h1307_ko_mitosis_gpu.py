#!/usr/bin/env python3
# h1307_ko_mitosis_gpu.py — GPU SCALE-UP of the H_1306 engine-native Korean mitosis rung.
#
# H_1306 (#2211, 🟢 GREEN) proved the MECHANISM engine-native on a 600 KB KO / 300 KB EN
# real-web window, stride-subsampled to ~2.7 K KO pairs (the hexa interpreter is list-based
# O(N)/growth-step, so CPU-bound). H_1307 asks the SCALE question the brief poses:
#   "Does MORE real Korean data push KO next-byte CE BELOW the 600 KB baseline 3.249?"
# It runs the SAME error-targeted Voronoi mitosis grow (gradient-free, p8 — cells only SPLIT,
# never merge) on a MUCH larger real-Korean pair set, GPU-accelerated on summer's RTX 5070
# (Blackwell sm_120). The GPU does NOT change the mechanism — it vectorizes the per-step
# nearest-cell ASSIGNMENT + per-cell next-byte MLE HEAD + held-out CE so a ~50-100x larger
# pair set is tractable in a few-hours run. The mitosis SPLIT logic is byte-faithful to
# CORE/h1306_ko_mitosis_engine_probe.hexa (a_engine_native_learning — engine-transfer is
# DIRECTIONAL until re-confirmed on the live hexa engine; see scope).
#
# REAL Korean only (NO synthetic, p1-p8, a_eeg_consciousness_record spirit): a larger slice
# of the SAME anima-7b 5-lang web corpus on Cloudflare R2 (bucket phanes, prefix
# anima-7b/web/{kor,eng}/shard0000.bytes), pulled via boto3 HTTP RANGE GET. Provenance +
# byte size + sha256 written to the manifest. Secrets (R2 keys) are read from ENV ONLY at
# fetch time, header/env-scoped, NEVER echoed/logged/inlined/committed (c7).
#
# FROZEN-FIRST bars (pre-registered .verdicts/1307_ko_mitosis_gpu/FREEZE.txt BEFORE the run,
# NOT moved — c9/p7; held-out deterministic next-byte CROSS-ENTROPY, NO perplexity-as-truth):
#   (L1 INTERNAL LEARNING)  KO CE[pt3 full] <= KO CE[pt1] - 0.05 nats  (the H_1306 learning bar,
#                            re-checked at scale — does growing on more KO drop held-out KO CE?)
#   (L2 SCALE-VS-600KB)     KO CE[full] <= 3.24897 (the H_1306 600 KB baseline)  [the SCALE claim
#                            the brief asks: more data pushes CE at-or-below the small-window CE]
#   (R RETENTION)           EN CE[after full KO grow] <= EN CE[seed 2-cell] + 0.05 nats
#                            (no catastrophic forgetting — the H_1300/H_1306 property at scale)
#   (G GROWTH)              final cells > 2  (mitosis actually grew cells for Korean)
#   GREEN iff L1 & R & G.  L2 is the SCALE headline (reported PASS/FAIL, gating the scale claim).
# FROZEN knobs (verbatim from H_1306/H_1297): V=256, FEAT_DIM=3, CTX=4, GROW_MAX, SPLIT_THRESH_CE,
#   MIN_OWNED, LAPLACE; seed 2-cell centers [[0.3,0.5,0.0],[0.7,0.5,0.5]]; even/odd train/test split.
#
# SCALE-HONEST (a_scale_honest_scope, a_toy_scale_recheck): this is a BIGGER real-text rung, NOT
# a fluent Korean LM. CTX=4 3-D byte features + a Voronoi-partitioned per-cell unigram-over-context
# head is a deliberately SIMPLE substrate — it tests whether MORE Korean error-pressure grows a
# finer partition that lowers held-out KO CE, with EN retained. Fluent Korean (deep context, decode
# path) is a larger follow-on. NO fluency overclaim.

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

# ── FROZEN knobs (verbatim from H_1306 / H_1297) ───────────────────────────────
CTX = 4
V = 256
FEAT_DIM = 3
GROW_MAX = 40
SPLIT_THRESH_CE = 0.05
MIN_OWNED = 8
LAPLACE = 1.0
SEED_CENTERS = [[0.3, 0.5, 0.0], [0.7, 0.5, 0.5]]
H1306_BASELINE_KO_CE = 3.24897   # the 600 KB CPU baseline this scale rung must beat-or-match

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
    data = obj["Body"].read()
    return data


def trim_utf8(b):
    for cut in range(0, 4):
        try:
            b[: len(b) - cut].decode("utf-8")
            return b[: len(b) - cut]
        except Exception:
            continue
    return b


# ── feature builder (identical phi to H_1306: CTX=4, 3-D) — vectorized ──────────
def utf8_cont_depth(arr_u8):
    # depth resets to 0 on a non-continuation byte, else +1 (continuation = 0x80..0xBF)
    is_cont = (arr_u8 >= 0x80) & (arr_u8 <= 0xBF)
    depth = np.zeros(len(arr_u8), dtype=np.float64)
    d = 0
    for i in range(len(arr_u8)):
        d = d + 1 if is_cont[i] else 0
        depth[i] = d
    return depth


def make_pairs(byte_arr):
    """(phi(context), next_byte) pairs over a uint8 array. Identical to H_1306 make_pairs_from:
    for i in [CTX, len-1): feat=[bs[i-1]/255, bs[i-2]/255, cont[i-1]/3], y=bs[i]."""
    n = len(byte_arr)
    cont = utf8_cont_depth(byte_arr)
    idx = np.arange(CTX, n - 1)
    last = byte_arr[idx - 1].astype(np.float64) / 255.0
    second = byte_arr[idx - 2].astype(np.float64) / 255.0
    cdep = cont[idx - 1] / 3.0
    X = np.stack([last, second, cdep], axis=1)
    Y = byte_arr[idx].astype(np.int64)
    return X, Y


# ── engine-native mitosis (BYTE-FAITHFUL to the hexa _grow_on, GPU-vectorized scoring) ──
def assign_all(centers_t, X_t):
    # nearest center by L2 (ties -> lowest index, matching vadapt_field_nearest_idx which
    # iterates and keeps strict `<` improvement => first/lowest index on a tie; torch.argmin
    # also returns the first min index on ties)
    d2 = torch.cdist(X_t, centers_t, p=2)  # [N, K]
    return torch.argmin(d2, dim=1)


def all_heads(Y_t, owner, K, ntr, dev):
    # [K, V] head matrix, add-LAPLACE, over the FIRST ntr train points
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


def grow_on(centers, X_tr, Y_tr, ntr, dev, grow_max):
    """Faithful port of hexa _grow_on: error-targeted Voronoi split, gradient-free, cells only
    SPLIT (p8 — NO merge). centers: python list of 3-vectors. Returns grown list."""
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
        # eligible: owned_n >= MIN_OWNED AND local_ce > SPLIT_THRESH_CE
        elig = [k for k in range(K) if owned_n[k] >= MIN_OWNED and local_ce[k] > SPLIT_THRESH_CE]
        if not elig:
            break
        # TARGETED: highest owned-CE eligible cell (strict > keeps first on tie, like hexa)
        pick = elig[0]
        bestce = local_ce[elig[0]]
        for k in elig[1:]:
            if local_ce[k] > bestce:
                bestce = local_ce[k]
                pick = k
        # engine_mitosis_tick gate (p8): grows exactly one (n -> n+1) when under cap; the
        # split replaces 1 cell with 2 => net +1, identical to the hexa probe.
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
        new_centers = [centers[i] for i in range(len(centers)) if i != pick]
        new_centers = new_centers + [c_lo, c_hi]
        centers = new_centers
    return centers


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ko-window", type=int, default=30_000_000, help="real KO bytes to use")
    ap.add_argument("--en-window", type=int, default=10_000_000, help="real EN bytes (retention)")
    ap.add_argument("--ko-stride", type=int, default=300, help="deterministic subsample stride KO")
    ap.add_argument("--en-stride", type=int, default=600, help="deterministic subsample stride EN")
    ap.add_argument("--grow-max", type=int, default=GROW_MAX)
    ap.add_argument("--out", default="/tmp/h1307_out")
    ap.add_argument("--ko-cache", default="/tmp/h1307_ko_raw.bytes")
    ap.add_argument("--en-cache", default="/tmp/h1307_en_raw.bytes")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    assert torch.cuda.is_available(), "CUDA not available — REFUSING to run on CPU (a_train_flame_forge)"
    dev = torch.device("cuda")
    cap = torch.cuda.get_device_capability(0)
    log(f"=== H_1307 — KOREAN MITOSIS GPU SCALE-UP (engine-native mechanism, RTX 5070 sm_{cap[0]}{cap[1]}) ===")
    log(f"device={torch.cuda.get_device_name(0)} cap={cap} torch={torch.__version__}")
    _t = (torch.randn(1024, 1024, device=dev) @ torch.randn(1024, 1024, device=dev)).sum().item()
    torch.cuda.synchronize()
    log(f"sm_{cap[0]}{cap[1]} kernel launch OK (sentinel {_t:.1f})")

    t0 = time.time()
    if os.path.exists(args.ko_cache) and os.path.getsize(args.ko_cache) >= args.ko_window:
        ko_raw = open(args.ko_cache, "rb").read()[: args.ko_window + 8]
        log(f"[corpus] KO from cache {args.ko_cache} ({len(ko_raw)} bytes)")
    else:
        log(f"[corpus] fetching {args.ko_window} REAL KO bytes from r2://{os.environ.get('R2_BUCKET','?')}/{R2_KO_KEY}")
        ko_raw = fetch_r2_range(R2_KO_KEY, args.ko_window + 8)
        open(args.ko_cache, "wb").write(ko_raw)
    if os.path.exists(args.en_cache) and os.path.getsize(args.en_cache) >= args.en_window:
        en_raw = open(args.en_cache, "rb").read()[: args.en_window + 8]
        log(f"[corpus] EN from cache {args.en_cache} ({len(en_raw)} bytes)")
    else:
        log(f"[corpus] fetching {args.en_window} REAL EN bytes from r2://{os.environ.get('R2_BUCKET','?')}/{R2_EN_KEY}")
        en_raw = fetch_r2_range(R2_EN_KEY, args.en_window + 8)
        open(args.en_cache, "wb").write(en_raw)

    ko_win = trim_utf8(ko_raw[: args.ko_window])
    en_win = trim_utf8(en_raw[: args.en_window])
    ko_sha = hashlib.sha256(ko_win).hexdigest()
    en_sha = hashlib.sha256(en_win).hexdigest()
    log(f"[corpus] KO window {len(ko_win)} bytes sha256={ko_sha[:16]}…  EN window {len(en_win)} bytes sha256={en_sha[:16]}…")

    ko_arr = np.frombuffer(ko_win, dtype=np.uint8).astype(np.int64)
    en_arr = np.frombuffer(en_win, dtype=np.uint8).astype(np.int64)
    log(f"[features] building pairs (CTX={CTX}, FEAT_DIM={FEAT_DIM}) …")
    Xko, Yko = make_pairs(ko_arr)
    Xen, Yen = make_pairs(en_arr)
    Xko, Yko = Xko[:: args.ko_stride], Yko[:: args.ko_stride]
    Xen, Yen = Xen[:: args.en_stride], Yen[:: args.en_stride]
    idx = np.arange(Xko.shape[0])
    Xktr, Yktr = Xko[idx % 2 == 0], Yko[idx % 2 == 0]
    Xkte, Ykte = Xko[idx % 2 == 1], Yko[idx % 2 == 1]
    n = Xktr.shape[0]
    nb1, nb2, nb3 = n // 3, 2 * n // 3, n
    log(f"[pairs] KO train={n} test={Xkte.shape[0]}  EN test={Xen.shape[0]}  curve=[{nb1},{nb2},{nb3}]")

    Xktr_t = torch.tensor(Xktr, dtype=torch.float64, device=dev)
    Yktr_t = torch.tensor(Yktr, dtype=torch.int64, device=dev)
    Xkte_t = torch.tensor(Xkte, dtype=torch.float64, device=dev)
    Ykte_t = torch.tensor(Ykte, dtype=torch.int64, device=dev)
    Xen_t = torch.tensor(Xen, dtype=torch.float64, device=dev)
    Yen_t = torch.tensor(Yen, dtype=torch.int64, device=dev)

    metrics = []

    def emit(rec):
        metrics.append(rec)
        log("  [metric] " + json.dumps(rec))

    seed_t = torch.tensor(SEED_CENTERS, dtype=torch.float64, device=dev)
    en_seed = score_ce(seed_t, Xktr_t, Yktr_t, nb1, Xen_t, Yen_t, dev)
    log(f"[seed] EN CE on 2-cell seed field = {en_seed:.5f}")

    g_t0 = time.time()
    c1 = grow_on(SEED_CENTERS, Xktr_t, Yktr_t, nb1, dev, args.grow_max)
    c1_t = torch.tensor(c1, dtype=torch.float64, device=dev)
    ko_ce1 = score_ce(c1_t, Xktr_t, Yktr_t, nb1, Xkte_t, Ykte_t, dev)
    en_ce1 = score_ce(c1_t, Xktr_t, Yktr_t, nb1, Xen_t, Yen_t, dev)
    emit({"pt": 1, "ko_train": nb1, "cells": len(c1), "ko_ce": round(ko_ce1, 5), "en_ce": round(en_ce1, 5)})

    c2 = grow_on(c1, Xktr_t, Yktr_t, nb2, dev, args.grow_max)
    c2_t = torch.tensor(c2, dtype=torch.float64, device=dev)
    ko_ce2 = score_ce(c2_t, Xktr_t, Yktr_t, nb2, Xkte_t, Ykte_t, dev)
    en_ce2 = score_ce(c2_t, Xktr_t, Yktr_t, nb2, Xen_t, Yen_t, dev)
    emit({"pt": 2, "ko_train": nb2, "cells": len(c2), "ko_ce": round(ko_ce2, 5), "en_ce": round(en_ce2, 5)})

    c3 = grow_on(c2, Xktr_t, Yktr_t, nb3, dev, args.grow_max)
    c3_t = torch.tensor(c3, dtype=torch.float64, device=dev)
    ko_ce3 = score_ce(c3_t, Xktr_t, Yktr_t, nb3, Xkte_t, Ykte_t, dev)
    en_after = score_ce(c3_t, Xktr_t, Yktr_t, nb3, Xen_t, Yen_t, dev)
    emit({"pt": 3, "ko_train": nb3, "cells": len(c3), "ko_ce": round(ko_ce3, 5), "en_ce": round(en_after, 5)})
    grow_wall = time.time() - g_t0
    torch.cuda.synchronize()

    cells_final = len(c3)
    learn_internal = ko_ce3 <= ko_ce1 - 0.05
    scale_vs_600k = ko_ce3 <= H1306_BASELINE_KO_CE
    retain = en_after <= en_seed + 0.05
    grow = cells_final > 2
    green = learn_internal and retain and grow
    total_wall = time.time() - t0
    n_pairs_total = int(Xktr.shape[0] + Xkte.shape[0] + Xen.shape[0])
    throughput = n_pairs_total / max(grow_wall, 1e-9)

    summary = {
        "id": "H_1307",
        "device": torch.cuda.get_device_name(0),
        "sm": f"{cap[0]}{cap[1]}",
        "torch": torch.__version__,
        "ko_window_bytes": len(ko_win),
        "en_window_bytes": len(en_win),
        "ko_window_sha256": ko_sha,
        "en_window_sha256": en_sha,
        "ko_train_pairs": int(n),
        "ko_test_pairs": int(Xkte.shape[0]),
        "en_test_pairs": int(Xen.shape[0]),
        "ko_stride": args.ko_stride,
        "en_stride": args.en_stride,
        "grow_max": args.grow_max,
        "curve": metrics,
        "en_seed_ce": round(en_seed, 5),
        "en_after_ce": round(en_after, 5),
        "ko_ce_pt1": round(ko_ce1, 5),
        "ko_ce_full": round(ko_ce3, 5),
        "h1306_baseline_ko_ce": H1306_BASELINE_KO_CE,
        "cells_final": cells_final,
        "L1_internal_learning": bool(learn_internal),
        "L2_scale_vs_600KB": bool(scale_vs_600k),
        "R_retention": bool(retain),
        "G_growth": bool(grow),
        "GREEN": bool(green),
        "grow_wall_s": round(grow_wall, 2),
        "total_wall_s": round(total_wall, 2),
        "throughput_pairs_per_s": round(throughput, 1),
    }
    with open(os.path.join(args.out, "h1307_summary.json"), "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    with open(os.path.join(args.out, "h1307_metrics.jsonl"), "w") as f:
        for m in metrics:
            f.write(json.dumps(m) + "\n")
        f.write(json.dumps({"seed_en_ce": round(en_seed, 5), "en_after_ce": round(en_after, 5)}) + "\n")
    manifest = {
        "ko_source": f"r2://{os.environ.get('R2_BUCKET','phanes')}/{R2_KO_KEY} bytes[0:{args.ko_window}] trimmed[:{len(ko_win)}]",
        "en_source": f"r2://{os.environ.get('R2_BUCKET','phanes')}/{R2_EN_KEY} bytes[0:{args.en_window}] trimmed[:{len(en_win)}]",
        "ko_window_bytes": len(ko_win),
        "en_window_bytes": len(en_win),
        "ko_window_sha256": ko_sha,
        "en_window_sha256": en_sha,
        "ko_train_pairs": int(n),
        "ko_test_pairs": int(Xkte.shape[0]),
        "en_test_pairs": int(Xen.shape[0]),
        "ko_stride": args.ko_stride,
        "en_stride": args.en_stride,
        "ctx": CTX, "feat_dim": FEAT_DIM, "V": V,
    }
    with open(os.path.join(args.out, "h1307_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    log("-------------------------------------------------------------------------------")
    log("KO learning curve (held-out KO next-byte CE, nats/byte):")
    for m in metrics:
        log(f"  pt{m['pt']} (KO train={m['ko_train']}, cells={m['cells']}): KO ce={m['ko_ce']}  EN ce={m['en_ce']}")
    log(f"retention: EN seed(2-cell)={en_seed:.5f} -> EN after full KO grow={en_after:.5f}")
    log(f"scale: KO ce[full]={ko_ce3:.5f}  vs H_1306 600KB baseline={H1306_BASELINE_KO_CE}")
    log(f"cells: 2 (seed) -> {cells_final} (mitosis added {cells_final - 2})")
    log(f"GPU grow+score wall={grow_wall:.1f}s  throughput={throughput:.0f} pairs/s  total={total_wall:.1f}s")
    log("-------------------------------------------------------------------------------")
    log(f"(L1) INTERNAL LEARN  KO ce[full] <= KO ce[pt1]-0.05: {ko_ce3:.5f} <= {ko_ce1 - 0.05:.5f} -> {'PASS' if learn_internal else 'FAIL'}")
    log(f"(L2) SCALE vs 600KB  KO ce[full] <= {H1306_BASELINE_KO_CE}: {ko_ce3:.5f} -> {'PASS' if scale_vs_600k else 'FAIL'}")
    log(f"(R)  RETENTION       EN ce[after] <= EN ce[seed]+0.05: {en_after:.5f} <= {en_seed + 0.05:.5f} -> {'PASS' if retain else 'FAIL'}")
    log(f"(G)  GROWTH          final cells > 2: {cells_final} -> {'PASS' if grow else 'FAIL'}")
    log("-------------------------------------------------------------------------------")
    log(f"H_1307 VERDICT TIER (GPU scale, engine-native mechanism): {'🟢 GREEN' if green else '🔴 HONEST-DEFERRED'}")
    log(f"  L1={learn_internal} L2(scale)={scale_vs_600k} R={retain} G={grow}")
    log("  GPU-accelerated SAME error-targeted Voronoi mitosis (gradient-free, p8 — cells only SPLIT);")
    log("  engine-transfer to live hexa is DIRECTIONAL (re-confirm on CORE/*.hexa = follow-on). NO fluency claim.")
    log("[done]")


if __name__ == "__main__":
    main()
