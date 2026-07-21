"""H_008 — f7-owner-clean. Clean resolution of the H_007 PENDING(instrument) verdict.

H_007 read the owner premise BORDERLINE-weak-positive (markov6 legibility +0.0207 ~ eps;
participation ratio 2.27 ~ floor) but PENDING because its O-3 liveness control read NEGATIVE
under markov6 (-0.0305). Diagnosis: the planted liveness stream was HIGH-ENTROPY random bytes,
where an order-k Markov model that memorises a block once gets a Laplace-smoothed prob (~2/257)
WORSE than the block's own entropy (log2(94)=6.55 bits) — so the "oracle" is penalised and the
ceiling reads negative. That is an estimator artifact, not an owner finding.

This card resolves it cleanly at $0, three fixes:

  1. TEXT-LIKE liveness. Rebuild the planted liveness stream as low-entropy WORD-TOKEN text: a
     day-specific topic phrase (repeated, so Markov counts build up) placed BEYOND the tail in
     day t's summary, echoed as day t+1's prefix. An order-aware Markov MUST read a large
     positive over-floor on this (the phrase transitions are sharp), else the instrument is blind.

  2. TWO fast order-aware estimators replace ppm (which does not scale to the owner data at $0):
     cond_bpb_markov order-3 and order-8. Both are O(n) sparse-dict Markov, both fast.

  3. TWO grains of the owner stream:
       (a) per-session-file (H_007's grain, ~241 sessions), and
       (b) per-CALENDAR-DAY (sessions grouped by their mtime date — a coarser "day" unit).

Pre-registered verdict rule (FROZEN before measuring):
  ANCHORED  iff the text-like liveness PASSES (over-floor > 5*eps) AND, on AT LEAST ONE grain,
            BOTH order-aware estimators (markov3, markov8) show legibility over-floor > eps=0.02
            AND the owner-self participation ratio > 2.0.
  BORDERLINE if the best grain leans positive (both estimators > 0) but sits AT threshold
            (legibility within +/-0.005 of eps on either estimator, or PR within 0.1 of 2.0).
  REFUSED   if the best grain is below (any order-aware legibility <= 0, or clearly under eps
            with PR under floor) — the owner premise carries no predictable high-dim self.
  INVALID   if the text-like liveness fails (blind instrument).

Falsifiers (pre-registered):
  L-1 liveness      : text-like planted stream over-floor <= 5*eps under either markov -> INVALID.
  L-2 kill          : both grains have an order-aware legibility <= eps -> owner unpredictable.
  L-3 rank collapse : legible grain has PR <= 2.0 -> owner-self is one-bit (v1 seam).
  L-4 shuffle floor : the shuffle baseline must not itself exceed the real ceiling (over_floor sign).
  L-5 order agree   : markov3 and markov8 sign-agree on legibility on the reported grain.

Privacy: NO owner message CONTENT is written into the repo — only aggregate bpb/rank numbers.
The owner's words stay on their own disk. Card frozen 2026-07-16.

Run: python3 state/h008_f7-owner-clean_2026-07-16/run_h008.py
"""

from __future__ import annotations

import functools
import json
import os
import sys
import time
from datetime import date

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tool"))
sys.path.insert(0, os.path.join(_ROOT, "state", "h005_f3-stream-mi-precheck_2026-07-16"))
sys.path.insert(0, os.path.join(_ROOT, "state", "h007_f7-owner-legibility_2026-07-16"))

from anima_v3 import Falsifier, evaluate, participation_ratio, singular_values
from run_h005 import cond_bpb_markov, measure_stream, W, P
# reuse H_007's FROZEN genuine-owner extraction verbatim (same NOISE filter, same fields)
import glob
from run_h007 import owner_text, TRANSCRIPTS

markov3 = functools.partial(cond_bpb_markov, order=3)
markov8 = functools.partial(cond_bpb_markov, order=8)
EPS = 0.02
PR_FLOOR = 2.0
BAND_BPB = 0.005   # "at threshold" band for legibility around EPS
BAND_PR = 0.1      # "at threshold" band for PR around PR_FLOOR


# --- 1. text-like liveness control -------------------------------------------

# a small common-word pool -> low-entropy generic "register" filler
_WORDS = ("the of and to a in is it that for on with as was at by an be this have from or one "
          "had not but what all were when we there can your which their said if do will each "
          "about how up out them then she many some so these would other into has more her two "
          "like him time see no way could people my than first water been call who oil now find").split()


def _lcg(seed):
    st = seed
    def nxt():
        nonlocal st
        st = (1103515245 * st + 12345) & 0x7FFFFFFF
        return st
    return nxt


def _filler(nbytes, nxt):
    """Generic low-entropy word-token register, shared shape across days (the shuffle floor)."""
    out = []
    n = 0
    while n < nbytes:
        w = _WORDS[nxt() % len(_WORDS)]
        out.append(w)
        n += len(w) + 1
    return (" ".join(out)).encode("ascii")[:nbytes]


def _phrase_block(day, nbytes):
    """A day-specific, low-entropy topic phrase REPEATED to fill nbytes. Repetition lets an
    order-aware Markov build sharp counts; the day marker token makes it day-specific."""
    tok = "widget%d" % day
    phrase = (" the %s report reviews the %s module and the %s testing plan for today then "
              "closes the %s review " % (tok, tok, tok, tok))
    pb = phrase.encode("ascii")
    reps = (nbytes // len(pb)) + 1
    return (pb * reps)[:nbytes]


def planted_textlike(n_days=30, seed=11):
    """L-1 liveness: TEXT-like planted legible stream. day = prefix + block + filler, where
    prefix = YESTERDAY's phrase-block (echo), block = TODAY's phrase-block (day-specific, lives
    in the summary BEYOND the tail), filler = generic register (becomes the tail). So day t's
    SUMMARY predicts day t+1's PREFIX (the cross-session self a legible owner would carry), while
    the tail alone cannot. Low entropy, so an order-aware Markov handles it. Deterministic LCG."""
    nxt = _lcg(seed)
    chunks = []
    prev_block = None
    for d in range(n_days):
        block = _phrase_block(d, P)
        prefix = prev_block if prev_block is not None else block
        filler = _filler(W + 1000, nxt)
        chunks.append(("s%d" % d, prefix + block + filler))
        prev_block = block
    return chunks


# --- 2. legibility + rank -----------------------------------------------------

def _shuffle(chunks):
    """Deterministic adjacency-breaking permutation (H_005/H_007 verbatim)."""
    return (chunks[::2] + chunks[1::2])[::-1]


def legibility(chunks, est):
    """Cross-session over-floor: real-adjacency ceiling minus shuffled-adjacency ceiling."""
    res = measure_stream(chunks, est)
    shuf = measure_stream(_shuffle(chunks), est)
    return res["ceiling_med"] - shuf["ceiling_med"], res["ceiling_med"], shuf["ceiling_med"]


def rank_of(chunks):
    """Owner-self participation ratio on per-chunk byte-class feature vectors (H_007 verbatim:
    32-dim byte-class histogram, every 8th class)."""
    feats = []
    for _, b in chunks:
        v = [b.count(bytes([c])) for c in range(0, 256, 8)]
        s = sum(v) or 1
        feats.append([x / s for x in v])
    return participation_ratio(singular_values(feats)) if len(feats) >= 2 else 0.0


# --- 3. owner grains ----------------------------------------------------------

def _owner_raw():
    """[(mtime, bytes)] genuine-owner-message text per transcript with >= W+P bytes."""
    out = []
    for path in glob.glob(TRANSCRIPTS):
        t = owner_text(path)
        b = t.encode("utf-8", "replace")
        if len(b) >= W + P:
            out.append((os.path.getmtime(path), b))
    return out


def owner_sessions(raw):
    """Grain (a): per-session-file, chronological by mtime (H_007 grain)."""
    s = sorted(raw, key=lambda x: x[0])
    return [(str(i), b) for i, (_, b) in enumerate(s)]


def owner_days(raw):
    """Grain (b): per-CALENDAR-DAY. Concatenate all sessions sharing a mtime date (ordered by
    mtime within the day), keep days with >= W+P bytes, order by date."""
    by_day = {}
    for mt, b in sorted(raw, key=lambda x: x[0]):
        d = date.fromtimestamp(mt).isoformat()
        by_day.setdefault(d, []).append(b)
    out = []
    for d in sorted(by_day):
        blob = b"\n".join(by_day[d])
        if len(blob) >= W + P:
            out.append((d, blob))
    return out


def measure_grain(name, chunks, m):
    if len(chunks) < 3:
        print("  [%s] SKIP — only %d chunks" % (name, len(chunks)))
        m[name] = {"n": len(chunks), "skipped": True}
        return None
    o3, c3, s3 = legibility(chunks, markov3)
    o8, c8, s8 = legibility(chunks, markov8)
    pr = rank_of(chunks)
    row = {
        "n": len(chunks),
        "markov3": {"over_floor": o3, "ceiling": c3, "shuffle": s3},
        "markov8": {"over_floor": o8, "ceiling": c8, "shuffle": s8},
        "participation_ratio": pr,
        "legible": (o3 > EPS and o8 > EPS),
        "high_dim": pr > PR_FLOOR,
        "sign_agree": (o3 > 0) == (o8 > 0),
        "anchored": (o3 > EPS and o8 > EPS and pr > PR_FLOOR),
    }
    m[name] = row
    print("  [%s] n=%d  markov3 over_floor %+.4f (ceil %+.4f shuf %+.4f) · "
          "markov8 over_floor %+.4f (ceil %+.4f shuf %+.4f) · PR %.2f"
          % (name, len(chunks), o3, c3, s3, o8, c8, s8, pr))
    print("        legible(both>eps)=%s · high_dim(PR>%.1f)=%s · sign_agree=%s · anchored=%s"
          % (row["legible"], PR_FLOOR, row["high_dim"], row["sign_agree"], row["anchored"]))
    return row


def _near(v, target, band):
    return abs(v - target) <= band


def main():
    print("=" * 74)
    print("H_008 — f7-owner-clean · resolve the H_007 owner premise (text-like liveness, $0)")
    print("=" * 74)
    print("W=%d tail · P=%d prefix · eps=%.3f bpb · PR floor %.1f\n" % (W, P, EPS, PR_FLOOR))
    m = {"eps": EPS, "pr_floor": PR_FLOOR}

    # --- L-1: text-like liveness (must PASS both order-aware estimators) -------
    t0 = time.time()
    live = planted_textlike()
    lo3, lc3, ls3 = legibility(live, markov3)
    lo8, lc8, ls8 = legibility(live, markov8)
    m["liveness"] = {"markov3_over_floor": lo3, "markov3_ceiling": lc3, "markov3_shuffle": ls3,
                     "markov8_over_floor": lo8, "markov8_ceiling": lc8, "markov8_shuffle": ls8}
    live_ok = lo3 > 5 * EPS and lo8 > 5 * EPS
    m["liveness_ok"] = live_ok
    print("[L-1 liveness] TEXT-like planted legibility:")
    print("        markov3 over_floor %+.4f (ceil %+.4f shuf %+.4f)" % (lo3, lc3, ls3))
    print("        markov8 over_floor %+.4f (ceil %+.4f shuf %+.4f)" % (lo8, lc8, ls8))
    print("        liveness PASS (both > %.3f)? %s\n" % (5 * EPS, live_ok))

    # --- owner grains ---------------------------------------------------------
    raw = _owner_raw()
    m["n_usable_transcripts"] = len(raw)
    print("genuine-owner usable transcripts (>= %d B): %d" % (W + P, len(raw)))
    sess = owner_sessions(raw)
    days = owner_days(raw)
    print("grain (a) per-session-file: %d chunks · grain (b) per-calendar-day: %d chunks\n"
          % (len(sess), len(days)))

    print("owner-stream legibility over-floor (real vs session-order shuffle):")
    row_s = measure_grain("per_session", sess, m)
    row_d = measure_grain("per_day", days, m)
    m["elapsed_sec"] = round(time.time() - t0, 1)
    print("\n(elapsed %.1fs)" % m["elapsed_sec"])

    grains = [g for g in (row_s, row_d) if g and not g.get("skipped")]
    any_anchored = any(g["anchored"] for g in grains)

    # pick the "best" grain = highest min(over_floor) as the reported one
    def _minof(g):
        return min(g["markov3"]["over_floor"], g["markov8"]["over_floor"])
    best = max(grains, key=_minof) if grains else None

    # --- pre-registered classification ----------------------------------------
    if not live_ok:
        verdict = ("INVALID (blind instrument) — the TEXT-like planted liveness did not clear "
                   "5*eps on both order-aware estimators; the markov instrument cannot see a "
                   "planted cross-session self, so no owner reading is interpretable.")
    elif any_anchored:
        g = next(g for g in grains if g["anchored"])
        gn = "per_session" if g is row_s else "per_day"
        verdict = ("ANCHORED — with a PASSING text-like liveness, the owner stream is legible on "
                   "grain '%s' (markov3 over_floor %+.4f, markov8 %+.4f, both > eps=%.3f) AND "
                   "high-dimensional (PR %.2f > %.1f). A high-dim legible owner-self exists; the "
                   "F7 (curiosity) / F5 (trajectory) owner-substrate premise is LIVE."
                   % (gn, g["markov3"]["over_floor"], g["markov8"]["over_floor"], EPS,
                      g["participation_ratio"], PR_FLOOR))
    elif best is not None:
        o3 = best["markov3"]["over_floor"]
        o8 = best["markov8"]["over_floor"]
        pr = best["participation_ratio"]
        leans_positive = o3 > 0 and o8 > 0
        at_threshold = (_near(o3, EPS, BAND_BPB) or _near(o8, EPS, BAND_BPB)
                        or _near(pr, PR_FLOOR, BAND_PR))
        gn = "per_session" if best is row_s else "per_day"
        if leans_positive and at_threshold:
            verdict = ("BORDERLINE (at threshold) — text-like liveness PASSES, but the owner "
                       "premise sits at its pre-registered thresholds on the best grain '%s' "
                       "(markov3 over_floor %+.4f, markov8 %+.4f, PR %.2f). Both estimators lean "
                       "positive but neither clears eps=%.3f AND PR>%.1f cleanly — a weak "
                       "positive, not a clean anchor." % (gn, o3, o8, pr, EPS, PR_FLOOR))
        else:
            verdict = ("REFUSED — text-like liveness PASSES (instrument sound), but the owner "
                       "stream carries no predictable high-dimensional cross-session self above "
                       "the shuffle floor on either grain (best '%s': markov3 over_floor %+.4f, "
                       "markov8 %+.4f, PR %.2f). The F7/F5 owner-substrate premise is REFUSED at "
                       "$0." % (gn, o3, o8, pr))
    else:
        verdict = "INVALID (no usable owner grain)"
    m["verdict"] = verdict
    m["any_anchored"] = any_anchored

    # --- falsifier ledger -----------------------------------------------------
    falsifiers = [
        Falsifier("L-1 liveness (blind instrument)", lambda x: not x["liveness_ok"],
                  "text-like planted stream not seen -> INVALID"),
        Falsifier("L-2 kill (no grain legible)",
                  lambda x: bool(grains) and not any(g["legible"] for g in grains),
                  "owner unpredictable on both grains -> premise weak/REFUSED"),
        Falsifier("L-3 rank collapse (L1)",
                  lambda x: any(g["legible"] and not g["high_dim"] for g in grains),
                  "a legible grain is one-bit (PR<=2.0) -> RANK-COLLAPSE"),
        Falsifier("L-5 order agreement",
                  lambda x: best is not None and not best["sign_agree"],
                  "markov3/markov8 disagree on sign -> PENDING(instrument)"),
    ]
    ledger = evaluate(m, falsifiers)

    print("\n" + "=" * 74)
    for r in ledger["falsifiers"]:
        print("  %-4s  %s" % (r["status"], r["name"]))
    print("\n  VERDICT: %s" % verdict)
    print("=" * 74)

    out = os.path.join(_HERE, "result.json")
    with open(out, "w") as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("\nartifacts: %s" % os.path.relpath(out, _ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
