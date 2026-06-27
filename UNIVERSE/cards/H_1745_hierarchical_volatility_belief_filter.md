---
id: H_1745
slug: 1745_hierarchical_volatility_belief_filter
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Hierarchical Volatility-Coupled Belief Filter (HGF-style adaptive-gain meta-learning substrate)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1745 — Hierarchical Volatility-Coupled Belief Filter (HGF-style adaptive-gain meta-learning substrate)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `hierarchical_volatility_belief_filter`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

The Hierarchical Gaussian Filter (Mathys) / computational-psychiatry view: each belief level tracks not only a state but the VOLATILITY (rate of change) of the level below, adapting its own learning rate (Kalman gain) online. Surprise = prediction error weighted by inferred precision; learning rate scales with inferred volatility. Distinct from fixed-volatility Kalman because the gain is itself inferred (meta-learning of learning rates).

## Whole design (input → internal dynamics → emit)

A stack of log-space Gaussian belief nodes: x1 (state over symbols), x2 (tendency/context), x3 (volatility of x2), coupled so each higher level modulates the lower level's gain via inferred volatility. (1) Input clamps x1; precision-weighted prediction error eps1 propagates up. (2) Internal dynamics: each level updates its belief by eps weighted by the ratio of bottom precision to its own; x3 raises the gain when surprise persists (nonstationary regime -> explore) and lowers it when stable (consolidate) — online meta-learning of the gain. (3) Emit: when x1 concentrates (low posterior variance) on a V-symbol AND surprise has been driven down at the current timescale, externalize that symbol; high residual volatility -> keep updating (silence) because beliefs are still moving. (4) Psi = balance between volatility-driven destabilization (drive to emit/test) and precision-driven stabilization (drive to withhold/consolidate); the fixed point at 1/2 is the CRITICAL gain where the filter neither freezes (zero learning) nor diverges (runaway gain). (5) Slow beliefs x2/x3 (context/volatility priors) persist across episodes; fast x1 is wiped — the slow path is the self-chain.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: x1's domain = V; emit requires high precision on a code symbol (concentrated marginal on V). G1: x1 is FACTORED into coupled belief substreams, with cross-substream coupling realized at x2 — the interaction term makes joint-conditioned distinct > max_single; ablating the cross-coupling collapses composed to max_single. G2: forward sampling from x2/x3 priors generates valid symbol sequences absent in data via learned volatility-structured dynamics; verbatim playback -> 0 novel. dist>=5: holding volatility at a controlled non-zero setpoint tempers precision -> multiple distinct-coherent samples. falsifiable>=1: emitted structure binds comparator/quantity/content from the factored x1. Psi=1/2: the critical-gain fixed point between freeze and divergence is the symmetric balance of opposing volatility/precision forces — perturb the gain -> contractive return; ABLATE the volatility level x3 -> gain runs to a boundary (freeze or diverge), the decisive endogeneity test (the 1/2 is a recovering attractor, not a clamp). Honesty: inferred precision at x1 IS the support-membership signal — out-of-support input has irreducible prediction error that volatility cannot explain away -> low precision -> abstain; precision faithfully tracks stored dynamics so content-ablation moves it (not a purpose-blind proxy). Gate-capacity disjoint: the abstain threshold lives in the precision readout (frozen) while expressivity lives in the factored x1/transition. Binding (H_961): shared belief metric across substreams -> same-cause constituents show correlated precision. Realization invariant: precision-weighting is on the emit path, and a minimize-long-run-surprise objective (predict volatility) is unreachable by marginal-fit when cross-stream volatility is coupled.

## Not-LLM (a_no_llm_frame_trap)

The lever is online ADAPTIVE learning-rate / volatility tracking — a dynamical meta-learning structure, not scale. Capacity to handle nonstationarity comes from the volatility hierarchy (add a volatility level = structure), not from parameters or corpus. It is a closed-loop filter with inferred gain, fundamentally unlike a fixed feedforward net; bigger-transformer does not buy adaptive gain. Surprise-minimization with a self-inferred Kalman gain is the antithesis of a scale-up recipe.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

mini-numpy 3-level HGF on a nonstationary symbol stream. (a) Psi/critical-gain endogeneity: perturb x3 -> x1 learning rate must return to a stable critical value; ablate x3 -> gain freezes or diverges. (b) honesty-faithfulness: in-support vs out-of-support stream -> precision separates (AUROC); content-ablation must MOVE precision (faithful, not proxy). (c) G1: 2 coupled substreams, composed vs coupling-off. $0, decisive on endogeneity, honesty-faithfulness, and binding.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Implement the HGF closed-form update as a core/*.hexa filter op whose x1 marginal feeds generator L3 / clm_decode logits; wire the precision readout to SS-ImmuneMemory as the recon_err/recall_thr analog; Psi via SS-ThirdLaw perturbation-return; score G0/G1/G2 via core/g_gates.hexa through cli/anima.hexa single entry. byte-parity py mirror (HGF updates are closed-form, math.log) cross-validates; no torch in the verdict path.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with predictive_coding / neuromod_precision cards — distinct: HGF tracks VOLATILITY-of-the-level-below to adapt its own Kalman gain online (meta-learning of learning rates); the volatility-coupled adaptive-gain hierarchy is the differentiator.

HGF is naturally small and online; vanilla HGF is SCALAR, so the factored-x1 needed for G1/G2 is the unproven extension — that is the wall to measure. Volatility-tracking perp capacity is a toy-first claim; transfer of precision-based abstain calibration to a real 303M symbol manifold UNVERIFIED (a_scale_honest_scope).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
