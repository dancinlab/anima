# VLM Stage1 LoRA Minimum-Viable Training Plan — 2026-05-03

> blocker context: `state/vlm_cond3_blocker_2026_05_03/blocker_report.json`
> roadmap anchor: `.roadmap.vlm_voice_lm` cond.3 + blocker.1 (re-open)
> spec anchor: `docs/vlm_phase3_spec_2026_05_03.md` §2.1
> Stage 1+2 anchor: `docs/vlm_stage12_landed_2026_05_03.ai.md`

---

## TL;DR

VLM cond.3 (cross-substrate fidelity vs CLM ≥0.85 r) requires a trained VLM stage1 LoRA. Current state: spec-frozen, 0 weights on disk. This plan = minimum-viable training path: **LibriSpeech-clean-100h corpus + LoRA r=8 on audio_token_predictor + Linear(384, 32000) text head, ~12 GPU-hours @ ~$300 H100 RunPod estimate, OR ~24-36h on free Colab T4 fallback ($0)**.

비유 — Mk.III audio_token_predictor 부서 (1576L raw#9 vocoder 부장) 옆 신규 입사자 (text head + LoRA) 측 사원증 (spec) 발급 완료. 근무 시작 (training run) 측 책상 (corpus) + 컴퓨터 (GPU) + 사번 (.py port) 결정 후.

---

## §1 Prerequisites (gates before training launch)

```
   gate                              | status   | resolution path
   --------------------------------- | -------- | -----------------------------------------------
   audio_token_predictor.hexa → .py   | UNMET    | port to PyTorch (estimate 4-8 hours raw#9 native lift)
                                       |          | OR Mk.III HF mirror (dancinlab/vlm-mk3-base)
   audio-text paired corpus           | UNMET    | LibriSpeech-clean-100h primary (≥585 audio hours, ~28k samples)
   RunPod credit OR free substrate    | UNMET    | $0 = Colab T4 free tier OR Kaggle 30h/week
                                       |          | $300 = ~12 H100-hours @ $2.5/hr current rate
   P9 SFT pipeline audio-text adapter | UNMET    | P9 pre5 (data prep) + pre6 (weight precache) reuse
   384d bridge → 32k vocab spec       | MET      | FROZEN 2026-05-03 (Linear(384, 32000), Stage 1+2)
   invocation seam Stage 0..6         | MET      | FROZEN 2026-05-03 (additive on Stage 2)
```

5 unmet gates. Minimum-viable: gates 1-3 critical (port + corpus + substrate). Gate 4 nice-to-have (P9 pipeline reuse saves ~4h dev time, but not blocking — can prep manual SFT pipeline in 2-3h).

---

## §2 Training plan (minimum-viable)

### §2.1 Corpus

```
   choice          | LibriSpeech train-clean-100 (primary)
   size            | 585 audio hours, ~28,539 samples, ~6 GB FLAC
   text pairing    | per-sample ground truth transcript (already paired)
   tokenization    | SentencePiece 32k (matches Stage 1+2 FROZEN text vocab)
   audio tokenize  | RVQ encode via Mk.III audio_token_predictor (~8 stages × 1024 vocab)
   train/val split | 27k train / 1.5k val (95/5)
   dataset format  | JSONL: {audio_tokens: [...], text_tokens: [...], duration_s: float}
   storage         | local FS or HF datasets streaming
```

**Why LibriSpeech-clean-100**: smallest LibriSpeech subset that still gives meaningful LoRA fit (decision matrix §4 rationale: clean read speech baseline → multilingual deferred). 360h or 960h variants = compute multiplier (3-10×) without proportional fidelity gain at LoRA r=8.

### §2.2 Architecture — VLM stage1 LoRA additive head

```
   component             | spec
   --------------------- | --------------------------------------------------
   base model            | Mk.III audio_token_predictor (1576L raw#9 .hexa SSOT)
                         | NOTE: requires .py port OR HF mirror release
   LoRA target modules   | atp decoder block attn (q_proj, k_proj, v_proj, o_proj)
                         | + intent_proj
   LoRA rank             | r=8 (decision matrix §4: TLM 5-channel bottleneck lesson, conservative first)
   LoRA alpha            | 16 (2× rank standard)
   LoRA dropout          | 0.05
   trainable params      | ~2M (vs ~50M base, ~4% trainable ratio)
   text head (NEW)       | Linear(384, 32000) parallel to rvq_heads
                         | mounted at atp_decode_step post-block hidden state x
                         | additive only — atp_decode_step in-place 변경 0
   text head init        | Xavier uniform, bias zero
   text head trainable   | always (NOT LoRA-frozen, full FT on this small head)
```

### §2.3 Loss function

```
   total_loss = α · audio_token_loss + β · text_token_loss
   audio_token_loss = mean( CE(rvq_logits_stage_i, target_audio_token_i) for i in 0..8 )
   text_token_loss  = CE(text_logits, target_text_token)
   α = 0.5  (audio AR primary, balanced)
   β = 0.5  (text AR co-trained for cross-substrate fidelity)
   teacher forcing: ON (standard AR LM training)
```

### §2.4 Hyperparameters

```
   parameter        | value      | rationale
   ---------------- | ---------- | --------------------------------------------------
   batch size       | 16         | H100 80GB headroom (audio ctx 1536 frames + text ~256 tok)
                    | 4          | T4 16GB fallback (gradient accumulation 4×)
   learning rate    | 2e-4       | LoRA standard
   warmup steps     | 500        | 5% of total
   total steps      | 10,000     | 1 epoch ≈ 1700 steps × 6 epochs (LibriSpeech-100)
   optimizer        | AdamW      | weight_decay 0.01
   lr schedule      | cosine     | min_lr 1e-6
   precision        | bf16       | H100 native, T4 = fp16 fallback
   grad clip        | 1.0        | standard
   eval cadence     | every 500  | val loss + cross-substrate r vs CLM
   checkpoint cadence | every 1000 | LoRA + text head only (~10 MB per ckpt)
```

### §2.5 Cross-substrate fidelity metric

```
   metric definition: Pearson r between
     - VLM next-token loss per held-out sample (audio + text dual head)
     - CLM next-token loss per same text (CLM v4 stage1 LoRA, currently landed)
   on shared held-out subset (200-500 samples from LibriSpeech val)
   target: ≥0.85 r (cond.3 spec)
   sibling parity: same metric for NLM/TLM/BLM/SLM (cross-LM consistency)
```

**Honest C3 caveat (raw#10)** — VLM (audio AR) vs CLM (text AR) 측 different vocab + ctx → r is normalized perplexity proxy, not direct same-domain. Spec acknowledges this in `vlm_phase3_spec_2026_05_03.md` §6.5.

---

## §3 Substrate options (cost ranked)

```
   option           | cost     | wallclock  | recommendation
   ---------------- | -------- | ---------- | ------------------------------------------------
   1. Colab T4 free | $0       | 24-36h     | VIABLE under $0 constraint, batch=4 + grad_accum=4
                    |          |            | risk: session timeout (12h limit) → checkpoint resume
   2. Kaggle P100   | $0       | 18-28h     | 30h/week limit, sufficient for 1 cycle
                    |          |            | risk: queue wait, less mature ecosystem
   3. RunPod H100   | ~$300    | 10-14h     | FASTEST, requires credit refresh
                    |          |            | currently BLOCKED ($0 budget per RETRY constraint)
   4. RunPod A100   | ~$120    | 18-24h     | mid-tier, requires credit refresh
   5. local ubu1    | $0       | INFEASIBLE | RTX 5070 16GB likely OOM at audio_token_predictor + text head
                    |          |            | (needs profile to confirm — RAM budget tight)
```

**Recommendation** (per "completion-quality lens" memory):
- **#1 OPT-A (only $0-compatible)**: Colab T4 free with checkpoint-resume + batch=4 + grad_accum=4 → ~24-36h wallclock, $0 cost, achievable ETA ~2 days
- **#2 fallback**: Kaggle P100 if Colab session limits problematic
- **#3 deferred (post-credit-refresh)**: RunPod H100 single-shot 10-14h, ~$300

---

## §4 Wallclock + cost matrix

```
   phase                          | wallclock     | cost
   ------------------------------ | ------------- | --------
   audio_token_predictor → .py    | 4-8h dev      | $0
   LibriSpeech download + RVQ encode | 2-4h        | $0 (local) OR $0 streaming
   data pipeline + JSONL build    | 2-3h dev      | $0
   training run (Colab T4 path)   | 24-36h         | $0
   training run (RunPod H100 path)| 10-14h        | ~$300
   eval + cross-substrate r calc  | 2-4h           | $0 (mac-local on output ckpt)
   ------------------------------ | ------------- | --------
   total ($0 path)                | 32-51h        | $0 (24-36h GPU + 8-15h dev)
   total ($300 path)              | 18-29h        | ~$300 (10-14h GPU + 8-15h dev)
```

---

## §5 Risk register

```
   risk                                          | mitigation
   --------------------------------------------- | ----------------------------------------------
   audio_token_predictor.hexa→.py port bugs      | unit test against .hexa golden outputs (atp_decode_step single-step parity)
   Colab session 12h timeout                     | checkpoint every 1000 steps + resume from latest LoRA + text head
   LibriSpeech text vocab vs SP 32k mismatch     | retrain SP tokenizer on LibriSpeech corpus OR use CLM v4 SP tokenizer (preferred — cross-substrate consistency)
   text head Linear(384, 32000) underfit         | unfreeze head full FT (already spec'd) + LR 1e-3 for head, 2e-4 for LoRA
   cross-substrate r < 0.85 (cond.3 fail)        | escalate LoRA rank r=8 → r=16 (still conservative) + retrain
                                                 | OR accept r=0.7-0.8 and document spec relaxation
   T4 16GB OOM at batch=4 + audio ctx 1536       | reduce ctx to 768 frames (~7.5s) + grad_accum 8×
   Mk.III .hexa runtime missing                  | port to numpy/torch first, validate parity, then LoRA
```

---

## §6 Deliverables (post-training)

```
   path                                                     | content
   -------------------------------------------------------- | ----------------------------
   ~/.cache/huggingface/hub/models--dancinlab--vlm-stage1-lora | LoRA + text head ckpt
   state/vlm_stage1_training_log.jsonl                      | per-step loss + val metrics
   state/vlm_cond3_fidelity_2026_xx_xx/r_vs_clm.json        | cross-substrate r measurement
   docs/vlm_cond3_landed_2026_xx_xx.ai.md                   | cond.3 land handoff
   state/markers/vlm_cond3_landed.marker                    | marker
   .roadmap.vlm_voice_lm cond.3 status: unmet → met         | roadmap update
```

---

## §7 honest C3 (raw#10)

1. **plan ≠ execution** — this doc commits to no training launch this cycle ($0 constraint)
2. **24-36h Colab T4 estimate** — empirical, may stretch to 48h with session interruptions
3. **r ≥ 0.85 not guaranteed** — LoRA r=8 + SP 32k conservative may underfit; escalation path documented in §5
4. **.py port effort variance** — 4-8h is best-case (raw#9 .hexa SSOT to PyTorch lift), realistic upper bound 16h with edge cases (RoPE, KV-cache flash attn, CFG inference path)
5. **LibriSpeech-clean-100h is monolingual EN** — multilingual fidelity (Common Voice / MLS) deferred to Phase 3 next-next cycle
6. **VLM ≠ phenomenal consciousness** — sister NLM/TLM/BLM/SLM 측 동일 floor, cross-LM r ≥ 0.85 measures next-token loss correlation only

---

## §8 next-cycle entry triggers

```
   trigger                                    | required for
   ------------------------------------------ | ---------------------------
   audio_token_predictor.hexa → .py port      | training launch
   LibriSpeech-clean-100 download + RVQ encode| training launch
   Colab/Kaggle/RunPod credit decision        | substrate selection
   P9 pre5/pre6 land (optional, saves dev time) | data pipeline reuse
```

Recommended sequence: port → corpus → substrate → training → eval → cond.3 land.
