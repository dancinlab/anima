#!/usr/bin/env python3
# h1368_ko_data_richness.py — the ONE remaining Korean-compression lever: DATA-RICHNESS.
#
# Representation (H_1322 featural 🧱) and interpolation (H_1359 JM=memorization 🧱) are closed.
# H_1359 confirmed the 2.51335 jamo floor is REAL on truly-NOVEL context (its novel-only CE was
# 2.88190, WORSE than the floor) and explicitly named the last lever: does novel-context CE DROP
# toward the floor as the corpus WINDOW grows?
#
# H_1368 builds a DATA-RICHNESS LADDER = PREFIX sub-windows of the SAME 30MB R2 KO corpus
# (3.75 / 7.5 / 15 / 30 MB). At each rung it scores the novel-only held-out CE using the IDENTICAL
# novel-filter, jamo representation, and FROZEN λ as H_1359 (NOT re-tuned per rung — anti-Goodhart).
# The 30MB rung must reproduce H_1359's 2.88190 (±0.02) as a sanity anchor. It then asks:
#   - monotone DECREASING with window?  (c2)
#   - what asymptote does the curve extrapolate to vs 2.51335?  (c3, two estimators)
#   - earned (shift surrogate goes wrong way) at every rung?  (c4)
#
# FROZEN-FIRST: bars pre-registered in .verdicts/1368_ko_data_richness/H_1368_FREEZE.txt BEFORE this
# run. REAL Korean only — R2 KO window sha ASSERTED == c47b6808... (== H_1316/H_1344/H_1359).
# DIRECTIONAL numpy; toy stride-300 byte-substrate next-symbol CE; CORE UNTOUCHED.

import argparse, hashlib, json, os, sys, time, unicodedata
import numpy as np

HANGUL_LO, HANGUL_HI = 0xAC00, 0xD7A3
H1316_JAMO_FLOOR = 2.51335     # the floor under test (H_1316 locked, nats/UTF-8-byte)
H1307_RAW_CEILING = 2.95342
H1307_KO_SHA = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
H1359_NOVEL_CE_30M = 2.88190   # H_1359 TEST A novel-only CE at 30MB (anchor)
LAPLACE = 1.0
NMAX = 5                       # FROZEN (== H_1344/H_1359)
RAW_W = np.array([2.0 ** k for k in range(NMAX)], dtype=np.float64)   # [1,2,4,8,16]
LAMBDA = RAW_W / RAW_W.sum()                                          # [1/31,...,16/31]
KO_STRIDE = 300
KO_WINDOW = 30_000_000
LADDER_MB = [3.75, 7.5, 15.0, 30.0]                                   # prefix sub-windows (MB)
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


# ── jamo symbol stream (IDENTICAL to H_1316/H_1344/H_1359: byte-fair axis) ────
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


# ── Jelinek-Mercer recursive interpolated n-gram (IDENTICAL to H_1344/H_1359) ─
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
    """One ladder rung: stride split, fit JM on TRAIN, score NOVEL-ONLY held-out CE
    (top-order context not in TRAIN top-order set), + circular-shift surrogate. IDENTICAL
    novel-filter as H_1359 TEST A."""
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


def fit_asymptote(windows_bytes, ces):
    """Two pre-registered asymptote estimators over the ladder (windows in bytes, ces nats/byte)."""
    W = np.asarray(windows_bytes, dtype=np.float64)
    y = np.asarray(ces, dtype=np.float64)
    out = {}
    # (i) log-window linear fit: CE = a + b*log2(W)
    x = np.log2(W)
    A = np.vstack([np.ones_like(x), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    a, b = float(coef[0]), float(coef[1])
    yhat = A @ coef
    ss_res = float(np.sum((y - yhat) ** 2)); ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2_log = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    out["log_fit"] = {"a": round(a, 5), "b_slope_per_log2W": round(b, 5),
                      "r2": round(r2_log, 5),
                      "ce_at_2x30MB": round(a + b * np.log2(2 * 30e6), 5),
                      "ce_at_10x30MB": round(a + b * np.log2(10 * 30e6), 5)}
    # (ii) power-law decay: CE = c_inf + Amp * W^(-p), grid-search p, linear-solve {c_inf,Amp}
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
    # RELIABILITY GUARDRAIL (anti-tune-to-green, c9): a 4-point power-law tail is severely
    # under-constrained. The fit is UNRELIABLE if the extrapolated asymptote is physically
    # implausible (a next-symbol CE on this substrate cannot fall below the empirical floor by an
    # arbitrary margin — c_inf below the jamo floor minus a wide 0.20 band signals the optimizer
    # flattened a slow power into a near-constant offset, not a real saturation), OR if the decay
    # exponent p is pinned at a grid edge (no curvature constraint). When UNRELIABLE we do NOT
    # let the asymptote drive the tier — descent is reported, asymptote is UNDETERMINED.
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


def classify_asymptote(c_inf, reliable):
    floor = H1316_JAMO_FLOOR
    if not reliable:
        return "UNDETERMINED", ("4-rung power-law extrapolation is under-constrained "
                                "(physically-implausible c_inf and/or p pinned at grid edge) — "
                                "descent is real but the asymptote cannot be pinned with 4 points")
    if c_inf < floor - 0.01:
        return "BELOW", "representation lever REOPENS (asymptote below 2.51335)"
    if c_inf <= floor + 0.01:
        return "AT", "30MB had not saturated; floor is the data-richness limit"
    return "ABOVE", "data-richness floor is REAL above the jamo floor"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ko-cache", default="/tmp/h1344_corpus/kor30m.bytes")
    ap.add_argument("--ko-window", type=int, default=KO_WINDOW)
    ap.add_argument("--stride", type=int, default=KO_STRIDE)
    ap.add_argument("--nmax", type=int, default=NMAX)
    ap.add_argument("--shift", type=int, default=99991)
    ap.add_argument("--out", default=".verdicts/1368_ko_data_richness/H_1368.txt")
    args = ap.parse_args()
    t0 = time.time()

    # ── REAL corpus (cache or R2 fetch); sha gate on the FULL 30MB window ──────
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

    # build the jamo vocab from the FULL window (vocab fixed across rungs — byte-fair, no per-rung vocab drift)
    full_text = ko_win.decode("utf-8")
    jamo_to_id, jamo_sorted = build_jamo_vocab(full_text)
    vj = 256 + len(jamo_sorted)
    log(f"[rep] Vj={vj} ({len(jamo_sorted)} distinct jamo) — fixed across all rungs")
    log(f"[A1] frozen lambda={LAMBDA.round(5).tolist()}  nmax={args.nmax} (== H_1344/H_1359, NOT re-tuned per rung)")

    # ── DATA-RICHNESS LADDER: prefix sub-windows of the 30MB corpus ───────────
    rungs = []
    for mb in LADDER_MB:
        wbytes = int(mb * 1_000_000)
        sub = trim_utf8(ko_win[:wbytes])
        sub_text = sub.decode("utf-8")
        syms, nby = make_symbol_stream(sub_text, jamo_to_id)
        r = score_rung(syms, nby, vj, args.nmax, args.stride, args.shift)
        r["window_mb"] = mb
        r["window_bytes"] = len(sub)
        r["stream_len"] = int(len(syms))
        rungs.append(r)
        log(f"[rung {mb:>5.2f}MB] bytes={len(sub)} stream={len(syms)} "
            f"novel_frac={r['novel_frac']} m_novel={r['m_novel']}  "
            f"CE_novel={r['ce_novel']} (Δfloor {r['delta_vs_floor']:+.5f})  "
            f"CE_shift={r['ce_shift']} (shift−novel {r['shift_minus_novel']:+.5f})")

    ces = [r["ce_novel"] for r in rungs]
    wins = [r["window_bytes"] for r in rungs]

    # ── c1 CURVE + 30MB anchor ────────────────────────────────────────────────
    ce_30 = rungs[-1]["ce_novel"]
    anchor_ok = abs(ce_30 - H1359_NOVEL_CE_30M) <= ANCHOR_TOL
    c1 = (len(rungs) >= 3) and anchor_ok
    log(f"[c1 CURVE] rungs={len(rungs)} 30MB novel-CE={ce_30} vs H_1359 anchor {H1359_NOVEL_CE_30M} "
        f"(|Δ|={abs(ce_30-H1359_NOVEL_CE_30M):.5f} <= {ANCHOR_TOL}: {anchor_ok}) → c1={c1}")

    # ── c2 DIRECTION: monotone decreasing? ────────────────────────────────────
    steps = [float(ces[i+1] - ces[i]) for i in range(len(ces) - 1)]
    decreasing = all(d <= -0.001 for d in steps)
    increasing = all(d >= 0.001 for d in steps)
    if decreasing:
        direction = "DECREASING"
    elif increasing:
        direction = "INCREASING"
    elif all(abs(d) < 0.001 for d in steps):
        direction = "FLAT"
    else:
        direction = "NON-MONOTONE"
    log(f"[c2 DIRECTION] step ΔCE={[round(d,5) for d in steps]} → {direction}")

    # ── c3 ASYMPTOTE ──────────────────────────────────────────────────────────
    fit = fit_asymptote(wins, ces)
    c_inf = fit["c_inf_estimate"]
    reliable = fit["asymptote_reliable"]
    asym_class, asym_note = classify_asymptote(c_inf, reliable)
    # robust auxiliary: from the log-linear descent, how many window DOUBLINGS to reach the floor?
    b = fit["log_fit"]["b_slope_per_log2W"]                  # ΔCE per doubling (negative if descending)
    if b < -1e-6:
        doublings_to_floor = (ces[-1] - H1316_JAMO_FLOOR) / (-b)
        window_to_floor_bytes = wins[-1] * (2.0 ** doublings_to_floor)
        fit["log_fit"]["doublings_30MB_to_floor"] = round(float(doublings_to_floor), 3)
        fit["log_fit"]["window_to_floor_bytes"] = float(window_to_floor_bytes)
    else:
        fit["log_fit"]["doublings_30MB_to_floor"] = None
        fit["log_fit"]["window_to_floor_bytes"] = None
    log(f"[c3 ASYMPTOTE] log_fit b={b} (r2 {fit['log_fit']['r2']}) "
        f"doublings_to_floor={fit['log_fit']['doublings_30MB_to_floor']}  "
        f"power_fit c_inf={c_inf} p={fit['power_fit']['p']} reliable={reliable} "
        f"→ {asym_class} vs floor 2.51335 ({asym_note})")

    # ── c4 EARNED: shift surrogate goes wrong way at EVERY rung ───────────────
    earned = [bool(r["shift_minus_novel"] >= 0.05) for r in rungs]
    c4 = all(earned)
    log(f"[c4 EARNED] per-rung shift−novel>=0.05 = {earned} → c4={c4}")

    # ── TIER ──────────────────────────────────────────────────────────────────
    if not c1 or not c4:
        tier = "INVALID-RED"
        verdict = ("🔴 INVALID — " + ("30MB anchor mismatch (methodology drift)" if not anchor_ok
                   else "shift surrogate did not go wrong way at every rung (signal suspect)"))
    elif direction == "DECREASING" and asym_class == "BELOW":
        tier = "GREEN"
        verdict = ("🟢 GREEN — novel-context CE DECREASES monotonically with corpus window AND the "
                   f"asymptote estimate ({c_inf}) is BELOW the 2.51335 jamo floor → enough data REOPENS "
                   "the representation lever on truly-novel context")
    elif direction == "DECREASING" and asym_class == "UNDETERMINED":
        d2f = fit["log_fit"]["doublings_30MB_to_floor"]
        tier = "DESCENDING-UNSATURATED"
        verdict = ("📉 DESCENDING-UNSATURATED — novel-context CE DECREASES monotonically with corpus "
                   f"window ({ces[0]}→{ces[-1]} over 3.75→30MB, ~{fit['log_fit']['b_slope_per_log2W']} "
                   "nats/doubling), so 30MB was NOT saturated and the data-richness lever is LIVE; but a "
                   "4-rung extrapolation CANNOT pin the asymptote (power-fit under-constrained). The "
                   f"log-linear descent would need ~{d2f} further window-doublings to merely TOUCH the "
                   "2.51335 floor — i.e. data helps but reaching the floor demands far more corpus than "
                   "this 30MB-bounded ladder holds. Whether the true asymptote sits AT, ABOVE, or BELOW "
                   "the floor is UNRESOLVED — needs a >30MB ladder (honest, c9; NO over-claim of GREEN)")
    elif direction == "DECREASING":
        tier = "DESCENDING-FLOOR"
        verdict = ("🟠 DESCENDING-FLOOR — novel-context CE DECREASES with corpus window (data-richness "
                   f"helps) but the asymptote estimate ({c_inf}) is {asym_class} the 2.51335 floor → "
                   "more data narrows the gap yet the floor holds in the limit; 30MB was below saturation")
    else:
        tier = "FLOOR-HARD"
        verdict = ("🧱 FLOOR-HARD — novel-context CE does NOT decrease monotonically with corpus window "
                   f"(direction={direction}) over [3.75,30]MB → the data-richness lever does NOT lower "
                   "novel-context CE in this range; 2.51335 is confirmed a HARD floor across all three "
                   "levers (representation H_1322 · interpolation H_1359 · data-richness H_1368), "
                   "lane DEPLETED (valid depleting result, c9)")

    res = {
        "id": "H_1368", "slug": "ko-data-richness",
        "ko_full_window_bytes": len(ko_win), "ko_full_window_sha256": ko_sha,
        "sha_match_H1316_floor": same, "Vj": vj, "distinct_jamo": len(jamo_sorted),
        "gate_stride": args.stride, "nmax": args.nmax,
        "frozen_lambda": LAMBDA.round(6).tolist(),
        "H1316_jamo_floor": H1316_JAMO_FLOOR, "H1307_raw_ceiling": H1307_RAW_CEILING,
        "H1359_novel_ce_30M_anchor": H1359_NOVEL_CE_30M,
        "ladder_mb": LADDER_MB,
        "rungs": rungs,
        "novel_ce_curve": ces,
        "step_delta_ce": [round(d, 5) for d in steps],
        # bars
        "bar_c1_CURVE": bool(c1), "c1_30MB_anchor_ok": bool(anchor_ok),
        "c1_30MB_novel_ce": ce_30, "c1_anchor_abs_delta": round(abs(ce_30 - H1359_NOVEL_CE_30M), 5),
        "bar_c2_DIRECTION": direction, "c2_decreasing": bool(decreasing),
        "bar_c3_asymptote_fit": fit, "c3_c_inf": c_inf,
        "c3_asymptote_class": asym_class, "c3_asymptote_note": asym_note,
        "bar_c4_EARNED": bool(c4), "c4_per_rung_earned": earned,
        "tier": tier, "verdict": verdict,
        "wall_sec": round(time.time() - t0, 1),
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=2) + "\n")
    log("\n===== H_1368 RESULT =====")
    log(json.dumps(res, ensure_ascii=False, indent=2))
    log(f"\nTIER: {tier}\n{verdict}")


if __name__ == "__main__":
    main()
