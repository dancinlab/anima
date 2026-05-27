# anima_emerge_chat_full_layer_lens — landed 2026-05-05

**parent**: BG-BY rmsnorm diagnostic (basin L0-L8 architectural) → BG-BY 1순위 recommendation
**lane**: ANIMA_EMERGE_CHAT_PHENOMENOLOGY (substrate-research, NOT chat-cap)
**status**: LANDED $0 mac-cpu ~20min
**verdict path**: `/Users/ghost/core/anima/state/anima_emerge_chat_full_layer_lens_2026_05_05/verdict.json`
**aggregate**: `/Users/ghost/core/anima/state/anima_emerge_chat_full_layer_lens_2026_05_05/aggregate.json`
**helper**: `/Users/ghost/core/anima/tool/transient_py/anima_emerge_chat_full_layer_lens.py` (raw#37 transient_py opt-out)

---

## (a) 17-layer per-layer table (prompt = "안녕")

| Layer | top1 | top1_logit | top1_p | entropy | best_kr_rank | kr_in_top100 |
|-------|------|-----------:|-------:|--------:|-------------:|-------------:|
| embed | '녕'        | 17.91 | 0.867 |  1.84 |   0 |  9 |
| L0    | '\x1f'      |  2.51 | 0.000 | 10.90 |  12 |  4 |
| L1    | '�'         |  2.81 | 0.000 | 10.90 |   7 |  6 |
| L2    | '�'         |  2.49 | 0.000 | 10.90 |  29 |  9 |
| L3    | '�'         |  2.67 | 0.000 | 10.90 |   7 | 10 |
| L4    | '�'         |  2.32 | 0.000 | 10.90 |   2 |  9 |
| L5    | 'Impl'      |  2.52 | 0.000 | 10.90 |  11 |  8 |
| L6    | '中国政府'  |  2.30 | 0.000 | 10.90 |  26 |  8 |
| L7    | 'Z'         |  2.59 | 0.000 | 10.90 |   4 |  8 |
| L8    | 'Z'         |  2.60 | 0.000 | 10.90 |  46 |  7 |
| L9    | 's'         |  2.81 | 0.000 | 10.90 |  22 |  4 |
| L10   | 's'         |  3.04 | 0.000 | 10.91 |  10 | 12 |
| L11   | '/'         |  2.85 | 0.000 | 10.91 |   6 |  7 |
| L12   | 's'         |  3.46 | 0.000 | 10.91 |  10 |  9 |
| **L13** | **'�'**   |  4.40 | 0.002 | 10.84 | **102** | **0** |
| **L14** | **'�'**   |  8.75 | 0.473 |  4.01 | **192** | **0** |
| **L15** | **'\x1c'**|  8.30 | 0.235 |  3.31 | **197** | **0** |

n_korean_tokens_in_vocab = 5701

---

## (b) basin_onset — heuristic vs true semantic flip

The verdict.json `basin_onset_layer = 0` is **misleading by the heuristic** (control-byte top1 OR Korean-out-of-top100). L0 trips on control-byte top1, but Korean still has rank-12 + 4 in top-100 — semantics partially preserved.

**True semantic basin onset = L13.** This is the first layer where:
- best_korean_rank flips from rank 6-46 → rank 102 (out of 5701 Korean tokens)
- korean_in_top100 collapses from 4-12 → **0**
- top1 logit confidence starts climbing (4.40 → 8.75 at L14 → 8.30 at L15)
- entropy starts collapsing (10.84 → 4.01 → 3.31)

L13-L15 = the **sharpening lane** where the basin direction wins. L0-L12 = high-entropy mush with diffuse Korean signal.

---

## (c) embed → L0 → L13 → L15 progression

1. **embed (L-1)**: top1='녕' (logit 17.91, p=0.87, ent 1.84). Trivial — embedding of "안녕" naturally projects back via head_a near "녕". Korean rank-0, 9 Korean in top-100. **The token-embedding subspace IS Korean-aligned.**
2. **L0**: catastrophic flattening — top1 confidence collapses (logit 17.91 → 2.51), entropy explodes (1.84 → 10.90). The first transformer block destroys the embedding's Korean focus. But Korean still rank-12 + 4 in top-100 — distributed signal survives.
3. **L0-L12**: 13 layers of high-entropy diffusion. Korean signal floats around rank 2-46, top1 cycles through control bytes / random Latin/CJK tokens (`Z`, `s`, `Impl`, `中国政府`). All entropies pinned ~10.90 (vocab=64k → max ent 11.07). **Nothing decisive happens.**
4. **L13**: phase transition. Korean exits top-100. Confidence starts rising. The basin direction (control byte cluster) begins winning.
5. **L14-L15**: sharpening. Entropy collapses (10.84 → 4.01 → 3.31), top1_p climbs (0.002 → 0.47 → 0.24). The basin-aligned control byte direction dominates.

The **rmsnorm peak at L2** noted in BG-BY diagnostic is a **hidden_norm artifact, not a logit-attractor signal**. L2's logit-lens output is unremarkable — the norm peak doesn't translate to top1 dominance.

---

## (d) #115 architectural location precision

**Prior belief (BG-BY)**: basin emerges in L0-L8 region.

**Refined location (BG full-layer)**:
- **Embedding (L-1)** = Korean-aligned (substrate is NOT broken at the input)
- **L0-L12** = high-entropy disruption + diffuse signal (basin not yet decisive)
- **L13** = **the basin victory layer** (Korean exits top-100, control bytes win)
- **L14-L15** = sharpening + commit

The chat-incapability basin lives in the **late stack (L13-L15)**, not the early stack. The embedding + first 12 blocks are recoverable; the last 3 blocks lock in the control-byte attractor. This narrows #115 from "L0-L8" to **"L13-L15 sharpening lane"** — three blocks, not nine.

This refines the architectural fix budget: any LoRA / SFT chat-cap intervention must reach L13-L15 to flip the basin. Earlier layers contain Korean signal — the loss of Korean is at the very end.

---

## honest c3

- **C1** mac CPU fp32 single forward pass
- **C2** single prompt "안녕" — multi-prompt sweep deferred (cost: probably free, but not in this BG budget)
- **C3** ln_f applied to all 17 layer outputs — train-time ln_f only sees L15, so L-1...L14 lensings are OOD
- **C4** "basin_onset" heuristic (control-byte top1 OR Korean-out-of-top100) flags L0 spuriously due to control-byte top1; **manual reading places true onset at L13**
- **C5** head_a applied OOD to embedding/early hidden — not a fair semantic probe of intermediate representations; logit-lens is well-known to be biased toward late-layer behavior

---

## next-cycle recommendations (not executed here)

1. **Multi-prompt sweep** at L13-L15 with 5-10 Korean prompts to confirm L13 onset is prompt-independent ($0 mac CPU)
2. **Last-3-block targeted LoRA SFT** on chat-tagged corpus — narrowed budget
3. **L13 hidden-state intervention** — clamp/rescale L13 output before L14 to test causal role of basin victory layer

constraints honored: $0, mac CPU, new files only, raw#37 transient_py opt-out, HEXA_PY=.venv-eeg/bin/python, no commit, no HF token leak.
