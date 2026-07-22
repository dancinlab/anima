#!/usr/bin/env python3
"""H_9914 -- under the oracle the store is never read, so what is left is the prompt.

core/clms.py:160 with oracle=True sets a = one_hot(target_slot), and for lane_type 3 that
gives v = val[pol_target] - mean(val[pols]). The entity strings enter only through K, and K
is used nowhere on this path. So the store's CONTENTS cannot explain H_9913's oracle gap
(C nonce 1.0000 vs E real 0.6641) -- only the prompt bytes can, through h at the query
position and g = h @ W_g.

But "the prompt" still hides two candidates, and they want different fixes:

  LENGTH      the trained nonce are all 5 letters; the real words are 5-7, so the prompt is
              longer and the query sits at a different offset in the window
  VOCABULARY  the trunk represents a real English word differently from a nonce string

This builds arms that separate them: nonce at lengths 5/6/7 against real words at lengths
5/6/7, same template, same store construction, same pol balance. If oracle accuracy tracks
LENGTH across both vocabularies, the cause is window geometry. If it tracks nonce-vs-real at
matched length, the cause is vocabulary. If both move, both contribute and the split says
how much.

Store contents are irrelevant under the oracle by construction, so they are held at the
original nonce pool throughout -- changing them would only add a variable that cannot act.
"""
import json, re, random, collections

SRC = "store.txt.held_balanced.json"
CORPUS = "en_general.txt"
N_ITEM, N_SLOT, SEED = 128, 8, 7

src = json.load(open(SRC))
nonce_pool = sorted({e for it in src["entries"] for e in it["store"]["entities"]})
assert all(len(w) == 5 for w in nonce_pool), "the trained nonce pool is not uniformly 5 bytes"

raw = open(CORPUS, encoding="utf-8", errors="replace").read(12_000_000)
STOP = {"which", "would", "there", "their", "about", "these", "other", "after", "first",
        "could", "where", "being", "while", "those", "should", "before", "between",
        "through", "because", "under", "again", "still", "every", "might", "never",
        "since", "during", "against"}
freq = collections.Counter(re.findall(r"[a-z]+", raw.lower()))
real_by_len = {L: [w for w, c in freq.most_common(20000)
                   if len(w) == L and w not in STOP][:400] for L in (5, 6, 7)}

rng = random.Random(SEED)
CONS, VOW = "bdgkmnprstvz", "aeiou"


def nonce(L):
    """same shape as the trained pool (alternating CV), extended to length L"""
    s = ""
    while len(s) < L:
        s += rng.choice(CONS) + rng.choice(VOW)
    return s[:L]


def build(kind, L):
    out = []
    for i in range(N_ITEM):
        op = i % 2
        pols = [0] * (N_SLOT // 2) + [1] * (N_SLOT // 2)
        rng.shuffle(pols)
        tslot = rng.randrange(N_SLOT)
        ents = rng.sample(nonce_pool, N_SLOT)          # never read under the oracle
        word = nonce(L) if kind == "nonce" else rng.choice(real_by_len[L])
        gold = "good" if (pols[tslot] == 0) != (op == 1) else "bad"
        out.append({"prompt": "%s %s => " % ("not" if op else "is", word),
                    "gold": gold, "entity": ents[tslot],
                    "store": {"entities": ents, "pols": pols},
                    "target_slot": tslot, "op": op})
    return out


for kind in ("nonce", "real"):
    for L in (5, 6, 7):
        m = dict(src)
        m["entries"] = build(kind, L)
        m["arm"] = "%s%d" % (kind, L)
        p = "len_%s%d.json" % (kind, L)
        json.dump(m, open(p, "w"), ensure_ascii=False)
        print("%-18s %3d items  prompt=%r" % (p, len(m["entries"]), m["entries"][0]["prompt"]))
print("real pool sizes:", {L: len(v) for L, v in real_by_len.items()})
