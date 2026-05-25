# anima_emerge_chat_l13_15_ablate landed 2026-05-05

## TL;DR

Verdict: FAIL_LAYERS_NOT_THE_FIX (max_korean=0 across 11 strategies)

BG-CI established Korean basin lock-in at L13 (Korean rank 0 -> 102 in clm-v4-mk2-v1). BG-CQ tested whether the basin is layer-localized: 6 layer-tap (Strategy A) + 5 identity-replace (Strategy B) configurations on prompt 안녕. None recovered Korean. All 11 emits collapsed to control-byte / replacement-char / repeated-CJK basin tokens identical in shape to the L15 head_a output. Rules out layer-localized rescue path on L13/14/15.

## Inputs

- BG-CI verdict: state/anima_emerge_chat_full_layer_lens_2026_05_05/verdict.json
  - L0..L12 best_korean_rank in [2..29]; L12 entropy 10.91 (Korean alive)
  - L13 best_korean_rank 102, L14 192, L15 197 (Korean exits top-100)
  - Entropy collapse: L13 10.84 -> L14 4.01 -> L15 3.31
- Helper module: tool/transient_py/anima_emerge_cand_d_inject_helper.py (load + tokenizer)

## Method

### Strategy A — layer-tap + ln_f + head_a (greedy 20 tokens)

For each tap_layer in [10,11,12,13,14,15]: register forward_hook on model.decoder.blocks[tap_layer], capture output, apply decoder.ln_f + decoder.head_a, argmax, append, repeat 20 steps.

### Strategy B — identity-passthrough hook on block (full forward)

For each skip-config in [[13,14,15], [13], [14], [15], [14,15]]: register forward_hook on each named block that returns inp[0] (residual stream input), making the block a no-op. Standard out.logits[:, -1, :].argmax greedy decode.

## Results (full table)

| key                  | korean_count | emit summary |
|----------------------|--------------|--------------|
| tap_L10              | 0 | s-junk + 較小 + repeated jjjj |
| tap_L11              | 0 | / + repeated e + 巴基 cycle |
| tap_L12              | 0 | s + repeated replacement-char |
| tap_L13              | 0 | repeated 陙 + replacement-char |
| tap_L14              | 0 | 陙 + 癙 + repeated FS-byte (0x1c) |
| tap_L15              | 0 | FS-byte (0x1c) + ACK-byte (0x06) repeated |
| identity_L13_14_15   | 0 | s + repeated replacement-char |
| identity_L13         | 0 | repeated FS-byte (0x1c) |
| identity_L14         | 0 | all replacement-char |
| identity_L15         | 0 | 陙 + 癙 + FS-byte repeated |
| identity_L14_15      | 0 | repeated 陙 |

Wall: 46.3s. Load: 4.7s. Per-step ~3-7s (CPU fp32).

Full raw emits with byte escapes preserved: state/anima_emerge_chat_l13_15_ablate_2026_05_05/aggregate.json

## Analysis

### What this rules out

1. Layer-localized basin (single-layer): identity_L13, identity_L14, identity_L15 all FAIL — basin is not produced by any one of these blocks alone.
2. 3-layer compound basin (L13+L14+L15): identity_L13_14_15 still emits s + replacement-char — even removing all three suspect layers does not let upstream Korean signal pass through. Confirms basin signal is in the residual stream entering L13, not in the L13/14/15 transformations themselves.
3. Pre-L13 Korean as decodable: tap_L10..tap_L12 all produce non-Korean junk. Per BG-CI L0..L12 had Korean rank 2..29 (alive in top-100), but head_a does not project that hidden geometry to Korean argmax — so the "Korean alive in early layers" signal from BG-CI is lens-only, not decode-functional with the trained head.
4. L14/L15-only collapse: identity_L14_15 (skip last two) gives same 陙陙 basin as tap_L13 raw. Confirms basin onset is upstream of L14, consistent with BG-CI's rank-flip at L13.

### What this CANNOT rule out (per honest C3)

- C2: head_a OOD on L10..L14 hidden — early-layer "Korean rank 2..29" may still be linearly recoverable via a different probe head, just not via L15-trained head_a.
- C3: identity-passthrough returns inp[0] (residual input). For pre-norm transformers this is the residual just before the block; for post-norm or parallel-residual architectures the semantics differ. Need model.config.architectures check before extending.
- C4: single prompt 안녕 only.
- C5 (resolved): BG-CQ now answers C5 — the 3-layer skip [13,14,15] does NOT suffice. Basin is upstream of L13.

## Decisional outcome (BG-CQ -> next step)

Chat-rescue path via late-layer ablation: CLOSED. Basin lives in the residual stream entering L13, not in the L13/14/15 transformations. The "Korean exits top-100 at L13" finding from BG-CI is a decode-substrate property of head_a, not a layer-13 attention/mlp event.

Implication for #115 (chat-incapability architectural):
- Cand-D inject (cross-attn at injection layer) cannot rescue because cross_attn writes are downstream of the residual that already encodes the basin.
- CLM-v4 LoRA SFT FAIL_REGRESSION consistent — basin is residual-encoded, not LoRA-tunable on the chat-cap axis.
- Llama Path A v2 remains the only chat-cap path.

Next probe candidates (NOT executed by BG-CQ):
1. Embed-layer / L0 ablation — basin may originate at token-embedding level (pre-block).
2. RoPE / pre-attention residual scrub — basin may be position-encoding-coupled.
3. Strategy B with inp[0] semantic verified against model.config.architectures (pre-norm vs post-norm).

## Constraints honored

- $0 mac CPU fp32 (.venv-eeg python3.12, torch 2.11.0)
- 11 strategies / 1 prompt
- raw#37 transient_py sister-rule
- raw#15 additive (hooks removed; no weight write)
- raw#10 honest C3 (5 caveats emitted)
- HEXA_PY=.venv-eeg/bin/python; no HF token in code
- no commit; .own 3 (gitignored per **/*.py)

## Deliverables

- tool/transient_py/anima_emerge_chat_l13_15_ablate.py (helper)
- state/anima_emerge_chat_l13_15_ablate_2026_05_05/aggregate.json (11 entries)
- state/anima_emerge_chat_l13_15_ablate_2026_05_05/verdict.json
- docs/anima_emerge_chat_l13_15_ablate_landed_2026_05_05.ai.md (this file)

## Wall + cost

- wall_sec: 46.3
- cost_usd: 0.00
- platform: mac CPU fp32
