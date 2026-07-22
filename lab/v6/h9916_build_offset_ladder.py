#!/usr/bin/env python3
"""H_9916 -- is the operator-offset damage MONOTONE, or PERIODIC in the trunk's dilations?

H_9915 confirmed POSITIONAL: shifting the operator one byte further from the query with a
single space collapses the store readout (1.0000 -> 0.6406) exactly as much as making the
entity a byte longer, while a space that does NOT move the operator leaves it at 1.0000.

That leaves the shape of the damage open, and the shape names the culprit. This ckpt is
E=3 embed convs, L=4 trunk layers, K=3, and `core/model.py:414` sets trunk dilations to
`min(2**i, cap)` for i in 0..L-1 -- so 1, 2, 4, 8.

A dilation-d causal conv with K=3 taps positions t, t-d, t-2d. If the operator is read by
such a tap, moving it by delta bytes breaks the alignment UNLESS delta is a multiple of d.
So the two shapes make opposite, falsifiable predictions:

  MONOTONE / POINT   every delta >= 1 stays collapsed; the model reads the operator at
                     exactly one distance and nowhere else
  PERIODIC-d         accuracy RECOVERS at delta in {2, 4, 8} -- and which delta recovers
                     names the dilation, hence the layer

Arms are delta = 0..8 spaces inserted between the operator and the entity. Entity stays at
the trained 5 bytes throughout, so entity length is held constant by construction and only
the operator's distance from the query moves. delta=0 is the trained condition and the
positive control.
"""
import json, random

SRC = "store.txt.held_balanced.json"
N_ITEM, N_SLOT, SEED, DELTAS = 128, 8, 7, range(0, 9)

src = json.load(open(SRC))
nonce_pool = sorted({e for it in src["entries"] for e in it["store"]["entities"]})
rng = random.Random(SEED)
CONS, VOW = "bdgkmnprstvz", "aeiou"


def nonce(L=5):
    s = ""
    while len(s) < L:
        s += rng.choice(CONS) + rng.choice(VOW)
    return s[:L]


def build(delta):
    out = []
    for i in range(N_ITEM):
        op = i % 2
        pols = [0] * (N_SLOT // 2) + [1] * (N_SLOT // 2)
        rng.shuffle(pols)
        tslot = rng.randrange(N_SLOT)
        ents = rng.sample(nonce_pool, N_SLOT)        # inert under the oracle (v = val[pols])
        gold = "good" if (pols[tslot] == 0) != (op == 1) else "bad"
        prompt = "%s%s%s => " % ("not" if op else "is", " " * (delta + 1), nonce())
        out.append({"prompt": prompt, "gold": gold, "entity": ents[tslot],
                    "store": {"entities": ents, "pols": pols},
                    "target_slot": tslot, "op": op})
    return out


for d in DELTAS:
    m = dict(src)
    m["entries"] = build(d)
    m["arm"] = "delta%d" % d
    p = "lad_d%d.json" % d
    json.dump(m, open(p, "w"), ensure_ascii=False)
    e = m["entries"][0]
    print("%-14s delta=%d  %3d items  prompt=%r  (%dB)"
          % (p, d, len(m["entries"]), e["prompt"], len(e["prompt"])))
