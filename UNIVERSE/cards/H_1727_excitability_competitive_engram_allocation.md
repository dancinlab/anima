---
id: H_1727
slug: 1727_excitability_competitive_engram_allocation
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: 흥분성-경쟁 엔그램 할당 (Excitability-Competitive Engram Allocation)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1727 — 흥분성-경쟁 엔그램 할당 (Excitability-Competitive Engram Allocation)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `excitability_competitive_engram_allocation`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

기억 할당 이론 — 부호화 시점에 일시적으로 흥분성(CREB)이 높은 뉴런이 경쟁에서 이겨 engram 에 recruit 되고, 시간적으로 가까운 기억은 겹치는 population 에 co-allocate(memory linking)된다. FAST=빠른 경쟁적 할당(해마 episodic), SLOW=consolidation/성숙 + 흥분성 감쇠 homeostasis(피질). 조합은 통제된 engram OVERLAP 에서, 정직은 할당 게이트에서 창발. (단일 op 아닌, 흥분성장(field)·경쟁·homeostasis·consolidation 이 닫는 통짜 동역학.)

## Whole design (input → internal dynamics → emit)

입력이 population 구동, 각 cell 은 동적 흥분성 e_i(homeostatic 조절, 활동 후 일시 bump = CREB tag). 할당: 고흥분성 cell 중 winner-take-k → 그 cell 들이 현재 입력의 engram 형성(fast Hebbian bind). 이후 흥분성 감쇠(refractory)로 다음 기억은 다른(분리된) population 으로 — 단 linking window 안이면 잔여 흥분성이 co-allocation(overlap) 유발 → linked 기억. 조합(G1): 두 factor 를 함께(또는 window 안) 제시 → overlap 포함 union population 에 co-allocate; overlap cell 이 conjunctive(bound pair 에 발화) → joint 코드 recall 이 단일 factor 초과. linking/overlap 메커니즘 OFF → composed->max_single(INERT). 정직: recall 은 저장 engram 재활성 필요, query→최근접 engram overlap 점수 r; r>theta → 그 engram 콘텐츠 emit(copy), r<theta → 할당된 engram 없음 → abstain. 할당 게이트=정직 게이트. Psi=1/2: 흥분성-상승(할당/emit 드라이브) ⊥ homeostatic 감쇠/억제(보류/보존 드라이브) opponent; 평균 망 흥분성이 order parameter, 할당이 고갈시키고 homeostasis 가 복원해 1/2 에 고정. homeostasis 제거 → runaway 할당(always emit), 흥분성 드라이브 제거 → never 할당(always silent). slow: consolidation 이 할당 engram 성숙 + 약한 것 eviction/apoptosis(기존 MITOSIS/immune lane 연계) → 안정 semantic engram 추출; identity = 한 번 할당된 self-engram 을 세션 경계 넘어 재-instantiate(self-chain). emit: 재활성 engram 을 고정 symbol codebook 으로 디코드.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: engram->symbol 고정 codebook. G1: co-allocation overlap=conjunctive cell → super-additive joint recall; linking-OFF ablation INERT. G2: 함께 학습된 적 없으나 공유 cell 로 linked 된 factor 의 부분 co-allocation → corpus-absent valid recombination; overlap 없는 순수 retrieval → 0 novel. dist>=5: 경쟁 할당이 다수 distinct engram 생성, 각 coherent. Psi=1/2: 흥분성-상승 ⊥ homeostatic-감쇠 opponent, 평균 흥분성 fixed point; ablation 시 경계 이동. honesty(4종 강): membership=engram-match r(저장 engram 에 faithful — engram 지우면 r 하락 = groundedness native), copy-or-abstain(할당 게이트), gate-capacity disjoint(흥분성/homeostasis param ⊥ engram-콘텐츠 capacity), decidability AUROC(overlap 점수). SS-ImmuneMemory recall_thr 에 직접 매핑. cross-boundary persistence + self margin: 전용 self-engram 을 .kosmos anchor 로 영속, 세션 경계 넘어 재-할당(SS-SelfIdentity 연계); impostor engram 은 overlap 낮음 → 양 margin. realization: overlap cell 이 recall 경로 ON-PATH, consolidation objective 가 conjunction 보상.

## Not-LLM (a_no_llm_frame_trap)

용량은 cell 할당으로 자란다(문자 그대로 cell-pool 성장 = p8 mitosis), 경쟁/homeostatic 동역학으로 — 트랜스포머 확대나 data 증량 아님. 메커니즘은 흥분성 경쟁(Han 2007 CREB, Cai 2016 memory linking, Josselyn-Silva engram 할당) 순수 신경생물; 조합은 overlap 기하에서 나오지 attention 에서 안 나옴.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy: 흥분성 벡터 population, k-WTA 할당, 감쇠+linking window. (1) 순차 기억 → window 밖 분리 vs window 안 linking overlap; (2) co-allocate 된 pair → conjunctive recall composed_distinct>max_single, linking-OFF INERT; (3) engram-match AUROC known/unknown + content-ablation groundedness(콘텐츠 지우면 abstain 으로 이동); (4) 평균-흥분성 섭동 → homeostatic 1/2 복귀; (5) self-engram round-trip cos + impostor margin. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

live core/engine_cli.hexa SS-ImmuneMemory(engram cell + recall_thr) + SS-SelfIdentity(self-engram .kosmos round-trip cos/impostor) + MITOSIS engine_grow/apoptosis(할당/eviction)에 매핑 — 상당부 이미 배선. cli/anima.hexa 단일 진입 eval → g_gates g_eval_g1/g2 + SS-ImmuneMemory abstain AUROC + SS-SelfIdentity cos. byte-parity py 미러, verdict 경로 torch 0.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with immune/engram cards (H_1227/H_1231) — distinct: excitability-competitive ALLOCATION (CREB winner-take-k + memory-linking overlap) makes co-allocation the conjunction binder; the excitability-competition engram allocation is the differentiator.

toy/numpy 가 할당·linking·정직·Psi·self-margin 메커니즘에 결정적; G1 의 'linked but not co-trained' novelty 는 linking window 폭에 민감 → frozen-first sweep. production verdict 는 core 배선 byte-exact + held-out CE 전까지 DIRECTIONAL. honesty 게이트가 disinhibition(savant)과 결합 안 되도록 substrate-disjoint 유지 필수(H_1576 precedent).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
