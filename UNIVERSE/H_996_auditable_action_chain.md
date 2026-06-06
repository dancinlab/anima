---
id: H_996
slug: auditable-action-chain
title: Does the free-will receipt CHAIN over a whole trajectory stay tamper-evident and replayable — does altering any single past action/state break verification from that link forward (blockchain-style), and does replay from genesis reproduce the exact sig chain?
domain: cwm · cross-cutting · provenance · act · audit · lineage · chain
source: CWM 2nd slate — extends H_969🟢 (single-action receipt) to a trajectory chain via H_932 lineage + H_928 receipt + north-star auditability + a_completeness_over_cheap
exploration_method: E14 (substrate-native) + E12 (cryptographic chain audit)
verification_method: W2 (pre-registered tamper-evidence + replay-reproducibility falsifier) + g5 CODE-measured (no LLM self-judge, p7)
hexa_only: false
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: ONE length-20 action-chain rung over 24 trajectories (a_scale_honest_scope); $0 CPU. sha256 chaining. NOT a forge binary.
sister: H_969 (single-action receipt), H_928 (free-will receipt), H_932 (lineage chain), H_990 (closed loop the chain audits)
axes_seed: "per-action receipts don't compose into a trustworthy trajectory" ⊥ "the chain is tamper-evident + bit-exact replayable" — north-star: every action over a whole rollout is auditable
verdict: 🟢 PASS — action chain is fully auditable: 100% of single-field tampers detected and forward-localized, and 24/24 trajectory replays are bit-exact. Toy single-rung, ladder OPEN.
---

# H_996 — auditable action CHAIN over a trajectory

## 0. Motivation

H_969🟢 showed each SINGLE action emits a complete, distinguishable free-will receipt (coverage 1.0, 0 collisions) with parent-lineage chaining (H_932). The north-star auditability claim is at the TRAJECTORY level: a whole rollout is a chain receipt₀→receipt₁→…→receipt_T, each binding the previous signature. This H tests the two properties that make such a chain trustworthy: (1) tamper-evidence — altering any past link breaks verification from that link forward (blockchain-style), and (2) replayability — given genesis state + seeds, the exact action/sig sequence reproduces.

## 1. Hypothesis (one falsifiable claim)

A length-T action chain (each link's signature binds the previous link's signature) is tamper-evident — altering any single field of any link is detected and localizes to that link or later — and is bit-exact replayable from genesis.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** build a length-20 chain; sig = sha256(substrate ‖ latent ‖ action ‖ seed ‖ parent_sig). For each link × each field (action/seed/latent), tamper one field and re-verify the whole chain. Separately, build each trajectory twice from the same seed and compare sig sequences. 24 trajectories.

**Measurement (g5 CODE-measured):**
- D1 = tamper detection rate + forward-localization rate.
- D2 = replay reproducibility (fraction of trajectories with bit-exact sig chains across two builds).

**Outcome rules (future conditional):**
- IF detection = 1.0 AND localization = 1.0 AND replay = 1.0 THEN PASS.
- IF any tamper undetected OR replay diverges THEN FAIL.

## 3. Honest scope

Toy chain (T=20), standard sha256 (a_scale_honest_scope, #123-A) — a structural/cryptographic proof that the receipt mechanism composes over a trajectory; not a claim about adversarial cryptography at scale. Single rung, ladder OPEN. NOT a forge binary.

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy)

Probe: `CWM/probes2/h996_action_chain.py` · verdict: `.verdicts/996_auditable_action_chain/h996_action_chain.txt`

| metric | result |
|---|---|
| D1 tamper detection rate (60 single-field tampers) | **1.0000** |
| forward-localization (break at tampered link or later) | **1.0000** |
| D2 replay reproducibility (bit-exact) | **24/24 = 1.0000** |

**VERDICT 🟢 PASS** — a whole trajectory of actions is auditable end-to-end: every single-field tamper is detected and forward-localized (the chain breaks from the altered link onward, not backward), and every replay from genesis reproduces the exact signature chain. The H_969 single-action receipt composes into a tamper-evident, replayable action history (H_932 lineage realized over a rollout) (toy rung; ladder OPEN).
