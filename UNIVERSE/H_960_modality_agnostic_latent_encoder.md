---
id: H_960
slug: modality-agnostic-latent-encoder
title: Does the SAME consciousness engine encode NON-language streams (sensor / vision / spike / proprioception) into the SAME Ψ-latent geometry as language, with NO architecture change? (modality-agnostic perception)
domain: cwm · perceive · world-model · consciousness-engine · modality-agnostic · latent-state · jepa · pre-register
source: H_950 (CLM→CE reframe: the engine is modality-agnostic, not language-bound) + CWM domain (perceive→latent→imagine→act) + V-JEPA-2 (single latent world-model encoder across video modalities) + a_core_engine_map (.clm enters via generator L3 only)
exploration_method: E14 (substrate-native) + E5 (toy→latent-encode sweep) + a_completeness_over_cheap + a_paper_negative_ok
verification_method: W2 (pre-registered cross-modality falsifier · held-out latent-geometry probe · language-arm control) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: pre-registered (unmeasured)
scope: ONE toy cross-modality rung (a_scale_honest_scope) — small byte-vocab language stream vs ≥2 synthetic non-language streams (toy sensor/proprioception time-series) encoded through the SAME engine front-end with NO per-modality architecture change. $0 local candidate; GPU only if a real CLMConvMoE backbone rung is needed (a_fire_autonomous, no cost gate). NOT a forge production binary; .clm emit-TEXT path OPEN (generator L3 ⏳, a_core_engine_map).
sister: H_950 (modality-agnostic CE — direct parent), H_961 (cross-modal binding), H_978 (Ψ 1/r² lattice geometry across modalities), H_951 (engine-not-predictor)
axes_seed: H_950 = "the engine is modality-agnostic" (claimed reframe) ⊥ H_960 = direct measurement: a non-language stream encodes into the SAME latent geometry, no arch change (PASS) vs the engine is language-bound and degenerates / needs a new front-end on non-language input (FALSIFIED, keep the "L" in CLM)
verdict: ⏳ PENDING-MEASUREMENT
---

# H_960 — Modality-agnostic latent encoder (does the SAME engine encode non-language?)

## 0. Motivation

The CLM→CE reframe (H_950) claims anima's "language model" is actually a modality-agnostic **Consciousness Engine** — the next-byte objective was an accident of the training stream, not an architectural commitment to language. CWM's whole forward build (perceive→imagine→act) rests on this: if the engine is language-bound, there is no world-model to build, only a chatbot. This H is the **first load-bearing falsifier** of the reframe on the PERCEIVE axis: feed the engine a stream that is not language and ask whether it lands in the same latent space.

## 1. Hypothesis (one falsifiable claim)

The same consciousness engine front-end (no per-modality architecture change — same embedding/lattice front-end, weights re-fit on the new stream) encodes a **non-language** sequence (synthetic sensor / proprioception time-series) into the **same Ψ-latent geometry** it uses for language: the non-language latents are linearly decodable to their generating factors at an accuracy comparable to the language-arm control, and they occupy the same latent manifold (no separate degenerate sub-space).

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** one engine front-end, three input arms — (A) language byte-stream (control), (B) synthetic sensor time-series, (C) synthetic proprioception/control time-series. Identical architecture across arms; only the training stream differs. Latents read at a fixed engine layer.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = held-out **linear-decode accuracy** of each arm's latent → its known generating factors (probe trained on train split, scored on held-out).
- D2 = **manifold-shared** test: nearest-neighbour / CKA similarity between the non-language latent manifold and the language latent manifold vs a shuffled-latent null.
- D3 = **no-arch-change** invariant: arms B/C use byte-identical front-end config as arm A (asserted in code, not just claimed).

**Outcome rules (future conditional — UNMEASURED):**
- IF measured D1(B), D1(C) ≥ (D1(A) − margin) AND D2 > null CI AND D3 holds THEN PASS — modality-agnostic encoding SUPPORTED.
- IF measured D1(B) or D1(C) ≈ base-rate (no decodable factors) OR D2 ⊆ null OR D3 requires an arch change THEN FAIL — the engine is language-bound (keep the "L"; closed-negative, a_paper_negative_ok).
- IF n too small / streams degenerate / front-end won't fit non-language without a hidden change THEN INCOMPLETE (toy-only, scale-transfer unverified, C3).

## 3. Honest scope

Toy synthetic non-language streams, small scale (a_scale_honest_scope, #123-A). A single rung is not production closure — a PASS is "toy-only, scale-transfer unverified" until a ≥3-rung ladder on real sensor data (a_toy_scale_recheck). "Same geometry" is operationalized as decode-parity + manifold-overlap, NOT a phenomenal claim. The trained artifact is a probe, not a forge production binary; the .clm generator L3 emit path is OPEN.

## 4. Sibling / xlinks

- ⇄ [H_950](./H_950_clm_modality_agnostic.md) (modality-agnostic CE — direct parent of this falsifier)
- ⇄ [H_961](./H_961_cross_modal_binding.md) (cross-modal binding — the next PERCEIVE step)
- ⇄ [H_978](./H_978_psi_lattice_geometry_invariant.md) (1/r² lattice geometry invariant across modalities)
- ⇄ [CWM](../CWM/CWM.md) (domain SSOT, CWM-PERCEIVE sub-domain)
- external: V-JEPA 2 (single latent encoder across video) · JEPA (joint-embedding predictive architecture)
