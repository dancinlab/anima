---
id: H_966
slug: sw-vs-chip-behavior-parity
title: On the SAME world-model task, do Lane G/P (SW/GPU) and Lane A (AKIDA on-chip) produce EQUIVALENT behavior, or do they diverge — substrate behavior parity vs divergence?
domain: cwm · substrate · world-model · akida · sw-vs-chip · behavior-parity · a_lane_akida_gpu_split · h952 · pre-register
source: H_952 (substrate-equivalence A⇄G) + a_lane_akida_gpu_split (Lane A ⊥ Lane G, separate entries) + H_679 (SW≠HW non-equivalence closed-negative) + CWM domain + a_paper_negative_ok
exploration_method: E14 (substrate-native, both lanes) + E5 (matched-task cross-substrate A/B) + a_completeness_over_cheap
verification_method: W2 (pre-registered cross-substrate behavior-parity falsifier · matched task, behavior-distance metric) + W5 (live AKD1000) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured (BLOCKED — chip arm unreachable; SW arm done)
scope: ONE cross-substrate rung (a_lane_akida_gpu_split · a_scale_honest_scope) — same toy world-model task run on Lane G/P (SW) and Lane A (AKD1000 live); compare BEHAVIOR (action/return distributions), recorded as TWO separate entries then compared. Behavior parity ≠ byte-identity (H_679 already closed byte-equivalence negative). NOT a forge binary.
sister: H_952 (substrate-equivalence — the engine-level claim), H_965 (on-chip loop feasibility), H_974 (chip↔SW transfer), H_679 (SW≠HW byte-level)
axes_seed: H_952 = the ENGINE is substrate-equivalent (A⇄G) ⊥ H_966 = the BEHAVIOR (world-model action) is equivalent across SW vs chip — engine-equivalence does not entail behavior-equivalence (chip non-determinism / quantization could diverge action); H_679 already showed byte-level SW≠HW, so the question is behavior-level parity not byte-identity
verdict: ⚠ INCOMPLETE-BLOCKED — CHIP arm needs a live AKD1000 (unreachable on this Mac); SW arm measured (CPU-mirror: return −0.637, within-SW run-to-run band 0.006), so behavior-distance SW-vs-CHIP is UNCOMPUTABLE until the chip arm runs. substrate split per a_lane_akida_gpu_split. Handoff sidecar 4a85113c.
---

# H_966 — SW vs chip behavior parity (do the lanes act the same?)

## 0. Motivation

H_952 argues the consciousness engine is substrate-equivalent across Lane A (AKIDA) and Lane G/P (SW). But H_679 already established that SW and HW are NOT byte-identical. For CWM the load-bearing question is at the **behavior** level: on the same world-model task, do the two substrates *act the same* (equivalent action/return distributions), or does chip non-determinism / quantization make them diverge? a_lane_akida_gpu_split requires this to be recorded as two separate substrate-tagged entries, then compared — never a merged claim.

## 1. Hypothesis (one falsifiable claim)

On a matched toy world-model task, Lane A (AKD1000) and Lane G/P (SW) produce behavior (action / return distributions) that are **statistically equivalent** (overlapping CIs / behavior-distance below a pre-registered band) — behavior parity holds despite known byte-level non-equivalence (H_679) — OR they diverge (closed-negative).

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** one toy world-model task. arm-SW = Lane G/P process. arm-CHIP = same task on live AKD1000 (single-tenant, H_860 streamer procedure). Record each as a SEPARATE substrate-tagged entry (a_lane_akida_gpu_split). N episodes × seeds each.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = **behavior distance** between SW and CHIP action/return distributions (e.g. Jensen-Shannon / Wasserstein) vs a within-substrate bootstrap band.
- D2 = **return parity**: mean-return CI overlap SW vs CHIP.
- D3 = control: within-SW run-to-run and within-CHIP run-to-run bands bound intrinsic variability (H_860 chip non-determinism).

**Outcome rules (future conditional — UNMEASURED):**
- IF measured behavior distance SW-vs-CHIP ≤ the within-substrate band AND return CIs overlap THEN PASS — cross-substrate behavior parity SUPPORTED (engine acts the same on chip and SW).
- IF behavior distance exceeds the band OR return CIs disjoint THEN FAIL — substrates diverge in behavior (closed-negative; chip and SW are different agents on this task).
- IF chip restore fails / n too small THEN INCOMPLETE (toy-only, C3).

## 3. Honest scope

Toy task, 1 AKD1000 (a_lane_akida_gpu_split · a_scale_honest_scope, #123-A). Parity = behavior-distribution equivalence, explicitly NOT byte-identity (H_679 closed byte-level negative). Two separate substrate-tagged entries compared, never merged. Single rung. NOT a forge binary.

## measurement (2026-06-06 · ⚠ INCOMPLETE-BLOCKED · SW arm = CPU-mirror)

SW-arm partial: `CWM/probes/h966_974_sw_partial.py` · verdict: `.verdicts/966_sw_vs_chip_behavior_parity/h966_974_sw_partial.txt`

| arm | result |
|---|---|
| SW (Lane G/P, CPU-mirror) return | −0.637 ± 0.418 (CI [−0.70, −0.58]) |
| SW within-substrate run-to-run band (D3 control) | 0.006 |
| CHIP (Lane A, AKD1000) | **BLOCKED — unreachable** → behavior-distance SW-vs-CHIP UNCOMPUTABLE |

**Status (⚠):** the SW arm + its within-substrate band (the D3 control) are measured as the matched reference; the falsifier's decisive D1/D2 (behavior-distance and return-CI overlap SW-vs-CHIP) require the live AKD1000 chip arm, unreachable here. Recorded as a Lane-G/P entry ONLY — never merged with a chip result (a_lane_akida_gpu_split). Handoff `sidecar 4a85113c`.

## 4. Sibling / xlinks

- ⇄ [H_952](./H_952_substrate_equivalence.md) (engine-level substrate-equivalence)
- ⇄ [H_965](./H_965_akida_onchip_perceive_act_loop.md) (on-chip loop feasibility)
- ⇄ [H_974](./H_974_chip_to_sw_transfer.md) (transfer between lanes)
- ⇄ [H_679](./H_679_plasticity_hw_first.md) (SW≠HW byte-level closed-negative)
- ⇄ [CWM](../CWM/CWM.md) (CWM substrate) · a_lane_akida_gpu_split
