# H_302 — eca_tpm × big_phi_bounded 결정성 진단: F301.8 cross-H 불일치 원인 추적

> H_301 (cycle#39) §honest L1: rule 60 st=21 n=5 cap=4 이 H_297 panel 의 16.5 와 다른 18.5 측정 (delta +2.0). rule 90 은 19.5 정확히 일치. 어디서 무엇이 분기됐나?

## 1. 동기

H_297-H_301 arc 의 모든 측정은 **deterministic toy-substrate** 라고 fence 됐다. 그러나 H_301 가 cross-H rule-specific value drift (rule 60 만) 를 잡았다. 가능 원인 4가지:

1. **Engine 비결정성**: eca_tpm 또는 big_phi_bounded 가 호출 순서 의존
2. **H_297 로깅 artifact**: 16.5 라고 적힌 게 실제 측정 아닌 별도 state 또는 다른 함수
3. **stdlib upgrade**: H_297 (2026-05-26 earlier) 와 H_301 사이에 iit4_bounded 가 변경됨 (gitlog 확인)
4. **n=5 single-state st=21 정의**: H_297 의 st=5 사용처와 H_301 의 st=21 정의 mismatch

H_302 가 4 가지 모두 정면 검정. **gold standard**: rule 90 n=5 st=21 cap=4 = 19.5 (3-H 일치) 가 baseline.

## 2. 가설

**H1 (REPRO-INTRA)**: 같은 호출을 같은 binary 안에서 두 번 → byte-identical. (engine 자체 결정성)
**H2 (ORDER-INDEPENDENT)**: rule 60 → rule 90 호출 순서와 rule 90 → rule 60 순서가 같은 rule 60 값 산출.
**H3 (CROSS-H-RULE-60-ANOMALY)**: H_301 의 rule 60 n=5 st=21 cap=4 = 18.5 가 *현재 engine 의 진짜 값* 임을 확인. H_297 16.5 는 historical artifact.
**H4 (CROSS-RULE-INTEGRITY)**: rule 90 외에 다른 rule 들도 cross-H 일치하는지 — 가령 H_298 n=6 panel 의 rule 110=9.532 vs H_302 재측정.

## 3. 측정 방법

- (H1) rule 60 n=5 st=21 cap=4 호출 두 번, byte-equal 확인.
- (H2) order swap: panel A = [rule 60, rule 90], panel B = [rule 90, rule 60]. rule 60 값이 두 panel 에서 같은지.
- (H3) 다양한 (rule 60 / 다른 rule) × (st=21, st=5) × cap=3/4 grid: H_297 16.5 가 어떤 state/cap 조합에서 나오는지 brute-force 탐색.
- (H4) rule 90 / 60 / 110 / 30 각각 n=5 st=21 cap=4 재측정, H_297 panel 표와 비교.

## 4. 사전등록 falsifier

- **F302.1 REPRO-INTRA**: rule 60 n=5 st=21 cap=4 두 번 호출 byte-identical.
- **F302.2 ORDER-INDEPENDENT**: panel A 의 rule 60 값 == panel B 의 rule 60 값.
- **F302.3 RULE-90-INTEGRITY**: rule 90 n=5 st=21 cap=4 = 19.5 (H_297 ↔ H_300 일치 재확인).
- **F302.4 RULE-60-CURRENT**: rule 60 n=5 st=21 cap=4 = 18.5 (H_301 재현).
- **F302.5 H_297-16-5-LOCATION**: brute-force grid 에서 어떤 (state, cap) 가 16.5 를 산출하는지. 발견 시 PASS (artifact 위치 확인); 미발견 시 FAIL (16.5 는 측정-소스-알 수 없음).
- **F302.6 BOUND**: 全 측정값 ≥ 0.

## 5. 비용

- $0 mac-local · 빠른 진단 (~20 calls × n=5 cap=4 = ~2-3min).

## 6. 가능한 결과

| 시나리오 | 의미 |
|---|---|
| F302.1-4 PASS + F302.5 PASS | engine 결정적; H_297 의 16.5 가 grid 어딘가에서 발견 → logging artifact |
| F302.1-4 PASS + F302.5 FAIL | engine 결정적이지만 H_297 16.5 출처 미상 — 과거 버전 차이 가능성 |
| F302.1 FAIL | engine 비결정성 — 심각, arc 전체 re-verify 필요 |
| F302.2 FAIL | order-dependent — eca_tpm 또는 big_phi_bounded 에 mutable shared state |

## 7. honest limits / C3

1. **L1**: H_297 의 측정 정확한 reproduction 은 H_297 의 *binary* 가 필요. 빌드 매번 새로 하지만 stdlib 가 그 사이 변경됐을 수 있음 (`git log -- stdlib/consciousness/iit4_bounded.hexa` 따로 점검).
2. **L2**: brute-force grid 가 좁음 — H_297 의 16.5 가 다른 state 에 있을 수도 있고 다른 n 에서 나왔을 수도. F302.5 는 *유력 후보 위치* 만 검정.
3. **L3**: 🟢 SUPPORTED-NUMERICAL tier — 진단 H 도 결정적 산술.

## 8. 폐쇄

F302.1-6 결판 후 close. 정답이 무엇이든 (artifact 발견 또는 미발견) 모두 honest verdict.

## 9. 산출물

- `state/h302_engine_determinism_diagnosis_2026_05_26/run_h302.hexa`
- `state/h302_engine_determinism_diagnosis_2026_05_26/result.json`
- `state/h302_engine_determinism_diagnosis_2026_05_26/run.log`

## 10. 후속

- H_303 (if F302.2 FAIL): order-dependent engine bug 분리 + hexa-lang inbox patch.
- H_303 (otherwise): anchor rule (0/204) state-sweep + lattice-symmetry analytical (H_300 의 D_5 non-symmetry 의문 회수).
