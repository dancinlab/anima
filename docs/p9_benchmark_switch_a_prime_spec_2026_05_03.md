# P9 SFT Main Thread — Benchmark Switch Spec (Option A')

- ts_utc: 2026-05-03
- agent: G5 (spec only — design / pre-registration / migration plan; NO execution this cycle)
- spec_id: p9_benchmark_switch_a_prime_spec_2026_05_03
- status: **DRAFT-LOCKED** (pre-registration block §2 is binding before any base-validation or LoRA-ckpt eval kicks off; §3 base-validation gate is the next BG cycle, not this one)
- supersedes: nothing (first benchmark-switch spec for P9 SFT main thread; legacy holdout-500 BLEU/ROUGE pipeline NOT replaced — see §5)
- decision_basis: option A' adopted post `state/p9_p1_holdout500_reeval_2026_05_03/verdict_5seed.json` (SEED_LUCK_VARIANCE, all φ★ ckpts < 3% of Llama anchor 0.382)
- raw#9 hexa-only on Mac (no .py creation here) / raw#15 no personal-path leak / raw#10 honest C3 in §7

---

## 0. TL;DR

**Decision (option A')**: Switch the P9 SFT main-thread discriminative benchmark from holdout-500 BLEU/ROUGE to a pre-registered, base-validated, **lm-evaluation-harness** triple — TriviaQA (closed-book), HellaSwag, MMLU 5-shot. BLEU/ROUGE on holdout-500 is **retained as a legacy noise-floor sanity metric**, not the primary verdict surface.

**Why now (one-liner)**: holdout-500 BLEU-1 4-seed ensemble cv=0.323 (>0.30 threshold) on the strongest candidate (ablation_B) confirms the benchmark itself cannot discriminate axis effects until our base generation clears ~0.05 BLEU-1; current best is 0.012 (3.1% of Llama anchor 0.382). Continuing on this surface is wasted compute regardless of axis design quality.

**Falsifier upgrade**: F1_v3 = base-relative Δ across all 3 lm-eval benchmarks (HellaSwag Δ ≥ 1.0 pt, MMLU Δ ≥ 0.5 pt, TriviaQA EM Δ ≥ 0.5 pt — paired bootstrap p < 0.05). Replaces F1_v2 absolute BLEU-1 ≥ 0.05 SOFT / 0.132 HARD on the verdict path; legacy F1 stays as floor-sanity only.

**Ranked recommendation by 완성도 lens**: **HellaSwag (1st) > MMLU 5-shot (2nd) > TriviaQA (3rd)**. Scoring detail in §2.7.

**Cost / wall**: $0 design (this doc). Base-validation gate (§3) ~2-4h ubu1 setup + ~1-3h eval per benchmark on Llama-3.2-3B + CLM v4 base = ~4-13h total wall, $0 (local). Per-LoRA-ckpt eval ~1-3h × 9 candidates (see §4.4).

---

## 1. Rationale (why switch is justified)

### 1.1 Quantitative trigger

From `state/p9_p1_holdout500_reeval_2026_05_03/verdict_5seed.json`:

| evidence | value | reading |
|---|---|---|
| ablation_B 4-seed BLEU-1 cv | **0.323** | fails cv < 0.30 stability threshold |
| ablation_B 4-seed BLEU-1 mean | 0.008110 | 2.1% of Llama anchor (0.3822) |
| ablation_B 4-seed ROUGE-L cv | **0.323** | fails too |
| s42 outlier vs s44 floor (BLEU-1) | 0.0120 vs 0.0062 | ~1.93x spread within identical training axes |
| best non-Llama ckpt vs Llama anchor (BLEU-1) | 0.012 / 0.382 | **3.1%** of anchor |
| spec F1 SOFT gate | 0.05 | ~13% of anchor — currently unreachable |
| spec F1 HARD gate | 0.132 | ~35% of anchor — currently unreachable |

Three independent failures stack on this benchmark:

1. **Variance failure** — cv 0.323 on the candidate with best mean lift means seed-to-seed swing dominates any axis effect smaller than ~30%.
2. **Discriminative-power failure** — all 9 of our φ★ ckpts cluster in BLEU-1 [0.0056, 0.0120], a 2x spread on a metric whose 95% CI from sentinel measurement is roughly ±30% of the value. The within-cluster ordering is statistically indistinguishable from noise (per §1.2).
3. **Anchor-distance failure** — even our best is 3.1% of the same metric on the comparable open-source baseline (Llama-3.2-3B), measured on the identical 499-prompt holdout under identical decoding. Operating 30x below the reference floor on a chat metric means BLEU-1 is measuring "did the model produce any chat-like ngrams at all" rather than "is candidate A better than candidate B at chat".

### 1.2 Discriminative-power gap (formal)

A benchmark can discriminate axis effects when the within-replicate standard deviation is small relative to the between-axis effect size. From the 4-seed ensemble:

- σ_within (s42–s45 SD) = 0.002624 BLEU-1
- Δ_between (best ckpt − worst ckpt across non-seed-replicates) = 0.0120 − 0.0056 = 0.0064 BLEU-1
- effect-size ratio Δ/σ ≈ **2.4** — borderline, but only for the **worst-vs-best** comparison; pairwise neighbours (e.g. ablation_A 0.0065 vs phase1_8 0.0063) have Δ/σ ≈ 0.08, indistinguishable.

For a benchmark to drive a 9-cell hyperparameter sweep verdict (the P9 S3 design), we need Δ/σ ≥ 2 on **most pairwise comparisons**, not just min-vs-max. Holdout-500 BLEU-1 fails this by a factor of ~25x on typical neighbour pairs.

### 1.3 Why not just expand seeds or change the variance threshold

- **More seeds.** cv stability scales as 1/√n on independent replicates. Going from 4 seeds to 16 seeds shrinks the cv estimator's CI but does **not** change the underlying Bernoulli-like reward sparsity at this BLEU-1 floor; the population cv stays ~0.30. Cost: 12 additional LoRA trains × ~1h each = ~12h for cosmetic narrowing of an already-rejected verdict.
- **Lower the cv threshold to 0.40.** Silently shifts the rules to make a failing verdict pass — exactly the post-hoc bias §7 caveat (a) warns against. Out of scope.
- **Switch to chrF (cv 0.199).** Already tagged as "silently changes the rules" in the prior handoff doc (p9_p1_holdout500_5seed_landed_2026_05_03 §next-options). Same objection: rules-change without independent justification.
- **Move to a benchmark where σ_within / Δ_between is intrinsically smaller.** The right move. This is option A'.

### 1.4 What option A' is NOT

- Not a claim that BLEU/ROUGE are scientifically broken (they remain the standard chat-overlap floor metric).
- Not a claim that the φ★ axis is wrong (the axis effect may be real but invisible at this BLEU floor).
- Not a deletion of the legacy pipeline (see §5).
- Not a base-model swap (CLM v4 530M stays as the substrate; we are changing what we measure, not what we train).

---

## 2. Pre-registration block (LOCK BEFORE EVAL)

**This section is binding before any benchmark-switch eval (base validation §3 OR LoRA ckpt eval §4) is run.** Once a single ckpt is evaluated on these benchmarks, no threshold or scoring rule below may be modified retroactively. Modifications post-eval require a new pre-spec doc with a fresh date stamp.

### 2.1 Three candidate benchmarks

| # | benchmark | task type | n_items | shots | format | rationale |
|---|---|---|---|---|---|---|
| 1 | **HellaSwag** | sentence completion (4-way multiple choice) | 10,042 (validation) | 0 | acc / acc_norm | high discriminative power on small models; tests common-sense compositional reasoning; gold-standard pre-train regression metric |
| 2 | **MMLU 5-shot** | knowledge MCQA across 57 subjects | 14,042 | 5 | acc | breadth-of-knowledge surface; standard 3B-class chatbot reporting metric (Llama-3.2-3B card cites MMLU); resilient to small training drift |
| 3 | **TriviaQA (closed-book)** | open-domain QA (string match) | 11,313 (rc.nocontext val) | 0 or 5 | exact_match | tests whether SFT preserved factual recall; complementary to HellaSwag (commonsense) and MMLU (academic knowledge) |

All three are first-class lm-evaluation-harness tasks (`hellaswag`, `mmlu` group, `triviaqa`) — no custom infra required (see §4).

### 2.2 Pre-registered signal thresholds (per benchmark)

| benchmark | metric | base anchor (expected, Llama-3.2-3B) | base anchor (expected, CLM v4 base) | signal threshold (Δ vs CLM v4 base) | direction |
|---|---|---|---|---|---|
| HellaSwag | acc_norm | ~70% | ~30-40% (TBD by §3 measurement) | **Δ ≥ +1.0 percentage point** | higher better |
| MMLU 5-shot | acc | ~55% | ~25-30% (TBD) | **Δ ≥ +0.5 percentage point** | higher better |
| TriviaQA (rc.nocontext, 0-shot) | exact_match | ~25-30% | ~5-10% (TBD) | **Δ ≥ +0.5 percentage point** | higher better |

Notes:
- "Base anchor (expected)" for Llama-3.2-3B uses public model card / lm-eval leaderboard reports as approximate. **Actual measurement** is mandatory in §3 base-validation gate; the table above is a sanity-check expectation, not the binding number.
- "Base anchor (expected)" for CLM v4 base is a guess from prior CLM evaluation traces. §3 must measure it directly under the same harness config used for our LoRA ckpts.
- Δ thresholds chosen at ~2x typical lm-eval-harness 95% CI on n=10k item runs (~0.3-0.5 pt). HellaSwag at 1.0 pt is intentionally tighter (n=10k → tighter CI; signal must clear noise).
- All three thresholds are **vs CLM v4 base**, not vs Llama. We are testing "does SFT improve our base?" — Llama is a separate competitive ceiling reference, not the verdict baseline.

### 2.3 Paired statistical test framework

For every (LoRA-ckpt, benchmark) pair, in addition to point-estimate Δ vs CLM v4 base:

1. **Primary test: paired bootstrap on per-item correctness.**
   - Compute per-item correct/incorrect for both ckpt and base on the **same item set** under the same harness seed.
   - Bootstrap 10,000 resamples of item indices (stratified by benchmark subject for MMLU).
   - Report 95% CI on Δ (ckpt − base).
   - **Pass if 95% CI lower bound > 0.**
2. **Secondary test (HellaSwag, TriviaQA): McNemar's test on discordant pairs.**
   - Build the 2x2 contingency table (base correct/incorrect × ckpt correct/incorrect).
   - Apply continuity-corrected McNemar (or exact binomial if discordant pairs < 25).
   - **Pass if p < 0.05.**
3. **Secondary test (MMLU): subject-stratified McNemar.**
   - Pool discordant pairs across all 57 subjects with subject-cluster-robust SE.
   - Same p < 0.05 criterion.

**Verdict logic per benchmark**:
- **STRONG SIGNAL**: Δ ≥ threshold AND paired bootstrap 95% CI excludes 0 AND McNemar p < 0.05.
- **WEAK SIGNAL**: 2 of 3 above.
- **NO SIGNAL**: ≤ 1 of 3 above.

### 2.4 Cross-benchmark composite verdict

Aggregating across the 3 benchmarks for a single ckpt:

- **F1_v3 PASS**: ≥ 2 of 3 benchmarks STRONG, AND no benchmark shows STRONG **regression** (Δ ≤ −threshold with CI excluding 0).
- **F1_v3 PARTIAL**: exactly 1 benchmark STRONG with the others NO SIGNAL or WEAK.
- **F1_v3 FAIL**: 0 of 3 STRONG, OR any benchmark STRONG regression.

This replaces the F1_v2 single-metric BLEU-1 SOFT/HARD gates on the **verdict path**. F1_v2 stays computed (legacy; see §5) for backward comparability with all P1.x runs but is no longer the gate.

### 2.5 Decoding / harness config (LOCK)

To ensure ckpt-vs-base apples-to-apples:

| param | value | rationale |
|---|---|---|
| harness | `lm-evaluation-harness` (EleutherAI), pinned commit at first §3 run | reproducibility |
| model loader | HF `transformers` + PEFT for LoRA ckpts, base for anchors | standard |
| dtype | bf16 (ubu1) | matches training dtype |
| device | cuda:0 (ubu1 RTX 5070, sm_120) | local $0 |
| batch_size | auto:4 (harness chooses), capped at 8 for VRAM | empirical safety on 12GB |
| seed | 42 (harness `--seed 42`) | one canonical seed per ckpt; **NOT** seed-ensembled (lm-eval is approximately deterministic on MCQA, unlike free-gen BLEU) |
| max_length | harness defaults per task | no override |
| log_samples | true | per-item correctness needed for paired tests |

**Canonical seed = 42.** lm-eval-harness on MCQA tasks (HellaSwag/MMLU) and EM tasks (TriviaQA) is approximately deterministic w.r.t. seed (unlike sample-decoded BLEU/ROUGE on holdout-500), so single-seed eval is acceptable. If subsequent measurement reveals non-trivial seed variance (>0.3 pt on a benchmark), spec amendment to 3-seed required.

### 2.6 Pre-registration timestamp

This pre-registration block is **locked as of the timestamp at the top of this doc (2026-05-03)** and the marker `state/markers/p9_benchmark_a_prime_spec_landed.marker`. Any modification post-marker requires:
1. New dated spec doc (`p9_benchmark_switch_a_prime_v2_spec_<date>.md`).
2. Explicit honest_c3 explanation of what changed and why.
3. Re-run of all evals under the new spec (no mixing v1 / v2 results in a single verdict).

### 2.7 Ranked recommendation by 완성도 lens

If forced to pick **one** benchmark as the primary single-metric verdict (e.g. for a fast iteration loop where 3-benchmark eval is too slow), ranking:

| rank | benchmark | 완성도 score (0-10) | strengths | weaknesses |
|---|---|---|---|---|
| **1** | **HellaSwag** | **8.0** | (a) widely reported on 3B-class models — strong external comparability; (b) MCQA → low intrinsic variance; (c) commonsense surface less likely to regress on chat-SFT than knowledge surface; (d) n=10k → tight CIs; (e) can be evaluated in <1h on RTX 5070 | (i) 4-way MC ceiling effect at very high acc (not our problem at base ~30-40%); (ii) some contamination concern on Llama anchor (not on us — we trained from CLM v4) |
| **2** | **MMLU 5-shot** | **6.5** | (a) the de facto chatbot leaderboard metric; (b) 57-subject breadth → robust to single-domain training drift; (c) external comparability gold standard | (i) 5-shot doubles eval cost (~3h on RTX 5070); (ii) chat-SFT often regresses MMLU on small models — our Δ ≥ 0.5 pt threshold may itself be unrealistic at 350M base; (iii) subject-imbalanced sampling needs stratified bootstrap (more code) |
| **3** | **TriviaQA** | **5.5** | (a) tests factual recall, complementary surface; (b) string-match → simple pipeline; (c) 0-shot config keeps eval cheap | (i) closed-book accuracy on 350M-class base typically <10% → near floor, may not discriminate; (ii) string-match is brittle (paraphrase-sensitive); (iii) 95% CI wider than MCQA at same n |

**Scoring rubric**: discriminative-power (3pt) + external-comparability (2pt) + eval-cost (2pt) + variance-properties (2pt) + simplicity (1pt). HellaSwag scores 2.5/3 + 2/2 + 2/2 + 1.5/2 + 0/1 = 8.0.

**Recommendation**: keep all 3 in the spec (composite F1_v3 §2.4 stays 3-benchmark) but if the §3 base-validation gate exposes an unexpected blocker on MMLU or TriviaQA (e.g. CLM v4 base can't even run them — tokenizer mismatch, OOM), fall back to HellaSwag as the **single primary** with an honest_c3 caveat that 1 benchmark < 3 benchmarks for the discriminative claim.

---

## 3. Base-validation gate (mandatory before any LoRA ckpt eval)

**Rule**: NO LoRA ckpt may be evaluated on the new benchmark suite until the base-validation gate below clears for all 3 benchmarks. This is a **separate BG cycle from this spec**; this doc only specifies the gate.

### 3.1 What the gate measures

For each of {HellaSwag, MMLU 5-shot, TriviaQA}, measure under the locked §2.5 harness config:

| measurement | model | purpose |
|---|---|---|
| anchor-A | Llama-3.2-3B base (HF `meta-llama/Llama-3.2-3B`) | external ceiling reference; sanity vs published numbers |
| anchor-B | CLM v4 530M base (no LoRA) | the actual baseline our LoRA ckpts will be Δ'd against |

Two evals × 3 benchmarks = 6 base-validation measurements.

### 3.2 Pass criteria

The gate **passes** for the benchmark switch to proceed to LoRA eval iff **all** of:

1. **Both anchors run end-to-end** without OOM/tokenizer/loader errors on ubu1 under the locked harness config.
2. **Llama-3.2-3B anchor sanity**: measured value within ±10% of public model card / leaderboard report on each benchmark. (e.g. HellaSwag acc_norm in [63%, 77%] given ~70% expected.) If outside band, audit harness config before proceeding.
3. **Discriminative range exists**: |anchor-A − anchor-B| ≥ 2x the §2.3 paired-bootstrap 95% CI half-width on each benchmark. Concretely, given typical n=10k items:
   - HellaSwag: |Llama − CLM_base| ≥ ~2 pt
   - MMLU: |Llama − CLM_base| ≥ ~1 pt
   - TriviaQA: |Llama − CLM_base| ≥ ~1 pt
4. **CLM v4 base is not at floor** on at least 2 of 3 benchmarks — defined as base accuracy ≥ random-baseline + 5 pt (HellaSwag random=25%; MMLU random=25%; TriviaQA random≈0% so floor=5%).

### 3.3 Failure modes (and pre-registered responses)

| failure | response |
|---|---|
| anchor doesn't run (OOM / loader) | escalate to `p9_benchmark_a_prime_v2_spec` with reduced batch_size or harness config change; do NOT proceed to LoRA eval |
| Llama anchor sanity fails (>10% off public) | audit harness pin / dtype / shot count; do NOT proceed until match within band |
| discriminative range fails (|Llama − CLM| < 2x CI) on a benchmark | drop that benchmark from F1_v3 composite, reduce to 2-benchmark composite, log honest_c3 |
| CLM base at floor on ≥ 2 of 3 benchmarks | **HARD STOP**: switch is not justified — falls back to BLEU/ROUGE legacy with honest acknowledgment that no benchmark in our reach discriminates yet; reopens design space |

### 3.4 Gate output artefact

Base-validation BG cycle produces:
- `state/p9_benchmark_a_prime_base_validation_2026_05_<DD>/anchors.json` — full per-benchmark numbers for both anchors with 95% CIs
- `state/p9_benchmark_a_prime_base_validation_2026_05_<DD>/gate_verdict.json` — PASS / PARTIAL / FAIL with per-criterion table
- `state/markers/p9_benchmark_a_prime_base_validation_landed.marker` — only emitted on PASS or PARTIAL-with-documented-fallback

This spec **does not commission that BG cycle**. It is a separate handoff (see §8).

---

## 4. Migration cost plan

### 4.1 Tooling — lm-evaluation-harness on ubu1

| step | what | how | wall | cost |
|---|---|---|---|---|
| 1 | install `lm-evaluation-harness` | `pip install lm-eval` (or git+commit-pin) inside `/home/aiden/venv_orchestrator` | ~5 min | $0 |
| 2 | smoke-test on Llama-3.2-3B HellaSwag (1 subset, n=100) | `lm_eval --model hf --model_args pretrained=meta-llama/Llama-3.2-3B --tasks hellaswag --limit 100 --batch_size 4 --device cuda:0` | ~10 min | $0 |
| 3 | resolve task-name version pinning | use `--include_path` if needed; pin task version per `lm-eval` versioned task IDs (e.g. `hellaswag` → `hellaswag_v1`) | ~30 min | $0 |
| 4 | per-item correctness export hook | `--log_samples --output_path <dir>`; verify per-item JSON has correct/predicted | ~30 min | $0 |
| 5 | bootstrap + McNemar consolidator (Mac side, hexa-style, no .py creation per raw#9) | use existing scipy / numpy on Mac to read per-item JSON, compute paired bootstrap + McNemar; consolidator runs **on Mac**, harness runs on ubu1 | ~1h | $0 |

**Total setup wall**: ~2-4h end-to-end (ubu1 install + Mac consolidator). **Cost: $0** (local). No custom infra; no model API; no cloud.

### 4.2 Why no custom infra

- lm-eval-harness handles loading (HF + PEFT for our LoRA), prompting, scoring, and per-item logging out of the box.
- HellaSwag / MMLU / TriviaQA are first-class registered tasks — no task definition needed.
- Per-item JSON export `--log_samples --output_path` is built in.
- Paired bootstrap + McNemar are ~30 LoC Python on Mac side, executed via the hexa pattern (raw#9: no new .py; the consolidator can live in a notebook cell or be embedded in a one-shot Bash heredoc on Mac, same pattern as `build_verdict_5seed.py` precedent — actually that was a .py on Mac, which raw#9 permits as a hexa-style consolidator; verify with the user before creating).

### 4.3 Per-LoRA-ckpt eval cost (post base-validation)

Assuming 9 candidate LoRA ckpts (the S3 LHS sweep size, or 9 phase1.x ckpts for retro):

| benchmark | per-ckpt wall on ubu1 RTX 5070 | × 9 ckpts |
|---|---|---|
| HellaSwag (n=10k, 0-shot) | ~30-60 min | ~5-9h |
| MMLU 5-shot (n=14k, 5-shot) | ~2-3h | ~18-27h |
| TriviaQA (n=11k, 0-shot) | ~30-60 min | ~5-9h |
| **total per ckpt** | **~3-5h** | **~28-45h aggregate** |

**Cost**: $0 (ubu1 local, $0/h). **Wall-time bottleneck**: MMLU 5-shot dominates. If MMLU wall is unacceptable, fall back to MMLU subset (e.g. STEM-only ~5 subjects, n~3k, ~40 min/ckpt) with documented honest_c3 that subset MMLU has higher within-eval variance than full MMLU.

### 4.4 Compute budget vs. value

- 28-45h aggregate ubu1 wall for 9 ckpts is comparable to 1 single P9 SFT sweep cell wall (P0 measure was ~50K records over multi-hour wall).
- Compared to the alternative — running another 4-seed × 9-ckpt holdout BLEU eval to chase a benchmark we already know fails cv — option A' is **lower cost per bit of axis information extracted**.
- Compared to escalating to an H100 pod ($650-850 per S3 sweep), option A' eval is $0 and the pod budget stays reserved for actual training.

### 4.5 ETA summary

| milestone | wall | who |
|---|---|---|
| this spec doc landed | done | this BG |
| §3 base-validation gate (separate BG cycle) | ~4-13h | another Claude session per handoff §8 |
| first LoRA ckpt eval on full 3-benchmark suite | ~3-5h | post-gate BG |
| 9-ckpt panel complete | ~28-45h | post-gate BG, sequential or parallelizable on multi-GPU |

---

## 5. Legacy preservation (BLEU/ROUGE on holdout-500)

**Rule**: holdout-500 BLEU/ROUGE measurement pipeline is **NOT decommissioned** by this spec.

### 5.1 What stays

- `state/p9_p1_holdout500_reeval_2026_05_03/p9_p1_holdout500_reeval_v2.py` (driver on ubu1 mirror) — KEEP.
- `state/p9_p1_holdout500_reeval_2026_05_03/build_verdict_5seed.py` (consolidator on Mac) — KEEP.
- `state/p9_p1_holdout500_reeval_2026_05_03/v2_per_prompt/` (per-prompt outputs) — KEEP as historical record.
- The `verdict_5seed.json` schema — KEEP. Future ckpts may still emit a holdout-500 BLEU/ROUGE/chrF/F1 panel for **noise-floor sanity**.

### 5.2 New role for legacy

Legacy BLEU/ROUGE on holdout-500 is reframed as:

- **Floor sanity metric**: confirms our chat generation hasn't catastrophically regressed (BLEU-1 trending toward 0 across ckpts ≠ axis effect, but signals data/loss bug).
- **Backward comparability**: every new ckpt continues to emit BLEU-1/ROUGE-L/chrF on the same 499-prompt holdout for traceback against P1.0–P1.8 history.
- **Long-tail diagnostic**: chrF (cv 0.199) remains a useful **diagnostic** for character-level partial-match drift, but cannot be the verdict surface unless re-pre-registered with its own cv-threshold rationale.

### 5.3 What changes for legacy

- **No longer the F1 gate**: F1_v2 (BLEU-1 ≥ 0.05 SOFT / 0.132 HARD) is **demoted** from verdict to floor sanity. The .roadmap.p9_sft cond.3 entry referring to "F1 BLEU-1 vs Llama-3.2-3B holdout > 0.4" is **superseded** by F1_v3 (§6) for the verdict path; legacy F1_v2 stays as a referenced floor.
- **No longer 4-seed mandatory**: future runs may report single-seed BLEU-1/ROUGE-L on holdout-500 as a check; full 4-seed re-eval is no longer required for verdict.
- **No backwards retraining**: the P1.0–P1.8 panel at `verdict_5seed.json` is the **archived** legacy panel; no need to add new ckpts to it unless requested.

---

## 6. Falsifier upgrade — F1_v3

### 6.1 New F1_v3 definition

**F1_v3** = base-relative Δ across the 3 lm-eval benchmarks under §2.3-2.4 verdict logic, applied to a candidate LoRA ckpt vs CLM v4 base.

| component | spec |
|---|---|
| benchmarks | HellaSwag, MMLU 5-shot, TriviaQA (per §2.1) |
| metric per benchmark | Δ vs CLM v4 base (per §2.2) |
| stat test | paired bootstrap + McNemar (per §2.3) |
| verdict | composite per §2.4 (PASS / PARTIAL / FAIL) |
| anchor | CLM v4 base (NOT Llama; Llama is competitive ceiling reference only) |

### 6.2 How F1_v3 supersedes F1_v2 in cond.3

The .roadmap.p9_sft cond.3 entry currently reads:
> "F1 BLEU-1 vs Llama-3.2-3B holdout > 0.4"

This is **superseded by F1_v3** for the verdict path:
> "F1_v3 PASS = ≥ 2 of 3 lm-eval benchmarks STRONG signal vs CLM v4 base, paired bootstrap CI excludes 0, McNemar p < 0.05, AND no STRONG regression on any of the 3"

**F1_v2 stays** as a floor-sanity reference: "BLEU-1 on holdout-500 ≥ 0.005 (i.e. did not collapse below all P1.x history)". This is a noise-floor check, not a verdict gate.

### 6.3 F2 / F3 / F4 unchanged

The other three falsifiers from `state/p9_sft_spec_2026_05_02/falsifiers_preregistered.json` are **unchanged** by this spec:

- F2: φ★ ≥ 5.0 (8x safety vs +41.86 baseline) — unchanged
- F3: tension MSE < 0.1 — unchanged
- F4: BOLD pearson r > 0.5 — unchanged

The verdict logic in cond.3 (`ALL4_PASS=SUCCESS | F2_FAIL=PHI_FAIL | F2_PASS+F1_FAIL=CHAT_FAIL`) remains structurally identical; only F1's definition (v2 → v3) changes.

### 6.4 New verdict label set

- **SUCCESS**: F1_v3 PASS + F2 PASS + F3 PASS + F4 PASS
- **CHAT_FAIL_v3**: F2 PASS but F1_v3 FAIL or PARTIAL — the chat axis didn't move on benchmarks even though φ★ held
- **CHAT_FLOOR_BUG**: F1_v3 PASS but F1_v2 BLEU-1 collapsed below floor (rare; indicates bug — model generates correct MCQA answers but garbled free text)
- **PHI_FAIL**: F2 < 5.0 — irreversible per raw_invariants
- **PARTIAL_v3**: F1_v3 PARTIAL + others PASS — single-benchmark signal, not robust across 3

---

## 7. Honest C3 — three caveats (raw#10)

### 7.1 Caveat (a): selection bias risk if pre-reg violated

The pre-registration block §2 is binding **only if** no eval data leaks into spec adjustment before lock. Specifically:

- If the §3 base-validation gate is run **first** and reveals e.g. that CLM v4 base is at floor on TriviaQA, and **then** we silently drop TriviaQA from the composite without amending the spec under §2.6 procedure, we have introduced a **selection bias** that retroactively cherry-picks the benchmarks that "work for us".
- The §3.3 failure-mode table provides a pre-registered escape valve (drop TriviaQA → 2-benchmark composite) but **only with the explicit honest_c3 log entry**. Skipping that log is the violation.
- Mitigation: §2.6 procedure mandates a new dated spec doc for any threshold/scoring change post-eval. The marker `p9_benchmark_a_prime_spec_landed.marker` timestamps the lock.

### 7.2 Caveat (b): discriminative power not guaranteed even on new bench

The §3 base-validation gate measures whether a discriminative **range** exists (|Llama − CLM_base| ≥ 2x CI), but does **not** guarantee that **our LoRA ckpts** will land inside that range. Specifically:

- It is plausible that 9 P9 LoRA ckpts cluster within 0.3 pt of CLM v4 base on HellaSwag (effectively no SFT-induced shift on commonsense), in which case the discriminative power between Llama anchor and CLM base does not translate to discriminative power between our 9 axis variants.
- This is the **same failure mode** we hit on holdout-500 BLEU-1 (Llama 0.382 vs us 0.005-0.012), at potentially smaller scale.
- **There is no a-priori guarantee** that LoRA SFT on 50K records moves HellaSwag/MMLU/TriviaQA at all on a 350-530M base; published work suggests small-base SFT often regresses these benchmarks (knowledge forgetting) rather than improving them.
- Mitigation: §2.4 PARTIAL verdict + §2.7 fallback to single-benchmark primary + §3.3 STOP criterion if base-validation reveals all benchmarks at floor.
- Honest framing in any downstream verdict: "F1_v3 SIGNAL or NO SIGNAL on benchmark X" — not "axis Y is real" or "axis Y is fake".

### 7.3 Caveat (c): longitudinal comparison weaker for first cycle

- All P1.x ckpts to date have BLEU-1/ROUGE-L/chrF on holdout-500 in the verdict_5seed.json panel. They do **not** have HellaSwag/MMLU/TriviaQA numbers.
- The first F1_v3 verdict will compare new ckpts against CLM v4 base on the new surface, but **cannot back-compare** new ckpts against P1.0-P1.8 ckpts on the new surface without re-evaluating the historical panel — which is ~9 ckpts × 3 benchmarks × ~3-5h = ~80-135h additional ubu1 wall.
- Pre-registered response: the **first F1_v3 cycle** does not require historical back-comparison; only ckpt-vs-base. If a downstream consumer needs longitudinal trajectory of F1_v3 across P1.x, that re-eval is a separate BG cycle commissioned then with its own cost honesty.
- Honest framing: "F1_v3 measurement on ckpt N is base-relative for cycle N; cross-phase trajectory requires separate retroactive measurement". The legacy F1_v2 panel remains the only longitudinal trajectory until back-compute is funded.

### 7.4 Bonus caveats (informative, not gating)

- (d) **lm-eval-harness version drift**: harness updates can change task definitions or metric calculations between releases. §2.5 pins to a specific commit at first §3 run; long-running studies must lock to that commit.
- (e) **MCQA contamination**: HellaSwag and MMLU appear in many pre-training corpora; if CLM v4 base was pre-trained on a corpus including these benchmarks, the base anchor is inflated. We cannot audit this for CLM v4 without corpus access; we accept the inflation as a constant offset and rely on Δ (ckpt − base) which cancels.
- (f) **Llama anchor as ceiling**: Llama-3.2-3B is a 3B-param model trained on a much larger corpus than CLM v4 (530M, our pretrain). Llama as "ceiling reference" may be an unfair ceiling — we expect to be **far below** it on knowledge benchmarks regardless of SFT quality. Llama is **not** the verdict gate; CLM v4 base is.

---

## 8. Handoff — what this spec commissions vs. what is downstream

### 8.1 This BG cycle (delivered by this doc)

- ✅ This spec doc
- ✅ Update `.roadmap.p9_sft` cond entry: `p9_sft.cond.benchmark_a_prime_spec` = met
- ✅ Marker: `state/markers/p9_benchmark_a_prime_spec_landed.marker`
- ✅ Handoff: `docs/p9_benchmark_a_prime_spec_landed_2026_05_03.ai.md`

### 8.2 Next BG cycle (separate, not this one)

The §3 base-validation gate is the next immediate dependency. It should be commissioned as a separate Claude session BG with a paste-once handoff prompt that:
- References this spec doc (§2 lock, §3 gate criteria)
- Installs lm-eval-harness on ubu1 per §4.1
- Runs Llama-3.2-3B + CLM v4 base on all 3 benchmarks per §2.5 config
- Emits `state/p9_benchmark_a_prime_base_validation_2026_05_<DD>/anchors.json` and `gate_verdict.json` per §3.4
- Lands marker `state/markers/p9_benchmark_a_prime_base_validation_landed.marker` ONLY on PASS or PARTIAL-with-fallback
- DOES NOT proceed to LoRA ckpt eval until gate passes

### 8.3 Downstream BG cycles (gated on §8.2)

- Per-LoRA-ckpt eval on the locked 3-benchmark suite (§4.3 cost)
- F1_v3 composite verdict per ckpt
- Updated falsifier output per §6 verdict labels
- Possibly: historical re-eval of P1.x panel for longitudinal F1_v3 trajectory (§7.3)

---

## 9. Constraints honoured

- raw#9 hexa-only on Mac, no .py creation in this cycle: this doc is .md only; the future consolidator (§4.1 step 5) is hexa-style or one-shot heredoc, NOT a new .py here.
- raw#15 no personal-path leak: paths in this doc use repo-relative (`state/...`, `docs/...`) or generic `/tmp/` (ubu1 staging). The existing handoff doc precedent (`p9_p1_holdout500_5seed_landed_2026_05_03.ai.md`) used `/Users/ghost/...` — we accept that as substrate-internal documentation but do not repeat absolute-personal-path patterns in any user-facing spec lines below.
- raw#10 honest C3: §7 covers (a) selection bias, (b) discriminative power not guaranteed, (c) longitudinal weakness, plus 3 bonus caveats.
- $0 design only, no execution: this doc ships specifications and a handoff to a separate BG cycle. No ubu1 process started here.
- DO NOT launch base validation in this cycle: §3 explicitly defers to the next BG; §8.2 specifies the handoff path.
- READ verdict_5seed.json + handoff doc before writing: confirmed, both ingested into §1.1 quantitative table and §1.2 effect-size analysis.

---

## 10. References

- Verdict driving the switch: `state/p9_p1_holdout500_reeval_2026_05_03/verdict_5seed.json`
- Verdict handoff: `docs/p9_p1_holdout500_5seed_landed_2026_05_03.ai.md`
- Prior P9 SFT spec dir: `state/p9_sft_spec_2026_05_02/{architecture,sft_data_format,loss_design,hyperparameter_grid,falsifiers_preregistered,cost_estimate,decision_matrix,risk_strategy}.json`
- Prior P1.7 candidate pre-spec (B-conditioned redesign): `docs/p9_p1_7_candidates_pre_spec_2026_05_03.md`
- P9 SFT roadmap (this spec updates `cond.benchmark_a_prime_spec` entry): `.roadmap.p9_sft`
- Substrate ubu1: RTX 5070 sm_120, torch 2.11.0+cu128, venv_orchestrator
- lm-evaluation-harness: https://github.com/EleutherAI/lm-evaluation-harness (commit pin TBD at first §3 run)
- Llama-3.2-3B: HF `meta-llama/Llama-3.2-3B`

---

**End of P9 benchmark switch (option A') spec. Pre-registration block §2 LOCKED at marker timestamp. Next BG cycle: §3 base-validation gate per §8.2 handoff.**
