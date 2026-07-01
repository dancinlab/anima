#!/usr/bin/env python3
# h1321_ko_jamo_wire_export.py — DATA-PREP for the ENGINE-NATIVE ko-jamo wiring rung
# CORE/h1321_ko_jamo_wire_probe.hexa (a_verified_must_wire + a_engine_native_learning).
#
# H_1321 is the r2 ENGINE-NATIVE WIRING follow-on of H_1316 (🟢 GREEN, PR #2224):
# H_1316 proved (numpy/torch MIRROR, DIRECTIONAL) that a COMPOSITIONAL JAMO representation
# breaks the Korean raw-byte CE ceiling 2.953 → 2.513. This exporter materializes the SAME
# deterministic jamo/raw/shuffle symbol streams that H_1316 builds, subsampled to a
# CPU-tractable pair SET, so the LIVE-engine .hexa probe (CORE/engine_cli.hexa VAdaptField +
# engine_mitosis_tick) can run the SAME gradient-free mitosis + held-out per-byte CE scoring
# ENGINE-NATIVE on the identical streams, and the result can be compared apples-to-apples to a
# SAME-WINDOW mirror reference CE (the W1 tolerance bar in .verdicts/1321_ko_jamo_wire/FREEZE.txt).
#
# THE REPRESENTATION TRANSFORM IS DETERMINISTIC UNICODE (NO learning): the jamo symbolization
# (NFD decomposition of Hangul syllables to L/V/T jamo) is data-prep; the MITOSIS + CE SCORING
# run ENGINE-NATIVE in the .hexa probe. The mirror CE this script emits is a REFERENCE for the
# W1 reproduce-within-tolerance bar ONLY — the binding verdict is the .hexa engine-native value.
#
# CORPUS (REAL only, p1-p8): the SAME r2://phanes/anima-7b/web/kor/shard0000.bytes[0:30M] KO
# window as H_1307 RUN A / H_1316. The 30MB window sha256 is ASSERTED == the H_1316 anchor
# c47b6808… (provenance gate); a mismatch → STOP (NO synthetic Korean). The jamo VOCAB + symbol
# ids are built over the FULL 30MB window (so Vj == the H_1316 Vj==323), THEN the symbol-pair
# stream is deterministically strided to a CPU-tractable count for the hexa interpreter. R2 keys
# are read by the SEPARATE fetch step into env only — this exporter reads the /tmp cache, touches
# NO secret (c7).
#
# $0 CPU, no GPU. Writes /tmp/h1321_*.{feats,next,nbytes} + /tmp/h1321_ref.txt + manifest.

import argparse
import hashlib
import json
import os
import sys
import unicodedata

import numpy as np

# ── FROZEN knobs (verbatim from H_1306/H_1307/H_1316) ───────────────────────────
GROW_MAX = 40
SPLIT_THRESH_CE = 0.05
MIN_OWNED = 8
LAPLACE = 1.0
FEAT_DIM = 3
H1307_CEILING_KO_CE = 2.9475
# H_1316 / H_1307 RUN A 30MB KO window sha (provenance gate — must match):
H1316_KO_SHA_30MB = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
HANGUL_LO, HANGUL_HI = 0xAC00, 0xD7A3

KO_CACHE = "/tmp/h1316_ko_raw.bytes"   # 30MB KO window (shared with H_1316; sibling cache)
OUT = "/tmp"


def log(*a):
    print(*a, flush=True)


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


# ── B3 NO-CHEAT: NFD→NFC round-trip over the whole window (verbatim H_1316) ─
def b3_roundtrip(text):
    bad = 0
    n_syll = 0
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            n_syll += 1
            nfd = unicodedata.normalize("NFD", ch)
            nfc = unicodedata.normalize("NFC", nfd)
            if nfc.encode("utf-8") != ch.encode("utf-8"):
                bad += 1
    return {"hangul_syllables": n_syll, "roundtrip_fail": bad, "ok": bad == 0}


def build_jamo_vocab(text):
    jset = set()
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            for jc in unicodedata.normalize("NFD", ch):
                jset.add(ord(jc))
    jamo_sorted = sorted(jset)
    jamo_to_id = {cp: 256 + i for i, cp in enumerate(jamo_sorted)}
    return jamo_to_id, jamo_sorted


def syll_jamo_nbytes(njamo):
    if njamo == 3:
        return [1, 1, 1]
    if njamo == 2:
        return [2, 1]
    if njamo == 1:
        return [3]
    out = [1] * njamo
    out[0] += (3 - njamo) if njamo < 3 else 0
    return out


def make_symbol_stream(text, jamo_to_id, jamo_remap=None):
    syms, nby = [], []
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            nfd = unicodedata.normalize("NFD", ch)
            nb = syll_jamo_nbytes(len(nfd))
            for j, jc in enumerate(nfd):
                sid = jamo_to_id[ord(jc)]
                if jamo_remap is not None:
                    sid = jamo_remap[sid]
                syms.append(sid)
                nby.append(nb[j])
        else:
            for b in ch.encode("utf-8"):
                syms.append(b)
                nby.append(1)
    return np.asarray(syms, dtype=np.int64), np.asarray(nby, dtype=np.int64)


def depth_stream(text):
    depth = []
    d = 0
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            nfd = unicodedata.normalize("NFD", ch)
            for j in range(len(nfd)):
                d = 0 if j == 0 else d + 1
                depth.append(d)
        else:
            for b in ch.encode("utf-8"):
                d = d + 1 if 0x80 <= b <= 0xBF else 0
                depth.append(d)
    return np.asarray(depth, dtype=np.int64)


# ── score_stream → (X, Y, idx): the H_1316 3-D feature family ────────────────────
def score_stream(syms, depth, vj):
    n = len(syms)
    idx = np.arange(4, n - 1)
    last = syms[idx - 1].astype(np.float64) / float(vj)
    second = syms[idx - 2].astype(np.float64) / float(vj)
    cdep = depth[idx - 1].astype(np.float64) / 3.0
    X = np.stack([last, second, cdep], axis=1)
    Y = syms[idx].astype(np.int64)
    return X, Y, idx


# ── SAME-WINDOW MIRROR mitosis (verbatim H_1306/H_1316 _grow_on, numpy) — REFERENCE only ─
def assign_all_np(centers, X):
    d2 = ((X[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
    return d2.argmin(axis=1)


def all_heads_np(Y, owner, K, ntr, vj):
    H = np.full((K, vj), LAPLACE, dtype=np.float64)
    for i in range(ntr):
        H[owner[i], Y[i]] += 1.0
    H = H / H.sum(axis=1, keepdims=True)
    return H


def owned_ce_np(Y, owner, k, ntr, prow):
    mask = owner[:ntr] == k
    if not mask.any():
        return -1.0
    yk = Y[:ntr][mask]
    return float(-np.log(prow[yk] + 1e-12).mean())


def grow_on_np(centers0, X, Y, ntr, vj):
    centers = [list(c) for c in centers0]
    while len(centers) < GROW_MAX:
        ct = np.asarray(centers, dtype=np.float64)
        owner = assign_all_np(ct, X)
        K = len(centers)
        owned_n = np.bincount(owner[:ntr], minlength=K)
        H = all_heads_np(Y, owner, K, ntr, vj)
        local_ce = np.full(K, -1.0)
        for k in range(K):
            if owned_n[k] > 0:
                local_ce[k] = owned_ce_np(Y, owner, k, ntr, H[k])
        elig = [k for k in range(K) if owned_n[k] >= MIN_OWNED and local_ce[k] > SPLIT_THRESH_CE]
        if not elig:
            break
        pick = elig[0]
        bestce = local_ce[elig[0]]
        for k in elig[1:]:
            if local_ce[k] > bestce:
                bestce = local_ce[k]
                pick = k
        pmask = owner[:ntr] == pick
        pts = X[:ntr][pmask]
        if pts.shape[0] == 0:
            break
        var = pts.var(axis=0)
        ax = int(var.argmax())
        col = pts[:, ax]
        scol = np.sort(col)
        m = len(scol)
        med = scol[m // 2] if m % 2 == 1 else (scol[m // 2 - 1] + scol[m // 2]) / 2.0
        lo, hi = col <= med, col > med
        if lo.sum() == 0 or hi.sum() == 0:
            break
        c_lo = pts[lo].mean(axis=0).tolist()
        c_hi = pts[hi].mean(axis=0).tolist()
        centers = [centers[i] for i in range(len(centers)) if i != pick] + [c_lo, c_hi]
    return centers


def per_byte_ce_np(centers, Xtr, Ytr, ntr, Xte, Yte, NBte, vj):
    ct = np.asarray(centers, dtype=np.float64)
    owner_tr = assign_all_np(ct, Xtr)
    H = all_heads_np(Ytr, owner_tr, len(centers), ntr, vj)
    owner_te = assign_all_np(ct, Xte)
    p = H[owner_te, Yte]
    nll = -np.log(p + 1e-12)
    total_nats = float(nll.sum())
    total_bytes = float(NBte.sum())
    return total_nats / total_bytes, len(centers)


def split_even_odd(X, Y, NB):
    idx = np.arange(X.shape[0])
    e = idx % 2 == 0
    o = idx % 2 == 1
    return X[e], Y[e], NB[e], X[o], Y[o], NB[o]


def seed_centers():
    return [[0.3, 0.5, 0.0], [0.7, 0.5, 0.5]]


def write_feats(path, X):
    with open(path, "w") as f:
        for row in X:
            f.write(" ".join(f"{v:.10f}" for v in row) + "\n")


def write_ints(path, Y):
    with open(path, "w") as f:
        f.write("\n".join(str(int(y)) for y in Y) + "\n")


def arm_export(syms, depth, nby, vj, stride, tag):
    """Build the subsampled even/odd train/test pair set for an arm, write engine-probe
    inputs, and compute the SAME-WINDOW mirror reference CE on the identical pairs."""
    X, Y, idx = score_stream(syms, depth, vj)
    NB = nby[idx]
    # deterministic stride subsample (CPU-tractable for the hexa interpreter), seed-independent
    X, Y, NB = X[::stride], Y[::stride], NB[::stride]
    Xtr, Ytr, NBtr, Xte, Yte, NBte = split_even_odd(X, Y, NB)
    # engine-probe inputs
    write_feats(f"{OUT}/h1321_{tag}_train.feats", Xtr)
    write_ints(f"{OUT}/h1321_{tag}_train.next", Ytr)
    write_feats(f"{OUT}/h1321_{tag}_test.feats", Xte)
    write_ints(f"{OUT}/h1321_{tag}_test.next", Yte)
    write_ints(f"{OUT}/h1321_{tag}_test.nbytes", NBte)
    # SAME-WINDOW mirror reference CE on the identical pair set
    centers = grow_on_np(seed_centers(), Xtr, Ytr, Xtr.shape[0], vj)
    ce, ncell = per_byte_ce_np(centers, Xtr, Ytr, Xtr.shape[0], Xte, Yte, NBte, vj)
    return {
        "tag": tag, "vocab": vj, "train": int(Xtr.shape[0]), "test": int(Xte.shape[0]),
        "test_bytes": int(NBte.sum()), "ref_ce": round(ce, 5), "ref_cells": ncell,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ko-window", type=int, default=30_000_000)
    ap.add_argument("--ko-stride", type=int, default=1200,
                    help="symbol-pair stride for the CPU-tractable hexa probe set")
    ap.add_argument("--seeds", default="4316,4317,4318")
    args = ap.parse_args()

    # ── REAL 30MB KO window, sha-gated to H_1316 ──
    if os.path.exists(KO_CACHE) and os.path.getsize(KO_CACHE) >= args.ko_window:
        ko_raw = open(KO_CACHE, "rb").read()[: args.ko_window + 8]
        log(f"[corpus] KO from cache {KO_CACHE}")
    else:
        log(f"[corpus] fetching {args.ko_window} REAL KO bytes from r2://{os.environ.get('R2_BUCKET','?')}/anima-7b/web/kor/shard0000.bytes")
        ko_raw = fetch_r2_range("anima-7b/web/kor/shard0000.bytes", args.ko_window + 8)
        open(KO_CACHE, "wb").write(ko_raw)
    ko_win = trim_utf8(ko_raw[: args.ko_window])
    ko_sha = hashlib.sha256(ko_win).hexdigest()
    same = (ko_sha == H1316_KO_SHA_30MB)
    log(f"[corpus] KO {len(ko_win)}B sha={ko_sha[:16]}…  identical-to-H_1316-30MB={same}")
    if not same:
        log("FATAL: KO 30MB window sha != H_1316 anchor — REFUSING to run (provenance gate, REAL-only). STOP.")
        sys.exit(3)
    ko_text = ko_win.decode("utf-8")

    # ── B3 NO-CHEAT over the full window ──
    b3 = b3_roundtrip(ko_text)
    log(f"[B3] hangul_syllables={b3['hangul_syllables']} roundtrip_fail={b3['roundtrip_fail']} ok={b3['ok']}")

    # ── jamo vocab over the FULL 30MB window (Vj must == H_1316 323) ──
    jamo_to_id, jamo_sorted = build_jamo_vocab(ko_text)
    n_jamo = len(jamo_sorted)
    VJ = 256 + n_jamo
    log(f"[jamo] distinct jamo={n_jamo}  Vj={VJ}  (H_1316 anchor Vj=323)")

    depth_j = depth_stream(ko_text)
    syms_j, nby_j = make_symbol_stream(ko_text, jamo_to_id, jamo_remap=None)
    assert len(syms_j) == len(depth_j) == len(nby_j)
    acct_bytes = int(nby_j.sum())
    acct_ok = (acct_bytes == len(ko_win))
    log(f"[B3] byte-accounting: Σ n_bytes(sym)={acct_bytes} corpus_bytes={len(ko_win)} close={acct_ok}")
    b3_ok = bool(b3["ok"] and acct_ok)

    # ── G0 raw-byte stream (V=256) ──
    ko_bytes = np.frombuffer(ko_win, dtype=np.uint8).astype(np.int64)
    raw_depth = np.zeros(len(ko_bytes), dtype=np.int64)
    d = 0
    for i in range(len(ko_bytes)):
        b = ko_bytes[i]
        d = d + 1 if 0x80 <= b <= 0xBF else 0
        raw_depth[i] = d
    raw_nby = np.ones(len(ko_bytes), dtype=np.int64)

    g0 = arm_export(ko_bytes, raw_depth, raw_nby, 256, args.ko_stride, "g0")
    log(f"[G0 raw-byte] {json.dumps(g0)}")

    # ── G1 jamo (intact) — vocab Vj (the hexa probe scores ALL its arms at Vj for fair feature scaling;
    #    G0 keeps V=256 — exactly as H_1316: feature is sym/vj per-arm) ──
    g1 = arm_export(syms_j, depth_j, nby_j, VJ, args.ko_stride, "g1")
    log(f"[G1 jamo intact] {json.dumps(g1)}")

    # ── G1c shuffle-jamo control, per seed (bijective permutation of jamo SYMBOL ids) ──
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    g1c_per_seed = []
    for si, sd in enumerate(seeds):
        rng = np.random.default_rng(sd)
        jids = np.arange(256, VJ)
        perm = rng.permutation(jids)
        remap = {int(jids[i]): int(perm[i]) for i in range(len(jids))}
        syms_sh, nby_sh = make_symbol_stream(ko_text, jamo_to_id, jamo_remap=remap)
        gc = arm_export(syms_sh, depth_j, nby_sh, VJ, args.ko_stride, f"g1c{si}")
        gc["seed"] = sd
        g1c_per_seed.append(gc)
        log(f"[G1c shuffle seed {sd}] {json.dumps(gc)}")

    g1c_mean = float(np.mean([g["ref_ce"] for g in g1c_per_seed]))

    # ── reference summary for the .hexa W1 tolerance bar ──
    ref = {
        "ko_window_bytes": len(ko_win), "ko_window_sha256": ko_sha,
        "identical_to_H1316_30MB": same, "Vj": VJ, "distinct_jamo": n_jamo,
        "ko_stride": args.ko_stride, "seeds": seeds,
        "h1307_ceiling_ko_ce": H1307_CEILING_KO_CE,
        "h1316_30MB_mirror_g1_ce": 2.51335,
        "same_window_mirror_g0_ce": g0["ref_ce"],
        "same_window_mirror_g1_ce": g1["ref_ce"],
        "same_window_mirror_g1c_ce_mean": round(g1c_mean, 5),
        "same_window_mirror_g1c_per_seed": [g["ref_ce"] for g in g1c_per_seed],
        "delta_g1_vs_ceiling": round(g1["ref_ce"] - H1307_CEILING_KO_CE, 5),
        "delta_g1_vs_shuffle": round(g1c_mean - g1["ref_ce"], 5),
        "delta_g1_vs_raw": round(g0["ref_ce"] - g1["ref_ce"], 5),
        "b3_roundtrip": b3, "b3_byte_accounting_close": acct_ok, "b3_ok": b3_ok,
    }
    with open(f"{OUT}/h1321_ref.txt", "w") as f:
        # one space-separated line the .hexa probe parses: VJ g0_ref g1_ref g1c_mean b3_ok(1/0)
        f.write(f"{VJ} {g0['ref_ce']:.5f} {g1['ref_ce']:.5f} {g1c_mean:.5f} {1 if b3_ok else 0}\n")
    with open(f"{OUT}/h1321_ref.json", "w") as f:
        json.dump(ref, f, indent=2, ensure_ascii=False)
    # per-seed shuffle tag list so the hexa probe knows how many g1c arms to score
    with open(f"{OUT}/h1321_seeds.txt", "w") as f:
        f.write(" ".join(str(i) for i in range(len(seeds))) + "\n")

    manifest = {
        "ko_source": f"r2://{os.environ.get('R2_BUCKET','phanes')}/anima-7b/web/kor/shard0000.bytes bytes[0:{args.ko_window}] trimmed[:{len(ko_win)}]",
        "ko_window_bytes": len(ko_win), "ko_window_sha256": ko_sha,
        "identical_to_H1316_30MB": same, "ko_stride": args.ko_stride,
        "Vj": VJ, "distinct_jamo": n_jamo, "seeds": seeds,
        "GROW_MAX": GROW_MAX, "SPLIT_THRESH_CE": SPLIT_THRESH_CE,
        "MIN_OWNED": MIN_OWNED, "LAPLACE": LAPLACE, "FEAT_DIM": FEAT_DIM,
        "g0": g0, "g1": g1, "g1c_per_seed": g1c_per_seed,
    }
    with open(f"{OUT}/h1321_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    log("-------------------------------------------------------------------------------")
    log(f"SAME-WINDOW mirror reference (CPU-tractable stride={args.ko_stride}, the EXACT pairs the .hexa probe sees):")
    log(f"  G0 raw-byte   ref CE = {g0['ref_ce']}  ({g0['train']}tr/{g0['test']}te)")
    log(f"  G1 jamo       ref CE = {g1['ref_ce']}  Δvs_ceiling={ref['delta_g1_vs_ceiling']}  ({g1['train']}tr/{g1['test']}te)")
    log(f"  G1c shuffle   ref CE = {round(g1c_mean,5)} (mean)  Δ(g1c-g1)={ref['delta_g1_vs_shuffle']}")
    log(f"H_1316 30MB anchor G1 = 2.51335.  Engine-native .hexa must reproduce same-window G1 within 0.05.")
    log(f"wrote /tmp/h1321_{{g0,g1,g1c*}}_{{train,test}}.{{feats,next}} + test.nbytes + h1321_ref.txt")
    log("[done]")


if __name__ == "__main__":
    main()
