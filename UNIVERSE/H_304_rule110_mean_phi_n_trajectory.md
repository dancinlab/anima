# H_304 — rule 110 mean-Phi N-trajectory: H_303 의 alt outlier-low 보정

> H_303 (cycle#41): rule 110 alt-state st=21 IS outlier-low. arc 의 H_298 rule 110 N-trajectory (7.66 → 17.7 → 9.5 → defer) 가 understated. H_304 가 mean-Phi 기반 진짜 N-trajectory 추출.

## 1. 동기

H_303 의 가장 강한 negative: rule 110 의 single alt-state st=21 Φ(n=5 cap=4)=17.694 는 distribution 의 **outlier-low** (< p25 = 20.88). distribution mean=27.07, median=25.62 → arc 단일 state 보고가 **35-43% 과소표현**.

H_298 panel for rule 110:
- n=4 exact (st=5) = 7.66
- n=5 bounded (st=21) = 17.694
- n=6 bounded (st=21) = 9.532

이 N-trajectory 가 단순 alt-bias 일 가능성 — 진짜 mean-Phi trajectory 가 다를 수 있다.

## 2. 가설

**H1 (RULE-110-ALT-UNDERSTATES)**: rule 110 mean-Φ 가 alt-state Φ 보다 *모든 N* 에서 상당히 (≥25%) 큼.

**H2 (MEAN-N-TRAJECTORY)**: mean-Φ 의 N-trajectory (n=4→5→6) 가 alt-state trajectory 와 다른 모양 — 단조 증가 또는 plateau, "dip at n=6" 패턴 없어짐.

**H3 (RULE-110-MEAN-AT-N5-FROM-H301)**: H_301 의 sweep stats 중 mean=27.07 + median=25.62 정합 (재측정 없이 cite).

## 3. 측정 방법

- (n=4) eca_tpm(110, 4) + 16 states × cap=3 (n-1 = near-exact) ensemble
- (n=5) cite H_301 mean=27.07 (32 states cap=4) — already correct (sorted-array, bug-free)
- (n=6) eca_tpm(110, 6) + 64 states × cap=3 lower bound ensemble (cost manageable)
- compute alt-state single value at each N too (st=5 for n=4, st=21 for n=5/6) for comparison.

## 4. 사전등록 falsifier

- **F304.1 RULE-110-N4-ALT-VS-MEAN**: rule 110 n=4 mean (16-state cap=3 ensemble) > alt-state value 7.66 (or close-to-7.66 cap=3 measurement) by ≥25%.
- **F304.2 RULE-110-N6-ALT-VS-MEAN**: rule 110 n=6 mean (64-state cap=3 ensemble) > alt-state st=21 cap=3 value by ≥25%.
- **F304.3 MEAN-TRAJECTORY-NOT-DIPPING**: mean-Φ N-trajectory n=4→5→6 도 H_298 의 17.7→9.5 dip 패턴 보이는지. (FAIL = dip 유지; PASS = dip 없어짐, 단조 증가).
- **F304.4 H301-MEAN-CITE**: H_301 rule 110 n=5 mean=27.07 정합 (단순 cite 검증, sanity check).
- **F304.5 ALT-AT-N4-N6-RECOMPUTE**: alt-state at n=4 st=5 + alt-state at n=6 st=21 재측정.
- **F304.6 BOUND**: 全 측정값 ≥ 0.

## 5. 비용

- $0 mac-local · n=4 cap=3 16 calls (fast) + n=6 cap=3 64 calls (~5-10min) + alt-state spot checks.

## 6. 가능한 결과

| 시나리오 | 의미 |
|---|---|
| 全 F304 PASS | rule 110 N-trajectory mean-based 가 진짜 representative, arc N-trajectory 정정 필요 |
| F304.3 FAIL | dip 패턴은 mean 에서도 유지 — rule 110 의 *진짜* N-trajectory 특성 |
| F304.1/2 FAIL | alt-state 가 mean 근처 — H_303 outlier finding rule 110 specific case-by-case |

## 7. honest limits

1. **L1 cap mix**: n=4 cap=3 (n-1) 과 n=5 cap=4 (n-1) 과 n=6 cap=3 (n-3) 는 cap 정밀도 다름. magnitude 직접 비교는 cap-conditional, binary 패턴 (mean vs alt) 만 robust.
2. **L2 n=7 deferred**: cap=3 n=7 ensemble (128 states) 는 wall budget 초과 가능, 미측정.
3. **L3 single rule (110)**: 다른 rule (30, 60, 90) 의 mean-N-trajectory 는 deferred.
4. **L4 ECA proxy**.
5. **L5 🟢 SUPPORTED-NUMERICAL tier**.

## 8. 폐쇄

F304.1-6 결판 → terminal close.

## 9. 산출물

- `state/h304_rule110_mean_phi_n_trajectory_2026_05_26/run_h304.hexa`
- `state/h304_rule110_mean_phi_n_trajectory_2026_05_26/result.json`
- `state/h304_rule110_mean_phi_n_trajectory_2026_05_26/run.log`

## 10. 후속

- H_305: 다른 rule (30, 60, 90) 의 mean-N-trajectory.
- H_306: rule 110 의 max-Phi N-trajectory (단일 representative 가 아닌 *최대* representative).
