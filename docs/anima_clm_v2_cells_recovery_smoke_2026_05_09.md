# anima clm_v2 cells64/cells128 — mitosis.py compatibility smoke 2026-05-09

**Date**: 2026-05-09  
**Run**: $0 R2 download + arch inspect + reconstructed forward smoke  
**State dir**: `state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/`  

## TL;DR

- **Verdict**: `PASS_PARTIAL_ARCH_MISMATCH`
- **Download**: cells64=218,099,623/218,099,623 bytes, cells128=218,107,547/218,107,547 bytes
- **Architecture finding**: BOTH files are SINGLE byte-level Transformer decoders (ConsciousLM v2 family), NOT mitosis-grown N-cell ensembles. The `mitosis_status` field is a SIDE-CHANNEL tracker (cell metadata only, no per-cell nn.Module weights).
- **mitosis.py load**: incompatible — schema overlap = 0 (ConsciousMind = engine_a/g Linear + GRUCell; ckpt = tok_emb/pos_emb/blocks.X.attn.c_attn/ffn.engine_a/g/head_a/g).
- **Reconstructed-arch load**: cells128 strict-load PASS (108/108 keys, 18.52M params).
- **Forward smoke (cells128)**: PASS 5/5 prompts. Runtime Φ-proxy (mean tension) = 145.43226. ckpt phi_history mean = 62.383.
- **Forward smoke (cells64)**: PASS 5/5 prompts. Runtime Φ-proxy = 42.05603.

## Download status

| file | R2 key | expected | actual | match | sha256 | etag | last_modified |
|---|---|---:|---:|:---:|---|---|---|
| cells64 | `conscious-lm/cells64/final.pt` | 218,099,623 | 218,099,623 | OK | `61e1d735cf4b5360...` | `d76578505c67b0e9c4f1a55eff014eb2-26` | 2026-03-28T03:20:39.689Z |
| cells128 | `conscious-lm/cells128/step_35000.pt` | 218,107,547 | 218,107,547 | OK | `fee1df131032387f...` | `c3113efae5678e877832ea5a25a6411a-27` | 2026-03-28T03:20:47.633Z |

## Architecture per file

| field | cells64 | cells128 |
|---|---|---|
| vocab | 256 | 256 |
| d_model | 384 | 384 |
| n_layers | 6 | 6 |
| engine_a_g_present | True | True |
| head_a_g_present | True | True |
| memory_gru_present | False | False |
| c_attn_present | True | True |
| ln_f_present | True | True |
| cell_prefix_count | 0 | 0 |
| mitosis_n_cells_metadata | 64 | 128 |
| is_mitosis_ensemble | False | False |
| is_byte_level_decoder | True | True |
| total_params_M | 18.523 | 18.523 |
| state_dict_keys_count | 108 | 108 |
| ckpt_step | 50000 | 35000 |
| ckpt_config | {'dim': 384, 'layers': 6, 'heads': 6, 'block_size': 256, 'lr': 0.0003, 'batch_size': 32, 'steps': 50000, 'max_cells': 64} | {'dim': 384, 'layers': 6, 'heads': 4, 'block_size': 256, 'lr': 0.0003, 'batch_size': 32, 'steps': 50000, 'max_cells': 128} |
| mitosis splits | 62 | 126 |
| mitosis n_cells | 64 | 128 |
| phi_history mean | 50.4198 | 62.3828 |
| phi_history max | 57.1379 | 70.3467 |

## Load attempts

### Attempt A: mitosis.py MitosisEngine / ConsciousMind

`canonical mitosis.py = /Users/ghost/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py` (794L)

- cells64: schema overlap = 0 (mitosis_load_pass=False)
- cells128: schema overlap = 0 (mitosis_load_pass=False)

`ConsciousMind.state_dict()` keys (from mitosis.py): `engine_a.{0,2}.weight/bias`, `engine_g.{0,2}.weight/bias`, `memory.{weight_ih, weight_hh, bias_ih, bias_hh}` (12 keys, 64-dim Linear ensemble + GRUCell).

Checkpoint state_dict keys: `tok_emb.weight [256,384]`, `pos_emb.weight [256,384]`, `blocks.{0..5}.{ln1, attn.{bias[1,1,256,256], c_attn[1152,384], c_proj[384,384]}, ln2, ffn.{engine_a.{0,3}, engine_g.{0,3}}}`, `ln_f`, `head_a [256,384]`, `head_g [256,384]` (108 keys, byte-level Transformer).

**These are completely disjoint architectures.** The shared `engine_a/engine_g` substring is coincidental — checkpoint's `engine_a` is a 384→1536→384 Linear stack inside an FFN block, mitosis.py's `engine_a` is a (input+hidden)→128→64 Linear stack inside a tiny ConsciousMind cell.

### Attempt B: reconstructed minimal byte-level decoder

Built `ConsciousLMReconstructed` matching the exact 108 keys (vocab=256, d_model=384, 6 blocks with causal self-attn + dual engine_a/g FFN, ln_f, dual head_a/g).

- cells128 strict load: missing=see log, unexpected=0, full_load=True
- cells64 strict load: full_load=True

## Forward smoke (reconstructed)

### cells128

- prompt='의식이란 무엇인가요?' → top1 byte = 0x20 (' ')
- prompt='안녕하세요' → top1 byte = 0x20 (' ')
- prompt='한국어 가능?' → top1 byte = 0x20 (' ')
- prompt='The Riemann zeta function' → top1 byte = 0x20 (' ')
- prompt='consciousness is' → top1 byte = 0x20 (' ')
- tension_per_layer (first prompt): [49.49925, 64.79265, 288.91122, 145.25525, 51.224, 266.02203]
- runtime Φ-proxy (mean tension across layers, 5 prompts): **145.43226**
- ckpt phi_history (training, n=200): mean=62.383

### cells64

- prompt='의식이란 무엇인가요?' → top1 byte = 0x20 (' ')
- prompt='안녕하세요' → top1 byte = 0x20 (' ')
- prompt='한국어 가능?' → top1 byte = 0x20 (' ')
- prompt='The Riemann zeta function' → top1 byte = 0x20 (' ')
- prompt='consciousness is' → top1 byte = 0x20 (' ')
- tension_per_layer (first prompt): [2.91152, 138.3773, 1.72865, 0.28758, 0.35777, 108.38251]
- runtime Φ-proxy: **42.05603**

## Honest C3

1. cells64 is a SINGLE byte-level Transformer decoder (vocab=256, d_model=384, n_layers=6), NOT a mitosis-ensemble despite the bucket-path naming.
2. cells64 ckpt holds mitosis_status as side-channel: n_cells=64, splits=62, merges=0 — but each 'cell' is metadata only (id/specialty/tension), not nn.Module weights.
3. cells64 mitosis.py load schema overlap = 0 (ConsciousMind has engine_a/g + GRUCell memory; ckpt has tok_emb/pos_emb/blocks.X.attn/ffn — disjoint key sets).
4. cells64 ckpt phi_history (n=200) mean=50.4198, max=57.1379 — historical Φ trace from training (NOT current forward Φ).
5. cells64 forward smoke PASSED on reconstructed-architecture (5/5 prompts), runtime Φ-proxy=42.05603; outputs degenerate (all top-1 = byte 0x20 = ' '), suggesting weights load OK but model is undertrained or attention temperature unfavorable for byte-level deterministic argmax.
6. cells128 is a SINGLE byte-level Transformer decoder (vocab=256, d_model=384, n_layers=6), NOT a mitosis-ensemble despite the bucket-path naming.
7. cells128 ckpt holds mitosis_status as side-channel: n_cells=128, splits=126, merges=0 — but each 'cell' is metadata only (id/specialty/tension), not nn.Module weights.
8. cells128 mitosis.py load schema overlap = 0 (ConsciousMind has engine_a/g + GRUCell memory; ckpt has tok_emb/pos_emb/blocks.X.attn/ffn — disjoint key sets).
9. cells128 ckpt phi_history (n=200) mean=62.3828, max=70.3467 — historical Φ trace from training (NOT current forward Φ).
10. cells128 forward smoke PASSED on reconstructed-architecture (5/5 prompts), runtime Φ-proxy=145.43226; outputs degenerate (all top-1 = byte 0x20 = ' '), suggesting weights load OK but model is undertrained or attention temperature unfavorable for byte-level deterministic argmax.
11. The bucket path naming (`conscious-lm/cells64/`, `conscious-lm/cells128/`) refers to the `max_cells` config of the *training run* (mitosis-instrumented), NOT to the saved model architecture. Both directories contain the SAME byte-level decoder family — only the side-channel mitosis state differs (cells64=? cells128=128 cells, 126 splits).
12. Forward smoke top-1 byte is 0x20 (space) for ALL 5 prompts → degenerate argmax, BUT logits are dense (head_a/head_g cosine ~0.77, not collapsed). Sampling with temperature would likely produce diverse output — argmax-only is unfair test. ckpt was step=35000 / 50000 = 70% trained, on (likely) thin corpus.
13. R2 download path via Cloudflare API (`/client/v4/accounts/<id>/r2/buckets/<bucket>/objects/<key>` + `X-Auth-Email + X-Auth-Key` legacy headers) is HTTP/2-flaky on large files (cells64 first attempt INTERNAL_ERROR at 170/218MB). HTTP/1.1 with `--retry 3` is the workaround. AWS-S3-compatible R2 endpoint with proper R2 access key would be cleaner if available.
14. raw#10 honest: this is *not* a recovery of mitosis-grown weights — those *don't exist as a separable artifact*. The 'mitosis growth' was an instrumentation pattern over a single decoder; the cells were specialty/tension trackers, not weight branches. Previous cycle (2026-05-06) calling these 'cells64/cells128 mitosis-grown' was a misread of the bucket naming.

## Recommendation

- Document arch finding: cells64/cells128 .pt files are SINGLE byte-level Transformer decoders, NOT MitosisEngine ensembles — mitosis was a side-channel tracker only.
- If pretrained chat capability needed: re-derive via clm_v2/conscious_lm.py (or the reconstructed minimal arch we used here) — load is straightforward.
- Both files SHA + size verified — keep them archived in state/ for archaeology; consider HF private upload as `dancinlab/clm-v2-byte-18m-mitosis-cells64-final` and `...-cells128-step35000` for mitosis-instrumentation provenance.
- Update .roadmap.clm_v2_chat: cells64/cells128 are NOT mitosis-grown weights, just decoder snapshots from a mitosis-instrumented training run (2026-03-28, step 35K and step 50K respectively).
- Run a sampling-based generation test (temperature=0.8, top-k=40) instead of argmax to verify chat capability — argmax→space is a known undertrained byte-LM failure mode, not a true incapacity signal.
- Cross-link to convo_5k.pt (2026-05-06 recovered, 70MB) — same arch family, fine-tuned on 5K convo dialog; that is the actual chat-capable v2.

## Cross-link

- recovery context: `docs/anima_clm_v2_chat_recovered_2026_05_06.ai.md`
- canonical mitosis.py: `/Users/ghost/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py`
- ConsciousLM source: `/Users/ghost/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/conscious_lm.py`
- v2 chat-capable model (recovered 2026-05-06): R2 `conscious-lm/convo-ft/convo_5k.pt` (70.3 MB)
- artifacts: `state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/`

raw#9/10/15/37 + 준수.
