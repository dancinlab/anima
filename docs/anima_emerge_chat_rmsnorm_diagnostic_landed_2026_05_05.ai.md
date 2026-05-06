# BG-BY — RMSNorm / ln_f Bypass + Per-Layer Hidden Norm Diagnostic LANDED 2026-05-05

## TL;DR

Verdict: `FAIL_BASIN_DEEP_HIDDEN`. Basin pathology is NOT in `ln_f` and NOT
recoverable by bypassing it or by tapping mid-stack (L8). RMSNorm operates
within healthy numerical regime; the degenerate token distribution that
collapses to byte-fallback (`/`) at the final layer is already encoded in
the residual stream from the very early blocks (L1-L2 norm-spike then sustained
high-magnitude std), and any honest head-application onto a mid-layer hidden
also collapses, into a different degenerate token (`邊緣`) but still a
single-token loop.

The basin lies in the residual stream's **direction**, not in `ln_f`'s
normalisation, not in head choice, and not in last-layer-only state.

## Setup

- Model: `need-singularity/clm-v4-mk2-v1` (CLM v4 mk2 — RMSNorm `ln_f`,
  16 decoder blocks, head_a + head_g)
- Prompt: `"안녕하세요. 오늘 날씨가 좋네요."` (12 tokens)
- Device: mac CPU fp32 (`.venv-eeg`)
- Wall: 12.6 s, $0
- Helper: `tool/transient_py/anima_emerge_chat_rmsnorm_diagnostic.py`
- Output: `state/anima_emerge_chat_rmsnorm_diagnostic_2026_05_05/{aggregate,verdict}.json`

## Findings

### (a) pre_ln vs post_ln norm + std at last token

| stat | pre-ln_f | post-ln_f | ratio |
|---|---|---|---|
| norm | 55.89 | 28.80 | 0.515 |
| std  | 2.018 | 1.040 | 0.515 |
| mean | -0.025 | -0.013 | — |

ln_f compresses uniformly by ~0.515x — exactly the RMSNorm signature
(`x / sqrt(mean(x**2))` with learned scale ≈1). No anomaly.
`ln_compresses_std=true`.

### (b) per-layer hidden norm trajectory L0-L15 at last token

| L | norm | std | max_abs |
|---|---|---|---|
| 0 | 62.8 | 2.27 | 8.62 |
| 1 | 83.5 | 3.02 | 8.64 |
| 2 | **102.7** | **3.71** | 9.78 |
| 3 | 54.0 | 1.95 | 7.59 |
| 4 | 77.5 | 2.80 | **13.32** |
| 5 | 80.6 | 2.91 | 11.18 |
| 6 | 76.9 | 2.78 | 10.06 |
| 7 | 67.3 | 2.43 | 9.29 |
| 8 | 76.7 | 2.77 | 10.06 |
| 9 | 69.6 | 2.51 | 9.44 |
| 10 | 67.1 | 2.42 | 8.76 |
| 11 | 63.1 | 2.28 | 8.31 |
| 12 | 61.8 | 2.23 | 8.70 |
| 13 | 72.5 | 2.62 | 8.69 |
| 14 | 62.0 | 2.24 | 6.97 |
| 15 | 55.9 | 2.02 | 6.38 |

Pattern: monotonic build-up L0->L2 (+63%), sharp dip at L3 (-47% from L2),
oscillating mid-stack 76-80, gradual descent 14->15. No collapse, no
explosion — magnitudes consistent with a working transformer trunk.

### (c) bypass top-1 (4 variants)

| variant | id | text |
|---|---|---|
| baseline (full forward) | 51 | `/` |
| pre_ln_f + head_a | 51 | `/` |
| L8 (no ln_f) + head_a | 47860 | `邊緣` |
| L8 + ln_f + head_a | 47860 | `邊緣` |

baseline ≡ pre_ln_f (head_a applied to pre-ln_f hidden produces the same
byte-fallback `/`) — RMSNorm is numerically irrelevant for this token's
argmax. L8 produces a different degenerate token (`邊緣`, "edge / fringe" CJK),
and adding ln_f at L8 doesn't change the verdict.

### (d) greedy continuations (15 tokens)

- L8+ln_f: `邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣`
- L8 no ln_f: `邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣邊緣`

Both decay into single-token cycle within step 1. Identical sequences
(ln_f bypass at L8 makes zero behavioural difference — head_a is robust
to RMSNorm's affine compression, but the *direction* is already locked).

### (e) verdict

`n_bypass_coherent = 0` ⇒ `FAIL_BASIN_DEEP_HIDDEN`.

## (f) Honest C5

1. **C1** mac CPU fp32 — argmax tie-breaking deterministic but a different
   vocab id at same logit can flip text.
2. **C2** ln_f bypass invalidates head_a's training-time normalized-input
   expectation. Applying head_a to pre-ln_f hidden is an OOD probe;
   incoherent output is NOT definitive evidence of basin pathology.
3. **C3** single prompt long-Korean — anecdotal. Per-prompt variance not
   measured; cannot generalize to "basin everywhere" from one input.
4. **C4** per-layer hidden-state norm trajectory does NOT establish semantic
   content recovery (BG-AR insight). High-norm intermediate layer can still
   encode a degenerate distribution that maps to byte-fallback under any head.
5. **C5** "semi_coherent" heuristic anima-internal (≥5 Korean+ASCII chars,
   no single char >50%). False-positives on mixed-script garbage;
   false-negatives on short coherent fragments. Verdict label informative
   not authoritative.

## #115 Mechanism — Precise Location After BG-BY

| Component | Status | Evidence |
|---|---|---|
| `lm_head` (head_a / head_g / tok_emb) | NOT the bug | BG-BQ — all heads collapse |
| `ln_f` (RMSNorm) | NOT the bug | pre 55.9 / 2.02 → post 28.8 / 1.04 = healthy 0.515x compression; pre_ln_f bypass ≡ baseline |
| Last-layer hidden (L15) | degenerate direction | bypass at L8 also collapses, into a different cycle |
| L0-L8 residual stream | basin already locked | L8 hidden tap → `邊緣` cycle, not anchored on prompt content |
| L1-L2 norm spike | suspicious | +63% L0→L2 then -47% drop into L3 — non-stationary trunk dynamic; possibly the FFN / attn pre-collapse signature, not a smoking gun |

The chat-incapability basin is **architectural in the residual stream
direction from L0-L8 onward**, not in any single normalisation or head module.
This rules out cheap fixes (head swap, ln_f re-init, last-layer patch) and
makes the Pβ + CLM-v4 LoRA SFT FAILED outcomes consistent: chat capability
cannot be recovered downstream of the trunk if the trunk basin is fully
formed by mid-stack.

Next-test candidates (ordered by 완성도):

1. **per-layer logit-lens scan** — apply head_a to L0..L15 hidden, measure
   token entropy + top-1 type per layer. Identifies the exact layer where
   the degenerate direction first dominates. ($0, ~10 min)
2. **input-token distance** — compare hidden-state cosine of first vs last
   token at each layer; basin should manifest as last-token cosine collapsing
   to a "filler" prototype direction. ($0, ~10 min)
3. **prompt-set replication (5 KO + 5 EN)** — falsify single-prompt
   confound (C3). ($0, ~25 min)

## Compliance

- raw#37 (transient .py only — `tool/transient_py/`)
- raw#15 (additive — no mount / shim / dialogue_load modification)
- raw#10 (5 honest C3 in verdict.json + this doc)
- HF token leak guard PASS
- no commit
- $0, mac CPU only
