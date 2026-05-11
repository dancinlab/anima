---
license: llama3.2
base_model: meta-llama/Llama-3.2-3B
library_name: peft
pipeline_tag: text-generation
tags:
- lora
- peft
- anima
- foundation-borrow
- korean
language:
- ko
- en
---

# anima-foundation-borrow-a-llama32-3b-lora

LoRA adapters fine-tuned on Llama-3.2-3B with the anima-persona Korean+mixed corpus (BG-JE 214 MB, ~702K QA pairs, 3-variant persona prefix rotation). Produced by the **BG-FOUNDATION-BORROW-A** lane on 2026-05-10 (cycle 2026-05-10, anima reborn, §43).

## Quick facts

- Base model: `meta-llama/Llama-3.2-3B` (3.2 B params, frozen)
- LoRA: r=32, alpha=64, dropout=0.05
- Target modules: `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`
- Training corpus: BG-JE 214.30 MB anima-persona (kowiki 70%, NEXUS-UBM 25%, UBM 3%, outside-well 2%, eval-inject 0.3%)
- Steps: 6000 (final loss 1.49)
- Hardware: H100 80 GB (RunPod), elapsed 2930 s (≈49 min)
- Cost actual: $3.568 USD

## Verdicts (anima reborn cycle 2026-05-10)

- §43 V14 PASS direction confirmed (4-fire SIMPLE_STACK_PASS_STRICT replication on 3 B+ foundation)
- V4 multi-seed: 11/15 sample-anyseed pass, 10/15 strict floor (target greedy=5/15, strict_floor>=10/15) → PASS_STRICT
- V14 mirror: trained > random by mitosis-trigger-rate proxy (MTRP=0.733)
- Korean Hangul ratio: 0.534 (target >=0.5, PASS)
- Honest C3: semantic_score (char-trigram cosine proxy) 0.055 < 0.5 floor; bigram_known proxy 0.258 < 0.95 floor — both proxies known weak vs. sentence-transformer eval
- Mitosis hook (foundation-A substrate predict): trained phi mean 2.880, max cells 24; PERFECT MATCH 5/5 prediction (§48)

## Files

| name | size | role |
|---|---|---|
| `adapter_step_1500/` | 186 MB | LoRA checkpoint at step 1500 |
| `adapter_step_3000/` | 186 MB | LoRA checkpoint at step 3000 |
| `adapter_step_4500/` | 186 MB | LoRA checkpoint at step 4500 |
| `adapter_step_6000/` | 186 MB | LoRA checkpoint at step 6000 |
| `adapter_final/` | 186 MB + tokenizer | Final adapter + tokenizer |
| `verdict.md` | 16 KB | Cycle verdict markdown |
| `verdict.json` | 10 KB | Machine-readable verdict |
| `v14_mirror.json` | 5.6 KB | V14 trained-vs-random mirror eval |
| `v4_results_multiseed.jsonl` | 51 KB | V4 multi-seed pass-rate detail |

## How to use

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B")
tok = AutoTokenizer.from_pretrained("dancinlab/anima-foundation-borrow-a-llama32-3b-lora", subfolder="adapter_final")
model = PeftModel.from_pretrained(base, "dancinlab/anima-foundation-borrow-a-llama32-3b-lora", subfolder="adapter_final")

prompt = "[anima identity] anima는 누구야?"
out = model.generate(**tok(prompt, return_tensors="pt"), max_new_tokens=128, do_sample=True, temperature=0.7)
print(tok.decode(out[0], skip_special_tokens=True))
```

## Caveats

- Persona prefix is part of the training distribution; outputs without one of `[anima identity] `, `[anima NEXUS-UBM] `, or `[anima 우주뇌지도] ` may drift toward base Llama behaviour.
- Semantic-score and bigram-known floors are proxy metrics calibrated for the BG-JE eval set; do not interpret them as production-grade semantic evaluation.
- Falsifier F-FOUNDATION-5 (gradient-leak through frozen Llama) tested negative.

## Lineage

- `foundation_borrow_a_llama32_3b_lora_r32_bg_je_214mb` (lineage tag)
- Cycle: anima reborn 2026-05-10
- BG: BG-FOUNDATION-BORROW-A
- Verdict schema: anima_bg_verdict_v6
- Corpus: [`dancinlab/anima-je-corpus`](https://huggingface.co/datasets/dancinlab/anima-je-corpus)

## License

Inherits from `meta-llama/Llama-3.2-3B` (Llama 3.2 Community License). LoRA weights distributed under the same terms; persona adapter has no separately licensed weights.
