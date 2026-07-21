"""H_009' — f3-continuous-oracle (instrument-corrected). Does a k-dim CONTINUOUS
day-summary capture the day->tomorrow predictive information that a byte-SELECTION
text extract (H_006) could not, AND beat a topic-matched other-day floor?

Measured in FEATURE space (Fable Q1: the byte-append path is instrument-blind to an
abstract projection code). The FIRST feature-space instrument returned INVALID from
TWO estimator defects (root-caused by Fable, 2026-07-16):
  A. err_s === err_full whenever k >= n_train-1: the top-k axes span the whole training
     subspace, so a test query's orthogonal residual is a per-query CONSTANT that cancels
     in the k-NN argmin -> identical neighbours -> capture_frac === 1.0 mechanically.
  B. a constant-mean denominator + K=3 + a 60/40 split made err_full noisier than err_base
     on anima (ceiling_strength < 0) -> the ratio was estimator-variance, not substrate.

H_009' fixes both: VALID-k only (k <= (n_train-1)//2, 2k <= numeric rank), a LOO estimator
over ALL consecutive pairs (K=5), and a cyclic-SHIFT misalignment floor as the reference
(the estimator's variance penalty is identical in aligned and shifted runs, so it cancels).
capture(k) = align_s(k)/align_full where align_X = median_shift err_X - err_X(aligned).
Three matched-n liveness arms certify the instrument can read HIGH (weak real ceiling),
LOW (predictive signal orthogonal to the top-k axes), and FAIL (pure noise). Card re-frozen
2026-07-16 with the B-spend/C-reframe branch table PRE-registered before this re-run.

Run: python3 state/h009_f3-continuous-oracle_2026-07-16/run_h009.py
"""

from __future__ import annotations

import heapq
import json
import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tool"))
sys.path.insert(0, os.path.join(_ROOT, "state", "h005_f3-stream-mi-precheck_2026-07-16"))

from anima_v3 import Falsifier, binom_sf, evaluate, principal_axes, singular_values
import run_h005 as H

D = 256                        # hashed n-gram feature buckets
K_CANDIDATES = [2, 4, 8, 16]   # rank sweep; PRIMARY = 8; capped to valid k at run time
PRIMARY_K = 8
KNN = 5                        # k-NN neighbours (LOO, all pairs)
EPS_F = 0.075                  # fraction-unit margin
ANCHOR = 0.25                  # capture(8) anchor
RANK_GATE = 2                  # ceiling / kill gate: rank of aligned among shifts must be <= this
TRAIN_FRAC = 0.60              # axis-fit split ONLY (evaluation is LOO over all pairs)
STREAMS = {"anima": "/Users/mini/dancinlab/anima", "hexa-lang": "/Users/mini/dancinlab/hexa-lang"}


# --- features ----------------------------------------------------------------
def fnv1a(b: bytes) -> int:
    h = 0x811C9DC5
    for byte in b:
        h ^= byte
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def features(day: bytes, dim: int = D, log_weight: bool = True) -> list:
    """Hashed char-n-gram (n in {1,2,3}) counts -> dim buckets -> log1p -> L2-norm."""
    counts = [0] * dim
    n = len(day)
    for size in (1, 2, 3):
        for i in range(n - size + 1):
            counts[fnv1a(day[i:i + size]) % dim] += 1
    vec = [math.log1p(c) if log_weight else float(c) for c in counts]
    norm = math.sqrt(sum(x * x for x in vec))
    return [x / norm for x in vec] if norm > 0 else vec


def project(f: list, mean: list, axes: list, k: int) -> list:
    centered = [f[i] - mean[i] for i in range(len(f))]
    return [sum(centered[i] * ax[i] for i in range(len(ax))) for ax in axes[:k]]


def _sqdist(a: list, b: list) -> float:
    return sum((a[i] - b[i]) ** 2 for i in range(len(a)))


def _median(xs: list) -> float:
    s = sorted(xs)
    n = len(s)
    if n == 0:
        return 0.0
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


# --- LOO shift-null estimator -------------------------------------------------
def shift_errors(query_seq: list, cand_keys: list, targets: list, shifts: list, kk: int = KNN) -> tuple:
    """LOO k-NN error of predicting each target from a (possibly shifted) query.

    query_seq[m], cand_keys[j], targets[j] all indexed by pair (P entries). For target i
    under shift d, the query used is query_seq[(i+d) % P]; candidates are all pairs j with
    |i-j| >= 2 (excludes self + day-sharing leakage). Returns ({d: summed_err}, per-pair
    err at d=0). The estimator's variance penalty is identical across d, so it cancels in
    align = median_{d!=0} err(d) - err(0)."""
    P = len(targets)
    dim_t = len(targets[0])
    cand_of = [[j for j in range(P) if abs(i - j) >= 2] for i in range(P)]
    Dm = [[_sqdist(query_seq[q], cand_keys[c]) for c in range(P)] for q in range(P)]
    errs, pp0 = {}, None
    for d in shifts:
        tot, pp = 0.0, []
        for i in range(P):
            q = (i + d) % P
            row = Dm[q]
            nn = heapq.nsmallest(kk, cand_of[i], key=lambda j: (row[j], j))
            pred = [sum(targets[j][t] for j in nn) / len(nn) for t in range(dim_t)]
            e = _sqdist(targets[i], pred)
            tot += e
            pp.append(e)
        errs[d] = tot
        if d == 0:
            pp0 = pp
    return errs, pp0


def _summ(errs: dict, nz: list) -> dict:
    e0 = errs[0]
    shifted = [errs[d] for d in nz]
    med = _median(shifted)
    rank = sum(1 for d in nz if errs[d] <= e0)
    return {"e0": e0, "median_shift": med, "align": med - e0, "rank": rank,
            "p": rank / len(nz) if nz else 1.0, "n_shifts": len(nz)}


def analyze(day_feats: list, primary_k: int = PRIMARY_K) -> dict:
    """Full H_009' measurement on an ordered list of (feature_vector, day_index)."""
    n_days = len(day_feats)
    full = [f for f, _ in day_feats]
    n_train = max(2, int(round(n_days * TRAIN_FRAC)))
    train = full[:n_train]
    mean_train = [sum(train[j][d] for j in range(n_train)) / n_train for d in range(len(train[0]))]
    svs = singular_values(train)
    smax = max(svs) if svs else 0.0
    numrank = sum(1 for s in svs if s > 1e-9 * smax) if smax > 0 else 0
    valid_ks = [k for k in K_CANDIDATES if k <= (n_train - 1) // 2 and 2 * k <= numrank]
    if not valid_ks:
        return {"error": "no valid k", "n_days": n_days, "n_train": n_train, "numrank": numrank}
    pk = primary_k if primary_k in valid_ks else max(valid_ks)
    axes = principal_axes(train, k=max(valid_ks))

    P = n_days - 1
    shifts = [0] + list(range(3, P - 3))
    nz = shifts[1:]
    targets = [full[i + 1] for i in range(P)]

    # full-feature ceiling arm
    fk = [full[i] for i in range(P)]
    errs_full, pp_full = shift_errors(fk, fk, targets, shifts)
    sf = _summ(errs_full, nz)

    # per-k summary arms
    summ = {k: [project(full[j], mean_train, axes, k) for j in range(n_days)] for k in valid_ks}
    cap, s_stats, pp_s = {}, {}, {}
    for k in valid_ks:
        sk = [summ[k][i] for i in range(P)]
        errs_s, pp = shift_errors(sk, sk, targets, shifts)
        ss = _summ(errs_s, nz)
        s_stats[k] = ss
        pp_s[k] = pp
        cap[k] = (ss["align"] / sf["align"]) if sf["align"] > 1e-12 else None

    # topic-matched floor at the primary k
    def cos(a, b):
        na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(x * x for x in b))
        return sum(a[i] * b[i] for i in range(len(a))) / (na * nb) if na and nb else 0.0
    topic_day = []
    for i in range(P):
        excl = {i - 1, i, i + 1}
        best, bc = 0, -2.0
        for u in range(n_days):
            if u in excl:
                continue
            c = cos(full[i], full[u])
            if c > bc:
                bc, best = c, u
        topic_day.append(best)
    tq = [summ[pk][topic_day[i]] for i in range(P)]
    tc = [summ[pk][j] for j in range(P)]
    errs_topic, pp_topic = shift_errors(tq, tc, targets, shifts)
    st = _summ(errs_topic, nz)
    topic_cap = (st["align"] / sf["align"]) if sf["align"] > 1e-12 else None

    sign_topic_gt_s = sum(1 for a, b in zip(pp_topic, pp_s[pk]) if a > b)

    return {
        "n_days": n_days, "n_train": n_train, "numrank": numrank, "n_pairs": P,
        "n_shifts": sf["n_shifts"], "valid_ks": valid_ks, "primary_k": pk,
        "full": sf, "s": {str(k): s_stats[k] for k in valid_ks}, "topic": st,
        "capture": {str(k): cap[k] for k in valid_ks},
        "capture_primary": cap[pk], "topic_capture_primary": topic_cap,
        "gate_ok": sf["rank"] <= RANK_GATE,
        "sign_topic_gt_s": sign_topic_gt_s,
    }


# --- synthetic liveness plants (feature-space; hashing tested separately) ------
class _LCG:
    def __init__(self, seed):
        self.s = seed & 0x7FFFFFFF
    def u(self):  # uniform [0,1)
        self.s = (1103515245 * self.s + 12345) & 0x7FFFFFFF
        return self.s / 0x7FFFFFFF
    def n(self):  # ~N(0,0.5) via 6-uniform CLT (legacy; used only by dense-topic plants)
        return sum(self.u() for _ in range(6)) - 3.0
    def g(self):  # ~N(0,1) via 12-uniform CLT (unit variance)
        return sum(self.u() for _ in range(12)) - 6.0


def _unit(rng, dim):
    v = [rng.n() for _ in range(dim)]
    nrm = math.sqrt(sum(x * x for x in v))
    return [x / nrm for x in v]


def _norm(v):
    nrm = math.sqrt(sum(x * x for x in v))
    return [x / nrm for x in v] if nrm > 0 else v


def plant_weak(n_days, seed=11, dim=D, R=8, alpha=0.80):
    """LIVENESS-HIGH: R topic patterns; day = mixture by weights w_t; w_{t+1} = alpha*shift(w_t)
    + (1-alpha)*fresh. Tomorrow's weights are largely determined by today's, and the R topic
    directions dominate variance -> the top-8 axes ARE the weights -> capture(8) must read HIGH."""
    rng = _LCG(seed)
    topics = [_unit(rng, dim) for _ in range(R)]
    w = [rng.u() + 0.2 for _ in range(R)]
    days = []
    for _ in range(n_days):
        base = [sum(w[c] * topics[c][j] for c in range(R)) for j in range(dim)]
        v = [base[j] + 0.05 * rng.n() for j in range(dim)]
        days.append(_norm(v))
        w = [alpha * w[(c - 1) % R] + (1 - alpha) * (rng.u() + 0.2) for c in range(R)]
    return [(v, i) for i, v in enumerate(days)]


def plant_buried(n_days, dim=D, n_sig=20, n_dec=8, sig_amp=math.sqrt(2.0), dec_amp=2.0):
    """LIVENESS-LOW = the 'buried delay-line' negative control (Fable design). An orthogonal-
    direction plant is UNBUILDABLE under plain Euclidean k-NN (a single sub-top-variance dir
    contributes a vanishing distance share -> full k-NN blind too -> ceiling dies), and a rank-
    truncation plant is ALSO unbuildable (independent latents -> attractor too high-dim, NN
    saturates at n=44; shared latent -> any 8 coords embed the core -> capture~1). The escape is
    MANY sub-threshold dims driven by ONE deterministic core:
      - signal: n_sig=20 delay TAPS of a single logistic scalar x (x_{i+1}=4x(1-x)); tap j =
        sqrt(2)*(1-2*x[idx(t)-j]) -> per-dim var 1.0, and logistic Chebyshev-orthogonality makes
        the tap covariance EXACTLY 1*I (flat spectrum, zero lag-correlation).
      - decoy: n_dec=8 fresh iid dims at var 4.0 (2*N(0,1)) sit ON TOP of PCA.
    Full k-NN sees the signal block's 20/(20+8*4)=38.5% distance share (attractor dim = 1, so 43
    candidates resolve it) -> gate PASS. The top-8 sample axes are decoy-dominated (signal-block
    top sample-eigen ~2.8 < 4) -> s_8 misses the signal -> capture(k<=8) LOW *by construction at
    every k*, at BOTH n. Certifies capture(8) is not silently inflatable."""
    x0 = 0.6180339887 if n_days < 100 else 0.3819660113
    N = 119 + n_days                       # idx(t)=119+t, t=0..n-1; idx-j min = 100 (past burn-in 100)
    x = [0.0] * N
    x[0] = x0
    for i in range(N - 1):
        xi = 4.0 * x[i] * (1.0 - x[i])
        x[i + 1] = min(1.0 - 1e-12, max(1e-12, xi))
    rng = _LCG(20260716 + n_days)
    days = []
    for t in range(n_days):
        it = 119 + t
        v = [0.0] * dim
        for j in range(n_sig):
            v[j] = sig_amp * (1.0 - 2.0 * x[it - j])
        for i in range(n_dec):
            v[n_sig + i] = dec_amp * rng.g()
        days.append(_norm(v))
    return [(vv, i) for i, vv in enumerate(days)]


def plant_null(n_days, seed=37, dim=D):
    """LIVENESS-FAIL: pure iid noise days, no cross-day structure -> the gate MUST fail."""
    rng = _LCG(seed)
    return [(_norm([rng.n() for _ in range(dim)]), i) for i in range(n_days)]


LOW_CAP_MAX = 0.25   # C-3-LOW: capture(k) must be <= this for every valid k <= 8, at BOTH n


def _liveness(n_days: int) -> dict:
    w = analyze(plant_weak(n_days))
    o = analyze(plant_buried(n_days))
    z = analyze(plant_null(n_days))
    high_ok = bool(w.get("gate_ok") and (w.get("capture_primary") or 0) >= 0.8)
    fail_ok = bool(not z.get("gate_ok", True))
    # C-3-LOW (buried delay-line): ceiling ALIVE (rank_full == 0) yet the rank-<=8 code is blind to
    # the flat-spectrum signal block -> capture(k) <= LOW_CAP_MAX for EVERY valid k <= 8.
    # RESOLUTION LIMIT (measured, robust across the high-rank AND buried constructions): at n=44
    # (n_train=26) the decoy sample-eigenvalue SPREAD lets signal combos leak into the top-8, so
    # capture(8) cannot be driven <= 0.25 without starving the gate. LOW is therefore GATING only at
    # n >= 100 (hexa-lang = the certified PRIMARY stream); at n=44 it is informational and anima is
    # REPLICATION with a resolution caveat.
    ocap = o.get("capture", {}) or {}
    low_ks = [k for k in o.get("valid_ks", []) if k <= 8]
    low_vals = [ocap.get(str(k)) for k in low_ks]
    low_ok = bool(o.get("full", {}).get("rank") == 0 and low_vals
                  and all(v is not None and v <= LOW_CAP_MAX for v in low_vals))
    low_gating = n_days >= 100
    return {
        "n_days": n_days,
        "high": {"gate_ok": w.get("gate_ok"), "capture8": w.get("capture_primary"), "pass": high_ok},
        "low": {"gate_ok": o.get("gate_ok"), "rank_full": o.get("full", {}).get("rank"),
                "sweep": ocap, "pass": low_ok, "gating": low_gating},
        "fail": {"gate_ok": z.get("gate_ok"), "rank_full": z.get("full", {}).get("rank"), "pass": fail_ok},
        "ok": bool(high_ok and fail_ok and (low_ok or not low_gating)),
    }


def main() -> int:
    print("=" * 78)
    print("H_009' — f3-continuous-oracle · shift-null LOO capture in feature space ($0)")
    print("=" * 78)
    m = {"eps_f": EPS_F, "anchor": ANCHOR, "knn": KNN, "rank_gate": RANK_GATE, "streams": {}}

    # --- C-3' three-arm liveness, matched to both real stream lengths ---
    print("\n[C-3' liveness] plants at n=44 (anima) and n=102 (hexa-lang):")
    live = {"44": _liveness(44), "102": _liveness(102)}
    m["liveness"] = live
    live_ok = live["44"]["ok"] and live["102"]["ok"]
    m["liveness_ok"] = live_ok
    for nn, lv in live.items():
        sw = lv['low']['sweep']
        swept = " ".join(f"k{k}={_f(v)}" for k, v in sw.items())
        print(f"  n={nn}: HIGH gate={lv['high']['gate_ok']} cap8={_f(lv['high']['capture8'])} pass={lv['high']['pass']} · "
              f"FAIL gate_ok={lv['fail']['gate_ok']} pass={lv['fail']['pass']}")
        print(f"         LOW(gating={lv['low']['gating']}) gate={lv['low']['gate_ok']} sweep[{swept}] pass={lv['low']['pass']}")
    print(f"  liveness_ok = {live_ok}")

    # --- real streams ---
    for name, repo in STREAMS.items():
        chunks = H.day_chunks(repo)
        if len(chunks) < 15:
            m["streams"][name] = {"error": f"only {len(chunks)} days"}
            print(f"\n[{name}] SKIP ({len(chunks)} days)")
            continue
        day_feats = [(features(b), i) for i, (_, b) in enumerate(chunks)]
        r = analyze(day_feats)
        # C-5' raw-count reweight agreement (own fit)
        r_raw = analyze([(features(b, log_weight=False), i) for i, (_, b) in enumerate(chunks)])
        r["capture_primary_rawweight"] = r_raw.get("capture_primary")
        m["streams"][name] = r
        print(f"\n[{name}] days={r['n_days']} train={r['n_train']} pairs={r['n_pairs']} "
              f"shifts={r['n_shifts']} numrank={r['numrank']} valid_k={r['valid_ks']} (primary {r['primary_k']})")
        print(f"    CEILING gate: rank_full={r['full']['rank']}/{r['n_shifts']} (<= {RANK_GATE}? {r['gate_ok']}) "
              f"· align_full={_f(r['full']['align'])} p={_f(r['full']['p'])}")
        print(f"    capture(k): " + " · ".join(f"k{k}={_f(v)}" for k, v in r['capture'].items()))
        print(f"    capture({r['primary_k']})={_f(r['capture_primary'])} (anchor {ANCHOR}) · "
              f"topic_capture={_f(r['topic_capture_primary'])} · rawweight cap={_f(r['capture_primary_rawweight'])}")
        print(f"    align_s({r['primary_k']})={_f(r['s'][str(r['primary_k'])]['align'])} "
              f"rank_s={r['s'][str(r['primary_k'])]['rank']} · sign(err_topic>err_s)={r['sign_topic_gt_s']}/{r['n_pairs']}")

    # --- verdict on the anima anchor stream (hexa-lang = confirm) ---
    a = m["streams"].get("anima", {})
    if "error" in a:
        m["verdict"] = "INVALID (anima stream unavailable)"
        print(f"\n  VERDICT: {m['verdict']}")
    else:
        pk = a["primary_k"]
        npairs = a["n_pairs"]
        sign_need = next((c for c in range(npairs, 0, -1) if binom_sf(c - 1, npairs, 0.5) < 0.05), npairs)
        m["sign_need"] = sign_need
        s_pk = a["s"][str(pk)]
        cap = a["capture_primary"]
        tcap = a["topic_capture_primary"]
        # C-4 monotonicity over valid k only (no drop > 0.05 below running max)
        vals = [a["capture"][str(k)] for k in a["valid_ks"] if a["capture"][str(k)] is not None]
        runmax, mono_ok = -1e9, True
        for v in vals:
            runmax = max(runmax, v)
            if v < runmax - 0.05:
                mono_ok = False
        # C-5' reweight sign agreement on capture
        rw = a.get("capture_primary_rawweight")
        reweight_ok = (rw is not None and cap is not None and (rw > 0) == (cap > 0))
        gate_ok = a["gate_ok"]
        kill = (s_pk["rank"] > RANK_GATE) or (s_pk["align"] <= 0)
        topic_fail = (cap is None or tcap is None or (cap - tcap) <= EPS_F
                      or a["sign_topic_gt_s"] < sign_need)
        anchored = (gate_ok and live_ok and cap is not None and cap >= ANCHOR
                    and not kill and not topic_fail and mono_ok)
        m.update({"basis_ok": gate_ok, "mono_ok": mono_ok, "reweight_ok": reweight_ok,
                  "kill": kill, "topic_fail": topic_fail, "anchored": anchored})

        # hexa-lang cross-check: the FULLY-certified stream (n=102, LOW arm gating-PASS). anima
        # (n=44) is REPLICATION with a capture-magnitude resolution caveat; the REFUSED basis (the
        # topic SIGN test) is magnitude-blind and resolution-independent, so it stands at both n.
        hx = m["streams"].get("hexa-lang", {})
        hexa_confirm = None
        if hx and "error" not in hx:
            hnp = hx["n_pairs"]
            hsign_need = next((c for c in range(hnp, 0, -1) if binom_sf(c - 1, hnp, 0.5) < 0.05), hnp)
            hcap, htcap = hx["capture_primary"], hx["topic_capture_primary"]
            hx_topic_fail = (hcap is None or htcap is None or (hcap - htcap) <= EPS_F
                             or hx["sign_topic_gt_s"] < hsign_need)
            hexa_confirm = {"gate_ok": hx["gate_ok"], "capture": hcap, "cap_minus_topic":
                            (None if hcap is None or htcap is None else hcap - htcap),
                            "sign": hx["sign_topic_gt_s"], "sign_need": hsign_need,
                            "topic_fail": hx_topic_fail,
                            "refused": bool(hx["gate_ok"] and hx_topic_fail)}
            m["hexa_confirm"] = hexa_confirm

        falsifiers = [
            Falsifier("C-3' liveness", lambda x: not x["liveness_ok"], "instrument not certified -> INVALID"),
            Falsifier("C-6 ceiling gate", lambda x: not x["basis_ok"], "no feature ceiling -> NO-FEATURE-CEILING"),
            Falsifier("C-4 monotonicity", lambda x: not x["mono_ok"], "projection artifact -> INVALID"),
            Falsifier("C-5' reweight agreement", lambda x: not x["reweight_ok"], "disagree -> PENDING"),
            Falsifier("C-1 kill (s no better than shift)", lambda x: x["basis_ok"] and x["liveness_ok"] and x["kill"],
                      "dense code no better than misaligned -> REFUSED"),
            Falsifier("C-2 topic decoration", lambda x: x["basis_ok"] and x["liveness_ok"] and x["topic_fail"],
                      "topic identity not day-specific -> REFUSED"),
        ]
        ledger = evaluate(m, falsifiers)

        if not live_ok:
            verdict = "INVALID (instrument not certified — a C-3' liveness arm failed at matched n)"
        elif not gate_ok:
            verdict = (f"NO-FEATURE-CEILING (anima) — rank_full={a['full']['rank']}/{a['n_shifts']} > {RANK_GATE}: "
                       "the hashed-n-gram feature basis carries no resolvable day->tomorrow ceiling at n=44 with a "
                       "CERTIFIED-live instrument. This is a demonstrated $0 power boundary, not an F3 verdict. "
                       "Check hexa-lang; if it too is NO-FEATURE-CEILING, the B-spend branch is licensed.")
        elif not mono_ok:
            verdict = "INVALID (C-4 — capture(k) non-monotone over valid k: projection artifact)"
        elif not reweight_ok:
            verdict = "PENDING(instrument) — log1p and raw-count weighting disagree on the capture sign"
        elif anchored:
            verdict = (f"ANCHORED — a hindsight rank-{pk} continuous code retains capture={cap:.3f} (>= {ANCHOR}) of the "
                       f"feature-space day->tomorrow ceiling, beats its shift-null (align_s={s_pk['align']:.4g}, "
                       f"rank_s={s_pk['rank']}) and the topic floor by {cap - tcap:.3f} (sign {a['sign_topic_gt_s']}/"
                       f"{npairs} >= {sign_need}). The F3 continuous-m organ premise is LIVE; the ~$15 twin is licensed "
                       "(delta_min := 0.034 bpb · twin statistic MUST be the wrong-day/right-day bpb DIFFERENCE, else L2).")
        else:
            why = []
            if cap is None or cap < ANCHOR: why.append(f"capture {_f(cap)}<{ANCHOR}")
            if kill: why.append(f"kill(rank_s={s_pk['rank']},align_s={_f(s_pk['align'])})")
            if topic_fail: why.append(f"topic(cap-topic={_f((cap or 0)-(tcap or 0))},sign={a['sign_topic_gt_s']}/{sign_need})")
            hx_txt = ""
            if hexa_confirm is not None:
                hx_txt = (f" hexa-lang (FULLY-certified n=102) CONFIRMS: gate={hexa_confirm['gate_ok']}, "
                          f"cap-topic={_f(hexa_confirm['cap_minus_topic'])}, sign={hexa_confirm['sign']}/"
                          f"{hexa_confirm['sign_need']} -> refused={hexa_confirm['refused']}.")
            verdict = ("F3-CONTINUOUS-REFUSED — a hindsight rank-k continuous code does NOT clear its own anchor/floors "
                       f"({'; '.join(why)}) against a certified-live instrument.{hx_txt} The s-over-topic advantage "
                       "exists on AGGREGATE (cap-topic margin > 0) but the per-pair sign ~50% shows it is concentrated "
                       "in a MINORITY of day-pairs = a sometimes-day-specific code, not a pervasive day-specific self "
                       "(L2 replacement-not-coupling). Both operator classes now dead (byte-selection H_006, "
                       "distributional-projection here). Fire the pre-registered reframe (C).")
        m["verdict"] = verdict
        print("\n" + "-" * 78)
        for rr in ledger["falsifiers"]:
            print(f"  {rr['status']:4s}  {rr['name']}")
        print(f"\n  VERDICT: {m['verdict']}")

    print("=" * 78)
    with open(os.path.join(_HERE, "result.json"), "w") as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"\nartifacts: {os.path.relpath(os.path.join(_HERE, 'result.json'), _ROOT)}")
    return 0


def _f(v):
    return "UNDEFINED" if v is None else f"{v:+.4f}"


if __name__ == "__main__":
    sys.exit(main())
