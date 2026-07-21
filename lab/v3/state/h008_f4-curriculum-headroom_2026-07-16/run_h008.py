"""H_008 — f4-curriculum-headroom. Does corpus SELECTION (a curriculum) have
headroom on held-out capability BEFORE building a learned acquisition policy —
and, decisively, is that headroom anything MORE than a $0 frozen n-gram retriever
already delivers? $0, deterministic. The F4 (corpus-farmer) premise precursor,
in the H_005/H_006 mold: measure the ceiling before the organ.

F4 claims: a LEARNED acquisition policy pi picks the next training batch; the self
= the cumulative curriculum; reward = improvement on a frozen probe (capability).
The hindsight-optimal selection is the CEILING on any learned pi (hindsight >=
learned, exactly the H_006 logic). We measure, at matched byte budget, on a
heterogeneous real corpus (3 developer git streams = 3 domains):

  capability(selection) := bpb(T | concat(selected chunks) as prime)   [lower=better]

using the H_005 order-aware estimators (markov6 authority, ppm confirm, gzip
reported). Arms per target T:
  ORACLE  = greedy hindsight selection (min bpb(T|prime))  -> the CEILING.
  OVERLAP = top-k by 6-gram overlap with T -> the FROZEN n-gram retriever (l11).
  RANDOM  = deterministic shuffle top-k -> the floor.
  ANTI    = k least-overlapping chunks -> bounds/negative control.

Three decisive quantities:
  headroom   = bpb(T|RANDOM) - bpb(T|ORACLE)          (is there ANY selection lever?)
  ceil_capt  = [bpb(T|RANDOM)-bpb(T|OVERLAP)] / headroom  (does a $0 frozen n-gram
               statistic already capture the ceiling? -> the l11 tautology gate)
  transfer   = [bpb(T2|RANDOM)-bpb(T2|ORACLE_for_T1)] /
               [bpb(T2|RANDOM)-bpb(T2|ORACLE_for_T2)]     (does selecting-for-T1
               generalize to a disjoint T2, or is it target-specific = Goodhart?)

Run: python3 state/h008_f4-curriculum-headroom_2026-07-16/run_h008.py
Card frozen 2026-07-16. stdlib only, no network, $0.
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tool"))
sys.path.insert(0, os.path.join(_ROOT, "state", "h005_f3-stream-mi-precheck_2026-07-16"))

from anima_v3 import Falsifier, evaluate
from run_h005 import cond_bpb, cond_bpb_ppm, cond_bpb_markov, day_chunks

# --- frozen inputs (must match the card) --------------------------------------
STREAMS = {
    "hexa-lang": "/Users/mini/dancinlab/hexa-lang",
    "anima": "/Users/mini/dancinlab/anima",
    "sidecar": "/Users/mini/dancinlab/sidecar",
}
L = 4096         # per-chunk training-unit size (matched budget)
PT = 6144        # target probe size (the "capability" held-out set)
K = 12           # selection budget: k chunks selected per arm
POOL_CAP = 90    # deterministic cap on candidate pool size
N_TGT = 6        # chunks reserved per held-out target
NGRAM = 6        # frozen retriever n-gram order (matches markov6 order)
EPS = 0.02       # decoration threshold in bpb (H_005 verbatim)
CAPT_HI = 0.90   # ceiling-capture fraction above which the frozen retriever
                 # is judged to SATURATE the ceiling -> l11 tautology


def _det_shuffle(idx):
    """Deterministic adjacency-breaking permutation (no Math.random, H_005 style)."""
    return (idx[::2] + idx[1::2])[::-1]


def _ngrams(b: bytes, n: int) -> set:
    return {b[i:i + n] for i in range(len(b) - n + 1)}


def overlap_score(chunk: bytes, tgt_grams: set, n: int) -> int:
    return len(_ngrams(chunk, n) & tgt_grams)


def greedy_oracle(pool: list, tgt: bytes, k: int, est=cond_bpb_markov) -> list:
    """Greedy hindsight selection: repeatedly add the chunk that most reduces
    bpb(tgt | prime). Greedy is a LOWER bound on optimal selection (H_006 note):
    a positive is decisive, a null suggestive. Returns selected pool indices."""
    remaining = list(range(len(pool)))
    prime = b""
    chosen = []
    for _ in range(min(k, len(pool))):
        best_i, best_bpb = None, None
        for i in remaining:
            b = est(tgt, prime + pool[i])
            if best_bpb is None or b < best_bpb:
                best_bpb, best_i = b, i
        chosen.append(best_i)
        prime = prime + pool[best_i]
        remaining.remove(best_i)
    return chosen


def select_overlap(pool: list, tgt: bytes, k: int, n: int) -> list:
    tg = _ngrams(tgt, n)
    scored = sorted(range(len(pool)), key=lambda i: -overlap_score(pool[i], tg, n))
    return scored[:k]


def select_anti(pool: list, tgt: bytes, k: int, n: int) -> list:
    tg = _ngrams(tgt, n)
    scored = sorted(range(len(pool)), key=lambda i: overlap_score(pool[i], tg, n))
    return scored[:k]


def score_set(pool: list, sel: list, tgt: bytes) -> dict:
    """bpb(tgt | concat(selected)) under all three estimators. Matched budget:
    every arm concatenates exactly len(sel) chunks of L bytes each."""
    prime = b"".join(pool[i] for i in sel)
    return {
        "markov6": cond_bpb_markov(tgt, prime),
        "ppm": cond_bpb_ppm(tgt, prime),
        "gzip": cond_bpb(tgt, prime),
    }


def domain_mix(sel: list, labels: list) -> dict:
    out = {}
    for i in sel:
        out[labels[i]] = out.get(labels[i], 0) + 1
    return out


def build_corpus():
    """Heterogeneous pool from 3 real git streams (3 domains) + two disjoint
    held-out targets. Deterministic: chunks in git-log order, streams interleaved."""
    per_stream = {}
    for name, repo in STREAMS.items():
        ch = day_chunks(repo, max_days=120)
        per_stream[name] = [(name, c[:L]) for _, c in ch if len(c) >= max(L, PT)]
    # held-out targets: LAST N_TGT chunks of hexa-lang (T1) and anima (T2),
    # removed from the pool (chronological hold-out).
    t1_src = per_stream["hexa-lang"][-N_TGT:]
    t2_src = per_stream["anima"][-N_TGT:]
    T1 = b"".join(c for _, c in t1_src)[:PT]
    T2 = b"".join(c for _, c in t2_src)[:PT]
    # pool = everything except the held-out target chunks, interleaved across
    # streams so a prefix cap does not become single-domain.
    remain = {
        "hexa-lang": per_stream["hexa-lang"][:-N_TGT],
        "anima": per_stream["anima"][:-N_TGT],
        "sidecar": per_stream["sidecar"],
    }
    interleaved = []
    idx = 0
    while any(idx < len(v) for v in remain.values()):
        for name in ("hexa-lang", "anima", "sidecar"):
            if idx < len(remain[name]):
                interleaved.append(remain[name][idx])
        idx += 1
    interleaved = interleaved[:POOL_CAP]
    labels = [n for n, _ in interleaved]
    pool = [c for _, c in interleaved]
    return pool, labels, T1, T2


def planted_pool(T1: bytes, seed: int = 7):
    """O-liveness control: a pool with a KNOWN-relevant GOLD subset (slices of T1
    itself) buried among high-entropy NOISE chunks. The oracle/overlap must recover
    gold -> large headroom. If not, the instrument is blind -> INVALID. LCG only."""
    state = seed

    def nxt():
        nonlocal state
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        return state
    pool, labels = [], []
    # gold: 6 non-overlapping L-slices of a repeated-T1 buffer
    buf = (T1 * (6 * L // len(T1) + 2))
    for g in range(6):
        pool.append(buf[g * L:(g + 1) * L])
        labels.append("gold")
    # noise: random printable bytes, unrelated to T1
    for _ in range(POOL_CAP - 6):
        pool.append(bytes([(nxt() % 94) + 33 for _ in range(L)]))
        labels.append("noise")
    order = _det_shuffle(list(range(len(pool))))
    return [pool[i] for i in order], [labels[i] for i in order]


def rand_target(seed: int = 11) -> bytes:
    """Diagnostic: a target of random printable bytes. Its headroom is the
    order-0 marginal-exploit component the proxy can grab from ANY target (it
    shares its marginal with all printable text) — reported to show how much of
    the 'selection lever' is trivial marginal matching."""
    state = seed

    def nxt():
        nonlocal state
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        return state
    return bytes([(nxt() % 94) + 33 for _ in range(PT)])


def byte_shuffle(b: bytes, seed: int = 13) -> bytes:
    """MARGINAL FLOOR control: byte-shuffle a real target — IDENTICAL unigram
    marginal, n-gram (order>=1) structure destroyed. Headroom on shuf(T1) is the
    order-0 component of the selection lever; headroom(T1) - headroom(shuf(T1))
    is the genuine HIGHER-ORDER content-selection signal (the H_005 shuffle-floor
    discipline, applied to the target). LCG Fisher-Yates, deterministic."""
    state = seed
    arr = bytearray(b)

    def nxt():
        nonlocal state
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        return state
    for i in range(len(arr) - 1, 0, -1):
        j = nxt() % (i + 1)
        arr[i], arr[j] = arr[j], arr[i]
    return bytes(arr)


def run_arms(pool, labels, T, tag):
    """All four arms for one target; returns per-arm bpb + selections + headroom."""
    sel_oracle = greedy_oracle(pool, T, K)
    sel_overlap = select_overlap(pool, T, K, NGRAM)
    sel_random = _det_shuffle(list(range(len(pool))))[:K]
    sel_anti = select_anti(pool, T, K, NGRAM)
    arms = {
        "oracle": {"sel": sel_oracle, "bpb": score_set(pool, sel_oracle, T),
                   "mix": domain_mix(sel_oracle, labels)},
        "overlap": {"sel": sel_overlap, "bpb": score_set(pool, sel_overlap, T),
                    "mix": domain_mix(sel_overlap, labels)},
        "random": {"sel": sel_random, "bpb": score_set(pool, sel_random, T),
                   "mix": domain_mix(sel_random, labels)},
        "anti": {"sel": sel_anti, "bpb": score_set(pool, sel_anti, T),
                 "mix": domain_mix(sel_anti, labels)},
    }
    out = {"tag": tag, "arms": arms}
    for est in ("markov6", "ppm", "gzip"):
        rnd = arms["random"]["bpb"][est]
        orc = arms["oracle"]["bpb"][est]
        ovl = arms["overlap"]["bpb"][est]
        headroom = rnd - orc
        ceil_capt = ((rnd - ovl) / headroom) if abs(headroom) > 1e-9 else float("nan")
        orc_over_ovl = ovl - orc  # how much the greedy oracle beats the frozen retriever
        out[est] = {"random": rnd, "oracle": orc, "overlap": ovl,
                    "anti": arms["anti"]["bpb"][est], "headroom": headroom,
                    "ceil_capture": ceil_capt, "oracle_over_overlap": orc_over_ovl}
    return out


def main() -> int:
    print("=" * 74)
    print("H_008 — f4-curriculum-headroom · does SELECTION beat a $0 n-gram retriever? ($0)")
    print("=" * 74)
    print(f"L={L} chunk · PT={PT} target · K={K} budget · pool<= {POOL_CAP} · "
          f"ngram={NGRAM} · eps={EPS}\n")

    pool, labels, T1, T2 = build_corpus()
    print(f"pool composition: {dict(Counter(labels))}  (n={len(pool)})")
    print(f"T1 = held-out hexa-lang ({len(T1)}B) · T2 = held-out anima ({len(T2)}B)\n")

    m = {"config": {"L": L, "PT": PT, "K": K, "POOL_CAP": POOL_CAP,
                    "NGRAM": NGRAM, "EPS": EPS, "pool_n": len(pool),
                    "pool_mix": dict(Counter(labels))}}

    # --- O-liveness FIRST: a blind instrument invalidates everything ----------
    p_pool, p_lab = planted_pool(T1)
    live = run_arms(p_pool, p_lab, T1, "liveness-planted")
    m["liveness"] = {"markov6": live["markov6"], "gold_in_oracle":
                     live["arms"]["oracle"]["mix"].get("gold", 0),
                     "gold_in_overlap": live["arms"]["overlap"]["mix"].get("gold", 0)}
    lh = live["markov6"]["headroom"]
    print(f"[O-3 liveness] planted-gold headroom(markov6) = {lh:+.4f} bpb "
          f"(must be >> {EPS}; headroom is the validity gate). diagnostic: gold in "
          f"oracle={m['liveness']['gold_in_oracle']}/6 overlap={m['liveness']['gold_in_overlap']}/6 "
          f"(greedy saturates T1 with ~2 gold slices, so a low gold count is CORRECT "
          f"submodular behaviour, not a blind instrument)")

    # --- marginal floor: byte-shuffled T1 (same unigram, no n-gram) -----------
    Tshuf = byte_shuffle(T1)
    mfloor = run_arms(pool, labels, Tshuf, "marginal-floor-shufT1")
    m["marginal_floor"] = mfloor["markov6"]
    # --- diagnostic: random printable target (pure marginal exploit) ----------
    Trand = rand_target()
    neg = run_arms(pool, labels, Trand, "diag-randtarget")
    m["diag_randtarget"] = neg["markov6"]
    print(f"[marginal floor] shuffled-T1 headroom(markov6) = {mfloor['markov6']['headroom']:+.4f} "
          f"bpb (the order-0 component); random-printable target = "
          f"{neg['markov6']['headroom']:+.4f} bpb\n")

    # --- primary: T1 arms -----------------------------------------------------
    r1 = run_arms(pool, labels, T1, "T1-hexa")
    m["T1"] = r1
    # --- T2 arms (for transfer) ----------------------------------------------
    r2 = run_arms(pool, labels, T2, "T2-anima")
    m["T2"] = r2

    for tag, r in (("T1 (hexa held-out)", r1), ("T2 (anima held-out)", r2)):
        print(f"[{tag}]  oracle mix={r['arms']['oracle']['mix']}  "
              f"overlap mix={r['arms']['overlap']['mix']}")
        for est in ("markov6", "ppm", "gzip"):
            e = r[est]
            print(f"    {est:7s}: random {e['random']:.4f}  oracle {e['oracle']:.4f}  "
                  f"overlap {e['overlap']:.4f}  anti {e['anti']:.4f}  || "
                  f"headroom {e['headroom']:+.4f}  ceil_capt {e['ceil_capture']:+.2f}  "
                  f"orc>ovl {e['oracle_over_overlap']:+.4f}")
        print()

    # --- transfer: does ORACLE_for_T1 help T2 (disjoint domain)? --------------
    sel_o1 = r1["arms"]["oracle"]["sel"]
    b_t2_from_o1 = score_set(pool, sel_o1, T2)
    m["transfer"] = {}
    print("[transfer / O-Goodhart]  selecting-for-T1, evaluated on T2:")
    for est in ("markov6", "ppm", "gzip"):
        rnd2 = r2[est]["random"]
        o2 = r2[est]["oracle"]
        from_o1 = b_t2_from_o1[est]
        denom = rnd2 - o2
        tr = ((rnd2 - from_o1) / denom) if abs(denom) > 1e-9 else float("nan")
        m["transfer"][est] = {"t2_random": rnd2, "t2_oracle_for_t2": o2,
                              "t2_from_oracle_t1": from_o1, "transfer_ratio": tr}
        print(f"    {est:7s}: bpb(T2|rand) {rnd2:.4f}  bpb(T2|oracleT2) {o2:.4f}  "
              f"bpb(T2|oracleT1) {from_o1:.4f}  transfer_ratio {tr:+.2f}")
    print()

    # --- verdict logic (markov6 authority, ppm confirm) -----------------------
    a = r1["markov6"]
    ap = r1["ppm"]
    # genuine higher-order content selection = raw headroom minus the order-0
    # marginal floor (byte-shuffled T1) AND the greedy oracle must beat the frozen
    # n-gram retriever. Both trivial baselines must be cleared.
    marg = m["marginal_floor"]["headroom"]
    genuine_over_marginal = a["headroom"] - marg
    orc_over_ovl = a["oracle_over_overlap"]            # markov6 (the SELECTION estimator)
    orc_over_ovl_ppm = ap["oracle_over_overlap"]       # ppm (INDEPENDENT confirm)
    m["genuine_over_marginal"] = genuine_over_marginal
    m["orc_over_ovl_ppm"] = orc_over_ovl_ppm
    m["liveness_ok"] = lh > 5 * EPS
    # raw headroom on the order-aware pair (gzip known to sit at its LZ floor, H_005).
    m["headroom_live"] = a["headroom"] > EPS and ap["headroom"] > 0
    m["ppm_agree"] = (a["headroom"] > 0) == (ap["headroom"] > 0)
    # l11 tautology (corpus domain): the raw selection headroom is REAL but neither
    # trivial baseline SURVIVES CROSS-ESTIMATOR:
    #  (a) the order-0 marginal floor eats it (genuine <= eps), OR
    #  (b) the greedy oracle's edge over the frozen n-gram retriever is an artifact
    #      of scoring with the SELECTION estimator — an INDEPENDENT estimator (ppm)
    #      does not confirm the oracle beats the retriever (orc_over_ovl_ppm <= 0).
    m["marginal_dominated"] = genuine_over_marginal <= EPS
    m["retriever_saturates"] = not (orc_over_ovl > EPS and orc_over_ovl_ppm > 0)
    m["tautology"] = m["headroom_live"] and (m["marginal_dominated"] or m["retriever_saturates"])
    tr_m6 = m["transfer"]["markov6"]["transfer_ratio"]
    m["goodhart"] = m["headroom_live"] and (not m["tautology"]) and (tr_m6 <= 0.25)

    falsifiers = [
        Falsifier("O-3 liveness (blind instrument)",
                  lambda x: not x["liveness_ok"],
                  "planted-gold headroom <= 5*eps -> INVALID"),
        Falsifier("F4-1 kill (no selection headroom)",
                  lambda x: not x["headroom_live"],
                  "oracle ceiling <= random floor -> F4-REFUSED (no lever)"),
        Falsifier("F4-2a marginal-dominated (order-0 floor eats the ceiling)",
                  lambda x: x["headroom_live"] and x["marginal_dominated"],
                  "headroom(T1) - headroom(shuf T1) <= eps -> the selection lever is "
                  "order-0 marginal matching, not content -> l11 corpus tautology"),
        Falsifier("F4-2b retriever-saturates (frozen n-gram >= greedy oracle)",
                  lambda x: x["headroom_live"] and x["retriever_saturates"],
                  "a $0 frozen n-gram retriever beats/ties the greedy oracle -> the "
                  "LEARNED policy is decoration over similarity retrieval"),
        Falsifier("F4-3 Goodhart (curriculum value is target-specific)",
                  lambda x: x["goodhart"],
                  "selecting-for-T1 does not transfer to disjoint T2 -> Goodhart"),
        Falsifier("F4-6 estimator disagreement",
                  lambda x: not x["ppm_agree"],
                  "markov6 and ppm disagree on headroom sign -> PENDING(instrument)"),
    ]
    ledger = evaluate(m, falsifiers)

    if not m["liveness_ok"]:
        verdict = "INVALID (blind instrument — liveness headroom below floor)"
    elif not m["headroom_live"]:
        verdict = ("F4-REFUSED — hindsight-optimal selection does not beat the random "
                   "floor on held-out capability; corpus selection has no measurable "
                   "headroom on this substrate (no lever to give a policy).")
    elif m["tautology"]:
        why = []
        if m["marginal_dominated"]:
            why.append(f"the order-0 marginal floor (shuffled-T1 headroom {marg:+.4f}) "
                       f"leaves only {genuine_over_marginal:+.4f} genuine higher-order signal "
                       f"(<= eps)")
        if m["retriever_saturates"]:
            why.append(f"the greedy oracle's edge over the frozen 6-gram retriever is an "
                       f"estimator-Goodhart artifact — markov6 (the selection estimator) says "
                       f"oracle_over_overlap {orc_over_ovl:+.4f} but the INDEPENDENT ppm says "
                       f"{orc_over_ovl_ppm:+.4f} (retriever ties/beats the oracle)")
        verdict = (f"F4-TAUTOLOGY (l11, corpus domain) — the raw selection headroom is REAL "
                   f"(+{a['headroom']:.4f} bpb) but decoration once the trivial baselines are "
                   f"removed: {' AND '.join(why)}. The 'learned acquisition policy / agency of "
                   f"choice' adds nothing a $0 frozen statistic does not — F4 is the corpus half "
                   f"of the frequency tautology, exactly as fake-diversity-audit warned.")
    elif m["goodhart"]:
        verdict = (f"F4-GOODHART — genuine higher-order selection ({genuine_over_marginal:+.4f} "
                   f"over marginal, {orc_over_ovl:+.4f} over retriever) exists but does NOT "
                   f"transfer to a disjoint target (transfer {tr_m6:+.2f}) -> target-specific "
                   f"overlap, the l6 jugular.")
    else:
        verdict = (f"F4-HEADROOM-LIVE (weak) — selection headroom +{a['headroom']:.4f} bpb clears "
                   f"BOTH trivial baselines: +{genuine_over_marginal:.4f} over the order-0 marginal "
                   f"floor AND +{orc_over_ovl:.4f} over the frozen n-gram retriever, and it "
                   f"transfers to a disjoint target (transfer {tr_m6:+.2f}). A genuine content-"
                   f"selection lever a policy could learn survives at $0.")
    m["verdict"] = verdict

    print("=" * 74)
    for r in ledger["falsifiers"]:
        print(f"  {r['status']:4s}  {r['name']}")
    print(f"\n  VERDICT: {verdict}")
    print("=" * 74)

    out = os.path.join(_HERE, "result.json")
    with open(out, "w") as f:
        json.dump(m, f, ensure_ascii=False, indent=1, default=lambda o: str(o))
        f.write("\n")
    print(f"\nartifacts: {os.path.relpath(out, _ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
