#!/usr/bin/env python3
"""H_9917 -- which property of the gap filler steers the failure: lexicality, byte class, entropy?

H_9916 found, exploratorily, that with the operator's offset held at 15 the direction of the
failure flips with what fills the span between the operator and the query:

    gap = spaces   kappa +0.962   (confident default-to-`is`)
    gap = letters  kappa -0.210   (biased toward `not`)

with overall accuracy 0.5156 in BOTH -- so overall cannot see the difference and kappa is the
primary DV. kappa = mean(is-cells) - mean(not-cells).

These arms hold the offset at 15 and the entity at its trained five bytes, and vary only the
five gap bytes. Each candidate predicts a different partition (frozen in the prereg):

    LEXICALITY   only pronounceable letters go negative; digits, punctuation and a repeated
                 character behave like spaces
    BYTE-CLASS   only space is special; digits, punctuation, letters and repeats all go negative
    ENTROPY      the low-entropy repeat behaves like spaces; random letters and digits go negative
"""
import json, random

SRC = "store.txt.held_balanced.json"
N_ITEM, N_SLOT, SEED = 128, 8, 7

src = json.load(open(SRC))
nonce_pool = sorted({e for it in src["entries"] for e in it["store"]["entities"]})
rng = random.Random(SEED)
CONS, VOW = "bdgkmnprstvz", "aeiou"


def nonce(L=5):
    s = ""
    while len(s) < L:
        s += rng.choice(CONS) + rng.choice(VOW)
    return s[:L]


GAPS = {
    "space":  lambda: "     ",
    "letters": lambda: nonce(5),
    "digits": lambda: "".join(rng.choice("0123456789") for _ in range(5)),
    "punct":  lambda: "".join(rng.choice(".,;:-") for _ in range(5)),
    "repeat": lambda: "zzzzz",
}


def build(gapfn):
    out = []
    for i in range(N_ITEM):
        op = i % 2
        pols = [0] * (N_SLOT // 2) + [1] * (N_SLOT // 2)
        rng.shuffle(pols)
        tslot = rng.randrange(N_SLOT)
        ents = rng.sample(nonce_pool, N_SLOT)      # inert under the oracle (v = val[pols])
        gold = "good" if (pols[tslot] == 0) != (op == 1) else "bad"
        # "{op} {gap5}{entity5} => "  -> operator's last byte sits 15 from the last index,
        # identical to lad_d5, so the ONLY variable across these arms is the gap's content.
        prompt = "%s %s%s => " % ("not" if op else "is", gapfn(), nonce(5))
        out.append({"prompt": prompt, "gold": gold, "entity": ents[tslot],
                    "store": {"entities": ents, "pols": pols},
                    "target_slot": tslot, "op": op})
    return out


for name, fn in GAPS.items():
    m = dict(src)
    m["entries"] = build(fn)
    m["arm"] = "gap_" + name
    p = "gap_%s.json" % name
    json.dump(m, open(p, "w"), ensure_ascii=False)
    e = m["entries"][0]
    off = len(e["prompt"]) - 1 - (1 if e["prompt"].startswith("is") else 2)
    print("%-18s %3d items  prompt=%r  len=%d  op-offset=%d"
          % (p, len(m["entries"]), e["prompt"], len(e["prompt"]), off))
