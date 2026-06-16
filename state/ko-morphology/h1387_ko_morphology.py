#!/usr/bin/env python3
# h1387_ko_morphology.py — Korean below-jamo NEW ANGLE: does a MORPHOLOGY-AWARE unit (BPE-on-jamo) or a
# LONGER-CONTEXT count-head reduce the novel-context CE below the jamo-floor+0.28 (~2.793) that the 3
# closed Korean levers (representation H_1322 🧱 · interpolation H_1359 🧱 · data-volume H_1368/H_1380 🟠)
# all hit?
#
# H_1380 pinned the novel-context CE asymptote at ~2.747 = jamo floor (2.51335) +0.28 on REAL KO (≤480MB)
# and NAMED two genuinely-new remaining angles (NOT more data/representation-at-jamo): (1) morphology-aware
# units (morpheme / BPE-on-jamo) and (2) cross-syllable long-range deps (nmax>5). H_1387 tests both, with
# BPE-on-jamo as the PRIMARY gating angle and the nmax sweep as a NON-GATING secondary diagnostic.
#
# PRIMARY = BPE-ON-JAMO: learn frequency-ranked merges over the TRAIN jamo stream (de-facto morpheme-ish
# sub-units), re-encode the stream into BPE units, fit the SAME Jelinek-Mercer count-head over BPE units,
# score the NOVEL-only held-out CE in nats/UTF-8-BYTE (byte-fair, the SAME axis as the jamo floor). Each
# BPE unit's total nats is divided by the unit's UTF-8 byte span → confound-fair vs the jamo floor.
# SHUFFLE CONTROL: random equal-COUNT merges (same number, random jamo-bigram pairs) → isolates the
# LINGUISTIC structure of the merges from mere granularity.
#
# FROZEN-FIRST: bars pre-registered in .verdicts/1387_ko_morphology/FREEZE.txt BEFORE this run.
# REAL Korean only — the SAME real shard0000 30MB prefix (sha c47b6808...) as H_1368/H_1380; NO synthetic.
# DIRECTIONAL numpy; toy stride-300 byte-substrate next-symbol CE; CORE UNTOUCHED. $0 CPU.

import argparse, hashlib, json, os, sys, time, unicodedata
from collections import Counter
import numpy as np

HANGUL_LO, HANGUL_HI = 0xAC00, 0xD7A3
H1316_JAMO_FLOOR = 2.51335
H1307_RAW_CEILING = 2.95342
H1368_KO_SHA_30M = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
H1359_NOVEL_CE_30M = 2.88190         # jamo-stream 30MB anchor (bar3)
H1380_RESIDUAL = 0.28
RESIDUAL_CE_TARGET = round(H1316_JAMO_FLOOR + H1380_RESIDUAL, 5)   # 2.79335
GAP_MARGIN = 0.05
RESIDUAL_BEAT = round(RESIDUAL_CE_TARGET - GAP_MARGIN, 5)          # 2.74335
LAPLACE = 1.0
NMAX = 5
RAW_W = np.array([2.0 ** k for k in range(NMAX)], dtype=np.float64)
LAMBDA = RAW_W / RAW_W.sum()
KO_STRIDE = 300
KO_KEY = "anima-7b/web/kor/shard0000.bytes"
BPE_MERGES = 2000
SEEDS = [4387, 4388, 4389]
ANCHOR_TOL = 0.02
NMAX_SWEEP = [5, 7, 9]               # secondary diagnostic (jamo stream)


def log(*a): print(*a, flush=True)


def trim_utf8(b):
    for cut in range(0, 4):
        try:
            b[: len(b) - cut].decode("utf-8"); return b[: len(b) - cut]
        except Exception:
            continue
    return b


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


# ── jamo symbol stream (IDENTICAL byte-fair axis to H_1316/H_1359/H_1368/H_1380) ───────
def build_jamo_vocab(text):
    jset = set()
    for ch in text:
        if HANGUL_LO <= ord(ch) <= HANGUL_HI:
            for jc in unicodedata.normalize("NFD", ch):
                jset.add(ord(jc))
    jamo_sorted = sorted(jset)
    jamo_to_id = {cp: 256 + i for i, cp in enumerate(jamo_sorted)}
    return jamo_to_id, jamo_sorted


def syll_jamo_nbytes(njamo):
    if njamo == 3: return [1, 1, 1]
    if njamo == 2: return [2, 1]
    if njamo == 1: return [3]
    out = [1] * njamo
    out[0] += (3 - njamo) if njamo < 3 else 0
    return out


def make_symbol_stream(text, jamo_to_id):
    """Returns (syms, nby): per-symbol id + per-symbol UTF-8 byte cost (the byte-fair denominator)."""
    syms, nby = [], []
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            nfd = unicodedata.normalize("NFD", ch)
            nb = syll_jamo_nbytes(len(nfd))
            for j, jc in enumerate(nfd):
                syms.append(jamo_to_id[ord(jc)]); nby.append(nb[j])
        else:
            for b in ch.encode("utf-8"):
                syms.append(b); nby.append(1)
    return np.asarray(syms, dtype=np.int64), np.asarray(nby, dtype=np.int64)


# ── Jelinek-Mercer recursive interpolated n-gram (IDENTICAL to H_1344/H_1359/H_1368/H_1380) ─
class JMNgram:
    def __init__(self, vj, nmax, lam, laplace=1.0):
        self.vj = vj; self.nmax = nmax; self.lam = np.asarray(lam, dtype=np.float64)
        self.laplace = laplace
        self.ctx = [dict() for _ in range(nmax + 1)]
        self.ctx_tot = [dict() for _ in range(nmax + 1)]

    def fit_pairs(self, stream, train_positions):
        S = stream
        for i in train_positions:
            i = int(i)
            s = int(S[i])
            for k in range(1, self.nmax + 1):
                if i - (k - 1) < 0:
                    continue
                ctx = tuple(S[i - k + 1: i].tolist()) if k > 1 else ()
                ck = self.ctx[k]; tk = self.ctx_tot[k]
                d = ck.get(ctx)
                if d is None:
                    d = {}; ck[ctx] = d; tk[ctx] = 0
                d[s] = d.get(s, 0) + 1
                tk[ctx] = tk[ctx] + 1
        self._uni_total = self.ctx_tot[1].get((), 0)

    def _phat(self, k, hist):
        if k == 1:
            return None
        ctx = tuple(hist[-(k - 1):]) if k > 1 else ()
        d = self.ctx[k].get(ctx)
        if d is None:
            return None
        tot = self.ctx_tot[k][ctx]
        return d, tot

    def logp_next(self, hist, s):
        uni_d = self.ctx[1].get(())
        uni_tot = self._uni_total
        c1 = (uni_d.get(s, 0) if uni_d else 0)
        p1 = (c1 + self.laplace) / (uni_tot + self.laplace * self.vj)
        mix = self.lam[0] * p1
        for k in range(2, self.nmax + 1):
            r = self._phat(k, hist)
            if r is None:
                pk = self._fallback_phat(k - 1, hist, s, p1)
            else:
                d, tot = r
                pk = d.get(s, 0) / tot if tot > 0 else p1
            mix += self.lam[k - 1] * pk
        return np.log(mix + 1e-300)

    def _fallback_phat(self, k, hist, s, p1):
        while k >= 2:
            r = self._phat(k, hist)
            if r is not None:
                d, tot = r
                return d.get(s, 0) / tot if tot > 0 else p1
            k -= 1
        return p1


def lam_for_nmax(nmax):
    w = np.array([2.0 ** k for k in range(nmax)], dtype=np.float64)
    return w / w.sum()


def positions_split(stream_len, nmax, stride):
    idx = np.arange(nmax - 1, stream_len)[::stride]
    e = idx[np.arange(len(idx)) % 2 == 0]
    o = idx[np.arange(len(idx)) % 2 == 1]
    return e, o


def topctx(stream, i, nmax):
    return tuple(stream[i - (nmax - 1): i].tolist())


def score_ce(jm, stream, nby, test_positions, nmax, shift=0):
    """CE in nats per UTF-8 byte: each scored unit's nats / that unit's UTF-8 byte span."""
    total_nats = 0.0; total_bytes = 0
    m = len(test_positions)
    for j in range(m):
        pos = int(test_positions[j])
        s = int(stream[pos])
        if shift:
            hpos = int(test_positions[(j + shift) % m])
        else:
            hpos = pos
        lo = max(0, hpos - (nmax - 1))
        hist = stream[lo:hpos].tolist()
        lp = jm.logp_next(hist, s)
        total_nats += -lp
        total_bytes += int(nby[pos])
    return total_nats / total_bytes, total_nats, total_bytes, m


def score_stream(syms, nby, vj, nmax, lam, stride, shift):
    """Stride split, fit JM on TRAIN, score NOVEL-ONLY held-out CE (top-order ctx absent from TRAIN
    top-order set) + circular-shift surrogate. SAME novel filter as H_1359 TEST A / H_1368."""
    tr_pos, te_pos = positions_split(len(syms), nmax, stride)
    jm = JMNgram(vj, nmax, lam, laplace=LAPLACE)
    jm.fit_pairs(syms, tr_pos)
    trc = set(topctx(syms, int(i), nmax) for i in tr_pos if int(i) >= nmax - 1)
    novel_te = np.asarray([int(i) for i in te_pos
                           if int(i) >= nmax - 1 and topctx(syms, int(i), nmax) not in trc],
                          dtype=np.int64)
    seen_n = sum(1 for i in te_pos if int(i) >= nmax - 1 and topctx(syms, int(i), nmax) in trc)
    ce_novel, _, _, m_novel = score_ce(jm, syms, nby, novel_te, nmax, shift=0)
    ce_shift, _, _, _ = score_ce(jm, syms, nby, novel_te, nmax, shift=shift)
    novel_frac = m_novel / max(1, m_novel + seen_n)
    return {
        "train_pos": int(len(tr_pos)), "test_pos": int(len(te_pos)),
        "m_novel": int(m_novel), "m_seen": int(seen_n), "novel_frac": round(novel_frac, 4),
        "ce_novel": round(ce_novel, 5), "delta_vs_floor": round(ce_novel - H1316_JAMO_FLOOR, 5),
        "delta_vs_residual": round(ce_novel - RESIDUAL_CE_TARGET, 5),
        "ce_shift": round(ce_shift, 5), "shift_minus_novel": round(ce_shift - ce_novel, 5),
    }


# ── BPE-on-jamo (morphology-aware unit) ────────────────────────────────────────────────
def learn_bpe(base_ids, base_nby, num_merges, rng=None):
    """Learn `num_merges` merges over a sequence of base symbol ids.
    rng=None → FREQUENCY-ranked (real BPE, structure). rng given → RANDOM equal-count merges
    (shuffle control: same number of merges, pairs chosen at RANDOM from observed adjacent pairs).
    Returns the ordered list of (a,b)->new_id merges. We learn on the TRAIN sequence ONLY.

    EFFICIENT incremental BPE — a doubly-linked list over positions with a LIVE adjacent-pair count
    dict; each merge updates only the local neighbors of replaced positions (NOT a full rescan). This
    is the standard fast BPE; the resulting merge order is IDENTICAL to the naive full-rescan version
    (ties broken by (count, pair) max — same as naive)."""
    sym = list(map(int, base_ids))
    N = len(sym)
    if N < 2:
        return []
    nxt = list(range(1, N)) + [-1]     # next live index (-1 = end)
    prv = [-1] + list(range(0, N - 1))  # prev live index
    alive = bytearray([1]) * N          # position still a live chain head?
    pair_counts = Counter()
    pair_pos = {}                       # pair -> set of left-index positions where it currently sits
    for i in range(N - 1):
        pr = (sym[i], sym[i + 1])
        pair_counts[pr] += 1
        pair_pos.setdefault(pr, set()).add(i)
    next_id = max(sym) + 1
    merges = []

    def _add(p, i):
        pair_counts[p] += 1
        pair_pos.setdefault(p, set()).add(i)

    def _rem(p, i):
        if p in pair_pos:
            pair_pos[p].discard(i)
        pair_counts[p] -= 1
        if pair_counts[p] <= 0:
            pair_counts.pop(p, None); pair_pos.pop(p, None)

    for _ in range(num_merges):
        if not pair_counts:
            break
        if rng is None:
            best = max(pair_counts.items(), key=lambda kv: (kv[1], kv[0]))[0]
        else:
            pairs = list(pair_counts.keys())
            best = pairs[int(rng.integers(0, len(pairs)))]
        a, b = best
        nid = next_id; next_id += 1
        merges.append((a, b, nid))
        # ONLY visit the live positions where this pair occurs (not a full scan)
        positions = sorted(pair_pos.get((a, b), set()))
        for i in positions:
            if not alive[i]:
                continue
            j = nxt[i]
            # position may have been invalidated by an adjacent merge earlier in this same loop
            if j == -1 or not alive[j] or sym[i] != a or sym[j] != b:
                continue
            p = prv[i]; k = nxt[j]
            if p != -1:
                _rem((sym[p], sym[i]), p)
            if k != -1:
                _rem((sym[j], sym[k]), j)
            _rem((a, b), i)
            sym[i] = nid
            nxt[i] = k
            if k != -1:
                prv[k] = i
            alive[j] = 0
            if p != -1:
                _add((sym[p], nid), p)
            if k != -1:
                _add((nid, sym[k]), i)
    return merges


def _apply_merges_linked(sym, nby, merges):
    """Apply an ordered merge list to (sym,nby) lists. POSITION-INDEXED — for each merge we visit ONLY
    the live positions where that pair occurs (not a full O(N) scan per merge), the same mechanics as
    learn_bpe. Returns (unit_ids, unit_nby) numpy arrays; merged unit byte = sum of parts (conserved)."""
    N = len(sym)
    if N == 0:
        return np.zeros(0, dtype=np.int64), np.zeros(0, dtype=np.int64)
    sym = list(map(int, sym)); nby = list(map(int, nby))
    nxt = list(range(1, N)) + [-1]
    prv = [-1] + list(range(0, N - 1))
    alive = bytearray([1]) * N
    pair_pos = {}
    for i in range(N - 1):
        pair_pos.setdefault((sym[i], sym[i + 1]), set()).add(i)
    for (a, b, nid) in merges:
        positions = pair_pos.pop((a, b), None)
        if not positions:
            continue
        for i in sorted(positions):
            if not alive[i]:
                continue
            j = nxt[i]
            if j == -1 or not alive[j] or sym[i] != a or sym[j] != b:
                continue
            p = prv[i]; k = nxt[j]
            # drop the two boundary pairs we consume from the index
            if p != -1 and (sym[p], sym[i]) in pair_pos:
                pair_pos[(sym[p], sym[i])].discard(p)
            if k != -1 and (sym[j], sym[k]) in pair_pos:
                pair_pos[(sym[j], sym[k])].discard(j)
            sym[i] = nid; nby[i] = nby[i] + nby[j]
            nxt[i] = k
            if k != -1:
                prv[k] = i
            alive[j] = 0
            # register the two new boundary pairs created by the merged unit
            if p != -1:
                pair_pos.setdefault((sym[p], nid), set()).add(p)
            if k != -1:
                pair_pos.setdefault((nid, sym[k]), set()).add(i)
    out_s = []; out_n = []
    i = 0
    while i != -1 and i < N:
        if alive[i]:
            out_s.append(sym[i]); out_n.append(nby[i])
        i = nxt[i]
    return np.asarray(out_s, dtype=np.int64), np.asarray(out_n, dtype=np.int64)


def apply_bpe(base_ids, base_nby, merges):
    """Apply a learned merge list to a base sequence. Returns (unit_ids, unit_nby)."""
    return _apply_merges_linked(list(map(int, base_ids)), list(map(int, base_nby)), merges)


def bpe_score(jamo_syms, jamo_nby, num_merges, nmax, stride, shift, rng=None):
    """Learn BPE on the TRAIN half of the jamo stream (no test leakage), re-encode the FULL stream
    with those merges, fit JM over BPE units, score NOVEL-only held-out CE (byte-fair)."""
    tr_pos, _ = positions_split(len(jamo_syms), nmax, stride)
    # learn merges on the TRAIN slice of the jamo stream (contiguous up to the last train position)
    train_end = int(tr_pos[-1]) + 1 if len(tr_pos) else len(jamo_syms)
    merges = learn_bpe(jamo_syms[:train_end], jamo_nby[:train_end], num_merges, rng=rng)
    unit_ids, unit_nby = apply_bpe(jamo_syms, jamo_nby, merges)
    vj = int(unit_ids.max()) + 1
    lam = lam_for_nmax(nmax)
    r = score_stream(unit_ids, unit_nby, vj, nmax, lam, stride, shift)
    r["n_merges"] = len(merges)
    r["unit_vocab"] = vj
    r["unit_stream_len"] = int(len(unit_ids))
    r["compression_units_per_jamo"] = round(len(unit_ids) / max(1, len(jamo_syms)), 4)
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ko-cache", default="/tmp/h1380_corpus/kor_big.bytes")
    ap.add_argument("--mb", type=float, default=30.0)
    ap.add_argument("--stride", type=int, default=KO_STRIDE)
    ap.add_argument("--nmax", type=int, default=NMAX)
    ap.add_argument("--merges", type=int, default=BPE_MERGES)
    ap.add_argument("--shift", type=int, default=99991)
    ap.add_argument("--out", default=".verdicts/1387_ko_morphology/result.txt")
    args = ap.parse_args()
    t0 = time.time()

    fetch_bytes = int(args.mb * 1_000_000) + 8
    if os.path.exists(args.ko_cache) and os.path.getsize(args.ko_cache) >= fetch_bytes - 8:
        ko_full = open(args.ko_cache, "rb").read()
        log(f"[corpus] cache {args.ko_cache} ({len(ko_full)} bytes)")
    else:
        log(f"[corpus] fetching {fetch_bytes} REAL KO bytes from r2://{os.environ.get('R2_BUCKET','?')}/{KO_KEY}")
        raw = fetch_r2_range(KO_KEY, fetch_bytes)
        ko_full = trim_utf8(raw)
        os.makedirs(os.path.dirname(args.ko_cache), exist_ok=True)
        open(args.ko_cache, "wb").write(ko_full)

    win = trim_utf8(ko_full[: int(args.mb * 1_000_000)])
    sha = hashlib.sha256(win).hexdigest()
    anchor_sha_ok = (sha == H1368_KO_SHA_30M)
    log(f"[corpus] {args.mb}MB-prefix sha {sha} == H_1368 baseline: {anchor_sha_ok}")
    if not anchor_sha_ok:
        log("FATAL: prefix sha mismatch — corpus drift, REAL-only NO synthetic. STOP."); sys.exit(3)

    text = win.decode("utf-8")
    jamo_to_id, jamo_sorted = build_jamo_vocab(text)
    vj_jamo = 256 + len(jamo_sorted)
    jamo_syms, jamo_nby = make_symbol_stream(text, jamo_to_id)
    log(f"[rep] Vj(jamo)={vj_jamo} ({len(jamo_sorted)} distinct jamo) jamo-stream={len(jamo_syms)}")
    log(f"[A1] frozen lambda(nmax5)={LAMBDA.round(5).tolist()} stride={args.stride} merges={args.merges} (FROZEN)")
    log(f"[target] jamo floor={H1316_JAMO_FLOOR} · +0.28 residual={RESIDUAL_CE_TARGET} · beat-bar (≤)={RESIDUAL_BEAT}")

    # ── BAR 3 CONTROL: jamo floor anchor (jamo stream, nmax5) ────────────────────────────
    jamo_r = score_stream(jamo_syms, jamo_nby, vj_jamo, args.nmax, LAMBDA, args.stride, args.shift)
    anchor_delta = round(abs(jamo_r["ce_novel"] - H1359_NOVEL_CE_30M), 5)
    anchor_ok = anchor_delta <= ANCHOR_TOL
    log(f"[bar3 ANCHOR] jamo novel-CE={jamo_r['ce_novel']} vs {H1359_NOVEL_CE_30M} (|Δ|={anchor_delta} ≤ {ANCHOR_TOL}: {anchor_ok}) "
        f"shift−novel={jamo_r['shift_minus_novel']:+.5f}")

    # ── PRIMARY: BPE-on-jamo (structured, frequency-ranked) ─────────────────────────────
    bpe_r = bpe_score(jamo_syms, jamo_nby, args.merges, args.nmax, args.stride, args.shift, rng=None)
    log(f"[BPE structured] merges={bpe_r['n_merges']} unit_vocab={bpe_r['unit_vocab']} "
        f"units/jamo={bpe_r['compression_units_per_jamo']} novel-CE={bpe_r['ce_novel']} "
        f"(Δfloor {bpe_r['delta_vs_floor']:+.5f}, Δresidual {bpe_r['delta_vs_residual']:+.5f}) "
        f"shift−novel={bpe_r['shift_minus_novel']:+.5f}  [{time.time()-t0:.0f}s]")

    # ── BAR 2 EARNED: shuffle control (random equal-count merges), 3 seeds ───────────────
    shuf_results = []
    for sd in SEEDS:
        rng = np.random.default_rng(sd)
        sr = bpe_score(jamo_syms, jamo_nby, args.merges, args.nmax, args.stride, args.shift, rng=rng)
        sr["seed"] = sd
        shuf_results.append(sr)
        log(f"[BPE shuffle seed={sd}] unit_vocab={sr['unit_vocab']} units/jamo={sr['compression_units_per_jamo']} "
            f"novel-CE={sr['ce_novel']} (Δresidual {sr['delta_vs_residual']:+.5f})  [{time.time()-t0:.0f}s]")
    shuf_ce_mean = round(float(np.mean([r["ce_novel"] for r in shuf_results])), 5)
    structured_gain_over_shuffle = round(shuf_ce_mean - bpe_r["ce_novel"], 5)

    # ── SECONDARY (NON-GATING): longer-context nmax sweep on the jamo stream ─────────────
    nmax_sweep = []
    for nm in NMAX_SWEEP:
        lam = lam_for_nmax(nm)
        r = score_stream(jamo_syms, jamo_nby, vj_jamo, nm, lam, args.stride, args.shift)
        r["nmax"] = nm
        nmax_sweep.append(r)
        log(f"[nmax={nm} jamo] novel-CE={r['ce_novel']} (Δresidual {r['delta_vs_residual']:+.5f}) "
            f"m_novel={r['m_novel']} shift−novel={r['shift_minus_novel']:+.5f}  [{time.time()-t0:.0f}s]")
    nmax_best = min(nmax_sweep, key=lambda r: r["ce_novel"])

    # ── BAR EVALUATION (frozen mapping) ─────────────────────────────────────────────────
    bpe_ce = bpe_r["ce_novel"]
    bar1 = bpe_ce <= RESIDUAL_BEAT
    shuffle_passes_bar1 = shuf_ce_mean <= RESIDUAL_BEAT
    bar2 = (not shuffle_passes_bar1) and (structured_gain_over_shuffle >= 0.03)
    shift_earned = bool(bpe_r["shift_minus_novel"] >= 0.05)
    bar3 = anchor_ok and shift_earned

    log(f"[bar1 GAP-REDUCED] BPE novel-CE={bpe_ce} ≤ {RESIDUAL_BEAT}? → bar1={bar1}")
    log(f"[bar2 EARNED] shuffle mean-CE={shuf_ce_mean} (passes bar1? {shuffle_passes_bar1}) · "
        f"structured gain over shuffle={structured_gain_over_shuffle:+.5f} (≥0.03 req) → bar2={bar2}")
    log(f"[bar3 CONTROL] anchor_ok={anchor_ok} shift_earned={shift_earned} → bar3={bar3}")

    if not bar3:
        tier = "INVALID-RED"
        verdict = (f"🔴 INVALID — bar3 control fail (anchor_ok={anchor_ok}, shift_earned={shift_earned}); "
                   "methodology drift / signal suspect.")
    elif bar1 and bar2:
        tier = "GAP-REDUCED-CANDIDATE"
        verdict = (f"🟢 GAP-REDUCED-CANDIDATE — BPE-on-jamo (morphology-aware unit) novel-CE={bpe_ce} BEATS the "
                   f"jamo-floor+0.28 residual ({RESIDUAL_CE_TARGET}) by ≥{GAP_MARGIN} (≤{RESIDUAL_BEAT}), AND the "
                   f"shuffle control (random equal-count merges) does NOT (mean {shuf_ce_mean}); structured gain "
                   f"over shuffle={structured_gain_over_shuffle:+.5f}. Morphology is a REAL new Korean lever on the "
                   "+0.28 residual the 3 closed levers hit. DIRECTIONAL numpy — engine-transfer UNVERIFIED.")
    elif bar1 and not bar2:
        tier = "COARSER-NOT-MORPHOLOGY"
        verdict = (f"🟠 COARSER-NOT-MORPHOLOGY — BPE-on-jamo novel-CE={bpe_ce} beats the residual ({RESIDUAL_CE_TARGET}), "
                   f"BUT the shuffle control (random merges) ALSO beats it (mean {shuf_ce_mean}) / structured gain "
                   f"{structured_gain_over_shuffle:+.5f} <0.03 → the gain is granularity (a coarser unit), NOT linguistic "
                   "morphology. The morphology CLAIM is not earned (honest, c9).")
    else:
        tier = "RESIDUAL-SURVIVES-MORPHOLOGY"
        sec = (f" The secondary nmax sweep (best nmax={nmax_best['nmax']}, novel-CE={nmax_best['ce_novel']}) "
               f"{'ALSO fails' if nmax_best['ce_novel'] > RESIDUAL_BEAT else 'DOES beat'} the {RESIDUAL_BEAT} bar.")
        depleted = nmax_best["ce_novel"] > RESIDUAL_BEAT
        verdict = (f"🧱 RESIDUAL-SURVIVES-MORPHOLOGY — BPE-on-jamo novel-CE={bpe_ce} does NOT beat the jamo-floor+0.28 "
                   f"residual ({RESIDUAL_CE_TARGET}, bar ≤{RESIDUAL_BEAT}); the +0.28 residual holds under a "
                   f"morphology-aware unit too." + sec +
                   (" → the Korean below-jamo question DEPLETES 🏁: closed across data·representation·interpolation·"
                    "morphology·long-range (clean closure, c9)." if depleted else
                    " → long-range (nmax) remains a live secondary angle."))

    res = {
        "id": "H_1387", "slug": "ko_morphology",
        "window_mb": args.mb, "window_bytes": len(win), "window_sha256": sha, "sha_match_H1368": anchor_sha_ok,
        "primary_angle": "BPE-on-jamo (morphology-aware unit)", "secondary_angle": "longer-context nmax sweep (NON-GATING)",
        "Vj_jamo": vj_jamo, "distinct_jamo": len(jamo_sorted), "gate_stride": args.stride, "nmax": args.nmax,
        "frozen_lambda_nmax5": LAMBDA.round(6).tolist(), "bpe_merges": args.merges, "seeds": SEEDS,
        "H1316_jamo_floor": H1316_JAMO_FLOOR, "H1380_residual": H1380_RESIDUAL,
        "residual_ce_target": RESIDUAL_CE_TARGET, "residual_beat_bar": RESIDUAL_BEAT,
        "H1359_novel_ce_30M_anchor": H1359_NOVEL_CE_30M,
        # CE table
        "jamo_floor_anchor": jamo_r,
        "bpe_structured": bpe_r,
        "bpe_shuffle_seeds": shuf_results,
        "bpe_shuffle_mean_ce": shuf_ce_mean,
        "structured_gain_over_shuffle": structured_gain_over_shuffle,
        "nmax_sweep": nmax_sweep, "nmax_best": {"nmax": nmax_best["nmax"], "ce_novel": nmax_best["ce_novel"]},
        # bars
        "bar1_GAP_REDUCED": bool(bar1), "bar1_bpe_ce": bpe_ce, "bar1_bar": RESIDUAL_BEAT,
        "bar2_EARNED": bool(bar2), "bar2_shuffle_mean_ce": shuf_ce_mean,
        "bar2_shuffle_passes_bar1": bool(shuffle_passes_bar1),
        "bar2_structured_gain_over_shuffle": structured_gain_over_shuffle,
        "bar3_CONTROL": bool(bar3), "bar3_anchor_ok": bool(anchor_ok), "bar3_anchor_abs_delta": anchor_delta,
        "bar3_shift_earned": bool(shift_earned), "bar3_shift_minus_novel": bpe_r["shift_minus_novel"],
        "tier": tier, "verdict": verdict, "wall_sec": round(time.time() - t0, 1),
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=2) + "\n")
    log("\n===== H_1387 RESULT =====")
    log(json.dumps(res, ensure_ascii=False, indent=2))
    log(f"\nTIER: {tier}\n{verdict}")


if __name__ == "__main__":
    main()
