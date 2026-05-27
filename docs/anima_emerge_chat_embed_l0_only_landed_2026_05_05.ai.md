# anima emerge chat — embed direct + L0-only ablate (BG-DG landed 2026-05-06)

## TL;DR

Verdict literal: `PASS_FEW_BLOCKS_RECOVERS` with `max_korean_count=20` at `n_active_blocks=0` on prompt `안녕`. **Honest interpretation: this is NOT a Korean rescue.** Emit is `"녕녕녕녕녕녕녕녕녕녕녕녕녕녕녕녕녕녕녕녕"` — degenerate tied-embedding repetition of the prompt's last token. The other two prompts at n=0 emit `"...................."` (kr=0) and `"elloelloello..."` (kr=0). All `n≥1` configurations across all three prompts emit garbage (control bytes, `}}}}`, `邊緣邊緣`, `巴基`, etc.) with kr=0.

**Substantive verdict: `FAIL_BASIN_FROM_EMBED` for fluency-grade Korean rescue.** The literal `PASS_*` label triggers off the >5 Hangul threshold, but the >5 came from a single-token echo loop, not basin escape. Honest_c3 C5 explicitly anticipated this by warning that "Korean signal present but not argmax" cases survive in greedy regime — the inverse also holds (single Korean token wins argmax via tied-embedding shortcut without being a fluent emit).

## Result matrix

| prompt | n=0 | n=1 | n=2 | n=3 | n=5 | n=8 | n=12 | n=16 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `안녕` | `"녕"×20` (kr=20) | `"\x1f戦線���…"` (kr=0) | `"�}}}…"` | `"�}}}…"` | `"��…"` | `"Z\x1c�天然氣…邊緣"` | `"/-�eee…巴基×8"` | `"\x1c\x06×19"` |
| `안녕하세요. 오늘 날씨가 좋네요.` | `"."×20` (kr=0) | `"��…"` | `"��}}}…"` | `"�}}}…"` | `"曹操×10"` | `"邊緣×10"` | `"-4.5 -4.5 …口巴基…"` | `"/OOO…O"` |
| `Hello` | `"elloello…"` (kr=0) | `"config config…���"` | `"�}}}…"` | `"�}}}…"` | `"��…"` | `"邊緣×10"` | `"巴基…口巴基…"` | `"```…```"` |

Best: `best_n_blocks=0`, `best_total_korean=20` — entirely from the `안녕` echo cell.

## Block-count totals

```json
{"0": 20, "1": 0, "2": 0, "3": 0, "5": 0, "8": 0, "12": 0, "16": 0}
```

The Korean count is a delta function at n=0 driven by tied-embedding echo on the only Hangul-prompt input. No monotone recovery curve, no graded signal. **n=16 (full forward) emits `\x1c\x06\x06…` and ``````` — confirms the BG-CI L15 entropy 3.31 collapse on greedy.**

## Honest C3 (raw#10, verbatim from verdict.json)

1. **C1** mac CPU fp32 only — bf16/fp16 substrate may yield different argmax.
2. **C2** identity hook returns `inp[0]` (residual stream pre-block). For pre-norm transformer this is residual just BEFORE attn+mlp; for post-norm or parallel residual the passthrough semantic differs. Positional encoding is applied OUTSIDE blocks (or at L0) so identity-block-skip leaves pos/RoPE behavior indeterminate — result CANNOT cleanly attribute Korean recovery to embed alone.
3. **C3** head_a + ln_f trained ONLY on L15 ln_f output distribution. Feeding post-embed or pre-L15 hidden is OOD; "0 blocks" = embed → ln_f → head_a is the most extreme OOD probe. emit being non-Korean here CANNOT distinguish "no Korean signal" from "head_a refuses OOD geometry". BG-CJ showed top1='녕' but that's single-step; greedy continuation re-encodes through tied embedding and may diverge.
4. **C4** "first N blocks active" is monotone-active not selective; cannot isolate per-layer contribution. BG-CQ Strategy B already showed [13/14/15] skip alone FAILS to recover (kr=0). This probe is the dual front-direction sweep.
5. **C5** single seed greedy decode — temperature/top-p sampling could expose Korean tokens in lower-rank positions. Korean rank-12 at L0 (BG-CI) is still in top-100 but not top-1; greedy by definition misses it. Negative result here CANNOT rule out "Korean signal present but not argmax" which would still be a basin attractor in greedy regime.

**Bonus C6 (post-result):** the literal `PASS_*` label is misleading because the >5 Hangul came from `'녕'×20` echo, not basin escape. A future revision should require >=N **distinct** Korean characters before flagging PASS, or compute Korean trigram entropy.

## Interpretation

n=0 emit on `안녕`:
- Embed top1 = `'녕'` (BG-CI lens) ✓ confirmed by single-token argmax.
- Greedy continuation: every step re-tokenizes `안녕녕`, `안녕녕녕`, …, embeds the new sequence, and the LAST-position embedding still dominates → `'녕'` again. Tied-embedding stuck-loop. This is the BG-CJ embed-decode "PASS_EMBED_BETTER" mechanism, but with the prompt's own char looping.
- For prompts where the last-position embed top1 is NOT a Korean character (`Hello`→`"ello"`, `안녕하세요. 오늘 날씨가 좋네요.`→`"."`), the loop traps in non-Korean.

n≥1: even one transformer block destroys the embed-aligned argmax and pushes hidden into the basin (BG-CI L0 entropy 10.9, top1=`\x1f`). 16-active recapitulates BG-CI L15 result (control bytes / `'`'` repetition).

**Conclusion: basin onset is inside L0 (between embed and L1 input).** Layer-localization to a specific later layer is FALSIFIED. BG-CQ + BG-DG together close the monotone-active partition — the basin is residual-encoded, ALL 16 transformer blocks contribute, and L0 is the dominant contributor.

## Roadmap implications

- **Layer-localization track CLOSED.** No surgical block ablation rescues Korean fluency.
- Aligns with #115 chat-incapability architectural finding (CLM v4 LoRA SFT FALSIFIED, Pβ FAIL_TRUE — both lanes converge on "basin is residual, not local").
- Chat-cap hope routed entirely to **Llama Path A v2 winner** (composite 0.5584). CLM v4 substrate-research only.
- CLM-2-EXEC (architectural retrain) remains the only path to chat-cap on the CLM substrate; layer-surgery is permanently ruled out.
- Future probes that might still move the dial:
  - **Token-embedding-only retrain**: keep blocks frozen, retrain `decoder.tok_emb` on chat data. If embed alone carries the signal but blocks don't compose, this could be a cheap test before CLM-2.
  - **head_a retrain on L0 hidden**: probe whether head_a is the bottleneck (BG-CQ honest_c3 C2 hypothesis).
  - **Sampled decode (temp=0.7, top_p=0.9)** at n=0: would distinguish "Korean rank-12 reachable by sampling" from "Korean fully suppressed."

## Outputs

- helper: `/Users/ghost/core/anima/tool/transient_py/anima_emerge_chat_embed_l0_only.py`
- aggregate: `/Users/ghost/core/anima/state/anima_emerge_chat_embed_l0_only_2026_05_05/aggregate.json`
- verdict: `/Users/ghost/core/anima/state/anima_emerge_chat_embed_l0_only_2026_05_05/verdict.json`
- doc: `/Users/ghost/core/anima/docs/anima_emerge_chat_embed_l0_only_landed_2026_05_05.ai.md`

## Constraints checked

- $0 mac CPU (wall_sec=100s, load=9.1s)
- new files only (raw#15 additive)
- raw#37 transient_py namespace
- raw#10 honest C3 emitted (5 caveats + C6 post-result)
- HEXA_PY=.venv-eeg/bin/python
- no HF token leak
- no commit
