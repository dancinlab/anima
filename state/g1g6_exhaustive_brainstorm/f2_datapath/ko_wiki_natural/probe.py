#!/usr/bin/env python3
"""F2 ko_wiki_natural — E1 order-gate on a LARGE NATURAL Korean-wiki corpus.

Reference-matched to e1_pregate/gate.py (H_9200 E1 $0 pre-GPU degeneracy gate):
  follower[(a,b)] = Counter of token[i+2] for every adjacent (a,b), a!=b, both in vocab.
  A pair (a,b) is QUALIFIED iff both (a,b) and (b,a) have >= MIN_OCC followers.
  differ iff top-follower(a,b) != top-follower(b,a).
  NON-DEGENERATE iff differ_frac >= 2/3 AND powered (n_qualified >= 10).
  Underpowered (n_qualified < 10) => INCONCLUSIVE-SPARSE.

Adaptation for Korean (documented):
  - Tokenization: WHITESPACE (Korean is space-delimited at word/eojeol level; the
    reference [a-z]+ regex would return ZERO Hangul tokens). Natural, non-engineered
    tokenization of the raw corpus. No stemming / particle-stripping (=authoring).
  - Vocab: REBUILT from THIS corpus by frequency, top-400 (matches reference vocab
    size 400). NOT hand-picked -- pure Counter.most_common(400). Pure-punctuation and
    markdown heading marks dropped so vocab is content tokens.
"""
import json, os, re
from collections import Counter, defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = "/Users/mini/dancinlab/anima/archive/data/.corpus_cache/.corpus_cache/ko_wiki.txt"
MIN_OCC = 3
BAR = 2.0 / 3.0
POWER = 10
VOCAB_N = 400

_CONTENT = re.compile(r"[0-9A-Za-z가-힣ᄀ-ᇿ㄰-㆏]")
_PUNCT = set("#=-*_|>`~[](){}.,!?;:\"'")

def tokenize(text):
    out = []
    for w in text.split():
        w = w.strip()
        if not w or set(w) <= _PUNCT:
            continue
        if _CONTENT.search(w):
            out.append(w)
    return out

def main():
    raw = open(CORPUS, encoding="utf-8", errors="ignore").read()
    toks = tokenize(raw)
    print(f"[1/4] corpus tokens (whitespace/eojeol): {len(toks)}")

    freq = Counter(toks)
    vocab = [w for w, _ in freq.most_common(VOCAB_N)]
    vset = set(vocab)
    print(f"[2/4] rebuilt vocab top-{VOCAB_N} from corpus. top5={vocab[:5]} "
          f"min-freq-in-vocab={freq[vocab[-1]]}")

    follower = defaultdict(Counter)
    for i in range(len(toks) - 2):
        a, b = toks[i], toks[i + 1]
        if a != b and a in vset and b in vset:
            follower[(a, b)][toks[i + 2]] += 1

    print(f"[3/4] distinct ordered vocab-adjacent pairs: {len(follower)}")
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
    powered = nq >= POWER
    if not powered:
        verdict = "INCONCLUSIVE-SPARSE"
    elif frac >= BAR:
        verdict = "NON-DEGENERATE-POWERED"
    else:
        verdict = "DEGENERATE-POWERED"

    out = {"cell": "ko_wiki_natural",
           "probe": "F2 E1 order-gate on ko_wiki natural corpus",
           "corpus": CORPUS, "tokenization": "whitespace/eojeol (Korean surface words)",
           "vocab_source": f"rebuilt from corpus, top-{VOCAB_N} by frequency",
           "n_tokens": len(toks), "vocab_size": len(vset),
           "min_occ": MIN_OCC, "bar": BAR, "power_threshold": POWER,
           "n_distinct_ordered_pairs": len(follower),
           "n_qualified_pairs": nq, "n_differ": differ,
           "differ_frac": round(frac, 4), "powered": powered,
           "verdict": verdict, "examples": qualified[:20]}
    json.dump(out, open(os.path.join(_HERE, "RESULT.json"), "w"),
              ensure_ascii=False, indent=1)

    print(f"[4/4] qualified={nq} differ={differ} frac={frac:.3f} "
          f"powered={powered} (bar {BAR:.3f}, power>={POWER})")
    print(f"      VERDICT: {verdict}")
    for e in qualified[:10]:
        print(f"        {e['pair']:30s} ab->{e['top_ab']:12s} ba->{e['top_ba']:12s} "
              f"{'DIFFER' if e['differ'] else 'same'}")

if __name__ == "__main__":
    main()
