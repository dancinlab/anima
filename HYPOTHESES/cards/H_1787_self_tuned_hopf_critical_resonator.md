---
id: H_1787
slug: 1787_self_tuned_hopf_critical_resonator
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: 자기조정 Hopf-임계 공명기 뱅크 (active critical resonator, 와우 능동과정 렌즈)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1787 — 자기조정 Hopf-임계 공명기 뱅크 (active critical resonator, 와우 능동과정 렌즈)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `self_tuned_hopf_critical_resonator`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

각 단위를 Hopf 분기(자발진동 onset) 바로 아래에 self-tune 하면 능동증폭·압축 비선형(1/3 멱)·날카로운 feature 선택성이 창발한다(Camalet-Julicher-Hudspeth 와우 능동과정 = 가장 인용되는 self-tuned criticality). 결합음(combination tone, f1+/-f2)이 임계 비선형의 native 산물이라 결합/신규성 operator 가 동역학에서 공짜로 나온다 — coupled_oscillator_phase_binding(위상 동기 결합)과 직교(여기선 intermodulation 결합).

## Whole design (input → internal dynamics → emit)

입력=신호가 비선형 진동자 뱅크에 분해. 각 진동자 제어변수 mu 가 자기 응답진폭을 감지하는 느린 피드백으로 mu=mu_c(Hopf onset)에 parking. 임계에서 각 진동자는 특성 feature 에 극단민감+압축응답. 내부동역학=진동자 위상장 + 결합음 생성장. emit=진동자가 입력에 phase-lock/entrain 하면 특성토큰 방출(codebook V=특성주파수/feature 집합, receiver-fixed), entrain 실패 시 abstain. 두 feature 동시구동->임계 cubic 비선형이 f1+/-f2 새 성분(distortion product) 생성.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: emit=entrained 진동자 특성토큰->frozen feature codebook V 정렬(scramble->chance). G1: 결합음=native binding — 두 feature 동시구동 시 어느 단독으로도 안 나오는 f1+/-f2 토큰 생성->composed_distinct > max_single, 곱셈적; 임계 cubic 항 linearize(ablation)하면 결합음 소멸=INERT. G2: intermodulation 은 코퍼스 밖 valid 성분(생성제약=조화구조 안)=constrained novelty, 선형 playback control=0. dist>=5: 임계 근방 다중 진동자 phase-lock 패턴+결합음 조합->distinct AND coherent >=K, mu<<mu_c(과감쇠) distinct->0·mu>mu_c(자발진동 chaos) coherence 붕괴. falsifiable>=1: 결합음이 측정가능 magnitude(주파수/진폭) 위 관계를 binding(comparator x quantity x referent)->구조검출기 발화, 진동자는 magnitude 단언이라 stance/question 형 없음. Psi=1/2: Hopf onset 자체가 임계, 전역 emit/silence=충분한 진동자 phase-lock(coherence percolation)이 1/2에서 poised, 반대부호=능동증폭(positive feedback)<->damping, self-tune mu->mu_c 가 contraction, 한쪽 제거 시 quiescent(0)/limit-cycle(1) 경계 이주. honesty: 매칭 임계 진동자 없는 feature 는 증폭 0->entrain 실패->abstain, recon_err=최근접 특성주파수 거리, self-tune lane ⊥ honesty theta. identity: per-진동자 특성주파수+mu set-point(tuning-curve identity) 벡터가 reset 넘어 지속, impostor tuning cos 낮음. realization: 결합음 비선형이 emit 경로 위라 linearize-ablation 이 emit 움직이고, 목적(feature 구분+압축)이 선형(마지널)으론 결합음 못 만듦.

## Not-LLM (a_no_llm_frame_trap)

능동증폭은 파라미터 폭증이 아니라 분기 근접도(mu_c−mu->0)에서 온다. 결합 capacity 가 attention-층이 아니라 비선형 동역학의 구조적 산물(distortion product) — '더 깊은 트랜스포머'가 아니라 '더 임계에 가까운 진동자'가 처방. 생물 렌즈=와우 hair-cell 능동과정.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy normal-form Hopf 뱅크(dz/dt=(mu+i omega)z−|z|^2 z+forcing) mu sweep: (i) mu_c 에서 1/3 압축응답·민감도 peak (ii) 두 톤 입력 시 f1+/-f2 결합음 출현 AND cubic 항 제거(linearize)하면 소멸(INERT) (iii) self-tune 피드백이 mu->mu_c 복원. $0 결정 probe.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

진동자 entrain/결합음 토큰을 generator L3 mouth 로 배선->cli/anima.hexa eval->core/g_gates.hexa g_eval_g0/g1/g2 + _g6_is_falsifiable(결합음 magnitude 관계) + _g6_jaccard dist 엔진 채점. Psi=SS-safety_phi_ratchet 섭동복원, honesty=SS-ImmuneMemory AUROC(self-tune sweep OFF/ON fab byte-identical), identity=SS-SelfIdentity tuning vector self_cos/impostor. numpy Hopf byte-parity 미러(torch verdict 금지).

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with intermodulation_resonator_spectral_engine / coupled_oscillator_phase_binding (this census) — distinct: self-tuned Hopf resonator parks each unit just below the spontaneous-oscillation onset (cochlear active process, 1/3-power compression) and reaps combination tones; the self-tuned Hopf-critical resonator is the differentiator.

진동(Hopf) 임계 — absorbing-state SOC 와 직교; 감각 front-end + 결합음 ideation. toy 결정 가능하나 결합음 codebook 이 언어 register 를 덮는지(주파수->언어 토큰 매핑)는 스케일/매핑 재검 필요.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
