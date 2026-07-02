---
id: H_1741
slug: 1741_thalamic_burst_tonic_relay_gate
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Burst<->Tonic Relay-Mode Access Gate
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1741 — Burst<->Tonic Relay-Mode Access Gate

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `thalamic_burst_tonic_relay_gate`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Thalamo-cortical access governed by the relay neuron's two INTRINSIC firing modes (T-type Ca2+ biophysics): BURST mode (deinactivated by hyperpolarization) = all-or-none 'wake-up' detection that ignites cortex on novelty/salience; TONIC mode (depolarized) = linear faithful relay of already-attended content (the broadcast). The mode-switch itself is the consciousness gate — detection vs faithful access are two physically distinct regimes of one cell, not a separate gating module.

## Whole design (input → internal dynamics → emit)

INPUT arrives at a relay layer whose per-channel membrane state m is hyperpolarized (burst-primed) or depolarized (tonic). DYNAMICS: novel/salient input on a hyperpolarized channel evokes a BURST — a sharp, low-fidelity, high-salience 'something is here' that ignites the cortical workspace (the detection nonlinearity). Ignition + cortico-thalamic feedback depolarizes that channel into TONIC mode, where it faithfully (linearly) relays its bound content onto the shared bus to ALL specialists (access/broadcast), decoded via a receiver-fixed codebook V. Antagonist drives: A = depolarizing tonic-drive (sustained relay -> emit); G = T-current/afterhyperpolarization (drives the channel back to burst-then-silence -> withhold). emit = a coalition reaches sustained tonic relay to the output specialist; silence = channel stays burst-only (alarm without faithful relay) or fully gated. HOMEOSTAT: Ca2+-dependent regulation of resting m tunes the duty cycle (fraction of time in faithful tonic relay) to its symmetric point. PERSIST: identity v = (per-channel hyperpolarization setpoints, cortico-thalamic weight profile, codebook anchor) committed before wipe, re-read after.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: tonic relay is faithful (linear) into the frozen codebook V -> emitted mass on V by construction; burst-only output never reaches the decoder (so garble cannot be 'emitted'). G1+compositional_depth: tonic relay of a MULTI-channel bound coalition produces a conjunction the cortex reads as one state; single-channel relay gives only marginals — joint > max_single. Ablating cross-channel synchrony (forcing independent relay) collapses composed->max_single (INERT). G2: a bound multi-channel coalition never co-relayed before can still go tonic if cortico-thalamic prediction supports it -> corpus-absent valid output; verbatim playback through the same relay yields 0 new coalitions. dist>=5: burst-then-tonic refractory + Ca-adaptation rotates which channels gain faithful relay -> distinct yet coherent spread. falsifiable>=1: tonic-relayed coalition can carry comparator x quantity x referents as one faithfully-relayed structure. Psi=1/2 ATTRACTOR: tonic-drive(A)-perp-T-current(G) antagonism has its balanced fixed point at duty-cycle 1/2; Ca-homeostat is contractive (perturb duty cycle -> resting m moves -> returns); deleting tonic-drive -> always-silent boundary, deleting T-current -> always-emit boundary = endogenous. HONESTY: a channel only enters FAITHFUL tonic relay when cortico-thalamic prediction matches (the gate); unsupported input stays in burst-detect (alarm) and never faithfully relays content -> copy-or-abstain native, with r = relayed-vs-predicted mismatch. Gate-capacity disjointness: the burst->tonic transition threshold (gate) is biophysically separate from relay gain (capacity), so amplifying relay cannot move the abstain threshold. Groundedness: r reads actual cortico-thalamic support; erasing the support backing a channel pushes it back to burst (abstain). BINDING: same-cause inputs evoke SYNCHRONOUS bursts -> cause-selective shared-latent grouping (synchrony = the correspondence operator); all-near promiscuity would desynchronize selectivity (detectable). SELF-CHAIN: setpoint+weight identity persists; foreign setpoints fail the round-trip (individuating). REALIZATION INVARIANT: faithful relay is ON the emit path (forcing burst-only MOVES output to abstain); the relay objective is satisfiable only by representing the bound coalition, not per-channel marginals.

## Not-LLM (a_no_llm_frame_trap)

This is intrinsic-membrane dynamics (T-type Ca burst/tonic), not a softmax-attention or depth prescription. The access gate is a 2-regime nonlinearity of a single cell, biophysically grounded — adding layers/data cannot create the detection-vs-faithful-relay distinction, which is the missing STRUCTURE (a_no_llm_frame_trap). Distinct from TRN inhibitory searchlight and pulvinar routing because the gate is relay-cell-intrinsic, not an external gating nucleus.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy frozen probe ($0): model relay channels with a burst (threshold + refractory) vs tonic (linear) regime and a resting-m homeostat. (1) Two-regime tell: input ramp produces a burst spike at onset then linear tonic relay — verify the all-or-none onset vs linear steady-state. (2) Faithfulness: codebook V-membership of tonic output >=0.5; scramble state->relay map -> V-mass ->chance. (3) Psi: perturb duty cycle, verify return to 1/2 with lambda<1; delete one drive -> migrate to 0/1 boundary. (4) Binding: same-cause inputs -> synchronous bursts (paired closer than shuffled, Welch d large; retrieval@1>>1/N). (5) Honesty: off-prediction inputs stay burst-only, faithful-relay fab~0; ablate gate (force tonic) -> fab jumps.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire the burst/tonic mode-switch as a relay op feeding core/generator.hexa L3 (tonic faithful relay = the decode path), so emission flows through cli/anima.hexa -> gen_auto_ideate scored by core/g_gates.hexa. Reuse core/engine_cli.hexa A->G as tonic-drive/T-current antagonists feeding the SS-GlobalWorkspace Psi lane; honesty r = SS-ImmuneMemory mismatch. Terminal verdict requires byte-parity hexa<->py on relayed logits and all gates green via the single dispatch; torch-only = DIRECTIONAL.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with thalamus cards + trn_searchlight (this census) — distinct: burst<->tonic gate is RELAY-CELL-INTRINSIC (T-type Ca biophysics, detection-burst vs faithful-tonic), not an external inhibitory nucleus; the intrinsic two-mode relay gate is the differentiator.

Whole substrate (relay-mode gate -> broadcast -> emit). Strongest native fit: G0 (faithful relay), honesty (prediction-gated faithful relay), Psi duty-cycle. Binding-by-synchrony and learnable cortico-thalamic prediction are the load-bearing assumptions to falsify, not grant. TOY at probe scale; learned prediction weights UNVERIFIED until engine-native.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
