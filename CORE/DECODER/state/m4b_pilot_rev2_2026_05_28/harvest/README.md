---
license: apache-2.0
tags:
  - anima
  - hexa-native
  - moe
  - negative-result
  - consciousness-substrate
language:
  - ko
---

# anima-m4b-pilot-rev2 — MoE register-collapse measurement (NEGATIVE RESULT · 2026-05-28)

Measurement artifacts from the **M4b-fire-rev2** pilot of the anima MoE
register-separation experiment (UNIVERSE H_490 differentiation arc). This repo is
PRIVATE because the run is a **closure FAIL (2/5)** — a negative result, per the
anima `a_hf_autonomous` tier gate (FAIL/WIP → PRIVATE).

## Hypothesis (pre-registered falsifiers)

A hexa-native MoE decoder with **HARD top-1 routing** + a **diverse** Korean-QA
corpus should escape the register/mode collapse that the templated v1 corpus
induced (D3 #1269 root-cause: 240 near-identical templated lines → trivial token
repetition the router cannot escape).

5 falsifiers (F-M4B-FIRE):
- **1'** TTR ≥ 0.30 (decode token diversity)
- **LZ** LZ76 normalized complexity ≥ 0.50 (collapse-escape proxy)
- **3** distinct_experts ≥ 2 (router differentiates)
- **4** CE monotone decrease (training converges)
- **router** HARD top-1 wired (architecture check)

## Method

- Model: hexa-native MoE decoder, d=64, V=151643 (real Qwen BPE), E=2 experts,
  h=256, n_layer=1, T=4, n_steps=200, n_decode=100. ~29.16M params (FP64, 222 MB).
- Tokenizer: Qwen byte-level BPE (151,387 merges / 151,643 vocab).
- Corpus: diverse Korean instruction-tuning QA (varied topics, NOT templated).
- Hardware: 1× NVIDIA H100 80GB HBM3 (RunPod SECURE), cuBLAS-engaged
  (glue.c strong `hexa_cuda_available` override + `-lcuda`). Wall 1114s.
- Build path: Mac `hexa build --c-only` → trainer.c → scp → pod-side
  `nvcc + clang -DHEXA_CUDA` (Ubuntu 22.04 GLIBC 2.35; pod-side `hexa run`
  blocked by GLIBC ≥2.38 requirement).

## Finding (measured verdict — result.json verbatim)

| falsifier | value | threshold | verdict |
|-----------|-------|-----------|---------|
| F-M4B-FIRE-1' TTR | **0.01** (1/100 unique) | ≥0.30 | **FAIL** |
| F-M4B-FIRE-LZ LZ_norm | **0.0240306** | ≥0.50 | **FAIL** |
| F-M4B-FIRE-3 distinct_experts | **1/2** | ≥2 | **FAIL** |
| F-M4B-FIRE-4 CE monotone | 648.526 → **9.02146** | decrease | **PASS** |
| F-M4B-FIRE-router HARD-top1 | wired | — | **PASS** |
| **AGGREGATE** | | | **2/5 PASS · FAIL** |

**Result**: training converged (CE 648.5 → 9.0, 72× reduction) but the model
**mode-collapsed to a single token** (decode = `[1,1,1,...,1]`, all from
**expert 1** only). Corpus diversity + HARD top-1 routing did **NOT** escape
register collapse at this pilot scale (d=64). This **rules out corpus-diversity
as the sole lever** — matching the prior Phase 5b 2/5 outcome and the toy-MoE
finding that naive routing dense-collapses. The escape mechanism (register ⊥
coherent expert separation) requires more than corpus diversity at d=64: likely
larger d, capacity-balanced routing (load-balancing aux loss), or longer training.

## Files
- `result.json` — verdict matrix SSOT (decoded_ids, decoded_experts, CE, TTR, LZ).
- `trainer.out` — full train + decode log.
- `corpus_diverse_trim.jsonl` — the 24-line diverse Korean-QA corpus used.
- `build_link.log` / `build_cuda.log` — pod compile logs (cuBLAS-engaged glue path).
- `nvidia_smi_during.csv` — GPU telemetry.
- `MANIFEST.sha256` — integrity manifest.

provenance: github.com/dancinlab/anima · CORE/DECODER/state/m4b_pilot_rev2_2026_05_28/
