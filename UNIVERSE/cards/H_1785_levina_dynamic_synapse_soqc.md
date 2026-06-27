---
id: H_1785
slug: 1785_levina_dynamic_synapse_soqc
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: 동적-시냅스 자기조직 준임계 엔진 (Levina-Herrmann-Geisel SOqC avalanche substrate)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1785 — 동적-시냅스 자기조직 준임계 엔진 (Levina-Herrmann-Geisel SOqC avalanche substrate)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `levina_dynamic_synapse_soqc`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

임계는 외부 homeostat 가 분기비 sigma 를 맞춰주는 게 아니라, depletable 시냅스 자원(short-term depression)의 고갈⇄회복이 sigma 를 sigma~1 근방으로 스스로 쓸어담는 self-organized quasi-criticality(SOqC)에서 창발한다. 침묵 중 자원 회복->supercritical 축적, avalanche 방전->자원 고갈->subcritical, 이 왕복이 임계를 parking. (branching_avalanche_homeostat 의 '명시적 sigma-homeostat 튜닝'과 직교 — 여기선 임계가 보존-유사 자원 동역학의 부산물.)

## Whole design (input → internal dynamics → emit)

입력=외부 perturbation 이 excitable E/I 재귀망의 일부 cell 점화. 각 시냅스에 자원 u in [0,1] (스파이크당 −du, 회복 +u/tau); 분기비 sigma~<u>*연결도. 침묵->u 회복->sigma 상승->다음 avalanche 크게 터짐->u 고갈->sigma 하강 = sigma=1 근방 attractor. 내부동역학=temporal avalanche 패턴. emit=avalanche 가 emit-boundary 까지 percolate 하면 그 패턴을 receiver-frozen assembly codebook V 에 nearest-template VQ-정렬해 토큰 방출, die-out 이면 abstain(침묵).

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: emit 이 avalanche->frozen assembly codebook V 정렬으로만 나가므로 V-mass 구조강제(state->emit scramble 시 chance 붕괴). G1: sigma=1 에서 susceptibility 발산->두 factor 동시점화 reach 가 곱셈적(cross-term!=0); 공유-cell 자원결합(binding 경로) OFF 시 composed->마지널 합(INERT native). G2: 임계 metastable 패턴 repertoire 가 조합적->코퍼스 밖 valid 패턴, verbatim playback control=0. dist>=5: 임계 잔여엔트로피+mode 분리로 distinct AND coherent 다중 avalanche. Psi=1/2: emit-percolate vs die-out order parameter 가 sigma=1 에서 1/2, 반대부호 operator=E(확산)<->I+자원고갈(억제), 자원회복이 contraction(섭동->sigma->1 자기복원), 한쪽 제거 시 fixed point 0/1 경계 이주=endogeneity. honesty: 어느 assembly basin 도 안 들면 die-out=abstain, recon_err=최근접 bound-assembly 거리·theta frozen·자원/percolation gate 제거 시 fab 상승. identity: per-시냅스 자원 baseline set-point 벡터(비휘발 store)가 reset 넘어 지속, tick small drift. realization: binding 이 percolation emit 경로 위라 ablation 이 emit 움직임.

## Not-LLM (a_no_llm_frame_trap)

capacity 가 파라미터·깊이가 아니라 sigma=1 근방 임계 repertoire 크기에서 나온다. 임계를 무료로 parking 하는 건 STD(생물 시냅스 메커니즘)이고, 모델을 키우면 오히려 임계를 깨고 ordered/chaotic 으로 떨어진다 — '더 큰 트랜스포머'가 아니라 '정확히 임계'가 처방.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy N~2000 excitable 망 + 시냅스 자원 동역학 시뮬: (i) sigma 시계열이 섭동 후 1.0 근방 self-restore (ii) avalanche size 분포 power-law tau~1.5 (iii) 두 입력 동시점화 reach > 마지널 합 AND 공유 자원결합 제거 시 그 초과가 0 붕괴(INERT). 결정 probe, $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

avalanche->assembly VQ 토큰 스트림을 generator L3 typed mouth 로 배선 후 cli/anima.hexa -- eval 단일진입 -> core/g_gates.hexa g_eval_g0/g1/g2 로 G0 kwr·G1 _g_coverage·G2 corpus-absence 엔진-네이티브 채점. Psi=1/2=SS-safety_phi_ratchet 섭동-복원, honesty=SS-ImmuneMemory recon_err/theta AUROC, identity=SS-SelfIdentity self_drift/_cos. numpy avalanche byte-parity py 미러로 logits/CE 대조(torch-only verdict 금지).

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with branching_avalanche_homeostat (this census) / self_organized_criticality — distinct: Levina SOqC parks sigma~1 as a BYPRODUCT of depletable synaptic-resource (STD) depletion/recovery, no explicit sigma-homeostat tuning; the dynamic-synapse SOqC is the differentiator.

temporal absorbing-state(directed-percolation universality) SOqC; toy numpy 로 결정 가능하나 임계 repertoire 가 실제 chat 4칸 register codebook 을 덮는지는 스케일 재검 필요(a_toy_scale_recheck).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
