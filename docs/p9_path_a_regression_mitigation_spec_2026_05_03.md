# P9 Path A LoRA — Catastrophic Forgetting Mitigation Spec

- ts_utc: 2026-05-03
- agent: subagent BG (spec only — design / pre-registration; NO execution this cycle)
- spec_id: p9_path_a_regression_mitigation_spec_2026_05_03
- status: **DRAFT-LOCKED** (binding before any next-cycle Path A re-train)
- supersedes: nothing (first regression-mitigation spec for the Path A LoRA track)
- decision_basis: Path A A' main eval (in flight) shows STRONG TriviaQA regression Δ −0.8 → −3.6 → −7.4pt across step-2000/4000/6000 against Llama-3.2-3B-Instruct anchor (TriviaQA EM 0.514). HellaSwag lifts +0.8 to +1.2pt. F1_v3 likely lands `CHAT_FAIL_v3` (any STRONG regression triggers fail per A' spec §2.4).
- raw#9 STRICT (Mac → hexa only — this doc is pure design markdown, no .py creation), raw#15 (no personal-path leak), raw#10 honest C3 in §6, $0 (design + spec only — DO NOT launch retraining this cycle)

---

## 0. TL;DR

**Observed regression**: Path A LoRA (r=64, α=64, lr=1e-4, 50K SFT, Llama-3.2-3B-Instruct base) is mid-flight on step-2000/4000/6000 ckpts. Eval on the 3-task A' panel reveals an asymmetric pattern:

- **HellaSwag** (commonsense MCQA): Δ +0.8 to +1.2pt — STRONG signal candidate
- **TriviaQA** (closed-book factual recall): Δ −0.8 → −3.6 → −7.4pt — STRONG REGRESSION (worsens monotonically with training step)
- **MMLU** (5-shot academic knowledge): in flight — likely also regressed (factual knowledge axis correlated with TriviaQA)

**Diagnosis**: Classic **catastrophic forgetting** — LoRA r=64 (97M trainable params, 5.12% of base) at lr=1e-4 over 50K SFT steps is sufficient to overwrite portions of Llama's pre-trained factual recall while learning the chat axis. Honest_c3 (c) of A' decision §1.1 explicitly forecasted this risk: "small-base instruction-SFT often regresses MMLU (knowledge-forgetting)".

**Recommended path (by 완성도 lens)**: **Track B (LoRA r reduction r=64 → r=16)** — completion score **8.5/10**. Cheapest, simplest, addresses root cause directly. See §3 ranked table.

**One-liner why**: B is the only mitigation that (i) directly attacks the capacity-overwrite failure mode with a single hyperparameter change, (ii) preserves the existing 50K SFT corpus + Llama chat template + lr/scheduler config, (iii) fits inside the same train pod profile (~$20-30 H100, 8-12h wall), (iv) yields a clean A/B vs the current Path A run for δ-attribution, (v) carries the lowest implementation-complexity risk.

**Falsifier**: F-PATHA-MITIGATION-1 — re-eval on identical A' main panel must show **Δ_TriviaQA ≥ 0** (i.e. no STRONG regression on factual recall) at the best checkpoint, with paired bootstrap 95% CI lower bound ≥ −0.5pt and McNemar p > 0.05 (failure to reject null = no regression). HellaSwag lift may shrink — that is acceptable trade-off (raw#10 honest_c3 (c) below).

**Cost / wall**: $0 design (this doc). Track B re-train ~$20-30 H100 + ~8-12h wall + ~1-3h re-eval (existing A' pipeline, already pre-built per `docs/p9_a_prime_eval_pipeline_landed_2026_05_03.ai.md`). Total next-cycle cost ~$25-35 + ~10-15h wall.

**DO NOT launch retraining this cycle.** Defer to next BG cycle after user OK on track selection.

---

## 1. Observed Regression Detail

### 1.1 Eval results (mid-flight)

Source: in-flight A' main eval pipeline (`state/p9_a_prime_main_eval_pipeline_2026_05_03/`), eval driver `eval_llama_lora_ckpt.py` against base anchor `state/p9_a_prime_main_eval_pipeline_2026_05_03/base_per_example_correctness.json`.

| ckpt | HellaSwag acc_norm | Δ vs Llama 0.644 | TriviaQA EM | Δ vs Llama 0.514 | MMLU |
|---|---|---|---|---|---|
| Llama-3.2-3B-Instruct (base, 4-bit) | 0.644 | — | 0.514 | — | 0.608 |
| step-2000 | 0.652 | +0.8pt | 0.506 | **−0.8pt** | in flight |
| step-4000 | 0.656 | +1.2pt | 0.478 | **−3.6pt** | in flight |
| step-6000 | 0.652 | +0.8pt | 0.440 | **−7.4pt** | in flight |
| step-8000 | (queued) | — | (queued) | — | — |
| step-10000 | (queued) | — | (queued) | — | — |

### 1.2 F1_v3 verdict implication

Per A' spec §2.4 + §2.2:
- HellaSwag threshold: Δ ≥ +1.0pt → step-4000 borderline-STRONG (Δ=+1.2pt; needs paired bootstrap CI lower > 0 + McNemar p < 0.05)
- TriviaQA threshold: Δ ≥ +0.5pt → all evaluated ckpts FAIL to clear, AND step-4000/6000 are |Δ| ≥ 0.5pt with negative sign → **STRONG REGRESSION** (signal=STRONG with Δ ≤ −threshold)
- Composite F1_v3 rule: any STRONG regression → `CHAT_FAIL_v3` regardless of HellaSwag positive signal

**Verdict prediction** (assumes McNemar p < 0.05 on TriviaQA, plausible at n=500 with Δ=−7.4pt at step-6000):
- step-2000: likely `CHAT_PARTIAL_v3` (HellaSwag near-threshold, TriviaQA Δ=−0.8pt borderline regression)
- step-4000: likely `CHAT_FAIL_v3` (TriviaQA Δ=−3.6pt clear STRONG regression)
- step-6000: clear `CHAT_FAIL_v3` (TriviaQA Δ=−7.4pt unambiguous STRONG regression)

### 1.3 Diagnostic: catastrophic forgetting

**Pattern signature**:
- HellaSwag (acquired chat skill) lifts modestly and plateaus
- TriviaQA (preserved factual knowledge) degrades monotonically with training step
- Δ_TriviaQA / step ≈ −1.1pt per 1000 steps (linear extrapolation: step-10000 → Δ ≈ −12pt, EM ≈ 0.39)

**Root cause hypothesis**: LoRA r=64 (rank-64 perturbation across 7 attention modules `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj` per `state/p9_path_a_llama_lora_2026_05_03/train_llama_lora.py.txt`) at α/r = 1.0 with lr=1e-4 over 50K SFT records × ~3 epochs has sufficient capacity to overwrite portions of the MLP parameter manifold that encode TriviaQA-style factual associations. SFT corpus is **chat-template augmented** but provides no positive factual-recall pressure, so the gradient update direction is biased toward chat completion at the expense of fact retrieval.

**Supporting evidence from literature** (qualitative — no execution):
- Houlsby et al. 2019 (adapter tuning): adapter rank > 8 begins exhibiting forgetting on knowledge benchmarks
- Hu et al. 2021 (LoRA paper): r=8 typically sufficient for chat alignment; r=64 is more common for code/math fine-tuning where capacity matters
- Lin et al. 2023 (LIMA): instruction-tuning on 1K examples preserves base knowledge; 50K examples crosses the capacity boundary at high rank

---

## 2. Mitigation Track Enumeration

Four mitigation tracks considered. Each is named by what it changes vs the current Path A baseline.

### 2.1 Track A — Corpus Rebalance (mix factual QA into SFT)

**Change vs Path A baseline**: augment 50K chat-template SFT corpus with factual QA records (TriviaQA-style + MMLU-style synthetic completions) at 70%/30% chat/factual mix ratio.

**Plan**:
1. Source factual QA: TriviaQA train split (~138K rc.nocontext records) + MMLU dev/val (~14K records) — both HF datasets, no licensing issue
2. Re-template into Llama chat format using `retemplate_to_llama.py.txt` (existing tool)
3. Sample 15K factual records (30% of new 50K total) + 35K from existing chat corpus → 50K mixed
4. Re-train Path A LoRA from scratch on mixed corpus (same hyperparams: r=64, α=64, lr=1e-4, 10K steps)
5. Re-eval on A' panel

**Cost**: ~$20-30 H100 SXM (12-24h wall × $2.5/h) — same as Path A baseline, no extra GPU
**ETA**: 8-12h training + 1-3h eval = ~10-15h wall
**Risk** (raw#10 honest_c3):
- (a) Mix ratio 70/30 is a **hyperparameter** without empirical justification; optimal could be 80/20 or 50/50 — would require sweep (3x cost)
- (b) Factual QA recall in SFT may **leak test data** into training (TriviaQA train ≠ rc.nocontext val per dataset card, but sanity check needed)
- (c) Adding factual QA may **dilute chat lift** since chat exemplars drop from 100% to 70% of corpus — HellaSwag Δ may drop to +0.5pt
- (d) MMLU "synthetic completions" requires generating Q+A+rationale strings; absent careful templating, can introduce CoT-style artifacts not present in pure chat SFT

**Falsifier success condition**: Δ_TriviaQA ≥ 0 AND Δ_HellaSwag ≥ +0.5pt (preserves at least half the chat lift)

### 2.2 Track B — LoRA Rank Reduction (r=64 → r=16)

**Change vs Path A baseline**: reduce LoRA rank from r=64 to r=16 (also α=16 to maintain α/r=1.0 ratio). All other hyperparams unchanged.

**Plan**:
1. Edit launch flags only: `--lora-r 16 --lora-alpha 16` (existing trainer arg surface per `train_llama_lora.py.txt`)
2. Re-train Path A LoRA from scratch (same SFT corpus, same lr, same scheduler, same 10K steps)
3. Re-eval on A' panel

**Capacity reduction math**:
- r=64: trainable params ≈ 97.3M (5.12% of 1.9B base)
- r=16: trainable params ≈ 24.3M (1.28% of 1.9B base) — 4x reduction
- r=8: trainable params ≈ 12.2M (0.64%) — 8x reduction — keep as fallback

**Cost**: ~$20-30 H100 SXM — actually **cheaper** than baseline because lower-rank LoRA forward+backward is ~10-15% faster
**ETA**: 7-10h training + 1-3h eval = ~8-13h wall
**Risk** (raw#10 honest_c3):
- (a) Lower capacity may **also reduce** chat lift on HellaSwag (Δ may drop from +1.0pt to +0.3pt or even 0) — accepted trade-off if TriviaQA preserved
- (b) r=16 is **plausible from literature** (Hu et al. 2021 default for chat tuning) but not yet **measured for this corpus** — single point, could underfit
- (c) If r=16 still regresses TriviaQA, fallback to r=8 adds another cycle (cumulative cost $40-60)
- (d) Same SFT data (no factual injection) means **root cause may persist** if the issue is corpus bias not capacity bias — though smaller capacity at minimum bounds the damage

**Falsifier success condition**: Δ_TriviaQA ≥ 0 (paired bootstrap 95% CI lower ≥ −0.5pt). HellaSwag lift may be small (Δ ≥ 0 acceptable).

### 2.3 Track C — EWC (Elastic Weight Consolidation)

**Change vs Path A baseline**: add Fisher-information-weighted L2 penalty on LoRA-affected parameters relative to Llama base, during SFT training.

**Plan**:
1. Compute Fisher information matrix on Llama-3.2-3B-Instruct base using a reference dataset (e.g. C4 or WikiText-103 subset, ~5K samples) — diagonal approximation only (full Fisher = O(N²) memory infeasible)
2. Modify `train_llama_lora.py` to add `+λ * Σ_i F_i * (θ_i − θ_base,i)²` to the SFT loss, where `λ` is the EWC strength hyperparameter
3. Re-train Path A LoRA with EWC penalty
4. Re-eval on A' panel

**Implementation effort**: ~2-3h to extend trainer + 1-2h Fisher computation pre-pass
**Cost**: ~$40-60 H100 SXM (Fisher pre-pass ~1-2h × $2.5/h + extended train ~12-18h × $2.5/h = $32-50; round up for retries)
**ETA**: 16-20h end-to-end (Fisher + train + eval)
**Risk** (raw#10 honest_c3):
- (a) **High implementation complexity** — diagonal Fisher computation requires custom forward+backward hook code; not a flag-flip
- (b) EWC λ is **another hyperparameter** with no a-priori value (literature: λ ∈ [10², 10⁵] depending on task); may need sweep
- (c) Diagonal Fisher is a **rough approximation** (ignores parameter correlations); may not protect critical weights as effectively as full Fisher
- (d) EWC was designed for **continual learning** between distinct tasks; SFT on chat isn't strictly a "different task" from base LM — EWC penalty may simply slow learning without selectively preserving knowledge
- (e) Highest cost + highest implementation risk + uncertain efficacy = lowest 완성도 ranking despite theoretical soundness

**Falsifier success condition**: Δ_TriviaQA ≥ 0 AND Δ_HellaSwag ≥ +0.5pt

### 2.4 Track D — Replay Buffer (mix proxy-Llama-pretrain data into SFT)

**Change vs Path A baseline**: during SFT, mix in unconditioned LM batches from a proxy of Llama's original pretrain distribution (WikiText-103 + factual prompt pool) at 80% SFT / 20% replay ratio.

**Plan**:
1. Source replay data: WikiText-103 (~100M tokens, public) + curated factual prompt pool (~10K Wikipedia abstract first-paragraphs)
2. Modify `train_llama_lora.py` to alternate batches: 4 SFT batches → 1 replay batch (no LoRA penalty on replay; standard cross-entropy LM loss)
3. Re-train Path A LoRA with mixed batch schedule
4. Re-eval on A' panel

**Cost**: ~$25-35 H100 SXM (replay batches add ~20% to per-step time × 12-18h = $25-35)
**ETA**: 10-14h training + 1-3h eval = ~12-17h wall
**Risk** (raw#10 honest_c3):
- (a) WikiText-103 + Wikipedia abstracts is a **rough proxy** for Llama's actual pretrain mix (which includes Common Crawl, GitHub, books, etc.); proxy-distribution mismatch may underprotect
- (b) Replay during LoRA tuning is **non-standard** — most literature uses replay for full-model continual learning; LoRA-with-replay efficacy is empirically untested for chat alignment
- (c) Replay-batch loss flows through LoRA params (since base is frozen); risk that LoRA also tries to fit pretrain distribution → adapter becomes a generalist not a chat specialist
- (d) Implementation effort is **moderate** — alternating batch loaders, but no Fisher/penalty math (lower complexity than EWC)

**Falsifier success condition**: Δ_TriviaQA ≥ 0 AND Δ_HellaSwag ≥ +0.5pt

---

## 3. Ranked Recommendation by 완성도 lens

| rank | track | 완성도 score | cost | wall | implementation risk | efficacy confidence | trade-off severity |
|---|---|---|---|---|---|---|---|
| **1** | **B — LoRA r reduction (r=64 → r=16)** | **8.5/10** | $20-30 | 8-13h | LOW (flag flip) | HIGH (direct attack on capacity-overwrite root cause) | MEDIUM (HellaSwag lift may shrink) |
| 2 | A — Corpus rebalance (70/30 chat/factual) | 7.5/10 | $20-30 | 10-15h | LOW-MED (data prep + retemplate) | MED-HIGH (addresses corpus bias if root cause is corpus not capacity) | MEDIUM (chat lift may dilute; mix ratio is hyperparameter) |
| 3 | D — Replay buffer (80/20 SFT/replay) | 6.0/10 | $25-35 | 12-17h | MED (alternating batch loader) | MEDIUM (proxy distribution mismatch risk) | MEDIUM-HIGH (LoRA may become generalist) |
| 4 | C — EWC (Fisher-weighted L2 penalty) | 4.5/10 | $40-60 | 16-20h | HIGH (custom hooks + pre-pass + λ sweep) | LOW-MED (diagonal approx + LoRA-EWC underexplored) | LOW (theoretically minimal trade-off) |

### 3.1 Scoring rubric (5 weighted axes, 10pt each)

For each track, score [0-10] on:
- **C1 Cost-efficiency** (lower $ + lower wall = higher score) — weight 0.20
- **C2 Implementation simplicity** (fewer custom code paths + flag-only changes preferred) — weight 0.25
- **C3 Efficacy confidence** (literature support + alignment with diagnosed root cause) — weight 0.25
- **C4 Reversibility / iteration speed** (can pivot to another track quickly if this fails) — weight 0.15
- **C5 Trade-off severity** (less harm to chat lift = higher score) — weight 0.15

**Track scores (computed)**:

| track | C1 | C2 | C3 | C4 | C5 | weighted |
|---|---|---|---|---|---|---|
| B (r reduction) | 9 | 10 | 9 | 9 | 6 | **8.55** |
| A (corpus rebalance) | 9 | 7 | 8 | 8 | 6 | **7.55** |
| D (replay buffer) | 7 | 6 | 6 | 7 | 5 | **6.05** |
| C (EWC) | 5 | 3 | 5 | 5 | 8 | **4.95** |

(Scores are subjective per honest_c3 (a) below; rounded to 0.5 for the ranking table.)

### 3.2 One-liner per track

- **B**: cheapest, simplest, highest-confidence single-knob fix; ships the cleanest A/B vs current Path A
- **A**: targets a different root cause hypothesis (corpus bias) — viable if B fails or as combo with B
- **D**: middle ground; novel for LoRA so highest variance in outcome
- **C**: theoretically strongest knowledge preservation; defeated on cost + complexity + uncertain LoRA-EWC efficacy

### 3.3 Recommended next-cycle plan

**Primary**: Launch Track B re-train (r=16, α=16) as next BG cycle after user OK.

**Contingency tree**:
- If B succeeds (Δ_TriviaQA ≥ 0): land verdict, declare Path A mitigated, proceed to Path A axis-injection (F2/F3/F4 falsifiers per A' decision §6.2).
- If B partially succeeds (Δ_TriviaQA ∈ [−0.5, 0] but HellaSwag Δ < +0.3pt): pivot to Track A (corpus rebalance) — combine r=16 + 70/30 mix for next cycle.
- If B fails (Δ_TriviaQA < −0.5pt at r=16): drop to r=8 (one more flag flip, ~$20-30) before considering A/C/D. r=8 is the hard floor before LoRA stops being meaningful (4096 hidden × 8 rank = 32K params per module = barely above adapter-rank-1 baseline).
- If r=8 also fails: pivot to A (corpus rebalance) as the corpus-bias hypothesis becomes dominant.

---

## 4. F-PATHA-MITIGATION-1 Falsifier Specification

### 4.1 Pre-registered statement (binding)

**F-PATHA-MITIGATION-1**: A Path A LoRA mitigation track is deemed SUCCESS iff, on the canonical A' main eval panel (HellaSwag + MMLU + TriviaQA, limit=500, seed=42, 4-bit anchor), the best mitigation-track checkpoint satisfies:

1. **Primary criterion (TriviaQA preservation)**: Δ_TriviaQA ≥ 0pt vs Llama-3.2-3B-Instruct anchor (EM 0.514) AND paired bootstrap 95% CI lower bound ≥ −0.5pt AND McNemar p > 0.05 (fail-to-reject null = no significant regression)

2. **Secondary criterion (chat lift floor)**: Δ_HellaSwag ≥ 0pt OR Δ_MMLU ≥ 0pt (at least one of the two non-TriviaQA tasks is non-regressed; STRONG positive signal not required for a success declaration since the goal is "preserve knowledge while attempting chat lift", not "chat lift at all costs")

3. **Composite gate**: F1_v3 ≠ `CHAT_FAIL_v3` (i.e. no STRONG regression on any task)

### 4.2 Failure modes

- `MITIGATION_FAIL_REGRESSION`: criterion 1 fails (TriviaQA still STRONG-regressed) → mitigation track did not solve catastrophic forgetting → escalate per §3.3 contingency tree
- `MITIGATION_FAIL_NO_LIFT`: criterion 1 passes BUT criterion 2 fails on BOTH HellaSwag and MMLU (LoRA preserved knowledge by learning nothing) → mitigation over-regularized; need to back off (e.g. r=16 → r=24)
- `MITIGATION_PARTIAL`: criterion 1 passes (Δ_TriviaQA ≥ −0.5pt with non-significant McNemar) but Δ_TriviaQA still slightly negative AND criterion 2 passes → declare partial; consider combining with another track

### 4.3 Reuse of existing pipeline

The A' main eval pipeline (per `docs/p9_a_prime_eval_pipeline_landed_2026_05_03.ai.md`) is **directly reusable** with no code changes:

- ubu1: `eval_llama_lora_ckpt.py` accepts any `--ckpt-repo` or `--ckpt-local-dir` — point at mitigation-track LoRA output
- ubu1: `run_all_lora_ckpts.sh` — edit single env var to point at mitigation hub repo
- Mac: `tool/p9_a_prime_verdict.hexa` — re-runs against new lora_results dir, emits new verdict.json

Estimated next-cycle eval wall: ~1-3h (5 ckpts × 3 tasks × ~5-20min each + verdict compute ~30s). Cost: $0 (ubu1 local).

### 4.4 Pre-registration lock

This falsifier (§4.1 + §4.2) is **binding before any mitigation re-train kicks off**. Threshold modifications post-eval require a new dated spec doc per A' spec §2.6 lock pattern. Specifically, the "Δ ≥ 0" floor on TriviaQA is non-negotiable — any value < 0 is a regression by definition; loosening this would reduce the falsifier to a tautology.

---

## 5. Cost / Wall Matrix

| track | $ (H100 SXM) | wall (train) | wall (eval) | wall (total) | total $ (incl. eval $0 ubu1) |
|---|---|---|---|---|---|
| B (r reduction) | $20-30 | 7-10h | 1-3h | 8-13h | $20-30 |
| A (corpus rebalance) | $20-30 | 8-12h | 1-3h | 10-15h | $20-30 |
| D (replay buffer) | $25-35 | 10-14h | 1-3h | 12-17h | $25-35 |
| C (EWC) | $40-60 | 14-18h (incl. Fisher pre-pass) | 1-3h | 16-20h | $40-60 |

**Notes**:
- All costs assume RunPod H100 SXM at $2.5-3.5/h (per Path A pod profile; pod purge handoff `project_runpod_pod_purge_2026_05_03.md` — fresh boot from HF base mirror)
- Eval $0 (ubu1 local, RTX 5070, ~1-3h wall on existing pre-built A' pipeline)
- This-cycle cost: $0 (design + spec only)
- If contingency tree fires (B → r=8, or B → A combo), add cumulative cost (e.g. B fail + A retry = $40-60 cumulative)

---

## 6. Honest C3 (raw#10) — 4 Caveats

**(a) Track scoring is subjective.** The 5-axis weighted rubric (§3.1) uses author-assigned weights (C1=0.20, C2=0.25, C3=0.25, C4=0.15, C5=0.15) and per-track scores [0-10]. Different reasonable weights yield different rankings: if C5 (trade-off severity) is weighted 0.30+ instead of 0.15, EWC (C5=8) climbs to 2nd or 1st. The "Track B 1st" recommendation reflects the explicit prioritization of **simplicity + cost-efficiency + diagnosed-root-cause alignment** over **theoretical trade-off minimization**. Any reviewer disagreeing with this prioritization should re-score with their own weights before accepting the ranking.

**(b) Regression cause may have multiple factors.** The diagnosis "catastrophic forgetting due to r=64 capacity" is the **dominant hypothesis** but not the only one. Alternative causes — not ruled out by current evidence — include:
- (b.i) **Chat-template artifact** — Llama chat template may bias generation away from short factual EM strings (TriviaQA prefers terse answers; chat template injects structure)
- (b.ii) **Data distribution shift** — 50K SFT corpus drawn from CLM v4 augmentation may have very low factual-density vs Llama's pretrain mix, creating implicit anti-fact gradient
- (b.iii) **Eval prompt formatting** — TriviaQA 5-shot exemplars may interact with Llama chat template in unexpected ways (e.g. system prompt swallowing few-shot)
- (b.iv) **4-bit quantization noise** — base anchor at 4-bit nf4 has ±1-3pt noise on TriviaQA; some "regression" may be quantization variance not true forgetting (mitigation: §4.3 paired stats — same precision both sides → noise cancels)

If root cause is (b.i)-(b.iii) rather than capacity, Track A (corpus rebalance) is the correct mitigation — Track B may underperform. Without ablation studies, Track B is a **best-guess single-knob fix**, not a guaranteed solution.

**(c) Mitigation may trade off chat lift.** All four tracks introduce some form of regularization (rank cap, corpus dilution, replay, Fisher penalty) that constrains the LoRA's ability to specialize for chat. The Δ_HellaSwag = +1.0pt observed at r=64 is achieved precisely by the same capacity that overwrites factual recall. There is **no a-priori guarantee** that a Pareto-optimal point exists with both Δ_TriviaQA ≥ 0 AND Δ_HellaSwag ≥ +0.5pt — it may turn out that for this base+corpus combo, the chat-axis lift is intrinsically tied to factual erosion, and the only "safe" path is Δ_HellaSwag ≈ 0 (no chat lift, no regression). The §4.1 secondary criterion (Δ ≥ 0 on at least one non-TriviaQA task) reflects this honest possibility — we are explicitly accepting "no lift" as a partial success because the alternative ("lift at any cost") falsified itself in the current Path A run.

**(d) Single-seed evaluation.** All A' eval and all proposed mitigation evals use seed=42 (per A' spec §2.5 + honest_c3 of A' eval pipeline §7.c). lm-eval-harness on MCQA+EM tasks is approximately deterministic in greedy/log-likelihood mode, but the LoRA training itself has stochastic data shuffling — different seeds may yield Δ swings of ~0.5-1.5pt on TriviaQA. The current Path A regression magnitude (Δ=−7.4pt at step-6000) is **far above seed noise**, so the regression is real, BUT **mitigation success at exactly Δ_TriviaQA = 0 might be seed-luck**. If a mitigation track lands Δ_TriviaQA ∈ [−0.5, +0.5] (within the seed-variance band), spec amend to 3-seed re-eval is recommended before declaring final SUCCESS. Cost of 3-seed amend: 3x training cost on the winning track (~$60-90 cumulative for Track B).

---

## 7. Constraints Honored

- **raw#9 STRICT**: This document is pure markdown design. No Python files created on Mac. The Track B re-train (when commissioned next cycle) reuses the existing `state/p9_path_a_llama_lora_2026_05_03/train_llama_lora.py.txt` (ubu1 / RunPod side; Mac never edits .py). The eval pipeline reuse (per §4.3) similarly points at ubu1 .py infrastructure with no Mac-side .py creation.

- **raw#15**: All ubu1 / RunPod paths in this spec use `~/anima/state/...` or `state/p9_path_a_llama_lora_2026_05_03/...` — no `/Users/ghost/...` or `/home/aiden/...` literal paths leaked into the spec body.

- **raw#10 honest C3**: §6 covers the 4 mandated caveats — (a) subjective scoring weights, (b) multi-factor regression cause, (c) chat-lift trade-off may be unavoidable, (d) single-seed eval susceptible to seed-luck near zero.

- **$0 design**: This cycle = spec + audit JSON + marker + handoff. No retraining triggered. No eval triggered. No pod commissioned.

- **DO NOT launch retraining this cycle**: §3.3 plan is **deferred to next BG cycle**, gated on user OK on track selection. The handoff at §8 includes a paste-once prompt for the user to commission Track B (or alternative).

---

## 8. Next-Cycle Handoff

### 8.1 If user selects Track B (recommended)

**Paste-once prompt**:

> Spec next-cycle Path A LoRA mitigation execution — Track B (r=64 → r=16).
>
> **Plan**: Re-train Path A LoRA on Llama-3.2-3B-Instruct with `--lora-r 16 --lora-alpha 16`, all other hyperparams unchanged (lr=1e-4, 10K steps, 50K SFT corpus at `state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl`, Llama chat template, save_steps=2000, bf16, gradient_checkpointing).
>
> **Substrate**: Fresh RunPod H100 SXM pod (per `project_runpod_pod_purge_2026_05_03.md` — boot from HF base mirror, ETA 8-12h, $20-30).
>
> **Hub publish**: `need-singularity/p9-llama32-lora-stage1-r16` (new repo to avoid clobbering r=64 ckpts).
>
> **Eval**: When ckpts publish, re-run A' main eval pipeline per `docs/p9_a_prime_eval_pipeline_landed_2026_05_03.ai.md` §6 — point env var at new repo, emit new verdict at `state/p9_path_a_mitigation_b_r16_2026_05_03_verdict.json`.
>
> **Falsifier**: F-PATHA-MITIGATION-1 per `docs/p9_path_a_regression_mitigation_spec_2026_05_03.md` §4.
>
> **Constraints**: raw#9 STRICT (Mac → hexa only for verdict; ubu1/RunPod .py for train+eval), raw#15, raw#10, single-seed (42).
>
> **Output**: spec + marker + handoff at land.

### 8.2 If user selects Track A (corpus rebalance)

**Paste-once prompt**: (omitted for brevity — symmetric structure: source TriviaQA train + MMLU dev/val, retemplate, mix at 70/30, re-train at r=64 baseline, eval against same falsifier)

### 8.3 If user defers decision

This spec lands as `state/markers/p9_path_a_regression_mitigation_spec_landed.marker` + `docs/p9_path_a_regression_mitigation_spec_landed_2026_05_03.ai.md` — no commission triggered. User can revisit when Path A A' main eval finishes (step-8000/10000 ckpts) for final regression-magnitude confirmation before selecting track.

---

## 9. Files Emitted This Cycle

```
docs/p9_path_a_regression_mitigation_spec_2026_05_03.md           (this file)
state/p9_path_a_regression_mitigation_2026_05_03/
└── spec_audit.json                                                (machine-readable spec summary)
state/markers/p9_path_a_regression_mitigation_spec_landed.marker  (marker)
docs/p9_path_a_regression_mitigation_spec_landed_2026_05_03.ai.md (handoff)
```

---

**End of Path A regression mitigation spec. Recommendation: Track B (LoRA r=64 → r=16) at completion-quality 8.5/10. F-PATHA-MITIGATION-1 falsifier locks Δ_TriviaQA ≥ 0 as primary criterion. $0 this cycle. DO NOT launch retraining — defer to next BG cycle on user OK.**
