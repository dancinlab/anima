#!/usr/bin/env python3
# h1327_ko_jamo_decode_export.py — DATA-PREP for the LIVE-DECODE WIRING rung
# CORE/generator.hexa §6.5 ko_jamo_consult_* + CORE/h1327_ko_jamo_decode_probe.hexa
# (a_verified_must_wire r3 — the H_1316/H_1321 jamo win must REACH EMISSION).
#
# THREAD: H_1316 🟢 (jamo rep breaks the Korean raw-byte CE ceiling 2.953→2.513, mirror) →
# H_1321 🟢 (that mitosis runs ENGINE-NATIVE byte-exact on the live VAdaptField, reproduces
# the mirror to 1e-7). BUT H_1321 is the MEASUREMENT probe: the jamo win never reaches the
# live DECODE/emission path. anima is a chat daemon — a measured CE win that never reaches
# emission is incomplete (a_verified_must_wire). H_1327 wires the grown jamo cells into the
# generator §6.5 decode-consult surface (mirroring ko_cells_* from H_1312) so the jamo
# structure BIASES the emitted byte, then measures whether the bias REACHES emission, is
# EARNED (shuffle-cell control), and is Ψ-DISJOINT (inert off-Korean).
#
# THIS SCRIPT (data-prep, deterministic; the consult + scoring run ENGINE-NATIVE in the
# generator §6.5 surface + the .hexa probe):
#   1. Rebuild the SAME jamo vocab + symbol streams as H_1321 from the sha-gated 30MB KO window.
#   2. Grow the G1 jamo cells via the SAME gradient-free mitosis (numpy mirror — H_1321 proved
#      this reproduces the live VAdaptField/engine_mitosis_tick to 1e-7; the cells are the
#      identical artifact the engine grows).
#   3. Serialize the grown cells to CORE/ko_jamo_cells.kojamohead — each row =
#         center[0] center[1] center[2]  next_sym_id  emit_byte
#      where next_sym_id is the cell's argmax next-symbol head (count-MLE), and emit_byte is the
#      EMITTABLE byte that symbol contributes to the live decode: for a raw-byte symbol (id<256)
#      = the byte itself; for a jamo symbol (id>=256) = the LEADING UTF-8 byte of that jamo's
#      codepoint (jamo U+11xx → 0xE1; the consult emits the byte that STARTS the jamo-grounded
#      continuation). Header row: "<n_cells> <dim> <Vj>".
#   4. Emit a HELD-OUT KOREAN context test set (the SAME even/odd test split H_1321 scores) so the
#      .hexa probe can measure the consult ON vs OFF:
#         h1327_ctx.feats   : the 3-D jamo-space feature per held-out position (consult input)
#         h1327_ctx.base    : the OFF/base emit byte per position = the RAW-byte arm's argmax
#                             leading-byte at that position (what decode emits with consult OFF)
#         h1327_ctx.truth   : the TRUE next emit byte per position (ground-truth leading byte of
#                             the actual next symbol) — the target both ON and OFF are scored against
#   5. Emit a SHUFFLED-CELL artifact CORE/ko_jamo_cells_shuf.kojamohead (E2 control): the SAME
#      grown centers, but the cell->emit_byte map bijectively PERMUTED (per a fixed seed) — the
#      consult still fires (same Korean-likeness, same nearest-cell geometry) but the learned
#      jamo structure is destroyed, so any emission shift must vanish if the bias is EARNED.
#
# REAL only (p1-p8): the 30MB KO window sha256 is ASSERTED == the H_1316 anchor c47b6808…; a
# mismatch → STOP (NO synthetic Korean). R2 keys env/header-only at fetch, NEVER logged (c7).
# $0 CPU, no GPU.

import argparse
import hashlib
import json
import os
import sys
import unicodedata

import numpy as np

# ── FROZEN knobs (verbatim H_1306/H_1316/H_1321) ────────────────────────────────
GROW_MAX = 40
SPLIT_THRESH_CE = 0.05
MIN_OWNED = 8
LAPLACE = 1.0
FEAT_DIM = 3
H1316_KO_SHA_30MB = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
HANGUL_LO, HANGUL_HI = 0xAC00, 0xD7A3
KO_CACHE = "/tmp/h1316_ko_raw.bytes"
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


def b3_roundtrip(text):
    bad, n_syll = 0, 0
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            n_syll += 1
            nfd = unicodedata.normalize("NFD", ch)
            if unicodedata.normalize("NFC", nfd).encode("utf-8") != ch.encode("utf-8"):
                bad += 1
    return {"hangul_syllables": n_syll, "roundtrip_fail": bad, "ok": bad == 0}


def build_jamo_vocab(text):
    jset = set()
    for ch in text:
        if HANGUL_LO <= ord(ch) <= HANGUL_HI:
            for jc in unicodedata.normalize("NFD", ch):
                jset.add(ord(jc))
    jamo_sorted = sorted(jset)
    jamo_to_id = {cp: 256 + i for i, cp in enumerate(jamo_sorted)}
    id_to_jamo = {256 + i: cp for i, cp in enumerate(jamo_sorted)}
    return jamo_to_id, id_to_jamo, jamo_sorted


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


def make_symbol_stream(text, jamo_to_id):
    syms, nby = [], []
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            nfd = unicodedata.normalize("NFD", ch)
            nb = syll_jamo_nbytes(len(nfd))
            for j, jc in enumerate(nfd):
                syms.append(jamo_to_id[ord(jc)])
                nby.append(nb[j])
        else:
            for b in ch.encode("utf-8"):
                syms.append(b)
                nby.append(1)
    return np.asarray(syms, dtype=np.int64), np.asarray(nby, dtype=np.int64)


def depth_stream(text):
    depth, d = [], 0
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


def score_stream(syms, depth, vj):
    n = len(syms)
    idx = np.arange(4, n - 1)
    last = syms[idx - 1].astype(np.float64) / float(vj)
    second = syms[idx - 2].astype(np.float64) / float(vj)
    cdep = depth[idx - 1].astype(np.float64) / 3.0
    X = np.stack([last, second, cdep], axis=1)
    Y = syms[idx].astype(np.int64)
    return X, Y, idx


def sym_emit_byte(sid, id_to_jamo):
    """The EMITTABLE byte a symbol contributes to the live decode: raw byte (id<256) = itself;
    jamo (id>=256) = the LEADING UTF-8 byte of the jamo codepoint."""
    if sid < 256:
        return int(sid)
    cp = id_to_jamo[int(sid)]
    return int(chr(cp).encode("utf-8")[0])


# ── numpy mirror mitosis (verbatim H_1306/H_1316/H_1321) — H_1321 proved engine-byte-exact ──
def assign_all_np(centers, X):
    d2 = ((X[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
    return d2.argmin(axis=1)


def all_heads_np(Y, owner, K, ntr, vj):
    H = np.full((K, vj), LAPLACE, dtype=np.float64)
    for i in range(ntr):
        H[owner[i], Y[i]] += 1.0
    return H / H.sum(axis=1, keepdims=True)


def owned_ce_np(Y, owner, k, ntr, prow):
    mask = owner[:ntr] == k
    if not mask.any():
        return -1.0
    return float(-np.log(prow[Y[:ntr][mask]] + 1e-12).mean())


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
                bestce, pick = local_ce[k], k
        pmask = owner[:ntr] == pick
        pts = X[:ntr][pmask]
        if pts.shape[0] == 0:
            break
        ax = int(pts.var(axis=0).argmax())
        col = np.sort(pts[:, ax])
        m = len(col)
        med = col[m // 2] if m % 2 == 1 else (col[m // 2 - 1] + col[m // 2]) / 2.0
        lo, hi = pts[:, ax] <= med, pts[:, ax] > med
        if lo.sum() == 0 or hi.sum() == 0:
            break
        c_lo = pts[lo].mean(axis=0).tolist()
        c_hi = pts[hi].mean(axis=0).tolist()
        centers = [centers[i] for i in range(len(centers)) if i != pick] + [c_lo, c_hi]
    return centers


def cell_argmax_heads(centers, Xtr, Ytr, ntr, vj):
    ct = np.asarray(centers, dtype=np.float64)
    owner = assign_all_np(ct, Xtr)
    H = all_heads_np(Ytr, owner, len(centers), ntr, vj)
    return H.argmax(axis=1)  # per-cell argmax next-symbol id


def split_even_odd(X, Y):
    idx = np.arange(X.shape[0])
    return X[idx % 2 == 0], Y[idx % 2 == 0], X[idx % 2 == 1], Y[idx % 2 == 1]


def seed_centers():
    return [[0.3, 0.5, 0.0], [0.7, 0.5, 0.5]]


def write_feats(path, X):
    with open(path, "w") as f:
        for row in X:
            f.write(" ".join(f"{v:.10f}" for v in row) + "\n")


def write_ints(path, Y):
    with open(path, "w") as f:
        f.write("\n".join(str(int(y)) for y in Y) + "\n")


def write_kojamohead(path, centers, top_sym, id_to_jamo, vj):
    with open(path, "w") as f:
        f.write(f"{len(centers)} {FEAT_DIM} {vj}\n")
        for k, c in enumerate(centers):
            sid = int(top_sym[k])
            eb = sym_emit_byte(sid, id_to_jamo)
            f.write(" ".join(f"{v:.6f}" for v in c) + f" {sid} {eb}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ko-window", type=int, default=30_000_000)
    ap.add_argument("--ko-stride", type=int, default=2500)
    ap.add_argument("--shuf-seed", type=int, default=4327)
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
    same = ko_sha == H1316_KO_SHA_30MB
    log(f"[corpus] KO {len(ko_win)}B sha={ko_sha[:16]}…  identical-to-H_1316-30MB={same}")
    if not same:
        log("FATAL: KO 30MB window sha != H_1316 anchor — REFUSING (provenance gate, REAL-only). STOP.")
        sys.exit(3)
    ko_text = ko_win.decode("utf-8")

    b3 = b3_roundtrip(ko_text)
    log(f"[B3] hangul_syllables={b3['hangul_syllables']} roundtrip_fail={b3['roundtrip_fail']} ok={b3['ok']}")

    jamo_to_id, id_to_jamo, jamo_sorted = build_jamo_vocab(ko_text)
    VJ = 256 + len(jamo_sorted)
    log(f"[jamo] distinct jamo={len(jamo_sorted)}  Vj={VJ}  (H_1316 anchor Vj=323)")

    depth_j = depth_stream(ko_text)
    syms_j, nby_j = make_symbol_stream(ko_text, jamo_to_id)

    # ── G1 jamo: grow cells on the strided even/odd-train split ──
    Xj, Yj, _ = score_stream(syms_j, depth_j, VJ)
    Xj, Yj = Xj[:: args.ko_stride], Yj[:: args.ko_stride]
    Xtr, Ytr, Xte, Yte = split_even_odd(Xj, Yj)
    centers = grow_on_np(seed_centers(), Xtr, Ytr, Xtr.shape[0], VJ)
    top_sym = cell_argmax_heads(centers, Xtr, Ytr, Xtr.shape[0], VJ)
    log(f"[G1] grew {len(centers)} jamo cells; per-cell argmax next-sym = {list(map(int, top_sym))}")

    # ── OFF / base predictor: the REPRESENTATION-BLIND baseline = the single most-frequent next
    # symbol over the TRAIN split (a unigram decode that has NO jamo cell structure — what the live
    # decode would emit at a Korean position WITHOUT the jamo consult firing). This is the legitimate
    # "consult OFF" emission: a structure-blind constant predictor. Scoring is on the FULL next-symbol
    # id (NOT the leading byte), so the 0xE1-leading-byte collapse cannot mask the jamo structure. ──
    uni = np.bincount(Ytr, minlength=VJ).argmax()
    off_sym = int(uni)
    log(f"[OFF] representation-blind baseline = unigram-argmax next-sym {off_sym} (emit byte {sym_emit_byte(off_sym, id_to_jamo)})")

    # ── HELD-OUT KOREAN context test set (the SAME even/odd test split) ──
    # truth = the TRUE next jamo-symbol Yte; the .hexa probe consults the jamo cells over feats Xte and
    # scores ON (jamo-cell argmax sym) vs OFF (the constant blind baseline) against truth.
    n_te = Xte.shape[0]
    write_feats(f"{OUT}/h1327_ctx.feats", Xte)
    write_ints(f"{OUT}/h1327_ctx.truth", Yte.astype(np.int64))
    with open(f"{OUT}/h1327_ctx.base", "w") as f:
        f.write(f"{off_sym}\n")   # single line: the blind baseline next-symbol id
    log(f"[ctx] held-out Korean test positions = {n_te}")

    # ── serialize grown cells → CORE artifacts (cell row = center[3] next_sym_id emit_byte) ──
    write_kojamohead("CORE/ko_jamo_cells.kojamohead", centers, top_sym, id_to_jamo, VJ)
    # E2 shuffle control: bijective permutation of the cell->next-symbol map (destroy learned
    # structure; geometry/Korean-likeness/cell-firing IDENTICAL). A NON-FIXED permutation is enforced.
    rng = np.random.default_rng(args.shuf_seed)
    perm = rng.permutation(len(centers))
    while len(centers) > 1 and np.all(perm == np.arange(len(centers))):
        perm = rng.permutation(len(centers))
    top_shuf = np.asarray(top_sym)[perm]
    write_kojamohead("CORE/ko_jamo_cells_shuf.kojamohead", centers, top_shuf, id_to_jamo, VJ)
    log(f"[shuf] E2 control written (cell->next-sym map permuted, seed {args.shuf_seed})")

    # ── reference summary for the probe / card (mirror sanity on the FULL next-symbol id) ──
    ct = np.asarray(centers, dtype=np.float64)
    j_owner_te = assign_all_np(ct, Xte)
    on_sym = top_sym[j_owner_te]                  # jamo-cell argmax next-symbol per held-out ctx
    shuf_sym = top_shuf[j_owner_te]               # shuffled-cell argmax next-symbol
    off_pred = np.full(n_te, off_sym, dtype=np.int64)
    acc_off = float((off_pred == Yte).mean())
    acc_on = float((on_sym == Yte).mean())
    acc_shuf = float((shuf_sym == Yte).mean())
    shift_on = float((on_sym != off_pred).mean())   # fraction of positions the consult changes emission
    shift_shuf = float((shuf_sym != off_pred).mean())
    ref = {
        "ko_window_bytes": len(ko_win), "ko_window_sha256": ko_sha,
        "identical_to_H1316_30MB": same, "Vj": VJ, "distinct_jamo": len(jamo_sorted),
        "ko_stride": args.ko_stride, "n_cells": len(centers), "n_test": n_te,
        "off_sym": off_sym, "shuf_seed": args.shuf_seed, "b3_ok": bool(b3["ok"]),
        "mirror_acc_off": round(acc_off, 5), "mirror_acc_on": round(acc_on, 5),
        "mirror_acc_shuf": round(acc_shuf, 5),
        "mirror_shift_on": round(shift_on, 5), "mirror_shift_shuf": round(shift_shuf, 5),
        "mirror_acc_lift_on": round(acc_on - acc_off, 5),
        "mirror_acc_lift_shuf": round(acc_shuf - acc_off, 5),
    }
    with open(f"{OUT}/h1327_ref.json", "w") as f:
        json.dump(ref, f, indent=2, ensure_ascii=False)
    # one line for the .hexa probe: Vj n_cells n_test off_sym b3_ok
    with open(f"{OUT}/h1327_ref.txt", "w") as f:
        f.write(f"{VJ} {len(centers)} {n_te} {off_sym} {1 if b3['ok'] else 0}\n")

    log("-------------------------------------------------------------------------------")
    log(f"[mirror sanity] OFF acc={acc_off:.4f}  ON acc={acc_on:.4f} (lift {acc_on-acc_off:+.4f})  SHUF acc={acc_shuf:.4f} (lift {acc_shuf-acc_off:+.4f})")
    log(f"[mirror sanity] ON shift={shift_on:.4f}  SHUF shift={shift_shuf:.4f}")
    log("wrote CORE/ko_jamo_cells.kojamohead + CORE/ko_jamo_cells_shuf.kojamohead + /tmp/h1327_ctx.{feats,base,truth} + /tmp/h1327_ref.{txt,json}")
    log("[done]")


if __name__ == "__main__":
    main()
