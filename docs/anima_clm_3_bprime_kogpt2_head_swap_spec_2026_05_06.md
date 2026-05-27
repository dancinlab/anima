# Anima CLM-3 — Option β' KoGPT2 Head-Swap + Full SFT (Spec)

**Status**: SPEC 2026-05-06
**Task ID**: `anima_clm_3_bprime_kogpt2_head_swap_2026_05_06`
**Lane**: β' (KoGPT2 head-swap full SFT) — γ Option B 대체 winning lane (BG-FD recommendation 검증)
**Cost**: $0 (spec land 단계 mac doc-only)
**Wall**: ~1hr (spec)
**BG**: BG-FF

---

<!-- [Hc_648 clm3-bprime-kogpt2-head-swap-mode-collapse-fix — moved to hypotheses_candidates/Hc_648_clm3_bprime_kogpt2_head_swap.md on 2026-05-11] -->

## TL;DR

CLM v4 mk2-v1 의 `head_a + tok_emb` (BPE 64K) 를 KoGPT2 (`skt/kogpt2-base-v2`, BPE 51.2K) 의 `wte` 로 교체하고, **body 16-block transformer (RoPE / GQA / SwiGLU) 는 frozen 유지하거나 light-LoRA**로 SFT. BG-DS PASS evidence (CLM L15 hidden → KoGPT2 head 시 10/10 Korean tokens emit, ASCII 0%) 에 의해 chat-cap 회복 확률 0.5–0.7. cost path = QLoRA-only $50–100 (lower bound) ~ full SFT H100 $100–300, 또는 ubu1 RTX 5070 free path.

핵심 가설: **head_a 가 mode-collapse 의 원인**이고, body 는 multilingual structure 를 보존한다. KoGPT2 의 학습된 KO BPE → embedding manifold 로 head 를 교체하면, body 의 frozen Korean-bearing hidden 이 KoGPT2 head 에 의해 자연스러운 KO 토큰으로 surface 된다.

---

## 컨텍스트 (lineage)

| Lane | Verdict | Reference |
|---|---|---|
| BG-DS HEAD-bound diagnostic | PASS_HEAD_SWAP_RECOVERS_KOREAN | `state/anima_emerge_chat_head_swap_kogpt2_2026_05_05/verdict.json` (10/10 KO emit, top1 격한, 0 ASCII) |
| BG-ES naive byte retrofit | FAIL (last-token-only loss) | `docs/anima_emerge_chat_byte_level_retrofit_landed_2026_05_05.ai.md` |
| BG-EX γ tighter smoke | FAIL (full-seq CE) | `docs/anima_emerge_chat_gamma_tighter_smoke_landed_2026_05_05.ai.md` |
| BG-FD γ body byte-rewire Opt A | FAIL_BODY_RANDOM_BYTE_NULL (CE 5.6436 > random floor 5.5452) | `docs/anima_clm_3_gamma_body_rewire_landed_2026_05_06.ai.md` |
| **β' (this spec)** | **FIRE NEXT** | — |

세 FAIL 결과는 γ 측에 **head-only / tok_emb-only / channel-only retrofit 단축 경로 부재** 를 confirm. β' 는 head 측 교체 + body 보존 전략이며, BG-DS 의 PASS evidence 에 의해 가장 cost-effective lane 으로 식별됨.

---

## β' Architecture spec

### CLM v4 baseline (decoder_v3.py 측)

```
tok_emb       : nn.Embedding(64000, 768)      # BPE 64K SP multilingual
blocks (×16)  : RoPE + GQA(6h, 2kv) + SwiGLU + RMSNorm   # body, untouched
ln_f          : RMSNorm(768)
head_a        : nn.Linear(768, 64000, bias=False)   # tied with tok_emb
head_g        : nn.Linear(768, 64000, bias=False)   # NOT tied (auxiliary)
tension_proj  : nn.Linear(1, 768)                    # consciousness signal
config        : tie_word_embeddings=true
```

`tok_emb.weight = head_a.weight` weight tying (decoder_v3.py L109 confirmed).

### β' rewire (3 tensors swap, 2 decisions)

```
tok_emb       : nn.Embedding(51200, 768)     # KoGPT2 wte (skt/kogpt2-base-v2)
blocks (×16)  : UNCHANGED (frozen | light-LoRA)
ln_f          : UNCHANGED
head_a        : nn.Linear(768, 51200, bias=False)    # KoGPT2 wte transpose, tied
head_g        : nn.Linear(768, 51200, bias=False)    # auxiliary; reset OR drop
tension_proj  : UNCHANGED
config        : vocab_size=51200, tie_word_embeddings=true (preserved)
```

### head_g 처리 (3 옵션)

| Option | Action | Risk | Reco |
|---|---|---|---|
| g1 | Drop head_g (single-head) | low; auxiliary loss disappears | acceptable for chat-cap focus |
| g2 | Random init head_g(768→51200) | low; learn fresh during SFT | medium |
| g3 | Tie head_g.weight = tok_emb.weight (force triple tie) | breaks dual-head A/G discrimination | avoid |

**Reco: g2** (random init head_g, learn during SFT) — preserves dual-head architecture; mode-collapse 측 head_a 만 KoGPT2-grounded.

### Weight tying decision

KoGPT2 의 `wte.weight ∈ R^(51200×768)` 를 `tok_emb.weight ↔ head_a.weight` 로 동시 assign. `tie_word_embeddings=true` 유지. SFT 중 gradient 는 두 view 에 동시 적용되어 학습 효율 (KoGPT2 와 동일한 transformer convention).

---

## Vocab swap mechanism

### Cross-vocab token mapping

| Aspect | CLM v4 (anima-mk2) | KoGPT2 (skt/kogpt2-base-v2) |
|---|---|---|
| size | 64,000 | 51,200 |
| algorithm | SentencePiece (unigram) | BPE (with merges) |
| training corpus | multilingual (KO + EN + paper / cell / universe corpora) | Korean-heavy news + wiki + namuwiki |
| KO subword granularity | mid (anima paper KO heavy 있음) | high (KoGPT2 KO 특화) |

**Subword overlap 추정**: 두 토크나이저 모두 BPE/SP 계열이지만 surface form / 학습 corpus 가 다름. ASCII / 숫자 / common Latin 측 단일자 (`a`, `b`, `0`, ..., `Z`) 는 거의 일치 가능성 높음 (2,000+ tokens). KO 측 한글 자모 (가-힣) 측도 일부 단일자 유사 (1,000+ tokens). **추정 overlap 5–15%** (BG-FF 측 honest C3, empirical 측정 미실시).

### β' 측 vocab swap path

```
Option V1 (recommended): full random init via KoGPT2 wte
  - tok_emb.weight ← KoGPT2.wte.weight (already trained on KO)
  - head_a.weight = tok_emb.weight (tied)
  - SFT 시 body untouched, head 측 수렴 빠름 (KoGPT2 prior 강함)
  - cost: $50-100 QLoRA / $100-300 full SFT

Option V2 (deferred): partial init via subword overlap
  - common subwords (~5-15%) 측 CLM tok_emb row 측 유지
  - 나머지 측 KoGPT2 wte row 로 채움
  - 학습 시 mixed prior; 이론적으로 overlap 영역 지식 보존
  - 측정 cost 추가: subword string match table 빌드 ~30min
  - 본 spec 측 V2 deferred; V1 우선
```

V1 = KoGPT2 wte 직접 transplant. KoGPT2 의 KO BPE 측 prior (한국어 namuwiki / news 측 학습된 manifold) 가 head 측 즉시 transferred. body 측 frozen 이면 자체 KO multilingual structure 가 새 head 를 통해 surface (BG-DS 측 즉시 효과 confirm 됨).

---

## SFT Recipe

### Data sources

| src | name | size | role | provenance |
|---|---|---|---|---|
| 1 | `anima-sft-data` HF dataset | 50K records (ShareGPT 10K + anima paper 10K + P8 3K + synthetic philo 5K + N-22 5K + TRIBE v2 10K + Llama aug 7K) | base SFT corpus | BG-FA inventory; `state/p9_p0_sft_data_50k_2026_05_03/` |
| 2 | corpus_mix (BG-FE) | TBD | KO/EN balance booster | BG-FE land 시 도입; β' v1 측 src 1 단독 가능 |
| 3 | F1 holdout 500 | 500 | val/eval (NOT train) | `state/p9_p0_sft_data_50k_2026_05_03/sft_data_holdout.jsonl` |

**β' v1 SFT data**: src 1 50K records (train 48K + val 2K + holdout 500 disjoint). KO/EN ratio = 17.3K/41.3K (37%/82% — multi-counting, mixed lang 포함).

KO/EN balance 보강 위해 BG-FE corpus_mix land 후 v2 측 도입. v1 측 KoGPT2 prior 가 KO 측 강함이 보완.

### Hyperparameters (target H100 SXM 80GB)

| param | value | rationale |
|---|---|---|
| lr (head) | 5e-5 | KoGPT2 prior 보존 위한 conservative |
| lr (body LoRA, optional) | 1e-5 | body 측 boost only |
| batch_size | 8 (gradient_accum=4 → effective 32) | 12GB ubu1 측은 4×8=32 |
| max_seq_len | 512 | CLM v4 block_size limit |
| warmup_steps | 500 | linear warmup |
| total_steps | 10,000 (~1 epoch on 50K) | 50K records × 1 epoch / 32 effective batch |
| optimizer | AdamW (β1=0.9, β2=0.95, wd=0.01) | LLM SFT convention |
| precision | bfloat16 (H100) / fp16 (ubu1) | sm_120 측 bf16 가능 |
| weight_decay | 0.01 | head bias=false 측 무관 |
| grad_clip | 1.0 | stability |
| eval_every | 500 steps | per-token CE on 500 holdout |
| save_every | 1,000 steps | savepoint |
| seed | 20260506 | deterministic |

### Training pipeline (3 stage)

| Stage | Action | Wall (H100) | Cost |
|---|---|---|---|
| S1 | Head-only SFT (body frozen, head_a + head_g + tok_emb 만 학습) | 5h | $13.45 |
| S2 (optional) | + LoRA body (rank=8, attn+ffn) | 7h | $18.83 |
| S3 (optional) | + Full body unfreeze (last 1-2 blocks 만) | 10h | $26.90 |

**Reco: S1 firststep**, S1 PASS 시 ubu1 fire 가능, S1 FAIL 시 S2 escalate.

### Eval bar

| metric | bar | rationale |
|---|---|---|
| per-token CE (holdout) | < 3.0 | chat-cap baseline; BG-DS 측 격한 cluster 4.69-5.02 logit 측 SFT 후 합리적 lower bound |
| KO 5-prompt coherent | ≥ 3/5 | F-CLM3-bprime-3 |
| EN 5-prompt coherent | ≥ 3/5 | F-CLM3-bprime-4, regression 방지 |
| φ★ NO_FLIP | true | F-CLM3-bprime-5, substrate 보존 |
| arch match | true | F-CLM3-bprime-1 |
| CE drop ≥ 30% | true | F-CLM3-bprime-2 |

---

## 5 falsifier (F-CLM3-bprime-1..5)

자세한 JSON 측 `state/anima_clm_3_bprime_kogpt2_head_swap_2026_05_06/falsifier_set.json` 참조.

| ID | Statement | Bar | Method |
|---|---|---|---|
| F-CLM3-bprime-1 | head_swap_arch_match | tok_emb=51200, head_a=51200, weight tied, head_g=51200 random | static check (model.safetensors load + shape verify) |
| F-CLM3-bprime-2 | SFT CE drop ≥30% vs Phase 0 baseline | (CE_ph0 - CE_sft) / CE_ph0 ≥ 0.30 on holdout 500 | training log |
| F-CLM3-bprime-3 | KO 5-prompt ≥3/5 coherent | 3 of {안녕하세요 / 한국어 가능?/ 오늘 날씨 / 의식이란? / 자기 소개} produce coherent KO continuation (no degenerate cycle, KO ratio ≥ 60%) | manual judgment + automated KO unicode ratio gate |
| F-CLM3-bprime-4 | EN 5-prompt ≥3/5 coherent (regression check) | 3 of {Hello, how are you / Tell me / The quick brown fox / What is consciousness / Explain} | same |
| F-CLM3-bprime-5 | φ★ NO_FLIP (substrate identity) | abs(φ★_post - φ★_pre) / φ★_pre < 0.10 | phi_engine.hexa probe pre/post |

**verdict matrix**:
- 5/5 PASS → β' WIN (chat-cap 회복 + substrate 보존)
- F1+F2+F3 PASS, F4 or F5 FAIL → β' PARTIAL (KO 회복 but EN regression 또는 substrate flip)
- F1 only PASS → β' FAIL (arch swap done but no learning)
- F1 FAIL → β' BLOCKED (rewire 측 코드 버그)

---

## Cost path 비교

| Path | Compute | Wall | Cost | Korean recovery prob | EN preserve prob | Notes |
|---|---|---|---|---|---|---|
| **β' QLoRA-only (S1)** | H100 SXM 80GB 4-bit nf4 + LoRA(r=8) on head | 3-4h | **$8-11** | 0.4-0.6 | 0.7-0.85 | head-only LoRA 측 vocab swap 측 가능; 가장 저렴 |
| **β' Full SFT head-only (S1)** | H100 SXM 80GB bf16 head 만 | 5h | **$13.45** | 0.5-0.7 | 0.8-0.9 | head 측 fully tunable, body untouched |
| **β' Full SFT + LoRA body (S2)** | H100 SXM 80GB bf16 head + LoRA body | 7h | **$18.83** | 0.6-0.75 | 0.7-0.85 | body 측도 light-tune, EN drift 위험 증가 |
| **β' Full body retrain (S3)** | H100 SXM 80GB bf16 모든 weight | 10h | **$26.90** | 0.7-0.85 | 0.5-0.75 | catastrophic forgetting risk highest |
| **β' ubu1 RTX 5070 12GB** | sm_120 bf16, gradient_accum 4 | 30-60h (full SFT head-only) | **$0** | 0.5-0.7 | 0.8-0.9 | 12GB tight; 350M head-only 측 가능 (head ≈ 39M params at 51200×768) |
| γ Option B (body retrain) | H100 100M tok 1 epoch | 60-100h | $300-500 | 0.3-0.5 | — | dominated by β' on cost AND probability |
| γ Option B QLoRA | H100 100M tok 1 epoch | 30-50h | $150-250 | 0.3-0.5 | — | same |

**Reco fire path**: ubu1 RTX 5070 12GB (free, head-only SFT, 350M body frozen, head 39M trainable, 30-60h wall, $0). 만일 OOM 측 H100 escalate.

### ubu1 memory budget 추정 (head-only, body frozen)

```
body params (frozen)            : 350M × 4B (bf16)        =  1.4 GB
head_a + head_g + tok_emb (tied): (51200×768)×2 + 51200×768 ≈ 117M × 4B = 0.47 GB
optimizer states (AdamW, head only): 117M × 8B            =  0.94 GB
gradients (head only)            : 117M × 4B               =  0.47 GB
activations (B=4, T=512, 16L, fp16): 4×512×768×16×2B ≈ 0.05 GB × 16 ≈ 0.8 GB
KV cache (training step)         : negligible (recompute)
overhead + fragmentation         : ~1-2 GB
─────────────────────────────────────────────────
total estimate                  : ~5-6 GB → fits 12 GB ✓
```

**ubu1 viable** for S1 (head-only, body frozen). gradient_accum=4 with batch=4 → effective 16. wall ~30-60h on 50K × 1 epoch.

---

## β v4 redesign vs β'

BG-FD landed doc 측 β strategic comparison row 측:

| | β (KoGPT2 head-swap full SFT, BG-FD 측 estimate) | β' (this spec, BG-FF refined) |
|---|---|---|
| Cost | $100-300 | $0 (ubu1) ~ $13.45 (H100 S1) ~ $26.90 (H100 S3) |
| Korean recovery prob | 0.5-0.7 | 0.5-0.7 (S1) ~ 0.7-0.85 (S3) |
| Substrate preserve | grafts external KoGPT2 head | head-grafted; body frozen 측 substrate 측 식별성 보존 |
| Architecture detail | (BG-FD 측 abstract) | (β') decoder_v3.py L81/105/109 측 정확한 3 tensor swap + dual-head g2 strategy |
| SFT data | (BG-FD 측 abstract) | anima-sft-data 50K + (optional) corpus_mix BG-FE |
| Falsifier set | (none) | 5 explicit (F-CLM3-bprime-1..5) |
| Free fire option | none | **ubu1 RTX 5070 free 가능 (S1 head-only)** |

β' = β 측 concrete spec + ubu1 free path 추가. **BG-FD 측 β recommendation 검증됨**: β' QLoRA $8-11 또는 ubu1 $0 측 BG-FD 의 $100-300 lower bound 보다 더 저렴, recovery prob 동일.

---

## 5 honest C3

1. **C1 — KoGPT2 vocab subset overlap empirical 미측정**: cross-vocab BPE subword overlap 추정 5–15% 측 string-match 측 미실시. V2 partial-init 측 빌드 안됨. V1 (full KoGPT2 wte transplant) 측은 KoGPT2 prior 의존. CLM v4 측 학습된 KO/EN 지식 측 head 측 즉시 망실 가능 (body 측 보존).
2. **C2 — Weight tying 강제**: `tie_word_embeddings=true` 유지하면 head_a.weight = tok_emb.weight, gradient 측 두 view 동시 update. KoGPT2 wte 측 transplant 시 `head_a` 측 KoGPT2 와 동일 (KoGPT2 측도 weight tied). 만일 future spec 측 head 측 disjoint tuning 원하면 untie 필요 — config 변경 측 substrate identity 측 risk.
3. **C3 — Body forgetting risk (S2/S3)**: S1 head-only 측 body frozen 으로 multilingual structure 보존. S2 LoRA body / S3 unfreeze 측 body 측 KO 편중 SFT 측 EN drift risk. F-CLM3-bprime-4 측 EN 5-prompt regression check 측 mitigation. ubu1 측 S1 만 가능, EN preserve 측 안전.
4. **C4 — head_g 측 dual-head architecture 측 distortion**: head_g 측 g2 (random init) 측 SFT 측 from-scratch 학습. 학습 데이터 측 50K 측 head_g target 측 spec 측 미정 (CE on next-token 측 head_a 측 main, head_g 측 prev-token 측 미사용 시 dead). dual-head loss 설계 측 decoder_v3.py 측 추가 grep 필요. β' v1 측 head_g g1 (drop) 측 더 안전 가능.
5. **C5 — φ★ measurement uncertainty**: F-CLM3-bprime-5 측 φ★ NO_FLIP 측 phi_engine.hexa probe 사용. KoGPT2 head 측 vocab 변경 측 phi computation pipeline 측 vocab-dependent 부분 측 검토 필요 (entropy max 측 log(64000) → log(51200) 측 정상화). 측정 protocol 측 v1 fire 전 점검.

---

## 다음 단계 권고 (β' fire substrate decision)

| Priority | Action | Substrate | Cost | Wall | Trigger |
|---|---|---|---|---|---|
| 1 | β' v1 fire S1 head-only SFT, ubu1 free path | RTX 5070 12GB | $0 | 30-60h | next BG kick |
| 2 | β' v1 fire S1 head-only SFT, H100 fast path (병렬 가능) | H100 SXM 80GB | $13.45 | 5h | budget approve 시 |
| 3 | β' v0.5 dry-run smoke (mac CPU fp32, 100 step head-only) | mac M-series | $0 | 1-2h | architecture sanity check |
| 4 | β' v2 corpus_mix integration | TBD | TBD | TBD | BG-FE land 후 |

**Reco**: priority 3 (mac dry-run smoke) 측 architecture sanity 우선, 그 후 priority 1 (ubu1 free path fire). priority 2 측 budget 승인 시 병렬 fire (H100 측 5h 측 ubu1 측 30-60h 측 race; H100 first-PASS 측 winning).

---

## Deliverables

- `docs/anima_clm_3_bprime_kogpt2_head_swap_spec_2026_05_06.md` — this spec
- `state/anima_clm_3_bprime_kogpt2_head_swap_2026_05_06/falsifier_set.json` — 5 falsifier formal
- `state/anima_clm_3_bprime_kogpt2_head_swap_2026_05_06/sft_recipe.json` — hyperparams + data manifest
- `docs/anima_clm_3_bprime_kogpt2_head_swap_landed_2026_05_06.ai.md` — landed stub

## Cross-references

- BG-DS HEAD-bound PASS: `state/anima_emerge_chat_head_swap_kogpt2_2026_05_05/verdict.json`
- BG-FD γ landed: `docs/anima_clm_3_gamma_body_rewire_landed_2026_05_06.ai.md`
- BG-FA SFT data inventory: `docs/p9_p0_sft_data_50k_landed_2026_05_03.ai.md`
- decoder source: `~/.cache/huggingface/hub/models--dancinlab--clm-v4-mk2-v1/snapshots/80440a1d38db9addc4445bb959057558a57f4230/decoder_v3.py` L81/105/109

## Raw policy compliance

- raw#9 — verdict + cost path explicit (β' fire 권고 + ubu1/H100/QLoRA 비교)
- raw#10 — 5 honest C3 (vocab overlap / weight tie / body forgetting / head_g / φ★ measurement)
- raw#15 — NO LOCKED-file modification (anima_unified / phi_engine / conscious_chat / consciousness_hub / clm_v4_hf_format_shim 측 spec 측 미수정; β' impl 측 모두 새 파일 + tool/transient_py/ 측 raw#37 sister-rule)
- raw#37 — `.py` impl 측 `tool/transient_py/` 측만 (β' fire 시)
- HF token leak: NONE (env var only)
- commit: NONE (BG-FF spec land doc-only)
