# 약후보 7 — ENGINE-NATIVE 흡수/distinct 측정표

> 목적: 순수 브레인스토밍 R3~R6(`CATALOGUE_BRAINSTORM.md`)에서 strong distinct 0 으로 고갈 확정됐으나
> "발사 시 인접 lane 흡수"로만 **예측**되고 실측 안 된 **약/경계 후보 7개**를 engine-native probe 로 **실제 측정**.
> 측정 = `state/gate_depletion_catalogue/weak_probe.hexa` → `hexa run` (live `core/engine_cli.hexa` lane op 호출,
> 하드게이트1 충족: numpy/torch 미러 아님, `.hexa` 가 실제 엔진 op 구동 · $0 local CPU · p7 · frozen-first).
> verdict 원문 = `state/verdicts/gate_depletion_catalogue/WEAK_PROBE_RUN.txt`.

## 방법 (frozen bar, c9 정직)

각 후보마다:
1. **흡수 예측** — 어느 기존 lane 에 흡수되는지(브레인스토밍 사전등록 예측).
2. **candidate op** — 후보 고유 연산을 결정적 스칼라로 구현, presence lift(두 케이스 분리) 측정.
3. **EXISTING-op 흡수-테스트** (load-bearing) — **구조적으로 일치하는 기존 엔진 op** 를 그 후보의 *동일* 판별 자극으로 구동.
   기존 op 가 두 케이스를 분리하면(|Δ| > FLAT_BAR=0.1) ⇒ **ABSORBED**(같은 연산·다른 입력=재포장).
   기존 op 가 평평/abstain(|Δ| ≤ 0.1)이고 presence≥LIFT_BAR=0.3 이면 ⇒ **DISTINCT**(새 lane).

> ⚠️ **c9 측정 정직(중요):** 1차 작성 probe 는 기존 op 에 *동일 입력*을 먹여(예: mood 에 stateless instant affect)
> Δ=0 을 인위 유도 → 6/7 DISTINCT 인 **측정 artifact** 가 나왔다. `a_break_the_wall` type-(a) 측정결함으로 판정,
> bar 불변(frozen-first, tune-to-green 아님)으로 **EXISTING-op 을 그 후보의 변동 자극으로 구동하는 구조-일치 테스트로 교정**.
> 교정 후 7/7 ABSORBED — 억지 distinct 승격을 측정-교정으로 제거(억지 고갈도 아님: 각 흡수가 실제 엔진 op Δ 로 입증).

## 측정 결과 (engine-native, ABSORBED=7 / DISTINCT=0)

| # | 후보 | 흡수 예측 lane | candidate presence | EXISTING-op Δ | 판정 | 엔진 경로(기존 op) |
|---|------|----------------|--------------------|--------------:|------|---------------------|
| 1 | **volatility** (2차 surprise) | PrecisionSurprise H_1468 | 0.160 (<0.3) | 0.160 (>0.1) | **ABSORBED** | `surprise(precision,err)` 평균 — volatile 레짐이 1차 surprise 평균부터 이미 높음 |
| 2 | **hazard-rate** (when-timing) | TRW H_1486 / SubjTime H_1475 | 0.833 | 2.500 (>0.1) | **ABSORBED** | `subjective_time(elapsed,…)` — 경과시간=novelty-event 채널이 지속대기 분리 |
| 3 | **mood** (느린 배경정서) | Affect H_1290 / Drive H_1292 | 1.977 | 2.696 (>0.1) | **ABSORBED** | `homeo_step` leaky-integrator 를 pos/neg 히스토리로 구동 → 같은 적분 구조가 분리 |
| 4 | **effort** (비용 적분) | Drive H_1292 / DividedAttn | 1.000 | 2.128 (>0.1) | **ABSORBED** | `homeo_step` 를 지속-부하(ungrounded) 스트림으로 → deficit 적분이 cost build-up 재현 |
| 5 | **TOJ** (선후 판단) | SubjTime H_1475 / TRW H_1486 | 1.000 | 0.750 (>0.1) | **ABSORBED** | `trw_recall` tick-position 코드 — discrete-tick substrate 에서 선후=위치코드 |
| 6 | **thought-ownership** | Self H_1471 / Agency H_1474 | 1.000 | 1.000 (>0.1) | **ABSORBED** | `self_cos` — candidate op 자체가 SelfIdentity 인식 op(사고토큰 재타겟=재포장) |
| 7 | **crossmodal-binding** | Gestalt H_1491 / Qualia H_1497 | 0.800 | 1.000 (>0.1) | **ABSORBED** | `gestalt_same_group(affinity)` 에 cross-space congruence 를 affinity 로 투입 → 분리 |

**집계: ABSORBED 7 / DISTINCT 0 (of 7).**

## 결론: 🧱 고갈 강화 (DEPLETION HARDENED)

- 약후보 7개 **전부** 인접 lane 으로 흡수 — 브레인스토밍 사전등록 예측(line 227-228 "발사 시 거의 다 인접 lane 흡수")과
  **정합**. strong distinct = R2 이후 연속 0 에 더해, 약후보 7개도 engine-native 실측으로 derivative 확정.
- 각 흡수는 **(a) 같은 엔진 op 구조(적분기 homeo·position-code trw·affinity gestalt·인식 self_cos)에 다른 입력을 먹인 재포장**
  (mood/effort/TOJ/crossmodal/thought-ownership), 또는 **(b) 기존 1차 신호가 이미 그 차이를 담음**(volatility 1차 surprise 평균,
  hazard 경과시간=novelty 채널)으로 분해. 새 substrate READING 불요 ⇒ 새 lane 아님.
- **새 lane 발굴 = breadth 고갈 단단히 정박.** 추가 §섹션 배선 없음(흡수=core 변경 0, 정직 유효결과 c9).
- 이후 방향(브레인스토밍 §권고-c 와 정합): 새 lane 발굴이 아니라 **기존 lane (1) 스케일업 · (2) 엔진-네이티브 배선
  (`a_verified_must_wire`) · (3) lane 간 통합/상호작용**(depth/integration).

## 인프라 부수정정 (a_break_the_wall type-c)

측정 중 `core/engine_cli.hexa` 의 `_ci_bit` 함수가 **닫는 `}` 누락**(raw brace +1)임을 발견 — `import "core/engine_cli.hexa"`
단독 모듈이 brace 불균형으로 fresh build 시 파서 Eof 에러(캐시 히트에만 가려져 있었음, h1492 포함 모든 engine-native probe
fresh build 차단). `_ci_bit` 의 `}` 추가로 정정 → engine_cli_smoke **280/0** 유지(무회귀), 모든 engine-native probe fresh build 복구.

## 산출물

- probe: `state/gate_depletion_catalogue/weak_probe.hexa` (engine-native, live `core/engine_cli.hexa` lane op 호출)
- verdict raw: `state/verdicts/gate_depletion_catalogue/WEAK_PROBE_RUN.txt`
- core 정정: `core/engine_cli.hexa` `_ci_bit` 닫는 brace
