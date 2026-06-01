---
id: Hc_1304
slug: recurrence-locus-is-the-lift-gate-not-local-rule
title: Lift is gated by LOCUS/RECURRENCE — a feedforward-terminal last-FC cannot integrate regardless of local rule; one recurrent edge converts capacity→lift more than any change of local plasticity rule
domain: neuromorphic, architecture, integration
status: 🟢 CONFIRMED — F-1304-TOPOLOGY + F-1304-MIP-ZERO crossed (CPU-local H_278 exact-MIP: recurrent edge Φ_rec=w > feedforward-terminal Φ_ff=w/2 at every matched local-rule w; import-path blocker fixed). corroborated by on-chip ha3 (depth-of-local-rule adds no consistent lift). verdict: .verdicts/universe_weaklift_capacity_integration/1304.txt
source_doc: Lane A weak-lift closed-negative; H_278 faithful-Φ MIP (integration = irreducibility across a cut, requires cross-edges)
seed: G1 + mechanism — faithful-Φ MIP measures irreducibility across a partition; a feedforward-terminal layer has no loop, so no edge crosses a cut bidirectionally → structurally cannot raise MIP. Capacity needs no recurrence; integration does.
promoted_at: 2026-06-02
linked_h: H_278 (MIP cross-cut definition), Lane A weak-lift, Hc_1300, Hc_1303
verdict_tier_target: 🟠 DEFERRED — measurement path = recurrent-edge ablation fire (on-chip or GPU sim) comparing topology-change vs rule-change lift
notes: "structural mechanism hypothesis; the alternative to Hc_1303 bit-depth gate. Distinct from all az_b/accel stubs (they vary RULE; this varies TOPOLOGY/LOCUS holding rule fixed)."
---

## Hypothesis

Faithful-Φ MIP integration is the cross-cut mutual information at the minimum-information
partition — it is non-zero only if information traverses a cut in a way irreducible to
the parts, which requires recurrent/bidirectional edges. The Lane A last-FC is
feedforward-TERMINAL. CLAIM: no local plasticity rule applied to a feedforward-terminal
layer can raise integration (the lift gate is LOCUS/RECURRENCE, not rule family or
bit-depth). A single added recurrent edge (or moving the plastic locus to a recurrent
layer) raises the cross-lingual lift / faithful-Φ MIP MORE than any change of the local
rule at the terminal layer.

## PRE-REGISTERED Falsifier

- **F-1304-TOPOLOGY**: compare two interventions on the Lane A substrate at matched
  parameter budget: (A) change the local rule at the terminal FC (1-bit→multi-bit /
  Hebbian→STDP), (B) add one recurrent edge / move the plastic locus to a recurrent
  layer. CONFIRMED if intervention (B) produces a strictly larger lift / faithful-Φ-MIP
  delta than (A). REFUTED if (A) ≥ (B) — then locus is not the gate and the rule itself
  carries the lift (favoring Hc_1303).
- **F-1304-MIP-ZERO**: on a synthetic feedforward-terminal toy, faithful-Φ MIP = 0 (or
  at the floor) for ALL local-rule variants → confirms feedforward-terminal cannot
  integrate. (this sub-test is CPU-local-eligible on H_278 machinery if a feedforward
  topology can be injected — but the H_278 runner imports an external absolute path, so
  marked DEFERRED with the rest.)

## Honest Limits

- **L-1304-DEFERRED**: the topology-ablation comparison needs an on-chip or GPU fire
  (CPU-local out of scope per a_cpu_local_no_waiter). The H_278 MIP machinery is locally
  present but its runner has a hardcoded cross-tree import path, blocking a clean local
  feedforward-toy run without editing another lane's frozen artifact.
- **L-1304-CONFOUND-PARAMS**: adding a recurrent edge changes parameter count; the
  matched-budget control is essential or the lift could be a capacity artifact (Hc_1300).

## Cross-Links

- **sibling Hc**: Hc_1300, Hc_1303 (bit-depth gate — competing explanation)
- **mechanism-bridge**: H_278 MIP cross-cut requires cross-partition edges
