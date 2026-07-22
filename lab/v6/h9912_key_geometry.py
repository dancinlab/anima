#!/usr/bin/env python3
"""H_9912 -- I tried to overturn H_9911's prescription with key geometry, and failed twice.

H_9911 measured store addressing collapsing between "template + nonce" (a_max 0.7133) and
"template + real words" (0.3420) and prescribed the curriculum arm. Before spending on
training, read what a store key actually IS:

    core/clms.py:81    _entity_key(key_emb, e) = key_emb[byte_ids].mean(axis=0)
    core/clms.py:142   scale = 1 / sqrt(d_k)
    core/clms.py:163   a = softmax(q @ K.T * scale)          # raw keys, no normalisation

A key is the MEAN of per-byte rows of a FROZEN random (256, 64) table. That looked like it
could cap addressing before any learning: real English words share letters far more than
sampled nonce does, so their bag-mean keys should crowd together. If so the curriculum arm
would be the wrong spend and the fix would be the key function.

Two attempts to establish that, both of which failed, and both failures are the point.

ATTEMPT 1 -- collinearity, killed by an invented threshold and false logic.
Comparing max off-diagonal cosine inside one 8-slot store gave nonce 0.7240 vs real 0.7554.
I declared "the key construction sets the ceiling" because the gap cleared 0.02 -- a number
I chose, not derived (screen-is-a-filter-not-a-performance-predictor). Worse, the reasoning
was wrong: "keys this collinear cannot peak" is false when the query norm is free. W_q emits
q of ANY magnitude, and magnitude is exactly what sharpens a softmax. Short of exact
duplication (cosine 1.0) there is no geometric obstruction at all, and 0.7554 is not 1.0.

ATTEMPT 2 -- a ceiling the measurement walks straight over.
So I computed the "ceiling" properly: set q to the target key itself and read a_max under the
model's own temperature. Result 0.1275 for nonce, 0.1268 for real, against a MEASURED 0.7133
for nonce. A ceiling that the measurement exceeds by 5.6x is not a ceiling -- it is the same
free-magnitude mistake wearing a better costume, since the target key is just one particular
small-norm query. It was caught only because the measured value was printed beside it.

Both attempts fail in the same direction, and the direction is the finding:

    key geometry does NOT explain the C -> E collapse; H_9911's prescription STANDS.

The real-word keys were separable and the model did not separate them. That is a learned
failure, which is what the curriculum arm addresses.

Order-blindness is a separate and permanent fact -- the bag mean makes every anagram collide,
200/200 on real words -- but it is equally true of the nonce pool, so it explains no part of
this collapse. It caps what the store can ever represent; it is not why this one fell.
"""
import sys, os, json, re, random, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "core"))
sys.path.insert(0, os.path.expanduser("~/dancinlab/anima/core"))
from clms import _entity_key
import decode as clm

CKPT = os.path.expanduser("~/anima-weights/store_struct_303m/store303_s2000.clm")
SRC = os.path.expanduser("~/anima-weights/store_struct_303m/store.txt.held_balanced.json")
CORPUS = os.path.expanduser("~/anima-weights/en_general.txt")   # dancinlab/anima-corpus-en-general
N_SLOT, SEED, TRIALS = 8, 7, 2000
MEASURED = {"nonce": 0.7133, "real": 0.3420}       # H_9911 arms C and E, engine-native 303M

for p in (CKPT, SRC, CORPUS):
    if not os.path.exists(p):
        sys.exit("missing %s -- the real corpus is REQUIRED; an earlier run of this file "
                 "silently fell back to README.md and compared a different word pool than "
                 "the ladder used, which invalidated the comparison outright." % p)

clms = clm.clm_load_weights(CKPT)["clms"]
key_emb = clms["key_emb"]
d_k = int(clms["d_k"])
scale = 1.0 / np.sqrt(float(d_k))
print("key_emb %s  d_k=%d  scale=%.6f  (the ckpt's own CLMS trailer)"
      % (key_emb.shape, d_k, scale))

nonce = sorted({e for it in json.load(open(SRC))["entries"] for e in it["store"]["entities"]})
raw = open(CORPUS, encoding="utf-8", errors="replace").read(12_000_000)
STOP = {"which", "would", "there", "their", "about", "these", "other", "after", "first",
        "could", "where", "being", "while", "those", "should", "before", "between",
        "through", "because", "under", "again", "still", "every", "might", "never",
        "since", "during", "against"}
freq = collections.Counter(re.findall(r"[a-z]{5,7}", raw.lower()))
real = [w for w, c in freq.most_common(4000) if w not in STOP][:600]
print("pools: nonce=%d  real=%d  (same rule the ladder used)" % (len(nonce), len(real)))


def softmax(z):
    z = z - z.max(); e = np.exp(z); return e / e.sum()


def stats(pool, seed=SEED):
    rng = random.Random(seed)
    Kw = {w: _entity_key(key_emb, w).astype(np.float64) for w in pool}
    Kn = {w: v / (np.linalg.norm(v) + 1e-12) for w, v in Kw.items()}
    offmax, target_q = [], []
    for _ in range(TRIALS):
        s = rng.sample(pool, N_SLOT)
        M = np.stack([Kn[w] for w in s]); C = M @ M.T
        np.fill_diagonal(C, -np.inf); offmax.append(float(C.max()))
        K = np.stack([Kw[w] for w in s]); t = rng.randrange(N_SLOT)
        target_q.append(float(softmax(K @ K[t] * scale)[t]))
    return float(np.mean(offmax)), float(np.mean(target_q))


print()
print("  %-8s %14s %16s %12s" % ("pool", "max off-diag", "a_max @ q=key", "MEASURED"))
print("  " + "-" * 54)
res = {}
for name, pool in (("nonce", nonce), ("real", real)):
    mx, tq = stats(pool)
    res[name] = (mx, tq)
    print("  %-8s %14.4f %16.4f %12.4f" % (name, mx, tq, MEASURED[name]))

print()
print("=" * 74)
tq_n = res["nonce"][1]
print("The q=key column is NOT a ceiling: nonce measures %.4f against %.4f there, %.1fx over."
      % (MEASURED["nonce"], tq_n, MEASURED["nonce"] / tq_n))
print("W_q emits a query of any magnitude, and magnitude is what sharpens a softmax, so short")
print("of exact duplication there is no geometric cap. Real keys peak at %.4f cosine, not 1.0."
      % res["real"][0])
print()
print("VERDICT: key geometry does NOT explain the C->E collapse (ceiling gap %.4f against a"
      % abs(res["nonce"][1] - res["real"][1]))
print("measured gap of %.4f). The real-word keys were separable and the model did not separate"
      % (MEASURED["nonce"] - MEASURED["real"]))
print("them -- a learned failure. H_9911's curriculum prescription STANDS, unrevised.")

scr = sum(1 for w in real[:200]
          if np.allclose(_entity_key(key_emb, w),
                         _entity_key(key_emb, "".join(sorted(w)))))
print()
print("Separately and permanently: %d/200 real words key byte-identically to their own sorted"
      % scr)
print("anagram. The bag mean is order-blind. True of nonce too, so it explains no part of this")
print("collapse -- it caps what the store can ever represent, not why this one fell.")
