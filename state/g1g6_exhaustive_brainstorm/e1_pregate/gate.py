#!/usr/bin/env python3
"""H_9200 E1 — $0 pre-GPU degeneracy gate (E1_design.md §"$0 pre-GPU gate", lines 49-54).

Before spending owned-pool GPU on the E1 CE-deleted forward-slot arm, verify the
target is even non-trivially satisfiable: at "composition slots" (concept a,b seen
adjacent), does the ORDER-SWAPPED follower differ from the STANDARD follower?

E1 mechanism (E1_design.md lines 25-28):
  standard target at slot after (a,b) = the token that follows (a,b) in corpus.
  swap     target                     = the token that WOULD follow (b,a) in corpus.
If the corpus rarely distinguishes order at the slot, the swap target collapses onto
the standard target -> E1's non-commutative CE target is DEGENERATE -> GPU spend wasted.

This is a MODEL-FREE corpus pass ($0 mini, no 303M decode) — pure adjacency statistics.

PREREG bar (frozen before run):
  NON-DEGENERATE (GPU-go OK) <=> among qualified ordered pairs (both (a,b) and (b,a)
      occur >= MIN_OCC times), the top-follower of (a,b) DIFFERS from the top-follower
      of (b,a) on >= 2/3 of pairs.  (== "swap target != standard target at >=2/3 slots")
  DEGENERATE (E1 wasteful, target-side exhausted) <=> differ-fraction < 2/3.
"""
import json, os, re
from collections import Counter, defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
VOCAB = os.path.join(_REPO, "state", "trunk_obj_step0", "noncommutative_derisk", "vocab.json")
CORPUS = os.path.join(_REPO, "archive", "state_legacy",
                      "anima_phase1a1_color_cosmology_2026_05_12", "consciousness_anchor.txt")
MIN_OCC = 3          # each ordered pair needs >= this many followers to escape noise
BAR = 2.0 / 3.0      # frozen differ-fraction threshold

def main():
    vocab = json.load(open(VOCAB))
    if isinstance(vocab, dict):
        vocab = vocab.get("vocab", list(vocab.keys()))
    vset = set(vocab)
    print(f"[1/3] vocab {len(vset)} words · corpus pass ...")

    # tokenize corpus to lowercase word tokens (census.py-compatible tokenization)
    toks = re.findall(r"[a-z]+", open(CORPUS, encoding="utf-8", errors="ignore").read().lower())
    print(f"      {len(toks)} tokens")

    # follower[(a,b)] = Counter of token[i+2] for every adjacent a,b in vocab
    follower = defaultdict(Counter)
    for i in range(len(toks) - 2):
        a, b = toks[i], toks[i + 1]
        if a != b and a in vset and b in vset:   # self-pairs (a==b) are trivially non-informative
            follower[(a, b)][toks[i + 2]] += 1

    print("[2/3] compare ordered pairs (a,b) vs (b,a) ...")
    qualified, differ = [], 0
    seen = set()
    for (a, b), fab in follower.items():
        if (a, b) in seen or (b, a) in seen:
            continue
        fba = follower.get((b, a))
        if fba is None:
            continue
        nab, nba = sum(fab.values()), sum(fba.values())
        if nab < MIN_OCC or nba < MIN_OCC:
            continue
        seen.add((a, b)); seen.add((b, a))
        top_ab = fab.most_common(1)[0][0]
        top_ba = fba.most_common(1)[0][0]
        d = top_ab != top_ba
        differ += int(d)
        qualified.append({"pair": f"{a}|{b}", "n_ab": nab, "n_ba": nba,
                          "top_ab": top_ab, "top_ba": top_ba, "differ": d})

    nq = len(qualified)
    frac = differ / nq if nq else 0.0
    verdict = "NON-DEGENERATE" if frac >= BAR else "DEGENERATE"
    decision = ("swap target != standard target at >=2/3 slots -> E1 target satisfiable "
                "-> clean owner GPU-go" if frac >= BAR else
                "swap target collapses onto standard at >2/3 slots -> E1 target degenerate "
                "-> target-side exhausted, no GPU spend")

    out = {"probe": "H_9200 E1 $0 pre-GPU degeneracy gate", "min_occ": MIN_OCC, "bar": BAR,
           "n_qualified_pairs": nq, "n_differ": differ, "differ_frac": round(frac, 4),
           "verdict": verdict, "decision": decision,
           "examples": qualified[:12]}
    json.dump(out, open(os.path.join(_HERE, "RESULT.json"), "w"), ensure_ascii=False, indent=1)

    print(f"[3/3] qualified pairs={nq} · differ={differ} · frac={frac:.3f} (bar {BAR:.3f})")
    print(f"      VERDICT: {verdict}")
    print(f"      {decision}")
    for e in qualified[:8]:
        print(f"        {e['pair']:28s} ab->{e['top_ab']:12s} ba->{e['top_ba']:12s} "
              f"{'DIFFER' if e['differ'] else 'same'}")

if __name__ == "__main__":
    main()
