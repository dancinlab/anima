#!/usr/bin/env python3
"""H_9915 -- is it the ENTITY's length, or the OPERATOR's byte offset from the query?

H_9914 established the trigger: the store readout works at exactly the trained entity length
(5 bytes) and collapses at 4, 6, 7, 8 and 9 alike. But "entity length" and "operator offset"
move together in that ladder. Windows are right-aligned padded, so "=> " always ends at T-1
and the operator's last byte sits at qpos - (len + 5): offset -10 at length 5, -11 at 6, -9
at 4. Every rung changed BOTH.

These arms separate them. Both frontier models, briefed independently, proposed the same
unconfounding move (fable's A3/A4, sol's P/E/D trio): change the operator's offset while
holding the entity at its trained length, and change one byte without moving the offset.

  A0  "{op} {e5} => "      offset -10   entity 5   trained condition = positive control
  A1  "{xx} {e5} => "      offset -10   entity 5   operator replaced by length-matched junk
                                                   -> MEASURED op-ablation floor, not assumed
  A3  "{op}  {e5} => "     offset -11   entity 5   THE DISCRIMINATOR: offset moved, length kept
  A3b "{op}   {e5} => "    offset -12   entity 5   dose: must mirror the length-7 numbers
  A4  " {op} {e5} => "     offset -10   entity 5   novelty-matched: one unseen byte, offset kept
  A6  "{op} {e5x} => "     offset -11   entity 6   H_9914 replication in the same batch

Predictions, so the arms falsify each other instead of all being "consistent with":

  POSITIONAL   A3 collapses to the length-6 numbers, A3b to length-7, A4 stays at 1.0
  CONTENT      A3 and A3b stay at 1.0 (no entity byte added), only A6 collapses
  GENERIC-OOD  A3, A3b and A4 all collapse together -- novelty alone, no structure

The op-ablation floor A1 matters because "collapsed" needs a shape to match, not just a
number below a bar: if the collapse arms reproduce A1's four-cell fingerprint, the operator
bit is being LOST rather than corrupted.
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


# op-ablation: same byte length as "is"/"not", consonant junk so it cannot be read as either
JUNK = {0: "qx", 1: "qxz"}
ARMS = {
    "A0_trained":   lambda op, w: "%s %s => "  % ("not" if op else "is", w),
    "A1_opjunk":    lambda op, w: "%s %s => "  % (JUNK[op], w),
    "A3_off11":     lambda op, w: "%s  %s => " % ("not" if op else "is", w),
    "A3b_off12":    lambda op, w: "%s   %s => " % ("not" if op else "is", w),
    "A4_leadspace": lambda op, w: " %s %s => " % ("not" if op else "is", w),
    "A6_len6":      lambda op, w: "%s %s => "  % ("not" if op else "is", w + rng.choice(CONS)),
}


def build(fmt):
    out = []
    for i in range(N_ITEM):
        op = i % 2
        pols = [0] * (N_SLOT // 2) + [1] * (N_SLOT // 2)
        rng.shuffle(pols)
        tslot = rng.randrange(N_SLOT)
        ents = rng.sample(nonce_pool, N_SLOT)      # inert under the oracle (v = val[pols])
        gold = "good" if (pols[tslot] == 0) != (op == 1) else "bad"
        out.append({"prompt": fmt(op, nonce()), "gold": gold, "entity": ents[tslot],
                    "store": {"entities": ents, "pols": pols},
                    "target_slot": tslot, "op": op})
    return out


for name, fmt in ARMS.items():
    m = dict(src)
    m["entries"] = build(fmt)
    m["arm"] = name
    p = "off_%s.json" % name
    json.dump(m, open(p, "w"), ensure_ascii=False)
    e = m["entries"][0]
    print("%-22s %3d items  prompt=%r  (entity %dB)"
          % (p, len(m["entries"]), e["prompt"], len(e["prompt"].split()[-2])))
