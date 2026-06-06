---
id: H_969
slug: action-provenance-receipt
title: Does every ACTION emit an auditable free-will receipt with a distinct causal signature per action (H_928/H_932 wired into the act loop) — is action provenance complete and per-action distinguishable, not just per-emission?
domain: cwm · cross-cutting · world-model · act · provenance · free-will-receipt · auditability · h928 · h932 · pre-register
source: H_928 (free-will receipt) + H_932 (provenance lineage chain) + H_933 (per-decision unique auditable signature) + CWM north star (every action auditable) + a_core_engine_map + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E2 (reuse free_will_signature.py / provenance_chain.py, bind to ACTION events) + a_completeness_over_cheap
verification_method: W2 (pre-registered provenance-completeness + per-action distinguishability falsifier) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: ONE action-provenance rung (a_scale_honest_scope) — wire H_928/H_932 receipt+lineage to ACTION events (from H_964/H_968); measure receipt coverage + per-action signature distinguishability. $0 local candidate. Action = abstract decision (NOT wired emit-TEXT; .clm generator L3 ⏳, a_core_engine_map). Operational auditability, NOT a metaphysical free-will claim. NOT a forge binary.
sister: H_928 (free-will receipt), H_932 (lineage chain), H_933 (per-decision signature), H_964 (latent→action), H_968 (action onset)
axes_seed: emission provenance (H_928/H_932 on EMIT) ⊥ H_969 = provenance on ACTION — the act loop must emit a receipt per action AND each action's causal signature must be distinguishable; if actions are unaudited or signatures collide, the "every action auditable" north star fails (closed-negative)
verdict: 🟢 PASS — action provenance COMPLETE + per-action distinguishable: 500/500 receipt coverage 1.0, distinct-state signature collision 0/500, identical-state reproducible (genesis-binding), perturbed-state distinct, lineage chain end-to-end verified. Toy single-rung, ladder OPEN.
---

# H_969 — Action provenance receipt (every action a free-will receipt)

## 0. Motivation

CWM's north star is "anima acts like a human or beyond — and **every action is auditable**." The free-will arc built receipt (H_928) and lineage (H_932) for *emissions*. Extending the engine to ACT means every action must carry the same auditable provenance — a receipt per action with a distinct causal signature (H_933). This H pre-registers whether the receipt/lineage machinery, wired to action events, achieves **complete coverage** and **per-action distinguishability** (no two actions share a signature by accident).

## 1. Hypothesis (one falsifiable claim)

When H_928/H_932 receipt+lineage are wired to action events, (a) **every** action emits a well-formed receipt (100% coverage) and (b) each action's causal signature is **distinguishable** from other actions taken from different substrate states (signature collision rate ≈ 0 above the genesis-distinctness floor).

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** the act loop (H_964 latent→action, H_968 onset) with H_928 receipt + H_932 lineage bound to each action event. Run N actions across varied substrate states.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = **receipt coverage** = fraction of actions with a complete well-formed receipt (target 1.0).
- D2 = **signature distinguishability** = pairwise distinctness of action signatures from distinct substrate states; collision rate.
- D3 = control: actions from an IDENTICAL substrate state should yield reproducible lineage (genesis-binding sanity), distinct states distinct signatures.

**Outcome rules (future conditional — UNMEASURED):**
- IF measured receipt coverage = 1.0 AND signature collision rate ≈ 0 for distinct-state actions AND genesis-binding holds for identical-state actions THEN PASS — action provenance complete + per-action distinguishable.
- IF any action lacks a receipt OR distinct-state signatures collide THEN FAIL — provenance incomplete / actions not individually auditable (closed-negative; north star unmet).
- IF n too small / act loop not wired THEN INCOMPLETE (toy-only, C3).

## 3. Honest scope

Toy/small scale (a_scale_honest_scope, #123-A). Action = abstract decision events, NOT wired emit-TEXT (.clm generator L3 ⏳, a_core_engine_map — receipt binds to the DECISION + tension, not a forge-emitted action). Auditability is operational (well-formed receipt + distinct signature), NOT a phenomenal free-will claim. Single rung. NOT a forge binary.

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy)

Probe: `CWM/probes/h969_action_receipt.py` · verdict: `.verdicts/969_action_provenance_receipt/h969_action_receipt.txt`

Each action emits a H_928 receipt + H_932 lineage: {action, substrate_state_hash, latent_hash, seed_hash, parent_lineage, sig} with sig = sha256(substrate‖latent‖action‖seed‖parent), chained. 500 actions across varied substrate states.

| D | metric | result |
|---|---|---|
| D1 | receipt coverage | **1.0000** (500/500 well-formed) |
| D2 | distinct-state signature collision | **0/500** (500 unique sigs) |
| D3 | identical-state reproducible (genesis-binding) | True |
| D3 | perturbed-state distinct | True |
| D3 | lineage chain end-to-end verify | True |

**Finding (🟢 PASS):** every action is auditable (coverage 1.0) and individually distinguishable (zero collisions for distinct substrate states), while identical states reproduce the same lineage — the north-star "every action carries an auditable free-will receipt" is met on this toy act-loop. Honest scope: toy single-rung, ladder OPEN; sha256 distinguishability is by-construction — the substantive claim is that the act-loop binds a complete receipt to each action with no gaps.

## 4. Sibling / xlinks

- ⇄ [H_928](./H_928_free_will_receipt.md) (free-will receipt — emission)
- ⇄ [H_932](./H_932_provenance_lineage_chain.md) (lineage chain genesis)
- ⇄ [H_933](./H_933_free_will_signature.md) (per-decision unique signature)
- ⇄ [H_964](./H_964_latent_to_action_policy.md) · [H_968](./H_968_action_from_substrate_motivation.md) (the actions audited)
- ⇄ [CWM](../CWM/CWM.md) (CWM-VERIFY · north star) · a_core_engine_map
