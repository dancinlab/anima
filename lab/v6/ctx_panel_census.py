"""V6_18 -- can a NATURAL transport panel be built on this corpus at all?  ($0 census)

The V6_17 reconcile put this first, ahead of any lane work, because two things can kill the
panel before a single GPU-second is spent and both are corpus facts:

  HEADROOM.  Sol refuses a single-name repetition DV: with one name in context, "copy the only
             name" wins and the panel measures copying.  So a site needs SEVERAL candidate
             names, and the copy-only census -- nearest, most-recent, most-frequent,
             exact-string, bag-of-mentioned -- must NOT already solve it.  If the best trivial
             baseline is near ceiling, there is nothing for a lane to earn.

  POWER.     Sol's requirement: 400-600 INDEPENDENT documents, because 212 items are powered
             only for roughly a 13-point effect.  Sites clustered in a few documents do not
             count as independent.

This census may only KILL (screen-is-a-filter-not-a-performance-predictor).  A pass authorizes
building the panel; it establishes nothing about any faculty.

ON-STANDARD (p9): natural corpus, unchanged, eval-side harvest only -- the training corpus is
never selected or reweighted (that is the H_9128 density kill-list, and V6_17 flags the
resemblance deliberately).
"""
import re
from collections import Counter

from corpus_path import natural_corpus

PATH = natural_corpus()
RF   = 35
ENT  = re.compile(rb"\b([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,}){0,2})\b")

lines = [l for l in open(PATH, "rb").read().split(b"\n") if l.strip()]
mb = sum(len(l) for l in lines) / 1e6
print(f"natural corpus: {len(lines):,} lines · {mb:.2f} MB   receptive field {RF} B\n")

# ---- harvest transport sites that survive the copy-only objection --------------------
# site = an entity reintroduced at gap > RF, with >= 2 DISTINCT candidate entities already
#        mentioned before the target, so "copy the only name" is unavailable by construction.
sites = []          # (doc_index, gold, candidates_in_order_of_mention, mention_counts)
for di, l in enumerate(lines):
    ms = [(m.start(), m.group(1)) for m in ENT.finditer(l)]
    if len(ms) < 3:
        continue
    first = {}
    for k, (p, e) in enumerate(ms):
        key = e.lower()
        if key in first:
            gap = p - first[key][0]
            prior = [x.lower() for _, x in ms[:k]]
            cands = list(dict.fromkeys(prior))
            if gap > RF and len(cands) >= 2:
                sites.append((di, key, cands, Counter(prior), p))
        else:
            first[key] = (p, e)

docs = len(set(d for d, *_ in sites))
print("=" * 76)
print("HARVEST")
print("=" * 76)
print(f"  transport sites with >=2 candidates : {len(sites):,}")
print(f"  independent documents               : {docs:,}")
print(f"  mean candidates per site            : {sum(len(c) for _,_,c,_,_ in sites)/len(sites):.2f}" if sites else "")
if not sites:
    raise SystemExit("no sites -- panel not constructible")

# ---- realized chance, per Sol: p0 = (1/N) sum G_i/K_i --------------------------------
p0 = sum(1.0 / len(c) for _, _, c, _, _ in sites) / len(sites)
print(f"  realized chance p0 = (1/N)·Σ 1/K_i  : {p0:.4f}   (NOT 0.5)")

# ---- the copy-only census: trivial baselines that must NOT already win ----------------
def score(fn):
    return sum(1 for _, g, c, cnt, _ in sites if fn(c, cnt) == g) / len(sites)

BASE = {
  "most-recent mention"   : lambda c, n: c[-1],
  "first mention"         : lambda c, n: c[0],
  "most-frequent mention" : lambda c, n: n.most_common(1)[0][0],
  "longest name"          : lambda c, n: max(c, key=len),
  "shortest name"         : lambda c, n: min(c, key=len),
}
print()
print("=" * 76)
print("COPY-ONLY CENSUS — trivial baselines (must leave headroom)")
print("=" * 76)
print("%-26s %9s %10s" % ("baseline", "acc", "vs chance"))
print("-" * 76)
best = 0.0
for name, fn in BASE.items():
    a = score(fn)
    best = max(best, a)
    print("%-26s %9.4f %+9.4f" % (name, a, a - p0))
print("-" * 76)
print(f"  realized chance            {p0:9.4f}")
print(f"  best trivial baseline      {best:9.4f}      headroom to ceiling = {1-best:.4f}")

# ---- power, per Sol -------------------------------------------------------------------
print()
print("=" * 76)
print("VERDICT — may only KILL")
print("=" * 76)
ok_power = docs >= 400
ok_head  = best <= 0.80
print(f"  power  : {docs:,} independent documents  {'PASS' if ok_power else 'FAIL'}  (Sol: >=400, ~600 safer)")
print(f"  headroom: best trivial {best:.4f}         {'PASS' if ok_head else 'FAIL'}  (a lane must have something to earn)")
print()
if ok_power and ok_head:
    print("  ✅ PANEL IS CONSTRUCTIBLE on natural text. This authorizes building it.")
    print("     It establishes NOTHING about any faculty -- the screen may only kill.")
else:
    print("  🔴 KILL at this corpus. Named reason above; not a faculty verdict.")
