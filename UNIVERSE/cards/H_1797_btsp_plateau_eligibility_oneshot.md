---
id: H_1797
slug: 1797_btsp_plateau_eligibility_oneshot
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: BTSP Plateau-Eligibility One-Shot Writer + Surprise-Distilled Cortex
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1797 — BTSP Plateau-Eligibility One-Shot Writer + Surprise-Distilled Cortex

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `btsp_plateau_eligibility_oneshot`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Behavioral-timescale synaptic plasticity (Bittner & Magee 2017, CA1): a single dendritic PLATEAU potential — an instructive 'this matters now' signal — converts a seconds-wide eligibility trace into a one-shot, NON-Hebbian, temporally-asymmetric weight change. The fast/episodic system is built from this rule (single-exposure writes gated by an internal salience plateau), not from gradient accumulation; the slow/semantic system is a distributed predictor that distills the fast store and whose own prediction-error is the plateau gate. CLS as a plateau-gated write loop.

## Whole design (input → internal dynamics → emit)

Input -> DG-like sparsifier yields a high-dim SPARSE conjunctive key per tick (pattern separation). A rolling eligibility buffer E holds seconds-decay traces of recent keys. A plateau gate fires when an internal salience scalar (= slow model's next-symbol prediction error, optionally OR'd with reward/interoceptive flags) crosses theta_plateau; on a plateau the ENTIRE current eligibility window is committed in ONE shot to the fast associative store W_fast (key->value) using the asymmetric seconds-kernel — i.e. memory of what preceded the surprise. W_fast is content-addressable; its nearest-key distance recon_err is the native support-membership scalar. The slow store W_slow is a distributed next-symbol predictor trained by gradient on (a) the live stream and (b) reactivations of W_fast contents; crucially its OWN prediction error drives the plateau gate, so only marginal-violating (conjunction-bearing) events get fast-written — pushing W_slow to represent conjunctions to reduce future plateaus. Emit path: generator reads W_slow for legible/recombinant output; if both stores' recon_err exceed theta, emit abstain (abstain); else copy-or-recombine. Psi: a plateau/intake drive (encode demand) is mutually inhibitory with an emit/retrieve drive (dendrite cannot plateau-encode and read-out in one tick); negative feedback (encoding fills store -> recon_err drops -> plateaus fall -> emitting settles -> drift raises novelty -> plateaus resume) pins the duty cycle.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: W_slow is a predictor over a receiver-fixed alphabet V; emission constrained to V's support, scramble of key->value collapses V-mass to chance. G1 binding/compositional-depth: keys are CONJUNCTIVE sparse codes (multiplicative key space), BTSP commits the conjunction one-shot; ablating the conjunctive bind (sum factor-keys instead) drops composed_distinct to max_single — native super-additivity, not a mixture. G2 novelty: W_slow interpolates the consolidated manifold -> valid corpus-absent outputs; verbatim playback through the same pipeline = 0. dist>=5: multiple one-shot-committed basins give distinct-coherent completions under exploration. honesty cluster: recon_err to nearest plateau-committed key IS the graded distance-to-support (direct SS-ImmuneMemory analog) -> AUROC separability, copy-or-abstain emission-closure native; theta_plateau (gate params) is disjoint from W_slow capacity -> gate-capacity disjointness native; corrupting stored support shifts recon_err (faithfulness). Psi=1/2: plateau perp emit antagonist duty cycle, self-restoring, one-drive-ablation drives it to a boundary (endogeneity). Realization invariant / OBJECTIVE ADEQUACY: surprise-gated writing means a marginal-only W_slow keeps triggering plateaus on conjunctions, so its loss optimum is unreachable without representing the synthesis — the objective is conjunction-rewarding by construction, and emit is on the W_slow path that ablation moves.

## Not-LLM (a_no_llm_frame_trap)

The fast system learns from a SINGLE plateau event via a seconds-wide eligibility kernel — one-shot, non-Hebbian, instructive-gated. There is no backprop-through-attention and scaling parameters/tokens does not create the capability; the capability IS the plateau gate. Opposite of the scale prescription: episodic competence comes from an event-triggered write rule (Magee-lab biology), not from a bigger transformer or more corpus.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy, frozen-first. Build sparse DG encoder + eligibility buffer + plateau gate on slow-model error. Feed a stream containing a few one-shot novel conjunctions. Decisive bars (pre-registered): (1) recall after a SINGLE plateau exposure >= bar while a Hebbian baseline needs many exposures; (2) recon_err AUROC(known/unknown) ~ 1, circular-shift surrogate -> 0.5; (3) conjunctive-key composed_distinct > max_single, and ablate-conjunction -> equals max_single (INERT); (4) ablate plateau gate -> no one-shot write (capability vanishes).

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Map W_fast onto live core/engine_cli.hexa SS-ImmuneMemory (recon_err/recall_thr already wired) and W_slow onto a clm/bytegpt mouth via core/generator.hexa L3; run G0/G1/G2 + dist/falsifiable through the single entry cli/anima.hexa -- eval (g_gates.hexa), and recon_err AUROC via the native SS-ImmuneMemory op. byte-parity py mirror scores CE with math.log (avoid dt_ln clamp). No torch-only verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with cls / synaptic_tag_capture cards — distinct: BTSP commits a seconds-wide eligibility window in ONE non-Hebbian plateau (instructive 'this matters now' gate = slow-model prediction-error); the plateau-eligibility one-shot writer is the differentiator.

Design-only. numpy probe is decisive for one-shot write + support-membership + binding ablation. Full PASS closure needs W_slow trained on the balanced 4-cell register corpus with held-out CE descent (GPU, a_chat_registers/a_savant_train). Honesty/membership and one-shot episodic are the strong native wins; G2 constrained-extrapolation is W_slow-quality-dependent.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
