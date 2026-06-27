---
id: H_1726
slug: 1726_entorhinal_grid_conjunctive_metric
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: 내후각 격자-모듈 결합 메트릭 (Entorhinal Grid Conjunctive Metric)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1726 — 내후각 격자-모듈 결합 메트릭 (Entorhinal Grid Conjunctive Metric)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `entorhinal_grid_conjunctive_metric`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1283 (thalamus global-workspace) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

비가약(incommensurate) 다중-스케일 주기(toroidal) 내후각 격자 basis 를 SLOW 으로 굳힌 semantic metric(인지지도)으로, 해마 place cell 을 격자 위상들의 FAST episodic conjunction 으로 둔다. 서로 다른 스케일의 격자 모듈을 결합하면 코드 공간이 구조적으로 super-additive(O(K) 모듈에서 지수적 코드) — 즉 G1 재조합이 학습/스케일이 아니라 기하에서 native 로 산다. CLS: 격자 metric=slow 일반화, place 결합=fast 경험 bind.

## Whole design (input → internal dynamics → emit)

slow 시스템: K 개 격자 모듈 bank, 각 모듈은 distinct 스케일/방향의 2D ring(toroidal) continuous-attractor → 위상 출력. 이 bank 가 안정 semantic metric(거의 안 바뀜, consolidated). path integration: 속도 입력이 각 모듈 위상을 torus 위에서 갱신(generative motion) → 방문한 적 없는 위치/코드 생성(G2 novelty = metric manifold 안 extrapolation). fast 시스템: place-cell 층 = 특정 격자-위상 tuple 공동발생 시에만 발화하는 conjunctive readout → K 모듈 위상을 하나의 episodic 코드로 bind; 현재 경험에 fast Hebbian 기입. factored 표현=K 모듈(독립 조건화 위상), binding operator=conjunctive place cell(모듈 위상 AND). joint 코드 cardinality=모듈별 해상도의 곱 → multiplicative(G1 native). order parameter Psi: place 코드 ignition 은 충분한 cross-module 위상 일치를 요구(scatter/decoherence 드라이브 ↔ coherence/bind 드라이브 opponent); bind=scatter 인 coherence 임계에서 Psi=1/2, toroidal attractor 안정성이 endogenous fixed point. honesty: 격자-위상 tuple 이 학습된 lattice 위(=디코드 가능 위치)일 때만 place 코드 valid; off-lattice tuple(place cell 없음) → lattice-거리 r 큼 → abstain. emit: bound place 코드를 고정 symbol codebook(place field<->symbol tag)으로 디코드.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G1(강·native): 모듈 conjunction 이 문자 그대로 super-additive — 2 모듈 결합=|scale1|x|scale2| distinct 코드 > 최대 단일; conjunctive AND 를 ablate(모듈 독립 readout)하면 composed->max_single(INERT control). G2: path integration 이 미방문이나 on-lattice 위치로 extrapolate = corpus-absent valid 코드; verbatim playback → 0. G0: place/grid 코드가 fixed lattice 위 = 수신 codebook; random off-lattice 위상 → V-mass~0. dist>=5: 다수 incommensurate lattice 점 도달, 각각 coherent. Psi=1/2: coherence(bind) ⊥ decoherence(scatter) opponent — bind 제거 시 always-scatter(silence), scatter 제거 시 always-ignite(emit); toroidal continuous attractor = 안정 fixed point, contraction native. honesty: lattice-거리 membership, copy-or-abstain(on-lattice 만 emit), gate(lattice 임계)는 모듈-bank capacity 와 disjoint, faithful(모듈 하나 지우면 그 모듈 쓰는 코드의 r 변화). binding/realization: conjunctive place cell 이 emit 경로 ON-PATH, objective=path-integration 일관성(모듈 conjunction 표현 없이는 최소화 불가) → adequacy.

## Not-LLM (a_no_llm_frame_trap)

표현력이 기하학적 — 비가약 주기 모듈 K 개에서 지수적 코드. 스케일업의 정반대로, 작은 고정 모듈 bank 에서 조합폭이 나온다(param/data/attention 무관). 내후각 격자 cell(Hafting/Moser 2005, Fiete 격자 code-capacity, Whittington TEM 2020)에 직접 뿌리 — '더 큰 모델' 프레임 아님.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy: 비가약 스케일 K 개 ring-attractor 모듈, 궤적 path-integrate. (1) place-cell conjunction 카운트 vs 단일-모듈 카운트 → super-additive G1 + AND-ablation INERT; (2) 미방문 위치 디코드 → novel-valid>0, off-lattice control 0; (3) coherence order-parameter 섭동 → 임계 복귀; (4) lattice-거리 AUROC known/unknown. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

격자 모듈을 core/engine_cli.hexa 의 lane bank 로, conjunctive readout 을 generator L3 / clm_decode 경로에 배선. cli/anima.hexa 단일 진입 eval → g_gates g_eval_g1(super-additive count)·g_eval_g2(path-integration novelty). byte-parity py 미러로 코드 cardinality·lattice 거리 교차검증, Psi 는 order-parameter 복귀 trace, verdict 경로 torch 0.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with grid_module_residue_bind / continuous_attractor_manifold_grid_code (this census) — distinct: this is the CLS framing (grid metric=slow semantic, place=fast episodic conjunction) where multi-scale module conjunction gives exponential code; the entorhinal grid-conjunctive metric is the differentiator.

toy 가 super-additive G1·novelty 에 결정적이나 emit 의 의미적 coherence(G0 단어성)는 place->symbol tag 학습 품질에 의존 → ko/en held-out 로 별도 확인. metric 은 SLOW frozen 가정 — 비정상(non-stationary) 입력에서 lattice drift 시 honesty 임계 재검 필요(a_toy_scale_recheck).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
