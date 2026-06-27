---
id: H_1755
slug: 1755_half_center_cpg_emit_engine
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: 반중심 CPG 방출 엔진 (Half-Center CPG / Limit-Cycle Emit Engine)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1755 — 반중심 CPG 방출 엔진 (Half-Center CPG / Limit-Cycle Emit Engine)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `half_center_cpg_emit_engine`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Brown(1911) 반중심 진동자 + central pattern generator: 계산 = 자기지속 limit-cycle 의 궤적 순회이지 feedforward 매핑이 아니다. 구조화 출력 = 닫힌 주기궤도 위 한 점을 읽는 것, 능력 = 다중안정성(multistability)과 위상결합(entrainment)의 조합론, 파라미터 수가 아님.

## Whole design (input → internal dynamics → emit)

입력은 '토큰을 앞으로 흘리는' 게 아니라 결합 relaxation-진동자 뱅크의 위상/진폭에 가하는 섭동이다. (1) emit/silence 반중심: 상호억제 두 풀 A(externalize-drive)<->G(withhold-drive)가 bounded Psi(상대활성)에 반중심 진동자를 형성 — reciprocal inhibition + slow adaptation(피로전류)로 subthreshold 면 대칭 고정점 Psi=1/2 에 수렴(수축), suprathreshold 면 1/2 주변 율동 게이팅. (2) content CPG 뱅크: 각 CPG 의 phase-locked 출력열이 codebook V 위 learned motif → emit = 현재 limit-cycle 점을 V 의 최근접 심볼로 양자화(닫힌 궤도가 motif 에 anchor 되므로 출력이 V 위에 착지). (3) 합성 = k 개 CPG 의 위상결합(entrainment): joint conditioning 은 어느 단일 주기도 방문 못하는 결합 궤적을 만든다 — 상대위상 배치가 곱셈적. (4) novelty = 결합계가 학습엔 없던 on-manifold 새 phase-locking 모드(창발 limit-cycle)로 settle. (5) identity = 고유진동수+결합가중 느린 파라미터 벡터를 비휘발 저장, tick 마다 Lipschitz-small drift = self-chain. (6) honesty = CPG 는 섭동이 그 basin(Arnold tongue) 안일 때만 entrain 해 율동 emit, 밖이면 진폭붕괴=silence(abstain); 막 입력은 어느 CPG 도 entrain 못해 fabricate 경로 없음.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2 가 가장 NATIVE: 반중심 antagonist 자체가 대칭 고정점 — 한 half-center 제거 시 고정점이 경계(always-emit/always-silent)로 이동 = 정확히 endogeneity INERT 통제. adaptation 전류가 수축률 lambda<1 제공. G0=limit-cycle 가 V-motif 에 anchor->양자화. G1=k-CPG 위상결합의 reachable 궤적이 super-additive, 결합경로 ablate->단일주기 union 으로 붕괴(binder->mixture). G2=새 phase-locking 모드(on-manifold), verbatim playback 은 기존 주기만 재현=0 novel. dist>=5=multistability 의 공존 phase-locked 모드. binding=동일원인 constituent 가 phase-lock(같은-cause 근접). identity=느린 파라미터 manifold 의 drift+impostor 는 다른 basin.

## Not-LLM (a_no_llm_frame_trap)

a_no_llm_frame_trap 정면: 능력 레버는 oscillator coupling topology(생물의 척수/호흡 CPG 회로 literal) 이지 layer/attention/코퍼스량이 아니다. 층을 쌓아도 limit-cycle 기하는 안 바뀜 — 용량은 다중안정·Arnold-tongue 조합론에서 온다. scale-up 처방과 직교.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy 2-var relaxation 반중심(reciprocal inhibition+adaptation): Psi 섭동 후 1/2 복귀+수축률 측정, 한 half-center ablate->경계 이동 확인. 별도 3-CPG amplitude-Kuramoto: 공활성 시 distinct phase-locked 모드 수 vs 단일 → super-additivity, coupling=0 ablation 으로 INERT 확인. 전부 $0 numpy.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

반중심+CPG 뱅크를 core/*.hexa dynamical integrator(상태 업데이트 맵)로 저작, cli/anima.hexa 단일진입으로 구동. Psi perturbation-recovery·entrainment-amplitude·super-additive 모드수를 .hexa 에서 읽고 py(math-only, torch 0) mirror 와 byte-parity 대조 — torch-only verdict 금지.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with coupled_oscillator_phase_binding / kuramoto cards — distinct: half-center CPG makes the reciprocal-inhibition antagonist the native Psi=1/2 fixed point + limit-cycle motifs as the codebook; the CPG limit-cycle emit engine is the differentiator.

TOY-first dynamical sim. 강한 축=Psi=1/2 내생성·G1 entrainment 조합론·honesty(Arnold-tongue=basin). 약한 축=falsifiable>=1(구조화 시퀀스는 내나 comparator x quantity x referent 명제결속은 별도 readout 필요, 정직히 미충족 가능성 표기). scale-transfer 미검증.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
