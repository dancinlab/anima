#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F2 cell = small_purpose_density.  $0 corpus-statistic probe (NO model load).

Question: Do the smaller purpose-built corpora (consciousness_self_ref.txt,
self_play_200.txt) carry MORE order-distinguishing relation structure PER TOKEN
than the large generic corpus.txt?  If order-distinguishing structure is real
data for E1, a purpose-built corpus should be DENSER in it.

Metric = E1 order-distinguishing gate (reference-matched to the E1 pre-gate as
described in the F2 task + cluster_C relation-density precedent):
  - tokenize = whitespace split.
  - vocab = top-400 tokens by frequency, REBUILT FROM THE SAME CORPUS (no
    hand-pick, no cross-corpus vocab -> no tune-to-green).
  - ordered adjacent concept pair (a,b): consecutive tokens, a,b both in vocab,
    a != b (exclude self-pairs).
  - top-follower(a,b) = most common token c immediately following the (a,b)
    bigram in the stream.
  - a UNORDERED pair {a,b} is QUALIFIED iff BOTH orders (a,b) and (b,a) occur
    >= MIN_OCC (=3) times.
  - differ_frac = fraction of qualified pairs where top-follower(a,b) !=
    top-follower(b,a).
  - NON-DEGENERATE iff differ_frac >= 2/3 AND n_qualified >= 10 (powered).
    Underpowered (n_qualified < 10) => INCONCLUSIVE-SPARSE.
  - DENSITY = n_qualified / (n_tokens / 1e6)  [qualified pairs per Mtoken].

Honesty: measures REAL corpora only. Underpowered/negative is the result.
"""
import json, os
from collections import Counter, defaultdict

MIN_OCC = 3
POWER = 10
TOP_N = 400
REPO = "/Users/mini/dancinlab/anima"
OUTDIR = f"{REPO}/state/g1g6_exhaustive_brainstorm/f2_datapath/small_purpose_density"

CORPORA = {
    "consciousness_self_ref": f"{REPO}/archive/data/consciousness_self_ref.txt",
    "self_play_200":          f"{REPO}/archive/data/self_play_200.txt",
    "corpus_generic":         f"{REPO}/archive/data/corpus.txt",
}


def tokenize(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read().split()


def build_vocab(tokens, top_n=TOP_N):
    freq = Counter(tokens)
    return set(w for w, _ in freq.most_common(top_n))


def probe(path):
    toks = tokenize(path)
    n_tok = len(toks)
    vocab = build_vocab(toks)

    ordered = Counter()                    # (a,b) -> occurrences of adjacent bigram
    follower = defaultdict(Counter)        # (a,b) -> Counter of token following the bigram
    for i in range(len(toks) - 1):
        a, b = toks[i], toks[i + 1]
        if a in vocab and b in vocab and a != b:
            ordered[(a, b)] += 1
            if i + 2 < len(toks):
                follower[(a, b)][toks[i + 2]] += 1

    # qualified unordered pairs: both directions >= MIN_OCC
    seen = set()
    qualified = []
    for (a, b) in ordered:
        key = frozenset((a, b))
        if key in seen:
            continue
        if ordered[(a, b)] >= MIN_OCC and ordered.get((b, a), 0) >= MIN_OCC:
            seen.add(key)
            qualified.append((a, b))

    n_qual = len(qualified)
    n_differ = 0
    examples = []
    for (a, b) in qualified:
        tf_ab = follower[(a, b)].most_common(1)
        tf_ba = follower[(b, a)].most_common(1)
        f_ab = tf_ab[0][0] if tf_ab else None
        f_ba = tf_ba[0][0] if tf_ba else None
        differ = (f_ab != f_ba)
        if differ:
            n_differ += 1
        if len(examples) < 12:
            examples.append({
                "pair": [a, b],
                "occ_ab": ordered[(a, b)], "occ_ba": ordered.get((b, a), 0),
                "top_follower_ab": f_ab, "top_follower_ba": f_ba,
                "differ": differ,
            })

    differ_frac = (n_differ / n_qual) if n_qual else 0.0
    density = n_qual / (n_tok / 1e6) if n_tok else 0.0

    powered = n_qual >= POWER
    if not powered:
        verdict = "INCONCLUSIVE-SPARSE"
    elif differ_frac >= 2.0 / 3.0:
        verdict = "NON-DEGENERATE-POWERED"
    else:
        verdict = "DEGENERATE-POWERED"

    return {
        "n_tokens": n_tok,
        "vocab_size": len(vocab),
        "n_ordered_adjacent_vocab_bigram_types": len(ordered),
        "n_qualified": n_qual,
        "n_differ": n_differ,
        "differ_frac": round(differ_frac, 4),
        "relation_density_qual_per_Mtoken": round(density, 4),
        "powered_n_ge_10": powered,
        "verdict": verdict,
        "examples": examples,
    }


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    out = {
        "cell": "small_purpose_density",
        "metric": "E1 order-distinguishing gate; MIN_OCC=3, power>=10, top-400 per-corpus vocab, whitespace tokens",
        "density_definition": "n_qualified / (n_tokens/1e6)  [order-distinguishing qualified pairs per Mtoken]",
        "results": {},
    }
    for name, path in CORPORA.items():
        out["results"][name] = probe(path)

    # cross-corpus density comparison
    dens = {k: v["relation_density_qual_per_Mtoken"] for k, v in out["results"].items()}
    out["density_comparison"] = dens
    out["purpose_built_denser_than_generic"] = (
        max(dens.get("consciousness_self_ref", 0), dens.get("self_play_200", 0))
        > dens.get("corpus_generic", 0)
    )

    print(json.dumps(out, indent=2, ensure_ascii=False))
    with open(f"{OUTDIR}/RESULT.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\n[saved] {OUTDIR}/RESULT.json", flush=True)


if __name__ == "__main__":
    main()
