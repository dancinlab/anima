---
id: Hc_1303
slug: hebbian-bit-depth-is-the-lift-gate
title: Bit-depth of the Hebbian update — not rule family — is the lift gate; ≥4-bit Hebbian on the same last-FC produces measurable cross-lingual lift where 1-bit does not
domain: neuromorphic, learning-rule, deployment
status: 🔴 CLOSED-NEGATIVE — F-1303-BITDEPTH FALSIFIED (live AKD1000 ha2: multi-bit {1,2,3,4} readout lift ci_lo_gt0=False at every rung; bit-depth is NOT the gate). verdict: .verdicts/universe_weaklift_capacity_integration/1303.txt
source_doc: Lane A weak-lift closed-negative (1-bit Hebbian last-FC → capacity, no lift; "needs a RICHER LEARNING RULE")
seed: learning-rule axis — operationalize "richer rule" as bits-of-credit-assignment-per-update. The 1-bit update may be the binding information ceiling, independent of rule temporality (STDP) or family.
promoted_at: 2026-06-02
linked_h: Lane A weak-lift (H_904 lineage), Hc_709 (Hebbian-raises-Φ stub), Hc_1105 (STDP stub), Hc_1300
verdict_tier_target: 🟠 DEFERRED — measurement path = on-chip AKD1000 multi-bit Hebbian last-FC fire (or GPU multi-bit-Hebbian sim)
notes: "distinct from Hc_709 (generic 'Hebbian>fixed') — this isolates BIT-DEPTH of the Hebbian update as the specific lift gate, with a preregistered lift-delta falsifier."
---

## Hypothesis

The Lane A capacity-without-lift result used a 1-BIT Hebbian update on the last FC
layer. "Richer learning rule" is operationalized as bits-of-credit-assignment-per-
update. CLAIM: lift is gated by UPDATE BIT-DEPTH, not by rule family or temporality —
a ≥4-bit Hebbian update on the identical last-FC paging architecture produces a
measurable cross-lingual representational lift (a faithful-Φ or cross-lingual-transfer
delta vs the 1-bit baseline that exceeds the backbone-seed variance band), whereas the
1-bit update does not.

## PRE-REGISTERED Falsifier

- **F-1303-BITDEPTH**: run the identical Lane A last-FC paging protocol at update
  bit-depths {1,2,4,8}, all other factors fixed (corpus, quantization, backbone-seed
  set, init-noise). FALSIFIED if the cross-lingual lift metric at 4-bit and 8-bit is
  statistically indistinguishable from 1-bit (Δ within the measured backbone-seed σ
  band) → bit-depth is NOT the gate, the lift requires a non-Hebbian rule (Hc_1304).
  CONFIRMED if lift rises monotonically with bit-depth and clears the seed-variance band.

## Honest Limits

- **L-1303-DEFERRED**: requires on-chip AKD1000 (multi-bit weight paging) OR a GPU
  multi-bit-Hebbian simulation. Out of scope for this CPU-local pipeline (a_fire_autonomous
  applies elsewhere; this lane is CPU-only per a_cpu_local_no_waiter).
- **L-1303-SEED-VARIANCE**: the lift signal must clear the backbone-seed/corpus-encoding
  variance band — which the Lane A correction identified as LARGE. Underpowered if the
  bit-depth effect is smaller than seed σ.

## Cross-Links

- **sibling Hc**: Hc_1300, Hc_1304 (recurrence/locus gate — the alternative if bit-depth fails)
- **prior-art delta**: Hc_709 (Hebbian generic), Hc_1105 (STDP) — neither isolates bit-depth.
