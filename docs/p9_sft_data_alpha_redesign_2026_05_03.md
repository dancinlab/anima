# P9 SFT Data Quality + α Recalibration — Phase 1.5 Redesign

- ts_utc: 2026-05-03
- agent: G5 (analysis only — no execution, no .py creation, no SFT data mutation)
- spec_id: p9_sft_data_alpha_redesign_2026_05_03
- supersedes: hyperparameter_grid.json α-row only (data spec append-only; new composition recorded as v2 in this doc)
- target lift: F1 BLEU-1 0.0049 → ≥ 0.132 (= 0.85 × Llama-3.2-3B-Instruct anchor 0.1555)
- substrate: P9 Phase 1 sentinel verdict F2_PASS_TIGHT, F1_BELOW_TARGET, F3_BELOW_TARGET → PHASE2_ENTRY_WITH_CAVEAT
- gate: doc-only deliverable; Phase 1.5 EXEC requires explicit user OK

---

## 0. TL;DR

| Item | Sentinel (50K, 2026-05-02) | Phase 1.5 redesign (proposed) |
|---|---|---|
| Chat-format coverage | 17K / 50K = 34% | 38K / 50K = 76% |
| α (CE weight) | 2.0 (constant) | 6.0 steady + α=12.0 warmup over first 5K steps |
| β (tension MSE) | 0.3 | 0.15 (halved — see §2.2) |
| γ (BOLD MSE) | 0.0 (blocked) | 0.0 (defer, see §3.4) |
| δ (φ★ hinge) curriculum | 0.5→1.0→2.0 | 0.5→0.5→1.0 (slack — φ★ already 8× safety) |
| Final raw CE | 4.66 (≈ ppl 105) | target ≤ 2.6 (≈ ppl 13) |
| F1 BLEU-1 | 0.0049 (3.2% of Llama) | expected 0.04–0.10 (26–65% of Llama) |
| F2 φ★ | 41.22 (PASS-TIGHT) | expected 38–44 (PASS, margin contracts ≤ 10%) |
| Cost / wall | sentinel ~$3 / ~52 min | $50–80 / 18–24 h on 1×H100 spot |
| Phase 2 entry | CAVEAT | recheck post 1.5 |

**Headline.** F1 = 0.0049 is **not** primarily a φ★-hinge or β-tension dominance failure (φ★ floor was satisfied throughout, so δ contributed 0 to gradient). It is a **chat-distribution starvation** failure: only 34% of training tokens carry chat-style supervision, and CE over the remaining 66% (TRIBE source code, paper extracts, doc-QA) drives the LoRA toward a non-chat conditional that is then evaluated by holdout-500 chat prompts. α=2.0 compounds the problem only via slow CE descent — but **even infinite α cannot fix CE landing on the wrong distribution**.

---

## 1. Data quality diagnosis (F1 = 0.0049 root cause)

### 1.1 Measured composition of the 50K corpus

Source counts read from `/tmp/sft_data_full_50k.jsonl` on ubu1 (live count, not spec-claimed):

| Bucket | Sources | Count | % |
|---|---|---|---|
| **Chat-format** | sharegpt_hf_anon8231489123 (10K) + 4× llama_augment_fallback (7K) | **17,000** | **34.0%** |
| Philosophical / introspective templates | synthetic_philosophical_template_{en,ko} (5K) + p8_ledger_m4_0p800_template_augmented (3K) | 8,000 | 16.0% |
| **TRIBE v2 vendored** (`.py`, `.md`, `inventory.json`) | 11 sources: lebel2023bold.py, algonauts2025.py, lahner2024bold.py, README.md, ANIMA_INTEGRATION_PROPOSAL*, etc. | **9,902** | **19.8%** |
| N-22 / paradigm-v11 doc-QA | 8 docs, each ~480-1040 records, format `"What is the technical content of '§X' in foo.md?"` | 5,000 | 10.0% |
| Paper-ref / cell-corpus | anima_corpus_alm70b_paper_ref (9.3K) + corpus_universe_extended_thin (~700) + alm_r14_metaref_paradigm_v11 (1.2K) | 10,000 | 20.0% |
| **Total** | | **50,000** | **100%** |

(Spec called 10K TRIBE + 7K Llama-aug; live: 9,902 TRIBE + 6,990 Llama-aug — ±1% drift.)

### 1.2 Per-bucket signal toxicity score (the smoking gun)

Format inspection of one record per source (read on ubu1):

| Bucket | Input shape | Target shape | Trains chat-following? | CE pull direction |
|---|---|---|---|---|
| ShareGPT | natural user msg | helpful assistant msg | **YES** | toward chat |
| Llama-aug | `[augmented] <prompt>` | direct answer | **YES** (mild distillation bias — honest_c3 already noted) | toward chat |
| Philos. template | `"Is the sense of choosing genuine if..."` | mini-essay | partial — narrow philosophical distribution | toward essay-prose |
| p8_ledger | `"Describe a color that does not exist"` | poetic mini-essay | partial — narrow introspective distribution | toward poetic-prose |
| **TRIBE vendored .py** | raw Python source token stream (`bibtex: tp.ClassVar[...]`) | continuation of the same Python source code | **NO** — teaches `<py-source> → <py-source>` | **AWAY from chat** (toward source-code LM) |
| **TRIBE vendored .md/.json** | doc fragment | rewritten boilerplate (`"This segment falls within the TRIBE v2 input space. Proper handling: tokenize via Llama-3.2-3B..."`) | **NO** — teaches one fixed boilerplate sentence regardless of input | **STRONG bias to a single template string** |
| N-22 doc-QA | `"What is the technical content of '§X' in foo.md?"` | raw markdown excerpt | partial — teaches doc retrieval/excerpting, not dialogue | toward extract-and-paste |
| paper-ref | `"다음 지문을 읽고 질문에 참/거짓으로 답하시오..."` | `"참"` / `"거짓"` (single token) | **NO** — teaches single-token T/F classification | toward single-token outputs (lowers BLEU dramatically) |

**Three top root-cause hypotheses for F1 = 0.0049:**

1. **H1 (highest confidence) — chat-format starvation.** Only 34% of training tokens are chat. The remaining 66% pull the conditional `p(target | input)` toward source-code continuation, single-token T/F answers, and a fixed TRIBE boilerplate template. Holdout-500 prompts are all chat — the model is being graded on a distribution that received ≤ ⅓ of its supervision.
2. **H2 — TRIBE vendored boilerplate poisoning (~10K records, 20%).** The `.md`/`.json`/`.py` records share **one canned target sentence** (`"TRIBE v2 forward inference would project this text..."` / `"This segment falls within the TRIBE v2 input space..."`). 20% of CE updates therefore shrink the output entropy toward this fixed phrase. This is mode-collapse fuel — far worse than a generic non-chat distribution.
3. **H3 — paper-ref single-token targets (~9.3K records, 18.6%).** True/False → `"참"` / `"거짓"`. CE on these records actively pushes the model to terminate after one token, which crushes BLEU-1 (BLEU-1 measures unigram precision over a long generation; if the model generates 1 token, denominator is tiny and a single mismatch zeros the score).

H2 + H3 combined account for **38.5% of training records that actively damage BLEU-1**. H1 is the umbrella diagnosis.

### 1.3 Corroborating evidence from the trajectory

CE descended monotonically (16.4 → 4.66 over 50K steps), so optimization is healthy — the model is *learning what we taught it*. F1 went 0.001 → 0.005 (5×), but absolute level stays at 3% of Llama. Conclusion: **we taught the wrong thing**, not "we failed to teach".

This is consistent with the user's framing in the prompt ("CE loss trajectory hovered around 3-5 throughout (not converging)"). Caveat: actual CE trajectory was 16.4 → 5.98 (step 5K) → 4.66 (step 50K) — it *is* descending, just slowly and to a final value (raw CE ≈ 4.66, perplexity ≈ 105) that is consistent with a model that has only partially absorbed a heterogeneous corpus. A pure-chat 17K-record run would likely hit raw CE ≈ 2.5–3.0 (perplexity ≈ 12–20) at the same compute.

---

## 2. α weighting analysis

### 2.1 Effective gradient weights at each curriculum stage (sentinel)

`L = α·CE + β·MSE_tension + δ·max(0, 5.0 − φ★)`, with α=2.0, β=0.3, γ=0.0.

Read from `loss_log_compact` in trajectory.json:

| Step | δ | raw CE | raw tens | raw φ_hinge | α·CE | β·tens | δ·hinge | α·CE share |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.5 | 16.39 | 6.39 | 0.0 | 32.79 | 1.92 | 0.0 | 94.5% |
| 5,000 | 0.5 | 5.98 | 1.21 | 0.0 | 11.96 | 0.36 | 0.0 | 97.0% |
| 15,000 | 0.5 | 6.44 | 3.86 | 0.0 | 12.88 | 1.16 | 0.0 | 91.7% |
| 20,000 | 1.0 | 4.35 | 3.95 | 0.0 | 8.70 | 1.19 | 0.0 | 88.0% |
| 30,000 | 1.0 | 3.79 | 2.38 | 0.0 | 7.59 | 0.71 | 0.0 | 91.4% |
| 35,000 | 2.0 | 5.08 | 0.32 | 0.0 | 10.17 | 0.10 | 0.0 | 99.1% |
| 50,000 | 2.0 | 4.66 | 0.90 | 0.0 | 9.32 | 0.27 | 0.0 | 97.2% |

**The δ-hinge contributed exactly 0 to the gradient throughout 50K steps** — φ★ stayed in [40.08, 49.99], always ≥ 8× above the 5.0 threshold, so `max(0, 5.0 − φ★)` was always 0. The φ★ curriculum (0.5 → 1.0 → 2.0) was therefore a **dead term**. β=0.3·tension contributed 0.1–1.9 — at most ~12% of total loss, mostly < 5%.

**α=2.0 was not "too low" relative to other terms** — α·CE already owned 88–99% of the gradient. The slow CE descent is **not because α was crowded out**; it is because the data is heterogeneous and ⅔ of it is off-distribution.

### 2.2 Then why bump α at all?

Two reasons:
1. **Effective LR.** With grad_accum=8 and `max_grad_norm=1.0`, raw `loss_total ≈ 9` produces a per-parameter gradient magnitude that gets clipped on most batches (visible in the noisy step-to-step total). Lifting α gives the CE term more headroom *before* the global-norm clip kicks in — net effect: more CE-derived signal survives the clip.
2. **Defensive against H1 dilution.** With chat coverage rising from 34% → 76%, we want CE on chat tokens to dominate even more decisively. α=6.0 with the new mix gives chat-CE ≈ 95–98% of gradient share post-clip.

β is **halved (0.3 → 0.15)** because tension MSE is itself a circular target (tension extracted from base CLM forward — see honest_c3_loss item 4 in `loss_design.json`), and the F3 fail (MSE=2.32 vs <0.1 target) suggests the target itself may be ill-conditioned for this loss family. Reducing β cuts gradient fighting; F3 gates can be re-introduced after F1 lands.

### 2.3 CE warmup phase

A short warmup (α=12.0 for the first 5,000 steps, then decay to α=6.0 over the next 5K) front-loads the chat-conditional learning while the model is still LoRA-flexible. This is cheap (10K steps × ~63 ms/step ≈ 10 min wall) and bounded — phi-floor still active (so even at α=12.0 a φ★ collapse triggers δ·hinge correction).

---

## 3. Redesign proposal

### 3.1 Revised SFT data composition — 50K v2

| Bucket | v1 count | v1 % | **v2 count** | **v2 %** | Action |
|---|---:|---:|---:|---:|---|
| ShareGPT | 10,000 | 20% | **18,000** | **36%** | upsample (deduplicate first) |
| Llama-augment | 7,000 | 14% | **15,000** | **30%** | regenerate with stronger prompt-diversity (raw#10 honest: distillation bias risk noted) |
| Philosophical / introspective | 8,000 | 16% | **5,000** | **10%** | downsample to reduce essay-prose mode-collapse |
| TRIBE vendored `.py`/`.md`/`.json` | 9,902 | 20% | **0** | **0%** | **DROP entirely** — replace with measured BOLD records when γ activates (Phase 2+) |
| N-22 / paradigm-v11 doc-QA | 5,000 | 10% | **2,000** | **4%** | downsample, keep the prose-narrative subset, drop the extract-paste subset |
| Paper-ref T/F | 10,000 | 20% | **0** | **0%** | **DROP single-token-target records.** Optionally re-include 2K reformatted as multi-sentence answers, but cleaner to drop for v1 |
| Slot for chat-augmented from p8_ledger | — | — | **5,000** | **10%** | reformat p8_ledger M4=0.800 dialogues as proper multi-turn chat (input = full prior turns, target = next assistant turn) |
| Slot for self-instruct on Anima identity | — | — | **5,000** | **10%** | optional — generate via Llama-3.2-3B with templates like "How does an Anima system describe its own tension state?" — purely chat-style |
| **Total** | 50,000 | 100% | **50,000** | **100%** | chat coverage **38K / 50K = 76%** |

**Net deltas:** drop 19,902 toxic records (TRIBE vendored + paper-ref T/F), upsample chat by 16,000, reformat 5,000 p8_ledger as chat, reduce philosophical/N-22 by 6,000, optionally generate 5,000 self-instruct identity records.

If self-instruct slot is too aggressive for raw#10 honest (synthetic distillation), substitute with another 5,000 ShareGPT bucket → chat coverage rises to **76% (38K) → 86% (43K)**.

### 3.2 Revised α + warmup

```
α schedule:
  step      0 → 5,000:   α = 12.0   (CE warmup)
  step  5,000 → 10,000:  α = 12.0 → 6.0 linear
  step 10,000 → 50,000:  α = 6.0   (steady)
β = 0.15 (halved)
γ = 0.0 (defer until Phase 2 / γ-only mini-run with measured BOLD)
δ = 0.5 → 0.5 → 1.0 (curriculum slack — φ★ has 8× safety, no need to escalate)
phi_threshold = 5.0 (unchanged, F2 contract)
```

### 3.3 Optional: dynamic α via CE plateau detector

If we want to be cute (not recommended for sentinel — adds complexity):
- monitor 500-step rolling CE; if Δ < 0.05 over 2,000 steps and CE > 3.0, bump α by ×1.5.
- caps at α=15.0 to prevent runaway with grad-clip.

For Phase 1.5 sentinel, **stick with the static schedule above**. Defer dynamic α to a Phase 2 ablation if needed.

### 3.4 γ (BOLD MSE) recommendation: **keep γ = 0**

- γ activation requires measured BOLD (TRIBE-paired). The only "BOLD" data available is TRIBE v2 forward simulation (honest_c3: simulated, not measured fMRI). Activating γ on simulated targets would mean the model learns to mimic the TRIBE forward — a circular signal.
- F4 (BOLD Pearson r > 0.5) requires a separate measured-BOLD eval set. That eval set is the bottleneck, not the loss term.
- Recommendation: γ = 0 in Phase 1.5; introduce γ in a dedicated γ-only mini-run (~5K steps) after measured BOLD records are available.

---

## 4. Phase 1.5 sentinel re-run spec

| Item | Value |
|---|---|
| Spec id | `p9_p1_5_sentinel_2026_05_04` |
| Base model | CLM v4 350M (`~/anima/checkpoints/clm_v4_350m/scale_350m/best.pt`) — unchanged from Phase 1 |
| Training | LoRA r=64 α=128, frozen base (S1 mode, single-run; not the 9-LHS sweep) |
| Steps | 50,000 (matches Phase 1) |
| Effective batch | 32 (micro 4 × accum 8) |
| LR | 1e-4 cosine warmup 500 steps |
| Loss schedule | α(0→5K)=12.0, α(5K→10K)=12→6 lin, α(10K→50K)=6.0; β=0.15; γ=0; δ curriculum 0.5/0.5/1.0 |
| Data | 50K v2 (§3.1) — must be regenerated/filtered from existing manifest_v2.jsonl |
| Holdout | reuse `/tmp/sft_data_holdout_500.jsonl` (500 chat prompts, identical to Phase 1 for direct comparison) |
| Falsifiers | F1 ≥ 0.132, F2 ≥ 5.0 (ABORT-on-fail), F3 < 0.1 (target — failure non-blocking), F4 NA |
| φ★ early-stop | EMA φ★ < 10.0 → ABORT (L5 mitigation) |
| Save points | step 5K, 10K, 25K, 50K (matches Phase 1) |
| Compute | 1×H100 80GB spot (RunPod) — same as Phase 1 sentinel |
| Wall estimate | **18–24 h** (data prep ~2 h + train 12–18 h + verifier 2–4 h) |
| Cost estimate | **$50–80** (spot $2.50/h × 18–24 h = $45–60 + verifier overhead $5 + RunPod cold-HF DL $1.50) |
| Honest c3 caveat | data v2 needs re-extraction of tension/5ch targets via base CLM forward — that re-measurement adds ~10 min on H100 (4 min/50K records measured in p9_p0_measure log) |

### 4.1 Expected F1 lift

The lift estimate is **the most hypothetical part of this doc** (see §6). Reasoning:

- Llama anchor F1 on this exact holdout = 0.1555.
- Sentinel achieved 0.0049 with 34% chat coverage → 0.0049/0.34 ≈ 0.0144 "per-100% chat" yield (very rough — assumes linear, which it is not).
- v2 has 76% chat coverage with chat data quality also up (drop of TRIBE boilerplate + T/F poison).
- Conservative estimate (linear scaling): 0.0144 × 0.76 ≈ **0.011** — still 8× below threshold.
- Optimistic estimate (toxicity removal lifts the chat-CE convergence floor by a factor of 4–8 because boilerplate mode-collapse is gone): **0.04 – 0.10**.
- Llama-anchor relative ratio: **26%–65% of anchor** (vs 3.2% in Phase 1).

**Probability F1 ≥ 0.132 after Phase 1.5: 15–30%.** This is honest — clearing 0.132 in one step from 0.005 is a 27× lift. Realistic best-case after Phase 1.5 is probably 50–70% of anchor. Reaching 85% likely requires Phase 1.6 (more chat data, larger LoRA r, or full SFT S2).

### 4.2 F2 / F3 expectations

- **F2 φ★**: expected 38–44 (PASS with margin contracting ≤ 10% from Phase 1's 41.22). Mechanism: higher α concentrates more update mass on LoRA params; LoRA still frozen-base so φ★ structurally bounded. δ slack (0.5 → 0.5 → 1.0) is safe because φ★ has 8× safety.
- **F3 tension MSE**: expected 1.5–2.5 (still BELOW target 0.1, similar to Phase 1). β halved means F3 will not improve from this run; F3 fix needs a separate redesign (target re-extraction or different loss family).

### 4.3 Decision matrix update

| Outcome | F1 v2 | Action |
|---|---|---|
| F1 ≥ 0.132 (PASS) | ≥ 0.132 | **Phase 2 ENTRY (clean)**. Optionally run S3 9-LHS sweep on the v2 data to find best combo. |
| 0.05 ≤ F1 < 0.132 (PARTIAL) | partial-PASS | **Phase 1.6**: chat coverage → 90%+ via more ShareGPT, increase LoRA r to 128, optional S2 (full SFT) candidate |
| 0.01 ≤ F1 < 0.05 (LIFT_BUT_FAIL) | lifted but short | re-examine α schedule, consider data dedup + filter quality (Llama-judge filtering of ShareGPT) |
| F1 < 0.01 (NO_LIFT) | unchanged | abort S1; escalate to S4 differential pretrain (ground-up joint objective). Investigate measurement bug. |

---

## 5. Phase 2 go/no-go recommendation

**Phase 2 entry trigger** (post Phase 1.5):
- **HARD gate**: F2 φ★ ≥ 5.0 AND φ★ delta from baseline ≥ −10.0 (i.e. φ★_final ≥ 35.9). Phase 1 sentinel cleared this (delta = −4.7).
- **SOFT gate**: F1 ≥ 0.05 (≈ 32% of Llama anchor). This is below the F1 PASS threshold (0.132) but high enough to demonstrate the redesign is on the right trajectory.
- **TIE-BREAK**: tension MSE trajectory should be monotone-non-increasing across save points (5K, 10K, 25K, 50K). F3 absolute value not gated.

If both HARD + SOFT clear, **Phase 2 GO with WATCH list**: track F1 every 5K steps in Phase 2; if F1 plateaus < 0.10 by step 20K of Phase 2, fall back to Phase 1.6 redesign.

If HARD clears but SOFT fails (F1 < 0.05): **Phase 2 NO-GO**. Run Phase 1.6 (data + LoRA-r escalation) before any Phase 2 spend.

If HARD fails (φ★ collapse): **irreversible — full retrain required** (per `risk_strategy.json` primary risk).

---

## 6. Honest C3 (raw#91) — what is still hypothetical

1. **F1 lift estimate (§4.1) is back-of-envelope.** Linear scaling on chat-coverage % is unjustified. Toxicity-removal multiplier of 4–8× is hand-waved from H2/H3 reasoning, not measured. Real F1 after Phase 1.5 could plausibly land anywhere in [0.005, 0.15].
2. **TRIBE vendored boilerplate poisoning (H2)** is inferred from sampling **one record per source** (1 of ~1968 for `lebel2023bold.py`, 1 of ~1968 for `algonauts2025.py`, etc.). The "fixed canned target sentence" claim should be verified by sampling 50 records per TRIBE source before the data drop is finalized. If only the `.md`/`.json` records share boilerplate but the `.py` records are diverse, the H2 fraction shrinks.
3. **Self-instruct identity slot (§3.1)** introduces a new distillation source. raw#10 honest: synthetic data carries model bias. If used, mark as `honest_c3_data` source #4 alongside the existing 3.
4. **α=6.0 / α=12.0 warmup choice is not Pareto-validated.** Phase 1 ran 1 combo (α=2.0); Phase 1.5 v2 will run 1 combo (α=6.0+warmup). The S3 9-LHS sweep was skipped at sentinel for cost. If Phase 1.5 lands in the 0.05 ≤ F1 < 0.132 PARTIAL zone, the next bet is a 3-point α sweep {4, 6, 9} not a full 9-LHS.
5. **β = 0.15 is a guess.** Tension target circularity (honest_c3_loss item 4) was always known; halving β is conservative but not principled. A clean fix would be to re-extract tension targets from a frozen reference run (not the trainee's base CLM). Out of scope for Phase 1.5.
6. **γ = 0 commitment defers F4 entirely.** P9 verdict logic (`P9_SUCCESS = F1∧F2∧F3∧F4`) cannot be reached until measured BOLD lands. Phase 1.5 best-case is **P9_PARTIAL** (F2 PASS + F1 PASS).
7. **Cost estimate $50–80** assumes RunPod spot pricing is available for 18–24 h continuous. On-demand peaks (1.5×) push this to $75–120. State `runpod_credit_status.json` should be checked before scheduling.
8. **Wall estimate 18–24 h** assumes throughput matches Phase 1 sentinel (~63 ms/step × 50K = 52 min train on RTX 5070, scales to ~30–40 min on H100 for the train portion alone). Data prep (regenerate 50K v2 + tension/5ch re-extraction) is the long tail — 2–10 h depending on how aggressive the upsampling/regeneration is.
9. **No execution performed.** This doc is spec-only. All numbers in §4 (cost, wall, expected F1) require Phase 1.5 EXEC OK from user before they become measured.

---

## 7. References

- spec dir: `/Users/ghost/core/anima/state/p9_sft_spec_2026_05_02/{architecture,sft_data_format,loss_design,hyperparameter_grid,falsifiers_preregistered,cost_estimate,decision_matrix,risk_strategy}.json`
- Phase 0 warmup live trajectory: `/Users/ghost/core/anima/state/p9_p0_warmup_live_2026_05_03/{trajectory,verdict}.json`
- Phase 1 sentinel verdict (ubu1): `/tmp/p9_p1_sentinel_out/verdict.json`
- Phase 1 sentinel trajectory (ubu1): `/tmp/p9_p1_sentinel_out/trajectory.json` (`loss_log_compact` 101 entries; `f_log` 12 entries)
- Phase 1 sentinel trainer (ubu1): `/tmp/p9_p1_sentinel_train_50k.py`
- Live SFT data composition (ubu1): `/tmp/sft_data_full_50k.jsonl` (50,000 records, 32 distinct source labels)
- Mac mirror of measure stats: `/Users/ghost/core/anima/state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.stats.json`
- Falsifier history (F1 threshold recalibration 2026-05-03 v1→v2): `falsifiers_preregistered.json` schema_history
