#!/usr/bin/env python3
"""H_9235 fork-A — NO-COPY word-initial extractor (Fable redesign · copy-trap fix).
The derivtrace/flat composed ('out:') span mixes COPYABLE words (from the definitions in-context) and
NON-COPYABLE words (a concept's associated keywords, requiring ROUTING not copy). This extracts training
examples ONLY at WORD-INITIAL positions of NON-COPYABLE composed words (target word absent from the recent
context window) — exactly the routing-signal positions where the trunk can't copy, so CE has a real gradient
(fixes the copy-dead signal). Context (definitions) kept = recovery signal. Pair-split held-out excluded by corpus.
Emits nocopy_prompts.json for `anima-py evaluate --dump-hidden --with-logits`."""
import sys
import json
import random
import re

DERIV = sys.argv[1] if len(sys.argv) > 1 else "flat.txt"
OUT = sys.argv[2] if len(sys.argv) > 2 else "nocopy_prompts.json"
N_TARGET = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
CTXWIN = 48                 # recent-context window a copy-head could copy from
SEED = 7
MARK = "out:"

lines = [ln.rstrip("\n") for ln in open(DERIV) if ln.strip()]
examples = []
for li, ln in enumerate(lines):
    j = ln.find(MARK)
    if j < 0:
        continue
    start = j + len(MARK)
    # word-initial positions in the composed span
    for m in re.finditer(r"[a-zA-Z]+", ln[start:]):
        pos = start + m.start()          # first byte of a composed word
        word = m.group(0)
        if len(word) < 3:
            continue
        ctx = ln[:pos]
        recent = ctx[-CTXWIN:]
        if word.lower() in recent.lower():
            continue                     # COPYABLE → skip (no routing signal there)
        # NON-COPYABLE word-initial → routing-signal position
        examples.append({"line": li, "pos": pos, "prompt": ctx,
                         "target": ord(ln[pos]) & 0xFF, "word": word})

rng = random.Random(SEED)
rng.shuffle(examples)
sub = examples[:N_TARGET]
for i, e in enumerate(sub):
    e["id"] = "n%05d" % i
json.dump({"n_items": len(sub), "n_all_nocopy": len(examples), "items": sub},
          open(OUT, "w"), ensure_ascii=False)
print("non-copyable word-initial composed positions total=%d → sampled=%d → %s" %
      (len(examples), len(sub), OUT))
# quick copy-audit of the sample (should be 0 copyable)
copyable = sum(1 for e in sub if e["word"].lower() in e["prompt"][-CTXWIN:].lower())
print("copyable in sample (should be 0):", copyable)
