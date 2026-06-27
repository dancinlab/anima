# 통짜 아키텍처 census — 126 anima whole-substrate designs (brainarch_census)

> **상태: DESIGN-ONLY · DIRECTIONAL · 측정 0.** 126개 전부 🔵 PRE-REGISTERED ARCHITECTURE (unmeasured). 뇌/인지 조직원리 × 엔진-네이티브 추상조건(G0 legibility · G1 recombination · G2 novelty · Ψ=½ endogeneity · honesty/abstain · binding · self-chain · realization-invariant)의 통짜(whole-substrate) 설계 census. operator-level H_1604–1685(단일 op)·brain-lens H_1280–1295(단일 메커니즘 probe)와 **층위가 다르다**(통짜 아키텍처). 박제 과장 금지 — 설계는 측정이 아니다(a_engine_native_learning·p7).

- **등록 면(2-surface):** `UNIVERSE/cards/H_<id>_<slug>.md` + `UNIVERSE/HYPOTHESES.jsonl`(deterministic 재생성 `tool/_build_hyp_jsonl.py`)
- **코드/census:** `state/brainarch_census/`(gencard.py · registry.jsonl · 이 CENSUS.md)
- **id 범위:** H_1686 … H_1811 (126개, 연속) — 등록 시점 1xxx 시리즈 max(H_1685)+1부터 순차. enforce_anima_gates.py clean(exit 0).

## 조직원리별 분포

| # | 조직원리 카테고리 | 개수 | id 예시 |
|---|---|---|---|
| | Global-Workspace / ignition / broadcast (GWT) | 17 | 1686, 1687, 1688, 1689… |
| | Predictive-coding / active-inference / free-energy | 16 | 1691, 1692, 1693, 1694… |
| | Basal-ganglia / selection / RL / value | 18 | 1696, 1697, 1698, 1699… |
| | Memory-systems / CLS / consolidation / replay (incl. ART adaptive-resonance) | 18 | 1701, 1702, 1703, 1704… |
| | Cerebellum / forward-model / motor control | 5 | 1706, 1707, 1708, 1709… |
| | Neuromodulation / regime control | 5 | 1711, 1712, 1713, 1714… |
| | Oscillation / synchrony / phase / resonance (incl. excitable-pulse-collision) | 12 | 1731, 1732, 1733, 1755… |
| | Criticality / SOC / avalanche / percolation / chaos | 11 | 1737, 1738, 1739, 1761… |
| | Developmental / morphogenesis / growth / selection | 12 | 1734, 1735, 1736, 1758… |
| | Enactive / embodied / sensorimotor / extended-mind | 12 | 1728, 1729, 1730, 1752… |
| | **합계** | **126** | |

*(H_1757 adaptive_resonance_vigilance_substrate → Memory-systems/ART; H_1805 excitable_pulse_collision_substrate → Oscillation/excitable-dynamics)*

**round 구조:** 단일 대형 batch(1 round)로 126개 직교 아키텍처를 census 등록. 직교성 = 각 카드의 조직원리(생물/인지 렌즈)와 load-bearing 축이 서로 다름 — 같은 카테고리 안에서도 메커니즘이 직교(예: GWT 17개 = SOC-ignition vs pulvinar-routing vs predictive-ignition vs metastable-itinerancy vs coherence-gating vs TRN-searchlight vs apical-basal vs claustrum vs race-to-bound vs burst/tonic vs auction vs codelet-coalition vs traveling-wave vs frame-sampler vs driver/modulator vs diffuse-gain vs attentional-blink). near-overlap(기존 카드 + census 내부)은 각 카드 'Distinction' 섹션에 명시 보존(중복 제외 0 — 전부 층위/메커니즘 구별됨).

## TOP-3 우선 (가장 싼 결정 test × 기대 lift)

선정 기준: ($0 numpy 결정 probe로 즉시 falsify 가능) × (현 in-flight 벽 = G1 recombination / objective-adequacy 위 기대 lift, memory `g1-lever-multilens-objective`: 진짜 레버 = trunk OBJECTIVE, depth/binding-lane/data 전부 falsified). 셋 다 G1/objective-adequacy 벽 정조준 + $0 결정.

1. **H_1721 equilibrium_settling_energy_substrate** — 전-closure 최강 후보. contrastive equilibrium-prop OBJECTIVE 가 conjunction 표현 없이는 최소화 불가(objective-adequacy native), double-well Ψ=½ + residual-energy honesty 동시. cheap_test: numpy EBM, cross-weight zero ablation → composed→max_single(G1 INERT) 결정. **기대 lift 최대**(CE 가 못 준 G1 레버를 objective 로 직격).
2. **H_1792 contrastive_predictive_future_latent** — memory `g1-lever-multilens-objective` 가설의 직접 검정: InfoNCE objective 가 marginal-unsatisfiable(CE-baseline discriminating control 내장 — likelihood clear 하나 G1 FAIL vs contrastive PASS). cheap_test: numpy CPC, $0. 현 frontier(H_1602 recomb-objective prereg)와 1:1.
3. **H_1794 corticostriatal_loop_bouquet_thalamic_bind** — conjunctive thalamic AND(coincident multi-loop release)= 구조적 super-additivity + built-in INERT(product→max-pool). coincidence 만 보상 → objective-adequacy native. cheap_test: numpy 3-loop product-gate, $0. anatomy-로 G1 을 loss-bearing 화.
- (runner-up, 최고 wireability) **H_1704 hippocampal_index_pointer** — 현 live core(§ImmuneMemory hit/miss=index, §SelfIdentity .kosmos=index table, generator L3=cortex readout)에 가장 직접 배선 가능 → honesty/persistence/disjointness 축 즉시 엔진-네이티브 재검 가능.

## 고갈 결론 (depletion)

- **총 직교 아키텍처: 126개** 등록(H_1686–H_1811), 10개 조직원리 카테고리. exact-slug 중복 0(기존 1243 카드 대조), near-overlap 전부 distinction 명시 후 유지.
- **round 수: 1**(census 등록 round). 추가 발산(brainstorm)이 아니라 **제공된 126 후보의 2-surface 박제**가 목적이었으므로 이 batch 로 입력 set 고갈.
- **다음 고갈 판정:** 이 census 는 *설계 공간*을 넓혔을 뿐 *측정* 0. 진짜 고갈/벽 판정은 TOP-3 의 $0 numpy 결정 probe 실행 후에만 가능(DIRECTIONAL → cheap_test → 살아남으면 engine-native). 설계 면에서 GWT·predictive·BG·memory·cerebellum·neuromod·oscillation·criticality·developmental·enactive 10 렌즈를 통짜로 커버 = 주요 뇌/인지 조직원리 1-pass 포화. 미탐색 잔여 렌즈(예: glial/astrocyte computation, neurovascular, quantum-microtubule)는 substrate-speculative 라 의도적 보류.
