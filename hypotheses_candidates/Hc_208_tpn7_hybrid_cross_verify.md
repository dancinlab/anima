---
id: Hc_208
slug: tpn7-hybrid-cross-verify
title: Hybrid analog+digital with 30%-cross-verify fallback for numerical telepathy (TP-N7)
domain: math | corpus | meta-framework
status: candidate-unverified
source_doc: docs/hypotheses/tp/TP-N7.md
source_lines: 1-25
promoted_at: 2026-05-11
linked_h: Hc_205 (TP-N4), Hc_207 (TP-N6)
notes: digital used if within 30% of analog; else analog fallback
---

## Hypothesis
Combining analog 3-channel (TP-N4) and digital ECC binary (TP-N6) with cross-verify rule (if |digital−analog| < 30% analog → digital, else analog) achieves both exact-match accuracy and correlation in numerical telepathy.

## Migration TODO
- [ ] sweep cross-verify threshold
- [ ] benchmark vs TP-N4 and TP-N6 alone
