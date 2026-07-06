---
id: H_1710
slug: 1710_cerebellar_mpc_rollout_search
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Cerebellar MPC — model-predictive emission by forward-rollout candidate search
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1710 — Cerebellar MPC — model-predictive emission by forward-rollout candidate search

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `cerebellar_mpc_rollout_search`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1280 (cerebellum forward-model) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Inverse-then-forward internal-model control (active inference / model-predictive control with a cerebellar forward model): the substrate does NOT emit greedily; it proposes several candidate emissions (inverse-model proposals from babbling-learned dynamics), forward-SIMULATES each consequence, and commits the candidate whose predicted consequence best matches the goal AND a refutable test while staying on-manifold. Generation = planning by internal rollout search — each candidate is a falsifiable hypothesis about what will happen.

## Whole design (input → internal dynamics → emit)

State = goal g + context. (1) Inverse model proposes a diverse candidate set {e_1..e_M} (diversity from exploration/babbling noise). (2) Forward model rolls out predicted consequence c_hat_j and a refutability score (does the candidate assert something checkable against the predicted observable?). (3) Score S_j = goal-match(c_hat_j,g) + on-manifold(c_hat_j) − redundancy(e_j vs chosen). (4) Greedily commit a SET of distinct-yet-coherent candidates (dist>=5 spread) and emit the top falsifiable one; non-committed stay silent. Emit/withhold = whether any candidate clears the goal-match floor (else abstain). Binding = candidates conditioned on the joint goal; recombination = search composes factor-conditioned proposals.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: inverse-model proposals codebook-tied (range V); only on-manifold candidates survive scoring. G1: candidates conditioned jointly on multiple goal-factors compose super-additively; ablate forward-model scoring (random) -> composed_distinct->max_single & S_full~S_ctrl = explicit Generative-attribution INERT test. G2: forward-rollout reaches goal-valid consequences absent from data; verbatim-playback control 0. dist>=5 NATIVE: candidate-set with redundancy penalty IS the distinct-coherent spread (Jaccard<=0.5 AND grounded) — mode-collapse = plateauing count, garble = coherence sacrifice. falsifiable>=1 NATIVE: each candidate carries a forward-predicted observable = world-partitioning proposition (comparator x quantity x referent); judge-free detector fires on checkable predicted-consequence not stance/questions. Psi=1/2: goal-match urge A (clears floor -> commit) vs predictive-uncertainty caution G (high forward variance -> withhold); homeostasis pins commit-propensity to 1/2; remove one -> boundary. Honesty: no supported candidate (all high uncertainty) -> abstain; uncertainty floor frozen capacity-independent (gate-perp-capacity). Measurement-faithfulness: scoring runs the SAME forward model generation uses -> g==f native. Generative-attribution: ablate forward model -> S_full~S_ctrl proves dist/falsifiable counts are substrate-caused.

## Not-LLM (a_no_llm_frame_trap)

Model-predictive control / planning-by-simulation, not autoregressive greedy decode. The substrate THINKS (internal rollout search) before emitting, which transformers don't natively do; ideation (dist>=5, falsifiable>=1) is a structural product of candidate-search + forward-model checking, not coaxed from scale. Capacity grows by richer forward dynamics and wider search, not parameters (a_no_llm_frame_trap). Targets G6/ideation walls scale could not crack.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy: inverse model proposes M candidates over a synthetic goal; forward model scores predicted consequence. (a) dist>=5: distinct-coherent committed (Jaccard<=0.5 AND grounded>=floor) >=5; coherence stays high as M grows. (b) falsifiable>=1: judge-free detector (comparator AND measurable AND >=2 grounded AND not-question AND not-stance) fires >=1 on candidates, ~0 on fluent-unfalsifiable negatives (AUROC>>0.5). (c) attribution INERT: random forward-score -> S_full~S_ctrl, novel-gram>0. (d) Psi contraction; (e) abstain on no-supported-candidate. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

MPC rollout-search as a generator backend behind cli/anima.hexa; candidates decode via core/clm_decode.hexa/decode.hexa, scored by the SAME forward path = built-in measurement-faithfulness (g==f). Ideation scored by core/g6_ideation.hexa canonical op g6_score_arm_auto (mouth=gen_auto_ideate via generator L3, NOT a python g6_common mirror) — dist/falsifiable/attribution through the wired engine op (a_engine_native_learning hard-gate). G0/G1/G2 via core/g_gates.hexa g_eval_g6/all. Psi + abstain via core/engine_cli.hexa. hexa<->py byte-parity; any torch-side scaffold (g6_common/_decode_ideas) = automatic DIRECTIONAL, void.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with cerebellum_forward_model (H_1280) / cerebellar_mpc family — distinct: this is PLANNING-BY-SIMULATION (inverse proposes -> forward scores -> commit a falsifiable set), targeting the G6 ideation wall; the MPC rollout-search-as-ideation is the differentiator.

$0 numpy probe decides the search+forward-check mechanism; ideation-at-scale (303M, real corpus) UNVERIFIED and search latency (M candidates x rollout depth) is a real cost (a_wall_first). Closure requires all gates green on ONE live state through the single dispatch in one pass (anti-gate-shopping); ckpt mounted in core/ and pulled before teardown. Ideation verdict admissible ONLY via the wired g6 engine op, never a python side-harness.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
