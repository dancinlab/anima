#!/usr/bin/env python3
"""C11 corpus-equivalence control (F2 datapath · SWEEP section-2 item 1).

Are consciousness_anchor.txt and corpus.txt the SAME concept-population, or
distinct populations? If distinct, any cross-corpus E1-gate difference could be
a vocab-population artifact rather than a real order-structure difference.

Measures ($0, pure corpus statistics — NEVER loads the model):
  (a) char n-gram overlap (Jaccard + cosine) over 3-gram and 4-gram sets/counts.
  (b) concept-marginal Jensen-Shannon divergence (base-2, bits, [0,1]) over the
      400-word consciousness-anchor vocab: per-corpus unigram distribution of the
      vocab words (whitespace tokenization, matching how vocab tokens look —
      e.g. '사용자:' '있습니다.').

Vocab source = state/trunk_obj_step0/noncommutative_derisk/vocab.json (frozen, by
frequency top-400; NOT hand-picked).
"""
import json, os, math, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "/Users/mini/dancinlab/anima"
VOCAB = os.path.join(REPO, "state", "trunk_obj_step0", "noncommutative_derisk", "vocab.json")
ANCHOR = os.path.join(REPO, "archive", "state_legacy",
                      "anima_phase1a1_color_cosmology_2026_05_12", "consciousness_anchor.txt")
CORPUS = os.path.join(REPO, "archive", "data", "corpus.txt")


def load_vocab():
    v = json.load(open(VOCAB))
    if isinstance(v, dict):
        v = v.get("vocab", list(v.keys()))
    return list(v)


def char_ngrams(text, n):
    return Counter(text[i:i + n] for i in range(len(text) - n + 1))


def jaccard(sa, sb):
    inter = len(sa & sb)
    uni = len(sa | sb)
    return inter / uni if uni else 0.0


def cosine(ca, cb):
    keys = set(ca) | set(cb)
    dot = sum(ca.get(k, 0) * cb.get(k, 0) for k in keys)
    na = math.sqrt(sum(v * v for v in ca.values()))
    nb = math.sqrt(sum(v * v for v in cb.values()))
    return dot / (na * nb) if na and nb else 0.0


def kl(p, q):
    s = 0.0
    for k in p:
        if p[k] > 0 and q.get(k, 0) > 0:
            s += p[k] * math.log2(p[k] / q[k])
    return s


def jsd(p, q):
    # p, q dicts over same key universe, each summing to 1
    m = {k: 0.5 * (p.get(k, 0) + q.get(k, 0)) for k in set(p) | set(q)}
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def vocab_dist(text, vset):
    toks = text.split()
    c = Counter(t for t in toks if t in vset)
    tot = sum(c.values())
    dist = {w: c.get(w, 0) / tot for w in vset} if tot else {w: 0.0 for w in vset}
    return dist, c, tot, len(toks)


def main():
    vocab = load_vocab()
    vset = set(vocab)
    print(f"[load] vocab {len(vset)} words")

    ta = open(ANCHOR, encoding="utf-8", errors="ignore").read()
    tc = open(CORPUS, encoding="utf-8", errors="ignore").read()
    print(f"[load] anchor {len(ta)} chars · corpus {len(tc)} chars")

    result = {"probe": "C11 corpus-equivalence control",
              "anchor_file": ANCHOR, "corpus_file": CORPUS,
              "anchor_chars": len(ta), "corpus_chars": len(tc)}

    # (a) char n-gram overlap
    ngram_stats = {}
    for n in (3, 4):
        ca = char_ngrams(ta, n)
        cc = char_ngrams(tc, n)
        sa, sc = set(ca), set(cc)
        ngram_stats[f"char{n}gram"] = {
            "anchor_distinct": len(sa), "corpus_distinct": len(sc),
            "shared_distinct": len(sa & sc),
            "jaccard": round(jaccard(sa, sc), 4),
            "cosine_counts": round(cosine(ca, cc), 4),
        }
        print(f"[ngram n={n}] jaccard={ngram_stats[f'char{n}gram']['jaccard']} "
              f"cosine={ngram_stats[f'char{n}gram']['cosine_counts']}")
    result["char_ngram_overlap"] = ngram_stats

    # (b) concept-marginal JSD over vocab
    da, ca_cnt, tota, na_tok = vocab_dist(ta, vset)
    dc, cc_cnt, totc, nc_tok = vocab_dist(tc, vset)
    j = jsd(da, dc)
    # per-corpus vocab coverage: fraction of vocab words with >0 occurrences
    cov_a = sum(1 for w in vset if ca_cnt.get(w, 0) > 0) / len(vset)
    cov_c = sum(1 for w in vset if cc_cnt.get(w, 0) > 0) / len(vset)
    print(f"[vocab] anchor {na_tok} toks · {tota} vocab-hits · cov {cov_a:.3f}")
    print(f"[vocab] corpus {nc_tok} toks · {totc} vocab-hits · cov {cov_c:.3f}")
    print(f"[JSD] concept-marginal JSD = {j:.4f} bits")

    result["concept_marginal_jsd"] = {
        "jsd_bits": round(j, 4),
        "anchor_total_tokens": na_tok, "corpus_total_tokens": nc_tok,
        "anchor_vocab_hits": tota, "corpus_vocab_hits": totc,
        "anchor_vocab_coverage": round(cov_a, 4),
        "corpus_vocab_coverage": round(cov_c, 4),
    }

    # top divergent vocab words (largest |p_anchor - p_corpus|)
    div = sorted(vset, key=lambda w: abs(da.get(w, 0) - dc.get(w, 0)), reverse=True)[:15]
    result["top_divergent_words"] = [
        {"w": w, "p_anchor": round(da.get(w, 0), 5), "p_corpus": round(dc.get(w, 0), 5)}
        for w in div]

    # verdict: concept-equivalent iff JSD small (<0.10 bits) AND ngram cosine high (>=0.90)
    jsd_small = j < 0.10
    ngram_high = ngram_stats["char3gram"]["cosine_counts"] >= 0.90
    if jsd_small and ngram_high:
        equiv = "CONCEPT-EQUIVALENT"
        note = ("low JSD + high n-gram cosine -> same concept-population; cross-corpus "
                "gate differences are NOT vocab-population artifacts (real).")
    elif not jsd_small and not ngram_high:
        equiv = "DISTINCT-POPULATIONS"
        note = ("high JSD + low n-gram cosine -> distinct populations; cross-corpus gate "
                "differences may be vocab-population artifacts.")
    else:
        equiv = "PARTIAL"
        note = (f"mixed signal (jsd_small={jsd_small}, ngram_high={ngram_high}); "
                "surface differs but concept-marginals partly aligned.")
    result["equivalence_verdict"] = equiv
    result["note"] = note
    print(f"[VERDICT] {equiv} — {note}")

    json.dump(result, open(os.path.join(HERE, "RESULT.json"), "w"),
              ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
