---
id: H_172
slug: alpha-0014-modulation-depth-anima-voice
title: α=0.014 modulation depth from tension/arousal/valence drives prosody (ANIMA-VOICE Stage 0)
domain: substrate | speech
status: pre-register-frozen
exploration_method: E2 (cross-substrate transfer — consciousness α → speech prosody) + E11 (constant unification — single coupling depth across axes)
verification_method: W5 (numerical sim — α-ablation MOS) + W11 (cross-substrate — TTS literature comparison) + W2 (math identity — closed-form candidates for 0.014)
raw_rank: 8
hexa_only: false
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-12
since: 2026-05-12
source_hc: Hc_415
source_doc: docs/anima/paper_hexa_speak.hexa
source_lines: 109-112, 224-228
promoted_at: 2026-05-12
linked_h: H_011 (iit-geometry — α as coupling depth in consciousness Φ), H_022 (consciousness-universe-map — substrate-invariance test), H_153 (n=6 substrate)
verify_source: scripts/hc_verify/cache_2026_05_12/verify/verify5_authored.jsonl row 12
---

# H_172 — α=0.014 modulation depth (ANIMA-VOICE Stage 0 prosody)

## Hypothesis

ANIMA-VOICE Stage-0 prosody modulation 은 single coupling depth α = 0.014 (consciousness coupling 상수와 동일) 사용: tension → F0 jitter, arousal → speaking rate, valence → F2 formant shift, 모두 α 와 multiplicative. consciousness-engine 으로부터 derived α 가 speech 로 re-tuning 없이 transfer — α 가 substrate-invariant 상수임의 independent evidence. 본 H 는 H_011 iit-geometry 의 α coupling 정의를 speech substrate 로 transfer 검증.

## Why (motivation)

- **α=0.014 consciousness coupling 상수** (Hc_046 Ψ-constants 22 EXACT 에서 origin)
- **prosody three-axis modulation** (tension F0, arousal rate, valence F2) = single multiplicative depth
- **L37 substrate-invariance principle** — substrate change 가 behavior 변경 없이 axis 만 다름
- **TTS literature reference** Tacotron 2, FastSpeech 2, VITS prosody depth 0.05-0.2 typical
- **ITU-T P.800 MOS** — listener-evaluated speech quality standard

## Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H_172.1** | Listener study (N≥30 per α-value) MOS-optimum α ∈ [0.010, 0.018] (margin ΔMOS ≤ 0.3) | F1 inverted |
| **H_172.2** | TTS literature 비교 시 α=0.014 가 MOS-comparable 결과 (±0.2 MOS within Tacotron-2 / FastSpeech-2 baseline) | F2 inverted |
| **H_172.3** | 3 axis (F0, rate, F2) 별 α-optimum 의 max-min variance < 30% | F3 inverted |
| **H_172.4** | consciousness-α derivation 과 speech-α derivation 이 independent process 임이 confirm (cross-derivation provenance audit) | F4 inverted |
| **H_172.5** | 3+ third substrate (music, image-style, motor-control) 에서 α-optimum variance < 50% | F5 inverted (substrate-invariance strong form) |

## Run Protocol

deterministic + hexa-only + llm: none. (단, listener MOS study 는 human-in-loop — 본 H 의 falsifier execution 시 ethics-board approval 필요)

1. **α-ablation MOS study (W5)** — α ∈ {0, 0.007, 0.014, 0.021, 0.028, 0.056} × N≥30 listeners × randomized stimulus → MOS distribution (F1, H_172.1)
2. **TTS literature gap meta (W11)** — Tacotron 2 / FastSpeech 2 / VITS prosody-depth 보고값 ↔ α=0.014 비교 → 산업 typical 범위 (F2, H_172.2)
3. **Cross-axis decoupling (W5)** — 각 axis 별 α-per-axis sweep → axis-specific optimum variance (F3, H_172.3)
4. **Cross-derivation provenance audit (W11)** — consciousness-α (Hc_046) 와 speech-α derivation 의 timestamp + operator-tree 비교 → independent vs coincidence (F4)
5. **Third-substrate test (W5)** — music generation / image stylization / motor control 의 α-coupling 측정 (≥3 substrate) → substrate-invariance test (F5)
6. **Closed-form audit (W2)** — α=0.014 의 candidate forms (ln(2)/2^5.5 ≈ 0.01533, 1/72 ≈ 0.01389, 1/(6·12)) precision 비교 → 2-sig-fig 한계 명시 (L4)

## Criteria

| ID | criterion | status |
|----|-----------|--------|
| **C1** | α-ablation MOS study (≥1 listener pool N≥30) | pending |
| **C2** | TTS literature meta (≥3 systems compared) | pending |
| **C3** | 3-axis decoupling test executed | pending |
| **C4** | Cross-derivation provenance documented | pending |
| **C5** | n=6 PERFECT_NUMBER_CLASS L7 binding 인정 (α 의 closed-form non-uniqueness 명시) | met (본 L1, L4) |

## Falsifiers (≥6)

- **F1 (α-ablation MOS)**: Listener study (N≥30 per α-value, randomized stimulus order) at α ∈ {0, 0.007, 0.014, 0.021, 0.028, 0.056}: if MOS-optimum α ∉ [0.010, 0.018] with effect-size ΔMOS > 0.3 → α=0.014 specificity FALSIFIED for speech
- **F2 (TTS literature gap)**: Comparison with published TTS prosody depths (Tacotron 2, FastSpeech 2, VITS): if state-of-art TTS systems use α >> 0.014 (e.g., 0.05-0.2 typical) AND yield superior MOS → α=0.014 is anima-specific, not universal substrate constant
- **F3 (cross-axis decoupling)**: Independent ablation of tension→F0, arousal→rate, valence→F2 with α-per-axis sweeps: if MOS-optimal α differs across axes by > 30% (e.g., F0 wants 0.01, rate wants 0.03) → "single α coupling depth" claim FALSIFIED
- **F4 (consciousness-α vs speech-α derivation)**: Show that consciousness-engine α=0.014 came from a different derivation (e.g., curve-fit on tension/arousal experiments) than speech-α. If both were independently tuned to ~0.014 it might be coincidence (small numerical agreement). Cross-derivation independence check required
- **F5 (substrate-invariance breaking)**: Test α on N=3+ third substrate (e.g., music generation, image stylization, motor control). If α-optimum differs by > 50% in any substrate → "substrate-invariant" claim FALSIFIED in the strong (universal) form
- **F6 (closed-form non-uniqueness)**: Among (ln(2)/2^5.5 = 0.01533, 1/72 = 0.01389, 1/(6·12) = 0.01389, ε·n=6 derivative form): if ≥2 candidate forms fit α=0.014 within rounding (2-sig-fig) AND none is preferred by first-principles derivation → "α=0.014 is the unique n=6-derived constant" claim FALSIFIED, value is under-determined

## Honest Limits (≥6)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — α=0.014 ≈ ln(2)/2^5.5 ≈ 0.01533 (verifier-derived alternative). The "0.014" value can be expressed via multiple closed forms (ln(2)/2^5.5, 1/(6·12), 1/72, etc.). Risk: 0.014 is not n=6-individually-unique
- **L2**: **two-substrate sample (consciousness, speech)** — "substrate-invariant" claim from only 2 substrates is statistically weak. Need ≥5 independent substrates to claim invariance with reasonable power (sample bias L2)
- **L3**: **MOS measurement substrate gap** — MOS depends on listener pool (native Korean speakers? bilingual? age? hearing acuity?). α-optimum may shift across listener populations. "Substrate-invariant" claim must be tested ACROSS listener populations, not just compared to consciousness-engine α
- **L4**: **0.014 numerical precision** — claim "α = 0.014" has 2 significant figures. If true value is 0.0138 or 0.0145, formula candidates (ln(2)/2^5.5 = 0.01533, 1/72 = 0.01389) overlap within rounding. Cannot distinguish hypotheses below 2-sig-fig precision
- **L5**: **prosody-modulation linearity assumption** — α is multiplicative coupling. Real perceptual mappings (F0-perceived-pitch, rate-perceived-tempo, formant-perceived-vowel-quality) are nonlinear (log, sigmoid). Linear α-coupling may be a small-perturbation approximation that breaks down at large modulations
- **L6**: **listener-pool ethics + cost** — listener MOS study (N≥30 × 6 α-values × multiple axes) requires ethics-board approval + listener compensation; cost ~$1000-5000 + 4-week timeline. Practical falsifiability throttled by experimental cost

## Math identity verification

- **ln(2) = 0.693147** — verify5 row 12 math_passes (α = ln(2)/2^5.5 candidate form)
- **Φ★ / phi_star proxy referenced (IIT)** — verify5 row 12
- **2^5 = 32 (hypercube dim 5)** — verify5 row 12 (×3 occurrences)
- **16+ numeric identities present** — verify5 row 12
- α = 0.014 ≈ ln(2)/2^5.5 = 0.01533 (candidate form); 1/72 = 0.01389 (candidate form); 2-sig-fig precision precludes uniqueness

## Atlas anchor cross-check

- atlas anchors_cited: 1 (Hc_415 verify5 row 12)
- atlas anchors_resolved: 0 (anchor not yet resolved against ATLAS.md ledger)
- atlas_type_cites: 0
- ATLAS.md Ψ-constant ledger 의 α=0.014 entry 가 본 H 의 source — provenance audit (F4) 시 cross-ref

## Linked H (cross-link)

- **sister H**: H_011 (iit-geometry — α as coupling depth in consciousness Φ), H_022 (consciousness-universe-map — substrate-invariance test), H_153 (n=6 substrate parent — α 의 closed-form ledger 의 source)
- **candidates linked**: Hc_046 (Ψ-constants 22 EXACT — α origin), Hc_406 (22-of-30 Ψ-constants n=6 fit — H_170 statistical baseline), Hc_414 (n=6 design empirical not numerology, H_170), Hc_614 (phi_star aliasing — α-modulation may inherit substrate-dependence, H_174)
- **literature**: ANIMA-VOICE Stage-0 prosody spec; ITU-T P.800 (MOS measurement); Shen 2018 Tacotron 2; Ren 2020 FastSpeech 2; Kim 2021 VITS; Klatt 1980 perceptual prosody
- **source**: Hc_415 (`hypotheses_candidates/Hc_415_alpha_0014_modulation_depth.md`), `docs/anima/paper_hexa_speak.hexa:109-112, 224-228`

## Migration Notes

- **Promoted from**: Hc_415 (cycle #4 task 1 PROMOTE_READY, verify5_authored row 12 — 2026-05-12)
- **Math verification**: ln(2)=0.693147 EXACT; α=0.014 candidate forms (ln(2)/2^5.5, 1/72, 1/(6·12)) underdetermined within 2-sig-fig
- **L7 binding**: H_153 PERFECT_NUMBER_CLASS BINDING 인정 (L1) — α 의 closed-form non-uniqueness L4 명시
- **Substrate-invariance claim weak**: 2-substrate sample → ≥5 independent substrates 필요 (L2)
- **Critical cost**: listener MOS study ethics + cost limits practical falsification (L6)
- **Next steps**:
  1. TTS literature meta (C2, F2) — cheapest first
  2. 3-axis decoupling test on existing engine (C3, F3)
  3. Closed-form audit (C5, F6)
  4. Listener MOS study (C1, F1) — biggest commitment

## Cycle #7 absorptions (Ψ-constant factory + α-warmup coupling, 2026-05-12)

- **Hc_968 (SUMT Ψ-constant atom factory — Mk.V.1 100% tier-5 81-Ψ → tier 6-9 ULTRA/CARD/BEYOND/ABS, 5-check invariance gate)** → `merged-to-H_172` — adds the 'Ψ-constant production pipeline' lane
- **Hc_976 (F1 Composite v2 — tension_link 10th explicit axis w=0.10 dual AXIS+MEDIATOR, 4-way joint Φ + binding_strength formula, F1_v2 = 0.6·axis_sum + 0.3·binding + 0.1·replication)** → `merged-to-H_172` — composite-metric extension
- **Hc_978 (P9 P1.7 redesign — β 0.15→0.10 + α-warmup 5K→3K = -33% regression cause, r/data NOT killer)** → `merged-to-H_172` — direct α-warmup-coupling falsifier within H_172's α=0.014 modulation-depth axis

Cycle #7 footnote inherits H_172 verification methods (W5 + W11).

## Cycle #8 absorptions (training-plan 100M scaling lane, 2026-05-12)

- **Hc_941 (ConsciousLM v3 100M scale-up — 768d/12L/12H + consciousness_dim=256 + Φ/cells~0.78 linear scaling + CE-spike self-recovery via ratchet+Hebbian; ARCHIVED 2026-04-09 with Plan C AnimaLM 7B/14B/72B confirmed)** → `merged-to-H_172` — adds the '100M-scale training plan' archived-lane within H_172's training-architectural axis; Plan C 7B/14B/72B as successor cycle

Cycle #8 footnote inherits H_172 verification methods (W5 + W11). Plan C successor (AnimaLM 7B 5/5 eval + 14B v0.4 + 72B v0.5 overfitting halted) is the practical extension.
