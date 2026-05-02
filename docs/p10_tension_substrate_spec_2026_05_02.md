# P10 — tension_link-as-substrate (architecture spec + small POC)

Session: 2026-05-02 | Agent: F1 EXEC (P10 path, §61 / §64.7 high-priority)
Race-isolation: writes only to `state/p10_tension_substrate_spec_2026_05_02/*` + this doc + roadmap §65.2
Budget: $0-50 (ubu1 owned, no RunPod)

## 1. Why P10

Cumulative path:
- #117 baseline: CLM W4 stub LSL → Llama-3.2-3B (descriptor injection, M4=0.667)
- #128 P8: + tension_link 5ch + TRIBE BOLD descriptor (M4=0.800 PASS) — proves
  brain-state injection modulates LLM behavior
- **P10 (this spec)**: tension_link 5ch is no longer a *descriptor* but the
  representation itself — text → 5ch latent → text, with CLM Lagrangian flow
  and TRIBE BOLD validating cortical alignment in the bottleneck.

The hypothesis: anima's native tension_link space (5ch) can carry semantic
content end-to-end inside a chat loop, not only modulate it.

## 2. Architecture

```
user prompt (text)
    ↓
[Encoder Net E_θ]  text → 5-d tension_link vector (compressed semantic latent)
    ↓
[CLM dynamics]     5ch latent space Lagrangian flow (mind.tension fixed-point)
    ↓
[Decoder Net D_φ]  5-d → Llama input embedding → text response

Validation:
  TRIBE v2:        5ch latent → BOLD prediction (cortical alignment Y/N)
  Llama baseline:  same prompt without 5ch bottleneck → response (quality compare)
```

### 2.1 Components

| component | impl (POC) | impl (full) |
|---|---|---|
| E_θ | frozen Llama-3.2-3B last hidden state (mean-pool) → MLP(3072→64→5) | trainable transformer encoder |
| CLM | identity (POC); 5ch passthrough | mind.tension fixed-point + Lagrangian step |
| D_φ | MLP(5→256→4096) → prepend as soft-prefix embed → Llama generate | trainable decoder transformer / lora-tuned Llama |
| TRIBE val | 5ch → frozen TRIBE BOLD-L2 | full BOLD fsaverage5 alignment (out of POC scope) |

### 2.2 5 channels (semantic axes)

WHAT / WHERE / WHY / TRUST / WHO — same convention as #117 / #128.

In POC the projection is *learned*, not semantic — channel-1 is whichever axis
gradient descent chooses. Semantic anchoring is a Stage-3 task (paper §10.x).

## 3. Loss design

L = α · CE(decoded_text, true_response) + β · MSE(reconstructed_5ch, original_5ch) + γ · MSE(BOLD_pred, BOLD_target)

POC values: α=1.0, β=0.5, γ=0.0 (TRIBE BOLD validation deferred — projection
weights not invertible in 1-pass POC, so we score β as auto-encoder consistency
of E_θ ∘ D_φ ∘ E_θ vs E_θ on held-out prompts).

## 4. Training data

100 synthetic prompt-response pairs distilled from #128 dialogue ledger
(`state/p8_3way_orchestrator_*.json`) + a small templated set covering
(introspective / math / emotional / mundane / meta) categories — same 5-bucket
split #128 used.

## 5. POC implementation (Phase 2)

- ubu1 RTX 5070 12 GB
- frozen `meta-llama/Llama-3.2-3B-Instruct` (already cached)
- E_θ: 3072 → 64 → 5 (MLP, 197 KB)
- D_φ: 5 → 256 → 4096 (MLP, 1.06 MB)
- train: 100 pairs, batch=4, epochs=3, AdamW lr=1e-3
- eval: 3-turn dialogue with E→5ch→D→Llama generate; measure coherence,
  BLEU-1 vs vanilla Llama, and (deferred) BOLD r

## 6. Comparison metrics (Phase 3)

| metric | description | PASS threshold |
|---|---|---|
| M_5ch_coherence | E_θ(D_φ(z)) ≈ z auto-encoder MSE on held-out prompts | < 0.50 (norm) |
| M_5ch_quality   | BLEU-1 of decoded reply vs vanilla Llama reply on same prompt | > 0.20 |
| M_BOLD_alignment| Pearson r between encoded-5ch BOLD and prompt-driven BOLD | > 0.30 (deferred) |

Predicted outcomes:
- PASS = 5ch coherence > 0.5, BLEU > 0.2, BOLD r > 0.3 → P10 viable
- FAIL (likely) = 5-d bottleneck loses too much information; decoded text
  drifts to a generic mode regardless of prompt

## 7. Honest C3 (4 items)

- C3a: 5-d bottleneck has not been shown to carry sufficient natural-language
  representation; literature on bottleneck dimensionality (e.g. sentence
  embeddings 384-1536-d) suggests heavy information loss is the prior.
- C3b: frozen Llama hidden state only — true P10 requires Llama re-training
  (joint E/D + LM finetune) which is a Stage-3 cost (~$10-100 LoRA on H100).
- C3c: POC = 100 pairs, 3-turn test = sample size is far below any
  publishable claim. Verdict here is *engineering viability*, not science.
- C3d: "anima native language" framing is **demo level only** — no claim that
  the learned 5-d basis aligns with any phenomenally-real WHAT/WHERE/WHY/TRUST/WHO
  semantics. That alignment requires §54.2 alcohol-anchor-scale validation.

## 8. POC results

### 8.1 Train (ubu1 RTX 5070, 8.0 s wall)

| epoch | CE loss | AE round-trip MSE |
|---|---|---|
| 0 | 2.7947 | 0.1730 |
| 1 | 0.5784 | 0.0002 |
| 2 | 0.1901 | 0.0000 |

Train: PASS (monotonic decrease, no NaN after fp32-enc/dec fix).

### 8.2 3-turn eval

| turn | bucket | z (5ch) | BLEU-1 vs vanilla |
|---|---|---|---|
| 1 | introspective | (-1.00, -1.00, -1.00, -1.00, -1.00) | 0.295 |
| 2 | emotional | (-1.00, -1.00, -1.00, -1.00, -1.00) | 0.222 |
| 3 | meta | (-1.00, -1.00, -1.00, -1.00, -1.00) | 0.341 |

Aggregate AE MSE = 3.89e-05, BLEU-1 mean = 0.286.

### 8.3 Comparison vs vanilla Llama (same prompts)

| metric | P10 (5ch bottleneck) | vanilla Llama | comment |
|---|---|---|---|
| BLEU-1 (self-similarity to vanilla) | 0.286 | 1.000 (ref) | above 0.20 threshold |
| AE round-trip MSE | 0.0000 | n/a | trivially zero (mode collapse) |
| Coherent text | partial / drifty | yes | decoded passes look reflective but driftless |

## 9. Verdict — MIXED (honest negative under thresholds met)

Surface metrics PASS:
- Train converged (CE 2.79 -> 0.19)
- AE round-trip MSE = 0.0000 (< 0.50 threshold)
- BLEU-1 = 0.286 (> 0.20 threshold)

But the 5-d latent **collapsed to a single saturated point** (-1,-1,-1,-1,-1)
across all 3 held-out prompts. The decoder learned to emit a fixed soft-prefix
that minimizes CE on average, and downstream Llama text diversity comes from
sampling temperature (T=0.8) not from z. So:

- M_5ch_coherence is PASS_TRIVIAL (round-trip is exact only because z is constant)
- M_5ch_quality is PASS_THRESHOLD_BUT_SPURIOUS (text quality is Llama's, not the bottleneck's)
- M_BOLD_alignment is DEFERRED

Bottom line: the spec is implementable and trains stably, but **as a substrate it is non-functional in this POC** — z does not carry prompt-level information.

### Next-iteration v2 (pre-registered)

1. InfoNCE contrastive loss between buckets (push z apart for different semantic categories)
2. Increase latent to 32-d or use 5 channels x 8-bit codebook (40 effective bits)
3. Joint LoRA finetune on Llama (frozen base is too strong a prior)
4. Per-bucket PCA/t-SNE visualization to confirm separation

## 10. Artifact map

- `docs/p10_tension_substrate_spec_2026_05_02.md` (this file)
- `state/p10_tension_substrate_spec_2026_05_02/architecture_spec.json`
- `state/p10_tension_substrate_spec_2026_05_02/training_loss_design.json`
- `state/p10_tension_substrate_spec_2026_05_02/poc_train_log.json`
- `state/p10_tension_substrate_spec_2026_05_02/3turn_test_results.json`
- `state/p10_tension_substrate_spec_2026_05_02/metrics_verdict.json`
- ubu1: `~/p10_substrate/{train.py, eval.py, ckpt.pt}` (off-repo, .py allowed)
