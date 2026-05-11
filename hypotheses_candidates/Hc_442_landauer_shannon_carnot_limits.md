---
id: Hc_442
slug: landauer-shannon-carnot-limits
title: SoC claims must not exceed Landauer (kT·ln2) / Shannon (BW·log₂(1+SNR)) / Carnot (1−T_c/T_h) limits
domain: physics
status: merged-to-H_067
merged_to: hypotheses/H_067.md
merged_at: 2026-05-11
source_doc: docs/spec/anima-soc/anima-soc.md
source_lines: 303-306, 500-513
promoted_at: 2026-05-11
linked_h: Hc_036
notes: §7.5 LIMITS check. Claims violating fundamental limits are rejected. Operationalized physical-limit verification.
---

## Hypothesis
Every quantitative SoC performance claim (energy per operation, channel capacity, thermodynamic efficiency) must satisfy the three fundamental limits: (1) Landauer minimum E ≥ kT·ln2 per bit erasure; (2) Shannon channel capacity C ≤ BW·log₂(1+SNR); (3) Carnot efficiency η ≤ 1 − T_c/T_h. Any architecture claim violating any one is rejected as physically impossible.

## Migration TODO
- [ ] Audit all current performance claims against the 3 limits
- [ ] Build automated limit checker in §7.5 stdlib
- [ ] Falsifier: a verified claim exceeding any limit
- [ ] Document margin: how close are realistic anima-soc claims to each limit?
