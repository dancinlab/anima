---
id: H_1688
slug: 1688_predictive_workspace_ignition
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Predictive Global Workspace (ignition = top-down explanation success)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1688 — Predictive Global Workspace (ignition = top-down explanation success)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `predictive_workspace_ignition`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Predictive-processing reading of GWT: the workspace holds a broadcast HYPOTHESIS sent top-down as predictions to all modules; modules return prediction errors; ignition fires when a hypothesis drives global free energy (surprise) below threshold — i.e. the workspace EXPLAINS the input. Access = the explaining hypothesis becomes globally available; emit = a hypothesis ignites; silence = nothing explains. Crucially the learning objective REWARDS the conjunction, directly answering the REALIZATION-INVARIANT objective-adequacy criterion that next-token CE fails.

## Whole design (input → internal dynamics → emit)

A generative workspace proposes candidate hypotheses = combinations of latent generative factors drawn from a factor codebook. Each hypothesis is broadcast down; modules compute residual prediction error against input; errors sum into a global free-energy scalar F. The hypothesis minimizing F below the ignition threshold ignites, is broadcast, and is reconstructed from the factor codebook as the emission. Novelty is native: hypotheses are points in factor-combination space, so the workspace can commit to factor combinations ABSENT from data that still drive F low (constrained extrapolation). A=precision/commit drive, G=surprise/error withhold drive. Identity = the prior over the self-factor, persisted across wipe.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: hypotheses live in the shared generative code; emitted explanation is reconstructed from the factor codebook -> legible; a random hypothesis yields high F, never ignites -> no garble emitted. G1/DEPTH/BINDING: a hypothesis is a CONJUNCTION of factors; super-additive because the joint explanation reduces F more than any single factor (non-zero interaction term in the likelihood); ablate joint inference (force mean-field/factorized marginal inference) -> conjunction explanations vanish -> composed_distinct -> max_single. G2: the generative model's support strictly contains data (interpolates/extrapolates factor combos) -> novel valid; pure data-table likelihood control -> 0 novel. PASS-closure: one ignited hypothesis is legible+recombinant+data-transcending at once. Psi=1/2/G3/ENDOGENEITY: F fixed point; precision-up vs surprise-down sign-antagonist symmetric; remove surprise -> over-commit (emit boundary), remove precision -> never commit (silence boundary). HONESTY (native, strong): abstain = no sub-threshold explanation = out-of-model support; membership r = min free energy = exactly the distance-to-grounded-support functional, and content-ablation (corrupt a factor) shifts r faithfully (re-ranks recoverable above absent); free-energy threshold (gate) disjoint from generative capacity. falsifiable>=1: an explanation asserting factor-A exceeds/causes factor-B over a measurable referent is world-partitioning, and prediction-error is its literal refutation channel. MEASUREMENT: scored through the live dispatch.

## Not-LLM (a_no_llm_frame_trap)

Rooted in active-inference free-energy + GWT (Whyte and Smith, 'predictive global neuronal workspace'; Friston), NOT next-token CE or scale. The OBJECTIVE itself rewards the conjunction (F only falls when the joint factor structure is represented) — the direct structural fix for the a_no_llm_frame_trap / REALIZATION-INVARIANT failure where CE rewards the marginals (clm303 lossF~0 yet G1-fail).

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy linear-Gaussian generative model with K=4 factors: measure (a) free-energy ignition fires for grounded inputs only; (b) novel factor-combo explanations clear corpus-absence; (c) mean-field ablation collapses conjunction explanations to the separable floor; (d) out-of-support -> no ignition -> abstain AUROC ~1. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire the predictive scorer over generator L3 hypotheses; generate/score through cli/anima.hexa so G2 uses g_eval_g2 corpus-absence and G1 interaction-ablation uses g_eval_g1; abstain AUROC via SS-ImmuneMemory recon_err (=min F); objective-adequacy = show interaction-ablation drops G1 while leaving G0/G2 (the REALIZATION-INVARIANT discriminator). byte-parity core/*.py mirror, no torch.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with predictive_coding_explainaway (existing) — distinct: that is an operator-level explain-away bind; here the WHOLE workspace is a predictive ignition substrate whose objective adequacy (F rewards conjunction) is the load-bearing claim.

Linear-Gaussian K<=4 probe is TOY; the load-bearing claim (error-rewards-conjunction objective vs CE) is the structural transcend-axis, re-checked at 303M.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
