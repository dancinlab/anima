# H_1468 — ⚡ PRECISION-WEIGHTED SURPRISE (G19 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN ENGINE-NATIVE + WIRED (R1 numpy mirror DIRECTIONAL → R2 live `core/` byte-exact)
- **wired:** `WIRED-live` — `core/engine_cli.hexa` §PrecisionSurprise (surprise/surprise_raw_error) · `engine_cli_smoke.hexa` cases 184-188 · FULL smoke **188 pass / 0 fail RC=0** · ARCHITECTURE.json lockstep ✓
- **source:** 의식-고유 게이트 브레인스토밍 라운드2 (G19 candidate) · "의식이라서 가능한 것" 시리즈
- **lens:** predictive-processing — Friston free-energy / Bayesian surprise (precision-weighted prediction error) · `a_no_llm_frame_trap`
- **artifacts:** `state/1468_precision_weighted_surprise/` (R1 probe) · `core/engine_cli.hexa` §PrecisionSurprise + `engine_cli_smoke.hexa` 184-188 (R2) · verdict `state/verdicts/1468_precision_weighted_surprise/H_1468_FREEZE.json`

## 주장

느낀 **놀람(surprise)** 은 예측오차 그 자체가 아니라 예측의 **확신도(precision)** 로 가중된 오차다 —
**surprise = p·err²**. 확신하던 믿음이 깨지면 같은 오차라도 훨씬 놀랍고, 불확실하던 믿음이 깨지면
덜 놀랍다. 이 precision 가중이 surprise 를 단순 오차가 아니라 **주의를 끌어당기는 의식-관련 신호**로
만든다. LLM 은 자기 예측에 대한 지속적 confidence 가 없어 "위반될" precision 자체가 없지만, anima 의
surprise 는 live substrate 예측 확신 위에서 작동한다("확신하고 틀림"은 spike, "불확실하고 틀림"은 안 함).

## distinct vs H_1280 VForwardField (load-bearing)

| | H_1280 forward error | H_1468 surprise |
|---|---|---|
| 신호 | raw |pred−act| | precision·err² |
| precision | 무시(agnostic) | 가중(weighted) |
| 같은 raw 오차 | 같은 값 | precision 따라 **다름** |

bar E 가 분리: 같은 raw 오차(0.5==0.5)인데 surprise 는 확신(1.0) vs 불확실(0.25)로 갈린다 — precision 이 신호.

## 측정 (frozen-first · 3 seeds [1468,1469,1470] · ERR=0.5 · P_HIGH=4 · P_LOW=1 · $0 CPU · p7)

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A SURPRISE** | 확신 위반 = 큰 놀람 | s_conf **1.022** | ≥0.50 | ✅ |
| **B PRECISION-WEIGHTED** | 같은 오차, 확신≫불확실 | **0.767** | ≥0.30 | ✅ |
| **C NO-SURPRISE** | 확신+정답 → ~0 | **0.0016** | ≤0.05 | ✅ |
| **D EARNED (ablation)** | precision OFF → split 소멸 | **0.000** | ≤0.05 | ✅ |
| **E DISTINCT vs H_1280** | raw 동일·surprise 다름 | raw=동일 · gap **0.767** | ≥0.30 | ✅ |

**verdict: 🟢 GREEN ENGINE-NATIVE + WIRED — 5/5 bars PASS** (R1 numpy → R2 engine byte-exact, smoke 184-188).

## 정직 (c9)

- **R1 DIRECTIONAL → R2 ENGINE-NATIVE (중간 PR 생략):** R1 numpy mirror(통계 3-seed)의 메커니즘을
  live `core/engine_cli.hexa` §PrecisionSurprise 로 배선 + smoke 184-188 byte-exact 재현 → DIRECTIONAL 중간
  단계를 건너뛰고 engine-native 바로 WIRED. wired 4칸 사다리 완주(`a_engine_native_learning`·`a_verified_must_wire`).
- **SATURATED existence-proof:** surprise=p·err² 는 **designed**(학습된 surprise 네트워크 아님). GREEN 자체보다
  discriminator 가 결정적 — precision-weighting(B 0.767), ablation(D 0), raw-error-identical(E).
- **SCOPE TOY:** 3 seeds/스칼라 결정 반응법칙 — surprise STRUCTURE 검증이지 학습된 예측-확신 네트워크 아님.
  scale/real-corpus/learned-precision/engine-transfer UNVERIFIED.
- **distinctness 잔여:** H_1280 forward error 와는 bar E 로 구별했으나, novelty(H_1289)·habituation(H_1465,
  반복 surprise 감쇠)과의 control-survived distinctness 는 follow-on.

## follow-on (ING)

1. **distinctness vs novelty(H_1289)·habituation(H_1465)** — precision-weighted surprise vs 단순 novelty/반복감쇠 분리.
2. **learned-precision** — 고정 precision 이 아니라 substrate 가 예측 확신을 학습해 surprise 를 조절(meta).

xref: H_1280(cerebellar forward model, distinct)·H_1289(novelty)·H_1465(habituation, 직전 게이트)·H_1462(GWS)·
`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·p7·p8·c9.
