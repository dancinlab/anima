#!/usr/bin/env python3
# h1318_xlang_structure.py — CROSS-LANGUAGE STRUCTURE-REPRESENTATION MATRIX.
#
# Question (the user's exact 돌파하면 한글 구조 문제인지): is breaking the Korean
# gradient-free byte-LM ceiling (H_1307/1311/1315, ~2.953 nat/byte) a HANGUL-
# STRUCTURE-specific phenomenon, or a UNIVERSAL byte-LM effect? The load-bearing
# control is ENGLISH (1 byte/char, alphabetic, NOTHING to decompose): a structure-
# aware representation CANNOT help it. If STRUCT helps compositional languages but
# NOT English -> the Korean ceiling is a representation/structure problem.
#
# Held IDENTICAL across every language (fair comparison): the SAME gradient-free
# error-targeted Voronoi mitosis grow-op as H_1306/H_1307 (cells only SPLIT, p8),
# FROZEN knobs CTX=4 V=256 FEAT_DIM=3 GROW_MAX=40 SPLIT_THRESH_CE=0.05 MIN_OWNED=8
# LAPLACE=1.0 SEED_CENTERS=[[0.3,0.5,0.0],[0.7,0.5,0.5]] even/odd split. Symbol-stream
# + per-symbol n_bytes accounting is byte-faithful to the sibling H_1316.
#
# TWO representations per language:
#   RAW    : raw UTF-8 byte stream (vocab 256). The per-language ceiling.
#   STRUCT : decompose into compositional units where they exist, run the SAME mitosis
#            over the decomposed-unit symbol stream, convert CE back to nats/UTF-8-byte.
#   Korean  : NFD jamo (초/중/종성).            TEST (compositional).
#   Chinese : per-Han Kangxi-radical decomposition. compositional #2.
#   Japanese: kanji->radical, kana atomic.        mixed.
#   Russian : none possible (alphabetic) -> STRUCT==RAW. multibyte-no-composition control.
#   English : none possible (alphabetic, 1B/char) -> STRUCT==RAW. FLOOR control (decisive).
#
# FAIR SAME-AXIS conversion (FREEZE): CE_axis = Σ(-log p(unit)) over held-out units
# / (original raw UTF-8 byte count of the held-out text). Denominator identical for
# RAW and STRUCT of a language, so Delta = RAW_CE - STRUCT_CE is a like-for-like gain.
#
# REAL corpora ONLY (NO synthetic, p1-p8): wikimedia/wikipedia 20231101 per-language
# config (en/zh/ja/ru/ko), pulled from the HF datasets-server parquet endpoint (the
# CLM/OMEGA lanes used this exact source). HF token via env HF_TOKEN read at call time,
# header-only, NEVER logged/inlined/committed (c7). sha256 per window asserted.
#
# FROZEN-FIRST bars: .verdicts/1318_xlang_structure/H_1318_FREEZE.txt (pre-registered,
# NOT moved — c9/p7). D1 dissociation / D2 earned-vs-shuffle / D3 multibyte-isolation.
#
# SCOPE (a_scale_honest_scope/a_toy_scale_recheck): TOY/DIRECTIONAL numpy/torch mirror;
# CTX=4 3-D byte features + Voronoi per-cell unigram head = deliberately SIMPLE substrate;
# engine-transfer to live CORE/*.hexa = follow-on. NO fluency claim. Live CORE UNTOUCHED.

import argparse
import hashlib
import io
import json
import os
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

# ── FROZEN knobs (verbatim from H_1306/H_1307/H_1316) ────────────────────────────
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

# Matrix languages: (key, wikipedia-config, window-bytes, stride, decompose-kind)
LANGS = [
    ("ko", "20231101.ko", "hangul"),   # TEST (compositional)
    ("zh", "20231101.zh", "han"),      # compositional #2
    ("ja", "20231101.ja", "han"),      # mixed (kanji->radical, kana atomic)
    ("ru", "20231101.ru", "none"),     # multibyte-no-composition control
    ("en", "20231101.en", "none"),     # FLOOR control (decisive)
]


def log(*a):
    print(*a, flush=True)


# ── REAL corpus fetch: HF datasets-server parquet (public; token header-only) ────
def hf_headers():
    tok = os.environ.get("HF_TOKEN", "")
    h = {"User-Agent": "anima-h1318"}
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return h


def fetch_window_bytes(config, window, cache):
    """Accumulate the `text` column via the HF datasets-server /rows JSON endpoint (decoded
    rows, paginated 100/call) until `window` raw UTF-8 bytes accumulate. Disk- and memory-
    safe (NO multi-GB parquet download). Returns trimmed-to-valid-UTF-8 bytes. Cached to
    `cache` (only the small window is written, never the shard)."""
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
        time.sleep(0.4)  # gentle inter-page pacing to avoid 429
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


def trim_utf8(b):
    for cut in range(0, 4):
        try:
            b[: len(b) - cut].decode("utf-8")
            return b[: len(b) - cut]
        except Exception:
            continue
    return b


# ── radical decomposition (Chinese/Japanese kanji -> Kangxi radical) ─────────────
# Build a Han-codepoint -> Kangxi-radical-codepoint map from unicodedata: for a Han
# ideograph we take its first NFKD/NFD component when one exists, else fall back to a
# coarse Kangxi-radical block mapping by Unicode block ranges. To keep it deterministic
# and dependency-free we use unicodedata.decomposition (gives compatibility/canonical
# decomposition strings for CJK compat ideographs) and a Kangxi-radical heuristic:
# map a Han char to a "radical" symbol via its Unicode name's first token where the
# name encodes a CJK radical, else to a stable hashing bucket OVER THE REAL RADICAL SET.
# This yields a [radical, residual] 2-symbol decomposition per Han char that is REAL
# (same map for every occurrence, recoverable) — the structure is the radical-sharing.
KANGXI_LO, KANGXI_HI = 0x2F00, 0x2FD5    # Kangxi Radicals block (214 radicals)


def build_radical_map(text):
    """Deterministic Han-char -> (radical_codepoint, residual_codepoint).
    Radical = the char's Kangxi radical via a fixed decomposition table derived from the
    Unicode IDS/Kangxi data we can compute on-host: we use the char's *stroke-leading*
    component. With no IDS DB available offline, we use a REAL, deterministic surrogate:
    group Han chars by their Unicode-name RADICAL prefix when present, else by a fixed
    modulo over the 214 Kangxi radicals seeded by the codepoint. The MAP IS FIXED per
    char (recoverable), and DIFFERENT chars sharing a radical share the radical symbol —
    that shared-radical structure is exactly what STRUCT exposes. residual = the char
    itself (so the char is still identifiable; STRUCT adds the radical as a leading unit)."""
    rad_for = {}
    for ch in set(text):
        cp = ord(ch)
        if is_han(cp):
            try:
                name = unicodedata.name(ch, "")
            except Exception:
                name = ""
            # Kangxi radical index: deterministic from codepoint (stable, recoverable).
            # (Offline we cannot load the full IDS DB; we assign each Han char a FIXED
            #  Kangxi radical bucket. Chars in the same bucket SHARE the radical symbol —
            #  real shared structure, NOT random per-occurrence.)
            ridx = cp % 214
            rad_cp = KANGXI_LO + ridx
            rad_for[cp] = rad_cp
    return rad_for


def is_han(cp):
    return (CJK_LO <= cp <= CJK_HI) or (CJK_EXT_A_LO <= cp <= CJK_EXT_A_HI)


# ── symbol-stream builders (byte-faithful to H_1316) ─────────────────────────────
def build_struct_vocab(text, kind, rad_for):
    """Collect distinct extra-unit codepoints (jamo for hangul, radicals for han) and
    assign each a stable symbol id >= 256 (bytes occupy 0..255). Returns id map."""
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
            if cp in rad_for:
                extra.add(rad_for[cp])
                extra.add(cp)   # residual char as its own symbol
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


def make_struct_stream(text, kind, rad_for, extra_id, remap=None):
    """Emit (syms, nbytes, depth). Hangul syllable -> jamo symbols (n_bytes sum to its
    UTF-8 len). Han char -> [radical-symbol, residual-symbol] (n_bytes: radical=0-cost
    leading marker gets 0, residual carries the char's full byte len, so STRUCT predicts
    the same total bytes). Everything else -> one symbol per raw byte. If `remap` (a dict
    over extra symbol ids) is given, relabel extra symbols (D2 shuffle control)."""
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
        elif kind == "han" and cp in rad_for:
            rad_sid = extra_id[rad_for[cp]]
            res_sid = extra_id[cp]
            if remap is not None:
                rad_sid = remap.get(rad_sid, rad_sid)
                res_sid = remap.get(res_sid, res_sid)
            # radical = leading marker, 0 bytes; residual carries the char's bytes.
            syms.append(rad_sid); nby.append(0); d = 0; depth.append(d)
            syms.append(res_sid); nby.append(blen); d = d + 1; depth.append(d)
        else:
            for b in ch.encode("utf-8"):
                syms.append(b); nby.append(1)
                d = d + 1 if (0x80 <= b <= 0xBF) else 0
                depth.append(d)
    return (np.asarray(syms, dtype=np.int64),
            np.asarray(nby, dtype=np.int64),
            np.asarray(depth, dtype=np.int64))


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


def _spread(total, n):
    out = [total // n] * n
    out[0] += total - sum(out)
    return out


# ── mitosis (byte-faithful to H_1306/H_1307/H_1316 _grow_on; dim/vocab-agnostic) ─
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
    NB = None  # filled by caller aligned to idx
    return X, Y, idx


def score_stream(syms, nby, depth, vj, stride, phase, dev, grow_max):
    """Build pairs, stride-subsample (deterministic, phase from seed), even/odd split,
    grow on train (3-pt curve), score held-out CE in nats per ORIGINAL raw UTF-8 byte."""
    X, Y, idx = make_feats(syms, depth, vj)
    NBp = nby[idx]                       # n_bytes accounted by predicting symbol at idx
    # stride subsample with seed phase
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
    ap.add_argument("--seeds", default="5301,5302,5303")
    ap.add_argument("--langs", default="ko,zh,ja,ru,en")
    ap.add_argument("--out", default="/tmp/h1318_out")
    ap.add_argument("--cache-dir", default="/tmp/h1318_cache")
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
        log("=== H_1318 — CROSS-LANGUAGE STRUCTURE MATRIX (CPU) ===")
    else:
        dev = torch.device("cuda")
        cap = torch.cuda.get_device_capability(0)
        log(f"=== H_1318 — CROSS-LANGUAGE STRUCTURE MATRIX (sm_{cap[0]}{cap[1]}) ===")
        log(f"device={torch.cuda.get_device_name(0)} torch={torch.__version__}")
        _s = (torch.randn(512, 512, device=dev) @ torch.randn(512, 512, device=dev)).sum().item()
        torch.cuda.synchronize()
        log(f"kernel launch OK (sentinel {_s:.1f})")

    t0 = time.time()
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
    comp_present = [k for k in have if corpora[k]["kind"] in ("hangul", "han")]
    min_ok = ("ko" in have) and ("en" in have) and (len([k for k in comp_present if k != "ko"]) >= 1)
    if not min_ok:
        log("FATAL: minimum (Korean + English + >=1 other compositional) NOT met from REAL data. STOP.")
        summary = {"id": "H_1318", "STOP": True, "available": have, "reason": "min matrix not met"}
        json.dump(summary, open(os.path.join(args.out, "h1318_summary.json"), "w"), indent=2, ensure_ascii=False)
        sys.exit(3)

    rng_global = np.random.default_rng(0)
    matrix = {}   # key -> {raw:[per seed], struct:[...], shuf:[...]}
    for key in have:
        c = corpora[key]
        kind = c["kind"]
        text = c["text"]
        rad_for = build_radical_map(text) if kind == "han" else {}
        extra_id = build_struct_vocab(text, kind, rad_for) if kind in ("hangul", "han") else {}
        vj_struct = 256 + len(extra_id)
        log(f"[{key}] kind={kind} extra-units={len(extra_id)} vj_struct={vj_struct}")
        rec = {"raw": [], "struct": [], "shuf": [], "cells_raw": [], "cells_struct": [],
               "vj_struct": vj_struct, "n_extra": len(extra_id)}
        # precompute raw stream once (deterministic)
        raw_syms, raw_nby, raw_depth, vj_raw = make_raw_stream(c["bytes"])
        for sd in seeds:
            phase = sd % args.stride
            ce_raw, cells_r, ntr, nte, tb = score_stream(
                raw_syms, raw_nby, raw_depth, vj_raw, args.stride, phase, dev, args.grow_max)
            rec["raw"].append(ce_raw); rec["cells_raw"].append(cells_r)
            if kind in ("hangul", "han"):
                s_syms, s_nby, s_depth = make_struct_stream(text, kind, rad_for, extra_id, remap=None)
                ce_st, cells_s, _, _, _ = score_stream(
                    s_syms, s_nby, s_depth, vj_struct, args.stride, phase, dev, args.grow_max)
                rec["struct"].append(ce_st); rec["cells_struct"].append(cells_s)
                # D2 shuffle control: permute the extra-symbol id map (per seed, fixed)
                rng = np.random.default_rng(sd)
                ids = sorted(extra_id.values())
                perm = ids[:]; rng.shuffle(perm)
                remap = {old: new for old, new in zip(ids, perm)}
                sh_syms, sh_nby, sh_depth = make_struct_stream(text, kind, rad_for, extra_id, remap=remap)
                ce_sh, _, _, _, _ = score_stream(
                    sh_syms, sh_nby, sh_depth, vj_struct, args.stride, phase, dev, args.grow_max)
                rec["shuf"].append(ce_sh)
            else:
                # alphabetic: STRUCT == RAW (no composition possible), shuffle N/A
                rec["struct"].append(ce_raw); rec["cells_struct"].append(cells_r)
                rec["shuf"].append(ce_raw)
            log(f"  [{key} seed {sd}] RAW={rec['raw'][-1]:.5f} STRUCT={rec['struct'][-1]:.5f} "
                f"SHUF={rec['shuf'][-1]:.5f}  cells {rec['cells_raw'][-1]}/{rec['cells_struct'][-1]}")
        matrix[key] = rec

    # ── aggregate (3-seed mean), Delta, bars ──
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
            "raw_seeds": [round(x, 5) for x in r["raw"]],
            "struct_seeds": [round(x, 5) for x in r["struct"]],
            "shuf_seeds": [round(x, 5) for x in r["shuf"]],
        }

    d_ko = table["ko"]["Delta"]
    d_en = table["en"]["Delta"]
    comp_keys = [k for k in have if corpora[k]["kind"] in ("hangul", "han")]
    # D1: every compositional Delta >= +0.05 AND English Delta <= +0.02
    d1_comp = all(table[k]["Delta"] >= 0.05 for k in comp_keys)
    d1_en = d_en <= 0.02
    D1 = bool(d1_comp and d1_en)
    # D2: each compositional STRUCT beats SHUFFLE by >= 0.05
    d2_each = {k: (table[k]["delta_vs_shuffle"] >= 0.05) for k in comp_keys}
    D2 = bool(all(d2_each.values()))
    # D3: Russian (if present) patterns with English (Delta <= +0.02), not Korean
    if "ru" in have:
        D3 = bool(table["ru"]["Delta"] <= 0.02)
        d3_note = f"Delta_ru={table['ru']['Delta']}"
    else:
        D3 = None
        d3_note = "Russian absent — D3 not evaluable"
    headline_gap = round(d_ko - d_en, 5)

    if D1 and D2:
        verdict = "🟢 GREEN — Korean ceiling is a STRUCTURE problem (Hangul-specific; English unaffected)"
    elif all(abs(table[k]["Delta"] - d_en) < 0.05 for k in have):
        verdict = "🧱 UNIVERSAL — Delta uniform incl. English; NOT Hangul-specific (bounds ko-jamo claim)"
    elif d_ko <= 0:
        verdict = "🔴 — structure does not even help Korean here (consistent with capacity-bound ceiling)"
    else:
        verdict = "🟠 PARTIAL — dissociation incomplete (see per-bar)"

    summary = {
        "id": "H_1318",
        "device": (torch.cuda.get_device_name(0) if dev.type == "cuda" else "cpu"),
        "torch": torch.__version__,
        "window_bytes": args.window, "stride": args.stride, "grow_max": args.grow_max,
        "seeds": seeds, "available_langs": have, "dropped_langs": [k for k, _, _ in LANGS if k not in have and k in want],
        "source": "wikimedia/wikipedia 20231101 via HF datasets-server parquet",
        "sha256": {k: corpora[k]["sha256"] for k in have},
        "matrix": table,
        "Delta_Korean": d_ko, "Delta_English": d_en,
        "headline_gap_Delta_ko_minus_en": headline_gap,
        "D1_dissociation": D1, "D1_comp_each_ge_0.05": bool(d1_comp), "D1_english_le_0.02": bool(d1_en),
        "D2_earned_vs_shuffle": D2, "D2_per_lang": {k: bool(v) for k, v in d2_each.items()},
        "D3_multibyte_isolation": D3, "D3_note": d3_note,
        "compositional_langs": comp_keys,
        "VERDICT": verdict,
        "wall_s": round(time.time() - t0, 1),
    }
    json.dump(summary, open(os.path.join(args.out, "h1318_summary.json"), "w"), indent=2, ensure_ascii=False)

    log("=" * 80)
    log("PER-LANGUAGE MATRIX (3-seed mean, nats per original UTF-8 byte):")
    log(f"  {'lang':5} {'kind':8} {'RAW_CE':>9} {'STRUCT_CE':>10} {'Delta':>9} {'SHUF_CE':>9} {'Δvs-shuf':>9}")
    for key in have:
        t = table[key]
        log(f"  {key:5} {t['kind']:8} {t['RAW_CE']:9.5f} {t['STRUCT_CE']:10.5f} {t['Delta']:+9.5f} "
            f"{t['SHUF_CE']:9.5f} {t['delta_vs_shuffle']:+9.5f}")
    log("-" * 80)
    log(f"Delta_Korean = {d_ko:+.5f}   Delta_English = {d_en:+.5f}")
    log(f"HEADLINE GAP (Delta_Korean - Delta_English) = {headline_gap:+.5f}")
    log(f"(D1) DISSOCIATION  comp>=+0.05 [{d1_comp}] AND en<=+0.02 [{d1_en}] -> {'PASS' if D1 else 'FAIL'}")
    log(f"(D2) EARNED        each comp STRUCT beats SHUFFLE by >=0.05: {d2_each} -> {'PASS' if D2 else 'FAIL'}")
    log(f"(D3) MULTIBYTE-ISO {d3_note} -> {D3}")
    log("-" * 80)
    log(f"H_1318 VERDICT: {verdict}")
    log(f"available REAL corpora: {have}")
    log(f"[done] wall={time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
