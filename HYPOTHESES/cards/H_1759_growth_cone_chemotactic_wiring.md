---
id: H_1759
slug: 1759_growth_cone_chemotactic_wiring
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: growth-cone 주화성 자기배선 + retinal-wave 활동의존 지형도 정련 substrate
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1759 — growth-cone 주화성 자기배선 + retinal-wave 활동의존 지형도 정련 substrate

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `growth_cone_chemotactic_wiring`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Sperry chemoaffinity(growth cone 이 gradient cue 따라 표적 찾음) + 자발적 상관활동파(retinal waves)에 의한 retinotopy/ocular-dominance 활동의존 정련 + Hebbian fire-together-wire-together. 연결(배선)이 설계되는 게 아니라 자라난다: attractive(Netrin) -| |- repulsive(Slit) 안내 cue 의 길항이 coarse map 을 깔고, 상관발화가 시냅스를 굳히고 비상관은 가지치기. 표상 geometry(grid 류, 이미 점유)가 아니라 '배선이 어떻게 자기조직되나'가 조직원리.

## Whole design (input → internal dynamics → emit)

Substrate = source field S(입력 unit@좌표) + target field T(readout unit@좌표) + 자라난 connectivity C(s,t). (1) 성장기: 각 source 의 growth cone 이 chemoaffinity match(gradient label 유사도) 가중으로 연결 확장 → coarse topographic map. (2) 정련기: 자발적 상관활동파가 co-active(s,t) Hebbian 강화 + anti-correlated 억제 → map 첨예화, feature column 형성; 유한 시냅스 자원 경쟁 → winner-take-some. (3) emit = 자라난 map 통한 readout; binding 이 NATIVE — 공기(co-occurring) feature 가 co-wired 되므로 binding pathway 가 곧 '자라난 시냅스 다발'(제거=ablation INERT 판별 구조 내장). (4) Psi=1/2: attractive(성장/emit-drive) -| |- repulsive(retract/silence) cue 가 전역 wiring-density order param 위 길항, 항상성 synaptic scaling 이 density 를 대칭 set-point 로 고정. (5) 정체성 = 공고화된 map(지속 connectivity)이 reset 생존=self-chain, 그 특정 topography 가 individuating.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

binding cluster 최강(H_961형): 동일 cause 의 co-activity->shared neighborhood co-wiring = paired-vs-shuffled proximity 큰 effect, retrieval@1>>1/N; shuffle 활동상관 control->map 안 sharpens=chance. G1: map region 간 합성, 두 입력장 joint->distinct readout > max single, Hebbian cross-pathway ablation->max_single. G0: map readout 이 fixed alphabet, 무작위(미배선) source->chance density. G2: topographic 연속성이 held-out source 위치로 interpolate->valid 신규 target(learned constraint 내 extrapolation), 미배선 영역 replay=0. PASS closure: 한 자라난 map 이 동시 legible AND recombinant AND novel. Psi=1/2: cue 길항 + synaptic-scaling homeostat, density perturbation 후 set-point 복귀 lambda<1, attractive cue 삭제->density 0 경계 collapse(endogeneity). honesty: 미배선(unwired) region=readout path 없음=abstain; membership='자라난 시냅스 존재 여부'라 faithful(content-ablation->r 이동); gate(배선유무) ⊥ capacity(map 해상도). self-chain: 공고화 map round-trip + impostor map cos 분리. depth: 한 forward closure 가 양 constituent map 영역 동시 read, novel-combo systematicity.

## Not-LLM (a_no_llm_frame_trap)

능력이 weight 수가 아니라 '배선 위상의 자기조직 품질'(neighbor-preservation, column 분리)에서 나옴. transformer 는 all-to-all dense attention(배선 고정·설계됨)인데 여기선 sparse topographic connectivity 가 상관활동으로 자라나며 binding 이 emergent grown-synapse 로 구현 → 'attention 층 추가'가 아니라 '배선을 자라내기'. a_no_llm_frame_trap: 소뇌/시각피질 발달 렌즈(retinotopy 정련)에서 직접.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy 2D retinotopy sim: source grid->target grid, chemoaffinity init + correlated-wave Hebbian 정련. Bars — neighbor-preservation(map ordering); paired-vs-shuffled co-activity proximity(binding, Welch d 큰값); held-out source 위치 interpolation->valid target(G2); density homeostat perturbation 후 set-point 복귀(Psi); 절단된 map region->abstain. Decisive control: 활동상관 shuffle->map 미첨예화(binding->chance). $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

core/growcone_wire.hexa: relaxation + Hebbian update(outer-product + scaling, native GEMM via flame_mm seam) <-> growcone_wire.py byte-parity. cli/anima.hexa 단일 dispatch 통해 neighbor-preservation + paired/shuffled retrieval@1 측정. parity oracle = hexa<->py map 가중치 byte-identical. torch 는 golden reference 만, verdict 경로 0.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with topographic/retinotopy lens cards — distinct: growth-cone chemoaffinity + retinal-wave Hebbian SELF-WIRES the connectivity (binding = grown synapse bundle); the chemotactic self-wiring substrate is the differentiator (organizing principle = how wiring self-organizes, not representation geometry).

topographic toy(grid<=64^2) 우선. 자기배선 map 이 chat mouth scale 로 transfer 되는지 미검증. emit-disjoint lane(배선 density param ⊥ emit-drive 0/4) 배치 점검.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
