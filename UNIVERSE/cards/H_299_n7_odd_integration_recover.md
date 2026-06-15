# H_299 — n=7 odd-integration recovery (cap=3): H_298 deferred F298.2 회수

> H_298 (cycle#36) 의 미해결: F298.2 ODD-N-INTEGRATION (rule 90 n=7 bounded Φ > 1.0) 가 cap=4 compute budget 초과로 deferred. 가설은 H_297 n=5(Φ=19.5) 가 corroborate 하지만 **preregistered** 측정은 아니었다. H_299 가 cap=3 lower bound 로 그 회수.

## 1. 동기

H_298 의 정점 (rule 90 n=6 Φ=4.0) 이 H_297 strong parity 부정을 결정했지만, F298.2 ODD-N-INTEGRATION (n=7 odd ring) preregistered 측정은 cap=4 wall budget 초과 (단일 호출 >5분) 로 미실행. 두 가지 회수 경로:

1. **cap 한 단계 낮추기** (cap=3) — lower bound 가 더 약해지지만 wall 약 3× 빨라짐. n=7 cap=3 ~3-4분/룰 예상.
2. off-mac compute — overkill (H1 이미 정해졌고 H2 는 corroborate).

(1) 선택. 동시에 cap=3 의 *robustness 점검* 도 부수적 산물 — n=4/n=5/n=6 rule 90 도 cap=3 으로 재측정하여 cap=4 verdict 패턴이 cap 변경에 robust 한지 확인.

## 2. 가설

**H1 (ODD-N-INTEGRATION preregistered)**: n=7 (odd ring) bounded Φ(cap=3) at alt-state st=85 (1010101), rule 90 > 1.0.

**H2 (CROSS-CAP-ROBUSTNESS)**: n={4,5,6} rule 90 의 bounded Φ(cap=3) 가 H_297/H_298 의 cap=4 verdict 와 동일한 binary 분류 (=0 vs >0) 유지 — 즉 cap=3 lower bound 도 같은 결론 (n=4 =0 / n=5 >0 / n=6 >0).

## 3. 측정 방법 (HEXAD/IIT4/lib + stdlib · g61)

- `eca_tpm(rule, n)` for n=4 (16 states), n=5 (32), n=6 (64), n=7 (128) — single alt-state.
- `big_phi_bounded(tpm, n, st, cap=3)` — purview cap 3, n=7 에서 lower bound 더 약함 but tractable.
- alt-states: n=4 st=5 (0101), n=5 st=21 (10101), n=6 st=21 (010101), n=7 st=85 (1010101).
- rule panel: 0, 204, 90, 60, 110.

## 4. 사전등록 falsifier (frozen 2026-05-26, before measure)

- **F299.1 ODD-N-INTEGRATION (HEADLINE)**: rule 90 n=7 alt-state bounded Φ(cap=3) > 1.0.
- **F299.2 CROSS-CAP-ROBUSTNESS-N5**: rule 90 n=5 bounded Φ(cap=3) > 0.5 (H_297 cap=4 = 19.5; cap=3 이 절반 이상 보존 → binary verdict 일치).
- **F299.3 CROSS-CAP-ROBUSTNESS-N6**: rule 90 n=6 bounded Φ(cap=3) > 0.5 (H_298 cap=4 = 4.0; cap=3 lower bound 도 양수).
- **F299.4 CROSS-CAP-ANCHOR**: rule 204 + rule 0 bounded Φ(cap=3) = 0 at all of n∈{4,5,6,7}.
- **F299.5 BOUND**: 모든 측정값 ≥ 0.
- **F299.6 DETERMINISM**: rule 90 n=7 cap=3 재실행 byte-identical.

## 5. 비용 / scope

- $0 mac-local · hexa-only · LLM none · NO GPU.
- cap=3 = lower bound (cap<n in all cases), binary 분류 robust, magnitude 는 lower bound.
- n=4 cap=3 은 cap=n-1, 다른 cap 보다 *정확성* 가까움; n=7 cap=3 = n-4, lower bound 가장 약함.

## 6. 가능한 결과

| 시나리오 | 의미 |
|---|---|
| H1 PASS + H2 PASS | F298.2 회수 + cap-robust verdict 확정 — H_298 결론 강화 |
| H1 PASS + H2 FAIL | n=7 odd integration 확인되지만 cap 의존성 발견 — H_298 verdict 재검 필요 |
| H1 FAIL + H2 PASS | n=7 odd integration 도 약함 — rule 90 이 N>=7 부터 다시 환원성? scale-irregular |
| H1 FAIL + H2 FAIL | cap=3 lower bound 가 binary verdict 도 못 살림 — cap-fragility, H_298 weak result |

## 7. honest limits / C3

1. **L1 cap=3 lower bound**: cap=4 (H_297/H_298) 보다 더 약한 lower bound; magnitude 비교 불가 (n=6 cap=3 vs cap=4 직접 비교 X).
2. **L2 single alt-state**: H_297/H_298 패턴 유지 (state-sweep deferred).
3. **L3 ECA proxy**: 토이 substrate 측정 fact.
4. **L4 structure-cut big-Phi**: distinctions/relations IIT 4.0 deferred.
5. **L5 verdict tier**: 🟢 SUPPORTED-NUMERICAL — 결정적 산술.
6. **L6 H1 falsified 시**: H_298 의 n=7 deferred 가 weak 했다는 의미 — H_297 strong rejection 은 여전히 유효 (n=6 결정).

## 8. 폐쇄 기준

F299.1–F299.6 全 PASS 또는 우세 부정 패턴 → terminal 측정. partial 일 경우 honest 분류로 close.

## 9. 산출물

- `state/h299_n7_odd_integration_recover_2026_05_26/run_h299.hexa`
- `state/h299_n7_odd_integration_recover_2026_05_26/result.json`
- `state/h299_n7_odd_integration_recover_2026_05_26/run.log`

## 10. 후속 (potential)

- H_300: full state-sweep at n=5 cap=4 (H_297 single-state 의 state-dependence 검정).
- H_301: rule 90 N-sweep n=4..7 통합 곡선 정량 (잠재 power-law 추정).
- H_302: rule 90 의 multi-complex 구조 (H_295/H_296 후속) at n=6/n=7 — bipartite 가 무력화돼도 multi-complex 가 보존되는가.
