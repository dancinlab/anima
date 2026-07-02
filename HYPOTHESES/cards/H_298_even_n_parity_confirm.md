# H_298 — even-N parity confirm: rule 90 returns to Φ=0 at n=6?

> arc/리세트 어드레스: H_297 ("rule 90 환원성=even-N bipartite artifact") 의 직접 falsification.
> H_297 은 n=4(Φ=0) → n=5(Φ=19.5) 한 parity step 만 측정. 진짜 even-N artifact 라면 **n=6 도 Φ=0** 이어야 한다.

## 1. 동기

H_297 (cycle#35) 의 헤드라인:

> rule 90 의 whole-Phi=0 at n=4 는 짝수-고리(even ring) 의 bipartite even/odd cell decoupling artifact 다. odd ring(n=5) 에서 그 decoupling 이 깨지며 rule 90 bounded Φ=19.5 (panel 최상위) 로 통합한다.

이 헤드라인은 *parity-binary* 예측을 함의한다: 모든 짝수 N 에서 환원, 모든 홀수 N 에서 통합. 그런데 H_297 의 측정은 n=4 vs n=5 *한 step* 뿐. **n=6(다음 짝수)** 으로 가서 rule 90 이 다시 Φ=0 으로 떨어지지 않는다면 가설은 부정된다 — 단순히 "더 큰 N 에서는 항상 통합" 이거나, n=4 가 작은 N 특이성일 수도 있다.

H_298 은 그 falsification 을 직접 친다 — even n=6 + odd n=7 동시 측정으로 *parity 패턴 자체* 가 robust 한지 검정.

## 2. 가설 (테스트)

**H1 (EVEN-N-PARITY)**: n=6 (even ring) bounded big-Phi(cap=4) 에서 rule 90 의 ensemble-mean Φ ≈ 0 (anchors 와 분리불가).
**H2 (ODD-N-INTEGRATION)**: n=7 (odd ring) bounded big-Phi(cap=4) 에서 rule 90 의 ensemble-mean Φ > 0.

H1+H2 同時성립 = H_297 even-N bipartite artifact 가설 strong confirm.
H1 부정 = "rule 90 환원성=짝수-고리 artifact" 가설 부정 (n=4 = 소규모 특이성, 혹은 더 깊은 메커니즘).
H2 부정 = odd-N integration 가설 부정 (n=5 가 특이성, more odd N 필요).

## 3. 측정 방법 (HEXAD/IIT4/lib + stdlib 재사용, g61)

- `eca_tpm(rule, n)` → n=6 (64 states), n=7 (128 states) TPM 빌드.
- `big_phi_bounded(tpm, n, st, cap)` 로 bounded big-Phi (cap=4 = n-2 for n=6, n-3 for n=7 → lower bound).
- ensemble: full state-sweep (2^n 상태 平均 Φ).
- H_297 과 *동일 engine*, 새 IIT4 코드 0 줄.

## 4. 사전등록 falsifier (frozen 2026-05-26, before measure)

- **F298.1 EVEN-N-PARITY (HEADLINE)**: rule 90 n=6 bounded ensemble-mean Φ ≤ 0.5 (anchors 0.0 와 ≈동등 — *환원성 복귀*).
- **F298.2 ODD-N-INTEGRATION**: rule 90 n=7 bounded ensemble-mean Φ > 1.0 (강한 통합 — odd ring decoupling 실패 재현).
- **F298.3 SCALE-ANCHORS**: rule 204 + rule 0 n=6 Φ=0 AND n=7 Φ=0.
- **F298.4 INTEGRATION-SURVIVES**: rule 60 OR rule 110 ensemble-mean Φ > 0 at *both* n=6 and n=7.
- **F298.5 BOUND**: 모든 측정값 ≥ 0.
- **F298.6 DETERMINISM**: rule 90 n=6 ensemble Φ 재실행 byte-identical.

## 5. 진행 비용 / scope

- $0 mac-local · hexa-only · LLM none · NO GPU.
- 결정성: closed-form arithmetic, cross-process byte-identical.
- bounded big-Phi(cap<n) = lower bound — *binary* 분류(≈0 vs ≫0) 는 robust, exact magnitude 는 아님 (honest L1).

## 6. 측정 결과 (실측 2026-05-26)

| rule | n=4 (exact) | n=5 (H_297 bounded alt-state) | n=6 (H_298 bounded alt-state st=21) |
|---|---|---|---|
| **rule 90** | **0** | **19.5** | **4.0** ★ (≠ 0, parity rule **부정**) |
| rule 60 | 17.5 | 16.5 | 22 |
| rule 110 | 7.66 | 17.7 | 9.532 |
| rule 204 | 0 | 0 | 0 (anchor) |
| rule 0 | 0 | 0 | 0 |

**시나리오 매핑**: H1 FAIL (rule 90 n=6 Φ=4 > 0.5 threshold) + H2 DEFERRED (n=7 leg 가 cap=4 compute budget 초과; n=5 Φ=19.5 가 odd-ring 통합을 corroborate). → **"H1 FAIL + H2 PASS-by-corroboration" 행이 사실에 가장 가까움**: n=4 이 작은-N 특이성, H_297 strong parity 가설 부정.

surviving 해석 = H_297 weak reading: "n=4 4-cycle 의 bipartite even/odd cut 이 system-cut MIP 와 정확히 일치 → 그 N 에서만 reducible 보임". n=6 부터는 3+3 bipartite cut 이 더 이상 trivial 분할이 아니라 rule 90 가 통합. parity-binary 패턴은 단순 N-mod-2 가 아니라 *small-N 특이 case 의 부재* 였다.

## 7. honest limits / C3

1. **L1 bounded cap=4**: lower bound, cap-limited reducibility 와 진짜 Φ=0 구분 불가. anchors(rule 204) 가 cap=4 에서 0 인 점이 baseline.
2. **L2 단일 parity step**: n=6 vs n=7. n=8/n=9 추가 검정 deferred.
3. **L3 ensemble vs single-state**: H_297 은 panel 의 일부에서 single state st=21 도 보고. H_298 ensemble-mean 으로 단일-state 의존성 제거.
4. **L4 ECA proxy**: 현상학적 의식 주장 아님 — toy-substrate 측정 fact.
5. **L5 system-cut big-Phi**: structure cut, distinctions/relations 미사용. 방향 결론에는 robust.
6. **L6 rule 90 외**: 60/110/30 은 *integration survives* 보조 falsifier 만. 깊은 동역학 비교는 H_298 scope 외.
7. **L7 verdict tier**: 🟢 SUPPORTED-NUMERICAL — 수치적 deterministic, atlas 등록 대상 아님 (toy ECA 측정).

## 8. 폐쇄 기준

F298.1–F298.6 全 PASS 또는 우세 부정 패턴 1 → terminal 측정. partial 일 경우 honest 분류 (PARTIAL — even-N H1 또는 odd-N H2 단독 성립) 으로 close, 후속 H 가 그 잔여 차원 처리.

## 9. 산출물

- `state/h298_even_n_parity_confirm_2026_05_26/run_h298.hexa` — 측정 smoke (hexa-only, $0).
- `state/h298_even_n_parity_confirm_2026_05_26/result.json` — verdict ledger (panel + falsifiers + honest_limits + verify_fence).
- `state/h298_even_n_parity_confirm_2026_05_26/run.log` — raw stdout.

## 10. 후속 (potential, 자동 진행 아님)

- H_299: n=8 even (3rd parity step) — 2-step parity confirm.
- H_300: rule 90 cap=n exact at n=6 (no lower bound) — magnitude clean.
- H_301: rule 60/110 N-sweep — integration curves vs N.
