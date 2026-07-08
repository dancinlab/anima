#!/usr/bin/env python3
"""KWR_KO_GATE frozen-first derivation (H_9212 ④) — MODEL-INDEPENDENT.

Derives the Korean known-word-ratio gate BEFORE any 303M output is ever scored
(p7 · frozen-first · no tune-to-green). Two model-independent kwr_ko distributions:

  (1) POSITIVE  — held-out real ko sentences from anima-corpus-ko-{general,sns}
                  (HF dancinlab · local mirror). UPPER reference.
  (2) NEGATIVE  — a GARBLE null: byte-shuffled real ko + seed-fixed random valid-
                  hangul strings. LOWER reference.

Gate rule (pre-registered, decided BEFORE running):
  KWR_KO_GATE = midpoint( pos_p5 , neg_p95 )   [5th pct of real, 95th pct of garble]
so real ko clears it and garble fails, with a stated separation margin.

kwr_ko itself is a MODEL-INDEPENDENT grammaticality proxy (josa-suffix density),
NOT lexicality (a_scale_honest_scope) — a different physical quantity from en 0.70.

This is corpus statistics only ($0, light CPU, mini-safe) — NOT an engine decode.
Reuses the ALREADY-LANDED tokenizer core/rho_fan.py::_rho_fan_words_uni for exact
parity with the path (3) will wire.
"""
import os
import sys
import json
import random

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, REPO)
from core.rho_fan import _rho_fan_words_uni, _is_hangul_cp

# -- ko known-word proxy (Fable design section 4 - closed-class, model-independent) --
# codepoint-suffix set: a pure-hangul eojeol ending in one of these (stem >=1 syllable)
# = a josa-bearing eojeol = grammatical ko surface. Longest-first for greedy match.
KO_JOSA_SUFFIX = sorted(
    ["에서", "부터", "까지", "처럼", "보다", "조차", "마저", "이나", "하고", "께서",
     "에게", "한테", "로서", "로써", "라도", "이란", "이라", "으로", "에는", "에도",
     "은", "는", "이", "가", "을", "를", "에", "의", "도", "만", "과", "와", "로", "랑"],
    key=len, reverse=True)
# exact-match function words (non-eojeol connectives / bound nouns)
KO_FUNC = {"그리고", "그러나", "하지만", "그래서", "또한", "그런데", "즉", "따라서",
           "그", "이", "저", "것", "수", "등", "및", "또", "더", "즉시", "때문",
           "위해", "대해", "통해", "관해", "무엇", "누구", "어디", "언제", "어떻게", "왜"}


def _is_pure_hangul(tok):
    """all codepoints of tok are hangul (the 3 rho_axon blocks)."""
    if not tok:
        return False
    for ch in tok:
        if not _is_hangul_cp(ord(ch)):
            return False
    return True


def _hangul_len(tok):
    """count hangul codepoints (each 1 str char here)."""
    return sum(1 for ch in tok if _is_hangul_cp(ord(ch)))


def kwr_ko(text):
    """model-independent ko grammaticality proxy: fraction of eojeol tokens that are
    (a) an exact KO_FUNC word, or (b) a pure-hangul eojeol ending in a josa suffix with
    stem >=1 syllable. 0.0 on empty. Tokenizer = the landed _rho_fan_words_uni (eojeol-run)."""
    wl = _rho_fan_words_uni(text)
    n = len(wl)
    if n == 0:
        return 0.0
    hit = 0
    for w in wl:
        if w in KO_FUNC:
            hit += 1
            continue
        if _is_pure_hangul(w):
            for suf in KO_JOSA_SUFFIX:
                if w.endswith(suf) and _hangul_len(w) - len(suf) >= 1:
                    hit += 1
                    break
    return float(hit) / float(n)


# -- corpus IO (HF local mirror) --
HF_HUB = os.path.expanduser("~/.cache/huggingface/hub")
CORPORA = {
    "ko-general": "datasets--dancinlab--anima-corpus-ko-general/snapshots",
    "ko-sns": "datasets--dancinlab--anima-corpus-ko-sns/snapshots",
}


def _find_corpus_file(rel):
    base = os.path.join(HF_HUB, rel)
    if not os.path.isdir(base):
        return None
    for snap in os.listdir(base):
        d = os.path.join(base, snap)
        for f in os.listdir(d):
            if f.endswith(".txt"):
                return os.path.join(d, f)
    return None


def load_sentences():
    """read both ko cells, split into sentences (min length filter), return list."""
    sents = []
    for cell, rel in CORPORA.items():
        p = _find_corpus_file(rel)
        if p is None:
            raise SystemExit(f"CORPUS-ABSENT: {cell} ({rel}) not on disk - see prereg fetch cmd")
        with open(p, "r", encoding="utf-8", errors="surrogateescape") as fh:
            raw = fh.read()
        for line in raw.split("\n"):
            for seg in line.replace("。", ".").split("."):
                seg = seg.strip()
                if len(seg) < 6:
                    continue
                if any(_is_hangul_cp(ord(c)) for c in seg):
                    sents.append(seg)
    return sents


def _pct(sorted_vals, p):
    if not sorted_vals:
        return 0.0
    k = (len(sorted_vals) - 1) * (p / 100.0)
    lo = int(k)
    hi = min(lo + 1, len(sorted_vals) - 1)
    frac = k - lo
    return sorted_vals[lo] * (1 - frac) + sorted_vals[hi] * frac


def _stats(vals):
    s = sorted(vals)
    n = len(s)
    mean = sum(s) / n if n else 0.0
    return {
        "n": n, "mean": round(mean, 4),
        "p5": round(_pct(s, 5), 4), "p25": round(_pct(s, 25), 4),
        "p50": round(_pct(s, 50), 4), "p75": round(_pct(s, 75), 4),
        "p95": round(_pct(s, 95), 4),
        "min": round(s[0], 4) if n else 0.0, "max": round(s[-1], 4) if n else 0.0,
    }


HANGUL_LO, HANGUL_HI = 0xAC00, 0xD7A3  # 가-힣 syllable block for random-hangul null


def main():
    SEED = 4302  # seed-fixed determinism (bit-det-drop keeps EVAL determinism)
    SAMPLE = 20000
    rng = random.Random(SEED)

    sents = load_sentences()
    rng.shuffle(sents)
    # HELD-OUT: derive the gate on a disjoint half so it never sees the eval half
    holdout = sents[:min(SAMPLE, len(sents) // 2)]

    # (1) POSITIVE - real ko sentences
    pos = [kwr_ko(s) for s in holdout]

    # (2a) NEGATIVE garble - byte-shuffle of the same real sentences (destroys UTF-8 +
    #      eojeol structure; a null with identical byte-content, no grammar)
    neg_shuf = []
    for s in holdout:
        bs = bytearray(s.encode("utf-8", "surrogateescape"))
        rng.shuffle(bs)
        neg_shuf.append(kwr_ko(bytes(bs).decode("utf-8", "surrogateescape")))

    # (2b) NEGATIVE garble - seed-fixed random VALID-hangul strings (worst case: a null
    #      that IS valid hangul but has no grammar; some tail syllables land on josa by chance)
    neg_rand = []
    lens = [len(_rho_fan_words_uni(s)) for s in holdout]
    lens = [x for x in lens if x > 0] or [8]
    for _ in range(len(holdout)):
        ntok = rng.choice(lens)
        toks = []
        for _t in range(ntok):
            sylls = rng.randint(1, 4)
            toks.append("".join(chr(rng.randint(HANGUL_LO, HANGUL_HI)) for _ in range(sylls)))
        neg_rand.append(kwr_ko(" ".join(toks)))

    neg_all = neg_shuf + neg_rand

    pos_st, shuf_st, rand_st, negall_st = (_stats(pos), _stats(neg_shuf),
                                           _stats(neg_rand), _stats(neg_all))

    # -- RULE SELECTION (model-independent · decided from distribution SHAPE, no 303M) --
    # Naive rule midpoint(pos_p5, neg_p95) DEGENERATES to 0.0: the POSITIVE dist has a fat
    # zero-tail (short / josa-free real fragments legitimately score 0 → pos_p5=0), while the
    # GARBLE null is a near point-mass at 0 (neg p95=0, mean~0). A p5-anchored gate would sit
    # at 0 and admit garble. The separation is real and large at the CENTER (real median vs
    # garble upper-ref), so the frozen rule anchors there instead:
    #   KWR_KO_GATE = midpoint( neg_combined_p95 , pos_p50 )
    # garble UPPER reference (p95) vs real CENTRAL tendency (median) — robust to the positive
    # zero-tail, still strictly between the two model-independent distributions.
    naive = round((pos_st["p5"] + negall_st["p95"]) / 2.0, 3)  # degenerate, shown for honesty
    neg_p95 = negall_st["p95"]
    pos_p50 = pos_st["p50"]
    gate = round((neg_p95 + pos_p50) / 2.0, 3)

    def _sep(g):
        rc = sum(1 for v in pos if v >= g) / len(pos)
        gf = sum(1 for v in neg_all if v < g) / len(neg_all)
        return round(rc, 4), round(gf, 4)

    real_clear, garble_fail = _sep(gate)

    out = {
        "seed": SEED, "sample_target": SAMPLE, "n_sentences_total": len(sents),
        "n_holdout": len(holdout),
        "positive_real": pos_st,
        "negative_byteshuffle": shuf_st,
        "negative_randomhangul": rand_st,
        "negative_combined": negall_st,
        "naive_p5_p95_midpoint_DEGENERATE": naive,
        "adopted_rule": "midpoint(neg_combined_p95, pos_p50)",
        "neg_p95": neg_p95, "pos_p50": pos_p50,
        "KWR_KO_GATE": gate,
        "real_clear_frac_at_gate": real_clear,
        "garble_fail_frac_at_gate": garble_fail,
        "en_gate_for_contrast": 0.70,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
