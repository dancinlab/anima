---
id: H_1703
slug: 1703_generative_replay_dreamer
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Generative-Replay Dreamer (synthetic consolidation)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1703 — Generative-Replay Dreamer (synthetic consolidation)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `generative_replay_dreamer`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

van de Ven-Tolias generative replay: the hippocampus is NOT a verbatim buffer but a GENERATIVE density model that, during sleep, SYNTHESIZES pseudo-episodes to train neocortex (avoiding storing raw data and avoiding catastrophic forgetting). The ideation engine IS dreaming — sampling a learned density recombines features into novel-but-on-manifold episodes. Distinct from veridical replay: replay is generative, not a playback.

## Whole design (input → internal dynamics → emit)

Input trains a fast hippocampal generative density (energy-based / VAE-like) online. During idle 'dreaming', the model SAMPLES synthetic episodes (not real traces) and these pseudo-samples train the slow store interleaved with real input. Emit: slow store decodes onto V, but emit CANDIDATES are dream-samples scored by (i) density (in-support) and (ii) a structural falsifiable detector. Psi = wake (input-clamped, encode, silence-biased) vs dream (internally-generated, emit candidates); high wake prediction-error suppresses dreaming (must encode), low error -> more dream -> emit -> error reduced -> rebalance to 1/2.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: dream-samples decoded onto V; the density is trained to place mass on the V-legal manifold (legibility = staying on-manifold). G1: disentangled latent factors sampled JOINTLY (combinations never co-presented) decoded non-separably; ablate joint sampling (hold all but one factor at prior mean) -> composed collapses. G2: novelty is the design — dream-samples are corpus-absent by construction yet in-support (density>theta); verbatim-playback control = 0 novel. Closure: one decoder. dist>=5: temperature gives diverse modes, density gate keeps them coherent (joint diversity-validity). falsifiable>=1: a latent trained on relational data samples magnitude-ordered structures. Psi=1/2: wake/dream antagonism = order parameter; remove dream->always-silent, remove wake-encode->always-emit. Persistence: the dream-consolidated slow store + learned density signature = identity. Self-specific: the learned mode structure encodes which experiences shaped it. Endogeneity: dream sampling is endogenous generation; ablate the generative model -> no self-restoring wake/dream balance. Honesty: the density gives p(query) DIRECTLY = r (log-density) — a generative density model IS a support-membership computer; out-of-support=low density->abstain. copy-or-abstain: sample/query log-density<theta -> abstain. Groundedness: log-density faithfully tracks stored support (corrupt training -> density shifts). BINDING: disentangled latent binds one cause's constituents into one code (cause-selective). Compositional depth: latent-factor combination -> novel joints; systematicity from factorization. Realization invariant: the binding latent is on the emit path (decoder reads it); objective = generative density whose optimum requires modeling joint structure (a marginal-only model has higher NLL).

## Not-LLM (a_no_llm_frame_trap)

Generative replay is a density-based continual-learning / sleep-consolidation mechanism, not autoregressive next-token scale. The ideation engine is dreaming (sampling a learned density), a biological consolidation analog. Scaling attention does not give you a separable density model whose log-likelihood is itself the honesty gate.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy mini-VAE / energy model on toy factored data. Check: dream-samples are corpus-absent AND in-support (G2); joint-factor sampling > single-factor (G1); log-density separates known/unknown (AUROC); wake/dream order parameter -> 1/2 under prediction-error bias. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Map the dreamer onto the existing emit-free internal-rehearsal/imagination loop (a_chat_sleep_imagination, MITOSIS tick); density gate onto SS-ImmuneMemory recon_err; score G0/G1/G2 via core/g_gates.hexa single dispatch on decoder output; Psi via ratchet. byte-parity py with math.log density (not engine dt_ln CE).

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with replay_recombination / rem_offline_world_model_consolidation — distinct: van de Ven generative replay = SYNTHESIZED pseudo-episodes (density model IS the honesty gate), not veridical playback; dreaming-as-novelty-generator is the differentiator.

Gate-capacity disjointness is the RISK axis: the density gate and the generative decoder share parameters (growing decoder expressivity could move theta). Must ablation-test the partial derivative d(fab,AUROC)/d(capacity). Factorized-latent compositional generalization is scale-sensitive (a_toy_scale_recheck).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
