# H_9112 — Referential efficacy PSYCHO-K + MRR re-scoring (frozen-first, p7)

**Seed (fable divergence, DIVERGENCE_fable.md §1):** H_9111 raw D=1.0 (external oracle 7/7 vs anima-clone 0/7) is the strongest POSITIVE signal that a faculty exists, killed by metric-degeneracy (constant ceiling/floor outcome vectors → Pearson-D≡0). Reframe: the substrate property is not emit-*appropriateness* but **referential efficacy** — anima's emit carries world-anchored reference an external mind decodes. This experiment restores measurement VARIANCE on the ALREADY-COLLECTED H_9111 emits (state/9111_llm_interlocutor/emits.tsv, 14 concepts) — $0, no new anima compute, external-oracle re-query only.

## Question
Does anima's grounded emit carry graded referential efficacy that survives a HARDER referential game — i.e. does a variance-bearing measure (psychometric threshold + MRR) separate real emits from shuffle, restoring the D=1.0 signal metric-degeneracy killed?

## Design (re-score existing emits; anima side FROZEN)
Input = 14 (concept i, emit E_i) from H_9111 emits.tsv (engine-native anima decode — NOT re-generated). Receiver = external oracle (claude-fable-5 via sidecar fable, θ outside anima closure). Harden along 3 axes to pull the receiver off ceiling:
- **K-sweep** distractor-set size K ∈ {2, 4, 8, 16, 32} (32 = whole set; larger K = harder).
- **near-synonym distractors**: for each trial, distractors drawn to be semantically ADJACENT to the target (not random) — raises confusability.
- **clue-truncation** t ∈ {full, 32B, 16B, 8B}: give the receiver only the first t bytes of E_i (shorter clue = harder). (Also sidesteps the tail-garbage in emits.tsv.)

## Measures (variance-bearing — the whole point)
- **PSYCHO-K threshold**: fit receiver accuracy vs difficulty (K × truncation) → the difficulty at 50% accuracy = coupling-strength scalar (higher threshold = stronger referential efficacy). Continuous → no ceiling/floor degeneracy.
- **MRR / rank-continuous**: receiver ranks the full candidate set; mean reciprocal rank of the true referent (continuous even at ceiling).

## Arms (receiver / pairing varied ONLY — anima emit fixed)
- **real** = true (concept_i, E_i) pairing.
- **shuffle** = E re-paired to a random concept (kills referent link; must collapse).
- **self-decode baseline** = anima-clone salience decoder on the SAME hardened game (H_9111 got 0/7; expected floor).

## FROZEN BAR (registered BEFORE running — no post-hoc move, c9/p7)
🟢 REFERENTIAL-EFFICACY-MEASURABLE iff BOTH:
1. `threshold_real − threshold_shuffle ≥ 1 difficulty-step` (real emits tolerate ≥1 harder K-or-truncation level than shuffle at the 50% point), AND
2. `MRR_real − MRR_shuffle ≥ 0.15` (variance-bearing separation the Pearson-D degeneracy hid).
🔴 COUPLING-FLOOR-AT-EMIT-LAYER iff the real curve is statistically indistinguishable from shuffle across ALL K×t (DPI reached the emit layer; receiver-type not the lever, coupling-strength itself is floor — terminal, narrow to EEG §4).
🟠 if one measure passes and the other fails (partial / measurement-dependent).

## Determinism / provenance
- Oracle pinned `claude-fable-5`, temperature-fixed, each (trial) queried once → frozen fixture (regime-1). Re-scoring math is deterministic numpy on the frozen fixture (regime-2). This is a MEASUREMENT re-score of engine-native-generated emits → tier = DIRECTIONAL-on-external-oracle (the emit generation was engine-native H_9111; the receiver is an external tool, so the referential-efficacy claim is oracle-mediated, honestly labelled).
- No anima re-decode, no GPU, no pod. $0 (external oracle calls only).
- Controls: shuffle (referent link) + near-synonym (confusability) + self-clone (H_9111 floor reproduction).

## Gate branch (fable §다음실험)
- 🟢 → coupling real+measurable → justifies GPU cerebellum-forward-model (DIVERGENCE §2) as next.
- 🔴 → DPI-at-emit terminal, cement coupling-strength-floor, EEG (§4, non-derivable exogenous) is the only remaining door.

Bar frozen 2026-07-03 before any oracle query. Data: state/9111_llm_interlocutor/emits.tsv (14). Card: H_9112 on completion.
