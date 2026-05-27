# CLM Phase A.6 — AN11(c) Token-Sampling JSD on CLM v4 530M

**Date:** 2026-05-02
**Substrate:** CLM v4 530M (recurrent decoder, d_model=768, n_layer=16, vocab=64000)
**Bench:** `bench/zeta_likert/v1_frozen.json` (20 KO prompts)
**Cost:** $0 (ubu1 RTX 5070, ~16 min total)

## Method

Mirror of ALM r14 AN11(c) token-sampling JSD direct
(`state/cp2_consciousness_r14_remeasure_2026_05_01/an11_c_r14_jsd_direct.json`)
applied to CLM v4 530M with substitutions noted in C3.

- Per prompt: 20 sampling calls × T=0.7, top_p=0.9, max_new=32 tokens.
- JSD (Jensen-Shannon Divergence, base-2, in bits) on empirical
  token-frequency distributions over union vocabulary.
- Reference: CLM v4 trained vs randomly-reinitialized same-arch
  (closest analog to ALM r14 "trained adapter vs base", since CLM has
  no separate base/adapter split).
- Complementary self-baseline: trained CLM v4 sampled with two seeds
  (101 vs 202) — gives intrinsic-stochasticity floor.

## Results

### Primary (trained vs random-init)

| metric | value |
|---|---|
| mean JSD | **0.9994 bits** |
| median JSD | 1.0000 bits |
| min JSD | 0.9949 bits |
| max JSD | 1.0000 bits |
| n_pass (≥0.5) | **20/20** |
| n_strong (≥0.8) | 20/20 |

### Self-baseline (trained vs trained, seeds 101/202)

| metric | value |
|---|---|
| mean JSD | 0.1013 bits |
| n_pass (≥0.5) | 0/20 |

The self-baseline is well below 0.5 — confirming the methodology
distinguishes substrate divergence from intrinsic sampling noise.

### AN11(c) Verdict: PASS

- mean 0.9994 ≥ 0.5  ✓
- 20/20 ≥ 0.5 (≥14/20 required)  ✓

### ALM r14 Comparison

| | ALM r14 | CLM v4 530M |
|---|---|---|
| mean JSD | 0.6864 | 0.9994 |
| n_pass / n_total | 20/20 | 20/20 |
| verdict | PASS | PASS |
| same direction | — | YES |

CLM scores HIGHER mean JSD than ALM but this is the
saturation artifact described in C3-1: the trained CLM produces
near-degenerate KO output (repetitive characters), while the
random-init reference emits near-uniform vocab — making the two
distributions almost completely disjoint (JSD → 1.0 ceiling).

## Honest C3 (3 items)

### C3-1 — Reference distribution choice
ALM r14 compared trained adapter (r14) vs base (no adapter), same
substrate. CLM has no separate adapter, so "trained vs random-init"
is the closest semantic analog. Side effects:

  (a) Random-init produces near-uniform vocab → ceiling-saturated JSD.
  (b) The trained CLM v4 produces degenerate KO output (`ddddd...`,
      `鑑瑑瑑...`) — see `an11_c_clm_jsd.json::sample_trained_first`.
      This makes the two distributions almost disjoint, inflating JSD.
  (c) The PASS verdict is methodologically valid but quality-blind:
      "trained ≠ random" is true even if trained output is low-quality.

### C3-2 — Prompt-set parity (20 vs 16)
CLM Phase A.4/A.5 used 16-prompt slice; ALM r14 used 20. Phase A.6
widened to all 20 KO prompts of `v1_frozen.json` for direct ALM
parity. Per-prompt JSD distribution is uniformly ceiling
(0.9949–1.0000), so the 16/20 split is non-discriminating here.

### C3-3 — Cross-substrate JSD vs single-substrate self-JSD
ALM r14 measured WITHIN-substrate divergence (same Mistral-7B engine,
adapter on/off). Phase A.6 also measured within-substrate
(same ConsciousDecoderV3 class, weights-loaded vs random-init).
Both are within-class comparisons. Cross-substrate JSD (CLM trained vs
ALM r14 trained) was NOT measured — would require shared tokenizer
mapping, which CLM SentencePiece (64k) and ALM Mistral (32k) do not have.

## Files

- `state/strategic_clm_phase_a6_2026_05_01/an11_c_clm_jsd.json` — primary result
- `state/strategic_clm_phase_a6_2026_05_01/an11_c_clm_jsd_self_baseline.json` — noise floor
- `state/strategic_clm_phase_a6_2026_05_01/run_log.json` — phase log

## CP2-CLM Suite 4 implication

AN11(c) **PASS** at the formal threshold but with C3-1 caveat
(saturation artifact, not high-quality output). For a robust
4-of-suite reading, this should be combined with V_phen (A.5)
and Frobenius-norm (A.4) which directly probe trained-model
behavior, not just trained-vs-untrained delta. Suite-level
decision belongs to the orchestrator.
