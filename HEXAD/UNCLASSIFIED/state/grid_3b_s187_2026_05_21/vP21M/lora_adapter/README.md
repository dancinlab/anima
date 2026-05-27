---
base_model: Qwen/Qwen2.5-1.5B
library_name: peft
tags:
  - lora
  - multilingual
  - qwen2.5
  - anima
language:
  - en
  - ko
  - zh
  - ru
  - ja
license: apache-2.0
---

# anima-vp21m — multilingual LoRA r32 for Qwen2.5-1.5B

Continue-trained LoRA adapter on top of `Qwen/Qwen2.5-1.5B`. Forked from
internal `vP21` baseline + 1500 steps on 5-language wiki + anima-corpus
mix. Produced 2026-05-22.

## Quick verdict

| lang | verdict | score/20 | gen | lang_coherent | notes |
|---|---|---|---|---|---|
| EN | STRONG | 18 | 18 | 20 | slight uplift over vP21G |
| KO | PARTIAL | 15 | 18 | 15 | sample-mode anima leak on 2 probes |
| ZH | STRONG | 16 | 20 | 16 | 0 memorize |
| RU | STRONG | 18 | 20 | 18 | 0 memorize, Cyrillic stable |
| JA | WEAK | 11 | 16 | 11 | sample-mode hallucination on 4 probes |

Aggregate: 3 STRONG + 1 PARTIAL + 1 WEAK + 0 PURE_MEMORIZE →
`VP21M_WORKS` (≥4 langs ≥ PARTIAL).

`register_regress=False` (anima register not over-fit).

## Training

| key | value |
|---|---|
| base | `Qwen/Qwen2.5-1.5B` |
| init adapter | vP21 LoRA r32 α64 (continue-train) |
| trainable | 36.93M (2.34% of 1.58B) |
| target modules | inferred from safetensors (Qwen attention + MLP projections) |
| steps | 1500 |
| bsz / block | 2 / 512 |
| LR | 5e-5 peak, cosine → 5e-6, warmup 50 |
| optimizer | PagedAdamW8bit (bnb 0.43.1) |
| dtype | bf16 |
| GPU | H100 80GB HBM3 SXM (runpod) |
| train wall | 198.8 s (3.3 min) |
| init CE → final CE | 1.7163 → 0.7787 (55% reduction) |

## Corpus

- 5-language wiki: `wikimedia/wikipedia` 20231101 snapshots (en/ko/zh/ru/ja),
  per-language native-script ratio filter (en ≥ 0.50, ko/zh/ru ≥ 0.20,
  ja ≥ 0.05). 19,337 records, 51.1 MB.
- anima-corpus s101 seed=1337 n=777000 (603 MB) — anima register +
  consciousness-substrate carving entries.
- Mix: 1 KB chunks interleaved with `wiki_frac=0.30`, global shuffle seed=42.
  Total 75.5 MB / 55,362 records.

## Eval

- Per-language OOD held-out: 10 probes × 5 langs × 2 modes (greedy + sample)
  = 100 generations.
- anima register Eval1: 10 anima-context probes × 2 modes = 20 generations.
- Multilingual classifier: anima-key detector (CJK/Cyrillic-aware) +
  `lang_coherent()` native-script ratio per lang.

## How to use

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B",
                                            torch_dtype="bfloat16")
tok  = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B")
model = PeftModel.from_pretrained(base, "dancinlab/anima-vp21m").eval()

ids = tok("The capital of Germany is", return_tensors="pt").input_ids
out = model.generate(ids, max_new_tokens=80, do_sample=True,
                     temperature=0.7, top_p=0.95, repetition_penalty=1.2)
print(tok.decode(out[0], skip_special_tokens=True))
```

## Limitations

- JA register: sample-mode hallucination on ~40% of probes — fix
  candidate: ja-only LoRA hot-swap (in progress).
- Anima register leak: 7/20 anima-context probes still echo training-set
  carving phrases. Use temperature 0.7 + context-grounded seeding.
- Single-shot LoRA r32 — no instruction tuning; raw completion only.

## Lineage

| step | what |
|---|---|
| vP21 | initial LoRA on EN wiki only |
| vP21G | EN STRONG (16/20) |
| vP21K | KO STRONG (continued from vP21G) |
| vP21M | this card — 5-lang merged on top of vP21 baseline |

Cost: $1.06 actual (cap $15).

## Provenance

- adapter sha256: `96c2b226cc1c85fe4f717d2898f2f5394657cd7f279b19fecd2575cd1821833e`
- corpus mix sha256: `bf2371ac2602932cd68255626736285a5e579e6aee4b8a0160f74f365d826f94`
- run dir: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21M/`

### Framework

- PEFT 0.12.0
- transformers 4.x
- bitsandbytes 0.43.1
