#!/usr/bin/env python3
"""g1g2_ref_parity.py — emit the H_1129 (G1) + H_1140 (G2) metric outputs on FIXED text
fixtures, so core/g_gates_smoke.hexa can assert byte-parity (same counts) for the .hexa ports.

This is the REFERENCE side of the reference-match (commons reference-match). It reuses the
EXACT metric logic from:
  - state/universe-probes/h1129_midcap_broad_converged_recombination.py  (G1 coverage)
  - state/universe-probes/h1140_novelty_emergence.py                     (G2 content_ngrams + corpus_absent)
extracted VERBATIM (no torch, no model — pure metric functions on given strings).

NOT on the verdict path (this is a parity oracle for the smoke). Run:
  python3 g1g2_ref_parity.py            # prints PARITY lines the .hexa smoke compares against
The .hexa parity case hardcodes these same fixtures + expected counts; if the numbers here
change, the smoke's expected values must change too (that divergence IS the result, c9).
"""
import re

# ── G1: h1129 coverage (CONCEPTS keyword sets VERBATIM) ──────────────────────
CONCEPTS = [
    ("consciousness arises from cells",      {"consciousness", "cells", "mind", "aware"}),
    ("tension ripples between distant minds", {"tension", "ripple", "distant", "between"}),
    ("memory composes into new meaning",      {"memory", "meaning", "compose", "new"}),
    ("silence still carries information",      {"silence", "information", "quiet", "carries"}),
    ("the engine dreams when alone",          {"dream", "engine", "alone", "sleep"}),
]


def words_g1(s):
    # h1129 words(): [0-9A-Za-z가-힣]+ lowercased. The .hexa port uses [0-9A-Za-z] (Latin);
    # the concept keyword sets are all Latin so coverage is byte-identical. Use Latin here
    # to match the .hexa scope exactly (parity is on the SAME tokenizer scope).
    return re.findall(r"[0-9A-Za-z]+", s.lower())


def coverage(text):
    wl = set(words_g1(text))
    return [i for i, (_, kw) in enumerate(CONCEPTS) if wl & kw]


# ── G2: h1140 content_ngrams + corpus_absent (VERBATIM) ──────────────────────
_STOP = set("""the a an of to and in is it that this for on with as are was be by at from or not
but his her they we you i he she them me my your our their its do does did has have had will
would can could should may might must shall when where what which who whom how why all any some
no one two then than into out up down over under more most less about so very just only own same
such each few other been here there now""".split())


def words_g2(s):
    return re.findall(r"[A-Za-z]+", s.lower())


def content_ngrams(text, dict_words):
    toks = words_g2(text)
    grams = set()
    for n in (2, 3):
        for i in range(len(toks) - n + 1):
            g = toks[i:i + n]
            if not all(len(w) >= 3 and w in dict_words for w in g):
                continue
            if all(w in _STOP for w in g):
                continue
            grams.add(" ".join(g))
    return grams


def corpus_absent_tokens(ngram, corpus_tokens):
    # the .hexa port scans the corpus TOKEN STREAM for the consecutive word sequence (equivalent
    # to h1140's punct/newline-tolerant grep over a [A-Za-z]+-tokenized corpus). Match that here.
    ws = ngram.split(" ")
    m = len(ws)
    for i in range(len(corpus_tokens) - m + 1):
        if corpus_tokens[i:i + m] == ws:
            return False
    return True


# ── FIXED FIXTURES (must match the .hexa smoke byte-for-byte) ────────────────
# G1 fixtures: (text, expected coverage count)
G1_FIX = [
    "consciousness in the cells and a distant mind",      # concepts 0 (consciousness,cells,mind) + 1 (distant) = 2
    "the engine dreams of silence and quiet information",  # 3 (silence,information,quiet) + 4 (dream,engine) = 2
    "a plain sentence with nothing special",               # 0
    "memory meaning tension ripple dream sleep aware",      # 0(aware)+1(tension,ripple)+2(memory,meaning)+4(dream,sleep) = 4
]

# G2 fixtures: dict_words (a small fixed set) + texts + expected content-ngram count;
# + a corpus token stream + expected corpus-absent count.
G2_DICT = {"memory", "tension", "ripples", "silence", "engine", "dreams", "distant",
           "minds", "consciousness", "cells", "carries", "information", "quiet", "novel",
           "meaning", "alone", "between", "new", "the", "and"}
G2_FIX = [
    "memory tension silence engine",   # bigrams: memory-tension, tension-silence, silence-engine; trigrams: 2 → 5 grams
    "the and the and",                 # all _STOP (the/and in _STOP? and yes, the yes) → 0
]
G2_CORPUS = "memory tension silence flows here"   # tokens: memory tension silence flows here
# corpus-absent over G2_FIX[0]'s grams: "memory tension" PRESENT, "tension silence" PRESENT,
#   "silence engine" ABSENT; trigrams "memory tension silence" PRESENT, "tension silence engine" ABSENT → absent=2


def main():
    print("# G1 coverage parity")
    for i, t in enumerate(G1_FIX):
        print(f"G1\t{i}\t{len(coverage(t))}")
    print("# G2 content_ngrams parity")
    for i, t in enumerate(G2_FIX):
        print(f"G2NG\t{i}\t{len(content_ngrams(t, G2_DICT))}")
    print("# G2 corpus_absent parity")
    ctoks = words_g2(G2_CORPUS)
    grams = sorted(content_ngrams(G2_FIX[0], G2_DICT))
    absent = sum(1 for g in grams if corpus_absent_tokens(g, ctoks))
    print(f"G2ABS\t0\t{absent}")


if __name__ == "__main__":
    main()
