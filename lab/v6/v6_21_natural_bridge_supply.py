"""V6_21 Stage-0 — $0 feasibility gate for the natural-bridge composition eval.

Before any GPU spend, answer Fable's pre-mortem on the corpus we actually have (4.6MB
natural EN prose): can a disjoint held-out slice POSE the 2-hop composition question at
n >= MDE per stratum AFTER degree-matching? If degree-matching kills the supply, natural
text at this scale cannot pose the question cleanly and no training ladder is warranted --
that is itself a result (redirect, do not spend GPU).

Strata (held-out pair (A,C), both entities also seen individually in training):
  SEEN      -- (A,C) co-occur in the training slice            (positive-control supply)
  BRIDGED   -- (A,C) never co-occur in training, but some B    (composition stratum)
               co-occurs with BOTH in training
  UNBRIDGED -- (A,C) never co-occur, and share no training B   (similarity floor)

Degree-matching (the pre-mortem mitigation): bridged pairs live in denser neighborhoods, so
BRIDGED could beat UNBRIDGED by topical proximity alone. We coarse-bin each pair by a
density signature (degree buckets of A and C + frequency buckets), then within each bin the
matched supply is min(BRIDGED, UNBRIDGED). The summed matched supply is the honest n the
GPU eval could actually field with the confound removed.

ON-STANDARD: measures the natural corpus. DIRECTIONAL feasibility only -- no faculty claim.
"""
import re, sys, collections, itertools

from corpus_path import natural_corpus

MDE = 300  # preregistered floor: n>=300/stratum -> ~0.55 vs 0.50 detectable at alpha=.05
HELDOUT_FRAC = 0.20  # last 20% of the corpus, disjoint from training by byte offset

ENT = re.compile(r"\b[A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})*\b")
STOP = {"The","This","That","These","Those","There","When","While","After","Before",
        "However","Although","Because","During","Some","Many","Most","Their","They",
        "It","In","On","At","For","From","With","And","But","New","List"}


def sentences(txt):
    for s in re.split(r"(?<=[.!?])\s+", txt):
        s = s.strip()
        if 20 < len(s) < 600:
            yield s


def entity_set(s):
    return {x for x in ENT.findall(s) if x.split()[0] not in STOP and len(x) > 3}


def build(txt):
    """Return (entity_freq, cooccur_pairs set, adjacency dict) for a slice."""
    freq = collections.Counter()
    pairs = set()
    adj = collections.defaultdict(set)
    for s in sentences(txt):
        e = entity_set(s)
        for x in e:
            freq[x] += 1
        for a, b in itertools.combinations(sorted(e), 2):
            pairs.add((a, b))
            adj[a].add(b)
            adj[b].add(a)
    return freq, pairs, adj


def deg_bucket(d):
    if d <= 1: return 0
    if d <= 3: return 1
    if d <= 7: return 2
    if d <= 15: return 3
    return 4


def freq_bucket(f):
    if f <= 1: return 0
    if f <= 2: return 1
    if f <= 5: return 2
    if f <= 12: return 3
    return 4


def signature(a, c, adj_tr, freq_tr):
    da, dc = len(adj_tr.get(a, ())), len(adj_tr.get(c, ()))
    fa, fc = freq_tr.get(a, 0), freq_tr.get(c, 0)
    # symmetric signature: sorted degree buckets + sorted freq buckets
    dbk = tuple(sorted((deg_bucket(da), deg_bucket(dc))))
    fbk = tuple(sorted((freq_bucket(fa), freq_bucket(fc))))
    return (dbk, fbk)


def main():
    full = open(natural_corpus(), encoding="utf-8", errors="ignore").read()
    n = len(full)
    cut = int(n * (1 - HELDOUT_FRAC))
    train_txt, eval_txt = full[:cut], full[cut:]

    freq_tr, pairs_tr, adj_tr = build(train_txt)
    train_ents = set(freq_tr)

    print("V6_21 Stage-0 -- natural-bridge composition eval FEASIBILITY GATE ($0)")
    print(f"corpus {n/1e6:.2f}MB  |  train {cut/1e6:.2f}MB  eval(held-out) {(n-cut)/1e6:.2f}MB (disjoint)")
    print(f"train: {len(train_ents)} entities, {len(pairs_tr)} co-occurring pairs")
    print(f"MDE floor = {MDE}/stratum\n")

    # mine held-out co-occurring pairs where BOTH entities were seen individually in training
    strata = {"SEEN": [], "BRIDGED": [], "UNBRIDGED": []}
    seen_eval_pairs = set()
    for s in sentences(eval_txt):
        e = entity_set(s)
        for a, c in itertools.combinations(sorted(e), 2):
            if (a, c) in seen_eval_pairs:
                continue
            if a not in train_ents or c not in train_ents:
                continue  # model could not have learned an unseen entity individually
            seen_eval_pairs.add((a, c))
            if (a, c) in pairs_tr:
                strata["SEEN"].append((a, c))
            else:
                shared = adj_tr.get(a, set()) & adj_tr.get(c, set())
                strata["BRIDGED" if shared else "UNBRIDGED"].append((a, c))

    # distractor feasibility: for (A,C) need C' freq-matched to C that never co-occurs with A
    def distractor_ok(a, c):
        fbk_c = freq_bucket(freq_tr.get(c, 0))
        na = adj_tr.get(a, set())
        for cand in train_ents:
            if cand == a or cand == c:
                continue
            if cand in na:
                continue  # co-occurs with A -> not a valid never-co-occur distractor
            if freq_bucket(freq_tr.get(cand, 0)) == fbk_c:
                return True
        return False

    print(f"{'stratum':<10} {'raw':>7} {'distractor-ok':>14}  {'signature bins':>15}")
    print("-" * 52)
    sig = {}
    raw = {}
    for name, items in strata.items():
        dok = sum(1 for a, c in items if distractor_ok(a, c))
        bins = collections.Counter(signature(a, c, adj_tr, freq_tr) for a, c in items)
        sig[name] = bins
        raw[name] = dok  # count only items that can actually form a 2AFC
        print(f"{name:<10} {len(items):>7} {dok:>14}  {len(bins):>15}")

    # degree-matched supply between BRIDGED and UNBRIDGED (symmetric, per signature bin)
    # restrict to distractor-feasible items so the matched n is the ACTUAL fieldable n
    def feasible_bins(name):
        b = collections.Counter()
        for a, c in strata[name]:
            if distractor_ok(a, c):
                b[signature(a, c, adj_tr, freq_tr)] += 1
        return b

    bB, bU = feasible_bins("BRIDGED"), feasible_bins("UNBRIDGED")
    matched = sum(min(bB[k], bU[k]) for k in set(bB) | set(bU))
    seen_ok = raw["SEEN"]

    print()
    print("degree+freq-matched supply (BRIDGED vs UNBRIDGED, per density-signature bin):")
    print(f"  matched fieldable n per stratum = {matched}")
    print(f"  SEEN fieldable n (positive control) = {seen_ok}")

    green = matched >= MDE and seen_ok >= MDE
    print()
    if green:
        print(f"GATE = GREEN -- matched {matched} >= {MDE} and SEEN {seen_ok} >= {MDE}")
        print("  -> eval can pose the composition question with the hub-density confound")
        print("     removed; construct the 2AFC eval + dispatch the training ladder.")
    else:
        why = []
        if matched < MDE: why.append(f"matched {matched} < {MDE}")
        if seen_ok < MDE: why.append(f"SEEN {seen_ok} < {MDE}")
        print(f"GATE = RED -- {', '.join(why)}")
        print("  -> at this corpus scale the natural axis cannot pose the composition")
        print("     question at MDE after degree-matching. A larger EN dump is REQUIRED")
        print("     before any GPU (Fable's 16-130MB ladder); do not spend GPU on 4.6MB.")
        print("  This RED is a RESULT, not a failure (V6_21 pre-mortem branch).")
    return 0 if green else 2


if __name__ == "__main__":
    sys.exit(main())
