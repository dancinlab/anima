"""H_006 — f3-bounded-oracle. Does a k-BOUNDED hindsight extract retain the ceiling?

$0 gate for the F3 twin. Per day-pair, score each line of day t (beyond the tail)
by its marginal lift (gzip, fast), take the top lines up to budget k, then measure
ceiling(k) = bpb(P|tail) - bpb(P|tail+extract_k) with the order-aware markov6 (ppm
confirm) against the H_005 shuffle floor. Emits the winning extracts as the twin's
oracle-select inputs. Card frozen 2026-07-16.

Run: python3 state/h006_f3-bounded-oracle_2026-07-16/run_h006.py
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

from anima_v3 import Falsifier, evaluate
import run_h005 as H
from run_h005 import cond_bpb, cond_bpb_ppm, cond_bpb_markov, W, P

markov6 = functools.partial(cond_bpb_markov, order=6)
EPS = 0.02
KS = [64, 256, 1024, 4096]
STREAMS = {"anima": "/Users/mini/dancinlab/anima",           # verdict-bearing (H_005 anchor)
           "hexa-lang": "/Users/mila/dancinlab/hexa-lang"}   # placeholder, fixed below
STREAMS["hexa-lang"] = "/Users/mini/dancinlab/hexa-lang"


MAX_LINES = 400   # cap lines scored per day (longest-first) — keeps selection O(1) per stream


def rank_lines(summary: bytes, tail: bytes, pref: bytes) -> list:
    """Rank day-t lines by marginal gzip lift ONCE. Returns [(lift, line), ...] desc.

    gzip is the FAST selection scorer (one call per line). Scored once per pair and
    reused across all budgets k — the earlier version re-scored per k (the slowdown)."""
    lines = [ln for ln in summary.split(b"\n") if ln.strip()]
    if len(lines) > MAX_LINES:                      # longest lines carry the most content
        lines = sorted(lines, key=len, reverse=True)[:MAX_LINES]
    base = cond_bpb(pref, tail)
    scored = [(base - cond_bpb(pref, tail + ln + b"\n"), ln) for ln in lines]
    scored.sort(key=lambda t: t[0], reverse=True)
    return scored


def extract_at_k(ranked: list, k: int) -> bytes:
    """Top ranked lines (positive lift) up to k bytes — no re-scoring."""
    out, size = [], 0
    for lift, ln in ranked:
        if lift <= 0:
            break
        if size + len(ln) + 1 > k:
            continue
        out.append(ln)
        size += len(ln) + 1
        if size >= k:
            break
    return b"\n".join(out)


def build_extracts(chunks: list, save_dir=None, stream=None) -> list:
    """Rank + extract for every pair ONCE (the gzip-heavy step), reused across estimators.

    Returns [(pref, tail, {k: extract_bytes}), ...] — no ceiling estimator involved here,
    so both markov6 and ppm consume the same cached extracts (the earlier version re-ranked
    per estimator, the slowdown)."""
    out = []
    for i in range(len(chunks) - 1):
        day_t = chunks[i][1]
        pref = chunks[i + 1][1][:P]
        tail = day_t[-W:]
        summary = day_t[:-W] if len(day_t) > W else b""
        ranked = rank_lines(summary, tail, pref)
        exts = {k: extract_at_k(ranked, k) for k in KS}
        out.append((pref, tail, exts))
        if save_dir and stream:
            with open(os.path.join(save_dir, f"{stream}_{chunks[i][0]}.txt"), "wb") as f:
                f.write(exts[4096])
    return out


def measure_bounded(prebuilt: list, est) -> dict:
    """ceiling(k) median over pairs, from pre-built extracts, under estimator `est`."""
    per_k = {k: [] for k in KS}
    for pref, tail, exts in prebuilt:
        b_tail = est(pref, tail)
        for k in KS:
            per_k[k].append(b_tail - est(pref, tail + exts[k]))

    def med(v):
        v = sorted(v)
        return v[len(v) // 2] if v else 0.0
    return {str(k): med(per_k[k]) for k in KS}


def planted_lines_stream(n_days: int = 30, seed: int = 5) -> list:
    """B-2 liveness for the LINE extractor: each day is many filler lines plus one
    day-specific BLOCK LINE placed beyond the tail; day t+1's prefix echoes yesterday's
    block line. A correct top-lines extractor selects the block line and recovers the
    ceiling. (H_005's planted stream has no newlines, so the line extractor can't test it.)"""
    state = seed
    def nxt():
        nonlocal state
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        return state
    chunks = []
    prev_block = None
    for d in range(n_days):
        block = bytes([(nxt() % 94) + 33 for _ in range(300)])       # day-specific block LINE
        fill_lines = [bytes([(nxt() % 26) + 97 for _ in range(80)]) for _ in range(120)]
        prefix = (prev_block if prev_block else block) + b"\n"        # prefix echoes yesterday's block
        # day = prefix(echoes prev) + block-line early (in summary) + filler lines (fill the tail)
        day = prefix + block + b"\n" + b"\n".join(fill_lines)
        chunks.append((f"d{d}", day))
        prev_block = block
    return chunks


def main() -> int:
    print("=" * 74)
    print("H_006 — f3-bounded-oracle · does a k-bounded hindsight extract keep the ceiling?")
    print("=" * 74)
    m = {"streams": {}, "eps": EPS}

    # liveness (B-2): line-structured planted latent; the extractor must select the block line
    live = planted_lines_stream()
    live_ceil = measure_bounded(build_extracts(live), markov6)
    m["liveness_ceiling"] = live_ceil
    live_ok = live_ceil["4096"] > 5 * EPS
    print(f"[B-2 liveness] planted ceiling(4096) = {live_ceil['4096']:.4f} (>>{EPS}?): {live_ok}\n")

    for name, repo in STREAMS.items():
        chunks = H.day_chunks(repo)
        if len(chunks) < 21:
            m["streams"][name] = {"error": f"only {len(chunks)} days"}
            print(f"[{name}] SKIP ({len(chunks)} days)")
            continue
        shuf = (chunks[::2] + chunks[1::2])[::-1]
        real_ext = build_extracts(chunks, _HERE + "/extracts", name)   # gzip ranking done ONCE
        shuf_ext = build_extracts(shuf)
        c_mk = measure_bounded(real_ext, markov6)
        f_mk = measure_bounded(shuf_ext, markov6)
        c_pp = measure_bounded(real_ext, cond_bpb_ppm)
        f_pp = measure_bounded(shuf_ext, cond_bpb_ppm)
        row = {"days": len(chunks), "markov6": {}, "ppm": {}}
        for k in KS:
            row["markov6"][str(k)] = {"ceiling": c_mk[str(k)], "over_floor": c_mk[str(k)] - f_mk[str(k)]}
            row["ppm"][str(k)] = {"ceiling": c_pp[str(k)], "over_floor": c_pp[str(k)] - f_pp[str(k)]}
        row["markov6_4096_over"] = row["markov6"]["4096"]["over_floor"]
        row["ppm_4096_over"] = row["ppm"]["4096"]["over_floor"]
        row["anchored"] = any(row["markov6"][str(k)]["over_floor"] > EPS for k in KS)
        row["agree_4096"] = (row["markov6_4096_over"] > 0) == (row["ppm_4096_over"] > 0)
        m["streams"][name] = row
        print(f"[{name}] days={row['days']}  ceiling(k) over-floor (markov6 | ppm):")
        for k in KS:
            print(f"    k={k:5d}: {row['markov6'][str(k)]['over_floor']:+.4f} | "
                  f"{row['ppm'][str(k)]['over_floor']:+.4f}")
        print(f"    -> anchored(some k)={row['anchored']} · agree@4096={row['agree_4096']}")

    real = {k: v for k, v in m["streams"].items() if "error" not in v}
    m["liveness_ok"] = live_ok
    anima = real.get("anima", {})
    m["anima_anchored"] = anima.get("anchored", False)
    m["both_refused"] = (len(real) > 0 and
                         all(v["markov6_4096_over"] <= EPS for v in real.values()))

    falsifiers = [
        Falsifier("B-2 liveness", lambda x: not x["liveness_ok"], "blind extractor -> INVALID"),
        Falsifier("B-1 kill (bounded diary doomed)",
                  lambda x: x["both_refused"],
                  "ceiling(4096) <= floor on both -> F3 twin cancelled"),
    ]
    ledger = evaluate(m, falsifiers)

    if not live_ok:
        verdict = "INVALID (blind extractor)"
    elif m["both_refused"]:
        verdict = ("F3-BOUNDED-REFUSED — a hindsight k<=4096 extract does NOT retain the ceiling on "
                   "either anchored stream; the day MI is incompressible below context scale. The F3 "
                   "twin is CANCELLED ($0 saved) — the k-bottleneck instantiation is dead even though "
                   "the unbounded MI (H_005) is real.")
    elif m["anima_anchored"]:
        verdict = ("ANCHORED — a bounded k<=4096 hindsight extract retains the ceiling above the "
                   "shuffle floor on anima; the bottlenecked diary is VIABLE. The F3 twin (H_007) is "
                   "licensed; the top-line extracts are emitted as its oracle-select inputs.")
    else:
        verdict = "PARTIAL — hexa-lang only / boundary; see per-stream rows"
    m["verdict"] = verdict

    print("\n" + "=" * 74)
    for r in ledger["falsifiers"]:
        print(f"  {r['status']:4s}  {r['name']}")
    print(f"\n  VERDICT: {verdict}")
    print("=" * 74)

    out = os.path.join(_HERE, "result.json")
    with open(out, "w") as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"\nartifacts: {os.path.relpath(out, _ROOT)} + extracts/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
