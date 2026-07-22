"""Is the scale curve an artifact of NESTED PREFIXES? Re-measure on DISJOINT samples.

V6_14 built its ladder from nested prefixes of one corpus, so each point contained every
smaller point. That makes the points non-independent and could manufacture a slope: a
larger prefix necessarily re-encounters everything the smaller one saw.

This re-runs the same measurement on DISJOINT random document blocks -- each size uses
DIFFERENT text, nothing shared. If the exponent survives, nesting was not the cause. If it
collapses, V6_14's extrapolation is void and the card has to be withdrawn.

ON-STANDARD: measures the natural corpus.
"""
import re, sys, math, collections, itertools, random

PATH = "/Users/mini/anima-weights/study303_long_transcript/cpt_mix.txt"
ENT = re.compile(r"\b[A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})*\b")
STOP = {"The","This","That","These","Those","There","When","While","After","Before",
        "However","Although","Because","During","Some","Many","Most","Their","They",
        "It","In","On","At","For","From","With","And","But","New","List"}

def audit(txt):
    pair = collections.Counter(); ents = collections.Counter(); n = 0
    for s in re.split(r"(?<=[.!?])\s+", txt):
        s = s.strip()
        if not (20 < len(s) < 600):
            continue
        n += 1
        e = {x for x in ENT.findall(s) if x.split()[0] not in STOP and len(x) > 3}
        for x in e:
            ents[x] += 1
        for a, b in itertools.combinations(sorted(e), 2):
            pair[(a, b)] += 1
    if not pair:
        return None
    tot = len(pair)
    once = sum(1 for v in pair.values() if v == 1)
    rep3 = sum(1 for v in pair.values() if v >= 3)
    return dict(sent=n, pairs=tot, once=100*once/tot,
                rep2=100*(tot-once)/tot, rep3=100*rep3/tot)

def fit(pts, key):
    xs = [math.log(m) for m, _ in pts]; ys = [math.log(r[key]) for _, r in pts]
    n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
    a = sum((x-mx)*(y-my) for x, y in zip(xs, ys))/sum((x-mx)**2 for x in xs)
    b = my - a*mx
    ss = sum((y-(a*x+b))**2 for x, y in zip(xs, ys)); st = sum((y-my)**2 for y in ys)
    return a, b, (1-ss/st if st else float("nan"))

def main():
    full = open(PATH, encoding="utf-8", errors="ignore").read()
    blocks = [b for b in full.split("\n") if len(b) > 40]
    rng = random.Random(7)
    rng.shuffle(blocks)
    print("DISJOINT-sample ladder — breaks V6_14's nested-prefix dependence")
    print("each size drawn from a DIFFERENT, non-overlapping slice of the shuffled corpus\n")
    print("%8s %8s %10s  %8s %8s %8s" % ("MB", "sents", "pairs", "seen 1x", ">=2x", ">=3x"))
    print("-" * 60)
    pts = []
    cursor = 0
    for frac in (0.0625, 0.125, 0.25, 0.5):
        want = int(len(full) * frac)
        chunk, got = [], 0
        while cursor < len(blocks) and got < want:
            chunk.append(blocks[cursor]); got += len(blocks[cursor]) + 1; cursor += 1
        if got < want * 0.9:
            break
        r = audit("\n".join(chunk))
        if not r:
            continue
        mb = got/1e6
        pts.append((mb, r))
        print("%8.2f %8s %10s  %7.1f%% %7.1f%% %7.1f%%" %
              (mb, f"{r['sent']:,}", f"{r['pairs']:,}", r["once"], r["rep2"], r["rep3"]))
    print("-" * 60)
    print()
    if len(pts) < 3:
        print("INSUFFICIENT — corpus too small to build disjoint blocks at these sizes.")
        return 1
    print("%-12s %10s %10s   %s" % ("series", "alpha", "R^2", "V6_14 (nested) alpha"))
    print("-" * 60)
    for key, nested in (("rep2", 0.845), ("rep3", 0.897)):
        a, b, r2 = fit(pts, key)
        d = a - nested
        print("%-12s %10.3f %10.4f   %.3f   (delta %+.3f)" % (key, a, r2, nested, d))
    a2, _, _ = fit(pts, "rep2"); a3, _, _ = fit(pts, "rep3")
    print()
    if abs(a2-0.845) < 0.15 and abs(a3-0.897) < 0.15:
        print("REPLICATES — the exponents survive on non-overlapping text, so V6_14's slope")
        print("was not manufactured by prefix nesting. The extrapolation keeps its footing")
        print("(its OTHER limits -- crude entity extraction, co-occurrence rather than stated")
        print("relations, an assumed >=3x threshold -- are untouched by this check).")
    else:
        print("DOES NOT REPLICATE — exponents move by %+.3f / %+.3f on disjoint text."
              % (a2-0.845, a3-0.897))
        print("V6_14's extrapolation rested on nesting and must be withdrawn or re-derived.")
    return 0

sys.exit(main())
