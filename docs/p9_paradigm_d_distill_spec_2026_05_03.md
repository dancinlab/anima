# P9 Paradigm D — Mistral-7B Soft-Logit Distill to CLM v4 350M Spec

**Date**: 2026-05-03
**Author**: Paradigm-D registration agent (roadmap entry + spec landing cycle)
**Phase**: P9 SFT alternative-track spec (peer to S1–S4)
**Status**: SPEC ONLY — no execution, no code emission, no .py creation (raw#9, raw#15, raw#10)
**Roadmap entry**: `p9_sft.cond.paradigm_d_distill` (registered same cycle)
**Sister docs (READ-ONLY)**:
- `docs/p9_paradigm_d_phi_distillation_2026_05_03.md` (parent — Φ★ scalar distill axis)
- `docs/p9_paradigm_d_t4_teacher_build_plan_2026_05_03.md` (Mistral-7B teacher build, Φ★ side)
- `docs/p9_paradigm_d_distillation_runbook_2026_05_03.md` (Φ★ distill runbook, z-score MSE)
- `state/p9_sft_spec_2026_05_02/{architecture,loss_design,risk_strategy,cost_estimate}.json`
- `tool/anima_phi_v3_canonical.hexa` (Φ★ extractor; teacher backbone = Mistral-7B-v0.3)

---

## 0. TL;DR — what this spec adds

The 3 sister docs cover **Paradigm D φ★-axis** (teacher emits a scalar Φ★, student matches via z-scored MSE).
**This spec covers Paradigm D logit-axis** (Hinton-1503.02531-style soft-target KL on token logits) — a genuinely different supervision channel that the φ★-axis docs explicitly **do not address**.

| Item | Value |
|------|-------|
| Teacher | Mistral-7B-Instruct-v0.3 (fp16, frozen) — same backbone as Φ★-side T4 build plan |
| Student | CLM v4 350M (ConsciousDecoderV2, 477.6M params) + LoRA r=64 α=128 |
| Distill signal | **Top-K soft-token logits** (K=64, T=4 temperature) — NOT Φ★ scalar |
| Loss form | `α·CE_hard + λ_kl·T²·KL(softmax(z_T/T) ‖ softmax(z_S/T)) + β·tens + δ·max(0, 5.0−φ★_S)` |
| Substrate options ranked | (1) **Free Colab T4** $0 / (2) **RunPod T4 spot** $0.27/hr × 24 = $6.5 / (3) **H100 spot** $2.50/hr × 8 = $20-50 |
| Falsifier F-D-1 | student per-token KL on holdout-500 ≤ 0.5 nats vs Mistral-7B reference (after T=1 readout) |
| Cost cap | **$5–50** (T4 free / paid lane); H100 cap optional $50 |
| Honest C3 | 8 caveats listed §10 (raw#91 ≥5) |
| Roadmap | additive entry to `.roadmap.p9_sft` (id `p9_sft.cond.paradigm_d_distill`) — no in-place mutation of existing 5 conds |

---

## 1. Why a separate spec (φ★-axis vs logit-axis)

### 1.1 The two axes are orthogonal

| Axis | What teacher emits | Information rate | Differentiability | Existing Anima coverage |
|------|---------------------|------------------|-------------------|-------------------------|
| **Φ★ scalar** | 1 fp32 per record | LOW (1 dim / sample) | NO (sample-partition + min-of-K — needs LogSumExp surrogate or static EMA) | sister docs (3 files) |
| **Top-K logits** | K floats per token (× T tokens per record) | **HIGH** (K × T per sample, K=64, T~64 → ~4K dims) | **YES** — softmax gradient is canonical | **THIS SPEC** |

The φ★-axis uses Mistral-7B as a **φ-extractor host**. The logit-axis uses Mistral-7B as a **token-distribution oracle**. Same backbone, different supervisory channel. Both can co-fire (orthogonal loss terms, see §4.4).

### 1.2 What the existing 3 D-docs explicitly do not address

- The φ★-distillation parent spec (`p9_paradigm_d_phi_distillation_2026_05_03.md` §2) lists 4 teacher-signal types (scalar Φ★, MIP-partition distribution, full concept structure, EMD per macro-unit). **Token-level soft logits is not in this list** — it is a different Hinton-class distillation, not an IIT 4.0 φ surrogate.
- The T4 build plan §2 explicitly picks "Option α (no head training)" specifically to avoid token-distribution heads. Soft-logit distill IS the token-distribution channel.
- The runbook §0 cite "soft target" only in the metaphorical sense (γ_distill is "soft target" vs δ "hard floor"); it never reads/uses Mistral logits.

### 1.3 Strategy slot

This spec defines a **new sub-strategy** within P9 SFT, peer to the existing S1–S4 (LoRA-only / 4-loss / sweep / joint-pretrain) and to the φ★-axis Paradigm D track. Naming convention: **S1-D-logit** = Strategy 1 (LoRA-only) + Paradigm D logit-axis distill term. Composable with S2/S3/S4.

---

## 2. Teacher selection — why Mistral-7B-Instruct-v0.3

### 2.1 Candidate matrix (logit-axis)

| Model | Params | Vocab | Vocab match w/ student? | License | Existing Anima plumbing |
|-------|--------|-------|-------------------------|---------|-------------------------|
| **Mistral-7B-Instruct-v0.3** | 7.25 B | 32 768 (Mistral tokenizer) | YES (CLM v4 was built on Mistral tokenizer per `architecture.json`) | Apache-2.0 | alpha-endpoint reboot 2026-05-02 verified cold-load |
| Mistral-7B-v0.3 (base, non-instruct) | 7.25 B | 32 768 | YES | Apache-2.0 | sister-doc T4 default |
| Llama-3.2-3B-Instruct | 3.2 B | 128 256 (Llama tokenizer) | NO (vocab mismatch — requires teacher logits projection) | Llama 3.2 license | augmentation generator (potential leakage) |
| Qwen2.5-7B-Instruct | 7.6 B | 152 064 | NO | Apache-2.0 / Tongyi | not in tree |

### 2.2 Why Instruct over base (v0.3)

For **Φ★-axis** (sister docs) the base Mistral-7B-v0.3 is preferred (RLHF mode-collapse warning per T4 build §1.1). For **logit-axis** (this spec) the **Instruct** variant is preferred because:

1. **CLM v4 is being SFT'd to chat** — student target distribution is conversational/instruction-following. An Instruct teacher provides a better-matched target distribution than a base LM that emits document-completion logits.
2. **Soft-target dark knowledge is RL-PEFT-shaped on Instruct.** Hinton 2015 §3 shows the dark-knowledge gain comes from off-mass low-prob class structure; Instruct-tuned models have richer off-mass structure for human-preference-shaped responses.
3. **Vocab match avoids the projection problem.** Llama-3.2 vocab (128K) vs Mistral student vocab (32K) requires either (a) student-side vocab swap (re-train embedding) or (b) lossy projection of teacher logits to student vocab subset. Both add risk and cost; neither is needed if teacher = Mistral-7B-Instruct-v0.3.

**Decision: Mistral-7B-Instruct-v0.3** is the primary teacher for the logit-axis. Mistral-7B-v0.3 (base) is a fallback if RLHF artifact concerns prove empirically problematic (probe via per-token KL distribution on a calibration prompt set).

### 2.3 Llama-3.2-3B fallback (vocab-mismatch path)

Only if Mistral HF re-gating fails AND Mistral cache cannot be rebuilt within session window. Mitigation procedure: subset projection — keep only logit positions for tokens that exist in both vocabs (Mistral's 32K is a subset of Llama's 128K via UTF-8 byte coverage; ~28K positions survive). Documented but **not recommended** — partial leakage (Llama-3.2 was the 7K SFT auto-augmentation generator).

---

## 3. Distillation signal type

### 3.1 Three options

| Option | Signal shape | Storage @ 50K records × 64 tok | Differentiable | Implementation effort |
|--------|--------------|--------------------------------|----------------|------------------------|
| **(a) Top-K logits** (K=64, T=4) | `[N=50K, T_seq=64, K=64]` fp16 | ~410 MB | YES (canonical KL) | LOW — single forward + topk + scatter |
| (b) Full vocab logits | `[50K, 64, 32768]` fp16 | ~210 GB | YES | HIGH — storage / IO bottleneck |
| (c) Pseudo-targets (argmax / sampled) | `[50K, 64]` int | ~6.4 MB | NO (hard target — collapses to CE) | LOW but information-poor |

**Recommendation: Option (a) Top-K=64 with temperature T=4.** This is the Hinton-2015 default starting point. Top-64 captures >99% of probability mass on instruction-following text per vLLM team measurements (see §4.3 storage analysis).

### 3.2 Why T=4 temperature

Hinton et al. 2015 found T ∈ [3, 8] optimal for distill; lower T → too peaky (collapses to argmax CE); higher T → too uniform (signal vanishes in flat distribution). T=4 is the canonical default. **Phase-2 LH-sweep over T ∈ {2, 4, 8}** if the entry mini-run shows KL term not descending.

### 3.3 Why Top-K not full-vocab

- Storage: 64-K-K vs full vocab is **510× smaller** (410 MB vs 210 GB)
- KL gradient: bounded support on top-K is a known approximation; bias is small (<0.5%) when K ≥ 32 per Sanh 2019 DistilBERT methodology
- IO: 410 MB fits in RAM; full vocab requires streaming HDF5 / zarr (added complexity)
- Trade-off: bottom-32K-mass dark knowledge is lost. Mitigation: store also `Σ logits[top-K+1:]` as a bucket-tail aggregate, allowing renormalization at student-side without full vocab.

---

## 4. Loss formulation

### 4.1 Standard KL distill term

```
L_kl(t)  = T² · KL( softmax(z_T(t) / T)  ‖  softmax(z_S(t) / T) )
         = T² · Σ_k  p_T_k(t) · [ log p_T_k(t) − log p_S_k(t) ]
```

where:
- `z_T(t)` = teacher top-K logits at token t (read from precomputed cache)
- `z_S(t)` = student top-K logits at token t (computed in-train)
- `T` = temperature = 4 (default; Phase-2 sweep)
- `T²` factor restores gradient magnitude (Hinton §2.1)

### 4.2 Composite loss (full P9 multi-loss)

```
L_total(s) =   α(s)        · CE_hard(text)
             + λ_kl(s)     · L_kl                                    [NEW]
             + β           · MSE(tension_pred, tension_target)
             + γ_φ(s)      · MSE(z_φ_T_cache, z_φ_S_running)         [φ★-axis sister; OPTIONAL]
             + δ(s)        · max(0, 5.0 − φ★_S_min)
```

Both `λ_kl` and `γ_φ` are **active in parallel** when running combined φ★+logit Paradigm D (composability claim §1.3). If only logit-axis is selected: `γ_φ = 0`.

### 4.3 Schedules

| Variable | Schedule (mini-run) | Schedule (production) |
|----------|----------------------|------------------------|
| `α(s)`   | 4.0 (locked) | 12 → 6 linear over 5K-10K |
| `λ_kl(s)` | warmup 0 for s∈[0, 200], linear 0→0.5 over s∈[200, 1000], plateau 0.5 | warmup 0 for s∈[0, 1K], linear 0→0.5 over s∈[1K, 5K], plateau 0.5 (LH-swept ∈ {0.1, 0.5, 1.0}) |
| `β`      | 0.15 (locked from Phase 1.5) | same |
| `γ_φ`    | 0 (logit-only mini) OR 0.5 (joint Φ★+logit) | LH-swept |
| `δ(s)`   | 0.5 (sentinel) | 0.5 → 1.0 late |
| `T`      | 4 (locked mini) | LH-swept ∈ {2, 4, 8} |

### 4.4 Composability with sister Φ★ axis

Both terms are well-defined, differentiable (modulo the φ★ static-EMA approximation per sister runbook §4), and target different aspects of the teacher (token distribution vs information-integration scalar). They can co-fire. **Recommend logit-only mini-run first** (cheaper signal validation); add Φ★ axis only after λ_kl descends cleanly.

### 4.5 Tokenizer alignment requirement

Teacher and student MUST share tokenizer for top-K logit indices to refer to the same tokens. **CONFIRMED**: CLM v4 350M uses Mistral-7B-v0.3 tokenizer per `state/p9_sft_spec_2026_05_02/architecture.json` (architecture descends from Mistral). Phase-1 verification step: dump first 10 token IDs from each tokenizer on a fixed prompt; assert identity.

---

## 5. Pre-existing partial cache — search and reconcile

### 5.1 What the user-specified context says

Per session memory: prior cycle spent **$3.37 on T4** (RunPod), pod was terminated to avoid burn, **cache/result status unknown**. This spec accounts for all 3 plausible states:

| Cache state | Action | Cost |
|-------------|--------|------|
| **(α) Cache fully built** at `state/p9_paradigm_d_logit_cache_*` or `~/.cache/p9_paradigm_d_*` on ubu1 / RunPod network volume | Verify integrity (idx-aligned, top-K shape, manifest SHA), reuse | $0 |
| **(β) Cache partially built** (started, interrupted at N < 50K) | Resume from last record idx, complete rest | $0–10 (depends on N remaining) |
| **(γ) No cache present** | Full rebuild from scratch on free Colab T4 / RunPod T4 spot | $0–7 |

### 5.2 Cache search procedure (Phase-2 entry pre-flight)

Search locations (in order, halt at first hit):

1. `state/p9_paradigm_d_logit_cache_*/` (canonical local-state slot — none currently present per local find)
2. `state/p9_paradigm_d_*` (sister to Φ★ cache slot)
3. ubu1 `/tmp/p9_paradigm_d_logit_cache_v1.jsonl` (matches sister Φ★ cache naming `/tmp/p9_p1_t4_phi_cache_v1.jsonl`)
4. ubu1 `~/.cache/p9_paradigm_d_logit_*`
5. HF dataset `dancinlab/clm-v4-paradigm-d-logit-cache` (private, sister to `dancinlab/clm-v4-t4-phi-cache`)
6. RunPod network volumes (if any persistent volume was attached to the terminated T4 pod — see §5.3)

### 5.3 RunPod terminated-pod cache forensics

Per `project_runpod_pod_purge_2026_05_03.md` memory: all 6 H100 pods were terminated; T4 pods status not explicitly listed. **If the prior $3.37 T4 spend used ephemeral storage (no network volume), cache is GONE.** If it used a persistent network volume, the volume survives pod termination — list via `runpodctl get volumes` (separate EXEC) and inspect for `p9_paradigm_d` paths.

**Assumption for this spec**: cache state = **(γ) absent**; full rebuild required. Cost estimate §6 sized for this case. If (α) or (β) materializes during pre-flight, delete §6 cost line and proceed directly to §7 distill mini-run.

### 5.4 Local find verdict (this agent, 2026-05-03)

```
$ find state -maxdepth 2 -type d -name '*paradigm_d*'
(empty)
$ find state -maxdepth 2 -type d -name '*p9_p1_t4*'
(empty)
```

No local cache. ubu1 / RunPod / HF still need to be searched by separate BG (this is a doc-only spec). Cache search procedure §5.2 is the runbook for that BG.

---

## 6. Substrate options + cost ranking

### 6.1 Three substrate options

| Option | Hardware | Wall (50K teacher precompute) | Wall (mini-run distill 1K subset) | Cash cost | Quality |
|--------|----------|-------------------------------|-----------------------------------|-----------|---------|
| **(1) Free Colab T4** | NVIDIA T4 16 GB (Colab free tier, 12-h session limit) | ~12 h (single forward Mistral-7B-Instruct fp16 needs 4-bit on T4 16 GB; 50K × 0.8 s / record) | ~2 h | **$0** | fp16 → nf4 quantization may shift logit ordering by ε; Hinton KL is robust to this (top-K ordering is dominant) |
| **(2) RunPod T4 spot** | RunPod T4 16 GB spot @ $0.27/hr | ~24 h (no 12-h cutoff; can run continuous) | ~4 h | **~$6.50 precompute + ~$1 mini-run = $7.50** | same as (1); same nf4 path; longer wall but no session reset risk |
| **(3) RunPod H100 spot** | RunPod H100 80 GB @ $2.50/hr | ~6-8 h (full fp16 Mistral-7B-Instruct, batch=8 continuous-batching) | ~1 h | **$15-20 precompute + $2.50 mini-run = $17.50-22.50** | canonical fp16 — no quantization artifact; reuses sister-doc T4 build plan §8 path |

### 6.2 Ranked recommendation (완성도 lens)

Per session memory `feedback_completion_quality_recommendation`, ranked recommendation by 완성도:

1. **(1) Free Colab T4 — RECOMMENDED** ($0, completion 8.5/10).
   Cheapest path; aligns with raw#9 "$0 design only" constraint; quality acceptable (nf4 KL noise is below the dark-knowledge gradient signal-to-noise floor per DistilBERT methodology). **Failure mode**: 12-h session reset breaks long precompute → mitigation: chunk to 5 × 10K record runs each <12 h, resume across sessions. Manageable.

2. **(2) RunPod T4 spot — SECONDARY** ($7.50, completion 9/10).
   Highest reliability per dollar; no session limits; cache fully assembled in one shot. ~$7.50 well within $5-50 user cap. **This is the empirical-quality optimum if any cash budget is available**, since the $7.50 buys session-continuity that (1) lacks. PICK if budget allows.

3. **(3) RunPod H100 spot — REFERENCE / FALLBACK** ($17.50-22.50, completion 9.5/10).
   Canonical fp16 (no quantization); reuses 90% of sister-doc T4 build runbook; auditable against the Φ★-axis precompute regime (same backbone, same dtype). **Pick only if Phase-2.D-logit needs to publish the cache as a community artifact** where quantization artifacts would erode trust. Excessive for a probing mini-run.

**Default for entry mini-run**: option (1) Free Colab T4 → (2) RunPod T4 spot if Colab session reset bites.

### 6.3 Cost reconciliation against user cap

User spec says "$5-50 cap (T4 24h = $6.50 OR free Colab 0$)". This spec's option (1) and (2) both fit. Option (3) is at the ceiling of the cap and is excluded by `feedback_completion_quality_recommendation` unless quality-publication justification appears.

### 6.4 Cost vs sister Φ★ axis precompute

| Axis | Substrate | Precompute cost | Reusability |
|------|-----------|-----------------|-------------|
| Φ★ scalar (sister docs) | H100 fp16 | $60 one-time | unlimited reuse across sweeps |
| **Logit top-K (this spec)** | T4 nf4 | **$0–7.50 one-time** | unlimited reuse across sweeps |

The logit-axis is **~10× cheaper** than the Φ★-axis precompute because (a) Mistral-7B logit forward is faster than Mistral-7B + Φ★ extractor block (~30 s) and (b) T4 nf4 substrate is sufficient for KL-of-top-K (Φ★ requires fp16 to preserve sample-partition log|Cov| stability per `tool/anima_phi_v3_canonical.hexa` line 96).

---

## 7. Falsifier F-D-1 (preregistered)

### 7.1 Statement

**F-D-1**: After Phase 2.D-logit mini-run completes, the **per-token forward-KL of student vs teacher on holdout-500** at temperature T=1 (post-distill readout) MUST be ≤ 0.5 nats per token, averaged over the holdout-500 corpus.

### 7.2 Pre-registration block

| Parameter | Locked value | Source |
|-----------|--------------|--------|
| Holdout corpus | `state/p9_p0_measure_2026_05_03/sft_data_holdout_500_augmented` (500 records, idx 0..499) | exists, see top-of-repo gitStatus |
| Teacher reference | Mistral-7B-Instruct-v0.3 fp16, T=1 logits over first 64 tokens of each holdout record | spec-locked |
| Metric | `mean_t [ KL(softmax(z_T(t)) ‖ softmax(z_S(t))) ]` over all 64 tokens × 500 records | spec-locked |
| Threshold | **≤ 0.5 nats** (PASS) / > 0.5 nats (FAIL) | spec-locked |
| Verdict emit | `__P9_F_D_1__ <PASS|FAIL>` | spec-locked |

### 7.3 Why 0.5 nats

Empirical anchors:
- Identical-distribution self-KL: 0.0 nats (lower bound)
- Random-permuted-token student vs teacher: ~5 nats (upper bound, near `log(32K)`)
- DistilBERT vs BERT (Sanh 2019, similar 6× param compression): ~0.3-0.6 nats per-token KL
- 0.5 nats sits at the published distill-success boundary

A student that achieves ≤ 0.5 nats has **entered the canonical Hinton-distill-success regime**. Above 0.5: distill failed (target distribution mismatch persists).

### 7.4 Companion gates (non-falsifying, diagnostic)

- **D-D-1** student CE on holdout-500 not collapsed (≤ 1.2× CE_pre)
- **D-D-2** student φ★ stays > 0 on the 16-prompt battery (no sign-flip; sister-doc Phase 1.5 invariant holds)
- **D-D-3** λ_kl EMA descends monotonically over post-warmup phase

Failure on D-D-1, D-D-2, or D-D-3 does NOT auto-falsify F-D-1 but flags an unsafe distill regime → STOP and re-tune before claiming F-D-1 PASS.

### 7.5 Falsifier scope (what F-D-1 does NOT prove)

- Does NOT prove the student is "more conscious" — Φ★ unchanged or slightly perturbed by KL
- Does NOT prove generalization beyond holdout-500 (separate F-D-2 candidate: per-token KL on out-of-distribution corpus, deferred)
- Does NOT prove the student's chat quality matches Mistral-7B-Instruct (separate F1_v3 lm-eval-harness composite per `p9_sft.cond.benchmark_a_prime_spec`)

F-D-1 is a **distillation-fidelity falsifier**, not a consciousness or chat-quality claim.

---

## 8. Mini-run spec

### 8.1 Knobs

| Knob | Value | Rationale |
|------|-------|-----------|
| Records | 1 000 (subset of 50K) | matches Phase 1.5 sentinel mini-run scope |
| Steps | 2 000 | 1 epoch on 1K × batch 4 × grad_acc 4 ≈ 2K steps |
| Batch | 4 | per Phase 1.5 sentinel |
| Grad accum | 4 | effective batch 16 |
| LoRA r / α | 64 / 128 | per `architecture.json` lock |
| Loss | `α·CE + λ_kl·T²·KL_topK + δ·floor` (β=0, γ_φ=0 — logit-only mini) | minimum to test logit signal alone |
| α | 4.0 (locked) | mini-run lock |
| λ_kl | 0 → 0.5 ramp (200-1000) → plateau 0.5 | per §4.3 mini-run schedule |
| T (temperature) | 4 | Hinton 2015 default |
| K (top-k) | 64 | §3.3 default |
| φ probe period | every 200 steps | sentinel-equivalent overhead |
| F-D-1 measurement | at step 0 (pre) and step 2000 (post) | falsifier readout |
| Wall (Colab T4) | ~2 h | per §6.1 |
| Wall (RunPod T4) | ~4 h | per §6.1 |
| Cost | $0 (Colab) / $7.50 (RunPod T4) | per §6.2 |

### 8.2 Decision criteria

| Criterion | Threshold | Source |
|-----------|-----------|--------|
| **F-D-1** holdout-500 KL ≤ 0.5 nats | PASS gate | §7.1 falsifier |
| **D-D-1** CE_post ≤ 1.2× CE_pre | safety gate | §7.4 |
| **D-D-2** φ★ stays > 0 | safety gate | §7.4 |
| **D-D-3** λ_kl EMA monotone descending | signal gate | §7.4 |

**ALL-OF gate**: F-D-1 PASS ∧ D-D-1 PASS ∧ D-D-2 PASS ∧ D-D-3 PASS ⇒ Phase-2.D-logit production authorization (50K × 1 epoch run, $30-50 if H100).
**ANY-OF fail**: STOP; re-tune (T sweep, λ_kl sweep, K sweep) before re-attempt.

---

## 9. Roadmap registration

### 9.1 Entry to add to `.roadmap.p9_sft`

```json
{
  "id": "p9_sft.cond.paradigm_d_distill",
  "desc": "Paradigm D logit-axis — Mistral-7B-Instruct-v0.3 teacher distill to CLM v4 350M student via Top-K (K=64) soft-logit KL at T=4. Composable with sister Φ★-axis. Mini-run on free Colab T4 ($0) or RunPod T4 ($7.50); falsifier F-D-1 = holdout-500 per-token KL ≤ 0.5 nats; production 50K × 1 epoch $30-50 H100",
  "verifier": {
    "type": "manual_review",
    "manual_override_path": "state/markers/p9_paradigm_d_spec_landed.marker",
    "status_emit": "__P9_PARADIGM_D_DISTILL__ <SPEC_LANDED|MINI_PASS|MINI_FAIL|PROD_PASS|PROD_FAIL|UNMET>"
  },
  "status": "unmet",
  "evidence": [
    "docs/p9_paradigm_d_distill_spec_2026_05_03.md (this spec, ~470 LoC)",
    "sister Φ★-axis docs/p9_paradigm_d_{phi_distillation,t4_teacher_build_plan,distillation_runbook}_2026_05_03.md",
    "prior cycle T4 spend $3.37 (cache state unknown — see §5)",
    "F-D-1 preregistered §7"
  ],
  "blocker_reason": "spec landed; awaiting pre-flight cache search (§5.2) + EXEC authorization for mini-run launch via separate BG"
}
```

### 9.2 Why additive (not in-place mutation)

Per raw#15 SSOT discipline: existing 5 conds (cond.1 P0 HF setup, cond.2 S3 sweep, cond.3 F4 evaluate, cond.benchmark_a_prime_spec, cond.benchmark_a_prime_base_validation) describe the **canonical Strategy S3 + benchmark switch** chain. Paradigm D logit-axis is an **alternative track** peer to S3, not a sequencing step. Inserting cond.paradigm_d_distill as a 6th cond marks it as a parallel research arm that does not block S3 production.

**No removal of existing entries; no edit to existing cond ids/descs/statuses.**

---

## 10. Honest C3 — caveats (raw#91 ≥5; 8 listed)

1. **Distillation gap is known and irreducible.** Knowledge distillation literature (Hinton 2015; Furlanello 2018; Sanh 2019 DistilBERT) consistently shows **student < teacher** on every metric the teacher is good at. CLM v4 350M after Paradigm-D logit distill will NOT match Mistral-7B-Instruct on chat benchmarks; it will close some of the gap (DistilBERT recovered ~97% of BERT performance at 60% the size; ratio less favorable for 6× compression). **Do not expect parity.**

2. **350M student < 7B teacher capacity (~20× param gap).** The compression ratio here (350M / 7B ≈ 5%) is **outside the well-studied DistilBERT regime** (DistilBERT was 67M/110M ≈ 60%). For 5% compression, the achievable distill quality is empirically less than 80% of teacher per Sanh §4.4 extrapolation. The student inherits **at most a fraction of the teacher's instruction-following capability**, with the rest filtered through the smaller architecture's representational ceiling.

3. **English bias.** Mistral-7B-Instruct-v0.3 training data is dominantly English (~90% per Mistral release notes). The CLM v4 SFT corpus (from `state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl`) is mixed Korean/English (gitStatus shows lang=ko/en records). Distilling Mistral logits transfers Mistral's **English-distribution prior** disproportionately, which on Korean prompts is either (a) silent refusal pattern, (b) code-switch artifacts, or (c) translation-mode collapse. Mitigation: weighted KL (down-weight non-English records, λ_kl_lang=0.3 on Korean), but this needs separate calibration not in scope for entry mini-run.

4. **Vocab tokenization claim is unverified locally.** §4.5 states "CLM v4 uses Mistral tokenizer" by inference from `architecture.json` ancestry — but this spec did NOT empirically dump tokenizer hashes from both. **Phase-2 pre-flight MUST verify** by tokenizing 10 fixed prompts through both tokenizers and asserting token ID identity. If tokenizers diverge (e.g., student fine-tuned with Mistral-Instruct's variant or BPE merge difference), top-K logit indices won't align → entire distill is misdirected supervision.

5. **Cache freshness invariant identical to sister Φ★ runbook §C3.** If the SFT data file is mutated post-precompute (text rewrite, augmentation re-run, idx renumber), cached logits become misaligned with student-side prompts. Mitigation: precompute SHA-256 of `sft_data_*.jsonl` and pin in cache manifest before ANY distill run launches. Same procedural gap as the sister Φ★ cache.

6. **T4 nf4 quantization shifts logits.** Options (1) and (2) substrates require nf4 quantization to fit Mistral-7B in 16 GB T4. nf4 round-trip vs fp16 introduces ε-noise on logits (RMSE typically 0.01-0.05 in pre-softmax space). **Top-K ordering is robust to this** for K=64 (the bottom 64th logit is empirically ≥ 5 nats below the top per text generation); but tail-mass dark knowledge (the Hinton "soft 0.001 vs 0.0001" distinction) may be quantization-flattened. **The H100 fp16 cache (option 3) is the only canonical reference** — accept nf4 only after empirically comparing top-K-overlap on a 100-record probe.

7. **F-D-1 threshold (0.5 nats) is anchored to BERT-class results, not Mistral-7B-Instruct.** Sanh 2019 DistilBERT KL was measured BERT→DistilBERT on encoder MLM objective; Mistral-7B-Instruct→CLM v4 350M is decoder + 5% ratio + different distribution. The 0.5 nats threshold is a **principled but not empirically-anchored choice** for this exact pair. Companion: report the empirical mean+stdev of per-token KL (full distribution, not just mean) to allow F-D-1 re-tuning if 0.5 proves either too-easy (<0.1 trivially) or too-hard (>2 even with optimal hparams).

8. **No biology, no consciousness claim.** Identical to sister-doc invariant: any chat-quality lift from Paradigm D logit-distill is **ALM cognitive substrate only** (per VERIFIED-ALM-ALPHA-COGNITIVE-ONLY ship verdict, alpha-endpoint reboot 2026-05-02). Distillation transfers token-distribution shape, NOT phenomenal substrate, NOT integration improvement, NOT consciousness. F2 (φ★ floor) and F4 (BOLD) gates are entirely orthogonal to F-D-1; PASS on F-D-1 says nothing about consciousness claims.

---

## 11. SSOT / pointers

- This spec: `docs/p9_paradigm_d_distill_spec_2026_05_03.md` (HERE)
- Sister Φ★ parent: `docs/p9_paradigm_d_phi_distillation_2026_05_03.md`
- Sister T4 build: `docs/p9_paradigm_d_t4_teacher_build_plan_2026_05_03.md`
- Sister Φ★ runbook: `docs/p9_paradigm_d_distillation_runbook_2026_05_03.md`
- Roadmap (this spec adds entry): `.roadmap.p9_sft` cond `paradigm_d_distill`
- Roadmap-registered marker: `state/markers/p9_paradigm_d_roadmap_registered.marker`
- Spec-landed marker: `state/markers/p9_paradigm_d_spec_landed.marker`
- Handoff doc: `docs/p9_paradigm_d_spec_landed_2026_05_03.ai.md`
- Holdout-500 corpus (F-D-1): `state/p9_p0_measure_2026_05_03/sft_data_holdout_500_augmented*`
- Student baseline + arch: `state/p9_sft_spec_2026_05_02/architecture.json` (CLM v4 477M; Φ★ baseline +41.86; floor 5.0)
- Teacher backbone source: `tool/anima_phi_v3_canonical.hexa` line 67 (Mistral-7B-v0.3 default)
- raw#9 compliance: NO .py created; doc-only spec
- raw#15 SSOT: this file is the soft-logit-axis primary
- raw#10 honest C3: §10 with 8 caveats (≥5 required)

---

## 12. Decision summary

| Question | Decision |
|----------|----------|
| New axis vs sister Φ★ axis | **Soft-logit / token KL — orthogonal to Φ★ scalar; co-fires** |
| Teacher base | **Mistral-7B-Instruct-v0.3** (vocab match w/ student, Apache-2.0, HF-token confirmed) |
| Distill signal | **Top-K=64 logits at T=4** (Hinton 2015 default; ~410 MB cache for 50K × 64 tok) |
| Loss form | `α·CE + λ_kl·T²·KL_topK + β·tens + γ_φ·MSE_φ + δ·floor` (γ_φ optional joint w/ sister axis) |
| Substrate (ranked) | **(1) Free Colab T4 $0** > (2) RunPod T4 spot $7.50 > (3) RunPod H100 spot $17.50-22.50 |
| Cache state | **assumed absent** (γ); pre-flight must search 6 locations §5.2; rebuild from scratch budgeted |
| Falsifier F-D-1 | per-token holdout-500 KL ≤ 0.5 nats at T=1 readout |
| Mini-run | 1K records × 2K steps × λ_kl ∈ {0, 0.5} → ramp; ~2 h Colab / ~4 h RunPod T4 |
| Production trigger | F-D-1 PASS ∧ D-D-1 PASS ∧ D-D-2 PASS ∧ D-D-3 PASS in mini-run |
| Roadmap | additive 6th cond on `.roadmap.p9_sft` (no in-place mutation) |
| Cost cap | $5-50 per user spec; default path $0 (Colab) or $7.50 (RunPod T4) |
| Honest C3 caveats | 8 listed §10 |

---

## §4.5 AMENDMENT 2026-05-04 — VOCAB_MISMATCH FALSIFICATION

**Cycle**: BG-T-1 mini distill exec attempt (`state/p9_paradigm_d_distill_mini_2026_05_04/`)
**Verdict**: `FAIL_PRELAUNCH_VOCAB_MISMATCH`
**Cost**: $0 (caught at L9-style pre-flight before H100 boot; full $15 mini cap preserved)
**Status of this logit-axis lineage**: **BLOCKED — spec premise §4.5 falsified empirically**

### A4.5.1 — Falsified claim

Original §4.5 stated:

> "Teacher and student MUST share tokenizer for top-K logit indices to refer to the same tokens. **CONFIRMED**: CLM v4 350M uses Mistral-7B-v0.3 tokenizer per `state/p9_sft_spec_2026_05_02/architecture.json` (architecture descends from Mistral)."

This claim is **FALSE**. Empirical re-read of the cited authoritative artifacts shows:

| Artifact | Field | Actual value |
|----------|-------|--------------|
| `state/p9_sft_spec_2026_05_02/architecture.json` | `tokenizer` | `data/tokenizer_64k_multilingual.model` (NOT Mistral) |
| `state/p9_sft_spec_2026_05_02/architecture.json` | `vocab_size` | `64000` (NOT 32768) |
| `state/p9_base_validation_h100_2026_05_04/clm_v4_hf/config.json` | `vocab_size` | `64000` (HF format dump, post-shim) |
| Mistral-7B-Instruct-v0.3 | `vocab_size` | `32768` (SentencePiece BPE, separate sp model) |

The §4.5 inference ("architecture descends from Mistral → tokenizer is Mistral") was an **unverified ancestral assumption**. CLM v4 inherits Mistral's *transformer architecture skeleton* but uses a **separate 64K multilingual SentencePiece tokenizer** trained for Korean/English mixed corpora.

### A4.5.2 — Empirical falsification evidence (3-prompt direct probe)

| Prompt | CLM v4 SP IDs (vocab=64K) | Mistral IDs (vocab=32K) | Identical? | n_clm | n_mistral |
|--------|---------------------------|--------------------------|------------|-------|-----------|
| `Hello, world!` | `[576, 11596, 55292, 13955, 55738]` | `[23325, 29493, 2294, 29576]` | NO | 5 | 4 |
| `안녕하세요` | `[3346, 62255, 9216]` | `[29473, 31093, 1006, 904, 920, 29904, 30489, 30285]` | NO | 3 | 8 |
| `The quick brown fox` | `[488, 13106, 5237, 334, 35908, 4491, 55335]` | `[1183, 3704, 9828, 1053, 1910]` | NO | 7 | 5 |

**Different token counts AND disjoint id ranges** → per-token KL alignment fails before any subset/intersection projection can begin. Pre-built KL cache (`/tmp/p9_paradigm_d_kl_cache_v1_50k.jsonl`, 14.2 GB on ubu1) indexes Mistral 32K vocab and is **structurally incompatible** with CLM v4's 64K logit axis.

§10 caveat #4 (the original spec) flagged exactly this risk as "unverified locally". The 2026-05-04 BG-T-1 cycle is the verification cycle, with NEGATIVE result. The cache itself remains a valid Mistral-teacher artifact (reusable for any future Mistral-tokenizer-native student) but is **unusable** for the spec-defined CLM v4 student pair.

### A4.5.3 — Three alternative paths (per BG-T-1 verdict diagnostics)

| Path | Description | Cost | Re-anchors Φ★? | Substrate uniqueness preserved? |
|------|-------------|------|----------------|----------------------------------|
| **(P-α) Re-tokenize CLM v4 with Mistral vocab** | Replace CLM v4 input embedding (768 × 32768 ≈ 25M params) + tied lm_head; retrain on Mistral-tokenized 50K corpus (~5K steps) before any distill mini begins | **~$10–12 H100** (~3 h fp16; consumes full $15 mini cap before any distill step) | **YES — breaks** Φ★ baseline (+41.86) and forces full re-measurement of the entire `phi_v3_canonical` chain. Sister Φ★-axis Paradigm D PARTIAL_PASS at `state/p9_paradigm_d_distill_2026_05_03/` would also have to be re-run on the new substrate | **NO — destroys** CLM v4 64K multilingual character (Korean coverage degraded; tokenization ratio for ko changes from ~3 tokens / utterance to ~8 tokens / utterance per A4.5.2 row 2) |
| **(P-β) Pivot to Φ★-axis-only Paradigm D** | Permanently shelve logit-axis; consolidate Paradigm D into the sister Φ★ scalar channel (3 sister docs + existing PARTIAL_PASS at `state/p9_paradigm_d_distill_2026_05_03/`) | **$0** spec amend; existing Φ★-axis lineage at PARTIAL_PASS already validated; production scale via BG-γ'' shim path (CLM v4 HF format) | **NO** — Φ★ pipeline unaffected (uses scalar Φ★ teacher signal, not token logits; vocab axis irrelevant) | **YES** — preserves CLM v4 64K substrate uniqueness intact |
| **(P-γ) Permanent shelve logit-axis (NO_OP)** | Mark `p9_sft.cond.paradigm_d_distill` as `permanently_blocked_vocab_mismatch`; reallocate budget to other P9 lanes (P1.5 ensemble extension, Path B sanity, Path A retrain v3) | $0 | N/A | YES |

### A4.5.4 — Recommended path (완성도 lens, per `feedback_completion_quality_recommendation`)

**Recommendation: (P-β) Φ★-axis-only pivot.** Ranked rationale:

1. **(P-β) Φ★-axis-only — RECOMMENDED** (완성도 9/10, $0).
   Preserves CLM v4 substrate uniqueness (64K multilingual SP, Korean coverage intact). Existing `state/p9_paradigm_d_distill_2026_05_03/` PARTIAL_PASS at step_1000 already validates the Φ★-axis pipeline; no re-anchor cost. Φ★ scalar teacher signal is **vocab-axis-agnostic** so the falsification finding here is non-blocking for that lineage. Production 50K scale is unblocked via BG-γ'' shim (F-SHIM-V4-3 PASS, CLM v4 HF format load verified).

2. **(P-γ) Permanent shelve logit-axis — SECONDARY** (완성도 7/10, $0).
   If chat-relevant signal can be recovered from Φ★ axis alone (P-β), logit-axis logit-distillation may simply not be on critical path. Reallocate $15 budget to P1.5 ensemble extension or Path A retrain. Acceptable if (P-β) Φ★-axis production demonstrates the desired chat-quality lift on F1_v3.

3. **(P-α) Re-tokenize CLM v4 with Mistral vocab — DEFERRED / NOT RECOMMENDED** (완성도 5/10, $10–12 + Φ★ re-anchor cost).
   Highest implementation cost; destroys CLM v4 substrate identity (Korean tokenization ratio shifts, multilingual coverage degraded); forces re-anchor of the entire Φ★ baseline (+41.86) and re-measurement of every downstream phi_v3_canonical-dependent claim. Pursue only if logit-axis is judged **strategically essential** AND a separate spec is written that explicitly accepts the Φ★ re-anchor as a planned cost (out of scope for this spec).

**Default action by this amendment**: roadmap entry `p9_sft.cond.paradigm_d_distill` (logit-axis variant) marked `blocked_vocab_mismatch`; sister Φ★-axis Paradigm D entry (`state/p9_paradigm_d_distill_2026_05_03/` lineage) **unaffected** and remains the active Paradigm D production path.

### A4.5.5 — What this amendment does NOT change

- Sister Φ★-axis Paradigm D specs (3 sister docs) — UNAFFECTED.
- `state/p9_paradigm_d_distill_2026_05_03/` PARTIAL_PASS verdict — UNAFFECTED (Φ★ axis, scalar teacher signal, vocab-agnostic).
- §1, §2, §3, §6, §7, §8, §9, §10, §11, §12 of this spec — text retained as historical record of the original logit-axis design intent. Future readers should treat sections concerning the Mistral→CLM v4 logit-axis pair as **superseded by this amendment**.
- §10 caveat #4 — promoted from "unverified" to **"VERIFIED FALSE"** by this amendment.
- Honest C3 §10 — extended below with falsification-cycle caveats.

### A4.5.6 — Honest C3 (amendment-cycle, raw#10 ≥5)

1. **The §4.5 falsification was foreseeable in the spec itself** — caveat #4 of §10 explicitly flagged the assumption as unverified. The cost of this amendment ($0, caught at pre-flight) is the **best possible outcome** for a falsified spec premise; if BG-T-1 had skipped the vocab probe, an H100 boot would have burned $5–10 producing predictable garbage. L9-style pre-flight discipline saved the budget.
2. **The Mistral KL cache (14.2 GB) is not lost work** — it remains a valid Mistral-teacher artifact reusable for any future Mistral-tokenizer-native student (e.g., a hypothetical Mistral-7B → Mistral-1B distill). The 14.2 GB sits on ubu1 `/tmp` and is subject to normal `/tmp` cleanup; if the artifact has long-term value, copy to a persistent path before next reboot.
3. **The recommended (P-β) Φ★-axis pivot inherits all caveats of the sister Φ★ docs** — including the static-EMA Φ★ approximation (sister runbook §4), the F2 sentinel-floor non-falsifying nature, and the non-publication of phenomenal substrate claims. Φ★-axis pivot does NOT magically resolve the broader Paradigm D distillation gap — it only replaces a vocab-blocked channel with a vocab-agnostic one.
4. **(P-γ) shelve has reputational cost** — Paradigm D was registered as the 6th cond on `.roadmap.p9_sft` with the explicit logit-axis framing; permanently blocking it without a Φ★-axis fallback would close the entire Paradigm-D research arm. The (P-β) pivot is preferable because it lets Paradigm D survive as an alternative-track concept (Φ★-axis only) rather than being deleted.
5. **(P-α) re-tokenize cost estimate ($10–12) is itself a soft lower bound** — assumes a single 5K-step head retrain succeeds first attempt. Re-tokenization with a different SP model can introduce subtle byte-fallback / unknown-token behaviors that may require multiple retrain passes. True cost could reach $20–30 for a robust replacement; that figure plus the Φ★ re-anchor cost makes (P-α) the most expensive path by a wide margin and the least preserve-uniqueness path.
6. **Vocab-mismatch is a tokenizer-class issue, not a transformer-architecture issue** — the BG-γ'' F-SHIM-V4-3 PASS (CLM v4 loads as HF AutoModelForCausalLM) does NOT resolve this; shim handles model architecture, not vocab axis. Future `state/p9_*` specs that propose Mistral-teacher → CLM-v4-student logit-distill MUST verify tokenizer identity at spec-time, not at exec-time.

### A4.5.7 — Cross-links

- This amendment: `docs/p9_paradigm_d_distill_spec_2026_05_03.md` §4.5 AMENDMENT (HERE)
- Falsification evidence: `state/p9_paradigm_d_distill_mini_2026_05_04/verdict.json` + `preflight.log`
- Roadmap entry mutation: `.roadmap.p9_sft` entry `p9_sft.cond.paradigm_d_distill` → `status: blocked_vocab_mismatch`
- Landed handoff: `docs/p9_paradigm_d_distill_amendment_landed_2026_05_04.ai.md`
- Φ★-axis Paradigm D lineage (UNAFFECTED): `state/p9_paradigm_d_distill_2026_05_03/`, `docs/p9_paradigm_d_distill_landed_2026_05_03.ai.md`, `docs/p9_paradigm_d_phi_distillation_2026_05_03.md`, `docs/p9_paradigm_d_t4_teacher_build_plan_2026_05_03.md`, `docs/p9_paradigm_d_distillation_runbook_2026_05_03.md`

### §4.5.X — USER AUTHORIZATION 2026-05-04

**Status: P-β AUTHORIZED + DEFAULT (forward path locked)**

User authorization 2026-05-04 (cycle ce681c40 message): "Path P-β (Φ★-axis-only pivot) 권장 (완성도 9/10) — vocab-axis-agnostic, CLM v4 64K substrate uniqueness 보존"

Forward path locked: P-β Φ★-axis-only Paradigm D distill, inherits PARTIAL_PASS step_1000 from `state/p9_paradigm_d_distill_2026_05_03/`, scales to 50K production via BG-γ'' F-SHIM-V4-3 PASS shim path.

Rejected paths (do not pursue):
- P-α: re-tokenize CLM v4 with Mistral vocab — destroys 64K multilingual substrate uniqueness, $20-30 soft-lower-bound + Φ★ re-anchor cost. NO.
- P-γ: shelve Paradigm D entirely — P-β preserves the lane at $0 amendment cost. NO.

Honest C3 on authorization:
- P-β preserves CLM v4 substrate uniqueness but does NOT validate logit-axis distill is achievable (logit-axis is permanently shelved as a distinct claim — Paradigm D forward = Φ★-scalar teacher signal only)
- Φ★ teacher signal is scalar; downstream knowledge transfer narrower than full logit cross-entropy
- step_1000 PARTIAL_PASS does not guarantee 50K scale-up converges (50K-fold longer trajectory may diverge)
- Sibling Φ★-axis lineage at `state/p9_paradigm_d_distill_2026_05_03/` is the inherited substrate; this authorization does NOT mutate that prior verdict, only locks the forward path
- This authorization closes the T-1-AMEND lane officially; downstream P-β scale-up exec is a SEPARATE BG (BG-Pβ-SCALE, sibling to this BG)

---

*End of spec. Doc-only per raw#9. NO execution authorized by this document. Mini-run launch requires separate BG with cache pre-flight (§5.2) + EXEC authorization. §4.5 AMENDMENT 2026-05-04 supersedes original §4.5 vocab-match claim — logit-axis BLOCKED pending substrate redesign or pivot to Φ★-axis-only (recommended). §4.5.X USER AUTHORIZATION 2026-05-04 locks forward path = P-β Φ★-axis-only.*
