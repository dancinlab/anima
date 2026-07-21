"""H_008 — f5-trajectory. Is the owner an individual that is the TRAJECTORY of what it
underwent — a DIRECTIONAL, CUMULATIVE temporal structure — as opposed to a frozen static
cross-session self (which H_005/H_007 already measured)? $0, deterministic.

F5 bets the individual = the trajectory of its history, distinguishable from a frozen
individual. H_005 (ANCHORED) and H_007 (owner legibility, borderline) already established
that STATIC cross-session MI exists. This card asks the residual F5 question: does that
self carry TRAJECTORY structure that a static (Markov-1, time-symmetric) description misses?

Two orthogonal probes, both over the chronological owner session stream
(state/h007::owner_sessions), both against the shuffle floor:

  PROBE A — CUMULATIVE.  Predict session t's prefix P (first P bytes) from the concatenated
    TAILS of the last-N sessions, N in {1,2,4,8}. The context SIZE is held fixed by a
    same-N shuffle control (N random far sessions' tails). over_floor(N) = bpb(P|N-random)
    - bpb(P|N-actual-past) isolates the SPECIFIC recent-past contribution at each depth.
      * If specific-self info lives only in the immediate predecessor (static / Markov-1),
        over_floor SATURATES at N=1: over_floor(8) ~ over_floor(1).
      * If it ACCUMULATES over the recent window (a cumulative trajectory), over_floor
        keeps GROWING with N.

  PROBE B — DIRECTION.  For the SAME target P_t, compare conditioning on the PAST neighbor
    tail_{t-1} vs the FUTURE neighbor tail_{t+1} (time-reversed). Both predict the same
    target, so bpb is directly comparable. direction_signal = bpb(P|future) - bpb(P|past).
      * Pure topical clustering / static co-occurrence is TIME-SYMMETRIC: t is as close to
        t-1 as to t+1, direction_signal ~ 0.
      * A genuine directed trajectory (arrow of time: the past shapes t, t shapes the
        future) is ASYMMETRIC: the past predicts t better, direction_signal > 0.

Controls (pre-registered):
  * L-A / L-B liveness — synthetic streams with a KNOWN cumulative / directional signal
    (literal block echoes, caught by gzip LZ) MUST read strongly positive, else the
    instrument is blind and no owner reading is interpretable.
  * NULL negative control — an i.i.d. random-session stream (no trajectory) MUST read
    over_floor ~ 0 and direction_signal ~ 0, else the instrument hallucinates trajectory.
  * shuffle floor — built into over_floor (A) and into past/future_over (B).

Primary estimator: gzip cond_bpb (the estimator with PROVEN liveness on this substrate;
H_007's markov6 went blind on high-entropy synthetic). markov6 reported as an order-aware
cross-check but does NOT gate the liveness. ppm is omitted (does not scale to owner data
at $0, per H_007). Card frozen 2026-07-16.

Privacy: NO owner message content is written into the repo — only aggregate bpb numbers.

Run: python3 state/h008_f5-trajectory_2026-07-16/run_h008.py
"""

from __future__ import annotations

import functools
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tool"))
sys.path.insert(0, os.path.join(_ROOT, "state", "h005_f3-stream-mi-precheck_2026-07-16"))
sys.path.insert(0, os.path.join(_ROOT, "state", "h007_f7-owner-legibility_2026-07-16"))

from anima_v3 import Falsifier, evaluate
from run_h005 import cond_bpb, cond_bpb_markov, W, P
from run_h007 import owner_sessions

markov6 = functools.partial(cond_bpb_markov, order=6)

# --- frozen inputs (must match the card) --------------------------------------
EPS = 0.02              # decoration threshold in bpb (campaign standard)
LIVE_MULT = 5           # liveness must clear 5*EPS
NS = (1, 2, 4, 8)       # cumulative history depths
MIN_SESSIONS = 40       # need enough targets with an 8-deep past
MAX_TARGETS = 250       # cap for $0 compute (deterministic head slice)
BLK = 256               # synthetic echo-block size


def _med(v):
    v = sorted(v)
    return v[len(v) // 2] if v else 0.0


def _tail(b):
    return b[-W:]


def _pref(b):
    return b[:P]


def _shuffle_idxs(t, n, count):
    """Deterministic FAR (non-neighbor) session indices for the shuffle floor.

    Offset by n//3 (>= 13 for n>=40, well past the +/-8 neighbor window) so the shuffle
    context is the same SIZE (count tails) but carries no genuine adjacency to t."""
    base = (t + n // 3) % n
    out = []
    k = 0
    while len(out) < count:
        j = (base + k) % n
        if not (t - 8 <= j <= t + 8):     # never a real neighbor
            out.append(j)
        k += 1
    return out


# ---------------------------------------------------------------- PROBE A
def probe_cumulative(sessions, est):
    """over_floor(N) for N in NS: does the SPECIFIC recent past help more, and DEEPER, than
    N random far sessions? Growth with N = cumulative trajectory; flat = static/Markov-1."""
    n = len(sessions)
    lo, hi = 8, n - 1                      # targets that have an 8-deep past
    targets = list(range(lo, hi))[:MAX_TARGETS]
    rows = {}
    for N in NS:
        overs = []
        for t in targets:
            pref = _pref(sessions[t][1])
            past_ctx = b"".join(_tail(sessions[t - k][1]) for k in range(N, 0, -1))   # t-N..t-1
            shuf_ctx = b"".join(_tail(sessions[j][1]) for j in _shuffle_idxs(t, n, N))
            b_past = est(pref, past_ctx)
            b_shuf = est(pref, shuf_ctx)
            overs.append(b_shuf - b_past)
        rows[N] = _med(overs)
    growth = rows[8] - rows[1]
    monotone = all(rows[NS[i + 1]] >= rows[NS[i]] - EPS / 2 for i in range(len(NS) - 1))
    return {"over_floor": rows, "growth_8_minus_1": growth, "monotone": monotone,
            "n_targets": len(targets)}


# ---------------------------------------------------------------- PROBE B
def probe_direction(sessions, est):
    """direction_signal = bpb(P_t | future tail_{t+1}) - bpb(P_t | past tail_{t-1}).
    Positive = the past predicts t better than the future does = arrow of time."""
    n = len(sessions)
    targets = list(range(1, n - 1))[:MAX_TARGETS]
    d_sig, past_over, fut_over = [], [], []
    for t in targets:
        pref = _pref(sessions[t][1])
        past = est(pref, _tail(sessions[t - 1][1]))
        future = est(pref, _tail(sessions[t + 1][1]))
        shuf = est(pref, _tail(sessions[_shuffle_idxs(t, n, 1)[0]][1]))
        d_sig.append(future - past)
        past_over.append(shuf - past)
        fut_over.append(shuf - future)
    return {"direction_signal": _med(d_sig), "past_over_floor": _med(past_over),
            "future_over_floor": _med(fut_over), "n_targets": len(targets)}


# ---------------------------------------------------------------- synthetic controls
def _lcg(seed):
    st = seed
    def nxt():
        nonlocal st
        st = (1103515245 * st + 12345) & 0x7FFFFFFF
        return st
    return nxt


def _pad(nxt, k):
    return bytes([(nxt() % 26) + 97 for _ in range(k)])


def planted_cumulative(n=60, seed=11):
    """L-A liveness: prefix_t = echo of the last 8 sessions' blocks (segment j = B_{t-1-j}).
    Deeper history recovers MORE of the prefix -> over_floor STRICTLY grows with N. Each
    session's own block B_t sits inside its TAIL. Literal echoes -> gzip LZ catches them."""
    nxt = _lcg(seed)
    blocks = [bytes([(nxt() % 94) + 33 for _ in range(BLK)]) for _ in range(n)]
    chunks = []
    nseg = P // BLK                                     # 8 segments in the prefix
    for t in range(n):
        segs = [blocks[t - 1 - j] if t - 1 - j >= 0 else _pad(nxt, BLK) for j in range(nseg)]
        prefix = b"".join(segs)                         # P bytes: [B_{t-1}|B_{t-2}|...|B_{t-8}]
        mid = _pad(nxt, W + P - BLK - 1000)             # push B_t into the tail region
        end = _pad(nxt, 1000)
        chunks.append((f"c{t}", prefix + mid + blocks[t] + end))   # tail contains B_t
    return chunks


def planted_directional(n=60, seed=23):
    """L-B liveness: prefix_t = full echo of the PREVIOUS session's block B_{t-1} (P bytes);
    each session's own block B_t sits in its TAIL. Past neighbor fully predicts t; the future
    neighbor carries B_{t+1}, unrelated -> strong forward/backward asymmetry."""
    nxt = _lcg(seed)
    blocks = [bytes([(nxt() % 94) + 33 for _ in range(P)]) for _ in range(n)]
    chunks = []
    for t in range(n):
        prefix = blocks[t - 1] if t - 1 >= 0 else _pad(nxt, P)
        mid = _pad(nxt, W - 1000)
        end = _pad(nxt, 1000)
        chunks.append((f"d{t}", prefix + mid + blocks[t] + end))   # tail contains B_t (P bytes)
    return chunks


def planted_null(n=60, seed=37):
    """Negative control: i.i.d. random sessions, NO trajectory. over_floor and
    direction_signal MUST read ~0 (the instrument does not hallucinate trajectory)."""
    nxt = _lcg(seed)
    chunks = []
    for t in range(n):
        body = bytes([(nxt() % 94) + 33 for _ in range(W + P + 1000)])
        chunks.append((f"z{t}", body))
    return chunks


def main() -> int:
    print("=" * 78)
    print("H_008 — f5-trajectory · directed/cumulative temporal self vs static MI ($0)")
    print("=" * 78)
    print(f"W={W} tail · P={P} prefix · eps={EPS} · N in {NS}\n")
    m = {}

    # --- liveness + null on gzip (the estimator with proven liveness here) -------------
    est = cond_bpb
    la = probe_cumulative(planted_cumulative(), est)
    lb = probe_direction(planted_directional(), est)
    nz_a = probe_cumulative(planted_null(), est)
    nz_b = probe_direction(planted_null(), est)
    m["liveness_cumulative"] = la
    m["liveness_directional"] = lb
    m["null_cumulative"] = nz_a
    m["null_directional"] = nz_b
    liveA_ok = la["growth_8_minus_1"] > LIVE_MULT * EPS and la["monotone"]
    liveB_ok = lb["direction_signal"] > LIVE_MULT * EPS
    nullA_ok = abs(nz_a["growth_8_minus_1"]) <= EPS
    nullB_ok = abs(nz_b["direction_signal"]) <= EPS
    m["liveA_ok"], m["liveB_ok"] = liveA_ok, liveB_ok
    m["nullA_ok"], m["nullB_ok"] = nullA_ok, nullB_ok
    print(f"[L-A cumulative liveness] over_floor {{{', '.join(f'{k}:{v:+.3f}' for k,v in la['over_floor'].items())}}}"
          f"  growth(8-1)={la['growth_8_minus_1']:+.4f} monotone={la['monotone']} -> ok={liveA_ok}")
    print(f"[L-B direction liveness]  direction_signal={lb['direction_signal']:+.4f} "
          f"(past_over {lb['past_over_floor']:+.3f} / future_over {lb['future_over_floor']:+.3f}) -> ok={liveB_ok}")
    print(f"[NULL negative]           cumulative growth={nz_a['growth_8_minus_1']:+.4f} ok={nullA_ok} · "
          f"direction={nz_b['direction_signal']:+.4f} ok={nullB_ok}")

    instrument_ok = liveA_ok and liveB_ok and nullA_ok and nullB_ok

    sessions = owner_sessions()
    m["n_sessions"] = len(sessions)
    print(f"\ngenuine-owner sessions (>= {W+P}B): {len(sessions)}")
    if len(sessions) < MIN_SESSIONS:
        m["verdict"] = f"INVALID (only {len(sessions)} sessions, need >= {MIN_SESSIONS})"
        print(f"\n  VERDICT: {m['verdict']}")
        _save(m)
        return 0

    # --- owner readings: primary gzip + markov6 cross-check --------------------------
    for name, e in (("gzip", cond_bpb), ("markov6", markov6)):
        ca = probe_cumulative(sessions, e)
        cb = probe_direction(sessions, e)
        m[f"owner_cumulative_{name}"] = ca
        m[f"owner_direction_{name}"] = cb
        print(f"\n[owner · {name}] cumulative over_floor "
              f"{{{', '.join(f'{k}:{v:+.4f}' for k,v in ca['over_floor'].items())}}}")
        print(f"              growth(8-1)={ca['growth_8_minus_1']:+.4f} monotone={ca['monotone']}")
        print(f"[owner · {name}] direction_signal={cb['direction_signal']:+.4f} "
              f"(past_over {cb['past_over_floor']:+.4f} / future_over {cb['future_over_floor']:+.4f})")

    # PRE-REGISTERED verdict keys off the PRIMARY (gzip); markov6 is a cross-check.
    ca = m["owner_cumulative_gzip"]
    cb = m["owner_direction_gzip"]
    static_self = ca["over_floor"][1] > EPS                 # is there ANY static self (N=1) at all?
    cumulative = ca["growth_8_minus_1"] > EPS               # does the past ACCUMULATE beyond N=1?
    directional = cb["direction_signal"] > EPS              # arrow of time?
    m["static_self"] = static_self
    m["cumulative"] = cumulative
    m["directional"] = directional
    m["instrument_ok"] = instrument_ok

    # markov6 agreement (sign) as a robustness note
    m["cumulative_agree"] = (ca["growth_8_minus_1"] > 0) == (m["owner_cumulative_markov6"]["growth_8_minus_1"] > 0)
    m["directional_agree"] = (cb["direction_signal"] > 0) == (m["owner_direction_markov6"]["direction_signal"] > 0)

    falsifiers = [
        Falsifier("C-live (blind instrument)", lambda x: not x["instrument_ok"],
                  "liveness/null controls fail -> PENDING(instrument)"),
        Falsifier("C-static (no self at all)", lambda x: not x["static_self"],
                  "no static self even at N=1 -> nothing for a trajectory to be OF"),
        Falsifier("C-cumulative-null", lambda x: x["static_self"] and not x["cumulative"],
                  "over_floor saturates at N=1 -> no cumulative depth"),
        Falsifier("C-direction-null", lambda x: x["static_self"] and not x["directional"],
                  "time-symmetric -> no arrow of time"),
    ]
    ledger = evaluate(m, falsifiers)

    if not instrument_ok:
        verdict = (f"PENDING(instrument) — controls failed (liveA={liveA_ok} liveB={liveB_ok} "
                   f"nullA={nullA_ok} nullB={nullB_ok}); owner reading not interpretable.")
    elif not static_self:
        verdict = (f"F5-REFUSED (no self) — even the immediate predecessor carries no over-floor "
                   f"self (N=1 over_floor {ca['over_floor'][1]:+.4f} <= {EPS}); there is no static "
                   f"cross-session self here for a trajectory to be OF at $0.")
    elif cumulative and directional:
        verdict = (f"F5-LIVE (directed trajectory) — the recent past ACCUMULATES (over_floor grows "
                   f"{ca['over_floor'][1]:+.4f}->{ca['over_floor'][8]:+.4f}, growth {ca['growth_8_minus_1']:+.4f}"
                   f" > {EPS}) AND time is ASYMMETRIC (direction_signal {cb['direction_signal']:+.4f} > {EPS}: "
                   f"the past predicts t better than the future). The owner-self carries directed "
                   f"trajectory structure a static/time-symmetric description misses. F5 premise LIVE.")
    elif cumulative and not directional:
        verdict = (f"F5-WEAK (undirected drift) — the recent past accumulates (growth "
                   f"{ca['growth_8_minus_1']:+.4f} > {EPS}) but time is SYMMETRIC (direction_signal "
                   f"{cb['direction_signal']:+.4f} <= {EPS}). This is a topical WINDOW / smooth drift, "
                   f"not a directed arrow-of-time trajectory. F5 adds a recency-window over F7 but no "
                   f"directed self.")
    else:
        verdict = (f"F5-REFUSED (static) — a static self exists at N=1 (over_floor {ca['over_floor'][1]:+.4f}) "
                   f"but it does NOT accumulate (growth {ca['growth_8_minus_1']:+.4f} <= {EPS}, saturates "
                   f"at N=1) and is time-SYMMETRIC (direction_signal {cb['direction_signal']:+.4f} <= {EPS}). "
                   f"The owner-self is a frozen Markov-1 cross-session MI; F5's TRAJECTORY claim adds "
                   f"nothing over F7's legibility on this substrate at $0.")
    m["verdict"] = verdict

    print("\n" + "=" * 78)
    for r in ledger["falsifiers"]:
        print(f"  {r['status']:4s}  {r['name']}")
    print(f"  agree(gzip vs markov6): cumulative={m['cumulative_agree']} direction={m['directional_agree']}")
    print(f"\n  VERDICT: {verdict}")
    print("=" * 78)
    _save(m)
    print(f"\nartifacts: {os.path.relpath(os.path.join(_HERE, 'result.json'), _ROOT)}")
    return 0


def _save(m):
    with open(os.path.join(_HERE, "result.json"), "w") as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
        f.write("\n")


if __name__ == "__main__":
    sys.exit(main())
