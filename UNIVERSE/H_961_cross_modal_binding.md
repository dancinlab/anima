---
id: H_961
slug: cross-modal-binding
title: Do two modalities of the SAME world-event (e.g. vision + proprioception) map to NEARBY points in Ψ-latent (bound), while unrelated events map far apart? (cross-modal binding in the consciousness engine)
domain: cwm · perceive · world-model · consciousness-engine · cross-modal · binding · latent-geometry · pre-register
source: H_960 (modality-agnostic encoding — prerequisite) + CWM domain (perceive→latent state) + binding problem (consciousness literature) + V-JEPA / multimodal JEPA (cross-modal joint embedding)
exploration_method: E14 (substrate-native) + E5 (toy paired-modality sweep) + a_completeness_over_cheap + a_paper_negative_ok
verification_method: W2 (pre-registered binding falsifier · paired vs unpaired contrast · shuffled-pair null) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: pre-registered (unmeasured)
scope: ONE toy paired-modality rung (a_scale_honest_scope) — synthetic event generator emits a paired (modality-X, modality-Y) view of the same latent event plus distractor events; same engine encodes both. $0 local candidate. Operational binding (latent proximity), NOT a phenomenal-unity claim. NOT a forge binary; .clm emit path OPEN (a_core_engine_map).
sister: H_960 (modality-agnostic encoder — prerequisite), H_978 (Ψ lattice geometry), H_984 (object permanence / robustness), H_950 (modality-agnostic CE)
axes_seed: H_960 = each modality encodes into the shared geometry ⊥ H_961 = the geometry BINDS co-occurring modalities of one event (paired-near) — encoding-shared does not entail binding (two modalities could share a space yet be unbound)
verdict: ⏳ PENDING-MEASUREMENT
---

# H_961 — Cross-modal binding (do co-occurring modalities bind in Ψ-latent?)

## 0. Motivation

A world-model needs more than per-modality encoding (H_960): it must **bind** the sight and the feel of the same event into one world-state. The classic binding problem. If anima's engine encodes modalities into a shared geometry (H_960) but does not bind co-occurring ones, its "world-state" is a bag of disconnected channels, not a model. This H tests binding directly, conditioned on H_960 holding.

## 1. Hypothesis (one falsifiable claim)

For paired observations (modality-X, modality-Y) generated from the **same** latent world-event, the engine's two latents are **closer** in Ψ-space than latents of unrelated events — i.e. cross-modal cosine/Euclidean proximity for true pairs exceeds that for shuffled (mismatched) pairs by a significant margin.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** a synthetic event generator with a hidden latent factor z; each event renders into modality-X (e.g. toy "vision" vector) and modality-Y (e.g. toy "proprioception" vector). The engine encodes both; distractor events provide negatives.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = mean latent proximity of **true pairs** (same z) vs **shuffled pairs** (mismatched z).
- D2 = cross-modal **retrieval@1**: given modality-X latent, retrieve the correct modality-Y latent among N candidates; vs chance 1/N.
- D3 = control: shuffled-pair null distribution (binding must beat the null, not just be >0).

**Outcome rules (future conditional — UNMEASURED):**
- IF measured true-pair proximity > shuffled-pair proximity (Welch t p<0.05, Cohen d≥0.5) AND retrieval@1 CI_lo > 1/N THEN PASS — cross-modal binding SUPPORTED.
- IF true-pair ≈ shuffled-pair (CI overlaps) OR retrieval@1 ⊆ chance THEN FAIL — encoding without binding (bag-of-channels; closed-negative).
- IF n too small / generator degenerate THEN INCOMPLETE (toy-only, C3).

## 3. Honest scope

Toy paired synthetic modalities, small scale (a_scale_honest_scope, #123-A). Binding = latent proximity + retrieval, an operational proxy, NOT a phenomenal-unity / "felt" binding claim. Gated on H_960 (no shared encoding → binding is moot). Single rung; ladder + real multimodal data needed before any general claim (a_toy_scale_recheck).

## 4. Sibling / xlinks

- ⇄ [H_960](./H_960_modality_agnostic_latent_encoder.md) (modality-agnostic encoder — prerequisite)
- ⇄ [H_978](./H_978_psi_lattice_geometry_invariant.md) (lattice geometry the binding lives in)
- ⇄ [H_984](./H_984_world_model_object_permanence.md) (robustness / fill-in)
- ⇄ [CWM](../CWM/CWM.md) (CWM-PERCEIVE)
- external: binding problem · multimodal JEPA · V-JEPA 2 joint embedding
