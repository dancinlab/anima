# H_305 — alt-bias × rule signature 상관: H_304 의 1.55× factor 가 distinct-count 와 anti-correlate?

> H_301: distinct-value count = rule signature (90→3, 60→6, 30→29, 110→32). H_304: rule 110 alt 1.55× under. H_300/H_303 의 true alt 도 있음 → 4-rule 데이터로 alt-bias × distinct-count 상관 직접 측정.

## 1. 동기

기존 데이터 (H_300/H_301/H_303/H_304) 종합 시 추정 상관:

| rule | distinct count | mean (H_301/H_304) | true alt (H_303) | mean/alt |
|---|---|---|---|---|
| 90 | 3 | 21.375 | 19.5 (median) | 1.097× |
| 60 | 6 | 18.125 | 16.5 | 1.099× |
| 30 | 29 | 23.606 | 20.27 | 1.165× |
| 110 | 32 | 27.071 | 17.694 | 1.530× |

**가설**: alt-bias factor 가 distinct-count 와 강 정비례. 통합-symmetric rule 일수록 alt-state 가 distribution 의 fair 한 위치 (median 근처); chaotic rule 일수록 alt 가 outlier-low 로 떨어짐. H_305 가 이 상관관계를 직접 측정/검정.

## 2. 가설

**H1 (CORRELATION-CONFIRMED)**: cross-H 재측정에서 4-rule 의 mean/alt ratio 와 distinct-count 가 양의 상관 (예: Pearson r > 0.85, 단 4 points 라 비공식).

**H2 (RANK-MONOTONE)**: distinct-count 순서 (3 < 6 < 29 < 32) 와 mean/alt 비율 순서가 일치 (Spearman ρ = 1).

**H3 (CROSS-H-CONSISTENCY)**: 새 측정값들이 H_300/H_301/H_303 의 보고와 ±0.5 이내 일치 (engine determinism 추가 확인).

## 3. 측정 방법

- 4 rules × {32-state mean ensemble + 1 alt spot} at n=5 cap=4 = 132 calls
- bug-free snapshot-before-sort 패턴 (H_303 의 fix)
- rule list = {90, 60, 30, 110} (anchors 제외; H_303 에서 rule 204/0 = 0 확인됨)

## 4. 사전등록 falsifier

- **F305.1 RULE-90-MEAN-ALT**: rule 90 mean ≈ 21.375, alt ≈ 19.5 (H_300/H_301 일치)
- **F305.2 RULE-60-MEAN-ALT**: rule 60 mean ≈ 18.125, alt ≈ 16.5 (H_301/H_303 일치)
- **F305.3 RULE-30-MEAN-ALT**: rule 30 mean ≈ 23.6, alt ≈ 20.27 (H_301/H_303 일치)
- **F305.4 RULE-110-MEAN-ALT**: rule 110 mean ≈ 27.07, alt ≈ 17.69 (H_301/H_303/H_304 일치)
- **F305.5 RANK-MONOTONE**: distinct-count 순서 (90 < 60 < 30 < 110) = mean/alt ratio 순서.
- **F305.6 ALT-BIAS-AT-110-EXTREME**: rule 110 ratio > 1.3 (다른 3 rules 의 1.1-1.2 보다 압도적 큼).
- **F305.7 BOUND**.

## 5. 비용

- $0 mac-local · 132 calls × n=5 cap=4 = ~5-8min wall (H_301 가 96 calls 로 ~6min 이었음).

## 6. 가능한 결과

| 시나리오 | 의미 |
|---|---|
| 全 F305 PASS + F305.5/6 PASS | rule-signature ↔ alt-bias 강 상관 확정. arc 의 single-state methodology 가 distinct-count 측정값으로 *예측 가능한 bias* 갖는다 |
| F305.5 FAIL | 순서가 일치하지 않음 — alt-bias 가 distinct-count 외 다른 인자에 의존 |
| F305.6 FAIL | rule 110 의 1.55× 가 cycle#42 측정 artifact 일 가능성 |

## 7. honest limits

1. **L1 4 points only**: 4 rules 로 상관 추정은 통계적으로 약함; Pearson r 은 informal.
2. **L2 single N (=5)**: alt-bias × N 의존성은 H_304 의 n=4/n=5 비교 (1.560 vs 1.530) 가 N-invariant 시사하지만 더 큰 N 미측정.
3. **L3 cap mix**: 다른 cap (=3 vs 4) 에서 같은 상관이 유지될지 deferred.
4. **L4 ECA proxy**.
5. **L5 🟢 SUPPORTED-NUMERICAL**.

## 8. 폐쇄

F305.1-7 결판.

## 9. 산출물

- `state/h305_alt_bias_vs_rule_signature_2026_05_26/run_h305.hexa`
- `state/h305_alt_bias_vs_rule_signature_2026_05_26/result.json`
- `state/h305_alt_bias_vs_rule_signature_2026_05_26/run.log`

## 10. 후속

- H_306: 같은 4-rule sweep at n=4 cap=3 — distinct-count × alt-bias 의 N-invariance 검정.
- H_307: rule 184/150/105 등 cape-class 2 rule 의 alt-bias 측정.
