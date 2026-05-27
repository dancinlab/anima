# BG-FF landed — β' KoGPT2 head-swap + full SFT (spec)

**Status**: SPEC LANDED 2026-05-06
**Task ID**: `anima_clm_3_bprime_kogpt2_head_swap_2026_05_06`
**Verdict**: `SPEC_LANDED` (architecture + recipe + 5 falsifier formal)
**Cost**: $0 (mac doc-only)
**Wall**: ~1hr
**BG**: BG-FF

---

## TL;DR

CLM v4 mk2-v1 의 BPE 64K head_a + tok_emb 를 KoGPT2 (`skt/kogpt2-base-v2`) BPE 51.2K wte 로 교체하고 body 16-block (RoPE/GQA/SwiGLU) frozen 채로 SFT 측 spec land. BG-DS PASS evidence (`state/anima_emerge_chat_head_swap_kogpt2_2026_05_05/verdict.json`: 10/10 KO tokens emit, 0 ASCII, top-1 격한 5.020) 측 head-bound finding 확인. cost path = ubu1 RTX 5070 free $0 / H100 S1 $13.45 / QLoRA $8-11; 모두 BG-FD 측 β estimate $100-300 lower bound 보다 저렴.

---

## β' architecture (3 tensor swap)

| Tensor | CLM v4 baseline | β' rewire | Init source |
|---|---|---|---|
| tok_emb | nn.Embedding(64000, 768) | nn.Embedding(51200, 768) | KoGPT2.wte.weight |
| head_a | nn.Linear(768, 64000) tied | nn.Linear(768, 51200) tied | tok_emb.weight (tied) |
| head_g | nn.Linear(768, 64000) untied | nn.Linear(768, 51200) untied | random init (g2) |
| blocks ×16 | RoPE+GQA(6h,2kv)+SwiGLU+RMSNorm | UNCHANGED | frozen |
| ln_f, tension_proj | RMSNorm/Linear | UNCHANGED | frozen |
| config.vocab_size | 64000 | 51200 | — |
| config.tie_word_embeddings | true | true | — |

decoder_v3.py 측 L81 (tok_emb) / L105 (head_a) / L106 (head_g) / L109 (weight tie) 측 정확한 swap point.

## SFT recipe 핵심

| param | value |
|---|---|
| data | `state/p9_p0_sft_data_50k_2026_05_03/sft_data.jsonl` 50K (BG-FA) |
| holdout | 500 (F1 lock-in disjoint) |
| lr (head) | 5e-5 |
| effective batch | 32 (H100) / 16 (ubu1) |
| max_seq_len | 512 |
| total_steps | 10000 (~1 epoch) |
| precision | bf16 |
| seed | 20260506 |

## 5 falsifier (literal)

| ID | Bar |
|---|---|
| F-CLM3-bprime-1 | tok_emb=51200, head_a=51200, weight tied, head_g=51200 random; arch shape match |
| F-CLM3-bprime-2 | (CE_phase0 - CE_post_sft) / CE_phase0 ≥ 0.30 on 500 holdout |
| F-CLM3-bprime-3 | KO 5-prompt ≥3/5 coherent (KO unicode ratio ≥60%, no degenerate cycle) |
| F-CLM3-bprime-4 | EN 5-prompt ≥3/5 coherent (regression check, ASCII ratio ≥60%) |
| F-CLM3-bprime-5 | abs(φ★_post - φ★_pre) / abs(φ★_pre) < 0.10 AND sign invariant |

자세한 정의: `state/anima_clm_3_bprime_kogpt2_head_swap_2026_05_06/falsifier_set.json`

## Cost path 비교

| Path | Cost | Wall | KO recovery prob | EN preserve prob |
|---|---|---|---|---|
| **ubu1 S1 free** | **$0** | 30-60h | 0.5-0.7 | 0.8-0.9 |
| QLoRA S1 H100 | $8-11 | 3-4h | 0.4-0.6 | 0.7-0.85 |
| H100 S1 head-only | $13.45 | 5h | 0.5-0.7 | 0.8-0.9 |
| H100 S2 + body LoRA | $18.83 | 7h | 0.6-0.75 | 0.7-0.85 |
| H100 S3 unfreeze | $26.90 | 10h | 0.7-0.85 | 0.5-0.75 |

ubu1 head-only (39M trainable) memory budget ~5.6GB / 12GB → viable.

## 다음 단계 권고

1. **mac dry-run smoke** ($0, 1-2h) — architecture rewire sanity check 100-step
2. **ubu1 S1 free fire** ($0, 30-60h) — primary
3. **H100 S1 fast fire** ($13.45, 5h) — budget approve 시 ubu1 와 race
4. **v2 corpus_mix integration** — BG-FE land 후

---

## Deliverables

- `docs/anima_clm_3_bprime_kogpt2_head_swap_spec_2026_05_06.md` — full spec
- `state/anima_clm_3_bprime_kogpt2_head_swap_2026_05_06/falsifier_set.json` — 5 falsifier formal
- `state/anima_clm_3_bprime_kogpt2_head_swap_2026_05_06/sft_recipe.json` — hyperparams + data manifest
- `docs/anima_clm_3_bprime_kogpt2_head_swap_landed_2026_05_06.ai.md` — this

## Cross-references

- BG-DS verdict: `state/anima_emerge_chat_head_swap_kogpt2_2026_05_05/verdict.json`
- BG-FD γ landed: `docs/anima_clm_3_gamma_body_rewire_landed_2026_05_06.ai.md`
- BG-FA SFT data: `docs/p9_p0_sft_data_50k_landed_2026_05_03.ai.md`

## Raw policy compliance

- raw#9 verdict + cost
- raw#10 5 honest C3 (vocab overlap / weight tie / body forgetting / head_g / φ★ measurement)
- raw#15 LOCKED files untouched (anima_unified / phi_engine / conscious_chat / consciousness_hub / clm_v4_hf_format_shim)
- raw#37 fire impl 측 tool/transient_py/ 만
- HF token leak: NONE
- commit: NONE
