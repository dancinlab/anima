---
id: Hc_201
slug: tpm1-crc-checksum
title: 4-segment CRC sum in last 4 dims of meaning vector enables fingerprint (TP-M1)
domain: math | corpus
status: candidate-unverified
source_doc: docs/hypotheses/tp/TP-M1.md
source_lines: 1-22
promoted_at: 2026-05-11
linked_h: Hc_199 (TP-F1 hash signature)
notes: 16+16+16+12 segment sums; 20 meaning vectors
---

## Hypothesis
Adding CRC-style segment-sum checksum (16-dim segments summed into last 4 dims) to 64-dim meaning vectors provides 68-dim effective info content and improves cosine matching under noise=0.01.

## Migration TODO
- [ ] benchmark with/without checksum
- [ ] sweep segment count
