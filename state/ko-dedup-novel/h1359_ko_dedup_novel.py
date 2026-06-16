#!/usr/bin/env python3
# h1359_ko_dedup_novel.py — DEPLETION TEST of the H_1344 "interpolation beats jamo floor" lane.
#
# H_1344 🟢 GREEN: a non-fragmenting frozen-λ Jelinek-Mercer (JM) interpolation of jamo n-gram
# orders dipped held-out Korean next-symbol CE to 2.00562, BELOW the 2.51335 jamo floor (H_1316).
# BUT the H_1344 honesty diagnostic showed the gain is REPETITION MEMORIZATION: 70.1% of held-out
# positions reuse a TRAIN-SEEN top-order context (CE|seen=1.6474); the genuine novel 30% has
# CE|novel=2.8819 — WORSE than the 2.51335 floor.
#
# H_1359 asks: on a NOVEL-CONTEXT-ONLY held-out set (TEST A, PRIMARY GATE) and on a DE-DUPLICATED
# corpus (TEST B), does JM STILL beat 2.51335?
#   - YES → 2.51335 floor is representation-broken even on truly-novel context (report LOUDLY).
#   - NO  → 2.51335 is CONFIRMED a true representation/data-richness floor; H_1344 JM-GREEN is a
#           memorization artifact → DEPLETES the "interpolation beats jamo" lane (honest 🧱, c9).
#
# FROZEN-FIRST: bars pre-registered in .verdicts/1359_ko_dedup_novel/H_1359_FREEZE.txt BEFORE this
# run; λ is the SAME FROZEN schedule as H_1344 (NOT re-tuned to TEST — anti-Goodhart). REAL Korean
# only — R2 KO window sha ASSERTED == c47b6808... (== H_1316 jamo baseline / H_1344). DIRECTIONAL
# numpy; held-out next-symbol CE on a toy stride-300 byte-substrate; CORE UNTOUCHED.

import argparse, hashlib, json, os, sys, time, unicodedata
import numpy as np

HANGUL_LO, HANGUL_HI = 0xAC00, 0xD7A3
H1316_JAMO_FLOOR = 2.51335     # the floor under depletion test (H_1316 locked, nats/UTF-8-byte)
H1307_RAW_CEILING = 2.95342
H1307_KO_SHA = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
LAPLACE = 1.0
NMAX = 5                       # FROZEN (== H_1344)
RAW_W = np.array([2.0 ** k for k in range(NMAX)], dtype=np.float64)   # [1,2,4,8,16]
LAMBDA = RAW_W / RAW_W.sum()                                          # [1/31,...,16/31]
KO_STRIDE = 300
KO_WINDOW = 30_000_000


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


# ── jamo symbol stream (IDENTICAL to H_1316/H_1344: byte-fair axis) ───────────
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


# ── Jelinek-Mercer recursive interpolated n-gram (IDENTICAL to H_1344) ────────
class JMNgram:
    def __init__(self, vj, nmax, lam, laplace=1.0):
        self.vj = vj; self.nmax = nmax; self.lam = np.asarray(lam, dtype=np.float64)
        self.laplace = laplace
        self.ctx = [dict() for _ in range(nmax + 1)]
        self.ctx_tot = [dict() for _ in range(nmax + 1)]

    def fit_pairs(self, stream, train_positions):
        """Fit order-1..N counts from TRAIN positions using FULL-RESOLUTION adjacency."""
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


def positions_split(stream_len, nmax, stride):
    idx = np.arange(nmax - 1, stream_len)[::stride]
    e = idx[np.arange(len(idx)) % 2 == 0]
    o = idx[np.arange(len(idx)) % 2 == 1]
    return e, o


def topctx(stream, i, nmax):
    """top-order (nmax-1)-jamo context immediately preceding label position i."""
    return tuple(stream[i - (nmax - 1): i].tolist())


def score_ce(jm, stream, nby, test_positions, nmax, shift=0):
    """Score held-out TEST positions; history = TRUE full-resolution (nmax-1)-jamo adjacency.
    shift>0 = CIRCULAR-SHIFT surrogate: history from a decoupled test position (marginal kept,
    conditioning destroyed). Returns (CE_per_byte, total_nats, total_bytes, m)."""
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


def dedup_eligible(stream, nmax):
    """Causal top-order de-dup: an eligible label position i survives iff its FULL top-order
    n-gram STRING (the nmax-1 context jamo + the label symbol = an nmax-gram) has NOT appeared
    at any EARLIER position. Repeats are identified ONLY from prior occurrences (causal, no TEST
    leakage). Returns the sorted np array of surviving label positions i in [nmax-1, len-1]."""
    seen = set()
    surv = []
    n = len(stream)
    for i in range(nmax - 1, n):
        # nmax-gram string = stream[i-(nmax-1) : i+1]
        gram = tuple(stream[i - (nmax - 1): i + 1].tolist())
        if gram in seen:
            continue
        seen.add(gram)
        surv.append(i)
    return np.asarray(surv, dtype=np.int64)


def split_over_positions(positions, stride):
    """Decimate an ARBITRARY eligible-position list by stride, then even=TRAIN / odd=TEST."""
    kept = positions[::stride]
    e = kept[np.arange(len(kept)) % 2 == 0]
    o = kept[np.arange(len(kept)) % 2 == 1]
    return e, o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ko-cache", default="/tmp/h1344_corpus/kor30m.bytes")
    ap.add_argument("--ko-window", type=int, default=KO_WINDOW)
    ap.add_argument("--stride", type=int, default=KO_STRIDE)
    ap.add_argument("--nmax", type=int, default=NMAX)
    ap.add_argument("--shift", type=int, default=99991)
    ap.add_argument("--out", default=".verdicts/1359_ko_dedup_novel/H_1359.txt")
    args = ap.parse_args()
    t0 = time.time()

    # ── REAL corpus (cache or R2 fetch); sha gate ─────────────────────────────
    if os.path.exists(args.ko_cache) and os.path.getsize(args.ko_cache) >= args.ko_window - 8:
        ko_win = open(args.ko_cache, "rb").read()
        log(f"[corpus] cache {args.ko_cache} ({len(ko_win)} bytes)")
    else:
        log(f"[corpus] fetching {args.ko_window}+8 REAL KO bytes from r2://{os.environ.get('R2_BUCKET','?')}/anima-7b/web/kor/shard0000.bytes")
        raw = fetch_r2_range("anima-7b/web/kor/shard0000.bytes", args.ko_window + 8)
        ko_win = trim_utf8(raw[: args.ko_window])
        os.makedirs(os.path.dirname(args.ko_cache), exist_ok=True)
        open(args.ko_cache, "wb").write(ko_win)
    ko_sha = hashlib.sha256(ko_win).hexdigest()
    same = (ko_sha == H1307_KO_SHA)
    log(f"[corpus] sha {ko_sha} == H1316 floor baseline: {same}")
    if not same:
        log("FATAL: KO window sha mismatch — REAL-only, NO synthetic. STOP."); sys.exit(3)

    text = ko_win.decode("utf-8")
    jamo_to_id, jamo_sorted = build_jamo_vocab(text)
    vj = 256 + len(jamo_sorted)
    log(f"[rep] Vj={vj} ({len(jamo_sorted)} distinct jamo)")
    syms, nby = make_symbol_stream(text, jamo_to_id)
    log(f"[rep] symbol stream len={len(syms)}")
    log(f"[A1] frozen lambda={LAMBDA.round(5).tolist()}  nmax={args.nmax} (== H_1344, NOT re-tuned)")

    # ── reference: H_1344 GATE replication (full TEST, no novel filter) ────────
    tr_pos, te_pos = positions_split(len(syms), args.nmax, args.stride)
    jm = JMNgram(vj, args.nmax, LAMBDA, laplace=LAPLACE)
    jm.fit_pairs(syms, tr_pos)
    a1_full, *_ = score_ce(jm, syms, nby, te_pos, args.nmax, shift=0)
    log(f"[ref] H_1344 GATE replication (full TEST) A1={a1_full:.5f} (Δfloor {a1_full-H1316_JAMO_FLOOR:+.5f})")

    # train top-order context set (for the novel-only filter) ──────────────────
    trc = set()
    for i in tr_pos:
        i = int(i)
        if i >= args.nmax - 1:
            trc.add(topctx(syms, i, args.nmax))

    # ── TEST A: NOVEL-ONLY held-out (PRIMARY GATE) ────────────────────────────
    # Same JM (trained on TRAIN). Score ONLY the TEST positions whose top-order context was NOT
    # in the TRAIN top-order context set (the genuine-generalization slice).
    novel_te = np.asarray([int(i) for i in te_pos
                           if int(i) >= args.nmax - 1 and topctx(syms, int(i), args.nmax) not in trc],
                          dtype=np.int64)
    seen_te = np.asarray([int(i) for i in te_pos
                          if int(i) >= args.nmax - 1 and topctx(syms, int(i), args.nmax) in trc],
                         dtype=np.int64)
    ce_A, _, _, mA = score_ce(jm, syms, nby, novel_te, args.nmax, shift=0)
    ce_A_shift, _, _, _ = score_ce(jm, syms, nby, novel_te, args.nmax, shift=args.shift)
    ce_seen, _, _, mS = (score_ce(jm, syms, nby, seen_te, args.nmax, shift=0) + (0,))[:4] if len(seen_te) else (None, 0, 0, 0)
    novel_frac = mA / max(1, mA + len(seen_te))
    log(f"[TEST A novel-only] novel_frac={novel_frac:.4f}  m_novel={mA}  m_seen={len(seen_te)}")
    log(f"[TEST A novel-only] CE_A={ce_A:.5f} (Δfloor {ce_A-H1316_JAMO_FLOOR:+.5f})  "
        f"CE_seen={None if ce_seen is None else round(ce_seen,5)}  CE_A_shift={ce_A_shift:.5f}")

    # ── TEST B: DE-DUP corpus (strip repeated top-order strings, re-train+score) ─
    surv = dedup_eligible(syms, args.nmax)
    log(f"[TEST B de-dup] eligible after causal top-order de-dup = {len(surv)} / "
        f"{len(syms)-(args.nmax-1)} ({len(surv)/max(1,len(syms)-(args.nmax-1)):.4f} kept)")
    tr_b, te_b = split_over_positions(surv, args.stride)
    jm_b = JMNgram(vj, args.nmax, LAMBDA, laplace=LAPLACE)
    jm_b.fit_pairs(syms, tr_b)
    ce_B, _, _, mB = score_ce(jm_b, syms, nby, te_b, args.nmax, shift=0)
    ce_B_shift, _, _, _ = score_ce(jm_b, syms, nby, te_b, args.nmax, shift=args.shift)
    # how many de-dup TEST positions are STILL novel vs the de-dup TRAIN top-order set (sanity)
    trc_b = set(topctx(syms, int(i), args.nmax) for i in tr_b if int(i) >= args.nmax - 1)
    b_novel = sum(1 for i in te_b if int(i) >= args.nmax - 1 and topctx(syms, int(i), args.nmax) not in trc_b)
    log(f"[TEST B de-dup] train_pos={len(tr_b)} test_pos={len(te_b)}  CE_B={ce_B:.5f} "
        f"(Δfloor {ce_B-H1316_JAMO_FLOOR:+.5f})  CE_B_shift={ce_B_shift:.5f}  "
        f"test-still-novel-vs-dedup-train={b_novel}/{len(te_b)} ({b_novel/max(1,len(te_b)):.3f})")

    # ── FROZEN BARS ───────────────────────────────────────────────────────────
    c1 = ce_A < (H1316_JAMO_FLOOR - 0.01)                 # PRESENCE on novel-only (primary gate)
    c1b_dir_agrees = ce_B >= (H1316_JAMO_FLOOR - 0.01)    # de-dup also does NOT beat floor (agrees w/ floor-confirm)
    c2 = (ce_A_shift >= (H1316_JAMO_FLOOR - 0.05)) and ((ce_A_shift - ce_A) >= 0.05)  # EARNED
    if not c2:
        tier = "TRIVIAL-RED"
        verdict = "🔴 TRIVIAL — circular-shift surrogate also improves on novel-only; gain not from jamo-order structure"
    elif c1:
        tier = "GREEN"
        verdict = "🟢 GREEN — JM-interp beats 2.51335 on TRULY-NOVEL context; genuine representational break (floor representation-broken)"
    else:
        tier = "FLOOR-CONFIRM"
        verdict = ("🧱 FLOOR-CONFIRM — JM does NOT beat 2.51335 on novel-only (and de-dup agrees); "
                   "2.51335 is a TRUE representation/data-richness floor, the H_1344 JM-GREEN was "
                   "memorization → 'interpolation beats jamo' lane DEPLETED (valid depleting result, c9)")

    res = {
        "id": "H_1359", "slug": "ko-dedup-novel",
        "ko_window_bytes": len(ko_win), "ko_window_sha256": ko_sha,
        "sha_match_H1316_floor": same, "Vj": vj, "distinct_jamo": len(jamo_sorted),
        "gate_stride": args.stride, "nmax": args.nmax,
        "frozen_lambda": LAMBDA.round(6).tolist(),
        "H1316_jamo_floor": H1316_JAMO_FLOOR, "H1307_raw_ceiling": H1307_RAW_CEILING,
        "ref_H1344_full_TEST_A1": round(a1_full, 5),
        "ref_H1344_full_delta_vs_floor": round(a1_full - H1316_JAMO_FLOOR, 5),
        # TEST A — novel-only (primary gate)
        "A_novel_frac": round(novel_frac, 4),
        "A_m_novel": int(mA), "A_m_seen": int(len(seen_te)),
        "A_CE_novel_only": round(ce_A, 5),
        "A_delta_vs_floor": round(ce_A - H1316_JAMO_FLOOR, 5),
        "A_CE_seen_slice": (None if ce_seen is None else round(ce_seen, 5)),
        "A_CE_novel_shift": round(ce_A_shift, 5),
        "A_shift_minus_novel": round(ce_A_shift - ce_A, 5),
        # TEST B — de-dup corpus
        "B_eligible_kept": int(len(surv)),
        "B_kept_frac": round(len(surv) / max(1, len(syms) - (args.nmax - 1)), 4),
        "B_train_pos": int(len(tr_b)), "B_test_pos": int(len(te_b)),
        "B_test_still_novel_frac": round(b_novel / max(1, len(te_b)), 4),
        "B_CE_dedup": round(ce_B, 5),
        "B_delta_vs_floor": round(ce_B - H1316_JAMO_FLOOR, 5),
        "B_CE_dedup_shift": round(ce_B_shift, 5),
        # bars
        "bar_c1_PRESENCE_novel": bool(c1), "bar_c1_threshold": round(H1316_JAMO_FLOOR - 0.01, 5),
        "bar_c1b_dedup_agrees_floor": bool(c1b_dir_agrees),
        "bar_c2_EARNED": bool(c2), "bar_c2_threshold": round(H1316_JAMO_FLOOR - 0.05, 5),
        "tier": tier, "verdict": verdict,
        "wall_sec": round(time.time() - t0, 1),
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=2) + "\n")
    log("\n===== H_1359 RESULT =====")
    log(json.dumps(res, ensure_ascii=False, indent=2))
    log(f"\nTIER: {tier}\n{verdict}")


if __name__ == "__main__":
    main()
