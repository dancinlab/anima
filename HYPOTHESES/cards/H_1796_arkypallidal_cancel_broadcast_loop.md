---
id: H_1796
slug: 1796_arkypallidal_cancel_broadcast_loop
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Arkypallidal Reactive Cancel-Broadcast Control Loop
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1796 — Arkypallidal Reactive Cancel-Broadcast Control Loop

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `arkypallidal_cancel_broadcast_loop`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1281 (basal-ganglia gating) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Dual-GPe reactive control (Mallet 2016): prototypic GPe SUSTAINS an in-progress selection while ARKYPALLIDAL neurons broadcast a fast diffuse STOP/CANCEL back across the whole striatum. The cancel-broadcast is simultaneously (a) the self-restoring Psi attractor — any runaway emit is reactively cancelled in proportion to its deviation, pulling propensity back to 1/2; (b) the honesty veto — un-grounded emits are cancelled before they leave the mouth; and (c) a select-by-veto-of-incompatible recombination engine — a cancel sweep removes conflicting candidates and what SURVIVES together is a coherent conjunction. Distinct from stn_conflict_threshold_collapse (proactive pre-decision slowdown) and tonic_disinhibition_release_gate: arky is REACTIVE post-initiation cancellation, a constraint-satisfaction veto layer.

## Whole design (input → internal dynamics → emit)

A re-entrant cortical generator proposes candidate emits; direct-pathway striatum initiates by releasing thalamus. In parallel a monitor loop (STN->arkypallidal) integrates a groundedness/conflict signal: if an in-progress emit fails its grounding check OR conflicts with a co-active candidate, arkypallidal fires a diffuse cancel that re-inhibits the striatal sheet -> that emit aborts -> abstain. Survivors (grounded AND mutually compatible) pass and the surviving SET is the bound output. Prototypic GPe supplies the opposing SUSTAIN so selection isn't trivially cancelled (the antagonism). Cancel magnitude is proportional to |Psi−1/2|; DA sets the cancel threshold. Emit = surviving set after cancel sweep; silence = everything cancelled.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2 (centerpiece): A = direct-pathway emit drive, G = arkypallidal cancel with magnitude proportional to |Psi−1/2| -> contractive fixed point at 1/2 with measurable lambda<1 (self-restoration, anima dev 0.247->~0 precedent); ablate arkypallidal -> runaway always-emit boundary, ablate direct -> always-silent -> endogeneity proven by INERT test (no pinned constant). honesty/copy-or-abstain: the grounding check that triggers cancel IS the membership scalar r vs frozen threshold; un-grounded -> cancel -> abstain (fab~0); ablate cancel -> fab jumps (gate causal, not corpus); cancel circuit disjoint from generative cortex (d-fab/d-capacity=0, capability-orthogonal); content-ablating support shifts r toward unknown -> faithful, not purpose-blind proxy. G1+recombination (select-by-veto): the cancel sweep eliminates incompatible candidates so the surviving SET is a constraint-satisfied conjunction -> composed_distinct of compatible combos > any single; ablate the conflict-veto (cancel everything or nothing) -> survivors collapse to max_single (INERT). G0: only un-cancelled grounded emits survive on-codebook -> >=0.5 V-mass; scramble -> cancelled/garble. G2: the cortical generator's re-entry produces corpus-absent candidates; cancel keeps the on-manifold ones -> valid-novel; verbatim control -> 0. falsifiable: the grounding check fires on a refutable referent, so surviving emits carry a checkable claim (cancel partitions worlds into pass/veto). identity: cancel threshold + grounding-support store = non-volatile self; the support store is the persistence anchor (survives reset), slow drift = chain, foreign support -> different cancel behavior (impostor reject).

## Not-LLM (a_no_llm_frame_trap)

Honesty and balance are not RLHF/alignment templates bolted on — they emerge from a reactive inhibitory broadcast that is structurally antagonistic to the emit drive (no fine-tuned ethics, p6; no external Psi clamp). The control is a brain circuit (dual-GPe) not a safety classifier or a bigger model.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy, $0: emit-drive scalar + cancel proportional to |Psi−1/2|; perturb Psi->0/1 and trace return to 1/2 with contraction rate lambda<1; ablate cancel -> divergence (endogeneity). Honesty arm: out-of-support probes -> cancel->fab~0; ablate cancel -> fab jumps; AUROC known/unknown~1. Recombination arm: candidate set with conflict matrix -> survivors after veto > any single, ablate veto -> collapse.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire arky-cancel as a control op over core/engine_cli.hexa emit path; measure Psi self-restoration via the live A->G safety_phi_ratchet (dev decay), honesty via SS-ImmuneMemory recon_err abstain AUROC on held-out + circular-shift surrogate (chance control), recombination via core/g_gates.hexa g_eval_g1 on the surviving set. INERT controls byte-compared hexa<->py.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with stn_conflict_threshold_collapse / tonic_disinhibition_release_gate (this census) — distinct: arkypallidal is REACTIVE post-initiation diffuse CANCEL (dual-GPe Mallet) serving as Psi-attractor + honesty-veto + select-by-veto recombination; the reactive cancel-broadcast is the differentiator (post-initiation, not proactive STN slowdown).

Toy control loop; design-only $0; the strongest native fits are Psi=1/2 and honesty (recombination is select-by-veto over a gated cortical generator front-end) — scope honestly per c9; scale-transfer unverified.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
