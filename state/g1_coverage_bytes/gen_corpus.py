#!/usr/bin/env python3
"""G1 coverage-density corpus generator (natural-language bytes, pair-specific recombination).

Design:
  - 24 concepts, each bound to a UNIQUE attribute via fact lines: "the ocean is silver ."
    (parts are taught identically in every arm)
  - composition rule via pair lines: "the ocean and the clock yield silver hollow ."
    (attributes in concept order -> answer for a held pair is a NEW combination of two
     learned parts, never a memorized string)
  - held: 60 ordered pairs, unseen in EVERY arm (same set across arms)
  - HIGH coverage: 400/552 ordered pairs (72%)  x 30 reps  = 12000 pair lines
  - LOW  coverage:  40/552 ordered pairs (7%, nested subset of HIGH) x 300 reps = 12000 pair lines
    -> size-matched in pair-line count (byte size within ~1%)
  - SHUFFLE control: identical to HIGH but each train pair gets a FIXED WRONG attribute pair
    (composition rule destroyed; template statistics preserved) -> held must fail
  - facts: 24 concepts x 250 reps = 6000 lines, identical in all arms

Measurement traps avoided:
  - v1 (too-strict): metric asks for attribute words, whose position after "yield" IS taught
    by the template -> seen-sanity can pass.
  - v2 (too-loose): success requires the two attributes SPECIFIC to the prompted pair
    (attributes are unique per concept) -> template-shaped babble scores 0.
"""
import argparse, json, os, random

CONCEPTS = ["ocean","clock","forest","mirror","candle","river","mountain","garden",
            "engine","letter","bridge","market","temple","harbor","meadow","lantern",
            "statue","orchard","tunnel","village","castle","desert","island","tower"]
ATTRS = ["silver","hollow","ancient","quiet","crimson","gentle","frozen","hidden",
         "rapid","golden","narrow","lively","sacred","misty","sunlit","amber",
         "marble","fragrant","shadowy","peaceful","mighty","barren","remote","lofty"]
SEED = 1234
HELD_N, HIGH_N, LOW_N = 60, 400, 40
HIGH_REP, LOW_REP, FACT_REP = 30, 300, 250
SEEN_EVAL_N = 60

def pair_line(c1, c2, a1, a2):
    return "the %s and the %s yield %s %s .\n" % (c1, c2, a1, a2)

def main(outdir):
    rng = random.Random(SEED)
    attr = dict(zip(CONCEPTS, ATTRS))
    pairs = [(a, b) for a in CONCEPTS for b in CONCEPTS if a != b]  # 552 ordered
    rng.shuffle(pairs)
    held = pairs[:HELD_N]
    avail = pairs[HELD_N:]
    high_train = avail[:HIGH_N]
    low_train = avail[:LOW_N]  # nested subset -> only coverage differs

    facts = ["the %s is %s .\n" % (c, attr[c]) for c in CONCEPTS for _ in range(FACT_REP)]

    sh_map = {}
    for (c1, c2) in high_train:
        while True:
            a1, a2 = rng.choice(ATTRS), rng.choice(ATTRS)
            if a1 != attr[c1] and a2 != attr[c2]:
                break
        sh_map[(c1, c2)] = (a1, a2)

    corpora = {
        "high": facts + [pair_line(c1, c2, attr[c1], attr[c2])
                         for (c1, c2) in high_train for _ in range(HIGH_REP)],
        "low": facts + [pair_line(c1, c2, attr[c1], attr[c2])
                        for (c1, c2) in low_train for _ in range(LOW_REP)],
        "shuffle": facts + [pair_line(c1, c2, sh_map[(c1, c2)][0], sh_map[(c1, c2)][1])
                            for (c1, c2) in high_train for _ in range(HIGH_REP)],
    }
    os.makedirs(outdir, exist_ok=True)
    sizes = {}
    for i, k in enumerate(sorted(corpora)):
        lines = corpora[k]
        random.Random(SEED + 7 * (i + 1)).shuffle(lines)
        blob = "".join(lines)
        with open(os.path.join(outdir, "corpus_%s.txt" % k), "w") as f:
            f.write(blob)
        sizes[k] = len(blob.encode())

    seen_eval = {
        "high": random.Random(SEED + 55).sample(high_train, SEEN_EVAL_N),
        "low": list(low_train),
        "shuffle": random.Random(SEED + 55).sample(high_train, SEEN_EVAL_N),
    }
    meta = {
        "seed": SEED, "attr": attr, "held": held,
        "high_train": high_train, "low_train": low_train,
        "shuffle_map": {"%s|%s" % (a, b): v for (a, b), v in sh_map.items()},
        "seen_eval": seen_eval,
        "reps": {"high": HIGH_REP, "low": LOW_REP, "fact": FACT_REP},
        "coverage": {"high": len(high_train) / float(len(pairs)),
                     "low": len(low_train) / float(len(pairs))},
        "bytes": sizes,
    }
    with open(os.path.join(outdir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=1)
    print("corpus bytes:", sizes)
    print("coverage:", meta["coverage"])

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=".")
    main(ap.parse_args().outdir)
