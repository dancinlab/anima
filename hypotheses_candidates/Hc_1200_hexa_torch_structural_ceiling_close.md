---
id: Hc_1200
slug: hexa-torch-structural-ceiling-close
title: hexa-torch (RFC 043) structurally closes the pure-hexa interpreter LM-scale-training ceiling that .py interim work-arounds revealed
domain: substrate / hexa-lang
status: candidate
proposed_at: 2026-05-16
source: derived from RFC 040 Phase D / E / E2 verdicts + .py d=768·12L verdict (2026-05-16) appended to PHILOSOPHY.tape
linked_rfc: hexa-lang inbox `rfc043-hexa-torch` (subsumes RFC 042); RFC 041 (B2 real CUDA kernels) as backend
linked_anchor: archive/PHILOSOPHY.tape §RFC040-PHASE-D-CUBLAS-VERIFY-2026-05-16 + §RFC040-PHASE-E2-GRAD-EXACT-BWD-2026-05-16 + §PY-D768x12L-INTERIM-SUBSTRATE-CONVERGE-2026-05-16
---

## Hypothesis

The pure-hexa interpreter cannot reach LM-scale training-convergence on its own
(Phase E2 named, real-limit substrate ceiling: GRAD-EXACT > 5 min at d ≥ 512;
no FINAL gn2 captured at d=768·12L). The structural answer is **hexa-torch**
(RFC 043, filed upstream) — a compiler-only NN training stdlib that combines
RFC 041 (real CUDA kernel backend) + RFC 040 (tensor backend) + RFC 034
(autograd) under an AOT whole-program fusion path. RFC 042 (AOT-native trainer
control-flow) is **subsumed** by RFC 043; fat native stdlib + thin hexa
orchestration is the structural close of the interpreter ceiling.

## Falsifier sketch (pre-registered, $0 design — fire deferred)

- **F-HEXA-TORCH-1 CPU-EQUIV-RETAINED**: hexa-torch trainer on small (d=32·3L,
  80-step, seed=42) must reproduce the Phase E2 CPU bit-equal init→final
  signature (`gn2 7.97116 → 3.73374e-07`, GRAD-EXACT identical Σ order). No
  fp-noise carve-out for the CPU path. (g3 anchor: hexa CPU farr arithmetic
  is the verified reference.)
- **F-HEXA-TORCH-2 GPU-BIT-EQUAL-CARRY**: at the scales the pure interpreter
  already cleared on cuBLAS (Phase E d=384·6L, Phase E2 GRAD-EXACT d=384·6L
  PASS), hexa-torch must hold max\|Δ\| ≤ 1e-9 vs CPU on cuBLAS Dgemm forward
  AND backward. (real-limit: cuBLAS roofline, NOT lattice — g3.)
- **F-HEXA-TORCH-3 LM-SCALE-CONVERGE**: at d=768·12L on the same byte corpus
  the .py interim run used, hexa-torch must capture a FINAL CE strictly
  below the random-init byte-floor (≈ ln 256 = 5.545) within a wall budget
  comparable to the .py reference (≈ 6 min on A100 for 2500 steps). This is
  the deliverable the pure interpreter could NOT reach.
- **F-HEXA-TORCH-4 SAFETENSORS-ROUND-TRIP**: hexa-torch ckpt → R2
  safetensors loader (HEXAD/D F-R2-SAFETENSORS) byte-equal + L2-norm
  invariant (existing 🔵 anchor).
- **F-HEXA-TORCH-5 NO-OVER-CLAIM**: hexa-torch performance MUST NOT be
  asserted as "beats PyTorch" — cuBLAS = match-not-beat is the GEMM
  roofline. n=6 lattice perf assertions = hard fail (f1/f2). Stage
  qualitatively (near / mid / ultimate); never fabricate speed multiples.

## Evidence anchors already in the ledger (do not re-derive)

- Phase D cuBLAS verify — 51.24 TFLOPS FP64 H100 (76 % peak), 13526 GF/s A100,
  4× independent (H100×2 + A100×2), max\|Δ\| = 4.44e-15 < 1e-9.
- Phase E2 GRAD-EXACT BACKWARD — 8 boxed call sites routed through the same
  proven cuBLAS Dgemm via exact GEMM reshapes (no fake B2 `*_gpu` -1 stubs,
  honest g3). CPU bit-equal carry; real A100 GRAD-EXACT PASS at d=384·6L.
- .py d=768·12L — `init CE 5.590832 → final 0.000708`, 2500 step, 336.85 s
  on A100. ConsciousDecoderV2 283.72 M params. NOT hexa-native; the anchor
  is architectural identity + the hexa CPU-equiv bit-equality proof of the
  hexa-native trainer of that same architecture.

## Honest C3 (pre-registered for the candidate)

1. RFC 043 is **filed**, not implemented — this candidate is a *roadmap
   hypothesis*, not a verdict-bearing claim. Promotion to `hypotheses/`
   gated on hexa-lang inbox progress.
2. The .py d=768·12L FINAL CE 0.000708 over a 152 KB byte corpus is plausibly
   memorization (corpus tiny vs param count 283 M). LM quality is NOT
   claimed — descent itself is the verdict. F-HEXA-TORCH-3 inherits this
   caveat; quality measurement is a separate falsifier (deferred).
3. cuBLAS = match, not beat. Any hexa-torch "performance" framing must obey
   f1/f2 (no lattice-fit perf claim) and g3 (real-limit roofline is the
   ceiling, not the proof).
4. The interpreter ceiling Phase E2 named is real-limit honest (CPU farr
   control-flow + watchdog wall); it is NOT an indictment of hexa-lang per
   se — it is the named architectural reason hexa-torch is filed.

## Pipeline status

candidate (this file) → hypotheses/ promotion gated on (a) hexa-lang
`rfc043-hexa-torch` upstream review + (b) at least F-HEXA-TORCH-1 design
freeze. NO PHILOSOPHY.tape verdict entry until F-HEXA-TORCH-1..5 measurement
fires under the standard pipeline.
