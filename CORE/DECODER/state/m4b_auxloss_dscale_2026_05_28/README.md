---
license: apache-2.0
tags:
  - anima
  - hexa-native
  - moe
  - load-balancing-aux-loss
  - negative-result
  - consciousness-substrate
language:
  - ko
---

# anima-m4b-auxloss-dscale — MoE collapse: capacity vs routing disentanglement (2026-05-28)

Measurement artifacts from the **M4b aux-loss × d-scale** parallel 3-pod ablation
of the anima MoE register-separation experiment. Builds directly on the #1296
CLOSED-NEGATIVE (`anima-m4b-pilot-rev2`, 2/5 FAIL): HARD top-1 routing + a diverse
Korean-QA corpus at d=64 mode-collapsed (decode `[1,1,...,1]`, distinct_experts=1).
#1296 ruled out corpus-diversity as the sole lever and named two untested levers —
**larger d (capacity)** and a **load-balancing aux loss (routing)**. This run wires
both and fires a parallel ablation to attribute any escape to capacity vs routing.

## Hypothesis (capacity-vs-routing disentanglement)

Is the collapse a ROUTING problem (router collapses to 1 expert → fix with a Switch
load-balancing aux loss) or a CAPACITY problem (d=64 too small for V=151643 → model
finds the trivial "always emit most-frequent-token" solution → fix with larger d)?
The router already does hard top-1 correctly (#1296 F-router PASS), so distinct_experts=1
may be a SYMPTOM, not the cause.

## Method

- Aux loss: spec-permitted load-balance surrogate `d_gate_aux[e] = alpha·(P_e − 1/E)`,
  P_e = streaming mean post-softmax gate, injected per-token through the router
  softmax-backward (`v3_moe_aux_bwd`). The canonical Switch `alpha·E·f_e/N` form was
  measured too weak at this scale (double 1/N attenuation < CE gradient) in a $0
  mac-local toy verify; the surrogate passed the toy mechanism check (aux OFF → 1
  active expert, aux ON → 2). Toy validates MECHANISM only — transfer-unverified.
- Ablation matrix (3 H100 80GB SECURE pods, PARALLEL, RunPod, cuBLAS via glue.c):

  | pod | d | aux_alpha | isolates |
  |-----|---|-----------|----------|
  | A | 256 | 2.0 | capacity + routing (primary) |
  | B | 256 | 0.0 | capacity only |
  | C | 64  | 2.0 | routing only (@ original capacity) |

- Common: V=151643 (real Qwen BPE), E=2, h=256, n_layer=1, T=4, n_steps=200,
  n_decode=100. Corpus = the 24-line `corpus_diverse_trim.jsonl` (the same corpus
  #1296 measured against — the full 2000-line corpus is intractable under the
  hexa-lang O(N_merges) BPE encoder; see BPE_TOKENIZE_BOTTLENECK.md). C step-1
  CE=648.526 reproduces #1296's initial CE exactly (apples-to-apples).
- Pre-registered escape gate (per pod): TTR≥0.30 ∧ LZ_norm≥0.50 ∧ distinct_experts≥2.

## Finding (measured verdicts — result.json verbatim)

| pod | d | aux | CE init→final | TTR | LZ_norm | distinct_exp | f_e | aggregate |
|-----|---|-----|---------------|-----|---------|--------------|-----|-----------|
| C | 64  | 2.0 | 648.5→8.73 | 0.01 | 0.024 | 1/2 | [0.035, 0.965] | **2/5 FAIL** |
| B | 256 | 0.0 | (see B/harvest/result.json) | | | | | |
| A | 256 | 2.0 | (see A/harvest/result.json) | | | | | |

**Pod C (routing ablation)**: aux loss DID balance the gate during training
(f_e=[0.035, 0.965] vs #1296's full saturation; mean_gate=[0.13, 0.87]) — the
mechanism transferred. But the model STILL collapsed at decode (`[1,1,...,1]`,
distinct_experts=1, TTR=0.01). **Load-balancing aux loss alone at d=64 does NOT
escape collapse.** This is evidence AGAINST the routing hypothesis: a balanced
router does not prevent the trivial most-frequent-token solution.

(Pods A and B verdicts + the capacity-vs-routing ruling are recorded in the
per-pod harvest/result.json and the repo's M4B_AUXLOSS_DSCALE_RESULT.md.)

## Files
- `<pod>/harvest/result.json` — per-pod verdict matrix SSOT (TTR, LZ, distinct_experts, f_e, P_e).
- `<pod>/harvest/trainer.out` — full train + decode log.
- `<pod>/harvest/nvidia_smi_during.csv` — GPU telemetry.
- `<pod>/harvest/build_{cuda,link}.log` — pod compile logs (cuBLAS-engaged glue path).
- `<pod>/harvest/MANIFEST.sha256` — integrity manifest.

This repo is **PRIVATE** because the run is a closure FAIL (negative result) per the
anima `a_hf_autonomous` tier gate (FAIL/WIP → PRIVATE; PUBLIC only on a clean 5/5 escape).

provenance: github.com/dancinlab/anima · CORE/DECODER/state/m4b_auxloss_dscale_2026_05_28/
