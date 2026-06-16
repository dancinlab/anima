#!/usr/bin/env python3
# h1324_xlang_han_ids.py — CROSS-LANGUAGE STRUCTURE MATRIX r2: PROPER IDS HAN DECOMP.
#
# Re-test of the H_1318 wall (a_break_the_wall / c16). H_1318 (🟠 PARTIAL) found the
# Korean ceiling-break is HANGUL-STRUCTURE-specific (English Δ=0, Russian Δ=0; only
# Hangul +0.212, shuffle-earned +0.100). BUT Chinese/Japanese came out NEGATIVE
# (Δ_zh=−1.481, Δ_ja=−1.230) ONLY because the FROZEN Kangxi-radical decomposition kept
# the FULL CHARACTER as a residual symbol → STRUCT vocab exploded to 9327/4738 → the
# tiny per-cell unigram head fragmented. That is a DECOMPOSITION ARTIFACT, not evidence
# that Han composition does not help.
#
# THE FIX (the ONLY change vs h1318_xlang_structure.py): decompose each Han char into
# its IDS (Ideographic Description Sequence) COMPONENT LEAVES — the real structural
# sub-character components — with NO full-char residual token (the bug that broke H_1318)
# and a MODEST component vocabulary. Korean (NFD jamo) + English (no-comp floor) stay in,
# BYTE-IDENTICAL to H_1318, as CALIBRATION ANCHORS so the matrix is directly comparable.
#
# Decomposition SOURCE: CHISE IDS Database (cjkvi/cjkvi-ids ids.txt) — canonical CJK
# component database, 88,937 entries; `U+XXXX<TAB>char<TAB>IDS`. One TOP level, leaves
# only (strip IDC operators ⿰…⿻, entity refs &...;, region tags [GTKV...]); atomic char
# → one component == itself; absent char → atomic fallback (counted). sha256 asserted.
#
# Held BYTE-IDENTICAL to H_1318: gradient-free error-targeted Voronoi mitosis grow-op
# (cells only SPLIT, p8), FROZEN CTX=4 V=256 FEAT_DIM=3 GROW_MAX=40 SPLIT_THRESH_CE=0.05
# MIN_OWNED=8 LAPLACE=1.0 SEED_CENTERS=[[0.3,0.5,0.0],[0.7,0.5,0.5]] even/odd split.
# CE in nats per ORIGINAL raw UTF-8 byte (same fair axis; Σ n_bytes == raw byte count).
#
# REAL corpora ONLY (NO synthetic, p1-p8): wikimedia/wikipedia 20231101 (ko/zh/ja/en)
# via HF datasets-server /rows (SAME source as H_1318; the 30 MB cache was not preserved
# on this host so it is re-fetched from the identical source). HF token via env HF_TOKEN
# read at call time, header-only, NEVER logged/inlined/committed (c7). sha256 per window.
#
# FROZEN-FIRST bars: .verdicts/1324_xlang_han_ids/H_1324_FREEZE.txt (pre-registered,
# NOT moved — c9/p7). H1 HAN-GAIN / H2 EARNED-vs-shuffle / H3 CALIBRATION (ko+en).
#
# SCOPE (a_scale_honest_scope/a_toy_scale_recheck): TOY/DIRECTIONAL numpy/torch mirror;
# CTX=4 3-D Voronoi + per-cell unigram head; one-level (non-recursive) IDS; engine-
# transfer to live CORE/*.hexa = follow-on. NO fluency claim. Live CORE UNTOUCHED.

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

try:
    import torch
    HAVE_TORCH = True
except Exception:
    HAVE_TORCH = False

# ── FROZEN knobs (verbatim from H_1318 / H_1306 / H_1307) ─────────────────────────
CTX = 4
FEAT_DIM = 3
GROW_MAX = 40
SPLIT_THRESH_CE = 0.05
MIN_OWNED = 8
LAPLACE = 1.0
SEED_CENTERS = [[0.3, 0.5, 0.0], [0.7, 0.5, 0.5]]

HANGUL_LO, HANGUL_HI = 0xAC00, 0xD7A3
CJK_LO, CJK_HI = 0x4E00, 0x9FFF          # CJK Unified Ideographs (Han)
CJK_EXT_A_LO, CJK_EXT_A_HI = 0x3400, 0x4DBF

# Ideographic Description Characters (composition operators in the IDS strings).
IDC = set("⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻")

# Matrix languages: (key, wikipedia-config, decompose-kind). Russian DROPPED (pure
# alphabetic control, gained 0.000 in H_1318); ko+en = calibration anchors, zh/ja = test.
LANGS = [
    ("ko", "20231101.ko", "hangul"),   # CALIBRATION anchor (compositional)
    ("zh", "20231101.zh", "han"),      # TEST (logographic compositional)
    ("ja", "20231101.ja", "han"),      # TEST (kanji->IDS components, kana atomic)
    ("en", "20231101.en", "none"),     # CALIBRATION anchor (no-composition floor)
]

IDS_URL = "https://raw.githubusercontent.com/cjkvi/cjkvi-ids/master/ids.txt"


def log(*a):
    print(*a, flush=True)


# ── REAL corpus fetch: HF datasets-server /rows (public; token header-only) ───────
def hf_headers():
    tok = os.environ.get("HF_TOKEN", "")
    h = {"User-Agent": "anima-h1324"}
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
    """Accumulate the `text` column via the HF datasets-server /rows JSON endpoint until
    `window` raw UTF-8 bytes accumulate. Disk/memory-safe (NO shard download). Cached."""
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


# ── PROPER IDS component decomposition (the H_1324 fix) ───────────────────────────
def is_han(cp):
    return (CJK_LO <= cp <= CJK_HI) or (CJK_EXT_A_LO <= cp <= CJK_EXT_A_HI)


def fetch_ids_db(cache):
    """Fetch the CHISE IDS database (cjkvi/cjkvi-ids ids.txt). sha256 asserted/recorded."""
    if os.path.exists(cache) and os.path.getsize(cache) > 1_000_000:
        raw = open(cache, "rb").read()
        log(f"[ids] from cache {cache} ({len(raw)}B)")
    else:
        for attempt in range(6):
            try:
                req = urllib.request.Request(IDS_URL, headers={"User-Agent": "anima-h1324"})
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
    """One TOP level, leaves only: strip IDC operators, entity refs &...;, region tags
    [GTKV...], whitespace. Returns the component-leaf list (chars)."""
    s = re.sub(r"&[^;]+;", "", decomp)
    s = re.sub(r"\[[^\]]*\]", "", s)
    return [c for c in s if c not in IDC and not c.isspace()]


def build_han_decomp(text, ids_db):
    """Han codepoint -> tuple(component-leaf codepoints), NO full-char residual.
    Atomic char (single leaf == self) -> (cp,). Absent char -> atomic fallback (counted)."""
    decomp = {}
    miss = 0
    for ch in set(text):
        cp = ord(ch)
        if not is_han(cp):
            continue
        d = ids_db.get(ch)
        if d is None:
            decomp[cp] = (cp,)   # atomic fallback for absent char (counted)
            miss += 1
            continue
        lv = ids_leaves(d)
        if not lv:
            decomp[cp] = (cp,)
            miss += 1
            continue
        decomp[cp] = tuple(ord(c) for c in lv)
    return decomp, miss


# ── struct-vocab + symbol-stream builders (byte-faithful to H_1318) ───────────────
def build_struct_vocab(text, kind, han_decomp):
    """Distinct extra-unit codepoints (jamo for hangul; IDS component leaves for han)
    -> stable symbol id >= 256 (bytes occupy 0..255)."""
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
                    extra.add(lcp)         # ONLY component leaves — NO full-char residual
    sorted_extra = sorted(extra)
    return {cp: 256 + i for i, cp in enumerate(sorted_extra)}


def make_raw_stream(win_bytes):
    syms = np.frombuffer(win_bytes, dtype=np.uint8).astype(np.int64)
    nby = np.ones(len(syms), dtype=np.int64)
    depth = np.zeros(len(syms), dtype=np.int64)
    d = 0
    is_cont = (syms >= 0x80) & (syms <= 0xBF)
    for i in range(len(syms)):
        d = d + 1 if is_cont[i] else 0
        depth[i] = d
    return syms, nby, depth, 256


def _spread(total, n):
    """Spread `total` bytes across n leaves; first leaf carries the remainder. Σ == total."""
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
    """Emit (syms, nbytes, depth). Hangul syllable -> jamo symbols (BYTE-IDENTICAL to
    H_1318). Han char -> its IDS component-leaf symbols, n_bytes spread so Σ == blen
    (NO full-char residual). Everything else -> one symbol per raw byte. `remap` (dict
    over extra ids) relabels extra symbols for the shuffle control (H2)."""
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
            nb = _spread(blen, len(leaves))   # spread the char's bytes across its leaves
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


# ── mitosis (byte-faithful to H_1318 _grow_on; dim/vocab-agnostic) ────────────────
def _t(dev, x, dt=None):
    if dt is None:
        dt = torch.float64
    return torch.tensor(x, dtype=dt, device=dev)


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
    centers = [list(c) for c in centers]
    while len(centers) < grow_max:
        ct = _t(dev, centers)
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
        col = pts[:, ax]
        m = col.shape[0]
        scol, _ = torch.sort(col)
        med = scol[m // 2].item() if m % 2 == 1 else ((scol[m // 2 - 1] + scol[m // 2]) / 2.0).item()
        lo_mask = col <= med; hi_mask = col > med
        if int(lo_mask.sum().item()) == 0 or int(hi_mask.sum().item()) == 0:
            break
        c_lo = pts[lo_mask].mean(dim=0).cpu().numpy().tolist()
        c_hi = pts[hi_mask].mean(dim=0).cpu().numpy().tolist()
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
    return X, Y, idx


def score_stream(syms, nby, depth, vj, stride, phase, dev, grow_max):
    X, Y, idx = make_feats(syms, depth, vj)
    NBp = nby[idx]
    sel = np.arange(phase % stride, X.shape[0], stride)
    X, Y, NBp = X[sel], Y[sel], NBp[sel]
    order = np.arange(X.shape[0])
    e = order % 2 == 0; o = order % 2 == 1
    Xtr, Ytr, NBtr = X[e], Y[e], NBp[e]
    Xte, Yte, NBte = X[o], Y[o], NBp[o]
    ntr = Xtr.shape[0]
    Xtr_t = _t(dev, Xtr); Ytr_t = _t(dev, Ytr, torch.int64)
    Xte_t = _t(dev, Xte); Yte_t = _t(dev, Yte, torch.int64)
    centers = grow_on(SEED_CENTERS, Xtr_t, Ytr_t, ntr, vj, dev, grow_max)
    ct = _t(dev, centers)
    owner_tr = assign_all(ct, Xtr_t)
    Hmat = all_heads(Ytr_t, owner_tr, len(centers), ntr, vj, dev)
    owner_te = assign_all(ct, Xte_t)
    p = Hmat[owner_te, Yte_t]
    nll = -torch.log(p + 1e-12)
    total_nats = nll.sum().item()
    total_bytes = float(NBte.sum())
    ce = total_nats / max(total_bytes, 1.0)
    return ce, len(centers), int(ntr), int(Xte.shape[0]), total_bytes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=int, default=30_000_000)
    ap.add_argument("--stride", type=int, default=300)
    ap.add_argument("--grow-max", type=int, default=GROW_MAX)
    ap.add_argument("--seeds", default="5324,5325,5326")
    ap.add_argument("--langs", default="ko,zh,ja,en")
    ap.add_argument("--out", default="/tmp/h1324_out")
    ap.add_argument("--cache-dir", default="/tmp/h1324_cache")
    ap.add_argument("--ids-cache", default="/tmp/h1324_cache/ids_cjkvi.txt")
    ap.add_argument("--cpu", action="store_true")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    os.makedirs(args.cache_dir, exist_ok=True)
    seeds = [int(s) for s in args.seeds.split(",")]
    want = args.langs.split(",")

    if not HAVE_TORCH:
        log("FATAL: torch unavailable — this mechanism needs torch (cdist/index_add). STOP.")
        sys.exit(2)
    if args.cpu or not torch.cuda.is_available():
        dev = torch.device("cpu")
        log("=== H_1324 — XLANG r2: PROPER IDS HAN DECOMP (CPU) ===")
    else:
        dev = torch.device("cuda")
        cap = torch.cuda.get_device_capability(0)
        log(f"=== H_1324 — XLANG r2: PROPER IDS HAN DECOMP (sm_{cap[0]}{cap[1]}) ===")
        log(f"device={torch.cuda.get_device_name(0)} torch={torch.__version__}")
        _s = (torch.randn(512, 512, device=dev) @ torch.randn(512, 512, device=dev)).sum().item()
        torch.cuda.synchronize()
        log(f"kernel launch OK (sentinel {_s:.1f})")

    t0 = time.time()

    # ── IDS DB (the proper-decomposition source) ──
    need_han = any(k in want for k in ("zh", "ja"))
    ids_db, ids_sha = ({}, "n/a")
    if need_han:
        ids_db, ids_sha = fetch_ids_db(args.ids_cache)

    # ── pull REAL corpora; DROP any language whose corpus is absent (NO synthetic) ──
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
        summary = {"id": "H_1324", "STOP": True, "available": have, "reason": "min matrix not met"}
        json.dump(summary, open(os.path.join(args.out, "h1324_summary.json"), "w"), indent=2, ensure_ascii=False)
        sys.exit(3)

    matrix = {}
    for key in have:
        c = corpora[key]
        kind = c["kind"]
        text = c["text"]
        han_decomp, han_miss = (build_han_decomp(text, ids_db) if kind == "han" else ({}, 0))
        extra_id = build_struct_vocab(text, kind, han_decomp) if kind in ("hangul", "han") else {}
        vj_struct = 256 + len(extra_id)
        if kind == "han":
            ndec = sum(1 for cp in han_decomp if len(han_decomp[cp]) >= 2 or han_decomp[cp][0] != cp)
            log(f"[{key}] kind=han distinct-Han={len(han_decomp)} component-vocab={len(extra_id)} "
                f"vj_struct={vj_struct} ids-miss={han_miss} decomposed-chars={ndec}")
        else:
            log(f"[{key}] kind={kind} extra-units={len(extra_id)} vj_struct={vj_struct}")
        rec = {"raw": [], "struct": [], "shuf": [], "cells_raw": [], "cells_struct": [],
               "vj_struct": vj_struct, "n_extra": len(extra_id),
               "distinct_han": (len(han_decomp) if kind == "han" else 0),
               "ids_miss": han_miss}
        raw_syms, raw_nby, raw_depth, vj_raw = make_raw_stream(c["bytes"])
        for sd in seeds:
            phase = sd % args.stride
            ce_raw, cells_r, ntr, nte, tb = score_stream(
                raw_syms, raw_nby, raw_depth, vj_raw, args.stride, phase, dev, args.grow_max)
            rec["raw"].append(ce_raw); rec["cells_raw"].append(cells_r)
            if kind in ("hangul", "han"):
                s_syms, s_nby, s_depth = make_struct_stream(text, kind, han_decomp, extra_id, remap=None)
                ce_st, cells_s, _, _, _ = score_stream(
                    s_syms, s_nby, s_depth, vj_struct, args.stride, phase, dev, args.grow_max)
                rec["struct"].append(ce_st); rec["cells_struct"].append(cells_s)
                # H2 shuffle control: permute the extra-symbol id map (per seed, fixed)
                rng = np.random.default_rng(sd)
                ids = sorted(extra_id.values())
                perm = ids[:]; rng.shuffle(perm)
                remap = {old: new for old, new in zip(ids, perm)}
                sh_syms, sh_nby, sh_depth = make_struct_stream(text, kind, han_decomp, extra_id, remap=remap)
                ce_sh, _, _, _, _ = score_stream(
                    sh_syms, sh_nby, sh_depth, vj_struct, args.stride, phase, dev, args.grow_max)
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
            "distinct_han": r["distinct_han"], "ids_miss": r["ids_miss"],
            "raw_seeds": [round(x, 5) for x in r["raw"]],
            "struct_seeds": [round(x, 5) for x in r["struct"]],
            "shuf_seeds": [round(x, 5) for x in r["shuf"]],
        }

    d_ko = table["ko"]["Delta"]
    d_en = table["en"]["Delta"]
    han_keys = [k for k in have if corpora[k]["kind"] == "han"]

    # H1 HAN-GAIN: zh AND ja each Δ >= +0.05
    h1_each = {k: (table[k]["Delta"] >= 0.05) for k in han_keys}
    H1 = bool(all(h1_each.values()) and len(han_keys) >= 1)
    # H2 EARNED: each Han STRUCT beats SHUFFLE by >= +0.05
    h2_each = {k: (table[k]["delta_vs_shuffle"] >= 0.05) for k in han_keys}
    H2 = bool(all(h2_each.values()))
    # H3 CALIBRATION: Korean still gains (>= +0.15) AND English flat (<= +0.02)
    h3_ko = d_ko >= 0.15
    h3_en = d_en <= 0.02
    H3 = bool(h3_ko and h3_en)

    if H1 and H2 and H3:
        verdict = ("🟢 GREEN — proper IDS Han composition GAINS (zh & ja); representation-bind "
                   "EXTENDS to logographic compositional scripts (bounds H_1318 Hangul-specificity "
                   "to the alphabetic/multibyte controls only)")
    elif H3 and (not H1):
        verdict = ("🔴/🧱 — even under PROPER IDS decomposition, Han composition does NOT help this "
                   "gradient-free unigram mechanism (REAL, distinct from the H_1318 artifact); "
                   "Hangul-specificity stands STRONGER")
    elif H3 and H1 and (not H2):
        verdict = "🟠 PARTIAL — Han gains but does not beat its shuffle control (gain not earned by structure)"
    elif not H3:
        verdict = "🔴 PIPELINE-DRIFT — calibration anchors moved (ko stopped gaining or en gained); investigate, no Han verdict"
    else:
        verdict = "🟠 PARTIAL — per-bar mixed (see H1/H2/H3 per-lang)"

    summary = {
        "id": "H_1324",
        "device": (torch.cuda.get_device_name(0) if dev.type == "cuda" else "cpu"),
        "torch": torch.__version__,
        "window_bytes": args.window, "stride": args.stride, "grow_max": args.grow_max,
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
        "H3_calibration": H3, "H3_ko_ge_0.15": bool(h3_ko), "H3_en_le_0.02": bool(h3_en),
        "han_langs": han_keys,
        "component_vocab": {k: table[k]["n_extra"] for k in han_keys},
        "VERDICT": verdict,
        "wall_s": round(time.time() - t0, 1),
    }
    json.dump(summary, open(os.path.join(args.out, "h1324_summary.json"), "w"), indent=2, ensure_ascii=False)

    log("=" * 80)
    log("PER-LANGUAGE MATRIX (3-seed mean, nats per ORIGINAL UTF-8 byte):")
    log(f"  {'lang':5} {'kind':8} {'RAW_CE':>9} {'STRUCT_CE':>10} {'Delta':>9} {'SHUF_CE':>9} {'Δvs-shuf':>9} {'comp-vocab':>10}")
    for key in have:
        t = table[key]
        log(f"  {key:5} {t['kind']:8} {t['RAW_CE']:9.5f} {t['STRUCT_CE']:10.5f} {t['Delta']:+9.5f} "
            f"{t['SHUF_CE']:9.5f} {t['delta_vs_shuffle']:+9.5f} {t['n_extra']:10d}")
    log("-" * 80)
    log(f"Delta_Korean = {d_ko:+.5f}   Delta_English = {d_en:+.5f}")
    log(f"Delta_zh = {table.get('zh',{}).get('Delta')}   Delta_ja = {table.get('ja',{}).get('Delta')}")
    log(f"(H1) HAN-GAIN     zh&ja each Δ>=+0.05: {h1_each} -> {'PASS' if H1 else 'FAIL'}")
    log(f"(H2) EARNED       each Han STRUCT beats SHUFFLE by >=0.05: {h2_each} -> {'PASS' if H2 else 'FAIL'}")
    log(f"(H3) CALIBRATION  ko Δ>=+0.15 [{h3_ko}] AND en Δ<=+0.02 [{h3_en}] -> {'PASS' if H3 else 'FAIL'}")
    log("-" * 80)
    log(f"H_1324 VERDICT: {verdict}")
    log(f"available REAL corpora: {have} | IDS sha256={ids_sha}")
    log(f"[done] wall={time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
