"""V6_15 -- CONSTRUCTION PAYOFF: why in-context binding could be learned where weight-fact binding is not.

Divergence 07's mechanism: below capacity, memorization is strictly cheaper than composition
under CE.  4.8MB << 170MB capacity, so the model CAN memorize every line.  That refutes the
naive "novel referent" resolution -- a within-line binding IS memorizable by memorizing the line.

The surviving resolution is ECONOMIC, and it is a corpus statistic, so it is measurable at $0:

    payoff(mechanism) = how many times learning it once pays off
                      = frequency of the CONSTRUCTION
    payoff(memorizing) = 1 per instance

A construction repeated N times with novel fillers each time pays N-fold for one mechanism;
memorizing pays once per line.  If G1-ctx constructions repeat 10^3-10^4x while their fillers
are near-unique, and G1-weight "constructions" (a specific fact pair) repeat ~1x, the two halves
of G1 sit on OPPOSITE sides of the same economics -- with no appeal to architecture at all.

ON-STANDARD (p9): natural corpus only.  DIRECTIONAL -- this is a property of the TEXT, and it
says what the objective PRICES, not what the model learned.  Nothing here cements anything.
"""
import re, sys
from collections import Counter

from corpus_path import natural_corpus

PATH = natural_corpus()
RF   = 35   # mouth receptive field in BYTES -- below this a bigram continuation suffices

ENT = re.compile(r"\b([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,}){0,2})\b")

# Binding CONSTRUCTIONS: each pairs two slots that must be held together.
# The construction is the TYPE (shared, repeatable); the slot fillers are the TOKENS (novel).
CONSTRUCTIONS = {
    "appositive  'X, the Y'":  re.compile(r"([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,}){0,2}),\s+(?:the\s+|an?\s+)([a-z]{3,}(?:\s+[a-z]{3,}){0,2})[,.]"),
    "copular     'X is a Y'":  re.compile(r"([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,}){0,2})\s+(?:is|was|were|are)\s+(?:the\s+|an?\s+)([a-z]{3,}(?:\s+[a-z]{3,}){0,2})\b"),
    "relative    'X who/which'":re.compile(r"([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,}){0,2}),?\s+(who|which|whose)\s+([a-z]{3,})"),
    "possessive  \"X's Y\"":   re.compile(r"([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,}){0,2})'s\s+([a-z]{3,}(?:\s+[a-z]{3,}){0,1})\b"),
    "of-relation 'the Y of X'":re.compile(r"the\s+([a-z]{3,}(?:\s+[a-z]{3,}){0,1})\s+of\s+([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,}){0,2})\b"),
}

def main():
    lines = [l for l in open(PATH, encoding="utf-8", errors="replace").read().split("\n") if l.strip()]
    mb = sum(len(l.encode()) for l in lines) / 1e6
    print(f"natural corpus: {len(lines):,} lines · {mb:.2f} MB  (ON-STANDARD · p9)")
    print(f"mouth receptive field = {RF} bytes -- a meeting FARTHER apart than this cannot be a bigram continuation")
    print()

    # ---- line duplication: can the model just memorize the lines? -------------------
    lc = Counter(lines)
    dup = sum(c for c in lc.values() if c > 1)
    print(f"line duplication: {len(lc):,} distinct / {len(lines):,}  ({100*dup/len(lines):.1f}% of lines are repeats)")
    print(f"  -> capacity is ~170MB and the corpus is {mb:.1f}MB, so memorizing every line is AFFORDABLE.")
    print(f"     'the referent is novel' therefore does NOT by itself resolve the tension.")
    print()

    # ---- G1-ctx supply: constructions -----------------------------------------------
    print("=" * 88)
    print("G1-ctx -- BINDING CONSTRUCTIONS (both slots present in the same line)")
    print("=" * 88)
    print("%-28s %9s %9s %9s %9s %9s" % ("construction (TYPE)", "count", "beyondRF", "distinct", "novel%", "payoff"))
    print("-" * 88)
    tot_ct = tot_rf = 0
    for name, rx in CONSTRUCTIONS.items():
        fills, beyond = [], 0
        for l in lines:
            for m in rx.finditer(l):
                g = m.groups()
                a, b = (g[0], g[-1])
                fills.append((a.lower(), b.lower()))
                # slot separation in bytes, from start of slot 1 to start of slot 2
                if abs(m.start(len(g)) - m.start(1)) > RF:
                    beyond += 1
        if not fills:
            continue
        fc = Counter(fills)
        novel = 100.0 * sum(1 for v in fc.values() if v == 1) / len(fc)
        payoff = len(fills) / (len(fills) / len(fc))   # = distinct-normalised type frequency
        tot_ct += len(fills); tot_rf += beyond
        print("%-28s %9d %9d %9d %8.1f%% %9d" % (name, len(fills), beyond, len(fc), novel, len(fc)))
    print("-" * 88)
    print("%-28s %9d %9d" % ("TOTAL", tot_ct, tot_rf))
    print()
    print(f"density: {tot_ct/mb:,.0f} binding constructions per MB "
          f"({tot_rf/mb:,.0f}/MB with the slots farther apart than the {RF}-byte receptive field)")
    print()
    print("READ: 'payoff' is the number of DISTINCT filler pairs the construction is asked to serve.")
    print("      Learn the construction once -> it pays off that many times.")
    print("      Memorize a line -> it pays off ONCE, and only for that line.")

    # ---- G1-weight supply, same corpus, for the contrast ---------------------------
    print()
    print("=" * 88)
    print("G1-weight -- CROSS-LINE ENTITY PAIRS (the half the 212-panel measures)")
    print("=" * 88)
    ent_lines = {}
    for i, l in enumerate(lines):
        for e in set(m.group(1).lower() for m in ENT.finditer(l)):
            ent_lines.setdefault(e, set()).add(i)
    pair = Counter()
    for i, l in enumerate(lines):
        es = sorted(set(m.group(1).lower() for m in ENT.finditer(l)))
        for x in range(len(es)):
            for y in range(x + 1, len(es)):
                pair[(es[x], es[y])] += 1
    singles = sum(1 for v in pair.values() if v == 1)
    print(f"distinct entity pairs: {len(pair):,}   seen exactly once: {singles:,} ({100*singles/len(pair):.1f}%)")
    print(f"mean repetitions per pair: {sum(pair.values())/len(pair):.2f}")
    print()
    print("=" * 88)
    print("THE CONTRAST")
    print("=" * 88)
    ratio = (tot_ct / len(CONSTRUCTIONS)) / (sum(pair.values()) / len(pair))
    print(f"  a G1-ctx construction is reused ...... {tot_ct//len(CONSTRUCTIONS):,}x on average (per construction type)")
    print(f"  a G1-weight fact pair is reused ...... {sum(pair.values())/len(pair):.2f}x")
    print(f"  ratio ................................ {ratio:,.0f}x")
    print()
    print("  Same corpus. Same objective. Same architecture. The two halves of G1 differ by ~10^4")
    print("  in how often learning the thing pays off -- which is exactly the quantity CE optimises.")

main()
