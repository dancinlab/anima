"""Does the singleton rate improve with corpus size? -- the data-scale question, measured.

V6_13 found 82% of entity pairs in 4.8MB of natural prose are seen exactly ONCE, and
argued that is why memorization is closed off. The design divergence asks whether the
whole approach is achievable at megabyte scale or needs the data-scale cell opened.

That is answerable rather than arguable: slice the SAME corpus at increasing sizes and
watch the singleton curve. If repetition grows fast with size, MB scale is simply the
wrong end of a curve that fixes itself. If it is flat, more of the same text will not
supply repetition and the shortfall is structural.

ON-STANDARD: this measures the natural corpus.
"""
import re, sys, collections, itertools

from corpus_path import natural_corpus

PATH = natural_corpus()
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
    return dict(sent=n, ents=len(ents), pairs=tot,
                once=100*once/tot, rep2=100*(tot-once)/tot, rep3=100*rep3/tot,
                ppe=tot/max(len(ents),1))

def main():
    full = open(PATH, encoding="utf-8", errors="ignore").read()
    print("natural-corpus SCALE ladder — does repetition arrive with size?  (ON-STANDARD)")
    print("same corpus, nested prefixes; entity/pair extraction identical to V6_13\n")
    print("%8s %8s %9s %10s  %8s %8s %8s  %7s" %
          ("MB", "sents", "entities", "pairs", "seen 1x", ">=2x", ">=3x", "pairs/ent"))
    print("-" * 82)
    rows = []
    for frac in (0.0625, 0.125, 0.25, 0.5, 1.0):
        cut = int(len(full) * frac)
        r = audit(full[:cut])
        if not r:
            continue
        rows.append((frac * len(full) / 1e6, r))
        print("%8.2f %8s %9s %10s  %7.1f%% %7.1f%% %7.1f%%  %7.2f" %
              (frac*len(full)/1e6, f"{r['sent']:,}", f"{r['ents']:,}", f"{r['pairs']:,}",
               r["once"], r["rep2"], r["rep3"], r["ppe"]))
    print("-" * 82)
    if len(rows) >= 2:
        (m0, a), (m1, b) = rows[0], rows[-1]
        d_once = b["once"] - a["once"]
        print()
        print("%.2fMB -> %.2fMB  (%.0fx more text)" % (m0, m1, m1/m0))
        print("  singleton rate   %.1f%% -> %.1f%%   (delta %+.1f points)"
              % (a["once"], b["once"], d_once))
        print("  seen 3+ times    %.1f%% -> %.1f%%   (delta %+.1f points)"
              % (a["rep3"], b["rep3"], b["rep3"]-a["rep3"]))
        print()
        if d_once > -3.0:
            print("READING: repetition does NOT arrive with size on this axis. A %.0fx increase"
                  % (m1/m0))
            print("moved the singleton rate by %+.1f points, so scaling THIS KIND of text does" % d_once)
            print("not convert single sightings into repeated ones -- new text brings new")
            print("entities at roughly the rate it brings new mentions of old ones.")
            print()
            print("That reframes the data-scale question. It is not 'we lack repetition because")
            print("the corpus is small'. Natural text of this kind is INTRINSICALLY singleton-")
            print("heavy, and an LLM's advantage at 10^12 tokens cannot be assumed to be")
            print("repetition of the SAME pairs -- that is a separate claim needing its own")
            print("measurement, not an extrapolation of this curve.")
        else:
            print("READING: the singleton rate falls by %.1f points over %.0fx more text, so"
                  % (-d_once, m1/m0))
            print("repetition DOES arrive with scale. Extrapolating the curve gives the size at")
            print("which pairs are seen often enough to generalise from -- measure, do not guess.")
    return 0

sys.exit(main())
