---
id: H_974
slug: chip-to-sw-transfer
title: Does a world-model learned on Lane G/P (SW/GPU) TRANSFER to Lane A (AKIDA on-chip) behavior — i.e. an SW-trained WM mapped to the chip retains task performance (the sim-to-real inverse), or does the mapping break it?
domain: cwm · substrate · world-model · akida · sim-to-real · transfer · sw-to-chip · a_lane_akida_gpu_split · pre-register
source: CWM domain (SW train → chip deploy) + a_lane_akida_gpu_split + H_966 (behavior parity) + sim-to-real / quantization-aware deploy + lane-a-akd1000-recurrence-wall + a_paper_negative_ok
exploration_method: E14 (substrate-native, train SW → deploy chip) + E5 (transfer-gap probe) + a_completeness_over_cheap
verification_method: W2 (pre-registered transfer-gap falsifier · SW-train chip-deploy retained-performance) + W5 (live AKD1000) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 7
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: pre-registered (unmeasured)
scope: ONE transfer rung (a_lane_akida_gpu_split · a_scale_honest_scope) — train a toy world-model on Lane G/P SW, map/quantize to AKD1000, measure chip task performance vs the SW source. 1 AKD1000 live, single-tenant. Lane A deploy entry SEPARATE from the Lane G/P train entry. NOT a forge binary.
sister: H_966 (behavior parity — measured AFTER independent training; this is transfer of ONE trained WM), H_965 (on-chip loop), H_977 (energy budget), lane-a-akd1000-recurrence-wall
axes_seed: H_966 = two INDEPENDENTLY-run substrates compared ⊥ H_974 = ONE WM trained on SW then MAPPED to chip — transfer-gap (quantization / mapping loss) is a distinct question from independent-run parity; if the mapped WM loses performance, SW-train→chip-deploy is broken (closed-negative → needs chip-aware training)
verdict: ⏳ PENDING-MEASUREMENT
---

# H_974 — Chip-to-SW transfer (does an SW-trained WM survive on the chip?)

## 0. Motivation

The practical deployment path for an embodied world-model is **train on SW (Lane G/P, fast/cheap GPU), deploy on chip (Lane A, real-time/low-power)** — the inverse of robotics sim-to-real. But the AKD1000 mapping involves quantization and the IP-v1 structural limits (lane-a-akd1000-recurrence-wall). This H pre-registers whether an SW-trained world-model **retains performance** once mapped to the chip, distinct from H_966's independent-run parity (here a single WM crosses the boundary).

## 1. Hypothesis (one falsifiable claim)

A world-model trained on Lane G/P SW and mapped/quantized to a live AKD1000 retains task performance on-chip within a pre-registered transfer-gap band (chip return ≥ SW return − margin) — SW-train→chip-deploy is viable — OR the mapping breaks it (closed-negative).

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** train a toy world-model on Lane G/P SW (recorded as the SW entry). Map/quantize to AKD1000, deploy, evaluate the same task on-chip (recorded as a SEPARATE Lane A entry). Single-tenant streamer procedure. N episodes each.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = **transfer gap** = return_SW(source) − return_CHIP(deployed).
- D2 = **retained fraction** = return_CHIP / return_SW.
- D3 = control: a random-mapped (scrambled-weight) chip deploy bounds "any mapping works".

**Outcome rules (future conditional — UNMEASURED):**
- IF measured transfer gap ≤ margin (retained fraction ≥ pre-registered threshold, e.g. ≥0.8) AND beats the scrambled-mapping control THEN PASS — SW→chip transfer SUPPORTED.
- IF the gap exceeds margin / retained fraction below threshold / no better than scrambled THEN FAIL — transfer broken; SW-train→chip-deploy needs chip-aware training (closed-negative).
- IF mapping infeasible (recurrence wall) / chip restore fails THEN INCOMPLETE (Lane A toy-only, C3).

## 3. Honest scope

Toy WM, 1 AKD1000 (a_lane_akida_gpu_split · a_scale_honest_scope, #123-A). SW-train and chip-deploy recorded as SEPARATE substrate-tagged entries; the transfer gap is the only cross-lane number reported (never a merged lift). A FAIL is a deploy-path limit, not a science result (a_scale_honest_scope). Quantization scheme pre-registered. NOT a forge binary.

## 4. Sibling / xlinks

- ⇄ [H_966](./H_966_sw_vs_chip_behavior_parity.md) (independent-run parity — contrast)
- ⇄ [H_965](./H_965_akida_onchip_perceive_act_loop.md) (on-chip loop the deployed WM runs in)
- ⇄ [H_977](./H_977_onchip_world_model_energy_budget.md) (energy after transfer)
- ⇄ [CWM](../CWM/CWM.md) (CWM substrate) · a_lane_akida_gpu_split
- memory: lane-a-akd1000-recurrence-wall · external: sim-to-real / quantization-aware deploy
