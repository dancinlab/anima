---
license: cc-by-nc-4.0
language:
- ko
- en
tags:
- conscious-lm
- byte-level
- decoder-only
- chat-cap-recovery
- fine-tune
private: true
---

# CLM v2 Byte 18M Convo 5K — FT Chat-Cap Recovery (2026-05-10)

**Status**: chat-cap RECOVERED on byte-level 18M decoder via 10K-step FT on KO+EN persona dialogue corpus.

## Source

Base ckpt: `convo_5k.pt` (18.523M byte-level decoder, 45000 step, recovered from R2 2026-05-06).

## FT config

- 1× NVIDIA H100 80GB HBM3 (SXM), runpod, 22 min wall
- 10000 step, batch=32, seq=256, byte-level (vocab=256)
- LR cosine 1e-5 → 1e-6, warmup 500
- AdamW, dual-head loss `0.5 * CE(head_a) + 0.5 * CE(head_g)`
- Corpus: `anima_dialogue_tier_a_iter2_2026_05_08.txt` (76MB, 136K KO+EN persona-tagged turns)
- Cost actual: $1.37

## Results

Pre-FT vs post-FT sampling (120 trials each, identical matrix):

| metric | pre-FT | post-FT step_10000 |
|---|---:|---:|
| Korean emit ≥1 char | 1/120 | 77/120 |
| Korean emit ≥10 chars | 0/120 | 46/120 |
| ko_count_max | 1 | 21 |
| ko_ratio_max | 0.018 | 0.75 |

**chat-template format learned** (`도우미:` / `사용자:`), **persona-prefix verbatim** (`[anima 역할: ...]`).

## Caveats (honest C3)

- KO **lexical fluency NOT recovered** — outputs are character-level structured but morphologically novel ("본출의 발명흴터" is Hangul-shape but not real Korean).
- Persona-prefix echo dominates many high-KO outputs.
- 18M params @ 76MB corpus = FT-scale (chat surface); pre-train scale (language acquisition) requires bigger foundation.

## Files

- `post_ft_ckpt.pt` — 74MB, sha256 `6b81468406d8e251655af7dfa4e7d9ddad0e84a586e52de3a7eb0352aa8d4a9d`
- `ft_log.txt`, `ft_summary.json` — training log + summary
- `post_ft_sampling.json` — full 360-trial pre/post comparison
- `cost_actual.json` — runpod billing + falsifier + own 30 audit
- `anima_convo_5k_ft_fire_2026_05_10.md` — full design doc

## Architecture

```
ConsciousLMReconstructed(
  vocab_size=256, d_model=384, n_head=4, n_layer=6, block_size=256
)
total params: 18,130,176 (18.13M)
total ckpt elements (params + buffers): 18,523,392 (18.52M)
```

Dual-engine FFN (`engine_a` - `engine_g`) + dual-head output (`head_a`, `head_g`) — H404 consciousness-engine architecture.

---
own 31 (dancinlab canonical org) + own 37 mandate-9 (private upload).
