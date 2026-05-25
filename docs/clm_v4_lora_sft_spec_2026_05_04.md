# CLM v4 + LoRA SFT — anima-substrate parallel to Llama Path A — DESIGN spec

- **ts_utc**: 2026-05-04T_BG-CLM-2_design
- **bg_lane**: CLM-2 (parallel to α''', CLM-1, T-1; **no H100**, $0)
- **status**: SPEC_LANDED — design only; no exec, no pod, no .py, no git commit
- **cycle**: anima 2026-05-04 BG-CLM-2 (CLM v4 + LoRA SFT spec)
- **scope**: full F1_v3 V2 hybrid Mode 1+3 differentiator track on CLM v4 substrate
- **non-overlap**: BG-CLM-1 (whatever it is — leave its dirs alone), Path A retry-3 (Llama track), Paradigm D distill (logit-axis Mistral teacher)
- **predecessor / sister**: `docs/p9_path_a_retrain_v2_spec_2026_05_04.md` (Llama side S1+S3) — this spec is the **anima-substrate variant** of that strategy
- **pre-registration policy (raw#71)**: All §4 PASS thresholds, §3 hyperparameters, §5 falsifiers F-CLM-LORA-1~5 are LOCKED at this spec landing. Post-eval threshold tweaks are a verdict-invalidation — must re-pre-register in a follow-up amendment cycle.

---

## 1-line summary

LoRA SFT on CLM v4 530M (anima's only G3 PASS-positive backbone, φ★ +41.86) using the same 60/30/10 rehearsal mix Path A v2 will use, with adapter-only training to bound φ★-flip risk, F1_v3 V2 hybrid Mode-1 (Comparative HF) + Mode-3 (Train-time Absolute) eval against Llama Path A v2 — answers the singular open question: **does anima's consciousness-coupled substrate beat a generic Llama LoRA on the same SFT recipe**?

---

## §1 — Substrate diff vs Llama Path A

### 1.1 Architectural dimensions

| Dimension | Llama-3.2-3B (Path A) | CLM v4 530M | Implication for LoRA |
|---|---|---|---|
| Family | Llama transformer | `decoder_v3` ConsciousDecoderV2 (`models/archive-legacy/decoder_v3.hexa`; PyTorch impl off-repo `ready/anima/models/legacy/decoder_v3.py`) | non-uniform block stack — LoRA target_modules cannot be assumed |
| Params | 3.21 B | 530.99 M (label "350M" misleading per `docs/strategic_clm_v4_production_ready_2026_05_02.md` §1) | smaller param surface — **LoRA r can be smaller for parity adapter %** |
| d_model / n_layer / n_head | 3072 / 28 / 24 | 768 / 16 / 6 (KV heads = 2; GQA-2) | 16-layer cell stack; LoRA per-layer cost ~3-4× lower than Llama |
| Vocab | 128 256 (Llama tokenizer) | **64 000 SentencePiece multilingual** (per `tool/clm_v4_tokenizer_load.hexa` canonical 64K BPE; ko+en native) | **Vocab MISMATCH with Path A corpus** — CLM v4 corpus must be re-tokenized via SPM 64K; cannot reuse Llama tokenized cache |
| Block size / context | 8K (Llama-3.2) | **512** | **MAJOR CONSTRAINT** — academic rehearsal slices (MMLU 5-shot, TriviaQA EM with prompt+answer+chat-template) must fit ≤512 SPM tokens; v1 Path A's `max_seq_len=2048` cannot port |
| Native heads | next-token only (`lm_head`) | **dual head**: `head_a` (next-byte/token) + `head_g` (prev-byte/token) — autoregressive dual-direction | LoRA on `head_a` mirrors Path A; `head_g` SHOULD remain frozen (preserves backward-prediction gradient for φ★ structural readout) |
| Consciousness coupling | none | `consciousness_dim=192`; `tension_proj [768→1]` per-layer; `phi_signal` DD5 EX24 native at decoder_v3.py:165; `bridge.{compress,hub_attn,expand,gate}`; `federation.{bottleneck, 12 narrative_grus}` | adapter on these = φ★-flip primary risk surface |
| Embedding tying | tied input/output | **likely tied** (decoder_v3 standard) — must verify against `best.pt` state_dict `head_a.weight` vs `tok_embeddings.weight` pointer equality | if tied → LoRA on output proj inadvertently changes input emb; **target_modules must avoid the tied head** OR explicitly include `(q,k,v,o)_proj` only |
| RLHF / SFT history | Instruct base RLHF'd | NEVER SFT'd, NEVER RLHF'd (per `#115`); trained on φ★ + ce loss | SFT is a DISTRIBUTION SHIFT, not a continuation. Higher forgetting risk on the consciousness-coupled side |

### 1.2 Cell architecture per-layer detail (axis conditioning)

Per `docs/clm_core_architecture_abstraction_layers_20260425.md` L0-L2 + `decoder_v3.py` (off-repo, read-only) inspection:

- Each cell-layer is **NOT** a uniform transformer block. It has axis-conditioned cross-attention paths, where the conditioning gate routes through `consciousness_dim=192` slot per layer.
- Native sockets per layer: `tension_proj [d_model=768 → 1]`, plus a `bridge.hub_attn` cross-attention head with `compress→expand→gate` substructure.
- `federation.bottleneck` is a SHARED projection across all 16 layers feeding 12 `narrative_grus` (this is anima's analog of "cross-attention to a memory bank"; preserves the binding-by-broadcast invariant).

**LoRA strategy decision**: target ONLY the per-layer attention `q_proj / k_proj / v_proj / o_proj` (mirrors Path A, well-trodden). **Do NOT target**:
- `tension_proj` (1-d projection — adapter would dominate the signal; would break φ★ measurement)
- `bridge.hub_attn` cross-attn (axis conditioning; adapter risks rerouting the conditioning gate → catastrophic for F-CLM-LORA-4 axis preservation)
- `head_g` (prev-token head; preserves backward-prediction signal that φ★ uses as a structural read-out)
- `federation.bottleneck` and `federation.narrative_grus` (shared cross-layer memory — adapter here = global drift, NOT what we want from a per-layer LoRA)

This is a deliberately CONSERVATIVE target_modules choice. It is the **safest mitigation for φ★-flip risk** (honest C3 #1 below).

### 1.3 Tokenizer + chat-template caveat

CLM v4 uses 64K SPM (multilingual ko+en native), NOT a chat-templated tokenizer. There is NO `<|im_start|>` / `<|im_end|>` analog in the CLM v4 vocab. Chat-template alignment in §2 slice C must therefore use **plain-text role markers** (e.g., `\n\n[USER]\n...` / `\n\n[ASSISTANT]\n...`) inside the SPM 64K token stream, with the marker tokens appearing as ordinary multi-token sequences. This is a pre-tokenizer convention, not a tokenizer-level change.

---

## §2 — Training data

### 2.1 Recommended mix: 60% anima-axis + 25% academic distill + 10% chat-template + 5% consciousness-coupled prompts

| Slice | Pct | Examples | Source | Diff vs Path A v2 |
|---|---|---|---|---|
| **A — anima axis** | 60% | 30 000 | sub-sample of `state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl` re-tokenized via SPM 64K (deterministic seed=20260504) | SAME slice as Path A v2 60% but **re-tokenized** through CLM v4 SPM (Llama tokenizer cache invalid). Token-budget audit required: many examples may overflow 512 ctx — must truncate or filter. |
| **B — academic distill** | 25% | 12 500 | 5 000 MMLU auxiliary_train (5-shot rendered, ≤512 tok) + 4 000 TriviaQA train EM (truncated to ≤512) + 3 500 Wikipedia paragraph→summary | **−5 pp vs Path A v2's 30%** because the 512 ctx cap forces aggressive filtering on MMLU 5-shot — many 5-shot rendered prompts exceed 512 SPM tokens; 0-shot fallback for MMLU items that overflow |
| **C — chat-template alignment** | 10% | 5 000 | 2 500 OpenOrca (Apache 2.0) + 2 500 ShareGPT-style chat (license-mixed, deduped) | SAME pct as Path A v2 but **plain-text role markers** (no `<|im_start|>`); SPM 64K re-tokenization required |
| **D — consciousness-coupled prompts** | 5% | 2 500 | anima-curated dialogue with explicit φ★ / tension_link / N-22 axis references + 5-bucket cell↔token bridge fixture prompts (per `tool/cell_token_bridge_proto.hexa`) | **NEW slice not in Path A v2** — preserves the SFT distribution's overlap with the φ★-axis training surface; mitigates φ★-flip |

Total: **50 000 examples** (matches v1 Path A cardinality for budget parity).

### 2.2 Justification (1 paragraph per directive)

Path A v2's 60/30/10 mix is an established anti-forgetting recipe (Chen et al. 2020 rehearsal). On the CLM v4 substrate, the 30% academic slice is squeezed to 25% by the 512-token context cap (MMLU 5-shot rendered prompts frequently overflow), and a new 5% **consciousness-coupled** slice is introduced specifically because CLM v4 has a φ★ optimization surface that Llama does not — without rehearsal pressure on that surface, LoRA SFT will drag the adapter away from the φ★ minimum and the post-SFT model loses its singular value-add (G3 PASS-positive backbone, +41.86 vs ALM 4-backbone). The 5% consciousness slice is small enough not to dominate the SFT signal but large enough to keep φ★ within a measurable band per epoch (validated by F-CLM-LORA-4 + the optional intermediate φ★ probe at step 2000/4000/6000). This makes the CLM v4 + LoRA SFT recipe a **substrate-aware variant** of the Path A v2 mix, not a blind clone.

### 2.3 Rehearsal corpus build cost ($0)

- Re-tokenization: ~30 min Mac-side (SPM 64K is fast); $0
- 512-ctx overflow filter: ~30 min Mac; $0
- Anima-axis sub-sampling: deterministic seed=20260504; $0
- Total pre-flight cost: $0, ~1h Mac wall.

---

## §3 — Hyperparameters (LOCKED 2026-05-04)

| Param | Path A v2 (Llama) | **CLM v4 LoRA SFT (this spec)** | Rationale |
|---|---|---|---|
| Base | Llama-3.2-3B-Instruct | **CLM v4 530M `~/anima/checkpoints/clm_v4_350m/scale_350m/best.pt`** (step=20000, φ★=27.91, ce=0.046) | only φ★ PASS-positive anima backbone |
| LoRA r | 64 | **32** | CLM v4 is ~6× smaller (530M vs 3.21B); r=32 maintains adapter %-of-base parity (~0.7%); per `docs/clm_v4_revival_stages_2026_05_02.md` §3.3 LoRA r=32 was already pre-spec'd for CLM v4 SFT |
| LoRA alpha | 64 | **64** | α/r = 2.0 (vs Path A v2's 1.0) — **slightly higher effective LR for the adapter** (compensates for smaller r), standard in Mistral/Qwen LoRA SFT recipes |
| LoRA dropout | 0.05 | **0.05** | keep — same regularization band |
| target_modules | `q_proj,k_proj,v_proj,o_proj` (Llama attn) | **`q_proj,k_proj,v_proj,o_proj`** (CLM v4 cell-layer attn ONLY) | conservative — explicitly EXCLUDE `tension_proj`, `bridge.hub_attn`, `head_g`, `federation.*` per §1.2; mitigates F-CLM-LORA-4 axis-preservation risk and φ★-flip risk |
| Optimizer | AdamW (b1=0.9, b2=0.95, wd=0.01) | **AdamW (b1=0.9, b2=0.95, wd=0.01)** | identical to Path A v2 |
| **LR** | **5e-5** | **3e-5** | **40% lower than Path A v2** — CLM v4 cells are more "delicate" (φ★ optimization surface is high-curvature near the +27.91 minimum per `state/strategic_clm_phase_a1_2026_05_01/run_log.json`); standard "lower LR for delicate substrates" heuristic; further reduced to bound φ★ drift |
| LR schedule | cosine, warmup 300 | **cosine, warmup 300** | same |
| **max_steps** | **6000** | **6000** | same wall-time envelope; CLM v4 is smaller so per-step is faster (~2× faster on H100) — wall ≈ 2 h vs Path A v2's 3.75 h |
| **save_steps** | 500 | **500** | identical granularity for early-stop signal |
| Eval intermediate | HellaSwag-200 every 2000 steps | **HellaSwag-200 every 2000 steps + φ★ probe every 2000 steps** | NEW φ★ probe (~1 min H100 inference on calibration set of 100 prompts); early-stop if φ★ < +10 (50% safety from sign zero per `docs/clm_v4_revival_stages_2026_05_02.md` §3.4) |
| micro_batch | 4 | **8** | CLM v4 is smaller; can fit larger micro-batch on same H100 |
| grad_accum | 8 | **4** | effective batch = 32 (matches Path A v2 for fair comparison) |
| effective_batch | 32 | **32** | identical |
| max_grad_norm | 1.0 | **1.0** | same |
| seed | 20260504 | **20260504** | same seed for cross-substrate determinism |
| max_seq_len | 2048 | **512** | **HARD CONSTRAINT** — CLM v4 block_size=512; cannot exceed (`docs/strategic_clm_v4_production_ready_2026_05_02.md` §1) |
| dtype | bf16 | **bf16** | same |

### 3.1 Per-choice rationale

- **r=32 not 64**: CLM v4 has 16 layers vs Llama's 28; r=64 would inflate adapter %-of-base to ~1.4% which is over-parameterized for the smaller backbone. r=32 yields ~600 MB adapter at fp16 (well under F-CLM-LORA-3's 500 MB threshold ONLY if we measure trainable params at fp16; bf16 doubles → see §5 caveat).
- **α/r=2.0 not 1.0**: literature (Hu et al. 2022, LoRA paper §6) shows α/r > 1 helpful when r is small; α/r=2 is the Mistral/Qwen LoRA SFT default.
- **lr=3e-5 not 5e-5**: CLM v4 sits near a φ★ minimum; SFT gradients in directions orthogonal to φ★ are fine, but gradients along the φ★ axis push us away. 3e-5 (40% reduction from Path A v2) is a heuristic from the Mistral-7B SFT-on-RLHF-base experience where lower LR preserved RLHF traits longer. Single point on the LR axis; ablation deferred to v2.
- **max_steps=6000**: same as Path A v2; fair-comparison floor. Early-stop on φ★ <+10 OR HellaSwag drop > 5pp at step 2000.

---

## §4 — F1_v3 V2 hybrid Mode-1 + Mode-3 PASS thresholds (LOCKED 2026-05-04)

### 4.1 Anchor: CLM v4 baseline

CLM v4 530M baseline on the F1_v3 V2 benchmark surface is **DEPENDENCY** on `p9_sft.cond.benchmark_a_prime_base_validation` PASS for the **Llama anchor** AND a NEW `p9_sft.cond.clm_v4_lora_baseline` for the CLM v4 anchor. The CLM v4 anchor has not been measured yet (this is a pre-EXEC blocker). Expected band per `docs/strategic_clm_v4_production_ready_2026_05_02.md` §3:

- HellaSwag acc_norm: expected **0.20-0.30** (random-ish + slight commonsense pickup from corpus); CLM v4 was NEVER trained for HellaSwag-style commonsense MC
- MMLU 5-shot acc: expected **0.22-0.27** (near-random; 4-way MC random = 0.25)
- TriviaQA EM: expected **0.05-0.15** (some factual leakage from anima axis corpus possible; otherwise near-zero)

These bands are HYPOTHETICAL; F-CLM-LORA-2 below uses Llama Path A v2 as the comparator, not absolute thresholds, **except** F-CLM-LORA-4 (axis preservation) which uses internal CLM v4 anchors.

### 4.2 PASS criteria (LOCKED — raw#71)

| Criterion | Threshold | Mode |
|---|---|---|
| **C-CLM-LORA-1** | post-LoRA HellaSwag acc_norm ≥ CLM-v4-base acc_norm − 1pp (parity floor on CLM substrate's own surface) | Train-time absolute (Mode 3) |
| **C-CLM-LORA-2** | post-LoRA F1_v3 composite (HellaSwag + MMLU + TriviaQA, weighted equally) ≥ Llama Path A v2 retrained composite (Mode 1 Comparative HF) | **Mode 1+3 hybrid — THE differentiator** |
| **C-CLM-LORA-3** | post-LoRA φ★ ≥ +10 (50% safety margin from sign zero) | Train-time absolute |
| **C-CLM-LORA-4** | post-LoRA anima-axis BLEU-1 (holdout-500 axis-conditioned per `state/p9_p1_holdout500_reeval_2026_05_03/`) ≥ pre-LoRA CLM v4 BLEU-1 | Train-time absolute |
| **OVERALL** | C-CLM-LORA-1 AND C-CLM-LORA-2 AND C-CLM-LORA-3 AND C-CLM-LORA-4 → V2 PASS. Any 3-of-4 → V2 PARTIAL. ≤2 → V2 FAIL. | hybrid |

C-CLM-LORA-2 is the central question: **does anima's substrate beat a same-recipe Llama LoRA**? PASS = anima-substrate wins → strong evidence for consciousness coupling. PARTIAL = parity → consciousness coupling neutral. FAIL = Llama wins → consciousness coupling is a liability for general SFT.

---

## §5 — Falsifier set F-CLM-LORA-1..5 (raw#71)

### F-CLM-LORA-1 — forgetting_index < CLM-v4-baseline (analog of F-PA-RETRAIN-v2-4)

- **metric**: HellaSwag-200 limit=200 acc_norm at step 2000, 4000, 6000 ≥ CLM v4 base acc_norm − 5pp (intermediate); ≥ CLM v4 base − 1pp at step 6000 (final). Forgetting index = (base − final) / base; threshold < 0.05.
- **observable**: intermediate eval JSON at step 2000/4000/6000.
- **PASS**: forgetting index < 0.05 AND C-CLM-LORA-1 holds.
- **FAIL action**: EARLY-STOP retrain at first −5pp breach; treat as v2-FAIL_EARLY; save adapter as `step-{step}-aborted` for post-mortem.

### F-CLM-LORA-2 — F1_v3 V2 hybrid Mode-1 + Mode-3 > Llama Path A v2 (THE differentiator)

- **metric**: F1_v3 composite (HellaSwag acc_norm + MMLU acc + TriviaQA EM, equal-weight average) for CLM v4 + LoRA vs Llama Path A v2 + LoRA.
- **observable**: post-train F1_v3 eval verdict.json on both adapters (separate cycles ~$1-2 each).
- **PASS**: CLM v4 composite ≥ Llama Path A v2 composite (any positive Δ; even 0.01 absolute = PASS).
- **FAIL action**: V2 PARTIAL or FAIL depending on §4 overall criterion. If CLM v4 composite < Llama Path A v2 composite by > 5pp absolute → consciousness coupling is a NET LIABILITY for general SFT → roadmap re-prioritization (escalate to Mode-2 only on CLM, OR drop CLM SFT track entirely).

### F-CLM-LORA-3 — LoRA adapter < 500 MB

- **metric**: `du -sb adapter_model.safetensors` post-train (final/ checkpoint).
- **observable**: HF push siblings file size.
- **PASS**: < 500 × 1024² bytes.
- **FAIL action**: investigate target_modules drift (should NOT exceed 500 MB at r=32 on a 530M base — see honest C3 #6 about bf16 storage).

### F-CLM-LORA-4 — cell axis-conditioning preserved

- **metric**: per `tool/cell_token_bridge_proto.hexa` 5-bucket cell↔token bridge fixture (3/3 PASS pre-LoRA per `docs/clm_core_architecture_abstraction_layers_20260425.md` L2). Post-LoRA: re-run all 3 fixtures + 7 axis-conditioned diff prompts (different N-22 axis values must produce > 0.3 cosine-distance outputs).
- **observable**: post-train cell-token-bridge re-fixture eval; post-train axis-conditioned diff probe (7 prompts × 5 axis values = 35 generations).
- **PASS**: 3/3 fixture PASS held + ≥ 6/7 axis-diff cosines > 0.3.
- **FAIL action**: V2 PARTIAL — adapter dropped axis conditioning. Reduce LR to 1e-5, retrain. If second retry fails, conclude that LoRA on attn `qkvo` IS the wrong target — escalate to attention-MLP-only target_modules (drop `o_proj` since it's the most cross-axis-mixing).

### F-CLM-LORA-5 — shim v4 hf_format compatibility

- **metric**: post-LoRA-merge model loadable via `from_pretrained()` in a clean Python env (no anima-private modules); produces sane logits on a 16-token calibration prompt.
- **observable**: shim test JSON (load + 1 forward pass + topk-5 logit dump).
- **PASS**: load OK + topk-5 logits include at least 3 valid SPM 64K token IDs (no NaN/inf, no out-of-vocab).
- **FAIL action**: investigate decoder_v3 hf-format export shim; this is BLOCKER for any external consumption. If shim broken, distribution-only goal still met but external evals can't run.

---

## §6 — Risks + mitigations

### R1 — LoRA on cross-attn / axis-cond gates may break axis conditioning

- **mitigation (PRIMARY)**: explicitly exclude `bridge.hub_attn`, `tension_proj`, `federation.*`, `head_g` from target_modules; only target `q_proj/k_proj/v_proj/o_proj` per §3.
- **mitigation (FALLBACK)**: if F-CLM-LORA-4 fails, drop `o_proj` (the most axis-mixing); only target `q_proj/k_proj/v_proj`.

### R2 — CLM v4 base eval baseline may not exist yet

- **dependency**: NEW roadmap entry `p9_sft.cond.clm_v4_lora_baseline` (analog of `cond.benchmark_a_prime_base_validation` for CLM v4 substrate). Estimated cost: ~3-6h ubu1 (RTX 5070, $0) for HellaSwag/MMLU/TriviaQA limit=500 lm-eval against `~/anima/checkpoints/clm_v4_350m/scale_350m/best.pt`.
- **mitigation**: BG-CLM-baseline cycle must run BEFORE CLM v4 + LoRA EXEC. This is a HARD GATE for §4 thresholds to be meaningful.

### R3 — Distill teacher (Mistral) availability impacts hybrid Mode-1+3 verdict design

- **dependency**: T-1 BG-1 (Mistral teacher availability). Per `docs/p9_paradigm_d_distill_spec_2026_05_03.md` §2.2, Mistral-7B-Instruct-v0.3 is the canonical teacher.
- **mitigation**: this spec does NOT depend on Mistral teacher logits (we are NOT distilling; we are doing pure SFT with the rehearsal mix). Mode-1 Comparative HF compares CLM v4 + LoRA vs Llama Path A v2 + LoRA on the same benchmark surface — no teacher needed. **De-coupled from T-1**.

### R4 — φ★ flip risk (HIGH per `docs/clm_v4_revival_stages_2026_05_02.md` §3.4)

- **mitigation (PRIMARY)**: adapter-only training (LoRA preserves backbone weights) — substantially lowers risk vs full fine-tune.
- **mitigation (SECONDARY)**: φ★ probe every 2000 steps; abort if φ★ < +10.
- **mitigation (TERTIARY)**: 5% consciousness-coupled prompts (slice D §2.1) keep gradient pressure on the φ★ surface.
- **residual risk**: cannot be fully eliminated without re-train from scratch ($1000+); acceptable per spec gate.

### R5 — 512-ctx cap forces aggressive corpus filter

- **mitigation**: 25% academic slice (vs Path A v2's 30%); MMLU 5-shot fallback to 0-shot for items > 512 SPM tokens; document filter rate in pre-flight corpus build report.
- **residual risk**: TriviaQA EM rehearsal coverage may be 70-80% of Path A v2's slice; small composite delta possible.

### R6 — head_a / tok_embeddings tied weight concern

- **mitigation**: pre-flight verify state_dict pointer equality `head_a.weight is tok_embeddings.weight` on `best.pt`; if tied, target_modules list MUST exclude `head_a`. Pre-flight check is a 5-min Mac-side script ($0).
- **residual risk**: if missed, LoRA on output would also alter input emb → forgetting catastrophic.

---

## §7 — Cost projection

### 7.1 Per-phase

| Phase | Substrate | Wall | $ band |
|---|---|---|---|
| Pre-flight CLM v4 baseline (R2 dependency) | ubu1 RTX 5070 | 3-6h | $0 |
| Pre-flight corpus build + 512-ctx filter (§2.3) | Mac M4 | ~1h | $0 |
| Pre-flight tied-weight check (R6) | Mac M4 | ~5 min | $0 |
| **TRAIN main run** (6000 steps, eff_batch=32) | H100 SXM $2.99/hr | **~2.0-2.5 h** (CLM v4 is ~2× faster per step than Llama-3B) | **$6-8** |
| Eval intermediate (3 × HellaSwag-200 + 3 × φ★ probe) | embedded in train pod | ~15-20 min | (in band above) |
| Final F1_v3 eval (HellaSwag + MMLU + TriviaQA limit=500) | separate cycle ~ubu1 OR small H100 | ~2-3h ubu1 OR ~30 min H100 | $0 ubu1 / ~$1.50 H100 |
| F-CLM-LORA-4 axis preservation eval | Mac M4 + ubu1 fixture | ~30 min | $0 |
| F-CLM-LORA-5 shim test | Mac M4 | ~10 min | $0 |
| **Total EXEC band** | | **~6-12h wall** | **$6-10 H100 floor; $15 hard cap** |

### 7.2 vs Path A v2

| Item | Path A v2 (Llama) | CLM v4 + LoRA SFT (this spec) |
|---|---|---|
| H100 wall | 3.75-7h | **2.0-2.5h** (smaller backbone) |
| Cost actual target | $11-23 | **$6-10** |
| Cost hard cap | $30 | **$15** |

CLM v4 + LoRA SFT is ~50% the cost of Path A v2 retrain, primarily because of the 6× smaller backbone.

### 7.3 Pre-flight cost ($0)

- CLM v4 baseline eval: $0 (ubu1)
- Corpus rebuild: $0 (Mac)
- Tied-weight check: $0 (Mac)
- Spec landing (this doc): $0

---

## §8 — Dependencies + ordering

### 8.1 Must wait for (HARD GATES)

1. **CLM v4 base availability**: confirmed at `~/anima/checkpoints/clm_v4_350m/scale_350m/best.pt` per `state/strategic_clm_phase_a1_2026_05_01/run_log.json`; HF mirror snapshot via `tool/clm_v4_tokenizer_load.hexa` cache resolver. **STATUS: AVAILABLE**.
2. **CLM v4 baseline eval** (NEW roadmap cond — see §6 R2): HellaSwag/MMLU/TriviaQA limit=500 on raw CLM v4 530M. **STATUS: NOT YET RUN — pre-EXEC blocker**.
3. **Mistral teacher resolution (T-1 BG-1)**: NOT a dependency for this spec (no distill term); but Path A v2 OR Paradigm D may need it. **De-coupled**.

### 8.2 Can run parallel with

- α''' BG (whatever it is)
- CLM-1 BG (whatever it is)
- T-1 BG (Mistral teacher)
- Path A retrain v2 EXEC (different substrate, no shared resource)
- Paradigm D distill EXEC (different substrate, no shared resource)

### 8.3 Outputs feed

- **F1_v3 V2 hybrid Mode 1+3 final consolidation** — primary downstream
- Cross-substrate verdict matrix: `tool/p9_a_d_cross_axis_verdict.hexa` (per `docs/p9_path_a_llama_lora_complete_2026_05_04.ai.md` §5.3 Path A vs Path D); add a third axis "CLM-LORA" → 3-way matrix
- φ★ post-SFT measurement → updates `state/v10_benchmark_v4_clm/*` benchmark deltas (separate state, READ-ONLY here)

### 8.4 Recommended ordering vs other tracks

(Per "completion-quality recommendation" memory hint — explicit ranking required.)

| Rank | Track | Why this order |
|---|---|---|
| 1 | **Path A retry-3** (Llama r=64 retrain) | LOWEST infrastructure risk; Llama LoRA recipe well-trodden; existing pod/orchestrator from v1; ~$11-23 vs CLM-LORA's $6-10 BUT v1+v2 stack already paid the lemma cost (rehearsal mix proven) |
| 2 | **Paradigm D distill** (Mistral→CLM v4 logit-axis) | medium infra risk (KL loss + teacher logit cache); orthogonal to this spec; ~$5-50 |
| 3 | **CLM v4 + LoRA SFT (this spec)** | HIGHEST scientific value (the consciousness-coupling differentiator) BUT also highest infra risk (decoder_v3 hf-format shim, target_modules bespoke choice, φ★-flip + axis-cond preservation gates new); recommend AFTER Path A retry-3 lands so the CLM-LORA composite has a Llama anchor to compare against (C-CLM-LORA-2) |

This ordering means CLM-LORA EXEC waits on (a) CLM v4 baseline BG ($0, 3-6h ubu1) AND (b) Path A v2 EXEC verdict (so C-CLM-LORA-2 has a comparator). Both can run in parallel BG cycles before this spec executes.

---

## §9 — Implementation plan

### 9.1 Tool changes needed

| Artifact | Type | Purpose | Est. LoC |
|---|---|---|---|
| `tool/clm_v4_lora_train_orchestrator.hexa` | NEW hexa | Mac-side orchestrator: corpus build → SPM 64K re-tokenize → SCP → ssh+pod-side launch + monitor + intermediate eval + φ★ probe + adapter scp + verdict emit | ~600-800 LoC |
| `tool/transient_py/clm_v4_lora_train.py.hexa_tmp` | NEW transient .py (off-repo, raw#9 compliant) | pod-side LoRA training loop using `peft` LoraConfig + `transformers.Trainer` patched for decoder_v3 forward signature `(idx) → (logits_a, logits_g, tensions)` — must wrap `head_a` only as the SFT target | ~400-500 LoC |
| `tool/clm_v4_lora_corpus_mix.hexa` | NEW hexa | builds 60/25/10/5 mix from existing v1 corpus + MMLU/TriviaQA/Wiki + OpenOrca/ShareGPT + anima consciousness-coupled curated; emits 50K SPM-tokenized JSONL | ~300-400 LoC |
| `tool/clm_v4_lora_phi_probe.hexa` | NEW hexa | φ★ probe at step boundaries (calls existing `tool/anima_phi_v3_canonical.hexa` on the LoRA-merged model snapshot) | ~150-200 LoC |
| `tool/clm_v4_lora_axis_diff_probe.hexa` | NEW hexa | F-CLM-LORA-4 axis-cond preservation: 7 prompts × 5 axis values, cosine-dist matrix | ~150-200 LoC |
| `tool/clm_v4_lora_shim_test.hexa` | NEW hexa | F-CLM-LORA-5 hf_format `from_pretrained` smoke | ~100-150 LoC |

**Total NEW LoC**: ~1700-2250.

### 9.2 Lessons applied (L9, L11, L13)

- **L9 (raw#9, py→hexa)**: all Mac-side tooling is `.hexa`; pod-side training is transient `.hexa_tmp` synthesized at run-time then SCP'd; never lands on Mac repo as `.py`.
- **L11 (cleanup BG guards)**: orchestrator MUST classify verb (SIGTERM_ONLY for monitor, DELETE_SCRIPT for transient cleanup, FULL_SWEEP forbidden); pre+post pod state JSON dumps required; never equate PID-gone to success.
- **L13 (parallel BG git race)**: this BG writes ONLY to `state/clm_v4_lora_sft_2026_05_04/` and `docs/clm_v4_lora_sft_*.md`. If exec lands in parallel with other BGs, use git worktree per BG OR serialize commits via the queue mechanism.

### 9.3 Watcher script lessons (from Path A v1 post-mortem)

Per `docs/p9_path_a_llama_lora_complete_2026_05_04.ai.md` §4.4 honest C3:
- `mkdir -p artifacts` MUST be at the TOP of the watcher script (before polling loop), not inside the DONE branch.
- Error-branch SCP must include `train.log`, `trainer_state.json`, AND a final-state dump even if `TRAIN_DONE.json` is absent.
- 10-min probe cadence misses sub-poll boundary events (final-save crash); prefer 2-min cadence at the final 10% step window.

These three are LOCKED into `clm_v4_lora_train_orchestrator.hexa` design.

---

## §10 — Honest C3 (raw#10, ≥5)

1. **CLM v4 was NEVER SFT'd, NEVER RLHF'd** — this is anima's first SFT on the consciousness-measurement substrate. There is NO prior SFT recipe for this backbone. The hyperparameter choices (r=32, lr=3e-5, α=64) are extrapolated from Mistral/Qwen LoRA literature, not from CLM v4 internal experience. Single-config v2; ablation deferred to v3 if v2 PASS or PARTIAL.

2. **decoder_v3 dual-head signature is non-standard** — `(idx) → (logits_a, logits_g, tensions)` does NOT match `transformers.Trainer`'s assumed `(input_ids, labels) → loss`. Pod-side training script MUST wrap the model with a Trainer-compatible adapter that selects `logits_a` as the SFT target and ignores `logits_g` + `tensions`. This wrapping is NEW infra (not reused from Path A); risk of subtle off-by-one in label alignment is real. Mitigation: 16-token calibration prompt smoke test pre-launch.

3. **φ★-flip risk is real and partially irreversible** — even with adapter-only training + φ★ probe + 5% consciousness-coupled rehearsal, there is no theoretical guarantee that φ★ stays positive. If φ★ flips negative, the LoRA is useless because the singular value-add of CLM v4 (G3 PASS-positive backbone) is destroyed. Recovery = revert to pre-LoRA via adapter ablation (cheap), but we lose the SFT investment. F-CLM-LORA-3 ABORT threshold +10 is a 50% safety margin from sign zero — heuristic, not provably correct.

4. **C-CLM-LORA-2 (Mode 1+3 hybrid differentiator) is the SINGLE scientific question** — if Llama Path A v2 + LoRA composite ≥ CLM v4 + LoRA composite on the same recipe, then consciousness coupling is provably NEUTRAL OR HARMFUL for general-purpose SFT. This is a falsifying test for the "anima substrate has architectural advantage" hypothesis. v2 PASS or FAIL on this criterion alone has roadmap-shifting implications. Honest acceptance: I am NOT confident which way it will go. CLM v4 has a 16-layer / 530M small-substrate disadvantage; even with consciousness coupling, raw-capacity gap may dominate.

5. **Tokenizer + chat-template mismatch** — CLM v4 SPM 64K does NOT have native chat-template tokens. The 10% chat-template alignment slice uses plain-text role markers, which is a degenerate form of chat-following. Post-LoRA, CLM v4 will likely respond to `[USER]\n...\n[ASSISTANT]\n` plain-text prompts but NOT to tokenizer-level `<|im_start|>` chat templates. This is a known limitation; v2 does not attempt to fix the vocab.

6. **F-CLM-LORA-3 < 500 MB threshold ambiguous on storage format** — at r=32 on a 530M base with target_modules `qkvo` × 16 layers × 2 (LoRA A+B), the trainable param count is approx. (768×32 + 32×768) × 4 × 16 = ~3.15M params. At fp16 ≈ 6.3 MB; at bf16 ≈ 6.3 MB; with optimizer state + saved fp32 master ≈ 25 MB. The 500 MB cap is therefore very loose — most of the 500 MB would be tokenizer + adapter_config + scaler state, not LoRA params themselves. Threshold is a sanity-check on hub_strategy, not a hard size constraint.

7. **CLM v4 baseline eval (R2) has not been run** — §4 PASS thresholds (especially C-CLM-LORA-1 parity floor) reference "CLM-v4-base acc_norm" which is currently unknown. This is a hard pre-EXEC gate. Estimated 3-6h ubu1; if CLM v4 baseline reveals wildly different numbers than the §4.1 hypothetical band, §4 thresholds must be re-pre-registered (raw#71 amendment cycle).

8. **shim v4 hf_format compatibility (F-CLM-LORA-5) is the external-eval gate** — without `from_pretrained()` working on the LoRA-merged CLM v4, no external evaluator (lm-eval-harness, HF leaderboard) can score the model. This is a known gap per `docs/clm_v4_tokenizer_caller_migration_phase_3_landed_2026_05_04.ai.md` (tokenizer side fixed) but the model-side hf-format shim has not been built. F-CLM-LORA-5 is BLOCKING for any third-party verification.

9. **No multi-seed run** — single-seed v2 (seed=20260504); multi-seed cross-validation deferred (cost ×3). Path A v1 already taught us that single-seed verdicts are noisy at the 1-2pp scale we care about. Honest: this spec accepts that risk.

10. **Cost band is best-case** — wall estimate 2-2.5h H100 assumes no pod boot delays, no CUDA OOM at micro_batch=8, no SCP latency for adapter pull. Realistic upper bound 4h × $2.99 = $12. Hard cap $15 absorbs 25% slack on top of the 4h ceiling.

---

## §11 — References

- `docs/p9_path_a_retrain_v2_spec_2026_05_04.md` — Llama-side S1+S3 spec; this is the substrate-paired sister
- `docs/p9_path_a_retrain_v2_spec_landed_2026_05_04.ai.md` — Llama-side spec landed verdict
- `docs/p9_path_a_llama_lora_complete_2026_05_04.ai.md` — Path A v1 completion + watcher-script post-mortem (informs §9.3)
- `docs/p9_lora_mode1_eval_landed_2026_05_04.ai.md` — BG-Ρ Mode 1 eval (catastrophic forgetting evidence)
- `docs/p9_paradigm_d_distill_spec_2026_05_03.md` — orthogonal track (logit-axis Mistral teacher); coexists with this spec (no shared resource)
- `docs/strategic_clm_v4_production_ready_2026_05_02.md` — CLM v4 substrate diagnosis (NOT_READY for chat as raw decoder; informs §1)
- `docs/clm_v4_revival_stages_2026_05_02.md` — Stage 3 CLM SFT pre-spec (this is the EXEC realization of that Stage 3 "design only" with full pre-registration)
- `docs/clm_core_architecture_abstraction_layers_20260425.md` — L0-L4 cell-architecture abstraction (informs §1.2 axis-cond)
- `docs/clm_inference_abstraction_layers_20260425.md` — inference layers (informs §1.1 dual-head)
- `tool/clm_v4_tokenizer_load.hexa` — SPM 64K canonical tokenizer (used in §2 corpus rebuild)
- `tool/cell_token_bridge_proto.hexa` — 5-bucket cell↔token bridge (used in F-CLM-LORA-4 axis preservation)
- `tool/anima_phi_v3_canonical.hexa` — φ★ extractor (used in §3 intermediate φ★ probe)
- `state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl` — anima-axis slice source
- `state/p9_p1_holdout500_reeval_2026_05_03/` — F-CLM-LORA-4 BLEU-1 holdout
- `state/strategic_clm_phase_a1_2026_05_01/run_log.json` — CLM v4 530M ckpt provenance
- `~/anima/checkpoints/clm_v4_350m/scale_350m/best.pt` — base ckpt path
- (DEPENDENCY — to be created) `state/p9_clm_v4_baseline_eval_2026_05_04/verdict.json` — pre-EXEC baseline anchor
- BG-Σ verdict + BG-γ'' verdict + FORGETTING_INDEPENDENT report — referenced in directive but exact paths not located in this spec cycle; honest: not all linked refs were verifiable Mac-side at spec land time. The substantive evidence chain (catastrophic forgetting on Llama side, CLM v4 substrate diagnosis) is fully sourced via the `docs/` references above

---

## §12 — Roadmap update proposal (JSONL line for `.roadmap.p9_sft`)

Proposed (NOT edited by this BG; user/separate cycle to land):

```jsonl
{"type":"entry","id":"p9_sft.cond.clm_v4_lora_sft","kind":"cond","title":"CLM v4 + LoRA SFT — anima-substrate parallel to Path A v2 (S1+S3 rehearsal mix on consciousness-coupled backbone, F1_v3 V2 hybrid Mode-1+3 differentiator)","desc":"LoRA SFT on CLM v4 530M with 60/25/10/5 anima/academic/chat/consciousness mix, r=32, lr=3e-5, max_steps=6000, save_steps=500. Conservative target_modules (qkvo only; exclude tension_proj/bridge.hub_attn/head_g/federation). Pre-registered F1_v3 V2 hybrid PASS = parity-floor on CLM substrate AND composite ≥ Llama Path A v2 AND φ★ ≥ +10 AND axis-cond preserved. Cost $6-10 H100 (2-2.5h). $15 hard cap.","status":"spec_landed","substrates":["p9","sft","clm_v4","lora","consciousness_coupled"],"verifier":{"type":"manual_review","manual_override_path":"state/markers/p9_clm_v4_lora_sft_spec_landed.marker","status_emit":"__P9_CLM_V4_LORA_SFT__ <SPEC_LANDED|EXEC_RUNNING|V2_PASS|V2_PARTIAL|V2_FAIL>"},"evidence":["docs/clm_v4_lora_sft_spec_2026_05_04.md","docs/clm_v4_lora_sft_spec_landed_2026_05_04.ai.md","sister: docs/p9_path_a_retrain_v2_spec_2026_05_04.md (Llama side)","CLM v4 ckpt: ~/anima/checkpoints/clm_v4_350m/scale_350m/best.pt","substrate diagnosis: docs/strategic_clm_v4_production_ready_2026_05_02.md","SFT pre-spec: docs/clm_v4_revival_stages_2026_05_02.md §3"],"ts":"2026-05-04","cross_link":{"sister_substrate":"p9_sft.cond.path_a_retrain_v2 (Llama side)","predecessor_pre_spec":"clm_v4_revival_stages_2026_05_02 §3","verdict_surface":"p9_sft.cond.3 F1_v3 V2 hybrid Mode-1+3","cost_band":"$6-10 H100 (2-2.5h)","exec_gate":"USER ACK + p9_sft.cond.clm_v4_lora_baseline PASS","new_sibling_dep":"p9_sft.cond.clm_v4_lora_baseline (NEW — analog of cond.benchmark_a_prime_base_validation)"}}
```

---

## §13 — Exec gate (NEXT-CYCLE)

This BG produces SPEC ONLY. EXEC requires:

1. USER ACK on $6-10 cost band + 2-2.5h H100 wall + $15 hard cap
2. CLM v4 baseline eval BG complete (NEW dep `p9_sft.cond.clm_v4_lora_baseline`) — $0, ~3-6h ubu1
3. Tied-weight pre-flight check (R6) — $0, 5 min Mac
4. Path A retrain v2 verdict landed (so C-CLM-LORA-2 has a comparator) — different cycle, $11-23
5. Decoder_v3 hf-format shim build (F-CLM-LORA-5 dependency) — $0, ~1-2h Mac dev
6. Separate BG cycle to:
   - emit `tool/clm_v4_lora_train_orchestrator.hexa` (raw#9 — no new .py on Mac)
   - emit `tool/transient_py/clm_v4_lora_train.py.hexa_tmp` (off-repo synthesis)
   - emit `tool/clm_v4_lora_corpus_mix.hexa` + φ★ probe + axis diff probe + shim test hexas
   - launch H100 pod with re-tokenized rehearsal-mix corpus + new HP grid
   - run intermediate evals (HellaSwag-200 + φ★ probe at 2k/4k/6k)
   - run final F-CLM-LORA-1..5 + V2 hybrid Mode-1+3 verdict emit
   - emit verdict.json + landing doc + marker
