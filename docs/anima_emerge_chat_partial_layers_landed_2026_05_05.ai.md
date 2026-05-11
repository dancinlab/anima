<!-- @no-lineage-citation-exempt-file — this doc records lint-marker tokens (raw#NN policy IDs) as content references; not version-bound lineage. -->

# anima emerge chat — partial layers (BG-CS) landed 2026-05-05

## Scope

BG-CS extends BG-CJ (`embed_decode`) and BG-CI (`full_layer_lens`) by
running greedy decode while replacing decoder `blocks[N+1..15]` with
identity (pass-through) hooks. Goal: localize where the Korean basin
collapses across the 16-block stack on `dancinlab/clm-v4-mk2-v1`.

## Inputs

- `state/anima_emerge_chat_embed_decode_2026_05_05/verdict.json` — BG-CJ
  found embed-only decode emits Korean-aligned tokens; full-forward
  emits no Korean. Conclusion: blocks "destroy semantic".
- `state/anima_emerge_chat_full_layer_lens_2026_05_05/verdict.json` —
  BG-CI logit-lens per layer; `basin_onset_layer = 0`,
  `best_korean_rank` mostly 4-46 across L0-L12, then 102/192/197 at
  L13/L14/L15 (Korean exits top-100 at L13).

## Helper

`tool/transient_py/anima_emerge_chat_partial_layers.py` (new, .own 3
transient sister-rule helper). Uses `inj_helper._try_load_model` and
`_load_tokenizer` for plumbing. Identity hook on a `DecoderBlockV2`
returns `(input_x, zeros_like(tension), None, 0.0)` to satisfy the
4-tuple unpacking in `ConsciousDecoderV3.forward` (line 169).

## Sweep

Single prompt `'안녕'`, greedy decode 20 next tokens, configs:

| `last_active_layer` | emit (first 20 chars)                               | korean_count | ascii_alpha |
| ------------------- | --------------------------------------------------- | -----------: | ----------: |
| `all_16_active`     | `'\x1c\x06\x06...\x06'` (×20)                       |            0 |           0 |
| `-1` (no blocks)    | `'녕녕녕녕녕녕녕녕녕녕녕녕녕녕녕녕녕녕녕녕'`         |       **20** |           0 |
| `0`                 | `'\x1f戦線���...'`                                  |            0 |           0 |
| `1`                 | `'�}}}}}}}}}}}}}}}}}}}'`                             |            0 |           0 |
| `2`                 | `'�}}}}}}}}}}}}}}}}}}}'`                             |            0 |           0 |
| `5`                 | `'ImplImpl中国政府可能であるImplωωωωωωωωωωωωωωω'`      |            0 |          12 |
| `8`                 | `'Z\x1c.44444444444444444'`                         |            0 |           1 |
| `10`                | `'s-�e較小~ijjjjjjjjjjjjj'`                           |            0 |          16 |
| `12`                | `'s�������������������'`                             |            0 |           1 |
| `13`                | `'�陙陙陙陙陙陙�'`                                   |            0 |           0 |
| `14`                | `'�陙��癙��\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c'`   |            0 |           0 |

## Verdict

```
schema:                    anima/emerge_chat_partial_layers/verdict/1
n_configs:                 11
max_korean_count:          20  (all from last=-1 single-token loop on '녕')
n_korean_emerging:         1   (only last=-1)
korean_disappear_layer:    0   (one block is enough)
korean_first_appear_layer: -1
verdict:                   PASS_PARTIAL_RESCUES (literal — max_korean > 5)
                           BUT degenerate: '녕'×20 is a stuck argmax loop.
```

## Findings

1. **Destruction onset at L0** — passing the embedded `'안녕'` through
   even one block (`last=0`) drops Korean count to 0 and produces
   control-byte/CJK-mixed garbage. This refines BG-CI's
   `basin_onset_layer=0` (Korean exits top-1 at L0) into the stronger
   *generative* claim that Korean cannot survive a single block in
   greedy decode mode.

2. **BG-CJ confirmed and tightened** — the 16-block destruction is
   already complete after block 0. Subsequent blocks (1-15) move the
   hidden state through other regions (CJK, ASCII, control bytes) but
   never re-enter the Korean basin in this prompt.

3. **`last=-1` rescue is degenerate** — bypassing all blocks plus the
   final ln_f scaling collapses argmax to a single Korean token (`'녕'`,
   the second piece of `'안녕'`) repeated 20×. This is BG-CJ-style
   "embed→head_a leakage", not a rescue. C2/C3/C4 carry: ln_f + head_a
   are train-time-only at L15 hidden distribution; applying them to
   raw embeddings is OOD by construction.

4. **L13 lens-vs-decode mismatch resolved** — BG-CI lens showed Korean
   surviving in top-100 through L12, then exiting at L13. The lens
   measures rank ordering; greedy decode requires top-1. Korean
   top-1 is already lost at L0 even though Korean tokens linger in
   top-100 through L12. BG-CI L13 onset = "Korean leaves the candidate
   set entirely"; BG-CS L0 onset = "Korean leaves the argmax". Both
   are consistent.

5. **`all_16_active` baseline confirms #115 architectural** — full
   forward emits `'\x1c\x06\x06...'` (control bytes, kr=0, ascii=0)
   on `'안녕'`. Consistent with the chat-capability FAIL on this
   substrate. PASS_PARTIAL_RESCUES is a label-level positive only;
   architectural chat path remains closed on CLM v4 best.pt.

## Honest C3

C1 — mac CPU fp32 deterministic; minor numeric drift vs GPU bf16.

C2 — identity hook bypasses block.attention + block.cross_attn +
block.ffn but RoPE is applied INSIDE self-attention. The bypassed
suffix sees pre-RoPE hidden states; ln_f + head_a depend on the
post-RoPE basin. Reading partial-stack hidden through the head is
OOD vs train-time distribution.

C3 — head_a + ln_f train-time-only at L15 hidden. Coherence at
intermediate layers would be remarkable; lack of coherence is
expected.

C4 — single prompt `'안녕'`. Greedy argmax over 20 steps locks into
single-token loops easily; absolute Korean count understates model
uncertainty. Per-step top-k entropy probe would refine.

C5 — BG-CI L13 onset (rank-100) + BG-CS L0 onset (rank-1) describe
two different "exits" from the Korean basin and are consistent. This
is a calibration signal for the L13 narrative, not a chat-capability
rescue path on its own.

## Deliverables

- `state/anima_emerge_chat_partial_layers_2026_05_05/aggregate.json` —
  per-config emit + counts (11 entries).
- `state/anima_emerge_chat_partial_layers_2026_05_05/verdict.json` —
  schema/1 verdict with falsifier-style aggregate.
- `tool/transient_py/anima_emerge_chat_partial_layers.py` — helper
  (gitignored per `**/*.py` plus .own 3 transient sister-rule).
- This doc.

## Compliance

- transient .py sister-rule (.own 3 / raw-37 family) PASS — gitignored namespace.
- additive only (raw-15 family) PASS — no mount.hexa, dialogue, or shim mod.
- honest C3 (raw-10 family) PASS — five caveats emitted to verdict.json + stderr.
- HF token leak — none. Helper does not log secrets.
- Commit — none (no `git add`/`git commit` performed).
- Cost — $0 (mac CPU only).
- Wall time — ~30s end-to-end (load 5.0s + 11 configs × ~2s greedy).
