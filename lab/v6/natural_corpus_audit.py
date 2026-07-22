"""Is there anything in NATURAL text that could teach composition? $0, on-standard.

The drill audit (H_9902) measured the SYNTHETIC corpus and found 51% of it was six cells
repeated. Under hardened p9 that number is off-standard for any faculty claim -- but the
same question asked of the NATURAL corpus is on-standard, because the natural corpus is
the standard.

What would compositional supervision look like in ordinary prose? At minimum, two entities
have to MEET: appear in one sentence, in a stated relation. If almost every sentence
carries one entity, the corpus is a pile of single facts and there is nothing to compose
from, at any model size.

Measured here, on 4.8MB of wiki-style prose:
  - entities per sentence (the meeting rate)
  - how many DISTINCT entity PAIRS ever meet
  - how many pairs meet MORE THAN ONCE (a pair seen once cannot be generalised from)
  - the 2-hop opportunity: pairs (A,C) that never meet, but where some B meets both
"""
import re, sys, collections, itertools

PATH = "/Users/mini/anima-weights/study303_long_transcript/cpt_mix.txt"
ENT = re.compile(r"\b[A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})*\b")
STOP = {"The","This","That","These","Those","There","When","While","After","Before",
        "However","Although","Because","During","Some","Many","Most","Their","They",
        "It","In","On","At","For","From","With","And","But","New","List"}

def sentences(txt):
    for s in re.split(r"(?<=[.!?])\s+", txt):
        s = s.strip()
        if 20 < len(s) < 600:
            yield s

def main():
    txt = open(PATH, encoding="utf-8", errors="ignore").read()
    per_sent, pair_count = collections.Counter(), collections.Counter()
    ent_count = collections.Counter()
    n = 0
    for s in sentences(txt):
        ents = {e for e in ENT.findall(s) if e.split()[0] not in STOP and len(e) > 3}
        n += 1
        per_sent[min(len(ents), 6)] += 1
        for e in ents:
            ent_count[e] += 1
        for a, b in itertools.combinations(sorted(ents), 2):
            pair_count[(a, b)] += 1
    print("natural corpus audit — %s" % PATH.split("/")[-1])
    print("sentences: %s · distinct entities: %s\n" % (f"{n:,}", f"{len(ent_count):,}"))
    print("entities per sentence (the MEETING rate)")
    for k in range(7):
        c = per_sent.get(k, 0)
        bar = "█" * int(40 * c / max(n, 1))
        print("  %s%-2d %7s  %5.1f%%  %s" % ("≥" if k == 6 else " ", k, f"{c:,}", 100*c/n, bar))
    meet = sum(c for k, c in per_sent.items() if k >= 2)
    print("\n  sentences where >=2 entities MEET: %s (%.1f%%)" % (f"{meet:,}", 100*meet/n))
    print("\ndistinct entity PAIRS that ever meet: %s" % f"{len(pair_count):,}")
    rep = sum(1 for v in pair_count.values() if v > 1)
    rep3 = sum(1 for v in pair_count.values() if v >= 3)
    print("  meet more than once : %s (%.1f%%)" % (f"{rep:,}", 100*rep/max(len(pair_count),1)))
    print("  meet 3+ times       : %s (%.1f%%)" % (f"{rep3:,}", 100*rep3/max(len(pair_count),1)))
    print("\n  -> a pair seen ONCE cannot be generalised from; it can only be memorised.")
    # 2-hop opportunity on the most frequent entities (keeps it cheap)
    top = [e for e, _ in ent_count.most_common(300)]
    idx = {e: i for i, e in enumerate(top)}
    adj = collections.defaultdict(set)
    for (a, b), _ in pair_count.items():
        if a in idx and b in idx:
            adj[a].add(b); adj[b].add(a)
    direct = hop2 = 0
    for a, c in itertools.combinations(top, 2):
        if c in adj[a]:
            direct += 1
        elif adj[a] & adj[c]:
            hop2 += 1
    tot = direct + hop2
    print("\n2-hop opportunity, top-300 entities (%s ordered pairs)" % f"{len(top)*(len(top)-1)//2:,}")
    print("  meet DIRECTLY (stated)      : %s" % f"{direct:,}")
    print("  never meet, but share a hop : %s   <- what composition would have to supply"
          % f"{hop2:,}")
    if tot:
        print("  ratio hop2/(direct+hop2)    : %.3f" % (hop2/tot))
    return 0

sys.exit(main())
