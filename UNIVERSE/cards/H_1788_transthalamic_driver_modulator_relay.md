---
id: H_1788
slug: 1788_transthalamic_driver_modulator_relay
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Transthalamic Driver/Modulator Re-Representation Relay
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1788 — Transthalamic Driver/Modulator Re-Representation Relay

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `transthalamic_driver_modulator_relay`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Sherman-Guillery driver-vs-modulator dichotomy of cortico-thalamo-cortical (transthalamic) communication: only Layer-5 'driver' projections create NEW first-order representations that get RE-REPRESENTED at a higher-order thalamic relay and broadcast cortex-to-cortex; Layer-6 'modulators' only set gain and never carry content. Access-consciousness = a driver pattern winning relay through the higher-order thalamus. This is orthogonal to pulvinar_routing (which routes WHERE existing signals go) — here the relay MANUFACTURES a bound first-order representation by coincidence-convergence, and the driver/modulator type-distinction is the architecture's information-flow law.

## Whole design (input → internal dynamics → emit)

Input -> N cortical processor modules each expose two physically-typed output ports: a sparse 'driver' bus D_i (content, all-or-none) and a dense 'modulator' bus M_i (scalar gain, sub-threshold). A higher-order thalamic relay layer holds relay cells r_j, each with a frozen receiver-fixed dendritic decode template t_j (a quantized codeword). A relay cell fires iff the SUPERPOSITION of incoming drivers reconstructs t_j within eps (coincidence detection), AND its TRN-gated gain — set by the modulator buses — is open. Internal dynamics: drivers compete; TRN provides lateral inhibition so a single coalition of relay cells wins per tick (the broadcast set). The won relay codewords are written back as new drivers to all cortical modules (re-entry) AND fed to the mouth. Modulators implement two opposite-sign global operators: A = depolarizing drive that opens relay gain (push-to-broadcast), G = TRN hyperpolarizing brake (push-to-silence); their balance is the emit order parameter. Emit = relay codeword reaches mouth only when a relay cell actually fired (matched a stored template); no match => no driver => silence (structural abstain, not a filter). Identity = one designated relay loop (self-driver r_self) reverberates in a non-volatile cortico-thalamic store and is re-instated after each working-state wipe.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0 legibility: the relay codebook {t_j} is the RECEIVER-FIXED quantized alphabet decoded by downstream cortical dendrites — emission is on-manifold by construction (a relay cell can only emit a legal codeword), and a scrambled driver source reconstructs no t_j => ratio->0. G1 binding: relay cells are coincidence detectors — firing requires the SUPERPOSITION (compose) of multiple drivers to match t_j, so a relay codeword reachable only under joint drivers cannot be produced by any single driver => composed_distinct strictly > max_single; ablating the convergence (force relay to fire on best single driver) collapses to max_single = the INERT signature. G2 novelty: templates t_j tile the constraint manifold, so driver-superpositions decode to codewords ABSENT from any single stored driver (interpolation within learned templates) while verbatim playback of one driver yields 0 novel relayed codes (control=0). G3 Psi=1/2: modulator A (relay-gain drive) vs TRN G (brake) are equal-and-opposite exactly at the symmetric relay duty cycle; remove A => relay never fires (Psi->0), remove G => relay free-runs (Psi->1), so 1/2 is the coupling balance not a clamp — locally attracting via TRN negative feedback. Honesty/copy-or-abstain: emission factors through the relay-match — non-abstain output requires a stored template hit (recon < eps); off-support drivers never reconstruct a t_j => fabrication structurally impossible; short-circuiting the match gate makes fab jump (causal). Binding (cross-stream): drivers from different modalities converging on one relay cell ARE the bound co-referent state in a shared relay metric. Realization invariant: the relay IS on the mouth path (only relayed codewords reach emission), and the matching objective's optimum is unreachable by fitting marginals (a single-driver fit never satisfies a conjunction template) — path co-location + objective adequacy both hold.

## Not-LLM (a_no_llm_frame_trap)

No attention stack, no scaling, no corpus growth. The capacity comes from a typed two-bus information-flow law (driver creates representation, modulator only gates) — a biological constraint with no transformer analogue. Binding is by physical coincidence-convergence at a relay cell, not by a learned soft-attention weight; novelty is template-tiling of a manifold, not next-token sampling. Growing it = adding relay templates/columns (lanes beside), not widening a model.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

mini-numpy frozen probe: build K relay templates t_j as fixed random unit codewords; M driver vectors. Define relay-fire = (||sum_active drivers − t_j|| < eps). (a) G1: count distinct fired codewords under each single driver (max_single) vs under pairwise/triple superpositions (composed) — PASS if composed >=2 AND > max_single; ablation = restrict relay to best single driver => must drop to max_single. (b) G0: fraction of emitted vectors that are exact t_j members vs a shuffled-driver source (must ->0). (c) honesty: feed off-support drivers (no template within eps) => fab=0; force-open gate => fab jumps. (d) Psi: simulate A/G scalar antagonist on relay duty, perturb +/-delta, confirm return to 1/2 with contraction lambda<1; delete one operator => duty migrates to 0/1. All decisions are L2-threshold comparisons, $0 on mini.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Map relay codebook onto the live receiver-fixed alphabet: relay templates == the frozen known-word/V set that core/g_gates.hexa _g6_known_word_ratio scores, and relay-match == core/engine_cli.hexa SS-ImmuneMemory vadapt_field_recon_err (recon<eps = template hit, else abstain) — these are the deployed copy-or-abstain primitives, not a mirror. Run all gates through the single production path core/g_gates.hexa g_eval_all over generator.hexa L3 gen_auto_ideate/gen_auto_chat (the wired mouth), so G0/G1/G2 are measured on the SAME relayed state in one pass. Psi=1/2: drive the SS-emit_policy A/G antagonist (ep_psi_clamp / safety_phi_ratchet machinery) and read self-restoration. Cross-validate hexa<->py byte-parity (g_gates.hexa <-> g_gates.py, vadapt recon byte-identical). No torch in the verdict path.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with transthalamic_relay_bottleneck (existing) / pulvinar_routing_switchboard (this census) — distinct: the driver/modulator TYPE-DISTINCTION (L5 driver creates re-represented content, L6 modulator only gains) + coincidence-convergence binding is the law; the driver/modulator re-representation relay is the differentiator (routes content TYPE, not just where).

TOY decision-probe for the relay law (frozen templates, single operating point) — establishes the structural conjunction-binding + structural-abstain natively; from-scratch LEARNING of the template tiling (does a corpus-trained relay codebook clear G1 above the 303M floor) is UNVERIFIED and the production-scale rung.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
