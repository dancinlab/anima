# F2 data-path investigation — synthesis

**Verdict: MIXED** (real powered content-word path in ONE synthetic corpus; diverse natural corpora content-starved; the powered path is collocational / in-distribution — the exact regime the G1 wall lives in).

Date: 2026-07-05 · $0 pure-corpus-statistics only · no model/.clm loaded.

## F2 question
Does ANY real corpus / gate-formulation carry DENSE (powered, n>=10) order-distinguishing
**compositional** structure — a real data path for E1 — or is order-distinguishing structure
fundamentally absent from all available natural corpora?

## What the 7 probes established (grounded)
| cell | vocab | n_qual | differ_frac | verdict | honest read |
|---|---|---|---|---|---|
| c11_corpus_equiv | — (control) | — | — | NA | anchor vs corpus.txt are DISTINCT populations (JSD 0.561, char3g cos 0.19, 28.5% coverage): E1 cross-corpus n=0 was a **vocab-population confound**, not order-scarcity. |
| self_vocab_corpustxt | corpus.txt top-400 freq | 41 | 0.951 | POWERED | but stopword/speaker-label driven (a/b/the/is) -> syntactic, not concept. |
| ko_wiki_natural | ko_wiki top-400 freq | 43 | 0.954 | POWERED | ~36/43 are \displaystyle LaTeX fragments; Hangul-only arm -> **n=7 underpowered**. |
| window_relax | anchor top-400 freq | 7932 (k3) | 0.957 | POWERED | E1-exact concept arm k1 n=2, k3 n=7 (only k5 n=10); widening/vocab is the lift, templated Q/A. |
| relation_typed | corpus.txt top-400 freq | TYPED 1 / RAW 16 | 1.0 | SPARSE / trivial | typed concept-CONN-concept ~absent; RAW is function-word-glued syntax. |
| small_purpose_density | per-corpus top-400 | 0 / 0 / 9 | 1.0 | SPARSE | smaller purpose corpora carry LESS structure per token, all underpowered. |
| crosscorpus_yield | per-corpus top-400 freq | anchor 195, ko_wiki 42, corpus 9 | 0.97 | POWERED (2/5) | dense — but qualified pairs dominated by markup/particle tokens (==, (, 수 있을, 사용자:). |

**Convergent read of the 7:** the E1 gate is POWERABLE (prior n=0 was a vocab-mismatch/population
artifact — decisively refuted). BUT every powered cell was powered on the **frequency-vocab layer**,
dominated by function words / markup / speaker-labels = **syntactic/template order, not concept
binding**. Every arm restricted to genuine concepts collapsed to underpowered (ko_wiki Hangul n=7 ·
window E1-exact k3 n=7 · relation TYPED n=1 · small-purpose n=0). Central F2 question left open: is the
powered signal a function-word-vocab artifact, or does real CONTENT-level order structure survive?

## The decisive tiebreaker I ran this session: `content_word_tiebreaker`
Strongest **non-Goodhart** formulation: rebuild vocab from each corpus by frequency, drop the top-50
most-frequent tokens (a **frequency-derived** stoplist — function words, NOT hand-picked) + require a
wordlike shape (>=2 letter/Hangul chars, no markup, no \LaTeX, no `사용자:` speaker labels), then top-400
of the remainder. Same frozen E1 gate (MIN_OCC=3, POWER=10, FRAC_BAR=2/3), reference-matched to
`crosscorpus_yield/probe.py`. Verbatim result:

```
consciousness_anchor   tok=2,326,605 | FREQ n=195 frac=0.974 NON-DEG-POWERED | CONTENT n= 49 frac=0.959 NON-DEG-POWERED
corpus                 tok=  629,994 | FREQ n=  9 frac=1.000 SPARSE          | CONTENT n=  0 frac=0.000 SPARSE
ko_wiki                tok=  220,933 | FREQ n= 42 frac=0.929 NON-DEG-POWERED | CONTENT n=  2 frac=1.000 SPARSE
CONCLUSION: content_word_powered_corpora=[consciousness_anchor]  verdict=CONTENT-PATH-FOUND
```

**consciousness_anchor SURVIVES the content-word filter: n=49 (>>10), differ_frac 0.959.** Surviving
pairs are genuine Korean content collocations, not function words or markup: 미치는/영향을 (c 142/154),
서비스를/제공하는 (53/3), 방법을/사용하는 (15/9), AI/기반 (80/4), 관련/제품 (3/6), 미칠/영향을 (451/3).
So content-level order-distinguishing structure is **real and powered** — the "only function words"
deflation is refuted for the anchor. **But the two diverse natural corpora COLLAPSE on content words:
corpus.txt n=0, ko_wiki n=2.**

## Why MIXED (not REAL-PATH-FOUND, not ALL-DATA-STARVED)
- **Not ALL-DATA-STARVED:** literally false — the anchor content-word arm is NON-DEGENERATE-POWERED
  (n=49) on the hardest non-Goodhart vocab. Content-level order structure is NOT universally absent.
- **Not a clean REAL-PATH-FOUND (GPU-go):** the signal is **corpus-specific to one synthetic,
  repetitive LLM-dialogue corpus** (consciousness_anchor, legacy phase1a1). Density is inflated by heavy
  repetition of stock phrases (c_ab up to **451**) => the order signal is **collocational / idiomatic /
  in-distribution**, not held-out recombination. That is precisely the regime the G1 wall occupies
  (memory h1835: in-context mastery, held-out transfer 0; §4/E1: recombination = falsified capability
  ceiling on all readout/objective/store/binding axes). Diverse prose (corpus.txt EN, ko_wiki) is
  content-level starved.

There IS a dense, real, non-Goodhart content-order data path — but only as **in-distribution
collocation in one synthetic corpus**, which does not by itself promise the held-out recombination G1
fails. A GPU-go on it risks reproducing the collocation-vs-recombination wall; declaring everything
starved under-reports the genuine n=49.

## The one $0 tiebreaker that forks the decision
**Held-out disjoint-vocabulary recombination test on consciousness_anchor** (surface analog of the G1
held-out test, still $0): split content vocab into two halves by frequency parity; from the train split
learn the order-follower map for seen collocation pairs; on held-out text test whether **NOVEL cross-half
pairs that never co-occurred in train** carry the same order-distinguishing follower asymmetry.
- novel unseen pairs carry order signal -> order is **compositional/generalizable** -> F2 is a real
  lever -> **E1 GPU-go** on the anchor content-word recipe (frozen-first; real G1 metric = held-out
  recombination decode; pool summer/aiden, never mini).
- only seen collocations carry it -> **memorized in-distribution collocation** -> F2 collocation-only
  confirmed -> **pivot to H_6163 engine-native falsifier-lane build** (unlocks H_9202 NT-falsifier).

## E1 recipe (if the tiebreaker clears)
- corpus: /Users/mini/dancinlab/anima/archive/state_legacy/anima_phase1a1_color_cosmology_2026_05_12/consciousness_anchor.txt
- vocab: freq top-400 AFTER dropping top-50 freq-stoplist + wordlike shape (content_word_tiebreaker/probe.py)
- gate: MIN_OCC=3, POWER=10, FRAC_BAR=2/3 -> n=49, differ_frac 0.959, NON-DEGENERATE-POWERED (verbatim)
- scope caveat (a_scale_honest_scope): single synthetic corpus · collocational/in-distribution · diverse natural corpora starved.

## Artifacts
- content_word_tiebreaker/probe.py + RESULT.json (the decisive arm, this session)
- {c11_corpus_equiv,self_vocab_corpustxt,ko_wiki_natural,window_relax,relation_typed,small_purpose_density,crosscorpus_yield}/RESULT.json (the 7 probes)

## RESOLVED — held-out recombination tiebreaker (heldout_recomb/, this session)
The forking $0 tiebreaker was RUN. First cut (cross-half by frequency parity) was caught as INVALID
(those pairs still co-occurred >=3x = seen collocations, not held-out) and replaced by two clean arms:
- **RARE restriction** (total count<=8, non-memorized combos): n=8 → INCONCLUSIVE-SPARSE (collapses).
- **TRUE held-out** (80/20 train/test, pairs never adjacent in train, components seen individually): **n=0**.
- FULL content stays n=49 POWERED but count median=16, max=454 = high-repetition collocation.

**VERDICT: COLLOCATION-ONLY.** Strip the high-repetition collocations or require genuine novelty and the
anchor's n=49 content-order signal VANISHES (8, then 0). It is memorized in-distribution collocation, the
exact G1 wall regime (h1835 in-context mastery, held-out transfer 0). **F2 has no held-out-recombination
data path in existing corpora.**

## Final F2 decision
- The E1 forward-slot is structurally GO(P0) (parallel-session #3014 premise-(b) de-risk) — the mechanism is sound.
- But F2 (its training data) is **collocation-only**: existing corpora supply memorized collocation, NOT
  held-out compositional order. An E1 GPU-go trained on this data risks reproducing the collocation-vs-
  recombination wall.
- **Next lever = H_6163 engine-native falsifier-lane build** (the single hard blocker; unlocks H_9202
  NT-falsifier, the next new-mechanism shot). Authored held-out-recombination concept data would be the
  only way to give E1 a non-collocational signal, but that is a data-authoring project, not existing data.
