# H_300 — n=5 state-sweep on rule 90: arc 의 single-state honest L 회수

> H_287–H_299 全 가설이 *single representative state* (대개 alternating "10101..." st=21) 만 측정. arc 의 honest L1 (state-dependence) 회수.

## 1. 동기

H_297/H_298/H_299 panel 의 모든 rule 90 measurements (n=5 Φ=19.5, n=6 Φ=4, n=7 Φ=6.5) 는 **단일 alternating state** st=21 (또는 st=85) 에서 측정됐다. 매 H 의 §honest L1/L2 는 "state-sweep deferred" 로 명시. 그러나:

- H_297 의 "n=5 Φ=19.5" 가 *최대* 인지 *평균* 인지 *최소* 인지 미상.
- rule 90 의 N-trajectory (H_299 cap=3: 0→6→4→6.5) 가 state-dependent perturbation 인지 robust trend 인지 미상.
- IIT 4.0 의 phi-structure 는 본질적으로 state-conditional — single-state 은 *structure 한 슬라이스* 만 잡는다.

H_300 가 이 가장 깊은 L1 을 회수: **n=5 의 全 32 state 에 걸쳐 rule 90 bounded Φ(cap=4) 분포 측정**.

## 2. 가설

**H1 (STATE-INVARIANT-NONZERO)**: n=5 rule 90 의 32 states 중 ≥80% (i.e. ≥26 states) 에서 bounded Φ(cap=4) > 1.0 — rule 90 통합이 alt-state st=21 의 특이성이 아니라 robust state-property.

**H2 (DISTRIBUTION-PROFILE)**: max ≥ 15, mean ≥ 5, min = 0 (rare/all-zero state 1-2개 허용) — H_297 reported 19.5 가 distribution 의 *상위 1/3 안* 에 있어야 single-state 보고가 misleading 하지 않음을 입증.

## 3. 측정 방법 (HEXAD/IIT4/lib + stdlib · g61)

- `eca_tpm(90, 5)` 한 번 빌드, 32 states 全 sweep.
- `big_phi_bounded(tpm, 5, st, 4)` for st ∈ {0..31}.
- distribution stat 계산 (min/max/mean/median/p25/p75/count_above_1).

## 4. 사전등록 falsifier (frozen 2026-05-26, before measure)

- **F300.1 STATE-INVARIANT-NONZERO (HEADLINE)**: ≥80% (26+/32) states 에서 rule 90 n=5 cap=4 Φ > 1.0.
- **F300.2 ALT-STATE-NOT-OUTLIER**: alt-state st=21 의 Φ 값 ≤ p90 (max 10% 안에 들면 single-state 보고가 inflated outlier 였다는 뜻 — 그 경우 H_297 finding *상한* 으로 honest 분류).
- **F300.3 DISTRIBUTION-PROFILE**: max ≥ 15 AND mean ≥ 5.
- **F300.4 ANCHOR-STATES-NONEMPTY**: 32 states 중 ≥1 개 Φ=0 (전체-0 또는 전체-1 state 가 rule 90 fixed-point — 통합 0 자명 기대).
- **F300.5 BOUND**: 모든 32 값 ≥ 0.
- **F300.6 DETERMINISM**: st=21 재실행 byte-identical (H_297 값 19.5 와 일치).

## 5. 비용 / scope

- $0 mac-local · hexa-only · LLM none · NO GPU.
- 32 calls × n=5 cap=4 (~5s/call 추정, H_297 ensemble 32-state 전체 ~수초) = ~3-5 min wall.
- 결정성: deterministic 산술 한 호출당.

## 6. 가능한 결과

| 시나리오 | 의미 |
|---|---|
| H1 PASS + H2 PASS | rule 90 통합 = robust state-property, H_297 single-state 보고 representative |
| H1 PASS + H2 FAIL | alt-state st=21 은 outlier-high; H_297 19.5 = 상한 (mean 은 더 낮음) |
| H1 FAIL + H2 PASS | rule 90 통합 state-fragile, alt-state 자체는 mid-distribution |
| H1 FAIL + H2 FAIL | rule 90 통합 state-fragile + alt-state 가 outlier-high → arc 전체 single-state finding 약화 |

## 7. honest limits / C3

1. **L1 bounded cap=4**: lower bound, magnitude 상대 비교만 robust.
2. **L2 32 states full sweep**: state-deferred L 의 *유일한* 정면 회수.
3. **L3 single rule (90)**: rule 60/110/30 등의 state-distribution 은 deferred.
4. **L4 single N (=5)**: n=6/n=7 state-sweep 은 compute-cost-prohibitive (이미 H_298 ensemble 이 그 N 에서 cap=4 wall budget 초과).
5. **L5 ECA proxy**: toy substrate fact.
6. **L6 verdict tier**: 🟢 SUPPORTED-NUMERICAL.
7. **L7 if H2 FAIL**: H_297 19.5 가 outlier 라도 *binary classification* (>0) 는 distribution-wide invariant 일 확률이 높음 — arc 의 verdict 핵심은 magnitude 가 아니라 binary.

## 8. 폐쇄 기준

F300.1–F300.6 全 결판 → terminal close. partial 일 경우 honest 분류.

## 9. 산출물

- `state/h300_n5_state_sweep_rule90_2026_05_26/run_h300.hexa`
- `state/h300_n5_state_sweep_rule90_2026_05_26/result.json` (32-state Phi values + dist stats)
- `state/h300_n5_state_sweep_rule90_2026_05_26/run.log`

## 10. 후속

- H_301: same sweep at n=6 (state-cost 64) — state-dependence at H_298 N.
- H_302: rule 60/110/30 의 n=5 state-distribution.
- H_303: rule 90 state-conditional Φ-structure (IIT 4.0 distinctions/relations).
