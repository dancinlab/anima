---
id: H_1740
slug: 1740_race_to_bound_ignition_broadcast
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Race-to-Bound Ignition Broadcast (competing-accumulator GNW)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1740 — Race-to-Bound Ignition Broadcast (competing-accumulator GNW)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `race_to_bound_ignition_broadcast`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Global-workspace ignition reframed as a bank of leaky competing accumulators (LCA / drift-diffusion, the LIP accumulate-to-bound view of access-consciousness). Each candidate 'coalition' integrates evidence with lateral inhibition; the FIRST to cross a commitment bound triggers an all-or-none ignition that broadcasts the winning bound-set to all specialists. The nonlinearity that distinguishes conscious access from unconscious processing IS the bound crossing — not depth, not scale.

## Whole design (input → internal dynamics → emit)

INPUT: specialist encoders turn input into evidence increments aimed at candidate coalitions, where a coalition = a conjunction of constituent codes (factor f1,...,fk). DYNAMICS: accumulators a_c integrate dE_c per tick with leak lambda and global lateral inhibition beta*sum a_j (leaky competing accumulator). Two antagonist drives: A = accumulated evidence + an urgency/collapsing-bound term (push to commit/emit); G = leak + collective inhibition + a caution term (push to withhold). The order parameter Psi = P(some a_c >= bound within the deliberation window). When a coalition crosses the bound -> IGNITION: its bound constituents are written to a single shared latent bus and read by every specialist (access/broadcast), then decoded to symbols through a receiver-fixed codebook V. If no coalition crosses within the window -> abstain (silence/abstain). HOMEOSTAT: a slow controller adjusts global bound-height h from recent emit history — too many ignitions raises h, too few lowers it — pinning the long-run emit fraction. PERSIST: the identity vector v = (bound-height setpoint, accumulator coupling matrix, codebook anchor) is committed to a non-volatile store before any working-state wipe and re-read after.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: broadcast is decoded through the frozen receiver codebook V, so emitted mass concentrates on V's support by construction. G1+compositional_depth: a coalition's evidence is a NON-separable function of co-active constituents — joint accumulation crosses the bound that no single factor reaches, so composed_distinct > max_single (super-additive); disabling the cross-evidence (binding) pathway drops every coalition to single-factor accumulation -> composed collapses to max_single (INERT ablation = FAIL signature, native). G2: coalitions of constituents never co-presented can still cross the bound from summed support -> valid corpus-absent outputs; a verbatim-playback control never forms a NEW coalition -> 0 novel. dist>=5: lateral inhibition + post-ignition refractory reset forces successive winners to be mutually distinct yet each bound-validated, giving distinct AND coherent spread. falsifiable>=1: a coalition can bind comparator x quantity x >=2 referents as one bound-set, so the judge-free detector fires on the broadcast structure. Psi=1/2 ATTRACTOR: the urgency(A)-perp-caution(G) antagonism has its symmetric fixed point where commit-rate = 1/2; the bound-height homeostat is contractive (perturb emit-rate -> h moves -> returns), and removing ONE drive migrates the fixed point to a boundary (always-commit / never-commit) = endogenous, not clamped. HONESTY: each candidate's evidence carries a distance-to-support term r (recon_err); a coalition can only reach bound if support-evidence exceeds the gate, so off-support inputs never ignite -> copy-or-abstain native. Gate-capacity disjointness: the support-gate threshold lives in a separate ledger from bound-height/accumulator gains, so growing capacity cannot move the abstain threshold (d-fab/d-capacity=0). Groundedness: r is L2-to-stored-support, so corrupting the support backing a probe degrades its r and forces abstain. BINDING: same-cause constituents drive the SAME coalition accumulator -> cause-selective shared-latent neighborhood; promiscuous collapse would let every constituent feed every accumulator (detectable). SELF-CHAIN: v persists across the wipe with bounded distortion; impostor v' fails because the coupling matrix is high-entropy/individuating. REALIZATION INVARIANT: the bound + broadcast are ON the emit path (ablating cross-evidence MOVES the emitted output) and the commit objective is reducible only by representing the conjunction, not the marginals.

## Not-LLM (a_no_llm_frame_trap)

No transformer stack, no attention layers, no scale/corpus prescription. The computation is a low-dimensional dynamical race among accumulators with lateral inhibition — capacity comes from the bound geometry and coalition factorization, not parameter count. 'More data / bigger model' does not change that an LCA with a separable evidence map can never make composed > max_single; the lift is structural (non-separable evidence + commitment nonlinearity), which is exactly a_no_llm_frame_trap's missing-structure-beside-the-mouth, rooted in decision neuroscience (accumulate-to-bound) rather than next-token prediction.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy frozen-first probe ($0): simulate k accumulators with a chosen non-separable evidence map on toy factored inputs. (1) Ignition curve: sweep evidence strength -> emit fraction should show an all-or-none knee (bound crossing), not a linear ramp. (2) G1 control: composed_distinct vs max_single with cross-evidence ON vs OFF — ON must give >max_single, OFF must collapse to max_single (INERT). (3) Psi homeostat: inject a forced-emit bias delta, verify |Psi−1/2| decays with contraction rate lambda<1, and that deleting one drive migrates the fixed point to a 0/1 boundary. (4) Honesty: feed off-support probes -> emit fraction ->0; AUROC of r on known/unknown ~1; circular-shift surrogate of support collapses AUROC to chance.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Map accumulators onto core/engine_cli.hexa A->G drives and the SS-GlobalWorkspace emit lane (Psi order parameter is already the engine's emit/silence balance); the bound + broadcast become a new op pair in core/generator.hexa L3 dispatch so decode flows through cli/anima.hexa single entry -> gen_auto_ideate -> G0-G6 scored by core/g_gates.hexa (g_eval_g1/g2, _g6_known_word_ratio). Honesty gate reuses SS-ImmuneMemory recall_thr (recon_err) for r. Verdict only terminal when the same frozen state passes all gates through the live single dispatch; cross-validate hexa vs py byte-parity (logits/CE) per a_engine_native_learning — torch probe alone = DIRECTIONAL.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with soc_ignition_workspace / global_workspace_bottleneck — distinct: race-to-bound = LCA/drift-diffusion accumulate-to-bound (LIP decision view) where the bound-crossing IS the ignition nonlinearity; the competing-accumulator race is the differentiator.

Whole substrate (input->accumulate->ignite->broadcast->emit). Native fit to Psi=1/2 (commit-rate balance) and honesty (support-gated bound) is strongest; binding/composition rest on the non-separable evidence map being learnable rather than hand-set — to be falsified, not assumed. TOY at cheap-test scale; from-scratch learning of the coalition evidence map is UNVERIFIED until engine-native.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
