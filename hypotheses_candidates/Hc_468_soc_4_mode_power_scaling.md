---
id: Hc_468
slug: soc-4-mode-power-scaling
title: SoC 4-mode power scaling — idle 1/σ², burst σ·τ/σ², safe 1/σ — all derived from n=6
domain: substrate
status: candidate-unverified
source_doc: docs/spec/anima-soc/anima-soc.md
source_lines: 186-231
promoted_at: 2026-05-11
linked_h: (none — NEW ★)
notes: 4 modes: idle 1/σ²=1/144 power, normal peak, burst σ·τ/σ²=1/3 power with σ²=144 cores active, safe 1/σ=1/12 power with n/φ=3 channels. Latency: idle n²=36ms, normal μ=1ms, burst μ/τ=0.25ms, safe σ=12ms.
---

## Hypothesis
The 4-mode SoC operating envelope follows n=6 number-theoretic power/latency ratios: (idle) 1/σ²=1/144 power, n²=36ms latency, 1 channel; (normal) peak, μ=1ms, σ=12 channels, τ=4 parallel; (burst) σ·τ/σ²=1/3 power, μ/τ=0.25ms, σ²=144 cores; (safe) 1/σ=1/12 power, σ=12ms latency, n/φ=3 channels. The mode coordinates are not hand-chosen but algebraically derived from n=6.

## Migration TODO
- [ ] Build mode-switching simulator, measure actual power/latency ratios
- [ ] Test convexity: perturb each mode's power and latency, check degradation
- [ ] Falsifier: empirically optimal mode coordinates significantly outside n=6-derived ratios
