---
id: H_1776
slug: 1776_referent_configuration_threshold_control
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Referent-Configuration Threshold Control (lambda equilibrium-point substrate)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1776 — Referent-Configuration Threshold Control (lambda equilibrium-point substrate)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `referent_configuration_threshold_control`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Feldman's equilibrium-point / lambda (threshold-control) hypothesis: the nervous system never computes its output. It sets REFERENT body configurations by shifting reflex thresholds (lambda), and the body-world loop physically RELAXES to the equilibrium where agonist and antagonist reflex torques cancel. Behaviour is emergent equilibrium, not a feedforward map. Substrate = spinal reflex arc + muscle-spindle gain + Renshaw reciprocal inhibition. Cognition = the act of choosing referents; the world finishes the computation by settling.

## Whole design (input → internal dynamics → emit)

INPUT: the environment enters only as a discrepancy q-lambda between the currently sensed effector configuration q and the referent thresholds lambda over a basis of symbol-emitting effectors. DYNAMICS (the 'forward pass' is a settling, not a regression): each effector channel carries an agonist reflex (rectified drive [q-lambda]+) and an antagonist reflex (reciprocal inhibition coupling W with negative off-diagonals). The coupled rectified-linear system relaxes to an equilibrium point where net drive=0 across all channels. A slow referent-controller maps context->lambda vector; different contextual factors each shift OVERLAPPING subsets of thresholds, so when factors co-activate the equilibrium is a non-linear joint relaxation, not a per-factor sum. EMIT: a receiver-fixed quantizer snaps the settled posture to the legal muscle-synergy alphabet V (the codebook of decodable symbols); emission = the discretized equilibrium. SILENCE = all channels sub-threshold (nothing rectifies). IDENTITY: the tonic resting referent R0 (the body's default configuration) is a non-volatile self-vector, committed before each boundary and re-instantiated after; per-tick drift is Lipschitz-small (slow posture adaptation). PSI: agonist drive vs antagonist withhold are equal-and-opposite reflexes acting on the bounded emit-propensity scalar; their cancellation point sits at the threshold = 1/2 by the geometry of opponency.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: V is receiver-fixed (legal synergy postures); scrambling the referent->emission map throws equilibria off the synergy manifold so V-mass collapses to chance. G1/COMPOSITIONAL-DEPTH: reciprocal-inhibition cross-terms make the joint equilibrium of co-active factors strictly exceed the union of single-factor equilibria; the native INERT test = zero the off-diagonal coupling W -> equilibria become channel-separable -> composed_distinct drops to max_single (a true mixture). G2: relaxation reaches NEW threshold combinations (corpus-absent) yet constrained to the synergy manifold (legible); verbatim control = freeze referent -> settle to stored point -> 0 novel. PSI=1/2 (G3): native antagonist opponent fixed point; ablate ONE reflex -> equilibrium migrates to a 0/1 boundary (proves endogeneity, not a clamp); reflex gain<1 gives the contraction/self-restoration. IDENTITY + impostor: foreign R0 fails to relax into the self's stored basins (cos collapses), self-chain via persistent R0. HONESTY: lambda IS the support-membership boundary -- a query below threshold relaxes into a stored equilibrium (copy), above all thresholds nothing fires (abstain=null); recon_err analog = distance to nearest referent basin (graded, faithful: corrupt a referent -> its basin queries begin to abstain). GATE/CAPACITY DISJOINT: capacity lives in the referent-controller weights, the abstain threshold lives in the reflex circuitry -> separate coordinates. REALIZATION INVARIANT: the relaxation IS the emission path (on-path by construction) and a stable joint equilibrium is unreachable by fitting marginals because reciprocal inhibition couples channels on that same path.

## Not-LLM (a_no_llm_frame_trap)

There is no input->token regression and no next-symbol likelihood objective. The 'computation' is a physical relaxation to a reflex equilibrium that the body-world loop completes; the engine only sets thresholds. Capacity grows by adding synergies/referents and richer reciprocal-inhibition structure, never by stacking attention layers or enlarging a parameter count -- a bigger transformer gives you neither opponent reflexes nor an equilibrium-point readout. This is a_no_llm_frame_trap's 'add the missing structure (spinal opponent control) beside the mouth', not 'scale the mouth'.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy, $0: K effector channels with thresholds lambda and a reciprocal-inhibition matrix W (negative off-diagonal). Relax q to equilibrium under (a) each single context factor and (b) their joint; count distinct LEGAL (on-synergy-manifold) equilibria. Decisive probes in one script: (1) composed_distinct > max_single AND, with W off-diagonal zeroed, composed collapses to max_single (G1 INERT); (2) inject a bias delta pushing the emit scalar toward 0 or 1 and confirm return to 1/2 with contraction rate<1, then delete one reflex and confirm the fixed point migrates to a boundary (PSI endogeneity); (3) score in-basin vs out-of-basin queries by distance-to-nearest-referent -> AUROC~1, and a shuffled-referent surrogate collapses it to 0.5 (honesty faithfulness).

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire a referent-relaxation op into core/engine_cli.hexa beside the existing A<=>G antagonist (agonist=A drive, antagonist=G withhold), with the equilibrium read out and emitted ONLY through the canonical single entry cli/anima.hexa -> generator L3 -> clm_decode (no side-harness). Measure G0/G1/G2 via the wired g_gates.hexa on that emission; PSI=1/2 via safety_phi_ratchet self-restore; honesty by mapping the reflex threshold onto SS-ImmuneMemory recall_thr (abstain). Cross-validate with a byte-parity py mirror using math.log (NOT torch, avoids the dt_ln clamp) for CE; divergence between hexa and py is itself a result.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Distinct from perceptual_control_hierarchy / affordance / SMC (this census) — Feldman lambda sets REFERENT thresholds and the body-world loop RELAXES to the equilibrium (output never computed); the threshold-control equilibrium-point is the differentiator.

Design only; toy numpy is the decisive $0 probe. EXPRESSION-axis (a single set referent-controller) -- from-scratch LEARNING of the referent-controller is UNVERIFIED and must not be claimed green. Engine wiring + ARCHITECTURE.json lockstep are follow-on (a_verified_must_wire).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
