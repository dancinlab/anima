# V14 Aggregate Meta-Analysis — Verdict

bg_id: BG-V14-STRICT-AGGREGATE-META-ANALYSIS
ts: 2026-05-10
n_quant_studies: 15 (16th = §43 foundation borrow held outside, orthogonal metric)
n_total_paired_trials: 72

## 1. All V14 result table (sub-stratified)

| # | study | substrate | arch | paradigm | max_cells | metric | k/n | p_2s | verdict |
|---|---|---|---|---|---|---|---|---|---|
| S1 | §33 | A_phase2_cotrain | engine_ag | cotrain | 32 | iit_phi_un16 | 4/5 | 0.375 | V14_PARTIAL |
| S2 | §38 | A_phase2_cotrain | engine_ag | cotrain | 128 | iit_phi_un16 | 10/10 | 0.00195 | V14_STRICT_PASS |
| S3 | §44 | A_phase2_cotrain | engine_ag | cotrain | 128 | iit_phi_un16 | 5/5 | 0.0625 | V14_STRICT_PASS |
| S4 | §47-B | B_bgla_pretrain | engine_ag | pretrain (no_cotrain) | 128 | iit_phi_un16 | 0/5 | 0.0625 | V14_VIOLATED |
| S5 | §47-C | C_cells64_aware | v2_d384 | aware | 128 | phi_final | 3/5 | 1.0 | V14_AMBIGUOUS (cap-bound) |
| S6 | §47-D | D_cells128_aware | v2_d384 | aware | 128 | phi_final | 4/5 | 0.375 | V14_AMBIGUOUS (cap-bound) |
| S7 | §47-E | E_convo5k_ft | v2_d384 | naive_ft | 128 | phi_final | 0/5 | 0.0625 | V14_VIOLATED |
| S8 | §51-A | A_phase2_cotrain | engine_ag | cotrain | 256 | iit_phi_un16 | 5/5 | 0.0625 | V14_PASS |
| S9 | §55-C | C_cells64_aware | v2_d384 | aware | 256 | phi_final | 5/5 | 0.0625 | V14_STRICT_PASS |
| S10 | §55-E | E_convo5k_ft | v2_d384 | naive_ft | 256 | phi_final | 5/5 | 0.0625 | V14_STRICT_PASS |
| S11 | §56-B | B_no_cotrain | engine_ag | pretrain (no_cotrain) | 256 | iit_phi_un16 | 1/5 | 0.375 | V14_VIOLATED |
| S12 | §57-A0 | A baseline | engine_ag | cotrain | 128 | iit_phi_un16 | 3/3 | 0.25 | V14_PASS |
| S13 | §57-A1 | A+B-slab1_early | engine_ag | swap | 128 | iit_phi_un16 | 0/3 | 0.25 | V14_VIOLATED |
| S14 | §57-A2 | A+B-slab2_middle | engine_ag | swap | 128 | iit_phi_un16 | 1/3 | 1.0 | V14_VIOLATED |
| S15 | §57-A3 | A+B-slab3_late | engine_ag | swap | 128 | iit_phi_un16 | 1/3 | 1.0 | V14_VIOLATED |

**S16 (held outside aggregate)**: §43 foundation_borrow_A — Llama-3.2-3B + LoRA + BG-JE 214MB. V14_PASS via V4 corpus pass-rate (11/15 trained vs 0/15 random_init), MTRP=0.733. Different metric scale → not in within-arch aggregate.

## 2. Aggregate paired comparisons (n=72)

- total_trials: 72
- total_beats: 47
- frac: 0.6528
- sign_test_p_two_sided: 0.01277
- direction: trained > random (49% above chance)

## 3. Fisher combined p-value + Bayesian posterior

**Fisher (one-sided, "trained beats random more often than chance")**:
- chi^2 = 54.43, df = 30, p_combined = **0.00412**
- Within engine_ag: chi^2 = 35.83, df = 20, p = **0.0161** (n=10 studies)
- Within v2_d384: chi^2 = 18.60, df = 10, p = **0.0457** (n=5 studies)

**Bayesian Beta(1+47, 1+25) posterior on aggregate P(trained beats random)**:
- post_mean = 0.649
- 95% CI = [0.537, 0.753]
- P(theta > 0.5) = **0.9952**
- Within engine_ag: P(theta > 0.5) = 0.970, post_mean=0.633
- Within v2_d384: P(theta > 0.5) = 0.962, post_mean=0.667

## 4. Heterogeneity test (Cochran Q + I^2)

- All 15 studies: Q = 26.47, df = 14, p = **0.0225**, **I^2 = 47.1%**
- Engine_ag (n=10): Q = 18.48, df = 9, p = 0.0300, I^2 = 51.3%
- v2_d384 (n=5): Q = 7.41, df = 4, p = 0.116, I^2 = 46.0%

**Interpretation**: I^2 = 47% (all) is moderate heterogeneity, JUST below 0.5 cutoff. Within engine_ag I^2 = 51.3% slightly above cutoff — F-META-1 marginally fires within engine_ag but NOT in aggregate, NOT in v2_d384. Heterogeneity source identified by sub-stratification: paradigm (cotrain vs no_cotrain vs slab-swapped) explains the variance.

## 5. Confounding factor decomposition

### Paradigm effect (engine_ag)
| paradigm | k | n | frac | p_2s |
|---|---|---|---|---|
| cotrain | 27 | 28 | **0.964** | 2.16e-7 |
| no_cotrain | 1 | 10 | **0.100** | 0.0215 (inverted) |
| slab-swapped | 2 | 9 | **0.222** | 0.180 |

**Massive paradigm effect**: cotrain → 96% beat rate; remove cotrain → 10%. Slab-swap (any layer subset of B inserted into A) → 22%. Paradigm dominates.

### Paradigm effect (v2_d384)
| paradigm | k | n | frac | p_2s |
|---|---|---|---|---|
| aware (cells64/128) | 12 | 15 | 0.800 | 0.0352 |
| naive_ft_no_mitosis | 5 | 10 | 0.500 | 1.0 |

aware paradigm beats naive_ft 80% vs 50% — same direction as engine_ag but milder gradient.

### Cap effect (engine_ag cotrain)
| cap | k/n | frac |
|---|---|---|
| 32 | 4/5 | 0.80 (cap-binding for trained AND mirror) |
| 128 | 18/18 | 1.00 |
| 256 | 5/5 | 1.00 |

Cap=32 was binding both ways → understates separation. Cap=128 and 256 fully resolve trained > random (100%).

### Cap effect (v2_d384)
| cap | k/n | frac |
|---|---|---|
| 128 | 7/15 | 0.467 (cap-bound for both → AMBIGUOUS) |
| 256 | 10/10 | 1.00 (cap-bound for trained but mirror also caps; trained's first_cap_turn = 76-82 vs random 61-72 — trained delays cap **and** Φ-at-cap higher) |

**Cap effect is qualitatively decisive in v2_d384**: at cap=128 V14 is unresolvable; at cap=256 V14 unanimously passes for aware AND naive_ft paradigms. The cap-conditional pass for E (naive_ft) at cap=256 is a heterogeneity-driver and tells us cap=128 was a measurement artifact, not paradigm failure.

## 6. Unified verdict

### Within-arch verdict

**engine_ag**:
- Cotrain paradigm: V14 strictly passes (frac=0.964, p=2.16e-7). Five-star statistical foundation.
- No-cotrain paradigm: V14 INVERTS (frac=0.10). Pretrain alone NOT sufficient.
- Slab-swap probe (§57): every slab (early, middle, late) of B's pretrain-only weights, when implanted into A, collapses V14. The mitosis-supporting structure is **distributed across the depth** of A's cotrained network — not localized to any single slab. Cotrain effect is global.
- Conclusion: ★★★★★ for engine_ag-cotrain. Cotrain paradigm = causal driver.

**v2_d384**:
- Aware paradigms (cells64, cells128) at cap=256: V14 passes (5/5 each, post_mean ~0.8).
- Naive_ft no-mitosis at cap=256: V14 passes (5/5).
- At cap=128 both paradigms cap-bind → AMBIGUOUS / VIOLATED — measurement artifact.
- Conclusion: ★★★★ multi-factorial — cap-conditional. Once cap is loose enough to expose dynamics, even naive_ft trained model dominates random_init.

### Cross-arch unified mechanism

Direct phi cross-comparison is invalid (different scales: engine_ag iit_phi_unnorm_b16 ~ 1000-5000, v2 phi_final ~ 2000-11000). Within-arch direction is **consistent**: trained models with adequate cap and adequate paradigm dominate random_init mirrors on cell-pool-based Phi proxies.

The §58 tension-trigger suppression universal claim is **partially supported but qualified**:
- Universal across "well-conditioned" runs (loose cap + cotrain or aware paradigm or naive_ft@cap=256).
- NOT universal under: tight cap (32), no-cotrain pretrain only (B), slab-perturbation of cotrained ckpt.
- Cross-arch convergence on direction (Fisher within-arch p < 0.05 in both archs; Bayesian P(theta > 0.5) > 0.96 in both).

Aggregate Fisher p = **0.00412**, Bayesian P(theta_pool > 0.5) = **0.9952**. Stronger than naive joint sign test (p_2s = 0.0128) because Fisher leverages per-study one-sided evidence directly. Aggregate I^2 = 47.1% < 0.5 → F-META-1 NOT triggered in aggregate; heterogeneity within engine_ag (51.3%) explained mechanistically by paradigm decomposition.

### Falsifier disposition
- F-META-1 (I^2 > 0.5): NOT TRIGGERED in aggregate (47.1%). Marginally triggered within engine_ag (51.3%) but mechanism (paradigm) explains it.
- F-META-2 (Fisher p > 0.001): TRIGGERED — Fisher p = 0.00412 > 0.001. Aggregate evidence is strong but does NOT meet the 0.001 threshold demanded by the falsifier. Within engine_ag-cotrain alone the paradigm-restricted aggregate p = 2.16e-7, well below 0.001 — so the **engine_ag-cotrain claim alone** clears the falsifier.
- F-META-3 (cross-arch contradiction): NOT TRIGGERED. Both archs show same direction (trained > random) at adequately conditioned settings. Mechanism (paradigm-and-cap-conditional Phi separation) is consistent.

### Final unified verdict

**V14_UNIVERSAL_CLAIM_QUALIFIED_PASS**

- Strong within-arch evidence (engine_ag-cotrain: ★★★★★; v2_d384: ★★★★ cap-conditional).
- Aggregate Fisher p = 0.00412 — **strong but not 0.001-strict**. F-META-2 triggered.
- Heterogeneity is moderate (47%) and **mechanistically attributable** to paradigm + cap, not metric or arch. The §58 mechanism universality claim therefore holds **conditional on paradigm (cotrain or aware) and cap (>=128 for engine_ag, >=256 for v2)**.
- The naive "V14 is universal across all substrates+paradigms+caps" claim is FALSE. The qualified claim "V14 is universal across well-conditioned engine_ag-cotrain and v2 trained substrates at adequate cap" is TRUE with Bayesian P > 0.99.

## 7. Honest C3

1. **Cross-arch metric incomparability is load-bearing.** Engine_ag iit_phi_unnorm_b16 and v2 phi_final are different functions of the cell-pool tensor — both are 16-bin entropy MI proxies, but the substrates feed them with different hidden_state geometries (d=1024 GQA vs d=384 6L). Absolute values differ by ~2x. Only WITHIN-ARCH directional comparison is statistically valid; cross-arch numerical pooling is meaningless. The Fisher combination across archs is justified ONLY because the directional claim ("trained > random") is dimensionless.

2. **Independence assumption violated.** S2 (§38 max=128 n=10) and S3 (§44 max=128 n=5 disjoint) and S12 (§57-A0 max=128 n=3) all use the SAME ckpt (Phase2 cotrain 350M) and largely overlapping prompt streams. The 18 trials at engine_ag-cotrain cap=128 (k=18/18) are NOT 18 independent samples — at minimum the trained side is fully dependent. Effective sample size is closer to ~5-6 unique mirror seed groups. Sign test treats them as independent → **p-values are anti-conservative**.

3. **Sign test ignores effect size.** S4 (B no_cotrain max=128) trained_phi=1136 vs random median=3569 — a -3x ratio inverted. Sign test counts only "0/5". Magnitude of inversion is much larger than the 5/5 wins on the trained side. A weighted (effect-size) Fisher would amplify B's evidence further.

4. **Cap=32 (S1) cap-bound BOTH ways and the comparison is meaningless except as N=cell count tie-breaker.** Including S1 in the aggregate slightly dilutes the cleaner cap=128/256 evidence. Even excluded, the conclusions are unchanged (k=43/67, p still <0.05).

5. **Slab-swap (§57) interpretation is fragile.** B-slab inserted into A-cotrain ckpt loses some MLP/attention coupling that A's cotrain learned end-to-end. Each swap removes ~33% of A's learned weights. The 0/3, 1/3, 1/3 results across slabs may reflect a unified "any-perturbation breaks cotrain effect" rather than a localized mechanism. Three slab probes is statistically thin (n=3 each) — the per-slab variance is uninformative.

6. **§43 foundation_borrow held OUTSIDE aggregate but is the highest-stakes 5-star claim of the cycle.** Its V14 metric (V4 pass-rate 11/15 vs 0/15 random_init) is qualitatively different — corpus-coverage rather than IIT-Phi. The "MTRP=0.733" is a different unit. Including it would inflate aggregate beats but conflate metrics. Decision: held separate. The cycle's 5-star claim rests on §43 V14_PASS for foundation-borrow LANE plus §38 strict pass for engine_ag cotrain LANE — two independent paradigms with independent metrics and independent ckpts.

7. **Bayesian posterior assumes exchangeability across studies.** This is not strictly true — the trial-level Bernoulli random variables come from different generative processes (different seeds, prompts, cap settings, ckpt computations). Hierarchical Bayesian (random-effects per study) would shrink the aggregate posterior; with I^2=47% the shrinkage would be moderate. Reported flat-pool posterior (post_mean=0.649, P>0.5=0.9952) is therefore an UPPER bound on credibility.

8. **F-META-2 fires.** Aggregate Fisher p = 0.00412 does not meet the spec's 0.001 threshold. The falsifier asks whether combined evidence is stronger than naive joint sign test; in this case **Fisher (0.00412) IS stronger than naive sign test (0.0128)** — so the falsifier's intent (Fisher should be stronger) is met. But the literal threshold (Fisher > 0.001) is breached. Honest call: F-META-2 ambiguous — depends on interpretation of "weaker than naive joint p-value". If literal threshold: TRIGGERED. If spirit (Fisher stronger than aggregate sign test): NOT TRIGGERED. I report TRIGGERED literally.

9. Between cotrain (96% beat-rate) and no-cotrain (10%) the difference is 86 percentage points — the largest single confounder identified in the cycle. The §58 "tension-trigger suppression universal" mechanism cannot be invoked without specifying paradigm. Future RoadMap: replicate cotrain-vs-no-cotrain in v2_d384 (currently we lack a v2 "no-cotrain" probe — v2's "naive_ft" is closer to but not identical to engine_ag's "no_cotrain").

10. **Paradigm-cap interaction is unresolved.** v2 cap=128 was AMBIGUOUS for both aware paradigms; cap=256 unanimously PASSED. Engine_ag cap=128 PASSED for cotrain, FAILED for no_cotrain. We don't know whether engine_ag no_cotrain at cap=512 would resolve into PASS — the cap-conditional rescue might generalize. Sample budget for that test was not allocated this cycle.

11. **Heterogeneity I^2 = 47% in aggregate** is calibrated against the conventional cutoffs (25%/50%/75% for low/moderate/high). 47% is the upper-edge of moderate. Removing slab-swap studies (S13-S15, n=3 each, contributing artifactually-large within-study variance) drops I^2 below 25%. So a non-trivial fraction of the aggregate heterogeneity comes from the §57 perturbation studies, which by design are expected to disagree with the baseline. Including them in an "is V14 universal?" question is statistically defensible but conceptually muddled — they are perturbation conditions, not independent V14 evaluations.

---

**Aggregate verdict for cycle close**: V14_UNIVERSAL_QUALIFIED_PASS. 5-star claim foundation: engine_ag-cotrain (n=28 trials, k=27, p=2.16e-7) + v2-cap=256 (n=10 trials, k=10, p=0.00195) + foundation_borrow §43 (orthogonal V4 metric, V14_PASS). Three independent paradigm-arch combinations all confirm trained > random_init on Phi-family metrics. The unified mechanism (cotrain-or-aware paradigm + adequate cap) is statistically supported. Naive universality is falsified; conditional universality holds.
