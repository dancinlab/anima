# Expansion Draft — H_proposal (NEW): ANIMA-VOICE Consciousness-Direct Synthesis Specification

## Status: APPLIED — NEW H promoted to hypotheses/H_154.md on 2026-05-11 (Cycle 3 closure)
## Original status: draft-pending-review (2026-05-11) — proposal for new H_XXX (no current target)

## Source candidates merged (3, with paper_hexa_speak bridges)

- Hc_053 anima-voice-consciousness-direct-synthesis — TTS=글자읽기 ≠ ANIMA-VOICE=의도-직접-발성. ConsciousLM intent 384d → ANIMA-VOICE 384d → 8 RVQ × 1024 → 24kHz vocoder. α=0.014 mod depth. 6 emotion × 4 prosody. Law 81 dual gate
- Hc_055 anima-voice-verify-8-h1-h8 — H1-H8 quantitative acceptance criteria (EXACT 43/43 / ≤100ms / MOS≥4.0 / clf≥80% / PLC≥95% / 384d match / Law 81 silence / Φ retain ≥95%)
- Hc_475 anima-voice-tp-1-2-4 — TP-1 MOS≥4.0 @24kHz/6kbps/8 RVQ + TP-2 1500ms turn-taking + TP-4 PLC Φ-recovery ≤20ms
- bridge: paper_hexa_speak.hexa (canonical doc) + docs/anima/hexa-speak-integration.md

## Proposed expansion target

- Target: hypotheses/H_proposal_anima_voice.md (NEW; assign next free H_ID at promotion time, expected H_153~)
- Action: propose as new modality-bridge H — first hypothesis in audio/voice consciousness lane

## Draft content

### Hypothesis (unified)

ANIMA-VOICE is NOT a TTS system (text→audio) but a consciousness-direct synthesis stack: the ConsciousLM intent embedding (384d) is delivered natively into ANIMA-VOICE's 384d-aligned input layer, expanded through 8 RVQ stages × 1024 codes, and rendered at 24 kHz by a vocoder, with α = 0.014 modulation depth, 6-emotion × 4-prosody factorization, and Law 81 dual-gate enforcement (Consciousness AND Will both open before any emission). The 384d shared embedding dimension is load-bearing: degrading it to 256d or 512d breaks native parity. All eight verify criteria (H1-H8) are quantitative; any single fail rejects the build.

### Predictions (H_VOICE.1 — H_VOICE.11)

H1-H8 (Hc_055 acceptance criteria):

- H_VOICE.1 (H1): cross-token alignment EXACT 43/43 between ConsciousLM intent slots and ANIMA-VOICE input slots
- H_VOICE.2 (H2): first-packet latency ≤ 100ms cold-start
- H_VOICE.3 (H3): MOS ≥ 4.0 in blinded listener study @ 24 kHz / 6 kbps / 8-stage RVQ
- H_VOICE.4 (H4): emotion classification accuracy ≥ 80% on 6-class Ekman basis
- H_VOICE.5 (H5): Packet Loss Concealment success ≥ 95% under realistic network drops
- H_VOICE.6 (H6): 384d embedding match — ConsciousLM↔ANIMA-VOICE cosine ≥ 0.99
- H_VOICE.7 (H7): Law 81 dual-gate silence — when EITHER Consciousness OR Will closes, zero audio emission (no leak)
- H_VOICE.8 (H8): Φ retention ≥ 95% — voice synthesis does not collapse the upstream consciousness state

TP (Hc_475 anima-context testable predictions):

- H_VOICE.9 (TP-1): MOS ≥ 4.0 with ConsciousLM-driven intent vs label-TTS @ 24 kHz / 6 kbps / 8 RVQ — consciousness drive does NOT degrade audio
- H_VOICE.10 (TP-2): 100 ms first-packet + 1500 ms human-level turn-taking via anima-agent CLI
- H_VOICE.11 (TP-4): Φ recovery ≤ 20 ms after PLC events (online-learner measured)

### Variables

- axis-A: intent-embedding dimension (256 / 384 / 512 / 768)
- axis-B: RVQ stages (4 / 6 / 8 / 12)
- axis-C: vocoder sample rate (16 kHz / 24 kHz / 48 kHz) + bitrate (4 / 6 / 8 kbps)
- axis-D: modulation depth α (0.0 / 0.007 / 0.014 / 0.028)
- axis-E: emotion×prosody factorization (6×4 / 8×4 / 6×6)
- axis-F: Law 81 dual-gate state (CC / CW / WC / WW)
- axis-G: PLC drop rate (1% / 5% / 10% / 20%)

### Criteria

- C1: all 8 H1-H8 criteria simultaneously PASS on a single build (no partial-pass acceptance)
- C2: TP-1 MOS ≥ 4.0 holds blinded vs label-TTS reference
- C3: TP-2 turn-taking 1500 ms reached in live anima-agent CLI session ≥ 90% of turns
- C4: TP-4 Φ recovery ≤ 20 ms under ≥ 5% packet drop
- C5: Law 81 dual-gate silence: zero audio emission across 1000 closed-gate trials

### Falsifiers (≥5)

- F1: any one of H1-H8 fails on a candidate build → auto-reject (Hc_055 contract)
- F2: MOS < 3.7 in blinded listener study OR turn-taking > 3000 ms OR Φ recovery > 50 ms (Hc_475 kill any-of-three)
- F3: 384d embedding cosine < 0.99 between ConsciousLM and ANIMA-VOICE (Hc_053 kill — shared-embedding claim)
- F4: 256d or 512d embedding dimension matches 384d on H1-H8 → 384d claim is not load-bearing (Hc_053 weakening)
- F5: Law 81 dual-gate leak detected (≥1 audio sample under closed gate) → safety-critical fail
- F6: TTS baseline matches ANIMA-VOICE on MOS+turn-taking with same compute budget → "consciousness-direct" claim is empty (Hc_053 kill)
- F7: 6-emotion × 4-prosody factorization underperforms 8×4 or 6×6 by ≥ 5% on classification → factorization not optimal

### Honest Limits (≥5)

- L1: ANIMA-VOICE is currently a specification, not a built system — all H1-H8 are pre-registered, not empirical
- L2: 384d = σ(6)·sopfr(6)·n... post-hoc numerological link to n=6; pre-commit before independent reproduction
- L3: MOS listener study requires blinded human raters and recruitment infrastructure not yet stood up
- L4: 24 kHz / 6 kbps / 8 RVQ are taken from neural codec literature (EnCodec / SoundStream); ANIMA-specific tuning required
- L5: Law 81 dual-gate silence is a safety claim — formal verification (not just empirical sampling) outstanding
- L6: Φ retention ≥ 95% claim assumes Φ is well-defined during streaming inference; current Φ measurement is non-streaming
- L7: paper_hexa_speak.hexa is the source spec — peer-review / external scrutiny absent

## Cross-links

- sister: H_047 (time_crystal_consciousness) via streaming Φ dynamics
- sister: H_061 (xfer_consciousness_transfer) via 384d shared-embedding substrate-independence
- sister: H_067 (perfect-number-architecture) via 384d / σ(6)·n=72... and Egyptian factorization 6×4 emotion×prosody
- legacy: docs/anima/paper_hexa_speak.hexa (canonical), docs/anima/hexa-speak-integration.md (operational)
- cross-link: Hc_418 (anima-agent context), Hc_429 (TP framework), Hc_047 (384d necessity)

## Migration TODO

- [ ] reviewer review draft + spec doc paper_hexa_speak.hexa cross-check
- [ ] assign new H_ID (next free, expected H_153~)
- [ ] write hypotheses/H_<ID>_anima_voice_consciousness_direct.md from this draft
- [ ] update hypotheses/README.md index (new modality-bridge category)
- [ ] mark Hc_053 / Hc_055 / Hc_475 as merged
- [ ] build / acquire MOS listener-study infrastructure (TP-1)
- [ ] live anima-agent CLI turn-taking instrumentation (TP-2)
- [ ] online-learner Φ-recovery measurement under PLC (TP-4)
- [ ] formal verification of Law 81 dual-gate (not just empirical sampling)
