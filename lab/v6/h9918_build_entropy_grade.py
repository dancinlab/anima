#!/usr/bin/env python3
"""H_9918 -- is the gap's variety a GRADE or a SWITCH?

H_9917 left ENTROPY as "supported" rather than confirmed because it measured only two points
of variety -- one distinct character (spaces +0.957, "zzzzz" +0.693) against five distinct
ones (letters -0.534, digits -0.741). That separates "variety is the variable" from
lexicality and byte class, but it cannot say whether variety acts as a continuous grade or as
a binary switch that trips the moment anything varies at all.

So: hold the gap to five bytes of LETTERS throughout (byte class is already killed), hold the
operator's offset at 15 and the entity at its trained five bytes, and vary only k, the number
of DISTINCT characters in the gap: 1, 2, 3, 5.

  GRADED  kappa falls monotonically with k, with real gaps between neighbours
  SWITCH  only k=1 is positive; k=2, 3 and 5 sit together
  NULL    kappa does not move with k -- H_9917's axis was not variety after all
"""
import json, random

SRC = "store.txt.held_balanced.json"
N_ITEM, N_SLOT, SEED, GAP = 128, 8, 7, 5
KS = (1, 2, 3, 5)

src = json.load(open(SRC))
nonce_pool = sorted({e for it in src["entries"] for e in it["store"]["entities"]})
rng = random.Random(SEED)
CONS, VOW = "bdgkmnprstvz", "aeiou"
ALPHA = CONS + VOW


def nonce(L=5):
    s = ""
    while len(s) < L:
        s += rng.choice(CONS) + rng.choice(VOW)
    return s[:L]


def gap_with_k(k):
    """Five letters drawn from exactly k distinct characters. Every one of the k appears at
    least once (otherwise the realised k would be smaller than the nominal one), then the
    remaining slots are filled from the same k and the whole thing is shuffled."""
    chars = rng.sample(ALPHA, k)
    out = list(chars) + [rng.choice(chars) for _ in range(GAP - k)]
    rng.shuffle(out)
    return "".join(out)


def build(k):
    out = []
    for i in range(N_ITEM):
        op = i % 2
        pols = [0] * (N_SLOT // 2) + [1] * (N_SLOT // 2)
        rng.shuffle(pols)
        tslot = rng.randrange(N_SLOT)
        ents = rng.sample(nonce_pool, N_SLOT)      # inert under the oracle (v = val[pols])
        gold = "good" if (pols[tslot] == 0) != (op == 1) else "bad"
        prompt = "%s %s%s => " % ("not" if op else "is", gap_with_k(k), nonce(5))
        out.append({"prompt": prompt, "gold": gold, "entity": ents[tslot],
                    "store": {"entities": ents, "pols": pols},
                    "target_slot": tslot, "op": op})
    return out


for k in KS:
    m = dict(src)
    m["entries"] = build(k)
    m["arm"] = "k%d" % k
    p = "ent_k%d.json" % k
    json.dump(m, open(p, "w"), ensure_ascii=False)
    e = m["entries"][0]
    off = len(e["prompt"]) - 1 - (1 if e["prompt"].startswith("is") else 2)
    realised = len(set(e["prompt"].split()[1][:GAP]))
    print("%-14s k=%d  %3d items  prompt=%r  op-offset=%d  realised-k(first)=%d"
          % (p, k, len(m["entries"]), e["prompt"], off, realised))
