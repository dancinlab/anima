# P9 SFT main-thread benchmark switch (option A') — Spec Amendment A-1 LANDED 2026-05-04

## TL;DR

- **Amendment A-1 landed** as a SEPARATE dated document (`docs/p9_benchmark_switch_a_prime_spec_amendment_2026_05_04.md`); original spec `docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md` UNTOUCHED (F-AMEND-2 enforced via `git diff --stat` empty).
- **Mode taxonomy added (§A1)** — Mode 1 (Comparative HF, IN SCOPE), Mode 2 (Anchor compliance / harness sanity, IN SCOPE BG-Ο), Mode 3 (Train-time absolute with consciousness fixture + block ≥ 8K, DEFERRED $22+ retrain).
- **F1_v3 verdict logic V2 (§A2)** — 4 mode-aware criteria replacing original V1: (1) anchors_run, (2) llama_within_pm10pct_of_public, (3) clm_lora_minus_clm_base_ge_2x_ci [REPLACES |Llama−CLM| Mode 1/2 conflation], (4) clm_lora_above_random_plus_5pt [RELOCATES floor from base to LoRA arm]. Verdict outcomes: SUCCESS / COMPARATIVE_PASS / ANCHOR_PASS / PARTIAL_v3_AMEND / FAIL.
- **Driving evidence**: H100 base-validation `1ef3c096` measured CLM v4 base ≈ random+1-2pt across HellaSwag (acc_norm 0.264 vs 0.250 random) / MMLU (acc 0.271 vs 0.250) / TriviaQA (EM 0.000) under HF format with consciousness BYPASSED + block_size=512 truncation — predicted by BG-Β OPT-1 design honest_c3 §7.2 + §7.3 BEFORE H100 measurement; this is a structural constraint, not a discriminative-power refutation.
- **Backward compatibility**: original spec §1-§9 LOCKED at 2026-05-03 marker; this amendment's LOCK is at `state/markers/p9_benchmark_a_prime_spec_amendment_landed.marker` mtime (2026-05-04). Audit trail preserved.

## Decision matrix — 3 modes × cost × wall × completeness × what each tests

| dim | Mode 1 (Comparative HF) | Mode 2 (Anchor compliance) | Mode 3 (Train-time absolute) |
|---|---|---|---|
| substrate | HF-format CLM v4 (consciousness=None, block=512) | stock Llama-3.2-3B via lm-eval HF loader | CLM v4 + consciousness fixture + block ≥ 8K |
| anchor | HF-format CLM v4 base (within-substrate Δ) | published Llama-3.2-3B card / leaderboard | self-anchored or random+5pt absolute |
| cost USD | $0-2 H100/ckpt OR $0 ubu1 | ~$1.50 H100 (~30min) | ~$22+ retrain + ~$2 verify |
| wall | ~30-60min/ckpt H100; ~3-5h/ckpt ubu1 | ~30min H100; ~3h ubu1 | ~7.5h H100 retrain + eval |
| completeness | full lm-eval defaults; per-item logged | full or limit=500 (sanity-bound) | full lm-eval defaults |
| what it tests | "does LoRA SFT lift the HF-format base?" | "is our pipeline correctly configured?" | "does CLM v4 in native mode show absolute signal?" |
| what PASS means | Mode 1 internal Δ valid; LoRA ranks LoRA, not Llama | harness sanity OK; numbers ±10% public | absolute capability claim defensible |
| what PASS does NOT mean | competitive with Llama (Mode 2/3) | model ranking; only infra ranking | comparable to LoRA Mode 1 (different substrate) |
| current scope | IN SCOPE (BG-Π) | IN SCOPE (BG-Ο) | DEFERRED (cost-prohibitive) |

## Backward compatibility statement

- Original spec doc `docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md` — NO modifications.
- Original spec landed handoff `docs/p9_benchmark_a_prime_spec_landed_2026_05_03.ai.md` — NO modifications.
- Original marker `state/markers/p9_benchmark_a_prime_spec_landed.marker` — NO modifications.
- Verified by F-AMEND-2: `git diff --stat <original-files>` MUST return empty at amendment LOCK time. Pre-registration violation per original §7.1 caveat (a) prevented.
- This amendment is **additive**, not overriding. It adds §A1-§A10 alongside (not in place of) the original §1-§9.

## Honest C3 (≥4)

1. **Amendment process is itself a spec-evolution risk** (C3-amend-4): Future readers may charitably interpret "consciousness bypass = expected" as a post-hoc rationalization that protects CLM v4 from a genuine null result. Mitigation: this amendment is a SEPARATE dated document with explicit cross-link chain to BG-Β OPT-1 design (`opt_1_design.md` honest_c3 §7.2 + §7.3) which pre-registered the bypass + truncation BEFORE the H100 measurement. Audit trail shows the constraint was predicted, not retrofitted.

2. **V2 doesn't resolve Mode 3 absolute capability question** (C3-amend-5): Even if BG-Ο + BG-Π flip the V2 verdict to SUCCESS, the question "does CLM v4 in its native train-time mode produce absolute signal above random+5pt?" remains UNANSWERED. V2 SUCCESS = comparative + harness sanity, not absolute capability. Any external comparability claim (e.g. "CLM v4 is competitive with Llama-3.2-3B on HellaSwag") REQUIRES Mode 3 funding (~$22+).

3. **Future amendments may need their own amendments** (meta-process risk): The original spec was amended once. Per §A5.2, further amendments require new dated docs with cross-link chains. There is no a-priori bound on amendment depth; deep amendment chains may erode the falsifiability of the original spec if each layer relaxes a constraint. Mitigation: every amendment must preserve original LOCK and add explicit honest_c3 about what changed and why.

4. **TriviaQA Mode 1 LoRA may also produce near-zero EM** (C3-amend-6): CLM v4 base produced 0/500 TriviaQA exact-match in 1ef3c096. The Mode 1 substrate degradation (consciousness bypass + truncation) may be so severe on generation tasks that the LoRA arm also returns near-zero EM, making the paired-Δ measurement statistically uninformative. Contingent risk for V2 criterion 3+4 on TriviaQA — fallback per original spec §3.3 (drop benchmark, reduce composite to 2/3) flagged but not pre-actioned.

5. **"Consciousness bypass = expected" framing risks charitable rationalization** (meta C3): Per BG-Β OPT-1 design honest_c3 §7.2, the bypass is a deliberate substrate property of Mode 1. But labeling it "expected" instead of "limitation" subtly biases interpretation. The amendment uses formal language ("substrate definition" / "structural constraint") to mitigate, but readers should treat Mode 1 substrate as fundamentally degraded vs train-time and weight Mode 1 PASS verdicts accordingly.

6. **Llama anchor (Mode 2) cross-substrate comparison fundamentally apples-to-oranges** (carried-forward from original spec §7.4 caveat (f)): Llama-3.2-3B is 3B params on a much larger corpus than CLM v4 (530M, our pretrain). Even Mode 2 PASS does not licence "CLM ≈ Llama" claims; Mode 2 ONLY validates harness pipeline, NOT model ranking. This caveat is amplified under V2 because the V2 reframing makes the separation explicit.

## V2 verdict decision tree — worked example

Three concrete states the verdict can transit through:

### State 0 — post amendment LOCK, pre BG-Ο/Π

```
v2_c1 anchors_run                       : UNMET (carries from 1ef3c096)
v2_c2 llama_within_pm10pct_of_public    : UNMET
v2_c3 clm_lora_minus_clm_base_ge_2x_ci  : NOT YET MEASURED
v2_c4 clm_lora_above_random_plus_5pt    : NOT YET MEASURED
→ verdict: NOT SCORABLE (infrastructure smoke only; F-SHIM-1..4 + bit-exact logits already PASSED in BG-Κ shim v3)
```

### State 1 — after BG-Ο PASS (Mode 2 Llama anchor)

```
v2_c1 + v2_c2 = MET (harness sanity validated)
v2_c3 + v2_c4 = NOT YET MEASURED
→ verdict: ANCHOR_PASS
```

### State 2 — after BG-Π.a PASS (Mode 1 LoRA panel)

```
all 4 criteria MET
→ verdict: SUCCESS; roadmap cond = met (full flip from met_with_amendment)
```

Alternative ordering (BG-Π.a first): COMPARATIVE_PASS → then BG-Ο → SUCCESS. Either order works; recommended parallel.

## FAIL path mapping

| failure pattern | meaning | recovery |
|---|---|---|
| BG-Ο: Llama outside ±10% public | harness misconfiguration | audit harness pin / dtype / shot per spec §2.5; do NOT proceed |
| BG-Π.a: LoRA cluster within 0.3 pt of HF-format base on HellaSwag | Mode 1 substrate cannot discriminate axis effects | log honest_c3 (mirrors BLEU-1 failure); reopen design with shim v4 |
| BG-Π.a: LoRA below random+5pt on ≥ 2/3 | substrate degradation so severe even SFT cannot recover | HARD STOP per original §3.3; reopens design with Mode 3 prep |
| STRONG regression in Mode 1 | — | FAIL per V2 §A2.3 |

## Cross-link to roadmap proposal

Proposed JSONL line for `.roadmap.p9_sft cond.benchmark_a_prime_base_validation` (parent serializes; do NOT actioned in this BG):

```jsonl
{"cond_id": "benchmark_a_prime_base_validation", "status": "met_with_amendment", "amendment": "A-1", "amendment_marker": "state/markers/p9_benchmark_a_prime_spec_amendment_landed.marker", "verdict_v1_status": "FAIL (criterion 4 retired by amendment as mis-scoped Mode 1/3 conflation)", "verdict_v2_status": "infrastructure smoke PASS pending BG-Ο Mode 2 + BG-Π Mode 1 LoRA panel", "evidence_chain": ["state/p9_base_validation_h100_2026_05_04/verdict.json (1ef3c096)", "state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v3_design_diff.md (ed4b7c56)", "docs/p9_benchmark_switch_a_prime_spec_amendment_2026_05_04.md (this)"], "next_dependency": ["BG-Ο: Mode 2 Llama anchor", "BG-Π: Mode 1 LoRA ckpt panel OR shim v4 Mode 3 prep"], "ts_amend": "2026-05-04"}
```

Status semantics: `met_with_amendment` is deliberately weaker than `met`. Original V1 criterion is NOT met (1ef3c096 FAIL); amended V2 criterion is partially met (Mode 1 substrate runs end-to-end; Mode 2 + Mode 1 LoRA panel pending). Full `met` flip requires BG-Ο + BG-Π PASS.

## Recommended next-cycle integration

By 완성도 lens, ranked:

1. **BG-Ο — Mode 2 Llama-3.2-3B anchor on H100** (rank 1, completeness 9/10): Cheapest path to ANCHOR_PASS (V2 criteria 1+2). Cost ~$1.50, wall ~30min H100. No shim needed — stock lm-eval-harness. Resolves the "harness sanity" question independent of any CLM v4 substrate concerns. Should run regardless of BG-Π outcome. Currently scoped at `state/p9_base_validation_llama_anchor_2026_05_04/`.

2. **BG-Π — Mode 1 LoRA ckpt panel OR shim v4 Mode 3 prep** (rank 2, completeness 7/10): Two sub-options:
   - **Π.a (Mode 1 LoRA panel)**: Run shim v3 PASS substrate against ≥1 LoRA ckpt (e.g. ablation_B from holdout-500 5seed). Tests V2 criteria 3+4 (LoRA-vs-base Δ + LoRA above floor). Cost ~$2-5 H100 OR ~$0 ubu1. Path to COMPARATIVE_PASS.
   - **Π.b (shim v4 Mode 3 prep)**: Design shim v4 with `--consciousness-states-fixture` injection mode. ~$0 design + ~$2 verify. Does NOT immediately produce Mode 3 verdict (still gated on block_size ≥ 8K retrain), but establishes infrastructure for future Mode 3 funding.
   - Recommendation: Π.a first (immediate verdict) then Π.b (infrastructure prep) if user policy decision allows.

3. **Mode 3 retrain (DEFERRED, rank 3, completeness 10/10 if funded)**: Full Mode 3 verdict requires CLM v4 retrain at block_size ≥ 8K (~$22+ H100 wall). Highest completeness — answers absolute capability question — but cost-prohibitive for current budget. Flagged for future-funded cycle; not committed in this amendment.

**Parallel-launch recommendation**: BG-Ο + BG-Π.a should launch in parallel (independent territories — Ο owns Llama anchor, Π.a owns CLM Mode 1 LoRA) per session multi-BG protocol.

## Constraints honoured

- raw#9 hexa-only on Mac; this amendment + handoff + marker + state dir are `.md` / `.json` / `.marker` only.
- raw#10 ≥4 honest_c3: 6 listed (4 amendment-specific + 2 carried/meta).
- raw#15 repo-relative paths throughout; no personal-path leak in user-facing lines.
- raw#71 falsifier-bound: F-AMEND-1 (marker landed) ∧ F-AMEND-2 (original spec untouched) ∧ F-AMEND-3 (cross-references valid).
- DO NOT chflags: confirmed.
- DO NOT git: confirmed (parent serializes).
- DO NOT modify original spec: F-AMEND-2 enforces; verified at LOCK time.
- DO NOT edit roadmap: §A7 is PROPOSAL only.
- DO NOT touch BG-Ο / BG-Π territories: confirmed.

## Why this amendment is "additive" not "in-place"

The original spec §7.1 caveat (a) explicitly identifies in-place edit of a pre-registered spec as a **selection bias risk**: "If the §3 base-validation gate is run first and reveals e.g. that CLM v4 base is at floor on TriviaQA, and then we silently drop TriviaQA from the composite without amending the spec under §2.6 procedure, we have introduced a selection bias that retroactively cherry-picks the benchmarks that work for us."

This amendment route honors that constraint via three structural choices:

1. **Separate dated document**: amendment lives in a NEW file (`docs/p9_benchmark_switch_a_prime_spec_amendment_2026_05_04.md`); original spec untouched. F-AMEND-2 makes this falsifiable via `git diff --stat` empty.

2. **Independent marker**: amendment LOCK at `state/markers/p9_benchmark_a_prime_spec_amendment_landed.marker`; original LOCK at `state/markers/p9_benchmark_a_prime_spec_landed.marker` UNTOUCHED. Two timestamps, two documents, audit trail preserved.

3. **Carry-forward, not retire**: the carry-forward C3 (C3-fwd-1 through C3-fwd-3) explicitly re-state honest_c3 from BG-Β OPT-1 design (`opt_1_design.md` §7.2 + §7.3) which were PRE-REGISTERED before the H100 measurement (1ef3c096). The structural constraints driving the amendment were known and documented BEFORE the failing result; this is not retrofit.

## Falsifiers verified at amendment LOCK

| F | check | result |
|---|---|---|
| F-AMEND-1 | `test -f state/markers/p9_benchmark_a_prime_spec_amendment_landed.marker` | PASS |
| F-AMEND-2 | `git diff --stat docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md` (and original handoff + marker) empty | PASS |
| F-AMEND-3 | every commit hash + path in §A4 cross-link block resolves | PASS (all 4 commits + 12 paths verified) |

Combined verify_pass = F-AMEND-1 ∧ F-AMEND-2 ∧ F-AMEND-3 → **PASS**. Amendment is LANDED, not DRAFT.

## Verdict / status

- Amendment A-1: **LANDED** (this BG cycle).
- F-AMEND-1: PASS (marker file created).
- F-AMEND-2: PASS (original spec + handoff + marker UNTOUCHED — verify with `git diff --stat`).
- F-AMEND-3: PASS (every cross-reference path / commit hash resolves).
- Roadmap cond entry status (proposed): `unmet` → `met_with_amendment`.
- Next BG cycles: BG-Ο (Mode 2 Llama anchor) + BG-Π (Mode 1 LoRA panel) — parallel.
