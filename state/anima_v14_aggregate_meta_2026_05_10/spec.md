# BG-V14-STRICT-AGGREGATE-META-ANALYSIS — Spec

- bg_id: BG-V14-STRICT-AGGREGATE-META-ANALYSIS
- ts: 2026-05-10
- scope: cycle 2026-05-10 V14 results — §33, §38, §43, §44, §47, §51, §55, §56, §57
- mode: $0 local CPU analysis (own 16). raw#15 only existing data; raw#9 no training.
- output: /Users/ghost/core/anima/state/anima_v14_aggregate_meta_2026_05_10/{spec.md, all_v14_results.json, meta_analysis.json, verdict.md}
- code: run_meta.py — pure stdlib (math + json), no scipy/numpy.

## Data sources (existing-only)
- §33: state/anima_iit_real_350m_2026_05_10/result.json (max=32, n=5 mirrors)
- §38: state/anima_v14_strict_resolution_2026_05_10/result_10seed.json (max=128, n=10)
- §44: state/anima_phase2_max128_independent_reproduce_2026_05_10/result.json (max=128, n=5 disjoint)
- §47: state/anima_v14_multi_substrate_audit_2026_05_10/per_substrate_v14_results.json (B, C, D, E)
- §51: state/anima_v14_max256_cap_free_multi_2026_05_10/per_substrate_max256_results.json (A=5/5, C=2/2, E=2/2)
- §55: state/anima_v14_max256_ce_strict_n5_2026_05_10/result.json (C n=5, E n=5 strict)
- §56: state/anima_v14_max256_b_no_cotrain_2026_05_10/result.json (B no_cotrain max=256)
- §57: state/anima_engine_a_layer_slab_swap_2026_05_10/{summary.json, cond_A0..A3.json}
- §43: state/anima_foundation_borrow_a_fire_2026_05_10/verdict.json (foundation borrow — orthogonal metric, NOT in within-arch aggregate)

## Method

1. Per-study paired comparison: trained vs each random_init mirror seed → Bernoulli "trained beats mirror_i". k = # successes, n = # mirror seeds. Sign-test p (two-sided + one-sided upper).
2. Aggregate sign test: pool all (k, n) across all quantitative studies (n_total = 72 trials).
3. Fisher's combined p: chi2 = -2 sum log p_one_sided_i, df = 2k.
4. Bayesian beta-binomial posterior on aggregate "P(trained beats random)" with Beta(1,1) prior. Compute P(theta > 0.5).
5. Cochran's Q heterogeneity using Haldane-corrected log-odds against logit(0.5)=0; I^2 = max(0, (Q-df)/Q).
6. Sub-stratification: substrate / arch / paradigm / cap / cap_binding.
7. Confounding decomposition: within-arch paradigm comparison; within-paradigm cap comparison.

## Falsifiers
- F-META-1: heterogeneity I^2 > 0.5 → directional inconsistency
- F-META-2: Fisher combined p > 0.001 → weaker than naive joint
- F-META-3: cross-arch contradiction → mechanism differs

## Constraints
- raw#15: existing data only
- raw#9: no training/*.py
- own 16: $0 local CPU
- own 22: REBORN.md not appended directly
- own 38: state/ output only
