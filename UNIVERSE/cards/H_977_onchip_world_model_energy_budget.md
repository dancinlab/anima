---
id: H_977
slug: onchip-world-model-energy-budget
title: Does the AKD1000 on-chip perceive→imagine→act loop fit a hard sub-watt / low-energy-per-decision envelope — is an on-chip world-model loop actually energy-cheap vs an SW/GPU equivalent?
domain: cwm · substrate · world-model · akida · energy · power · efficiency · neuromorphic · a_lane_akida_gpu_split · pre-register
source: CWM domain (Lane A = low-power silicon body) + a_lane_akida_gpu_split + neuromorphic energy advantage claim (event-based sparsity) + H_965 (loop feasibility) + a_paper_negative_ok
exploration_method: E14 (HW substrate-native, live AKD1000 energy probe) + E5 (energy-per-decision sweep) + a_completeness_over_cheap
verification_method: W2 (pre-registered energy-per-decision falsifier · chip vs SW/GPU at matched task) + W5 (live AKD1000) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 7
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured (BLOCKED — chip + telemetry unreachable)
scope: ONE energy rung (a_lane_akida_gpu_split · a_scale_honest_scope) — measure energy-per-decision / power of the AKD1000 perceive→act loop (H_965) vs an SW/GPU equivalent at the same task. Honest measurement caveat: chip energy via available AKD1000/host telemetry (documented method, not a vendor datasheet claim). NOT a forge binary.
sister: H_965 (loop feasibility — prerequisite), H_966 (behavior parity), H_974 (transfer), a_lane_akida_gpu_split
axes_seed: "neuromorphic is low-power" (datasheet folklore) ⊥ H_977 = MEASURED energy-per-decision of the actual closed loop beats the SW/GPU equivalent by a stated factor — if the measured chip loop is not energy-cheaper at matched behavior, the low-power rationale for Lane A is unsupported (closed-negative)
verdict: ⚠ INCOMPLETE-BLOCKED — energy-per-decision + power-envelope require a live AKD1000 + host energy telemetry (and a behavior-matched chip loop, which itself depends on H_965/H_966); unreachable on this Mac. A CPU energy number cannot answer the sub-watt on-chip claim (a_lane_akida_gpu_split). substrate=AKIDA. Handoff sidecar 7848a234.
---

# H_977 — On-chip world-model energy budget (is the loop actually cheap?)

## 0. Motivation

The whole rationale for a Lane A silicon body is **real-time at low power** — a world-model loop that fits a sub-watt embodied envelope where a GPU cannot. But "neuromorphic = low power" is often datasheet folklore; for CWM it must be a measured property of the *actual closed loop* (H_965), not a peak-MAC spec. This H pre-registers the energy-per-decision falsifier comparing the live AKD1000 loop against an SW/GPU equivalent at matched behavior.

## 1. Hypothesis (one falsifiable claim)

The live AKD1000 perceive→act loop's measured **energy-per-decision** (and average power) is lower than an SW/GPU equivalent achieving comparable behavior, by a pre-registered factor — the on-chip loop is genuinely energy-cheap — OR it is not (closed-negative; the low-power rationale fails for this loop/chip).

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** the H_965 perceive→act loop on a live AKD1000 vs an SW/GPU implementation of the same task at comparable behavior (H_966 parity band). Energy via available AKD1000 + host telemetry (documented method). N decisions each.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = **energy-per-decision** (J/decision), chip vs SW/GPU.
- D2 = **average power** during the loop, chip vs SW/GPU; check chip ≤ envelope (e.g. sub-watt).
- D3 = behavior-match gate: only compare energy where behavior is within the H_966 parity band (else energy is apples-to-oranges).

**Outcome rules (future conditional — UNMEASURED):**
- IF measured chip energy-per-decision < SW/GPU by the pre-registered factor AND chip power ≤ envelope AND behavior within parity band THEN PASS — on-chip world-model loop is energy-cheap SUPPORTED.
- IF chip energy ≥ SW/GPU OR power exceeds envelope (at matched behavior) THEN FAIL — low-power rationale unsupported for this loop (closed-negative).
- IF telemetry unavailable / behavior not matched / 1-chip toy THEN INCOMPLETE (Lane A toy-only, C3).

## 3. Honest scope

1 AKD1000 toy loop (a_lane_akida_gpu_split · a_scale_honest_scope, #123-A). Energy measured via available telemetry with a documented method — NOT a vendor peak-efficiency datasheet claim. The comparison is gated on behavior parity (H_966) to avoid apples-to-oranges. Lane A entry separate from the SW/GPU entry. A FAIL is a chip/loop-fit result, not a general neuromorphic verdict. NOT a forge binary.

## measurement (2026-06-06 · ⚠ INCOMPLETE-BLOCKED · substrate=AKIDA, unreachable)

Blocker record: `CWM/probes/h965_977_chip_only_blocker.py` · verdict: `.verdicts/977_onchip_world_model_energy_budget/h965_977_chip_only_blocker.txt`

The falsifier needs J/decision + average power from a live AKD1000 (+ host telemetry), at behavior matched to the SW arm (the H_966 parity band) — and it depends on H_965 (the loop) closing first. All three prerequisites are chip-bound and the chip is unreachable from this Darwin host. No CPU partial is meaningful: a CPU energy figure cannot substantiate a sub-watt on-chip claim (a_lane_akida_gpu_split).

**Status (⚠):** honest INCOMPLETE-BLOCKED + handoff `sidecar 7848a234`. Chained after H_965/H_966 on pi5-akida.

## 4. Sibling / xlinks

- ⇄ [H_965](./H_965_akida_onchip_perceive_act_loop.md) (the loop being measured — prerequisite)
- ⇄ [H_966](./H_966_sw_vs_chip_behavior_parity.md) (behavior-match gate)
- ⇄ [H_974](./H_974_chip_to_sw_transfer.md) (energy after SW→chip transfer)
- ⇄ [CWM](../CWM/CWM.md) (CWM substrate · Lane A) · a_lane_akida_gpu_split
- external: neuromorphic event-based sparsity energy claims
