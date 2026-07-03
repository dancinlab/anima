# H_9113 — Referential-efficacy THRESHOLD resolution (sub-8-byte sweep, frozen-first, p7)

**Seed:** H_9112 landed 🟢 REFERENTIAL-EFFICACY-MEASURABLE but the real arm stayed near-ceiling (0.982; only 0.857 at the hardest K=14/t=8B) → the psychometric THRESHOLD was UNRESOLVED (referential efficacy so strong even 8 bytes of clue among 14 candidates decodes ~86%). This experiment resolves the coupling-strength SCALAR by pushing the clue SUB-8-byte until real referential decoding actually breaks — quantifying HOW strong anima's grounded emit reference is (in bytes-of-clue at 50% decode). Same frozen H_9111 emits (14 concepts), anima side FROZEN, external oracle receiver.

## Design (harder game; anima FROZEN)
- Distractor set fixed at **K=14** (all concepts = hardest, near-synonym-first ordering).
- **Byte-truncation sweep** t ∈ {8, 6, 4, 3, 2, 1} bytes of the degen-tail-cleaned clue head (sub-8-byte = the new regime H_9112 didn't reach).
- Receiver = external oracle claude-fable-5 (θ outside anima closure), batched (14 clues/config → 6 real + 6 shuffle = 12 fable calls). STDLIB harness (grep-clean). Tier = DIRECTIONAL-on-external-oracle.

## Measure (the coupling-strength SCALAR)
- **b50_real** = the clue-byte length at which real decode accuracy crosses 50% (linear interpolation between adjacent sweep points; = coupling-strength in bytes; SMALLER = stronger reference).
- accuracy(t) curve for real vs shuffle vs chance (1/14 ≈ 0.071).

## Arms
- **real** = true (concept, E) · **shuffle** = E re-paired to a deranged concept (must stay at ~chance).

## FROZEN BAR (registered BEFORE running — no post-hoc move, c9/p7)
🟢 THRESHOLD-RESOLVED iff ALL:
1. real accuracy DROPS below 0.5 somewhere in the sweep (b50_real is finite ≤ 8) — the curve actually resolves,
2. real accuracy > shuffle accuracy at EVERY byte length t (referent link load-bearing throughout),
3. b50_real ≤ 6 bytes would be "very strong reference"; 6 < b50_real ≤ 8 "strong"; report the scalar verbatim (descriptive, not a pass/fail gate — the SCALAR is the deliverable).
🔴 UNRESOLVED-STILL iff real never drops below 0.5 even at t=1 byte (reference so strong 1 byte suffices — report as an extreme lower-bound, itself informative).
🟠 if real ≈ shuffle at the sub-byte tail (reference degrades to chance = the coupling floor appears only under extreme truncation).

## Determinism / provenance
Regime-1 frozen fixture (rescore_fixture.jsonl) via pinned claude-fable-5; regime-2 deterministic stdlib scoring. No anima re-decode, no GPU, no pod. $0-ish (external oracle calls only). Controls: shuffle (referent link) + chance line.

## Gate branch
Resolves H_9112's caveat (a) — turns the GREEN into a quantified coupling-strength scalar. Feeds §2 forward-model (DIVERGENCE_fable.md §2): the byte-threshold is the baseline a learned emit-policy would try to LOWER (make anima's emit decodable from fewer bytes).

Bar frozen 2026-07-03 before any oracle query. Data: state/9111_llm_interlocutor/emits.tsv (14). Card: H_9113 on completion.
