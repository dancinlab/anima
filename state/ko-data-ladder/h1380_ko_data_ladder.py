#!/usr/bin/env python3
# h1380_ko_data_ladder.py — EXTEND the Korean data-richness ladder PAST 30MB.
#
# H_1368 (ko-data-richness) showed the NOVEL-context CE is still DESCENDING at 30MB on a ladder of
# PREFIX sub-windows of r2://.../anima-7b/web/kor/shard0000.bytes (3.75/7.5/15/30MB →
# 3.15254/3.07077/2.95376/2.88190; gap to the 2.51335 jamo floor shrank 42% over 8x; log-linear
# b=-0.0929/doubling, r2=0.992 → ~470MB to TOUCH the floor; power-law c_inf UNDETERMINED, c9).
# It left NEXT-1: extend the ladder past 30MB to pin the asymptote vs 2.51335.
#
# H_1380 fetches LARGER PREFIXES of the SAME real shard0000 (10.5GB of REAL Korean, HEAD-verified) and
# adds 60/120/240/480MB rungs (and beyond if still descending). The 30MB rung is the EXACT H_1368
# window (sha c47b6808...) and MUST reproduce novel-CE=2.88190 (|Δ|≤0.02) as a methodology-drift
# anchor. It re-uses the H_1368 jamo representation, FROZEN Jelinek-Mercer λ (nmax=5), NOVEL-only
# held-out filter, and circular-shift surrogate VERBATIM (NOT re-tuned per rung — anti-Goodhart).
# It ALSO re-measures the jamo floor on the extended corpus (bar 4 sanity — should stay ~constant).
#
# FROZEN-FIRST: bars pre-registered in .verdicts/1380_ko_data_ladder/FREEZE.txt BEFORE this run.
# REAL Korean only — prefixes of the SAME real shard0000 used by H_1368; NO synthetic padding.
# DIRECTIONAL numpy; toy stride-300 byte-substrate next-symbol CE; CORE UNTOUCHED. $0 CPU.

import argparse, hashlib, json, os, sys, time, unicodedata
import numpy as np

HANGUL_LO, HANGUL_HI = 0xAC00, 0xD7A3
H1316_JAMO_FLOOR = 2.51335     # the floor under test (H_1316 locked, nats/UTF-8-byte)
H1307_RAW_CEILING = 2.95342
H1368_KO_SHA_30M = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"  # 30MB window sha
H1359_NOVEL_CE_30M = 2.88190   # H_1359/H_1368 TEST A novel-only CE at 30MB (anchor)
LAPLACE = 1.0
NMAX = 5                       # FROZEN (== H_1344/H_1359/H_1368)
RAW_W = np.array([2.0 ** k for k in range(NMAX)], dtype=np.float64)   # [1,2,4,8,16]
LAMBDA = RAW_W / RAW_W.sum()                                          # [1/31,...,16/31]
KO_STRIDE = 300
KO_KEY = "anima-7b/web/kor/shard0000.bytes"
# EXTENDED ladder: 30MB (H_1368 anchor) + new rungs past 30MB.
LADDER_MB = [30.0, 60.0, 120.0, 240.0, 480.0]
ANCHOR_TOL = 0.02


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


# ── jamo symbol stream (IDENTICAL to H_1316/H_1344/H_1359/H_1368: byte-fair axis) ────
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


# ── Jelinek-Mercer recursive interpolated n-gram (IDENTICAL to H_1344/H_1359/H_1368) ─
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


def positions_split(stream_len, nmax, stride):
    idx = np.arange(nmax - 1, stream_len)[::stride]
    e = idx[np.arange(len(idx)) % 2 == 0]
    o = idx[np.arange(len(idx)) % 2 == 1]
    return e, o


def topctx(stream, i, nmax):
    return tuple(stream[i - (nmax - 1): i].tolist())


def score_ce(jm, stream, nby, test_positions, nmax, shift=0):
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


def score_rung(syms, nby, vj, nmax, stride, shift):
    """One ladder rung: stride split, fit JM on TRAIN, score NOVEL-ONLY held-out CE (top-order
    context not in TRAIN top-order set), + circular-shift surrogate. IDENTICAL novel-filter as
    H_1359 TEST A / H_1368."""
    tr_pos, te_pos = positions_split(len(syms), nmax, stride)
    jm = JMNgram(vj, nmax, LAMBDA, laplace=LAPLACE)
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
        "ce_shift": round(ce_shift, 5), "shift_minus_novel": round(ce_shift - ce_novel, 5),
    }


def measure_jamo_floor(syms, nby, vj, nmax, stride):
    """bar 4 sanity: re-measure the jamo floor (full-fit JM next-symbol CE over ALL gate positions,
    NO novel-filter) on this corpus — the floor reference under H_1316 is the in-distribution count-MLE
    CE. It should stay ~constant (≈2.51335) as the window grows. (We fit on TRAIN, score the gate set
    in-distribution — i.e. WITHOUT the novel-only restriction, which is the floor definition.)"""
    tr_pos, te_pos = positions_split(len(syms), nmax, stride)
    jm = JMNgram(vj, nmax, LAMBDA, laplace=LAPLACE)
    jm.fit_pairs(syms, tr_pos)
    ce_all, _, _, m = score_ce(jm, syms, nby, te_pos, nmax, shift=0)
    return round(ce_all, 5), int(m)


def fit_asymptote(windows_bytes, ces):
    """Two pre-registered asymptote estimators (windows in bytes, ces nats/byte) — IDENTICAL to
    H_1368 including the reliability guardrail."""
    W = np.asarray(windows_bytes, dtype=np.float64)
    y = np.asarray(ces, dtype=np.float64)
    out = {}
    x = np.log2(W)
    A = np.vstack([np.ones_like(x), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    a, b = float(coef[0]), float(coef[1])
    yhat = A @ coef
    ss_res = float(np.sum((y - yhat) ** 2)); ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2_log = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    out["log_fit"] = {"a": round(a, 5), "b_slope_per_log2W": round(b, 5), "r2": round(r2_log, 5)}
    best = None
    for p in np.linspace(0.02, 2.0, 199):
        z = W ** (-p)
        Az = np.vstack([np.ones_like(z), z]).T
        cf, *_ = np.linalg.lstsq(Az, y, rcond=None)
        yh = Az @ cf
        rss = float(np.sum((y - yh) ** 2))
        if best is None or rss < best[0]:
            best = (rss, float(cf[0]), float(cf[1]), float(p))
    rss, c_inf, amp, p = best
    r2_pow = 1.0 - rss / ss_tot if ss_tot > 0 else float("nan")
    # RELIABILITY GUARDRAIL (anti-tune-to-green, c9) — IDENTICAL to H_1368.
    p_edge = (p <= 0.025) or (p >= 1.99)
    implausible = c_inf < (H1316_JAMO_FLOOR - 0.20)
    reliable = not (p_edge or implausible)
    out["power_fit"] = {"c_inf": round(c_inf, 5), "amp": round(amp, 5), "p": round(p, 4),
                        "r2": round(r2_pow, 5), "p_at_grid_edge": bool(p_edge),
                        "c_inf_implausible_below_floor": bool(implausible),
                        "reliable": bool(reliable)}
    out["c_inf_estimate"] = round(c_inf, 5)
    out["asymptote_reliable"] = bool(reliable)
    return out


def classify_asymptote(c_inf, reliable, lowest_ce):
    """Bar 2 decision rule (frozen). BELOW reinforced if the lowest measured rung is itself ≤ floor."""
    floor = H1316_JAMO_FLOOR
    if not reliable:
        return ("STILL-DESCENDING-UNRESOLVED",
                "finite-rung power-law extrapolation under-constrained (implausible c_inf and/or p "
                "pinned at grid edge) — descent is real but the asymptote cannot be pinned; honest "
                "INCOMPLETE, report the log-linear extrapolation as a PREDICTION (c9)")
    if c_inf < floor - 0.01:
        return ("BELOW",
                f"representation lever REOPENS via data (reliable asymptote {c_inf} below 2.51335)")
    if c_inf <= floor + 0.01:
        return ("AT", "floor is the data-richness limit (asymptote ≈ 2.51335) — terminal across data")
    return ("ABOVE", "data-richness floor is REAL above the jamo floor (data narrows the gap)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ko-cache", default="/tmp/h1380_corpus/kor_big.bytes")
    ap.add_argument("--max-mb", type=float, default=480.0,
                    help="max ladder window to attempt (fetched + measured)")
    ap.add_argument("--stride", type=int, default=KO_STRIDE)
    ap.add_argument("--nmax", type=int, default=NMAX)
    ap.add_argument("--shift", type=int, default=99991)
    ap.add_argument("--out", default=".verdicts/1380_ko_data_ladder/result.txt")
    args = ap.parse_args()
    t0 = time.time()

    ladder = [mb for mb in LADDER_MB if mb <= args.max_mb + 1e-9]
    fetch_bytes = int(max(ladder) * 1_000_000) + 8

    # ── REAL corpus (cache or R2 fetch of the LARGEST prefix needed) ──────────────
    if os.path.exists(args.ko_cache) and os.path.getsize(args.ko_cache) >= fetch_bytes - 8:
        ko_full = open(args.ko_cache, "rb").read()
        log(f"[corpus] cache {args.ko_cache} ({len(ko_full)} bytes)")
    else:
        log(f"[corpus] fetching {fetch_bytes} REAL KO bytes from r2://{os.environ.get('R2_BUCKET','?')}/{KO_KEY}")
        raw = fetch_r2_range(KO_KEY, fetch_bytes)
        ko_full = trim_utf8(raw)
        os.makedirs(os.path.dirname(args.ko_cache), exist_ok=True)
        open(args.ko_cache, "wb").write(ko_full)
    log(f"[corpus] full fetched window = {len(ko_full)} bytes ({len(ko_full)/1e6:.1f} MB)")

    # 30MB anchor sha gate (the H_1368 window = first 30MB-trimmed prefix; sha must match)
    win30 = trim_utf8(ko_full[:30_000_000])
    sha30 = hashlib.sha256(win30).hexdigest()
    anchor_sha_ok = (sha30 == H1368_KO_SHA_30M)
    log(f"[corpus] 30MB-prefix sha {sha30} == H_1368/H_1316 baseline: {anchor_sha_ok}")
    if not anchor_sha_ok:
        log("FATAL: 30MB-prefix sha mismatch — corpus drift, REAL-only NO synthetic. STOP."); sys.exit(3)

    # jamo vocab fixed ONCE on the FULL fetched window (no per-rung vocab drift, byte-fair)
    full_text = ko_full.decode("utf-8")
    jamo_to_id, jamo_sorted = build_jamo_vocab(full_text)
    vj = 256 + len(jamo_sorted)
    log(f"[rep] Vj={vj} ({len(jamo_sorted)} distinct jamo) — fixed across all rungs")
    log(f"[A1] frozen lambda={LAMBDA.round(5).tolist()} nmax={args.nmax} (== H_1344/H_1359/H_1368, NOT re-tuned per rung)")

    # ── EXTENDED DATA-RICHNESS LADDER: prefix sub-windows ─────────────────────────
    rungs = []
    for mb in ladder:
        wbytes = int(mb * 1_000_000)
        if wbytes > len(ko_full):
            log(f"[rung {mb:>6.1f}MB] SKIP — exceeds fetched window ({len(ko_full)} bytes)")
            continue
        sub = trim_utf8(ko_full[:wbytes])
        sub_sha = hashlib.sha256(sub).hexdigest()
        sub_text = sub.decode("utf-8")
        syms, nby = make_symbol_stream(sub_text, jamo_to_id)
        r = score_rung(syms, nby, vj, args.nmax, args.stride, args.shift)
        r["window_mb"] = mb
        r["window_bytes"] = len(sub)
        r["window_sha256"] = sub_sha
        r["stream_len"] = int(len(syms))
        rungs.append(r)
        log(f"[rung {mb:>6.1f}MB] bytes={len(sub)} sha={sub_sha[:12]} stream={len(syms)} "
            f"novel_frac={r['novel_frac']} m_novel={r['m_novel']}  "
            f"CE_novel={r['ce_novel']} (Δfloor {r['delta_vs_floor']:+.5f})  "
            f"CE_shift={r['ce_shift']} (shift−novel {r['shift_minus_novel']:+.5f})  "
            f"[{time.time()-t0:.0f}s]")

    if len(rungs) < 2:
        log("FATAL: <2 rungs measured — cannot extend ladder. STOP."); sys.exit(4)

    ces = [r["ce_novel"] for r in rungs]
    wins = [r["window_bytes"] for r in rungs]
    mbs = [r["window_mb"] for r in rungs]
    new_rungs = [r for r in rungs if r["window_mb"] > 30.0 + 1e-9]

    # ── bar 1 LADDER-EXTENDED ─────────────────────────────────────────────────────
    bar1 = len(new_rungs) >= 2
    log(f"[bar1 LADDER-EXTENDED] new rungs>30MB={len(new_rungs)} (>=2 req) → bar1={bar1}")

    # ── bar 4 CONTROL: 30MB anchor reproduces + shift EARNED + floor re-measured ──
    anchor_rung = next((r for r in rungs if abs(r["window_mb"] - 30.0) < 1e-6), None)
    anchor_ok = anchor_rung is not None and abs(anchor_rung["ce_novel"] - H1359_NOVEL_CE_30M) <= ANCHOR_TOL
    anchor_delta = round(abs(anchor_rung["ce_novel"] - H1359_NOVEL_CE_30M), 5) if anchor_rung else None
    earned = [bool(r["shift_minus_novel"] >= 0.05) for r in rungs]
    all_earned = all(earned)
    # re-measure the jamo floor on the LARGEST window (full corpus, in-distribution, no novel-filter)
    big = rungs[-1]
    big_bytes = big["window_bytes"]
    big_sub = trim_utf8(ko_full[:big_bytes]); big_text = big_sub.decode("utf-8")
    big_syms, big_nby = make_symbol_stream(big_text, jamo_to_id)
    floor_remeasured, floor_m = measure_jamo_floor(big_syms, big_nby, vj, args.nmax, args.stride)
    floor_delta = round(floor_remeasured - H1316_JAMO_FLOOR, 5)
    floor_stable = abs(floor_delta) <= 0.10
    bar4 = anchor_ok and all_earned
    log(f"[bar4 CONTROL] 30MB anchor={anchor_rung['ce_novel'] if anchor_rung else None} "
        f"vs {H1359_NOVEL_CE_30M} (|Δ|={anchor_delta}<= {ANCHOR_TOL}: {anchor_ok}) · "
        f"shift earned per-rung={earned} (all={all_earned}) · "
        f"floor re-measured@{big['window_mb']}MB={floor_remeasured} (Δ vs 2.51335={floor_delta:+.5f}, stable={floor_stable}) → bar4={bar4}")

    # ── bar 2 ASYMPTOTE + honest descent check ────────────────────────────────────
    steps = [float(ces[i+1] - ces[i]) for i in range(len(ces) - 1)]
    decreasing = all(d <= -0.001 for d in steps)
    increasing = all(d >= 0.001 for d in steps)
    flat = all(abs(d) < 0.001 for d in steps)
    direction = "DECREASING" if decreasing else "INCREASING" if increasing else "FLAT" if flat else "NON-MONOTONE"
    fit = fit_asymptote(wins, ces)
    c_inf = fit["c_inf_estimate"]; reliable = fit["asymptote_reliable"]
    asym_class, asym_note = classify_asymptote(c_inf, reliable, min(ces))
    b = fit["log_fit"]["b_slope_per_log2W"]
    if b < -1e-6:
        d2f = (ces[-1] - H1316_JAMO_FLOOR) / (-b)
        win_to_floor = wins[-1] * (2.0 ** d2f)
        fit["log_fit"]["doublings_maxrung_to_floor"] = round(float(d2f), 3)
        fit["log_fit"]["window_to_floor_bytes"] = float(win_to_floor)
        fit["log_fit"]["window_to_floor_mb"] = round(float(win_to_floor) / 1e6, 1)
    else:
        fit["log_fit"]["doublings_maxrung_to_floor"] = None
        fit["log_fit"]["window_to_floor_bytes"] = None
        fit["log_fit"]["window_to_floor_mb"] = None
    log(f"[bar2 DIRECTION] step ΔCE={[round(d,5) for d in steps]} → {direction}")
    log(f"[bar2 ASYMPTOTE] log_fit b={b} (r2 {fit['log_fit']['r2']}) "
        f"win_to_floor≈{fit['log_fit']['window_to_floor_mb']}MB  power c_inf={c_inf} p={fit['power_fit']['p']} "
        f"reliable={reliable} → {asym_class} vs floor 2.51335 ({asym_note})")

    # ── TIER (frozen mapping) ─────────────────────────────────────────────────────
    if not bar1:
        tier = "STOP-NO-DATA"
        verdict = "🛑 STOP-NO-DATA — fewer than 2 rungs beyond 30MB; H_1368 30MB extrapolation stays best-available."
    elif not anchor_ok:
        tier = "INVALID-RED"
        verdict = f"🔴 INVALID — 30MB anchor mismatch (|Δ|={anchor_delta}), methodology drift."
    elif not all_earned:
        tier = "INVALID-RED"
        verdict = f"🔴 INVALID — shift surrogate not earned at every rung ({earned}); signal suspect."
    elif direction in ("FLAT",) or (asym_class == "AT"):
        tier = "FLOOR-TERMINAL-AT"
        verdict = (f"🧱 FLOOR-TERMINAL-AT — extended ladder ({mbs[0]}→{mbs[-1]}MB) drives novel-CE to the "
                   f"2.51335 jamo floor (asymptote≈{c_inf}, direction={direction}); the Korean below-jamo "
                   "arc is CLOSED across data too (representation H_1322 · interpolation H_1359 · "
                   "data-richness H_1368/H_1380). Lane DEPLETED (valid, c9).")
    elif asym_class == "BELOW":
        tier = "FLOOR-BREAKS-BELOW"
        verdict = (f"🟢 FLOOR-BREAKS-BELOW (CANDIDATE) — novel-CE decreases monotonically over the EXTENDED "
                   f"ladder ({ces[0]}→{ces[-1]}, {mbs[0]}→{mbs[-1]}MB) AND the reliable asymptote ({c_inf}) "
                   "sits BELOW the 2.51335 jamo floor → enough real data REOPENS the representation lever "
                   "(H_1322 🧱 bypassed via data) on truly-novel context. DIRECTIONAL numpy — engine-native "
                   "re-confirmation is the follow-on.")
    elif asym_class == "ABOVE":
        tier = "DESCENDING-FLOOR-ABOVE"
        verdict = (f"🟠 DESCENDING-FLOOR-ABOVE — novel-CE decreases with window (data-richness helps) but the "
                   f"reliable asymptote ({c_inf}) is ABOVE the 2.51335 floor → more data narrows the gap yet a "
                   "floor holds above jamo in the limit.")
    else:  # STILL-DESCENDING-UNRESOLVED
        d2f = fit["log_fit"].get("window_to_floor_mb")
        tier = "DESCENDING-UNSATURATED-EXTENDED"
        verdict = (f"📉 DESCENDING-UNSATURATED-EXTENDED — novel-CE STILL decreases monotonically over the "
                   f"EXTENDED ladder ({ces[0]}→{ces[-1]} over {mbs[0]}→{mbs[-1]}MB, ~{b} nats/doubling) so even "
                   f"{mbs[-1]}MB has NOT saturated; but a {len(rungs)}-rung power-law extrapolation remains "
                   "under-constrained (UNRELIABLE c_inf). Log-linear descent reaches the 2.51335 floor near "
                   f"~{d2f}MB. Whether the true asymptote sits AT/ABOVE/BELOW the floor is STILL UNRESOLVED at "
                   "the max data reached — honest INCOMPLETE (NO GREEN over-claim, c9); the floor-break "
                   "question now needs a larger ladder still or an engine-native re-test.")

    res = {
        "id": "H_1380", "slug": "ko_data_ladder",
        "ko_full_window_bytes": len(ko_full), "ko_full_window_mb": round(len(ko_full)/1e6, 1),
        "ko_30MB_prefix_sha256": sha30, "sha_match_H1368": anchor_sha_ok,
        "Vj": vj, "distinct_jamo": len(jamo_sorted), "gate_stride": args.stride, "nmax": args.nmax,
        "frozen_lambda": LAMBDA.round(6).tolist(),
        "H1316_jamo_floor": H1316_JAMO_FLOOR, "H1307_raw_ceiling": H1307_RAW_CEILING,
        "H1359_novel_ce_30M_anchor": H1359_NOVEL_CE_30M,
        "ladder_mb": ladder, "rungs": rungs,
        "novel_ce_curve": ces, "step_delta_ce": [round(d, 5) for d in steps],
        # bars
        "bar1_LADDER_EXTENDED": bool(bar1), "new_rungs_gt30MB": len(new_rungs),
        "bar2_DIRECTION": direction, "bar2_asymptote_fit": fit,
        "bar2_c_inf": c_inf, "bar2_asymptote_class": asym_class, "bar2_asymptote_note": asym_note,
        "bar3_HELDOUT": "novel-only odd-stride slice, top-order ctx absent from TRAIN (== H_1368/H_1359 TEST A)",
        "bar4_CONTROL": bool(bar4), "bar4_30MB_anchor_ok": bool(anchor_ok), "bar4_anchor_abs_delta": anchor_delta,
        "bar4_per_rung_earned": earned, "bar4_all_earned": bool(all_earned),
        "bar4_floor_remeasured": floor_remeasured, "bar4_floor_delta_vs_2.51335": floor_delta,
        "bar4_floor_stable": bool(floor_stable), "bar4_floor_window_mb": big["window_mb"],
        "tier": tier, "verdict": verdict, "wall_sec": round(time.time() - t0, 1),
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=2) + "\n")
    log("\n===== H_1380 RESULT =====")
    log(json.dumps(res, ensure_ascii=False, indent=2))
    log(f"\nTIER: {tier}\n{verdict}")


if __name__ == "__main__":
    main()
