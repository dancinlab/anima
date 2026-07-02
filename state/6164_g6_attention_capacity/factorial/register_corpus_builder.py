#!/usr/bin/env python3
"""register_corpus_builder.py — H_6164 FACTOR REG: falsifiable-claim register corpus.

DESIGN-ONLY SCAFFOLD (pre-registration). torch-free / numpy-free (pure stdlib) so the
frame-guard + freq-gate logic runs in a <30s smoke.

CRUX (Goodhart / frame-guard, a_no_llm_frame_trap): REG-on must teach the co-emission
STRUCTURE — that a single sentence pairs a COMPARATOR/conditional mark with a MEASURABLE/
quantity mark — WITHOUT hand-authoring the test ideas or leaking the h1305 eval concept set.
It is corpus-ATTESTED (mined from a real how-to/scientific-register source), freq-gated,
and held-out from the h1305 CONCEPT set + eval/held-out seeds.

  REG-off = volume-matched slice of the existing 4-cell web-prose corpus (no co-emission
            structure). The ONLY difference vs REG-on is the register structure.
  REG-on  = source sentences that CO-EMIT >=1 comparator-set token AND >=1 measurable-set
            token (the FROZEN detector's own word-sets used as the MINER filter), passed
            through the frame-guard.

The FROZEN word-sets are imported VERBATIM from the h1305 detector (single source of truth);
we never re-author them here (p7).
"""
import os, sys, re, random, collections

HERE = os.path.dirname(os.path.abspath(__file__))
H1449 = os.path.join(os.path.dirname(os.path.dirname(HERE)),
                     "archive", "state", "1449_g6_attention_injection")

# ── FROZEN word-sets (VERBATIM from h1305 _is_falsifiable — the detector we must satisfy) ──
COMPARATOR = {"if", "when", "whenever", "than", "more", "less", "greater", "fewer",
              "higher", "lower", "increases", "decreases", "correlates", "predicts",
              "causes", "depends", "unless", "whereas", "versus", "compared",
              "proportional", "faster", "slower", "stronger", "weaker"}
MEASURABLE = {"measure", "measured", "rate", "number", "count", "amount", "level",
              "degree", "threshold", "ratio", "frequency", "probability", "magnitude",
              "score", "value", "quantity", "percent", "times", "fraction", "distance",
              "duration", "speed", "size", "strength", "density"}

# ── h1305 CONCEPT set + eval/held-out seed tokens (the frame-guard DISJOINT set) ──
# From core/g6_ideation.hexa _g6_concepts() + g6_common.HELDOUT_SEEDS + gauge IDEATION_SEEDS.
CONCEPT_WORDS = {
    "consciousness", "arises", "cells", "cell", "tension", "ripples", "distant", "minds",
    "mind", "memory", "composes", "meaning", "silence", "carries", "information", "engine",
    "dreams", "dream", "alone", "substrate", "emit", "mitosis", "phi", "novelty", "coherence",
    # held-out seed content nouns (a testable claim about minds/silence/memory/regimes/…):
    "testable", "prediction", "hypothesis", "regimes", "experiment",
}


def _words(s):
    return re.findall(r"[0-9a-z]+", s.lower())


def mine_register_sentences(source_lines, min_len=6, max_len=40):
    """Select source sentences that CO-EMIT a comparator AND a measurable mark (STRUCTURE),
    then apply the frame-guard. Returns (kept, rejects_by_reason).

    This is the corpus-attested miner: it does NOT author claims, it SELECTS real sentences
    whose FORM already binds comp∧meas. The subject nouns come from the source, not from us.
    """
    kept, rej = [], collections.Counter()
    for raw in source_lines:
        s = raw.strip()
        wl = _words(s)
        n = len(wl)
        if n < min_len or n > max_len:
            rej["len"] += 1; continue
        wset = set(wl)
        has_comp = bool(wset & COMPARATOR)
        has_meas = bool(wset & MEASURABLE)
        if not (has_comp and has_meas):            # STRUCTURE gate: co-emission required
            rej["no_co_emit"] += 1; continue
        if wset & CONCEPT_WORDS:                    # frame-guard (a): concept-leak
            rej["concept_leak"] += 1; continue
        if s.rstrip().endswith("?"):                # not a question (detector c_ii parity)
            rej["question"] += 1; continue
        kept.append(s)
    return kept, dict(rej)


def freq_gate(kept, min_subject_freq=3):
    """Freq-gate (frame-guard b/c): keep only sentences whose NON-mark content nouns are
    corpus-attested (appear >= min_subject_freq across the kept pool) — drops one-off proper
    nouns / rare tokens so the register teaches attested co-emission, not memorizable answers.
    """
    stop = COMPARATOR | MEASURABLE | {
        "the", "a", "an", "of", "and", "to", "in", "is", "it", "that", "this", "with",
        "for", "on", "at", "by", "or", "as", "be", "are", "was", "its", "then", "so"}
    freq = collections.Counter()
    for s in kept:
        for w in set(_words(s)):
            if w not in stop and len(w) >= 3:
                freq[w] += 1
    out = []
    for s in kept:
        content = [w for w in set(_words(s)) if w not in stop and len(w) >= 3]
        if content and all(freq[w] >= min_subject_freq for w in content):
            out.append(s)
    return out, dict(freq.most_common(20))


def build_reg_on(source_lines, n_lines, seed=6164):
    """REG-on corpus builder: mine → freq-gate → sample to n_lines (deterministic).
    Returns the register corpus text + an audit dict (rejects, kept counts).
    """
    kept, rej = mine_register_sentences(source_lines)
    gated, top = freq_gate(kept)
    rng = random.Random(seed)
    if not gated:
        return "", {"kept": 0, "gated": 0, "rejects": rej, "top_content": top}
    sample = [rng.choice(gated) for _ in range(n_lines)]
    audit = {"kept": len(kept), "gated": len(gated), "sampled": len(sample),
             "rejects": rej, "top_content": top}
    return "\n".join(sample) + "\n", audit


def build_reg_off(webprose_lines, n_lines, seed=6164):
    """REG-off: volume-matched sample of the existing 4-cell web-prose (NO co-emission
    structure). Same n_lines so the ONLY difference vs REG-on is the register."""
    rng = random.Random(seed)
    pool = [l.strip() for l in webprose_lines if l.strip()]
    if not pool:
        return "", {"pool": 0}
    return "\n".join(rng.choice(pool) for _ in range(n_lines)) + "\n", {"pool": len(pool)}


# NOTE: the PRODUCTION REG-on source = a real how-to/scientific register slice
# (e.g. a FineWeb "science/procedural" filter or wikiHow dump already in the anima HF
# datasets), NOT the h1435 synthetic templates. h1435 gen_corpus is the SYNTHETIC
# fallback baseline only (it hand-templates comp/meas and hit the H_1449 wall) — the
# corpus-attested miner above is the frame-guarded upgrade this pre-reg tests.


if __name__ == "__main__":
    # <30s smoke: synthetic source mixing (a) real-form co-emission, (b) concept-leak,
    # (c) no-co-emit web-prose, (d) rare-subject. Asserts the frame-guard routes each.
    import json
    src = []
    # (a) 6 attested co-emission sentences over NEUTRAL repeated subjects (should survive):
    for _ in range(6):
        src += ["the reactor pressure increases when the coolant rate is higher than design",
                "a heavier alloy shows a lower failure rate than the lighter sample",
                "the signal decays faster whenever the noise level is greater"]
    # (b) concept-leak (co-emits but mentions 'consciousness'/'memory' → dropped):
    src += ["consciousness increases when the memory count is higher than before"]
    # (c) plain web-prose, no co-emission (dropped by STRUCTURE gate):
    src += ["the river flowed quietly past the old town at dusk"] * 4
    # (d) a question (dropped):
    src += ["is the rate higher than the threshold when pressure increases?"]
    txt, audit = build_reg_on(src, n_lines=20)
    print(json.dumps({"reg_on_lines": txt.count(chr(10)), "audit": audit}, indent=2))
    # hard asserts (smoke gate):
    assert audit["rejects"].get("concept_leak", 0) >= 1, "concept-leak must be caught"
    assert audit["rejects"].get("no_co_emit", 0) >= 4, "web-prose must be dropped"
    assert audit["rejects"].get("question", 0) >= 1, "question must be dropped"
    assert audit["gated"] >= 3, "attested co-emission sentences must survive"
    print("SMOKE_OK")
