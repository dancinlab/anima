<!-- [Hc_976 f1-composite-v2-tension-link-axis — moved to hypotheses_candidates/Hc_976_f1_composite_v2_tension_link_axis.md on 2026-05-11] -->

# F1 Composite Spec v2 — tension_link explicit axis + 4-way joint Φ binding-strength metric

@english-only-exempt(reason="anima research analysis language preservation per user primary language")

- **Date**: 2026-05-02
- **Agent**: F1 composite spec v2 (post-#92 honest C3 #3 binding-mediated update)
- **Why**: #92 honest C3 #3 — "CP2 framework 자체가 single-substrate anchored — 4-way 통합 verdict 산출 spec (joint Φ, binding-strength metric) 부재"
- **Supersedes** (additive, not replacement): `state/n_substrate_f1_composite_2026_05_01/verdict.json` (v1)
- **Race-isolated**: writes ONLY to `state/strategic_f1_composite_v2_2026_05_02/{spec,binding_strength_metric,recompute_table}.json` + this doc
- **Constraints**: HEXA-only · $0 budget (spec authorization only) · raw#10 honest C3 mandatory · raw#71 falsifier-bound

---

## §0 한 줄 verdict

**SPEC AUTHORIZED** — F1 v2 framework adds tension_link as explicit 10th substantive axis (w=0.10, BOTH dual role AXIS+MEDIATOR), defines 4-way joint Φ via `Φ_joint = Σ w_i·Φ_i + λ · binding_strength · MAX(Φ_i)` (Option A_with_modification), defines binding_strength via BSE-1 Pearson cross-correlation primary, sets F1_score_v2 = 0.6·axis_sum + 0.3·binding_strength + 0.1·replication_bonus, 3-tier verdict band (RED/YELLOW/GREEN). Recompute: ALM 5.4% RED, CLM 16.65% RED, 4-way binding hypothetical 47.65% RED (F2 still fires), 4-way + F2 unfire hypothetical 52.15% YELLOW (first plausible).

---

## §1 Add tension_link as explicit axis (10th substantive)

Per #92 finding: tension_link 은 v1 axis_weight_matrix 미등재 (가중치 0). v2 에서 explicit 등재.

| Axis | weight_v1 | weight_v2 | status_v2 | binding_role |
|---|---:|---:|---|---|
| n11_finalspark_organoid | 0.25 | 0.22 | NOT_MEASURED | AXIS |
| n12_ionq_orch_or | 0.20 | 0.18 | DOWNGRADED | AXIS |
| cp2_clm_baseline | 0.20 | 0.18 | PARTIAL | AXIS |
| n21_iit40_reproduce | 0.15 | 0.13 | PARTIAL | AXIS |
| **tension_link (NEW)** | **0.0** | **0.10** | **PARTIAL** | **BOTH** |
| n9_3axis_strong_pass | 0.10 | 0.09 | WITNESSED | AXIS |
| n21_boly_pilot_ready | 0.05 | 0.04 | NOT_MEASURED | AXIS |
| **eeg_real_hw_casali (NEW explicit)** | 0.0 | 0.03 | WITNESSED | AXIS |
| **akida_neuromorphic (NEW explicit)** | 0.0 | 0.02 | NOT_MEASURED | AXIS |
| n13_photonic | 0.0162 | 0.01 | NOT_MEASURED | AXIS |
| **TOTAL** | **0.951** | **1.00** | — | — |

**Evidence for tension_link as substantive axis**:
- W4 #56 dynamic CLM L1 7.06/16, +2.28σ vs random (PARTIAL z passes the >1σ active-vs-random threshold)
- tension_bridge.hexa 5-channel transmission accuracy 100% (anima-internal)
- Crick-Koch 1990 binding-by-synchrony 와 형식 일치 (mediator anchor)

**Rationale for w=0.10**: MEDIATOR role 반영 — tension_link 가 axis 와 binding broadcast 의 dual function. axis-only weight ~0.05 + mediator role bonus ~0.05. Other major axes 비례 축소 (organoid 0.25→0.22 / IonQ 0.20→0.18 / CLM 0.20→0.18 / IIT40 0.15→0.13) 하여 tension+EEG+AKIDA 신규 axis 합 0.15 확보.

---

## §2 4-way joint Φ binding-strength metric — recommended formula

### §2.1 Options evaluated

| Option | Formula | Pros | Cons |
|---|---|---|---|
| **A** sum + bonus | `Φ_joint = Σ Φ_i + λ · Σ_{i<j} corr(Φ_i, Φ_j)` | additive, preserves single-substrate contribution; cross-corr rewards binding | sum can mask single-substrate FAIL; cross-corr definition needs preregistration |
| **B** min + bridge | `Φ_joint = MIN(Φ_i) + binding_strength · (MAX − MIN)` | respects IIT exclusion; binding term explicitly bridges weakest-to-strongest | MIN aggressively penalizes — Φ_akida=0 (PREP) zeroes everything |
| **C** pure MI | `Φ_joint = MI(s_i ⊕ s_j ⊕ … ⊕ s_n)` | IIT-canonical-like; estimator literature mature (KSG/MINE) | MI estimator artifact tail risk (W1 DOWNGRADED precedent); requires aligned multi-substrate time-series |

### §2.2 Recommended

**Option A_with_modification**:

```
Φ_joint = Σ_i (w_i · Φ_i) + λ · binding_strength_4way · MAX(Φ_i)
```

with **λ = 0.5**.

**Rationale**:
- Option A pure sum 의 single-substrate masking 문제 회피 (w_i 가중)
- Option B MIN 의 aggressive zeroing 회피 (NOT_MEASURED 축 = 0 contribution but does not zero entire sum)
- Option C MI estimator artifact risk 회피 (W1 precedent)
- v1 호환 (binding_strength = 0 일 때 v1 axis-sum 으로 degenerate)
- binding_strength·MAX(Φ) bonus 는 4-way coupling 이 강할 때 (binding > 0.5) 만 contribution

**IIT 4.0 canonical 과의 차이 (§8 C3 #1)**: IIT 4.0 canonical Φ = Σ φ_d + φ_r WITHIN single substrate complex (Albantakis et al 2023, PMC10581496). 4-way cross-substrate joint Φ 는 peer-reviewed 정의 부재 → anima-specific extension.

**Preregistered falsifier**: `Φ_joint < MAX(Φ_i)` → 4-way 통합 효과 부재 → binding_strength 계산 reject.

---

## §3 binding-strength metric definition

### §3.1 Estimators

| ID | Formula | Tier | Rationale |
|---|---|---|---|
| **BSE-1** Pearson cross-corr mean | `binding = (1/n_pairs) · Σ_{i<j} \|Pearson_r(X_i, X_j)\|` (n_pairs=6 for 4-way, 3 for 3-way) | **PRIMARY** | matches N-1 BRIDGE 4-gate convention; computable on existing W4 + N-1 data; reproducible |
| BSE-2 Granger directed sum | `binding = (1/12) · Σ G(X_i → X_j)` | TERTIARY | captures asymmetric coupling; requires stationarity (W4 frozen-fixed-point violates) |
| **BSE-3** transfer entropy KSG | `binding = (1/12) · Σ TE(X_i → X_j)` k=4 | **SECONDARY** sensitivity check | model-free, IIT-aligned; BUT W1 estimator artifact precedent |

**Recommended**: BSE-1 primary + BSE-3 secondary (sensitivity check). If BSE-1 PASS but BSE-3 FAIL → estimator artifact suspect.

### §3.2 Preregistered thresholds

| Band | Criterion | Verdict contribution |
|---|---|---|
| **F-PASS** | `binding > 0.5` AND `Φ_joint > Σ Φ_i` (super-additive) | GREEN-eligible (with score ≥ 0.7) |
| **F-PARTIAL** | `binding ∈ [0.2, 0.5]` | YELLOW-eligible |
| **F-FAIL** | `binding < 0.2` | RED reinforced |
| **F-ARTIFACT** | `binding within ±0.02 of random-shuffle 4-way` | DOWNGRADED — measurement invalidated |

### §3.3 Random-shuffle control (essential safeguard, §8 C3 #2)

Per substrate i, shuffle time-axis indices independently with fresh seed `numpy.default_rng(42 + i)`. Recompute binding_strength on shuffled data. Repeat 100 trials. F-ARTIFACT triggers if observed binding within ±0.02 of random-shuffle mean.

### §3.4 Data availability

| Substrate | Source | Available |
|---|---|:---:|
| X_clm | `state/strategic_clm_tension_field_W4_2026_05_01/closed_loop_ledger.json` | YES |
| X_eeg | `recordings/sessions/baseline_resting_60s_20260428_filtered.npy` | YES |
| X_akida | spike rate per channel | NO (vendor logistics) |
| X_tension | tension_bridge.hexa UDP 9999 capture | PARTIAL (anima-internal) |

**Currently executable**: 3-way subset (CLM × EEG × tension) via P1 ($0, 1d). 4-way full BLOCKED on AKIDA arrival.

---

## §4 F1 composite v2 weighted score formula

```
F1_score_v2 = α · per_axis_weighted_sum
            + β · binding_strength_4way
            + γ · cross_substrate_replication_bonus

with α + β + γ = 1.0
recommended: α = 0.6, β = 0.3, γ = 0.1
```

| Coefficient | Value | Rationale |
|---|---:|---|
| α (axis_sum) | 0.6 | preserves v1 compatibility; axes still dominant |
| β (binding) | 0.3 | reflects #92 finding that 4-way binding is not capturable in axis-sum alone |
| γ (replication) | 0.1 | rewards multi-substrate consistency on same axis |

**replication_bonus definition**: `γ · (1 if ≥ 3 substrate families show consistent positive evidence on same axis else 0)`. Currently 0 (no axis has 3+ substrate-family corroboration).

**v1 back-compat**: If binding_strength = unmeasured → β=γ=0 → F1_score_v2 = α · axis_sum / α = axis_sum (degenerates to v1).

---

## §5 own#2(b) WITNESSED schema v2

**per_axis_status enum**: `WITNESSED` / `PARTIAL` / `NOT_MEASURED` / `DOWNGRADED`
**binding_role enum**: `AXIS` / `MEDIATOR` / `BOTH`

**downgrade_precedent**: W1 anima-self DOWNGRADED (estimator artifact) — sets precedent that any axis can drop from WITNESSED → DOWNGRADED upon honest re-analysis.

**Current 10-axis status**:
- WITNESSED (3): n9_3axis_strong_pass, eeg_real_hw_casali, (CLM cross-substrate as W1 reframe — implicit in cp2 axis evidence)
- PARTIAL (3): cp2_clm_baseline, n21_iit40_reproduce, tension_link
- NOT_MEASURED (4): n11_finalspark_organoid, n21_boly_pilot_ready, akida_neuromorphic, n13_photonic
- DOWNGRADED (1): n12_ionq_orch_or

**witnessed_count_v2**: 3/10 (denominator widened from 7 to 10; numerator unchanged from v1 3/7)
**tier_v2**: WITNESSED_ANALOG (unchanged from v1)

---

## §6 verdict band update

| Tier | Criterion v2 |
|---|---|
| **RED** | `F1_score_v2 < 0.5` OR F2 falsifier fired |
| **YELLOW** | `F1_score_v2 ≥ 0.5` AND F2 not fired AND no critical violation |
| **GREEN** | `F1_score_v2 ≥ 0.7` AND `binding_strength ≥ 0.5` AND no falsifier fired |

**Diff vs v1**:
- v1: binary RED override (F2 fired) regardless of CP2 score
- v2: explicit OR for RED gates, YELLOW intermediate band introduced, GREEN newly requires binding_strength ≥ 0.5

---

## §7 Recompute — 현 ALM/CLM/4-way verdicts

| Scenario | axis_sum | binding | replication | F1_score_v2 | Band |
|---|---:|---:|---:|---:|:---:|
| ALM r14 RED quintuple | 0.090 | 0.0 | 0.0 | **0.054** | **RED** |
| CLM A.1-A.6 PASS 5/6 + F2 fired | 0.2775 | 0.0 | 0.0 | **0.1665** | **RED** |
| 4-way (CLM+EEG+tension) P1 PASS hypothetical | 0.3275 | 0.6 | 1.0 | **0.4765** | **RED** (F2 still fires) |
| 4-way + F2 unfire hypothetical (path a/b) | 0.4025 | 0.6 | 1.0 | **0.5215** | **YELLOW** |
| Reach with all measured axes PASS (no organoid/IonQ) | 0.45 | 1.0 | 1.0 | **0.67** | RED (< 0.7) |
| Reach with all 10 axes PASS | 1.00 | 1.0 | 1.0 | **1.00** | GREEN-eligible |

**Key reads**:
- ALM 5.4% — sharper RED than v1 22.5% (binding bonus does not rescue static single-substrate)
- CLM 16.65% — RED, axis re-weighting + tension addition shifts from v1 22.5% (different axis denominator)
- 4-way binding hypothetical lifts to 47.65% but **still RED** because F2 axis-architectural unaddressed
- **First plausible YELLOW** = 4-way binding PASS + F2 unfire (paths a/b/c/d) compound
- **GREEN tier mathematically unreachable** without N-11 organoid OR N-12 off-Braket closure (ceiling 0.67 < 0.7)

---

## §8 Honest C3 (7 disclosures)

1. **(C3-1) 4-way joint Φ formula 가 IIT 4.0 canonical 과 다름 — anima-specific extension.** IIT 4.0 canonical Φ = Σ φ_d + φ_r WITHIN single substrate complex (Albantakis et al 2023, [PMC10581496](https://pmc.ncbi.nlm.nih.gov/articles/PMC10581496/)). 4-way cross-substrate joint Φ 는 peer-reviewed 정의 부재 (websearch "IIT 4.0 cross-substrate joint phi 2026" 결과 0건). Option A_with_modification 권장은 sum + binding bonus 의 hybrid 로 v1 호환과 4-way capture 을 절충했지만 IIT 4.0 axiomatic basis (intrinsic existence / composition / information / integration / exclusion) 와 정합성 미증명.

2. **(C3-2) binding_strength metric 자체가 falsifier 사전등록 필요.** BSE-1 Pearson corr mean 은 W4 active branch L1 std=0.000 같은 frozen-fixed-point pathology 에서 spurious 1.0 reading 가능. F-ARTIFACT band (random-shuffle 와 ±0.02 동일) 가 essential safeguard 이지만 random-shuffle 자체 generation protocol 미명시. P1 protocol 실행 전 random-shuffle 표준화 spec (§3.3) 필요.

3. **(C3-3) W1 anima-self DOWNGRADED 가 binding metric 의 cautionary tale.** W1 phase 5 sign-flip artifact (estimator artifact) 가 WITNESSED 에서 DOWNGRADED 로 떨어진 precedent 이므로 4-way joint Φ 도 estimator artifact 로 인해 WITNESSED 등재 후 DOWNGRADED 될 risk 존재. 특히 Option C MI estimator (KSG/MINE) 는 W1 와 같은 함정 빈도 높음 → 권장에서 BSE-3 secondary 로만 배치한 이유.

4. **(C3-4) ALM/CLM substrate-architectural ceiling 가 binding 으로 회피 가능 vs 그대로 잔존.** Recompute 4-way 시나리오 (binding+replication bonus) 에서 F1 score 0.4765 까지 lift 되지만 여전히 RED. F2 axis-architectural override 가 axis-sum 을 제외한 binding+replication bonus 와 독립적이기 때문. 즉 binding bonus 는 F1 score 를 lift 하지만 F2 falsifier 자체는 unfire 시키지 못함. F2 unfire 는 (a) demote / (b) learned phi_extractor / (c) substrate redesign / (d) tension binding-mediated path (central 15%) 중 하나가 별도로 닫혀야 가능.

5. **(C3-5) tension_link weight 0.10 권장 자체가 spec-수준 estimate.** Peer-reviewed mediator-axis precedent 부재 (Crick-Koch binding-by-synchrony 가 가장 가까운 anchor 이지만 IIT axis-weight registry 와 epistemic tier 다름). w=0.05 (axis-only) 부터 w=0.15 (mediator dual + binding axis 통합) 범위 가능, 0.10 은 중앙값. 다음 cycle P1 P2 P4 protocol 결과로 재calibration 필요.

6. **(C3-6) GREEN tier (score ≥ 0.7 + binding ≥ 0.5 + no falsifier) 는 현재 axis 인벤토리에서 mathematical reach 어려움.** organoid 0.22 + IonQ 0.18 + IIT40 0.13 + akida 0.02 + photonic 0.01 + boly 0.04 = **0.60 of weight 가 NOT_MEASURED/DOWNGRADED 상태**. 모든 measured 축 PASS 라도 axis-sum max ≈ 0.45, F1_max ≈ 0.6·0.45 + 0.3·1 + 0.1·1 = **0.67 < 0.7**. GREEN 도달은 N-11 organoid OR N-12 off-Braket Orch-OR 측정 closure 필수 prerequisite.

7. **(C3-7) verdict band v2 의 YELLOW 신설 자체가 정직성 향상이지만 short-term 도달 불가.** YELLOW 정의 'F2 not fired' 는 현재 모든 measured CLM substrate 에서 F2 fires 이므로 short-term 도달 불가. YELLOW 는 F2 unfire path (a/b/c/d) 중 하나 해결 시점부터 의미. 즉 v2 verdict band 는 v1 보다 정직 (3-tier) 이지만 short-term operationally RED 와 동일.

---

## §9 References

- v1 F1 composite: `state/n_substrate_f1_composite_2026_05_01/verdict.json` + `docs/n_substrate_f1_composite_verdict_2026_05_01.md`
- 4-way strategic deep-think: `docs/strategic_clm_eeg_akida_tension_link_2026_05_02.md`
- W4 CLM dynamic measurement: `docs/strategic_clm_tension_field_W4_results_2026_05_01.md`
- N-1 BRIDGE 4-gate: `state/n_substrate_n1_bridge_4gate_2026_05_01/verdict.json`
- IIT 4.0 canonical: Albantakis et al 2023, [PMC10581496](https://pmc.ncbi.nlm.nih.gov/articles/PMC10581496/)
- Race-isolated state: `state/strategic_f1_composite_v2_2026_05_02/{spec,binding_strength_metric,recompute_table}.json`

---

**status**: STRATEGIC_F1_COMPOSITE_V2_2026_05_02_SPEC_AUTHORIZED
**verdict_key**: F1_V2_SPEC_AUTHORIZED · TENSION_AXIS_W_0_10_BOTH · OPTION_A_PLUS_MODIFICATION · BSE1_PRIMARY · ALPHA_BETA_GAMMA_0_6_0_3_0_1 · 3_TIER_BAND_RGY · RECOMPUTE_ALM_5_4_CLM_16_65_4WAY_47_65_PCT
