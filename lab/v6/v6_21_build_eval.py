"""V6_21 Stage-1a -- build the 2AFC eval items from the degree-matched strata ($0).

ON-STANDARD (p9): the probe is the ACTUAL held-out natural sentence, NOT a hand-built
template. For a held-out sentence S in which A and C co-occur, the 2AFC is:
  attested = S            (the real natural sentence, verbatim)
  distract = S with C replaced by a frequency-matched never-co-occurring entity C'
The model "prefers" whichever it finds more likely (lower byte-NLL). Correct = it prefers
the real natural sentence. Both the fact (A,C meet) AND the phrasing (S) are natural;
nothing is hand-fit -- this is the p9-clean version (the earlier hand-built templates were
drill-installed and off-standard).

Strata (see V6_21 card): SEEN (positive control), BRIDGED (composition), UNBRIDGED
(similarity floor). BRIDGED and UNBRIDGED are degree+freq matched per density-signature
bin so a bridged-beats-unbridged gap cannot be hub-density (Fable's pre-mortem).

Deterministic: no RNG. Ordering is by (signature bin, sorted entity names).
"""
import re, sys, json, collections, itertools

from corpus_path import natural_corpus

HELDOUT_FRAC = 0.20
CAP = 500  # items per stratum (>= MDE 300 with margin)

ENT = re.compile(r"\b[A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})*\b")
STOP = {"The","This","That","These","Those","There","When","While","After","Before",
        "However","Although","Because","During","Some","Many","Most","Their","They",
        "It","In","On","At","For","From","With","And","But","New","List"}


_DATE_LIST = re.compile(r"^\s*\d{3,4}\s*[–-]")     # "1944 – ..." births/deaths list rows
_YEAR_ONLY = re.compile(r"\b\d{3,4}\b\s*[–-]\s*[A-Z]")  # embedded date-list fragments

def sentences(txt):
    """Prose-only sentence yield. Rejects list-dump structure (multi-line blocks, date-list
    rows, bullet/heading fragments) so entity co-occurrence means a real in-sentence
    relation, not list adjacency. This is what keeps the probe p9-clean AND meaningful."""
    for line in txt.split("\n"):                    # 1 line = 1 candidate (kills block spans)
        line = line.strip()
        if not line or _DATE_LIST.match(line):
            continue
        for s in re.split(r"(?<=[.!?])\s+", line):
            s = s.strip()
            if not (30 < len(s) < 400):
                continue
            if _YEAR_ONLY.search(s):                # embedded "1984 – Name," list fragment
                continue
            if s.count(",") > 6 or sum(ch.isdigit() for ch in s) > 12:
                continue                            # comma/digit dumps = tables/lists
            if not s.endswith((".", "!", "?")):     # real prose ends in terminal punct
                continue
            yield s


def entity_set(s):
    return {x for x in ENT.findall(s) if x.split()[0] not in STOP and len(x) > 3}


def build(txt):
    freq = collections.Counter(); pairs = set(); adj = collections.defaultdict(set)
    for s in sentences(txt):
        e = entity_set(s)
        for x in e: freq[x] += 1
        for a, b in itertools.combinations(sorted(e), 2):
            pairs.add((a, b)); adj[a].add(b); adj[b].add(a)
    return freq, pairs, adj


def deg_bucket(d):
    return 0 if d<=1 else 1 if d<=3 else 2 if d<=7 else 3 if d<=15 else 4
def freq_bucket(f):
    return 0 if f<=1 else 1 if f<=2 else 2 if f<=5 else 3 if f<=12 else 4
def signature(a, c, adj, freq):
    dbk = tuple(sorted((deg_bucket(len(adj.get(a,()))), deg_bucket(len(adj.get(c,()))))))
    fbk = tuple(sorted((freq_bucket(freq.get(a,0)), freq_bucket(freq.get(c,0)))))
    return (dbk, fbk)


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "v6_21_eval_items.jsonl"
    full = open(natural_corpus(), encoding="utf-8", errors="ignore").read()
    cut = int(len(full) * (1 - HELDOUT_FRAC))
    train_txt, eval_txt = full[:cut], full[cut:]
    freq_tr, pairs_tr, adj_tr = build(train_txt)
    train_ents = set(freq_tr)
    # frequency-bucket index of training entities, for distractor selection
    by_fbk = collections.defaultdict(list)
    for e in sorted(train_ents):
        by_fbk[freq_bucket(freq_tr[e])].append(e)

    # store the FIRST held-out sentence in which each pair co-occurs (the natural probe)
    strata = {"SEEN": {}, "BRIDGED": {}, "UNBRIDGED": {}}
    seen = set()
    for s in sentences(eval_txt):
        es = entity_set(s)
        for a, c in itertools.combinations(sorted(es), 2):
            if (a, c) in seen or a not in train_ents or c not in train_ents:
                continue
            seen.add((a, c))
            if (a, c) in pairs_tr:
                strata["SEEN"][(a, c)] = s
            else:
                shared = adj_tr.get(a, set()) & adj_tr.get(c, set())
                strata["BRIDGED" if shared else "UNBRIDGED"][(a, c)] = s

    def cloze(a, c, s):
        """A never-co-occurring, frequency-matched C' that word-boundary-replaces C in the
        natural sentence s, giving a minimal natural-vs-swapped pair. Returns (c', s')."""
        na = adj_tr.get(a, set())
        pat = re.compile(r"\b" + re.escape(c) + r"\b")
        if not pat.search(s):
            return None
        for cand in by_fbk[freq_bucket(freq_tr.get(c, 0))]:
            if cand == a or cand == c or cand in na:
                continue
            if re.search(r"\b" + re.escape(cand) + r"\b", s):
                continue  # C' already in the sentence -> not a clean swap
            return cand, pat.sub(cand, s, count=1)
        return None

    # precompute cloze feasibility (needs the natural sentence) once per pair
    def feasible(name):
        out = {}
        for (a, c), s in strata[name].items():
            cl = cloze(a, c, s)
            if cl:
                out[(a, c)] = (s, cl[0], cl[1])  # (sentence, c', s')
        return out
    fSEEN, fB, fU = feasible("SEEN"), feasible("BRIDGED"), feasible("UNBRIDGED")

    # degree-match BRIDGED vs UNBRIDGED: keep only density-signature bins present in BOTH
    def bins(feas):
        b = collections.defaultdict(list)
        for (a, c) in feas:
            b[signature(a, c, adj_tr, freq_tr)].append((a, c))
        return b
    bB, bU = bins(fB), bins(fU)
    matchedB, matchedU = [], []
    for k in sorted(set(bB) & set(bU)):
        m = min(len(bB[k]), len(bU[k]))
        matchedB += sorted(bB[k])[:m]
        matchedU += sorted(bU[k])[:m]

    chosen = {"SEEN": (fSEEN, sorted(fSEEN)[:CAP]),
              "BRIDGED": (fB, matchedB[:CAP]),
              "UNBRIDGED": (fU, matchedU[:CAP])}

    n = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for stratum, (feas, keys) in chosen.items():
            for a, c in keys:
                s, cp, sp = feas[(a, c)]
                f.write(json.dumps({"stratum": stratum, "a": a, "c": c, "c_distract": cp,
                                    "attested": [s], "distract": [sp]},
                                   ensure_ascii=False) + "\n")
                n += 1
    print(f"wrote {n} items -> {out_path}  (natural-cloze probes, p9-clean)")
    for k, (_, keys) in chosen.items():
        print(f"  {k:<10} {len(keys)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
