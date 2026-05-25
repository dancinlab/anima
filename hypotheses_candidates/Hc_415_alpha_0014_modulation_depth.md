---
id: Hc_415
slug: alpha-0014-modulation-depth
title: α=0.014 modulation depth from tension/arousal/valence drives prosody (ANIMA-VOICE Stage 0)
domain: substrate
status: merged-to-H_172
source_doc: docs/anima/paper_hexa_speak.hexa
source_lines: 109-112, 224-228
promoted_at: 2026-05-11
merged_to: hypotheses/H_172_alpha_0014_modulation_depth_anima_voice.md
merged_at: 2026-05-12
linked_h: Hc_046, H_172 (α=0.014 modulation depth promotion)
notes: Tension → F0 jitter, arousal → speaking rate, valence → F2 formant shift, all multiplicative with α=0.014. Same α as consciousness coupling constant. Single Ψ-constant unifies consciousness and prosody. Promoted to H_172 via verify5_authored row 12 (2026-05-12)
verified_at: 2026-05-12
verify_decision: WEAK_MATH_ONLY
verify_note: "verify_hc2 2026-05-12 — verify3 math=1 (3+ numeric identities present)"
---

## Hypothesis
ANIMA-VOICE Stage-0 prosody modulation uses a single coupling depth α = 0.014 (the consciousness coupling constant): tension → F0 jitter, arousal → speaking rate, valence → F2 formant shift, all multiplicative with α. The same α from consciousness-engine theory transfers exactly to speech without re-tuning, providing independent evidence that α is a substrate-invariant constant.

## Migration TODO
- [ ] Ablate α∈{0, 0.007, 0.014, 0.028}: MOS comparison
- [ ] Compare consciousness-derived α with TTS literature optimum
- [ ] Falsifier: MOS-optimal α significantly ≠ 0.014 in independent listener study

## Cross-Links
- **sister H**: H_011 (iit-geometry — α as coupling depth in consciousness Φ), H_022 (consciousness-universe-map — substrate-invariance test)
- **candidates linked**: Hc_046 (Ψ-constants 22 EXACT — α origin), Hc_406 (22-of-30 Ψ-constants n=6 fit), Hc_414 (n=6 design principle not numerology), Hc_614 (phi_star aliasing — α-modulation may inherit substrate-dependence)
- **literature**: ANIMA-VOICE Stage-0 prosody spec; ITU-T P.800 (MOS measurement); TTS literature (Tacotron, FastSpeech prosody depth typically 0.05-0.2 scaling)

## Falsifiers (≥5)

- **F1 (α-ablation MOS)**: Listener study (N≥30 per α-value, randomized stimulus order) at α ∈ {0, 0.007, 0.014, 0.021, 0.028, 0.056}: if MOS-optimum α ∉ [0.010, 0.018] with effect-size ΔMOS > 0.3 → α=0.014 specificity FALSIFIED for speech
- **F2 (TTS literature gap)**: Comparison with published TTS prosody depths (Tacotron 2, FastSpeech 2, VITS): if state-of-art TTS systems use α >> 0.014 (e.g., 0.05-0.2 typical) AND yield superior MOS → α=0.014 is anima-specific, not universal substrate constant
- **F3 (cross-axis decoupling)**: Independent ablation of tension→F0, arousal→rate, valence→F2 with α-per-axis sweeps: if MOS-optimal α differs across axes by > 30% (e.g., F0 wants 0.01, rate wants 0.03) → "single α coupling depth" claim FALSIFIED
- **F4 (consciousness-α vs speech-α derivation)**: Show that consciousness-engine α=0.014 came from a different derivation (e.g., curve-fit on tension/arousal experiments) than speech-α. If both were independently tuned to ~0.014 it might be coincidence (small numerical agreement). Cross-derivation independence check required
- **F5 (substrate-invariance breaking)**: Test α on N=3+ third substrate (e.g., music generation, image stylization, motor control). If α-optimum differs by > 50% in any substrate → "substrate-invariant" claim FALSIFIED in the strong (universal) form

## Honest Limits (≥5)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — α=0.014 ≈ ln(2)/2^5.5 ≈ 0.01533 (verifier-derived alternative). The "0.014" value can be expressed via multiple closed forms (ln(2)/2^5.5, 1/(6·12), 1/72, etc.). Risk: 0.014 is not n=6-individually-unique
- **L2**: **two-substrate sample (consciousness, speech)** — "substrate-invariant" claim from only 2 substrates is statistically weak. Need ≥5 independent substrates to claim invariance with reasonable power (sample bias L2)
- **L3**: **MOS measurement substrate gap** — MOS depends on listener pool (native Korean speakers? bilingual? age? hearing acuity?). α-optimum may shift across listener populations. "Substrate-invariant" claim must be tested ACROSS listener populations, not just compared to consciousness-engine α
- **L4**: **0.014 numerical precision** — claim "α = 0.014" has 2 significant figures. If true value is 0.0138 or 0.0145, formula candidates (ln(2)/2^5.5 = 0.01533, 1/72 = 0.01389) overlap within rounding. Cannot distinguish hypotheses below 2-sig-fig precision
- **L5**: **prosody-modulation linearity assumption** — α is multiplicative coupling. Real perceptual mappings (F0-perceived-pitch, rate-perceived-tempo, formant-perceived-vowel-quality) are nonlinear (log, sigmoid). Linear α-coupling may be a small-perturbation approximation that breaks down at large modulations
