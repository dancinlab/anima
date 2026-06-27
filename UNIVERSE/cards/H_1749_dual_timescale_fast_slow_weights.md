---
id: H_1749
slug: 1749_dual_timescale_fast_slow_weights
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Two-Speed Synaptic Substrate (fast Hebbian overlay + slow consolidated base)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1749 — Two-Speed Synaptic Substrate (fast Hebbian overlay + slow consolidated base)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `dual_timescale_fast_slow_weights`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

CLS realized AT THE SYNAPSE, not as two boxes: every connection W = W_slow + g_fast*W_fast. W_slow is the consolidated neocortical/semantic base (slow gradient/Hebbian-EMA, persistent, learns the generating manifold). W_fast is the hippocampal episodic overlay — a rank-limited, exponentially-DECAYING one-shot Hebbian outer-product written per episode (a sliding episodic window). One forward pass reads both; recall of a fresh episode = fast-weight resonance (near-verbatim), generalization = slow base. Consolidation = the slow base slowly distills whatever the fast overlay keeps re-presenting (interleaved), so the overlay can decay without forgetting. Complementarity is a single weight decomposition, not a module pair.

## Whole design (input → internal dynamics → emit)

Input->key/state h. Forward y=f(W_slow*h + g_fast*(W_fast*h)); W_fast updated Delta=eta*(post outer pre), decayed by lambda each tick. Emit = symbol distribution over frozen codebook V from y. The gain g_fast in [0,1] is the order parameter: g_fast->1 = episodic-recall-dominated emission (copy from recent store, the built-in verbatim mode); g_fast->0 = semantic-generative emission from the manifold. Two opposite-sign controllers set g_fast: episodic-drive A (recency/novelty pressure to externalize the fresh trace) and consolidation-drive G (semantic-coherence pressure to withhold/generalize). Offline/idle, W_slow does interleaved EMA updates toward what W_fast reliably reconstructs (transfer), then W_fast decays.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

HONESTY native: W_fast is an explicit content store; r(query)=resonance/recon-error of W_fast*h = support-membership (known recent episodes resonate low-r, unknown high-r) -> AUROC->1; copy-or-abstain = emit abstain when neither overlay resonates nor slow base passes confidence; gate-capacity disjoint because abstain theta lives on the r-distribution while expressivity lives in W_slow rank (d-fab/d-W_slow_capacity=0); groundedness because r literally = W_fast reconstruction (corrupt the stored episode -> r shifts). RETRIEVAL CONTROL is a literal operating mode: g_fast=1, W_slow-gain=0 emits ONLY stored episodes => 0 corpus-absent (the G2 mandatory control arm is built into the substrate). G2 novelty: slow base internalized constraints -> emits valid off-data points. G1 recombination/BINDING: two conditioned factors project into the SAME shared hidden layer before readout; the nonlinearity f over summed W_slow*h carries the non-separable cross term -> composed_distinct>max_single; interaction-ablation = force readout to max/concat of single-factor projections (block shared-hidden mixing) -> drops to max_single. COMPOSITIONAL DEPTH = that shared-hidden conjunction + systematicity from factored W_slow. REALIZATION INVARIANT: emission reads both matrices on the very path that generates (on-path), and the consolidation objective is defined over W_fast COMPOUNDS (interleaved replay of compound episodes) so CE-on-marginals alone can't minimize it -> directly defuses the clm303 lossF~0-yet-recombine-fail trap. Psi=1/2: g_fast is the bounded scalar, A and G opposite-sign; fixed point at A=G->1/2, contractive (over-emit depletes recency->A down; over-withhold raises unconsolidated tension->A up), Lyapunov |g_fast−1/2|; endogeneity by INERT test (remove A or G -> g_fast runs to a boundary = always-copy/always-generalize). SELF-CHAIN: identity v = a protected, non-decayed low-rank component of W_slow surviving the W_fast wipe across the session boundary; Lipschitz-small drift = connected moving chain; ablate the anchor -> cross-boundary cos->chance; high-entropy anchor -> impostor cos~0. CLOSURE: G0/G1/G2 co-located in one emission map under one g_fast setting; G0 from V-tied CE-trained readout (scramble h->emit collapses ratio). dist>=5 from residual entropy across g_fast/temperature + multi-attractor W_slow; falsifiable>=1 from the same factor-composition (comparator x magnitude x referents). Measurement-faithfulness: g_fast is part of the deployed forward, so the measured path = deployed path.

## Not-LLM (a_no_llm_frame_trap)

Not scale/attention: a transformer has ONE timescale (weights frozen at inference); here the episodic capability is RUNTIME-plastic fast weights decaying over a Hebbian overlay, a CLS two-timescale synaptic decomposition from biology. No corpus increase or extra attention layer creates a decaying one-shot store; the lever is the W_slow+W_fast split itself (a_no_llm_frame_trap — structure beside the model, not a bigger model).

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy mini d=64: W_slow EMA-trained on a factored toy grammar (color x shape), W_fast = decaying Hebbian outer-product. Frozen-first probes: (a) g_fast=1 -> verbatim recall yields 0 novel (control arm sanity); (b) tuned g_fast -> composed_distinct(color compose shape) >=2 AND >max_single (G1) and drops to max_single when shared-hidden mixing is blocked (interaction-ablation); (c) perturb g_fast off 1/2 -> restoration with lambda<1; (d) ablate anchor row, simulate W_fast wipe -> cross-boundary cos->chance vs ~1.0 with anchor. All $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Maps onto live core/: W_fast overlay ~ SS-ImmuneMemory/OsmoticStore (osmotic_learn writes, osmotic_retains = resonance r, adapt_field_recon_err/vadapt_field_recon_err); slow base ~ .clm mouth via core/generator.hexa gen_auto_backend. Run cli/anima.hexa eval (single entry -> gen_auto_ideate/gen_auto_chat) -> core/g_gates.hexa g_eval_g0/g1/g2 + g6_score_arm_auto (_g6_is_falsifiable/_g6_jaccard/_g6_known_word_ratio); retrieval control = g_fast=1 mode through the SAME dispatch. Psi via safety_phi_ratchet perturbation trace; self-chain via core/engine_cli.hexa self_new/self_drift/self_cos/self_anchor/self_reset round-trip; honesty via osmotic_retains AUROC + fab on out-of-support. Byte-parity core/*.py mirror (g_gates.py/engine_cli.py) cross-validates — no torch-only verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with cls_replay_consolidation (this census) / OsmoticStore — distinct: CLS realized AT THE SYNAPSE as W=W_slow+g_fast*W_fast (one weight decomposition, g_fast as Psi order parameter), not two boxes; the dual-timescale synaptic overlay is the differentiator.

Toy numpy first (a_toy_scale_recheck): fast-overlay rank & decay lambda are scale-sensitive; toy GREEN is directional, transfer to 303M unverified until an engine-native fire on a live ckpt re-measures the same frozen bars. Overlaps OsmoticStore — wire into it, don't duplicate.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
