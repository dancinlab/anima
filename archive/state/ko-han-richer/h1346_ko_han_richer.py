#!/usr/bin/env python3
# h1346_ko_han_richer_head.py — CROSS-LANGUAGE STRUCTURE MATRIX r3: RICHER HEAD.
#
# Named follow-on of H_1324 (a_break_the_wall / c16). H_1324 (🔴/🧱) found that
# even under a PROPER one-level IDS component decomposition, Chinese AND Japanese
# kanji composition does NOT help the gradient-free per-cell UNIGRAM mechanism
# (zh Δ=−0.737, ja Δ=−0.628; neither beats its component-shuffle). H_1324's own
# diagnosis (c9): the Han structure is MULTI-LEVEL (語→言+吾, 吾→五+口) which a
# ONE-level leaf head flattens, and the missing signal is the component-BIGRAM
# statistics a CTX=4 Voronoi-UNIGRAM head cannot capture. H_1346 supplies BOTH
# richer ingredients as a NEW pre-registration:
#
#   (1) RECURSIVE multi-level IDS — expand each leaf again via the same CHISE
#       IDS DB to MAX_DEPTH=3 (a component TREE → deepest atomic frontier).
#   (2) COMPONENT-BIGRAM per-cell head — P(next | cell, prev-symbol) with
#       add-λ backoff to the cell unigram (context-1, not context-0 unigram).
#
# Applied IDENTICALLY to RAW, STRUCT, SHUFFLE in EVERY language so the matrix is
# fair. Korean (NFD jamo) + English (no-comp floor) stay as calibration anchors.
# The grow-op (cell PARTITION) is held byte-faithful to H_1324's _grow_on.
#
# torch ABSENT on this host → the dim/vocab-agnostic mitosis grow-op is
# re-implemented in PURE NUMPY, byte-faithful to the H_1324 torch _grow_on:
# same error-targeted Voronoi median-split on the max-variance axis, same Laplace
# count heads. $0 CPU. TOY/DIRECTIONAL mirror; engine-transfer = follow-on.
#
# REAL corpora ONLY (NO synthetic, p1-p8): wikimedia/wikipedia 20231101 (ko/zh/
# ja/en) via HF datasets-server /rows (SAME source as H_1318/H_1324). HF token
# via env HF_TOKEN, header-only, NEVER logged/inlined/committed (c7). sha256 per
# window + IDS DB asserted.
#
# FROZEN-FIRST bars: .verdicts/1346_ko_han_richer_head/FREEZE.txt (pre-registered,
# NOT moved — c9/p7). H1 HAN-GAIN / H2 EARNED-vs-shuffle / H3 CALIBRATION (ko+en).

import argparse
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request

import numpy as np

# ── FROZEN knobs (verbatim from H_1324 / H_1318) ──────────────────────────────
CTX = 4
FEAT_DIM = 3
GROW_MAX = 40
SPLIT_THRESH_CE = 0.05
MIN_OWNED = 8
LAPLACE = 1.0
SEED_CENTERS = [[0.3, 0.5, 0.0], [0.7, 0.5, 0.5]]

# ── NEW richer-head knobs (the only frozen additions vs H_1324) ───────────────
MAX_DEPTH = 3          # recursive IDS expansion depth (component TREE)

HANGUL_LO, HANGUL_HI = 0xAC00, 0xD7A3
CJK_LO, CJK_HI = 0x4E00, 0x9FFF
CJK_EXT_A_LO, CJK_EXT_A_HI = 0x3400, 0x4DBF

IDC = set("⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻")

LANGS = [
    ("ko", "20231101.ko", "hangul"),   # CALIBRATION anchor (compositional)
    ("zh", "20231101.zh", "han"),      # TEST (logographic compositional)
    ("ja", "20231101.ja", "han"),      # TEST (kanji->recursive IDS; kana atomic)
    ("en", "20231101.en", "none"),     # CALIBRATION anchor (no-composition floor)
]

IDS_URL = "https://raw.githubusercontent.com/cjkvi/cjkvi-ids/master/ids.txt"


def log(*a):
    print(*a, flush=True)


# ── REAL corpus fetch: HF datasets-server /rows (public; token header-only) ───
def hf_headers():
    tok = os.environ.get("HF_TOKEN", "")
    h = {"User-Agent": "anima-h1346"}
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return h


def trim_utf8(b):
    for cut in range(0, 4):
        try:
            b[: len(b) - cut].decode("utf-8")
            return b[: len(b) - cut]
        except Exception:
            continue
    return b


def fetch_window_bytes(config, window, cache):
    if os.path.exists(cache) and os.path.getsize(cache) >= window:
        b = open(cache, "rb").read()[: window + 8]
        log(f"[corpus] {config} from cache {cache} ({len(b)}B)")
        return trim_utf8(b[:window])
    buf = bytearray()
    NL = "\n".encode("utf-8")
    offset = 0
    PAGE = 100
    while len(buf) < window + 64:
        url = (f"https://datasets-server.huggingface.co/rows?dataset=wikimedia/wikipedia"
               f"&config={config}&split=train&offset={offset}&length={PAGE}")
        d = None
        for attempt in range(8):
            try:
                req = urllib.request.Request(url, headers=hf_headers())
                d = json.load(urllib.request.urlopen(req, timeout=180))
                break
            except urllib.error.HTTPError as he:
                if he.code in (429, 502, 503, 504):
                    wait = min(60, 5 * (2 ** attempt))
                    log(f"[corpus] {config} offset {offset} HTTP {he.code} -> backoff {wait}s (attempt {attempt+1}/8)")
                    time.sleep(wait)
                    continue
                raise
        if d is None:
            raise RuntimeError(f"{config} offset {offset}: exhausted retries (rate-limited)")
        rows = d.get("rows", [])
        if not rows:
            break
        time.sleep(0.4)
        for r in rows:
            s = r["row"].get("text") or ""
            if s:
                buf += s.encode("utf-8")
                buf += NL
        offset += len(rows)
        if len(rows) < PAGE:
            break
    b = bytes(buf[: window + 8])
    with open(cache, "wb") as f:
        f.write(b)
    log(f"[corpus] {config} fetched {len(b)}B via /rows (offset reached {offset})")
    return trim_utf8(b[:window])


# ── RECURSIVE IDS decomposition (richer-head change #1) ───────────────────────
def is_han(cp):
    return (CJK_LO <= cp <= CJK_HI) or (CJK_EXT_A_LO <= cp <= CJK_EXT_A_HI)


def fetch_ids_db(cache):
    if os.path.exists(cache) and os.path.getsize(cache) > 1_000_000:
        raw = open(cache, "rb").read()
        log(f"[ids] from cache {cache} ({len(raw)}B)")
    else:
        for attempt in range(6):
            try:
                req = urllib.request.Request(IDS_URL, headers={"User-Agent": "anima-h1346"})
                raw = urllib.request.urlopen(req, timeout=180).read()
                break
            except Exception as e:
                wait = min(60, 5 * (2 ** attempt))
                log(f"[ids] fetch attempt {attempt+1}/6 failed: {repr(e)[:120]} -> backoff {wait}s")
                time.sleep(wait)
        else:
            raise RuntimeError("IDS DB fetch exhausted retries")
        with open(cache, "wb") as f:
            f.write(raw)
        log(f"[ids] fetched {len(raw)}B")
    sha = hashlib.sha256(raw).hexdigest()
    log(f"[ids] sha256={sha}")
    ids = {}
    for line in raw.decode("utf-8", errors="ignore").splitlines():
        if not line or line.startswith("#") or line.startswith(";;"):
            continue
        p = line.split("\t")
        if len(p) < 3:
            continue
        ch, decomp = p[1], p[2]
        if ch and ch not in ids:
            ids[ch] = decomp
    log(f"[ids] {len(ids)} entries loaded")
    return ids, sha


def ids_leaves(decomp):
    """One-level component leaves (strip IDC ops, &...; entity refs, [GTKV] tags)."""
    s = re.sub(r"&[^;]+;", "", decomp)
    s = re.sub(r"\[[^\]]*\]", "", s)
    return [c for c in s if c not in IDC and not c.isspace()]


def recursive_leaves(ch, ids_db, max_depth):
    """Expand `ch` to its depth-`max_depth` atomic component frontier. At each
    level, replace a component by its own one-level leaves IF it is a Han char
    present in the DB AND not already atomic (its leaves != [itself]); else keep
    it. Returns the deepest reachable component list (codepoints as chars)."""
    frontier = [ch]
    for _ in range(max_depth):
        nxt = []
        changed = False
        for c in frontier:
            cp = ord(c)
            if not is_han(cp):
                nxt.append(c)
                continue
            d = ids_db.get(c)
            if d is None:
                nxt.append(c)
                continue
            lv = ids_leaves(d)
            # atomic / self-referential (1 leaf == itself) → stop expanding it
            if not lv or (len(lv) == 1 and lv[0] == c):
                nxt.append(c)
                continue
            nxt.extend(lv)
            changed = True
        frontier = nxt
        if not changed:
            break
    return frontier


def build_han_decomp(text, ids_db, max_depth):
    """Han codepoint -> tuple(recursive component-leaf codepoints), NO full-char
    residual. Atomic / absent char -> (cp,) (counted)."""
    decomp = {}
    miss = 0
    total_leaves = 0
    n_dec = 0
    for ch in set(text):
        cp = ord(ch)
        if not is_han(cp):
            continue
        if ids_db.get(ch) is None:
            decomp[cp] = (cp,)
            miss += 1
            continue
        lv = recursive_leaves(ch, ids_db, max_depth)
        if not lv:
            decomp[cp] = (cp,)
            miss += 1
            continue
        decomp[cp] = tuple(ord(c) for c in lv)
        total_leaves += len(decomp[cp])
        if len(decomp[cp]) >= 2 or decomp[cp][0] != cp:
            n_dec += 1
    avg_leaves = (total_leaves / max(1, n_dec)) if n_dec else 0.0
    return decomp, miss, n_dec, avg_leaves


# ── struct-vocab + symbol-stream builders (byte-faithful to H_1324) ───────────
def build_struct_vocab(text, kind, han_decomp):
    extra = set()
    if kind == "hangul":
        for ch in text:
            cp = ord(ch)
            if HANGUL_LO <= cp <= HANGUL_HI:
                for jc in unicodedata.normalize("NFD", ch):
                    extra.add(ord(jc))
    elif kind == "han":
        for ch in text:
            cp = ord(ch)
            if cp in han_decomp:
                for lcp in han_decomp[cp]:
                    extra.add(lcp)
    sorted_extra = sorted(extra)
    return {cp: 256 + i for i, cp in enumerate(sorted_extra)}


def make_raw_stream(win_bytes):
    syms = np.frombuffer(win_bytes, dtype=np.uint8).astype(np.int64)
    depth = np.zeros(len(syms), dtype=np.int64)
    d = 0
    is_cont = (syms >= 0x80) & (syms <= 0xBF)
    for i in range(len(syms)):
        d = d + 1 if is_cont[i] else 0
        depth[i] = d
    nby = np.ones(len(syms), dtype=np.int64)
    return syms, nby, depth, 256


def _spread(total, n):
    if n <= 0:
        return []
    base = total // n
    out = [base] * n
    out[0] += total - base * n
    return out


def syll_nbytes(njamo, blen):
    if njamo == 3:
        return [1, 1, 1] if blen == 3 else _spread(blen, 3)
    if njamo == 2:
        return [blen - 1, 1]
    if njamo == 1:
        return [blen]
    out = [1] * njamo
    out[0] += max(0, blen - njamo)
    return out


def make_struct_stream(text, kind, han_decomp, extra_id, remap=None):
    syms, nby, depth = [], [], []
    d = 0
    for ch in text:
        cp = ord(ch)
        blen = len(ch.encode("utf-8"))
        if kind == "hangul" and HANGUL_LO <= cp <= HANGUL_HI:
            nfd = unicodedata.normalize("NFD", ch)
            nb = syll_nbytes(len(nfd), blen)
            for j, jc in enumerate(nfd):
                sid = extra_id[ord(jc)]
                if remap is not None:
                    sid = remap.get(sid, sid)
                syms.append(sid); nby.append(nb[j])
                d = 0 if j == 0 else d + 1
                depth.append(d)
        elif kind == "han" and cp in han_decomp:
            leaves = han_decomp[cp]
            nb = _spread(blen, len(leaves))
            for j, lcp in enumerate(leaves):
                sid = extra_id[lcp]
                if remap is not None:
                    sid = remap.get(sid, sid)
                syms.append(sid); nby.append(nb[j])
                d = 0 if j == 0 else d + 1
                depth.append(d)
        else:
            for b in ch.encode("utf-8"):
                syms.append(b); nby.append(1)
                d = d + 1 if (0x80 <= b <= 0xBF) else 0
                depth.append(d)
    return (np.asarray(syms, dtype=np.int64),
            np.asarray(nby, dtype=np.int64),
            np.asarray(depth, dtype=np.int64))


# ── mitosis grow-op (PURE NUMPY, byte-faithful to the H_1324 torch _grow_on) ──
def assign_all(centers, X):
    """argmin L2 to centers. centers (K,3), X (n,3) -> owner (n,)."""
    d2 = ((X[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
    return np.argmin(d2, axis=1)


def cell_unigram_heads(Y, owner, K, ntr, vj):
    """Per-cell Laplace unigram P(next|cell). Returns (K, vj)."""
    Hmat = np.full((K, vj), LAPLACE, dtype=np.float64)
    own = owner[:ntr]
    y = Y[:ntr]
    flat = own * vj + y
    np.add.at(Hmat.reshape(-1), flat, 1.0)
    Hmat = Hmat / Hmat.sum(axis=1, keepdims=True)
    return Hmat


def owned_ce(Y, owner, k, ntr, p_row):
    mask = (owner[:ntr] == k)
    if not mask.any():
        return -1.0
    yk = Y[:ntr][mask]
    return float(-np.log(p_row[yk] + 1e-12).mean())


def grow_on(centers, X_tr, Y_tr, ntr, vj, grow_max):
    """Error-targeted Voronoi median-split grow-op. Numpy port byte-faithful to
    H_1324: split the eligible cell of highest local UNIGRAM CE on its max-
    variance axis at the median. Cell PARTITION is unigram-driven (the split
    decision is held IDENTICAL to H_1324 so the partition is comparable); only
    the FINAL scoring head differs (bigram, below)."""
    centers = [list(c) for c in centers]
    while len(centers) < grow_max:
        ct = np.asarray(centers, dtype=np.float64)
        owner = assign_all(ct, X_tr)
        K = len(centers)
        owntr = owner[:ntr]
        owned_n = np.bincount(owntr, minlength=K)
        Hmat = cell_unigram_heads(Y_tr, owner, K, ntr, vj)
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
        var = pts.var(axis=0)
        ax = int(np.argmax(var))
        col = pts[:, ax]
        m = col.shape[0]
        scol = np.sort(col)
        med = scol[m // 2] if m % 2 == 1 else (scol[m // 2 - 1] + scol[m // 2]) / 2.0
        lo_mask = col <= med; hi_mask = col > med
        if int(lo_mask.sum()) == 0 or int(hi_mask.sum()) == 0:
            break
        c_lo = pts[lo_mask].mean(axis=0).tolist()
        c_hi = pts[hi_mask].mean(axis=0).tolist()
        centers = [centers[i] for i in range(len(centers)) if i != pick] + [c_lo, c_hi]
    return centers


def make_feats(syms, depth, vj):
    n = len(syms)
    idx = np.arange(CTX, n - 1)
    last = syms[idx - 1].astype(np.float64) / float(vj)
    second = syms[idx - 2].astype(np.float64) / float(vj)
    cdep = depth[idx - 1].astype(np.float64) / 3.0
    X = np.stack([last, second, cdep], axis=1)
    Y = syms[idx].astype(np.int64)
    Prev = syms[idx - 1].astype(np.int64)   # the BIGRAM context (prev symbol)
    return X, Y, Prev, idx


def score_stream(syms, nby, depth, vj, stride, phase, grow_max):
    """RICHER-HEAD scoring: same grown Voronoi cells as H_1324, but the per-cell
    head is a BIGRAM P(next | cell, prev) with add-λ backoff to the cell unigram.
    CE in nats per ORIGINAL UTF-8 byte (same fair axis)."""
    X, Y, Prev, idx = make_feats(syms, depth, vj)
    NBp = nby[idx]
    sel = np.arange(phase % stride, X.shape[0], stride)
    X, Y, Prev, NBp = X[sel], Y[sel], Prev[sel], NBp[sel]
    order = np.arange(X.shape[0])
    e = order % 2 == 0; o = order % 2 == 1
    Xtr, Ytr, Ptr = X[e], Y[e], Prev[e]
    Xte, Yte, Pte, NBte = X[o], Y[o], Prev[o], NBp[o]
    ntr = Xtr.shape[0]
    centers = grow_on(SEED_CENTERS, Xtr, Ytr, ntr, vj, grow_max)
    ct = np.asarray(centers, dtype=np.float64)
    K = len(centers)
    owner_tr = assign_all(ct, Xtr)
    owner_te = assign_all(ct, Xte)

    # cell unigram (backoff target), Laplace MLE — same as H_1324's head
    Huni = cell_unigram_heads(Ytr, owner_tr, K, ntr, vj)   # (K, vj), normalised

    # cell BIGRAM transition counts: C[cell, prev, next]; estimate
    # P(next | cell, prev) = (count + LAPLACE) / (rowsum + LAPLACE*vj).
    # Build sparse via dict keyed (cell, prev) -> count vector lazily for memory.
    # vj can be ~2k (han) → (K, vj, vj) dense is too big; use dict-of-arrays.
    from collections import defaultdict
    bigram_counts = defaultdict(lambda: np.zeros(vj, dtype=np.float64))
    own = owner_tr[:ntr]
    for c, pv, nx in zip(own, Ptr, Ytr):
        bigram_counts[(int(c), int(pv))][nx] += 1.0

    # score held-out under the bigram head with add-λ backoff to cell unigram
    nll_sum = 0.0
    for c, pv, nx in zip(owner_te, Pte, Yte):
        key = (int(c), int(pv))
        cv = bigram_counts.get(key)
        if cv is None:
            # unseen (cell, prev) context → back off to cell unigram (Laplace MLE)
            p = Huni[int(c), nx]
        else:
            denom = cv.sum() + LAPLACE * vj
            p = (cv[nx] + LAPLACE) / denom
        nll_sum += -np.log(p + 1e-12)
    total_bytes = float(NBte.sum())
    ce = nll_sum / max(total_bytes, 1.0)
    return ce, K, int(ntr), int(Xte.shape[0]), total_bytes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=int, default=30_000_000)
    ap.add_argument("--stride", type=int, default=300)
    ap.add_argument("--grow-max", type=int, default=GROW_MAX)
    ap.add_argument("--max-depth", type=int, default=MAX_DEPTH)
    ap.add_argument("--seeds", default="5346,5347,5348")
    ap.add_argument("--langs", default="ko,zh,ja,en")
    ap.add_argument("--out", default="/tmp/h1346_out")
    ap.add_argument("--cache-dir", default="/tmp/h1346_cache")
    ap.add_argument("--ids-cache", default="/tmp/h1346_cache/ids_cjkvi.txt")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    os.makedirs(args.cache_dir, exist_ok=True)
    seeds = [int(s) for s in args.seeds.split(",")]
    want = args.langs.split(",")

    log("=== H_1346 — XLANG r3: RICHER HEAD (recursive-IDS depth %d + component-BIGRAM, pure numpy CPU) ===" % args.max_depth)
    t0 = time.time()

    need_han = any(k in want for k in ("zh", "ja"))
    ids_db, ids_sha = ({}, "n/a")
    if need_han:
        ids_db, ids_sha = fetch_ids_db(args.ids_cache)

    corpora = {}
    for key, cfg, kind in LANGS:
        if key not in want:
            continue
        cache = os.path.join(args.cache_dir, f"{key}_{args.window}.bytes")
        try:
            win = fetch_window_bytes(cfg, args.window, cache)
        except Exception as e:
            log(f"[corpus] {key} ({cfg}) FETCH FAILED -> DROP honestly: {repr(e)[:160]}")
            continue
        if len(win) < args.window // 2:
            log(f"[corpus] {key} only {len(win)}B (< half window) -> DROP honestly")
            continue
        sha = hashlib.sha256(win).hexdigest()
        text = win.decode("utf-8", errors="ignore")
        corpora[key] = {"bytes": win, "text": text, "kind": kind, "sha256": sha, "nbytes": len(win)}
        log(f"[corpus] {key} kind={kind} {len(win)}B sha256={sha[:16]}…")

    have = list(corpora.keys())
    log(f"[avail] REAL corpora available: {have}")
    han_present = [k for k in have if corpora[k]["kind"] == "han"]
    min_ok = ("ko" in have) and ("en" in have) and (len(han_present) >= 1)
    if not min_ok:
        log("FATAL: minimum (Korean + English + >=1 Han) NOT met from REAL data. STOP.")
        summary = {"id": "H_1346", "STOP": True, "available": have, "reason": "min matrix not met"}
        json.dump(summary, open(os.path.join(args.out, "h1346_summary.json"), "w"), indent=2, ensure_ascii=False)
        sys.exit(3)

    matrix = {}
    for key in have:
        c = corpora[key]
        kind = c["kind"]
        text = c["text"]
        if kind == "han":
            han_decomp, han_miss, ndec, avg_lv = build_han_decomp(text, ids_db, args.max_depth)
        else:
            han_decomp, han_miss, ndec, avg_lv = {}, 0, 0, 0.0
        extra_id = build_struct_vocab(text, kind, han_decomp) if kind in ("hangul", "han") else {}
        vj_struct = 256 + len(extra_id)
        if kind == "han":
            log(f"[{key}] kind=han distinct-Han={len(han_decomp)} component-vocab={len(extra_id)} "
                f"vj_struct={vj_struct} ids-miss={han_miss} decomposed-chars={ndec} avg-leaves={avg_lv:.2f} depth={args.max_depth}")
        else:
            log(f"[{key}] kind={kind} extra-units={len(extra_id)} vj_struct={vj_struct}")
        rec = {"raw": [], "struct": [], "shuf": [], "cells_raw": [], "cells_struct": [],
               "vj_struct": vj_struct, "n_extra": len(extra_id),
               "distinct_han": (len(han_decomp) if kind == "han" else 0),
               "ids_miss": han_miss, "avg_leaves": round(avg_lv, 3)}
        raw_syms, raw_nby, raw_depth, vj_raw = make_raw_stream(c["bytes"])
        for sd in seeds:
            phase = sd % args.stride
            ce_raw, cells_r, ntr, nte, tb = score_stream(
                raw_syms, raw_nby, raw_depth, vj_raw, args.stride, phase, args.grow_max)
            rec["raw"].append(ce_raw); rec["cells_raw"].append(cells_r)
            if kind in ("hangul", "han"):
                s_syms, s_nby, s_depth = make_struct_stream(text, kind, han_decomp, extra_id, remap=None)
                ce_st, cells_s, _, _, _ = score_stream(
                    s_syms, s_nby, s_depth, vj_struct, args.stride, phase, args.grow_max)
                rec["struct"].append(ce_st); rec["cells_struct"].append(cells_s)
                rng = np.random.default_rng(sd)
                ids = sorted(extra_id.values())
                perm = ids[:]; rng.shuffle(perm)
                remap = {old: new for old, new in zip(ids, perm)}
                sh_syms, sh_nby, sh_depth = make_struct_stream(text, kind, han_decomp, extra_id, remap=remap)
                ce_sh, _, _, _, _ = score_stream(
                    sh_syms, sh_nby, sh_depth, vj_struct, args.stride, phase, args.grow_max)
                rec["shuf"].append(ce_sh)
            else:
                rec["struct"].append(ce_raw); rec["cells_struct"].append(cells_r)
                rec["shuf"].append(ce_raw)
            log(f"  [{key} seed {sd}] RAW={rec['raw'][-1]:.5f} STRUCT={rec['struct'][-1]:.5f} "
                f"SHUF={rec['shuf'][-1]:.5f}  cells {rec['cells_raw'][-1]}/{rec['cells_struct'][-1]}")
        matrix[key] = rec

    def mean(x):
        return float(np.mean(x)) if x else float("nan")

    table = {}
    for key in have:
        r = matrix[key]
        raw_m = mean(r["raw"]); st_m = mean(r["struct"]); sh_m = mean(r["shuf"])
        delta = raw_m - st_m
        table[key] = {
            "kind": corpora[key]["kind"], "RAW_CE": round(raw_m, 5), "STRUCT_CE": round(st_m, 5),
            "SHUF_CE": round(sh_m, 5), "Delta": round(delta, 5),
            "delta_vs_shuffle": round(sh_m - st_m, 5),
            "cells_raw": r["cells_raw"], "cells_struct": r["cells_struct"],
            "vj_struct": r["vj_struct"], "n_extra": r["n_extra"],
            "distinct_han": r["distinct_han"], "ids_miss": r["ids_miss"], "avg_leaves": r["avg_leaves"],
            "raw_seeds": [round(x, 5) for x in r["raw"]],
            "struct_seeds": [round(x, 5) for x in r["struct"]],
            "shuf_seeds": [round(x, 5) for x in r["shuf"]],
        }

    d_ko = table["ko"]["Delta"]
    d_en = table["en"]["Delta"]
    han_keys = [k for k in have if corpora[k]["kind"] == "han"]

    h1_each = {k: (table[k]["Delta"] >= 0.05) for k in han_keys}
    H1 = bool(all(h1_each.values()) and len(han_keys) >= 1)
    h2_each = {k: (table[k]["delta_vs_shuffle"] >= 0.05) for k in han_keys}
    H2 = bool(all(h2_each.values()))
    h3_ko = d_ko >= 0.15
    h3_en = abs(d_en) <= 0.02
    H3 = bool(h3_ko and h3_en)

    if H1 and H2 and H3:
        verdict = ("🟢 GREEN — the RICHER (recursive-IDS + component-bigram) head EXTRACTS the Han "
                   "composition signal the flat unigram missed; representation-bind EXTENDS to "
                   "logographic scripts (bounds the H_1318/H_1324 Hangul-specificity to a head-order limit)")
    elif H3 and (not H1):
        verdict = ("🔴/🧱 — even under a RICHER head (recursive multi-level IDS + component-bigram), Han "
                   "composition does NOT help this gradient-free mitosis mechanism; Hangul-specificity "
                   "STRENGTHENED (the flat-unigram negative was NOT a head-order artifact, honest)")
    elif H3 and H1 and (not H2):
        verdict = "🟠 PARTIAL — Han gains under the richer head but does not beat its component shuffle (gain = head capacity, not earned structure)"
    elif not H3:
        verdict = "🔴 PIPELINE-DRIFT — calibration anchors moved under the head change (ko stopped gaining or en gained); investigate, no Han verdict"
    else:
        verdict = "🟠 PARTIAL — per-bar mixed (see H1/H2/H3 per-lang)"

    summary = {
        "id": "H_1346",
        "head": "richer: recursive-IDS depth=%d + per-cell component-BIGRAM (add-λ backoff to cell unigram)" % args.max_depth,
        "window_bytes": args.window, "stride": args.stride, "grow_max": args.grow_max,
        "max_depth": args.max_depth,
        "seeds": seeds, "available_langs": have,
        "dropped_langs": [k for k, _, _ in LANGS if k not in have and k in want],
        "corpus_source": "wikimedia/wikipedia 20231101 via HF datasets-server /rows",
        "ids_source": "CHISE IDS Database (cjkvi/cjkvi-ids ids.txt)", "ids_sha256": ids_sha,
        "sha256": {k: corpora[k]["sha256"] for k in have},
        "matrix": table,
        "Delta_Korean": d_ko, "Delta_English": d_en,
        "Delta_zh": table.get("zh", {}).get("Delta"), "Delta_ja": table.get("ja", {}).get("Delta"),
        "H1_han_gain": H1, "H1_per_lang": {k: bool(v) for k, v in h1_each.items()},
        "H2_earned_vs_shuffle": H2, "H2_per_lang": {k: bool(v) for k, v in h2_each.items()},
        "H3_calibration": H3, "H3_ko_ge_0.15": bool(h3_ko), "H3_en_abs_le_0.02": bool(h3_en),
        "han_langs": han_keys,
        "component_vocab": {k: table[k]["n_extra"] for k in han_keys},
        "avg_leaves": {k: table[k]["avg_leaves"] for k in han_keys},
        "VERDICT": verdict,
        "wall_s": round(time.time() - t0, 1),
    }
    json.dump(summary, open(os.path.join(args.out, "h1346_summary.json"), "w"), indent=2, ensure_ascii=False)

    log("=" * 84)
    log("PER-LANGUAGE MATRIX (3-seed mean, nats per ORIGINAL UTF-8 byte; RICHER bigram head):")
    log(f"  {'lang':5} {'kind':8} {'RAW_CE':>9} {'STRUCT_CE':>10} {'Delta':>9} {'SHUF_CE':>9} {'Δvs-shuf':>9} {'comp-vocab':>10} {'avg-lv':>7}")
    for key in have:
        t = table[key]
        log(f"  {key:5} {t['kind']:8} {t['RAW_CE']:9.5f} {t['STRUCT_CE']:10.5f} {t['Delta']:+9.5f} "
            f"{t['SHUF_CE']:9.5f} {t['delta_vs_shuffle']:+9.5f} {t['n_extra']:10d} {t['avg_leaves']:7.2f}")
    log("-" * 84)
    log(f"Delta_Korean = {d_ko:+.5f}   Delta_English = {d_en:+.5f}")
    log(f"Delta_zh = {table.get('zh',{}).get('Delta')}   Delta_ja = {table.get('ja',{}).get('Delta')}")
    log(f"(H1) HAN-GAIN     zh&ja each Δ>=+0.05: {h1_each} -> {'PASS' if H1 else 'FAIL'}")
    log(f"(H2) EARNED       each Han STRUCT beats SHUFFLE by >=0.05: {h2_each} -> {'PASS' if H2 else 'FAIL'}")
    log(f"(H3) CALIBRATION  ko Δ>=+0.15 [{h3_ko}] AND |en Δ|<=+0.02 [{h3_en}] -> {'PASS' if H3 else 'FAIL'}")
    log("-" * 84)
    log(f"H_1346 VERDICT: {verdict}")
    log(f"available REAL corpora: {have} | IDS sha256={ids_sha}")
    log(f"[done] wall={time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
