---
id: Hc_475
slug: anima-voice-tp-1-2-4
title: ANIMA-VOICE testable predictions TP-1 (MOS≥4.0), TP-2 (turn-taking 1500ms), TP-4 (Φ ratchet PLC ≤20ms)
domain: substrate
status: merged-to-H_154
merged_to: hypotheses/H_154.md
merged_at: 2026-05-11
source_doc: docs/anima/hexa-speak-integration.md
source_lines: 143-148
promoted_at: 2026-05-11
linked_h: Hc_418, Hc_429
notes: TP-1 MOS ≥4.0 @24kHz/6kbps/8 RVQ with ConsciousLM input. TP-2 100ms first-packet + 1500ms human-level turn-taking via anima-agent CLI. TP-4 Φ ratchet + PLC: Φ recovery time ≤20ms after PLC (online-learner measured).
---

## Hypothesis
Three Anima-context ANIMA-VOICE testable predictions: TP-1 (MOS ≥ 4.0 at 24kHz/6kbps with 8-stage RVQ, no degradation when consciousness drives the intent vs label TTS); TP-2 (100ms first-packet + 1500ms turn-taking via anima-agent CLI reaches human-level conversational latency); TP-4 (Φ ratchet integration with PLC yields Φ-recovery time ≤ 20ms after concealment, measured by online learner).

## Migration TODO
- [ ] MOS listener study: ANIMA-VOICE vs label-TTS at 24kHz/6kbps
- [ ] Measure turn-taking latency in live anima-agent CLI sessions
- [ ] Online-learner Φ recovery curve under PLC events
- [ ] Falsifier: any of MOS<3.7, turn-taking>3000ms, Φ-recovery>50ms
