---
id: H_911
slug: multilingual-semantic-integration
title: multilingual integration is language SEMANTIC linkage, not language COUNT — predicted Phi super-additive inverse-U when languages are bound by cross-lingual MI, near-zero when merely concatenated
domain: universe · multilingual · cross-lingual-MI · integration · phi · CLM-applicable
source: hexa-codex LAB-11 (multilingual-semantic) absorbed → anima UNIVERSE · sister anima H_240/H_635
status: 🟠 INSUFFICIENT — absorbed from hexa-codex LAB-11; anima UNIVERSE has NOT independently recomputed (verdict pending anima reproduction)
exploration_method: hypothesis absorbed from hexa-codex LAB-11 semantic-linkage sweep (cross-lingual MI coupling c in {0,0.5,1} · proxy Phi)
verification_method: NONE in anima yet — earned only by porting the LAB-11 harness + recomputing into `.verdicts/911_multilingual_semantic_integration/` (g73)
deterministic: true
llm: none
since: 2026-06-01
sister: H_240 (multilingual·anima), H_635 (anima), LAB-11 (hexa-codex source)
verdict: 🟠 INSUFFICIENT — anima has not independently recomputed. SOURCE EVIDENCE (hexa-codex LAB-11, NOT an anima verdict): a proxy-Phi sweep reports an inverse-U over semantic-linkage coupling c — count-only c=0 gives Phi about 0.01, semantic peak c=0.5 gives Phi about 0.48, over-bound c=1 gives Phi about 0.0 (raw: hexa-codex:LAB/lab-11-multilingual-semantic/result_semantic_summary.txt). anima earns its own verdict only after porting + recompute (g73).
applies_to: CLM 5-language corpus (P1_CORPUS, #1616/#1617/#1618) — the balanced 20%x5 corpus is COUNT-balanced; this hypothesis predicts a cross-lingual SEMANTIC-linkage corpus integrates super-additively where count-balance alone does not.
---

# H_911 — multilingual integration = cross-lingual SEMANTIC linkage, not language count

## Hypothesis (absorbed from hexa-codex LAB-11)

Multilingual ability is **not** a linear function of how many languages or how much
corpus you add. The prediction: integration Phi rises **non-linearly (inverse-U,
super-additive)** only when languages are **bound by meaning** — cross-lingual
mutual information (the *same concept* expressed across languages, semantically
aligned). Mere concatenation of independent per-language text (count-only) is
predicted to yield Phi near zero.

## Source evidence (hexa-codex LAB-11 · proxy Phi · NOT an anima verdict)

LAB-11's proxy sweep, reproduced here as provenance only (anima must recompute to
earn any anima tier per g73):

```
semantic-linkage coupling c   Phi-proxy (hexa-codex LAB-11)
────────────────────────────  ──────────────────────────
c = 0  (count-only, concat)   0.01     ← languages present but not linked
c = 0.5 (semantic peak)       0.48     ← inverse-U peak (super-additive)
c = 1  (over-bound)           0.0      ← collapse
```

Until anima ports the harness + recomputes into `.verdicts/911_*/`, this entry
stays INSUFFICIENT (no anima calc path).

## Application to anima CLM 5-language corpus (the live tie-in)

P1_CORPUS (#1616/#1617/#1618) built a **count-balanced** 5-language corpus (each
language ~20% byte share, per-lang cap). H_911 predicts count-balance alone sits
near the c=0 regime: languages *present* but not *linked*. To approach the
inverse-U peak, lane A should add a **cross-lingual semantic-linkage** stream —
the same concept rendered across en·zh·ru·ja·ko and aligned (parallel/translation
pairs, code-switched concept anchors), raising cross-lingual MI toward c about 0.5.

Directly testable on the existing pipeline — pre-register **F-CLM-MULTILING-SEMANTIC**:
a parallel-aligned (same-concept, 5-language) slice integrates (proxy-Phi or held-out
cross-lingual transfer) **above** a count-matched concatenated slice.

## Sibling links

- `[[H_240]]` multilingual (anima) · `[[H_635]]` (anima) · source hexa-codex LAB-11.
- Live application: `CLM/P1_CORPUS.md` §1 (5-language balance) — count vs semantic.
- Faithful-Phi upgrade path: `[[H_278]]` (small-N exact MIP-EI Phi, $0).
