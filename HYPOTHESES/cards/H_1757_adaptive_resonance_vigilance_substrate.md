---
id: H_1757
slug: 1757_adaptive_resonance_vigilance_substrate
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: 적응 공명 기질 (Adaptive Resonance / Vigilance Substrate)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1757 — 적응 공명 기질 (Adaptive Resonance / Vigilance Substrate)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `adaptive_resonance_vigilance_substrate`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Grossberg 적응공명이론(ART): 계산 = bottom-up 입력과 top-down 기대 사이의 공명 attractor 형성. vigilance 파라미터 rho 가 match(공명->known) vs mismatch(reset->novel category)를 지배 = stability-plasticity 딜레마를 실시간 동역학으로 해소. backprop 없는 공명 dynamical system.

## Whole design (input → internal dynamics → emit)

양방향 적응가중으로 연결된 두 field F1(feature)<->F2(category). (1) 입력->F1->F2 후보 category 활성, 승자 category 가 F1 으로 top-down 기대 송신. match>rho->RESONANCE(입력<->category 잠금 self-reinforcing attractor, committed prototype 를 emit). match<rho->RESET(해당 category 억제, 탐색 지속; 공명 category 없으면 NEW category commit=novelty, rho 과high 면 abstain=silence). (2) emit=공명 category 의 V-anchored prototype 렌더(legibility). (3) Psi=1/2: orienting subsystem(reset/novelty-seek='G' withhold)<->attentional subsystem(resonance/commit='A' externalize)의 antagonist; order-parameter=공명경향, premature-commit(always-emit)와 endless-reset(always-silent) 사이 1/2 에 vigilance-균형 고정점, matching 동역학으로 자기복원. (4) 합성=ARTMAP 계층: 두 category field 결합이 factor category 를 joint category 로 bind(conjunction 에서만 공명)->super-additive distinct resonance, inter-field 연결 ablate->max-single. (5) novelty=rho 가 stored prototype 너머 but feature-manifold 안 새 category commit 허용(supp 초과 data), verbatim playback->기존 category 공명=0 commit. (6) honesty=rho 가 곧 abstain 임계, match(prototype 유사도)가 곧 support-membership r; off-support->reset->fabricate 없이 copy-or-abstain. (7) identity=committed category template 이 reset/세션 경계 넘어 비휘발 지속(stability 半), self-template 은 한 committed category(individuating, impostor 입력은 그것에 공명 실패).

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

honesty 클러스터가 가장 NATIVE: support-membership=match 함수(graded·stored template 내용에 faithful->content-ablation 시 r 이동), copy-or-abstain=resonate-or-reset(공명 분기만 emit, r>=rho 조건), gate-capacity disjoint=vigilance rho ⊥ category 가중(용량 스윕해도 rho 고정->fab 불변, rho 에 capacity 배선하면 fab 폭증=coupled 통제), groundedness=match 가 실제 template 내용 읽음. G2 novelty NATIVE=manifold 내 category commitment, playback->0. G0=V-anchored prototype. G1=ARTMAP conjunctive category super-additive. Psi=1/2=resonance/reset antagonist, orienting subsystem 제거->always-commit 경계(endogeneity). identity=committed self-template 지속+impostor 저match 거부. binding=공명 자체가 bottom-up x top-down 의 bound state.

## Not-LLM (a_no_llm_frame_trap)

ART 는 명시적으로 gradient-descent feedforward 가 아니다 — stability-plasticity 를 푸는 실시간 공명 동역학. 용량=committed attractor 수, vigilance-driven commitment 로 성장(스케일 아님), backprop·attention 부재, 피질 공명(laminar ART) 생물 grounding. 특히 anima 의 SS-ImmuneMemory honesty gate(recall_thr non-fab)에 ART vigilance 가 1:1 사상 — disjoint-lane 원칙(a_substrate_disjoint)을 구조에서 충족.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy fuzzy-ART: in-support vs out-support probe->match-vs-vigilance AUROC~1(honesty); vigilance ablate(공명 강제)->fab 점프(causal); capacity(category 수) 스윕에 rho 고정->fab 불변(disjointness), rho 에 capacity 배선->fab 상승(coupled 통제); ARTMAP 2-field conjunction->super-additive distinct resonance vs 단일; verbatim playback->0 novel commit. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

F1/F2 공명 루프를 core/*.hexa fixed-point iterator 로 저작, vigilance gate 를 SS-ImmuneMemory recall_thr 처럼 wire. match/AUROC/fab/super-additive resonance 를 단일진입(cli/anima.hexa)에서 읽고 py math-mirror(torch 0)와 byte-parity 대조 — torch-only verdict 금지.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with SS-ImmuneMemory abstain gate + nm_modern_hopfield — distinct: ART's vigilance parameter rho IS the stability-plasticity resonance gate (resonate-or-reset), mapping 1:1 to recall_thr; the adaptive-resonance vigilance substrate is the differentiator.

강한 축=honesty 전부(membership decidability·copy-or-abstain·gate-capacity disjoint·groundedness)+G2 novelty+identity 지속/impostor. 약한 축=falsifiable>=1·dist>=5 풍부 생성성은 template 표현력에 의존(정직히 약점 표기). TOY fuzzy-ART first, scale-transfer 미검증(a_toy_scale_recheck).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
