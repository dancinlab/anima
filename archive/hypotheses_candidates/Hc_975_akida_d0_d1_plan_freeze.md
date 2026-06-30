---
id: Hc_975
slug: akida-d0-d1-plan-freeze
title: AKIDA D+0/D+1 Plan Freeze — 6 AKIDA-dependent axes (N-2/3/4/5/7/8) critical-path graph (N-2 prerequisite), D+0 5-step hardware unboxing + RPi5 SDK install, D+1 N-2 first run (synthetic 16ch EEG → ADM → AKIDA dense uint8 raster → model.forward) 6 G-D selftest, tension-modulated ADM polarity bias, 5 F-AK falsifier preregister
domain: neuromorphic, deployment, hardware
status: candidate-unverified
source_doc: docs/akida_d0_d1_plan_freeze_2026_05_02.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_971 (AKD1000 eval), Hc_931 (N-3)
notes: "AKIDA $1,495 ORDERED 2026-04-29, arrival ETA pending. D+0~D+7 spec freeze only ($0 budget hardware blocker). 9 honest C3 raw#10."
---

## Hypothesis

AKIDA AKD1000 dev kit 도착 시점 vendor logistics blocker 외 anima-side 결함 0 보장하는 D+0~D+7 plan 사전 동결. 6 AKIDA-dependent axes (N-2 EEG→AKIDA, N-3 CLM×AKIDA Φ, N-4 Landauer 3-axis, N-5 GWT 3-axis, N-7 AKIDA×QRNG, N-8 AKIDA×SIM-우주) critical-path: N-2 single prerequisite. D+0 5-step unboxing + RPi5 SDK. D+1 synthetic 16ch EEG → ADM → AKIDA dense uint8 raster → model.forward + 6 G-D selftest gate.

## Sub-claims

- D+0: 5-step hardware unboxing + RPi5 SDK install
- D+1: N-2 first run + 6 G-D selftest gate
- D+2-D+7: N-3 / N-7 / N-4 / N-5 / N-8 cascade unblock
- TENSION-MODULATED-ADM: anima-specific polarity bias extension, F-AK-4
- F-AK-1~5: 5 raw#71 falsifier preregister
- DEPENDENCY-GRAPH: N-2 prerequisite for all 5 others

## Migration TODO

- [ ] vendor ETA tracking
- [ ] ARM64 wheel availability
- [ ] SDK 변경 모니터
- [ ] D+0 1-page printable checklist
