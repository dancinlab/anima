"""V6_16 -- the LOCAL-AMBIGUITY filter both divergence models independently demanded.

V6_15 measured 2,234 long-distance binding events per MB of natural text.  Fable and Sol,
working in parallel and blind to each other, each refused that number as a supervision
density and named the SAME missing filter:

    Sol : "Calling the entity-meeting rate 'G1-ctx supervision density' -- it is an upper
           bound until write->read, ambiguity, and local-shortcut filters are applied."
           "Measure the mass where H(Y | X_35) > 0 and distant binding reduces it."

The reason is exact.  A long-range binding event creates CE pressure for a transport
mechanism ONLY IF the local window cannot already answer.  If the 35 bytes before the target
determine the next byte -- because that exact context occurs once, or always continues the
same way -- then the model needs no lane, and the event is free to memorize.

So the honest quantity is not "events beyond RF" but:

    PRESSURE SITE  =  an event beyond RF whose 35-byte local context is GENUINELY AMBIGUOUS
                      in this corpus:  seen >= 2 times, continuing >= 2 different ways.

This is a filter that can only SHRINK V6_15's number.  If it collapses, my number was an
upper bound that does not survive, and I say so.

ON-STANDARD (p9): natural corpus, unchanged.  DIRECTIONAL -- a property of the text.
"""
import re
from collections import Counter, defaultdict

PATH = "/Users/mini/anima-weights/study303_long_transcript/cpt_mix.txt"
RF   = 35

ENT  = re.compile(rb"\b([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,}){0,2})\b")
PRON = re.compile(rb"\b(he|she|it|they|him|her|them|his|hers|its|their|theirs)\b", re.I)

raw   = open(PATH, "rb").read()
lines = [l for l in raw.split(b"\n") if l.strip()]
mb    = sum(len(l) for l in lines) / 1e6
print(f"natural corpus: {len(lines):,} lines · {mb:.2f} MB  (ON-STANDARD · p9)")
print(f"receptive field = {RF} bytes\n")

# ---- 1. harvest the beyond-RF events V6_15 counted, keeping their local context ----------
sites = []   # (kind, 35-byte local context before target, target byte)
for l in lines:
    pos = {}
    for m in ENT.finditer(l):
        e = m.group(1).lower()
        if e in pos and m.start() - pos[e] > RF and m.start() >= RF:
            sites.append(("name", bytes(l[m.start()-RF:m.start()]), l[m.start():m.start()+1]))
        pos[e] = m.start()
    ents = [m.start() for m in ENT.finditer(l)]
    if ents:
        for m in PRON.finditer(l):
            prev = [p for p in ents if p < m.start()]
            if prev and m.start() - max(prev) > RF and m.start() >= RF:
                sites.append(("pron", bytes(l[m.start()-RF:m.start()]), l[m.start():m.start()+1]))
print(f"beyond-RF events (V6_15's number): {len(sites):,}  =  {len(sites)/mb:,.0f} /MB")

# ---- 2. how ambiguous is each site's local context, ACROSS THE WHOLE CORPUS? ------------
want = set(c for _, c, _ in sites)
print(f"distinct local contexts to resolve: {len(want):,}")

seen = defaultdict(set)      # context -> set of bytes that follow it anywhere in the corpus
cnt  = Counter()             # context -> how many times it occurs at all
for i in range(len(raw) - RF):
    c = raw[i:i+RF]
    if c in want:
        cnt[c] += 1
        seen[c].add(raw[i+RF])

uniq   = sum(1 for _, c, _ in sites if cnt[c] <= 1)
determ = sum(1 for _, c, _ in sites if cnt[c] > 1 and len(seen[c]) == 1)
ambig  = sum(1 for _, c, _ in sites if cnt[c] > 1 and len(seen[c]) > 1)

print()
print("=" * 74)
print("LOCAL-AMBIGUITY BREAKDOWN of the beyond-RF events")
print("=" * 74)
print("%-46s %9s %8s" % ("local 35-byte context is...", "count", "share"))
print("-" * 74)
n = len(sites)
print("%-46s %9d %7.1f%%   -> memorizable, NO pressure" % ("unique in the corpus (seen once)", uniq, 100*uniq/n))
print("%-46s %9d %7.1f%%   -> determined, NO pressure" % ("repeated but always same continuation", determ, 100*determ/n))
print("%-46s %9d %7.1f%%   -> PRESSURE SITE" % ("repeated AND continues >=2 ways", ambig, 100*ambig/n))
print("-" * 74)
print(f"PRESSURE SITES: {ambig:,} = {ambig/mb:,.0f} /MB")
print()
print("by event kind:")
for k in ("name", "pron"):
    tot = sum(1 for kk, _, _ in sites if kk == k)
    amb = sum(1 for kk, c, _ in sites if kk == k and cnt[c] > 1 and len(seen[c]) > 1)
    print("  %-6s  %6d beyond-RF -> %5d pressure (%.1f%%)  %6.0f /MB" % (k, tot, amb, 100*amb/tot if tot else 0, amb/mb))

print()
print("=" * 74)
print("VERDICT ON V6_15's NUMBER")
print("=" * 74)
print(f"  V6_15 reported ......... {n/mb:,.0f} /MB   (beyond-RF events)")
print(f"  after ambiguity filter . {ambig/mb:,.0f} /MB   (events the local window CANNOT answer)")
print(f"  shrinkage .............. {n/ambig:.1f}x" if ambig else "  COLLAPSED TO ZERO")
print()
print("  Both divergence models called V6_15's number an upper bound. This is how much of it")
print("  survives the filter they named. Whatever this number is, it is the honest one.")
