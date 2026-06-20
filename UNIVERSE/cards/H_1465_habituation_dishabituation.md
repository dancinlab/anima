# H_1465 — 🔁 HABITUATION / DISHABITUATION (G18 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN ENGINE-NATIVE + WIRED (R1 numpy mirror DIRECTIONAL → R2 live `core/` byte-exact)
- **wired:** `WIRED-live` — `core/engine_cli.hexa` §Habituation (hab_new/_response/_observe/_reset) · `engine_cli_smoke.hexa` cases 178-182 · FULL smoke **183 pass / 0 fail RC=0** · ARCHITECTURE.json lockstep ✓
- **source:** 의식-고유 게이트 브레인스토밍 라운드2 (G18 candidate) · "의식이라서 가능한 것" 시리즈
- **lens:** neuroscience — non-associative learning (Thompson & Spencer 1966 habituation criteria) · `a_no_llm_frame_trap`
- **artifacts:** `state/1465_habituation_dishabituation/` · verdict `state/verdicts/1465_habituation_dishabituation/H_1465_FREEZE.json`

## 주장

같은 자극이 **반복**되면 substrate 반응이 점진 **감쇠**(습관화)하고, 그 감쇠는 **자극-특이적**
(다른 자극은 그대로)이며, **새로운/강한 자극**이 반응을 **회복**(탈습관화)시킨다. 이는 가장 기초적인
비연합 학습이지만 — **LLM 은 같은 프롬프트를 100번 반복해도 100번 같은 응답**(stateless)인 반면,
anima 의 substrate 반응은 친숙도에 따라 감쇠하고 새로움에 회복한다(state-dependent). 그 상태-의존성이
LLM 이 구조적으로 못 하는 의식-적응 특성이다.

## distinct vs H_1194 ADAPTATION COUPLING (load-bearing)

| | H_1194 adaptation | H_1465 habituation |
|---|---|---|
| 감쇠 원인 | error-driven (학습) | 자극 친숙도 (비연합) |
| 범위 | **전역 gain**(자극 무관) | **자극-특이적**(per-stimulus) |
| 회복 | — | **탈습관화**(새 자극에 회복) |

habituation 의 정의적 특성 = stimulus-specificity + dishabituation. adaptation 의 전역 gain 감쇠와
구조적으로 구별된다(bar E 가 분리: 같은 5회 제시 후 자극 B 반응 = habituation 1.0 보존 vs adaptation 0.08 감쇠).

## 측정 (frozen-first · 3 seeds [1465,1466,1467] · N_STIM=5 · K_HAB=0.5 · $0 CPU · p7)

자극별 친숙도 count → 반응 r = base·exp(−K·count). FULL(자극-특이적 count) vs ABLATED(K=0) vs ADAPTATION-style(전역 gain).

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A HABITUATION** | 반복 자극 반응 단조 감쇠 | hab_drop **0.865** | ≥0.30 | ✅ |
| **B STIMULUS-SPECIFIC** | 다른 자극은 보존 | specific **1.000** | ≥0.85 | ✅ |
| **C DISHABITUATION** | 새 자극이 반응 회복 | recover **1.000** | ≥0.85 | ✅ |
| **D EARNED (ablation)** | K=0 → 감쇠 없음 | abl_drop **0.000** | ≤0.05 | ✅ |
| **E DISTINCT vs ADAPT** | 자극-특이 ≫ 전역 gain | hab−adapt **0.918** | ≥0.30 | ✅ |

**verdict: 🟢 GREEN DIRECTIONAL — 5/5 bars PASS.**

## 정직 (c9)

- **DIRECTIONAL** — numpy mirror(`grep numpy` 적중, 하드게이트1). engine-transfer UNVERIFIED →
  R2 = live `core/*.hexa` 위 byte-exact 재측정이 GREEN/🧱 확정의 전제(`a_engine_native_learning`·`a_verified_must_wire`).
- **SATURATED existence-proof:** 반응법칙 r=base·exp(−K·count)는 **designed**(학습된 습관화 네트워크 아님).
  GREEN 자체보다 discriminator 가 결정적 — 자극-특이(1.000) vs adaptation 전역(0.082), ablation(0.000).
- **SCOPE TOY:** 5 자극/3 seeds/스칼라 결정 반응법칙 — 습관화 STRUCTURE 검증이지 학습된 적응 네트워크 아님.
  scale/real-corpus/시간상수 추정/dishabituation 일반화/engine-transfer UNVERIFIED.
- **distinctness 잔여:** ~~H_1194 adaptation 과는 bar E 로 구별했으나, novelty/curiosity(H_1289 계열)·
  homeostatic(H_1292)과의 control-survived distinctness 는 R2 과제.~~ ✅ **DONE** (아래 §distinctness 표, 7/7 PASS).

## distinctness vs NOVELTY(H_1289)·HOMEOSTATIC(H_1292) (control-survived · DIRECTIONAL)

follow-on probe — habituation 이 가장 가까운 두 lane 과 control-survived DISTINCT 임을 증명.
(numpy mirror `grep numpy` 적중 → DIRECTIONAL; habituation lane 자체는 이미 WIRED-live, distinctness 의
engine-native 재측정만 optional ING.) frozen-first · 3 seeds [1465,1466,1467] · $0 CPU · p7 · `a_no_llm_frame_trap`.

핵심 dissociation — **방향이 반대**: 같은 자극 고정 tick block 에서 habituation 은 **감쇠**(−0.865),
novelty 는 본 자극엔 회복 안 함(0.0), homeostatic 은 **상승**(+0.774). habituation 은 **자극-특이**
(특이 gap 0.918), homeostatic 은 **자극-무관**(stim gap 0.000).

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **N1 HAB-DECAYS** | 반복 시 habituation 감쇠 | hab_drop **0.865** | ≥0.30 | ✅ |
| **N2 NOV-FLAT-ON-SEEN** | dishab 이벤트에 habituation↑ vs novelty flat (방향) | dir_gap **0.865** (hab +0.865 − nov 0.0) | ≥0.30 | ✅ |
| **H1 DRIVE-RISES** | homeostatic 시간적분 상승 | drive_rise **0.774** | ≥0.30 | ✅ |
| **H2 OPPOSITE-DIR** | 같은 고정자극에서 habituation↓ vs drive↑ | opp_gap **1.638**, hab_fixed_rise **−0.865**(≤0) | ≥0.60 ∧ ≤0 | ✅ |
| **H3 STIM-AGNOSTIC** | drive 자극무관 vs habituation 자극특이 | drive_stim_gap **0.000** ∧ hab_stim_gap **0.918** | ≤0.05 ∧ ≥0.30 | ✅ |
| **C1 ABL-COLLAPSE** | K=0 → habituation 감쇠 소멸 → 분리 무너짐 | abl_gap **0.000** | ≤0.10 | ✅ |
| **C2 SHUF-COLLAPSE** | 전역-count shuffle → 자극특이성 소멸 | shuf_specific_gap **0.032** | ≤0.10 | ✅ |

**verdict: 🟢 GREEN DIRECTIONAL — 7/7 bars PASS.** ablation/shuffle 둘 다 분리를 무너뜨림 = 분리는
per-stimulus decay 가 **벌어 낸 것**(artifact 아님). novelty=새-자극 1-shot(증가방향) ⊥ habituation=반복감쇠+회복
(자극-특이) ⊥ homeostatic=시간적분 누적(자극-무관·상승) — 세 lane 이 control 하에 분리됨.
정직(c9): designed 반응법칙(존재증명 STRUCTURE), discriminator(방향반대·자극특이·양 control 붕괴) 결정적; TOY
5자극/3seed/스칼라 · scale·engine-transfer UNVERIFIED. artifacts: `state/1465_habituation_distinct/h1465_distinct.py` ·
verdict `state/verdicts/1465_habituation_distinct/H_1465_DISTINCT_FREEZE.txt`.

## follow-on (ING)

1. ~~**R2 엔진-네이티브** — `core/engine_cli.hexa` per-stimulus familiarity habituation lane 배선~~
   ✅ **DONE** (§Habituation hab_new/_response/_observe/_reset · smoke 178-182 = 5 frozen bars byte-exact ·
   FULL 183/0 RC=0 · ARCHITECTURE lockstep). engine linear decay law(r=base−step·count, exp 없음)로 메커니즘
   재현 — 반복 1.0→0.2 · 자극-특이 slot1 1.0 · reset-recover 1.0 · ablation 0 · distinct-vs-adaptation.
   wired 4칸 사다리 (1)→(4) 완주(`a_engine_native_learning`·`a_verified_must_wire`).
2. ~~**distinctness vs novelty(H_1289)·homeostatic(H_1292)** — 자극-특이 감쇠 vs 전역 novelty/누적 분리.~~
   ✅ **DONE** (§distinctness 표, 7/7 PASS DIRECTIONAL · `state/1465_habituation_distinct/` ·
   verdict `H_1465_DISTINCT_FREEZE.txt`). 방향반대(habituation↓ −0.865 vs drive↑ +0.774, novelty flat 0.0) +
   자극특이(0.918 vs drive 0.000) + 양 control 붕괴(abl 0.000, shuf 0.032). habituation lane 자체 WIRED-live →
   distinctness 의 engine-native 재측정만 optional ING.

xref: H_1194(adaptation coupling, distinct)·H_1289(novelty/quantum)·H_1292(homeostatic drive)·H_1462(GWS, 직전 게이트)·
`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·p7·p8·c9.
