#!/usr/bin/env python3
# h1344_ko_jm_interpolation.py — does a NON-FRAGMENTING frozen-lambda Jelinek-Mercer
# interpolation of jamo-level n-gram ORDERS dip below the 2.51335 jamo floor on held-out
# Korean, or confirm the data-richness floor?
#
# CONTEXT: Korean byte-LM floor 2.95342 (raw byte) -> 2.51335 (NFD jamo, H_1316 GREEN, wired
# H_1321). The 2.51335 floor was reached by a FIXED-CAPACITY gradient-free Voronoi MITOSIS over
# a 3-D context (cannot smoothly back off across orders). Jelinek-Mercer interpolation is the
# classic NON-FRAGMENTING fix: every order's count-MLE is computed on the FULL TRAIN stream (no
# count fragmentation across cells), and a FROZEN lambda mixes them. If higher-order jamo context
# carries exploitable signal beyond the floor -> dip below 2.51335; if data-richness-bound ->
# honest floor-confirm (valid, c9).
#
# FROZEN-FIRST: bars pre-registered in .verdicts/1344_ko_jm_interpolation/H_1344_FREEZE.txt BEFORE
# this run; lambda is FIXED (geometric w_k=2^(k-1), N=5) and NOT tuned to TEST (the anti-Goodhart
# point). REAL Korean only — R2 KO window sha ASSERTED == c47b6808... (== H_1316 jamo baseline).
#
# DIRECTIONAL numpy; held-out next-symbol CE on a toy stride-300 byte-substrate (NOT a fluent
# decoder, NO fluency claim); engine-transfer = follow-on (CORE untouched). a_scale_honest_scope.

import argparse, hashlib, json, os, sys, time, unicodedata
import numpy as np

HANGUL_LO, HANGUL_HI = 0xAC00, 0xD7A3
H1316_JAMO_FLOOR = 2.51335     # the floor this lane must break (H_1316 locked, nats/UTF-8-byte)
H1307_RAW_CEILING = 2.95342    # raw-byte ceiling (reference)
H1307_KO_SHA = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
LAPLACE = 1.0                  # unigram-only Laplace (classic JM: higher orders backed off by interp)
NMAX = 5                       # max jamo n-gram order (FROZEN)
# FROZEN lambda schedule (geometric emphasis, normalized) — pre-registered, NOT tuned to TEST:
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


# ── jamo symbol stream (IDENTICAL to H_1316: byte-fair axis) ──────────────────
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


# ── B3-style no-cheat: roundtrip + byte accounting ────────────────────────────
def roundtrip_and_accounting(text, syms, nby):
    bad = 0; n_syll = 0
    for ch in text:
        if HANGUL_LO <= ord(ch) <= HANGUL_HI:
            n_syll += 1
            nfc = unicodedata.normalize("NFC", unicodedata.normalize("NFD", ch))
            if nfc.encode("utf-8") != ch.encode("utf-8"):
                bad += 1
    return {"hangul_syllables": n_syll, "roundtrip_fail": bad,
            "sum_nbytes": int(nby.sum()), "corpus_bytes": len(text.encode("utf-8"))}


# ── Jelinek-Mercer recursive interpolated n-gram (NON-FRAGMENTING) ────────────
class JMNgram:
    """Order-1..N count-MLE tables on a TRAIN stream, mixed by a FROZEN lambda.

    p_JM(s|h) = sum_{k=1..N} lambda_k * phat_k(s | last (k-1) syms of h)
    phat_1 = Laplace-smoothed unigram (no zeros).  For k>=2, phat_k uses the TRAIN order-k
    counts; if the order-k context was UNSEEN on TRAIN, phat_k recursively falls back to
    phat_{k-1} (standard JM recursive back-off) so every order returns a proper distribution.
    Counts are built on the FULL TRAIN stream per order (NO fragmentation across cells).
    """
    def __init__(self, vj, nmax, lam, laplace=1.0):
        self.vj = vj; self.nmax = nmax; self.lam = np.asarray(lam, dtype=np.float64)
        self.laplace = laplace
        # ctx_counts[k] : dict ctx-tuple(len k-1) -> dict{sym:count}; k=1 ctx = ()
        self.ctx = [dict() for _ in range(nmax + 1)]   # index by order k (1..nmax)
        self.ctx_tot = [dict() for _ in range(nmax + 1)]

    def fit_pairs(self, stream, train_positions):
        """Fit order-1..N counts from TRAIN positions using FULL-RESOLUTION adjacency.
        stream = the FULL undecimated symbol stream (true adjacency).
        train_positions = positions i (label index) selected for TRAIN (held-out split is over
        WHICH positions, NOT over the stream resolution — so each position's (k-1)-history is the
        TRUE immediately-preceding jamo, exactly the H_1316 'last/second sym' adjacency). Each
        train position contributes its order-k context->label count for every k=1..N. Counts are
        built on the FULL stream's adjacency (NO fragmentation)."""
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
        """order-k count-MLE for next-sym dist given history (tuple). Returns dict{sym:prob}
        or None if context unseen (caller falls back). k=1 always returns Laplace unigram."""
        if k == 1:
            return None  # handled specially as a smoothed vector in logp
        ctx = tuple(hist[-(k - 1):]) if k > 1 else ()
        d = self.ctx[k].get(ctx)
        if d is None:
            return None
        tot = self.ctx_tot[k][ctx]
        return d, tot

    def logp_next(self, hist, s):
        """log p_JM(s | hist).  hist = list/array of prior syms (most recent last)."""
        # order-1 Laplace unigram prob for s
        uni_d = self.ctx[1].get(())
        uni_tot = self._uni_total
        c1 = (uni_d.get(s, 0) if uni_d else 0)
        p1 = (c1 + self.laplace) / (uni_tot + self.laplace * self.vj)
        # recursive interpolation: p_k_mix = sum_{j<=k} ... but we use the per-order phat with
        # recursive fallback to lower order when context unseen.
        mix = self.lam[0] * p1
        for k in range(2, self.nmax + 1):
            r = self._phat(k, hist)
            if r is None:
                # unseen order-k context -> fall back to the order-(k-1) MIXED estimate.
                # Use the highest seen order's count-MLE; recurse downward.
                pk = self._fallback_phat(k - 1, hist, s, p1)
            else:
                d, tot = r
                pk = d.get(s, 0) / tot if tot > 0 else p1
            mix += self.lam[k - 1] * pk
        return np.log(mix + 1e-300)

    def _fallback_phat(self, k, hist, s, p1):
        """recursive back-off: return the order-k count-MLE prob for s, falling to lower order
        (down to the Laplace unigram p1) when a context is unseen."""
        while k >= 2:
            r = self._phat(k, hist)
            if r is not None:
                d, tot = r
                return d.get(s, 0) / tot if tot > 0 else p1
            k -= 1
        return p1


def positions_split(stream_len, nmax, stride):
    """The held-out split is over WHICH label positions (NOT over the stream resolution — the
    full-resolution adjacency is always preserved). Positions = label index i in [nmax-1, len-1];
    decimate by stride, then even index = TRAIN, odd index = TEST (the H_1316 even/odd@stride
    construction, but the n-gram context at each kept position is the TRUE adjacent jamo)."""
    idx = np.arange(nmax - 1, stream_len)[::stride]
    e = idx[np.arange(len(idx)) % 2 == 0]
    o = idx[np.arange(len(idx)) % 2 == 1]
    return e, o


def score_ce(jm, stream, nby, test_positions, nmax, shift=0):
    """Score held-out TEST positions; history = TRUE full-resolution (nmax-1)-jamo adjacency.
    shift>0 = CIRCULAR-SHIFT surrogate (A2c): the history is taken from a position circularly
    shifted by `shift` within the TEST set, so each next-sym is scored against a DECOUPLED jamo
    history (true marginal kept, true conditioning destroyed). Returns CE_per_byte."""
    total_nats = 0.0; total_bytes = 0
    m = len(test_positions)
    for j in range(m):
        pos = int(test_positions[j])
        s = int(stream[pos])                       # true label at this test position
        if shift:
            hpos = int(test_positions[(j + shift) % m])  # history from a decoupled test position
        else:
            hpos = pos
        lo = max(0, hpos - (nmax - 1))
        hist = stream[lo:hpos].tolist()
        lp = jm.logp_next(hist, s)
        total_nats += -lp
        total_bytes += int(nby[pos])
    return total_nats / total_bytes, total_nats, total_bytes, m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ko-cache", default="/tmp/h1344_corpus/kor30m.bytes")
    ap.add_argument("--ko-window", type=int, default=KO_WINDOW)
    ap.add_argument("--stride", type=int, default=KO_STRIDE)
    ap.add_argument("--nmax", type=int, default=NMAX)
    ap.add_argument("--shift", type=int, default=99991)  # circular-shift offset for A2c
    ap.add_argument("--dense-stride", type=int, default=6)        # NON-GATING density diagnostic
    ap.add_argument("--dense-test-cap", type=int, default=80000)  # bound dense TEST scoring loop
    ap.add_argument("--out", default=".verdicts/1344_ko_jm_interpolation/H_1344.txt")
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
    acct = roundtrip_and_accounting(text, syms, nby)
    log(f"[no-cheat] syllables={acct['hangul_syllables']} roundtrip_fail={acct['roundtrip_fail']} "
        f"sum_nbytes={acct['sum_nbytes']} corpus_bytes={acct['corpus_bytes']} "
        f"match={acct['sum_nbytes']==acct['corpus_bytes']}")

    # ── GATING arm: stride=300 held-out split (byte-fair to the 2.51335 floor) ────
    # The split is over WHICH label positions are train/test; each kept position's n-gram history
    # is the TRUE full-resolution adjacent jamo (NOT a decimated/fake context — that was the bug
    # the floor's mitosis never had: H_1316 conditions on the real last/second adjacent symbol).
    def run_arm(stride, label, cap=None):
        tr_pos, te_pos = positions_split(len(syms), args.nmax, stride)
        if cap is not None and len(te_pos) > cap:
            # bound TEST scoring cost (Python loop); TRAIN counts keep full density for repeats.
            te_pos = te_pos[:cap]
        log(f"[{label}] split stride={stride} train_pos={len(tr_pos)} test_pos={len(te_pos)}")
        jm = JMNgram(vj, args.nmax, LAMBDA, laplace=LAPLACE)
        jm.fit_pairs(syms, tr_pos)
        a1, *_ = score_ce(jm, syms, nby, te_pos, args.nmax, shift=0)
        a2, *_ = score_ce(jm, syms, nby, te_pos, args.nmax, shift=args.shift)
        jm0 = JMNgram(vj, args.nmax, np.array([1.0] + [0.0] * (args.nmax - 1)), laplace=LAPLACE)
        jm0.fit_pairs(syms, tr_pos)
        a0, *_ = score_ce(jm0, syms, nby, te_pos, args.nmax, shift=0)
        log(f"[{label}] A0_unigram={a0:.5f}  A1_JM={a1:.5f} (Δfloor {a1 - H1316_JAMO_FLOOR:+.5f})  A2c_shift={a2:.5f}")
        return {"stride": stride, "train_pos": int(len(tr_pos)), "test_pos": int(len(te_pos)),
                "A0_unigram_ce": round(a0, 5), "A1_jm_interp_ce": round(a1, 5),
                "A2c_circshift_ce": round(a2, 5)}

    log(f"[A1] frozen lambda={LAMBDA.round(5).tolist()}  nmax={args.nmax}")
    gate = run_arm(args.stride, "GATE@stride300")          # byte-fair to the floor
    a0_ce = gate["A0_unigram_ce"]; a1_ce = gate["A1_jm_interp_ce"]; a2_ce = gate["A2c_circshift_ce"]

    # ── HONESTY diagnostic (NON-GATING): split the gate TEST by whether its top-order context was
    # SEEN in train. The corpus is repetitive web text; a high-order n-gram MEMORIZES repeated
    # strings. This separates (i) the memorized-repetition slice from (ii) the genuine
    # novel-context generalization slice, so the GREEN is reported with full provenance (c9). ──
    def context_split_diag(stride):
        tr_pos, te_pos = positions_split(len(syms), args.nmax, stride)
        jm = JMNgram(vj, args.nmax, LAMBDA, laplace=LAPLACE)
        jm.fit_pairs(syms, tr_pos)
        trc = set(tuple(syms[int(i) - (args.nmax - 1): int(i)].tolist()) for i in tr_pos if int(i) >= args.nmax - 1)
        seen_n = seen_b = 0; nov_n = nov_b = 0; n_seen = n_nov = 0
        for i in te_pos:
            i = int(i)
            if i < args.nmax - 1: continue
            ctx = tuple(syms[i - (args.nmax - 1): i].tolist())
            s = int(syms[i]); lp = jm.logp_next(syms[max(0, i - (args.nmax - 1)):i].tolist(), s)
            if ctx in trc:
                seen_n += -lp; seen_b += int(nby[i]); n_seen += 1
            else:
                nov_n += -lp; nov_b += int(nby[i]); n_nov += 1
        return {"seen_frac": round(n_seen / max(1, n_seen + n_nov), 4),
                "ce_seen_ctx": round(seen_n / max(1, seen_b), 5) if seen_b else None,
                "ce_novel_ctx": round(nov_n / max(1, nov_b), 5) if nov_b else None,
                "n_seen": n_seen, "n_novel": n_nov}
    ctxdiag = context_split_diag(args.stride)
    log(f"[honesty] top-order context SEEN-in-train frac={ctxdiag['seen_frac']}  "
        f"CE|seen={ctxdiag['ce_seen_ctx']}  CE|novel={ctxdiag['ce_novel_ctx']}")

    # ── NON-GATING density diagnostic (a_break_the_wall): give JM its genuine chance with enough
    # data for higher orders to repeat. stride=6 = ~50x denser than the stride-300 gate (≈2M train
    # positions; higher-order jamo contexts now actually recur). This is NOT byte-fair to the
    # stride-300 floor (different density), so it does NOT gate — it only tells us whether the floor
    # is an INVESTMENT artifact (too little train data) or a genuine data-richness floor. TEST is
    # capped to bound the Python scoring loop; TRAIN counts keep full stride-6 density. ──
    dense = run_arm(args.dense_stride, "DENSE", cap=args.dense_test_cap)

    # ── BARS (GATING uses ONLY the stride-300 byte-fair arm + frozen lambda) ──────
    c1 = a1_ce < (H1316_JAMO_FLOOR - 0.01)        # PRESENCE: beats floor by >=0.01
    c2 = a2_ce >= (H1316_JAMO_FLOOR - 0.05)        # EARNED: surrogate does NOT also beat floor
    a1_beats_a2 = (a2_ce - a1_ce) >= 0.05
    if c1 and c2:
        tier = "GREEN"; verdict = "🟢 GREEN — JM-interp dips below the 2.51335 jamo floor; gain is earned (surrogate does not)"
    elif not c1:
        tier = "FLOOR-HONEST"; verdict = "🧱 HONEST-FLOOR — JM-interp does NOT beat 2.51335; data-richness floor confirmed (valid, c9)"
    else:  # c1 true but c2 false
        tier = "TRIVIAL-RED"; verdict = "🔴 TRIVIAL — A1 beats floor but circular-shift surrogate ALSO does; gain not from jamo-order structure"

    res = {
        "id": "H_1344", "slug": "ko-jm-interpolation",
        "ko_window_bytes": len(ko_win), "ko_window_sha256": ko_sha,
        "sha_match_H1316_floor": same, "Vj": vj, "distinct_jamo": len(jamo_sorted),
        "gate_stride": args.stride, "nmax": args.nmax,
        "frozen_lambda": LAMBDA.round(6).tolist(),
        "no_cheat": acct,
        "H1316_jamo_floor": H1316_JAMO_FLOOR, "H1307_raw_ceiling": H1307_RAW_CEILING,
        "GATE_arm": gate,           # byte-fair stride-300 (the gating numbers)
        "DENSE_arm": dense,         # NON-GATING density diagnostic (stride-6, higher-order data)
        "context_seen_diag": ctxdiag,  # NON-GATING: memorized-repetition vs novel-context slice
        "A0_unigram_ce": round(a0_ce, 5),
        "A1_jm_interp_ce": round(a1_ce, 5),
        "A1_delta_vs_floor": round(a1_ce - H1316_JAMO_FLOOR, 5),
        "A2c_circshift_ce": round(a2_ce, 5),
        "A2c_delta_vs_floor": round(a2_ce - H1316_JAMO_FLOOR, 5),
        "A1_beats_A2c_by": round(a2_ce - a1_ce, 5),
        "DENSE_A1_delta_vs_floor": round(dense["A1_jm_interp_ce"] - H1316_JAMO_FLOOR, 5),
        "bar_c1_PRESENCE": bool(c1), "bar_c1_threshold": round(H1316_JAMO_FLOOR - 0.01, 5),
        "bar_c2_EARNED": bool(c2), "bar_c2_threshold": round(H1316_JAMO_FLOOR - 0.05, 5),
        "a1_beats_a2_by_0.05": bool(a1_beats_a2),
        "tier": tier, "verdict": verdict,
        "wall_sec": round(time.time() - t0, 1),
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=2) + "\n")
    log("\n===== H_1344 RESULT =====")
    log(json.dumps(res, ensure_ascii=False, indent=2))
    log(f"\nTIER: {tier}\n{verdict}")


if __name__ == "__main__":
    main()
