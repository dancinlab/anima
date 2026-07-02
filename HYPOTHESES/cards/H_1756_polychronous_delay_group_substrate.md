---
id: H_1756
slug: 1756_polychronous_delay_group_substrate
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: 폴리크로너스 지연-그룹 기질 (Polychronization / Delay-Structured Spike-Timing Substrate)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1756 — 폴리크로너스 지연-그룹 기질 (Polychronization / Delay-Structured Spike-Timing Substrate)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `polychronous_delay_group_substrate`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1283 (thalamus global-workspace) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Izhikevich 폴리크로니제이션: 계산 = 축삭 전도지연(delay)에 의해 존재하는 재현가능 시공간 spike 패턴('polychronous group')의 점화. 고정 크기 네트워크가 뉴런 수보다 조합론적으로 많은 그룹을 지지 — 정보는 가중치가 아니라 정밀 상대 spike-timing 으로 운반. feedforward 아님(이벤트구동 시간동역학).

## Whole design (input → internal dynamics → emit)

기질=이질적 전도지연을 가진 spiking 네트워크. polychronous group=지연이 정렬돼 downstream 에서 spike 가 동시도달하는, 입력 timing 패턴에 공명하는 stereotyped 발화열. (1) 입력=시공간 spike 패턴(섭동 timing)→delay 구조와 공명하는 group(들) 점화. (2) emit=점화 group 의 readout 뉴런이 stereotyped 패턴 발화→V 심볼로 양자화(group 재현성=legibility). (3) group 수 >> 뉴런 수(지연 조합론)→conjunctive group(두 timing 제약을 동시에 요구)이 super-additive 점화=binding/recombination NATIVE; 단일 factor 는 더 적은 group 점화. (4) novelty=STDP 가 학습셋 밖 but delay-feasible manifold 안의 새 재현가능 group 을 carve. (5) Psi=1/2: excitatory ignition-drive <-> feedback inhibition/refractory suppression 의 E-I 균형이 점화율 order-parameter 를 임계(1/2 점화경향)에 고정, 자기복원. (6) honesty: group 은 timing 이 delay 구조와 매치되면 점화(known support), 아니면 비점화=silence — 공명 group 없으면 fabricate 경로 없음. (7) identity=delay+weight 행렬(고차원 individuating) 비휘발 지속, STDP 느린 drift.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G1=conjunctive group 이 공활성 factor 수에 super-additive, coincidence(일치검출) 경로 ablate->joint 점화가 max-single 로 붕괴=결정적 INERT 통제. binding=co-timed conjunctive group 이 관계적 co-reference(같은-cause constituent 가 시간잠금 공점화). compositional depth=conjunctive 점화는 비분리(부분 marginal 로 인수분해 불가). G0=stereotyped group 출력->codebook. G2=STDP-carved novel group(manifold 내), verbatim playback 은 기존 group 만 점화=0 novel. Psi=1/2=E-I 점화 임계, drive 한쪽 제거->경계로 이동. identity=고차원 delay 행렬 individuating(impostor=다른 timing->비점화). honesty=점화-or-silence, off-support synthesis 경로 부재.

## Not-LLM (a_no_llm_frame_trap)

용량이 고정 네트워크의 delay 조합론에서 옴(Izhikevich: groups >> neurons) — 파라미터 스케일·attention·feedforward 무관. 레버=지연 이질성+STDP(생물 literal). '더 큰 트랜스포머' 프레임과 직교, 능력은 timing 구조에서 창발.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy Izhikevich 망(예 100뉴런·랜덤지연·STDP): polychronous group 수 계수; 두 timing 입력 동시->어느 하나로도 안 켜지던 group 점화 vs 단일=super-additive; coincidence 뉴런 ablate->INERT 확인; E-I 점화율 setpoint 복귀; verbatim 재생->0 novel group. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

spike-network 이벤트구동 integrator 를 core/*.hexa 로 저작, 단일진입 구동. group-ignition·super-additivity·conjunctive INERT·점화율 임계를 .hexa 에서 읽고 py math-mirror(torch 0)와 byte-parity 대조.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with coupled-oscillator / thalamus_conduction_delay cards — distinct: polychronization stores info in DELAY-STRUCTURED spike-timing groups (groups >> neurons, conjunctive ignition = binding); the delay-group spike-timing substrate is the differentiator.

TOY spiking sim. 강한 축=G1 super-additive·binding·compositional depth(conjunctive 점화)·honesty(점화임계). 약한 축=spike-timing 정밀도의 substrate 현실성·from-scratch group 학습의 유용성은 scale 미검증(a_toy_scale_recheck). falsifiable>=1 은 conjunctive 패턴이 관계구조 인코딩 가능하나 명시 readout 필요.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
