"""V6_15b -- the LONG-DISTANCE in-context binding supply, measured without a short-range regex.

ctx_payoff.py found 3/4259 constructions beyond the 35-byte receptive field.  That number
measures the INSTRUMENT, not the corpus: patterns like "X, the Y" and "X's Y" require literal
adjacency, so they cannot express a long-distance binding no matter how many the corpus holds.

The events that ARE long-distance are the ones natural prose runs on constantly and that no
short regex can catch:

  (a) NAME REINTRODUCTION -- an entity named early and named again later; the second mention
      must be linked to the first.
  (b) PRONOUN RESOLUTION  -- an entity named, then referred to by he/she/it/they/his/her/...

Both are measured by DISTANCE IN BYTES between the two mentions, against the mouth's 35-byte
receptive field.  Beyond that window the two mentions are, for this architecture, mathematically
independent -- a local conv cannot see them together.

ON-STANDARD (p9): natural corpus only.  DIRECTIONAL -- a property of the TEXT.
"""
import re
from collections import Counter

from corpus_path import natural_corpus

PATH = natural_corpus()
RF   = 35

ENT  = re.compile(r"\b([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,}){0,2})\b")
PRON = re.compile(r"\b(he|she|it|they|him|her|them|his|hers|its|their|theirs)\b", re.I)

def pct(rows, edges):
    n = len(rows)
    print("%-14s %9s %8s" % ("distance", "count", "share"))
    print("-" * 34)
    lo = 0
    for e in edges:
        c = sum(1 for d in rows if lo <= d < e)
        print("%-14s %9d %7.1f%%" % (f"{lo}-{e-1} B", c, 100 * c / n if n else 0))
        lo = e
    c = sum(1 for d in rows if d >= lo)
    print("%-14s %9d %7.1f%%" % (f">={lo} B", c, 100 * c / n if n else 0))
    beyond = sum(1 for d in rows if d > RF)
    print("-" * 34)
    print("beyond RF(%d B): %d / %d = %.1f%%" % (RF, beyond, n, 100 * beyond / n if n else 0))
    return beyond, n

lines = [l for l in open(PATH, encoding="utf-8", errors="replace").read().split("\n") if l.strip()]
mb = sum(len(l.encode()) for l in lines) / 1e6
print(f"natural corpus: {len(lines):,} lines · {mb:.2f} MB  (ON-STANDARD · p9)")
print(f"receptive field = {RF} bytes\n")

# (a) name reintroduction ------------------------------------------------------------
reintro, novel_pairs = [], Counter()
for l in lines:
    pos = {}
    for m in ENT.finditer(l):
        e = m.group(1).lower()
        if e in pos:
            reintro.append(m.start() - pos[e])
            novel_pairs[e] += 1
        pos[e] = m.start()
print("=" * 60)
print("(a) NAME REINTRODUCTION -- same entity named twice in one line")
print("=" * 60)
b1, n1 = pct(reintro, [10, 20, 35, 60, 100, 200])
print(f"density: {n1/mb:,.0f} / MB   beyond-RF: {b1/mb:,.0f} / MB\n")

# (b) pronoun resolution --------------------------------------------------------------
pron = []
for l in lines:
    ents = [(m.start(), m.group(1)) for m in ENT.finditer(l)]
    if not ents:
        continue
    for m in PRON.finditer(l):
        prev = [p for p, _ in ents if p < m.start()]
        if prev:
            pron.append(m.start() - max(prev))
print("=" * 60)
print("(b) PRONOUN RESOLUTION -- pronoun to its nearest preceding named entity")
print("=" * 60)
b2, n2 = pct(pron, [10, 20, 35, 60, 100, 200])
print(f"density: {n2/mb:,.0f} / MB   beyond-RF: {b2/mb:,.0f} / MB\n")

print("=" * 60)
print("VERDICT ON THE G1-ctx PREMISE")
print("=" * 60)
tb, tn = b1 + b2, n1 + n2
print(f"  long-distance in-context binding events: {tb:,} of {tn:,} ({100*tb/tn:.1f}%)")
print(f"  supply: {tb/mb:,.0f} per MB -- events the {RF}-byte receptive field CANNOT span")
print()
print(f"  compare G1-weight (the half the 212-panel measures):")
print(f"    a cross-line fact pair recurs 1.58x, 56% are seen exactly once")
print()
print("  So the premise survives its own instrument check ONLY if this number is large.")
