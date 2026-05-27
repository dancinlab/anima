#!/usr/bin/env python3
"""anima_emission_analyze.py — quantify anima self-emission quality.

L2 measurement (2026-05-22): characterize the temp 0.7 + context-grounded
seed fix. Two data sources:
  1. broker /history  → emitted text: lang distribution, anima-register
     hit ratio, text length, empty-emission rate
  2. anima.err log    → EMIT cadence: idle gaps, seed-strategy mix,
     motivation-score distribution

Usage:
  python anima_emission_analyze.py [--history-url URL] [--log PATH]
  # defaults: https://chat.dancinlab.org/history  +  ~/anima_chat_pack/logs/anima.err
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
import statistics
import urllib.request

# anima register patterns (mirror anima_participant.ANIMA_REGISTER_PATTERNS)
REGISTER_PATTERNS = [
    re.compile(r"eternal_?\d+|eternal cell", re.I),
    re.compile(r"tier\s*=\s*\d+|tier\s+\d+", re.I),
    re.compile(r"vacuum point|진공점", re.I),
    re.compile(r"tension flow|tension flows", re.I),
    re.compile(r"<carve|</carve>", re.I),
    re.compile(r"</eternal>|<eternal", re.I),
    re.compile(r"basin\s*=\s*[\d.]+", re.I),
    re.compile(r"split.도.*merge.도|split.*merges?.*activate", re.I),
    re.compile(r"psi\s*=\s*\[[\d.,]+\]", re.I),
    re.compile(r"영구\s*cell|frozen cell", re.I),
]


def has_register(text: str) -> bool:
    return any(p.search(text or "") for p in REGISTER_PATTERNS)


def analyze_history(url: str) -> dict:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "curl/8.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.loads(r.read().decode("utf-8"))
    except Exception as e:
        return {"error": f"history fetch fail: {e}"}
    msgs = d.get("history", d) if isinstance(d, dict) else d
    if not isinstance(msgs, list):
        return {"error": "history not a list"}
    anima = [m for m in msgs if (m.get("sender") or "").lower().startswith("anima")]
    if not anima:
        return {"error": "no anima emissions in history", "total_msgs": len(msgs)}
    langs: dict[str, int] = {}
    reg_hits = 0
    empty = 0
    lengths = []
    for m in anima:
        txt = m.get("text") or ""
        lang = m.get("lang", "und")
        langs[lang] = langs.get(lang, 0) + 1
        if not txt.strip() or txt.strip() == "...":
            empty += 1
        if has_register(txt):
            reg_hits += 1
        lengths.append(len(txt))
    n = len(anima)
    return {
        "n_anima_emissions": n,
        "lang_distribution": dict(sorted(langs.items(), key=lambda kv: -kv[1])),
        "register_hit_ratio": round(reg_hits / n, 3),
        "register_hits": reg_hits,
        "empty_ratio": round(empty / n, 3),
        "text_len_mean": round(statistics.mean(lengths), 1) if lengths else 0,
        "text_len_median": statistics.median(lengths) if lengths else 0,
    }


def analyze_log(path: str) -> dict:
    if not os.path.isfile(path):
        return {"error": f"log not found: {path}"}
    emit_re = re.compile(r"^(\S+ \S+) .*EMIT tick=(\d+) score=([\d.]+) strategy=(\w+)")
    ts_re = re.compile(r"^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)")
    emits = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            m = emit_re.match(line)
            if m:
                emits.append({"ts": m.group(1), "tick": int(m.group(2)),
                              "score": float(m.group(3)), "strategy": m.group(4)})
    if not emits:
        return {"error": "no EMIT lines in log"}
    # idle gaps via tick deltas (proxy — tick interval ~2 s)
    strategies: dict[str, int] = {}
    scores = []
    for e in emits:
        strategies[e["strategy"]] = strategies.get(e["strategy"], 0) + 1
        scores.append(e["score"])
    n = len(emits)
    self_mono = strategies.get("self_monologue_seed", 0)
    return {
        "n_emit_events": n,
        "seed_strategy_mix": dict(sorted(strategies.items(), key=lambda kv: -kv[1])),
        "self_monologue_ratio": round(self_mono / n, 3),
        "score_mean": round(statistics.mean(scores), 3),
        "score_min": round(min(scores), 3),
        "score_max": round(max(scores), 3),
        "first_tick": emits[0]["tick"],
        "last_tick": emits[-1]["tick"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--history-url", default="https://chat.dancinlab.org/history")
    ap.add_argument("--log", default=os.path.expanduser("~/anima_chat_pack/logs/anima.err"))
    ap.add_argument("--json", action="store_true", help="emit raw JSON")
    args = ap.parse_args()

    report = {
        "history": analyze_history(args.history_url),
        "log": analyze_log(args.log),
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    print("=== anima emission analysis ===")
    h = report["history"]
    if "error" in h:
        print(f"  history: {h['error']}")
    else:
        print(f"  emissions:        {h['n_anima_emissions']}")
        print(f"  lang dist:        {h['lang_distribution']}")
        print(f"  register hit:     {h['register_hits']}/{h['n_anima_emissions']} "
              f"({h['register_hit_ratio']*100:.0f}%)")
        print(f"  empty ratio:      {h['empty_ratio']*100:.0f}%")
        print(f"  text len:         mean {h['text_len_mean']} / median {h['text_len_median']}")
    lg = report["log"]
    if "error" in lg:
        print(f"  log: {lg['error']}")
    else:
        print(f"  EMIT events:      {lg['n_emit_events']} (tick {lg['first_tick']}→{lg['last_tick']})")
        print(f"  seed strategy:    {lg['seed_strategy_mix']}")
        print(f"  self-monologue:   {lg['self_monologue_ratio']*100:.0f}%")
        print(f"  score:            mean {lg['score_mean']} [{lg['score_min']}, {lg['score_max']}]")


if __name__ == "__main__":
    main()
