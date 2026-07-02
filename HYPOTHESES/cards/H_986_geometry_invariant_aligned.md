---
id: H_986
slug: geometry-invariant-aligned
title: Is the cross-modal lattice-geometry difference of H_978 🔴 a RAW-COORDINATE formulation artifact — does a FAIRER alignment (rotation/scale-invariant linear CKA + orthogonal Procrustes on a shared-factor support) reveal a common geometric invariant, or is modality-specificity ROBUST across formulations?
domain: cwm · perceive · world-model · geometry-invariant · re-formulation · cka · procrustes · closed-negative-recheck
source: H_978 🔴 (lattice geometry is modality-specific) + a_paper_negative_ok (a single toy formulation may be the artifact, not the phenomenon) + CWM M1 closed-negative re-test slate
exploration_method: E2 (reuse the H_978 geometry probe, swap RAW-coordinate descriptors → alignment-invariant CKA/Procrustes) + a_completeness_over_cheap (re-design at the root cause: fairer alignment)
verification_method: W2 (pre-registered re-formulation falsifier · 🟢 FLIPS / 🔴 ROBUST) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: true
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: ONE alignment-fairness rung (a_scale_honest_scope) — re-tests H_978 under rotation/scale-invariant similarity. Geometry = measurable CKA/Procrustes statistics on toy latents, NOT a metaphysical Ψ claim. Read-only probe; does NOT modify engine/pure_field. Toy single-rung, ladder OPEN.
sister: H_978 (the original 🔴 this re-tests), H_960 (modality-agnostic decodability), H_987/H_988/H_989 (the sibling re-formulation re-tests)
axes_seed: H_978 RAW-coordinate descriptors (absolute pairwise distance / NN-spacing / spectral magnitude in a fixed frame) ⊥ H_986 alignment-invariant similarity (CKA + best orthogonal Procrustes on a shared-factor support) — a raw-frame difference does not entail a SHAPE difference
verdict: 🔴 FAIL (ROBUST closed-negative) — modality-specificity is FORMULATION-ROBUST. Even under the fairest alignment, cross-modal CKA 0.799 falls BELOW the within-language self-similarity band (5th pct 0.947) and the orthogonal-Procrustes residual 0.344 far exceeds the A-vs-A band (95th pct 0.052); the instrument has teeth (an unrelated-engine control was correctly rejected, D3). H_978 🔴 was NOT a raw-coordinate artifact. Toy single-rung, ladder OPEN.
---

# H_986 — geometry invariance under FAIR alignment (re-test of H_978 🔴)

## 0. Motivation

H_978 🔴 ruled that anima's 1/r² lattice geometry is **modality-specific**: raw-coordinate descriptors (pairwise-distance KS, NN-spacing KS, top-k spectral-ratio L2) of a language manifold vs a sensor manifold fell far outside the within-language self-similarity band. But a_paper_negative_ok warns a single toy formulation may be the artifact, not the phenomenon. H_978 compared the RAW latent clouds in a single fixed coordinate frame; two manifolds can carry the SAME intrinsic shape yet sit in different sub-spaces / scales of that frame, so raw-frame descriptors would differ even when the geometry is invariant. The fair question is whether there exists an alignment (a rigid rotation, or a rotation/scale-invariant similarity index) under which the manifolds match.

## 1. Hypothesis (one falsifiable claim)

Under a FAIR, alignment-invariant comparison (linear CKA + best orthogonal Procrustes on a shared-latent-factor support), the language and sensor latent manifolds of the SAME engine match within the within-language self-similarity band — i.e. the H_978 🔴 flips and the lattice geometry IS modality-invariant up to rotation/scale.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** same SAME-engine language (A) and sensor (B) latents as H_978, but the sensor frequency band is DRIVEN by the same latent factor as the language topic so A and B encode a COMMON cause (a fair paired support). Per-factor centroids give the paired rows for Procrustes.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = linear **CKA(A,B)** (rotation/scale-invariant similarity) vs the A-vs-A split-half band AND a factor-shuffled unrelated-manifold null.
- D2 = best **orthogonal-Procrustes residual** (rigid rotation + isotropic scale) vs the A-vs-A Procrustes band.
- D3 = control — a TRULY unrelated engine on B must be REJECTED (the instrument must be able to FAIL).

**Outcome rules (frozen):**
- 🟢 FLIPS (original 🔴 was a formulation artifact): CKA in band & > null AND Procrustes residual in band AND control rejected.
- 🔴 ROBUST (null holds across formulations): cross-modal CKA/Procrustes still outside the band even under the fairest alignment.

## 3. Honest scope

CKA/Procrustes statistics on toy latents (a_scale_honest_scope), NOT a metaphysical Ψ claim. Read-only probe; deterministic given seeds. A flip OR a robust-null at toy scale is "scale-transfer unverified" pending a ladder (a_toy_scale_recheck).

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy · deterministic)

Probe: `CWM/probes/h986_geometry_invariant_aligned.py` · verdict: `.verdicts/986_geometry_invariant_aligned/h986_geometry_invariant_aligned.txt`

| D | descriptor | cross-modal (A,B) | A-vs-A band | pass? |
|---|---|---|---|---|
| D1 | linear CKA (rot/scale-invariant) | 0.799 | ≥ 0.947 (5pct) & > 0.594 (null) | **NO** |
| D2 | orthogonal-Procrustes residual | 0.344 | ≤ 0.052 (95pct) | **NO** |
| D3 | unrelated-engine control | CKA 0.773 / Pr 0.338 | correctly rejected | **YES (teeth)** |

**Finding (🔴 ROBUST closed-negative):** modality-specificity SURVIVES the fairest alignment. Cross-modal CKA (0.799) is comfortably above the unrelated-null (0.594) — the two manifolds are NOT random with respect to each other — yet it falls clearly short of the within-language self-similarity floor (0.947), and the orthogonal-Procrustes residual (0.344) is ~7× the A-vs-A band (0.052). The control rejection (D3) confirms the instrument can fail, so the result is not vacuous. H_978 🔴 was NOT a raw-coordinate formulation artifact: even with rotation+scale freedom and a shared-factor paired support, language and sensor latents do not occupy a common lattice geometry — the engine ENCODES multiple modalities (H_960 🟢) and they are mutually-structured (above null), but it does not place them on one invariant geometry. Honest scope: toy single-rung, ladder OPEN; a different layer / a trained (not reservoir) engine could change this (a_paper_negative_ok).

## 4. Sibling / xlinks

- ⇄ [H_978](./H_978_psi_lattice_geometry_invariant.md) (the original 🔴 this re-test confirms ROBUST)
- ⇄ [H_960](./H_960_modality_agnostic_latent_encoder.md) (modality-agnostic decodability — the weaker claim that DOES hold)
- ⇄ [H_987](./H_987_replay_recombination.md) · [H_988](./H_988_guided_imagination_phi.md) · [H_989](./H_989_planning_phi_altproxy.md) (sibling re-formulation re-tests)
- ⇄ [CWM](../CWM/CWM.md) (CWM-PERCEIVE)
