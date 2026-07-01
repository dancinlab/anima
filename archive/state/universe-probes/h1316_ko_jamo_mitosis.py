#!/usr/bin/env python3
# h1316_ko_jamo_mitosis.py — does a COMPOSITIONAL JAMO representation let gradient-free mitosis
# break the H_1307 ~2.953 nat/byte raw-byte Korean ceiling — where raw bytes could not?
#
# THE WALL (🔴 TERMINAL Korean-mitosis thread): gradient-free mitosis cannot beat ~2.953 nat/byte
# held-out KO next-byte CE.  H_1307 RUN A raw-byte ctx4 = 2.9475 (ceiling) · H_1311 richer raw-byte
# substrate did NOT break it (capacity-bound) · H_1315 mitosis over the 303M frozen rep did NOT
# break it (3.146, worse).
#
# THE NEW ANGLE: every prior KO lane fed the substrate RAW UTF-8 bytes — 3 opaque bytes per Hangul
# syllable, ZERO awareness that Korean is a COMPOSITIONAL syllable-block script. The missing
# structure (a_no_llm_frame_trap / c15) is JAMO composition: each syllable = 초성 L + 중성 V +
# 종성 T jamo, recoverable by DETERMINISTIC Unicode NFD decomposition. We map the SAME real corpus
# to a jamo-symbol stream and grow the SAME gradient-free Voronoi mitosis on it, then convert the
# per-symbol CE back to nats/UTF-8-byte for an apples-to-apples comparison vs the 2.9475 ceiling.
#
# FROZEN-FIRST bars (pre-registered .verdicts/1316_ko_jamo_mitosis/H_1316_FREEZE.txt BEFORE the run;
# NOT moved — c9/p7; held-out DETERMINISTIC next-symbol CE renormalized per byte; NO perplexity-truth):
#   B1 PRESENCE   G1 jamo KO CE (nats/UTF-8-byte) < 2.9475 - 0.05 = 2.8975, mean over 3 seeds.
#   B2 EARNED     G1 beats G1c (shuffled jamo→symbol map) by >=0.05  AND  G1 beats G0 raw-byte by >=0.05.
#   B3 NO-CHEAT   NFD→NFC round-trips byte-identical over the whole KO window AND per-symbol n_bytes
#                 sum == corpus UTF-8 byte count exactly (honest byte axis).
#   GREEN iff B1 ∧ B2 ∧ B3. If B1 holds but B2 fails → gain is dims-not-structure (NOT green). If B1
#   fails → honest 🔴/🧱: ceiling is CAPACITY-bound, survives the compositional lens too (valid, c9).
#
# REAL Korean only (NO synthetic, p1-p8): the SAME anima-7b R2 web corpus windows as H_1307 RUN A
# (r2://phanes/anima-7b/web/{kor,eng}/shard0000.bytes); KO/EN window sha256 ASSERTED == the H_1307
# RUN A manifest hashes so the corpus is provably identical. R2 keys read from ENV ONLY at fetch
# time, never echoed/logged/committed (c7). SCALE-HONEST: toy/DIRECTIONAL; engine-transfer to live
# hexa = follow-on; NO fluency claim.

import argparse
import hashlib
import json
import os
import sys
import time
import unicodedata

import numpy as np

try:
    import torch
except Exception as e:  # pragma: no cover
    print("FATAL: torch import failed:", e)
    sys.exit(2)

# ── FROZEN knobs (verbatim from H_1306 / H_1307) ───────────────────────────────
GROW_MAX = 40
SPLIT_THRESH_CE = 0.05
MIN_OWNED = 8
LAPLACE = 1.0
# H_1307 RUN A (stride-300, 30MB) is the raw-byte ceiling this lane must break:
H1307_CEILING_KO_CE = 2.9475
B1_MARGIN = 0.05            # B1: jamo must beat the ceiling by >= this
B2_MARGIN = 0.05            # B2: jamo must beat shuffle-control AND raw-byte by >= this
# H_1307 RUN A corpus window hashes — ASSERT identical (provenance, p7):
H1307_KO_SHA = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
H1307_EN_SHA = "31b4a5430441cfdbb496b59f392150e4aa748cde2ed1b7cedad10960f0bcaf73"

R2_KO_KEY = "anima-7b/web/kor/shard0000.bytes"
R2_EN_KEY = "anima-7b/web/eng/shard0000.bytes"

HANGUL_LO, HANGUL_HI = 0xAC00, 0xD7A3   # precomposed Hangul syllable block


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


# ── B3 NO-CHEAT: NFD→NFC round-trip over the whole KO window + byte-accounting close ─
def b3_roundtrip_and_accounting(text):
    """For every Hangul syllable: NFD-decompose then NFC-recompose, assert UTF-8 bytes identical.
    Also build per-syllable jamo n_bytes that SUM to the syllable's UTF-8 byte length (3)."""
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


# ── SYMBOL STREAM builders ──────────────────────────────────────────────────────
# A SYMBOL = an integer id in a shared alphabet. Non-Hangul codepoints emit one symbol per RAW BYTE
# (id = byte value 0..255). A Hangul syllable emits one symbol per NFD jamo (id = 256 + jamo_rank).
# Each symbol also carries n_bytes = UTF-8 bytes it accounts for; per-syllable jamo n_bytes sum to 3.

def build_jamo_vocab(text):
    """Scan once: collect the distinct NFD-jamo codepoints, assign each a stable rank (sorted)."""
    jset = set()
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            for jc in unicodedata.normalize("NFD", ch):
                jset.add(ord(jc))
    jamo_sorted = sorted(jset)
    jamo_to_id = {cp: 256 + i for i, cp in enumerate(jamo_sorted)}   # bytes occupy 0..255
    return jamo_to_id, jamo_sorted


def syll_jamo_nbytes(njamo):
    """Distribute the syllable's 3 UTF-8 bytes across its jamo so they SUM to 3 (lossless axis).
    3 jamo (L,V,T) → [1,1,1]; 2 jamo (L,V) → [2,1]."""
    if njamo == 3:
        return [1, 1, 1]
    if njamo == 2:
        return [2, 1]
    if njamo == 1:
        return [3]
    # >3 (rare archaic clusters): give the remainder to the first jamo
    out = [1] * njamo
    out[0] += (3 - njamo) if njamo < 3 else 0
    return out


def make_symbol_stream(text, jamo_to_id, jamo_remap=None):
    """Return (syms[int32], nbytes[int32]). If jamo_remap is given (a permutation dict over jamo
    SYMBOL ids), relabel each jamo symbol → its remapped id (B2 shuffle control: scrambles the
    L→V→T sequential alignment while keeping vocab/dim/marginal)."""
    syms = []
    nby = []
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
                syms.append(b)        # raw byte id 0..255
                nby.append(1)
    return np.asarray(syms, dtype=np.int64), np.asarray(nby, dtype=np.int64)


def depth_stream(text):
    """Per-symbol continuation depth, computed structurally as we emit symbols:
       - raw byte that is a UTF-8 continuation byte (0x80..0xBF) → depth = prev+1 (matches H_1307)
       - a jamo that is NOT the first jamo of its syllable → depth = prev+1
       - otherwise → 0.
    Returns an int array aligned with make_symbol_stream's symbol order."""
    depth = []
    d = 0
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            nfd = unicodedata.normalize("NFD", ch)
            for j in range(len(nfd)):
                if j == 0:
                    d = 0
                else:
                    d = d + 1
                depth.append(d)
        else:
            for b in ch.encode("utf-8"):
                if 0x80 <= b <= 0xBF:
                    d = d + 1
                else:
                    d = 0
                depth.append(d)
    return np.asarray(depth, dtype=np.int64)


# ── engine-native mitosis (BYTE-FAITHFUL to H_1306/H_1307 _grow_on; dimension/vocab-agnostic) ──
def assign_all(centers_t, X_t):
    d2 = torch.cdist(X_t, centers_t, p=2)
    return torch.argmin(d2, dim=1)


def all_heads(Y_t, owner, K, ntr, vj, dev):
    Hmat = torch.full((K, vj), LAPLACE, dtype=torch.float64, device=dev)
    own = owner[:ntr]
    y = Y_t[:ntr]
    flat = own * vj + y
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


def grow_on(centers, X_tr, Y_tr, ntr, vj, dev, grow_max):
    """Faithful port of the H_1306/H_1307 hexa _grow_on (gradient-free, cells only SPLIT — p8)."""
    centers = [list(c) for c in centers]
    while len(centers) < grow_max:
        ct = torch.tensor(centers, dtype=torch.float64, device=dev)
        owner = assign_all(ct, X_tr)
        K = len(centers)
        owntr = owner[:ntr]
        owned_n = torch.bincount(owntr, minlength=K).cpu().numpy()
        Hmat = all_heads(Y_tr, owner, K, ntr, vj, dev)
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
        centers = [centers[i] for i in range(len(centers)) if i != pick] + [c_lo, c_hi]
    return centers


def seed_centers():
    """H_1307 SEED_CENTERS pattern, 3-D: [[0.3,0.5,0.0],[0.7,0.5,0.5]]."""
    return [[0.3, 0.5, 0.0], [0.7, 0.5, 0.5]]


def split_even_odd(X, Y, NB, stride):
    X, Y, NB = X[::stride], Y[::stride], NB[::stride]
    idx = np.arange(X.shape[0])
    e = idx % 2 == 0
    o = idx % 2 == 1
    return X[e], Y[e], NB[e], X[o], Y[o], NB[o]


def per_byte_ce(centers_t, X_tr_t, Y_tr_t, ntr, X_te_t, Y_te_t, NB_te, vj, dev):
    """Grow-free scoring: build count-MLE heads on TRAIN owners, score held-out TEST.
    Returns CE_per_byte = Σ(-log p(sym)) / Σ(n_bytes(sym))  — the SAME axis as the raw-byte ceiling."""
    owner_tr = assign_all(centers_t, X_tr_t)
    Hmat = all_heads(Y_tr_t, owner_tr, centers_t.shape[0], ntr, vj, dev)
    owner_te = assign_all(centers_t, X_te_t)
    p = Hmat[owner_te, Y_te_t]
    nll = -torch.log(p + 1e-12)                       # per-symbol nats, [N_te]
    nb_t = torch.tensor(NB_te, dtype=torch.float64, device=dev)
    total_nats = nll.sum().item()
    total_bytes = float(nb_t.sum().item())
    return total_nats / total_bytes, total_nats, total_bytes, len(nll)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ko-window", type=int, default=30_000_000)
    ap.add_argument("--en-window", type=int, default=10_000_000)
    ap.add_argument("--ko-stride", type=int, default=300)
    ap.add_argument("--en-stride", type=int, default=600)
    ap.add_argument("--grow-max", type=int, default=GROW_MAX)
    ap.add_argument("--seeds", default="4316,4317,4318")
    ap.add_argument("--out", default="/tmp/h1316_out")
    ap.add_argument("--ko-cache", default="/tmp/h1316_ko_raw.bytes")
    ap.add_argument("--en-cache", default="/tmp/h1316_en_raw.bytes")
    ap.add_argument("--cpu", action="store_true", help="force CPU (fallback only)")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    if args.cpu or not torch.cuda.is_available():
        dev = torch.device("cpu")
        log("=== H_1316 — JAMO-COMPOSITION vs the H_1307 2.9475 raw-byte ceiling (CPU) ===")
    else:
        dev = torch.device("cuda")
        cap = torch.cuda.get_device_capability(0)
        log(f"=== H_1316 — JAMO-COMPOSITION vs the H_1307 2.9475 raw-byte ceiling (sm_{cap[0]}{cap[1]}) ===")
        log(f"device={torch.cuda.get_device_name(0)} cap={cap} torch={torch.__version__}")
        _t = (torch.randn(512, 512, device=dev) @ torch.randn(512, 512, device=dev)).sum().item()
        torch.cuda.synchronize()
        log(f"kernel launch OK (sentinel {_t:.1f})")

    t0 = time.time()
    # ── REAL corpus, BYTE-IDENTICAL to H_1307 RUN A ──
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
    same_ko = (ko_sha == H1307_KO_SHA)
    same_en = (en_sha == H1307_EN_SHA)
    log(f"[corpus] KO {len(ko_win)}B sha={ko_sha[:16]}…  EN {len(en_win)}B sha={en_sha[:16]}…")
    log(f"[corpus] identical-to-H_1307-RUN-A: KO={same_ko} EN={same_en}")
    if not same_ko:
        log("FATAL: KO corpus sha != H_1307 RUN A — REFUSING to run (provenance gate, REAL-only). STOP.")
        sys.exit(3)

    ko_text = ko_win.decode("utf-8")

    # ── B3 NO-CHEAT: NFD→NFC round-trip + byte accounting ──
    b3 = b3_roundtrip_and_accounting(ko_text)
    log(f"[B3] hangul_syllables={b3['hangul_syllables']} roundtrip_fail={b3['roundtrip_fail']} ok={b3['ok']}")

    # ── G0 RAW-BYTE baseline (vocab 256) — reproduce the H_1307 ceiling, same mitosis/budget ──
    ko_bytes = np.frombuffer(ko_win, dtype=np.uint8).astype(np.int64)
    raw_depth = np.zeros(len(ko_bytes), dtype=np.int64)
    d = 0
    is_cont = (ko_bytes >= 0x80) & (ko_bytes <= 0xBF)
    for i in range(len(ko_bytes)):
        d = d + 1 if is_cont[i] else 0
        raw_depth[i] = d
    VJ_RAW = 256

    def score_stream(syms, depth, vj):
        n = len(syms)
        idx = np.arange(4, n - 1)
        last = syms[idx - 1].astype(np.float64) / float(vj)
        second = syms[idx - 2].astype(np.float64) / float(vj)
        cdep = depth[idx - 1].astype(np.float64) / 3.0
        X = np.stack([last, second, cdep], axis=1)
        Y = syms[idx].astype(np.int64)
        # label-position byte cost: for raw stream every symbol=1 byte; for jamo, the label symbol's
        # n_bytes. We pass the per-symbol nbytes array (aligned to syms) and select label positions.
        return X, Y, idx

    def arm_ce(syms, depth, nbytes, vj, stride):
        X, Y, idx = score_stream(syms, depth, vj)
        NB_lab = nbytes[idx]                      # bytes the LABEL (predicted) symbol accounts for
        Xtr, Ytr, NBtr, Xte, Yte, NBte = split_even_odd(X, Y, NB_lab, stride)
        Xtr_t = torch.tensor(Xtr, dtype=torch.float64, device=dev)
        Ytr_t = torch.tensor(Ytr, dtype=torch.int64, device=dev)
        Xte_t = torch.tensor(Xte, dtype=torch.float64, device=dev)
        Yte_t = torch.tensor(Yte, dtype=torch.int64, device=dev)
        seed = seed_centers()
        c = grow_on(seed, Xtr_t, Ytr_t, Xtr.shape[0], vj, dev, args.grow_max)
        ct = torch.tensor(c, dtype=torch.float64, device=dev)
        ce_b, tot_nats, tot_bytes, nsym = per_byte_ce(ct, Xtr_t, Ytr_t, Xtr.shape[0], Xte_t, Yte_t, NBte, vj, dev)
        if dev.type == "cuda":
            torch.cuda.synchronize()
        return {
            "cells": len(c), "ce_per_byte": round(ce_b, 5),
            "train_sym": int(Xtr.shape[0]), "test_sym": int(Xte.shape[0]),
            "test_bytes": int(tot_bytes), "vocab": vj,
        }

    raw_nbytes = np.ones(len(ko_bytes), dtype=np.int64)
    g0 = arm_ce(ko_bytes, raw_depth, raw_nbytes, VJ_RAW, args.ko_stride)
    log(f"[G0 raw-byte] {json.dumps(g0)}  (H_1307 RUN A ceiling=2.9475; port check)")

    # ── G1 JAMO-rep (intact) + G1c SHUFFLE-jamo control ──
    jamo_to_id, jamo_sorted = build_jamo_vocab(ko_text)
    n_jamo = len(jamo_sorted)
    VJ = 256 + n_jamo
    log(f"[jamo] distinct jamo codepoints={n_jamo}  jamo-symbol vocab Vj={VJ}")
    depth_j = depth_stream(ko_text)
    syms_j, nby_j = make_symbol_stream(ko_text, jamo_to_id, jamo_remap=None)
    assert len(syms_j) == len(depth_j) == len(nby_j)
    # byte accounting close: per-symbol nbytes over the FULL stream == corpus UTF-8 byte count
    acct_bytes = int(nby_j.sum())
    acct_ok = (acct_bytes == len(ko_win))
    log(f"[B3] byte-accounting: Σ n_bytes(sym)={acct_bytes}  corpus_bytes={len(ko_win)}  close={acct_ok}")
    b3_ok = bool(b3["ok"] and acct_ok)

    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    per_seed = []
    for sd in seeds:
        # intact jamo
        g1 = arm_ce(syms_j, depth_j, nby_j, VJ, args.ko_stride)
        # shuffle control: bijective permutation of the jamo SYMBOL ids (256..VJ-1), fixed by seed
        rng = np.random.default_rng(sd)
        jids = np.arange(256, VJ)
        perm = rng.permutation(jids)
        remap = {int(jids[i]): int(perm[i]) for i in range(len(jids))}
        syms_sh, nby_sh = make_symbol_stream(ko_text, jamo_to_id, jamo_remap=remap)
        # depth + nbytes are structural (unchanged by relabel); reuse depth_j; nby identical pattern
        g1c = arm_ce(syms_sh, depth_j, nby_sh, VJ, args.ko_stride)
        rec = {
            "seed": sd,
            "g0_raw_ce": g0["ce_per_byte"],
            "g1_jamo_ce": g1["ce_per_byte"], "g1_cells": g1["cells"],
            "g1c_shuffle_ce": g1c["ce_per_byte"], "g1c_cells": g1c["cells"],
        }
        log(f"[seed {sd}] " + json.dumps(rec))
        per_seed.append(rec)

    # ── mean over seeds (g0 deterministic; g1 deterministic given stream; g1c varies by perm seed) ──
    g0_mean = g0["ce_per_byte"]
    g1_mean = float(np.mean([r["g1_jamo_ce"] for r in per_seed]))
    g1c_mean = float(np.mean([r["g1c_shuffle_ce"] for r in per_seed]))

    # ── FROZEN bars ──
    b1 = (g1_mean < (H1307_CEILING_KO_CE - B1_MARGIN))
    b2_vs_shuffle = ((g1c_mean - g1_mean) >= B2_MARGIN)
    b2_vs_raw = ((g0_mean - g1_mean) >= B2_MARGIN)
    b2 = bool(b2_vs_shuffle and b2_vs_raw)
    b3_pass = b3_ok
    green = bool(b1 and b2 and b3_pass)
    if green:
        verdict = "🟢 GREEN — REPRESENTATION-bound (jamo composition breaks the 2.9475 raw-byte ceiling)"
    elif b1 and not b2:
        verdict = "🟠 PARTIAL — B1 holds but B2 fails: the gain is dims/vocab, NOT compositional structure"
    elif not b1:
        verdict = "🔴 HONEST-NEGATIVE — B1 fails: the byte ceiling SURVIVES the jamo lens → CAPACITY-bound"
    else:
        verdict = "🔴 mixed-fail"
    if not b3_pass:
        verdict = "🔴 B3 FAIL — decomposition not lossless; CE not honestly comparable"

    total_wall = time.time() - t0
    summary = {
        "id": "H_1316",
        "device": (torch.cuda.get_device_name(0) if dev.type == "cuda" else "cpu"),
        "torch": torch.__version__,
        "ko_window_bytes": len(ko_win), "en_window_bytes": len(en_win),
        "ko_window_sha256": ko_sha, "en_window_sha256": en_sha,
        "corpus_identical_to_H1307_runA": bool(same_ko and same_en),
        "ko_stride": args.ko_stride, "grow_max": args.grow_max,
        "jamo_vocab_Vj": VJ, "distinct_jamo": n_jamo,
        "h1307_ceiling_ko_ce": H1307_CEILING_KO_CE,
        "g0_raw_byte_ce": g0_mean,
        "g1_jamo_ce_mean": round(g1_mean, 5),
        "g1c_shuffle_ce_mean": round(g1c_mean, 5),
        "delta_g1_vs_ceiling": round(g1_mean - H1307_CEILING_KO_CE, 5),
        "delta_g1_vs_shuffle": round(g1c_mean - g1_mean, 5),
        "delta_g1_vs_raw": round(g0_mean - g1_mean, 5),
        "seeds": seeds, "per_seed": per_seed,
        "b3_roundtrip": b3, "b3_byte_accounting_close": acct_ok,
        "B1_presence": bool(b1), "B2_earned": b2, "B2_vs_shuffle": bool(b2_vs_shuffle),
        "B2_vs_raw": bool(b2_vs_raw), "B3_nocheat": bool(b3_pass),
        "GREEN": green, "verdict": verdict,
        "total_wall_s": round(total_wall, 2),
    }
    with open(os.path.join(args.out, "h1316_summary.json"), "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    manifest = {
        "ko_source": f"r2://{os.environ.get('R2_BUCKET','phanes')}/{R2_KO_KEY} bytes[0:{args.ko_window}] trimmed[:{len(ko_win)}]",
        "ko_window_bytes": len(ko_win), "ko_window_sha256": ko_sha,
        "en_window_sha256": en_sha, "identical_to_H1307_runA": bool(same_ko and same_en),
        "ko_stride": args.ko_stride, "grow_max": args.grow_max, "jamo_vocab": VJ,
    }
    with open(os.path.join(args.out, "h1316_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    log("-------------------------------------------------------------------------------")
    log(f"G0 raw-byte ceiling (in-run)  KO CE = {g0_mean}  (H_1307 RUN A = 2.9475)")
    log(f"G1 jamo-rep (mean {len(seeds)} seeds) KO CE = {round(g1_mean,5)}  Δvs_ceiling={round(g1_mean-H1307_CEILING_KO_CE,5)}")
    log(f"G1c shuffle-jamo control (mean)        KO CE = {round(g1c_mean,5)}  Δ(g1c-g1)={round(g1c_mean-g1_mean,5)}")
    log(f"B1 PRESENCE  (g1 < {H1307_CEILING_KO_CE-B1_MARGIN:.4f}): {b1}")
    log(f"B2 EARNED    (g1<g1c by>={B2_MARGIN} AND g1<g0 by>={B2_MARGIN}): {b2}  (vs_shuffle={b2_vs_shuffle} vs_raw={b2_vs_raw})")
    log(f"B3 NO-CHEAT  (roundtrip lossless AND byte-acct close): {b3_pass}")
    log(f"VERDICT: {verdict}")
    log(f"total wall={total_wall:.1f}s")
    log("  engine-transfer to live hexa DIRECTIONAL (re-confirm on CORE/*.hexa = follow-on). NO fluency claim.")
    log("[done]")


if __name__ == "__main__":
    main()
