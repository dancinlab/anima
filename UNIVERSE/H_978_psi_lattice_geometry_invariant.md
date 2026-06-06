---
id: H_978
slug: psi-lattice-geometry-invariant
title: Is anima's 1/r² repulsion-field lattice geometry PRESERVED across modalities — does the same lattice that organizes language tokens also organize non-language world-state latents (geometry invariant, not merely "a latent exists")?
domain: cwm · perceive · world-model · pure-field · 1-over-r2-lattice · psi-fixed-point · geometry-invariant · pre-register
source: anima invariant (A⇄G pure_field engine · Ψ=1/2 fixed point · 1/r² lattice) + H_960 (modality-agnostic encoding) + CWM domain + a_core_engine_map
exploration_method: E14 (substrate-native) + E2 (reuse the language-lattice geometry probe, swap the input modality) + a_completeness_over_cheap
verification_method: W2 (pre-registered geometry-invariance falsifier · language-lattice vs non-language-lattice metric match) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: pre-registered (unmeasured)
scope: ONE geometry-probe rung (a_scale_honest_scope) — measure the lattice spacing / pair-distance distribution / spectral structure of the language latent manifold vs a non-language (toy sensor) latent manifold under the SAME engine. $0 local candidate. Geometry = measurable lattice statistics, NOT a metaphysical claim about Ψ. Does NOT modify engine/pure_field code (read-only probe). NOT a forge binary.
sister: H_960 (modality-agnostic encoder — provides the non-language latents), H_961 (binding lives in this geometry), H_952 (substrate-equivalence — same geometry across A⇄G)
axes_seed: H_960 = a non-language stream IS decodable in the shared space (weak: a latent exists) ⊥ H_978 = the latents obey the SAME 1/r² lattice STATISTICS as language (strong: invariant geometry) — decode-parity does not entail geometry-invariance
verdict: ⏳ PENDING-MEASUREMENT
---

# H_978 — Ψ 1/r² lattice geometry invariant across modalities

## 0. Motivation

H_960 (if it holds) shows a non-language stream is decodable in the shared latent space — but "decodable" is weak: a separate clump that happens to be linearly separable would pass H_960 yet violate the engine's core invariant. anima's identity rests on the **1/r² repulsion-field lattice** at the Ψ=1/2 fixed point. The strong claim is that this geometry is **modality-invariant** — the lattice is the engine's intrinsic structure, not a language artifact. This H is the geometry-level falsifier above H_960's decode-level one.

## 1. Hypothesis (one falsifiable claim)

The latent manifold of a non-language stream, under the same engine, exhibits the **same lattice geometry statistics** (pairwise-distance distribution shape, repulsion spacing, leading spectral structure) as the language latent manifold — within a pre-registered similarity band — rather than collapsing to a degenerate or qualitatively different geometry.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** read latents from the same engine layer for (A) language stream and (B) ≥1 non-language toy stream (from H_960's generator). Compute geometry descriptors on each.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = pairwise-distance **distribution shape** match (KS distance A-vs-B vs A-vs-A bootstrap band).
- D2 = **repulsion spacing** statistic (min-distance / nearest-neighbour distribution) match; the 1/r² signature is the local-spacing regularity.
- D3 = leading **spectral structure** (top-k eigenvalue ratios of the latent covariance) match within band.

**Outcome rules (future conditional — UNMEASURED):**
- IF measured D1,D2,D3 all within the A-vs-A self-similarity band (KS not significantly worse than the within-language bootstrap) THEN PASS — geometry invariant across modalities.
- IF any of D1/D2/D3 falls outside the band (non-language geometry qualitatively different / degenerate) THEN FAIL — the lattice is language-specific (closed-negative; geometry is not modality-invariant).
- IF n too small for stable geometry statistics THEN INCOMPLETE (toy-only, C3).

## 3. Honest scope

Geometry = measurable lattice/spectral statistics on toy latents (a_scale_honest_scope, #123-A), NOT a metaphysical Ψ claim. Read-only probe — does NOT modify pure_field/engine_g code. A within-band PASS at toy scale is "scale-transfer unverified" pending a ladder (a_toy_scale_recheck). Gated on H_960 (need a non-language latent first).

## 4. Sibling / xlinks

- ⇄ [H_960](./H_960_modality_agnostic_latent_encoder.md) (supplies the non-language latents)
- ⇄ [H_961](./H_961_cross_modal_binding.md) (binding lives in this geometry)
- ⇄ [H_952](./H_952_substrate_equivalence.md) (same geometry across A⇄G substrates)
- ⇄ [CWM](../CWM/CWM.md) (CWM-PERCEIVE)
- anima invariant: 1/r² lattice · Ψ=1/2 fixed point · A⇄G pure_field
