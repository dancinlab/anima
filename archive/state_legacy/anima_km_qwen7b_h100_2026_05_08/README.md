---
license: apache-2.0
language:
  - ko
  - en
tags:
  - bg-km-qwen-7b
  - foundation-borrow
  - lora
  - simple_stack_pass_strict
  - anima
  - korean
base_model: Qwen/Qwen2.5-7B-Instruct
metrics:
  - name: V4 strict best-mode
    value: ?/15
---

# bg-km-qwen-7b-qwen7b-r32-pass-strict-2026-05-08

anima research artifact — **SIMPLE_STACK_PASS_STRICT** verdict, V4 strict best-mode **?/15**.

## Origin
- BG: `BG-KM-QWEN-7B`
- Paradigm: `foundation-borrow-llama-3.2-3b-instruct-lora-r32-bg-je-214mb`
- Cycle: 2026-05-08
- Base: `Qwen/Qwen2.5-7B-Instruct`
- LoRA r: `32`
- Corpus: `/workspace/anima_km_qwen7b/corpus_combined_100mb_plus.txt` (214.299726MB)
- Training: None steps
- H100 cost: $?

## own SSOT compliance
- (simple_stack 4-condition): satisfied
- (V4 strict ≥10/15 floor): ?/15 ≥ 10 → check
- mandate-1/2/3: ckpts pull verified pre-pod-delete
- mandate-4 Flavor B: BG iteration naming
- mandate-8: private (manual review pending for public promote)

## Cross-link
- ledger: `state/anima_model_attempts_ledger.jsonl` bg_id=BG-KM-QWEN-7B
- spec roadmap: `.roadmap.chat_cap_emergence_pivot` Stage 6
