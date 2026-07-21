"""H_007 — f7-owner-legibility. Is the owner's real message stream predictable AND
high-dimensional — the premise F7 (curiosity) and F5 (trajectory) both need? $0.

Privacy: NO owner message content is written into the repo — only aggregate bpb
and rank numbers. The owner's words stay on their own disk. Card frozen 2026-07-16.

Run: python3 state/h007_f7-owner-legibility_2026-07-16/run_h007.py
"""

from __future__ import annotations

import glob
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tool"))
sys.path.insert(0, os.path.join(_ROOT, "state", "h005_f3-stream-mi-precheck_2026-07-16"))

from anima_v3 import Falsifier, evaluate, participation_ratio, singular_values
from run_h005 import cond_bpb, cond_bpb_ppm, cond_bpb_markov, measure_stream, planted_latent_stream, W, P
import functools

markov6 = functools.partial(cond_bpb_markov, order=6)
EPS = 0.02
PR_FLOOR = 2.0
NOISE = re.compile(r'^(\s*<|Caveat:|\[Request interrupted|# |Contents of|system-reminder|<command-)')
TRANSCRIPTS = os.path.expanduser("~/.claude/projects/*/*.jsonl")


def owner_text(path: str) -> str:
    """Genuine owner typing from one transcript: type==user text, no tool_result, no hook noise."""
    parts = []
    try:
        fh = open(path, encoding="utf-8", errors="replace")
    except OSError:
        return ""
    for line in fh:
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if r.get("type") != "user":
            continue
        c = r.get("message", {}).get("content")
        if isinstance(c, list):
            if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c):
                continue
            txt = "".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
        elif isinstance(c, str):
            txt = c
        else:
            txt = ""
        txt = txt.strip()
        if len(txt) < 3 or NOISE.match(txt):
            continue
        parts.append(txt)
    return "\n".join(parts)


def owner_sessions() -> list:
    """[(mtime, bytes), ...] of genuine-owner-message sessions with >= W+P bytes, chronological."""
    out = []
    for path in glob.glob(TRANSCRIPTS):
        t = owner_text(path)
        b = t.encode("utf-8", "replace")
        if len(b) >= W + P:
            out.append((os.path.getmtime(path), b))
    out.sort(key=lambda x: x[0])
    return [(str(i), b) for i, (_, b) in enumerate(out)]


def planted_legible(n=30, seed=9) -> list:
    """O-3 liveness: a high-dimensional legible stream — each session's tail predicts the next
    session's prefix via a per-session block placed beyond the tail (H_005 planted pattern)."""
    st = seed
    def nxt():
        nonlocal st
        st = (1103515245 * st + 12345) & 0x7FFFFFFF
        return st
    chunks, prev = [], None
    for d in range(n):
        block = bytes([(nxt() % 94) + 33 for _ in range(P)])
        filler = bytes([(nxt() % 26) + 97 for _ in range(W + 1000)])
        prefix = prev if prev else block
        chunks.append((f"s{d}", prefix + block + filler))
        prev = block
    return chunks


def rank_of(chunks: list) -> float:
    feats = []
    for _, b in chunks:
        v = [b.count(bytes([c])) for c in range(0, 256, 8)]
        s = sum(v) or 1
        feats.append([x / s for x in v])
    return participation_ratio(singular_values(feats)) if len(feats) >= 2 else 0.0


def legibility(chunks: list, est) -> float:
    res = measure_stream(chunks, est)
    shuf = measure_stream((chunks[::2] + chunks[1::2])[::-1], est)
    return res["ceiling_med"] - shuf["ceiling_med"]


def main() -> int:
    print("=" * 74)
    print("H_007 — f7-owner-legibility · is the owner a predictable, high-dim other? ($0)")
    print("=" * 74)
    m = {}

    live = planted_latent_stream()   # H_005's proven cross-boundary planted (read 7.79 there)
    live_leg = legibility(live, markov6)
    m["liveness_legibility"] = live_leg
    live_ok = live_leg > 5 * EPS
    print(f"[O-3 liveness] planted legibility = {live_leg:+.4f} (>>{EPS}?): {live_ok}")

    sessions = owner_sessions()
    m["n_sessions"] = len(sessions)
    print(f"genuine-owner sessions (>= {W+P}B): {len(sessions)}")
    if len(sessions) < 100:
        m["verdict"] = f"INVALID (only {len(sessions)} sessions, need >=100)"
        print(f"\n  VERDICT: {m['verdict']}")
        json.dump(m, open(os.path.join(_HERE, "result.json"), "w"), indent=1)
        return 0

    leg_mk = legibility(sessions, markov6)
    leg_pp = legibility(sessions, cond_bpb_ppm)
    leg_gz = legibility(sessions, cond_bpb)
    pr = rank_of(sessions)
    m["legibility_markov6"] = leg_mk
    m["legibility_ppm"] = leg_pp
    m["legibility_gzip"] = leg_gz
    m["participation_ratio"] = pr
    print(f"\nowner-stream legibility over-floor:  markov6 {leg_mk:+.4f} · ppm {leg_pp:+.4f} · gzip {leg_gz:+.4f}")
    print(f"owner-self participation ratio (dimensionality): {pr:.2f}  (floor {PR_FLOOR})")

    order_aware = [leg_mk, leg_pp]
    m["legible"] = all(o > EPS for o in order_aware)
    m["agree"] = (leg_mk > 0) == (leg_pp > 0)
    m["high_dim"] = pr > PR_FLOOR
    m["liveness_ok"] = live_ok

    falsifiers = [
        Falsifier("O-3 liveness", lambda x: not x["liveness_ok"], "blind instrument -> INVALID"),
        Falsifier("O-5 estimator agreement", lambda x: not x["agree"], "markov6/ppm disagree -> PENDING"),
        Falsifier("O-1 legibility kill", lambda x: not x["legible"], "owner unpredictable -> F7-REFUSED"),
        Falsifier("O-2 rank collapse (L1)", lambda x: x["legible"] and not x["high_dim"],
                  "owner-self is one-bit -> RANK-COLLAPSE"),
    ]
    ledger = evaluate(m, falsifiers)

    if not live_ok:
        verdict = "INVALID (blind instrument)"
    elif not m["agree"]:
        verdict = "PENDING(instrument) — markov6 and ppm disagree on legibility sign"
    elif not m["legible"]:
        verdict = ("F7-REFUSED — the owner's message stream carries no predictable cross-session self "
                   "above the shuffle floor; nothing high-dimensional to be curious about. The F7/F5 "
                   "owner-substrate premise is REFUSED at $0.")
    elif not m["high_dim"]:
        verdict = (f"RANK-COLLAPSE — the owner is legible (over-floor {leg_mk:+.4f}) but the owner-self "
                   f"collapses to participation ratio {pr:.2f} <= {PR_FLOOR} (the v1 one-bit seam). F7's "
                   f"high-dimensionality claim is DEAD.")
    else:
        verdict = (f"ANCHORED — the owner's stream is legible (over-floor markov6 {leg_mk:+.4f}) AND "
                   f"high-dimensional (PR {pr:.2f} > {PR_FLOOR}). A high-dimensional legible owner-self "
                   f"exists; the F7 (curiosity) / F5 (trajectory) premise is LIVE.")
    m["verdict"] = verdict

    print("\n" + "=" * 74)
    for r in ledger["falsifiers"]:
        print(f"  {r['status']:4s}  {r['name']}")
    print(f"\n  VERDICT: {verdict}")
    print("=" * 74)
    json.dump(m, open(os.path.join(_HERE, "result.json"), "w"), indent=1)
    print(f"\nartifacts: {os.path.relpath(os.path.join(_HERE, 'result.json'), _ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
