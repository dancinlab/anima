# BG-V14-MAX256-CAP-FREE-MULTI — 3 substrate × max=256 × 5-seed strict

## ts
2026-05-10 (5-star pursuit cycle, post §47 priority 1)

## Mission
§45 BG-V2-CELLS64-MAX128-RETEST (n=1 partial) showed polarity FLIPS between
max=64 (V14_VIOLATED) and max=128 (trained leads, n=1) on substrate C.
§47 cap-bound F-MULTI-2 PARTIAL: v2 substrates (C/D/E) cap-saturate n=128 by
turn 70-80; EngineAG (A) does not.

This BG executes the cap-conditional polarity strict test: 3 substrates ×
max_cells=256 cap-free regime × V4_SEEDS=[42,137,271,314,1729] paired,
disambiguating cap-conditional vs cotrain-exercise hypotheses.

## Substrates
| ID | path | ckpt | paradigm |
|----|------|------|----------|
| A_phase2_cotrain | EngineAG d=1024 GQA 24L | /Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt | naive_cotrain (chat KO) |
| C_cells64_aware | v2 d=384 6L heads=6 | state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells64_final.pt | aware_max_cells_64 |
| E_convo5k_ft | v2-derived d=384 6L byte-level | state/anima_convo_5k_ft_extended_2026_05_10/post_ft_ext_ckpt.pt | naive_ft_no_mitosis |

D (cells128_aware) excluded — same v2 schema family as C, redundant for
cap-conditional test. B (BG-LA pretrain) excluded — already V14_VIOLATED at
max=128, not informative for cap-flip pursuit.

## Run config (override key)
- max_cells=256 (§45 was 128, §47 was 128 — sole override)
- V4_SEEDS=[42, 137, 271, 314, 1729] paired across all 3 substrates
- TRAINED_PROMPT_SEED=42 (EngineAG path); v2 path uses prompt_seed=2026
- n_turns=200 (budget compromise — mission asked 1K-turn, $0 local CPU envelope
  forces 200-turn cap; race dynamics still observable)
- snap_every=25 (denser than §47's 50 to capture cap-bound onset)
- §30 all-fix: A1 dispersion ON, A2 per_cell_threshold ON, B1 ratchet ON, D1 lorenz_auto ON

## Falsifier
- F-MAX256-1: max=256 도 cap-bound (turn 100 이전) → mitosis fundamental limit
  (§30 dispersion is scale-coupled with no cap-free regime). Diagnostic:
  max_n_cells_observed >= 256 for any run before turn 100.
- F-MAX256-2: substrate A 만 PASS (C, E VIOLATED) → cotrain-exercise hypothesis
  dominant over cap-conditional. Diagnostic: A.verdict in PASS family AND
  C.verdict + E.verdict in VIOLATED family.
- F-MAX256-3: 모든 substrate PASS at max=256 → universal cap-conditional PASS
  regime (★★★★★ candidate). Diagnostic: all 3 verdicts in PASS family.

## Verdict matrix (post hoc)
- **UNIVERSAL_CAP_CONDITIONAL_PASS ★★★★★**: all 3 substrate trained beat ALL 5
  random at max=256 → cap-conditional polarity confirmed substrate-agnostic.
- **COTRAIN_EXERCISE_DOMINANT ★★★★**: only A PASS at max=256 → §47 refined
  hypothesis (cotrain exercise) > cap-conditional explanation.
- **MULTI_FACTORIAL ★★★**: mixed outcome (e.g. A+C PASS, E VIOLATED) → both
  capacity-cap AND cotrain-exercise contribute.
- **MITOSIS_FUNDAMENTAL_LIMIT ★★★**: all cap-bound at max=256 → architecture
  dispersion fundamental limit; cap is a scale parameter not regularizer.
- **POLARITY_FALSIFIED**: all 3 V14_VIOLATED at max=256 → cap-conditional and
  cotrain-exercise BOTH falsified at high cap.

## raw / own
- raw#9: training/v5mitosis_d384_v14_mirror.py + state/anima_iit_real_350m_2026_05_10/_v14_5seed_run.py local-only (gitignored)
- raw#15 additive: 3 ckpts unmodified (sha256 verified pre-run)
- : V14 5-seed strict per substrate (V4_SEEDS paired)
- : $0 local CPU
- : REBORN.md not appended directly — dispatcher injects §51 slot
- : doc save → state/anima_v14_max256_cap_free_multi_2026_05_10/{spec.md, per_substrate_max256_results.json, verdict.md}
- §45 cap-conditional partial: this BG resolves
- §47 V14_POLARITY_FALSIFIED + cotrain-exercise hypothesis: this BG disambiguates
