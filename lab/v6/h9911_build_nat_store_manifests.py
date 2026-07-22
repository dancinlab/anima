#!/usr/bin/env python3
"""H_9802 -- does NATURAL text address the store, and if not, where does addressing die?

The pre-check as originally written asks one question ("is natural text at the uniform
floor?"), and a single natural arm cannot answer it usefully: if it reads floor we still
would not know whether the store failed on the WORDS (nonce-trained keys do not recognise
real vocabulary) or on the SENTENCE (real left context swamps the query). Those want
different fixes, so the instrument is a ladder that changes exactly ONE thing per rung.

  C  template + nonce      "not kunem => "                        <- the trained condition
  E  template + real       "not government => "                   <- only the WORDS changed
  A  natural + real        "...long AP sentence ... government => " <- only the CONTEXT changed
  B  natural + absent      same as A, addressed word NOT in store <- FLOOR control

C is the positive control and it already reads a_max 0.7133 against a derived uniform of
0.1250. B is the floor: if A and B are equal, the address is not content-driven and the
comparison of A against C says nothing about naturalness.
"""
import json, re, random, sys, collections

CORPUS = "en_general.txt"
SRC    = "store.txt.held_balanced.json"
N_ITEM = 128
N_SLOT = 8
SEED   = 7

src = json.load(open(SRC))
nonce_pool = sorted({e for it in src["entries"] for e in it["store"]["entities"]})

raw = open(CORPUS, encoding="utf-8", errors="replace").read(12_000_000)

# real content words, length-matched to the 5-letter nonce keys so word LENGTH is not the
# thing that changed between rungs
words = re.findall(r"[a-z]{5,7}", raw.lower())
freq = collections.Counter(words)
STOP = {"which","would","there","their","about","these","other","after","first","could",
        "where","being","while","those","should","before","between","through","because",
        "under","again","still","every","might","never","since","during","against"}
real_pool = [w for w, c in freq.most_common(4000) if w not in STOP][:600]

# natural sentences that END in one of our real words (so the query position sits on the
# addressed word exactly as the template puts it there)
sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", raw[:6_000_000]) if 60 <= len(s) <= 240]
by_last = collections.defaultdict(list)
for s in sents:
    toks = re.findall(r"[A-Za-z]+", s)
    if len(toks) < 8:
        continue
    for w in toks[-6:]:
        lw = w.lower()
        if lw in set(real_pool):
            by_last[lw].append(s)
            break

rng = random.Random(SEED)


def entry(op, pols, ents, tslot, prompt):
    gold = "good" if (pols[tslot] == 0) != (op == 1) else "bad"
    return {"prompt": prompt, "gold": gold, "entity": ents[tslot],
            "store": {"entities": list(ents), "pols": list(pols)},
            "target_slot": tslot, "op": op}


def build(arm):
    out = []
    usable = [w for w in real_pool if by_last.get(w)]
    for i in range(N_ITEM):
        op = i % 2
        pols = [0] * (N_SLOT // 2) + [1] * (N_SLOT // 2)
        rng.shuffle(pols)
        tslot = rng.randrange(N_SLOT)
        if arm == "E":                                     # template + real words
            ents = rng.sample(real_pool, N_SLOT)
            prompt = "%s %s => " % ("not" if op else "is", ents[tslot])
        elif arm in ("A", "B"):                            # natural context
            key = usable[i % len(usable)]
            sent = rng.choice(by_last[key])
            if arm == "A":                                 # addressed word IS in the store
                ents = rng.sample([w for w in real_pool if w != key], N_SLOT - 1) + [key]
                rng.shuffle(ents)
                tslot = ents.index(key)
            else:                                          # FLOOR: addressed word ABSENT
                ents = rng.sample([w for w in real_pool if w != key], N_SLOT)
                tslot = rng.randrange(N_SLOT)
            prompt = "%s %s => " % (sent, "not" if op else "is")
            prompt = "%s %s %s => " % (sent, "not" if op else "is", key)
        else:
            raise ValueError(arm)
        out.append(entry(op, pols, ents, tslot, prompt))
    return out


for arm in ("E", "A", "B"):
    m = dict(src)
    m["entries"] = build(arm)
    m["arm"] = arm
    p = "nat_%s.json" % arm
    json.dump(m, open(p, "w"), ensure_ascii=False)
    e0 = m["entries"][0]
    print("%s  %d items  prompt=%r" % (p, len(m["entries"]), e0["prompt"][:110]))
print("real_pool=%d  nonce_pool=%d  sentences_with_usable_last=%d"
      % (len(real_pool), len(nonce_pool), sum(len(v) for v in by_last.values())))
