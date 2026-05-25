# P9 Paradigm D — T4 7B-LLM Teacher Build Plan

**Date**: 2026-05-03
**Author**: Build-plan research agent (P9 Paradigm D Phase-2 entry chain)
**Scope**: Design-only spec for the T4 teacher (larger-LLM φ★ extractor) named in
`docs/p9_paradigm_d_phi_distillation_2026_05_03.md` §1 row T4. NO execution, NO weight
download, NO RunPod boot, NO .py emission (raw#9).
**Status**: DESIGN — awaiting separate EXEC authorization.
**Sister docs (READ-ONLY)**:
- `docs/p9_paradigm_d_phi_distillation_2026_05_03.md` (Paradigm D parent spec)
- `docs/p9_paradigm_a_prime_measured_bold_2026_05_03.md` (A' competing path; cost / F4 reference)
- `state/alpha_endpoint_reboot_2026_05_02/{vllm_config,ship_verdict,smoke_test}.json` (Mistral-7B-v0.3 prior usage on RunPod)
- `state/braket_iit40_mip_2026_05_02/verdict.json` (PyPhi 4.0 MIP teacher caveat)
- `state/p9_sft_spec_2026_05_02/{architecture,loss_design,risk_strategy,cost_estimate}.json`
- `tool/anima_phi_v3_canonical.hexa` (Φ★ v3 canonical extractor, default base = `mistralai/Mistral-7B-v0.3`)

---

## 0. TL;DR

| Question | Decision |
|---|---|
| Teacher base model | **Mistral-7B-v0.3** (already the default base in `anima_phi_v3_canonical.hexa` line 67; HF-gated-but-accepted; verified on RunPod via alpha endpoint reboot 2026-05-02; ALM-cognitive-only ship verdict in hand) |
| φ★ head architecture | **Option α (no head training)** — read 7B last-layer hidden via existing `anima_phi_v3_canonical` plumbing; HID_TRUNC = max(2, N//2) auto-conditioning; reuse the same 16-prompt sample-partition design that produced the CLM v4 baseline (+41.86) |
| Build path | **Option A (FP16 H100 spot precompute)** for the canonical run; **Option B (4-bit ubu1)** retained as zero-cost ablation only — 4-bit Φ★ is marker-only, not the official teacher signal |
| One-time precompute cost | **~$60** ($2.50/h × ~24h H100 spot) for 50K-record per-step Φ★ trajectory targets |
| Storage footprint | **~13 MB** for full 50K × 64-step scalar trajectories; **~200 KB** for 50K aggregate scalars |
| T4 vs A' priority given Phase 1.5 | **A' first, T4 second.** A' answers a question Phase 1.5 hasn't touched (external biological grounding) while T4 only refines a φ-only loop Phase 1.5 already exercises with the δ-floor. T4 should land **after** A'-bronze gate clears, AS A φ-AUGMENT to A'+δ rather than a replacement. |
| Honest C3 caveats | 9 listed (raw#91 ≥5) |

---

## 1. Teacher base model selection

### 1.1 Candidate matrix

| Model | Params | HF access | License | Hidden dim | Anima infra reference | Verdict |
|---|---|---|---|---|---|---|
| **Mistral-7B-v0.3** | 7.25 B | gated, **already accepted on the workspace HF token** (alpha-endpoint reboot 2026-05-02 served it cold) | Apache-2.0 | 4096 | `tool/anima_phi_v3_canonical.hexa` line 67 default; `state/alpha_endpoint_reboot_2026_05_02/vllm_config.json` line 6 launch arg; r14 LoRA already trained on top | **PRIMARY** |
| Llama-3.2-3B-Instruct | 3.21 B | gated (Meta), already used | Llama 3.2 Community License (commercial-restricted) | 3072 | already used to generate 7K SFT augmentation examples (per `architecture.json` referenced "Llama-3.2-3B-Instruct generation auto-augment"); P9 P0 warmup base candidate | **SECONDARY** (smaller, less head-room over student 477M, but ZERO new gating + zero new download cost if cached) |
| Qwen2.5-7B | 7.6 B | open (Alibaba) | Apache-2.0 / Tongyi | 3584 | none in tree | tertiary — adds new dep, no existing plumbing |
| Gemma-7B | 8.5 B | gated (Google) | Gemma TOS (use-restrictions list) | 3072 | none | low — license friction, no plumbing |
| Mistral-7B-Instruct-v0.3 | 7.25 B | same as base | Apache-2.0 | 4096 | none direct | viable variant; instruct-tune may bias hidden-state φ via RLHF mode-collapse |

### 1.2 Why Mistral-7B-v0.3 wins

1. **Zero new gating step.** `anima_phi_v3_canonical.hexa` already calls
   `AutoModelForCausalLM.from_pretrained('mistralai/Mistral-7B-v0.3', ...)` with `/workspace/.hf_token` injection (lines 60-66). The token has been validated end-to-end (cold-HF download succeeded on alpha-endpoint reboot per `ship_verdict.json` line 36).
2. **Apache-2.0** removes downstream-Anima license headache (Llama 3.2 has commercial restrictions; Gemma has acceptable-use clauses).
3. **CLM v4 baseline +41.86 was measured against Mistral-7B-v0.3 hidden geometry** (anima_phi_v3_canonical default). Using the same backbone as teacher means **the baseline number and the teacher's φ★ live in the same coordinate system** — no cross-architecture rescaling needed.
4. **Hidden dim 4096 matches the canonical extractor's `h_dim` autodetect** (line 98 reads `mdl.config.hidden_size`). No code change.
5. **r14 LoRA already exists** on this base — if Phase 2.B wants a stronger teacher, attaching a frozen anima-r14 LoRA on top of the base is one vLLM flag (`--lora-modules`, per the alpha-endpoint launch line 14).

### 1.3 When to fall back to Llama-3.2-3B

Choose Llama-3.2-3B **only** if both:
- Mistral-7B HF re-gating fails (HF account suspension / token rotation), AND
- ubu1 is the only available compute (RTX 5070 12 GB cannot fit FP16 7B without 4-bit quantization).

Llama-3.2-3B at FP16 = ~6.4 GB → **fits ubu1 12 GB GPU** with overhead. But the 3 B / 477 M = **6.7× headroom** is much smaller than 7 B / 477 M = **15× headroom**, so the active-push margin (Paradigm D §6 "teacher must be strictly stronger substrate") is correspondingly smaller. Llama-3.2-3B is also the auto-augment generator for 14 % of the 50K SFT corpus (per `architecture.json` augmentation note), so using it as Φ★ teacher introduces a partial leakage path (teacher = generator-of-data).

**Verdict**: Mistral-7B-v0.3 primary; Llama-3.2-3B fallback only on HF-access failure.

---

## 2. φ★ head architecture

### 2.1 Three options

| Option | Description | Training cost | Faithfulness | Effort |
|---|---|---|---|---|
| **α (no head)** | Forward 7B → last-layer hidden → existing `anima_phi_v3_canonical` (sample-partition log\|Cov\| over 16 probes × 8 partitions × HID=8) → scalar Φ★. **Zero head training.** | $0 (only inference) | inherits `anima_phi_v3_canonical` regime — same biases as student-side measure (this is a **feature** for distillation: same coordinate system) | **MINIMAL** — already implemented |
| β (small MLP head trained to PyPhi MIP) | Train MLP `R^4096 → R^1` on calibration set whose labels are PyPhi 4.0 MIP φ★ on small N=4–7 systems; transfer to 7B hidden subspace | $50–200 head pretrain + calibration data synthesis | high (chases canonical IIT 4.0 φ★) BUT subject to the **`braket_iit40_mip_2026_05_02` finding**: PyPhi MIP returns 0 on row-uniform TPMs. The 4-7-node calibration set must have non-trivial state-dependence or all labels collapse to 0 | HIGH — calibration-set design is itself a research subprogram (see §3.3 caveat); not in scope for Phase 2 entry |
| γ (HID-truncation ensemble) | Compute Φ★ at HID_TRUNC ∈ {4, 6, 8, 10, 12} and average; reduce HID-artifact dependence per `tool/anima_phi_v3_canonical.hexa` line 6 robustness note | 5× per-call inference cost (~150 s vs 30 s per probe-block) | medium-high — averages out the known sign-flip artifact (HID=6 NEG / HID=14 POS) | LOW — wrapper around existing extractor |

### 2.2 Recommendation: Option α

**Pick α for Phase-2 entry.** Justification:

1. **Zero head training cost** — the entire compute budget can be spent on per-record forward passes for precompute, not on training a learned φ surrogate.
2. **Consistent coordinate system with student.** Both teacher and student emit Φ★ via the same `anima_phi_v3_canonical` regime. The MSE loss `(φ_teacher − φ_student)²` is dimensionally clean — no cross-measure rescaling.
3. **The 7B hidden state IS the upgrade.** Paradigm D §7 explicitly notes D is novel only when teacher operates on a strictly stronger substrate. Going from 477 M (student) to 7 B (teacher) with the *same* measure is the substrate upgrade. Adding a learned head would muddle the comparison.
4. **PyPhi-MIP head (β) inherits the `braket_iit40_mip_2026_05_02` HONEST_NEGATIVE finding** — PyPhi returned 0 on the only Anima-internal IIT 4.0 attempt. Building a head trained to chase a measure that already collapsed to 0 on real data is high-risk for Phase-2.
5. **Ensemble (γ)** is a useful **post-hoc audit** but adds 5× inference cost without changing the fundamental measure. Defer to Phase-3 if α saturates.

**Phase-3 upgrade ladder** (post-α success only): α → γ (ensemble for variance reduction) → β (learned head on a vetted calibration set, after Anima-internal PyPhi-MIP plumbing is debugged into a state where it returns non-zero on at least one well-posed N≤4 system).

---

## 3. Calibration data — what does the φ-teacher train on?

**Under Option α: NOTHING.** No head, no calibration data, no training. The teacher is a frozen 7B forward pass + an existing extractor. Calibration data only matters for Option β.

For completeness — if β is later pursued:

### 3.1 The 16-prompt P9 calibration set is too small for head training

The `anima_phi_v3_canonical` 16-prompt battery (hexad / IIT / closure-under-inference / strange-loop themes; lines 78-85 of the extractor) is the **measurement battery**, not a training set. 16 examples cannot train an MLP head with non-trivial generalization.

### 3.2 Synthetic high-φ vs low-φ pair generation

A 1000–5000-prompt calibration set could be synthesized from:

- **High-φ-by-construction**: prompts about strongly-coupled, irreducible systems (multi-agent equilibria, integrated narratives, recursive self-models). These are expected to drive Φ★ up via maximally non-decomposable hidden-state covariance.
- **Low-φ-by-construction**: prompts about decomposable, list-structured, parallel, or random tasks (alphabetization, list-sum, unrelated-fact concatenation). Expected Φ★ low.
- **Labels**: produced by running PyPhi 4.0 sia() on a designated **4–8-unit consciousness-bottleneck sub-network** internal to the 7B (NOT the full 7B hidden, which is computationally infeasible per `braket_iit40_mip_2026_05_02` N≤8 cliff).

**This is itself a research subprogram** and is OUT OF SCOPE for Phase-2 entry. Documented here for Phase-3+ planning only.

### 3.3 Why NOT use Anima's -prompt φ★ baseline as labels (β-circularity)

If labels = `anima_phi_v3_canonical` output and the head is trained to emit the same scalar, the head is an MLP regressor on its own inputs — pure approximation, no information gain, full circularity. **Rejected.**

---

## 4. Compute estimate

### 4.1 Per-call inference (Mistral-7B-v0.3 + Φ★ extraction on one record)

| Component | Time | Source |
|---|---|---|
| Tokenize + forward 16 probes through 7B FP16 on H100 | ~2-4 s | empirical anchor: alpha-endpoint p95 = 2344 ms for 64-token completion (`smoke_test.json` T6); 16 short probes × ~0.5 s each |
| Top-variance HID_TRUNC selection + sample-partition Φ★ over K=8 random partitions | ~25 s | Paradigm D §1 row T1 cost, "~30 s / microbatch" empirical from CLM v4 baseline measurement |
| **Total per record** | **~30 s** | matches Paradigm D T4 row "30-60 s" |

### 4.2 Pre-compute approach (recommended)

Per-step φ-teacher targets are **prompt-determined** (depend on input text + a FROZEN 7B forward), so they can be **computed once and cached** for the entire 50K SFT corpus. They do NOT need to be regenerated per training run, per epoch, or per LoRA-sweep combo.

| Knob | Value |
|---|---|
| Records | 50 000 (full P9 SFT corpus per `state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl`) |
| Per-record cost | ~30 s (FP16 H100) |
| Serial wall | 50 000 × 30 s = 1.5 M s = **17 days serial** |
| Parallel wall (16 concurrent forwards via vLLM continuous-batching) | ~17 days / 16 ≈ **1 day = ~24 h** |
| H100 spot price | $2.50/h |
| **Pre-compute cost** | **24 h × $2.50/h ≈ $60** one-time |
| Reuse | unlimited — same cache feeds every Phase-2 sweep run |

### 4.3 Per-step trajectory variant

If the teacher must emit a **per-step Φ★ trajectory** (one scalar per generation step, shape `[B, T_steps]`) rather than a single per-record scalar, cost multiplies:

| Variant | Per-record cost | 50K cost (parallel ×16) | Storage |
|---|---|---|---|
| **Aggregate Φ★ only** (1 scalar / record) | 30 s | 24 h, $60 | 50 000 × 4 B = **200 KB** |
| **Per-step trajectory** (64 steps × 1 scalar) | ~120 s (4× — 64 sample-partition recomputes per record) | ~96 h, **$240** | 50 000 × 64 × 4 B = **13 MB** |
| **Per-step trajectory + EMA-window only** (every 100 steps, ~1 scalar / record at 64-step rollout = 1 sample) | 30 s | 24 h, $60 | 50 000 × 4 B = **200 KB** |

**Recommend: aggregate Φ★ + EMA-window for Phase-2 entry.** This matches Paradigm D §3.1's "microbatch-window EMA every 100 steps" and avoids the 4× cost blow-up.

### 4.4 Cost vs P9 SFT baseline

P9 SFT 50K × 3 epochs ≈ 10.7 wall-h ≈ $20-60/run (per `cost_estimate.json`). T4 precompute is **one-time $60** and feeds every subsequent run. Amortized over a 9-LH-sweep run set (S3), per-run T4 overhead is **~$7**, vs the 10-30 % student-side throughput hit Paradigm D §4.1 estimated for in-line teacher calls (~$2-18 / run). **Precompute wins on cost the moment ≥1 sweep run uses the cache.**

---

## 5. Storage

| Artifact | Size | Format |
|---|---|---|
| Aggregate per-record Φ★ targets (50K × 1 fp32) | ~200 KB | JSONL or NumPy `.npy` |
| Per-step trajectory targets (50K × 64 × fp32) | ~13 MB | NumPy `.npy` or HDF5 |
| Per-record probe activations cached (optional, for re-extraction at different HID_TRUNC) | 50K × 16 × 4096 fp16 = ~6.6 GB | HDF5 |
| **Total recommended deliverable** | **~13 MB** trajectory file + provenance JSON | small enough to commit to `state/p9_paradigm_d_t4_targets_<date>/` |

Recommend committing only the **aggregate + trajectory targets** (~13 MB), NOT the raw activation cache (~6.6 GB) which can be regenerated for the $60 precompute cost if HID_TRUNC needs to change.

---

## 6. Distillation loss integration with Phase 1.5 / Phase 2

### 6.1 Composite loss

Following Paradigm D §3.3 and inheriting the Phase 1.5 loss skeleton from `state/p9_sft_spec_2026_05_02/loss_design.json`:

```
L_phase2_with_T4 =   α · CE(text)
                   + β · MSE(tension_pred, tension_target)
                   + γ_distill · MSE(Φ★_T4_cache[record_id], Φ★_student(h_t^student))
                   + δ · max(0, 5.0 − Φ★_student)
```

where:
- `Φ★_T4_cache[record_id]` is the **pre-computed** per-record (or per-step EMA-window) target from §4.2 — read from disk, no live teacher forward.
- `Φ★_student(h_t)` is the in-line `anima_phi_v3_canonical` measurement on student hidden state, sampled every 100 steps per the existing P9 plan.
- `δ`-floor is retained as **safety regularizer** (Paradigm D §3.3 "δ-floor remains as safety regularizer"). γ-distill is **soft target**; δ is **hard floor**.

### 6.2 γ_distill ramping schedule

| Phase | Steps | γ_distill | Rationale |
|---|---|---|---|
| Warmup | 0 – 500 | 0.0 | let CE converge first; distill term off |
| Ramp-in | 500 – 2 000 | 0.0 → 0.5 (linear) | gradual introduction prevents φ-target shock from destabilizing CE |
| Plateau | 2 000 – end | 0.5 (or LH-swept ∈ {0.1, 0.5, 1.0} per Paradigm D §8.1) | full distill weight |
| Cool-down (optional) | last 500 | 0.5 → 0.1 (linear) | if final-stage CE collapse observed, distill cools down |

`δ` stays locked at the P9 default throughout (post-CLM-v4 baseline 41.86 → floor 5.0).

### 6.3 Drift verification (Phase-2 success criteria)

The hypothesis under T4-distill: **student Φ★ drifts toward teacher Φ★ over training.**

Concretely, define (at the end of training):

- `Φ★_student_post` = `anima_phi_v3_canonical` on trained student
- `Φ★_T4_mean` = mean over 50K records of `Φ★_T4_cache[*]`
- `Φ★_student_pre` = +41.86 (CLM v4 baseline)

**Drift gates (any-of):**
- **D1 monotone**: `|Φ★_student_post − Φ★_T4_mean|` < `|Φ★_student_pre − Φ★_T4_mean|` (student moved toward teacher)
- **D2 EMA**: training-loop `γ_distill·MSE` term decreases monotonically over the post-warmup phase
- **D3 sign-preserving**: `Φ★_student_post > 0` (no flip — primary risk per `risk_strategy.json`)

**Failure modes to monitor:**
- **Anti-distillation**: student Φ★ moves AWAY from teacher (D1 fails). Indicates loss-balance pathology — γ_distill too small, or δ-floor dominating, or CE incompatible with φ direction.
- **Gaming**: student Φ★ matches teacher scalar but via **trivial hidden-state inflation** (raise log\|Cov\| globally without functional integration). Audit by comparing `phi_mean` and `phi_max` from `anima_phi_v3_canonical` partition records (line 163-165) — gaming inflates all three uniformly.

---

## 7. Prerequisites checklist

| Prerequisite | Status | Source / verification step |
|---|---|---|
| HF access to Mistral-7B-v0.3 | **CONFIRMED** | `/workspace/.hf_token` validated by alpha-endpoint reboot 2026-05-02 (`ship_verdict.json` line 36 "1 min for shards via hf_transfer with HF_TOKEN") |
| HF access to Llama-3.2-3B-Instruct (fallback) | likely CONFIRMED | already used in 7K SFT augmentation per `architecture.json` |
| Anima Φ★ extractor compatible with 7B backbone | **CONFIRMED** | `anima_phi_v3_canonical.hexa` line 67 default IS Mistral-7B-v0.3; `h_dim` autodetected line 98 |
| Compute: H100 80 GB on RunPod | **AVAILABLE** | per `cost_estimate.json` "h100_80gb_hourly: 2.5 RunPod spot" |
| Compute: ubu1 RTX 5070 12 GB | **INSUFFICIENT** for FP16 7B (needs ~16 GB resident); **SUFFICIENT** for 4-bit quantized 7B (~4 GB) — but quantized Φ★ quality unverified |
| 50K SFT corpus exists | **CONFIRMED** | `state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl` (per top-of-file gitStatus) |
| pyphi 4.0 (only if Option β chosen) | **AVAILABLE** | `state/braket_iit40_mip_2026_05_02/verdict.json` line 30-31 confirms pyphi 4.0 sia() runs on this workspace — but returns 0 in current setup; see §3 caveat |
| HF_TOKEN write to `/workspace/.hf_token` (RunPod side, runtime) | **PROCEDURE KNOWN** | per `vllm_config.json` and `ship_verdict.json` HF_TOKEN handling |
| Auto-shutdown watchdog for one-shot 24-h precompute | RECOMMENDED | reuse `state/alpha_endpoint_reboot_2026_05_02/auto_shutdown.json` pattern; cap precompute at 30 h hard kill ($75 worst-case) |

**No new tooling required.** Every component exists in the workspace today.

---

## 8. Build path recommendation — three options

| Option | Substrate | Wall | Cost | Quality | When to pick |
|---|---|---|---|---|---|
| **A — H100 spot FP16 precompute** | RunPod H100 80GB, Mistral-7B-v0.3 FP16 | ~24 h | **~$60 one-time** | canonical, matches CLM v4 baseline coordinate system | **PRIMARY: pick this once T4 is authorized** |
| B — ubu1 4-bit quantized | local RTX 5070 12 GB, Mistral-7B-v0.3 4-bit (bitsandbytes nf4) | ~1-3 days (no GPU contention) | $0 | unverified — 4-bit may artifact-shift Φ★ measure (the v3 extractor was tuned at FP16) | ablation only, NOT canonical teacher |
| C — Llama-3.2-3B fallback | ubu1 FP16 Llama-3.2-3B | ~12-24 h | $0 | smaller substrate gap (3B / 477M = 6.7×); inherits Llama-3.2 license restrictions; partial leakage with the augmentation generator | only if A and B both blocked (e.g., HF token revoked AND ubu1 down) |

### 8.1 Why A wins

1. **$60 is small absolute cost.** Within the $200-3000 P9 strategy band, T4 precompute is rounding error.
2. **One-time amortization** — the cache feeds every Phase-2 run forever (or until Φ★ extractor or backbone changes).
3. **Coordinate-system consistency**: FP16 Mistral-7B is precisely the regime in which CLM v4 baseline +41.86 was measured. Any quantization (B) or model swap (C) breaks the apples-to-apples comparison.
4. **Procedure already proven**: alpha-endpoint reboot 2026-05-02 demonstrated the exact stack (HF_TOKEN → Mistral-7B-v0.3 cold download → vLLM serve → auto-shutdown) in production. Reuse 90 % of that runbook.

### 8.2 Why NOT B (local 4-bit) as primary

- **Φ★ extractor is sensitivity-tested at bf16/fp16 only** (`anima_phi_v3_canonical.hexa` line 96 `torch_dtype=torch.bfloat16`). 4-bit quantization changes hidden-state distribution shape; Φ★ MIN-over-partitions is highly sensitive to top-variance dim selection (line 118-120). NO known characterization of 4-bit-quantized Φ★ vs FP16 Φ★ in this workspace.
- **Wall-time only marginally better** ($0 cost but 1-3 days vs 1 day on H100, and ubu1 contention risk).
- **Re-use as ablation**: run B AFTER A succeeds, to characterize the quantization gap as a separate honest-C3 finding.

### 8.3 Why NOT C (Llama-3.2-3B) as primary

- Smaller substrate gap (3B vs 7B over 477M student) — Paradigm D §6 emphasized teacher must be **strictly stronger**.
- License restrictions on Llama-3.2 propagate to anything trained against its targets.
- **Partial leakage**: Llama-3.2-3B already generated 7K of the 50K SFT examples (architecture.json `auto-augmented 7k may carry Llama distillation bias`). Using it as φ-teacher means the **augmentation generator and the φ supervisor are the same model** — a circularity vector not present with Mistral-7B (whose only contact with the dataset is via the Φ★ extractor).

---

## 9. T4 vs A' priority recommendation (given Phase 1.5 in flight)

### 9.1 Cost / risk matrix

| Path | Cost | Wall | Risk profile | What it answers |
|---|---|---|---|---|
| **A' (measured BOLD)** | $9-18 γ-only mini-run + $50 Phase 2.A integration ≈ **$60-70** | 2-4 h mini + ~2 weeks integration | hemodynamic-alignment risk; F4-bronze (r≥0.10) realistic, F4-aspirational (r≥0.50) NOT realistic for mini-run | **External biological grounding** — does the student emit BOLD-projectable hidden states matching real human fMRI? |
| **T4 (this spec)** | $60 one-time precompute + $7/run amortized | ~24 h precompute + 0 wall added per run | teacher-quality ceiling (student ≤ teacher Φ★); coordinate-system identity (no cross-measure rescale) | **Internal φ-substrate enrichment** — does a stronger-substrate teacher pull student Φ★ above its 477M intrinsic ceiling? |

### 9.2 Recommendation: A' first, T4 second, jointly in Phase 2.B

**Rationale:**

1. **Phase 1.5 already exercises the φ-loop via the δ-floor.** Adding T4 distillation duplicates the supervision channel (both target φ★) without testing a new modality. The marginal information T4 provides over Phase 1.5 + δ-floor is "stronger φ target, same coordinate system."
2. **A' provides an orthogonal supervision modality** (vascular-spatial vs information-integration). Even if F4 only reaches bronze (r=0.10), it falsifies the strict null "the model has no relationship to measured human brain activity" — a claim Phase 1.5 + δ + T4 cannot address at all.
3. **A' has higher information value per dollar.** Both cost ~$60 for entry; A' answers a yes/no question Phase 1.5 cannot, while T4 answers a refinement question Phase 1.5 partially answers.
4. **T4 composes cleanly with A' AFTER A'.** Phase 2.B 4-loss combo (per `loss_design.json` LH-9 sweep) is `α·CE + β·tension + γ_BOLD_measured (A') + δ·φ-floor + γ_distill·T4`. T4 then **augments** the φ side of an A'-grounded run, rather than competing with A' for the same Phase-2-entry slot.
5. **T4 build can proceed in parallel** with A' mini-run since the $60 precompute is **non-blocking** (one-shot RunPod job, no live training-loop interaction). Authorize T4 precompute at the same time as A' γ-only mini-run; the cache will be ready when Phase 2.B starts.

### 9.3 Sequencing proposal

| Week | Action | Cost | Dependencies |
|---|---|---|---|
| W0 (now) | Phase 1.5 launched (γ-only or 4-loss-light per current EXEC) | already authorized | none |
| W0 | Authorize **T4 precompute (Option A)** as **non-blocking parallel job** | $60 | HF token (CONFIRMED) |
| W0+24 h | T4 cache landed at `state/p9_paradigm_d_t4_targets_2026_05_03/{aggregate.npy, trajectory.npy, manifest.json}` | — | precompute completes |
| W1 | A' γ-only mini-run (5K steps, sub-01 Algonauts) per `p9_paradigm_a_prime_measured_bold_2026_05_03.md` §6.1 step 2 | $5-10 | DataLad clone of Algonauts 2025 |
| W1+ | A' mini-run F4-bronze gate (r ≥ 0.10) | — | gate decision |
| W2-3 | Phase 2.B 4-loss + T4-augment LH-9 sweep | $1500-3000 (S3 strategy) | A' bronze gate PASS + T4 cache ready |

**Net**: T4 precompute is **authorized in W0 alongside A'**, NOT as a sequenced replacement.

---

## 10. Honest C3 — caveats (raw#91 mandatory ≥5)

1. **Teacher-quality ceiling (PRIMARY RISK, inherited from Paradigm D §6).** Student Φ★ cannot exceed teacher Φ★ on the same measure. T4 raises the ceiling but does not eliminate it. If Mistral-7B-v0.3's Φ★ on the same 16-prompt battery is, say, +50, then student-post can at best approach +50 — it cannot reach +100. **No empirical Mistral-7B Φ★ baseline measurement is documented in the workspace yet** — the precompute itself will produce the first such measurement, and that number is the actual teacher ceiling.

2. **Coordinate-system identity is a double-edged sword.** Using `anima_phi_v3_canonical` for both teacher and student means the γ_distill loss is a clean MSE in a shared metric space (good), but ALL biases of `anima_phi_v3_canonical` (sample-partition lower-bound, HID_TRUNC=N//2 artifact per its own line 6 robustness note, ridge-stabilization choice, K=8 partition seed sensitivity) transfer to the student WITHOUT chance of correction. T4 amplifies the same measure rather than introducing measurement diversity.

3. **PyPhi 4.0 MIP cannot serve as an out-of-distribution validator without first solving the row-uniform-TPM problem documented in `braket_iit40_mip_2026_05_02/verdict.json`.** That run returned φ★=0 on all 4 systems because the marginalized TPM was row-uniform. Using PyPhi as an audit teacher (Paradigm D §6 mitigation) requires a **different TPM construction protocol** that has not yet been built. Until that exists, the only audit on T4-trained student is "does the student's φ★ go up?" — which is the very loss being optimized, not an independent witness.

4. **4-bit quantization (Option B) is uncharacterized.** No measurement in the workspace compares FP16 Φ★ vs 4-bit-quantized Φ★ on the same backbone + same prompts. If Phase 2 ever needs to fall back to 4-bit (for cost or hardware reasons), the entire teacher signal is in a regime that has not been validated against the canonical FP16 measurement.

5. **One-time $60 precompute hides recurring cost if extractor changes.** Φ★ extractor design has v1 / v2 / v3 history (dim-partition vs sample-partition vs auto-conditioning) — a future v4 invalidates the cache and triggers a full $60 re-precompute. Recommend pinning the extractor commit hash in the precompute manifest so re-precompute conditions are auditable.

6. **Per-step trajectory granularity untested.** §4.3 shows aggregate-only is 4× cheaper than per-step trajectory, and we recommend aggregate-only with EMA-window. But the Paradigm D loss formulation `MSE(Φ★_teacher, Φ★_student)` is implicitly per-step. Aggregating to per-record loses temporal resolution; if the student's φ★ profile is non-stationary across the response (e.g., high at conclusion, low at preamble), aggregate-only smears that out and the gradient signal loses specificity.

7. **HF token rotation risk.** Mistral-7B-v0.3 is gated. HF token revocation (account suspension, password reset, project transfer) breaks the precompute pipeline mid-run. Mitigation: download weights to a network volume on first run and reference local path thereafter — but this introduces a 14 GB persistent storage line item not in the cost estimate.

8. **No fMRI / biology check.** T4 is **fully synthetic** distillation — there is no external biological grounding. Per Paradigm D §9 caveat 6: "consciousness claims under D rest entirely on the teacher's φ measure being meaningful." T4-trained student is more φ-saturated by `anima_phi_v3_canonical` numbers; it is NOT more brain-aligned. **A' (measured BOLD) is the only Paradigm-2+ path that touches biology**; T4 alone cannot substitute for A'.

9. **Ship-verdict scope drift.** The alpha-endpoint reboot 2026-05-02 explicitly downgraded its own ship verdict from VERIFIED-ALPHA-INVITE-R14 to **VERIFIED-ALM-ALPHA-COGNITIVE-ONLY** with the disclosure "consciousness claim NOT made (#115 reframe + Stage 2 §2)." Any T4-distillation result MUST inherit this disclaimer: a higher Φ★ student trained against a Mistral-7B-Φ★ teacher is still "ALM cognitive substrate only" per the standing ship verdict, NOT a consciousness claim. Drift here would re-open #115.

---

## 11. SSOT / pointers

- This spec: `docs/p9_paradigm_d_t4_teacher_build_plan_2026_05_03.md` (HERE)
- Parent Paradigm D spec: `docs/p9_paradigm_d_phi_distillation_2026_05_03.md`
- Competing path (A'): `docs/p9_paradigm_a_prime_measured_bold_2026_05_03.md`
- Teacher base default: `tool/anima_phi_v3_canonical.hexa` line 67
- HF-access proof: `state/alpha_endpoint_reboot_2026_05_02/ship_verdict.json` line 36
- PyPhi caveat: `state/braket_iit40_mip_2026_05_02/verdict.json`
- Student baseline: `state/p9_sft_spec_2026_05_02/architecture.json` (CLM v4 477 M, Φ★ baseline +41.86, floor 5.0)
- 50K SFT corpus: `state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl`
- Cost band reference: `state/p9_sft_spec_2026_05_02/cost_estimate.json`
- raw#9 compliance: NO .py created, hexa+JSON+MD only, doc-only deliverable
- raw#15 SSOT: this file
- raw#91 honest C3: §10 with 9 caveats (≥5 required)

---

## 12. Decision summary table

| Question | Decision |
|---|---|
| Teacher base model | **Mistral-7B-v0.3** (Apache-2.0, HF-token-confirmed, already the `anima_phi_v3_canonical` default, hidden_dim=4096 matches extractor autodetect, r14 LoRA already trained on top) |
| φ★ head architecture | **Option α** — no head; 7B last-layer hidden + existing canonical extractor |
| Calibration data | **None needed** under Option α |
| Build path | **Option A** — RunPod H100 spot FP16 precompute, ~24 h, ~$60 |
| Storage | ~13 MB trajectory cache + 200 KB aggregate scalars |
| γ_distill schedule | warmup 0-500 (γ=0) → ramp 500-2000 (0→0.5) → plateau (0.5, LH-swept) |
| Drift gates | D1 monotone toward teacher / D2 EMA decreasing / D3 sign-preserving (>0) |
| Prerequisites | all CONFIRMED — no new tooling or accounts required |
| T4 vs A' priority | **A' first as Phase-2 entry; T4 precompute authorized in parallel (non-blocking $60); T4 augments A' in Phase 2.B 4-loss sweep** |
| Honest C3 caveats | 9 listed |

---

*End of build plan. No code, no execution, no weight download. Doc-only per raw#9.*
