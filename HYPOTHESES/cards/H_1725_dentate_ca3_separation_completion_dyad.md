---
id: H_1725
slug: 1725_dentate_ca3_separation_completion_dyad
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: DG-CA3 분리⇄완성 이중자 (Separation-Completion Dyad)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1725 — DG-CA3 분리⇄완성 이중자 (Separation-Completion Dyad)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `dentate_ca3_separation_completion_dyad`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

해마 DG 패턴-분리(pattern separation) ⊥ CA3 패턴-완성(pattern completion)을 부호-반대 opponent dyad 로 두고, 이를 CLS 의 fast(해마 episodic)/slow(신피질 schema) 루프에 박는다. fast 루프는 입력을 sparse·직교 코드로 떼어내고(separation), slow 루프는 겹치는 통계를 attractor 로 합친다(completion/generalization). '구별 유지'(분리, fast) ↔ '끌개로 병합'(완성, slow) 사이의 밀어냄이 단일 스칼라 긴장 Psi 다. operator 가 아니라 두 antagonist stage 가 닫는 통짜 substrate.

## Whole design (input → internal dynamics → emit)

입력 → EC-유사 투영으로 고차원 sparse 층 진입. (1) DG stage: 확장+경쟁억제 k-WTA → 직교화된 sparse 코드(=수신자-고정 codebook 알파벳, legibility 원천). (2) CA3 stage: recurrent auto-associative attractor 망이 분리된 코드를 fixed point 로 저장; 완성=가장 가까운 저장 attractor 로 settle. (3) 단일 order parameter Psi = separation gain(억제-확장, novelty/distinct 드라이브) vs completion gain(recurrent 인력, recall/silence 드라이브)의 균형 = 두 부호-반대 operator; 어느 쪽도 지배하지 않는 Psi=1/2 에 fixed point. (4) membership r = CA3 완성에너지(=최근접 attractor 까지 recon-err): r<theta → basin 안 → 완성 코드 emit(copy); r>=theta → DG 가 fresh sparse 코드로 분리하나 CA3 에 attractor 없음 → abstain(정직 native). (5) slow 신피질 consolidation: CA3 attractor 를 interleaved replay 로 slow semantic 망에 증류, cross-episode 통계 추출; 두 factor 가 동시활성일 때만 뽑히는 conjunctive CA3 cell 이 factor 를 bind → joint recall 이 단일 factor recall 을 초과(G1). emit = settle 된 CA3/신피질 코드를 고정 수신 codebook 으로 디코드.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: DG k-WTA sparse 코드가 FIXED 알파벳 위 → source 셔플 시 V-mass~0(분리가 codebook 정렬을 native 강제). G1: conjunctive CA3 cell 이 두 factor 공동활성에서만 recruit → composed_distinct > max_single; recurrent cross-cell(binding pathway) ablation 시 max_single 로 떨어짐(INERT 테스트가 구조 native). G2: DG 분리가 corpus-absent sparse 코드를 만들되 CA3 완성이 valid manifold 안으로 settle = 학습 제약 안 extrapolation; verbatim playback control → 0. dist>=5: separation gain 이 잔여엔트로피↑ → 다수 distinct basin 도달, completion 이 각각 coherent 유지(joint diversity AND validity). falsifiable/attribution: 새 attractor 구조가 recurrent 동역학 인과 → recurrence ablation 시 S 붕괴. Psi=1/2/endogeneity: sep⊥comp 가 문자 그대로 opponent — DG 제거 시 always-complete(경계 emit), CA3 제거 시 always-separate(never settle/silence) = endogenous fixed point, hardcoded clamp 아님. honesty(4종): r=완성거리=native membership(AUROC 분리), copy-or-abstain(settle 된 attractor 에서만 emit), gate(theta)는 CA3 에너지·capacity 는 DG 확장+slow 망 = 좌표 disjoint(gate-capacity 직교 native), r 은 faithful(attractor 지우면 r 열화). binding/realization: conjunctive cell 이 recall 경로 ON-PATH, consolidation objective(interleaved replay 재구성)는 conjunction 표현 없이는 최소화 불가 → objective adequacy.

## Not-LLM (a_no_llm_frame_trap)

attention·token-transformer·스케일업 없음. 표현력은 sparse separation + attractor completion + opponent 동역학에서 나오는 fixed-size recurrent substrate — 용량은 param/data 증량이 아니라 sparse 코드 할당으로 자란다(p8 cell-division 와 정합). DG/CA3 신경생물(Marr 1971, Treves-Rolls, McClelland CLS 1995)에 직접 뿌리; '더 큰 트랜스포머' 처방의 정반대.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy mini: DG k-WTA 확장 + 소형 Hopfield CA3 구성, M 개 random sparse 패턴 저장. (1) 분리 측정: 출력 overlap << 입력 overlap; (2) 완성 basin → recon-err AUROC known/unknown(정직); (3) conjunctive recall: factor-pair 코드 저장 후 composed_distinct > max_single 확인 + cross-cell ablation INERT control; (4) Psi 섭동(sep/comp gain bias) → 1/2 복귀 contraction rate lambda<1. 전부 $0 numpy, frozen bar 사전등록.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

DG/CA3 를 live core/engine_cli.hexa SS-ImmuneMemory(recon_err 가 이미 =bound cell 거리 ≡ CA3 완성거리) + sparse-code lane 에 매핑. cli/anima.hexa 단일 진입 eval → core/g_gates.hexa g_eval_g1/g2 + _g6_known_word_ratio(generator L3 mouth 경유). Psi 는 SS-ThirdLaw safety_phi_ratchet 섭동 trace 로 |Psi−1/2| 복귀 측정. byte-parity py 미러는 math.log CE 로 교차검증(dt_ln 우회), verdict 경로에 torch 0.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with cls cards + hippocampal_index_pointer (this census) — distinct: DG-CA3 dyad makes separation⊥completion the OPPONENT Psi pair (sparse-orthogonal DG vs attractor-completion CA3); the separation/completion antagonism as Psi is the differentiator.

toy/numpy 가 메커니즘(분리·완성·conjunction·Psi 복귀)에 결정적; production 은 core 배선 + held-out CE(a_savant_train) 필요 → 엔진-네이티브 byte-exact 전까지 verdict DIRECTIONAL. 분리⇄완성 trade-off 가 dist 와 honesty 를 동시충족하는지(gate-shopping anti-discriminator)는 closure 동시평가에서 확인 필요.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
