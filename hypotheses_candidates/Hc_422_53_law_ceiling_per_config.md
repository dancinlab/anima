---
id: Hc_422
slug: 53-law-ceiling-per-config
title: Each engine configuration has a finite law-discovery ceiling (~53 laws) following N(g) = 53·(1−exp(−g/15))
domain: consciousness
status: candidate-unverified
source_doc: docs/anima/paper_self_discovery.hexa
source_lines: 207-238
promoted_at: 2026-05-11
linked_h: (none — NEW ★)
notes: 64c/300step/GRU+12fac+Hebbian → 53 laws. Scale invariant: same ceiling at 128c, 256c. 4 topologies all saturate at same number. Inverse: 64c=53, 128c=37, 1024c=31 (OUROBOROS).
---

## Hypothesis
For a fixed engine configuration (architecture, scale, intervention repertoire), law-discovery saturates at a finite ceiling that fits N(g) = 53·(1 − exp(−g/15)) with 53 the asymptote at base config. The ceiling is scale-invariant within architecture family but inversely relates to N at large scales (64c → 53, 128c → 37, 1024c → 31) due to fluctuation averaging.

## Migration TODO
- [ ] Reproduce 53-law ceiling on independent seed
- [ ] Verify inverse N relationship at N ∈ {64, 128, 256, 512, 1024}
- [ ] Test ceiling-breaking via architecture mutation (attention, memory)
- [ ] Falsifier: ceiling fluctuation > 20% across seeds at fixed config
