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
- **distinctness 잔여:** H_1280 forward error 와는 bar E 로 구별, novelty(H_1289)·habituation(H_1465)
  control-survived distinctness 도 ✅ DONE (아래 distinctness probe).

## distinctness vs NOVELTY(H_1289) · HABITUATION(H_1465) ✅ DONE (R2 follow-on)

precision-weighted surprise(p·err²)가 인접 두 신호와 control-survived DISTINCT 임을 numpy probe 로 증명
(frozen-first · 3 seeds [1468,1469,1470] · $0 CPU · p7 · deterministic 3-run byte-identical · numpy mirror **DIRECTIONAL**).

- **vs NOVELTY** = 자극 새로움(1회 recon-err, precision 무관) ⊥ surprise=precision-weighted: 같은 novelty 두 케이스에서 surprise 가 precision 으로 갈림.
- **vs HABITUATION** = 반복 자극 반응 감쇠(친숙도, error 무관) ⊥ surprise=예측오차(violation): 반복돼도 error 크면 surprise 유지.

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **N1 NOVELTY-IDENTICAL** | 두 케이스 novelty 동일 | \|0.5055−0.5055\|=**0.0000** | ≤0.01 | ✅ |
| **N2 SURPRISE-SPLITS** | 같은 novelty, surprise 가 precision 으로 갈림 | conf 1.022 − unsure 0.256 = **0.767** | ≥0.30 | ✅ |
| **N3 ABLATION (precision OFF)** | uniform p=1 → split 소멸 | **0.0000** | ≤0.05 | ✅ |
| **H1 SURPRISE-PERSISTS** | 반복돼도 still-wrong → surprise 유지 | last/first ratio **0.977** | ≥0.85 | ✅ |
| **H2 HABITUATION-DECAYS** | 같은 반복이 habituation 응답 감쇠 | drop **0.865** | ≥0.30 | ✅ |
| **H3 SHUFFLE control** | error↔repeat-index 디코릴 → 분리 소멸 | real div 0.783 → shuffled **−0.0404** | \|div\|≤0.05 | ✅ |

**verdict: 🟢 GREEN DIRECTIONAL — 6/6 bars PASS** (numpy mirror, engine-transfer UNVERIFIED → terminal 아님).
artifact: `state/1468_surprise_distinct/h1468_distinct.py` · freeze `state/verdicts/1468_surprise_distinct/H_1468_DISTINCT.txt`.

정직(c9): N1/N3 SATURATED existence-proof(novelty byte-identical, ablation split 정확히 0.000) — p·err² 는 designed 스칼라 법칙(학습된 net 아님), discriminator 결정적. H3 는 200-permutation 평균으로 control 의 디코릴 EXPECTED divergence 를 읽음(5-원소 단일 permutation = 고분산 추정치) — **bar frozen-first, 임계 미이동**(real 0.783 → shuffled ~0.04). SCOPE TOY: 3 seeds/스칼라 반응법칙, scale/real-corpus/learned-precision UNVERIFIED. 엔진-네이티브 재측정(.hexa via core/) = follow-on.

## follow-on (ING)

1. ~~distinctness vs novelty(H_1289)·habituation(H_1465)~~ ✅ **DONE** — 6/6 GREEN DIRECTIONAL (위 distinctness probe). 엔진-네이티브(.hexa) 재측정 follow-on.
2. **learned-precision** — 고정 precision 이 아니라 substrate 가 예측 확신을 학습해 surprise 를 조절(meta).

xref: H_1280(cerebellar forward model, distinct)·H_1289(novelty)·H_1465(habituation, 직전 게이트)·H_1462(GWS)·
`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·p7·p8·c9.
