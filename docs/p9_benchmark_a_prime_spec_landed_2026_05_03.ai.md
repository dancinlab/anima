# P9 SFT main-thread benchmark switch (option A') spec — LANDED 2026-05-03

## TL;DR

Spec doc landed for option A' adoption: switch P9 SFT main-thread primary discriminative benchmark from holdout-500 BLEU/ROUGE to a pre-registered, base-validated, lm-evaluation-harness triple {HellaSwag, MMLU 5-shot, TriviaQA}. Legacy BLEU/ROUGE retained as floor-sanity metric, NOT decommissioned. Falsifier F1 upgraded v2 → v3 (base-relative Δ across 3 benchmarks with paired bootstrap + McNemar). F2/F3/F4 unchanged.

Pre-registration block §2 of the spec is LOCKED at the marker timestamp; no post-eval threshold/scoring change permitted without a fresh dated spec doc per §2.6.

This BG cycle: design/spec only, $0, no execution. Next BG cycle (separate handoff): §3 base-validation gate measuring Llama-3.2-3B + CLM v4 base on all 3 benchmarks before any LoRA ckpt eval.

## Inputs

- Driving verdict: `state/p9_p1_holdout500_reeval_2026_05_03/verdict_5seed.json` (SEED_LUCK_VARIANCE, ablation_B 4-seed cv 0.323 fails 0.30 threshold)
- Driving handoff: `docs/p9_p1_holdout500_5seed_landed_2026_05_03.ai.md`
- Prior P9 spec dir: `state/p9_sft_spec_2026_05_02/`
- Prior P1.7 candidate pre-spec: `docs/p9_p1_7_candidates_pre_spec_2026_05_03.md`
- Roadmap SSOT: `.roadmap.p9_sft`

## Outputs

- Spec doc: `docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md` (~430 LoC, comprehensive 10-section spec)
- Marker: `state/markers/p9_benchmark_a_prime_spec_landed.marker`
- Handoff: this doc (`docs/p9_benchmark_a_prime_spec_landed_2026_05_03.ai.md`)
- Roadmap update: `.roadmap.p9_sft` adds `p9_sft.cond.benchmark_a_prime_spec` entry, status=met

## Decision summary

### Why switch is justified

Three failures stack on holdout-500 BLEU/ROUGE:

1. **Variance failure** — ablation_B 4-seed cv 0.323 (>0.30 spec threshold) on both BLEU-1 and ROUGE-L. s42 outlier (~2x s44) shows ~1.93x within-axis spread.
2. **Discriminative-power failure** — pairwise neighbour Δ/σ ≈ 0.08, indistinguishable from noise; only worst-vs-best comparison clears Δ/σ ≥ 2.
3. **Anchor-distance failure** — best non-Llama ckpt 0.012 vs Llama anchor 0.382 = 3.1% of anchor; SOFT gate (0.05, ~13% of anchor) currently unreachable.

### Pre-registered benchmark triple (LOCK)

| benchmark | metric | signal threshold (Δ vs CLM v4 base) | rank |
|---|---|---|---|
| HellaSwag | acc_norm | ≥ +1.0 pt | **1st (8.0)** |
| MMLU 5-shot | acc | ≥ +0.5 pt | 2nd (6.5) |
| TriviaQA (rc.nocontext, 0-shot) | exact_match | ≥ +0.5 pt | 3rd (5.5) |

Stat tests per benchmark: paired bootstrap (10k resamples, 95% CI must exclude 0) + McNemar's test (p < 0.05, subject-stratified for MMLU). Verdict logic per benchmark: STRONG / WEAK / NO SIGNAL. Composite F1_v3: ≥ 2 of 3 STRONG, no STRONG regression.

### Base-validation gate (next BG cycle, NOT this one)

Mandatory before any LoRA ckpt eval. Measure Llama-3.2-3B + CLM v4 base on all 3 benchmarks. PASS criteria:
1. Both anchors run end-to-end on ubu1.
2. Llama anchor within ±10% of public report.
3. Discriminative range |Llama − CLM_base| ≥ 2x paired-bootstrap CI (≥ 2 pt HellaSwag, ≥ 1 pt MMLU/TriviaQA).
4. CLM base ≥ random + 5 pt on ≥ 2 of 3 benchmarks.

HARD STOP if criterion 4 fails on ≥ 2 benchmarks → falls back to BLEU/ROUGE legacy with honest acknowledgment.

### Falsifier upgrade

F1_v3 = base-relative Δ across 3 lm-eval benchmarks (composite per §2.4 of spec). Replaces F1_v2 (BLEU-1 ≥ 0.05 SOFT / 0.132 HARD) on the verdict path. F1_v2 demoted to floor-sanity reference.

F2 (φ★ ≥ 5.0), F3 (tension MSE < 0.1), F4 (BOLD pearson r > 0.5) unchanged.

New verdict labels: SUCCESS / CHAT_FAIL_v3 / CHAT_FLOOR_BUG / PHI_FAIL / PARTIAL_v3.

### Legacy preservation

BLEU/ROUGE on holdout-500 NOT decommissioned. Pipeline (`p9_p1_holdout500_reeval_v2.py` + `build_verdict_5seed.py`) stays. Reframed as: floor sanity metric + backward comparability + chrF as long-tail diagnostic.

### Migration cost

- lm-eval-harness setup on ubu1: ~2-4h, $0 (pip install + smoke + per-item logging hook)
- Per LoRA ckpt eval × 9 candidates: ~3-5h × 9 = ~28-45h aggregate ubu1 wall, $0
- No custom infra. No model API. No cloud.

## Honest C3 (raw#10) — three caveats

(a) **Selection bias risk if pre-reg violated** — the §2 block is binding only if no eval data leaks into spec adjustment before lock. §2.6 procedure mandates new dated spec doc for any post-eval change.

(b) **Discriminative power not guaranteed even on new bench** — base-validation §3 measures range between anchors but does not guarantee our 9 LoRA ckpts will land inside that range. Possible failure mode mirrors holdout-500 (clustering near base). §2.4 PARTIAL verdict + §2.7 fallback + §3.3 STOP criterion mitigate.

(c) **Longitudinal comparison weaker for first cycle** — historical P1.x ckpts have BLEU/ROUGE only; back-compute on new surface = ~80-135h additional ubu1 wall (separate BG when funded). First F1_v3 cycle is base-relative only, no cross-phase trajectory.

## Verdict / status

- Spec: **DRAFT-LOCKED**. Pre-registration block timestamped at marker.
- Roadmap cond entry: **MET** (this spec is the deliverable).
- Next dependency: §3 base-validation gate (separate BG cycle, paste-once handoff per spec §8.2).
- DO NOT proceed to LoRA ckpt eval until base-validation gate emits its marker.

## Constraints honoured

- raw#9: no .py created in this cycle. Future consolidator (lm-eval per-item bootstrap on Mac) will be hexa-style or one-shot heredoc per spec §4.1 step 5.
- raw#15: spec body uses repo-relative paths (`state/...`, `docs/...`); no personal-path leak in user-facing lines.
- raw#10: §7 of spec covers (a) selection bias, (b) discriminative power not guaranteed, (c) longitudinal weakness, plus 3 bonus caveats (d-f).
- $0 design only, no execution: confirmed.
- Read verdict_5seed.json + handoff doc before writing: confirmed, ingested into §1.1 quantitative table + §1.2 effect-size analysis.
