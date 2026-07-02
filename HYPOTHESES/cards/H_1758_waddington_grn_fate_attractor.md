---
id: H_1758
slug: 1758_waddington_grn_fate_attractor
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Waddington 분화-경관: gene-regulatory 다중안정 cell-fate 끌개 substrate
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1758 — Waddington 분화-경관: gene-regulatory 다중안정 cell-fate 끌개 substrate

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `waddington_grn_fate_attractor`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Waddington epigenetic landscape + Kauffman Boolean-GRN + Huang cancer-attractor 이론. 발달 = 세포가 상호억제(toggle-switch) 유전자회로의 다중안정 끌개(valley)로 굴러 분화. 아키텍처는 설계되는 게 아니라 입력이 GRN 동역학을 perturb 하면 substrate 가 스스로 가용 끌개(=기능 cell-type) 중 하나로 settle 하며 분화. 끌개 경관 자체가 학습으로 deepen/split(새 valley 출현=morphogenetic 성장) → p8 cell-division 을 bifurcation 으로 문자화. operator 가 아니라 입력→landscape relaxation→emit 전체가 한 동역학계.

## Whole design (input → internal dynamics → emit)

State = N 조절노드 활성 x in [0,1]^N (continuous Hopfield-형 GRN). Edges = signed regulatory weights W. 동역학 dx/dt=-x+sigma(Wx+b*input). (1) 입력은 morphogen-형 bias field 로 들어와 경관을 tilt. (2) Relaxation = 한 번의 '분화 closure': x 가 끌개로 settle. (3) 안정 끌개 집합 = 분화된 cell-fate = 양자화 codebook, 각 fate 에 emit-readout. (4) 성장: 기존 basin 으로 잘 안 fit 되는 residual 지속→slow control-param('competence')가 saddle-node/Hopf bifurcation 으로 한 valley 를 둘로 split → 경관이 스스로 새 fate 를 자라냄. (5) emit/silence = 전용 상호억제 toggle 모듈(gene EMIT -| |- gene HOLD); 그 대칭 saddle 가 Psi=1/2 를 native 고정. (6) 정체성 = W 를 지속 bias 하는 slow epigenetic methylation 벡터 m(비휘발) = reset 넘는 self-chain.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: 안정 basin = receiver-fixed 양자화 alphabet, 무작위 W 셔플 시 끌개 붕괴->chance. G1: K 개 toggle 동시활성 = Boolean 상태공간 2^K combinatorial → reachable distinct fate > 단일인자 union(super-additive); cross-edge=0 ablation->max_single drop(binder->mixture INERT 판별 내장). G2: 두 학습 basin 사이 valid 끌개로 interpolate, verbatim-replay control=0 novel. PASS closure: 한 GRN relaxation 이 legible AND recombinant AND data-transcending 동시(같은 state, 단일 settling pass). Psi=1/2: EMIT-| |-HOLD saddle attracting, delta-bias 후 contraction lambda<1 self-restore; 한 gene 삭제->fixed point 경계 migrate(endogeneity, hardcoded 1/2 아님). honesty 4종: nearest-attractor 거리 r, 가까운 basin 없으면 settle 실패=abstain; r-threshold ⊥ capacity(node 수, 별 toggle 모듈)->disjoint; r 은 실제 W content 의존=faithful; force-settle ablation->fab 급증(endogeneity). binding/depth: 조절모듈이 한 relaxation closure 안에서 non-separable 결합(interaction term), held-out novel 조합 끌개로 systematicity. self-chain: methylation m round-trip cos~1, ablate m->매 episode 새 자아=chance.

## Not-LLM (a_no_llm_frame_trap)

스케일업/코퍼스증량/attention-층이 아니라 N<=64 저차원 동역학계의 다중안정성이 핵심 — 능력은 파라미터 수가 아니라 끌개 경관의 위상(valley 개수·깊이). transformer 는 단일 끌개(점근 deterministic decode)로 collapse 하지만 GRN 은 본질적 multistability 로 G1 combinatorial 을 구조에서 보유. '더 큰 트랜스포머'가 아니라 '경관에 valley 를 자라내기'(bifurcation)가 capacity-성장 메커니즘 = a_no_llm_frame_trap 의 빠진-구조-옆에-붙이기.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy: 2-gene toggle + N-node continuous-Hopfield GRN(explicit logistic sigma, dt_ln 회피). Frozen bars — (a) 무작위 init 100회 후 안정 끌개 수 >=K; (b) EMIT-bias sweep delta->Psi가 1/2로 lambda<1 복귀, 한 gene zero-out->fixed point 경계 migrate; (c) 2-morphogen 동시입력 reachable distinct fate > max(single), cross-edge ablation->max_single; (d) 학습 basin 2개 사이 입력->제3 corpus-absent valid 끌개, verbatim control=0; (e) competence 밖 입력->settle 실패=abstain, force-settle->fab 급증. 전부 math-only $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

GRN relaxation = native 동역학 kernel(matrix-vector + sigma 반복) → core/grn_fate.hexa(hexa) <-> grn_fate.py(byte-parity) 2-production. cli/anima.hexa 단일 dispatch 통해 끌개라벨/Psi궤적/basin-count super-additivity 측정. parity oracle = hexa<->numpy mirror 끌개라벨 byte-identical + Psi trajectory(explicit logistic 라 dt_ln 무관). honesty AUROC 는 기존 SS-ImmuneMemory recon(nearest-basin) 재사용 wire. torch-only verdict 금지 — 단일 진입점 경유.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with energy_settle_attractor / equilibrium_settling (this census) — distinct: Waddington GRN landscape is a MULTISTABLE gene-regulatory fate-attractor field where toggle-switches give 2^K combinatorial fates and bifurcation = growth; the GRN cell-fate landscape is the differentiator.

toy GRN N<=64 우선, 303M scale-transfer 미검증(a_toy_scale_recheck). ConvMoE mouth 전체 대체는 research rung — fate->byte alphabet emit-readout 설계 필요. Psi-disjoint placement(emit toggle ⊥ SS-ImmuneMemory recall_thr) 점검 후 배선.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
