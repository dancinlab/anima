#!/usr/bin/env python3
"""Regenerate morph_corpus.txt (the MORPH-ATOM / NAT-ATOM natural corpus) from NSMC — deterministic.

morph_corpus.txt (~9MB of natural Korean review lines) is the codec-training + CPT corpus for the whole
MORPH-ATOM family. It was never committed (size), and the /tmp copy was lost with a scratchpad wipe
(convergence scratchpad-tmp-loss-1) — so this script makes it REPRODUCIBLE: NSMC (github raw, the same
source gen_nbind.load_nsmc uses) → one review per line → morph_corpus.txt.

Usage: gen_morph_corpus.py [--out morph_corpus.txt]
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_nbind as G

OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "morph_corpus.txt"

rows = list(G.load_nsmc(None))          # [(text, label), …] — deterministic github-raw fetch + cache
n = 0
with open(OUT, "w", encoding="utf-8") as f:
    for t, _lab in rows:
        t = t.strip()
        if t:
            f.write(t + "\n"); n += 1
print("CORPUS_DONE: %d lines -> %s (%d bytes)" % (n, OUT, os.path.getsize(OUT)))
