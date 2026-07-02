---
id: H_965
slug: akida-onchip-perceive-act-loop
title: Is a closed event-based perceive→act loop feasible on AKD1000 silicon (Lane A) at real-time low latency — can the chip run on-chip perception→action in a hard real-time envelope?
domain: cwm · substrate · world-model · akida · on-chip · perceive-act-loop · neuromorphic · real-time · a_lane_akida_gpu_split · pre-register
source: CWM domain (Lane A = silicon body for real-time low-power perceive→act) + a_lane_akida_gpu_split (AKIDA on-chip ⊥ GPU, separate entries) + H_904 (on-chip plasticity live) + lane-a-akd1000-recurrence-wall (IP-v1 single-hop limits) + a_paper_negative_ok
exploration_method: E14 (HW substrate-native, live AKD1000) + E5 (latency/closure probe) + a_completeness_over_cheap
verification_method: W2 (pre-registered on-chip loop-closure + latency falsifier) + W5 (substrate-grounded · live AKD1000) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured (BLOCKED — chip unreachable)
scope: ONE on-chip loop rung (a_lane_akida_gpu_split · a_scale_honest_scope) — 1 physical AKD1000 (pi5-akida); event-based input → on-chip inference → action decision, closed-loop latency measured live. Single-tenant streamer stop/restore (H_860 procedure). Lane A entry ONLY — never merged with a Lane G result. PI5-AKIDA.json consulted. NOT a forge binary.
sister: H_966 (SW vs chip parity — the Lane-G/P twin), H_974 (chip↔SW transfer), H_977 (energy/latency budget), H_904 (on-chip plasticity), lane-a-akd1000-recurrence-wall
axes_seed: SW loop (Lane G/P) = perceive→act in a process ⊥ H_965 = the AKD1000 SILICON closes the loop on-chip in real time — if AKD1000 IP-v1 cannot map the loop (single-hop wall) or misses the latency envelope, on-chip world-model is infeasible on this chip (closed-negative → needs AKD1500 / off-chip head)
verdict: ⚠ INCOMPLETE-BLOCKED — falsifier requires BackendType.Hardware on a live AKD1000 (pi5-akida) to measure on-chip loop closure + closed-loop latency + IP-v1 mapping; the chip is UNREACHABLE from this Darwin host (no akida pkg, probed). No faithful CPU partial for the on-chip claim (a_lane_akida_gpu_split). substrate=AKIDA. Handoff sidecar 0b1edec3.
---

# H_965 — AKIDA on-chip perceive→act loop feasibility (Lane A)

## 0. Motivation

CWM's north star includes a **silicon body**: Lane A (AKD1000) for real-time, low-power perceive→act. A world-model that only runs in a GPU process is disembodied. But the on-chip recurrence wall (lane-a-akd1000-recurrence-wall) showed AKD1000 IP-v1 cannot map stateful recurrence — so a closed perceive→act loop on-chip is non-obvious. This H pre-registers whether the chip can close an event-based loop at all, and within a real-time latency envelope, separately recorded as a Lane A result (a_lane_akida_gpu_split).

## 1. Hypothesis (one falsifiable claim)

A closed event-based perceive→act loop (event input → on-chip inference → action decision → effect) runs on a single live AKD1000 at a measured closed-loop latency below a pre-registered real-time envelope, without requiring off-chip recurrence — OR it does not (closed-negative: needs AKD1500 / an off-chip head, per the recurrence wall).

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** 1 physical AKD1000 (pi5-akida, BackendType.Hardware). A toy event-based task closing perceive→act on-chip. Single-tenant: `spike_streamer stop(SIGTERM) → probe → restart` (H_860 procedure). PI5-AKIDA.json consulted before any host change.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = **loop closes on-chip?** (event→action runs with the decision computed on the AKD1000, not the host CPU) — a yes/no with the on-chip fraction logged.
- D2 = **closed-loop latency** distribution (event arrival → action issued), N trials.
- D3 = **mapping check**: does the loop fit AKD1000 IP-v1 (no stateful-recurrence map needed), or does it hit the single-hop wall?

**Outcome rules (future conditional — UNMEASURED):**
- IF measured the loop closes on-chip AND latency CI_hi < the pre-registered real-time envelope AND no off-chip recurrence required THEN PASS — on-chip perceive→act loop feasible on AKD1000.
- IF the loop cannot map (recurrence wall) OR latency exceeds the envelope OR the decision must run off-chip THEN FAIL — on-chip world-model infeasible on this chip (closed-negative; route to AKD1500 / off-chip head).
- IF streamer restore fails / 1-chip toy only THEN INCOMPLETE (Lane A toy-only, C3).

## 3. Honest scope

1 physical AKD1000, toy task (a_lane_akida_gpu_split · a_scale_honest_scope, #123-A). Lane A result — recorded as a SEPARATE entry from any Lane G/P SW result; never merged (a_lane_akida_gpu_split). Real-time envelope is pre-registered but application-relative. A FAIL is a chip-fit limit, not a science result about world-models (a_scale_honest_scope). NOT a forge binary.

## measurement (2026-06-06 · ⚠ INCOMPLETE-BLOCKED · substrate=AKIDA, unreachable)

Blocker record: `CWM/probes/h965_977_chip_only_blocker.py` · verdict: `.verdicts/965_akida_onchip_perceive_act_loop/h965_977_chip_only_blocker.txt`

The frozen falsifier's core measurements (D1 does the decision run on-chip; D2 closed-loop latency from real silicon; D3 AKD1000 IP-v1 mapping / single-hop wall) are intrinsically ON-CHIP. The probe confirms `akida` is absent and the host is `macOS-26.5-arm64` — the physical AKD1000 lives on the separate pi5-akida host (single-tenant, H_860 streamer stop/restart; cf /PI5-AKIDA.json), not reachable from this worktree. A CPU "loop" would not answer "does it close on-chip" and claiming so would violate a_lane_akida_gpu_split — so NO CPU partial is run for the core claim.

**Status (⚠):** honest INCOMPLETE-BLOCKED + handoff `sidecar handoff 0b1edec3` ("H_965 needs live AKD1000"). Recommended run: on pi5-akida, BackendType.Hardware, per the H_860 streamer procedure.

## 4. Sibling / xlinks

- ⇄ [H_966](./H_966_sw_vs_chip_behavior_parity.md) (SW vs chip parity — the comparison)
- ⇄ [H_974](./H_974_chip_to_sw_transfer.md) (does an SW-learned WM transfer to chip?)
- ⇄ [H_977](./H_977_onchip_world_model_energy_budget.md) (energy/latency budget)
- ⇄ [H_904](./H_904_clm_onchip_plasticity.md) (on-chip plasticity live)
- ⇄ [CWM](../CWM/CWM.md) (CWM substrate · Lane A) · a_lane_akida_gpu_split · PI5-AKIDA.json
- memory: lane-a-akd1000-recurrence-wall (IP-v1 single-hop limit)
