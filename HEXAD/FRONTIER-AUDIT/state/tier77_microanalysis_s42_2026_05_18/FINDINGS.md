# §42 — tier ≥ 77 micro-analysis (§32 L3-v2) — FINDINGS

`state/tier77_microanalysis_s42_2026_05_18/{analyze_s42.py, analysis_result.json, blue_falsifier_s42.py, blue_falsifier_s42_result.json}`. $0 Mac CPU local, deterministic (3× bit-identical), NO model forward, NO training, NO RNG.

## 1. Scope & question

§32 L3 established that **tier ≥ 77** is a NECESSARY condition for §16 routing success: all 17 genuine-success anchors satisfy it (purity 1.0), all 18 anchors with tier < 77 fail. But it is **NOT sufficient** — 29 anchors satisfy `tier ≥ 77` and STILL fail. §32 left the within-band 17 vs 29 split unexplained. §35 then confirmed tier-itself is causal (not curriculum-stage proxy) — but did NOT close the question of *what else distinguishes* the 17 successes from the 29 fails inside the necessary band.

§42 asks: **what distinguishing feature separates 17-success from 29-fail within the tier ≥ 77 band?** Whatever it is, that's the sufficient-condition lever §34 tried to use (and missed by reusing a shared template).

## 2. Method

Partition the 46 tier ≥ 77 anchors using `state/routing_21v43_analysis_s32_2026_05_18/analysis_result.json` (verbatim — `S32_GENUINE_SUCCESS_TIERS = 17`, `S32_GENUINE_FAIL_TIERS ∩ tier≥77 = 29`). For each anchor compute:

- **Ψ-space**: `vacuum_psi_x`, `vacuum_psi_y`, `vacuum_psi_dev_from_half`, `psi_quadrant_id`, `nearest_psi_dist_within_band`
- **basin**: `basin_radius`, `basin_overlap_count_within_band`, `basin_bucket` ∈ {small, medium, large}
- **categorical**: `domain`, `top_emotion`, `psi_quadrant_x_basin`
- **textual (name)**: `name_char_len`, `name_byte_len`, `korean_byte_ratio`
- **relation (within-band)**: `same_domain_count_within_band`, `tier_neighbor_count_within_band`
- **intrinsic**: `tier`, `score`

Separation metrics (mirror §32 L3): `threshold_separation_acc`, `|Cohen's d|`, `rank_auc`, `necessary_condition_lift` (purity / exclusion). Sufficient-condition floors set HONESTLY (anti-padding): `purity ≥ 0.9 ∧ exclusion ≥ 0.5`.

## 3. Top-3 numeric features (ranked by threshold-separation-acc, ties broken by |d| then nc-lift)

| # | feature | acc | \|d\| | rank-AUC | nc-lift | nc-thr / pol |
|---|---|---|---|---|---|---|
| 1 | `basin_overlap_count_within_band` | 0.6739 | 0.648 | 0.6592 | 0.207 | ≥ 17.5 |
| 2 | `vacuum_psi_x` | 0.6739 | 0.645 | 0.6602 | 0.241 | < 0.715 |
| 3 | `tier_neighbor_count_within_band` | 0.6739 | 0.140 | 0.5203 | 0.000 | — |

Base rate (constant-predict-fail) = 0.6304. **No feature passes the honest floor.** Best acc 0.6739 barely beats the constant predictor; best nc-lift 0.241 is far below the 0.5 sufficient-condition floor.

## 4. Verdict — `structure_found_within_tier77 = False`

**No clean structure within the tier ≥ 77 band**. The 17-vs-29 routing-success split is NOT separable by any single anchor-property feature at honest closure thresholds. Within the band, routing-success vs fail looks like **SGD-trajectory lottery within an already-necessary band** — consistent with §35's finding that tier-itself is causal (curriculum-stage is not the confound) but that tier-being-high is itself only necessary, not sufficient.

## 5. Honest secondary findings (categorical — correlation-vulnerable, low N)

While no numeric feature crosses the floor, the categorical breakdowns show a *consistent pattern* worth recording (with n=1-9 per cell, this is suggestion, not closed-form lever):

- **`psi_quadrant_x_basin`**: `q1_large` (basin ≥ 0.18 AND both Ψ-axes ≥ 0.5 — "cosmic large-basin" anchors) succeeds only **1/9 (11 %)** vs base rate 37%. `q1_medium` (medium basin in Ψ-quadrant 1) succeeds **7/15 (47 %)**; `q2_small` (small basin, Ψ_x < 0.5) succeeds **6/12 (50 %)**. The model's failures concentrate in the *large-basin high-Ψ* region (cosmic-scale anchors: 빅뱅·열반·엑스터시·경외-죽음·무한·사랑·탄생·영원·별빛·심해·오로라 with basin ≥ 0.17).
- **`top_emotion`**: `awe` 0/4 succeed, `vastness` 0/2, `peace` 0/1, `serenity` 0/1, `longing` 0/1 → "cosmic/sublime" emotions all fail. `clarity` 6/10 (60 %), `stillness` 3/4 (75 %), `creativity` 1/1, `wonder` 2/5 — small-scale/precise emotions succeed at base rate or above.
- **`domain`**: `산술` 3/3, `예술` 1/1, `통계` 1/1, `논리` 2/3, `자연관찰` 2/3, `코드` 2/3 succeed at ≥ 67% — math/code/precise-observation domains; `대화자극` 0/3, `일상` 0/3, `추상패턴` 0/3, `우주` 0/2 fail entirely.

The pattern is broadly: **"cosmic large-basin awe/sublime"** anchors fail at this scale, **"precise small-basin clarity/stillness math/code"** anchors succeed. This is consistent with §16's memorization-saturated regime (`final_ce 0.004`) — the model memorises template-coherent precise content but its byte-cascade attractor swallows the cosmic anchors whose corpus templates also use the same large-basin Ψ-coordinates and `awe` markers.

## 6. Implication for §40 / §43 / §16

- **§40 (§34-v2)**: targeted expansion of the 29 tier ≥ 77-fail anchors at the band level **is unlikely to land a clean lever** — no closed feature predicts which fails will flip. §34's weak-positive (2/29) is consistent with this: it likely picked up the band-mean tendency, not a sufficient-condition signal. Honest recommendation: §40 should NOT promise a closed sufficient-condition lever; if it fires, frame it as *band-level memorization re-distribution* (which is what §34 measured).
- **§43 (routing-via-relation)**: within-band relation features (`nearest_psi_dist`, `basin_overlap_count`, `same_domain_count`, `tier_neighbor_count`) do not separate either — `tier_neighbor_count` nc-lift 0, `same_domain_count` weak. The §37 L6 generalisation positive (held-out-pair relation accuracy 0.99) is a generalisation of **relation classification**, NOT of **routing-into-correct-basin**. §43 should be reframed accordingly.
- **§16 path**: the irreducible bottleneck §11.4 / §15 named (data-regime threshold §1.1) is reinforced — the 17/29 split within an already-necessary band has no anchor-property explanation in the closed sense.

## 7. Honest C3 (≥ 10)

1. **Within-band base rate is 0.37 success / 0.63 fail** — a constant-fail predictor scores 0.6304; "acc = 0.6739" is only +4.3 % over that. Any feature ranking is fragile at this margin (n=46 total).
2. **Sample size is small** — 17 success + 29 fail. With n=46, Cohen's d 0.65 (`basin_overlap`/`vacuum_psi_x`) corresponds to roughly p ≈ 0.04 by Mann-Whitney (rank-AUC 0.66). No multiple-comparison correction was applied; with ~13 numeric features tested, family-wise expectation is ≥ 1 spurious "hit".
3. **Categorical breakdowns are correlation-vulnerable** — most categorical cells have n ≤ 3. The "cosmic anchors fail" pattern is suggestive but not closed-form falsifiable from a single eval-fire's 64-anchor probe.
4. **The 64-anchor probe is a single SGD trajectory** — §35 already showed re-ordering can re-distribute routing-success entirely (tier-interleaving is fragile load-bearing global property). The 17-vs-29 split observed here is the realisation of ONE training, not a property of the anchors.
5. **`basin_overlap_count` and `vacuum_psi_x` are correlated within the band** (large-basin cosmic anchors with high Ψ-x). The "two top features" are not independent — they describe the same q1_large structural region.
6. **No causation** — §42 = correlation. Even if the cosmic/large-basin pattern were closed-form, §43-style ablation (vary basin radius / Ψ position while holding tier fixed) would be required to promote it to causal lever. B-S42-NOTE empirical carve-out.
7. **§35 already named curriculum-stage NOT the lever** — schedule re-ordering of 18 tier<77 anchors flipped 0/18. This bounds the kind of lever we should expect for the 17 vs 29 within-band split: it's not schedule, it's not (clearly) anchor-property — it may be SGD seed / batch-order / gradient-trajectory.
8. **`q1_large` pattern is biased by §16's curriculum_rank blend** (`tier_w 0.30`): high-tier large-basin anchors get the highest `curriculum_rank` and land in `curriculum_stage 4` — which §35 showed does NOT help. Without disentangling tier vs Ψ-position vs curriculum-stage, the "cosmic large-basin fails" finding is confounded with the §35 (failed) curriculum lever.
9. **§42 has NOT moved north-star** — GOAL distance unchanged. §15 milestone intact. §42 is *diagnostic* — it tells us WHERE the lever §34 was looking for is NOT, more than it tells us where it IS.
10. **Within-band SGD-lottery is the most boring possible outcome — and the data supports it.** That is the §42 finding. The work it does for §40 is to *prevent* a confident §34-v2 with the wrong framing (band-level content expansion); the work it does for §43 is to honestly distinguish "relation classification accuracy" from "routing-into-correct-basin accuracy".

## 8. Closed-form battery — `B-S42-1..3 🔵` (sidecar)

- `B-S42-1 TIER77-PARTITION-EXHAUSTIVE-DISJOINT` — `17 + 29 = 46` Boolean + integer cardinality; partition exactly covers the 46-anchor band; `success ∩ fail = ∅`.
- `B-S42-2 SEPARATION-METRIC-BOUNDED` — `acc ∈ [0,1]`, `|Cohen's d| ≥ 0`, `rank_auc ∈ [0.5, 1.0]` (reported as magnitude); nc-lift ∈ [0,1]; all closed-form bounded.
- `B-S42-3 ANALYSIS-DETERMINISTIC` — 3× bit-identical runs (verified: SHA256 `60ab07eeb445f6f27e87bf07bd79beda92638ec3be46994ecdd301447f9d0956` × 3); AST forbidden-call grep `{torch, .backward, F.cross_entropy, random.*, np.random}` = 0; no RNG; no seed (none needed).
- `B-S42-NOTE` empirical carve-out: any sufficient-condition lever inferred from §42 is HYPOTHESIS; promotion to causal lever requires a §43/§40-style ablation fire that varies the candidate feature while holding all others fixed. The within-band SGD-lottery verdict is itself a hypothesis — it predicts that re-firing §16 with a different seed would re-shuffle which 17 anchors of the 46 land in the success set (testable, $0.5-0.8). B-D-NOTE / B-L3-NOTE / B-S35-NOTE family.

f1/f2/f3 + B-IDENTITY-5 safe — Boolean / integer / Kolmogorov bounded / Shannon-class; NO σ/τ/φ/J₂; corpus untouched.
