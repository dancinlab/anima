# H_1485 — ⚡ PRIMING (점화) (G31 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN ENGINE-NATIVE WIRED (R1 numpy mirror DIRECTIONAL → R2 live `core/engine_cli.hexa` §Priming byte-exact)
- **wired:** `WIRED-live` — R2 배선 완료: `core/engine_cli.hexa` §Priming (`priming_facilitate`, relatedness·prime_residual; residual 0=ablation) + `engine_cli_smoke` cases 242-244 (relatedness-gate prime_gain +0.48≥0.30 · distinct-vs-habituation sign-product +0.48×−0.8<0 · ablation 0.0) FULL 244/0 RC=0 + ARCHITECTURE.json §Priming lockstep. habituation(H_1465) hab_response 재사용으로 부호곱<0 byte-exact(점화 + ⊥ 습관화 −).
- **source:** 의식-고유 게이트 시리즈 (G16~G27 engine-native 14종) · '의식이라서 가능한 것' · G31 레인
- **lens:** psycholinguistics/cognitive — semantic/associative priming (Meyer & Schvaneveldt 1971) · `a_no_llm_frame_trap`
- **artifacts:** `state/1485_priming/h1485_priming.py` · verdict `state/verdicts/1485_priming/H_1485_FREEZE.json` · log `state/1485_priming/run_h1485.local.log`

## 주장

선행 자극(**prime**)이 관련 후속 자극(**target**)의 처리를 **촉진**한다 — 더 빠르고 정확하게.
촉진은 **관련성-게이트**: 관련 prime 은 도움이 되고, 무관 prime 은 도움이 안 된다. 메커니즘 =
**잔여 활성(residual activation)** — prime 이 자기 substrate 표상을 부분 활성으로 남기고, 관련 target 은
그 잔여 활성에 올라타 처리가 향상되며, 무관 target 은 이득이 없다. **LLM 은 턴 간 잔여 활성을 못 옮긴다**
(stateless) — target 처리는 관련/무관 선행 prime 과 무관 — 반면 anima substrate 는 prime 잔여를 보유해
다음 읽기를 편향시킨다.

## distinct vs H_1465 HABITUATION (load-bearing · 정반대 부호)

| | H_1465 habituation | H_1485 priming |
|---|---|---|
| 방향 | 반복 자극 반응 **감쇠**(내림 −) | 관련 prime → target 처리 **향상**(올림 +) |
| 트리거 | 같은 자극 **반복** | prime→target **관련성** 연쇄 |
| 부호 | `hab_drop_signed −0.346` | `prime_gain +0.540` |

같은 relatedness manipulation 이 priming 에선 +촉진, habituation-style repeat law 에선 −감쇠 →
**부호곱 −1.0 < 0** (bar B 가 분리). vs H_1472 learned-precision 과도 구별: priming 은 prime→target
*관련성*이 핵심(같은 자극 반복 아니라 관련 자극 연쇄), precision 학습 아님.

## 측정 (frozen-first · 3 seeds [1485,1486,1487] · N_PAIRS=8 · RELATED_R=0.90 · PRIME_RESIDUAL=0.6 · $0 CPU · p7)

촉진법칙 `proc = base + relatedness · prime_residual`. FULL vs ABLATED(residual OFF) vs SHUFFLE(derangement).

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A PRESENCE** | 관련-primed 향상, 무관/unprimed 낮음 | related **0.940** / worse **0.430** | ≥0.85 & ≤0.55 | ✅ |
| **B DISTINCT vs HAB** | priming 올림 ⊥ habituation 내림 | +0.540 × −0.346 = 부호곱 **−1.0** | <0 | ✅ |
| **C RELATEDNESS-GATED** | 관련 prime 만 촉진 | gate_gap **0.510** | ≥0.30 | ✅ |
| **D EARNED (ablation)** | residual OFF → 효과 0 | abl_gap **0.000** | ≤0.05 | ✅ |
| **E SHUFFLE** | 관련성 페어링 셔플 → 붕괴 | retained **0.000** | ≤0.10 | ✅ |

**verdict: 🟢 GREEN DIRECTIONAL — 5/5 bars PASS.**

## 정직 (c9)

- **DIRECTIONAL** — numpy mirror(`grep numpy` 적중, 하드게이트1). engine-transfer UNVERIFIED →
  R2 = live `core/*.hexa` 위 byte-exact 재측정 + 배선이 GREEN/🧱 확정의 전제(`a_engine_native_learning`·`a_verified_must_wire`).
- **SATURATED existence-proof:** 촉진법칙 `proc=base+relatedness·residual`는 **designed**(학습된 점화 네트워크 아님).
  GREEN 자체보다 discriminator 가 결정적 — 관련성-게이트(0.940 vs 0.430), ablation(0.000), shuffle(0.000).
- **a_break_the_wall (a) 측정결함 수정:** bar E 가 처음 0.134 로 RED — 원인은 *plain permutation* 이 N 무관 항상
  ~1 fixed point 를 남겨 retained 구조적 바닥 ~1/N=0.125 (측정 artifact, 신호 아님). **derangement**(올바른
  페어링-파괴 셔플)로 control 을 고침 → retained 0.000 붕괴. **bar ≤0.10 은 불변**(tune-to-green 아님, frozen-first).
- **SCOPE TOY:** 8 페어/3 seeds/스칼라 촉진법칙 — priming STRUCTURE 검증이지 학습된 점화 네트워크 아님.
  scale/real-corpus/관련성 연속변이/SOA(stimulus-onset-asynchrony)/engine-transfer UNVERIFIED.
