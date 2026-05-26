# H_301 — n=5 state-sweep extended to rule 60·110·30: H_300 의 L2 회수

> H_300 (cycle#38) §honest L2: "rule 60/110/30 state-distribution deferred". H_301 가 같은 32-state sweep 을 다른 통합 rule 에도 확장 — arc 의 single-state methodology 가 *모든 panel rule* 에 대해 정당화되는지.

## 1. 동기

H_300 closed rule 90 의 state-dependence 정밀: distribution = 3 distinct values {19.0, 19.5, 27.5}, alt-state st=21 Φ=19.5 = **median**. 그러나:

- rule 60·110·30 (panel 의 다른 *통합* rules) state-distribution 미상.
- H_297 의 single-state 보고가 rule 90 에서는 median 이지만, *다른 rule 들에서도* median 인지? Cherry-pick 아닌 fair 인지?
- 분포의 *shape* (몇 개 distinct values, lattice-symmetry, parity-correlation) 가 rule 별로 어떻게 다른지 — IIT 4.0 phi-structure 의 rule-conditional 분포 결과 첫 정면 검정.

H_301 가 rule 60·110·30 각각에 같은 32-state sweep 적용해서 H_300 methodology 가 generalize 되는지 확인.

## 2. 가설

**H1 (ALL-RULES-STATE-INVARIANT)**: rule 60·110·30 각각, 32 states 중 ≥80% (≥26) 에서 bounded Φ(cap=4) > 1.0.

**H2 (ALT-STATE-FAIR-FOR-ALL)**: 각 rule 에 대해 alt-state st=21 의 Φ 값이 distribution 의 median (p50) ± 25% 범위 안 — *모든 panel rule* 에서 single-state methodology 가 fair representative.

**H3 (DISTRIBUTION-VARIETY)**: rule 60·110·30 의 distinct value 개수가 H_300 rule 90 의 3 와 일치 OR 다른 패턴이 나오면 각 rule 의 symmetry 그룹이 다름을 시사.

## 3. 측정 방법

- `eca_tpm(rule, 5)` for rule ∈ {60, 110, 30}.
- `big_phi_bounded(tpm, 5, st, 4)` for st ∈ {0..31}.
- distribution stats: min/max/mean/median/p25/p75 + distinct-value count.

## 4. 사전등록 falsifier (frozen 2026-05-26)

- **F301.1 STATE-INVARIANT-NONZERO-60**: rule 60, ≥26/32 states Φ > 1.0.
- **F301.2 STATE-INVARIANT-NONZERO-110**: rule 110, ≥26/32 states Φ > 1.0.
- **F301.3 STATE-INVARIANT-NONZERO-30**: rule 30, ≥26/32 states Φ > 1.0.
- **F301.4 ALT-STATE-FAIR-60**: rule 60, alt-state st=21 Φ ∈ [p25, p75].
- **F301.5 ALT-STATE-FAIR-110**: rule 110, alt-state st=21 Φ ∈ [p25, p75].
- **F301.6 ALT-STATE-FAIR-30**: rule 30, alt-state st=21 Φ ∈ [p25, p75].
- **F301.7 BOUND**: 모든 96 측정값 ≥ 0.
- **F301.8 DETERMINISM**: rule 60 st=21 cross-match with H_297 panel value (16.5).

## 5. 비용

- $0 mac-local · 96 calls × n=5 cap=4 ~10-15min wall 예상.
- 결정성: deterministic, full sweep.

## 6. 가능한 결과

| 시나리오 | 의미 |
|---|---|
| 全 F301.1-6 PASS | arc methodology generalize — single-state fair for all panel rules |
| 일부 F301.4-6 FAIL | alt-state 가 rule 별로 outlier-한 적이 있었음 — H_297 panel 재해석 필요 |
| 일부 F301.1-3 FAIL | 어느 rule 는 state-fragile — 통합이 alt-state 의존적 |

## 7. honest limits / C3

1. **L1 cap=4** lower bound (arc 일관).
2. **L2 single N**, rule 90 외 3 rules.
3. **L3** rule 0/204/255/51 (anchors) sweep 은 deferred — H_300 anchor result (0/32 zero on rule 90) 가 nonempty 였으니 anchor rule 도 같은 패턴 예상.
4. **L4** ECA proxy.
5. **L5** 🟢 SUPPORTED-NUMERICAL tier.

## 8. 폐쇄 기준

F301.1–F301.8 全 결판 → terminal close. partial → honest 분류.

## 9. 산출물

- `state/h301_n5_state_sweep_other_rules_2026_05_26/run_h301.hexa`
- `state/h301_n5_state_sweep_other_rules_2026_05_26/result.json`
- `state/h301_n5_state_sweep_other_rules_2026_05_26/run.log`

## 10. 후속

- H_302: lattice-symmetry analytical — H_300 의 D_5 rotation 이 Φ-symmetry **아닌** observation (같은 Z_5 orbit 안 다른 Φ) 의 원인 분석. eca_tpm encoding convention 또는 bounded big-Phi 의 cut-selection bias.
- H_303: anchor rule (0/204/255/51) state-distribution — 全-0 예상 확인.
