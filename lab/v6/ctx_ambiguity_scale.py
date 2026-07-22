"""V6_16b -- is the 308x collapse a property of the TEXT, or of the corpus SIZE?

ctx_ambiguity.py applied the filter both divergence models demanded and V6_15's 2,244/MB
became 7/MB.  Before reading that as "natural text does not supply the pressure", two
confounds have to be separated, because the criterion is an EXACT 35-byte string match:

  (i) DUPLICATION.  59.8% of lines are outright repeats.  A duplicated line makes its own
      contexts "repeated but always the same continuation" -- which is not local determinacy,
      it is the same text twice.  Fix: rerun on deduplicated lines.

  (ii) CORPUS SIZE.  "seen once => memorizable => no pressure" is an argument about 4.8MB
      being far below the ~170MB capacity, NOT about the architecture.  A context unique in
      4.8MB is not unique in 500MB.  So pressure density should GROW with corpus size.
      Fix: measure the curve, don't assume the point.

If pressure density rises with size, 7/MB is a statement about THIS corpus, and it converges
from a new direction with the scale answer already measured (43-224MB).  If it is flat, the
text genuinely does not supply the pressure and the G1-ctx lane is dead on natural corpus --
which I would then say plainly.

ON-STANDARD (p9).  DIRECTIONAL.
"""
import re
from collections import Counter, defaultdict

PATH = "/Users/mini/anima-weights/study303_long_transcript/cpt_mix.txt"
RF   = 35
ENT  = re.compile(rb"\b([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,}){0,2})\b")
PRON = re.compile(rb"\b(he|she|it|they|him|her|them|his|hers|its|their|theirs)\b", re.I)

def harvest(lines):
    sites = []
    for l in lines:
        pos = {}
        for m in ENT.finditer(l):
            e = m.group(1).lower()
            if e in pos and m.start() - pos[e] > RF and m.start() >= RF:
                sites.append(bytes(l[m.start()-RF:m.start()]))
            pos[e] = m.start()
        ents = [m.start() for m in ENT.finditer(l)]
        if ents:
            for m in PRON.finditer(l):
                prev = [p for p in ents if p < m.start()]
                if prev and m.start() - max(prev) > RF and m.start() >= RF:
                    sites.append(bytes(l[m.start()-RF:m.start()]))
    return sites

def pressure(lines):
    raw   = b"\n".join(lines)
    mb    = len(raw) / 1e6
    sites = harvest(lines)
    if not sites:
        return mb, 0, 0, 0.0
    want  = set(sites)
    seen  = defaultdict(set); cnt = Counter()
    for i in range(len(raw) - RF):
        c = raw[i:i+RF]
        if c in want:
            cnt[c] += 1; seen[c].add(raw[i+RF])
    amb = sum(1 for c in sites if cnt[c] > 1 and len(seen[c]) > 1)
    return mb, len(sites), amb, amb / mb

allines = [l for l in open(PATH, "rb").read().split(b"\n") if l.strip()]
dedup   = list(dict.fromkeys(allines))
print(f"lines: {len(allines):,} raw -> {len(dedup):,} deduplicated ({100*(1-len(dedup)/len(allines)):.1f}% were repeats)\n")

for label, pool in (("WITH duplicate lines", allines), ("DEDUPLICATED", dedup)):
    print("=" * 78)
    print(label)
    print("=" * 78)
    print("%-10s %9s %12s %12s %12s" % ("corpus", "MB", "beyond-RF", "pressure", "pressure/MB"))
    print("-" * 78)
    n = len(pool)
    for frac in (0.125, 0.25, 0.5, 1.0):
        sub = pool[: int(n * frac)]
        mb, tot, amb, dens = pressure(sub)
        print("%-10s %9.2f %12d %12d %12.1f" % (f"{frac:.0%}", mb, tot, amb, dens))
    print()

print("=" * 78)
print("READ")
print("=" * 78)
print("  RISING pressure/MB  -> 7/MB is a statement about 4.8MB, not about natural text;")
print("                         the missing ingredient is corpus SIZE, converging with the")
print("                         43-224MB scale answer measured from pair repetition.")
print("  FLAT pressure/MB    -> natural text genuinely does not supply the pressure at any")
print("                         size reachable here, and the G1-ctx lane is dead on standard.")
