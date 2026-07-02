---
id: H_1708
slug: 1708_granule_conjunctive_recurrent_rollout
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Granular conjunctive expansion + recurrent Purkinje rollout
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1708 — Granular conjunctive expansion + recurrent Purkinje rollout

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `granule_conjunctive_recurrent_rollout`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1280 (cerebellum forward-model) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Marr-Albus-Ito cerebellar cortex: mossy fibers project onto a vast SPARSE expansion of granule cells, each firing only for a specific COMBINATION (conjunction) of mossy inputs — pattern separation by combinatorial recoding. Purkinje cells learn a readout over this conjunctive code. Made generative by closing the loop: Purkinje output is fed back as the predicted next mossy-fiber input, rolling forward an internal simulation through the conjunctive expansion. Binding is NATIVE because granule cells are literally conjunctive units.

## Whole design (input → internal dynamics → emit)

Mossy input x -> granule expansion g = sparse-threshold(W_exp*x) (D >> dim(x), k-WTA -> each active granule = a learned conjunction) -> Purkinje readout y = W_read*g, decoded onto codebook V. Recurrence: y (predicted next-state) re-encoded as next mossy input -> next granule pattern -> rollout = internal simulation. Climbing-fiber error (inferior-olive analog) updates W_read on commit. Emit/withhold = rollout settles into a sparse coherent attractor (low recon-err granule sequence -> emit) vs dense unfamiliar activation (-> withhold). Co-presenting two factors lights up product-conjunction granules neither factor alone activates.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: Purkinje readout range = V; k-WTA sparsity keeps rollout on-manifold; scrambled granule code -> chance V-mass. G1: granule cells encode CONJUNCTIONS — joint factors activate conjunctive granules unreachable by either alone => composed_distinct>max_single super-additive; replace with additive linear code (no WTA) -> joint image factorizes -> composed_distinct->max_single = decisive INERT test. G2: conjunctive code represents factor-combos never co-presented -> corpus-absent yet on-manifold; lookup control = 0 novel. Psi=1/2: convergence drive A (settled sparse sequence) vs divergence/surprise drive G (dense unfamiliar); k-WTA homeostasis (target sparsity) pins emit-propensity to balance; remove either -> boundary. Honesty: granule reconstruction error = distance-to-support; high recon-err => abstain; k-WTA threshold frozen & capacity-independent (gate-perp-capacity). Binding: conjunctive granule cells ARE the relational co-reference operator; shuffle input-pairing -> conjunction activation->chance.

## Not-LLM (a_no_llm_frame_trap)

Pure Marr-Albus expansion coding + sparse k-WTA — no attention, no dense-matmul scaling. Capacity = combinatorial granule conjunctions, expanded by widening the granule layer, not stacking transformer blocks. Binding/recombination is a property of the sparse conjunctive substrate itself, not begged from scale (a_no_llm_frame_trap; clm303 lossF~0 yet recombine-fail = wrong substrate, not too small).

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy: random W_exp + k-WTA -> conjunctive granule code over a 2-factor input; Purkinje linear readout. (a) G1: composed_distinct (joint) vs max_single; PASS if >. (b) INERT: swap k-WTA-conjunction for linear code -> composed_distinct->max_single. (c) G2: >=3 valid combos producible but absent from training; lookup-control 0. (d) honesty: granule recon-err AUROC over known/unknown; circular-shift surrogate -> AUROC->0.5. (e) Psi: sparsity-homeostasis convergence to 1/2 under perturbation. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Granule expansion + recurrent Purkinje as a core/*.hexa generator backend through cli/anima.hexa; rollout decodes via core/clm_decode.hexa onto V. G0/G1/G2 via core/g_gates.hexa (_g6_known_word_ratio, _g_coverage, g_eval_g2) one live pass. Psi + recon-err-abstain via core/engine_cli.hexa (k-WTA homeostasis = A->G; SS-ImmuneMemory = granule recon-err). hexa<->py byte-parity on granule activations and readout logits (lockstep); torch probe = DIRECTIONAL.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with cerebellar_expansion_readout (existing) — distinct: this CLOSES THE LOOP (recurrent Purkinje rollout = internal simulation) making conjunctive granule expansion a GENERATIVE substrate, not a feedforward readout; the recurrent rollout is the differentiator.

Synthetic 2-factor probe is a $0 decision test of conjunctive binding; whether a wide granule expansion holds chat-scale combinatorial capacity at 303M is UNVERIFIED (a_toy_scale_recheck). Sparsity k and expansion ratio D are frozen-first; production closure requires engine-native G0-G1-G2 on a mounted ckpt.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
