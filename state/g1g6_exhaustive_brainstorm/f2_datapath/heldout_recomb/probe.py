#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F2 held-out recombination tiebreaker — the $0 fork that decides E1 GPU-go vs H_6163 pivot.

content_word_tiebreaker showed consciousness_anchor carries n=49 POWERED content-word order pairs
(differ_frac 0.959) — but with c_ab up to 451 (heavy repetition) => possibly memorized collocation,
not held-out recombination. This probe forks the decision (synthesis spec, surface analog of the G1
held-out test, still $0 no-model):

  Split the content vocab into two DISJOINT halves A,B by frequency parity. Then:
   - WITHIN-half qualified pairs (both in A or both in B) = seen collocations.
   - CROSS-half qualified pairs (one in A, one in B) = novel-cluster recombination.
  If cross-half order-distinguishing structure is POWERED + NON-DEGENERATE comparable to within-half,
  the order signal generalizes across vocab clusters -> compositional -> E1 GPU-go.
  If cross-half collapses (n<POWER or degenerate) while within-half is powered, OR the whole signal is
  concentrated in very-high-count collocations -> memorized in-distribution collocation (the G1 wall
  regime) -> pivot to H_6163 falsifier-lane.

Vocab construction + gate metric reference-matched to content_word_tiebreaker/probe.py (verbatim).
"""
import json, re, os
from collections import Counter, defaultdict

MIN_OCC = 3; TOP_VOCAB = 400; POWER = 10; FRAC_BAR = 2.0 / 3.0; DROP_TOP = 50
HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = "/Users/mini/dancinlab/anima/archive/state_legacy/anima_phase1a1_color_cosmology_2026_05_12/consciousness_anchor.txt"
LETTER = re.compile(r"[A-Za-z가-힣一-鿿]")

def wordlike(tok):                                  # verbatim from content_word_tiebreaker
    if len(tok) < 2: return False
    if tok.endswith(":"): return False
    letters = LETTER.findall(tok)
    if len(letters) < 2: return False
    if sum(1 for c in tok if not LETTER.match(c)) > len(letters): return False
    if tok.startswith("\\"): return False
    return True

def tokenize(p):
    t = []
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        for line in f: t.extend(line.split())
    return t

def gate_over(toks, vocab, membership_ok):
    """Run the E1 order-gate but only over pairs whose (a,b) pass membership_ok(a,b)."""
    pair_follow = defaultdict(Counter); pair_count = Counter(); n = len(toks)
    for i in range(n - 1):
        a, b = toks[i], toks[i + 1]
        if a in vocab and b in vocab and a != b and membership_ok(a, b):
            pair_count[(a, b)] += 1
            if i + 2 < n: pair_follow[(a, b)][toks[i + 2]] += 1
    seen = set(); n_qual = 0; n_differ = 0; counts = []
    for (a, b) in list(pair_count.keys()):
        key = tuple(sorted((a, b)))
        if key in seen: continue
        c_ab = pair_count[(a, b)]; c_ba = pair_count[(b, a)]
        if c_ab >= MIN_OCC and c_ba >= MIN_OCC:
            seen.add(key); n_qual += 1; counts.append(c_ab + c_ba)
            tf_ab = pair_follow[(a, b)].most_common(1); tf_ba = pair_follow[(b, a)].most_common(1)
            f_ab = tf_ab[0][0] if tf_ab else None; f_ba = tf_ba[0][0] if tf_ba else None
            if f_ab != f_ba: n_differ += 1
    frac = (n_differ / n_qual) if n_qual else 0.0
    v = ("NON-DEGENERATE-POWERED" if (n_qual >= POWER and frac >= FRAC_BAR)
         else "DEGENERATE-POWERED" if n_qual >= POWER else "INCONCLUSIVE-SPARSE")
    counts.sort()
    med = counts[len(counts) // 2] if counts else 0
    return {"n_qualified": n_qual, "n_differ": n_differ, "differ_frac": round(frac, 4),
            "verdict": v, "count_min": counts[0] if counts else 0, "count_median": med,
            "count_max": counts[-1] if counts else 0}

MAXCOUNT_RARE = 8          # total (c_ab+c_ba) <= this = rare/non-memorized combination (near MIN_OCC floor)

def gate_heldout(train_toks, test_toks, vocab):
    """TRUE held-out test: pairs QUALIFIED in the held-out TEST that were NEVER adjacent (either
    order) in TRAIN — novel combinations whose components were seen individually in train. Reports
    whether these novel pairs still carry order-distinguishing follower asymmetry."""
    tr_adj = set()
    for i in range(len(train_toks) - 1):
        a, b = train_toks[i], train_toks[i + 1]
        if a in vocab and b in vocab and a != b:
            tr_adj.add((a, b))
    tr_words = set(train_toks)
    # in TEST, only pairs whose components were BOTH seen in train (seen individually) but the ordered
    # combination was NEVER adjacent in train (novel recombination)
    novel_ok = lambda a, b: (a in tr_words and b in tr_words
                             and (a, b) not in tr_adj and (b, a) not in tr_adj)
    return gate_over(test_toks, vocab, novel_ok)

def main():
    toks = tokenize(CORPUS); freq = Counter(toks)
    ranked = [w for w, _ in freq.most_common()]
    stop = set(ranked[:DROP_TOP])
    content_ranked = [w for w in ranked if w not in stop and wordlike(w)][:TOP_VOCAB]
    vocab = set(content_ranked)

    full = gate_over(toks, vocab, lambda a, b: True)              # reproduces content_word n=49

    # ARM 1 — rare-combination restriction: strip high-repetition collocations, keep only pairs with
    # total count <= MAXCOUNT_RARE. If order structure survives on RARE (non-memorized) combos it is
    # more compositional; if it collapses, the n=49 signal was memorized collocation.
    def gate_rare(toks, vocab):
        pf = defaultdict(Counter); pc = Counter(); n = len(toks)
        for i in range(n - 1):
            a, b = toks[i], toks[i + 1]
            if a in vocab and b in vocab and a != b:
                pc[(a, b)] += 1
                if i + 2 < n: pf[(a, b)][toks[i + 2]] += 1
        seen = set(); nq = nd = 0
        for (a, b) in list(pc.keys()):
            key = tuple(sorted((a, b)))
            if key in seen: continue
            c_ab, c_ba = pc[(a, b)], pc[(b, a)]
            if c_ab >= MIN_OCC and c_ba >= MIN_OCC and (c_ab + c_ba) <= MAXCOUNT_RARE:
                seen.add(key); nq += 1
                f1 = pf[(a, b)].most_common(1); f2 = pf[(b, a)].most_common(1)
                if (f1[0][0] if f1 else None) != (f2[0][0] if f2 else None): nd += 1
        frac = (nd / nq) if nq else 0.0
        v = ("NON-DEGENERATE-POWERED" if (nq >= POWER and frac >= FRAC_BAR)
             else "DEGENERATE-POWERED" if nq >= POWER else "INCONCLUSIVE-SPARSE")
        return {"n_qualified": nq, "n_differ": nd, "differ_frac": round(frac, 4), "verdict": v}
    rare = gate_rare(toks, vocab)

    # ARM 2 — true held-out: 80/20 text split, novel pairs never adjacent in train
    cut = int(len(toks) * 0.8)
    heldout = gate_heldout(toks[:cut], toks[cut:], vocab)

    rare_ok = rare["verdict"] == "NON-DEGENERATE-POWERED"
    held_ok = heldout["verdict"] == "NON-DEGENERATE-POWERED"
    if rare_ok and held_ok:
        verdict = "COMPOSITIONAL-GENERALIZES"
        decision = ("order structure survives BOTH the rare-combination restriction (non-memorized) AND "
                    "the true held-out novel-pair test -> the anchor order signal generalizes beyond "
                    "memorized collocation -> F2 real lever -> E1 GPU-go on the anchor content-word recipe "
                    "(frozen-first, real G1 metric = held-out recomb decode on pool).")
    elif not rare_ok and not held_ok:
        verdict = "COLLOCATION-ONLY"
        decision = ("order structure COLLAPSES on both rare combinations and true held-out novel pairs "
                    "while full-collocation is powered -> the n=49 signal is memorized in-distribution "
                    "collocation, NOT held-out recombination = the G1 wall regime (h1835 in-context "
                    "mastery, held-out transfer 0). F2 cannot escape the wall via existing data -> pivot "
                    "to H_6163 engine-native falsifier-lane build (unlocks H_9202 NT-falsifier).")
    else:
        verdict = "MIXED-DIRECTIONAL"
        decision = ("rare-arm and held-out-arm disagree (rare_powered=%s held_powered=%s) -> partial "
                    "generalization; the $0 corpus-stat cannot cleanly fork. Real decision needs the "
                    "engine-native G1 held-out metric (model) = the E1 GPU-go itself, so treat as "
                    "DIRECTIONAL and gate E1 on owner GPU-go with the scope caveat." % (rare_ok, held_ok))

    out = {"probe": "F2 held-out recombination tiebreaker (corrected: rare + true-heldout arms)",
           "corpus": "consciousness_anchor", "n_tokens": len(toks), "content_vocab": TOP_VOCAB,
           "note": ("prior cross-half-by-frequency-parity arm was INVALID (those pairs still co-occurred "
                    ">=3x = seen collocations, not held-out); replaced by rare-count restriction + true "
                    "80/20 train/test novel-pair test."),
           "full_content": full, "rare_combo_restriction": rare, "true_heldout_novel": heldout,
           "verdict": verdict, "decision": decision}
    json.dump(out, open(os.path.join(HERE, "RESULT.json"), "w"), ensure_ascii=False, indent=1)

    print(f"tokens={len(toks)} content_vocab={TOP_VOCAB}")
    print(f"  FULL content       : n={full['n_qualified']:3d} frac={full['differ_frac']} {full['verdict']} "
          f"(count med={full['count_median']} max={full['count_max']})")
    print(f"  RARE (count<={MAXCOUNT_RARE}) : n={rare['n_qualified']:3d} frac={rare['differ_frac']} {rare['verdict']}")
    print(f"  TRUE HELD-OUT novel: n={heldout['n_qualified']:3d} frac={heldout['differ_frac']} {heldout['verdict']}")
    print(f"  >>> VERDICT: {verdict}")
    print(f"      {decision}")

if __name__ == "__main__":
    main()
