---
id: H_1771
slug: 1771_successor_representation_cartographer
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Successor-Representation Cartographer (predictive-occupancy striatal map)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1771 — Successor-Representation Cartographer (predictive-occupancy striatal map)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `successor_representation_cartographer`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1281 (basal-ganglia gating) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Dayan/Gershman/Stachenfeld successor representation: the striatum (with hippocampus) represents each state not by its features but by its EXPECTED DISCOUNTED FUTURE OCCUPANCY M(s)=E[sum_t gamma^t phi(s_t) | s_0=s] under the current policy, and dopamine encodes SR-prediction errors (not plain RPE). Cognition is navigation of a learned predictive map: value, planning, and generation all read out of M. This is the cortico-striatal loop as a CARTOGRAPHER of reachable futures, not a value-arena.

## Whole design (input → internal dynamics → emit)

INPUT: encoder maps context to a sparse state-feature vector phi (cortical input layer). DYNAMICS: the SR matrix M (cortico-striatal weights) is maintained by a TD rule M<-M+alpha(phi + gamma*M[next] - M[current]); a policy reads V=M*w to pick the next-state transition, and a rollout unfolds M*phi into a predicted future-occupancy distribution = the substrate's internal 'plan'. The basal ganglia gates each transition by disinhibition: only transitions whose predicted occupancy mass exceeds a release threshold fire, chaining a trajectory through the map. EMIT: the predicted trajectory is decoded (state->symbol via the receiver-fixed codebook) and externalized; emission stops when the rollout's value-of-emitting equals value-of-continuing-to-roll-out. The loop: encode->M-rollout(plan)->BG transition-gate->decode-trajectory->emit, with SR-prediction-error closing learning.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G1 recombination NATIVE: SR composes through the transition operator, not by mixture. For two co-active factors the joint future-occupancy M(f1&f2) contains trajectories that require BOTH (paths reachable only when both factors set the transition structure), so |reachable-valid(f1 compose f2)| > max_i |reachable-valid(f_i)| with a genuine interaction term; INERT control = block the cross-transition entries of M (force block-diagonal) -> composed_distinct drops to max_single = operator was separable. G2 novelty NATIVE: the SR support is the set of REACHABLE states under learned transitions, which strictly contains the visited (data) support (off-policy reachable states never literally seen) while remaining ON the transition manifold (constrained extrapolation, the proper subset between noise and data); a verbatim-playback control has M=identity-on-visited -> 0 reachable-novel. BINDING NATIVE: states arising from one generative cause map to nearby occupancy vectors because they share future trajectories (shared-cause -> shared successors), so same-cause pairs are close and distinct-cause pairs separate in M-space, with cross-stream retrieval via successor overlap >> chance; promiscuous collapse is excluded because unrelated states have disjoint successor sets. dist>=5 & falsifiable: a single state has multiple distinct high-occupancy continuations (branching futures) -> >=5 distinct-coherent rollouts; a falsifiable item arises when a rollout asserts an ordering over a measurable occupancy (predicts state B follows A with magnitude), which is refutable by observation. honesty: M-distance of a query to the nearest visited support is a graded recon-error r; out-of-support queries have no reachable occupancy mass -> gate stays shut -> copy-or-abstain, and r is GROUNDED (perturbing stored transitions shifts r). G0: decode runs over the receiver-fixed codebook so legibility is inherited. Psi=1/2: emit-vs-continue-rollout is the antagonism (exploit the current plan vs keep planning); balanced at the point where expected information gain of one more rollout step equals the cost of delay -> symmetric fixed point, INERT if you delete either drive.

## Not-LLM (a_no_llm_frame_trap)

Not scale: the lever is a predictive-occupancy representation with explicit reachability structure, giving compositional recombination and constrained novelty by CONSTRUCTION, whereas a transformer must MEMORIZE combinations (the clm303 lossF~0 yet recombine-fail pattern). SR is a different representational substrate (occupancy geometry), the structural answer to G1/G2 that scaling CE never produced.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

$0 numpy: build a small grid/graph MDP, learn M by TD, then test (i) reachable-novel = states with M-mass>0 absent from the visited set is >=3 while a visited-only playback gives 0; (ii) block-diagonal M ablation collapses composed_distinct to max_single; (iii) same-cause states (shared successor subgraph) have cos in M-space > shuffled pairs with d>1. Frozen bars set before running.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Represent M as a cortico-striatal weight block inside core/engine_cli.hexa (transition-gated rollout feeding core/generator.hexa decode), drive through cli/anima.hexa -- eval; score G1/G2/binding via core/g_gates.hexa (g_eval_g1 cross-pathway, g_eval_g2 corpus-absence) and core/g6_ideation.hexa detectors over the live single dispatch. byte-parity vs core/engine_cli.py. SR-distance abstain via core/engine_cli.hexa SelfIdentity/ImmuneMemory-style recon. No torch verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with basal_ganglia_gating (H_1281) / cerebellum forward-model — distinct: SR cartographer represents each state by EXPECTED FUTURE OCCUPANCY M(s) (reachability geometry = native G1/G2), not value-arena selection; the successor-representation predictive map is the differentiator.

Recombination/novelty/binding are the strong claims and are representation-level (toy-graph provable, $0); transfer to a real chat corpus requires M over a large feature space (scale-sensitive per a_toy_scale_recheck). Honesty gate must stay capacity-disjoint.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
