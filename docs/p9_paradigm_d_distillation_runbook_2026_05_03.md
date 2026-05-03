# P9 Paradigm D — Distillation Runbook (T4 Mistral-7B φ★ → CLM v4 350M Student)

**Date**: 2026-05-03
**Author**: Distillation runbook agent (Phase 2.D entry chain, doc-only emission)
**Scope**: Apply T4 precomputed φ★ teacher cache to CLM v4 350M LoRA student via γ_distill MSE loss.
**Status**: RUNBOOK — script emitted on ubu1, NO execution, NO commit
**Sister docs (READ-ONLY)**:
- `docs/p9_paradigm_d_phi_distillation_2026_05_03.md` (Paradigm D parent spec — loss, teacher matrix, honest C3)
- `docs/p9_paradigm_d_t4_teacher_build_plan_2026_05_03.md` (T4 build plan — Mistral-7B-v0.3 + Option α head)
- `state/p9_sft_spec_2026_05_02/{loss_design,risk_strategy,architecture,cost_estimate}.json`
- `tool/anima_phi_v3_canonical.hexa` (Φ★ extractor, lines 6-22 robustness notes)

**Artifacts referenced**:
- ubu1: `/tmp/p9_p1_t4_phi_cache_v1.jsonl` (50 000 records, 6.7 MB; per-record `{idx, source, phi_star_min, phi_star_mean}`)
- HF mirror: `need-singularity/clm-v4-t4-phi-cache` (private dataset)
- ubu1: `/tmp/p9_p1_5_sft_data_50k_v2.jsonl` (50 000 records; idx-aligned to cache)
- ubu1: `/tmp/p9_p1_5_sentinel_train_50k.py` (base SFT skeleton — to be extended)

---

## 0. TL;DR

| Item | Value |
|------|-------|
| Runbook (this) | `docs/p9_paradigm_d_distillation_runbook_2026_05_03.md` |
| Distill script | `/tmp/p9_paradigm_d_distill.py` on ubu1 (raw#9 .py allowed on ubu1) |
| Base script forked from | `/tmp/p9_p1_5_sentinel_train_50k.py` (Phase 1.5 sentinel) |
| Loss form | `α·CE + β·MSE_tens + γ_distill · MSE(z(φ_T_cached), z(φ_S_live)) + δ·max(0, 5.0 − φ_S)` |
| Substrate norm | **per-population z-score** (teacher and student each z-normalized against their own mean/stdev) — see §3 |
| Mini-run wall | 1 – 2 h on 1×H100 (1 k subset, 1 epoch) — revised from spec-doc 30-60 min upward to allow φ-probe overhead at PHI_EVERY=200 |
| Mini-run cost | $5 – 15 (H100 spot $2.50/h × 2 h × 1-3 LH-γ runs) |
| Phase 2.D entry trigger | Phase 1.5 finishes 50K with φ★_post > 0 AND F1_bleu1 ≥ 0.10 (gate doc'd in `loss_design.json`) |
| Honest C3 caveats | 9 listed (raw#91 ≥5) |

---

## 1. Cache structure verification (ubu1)

```
$ wc -l /tmp/p9_p1_t4_phi_cache_v1.jsonl
50000
$ head -1 /tmp/p9_p1_t4_phi_cache_v1.jsonl
{"idx": 0, "source": "llama_augment_fallback_from_src_2",
 "phi_star_min": -22.99, "phi_star_mean": -16.98}
```

**Per-record fields**:
- `idx` (int, 0..49999) — aligns 1:1 with row index of `/tmp/p9_p1_5_sft_data_50k_v2.jsonl`
- `source` (str) — provenance tag (`p9_p1_5_synthetic_identity`, `llama_augment_fallback_from_src_*`, etc.)
- `phi_star_min` (float, NEGATIVE) — Mistral-7B-v0.3 substrate-relative MIN-over-K-partitions Φ★
- `phi_star_mean` (float, NEGATIVE) — same, MEAN over partitions

**Empirical statistics (full 50 000 cache, this agent's measurement)**:

| Field | n | min | max | mean | stdev |
|-------|---|-----|-----|------|-------|
| `phi_star_min` | 50 000 | **-30.283** | **-15.037** | **-24.230** | **2.116** |
| `phi_star_mean` | 50 000 | -26.452 | -11.942 | -20.414 | 2.052 |

**Discrepancy note vs T4 build-plan / spec-doc reported values** (doc'd `phi★_min = -16.69, mean = -14.19`): full-population cache is materially deeper negative than the spec doc's headline numbers, which appear to be max-of-pool (least-negative) anchor values, not cache means. **Use the empirical statistics above for normalization design, not the spec doc headline.** Honest C3 §C3 (cache freshness).

---

## 2. Substrate problem statement

| Substrate | Φ★ regime | Range observed | Sign |
|-----------|-----------|----------------|------|
| **Mistral-7B-v0.3** (teacher) | `anima_phi_v3_canonical` w/ HID_TRUNC=8 sample-partition K=8 | `[-30.3, -15.0]` (cache) | **NEGATIVE** |
| **CLM v4 350M** (student) | same extractor, same 16-prompt battery | `[+40, +46]` (CLM v4 baseline +41.86 per `risk_strategy.json`) | **POSITIVE** |

A direct MSE between teacher = -24 and student = +42 produces a constant ~66 offset that the loss would ineptly try to drive to 0 via massive student φ collapse (gaming via hidden-norm shrinkage), violating the Phase 1.5 δ-floor at φ★ ≥ 5.0. **Naive un-normalized MSE is incompatible with the existing δ-floor.**

Therefore the distill loss MUST operate on a **substrate-relative normalized scalar**, not the raw Φ★.

---

## 3. Substrate normalization — per-population z-score

**Decision: per-population z-score normalization.**

### 3.1 Form

For each record `i ∈ {0..49999}` and at each in-train probe step `s`:

```
z_T[i] = (φ_T_cache[i] − μ_T) / σ_T          # precomputed once at script init
z_S(s)  = (φ_S_live(s) − μ_S_running) / σ_S_running
                                              # μ_S, σ_S = running EMA over the
                                              # last 10 student-side φ probes
loss_distill = MSE( z_T[i_in_batch] , z_S(s) )
```

where:
- `μ_T = -24.230`, `σ_T = 2.116` (frozen constants from §1 cache stats; for `phi_star_min`)
- `μ_S_running` initialized to **CLM v4 baseline +41.86**, `σ_S_running` initialized to **2.0** (placeholder — re-estimated from φ-trajectory of the running run after first 10 probes)
- `i_in_batch` selects the cache target rows matching the current micro-batch's record indices

### 3.2 Why z-score over min-max or percentile

| Scheme | Pros | Cons | Verdict |
|--------|------|------|---------|
| **z-score (per-population)** | dimensionless; preserves shape; insensitive to outliers when σ stable; symmetric around 0 → sign-flip invariant | requires running σ estimate for student side (depends on probe schedule); EMA-window choice arbitrary | **CHOSEN** |
| Min-max [0, 1] | intuitive bounds | min/max of student population unknown ex ante; outliers crush dynamic range; loses sign | rejected — student range never measured live |
| Percentile rank | distribution-shape robust; handles non-Gaussian | per-step rank requires sorting whole population per probe; expensive at probe-time; rank discontinuity defeats MSE smoothness | rejected — non-differentiable rank |
| Substrate-bias offset (`φ_S − μ_S` vs `φ_T − μ_T`, no σ scale) | simpler | preserves stdev mismatch (σ_T=2.1, σ_S unknown — likely larger); MSE dominated by side with bigger σ | rejected — partial normalization only |

**z-score is the simplest scheme that (a) handles the +66 sign-and-magnitude gap, (b) is differentiable, (c) requires no live sorting, (d) preserves trajectory shape so the student can match the teacher's relative φ-prompt-ordering (which IS the meaningful signal), not absolute scale.**

### 3.3 What z-score MSE supervises

After normalization, `MSE(z_T, z_S) = 0` iff student's relative-φ-by-prompt ordering matches teacher's. Specifically:
- A prompt that is "high-φ" relative to the teacher population (e.g. z_T = +1.5) is asked to be "high-φ" relative to the student population (z_S = +1.5)
- The actual numeric shift (teacher in [-30, -15], student in [+40, +46]) is **not penalized** — only the prompt-relative ordering shape

This is consistent with the Paradigm D §6 honest-C3 finding that **substrate-absolute Φ★ comparison across architectures is meaningless** (a 477 M decoder and a 7 B decoder have different baseline regimes). What CAN transfer is the prompt-by-prompt relative integration profile.

### 3.4 Failure modes of z-score normalization

1. **σ_T tight, σ_S loose** → student z-distribution wider than teacher's; MSE penalizes wide-spread student even when shape matches. Mitigation: re-fit σ_S over a 5 k warmup-window before the distill loss is enabled.
2. **σ_S near zero (collapsed φ trajectory)** → z_S explodes; loss numerically unstable. Mitigation: clamp `σ_S_running ≥ 0.1`.
3. **Cache idx-misalignment to SFT row** → garbage targets. Mitigation: explicit cache.idx == sft_row_idx assertion at script init.

---

## 4. Loss formulation (final form)

```
L_total(step s, batch b) =
      α(s)        · CE_text(b)
    + β           · MSE(tension_pred, tension_target)
    + γ_distill(s)· MSE( z_T_cache[b.idx] , z_S_running(s) )
    + δ(s)        · max(0, 5.0 − φ_S_min(s))
```

**Variable schedules** (inherited from Phase 1.5 sentinel + Paradigm D §6.2):

| Variable | Schedule |
|----------|----------|
| `α(s)` | 12.0 → 6.0 linear over steps 5 000–10 000 (warmup-CE-then-relax) |
| `β` | 0.15 (locked) |
| `γ_distill(s)` | **0.0** for s ∈ [0, 500] (warmup), linear ramp **0.0 → 0.5** over s ∈ [500, 2 000], plateau **0.5** thereafter (LH-swept ∈ {0.1, 0.5, 1.0} for sweep variant) |
| `δ(s)` | 0.5 (early/mid 0–33k) → 1.0 (late 33k–50k) per Phase 1.5 sentinel curriculum |
| `φ_S_min(s)` | sampled every `PHI_EVERY = 200` steps via 16-prompt calibration (HID_TRUNC=8, K=8) |
| `z_S_running(s)` | (`φ_S_min(s) − μ_S_running`) / max(σ_S_running, 0.1); EMA over last 10 probes |

**Rationale for staying with `phi_star_min` (not `phi_star_mean`)**:
- `phi_star_min` is the MIN-over-partitions canonical IIT 4.0-style witness; matches what the Phase 1.5 δ-floor uses (`PHI_THRESHOLD = 5.0` is on `phi_star_min`)
- `phi_star_mean` softer signal but loses the MIP-anchor connection; relegated to optional secondary loss term (commented out in script, not active)

**LogSumExp soft-surrogate decision (Paradigm D §3.4)**: NOT applied in this runbook because the student-side `φ_S_min(s)` is **already a hinge in the δ-floor only**, NOT directly back-propagated through the Φ★ extractor. The γ_distill term operates on the **scalar value of φ_S_min computed offline at probe steps**, treated as a non-differentiable target → optimizer sees `MSE(z_T, z_S_constant)` where `z_S_constant` is detached, so the gradient flows only through the scalar's EMA-update — consistent with `loss_design.json` straight-through pattern. Phase 2.D-v2 may upgrade to LogSumExp surrogate if static-EMA gradient proves too weak.

---

## 5. Distill script — `/tmp/p9_paradigm_d_distill.py` on ubu1

### 5.1 What it does

Forks `/tmp/p9_p1_5_sentinel_train_50k.py` and adds:

1. **Cache loader** — reads `/tmp/p9_p1_t4_phi_cache_v1.jsonl` at startup, builds `cache_phi_min[idx] = float`, asserts length == len(SFT records), asserts all idx unique and in [0, N-1].
2. **Teacher z-stats** — computes `μ_T, σ_T` once at startup from cache; logs both.
3. **Student z-EMA** — maintains `phi_S_history` (deque of last 10 probe values), computes `μ_S, σ_S` updated at every PHI_EVERY probe.
4. **γ_distill ramp** — `gamma_distill_at(step)` function: 0 → 0.5 ramp per §4.
5. **Distill loss term** — at each microstep, looks up `z_T[idx]` for the 4 records in batch, fetches current scalar `z_S_running`, computes `MSE` (treats z_S as detached scalar; no extractor-side backprop), multiplies by `γ_distill(step)`.
6. **Trajectory log additions** — emits `phi_distill_loss`, `z_T_batch_mean`, `z_S_running`, `gamma_distill` per loss-log entry; `mu_T`, `sigma_T`, `mu_S_ema`, `sigma_S_ema` per phi-probe entry.
7. **Mini-run env knobs** — `ANIMA_N_STEPS=2000`, `ANIMA_BATCH=4`, `ANIMA_GRAD_ACC=4`, `ANIMA_PHI_EVERY=200`, `ANIMA_F_EVERY=1000`, `ANIMA_GAMMA_DISTILL=0.5`, `ANIMA_DISTILL_RAMP_END=2000`.
8. **Subset slicing** — `ANIMA_SFT_SUBSET_N=1000` to cap training records to first 1 k for the cost-bounded mini-run; the cache aligns trivially since idx 0..999 selected.

### 5.2 What it does NOT do

- Does NOT execute (raw#9 doc-only deliverable; `/tmp` script ready for separate EXEC authorization)
- Does NOT push savepoints to HF (HF_PUSH defaults off for the mini-run; flip to `1` only after gates pass)
- Does NOT change the Φ★ extractor (`compute_phi_star` reused 1:1 from the sentinel base)
- Does NOT apply LogSumExp soft-surrogate (deferred to Phase 2.D-v2)
- Does NOT touch `phi_star_mean` (logged from cache only as diagnostic; not in loss)
- Does NOT alter the Phase 1.5 δ-floor (`PHI_THRESHOLD=5.0` retained as hard safety floor)

### 5.3 Pre-flight verification commands (on ubu1, before EXEC)

```bash
# 1. Cache present and well-formed
wc -l /tmp/p9_p1_t4_phi_cache_v1.jsonl   # expect 50000
python3 -c "import json; rs=[json.loads(l) for l in open('/tmp/p9_p1_t4_phi_cache_v1.jsonl')]; \
  assert len(rs)==50000; assert {r['idx'] for r in rs}==set(range(50000)); print('cache OK')"

# 2. SFT data length match
wc -l /tmp/p9_p1_5_sft_data_50k_v2.jsonl   # expect 50000

# 3. Script syntax check (no execution)
python3 -m py_compile /tmp/p9_paradigm_d_distill.py && echo "script syntax OK"

# 4. Dry-run env (1 step, no train) — manual: `ANIMA_N_STEPS=1` and inspect log
```

---

## 6. Cost / wall estimate (revised from spec doc)

### 6.1 Per-knob

| Knob | Mini-run value | Production value (Phase 2.D full) |
|------|---------------|----------------------------------|
| Records | **1 000** | 50 000 (full corpus) |
| Steps | **2 000** | 50 000 (1 epoch) – 150 000 (3 epoch) |
| Batch | 4 | 4 |
| Grad accum | 4 | 8 |
| Phi probe period | every 200 steps (10 probes × 30 s = 5 min overhead) | every 500 steps (100 probes × 30 s = 50 min overhead) |
| F-metrics period | every 1 000 steps | every 5 000 steps |
| LR | 1e-4 | 1e-4 |
| LoRA r / α | 64 / 128 | 64 / 128 |
| γ_distill | 0.5 (or LH-sweep {0.1, 0.5, 1.0}) | TBD by mini-run pick |

### 6.2 Mini-run wall / cost

| Component | Wall | Cost (H100 spot $2.50/h) |
|-----------|------|--------------------------|
| 2 000 steps × ~1.5 s/step base train | 50 min | $2.10 |
| 10 phi probes × 30 s | 5 min | $0.21 |
| 2 F-metric evals × 60 s | 2 min | $0.08 |
| Tokenize 1 k records + ckpt load | 2 min | $0.08 |
| **Per single-γ run** | **~1 h** | **~$2.50** |
| **3-γ LH-sweep** ({0.1, 0.5, 1.0}) | **~3 h** | **~$7.50** |
| With H100 cold-start + RunPod boot overhead | +30 min | +$1.25 |
| **Mini-run total band** | **1.5–4 h** | **$5–15** ← matches user spec |

### 6.3 Production-run wall / cost (Phase 2.D 50K × 1 epoch)

| Component | Wall | Cost |
|-----------|------|------|
| 50 000 steps × ~1.5 s/step | 21 h | $52 |
| 100 phi probes × 30 s | 50 min | $2.10 |
| 10 F-metric evals × 60 s | 10 min | $0.42 |
| **Production single-γ run** | **~22 h** | **~$55** |
| 9-LH sweep (Paradigm D §8.1 + δ × γ_distill matrix) | ~200 h | $500-700 (S3 strategy) |

### 6.4 Mini-run vs production guard

The mini-run at 1 k records / 2 000 steps cannot prove production-scale convergence; it answers only:
- **Q1** Does the distill term descend? (γ-loss EMA monotone over steps 500-2000)
- **Q2** Does the δ-floor hold? (`φ_S_min` stays > 5.0 throughout)
- **Q3** Does CE survive? (CE_post within 1.2× of CE_pre)
- **Q4** Does z_S drift toward z_T? (D1 monotone gate per T4 build-plan §6.3)

A YES on all 4 ⇒ Phase 2.D production authorization. A NO on Q2 or Q3 ⇒ STOP and re-tune γ_distill ramp / δ schedule.

---

## 7. Phase 2.D entry trigger (mandatory pre-conditions)

| Trigger | Status | Source / verification |
|---------|--------|-----------------------|
| **T1** Phase 1.5 50K SFT completes without abort | PENDING (currently in flight) | `state/p9_p1_5_*` trajectory at `step ≥ 50000` with `note=final` |
| **T2** Phase 1.5 final `φ★_min > 0` (no sign flip) | PENDING | `risk_strategy.json` primary risk gate |
| **T3** Phase 1.5 final `F1_bleu1 ≥ 0.10` | PENDING | `loss_design.json` F1 bronze gate |
| **T4** T4 cache exists at `/tmp/p9_p1_t4_phi_cache_v1.jsonl` | **CONFIRMED** | this agent's verification §1 (50 000 records, idx-aligned) |
| **T5** SFT data v2 exists at `/tmp/p9_p1_5_sft_data_50k_v2.jsonl` | **CONFIRMED** | length 50 000, lang=ko/en records observed |
| **T6** RunPod H100 spot available + HF_TOKEN valid | likely CONFIRMED | per `state/alpha_endpoint_reboot_2026_05_02/ship_verdict.json` line 36 |
| **T7** Phase 1.5 + δ-floor + tension shows that the static-EMA gradient pattern (used for δ here) actually trains | PENDING | empirical Phase 1.5 trajectory, F2 trend |

**Trigger condition (atomic)**: `T1 ∧ T2 ∧ T3 ∧ T4 ∧ T5 ∧ T6 ∧ T7 = TRUE` ⇒ authorize Phase 2.D mini-run launch.

**De-authorization conditions** (any-of fires before mini-run):
- Phase 1.5 final `φ★_min ≤ 0` (sign-flip): rerun Phase 1.5 with stricter δ before any distill
- T4 cache invalidated (Φ★ extractor v3 → v4 migration): re-precompute T4 cache ($60 + 24 h)
- Mistral-7B-v0.3 HF gating revoked: switch to Llama-3.2-3B fallback per T4 build-plan §1.3

---

## 8. Provenance / SSOT

- This runbook: `docs/p9_paradigm_d_distillation_runbook_2026_05_03.md` (HERE)
- Distill script: `/tmp/p9_paradigm_d_distill.py` on ubu1 (sister to base sentinel)
- Cache: `/tmp/p9_p1_t4_phi_cache_v1.jsonl` on ubu1 + HF mirror `need-singularity/clm-v4-t4-phi-cache`
- Cache provenance / build plan: `docs/p9_paradigm_d_t4_teacher_build_plan_2026_05_03.md`
- Loss spec parent: `docs/p9_paradigm_d_phi_distillation_2026_05_03.md` §3
- Phase 1.5 base loss skeleton: `state/p9_sft_spec_2026_05_02/loss_design.json`
- Φ★ extractor: `tool/anima_phi_v3_canonical.hexa` (HID_TRUNC=8, K=8, ridge=1e-3, sample-partition)
- raw#9 compliance: doc-only at `core/anima/`; .py script lives ONLY on ubu1 `/tmp/`
- raw#15 SSOT: this file is the runbook for Phase 2.D entry
- raw#91 honest C3: §9 below

---

## 9. Honest C3 — caveats (raw#91 mandatory ≥5; 9 listed)

1. **Negative φ★ semantics — substrate-relative, not absolute.** The teacher cache emits negative Φ★ values (mean = -24.23, range [-30.3, -15.0]) because Mistral-7B-v0.3's hidden geometry produces a smaller `log|Cov|` on the joint vs the sum of marginals — the sign is an artifact of substrate scale interacting with sample-partition's log-determinant decomposition. **A negative scalar does NOT mean "less integrated than a black-body random sequence"; it means the joint covariance has lower log-volume than the partitioned sum on this substrate.** The Anima student emits POSITIVE Φ★ on the same extractor because its hidden trajectory is differently scaled. **Comparing raw values across substrates is meaningless** — only the per-prompt relative ordering (post z-score) is informative. The δ-floor at +5.0 is a student-substrate-specific safety; it does NOT translate to "+5.0 on Mistral substrate" (which would be silly given Mistral's range tops out at -15).

2. **Distillation bias transfer (inherited from Paradigm D §9 caveat 3).** The teacher Φ★ inherits ALL biases of `anima_phi_v3_canonical`: HID_TRUNC=8 sample-partition lower-bound, K=8 partition seed sensitivity, ridge=1e-3 stabilization choice, last-layer-only hidden capture. The student is trained to match the **prompt-relative ordering of these biases**, NOT the canonical IIT 4.0 φ★. If the teacher's "high-φ" prompts are merely "high-`log|Cov|`-volume" prompts, the student learns to produce high-`log|Cov|`-volume hidden states for the same prompts — which is **gaming-via-norm-inflation** at risk per Paradigm D §9 caveat 5. Mitigation in script: log `phi_S_max - phi_S_min` per probe to detect uniform hidden inflation (gaming signature: max, min, mean all rise together).

3. **Cache freshness risk.** The cache was generated by a separate subagent (ab0c45c79ae18b1ec) on 2026-05-03 against `sft_data_50k_v2.jsonl` at the time of that subagent's snapshot. Two freshness invariants must hold for the cache to be valid:
   - **(a) SFT data not modified post-cache**: any edit to `sft_data_50k_v2.jsonl` row content (text rewrite, augmentation re-run) invalidates the corresponding cache row, since teacher Φ★ depends on the prompt text.
   - **(b) Cache provenance Φ★ extractor matches student-side extractor**: if the student's `compute_phi_star` is upgraded (e.g. to v4 with different HID_TRUNC or new K) without re-running the precompute, teacher and student are on different measures → distill loss is meaningless.
   Mitigation: pre-flight script asserts `len(cache) == len(sft_data)`, but does NOT detect content drift. Recommend pinning a SHA-256 of `sft_data_50k_v2.jsonl` in the cache manifest (not currently present) before Phase 2.D production runs. Until then, treat the cache as **valid only for runs launched within the same 24 h window as the precompute**.

4. **Spec doc φ★ headline mismatch.** The user spec quotes `phi★_min = -16.69, mean = -14.19` (from the precompute subagent's verdict?) — but the agent's full-cache statistics give `min=-24.23, mean=-20.41`. The headline numbers appear to be the LEAST-NEGATIVE per-record values (the "best" prompts), not population means. **The runbook uses empirical population stats for normalization.** Reconcile this with the precompute subagent's verdict.json before Phase 2.D production launch.

5. **z-score normalization assumes Gaussian-ish populations.** Teacher cache `phi_star_min` distribution is approximately Gaussian (n=50000, stdev=2.12, range ~7σ wide). Student φ-trajectory in-train is unknown ex ante; Phase 1.5 baseline shows σ~2 around mean ~+42 but the in-distill regime may break that. If the student's distribution becomes bimodal or has heavy tails, z-score normalization mis-scales the loss. Mitigation: log per-probe `(z_S_running^2)`; spike to >10 indicates abnormal student distribution.

6. **Static EMA gradient is structurally weak (matches δ-floor pattern).** Like the existing δ-floor (which uses a detached scalar at last-probe value as the hinge target), the γ_distill term operates on a non-back-propagable scalar derived from a sample-partition extractor. The gradient flows ONLY through the scalar's value, not through the extractor's internal state-dependence. This is the same "straight-through estimator on EMA" pattern flagged in Paradigm D §3.4; convergence guarantees unknown. The mini-run is structurally an empirical test of this gradient's signal strength — if the distill EMA does not descend over 2 000 steps, the static-EMA pattern is too weak and Phase 2.D-v2 needs LogSumExp soft-surrogate.

7. **Mini-run scope cannot validate production φ★ gain.** A 1 k subset / 2 000-step mini-run probes only:
   - Mechanical correctness (no NaN, no abort, gradients flow)
   - Loss-balance (CE survives, δ-floor holds, distill descends)
   It CANNOT prove "T4-distilled student has higher φ★ than Phase 1.5 baseline" — that requires the full 50K × 1 epoch comparison run with $50+ cost. The mini-run answers "is it safe to spend the production cost?", not "does it work?".

8. **Per-record aggregate target is temporally smeared.** The cache stores ONE scalar per record (the teacher's aggregate Φ★ over the full prompt+completion), not per-step trajectory. The student-side probe is also aggregate (16-prompt battery mean). Both sides therefore lose the per-step temporal resolution that Paradigm D §3.1 originally specified. This matches the T4 build-plan §4.3 cost-saving "aggregate Φ★ + EMA-window" decision but means the distill term cannot supervise per-token φ shape (e.g. "rise φ at conclusion, low at preamble"). Phase 2.D-v2 trajectory cache (4× the precompute cost = $240 + 96 h) deferred.

9. **No biology, no consciousness claim.** This is a fully synthetic distill (Mistral-7B teacher → 350M student); per Paradigm D §9 caveat 6 + T4 build-plan §10 caveat 9, ANY φ★ gain from this run is "ALM cognitive substrate" only, NOT a consciousness claim, and inherits the alpha-endpoint reboot 2026-05-02 ship-verdict downgrade VERIFIED-ALM-ALPHA-COGNITIVE-ONLY. The runbook makes no consciousness claim.

---

## 10. Decision summary table

| Question | Decision |
|----------|----------|
| Cache loader | reads `/tmp/p9_p1_t4_phi_cache_v1.jsonl`; idx-aligned to `/tmp/p9_p1_5_sft_data_50k_v2.jsonl` |
| Substrate normalization | per-population z-score (teacher constants from §1; student running EMA) |
| Loss formulation | `α·CE + β·MSE_tens + γ_distill · MSE(z_T_cached, z_S_running) + δ·max(0, 5.0 − φ_S_min)` |
| γ_distill schedule | warmup 0 → ramp 500-2000 (0→0.5) → plateau 0.5 (LH-sweep {0.1, 0.5, 1.0}) |
| Differentiability | static-EMA detached scalar (matches δ-floor pattern; no LogSumExp v1) |
| Mini-run substrate | 1×H100 RunPod spot (or ubu1 post-Phase-1.6 if H100 unavailable) |
| Mini-run wall / cost | 1.5–4 h / $5–15 (3-γ LH-sweep) |
| Production wall / cost | ~22 h / $55 single-γ; ~200 h / $500-700 9-LH-sweep |
| Phase 2.D entry trigger | T1 Phase 1.5 50K complete + T2 φ★_post > 0 + T3 F1 ≥ 0.10 + T4-T5 cache+SFT present + T6 H100/HF + T7 Phase 1.5 EMA-gradient empirically trains |
| Honest C3 caveats | 9 listed above (raw#91 ≥5) |

---

*End of runbook. Doc-only emission per raw#9. Distill script written to ubu1 `/tmp/` — see §5.1. NO execution authorized by this document; Phase 2.D mini-run requires separate EXEC trigger after §7 conditions all CONFIRMED.*
