# HF Private Upload Spec — anima-native-ko-chat-template (BG-HA)

**Status**: PRIVATE upload pending (own 15 PRIVATE→PUBLIC lifecycle, post-verification only)
**bg_id**: BG-HA
**verdict**: SIMPLE_STACK_PASS (own 18 4-cond × 5-prompt × 7-cell)
**ts_run**: 20260507_012829

## Repo target (PRIVATE first)

- repo_id: `need-singularity/anima-native-ko-chat-template-byte-18m`
- visibility: **PRIVATE** (own 15 — public promote AFTER verification gates)
- repo_type: model

## Artifacts to upload

| local path | hf path | size |
|---|---|---|
| `state/anima_native_ko_chat_template_train_2026_05_07/ckpt_final/ckpt_final.pt` | `ckpt_final.pt` | 70.3MB |
| `state/anima_native_ko_chat_template_train_2026_05_07/verdict.json` | `verdict.json` | 12.4KB |
| `state/anima_native_ko_chat_template_train_2026_05_07/eval_log.jsonl` | `eval_log.jsonl` | 109KB |
| `state/anima_native_ko_chat_template_train_2026_05_07/train.log` | `train.log` | 65KB |
| `tool/transient_py/anima_native_ko_chat_template_train.py` | `train_script.py` | reference |

## Model card stubs (own 14 hf_upload_mk2 naming convention)

```yaml
license: apache-2.0
language: ko
tags:
  - anima-native
  - byte-level
  - korean
  - from-scratch
  - own-18-simple-stack-pass
pipeline_tag: text-generation
```

### Title (KO+EN bilingual per anima convention)

```
anima-native-ko-chat-template (18M byte-level Korean chat-template)
한국어 chat-template 18M byte-level 모델 — 첫 own 18 simple-stack PASS
```

### Body 핵심 fields

- **Architecture**: ConsciousLM (custom, NOT external substrate per own 17)
  - vocab=256 (byte-level), n_layer=6, d_model=384, n_head=6, block_size=256
  - total params: 18,031,872 (~18M)
- **Training**: 10000 steps, batch=8, grad_accum=8 (effective 64), lr=3e-4 cosine warmup 500
- **Hardware**: ubu1 RTX 5070 sm_120 bf16, 124s (2.07min) wall
- **Corpus**: corpus_chat_template.txt 236.96MB (chat-template ≥30% per own 20)
- **train_loss_final**: L_A=1.5907

### Eval (own 18 4-cond × 5-prompt × 7-cell)

| prompt | C1.1 | C1.2 | C1.3 | C2.1 | C2.2 | C2.3 | C2.4 |
|---|---|---|---|---|---|---|---|
| 안녕하세요 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 한국어 가능? | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 오늘 기분 어때? | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 사용자/도우미 turn | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 코드를 짜줘 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

**SIMPLE_STACK_PASS = 5/5** (sample mode aggregate, C2.4 strict ALL-of)
**c2_4_named_speaker_leak**: False (10 names checked, 0 leaked)

## Verification gates (PRIVATE → PUBLIC promotion conditions)

1. [ ] PRIVATE upload sha256 verify (LFS x-linked-etag round-trip)
2. [ ] Inference smoke test from HF Hub (load_state_dict + 5-prompt regen)
3. [ ] SIMPLE_STACK_PASS reproducible on Mac MPS load
4. [ ] cross-platform replay (ubu1 train → Mac inference equivalence)
5. [ ] 사용자 explicit `OK PUBLIC promote` after gates

## Pre-push hook

`tool/hf_upload_mk2_pre_push_hook.hexa` — own 14 mandate.

## Cross-link

- own 17: anima identity boundary (anima-native, NO external substrate wrap)
- own 18: simple-stack 4-condition × 7-cell strict
- own 19: corpus priority (chat-template ≥30%)
- own 20: chat-template format mandate
- own 14: hf_upload_mk2 naming
- own 15: PRIVATE → PUBLIC lifecycle
- ledger: `docs/anima_consciousness_check_simple_stack_2026_05_06.md` row 11

## Next cycle

- BG-HB: actual HF private upload (separate cycle, hf_upload_mk2.hexa flow)
- BG-HC: cross-platform inference verify (Mac MPS reload)
- BG-HD: PUBLIC promote (post user 결재)
