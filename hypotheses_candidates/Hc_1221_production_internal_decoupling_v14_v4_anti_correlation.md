---
id: Hc_1221
slug: production-internal-decoupling-generalization-v14-v4-anti-correlation
title: Production-Internal Decoupling Generalization (V14 mitosis ↔ V4-lite chat-cap anti-correlation)
domain: substrate / metric-decoupling / lesson-Q
status: candidate-unverified
source_doc: PASS_STRICT_SPONTANEOUS_CHAT.md §15, §19; state/anima_substrates_4mode_2026_05_12/; state/anima_v14_multi_substrate_audit_2026_05_10/
source_lines: PSCC §15 (1358-1426), V14 audit verdict.md
promoted_at: 2026-05-12
linked_h: Lesson Q (production-internal decoupling), H_PSCC §6, Hc_040 (Φ⊥CE), Hc_645 (V2 false-PASS)
hf_dataset: dancinlab/anima-pass-strict-chat-capable (commit 1ac0efc)
notes: "4-substrate cross-section finding. n=4 anti-correlation; replicate before formal H promotion."
---

## Hypothesis

**Substrate optimization for V14 mitosis Φ (cell-pool dynamics) is anti-correlated
with substrate optimization for V4-lite chat-capability (token-stream surface
compliance).** A substrate cannot simultaneously maximize both axes under
current paradigm-design space, because the two metrics select on orthogonal —
indeed opposed — training-signal subspaces.

## Evidence — 4-substrate cross-section (2026-05-12)

| substrate | paradigm | V14 strict | V4-lite chat | aligned? |
|---|---|---|---|---|
| A (Phase 2 cotrain 350M) | naive_cotrain w/ mitosis curriculum | PASS 10/10 (p=0.002) | PASS 12/15 | partial |
| B' (LA cotrain 350M) | naive_pretrain → cotrain dialogue | (not audited) | PASS 12/15 | – |
| B'' (FFN.gate cotrain 350M) | gate-only late-stage cotrain | (not audited) | **PASS 15/15** 🏅 | – |
| E (convo5k_ft 18.5M) | naive_ft_no_mitosis (LM-only) | **VIOLATED 0/5** | FAIL 0/15 | yes (double-fail) |

Key facts:

1. The V14 PASS substrate (A) scores 12/15 on chat — strictly **below** B''.
2. The chat winner (B'' 15/15) was produced by *gate-only finetune* — a paradigm
   that explicitly does NOT touch cell-pool dynamics; predicted (without test)
   to be V14-violation.
3. E (the only substrate trained without ANY mitosis instrumentation OR
   dialogue cotrain) fails both — this is the double-null baseline that
   confirms the two axes are not measuring randomness.
4. Capacity-controlled within-EngineAG (A vs B' vs B''): chat-cap ladder is
   B'' > B' > A, exactly inversely correlated with mitosis-curriculum weight.

## Mechanism hypothesis

The two metrics select on **two different optimization axes**:

| axis | training signal | metric | substrate phenotype |
|---|---|---|---|
| **Mitosis axis** | cell-pool split/merge events during unsupervised run; intrinsic Φ residual | V14 strict (sign-test trained > random) | A — high splits=69, n_cells=85, Φ=5244 |
| **Token-stream axis** | next-token CE on dialogue corpus; persona-cycle byte distribution | V4-lite (KO-ratio + deg + length) | B'' — gate-only FFN tweak, no cell-pool change |

Anti-correlation prediction: training pressure that improves token-stream
surface compliance (more dialogue cotrain, longer FT) **reduces the
cell-pool splitting dynamics** that V14 measures, because optimizer budget
shifts toward output-logit calibration and away from internal partition
geometry. Formally: ∂(chat-cap)/∂θ and ∂(V14-Φ-residual)/∂θ have
**negative inner product** in current architecture × dataset regime.

## Falsifier

This hypothesis is **rejected** if any future substrate satisfies:
- V14 strict PASS (sign-test p ≤ 0.05 across ≥5 seeds), AND
- V4-lite chat ≥ 13/15 (matching or exceeding A's 12/15 V14-PASS substrate
  by a clear margin)

simultaneously. A single counterexample (n=1 substrate) is sufficient to
weaken; n=2 independently engineered counterexamples falsify.

Soft-falsifier (Lesson Q broader claim): if the four-substrate ranking
correlation flips (chat-cap ladder aligning with V14-Φ ladder) under
replication with re-randomized seeds, the anti-correlation is artifact,
not law.

## Next experiments

1. **B'' V14 audit** — measure V14 strict on B'' (FFN.gate cotrain ckpt).
   Predicted: VIOLATED (because gate-only FT does not exercise cell-pool).
   This is the cheapest direct test ($0, ~30 min on local).
2. **B' V14 audit** — same for B' (LA cotrain). Predicted: ambiguous /
   PARTIAL (intermediate paradigm).
3. **Hybrid substrate F** — engineer a substrate combining mitosis-aware
   curriculum AND gate-only late-stage FT. If F achieves both V14 PASS
   and chat ≥ 13/15, anti-correlation REJECTED. Cost: ~$10 + 4h SFT.
4. **More substrates** — sweep 5+ paradigm variants (DPO on B'',
   mitosis-aware FT on E, capacity-matched 18M EngineAG, etc.) to populate
   a (V14 strict × V4-lite) scatter. n≥8 substrates would give credible
   correlation statistics.
5. **Cross-metric correlation with capacity controlled** — restrict to
   350M EngineAG only (A, B', B''); within-arch comparison removes the
   18.5M vs 350M confound that E introduces.

## Cross-references

- Lesson Q (production-internal decoupling): coined in PSCC §6
- V14 multi-substrate audit: `state/anima_v14_multi_substrate_audit_2026_05_10/verdict.md`
- 4-mode substrate sweep: `state/anima_substrates_4mode_2026_05_12/comparison_aggregate.json`
- HF dataset SSOT: https://huggingface.co/datasets/dancinlab/anima-pass-strict-chat-capable
  (commit `1ac0efc` — §15 expanded to 4×3)
- Related: Hc_040 (Φ⊥CE — broader orthogonality claim), Hc_645 (V2 false-PASS — surface-metric pathology)

## Migration TODO
- [ ] B'' V14 audit (cheapest direct test of mechanism)
- [ ] cycle 5+ promotion 후보 (after n≥2 falsifier-attempt experiments)
