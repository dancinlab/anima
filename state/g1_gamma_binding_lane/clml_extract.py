#!/usr/bin/env python3
"""H_9235 fork-A CLML lane — training-example extractor (torch-free · procedural).
Parses the derivtrace corpus (anima corpus derivtrace, held-out pair excluded) into next-byte training
examples at the COMPOSED span (after 'out:'), where the lane must route both concepts from the definition
context to the composed output. Each example = (context prompt line[:pos], target byte line[pos]) at a
composed position; the T=24 window (right-aligned) is taken by the dump. Subsampled (seed) to keep the
one-time frozen-trunk yn dump feasible in numpy (a_scale_honest_scope).
Emits train_prompts.json for `anima evaluate --dump-hidden --with-logits`."""
import sys
import json
import random

DERIV = sys.argv[1] if len(sys.argv) > 1 else "deriv.txt"
OUT = sys.argv[2] if len(sys.argv) > 2 else "train_prompts.json"
N_TARGET = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
SEED = 7
MARK = "out:"

lines = [ln.rstrip("\n") for ln in open(DERIV) if ln.strip()]
examples = []
for li, ln in enumerate(lines):
    j = ln.find(MARK)
    if j < 0:
        continue                                  # single-concept line (no composition) — skip
    start = j + len(MARK)                          # first composed byte position (after 'out:')
    for pos in range(start, len(ln)):
        ctx = ln[:pos]
        if len(ctx) < 4:
            continue
        examples.append({"line": li, "pos": pos, "prompt": ctx, "target": ord(ln[pos]) & 0xFF})

rng = random.Random(SEED)
rng.shuffle(examples)
sub = examples[:N_TARGET]
for i, e in enumerate(sub):
    e["id"] = "t%05d" % i

json.dump({"n_items": len(sub), "n_all_composed": len(examples), "items": sub},
          open(OUT, "w"), ensure_ascii=False)
print("composed positions total=%d → sampled=%d (seed=%d) → %s" % (len(examples), len(sub), SEED, OUT))
