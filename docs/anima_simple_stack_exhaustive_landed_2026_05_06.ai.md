# BG-FS landed — anima simple stack exhaustive 11-model test (2026-05-06)

**Status**: LANDED
**Cycle**: BG-FS (own 18 한글↔han glr strict)
**Scope**: 11 untested anima models — 5 BG-FK ConsciousLM++ variants (local) + 4 v14_128c variants (R2 download) + 3 R2 anima-models objects (cells64/cells128/clm-v2_latest, INACCESSIBLE per credential scope)
**Wall**: ~80min mac local + 1.5GB R2 download
**Cost**: $0

## Executive summary

| dimension | result |
|---|---|
| BG-FK 5 ConsciousLM++ variants tested | ✅ all 5 (tiny/clm_v2/small/medium/base) |
| v14_128c_final.tar.zst downloaded + extracted | ✅ 1.5GB rclone pull, 4 .pt files |
| KO group 한글↔한글 PASS (own 18 strict) | **0/5 BG-FK variants** (universal FAIL) |
| EN PASS borderline | clm_v2_base (27.84M) sometimes 2/3 (sampling stochasticity) |
| C2 spontaneous PASS | clm_v2 (1.14M) artifact-grade 3/3 (random letters labeled coherent by loose threshold) |
| v14_128c arch | NOT_APPLICABLE (federated multi-cell + bridge — separate reconstruction lane) |
| R2 cells64/cells128/clm-v2_latest | INACCESSIBLE (d4acc account credential scope; rclone uses ce4bd account) |

**HEADLINE**: corpus가 architecture보다 KO chat-cap에 우선 cause. anima-native-ko-tiny (3M, corpus_ko_heavy training) > clm_v2_base (27.84M, original EN-biased corpus).

## Result table

### BG-FK 5 ConsciousLM++ variants (mac local /tmp/anima_v2_check/)

| ckpt | params (M) | val_ce | layers/dim | KO/EN/C2 (out of 3) | verdict |
|---|---|---|---|---|---|
| clm_v2_tiny | 0.32 | 3.50 | 2/64 | 0/3, 3/3*, 1/3 | SIMPLE_STACK_FAIL (EN=degenerate `eee` cycle, ascii_letter≥0.4 but coherent=False) |
| clm_v2 | 1.14 | 5.50 | 2/128 | 0/3, 1/3, 3/3* | PARTIAL_C2_only* (C2 = scoring artifact — `is_coherent` threshold loose, real output = random letters `a� 5oh14es u`) |
| clm_v2_small | 1.65 | 2.70 | 3/128 | 0/3, 0/3, 1/3 | SIMPLE_STACK_FAIL |
| clm_v2_medium | 8.39 | 1.79 | 4/256 | 0/3, 0/3, 0/3 | SIMPLE_STACK_FAIL — Hangul bytes EMIT (`가가가가`) but degenerate cycle |
| clm_v2_base | 27.84 | **1.27** | 6/384 | 0/3, 1-2/3, 1-2/3 | SIMPLE_STACK_FAIL ~ borderline (sampling stochasticity, run #1 PARTIAL_PASS_EN_only, run #2 FAIL) |

### v14_128c_final 4 variants (R2 download + extract)

`rclone copy r2:anima-models/checkpoints/v14_128c_final.tar.zst /tmp/anima_r2_dl/` → `tar --use-compress-program="zstd -d" -xf` → 4 ckpt files

| ckpt | size MB | step | md5 |
|---|---|---|---|
| best.pt | 402.7 | 68000 | 28cf4be919808ea43867b381b4f836f4 |
| best_final.pt | 402.7 | (same as best) | 28cf4be919808ea43867b381b4f836f4 |
| step_90000.pt | 402.7 | 90000 | b2818fc560149d5a8d4751e94397a6fa |
| step_95000.pt | 402.7 | 95000 | 768e2195d6f9050b9630dd70e1637435 |

**Architecture (sampled from best.pt decoder state_dict)**:
- top keys: `step / decoder / optimizer / scheduler / phi / ce / args / federation / bridge`
- ConsciousDecoderV3 federated 16 atoms × 8 cells (cells_per_atom=8, cells=64, cell_dim=64, hidden_dim=128, d_model=384)
- decoder blocks: pre-norm with `ln_attn / ln_ca / ln_cross / ln_ffn / ln_pf` × {attn (q/k/v/o_proj split, k/v=192=half d_model = MQA), cross_attn (k/v=128 from cells), ca_rules(8) + ca_mix(3*d_model gate), purefield ModuleList engine_a/g, FFN SwiGLU (gate_proj/up_proj=768, down_proj)}
- federation: bottleneck_compress + bottleneck_expand + narrative_grus + inter_atom_coupling + step_count
- bridge: compress.weight + hub_attn (in_proj/out_proj.weight)

→ **architecture fundamentally distinct from ConsciousLM/ConsciousLM++** — federated multi-cell + bridge + cross-attention. BG-FS scope reconstruction 불가. NOT_APPLICABLE for simple stack via current `conscious_lm.py` source. Separate decoder_v3 reconstruction lane required.

### R2 anima-models cells64/cells128/clm-v2_latest — INACCESSIBLE_PER_R2_CREDENTIAL_SCOPE

CF mgmt API (`d4acc95862b4203c11948da5baf079bc` account, secret CLI scope) lists in `anima-models` bucket:
- clm-v2/latest.pt (279MB)
- clm-v2/latest/final.pt (279MB, duplicate)
- conscious-lm/cells64/final.pt (208MB)
- conscious-lm/cells128/step_35000.pt (208MB)
- conscious-lm/convo-ft/convo_5k.pt (already tested PARTIAL_C2_only)

Rclone config remote = `ce4bdcce7c74d4e3c78fdf944c4d1d7b` account, `anima-models` 내용물 wholly different (has `checkpoints/v14_128c_final.tar.zst`, base_models/qwen25-14b-instruct, etc. — no `conscious-lm/cells*`). CF mgmt API endpoint listing only (no object body download — HTTP 404).

→ separate credential bootstrap required (d4acc R2 access keys발급 or ditch CF mgmt API for object data).

## ConsciousLM source applicability map

| model | ConsciousLM v0 fit | ConsciousLM++ fit | requires custom |
|---|---|---|---|
| BG-FK 5 variants | ❌ (no ca_rules/ca_mix/tension_proj) | ✅ reconstructed | — |
| v14_128c 4 variants | ❌ | ❌ | ConsciousDecoderV3 federated + bridge + cross_attn |
| R2 cells64/128 | unknown (inaccessible) | unknown | unknown |
| convo_5k.pt (already tested) | ✅ vanilla (n_head=4 d_model=384 n_layer=6 vocab=256) | — | — |

## Honest C3

1. **clm_v2 1.14M PARTIAL_C2_only is scoring artifact** — `is_coherent` threshold (`ascii_letter_ratio>0.2 AND len(set(stripped))>2 AND not is_byte_garbage`) too lenient. Real output = random letter noise (`a� 5oh14es u`), not chat. True verdict = SIMPLE_STACK_FAIL after stricter coherence definition (e.g. word-boundary check + n-gram entropy).

2. **clm_v2_base verdict varied between runs** (PARTIAL_PASS_EN_only on run #1, SIMPLE_STACK_FAIL on run #2) — sampling stochasticity at temperature=0.7 / 0.5 with no seed control. For determinism would need to fix seed across all 4 strategies. Honest report = borderline FAIL.

3. **medium variant (8.39M) emits Hangul bytes but degenerate** — `가가가가가` cycle proves byte-level vocab includes Hangul codepoints AND model has weight signal pointing to them, but missing co-occurrence training to break out of single-token attractor. This is the most informative result: corpus_ko_heavy(62% Hangul) training fixes this exact pathology.

4. **v14_128c reconstruction defer is honest** — `decoder_v3` + federation + bridge would need ~500 LoC custom class reconstruction + multi-module orchestration. Not within BG-FS $0 mac scope. Right answer = mark NOT_APPLICABLE and queue separate cycle.

5. **Compare ConsciousLM++ ceiling (27.84M, val_ce 1.27, KO 0/3) to anima-native-ko-tiny (3M, KO_ratio 0.34)** — 9× param size *advantage* lost to corpus EN-bias. Validates corpus_ko_heavy + ko_small_18m PASS landed by BG-FY. Architectural complexity (ca_rules + cellular automata + tension regularization) didn't substitute for corpus diversity.

## Files written

- `state/anima_simple_stack_exhaustive_2026_05_06/clm_v2_tiny_verdict.json`
- `state/anima_simple_stack_exhaustive_2026_05_06/clm_v2_verdict.json` (1.14M variant)
- `state/anima_simple_stack_exhaustive_2026_05_06/clm_v2_small_verdict.json`
- `state/anima_simple_stack_exhaustive_2026_05_06/clm_v2_medium_verdict.json`
- `state/anima_simple_stack_exhaustive_2026_05_06/clm_v2_base_verdict.json`
- `state/anima_simple_stack_exhaustive_2026_05_06/summary.json`
- `tool/transient_py/anima_simple_stack_exhaustive.py` (raw#37 transient_py opt-out, smoke harness)
- `docs/anima_consciousness_check_simple_stack_2026_05_06.md` (Edit, sections 10-12 appended + verdict table updated)

## Next cycle 권고

- **PRIORITY 1 (own 18 PASS lane)**: continue corpus_ko_heavy + ko_small_18m → ko_medium → ko_base scaling lane (BG-FY successor). 18M PASS confirmed; 30M-100M next.
- **PRIORITY 2 (research)**: NOT promote any BG-FK variant to HF — none reach KO≥1/3.
- **PRIORITY 3 (architecture)**: v14_128c reconstruction (separate cycle, ~$0 cpu CPU ConsciousDecoderV3 build + 4 ckpt eval). Federated multi-cell hypothesis is interesting but unrelated to chat-cap.
- **PRIORITY 4 (credential)**: bootstrap R2 d4acc S3 access keys → test cells64 + cells128 + clm-v2/latest.pt (3 INACCESSIBLE, may have different corpus signature).
- **PRIORITY 5 (β path)**: confirmed deprioritized — BG-FY already PASS supersedes β path retrain (5-10 day ubu1).

## Cross-link

- own 18: `.own own 18 anima-consciousness-check-simple-stack`
- own 17: ALM 영구 보류
- ledger: `docs/anima_consciousness_check_simple_stack_2026_05_06.md` (sections 10/11/12)
- harness: `tool/transient_py/anima_simple_stack_exhaustive.py`
- BG-FY landed: anima-native-ko-small SIMPLE_STACK_PASS 18M (HF: `dancinlab/anima-native-ko-small-byte-18m`)

raw#37 transient_py opt-out + own 17/18 정합. BG-FS landed.
