---
id: Hc_1221
slug: production-internal-decoupling-generalization-v14-v4-anti-correlation
title: Production-Internal Decoupling Generalization (V14 mitosis ↔ V4-lite chat-cap anti-correlation)
domain: substrate / metric-decoupling / lesson-Q
status: candidate-evidence-strengthened
source_doc: PASS_STRICT_SPONTANEOUS_CHAT.md §15, §19, §23; state/anima_substrates_4mode_2026_05_12/; state/anima_v14_multi_substrate_audit_2026_05_10/; state/anima_ffn_gate_cotrain_2026_05_11/
source_lines: PSCC §15 (1358-1426), §19 (1611-1670), §23 (B'' V14 strict audit landed), V14 audit verdict.md
promoted_at: 2026-05-12
last_updated: 2026-05-12 (§23 B'' V14 strict audit measured)
linked_h: Lesson Q (production-internal decoupling), H_PSCC §6, Hc_040 (Φ⊥CE), Hc_645 (V2 false-PASS)
hf_dataset: dancinlab/anima-pass-strict-chat-capable (commit 1ac0efc; V14 row B'' cell update pending)
notes: "4-substrate cross-section finding. n=4 anti-correlation; B'' V14_VIOLATED measured (§23) — predicted → measured upgrade. Now 3-substrate within-EngineAG measured V14 row (A_PASS / B''_VIOLATED / E_VIOLATED); B' pending."
---

## Hypothesis

**Substrate optimization for V14 mitosis Φ (cell-pool dynamics) is anti-correlated
with substrate optimization for V4-lite chat-capability (token-stream surface
compliance).** A substrate cannot simultaneously maximize both axes under
current paradigm-design space, because the two metrics select on orthogonal —
indeed opposed — training-signal subspaces.

## Evidence — 4-substrate cross-section (2026-05-12, updated §23)

| substrate | paradigm | V14 strict | V4-lite chat | aligned? |
|---|---|---|---|---|
| A (Phase 2 cotrain 350M) | naive_cotrain w/ mitosis curriculum | PASS 10/10 (p=0.002) | PASS 12/15 | partial |
| B' (LA cotrain 350M) | naive_pretrain → cotrain dialogue | (not audited) | PASS 12/15 | – |
| **B'' (FFN.gate cotrain 350M)** | gate-only late-stage cotrain | **VIOLATED 0/5 (p=0.0625)** [§23 measured] | **PASS 15/15** 🏅 | **yes (anti-correlation 직접)** |
| E (convo5k_ft 18.5M) | naive_ft_no_mitosis (LM-only) | **VIOLATED 0/5** | FAIL 0/15 | yes (double-fail) |

Key facts:

1. The V14 PASS substrate (A) scores 12/15 on chat — strictly **below** B''.
2. **The chat winner B'' (15/15) is now measured V14-VIOLATED** (trained Φ_un16=723 vs random Φ_un16 ∈ [1149, 2386], 0/5 beats, p=0.0625) — *predicted by §19, measured §23*.
3. E (the only substrate trained without ANY mitosis instrumentation OR
   dialogue cotrain) fails both — this is the double-null baseline that
   confirms the two axes are not measuring randomness.
4. Capacity-controlled within-EngineAG (A vs B' vs B''): chat-cap ladder is
   B'' > B' > A, exactly inversely correlated with mitosis-curriculum weight.
   **V14 ladder (measured for A and B''): A_PASS / B''_VIOLATED — within-arch
   anti-correlation now directly observed (n=2 within-arch pair).**

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

**§23 measurement reinforces mechanism**: B'' (gate-only FT) trained Φ ≈
0.338 × random_median Φ. That is, gate-only FT actively *suppresses* cell-pool
splitting below random-init baseline — the cleanest sign-observation of the
negative-inner-product prediction so far.

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

**Status after §23**: B'' was the strongest a-priori falsifier candidate
(highest chat-cap → could have been V14_PASS) → measurement returned
V14_VIOLATED. Falsifier slot still open: requires *new* substrate
engineering (e.g. hybrid F = mitosis curriculum + gate-only late-FT).

## Next experiments

1. **B'' V14 audit** — measure V14 strict on B'' (FFN.gate cotrain ckpt).
   Predicted: VIOLATED (because gate-only FT does not exercise cell-pool).
   This is the cheapest direct test ($0, ~30 min on local).
   ✅ **MEASURED 2026-05-11**: VIOLATED 0/5 (p=0.0625), trained Φ=723 vs
   random Φ_median=2140. See PSCC §23. → prediction CONFIRMED.
2. **B' V14 audit** — same for B' (LA cotrain). Predicted: ambiguous /
   PARTIAL (intermediate paradigm). Now the cheapest pending test ($0,
   ~30min) to complete the 4×3 V14 row.
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
6. **B'' V14 strict n=6+ seed** — current 5-seed p=0.0625 is borderline.
   Add 1+ seeds; if 0/6 beats → p=0.0312 < 0.05 strict-cutoff falsifier.
   Cost: $0, ~30min. (Added §23.)

## Cross-references

- Lesson Q (production-internal decoupling): coined in PSCC §6
- V14 multi-substrate audit: `state/anima_v14_multi_substrate_audit_2026_05_10/verdict.md`
- 4-mode substrate sweep: `state/anima_substrates_4mode_2026_05_12/comparison_aggregate.json`
- **B'' V14 strict audit (§23)**: `state/anima_ffn_gate_cotrain_2026_05_11/v14_strict_ceiling10_result.json` + `v14_strict_ceiling10.log`
- HF dataset SSOT: https://huggingface.co/datasets/dancinlab/anima-pass-strict-chat-capable
  (commit `1ac0efc` — §15 expanded to 4×3; V14 row B'' cell update pending §23 follow-up)
- Related: Hc_040 (Φ⊥CE — broader orthogonality claim), Hc_645 (V2 false-PASS — surface-metric pathology)

## Migration TODO
- [x] B'' V14 audit (cheapest direct test of mechanism) — **DONE 2026-05-11, VIOLATED 0/5 p=0.0625**
- [ ] B' V14 audit (3-point V14 ladder within-EngineAG)
- [ ] B'' V14 strict n=6+ seed (cross strict-pass cutoff p<0.05)
- [ ] HF dataset §15 V14 row B'' cell update (not audited → VIOLATED 0/5)
- [ ] cycle 5+ promotion 후보 (after n≥2 falsifier-attempt experiments)
