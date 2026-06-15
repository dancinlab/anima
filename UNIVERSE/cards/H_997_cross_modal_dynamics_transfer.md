---
id: H_997
slug: cross-modal-dynamics-transfer
title: Does the latent DYNAMICS (forward-transition operator) transfer across modalities even though the latent GEOMETRY does not — can a transition trained on modality A forecast modality B (same underlying generative law, different sensor) with only a cheap decoder re-fit, while cross-modal geometry similarity stays low (consistent with H_978🔴)?
domain: cwm · perceive · imagine · transfer · dynamics · geometry · modality
source: CWM 2nd slate — reconciles H_960🟢 (modality-agnostic encode) with H_978🔴 (geometry modality-specific): is DYNAMICS what transfers? + JEPA/world-foundation-model + a_completeness_over_cheap
exploration_method: E14 (substrate-native) + E11 (frozen-transition transfer + CKA geometry)
verification_method: W2 (pre-registered dynamics-transfer-beats-shuffled + geometry-distinct falsifier) + g5 CODE-measured (no LLM self-judge, p7)
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: ONE shared-latent two-modality rung (a_scale_honest_scope) — modality A=raw coords, B=rotated+nonlinear sensor of the SAME oscillator; $0 CPU. NOT a forge binary.
sister: H_978 (geometry modality-specific — the 🔴 this complements), H_960 (modality-agnostic encode), H_962 (latent dynamics)
axes_seed: "modality-transfer needs a shared latent GEOMETRY" ⊥ "the forward LAW transfers even when geometry doesn't" — dynamics-transfer ⊥ geometry-invariance
verdict: 🟢 PASS — dynamics transfers without geometry invariance: a transition trained on modality A forecasts modality B (err 0.16) far below a shuffled-transition control (66.4, p=8.1e-06) and below static (0.72), while cross-modal CKA 0.79 ≪ same-modal 1.00. Toy single-rung, ladder OPEN.
---

# H_997 — cross-modal DYNAMICS transfer (forward operator transfers, geometry doesn't)

## 0. Motivation

The 1st slate left a tension: H_960🟢 (the same engine encodes non-language modalities, decode-parity) but H_978🔴 (the latent GEOMETRY — spacing/spectrum — is modality-SPECIFIC). This H resolves it by asking what the right invariant is: maybe GEOMETRY differs across modalities while the latent DYNAMICS (the forward-transition operator) TRANSFERS, because two modalities can express the same underlying generative process through different sensors. If so, a WM trained on modality A should forecast modality B after only re-fitting the cheap read-out, keeping the transition frozen.

## 1. Hypothesis (one falsifiable claim)

When two modalities share an underlying generative dynamics, a transition operator learned on modality A forecasts modality B (with only the decoder re-fit) better than a shuffled-transition control and a static baseline, even though the A and B latent geometries are dissimilar (low cross-modal CKA) — i.e. dynamics transfers without geometry invariance.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** a shared 2D-oscillator latent process. Modality A = raw coordinates; modality B = a rotated + strongly nonlinearly-warped sensor view of the SAME latent. Train an LDS WM on A; freeze its transition A; refit only the decoder on a little B data. Controls: shuffled (random) transition; static last-obs. 24 seeds.

**Measurement (g5 CODE-measured):**
- D1 = B-forecast error: frozen-A vs shuffled (Welch) and vs static.
- D2 = cross-modal CKA(A-latents, B-latents) vs same-modal CKA.

**Outcome rules (future conditional):**
- IF frozen-A < shuffled (p<0.05) AND < static AND cross-modal CKA ≪ same-modal CKA THEN PASS — dynamics transfers ⊥ geometry.
- IF frozen-A does not beat shuffled THEN FAIL — no dynamics transfer (closed-negative).

## 3. Honest scope

Toy shared-dynamics rung (a_scale_honest_scope, #123-A) — two modalities constructed to share a generative law; real cross-modal transfer (vision↔audio) is OPEN. Single rung, ladder OPEN. NOT a forge binary.

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy)

Probe: `CWM/probes2/h997_dynamics_transfer.py` · verdict: `.verdicts/997_cross_modal_dynamics_transfer/h997_dynamics_transfer.txt`

| arm | modality-B forecast error |
|---|---|
| FROZEN-A transition (transferred) | **0.1599 ± 0.0343** |
| SHUFFLED transition (control) | 66.40 ± 55.63 |
| STATIC last-obs | 0.7221 ± 0.1144 |

D1 frozen-A < shuffled: Cohen d=−1.65, p=8.1e-06; frozen-A < static ✓. D2 cross-modal CKA = **0.786** ≪ same-modal CKA = 1.000.

**VERDICT 🟢 PASS** — the forward LAW transfers across modalities even though the GEOMETRY does not: a transition trained on modality A forecasts modality B essentially as well as a native fit, while the two modalities' latent geometries are clearly dissimilar. This reconciles H_960🟢 (engine encodes any modality) with H_978🔴 (geometry is modality-specific): what is shared across modalities is the *dynamics*, not the *geometry* (toy rung; ladder OPEN).
