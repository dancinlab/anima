---
id: H_1786
slug: 1786_kinouchi_copelli_dynamic_range_sensorium
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: 임계 동적범위 감각피질 (Kinouchi-Copelli dynamic-range sensorium)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1786 — 임계 동적범위 감각피질 (Kinouchi-Copelli dynamic-range sensorium)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `kinouchi_copelli_dynamic_range_sensorium`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

임계점은 dynamic range(여러 decade 입력강도를 graded 출력으로 구분)와 stimulus repertoire 를 동시에 최대화한다(Kinouchi-Copelli). 아키텍처 전체를 '임계에 poised 된 excitable sheet 가 입력을 decade-횡단 Stevens 멱법칙으로 코딩->그 graded 활성을 codebook 으로 양자화'하는 감각 front-end 로 설계 — codebook coverage 가 dynamic range 에 비례.

## Whole design (input → internal dynamics → emit)

입력=자극이 excitable sheet cell 을 확률 점화, 이웃-매개 avalanche 로 증폭. 느린 gain 보정이 sigma->1 self-tune. 임계에서 입력률 r->평균활성 F 가 멱법칙(F~r^m, m~수 decade). 내부동역학=순간 avalanche 활성장. emit=F 가 percolation 임계 넘으면 활성패턴을 학습 VQ 로 frozen codebook V 에 graded 양자화해 토큰 방출, 안 넘으면 abstain. 임계가 가장 많은 구분가능 코드칸을 연다.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: graded 활성->frozen VQ codebook V 정렬, dynamic range 극대화가 V-칸 점유 최대화(scramble->chance). G1: 임계 susceptibility 발산->두 자극 joint 활성패턴이 마지널 합 초과(곱셈 cross-term); divisive normalization 이 binding 경로, 제거 시 composed->max_single(INERT). G2: dynamic range 가 known 자극 사이 graded 보간/외삽을 임계 manifold 위 valid 로 방출=constrained-extrapolation, saturated playback control=0. dist>=5: 임계=최대 잔여엔트로피+mode 분리->distinct AND coherent >=K, ordered 면 distinct->0·chaotic 이면 coherence 붕괴=임계만 양쪽 동시. Psi=1/2: emit-ignite vs sub-threshold order parameter 가 sigma=1 에서 1/2, 반대부호=이웃증폭 <-> divisive normalization/refractory, gain self-tune 이 contraction, 한쪽 제거 시 경계 이주. honesty: dynamic range 밖 자극은 saturate/ignite 실패->abstain, recon_err=임계 manifold 거리, gain 보정 lane ⊥ honesty theta(gate-capacity disjoint). identity: per-cell gain-calibration 벡터가 reset 넘어 지속. realization: normalization 이 emit 경로 위라 ablation 이 emit 움직이고, 목적(자극 구분 최대화)이 마지널만으론 최적 도달 불가.

## Not-LLM (a_no_llm_frame_trap)

capacity=dynamic range(임계의 발산하는 susceptibility)이지 파라미터·깊이가 아니다. Kinouchi-Copelli: ordered/chaotic 둘 다 dynamic range 압축, 오직 임계에서만 멱법칙 — '더 크게'가 아니라 '정확히 임계'가 처방. 생물 렌즈=감각수용기/피질 sheet 의 decade-횡단 코딩.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy excitable sheet(Greenberg-Hastings 류) sigma sweep: dynamic range Delta(dB)가 sigma=1 에서 peak·ordered/chaotic 급락(Kinouchi-Copelli 재현), 두 자극 joint 구분칸수 > 마지널 AND normalization 제거 시 붕괴. $0 결정 probe.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

VQ codebook 토큰을 generator L3 mouth 로 배선->cli/anima.hexa eval->core/g_gates.hexa g_eval_g0/g1/g2 + dist(_g6_jaccard distinct-coherent) 엔진 채점. Psi=SS-safety_phi_ratchet, honesty=SS-ImmuneMemory AUROC(gain sweep OFF/ON fab byte-identical=disjoint 확인), identity=SS-SelfIdentity. numpy sheet byte-parity 미러(torch-only 금지).

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with branching_avalanche_homeostat / kinouchi family — distinct: Kinouchi-Copelli sensorium maximizes DYNAMIC RANGE (decade-spanning graded coding) at criticality as the codebook-coverage lever; the dynamic-range sensorium is the differentiator.

response/susceptibility 임계(static dynamic-range) 감각 front-end; toy 결정 가능, codebook 이 실제 register 4칸 덮는지 스케일 재검 필요.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
