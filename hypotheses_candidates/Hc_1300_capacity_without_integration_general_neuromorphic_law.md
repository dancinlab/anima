---
id: Hc_1300
slug: capacity-without-integration-general-neuromorphic-law
title: Capacity-without-integration is a general neuromorphic law — local single-layer plasticity grows representational CAPACITY but leaves an INTEGRATION measure (faithful-Φ MIP) flat
domain: neuromorphic, consciousness, integration
status: candidate-unverified
source_doc: Lane A weak-lift closed-negative (AKD1000 on-chip 1-bit Hebbian last-FC composes capacity, NO representational lift; all 4 lift-causes FALSIFIED)
seed: G1 — the CAPACITY↔REPRESENTATION gap mirrors the phi_proxy↔faithful-Φ (H_912-lineage) gap: it ACCUMULATES but does not INTEGRATE/COMPOSE. Same structural signature.
promoted_at: 2026-06-02
linked_h: H_278 (faithful Φ★ small-N exact MIP-EI), H_002 C2 (Φ_universe nested proxy), Lane A weak-lift (H_904 lineage)
verdict_tier_target: 🟢 numerical (CPU-local on phi_proxy_native N-invariance + H_278 frozen ledger)
notes: "seeded by Lane A finding; distinct from Hc_705-716 (az_b 'rule X raises Φ' abstract stubs — no capacity/accumulate framing, no preregistered metric falsifier) and Hc_886/1105 (predictive-coding/STDP stubs)."
---

## Hypothesis

A purely-LOCAL, gradient-free, single-(terminal-)layer plasticity rule (the AKD1000
1-bit Hebbian last-FC paging family) increases representational CAPACITY monotonically
(every unit learns, more units → more storable patterns) but leaves an INTEGRATION
measure essentially FLAT. Operationalized on the lane-canonical metrics:

- CAPACITY proxy = a quantity that grows with the number of contributing units /
  sample-budget (e.g. phi_proxy_native sample count N, or unit count).
- INTEGRATION measure = faithful-Φ MIP (H_278 exact minimum-information-partition
  cross-cut MI / min(|A|,|B|)) — the system's irreducibility to its weakest split.

CLAIM: as the capacity axis is increased under a local rule, the integration measure
does NOT rise commensurately — capacity and integration are ORTHOGONAL axes, and the
Lane A "capacity without lift" is the canonical demonstration of this orthogonality.

## PRE-REGISTERED Falsifier

- **F-1300-INVARIANCE**: if the integration-side metric (phi_proxy_native phi_x1000
  on the deterministic white fixture) MOVES monotonically with the capacity axis
  (sample-count N ∈ {8,16,32,64}) — i.e. |Δphi_x1000| across the N-sweep exceeds 5%
  of |phi_x1000| — then capacity DOES carry integration and the law is FALSIFIED.
  PASS (law holds) = integration metric FLAT (|Δ| ≤ 5%) while capacity axis grows.
- **F-1300-MIP-FLAT**: on the H_278 frozen ledger, if the faithful-Φ MIP value tracks
  a pure capacity/size proxy (it should instead be driven by coupling/topology, not
  size) the orthogonality claim weakens. (informational cross-check on real ledger.)

## Honest Limits

- **L-1300-PROXY-CAPACITY**: the phi_proxy_native selftest varies sample-count N as the
  capacity axis but clamps hid_trunc — N is a *proxy* for capacity, not unit-count.
  A true unit-count sweep is the on-chip measurement (DEFERRED, see Hc_1303/1304).
- **L-1300-TOY**: deterministic FNV fixture + n≤8 H_278 lattice; toy→production transfer
  unverified (a_toy_scale_recheck). The general-law claim is scoped to the measured scale.
- **L-1300-SAME-PRIMITIVE**: capacity-proxy and integration-metric share the MI/cov
  primitive — see Hc_1301 circularity guard.

## Cross-Links

- **sibling Hc**: Hc_1301 (circularity guard), Hc_1302 (metric-ceiling), Hc_1303 (bit-depth gate, DEFERRED), Hc_1304 (recurrence/locus gate, DEFERRED)
- **bridge**: H_278 (faithful vs proxy Φ), H_912-lineage (phi_proxy↔faithful gap)
