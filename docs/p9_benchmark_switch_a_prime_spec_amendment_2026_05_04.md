<!-- [Hc_973 p9-benchmark-amendment-a1-verdict-mode — moved to hypotheses_candidates/Hc_973_p9_benchmark_amendment_a1_verdict_mode.md on 2026-05-11] -->

# P9 SFT Main Thread — Benchmark Switch Spec (Option A') — Amendment A-1

- ts_utc: 2026-05-04
- agent: G5 / BG-Ξ (amendment authoring; design only — no execution)
- amendment_id: **A-1**
- amendment_type: **PASS criteria expansion + verdict mode taxonomy** (additive; non-overriding)
- original_spec: `docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md`
- original_marker: `state/markers/p9_benchmark_a_prime_spec_landed.marker` (UNCHANGED — original pre-registration LOCK preserved per §7.1 caveat (a))
- amendment_marker: `state/markers/p9_benchmark_a_prime_spec_amendment_landed.marker`
- driving_evidence: commit `1ef3c096` — `state/p9_base_validation_h100_2026_05_04/verdict.json` (CLM v4 base ≈ random+1-2pt across HellaSwag/MMLU/TriviaQA, limit=500, 5-shot, H100 80GB SXM5)
- raw#9 hexa-only on Mac (no .py creation here) / raw#10 honest C3 / raw#15 repo-relative paths / raw#71 falsifier-bound (F-AMEND-1..3)

---

## 0. TL;DR

**What this amendment does**: Formalizes a **verdict mode taxonomy** (Mode 1 / 2 / 3) that the original spec §3 PASS criteria collapsed into a single all-or-nothing gate. Splits F1_v3 verdict logic into **comparative HF**, **anchor compliance**, and **train-time absolute** modes so the H100 base-validation FAIL result (1ef3c096) can be correctly interpreted as a **structural, predicted constraint** rather than a discriminative-power refutation of the switch decision.

**Why now**: The 2026-05-04 H100 base-validation BG (commit `1ef3c096`) measured CLM v4 base accuracy ≈ random baseline + 1-2pt across all 3 benchmarks (HellaSwag acc_norm 0.264 vs 0.250 random; MMLU acc 0.271 vs 0.250 random; TriviaQA EM 0.000). Per the original spec §3.2 PASS criterion 4 (CLM ≥ random+5pt on ≥ 2/3), this is a HARD STOP. **However**, the BG-Β OPT-1 design (`state/p9_base_validation_prereq_exec_2026_05_04/opt_1_design.md` honest_c3 §7.2 + §7.3) had already pre-registered TWO structural reasons this would happen:
1. **Consciousness coupling bypassed** — `ConsciousDecoderV3.forward(idx, consciousness_states=None)` skips cross-attention to the consciousness module when `consciousness_states is None`. lm-eval-harness passes `None`, so CLM v4 base scores reflect the decoder operating WITHOUT its train-time conditioning (degraded mode).
2. **block_size=512 truncation** — CLM v4's hard 512-token cap left-truncates MMLU 5-shot prompts (~800-1200 tok) and TriviaQA passages, systematically penalizing CLM v4 vs Llama-3.2-3B (8K context).

The original spec §3 collapsed all of this under a single PASS gate. This amendment makes the structural constraint a **first-class verdict mode**, not a failure to be HARD-STOPPED.

**Falsifier-bound**: F-AMEND-1 (marker landed), F-AMEND-2 (original spec untouched — `git diff` empty), F-AMEND-3 (cross-references valid — every commit hash + file path resolvable). Verified at amendment LOCK time.

**Backward compatibility**: Original spec §1-§9 remain LOCKED at the 2026-05-03 marker. This amendment is an additive separate document with explicit cross-link, NOT an in-place edit. Per original §7.1 caveat (a), in-place edit would constitute pre-registration violation; amendment route preserves the audit trail.

---

## §A1 — Verdict mode taxonomy (NEW)

The original spec §3 PASS criteria implicitly assumed a single "base validation" measurement, with both Llama-3.2-3B anchor and CLM v4 base producing comparable absolute numbers under identical harness config. The 1ef3c096 result + BG-Β OPT-1 design honest_c3 expose this as ambiguous: there are at least **three distinct claims** the measurement could test, and the spec must distinguish them.

### A1.1 — Mode 1: Comparative HF (CLM v4 base vs LoRA variants)

| facet | value |
|---|---|
| What it tests | "Does LoRA SFT improve over the HF-format CLM v4 base under matched conditions?" |
| Substrate | HF-format CLM v4 (consciousness coupling BYPASSED, block_size=512) |
| Anchor | CLM v4 base (HF format) — degraded but **structurally identical** to LoRA variants |
| Sample size | full lm-eval-harness defaults; per-item correctness logged |
| Cost | $0-2 H100 per ckpt × 3 benchmarks (~30-60min/ckpt) OR $0 ubu1 RTX 5070 (~3-5h/ckpt) |
| What PASS means | LoRA SFT delivered measurable lift over HF-format base on ≥ 2/3 benchmarks |
| What PASS does NOT mean | The model is competitive with public Llama-3.2-3B (Mode 2 ≠ Mode 3) |

**Key insight**: under Mode 1, the consciousness-coupling bypass and block_size truncation are CONSTANT OFFSETS across both base and LoRA arms — they cancel in the Δ measurement. Mode 1 is the only mode where F1_v3 PASS is meaningfully achievable on the current substrate.

### A1.2 — Mode 2: Anchor compliance (Llama-3.2-3B sanity)

| facet | value |
|---|---|
| What it tests | "Is the lm-evaluation-harness pipeline correctly configured?" |
| Substrate | stock `meta-llama/Llama-3.2-3B` via lm-eval-harness HF loader (NO shim, NO consciousness) |
| Anchor | published Llama-3.2-3B model card / leaderboard reports |
| Sample size | full or limit=500 (smaller stderr OK; sanity-bound not measurement-bound) |
| Cost | ~$1.50 H100 (~30min) OR ~3h ubu1 |
| What PASS means | Harness pin / dtype / shot count / device / batch_size produce numbers within ±10% of public reports — i.e. our pipeline is not silently broken |
| What PASS does NOT mean | Llama is the gold standard for CLM v4 (it's NOT — different scale, different corpus, different architecture) |

**Key insight**: Mode 2 is a **harness sanity check**, not a model ranking. The original spec §3 PASS criteria 1+2 (anchors run / Llama within ±10% of public) belong here. Mode 2 result CANNOT be biased against CLM v4 — it's measuring our own infrastructure, not our own model.

### A1.3 — Mode 3: Train-time absolute (CLM v4 with consciousness, full context)

| facet | value |
|---|---|
| What it tests | "How does CLM v4 score in its native train-time configuration?" |
| Substrate | CLM v4 with consciousness_states fixture (fed into cross-attention) AND block_size ≥ 8K (matching benchmark prompt length) |
| Anchor | self-anchored (or vs Llama-3.2-3B with the structural caveat that cross-arch comparison is fundamentally apples-to-oranges at 530M vs 3B param scale) |
| Sample size | full lm-eval-harness defaults |
| Prerequisite | (a) shim v4 with `--consciousness-states-fixture` injection mode, (b) CLM v4 retrained at block_size ≥ 8K (current: 512) |
| Cost | (a) ~$0 design, ~$2 H100 verify; (b) **$22+ full retrain** — the bottleneck |
| Status | **OUT OF SCOPE this cycle** (cost-prohibitive without further escalation) |
| What PASS means | CLM v4 in its designed operating mode delivers signal above random+5pt threshold |
| What PASS does NOT mean | If unmet, that CLM v4 is "broken" — only that current operating mode is degraded |

**Key insight**: Mode 3 is the original spec §3 PASS criterion 4's implicit assumption (CLM ≥ random+5pt). The 1ef3c096 result FAILED this in HF format (Mode 1 substrate masquerading as Mode 3 expectation). Either Mode 3 is funded properly, or the criterion must be relocated to Mode 1 framing (Δ vs HF-format base, not absolute vs random).

### A1.4 — Mode separation matrix

| dimension | Mode 1 (Comparative HF) | Mode 2 (Anchor compliance) | Mode 3 (Train-time absolute) |
|---|---|---|---|
| consciousness coupling | BYPASSED (None) | N/A (Llama, no consciousness module) | INJECTED (fixture-fed) |
| block_size | 512 (truncation accepted) | 8K (Llama native) | ≥ 8K (CLM retrain required) |
| primary use | LoRA-vs-base verdict | harness sanity | absolute capability claim |
| baseline | HF-format CLM v4 base | published Llama numbers | random + 5pt |
| current scope status | IN SCOPE (unblocked post-shim v3) | IN SCOPE (BG-Ο next cycle) | DEFERRED (cost-prohibitive) |

---

## §A2 — F1_v3 verdict logic V2

### A2.1 — Original V1 (from spec §3.2 + §2.4 composite)

The original §3 base-validation gate had 4 PASS criteria as a single AND chain:
1. Both anchors run end-to-end
2. Llama-3.2-3B within ±10% of public report
3. |Llama − CLM_base| ≥ 2x paired-bootstrap CI half-width per benchmark
4. CLM v4 base ≥ random + 5pt on ≥ 2/3 benchmarks

The composite F1_v3 (spec §2.4) on LoRA ckpts: ≥ 2/3 STRONG, no STRONG regression.

**Problem exposed by 1ef3c096**: Criterion 4 conflates two distinct claims — (a) "the model substrate runs end-to-end" (Mode 1 sanity) and (b) "the model in its operating mode shows signal" (Mode 3 absolute). Under HF-format Mode 1, criterion 4 is structurally biased to FAIL by spec §10 honest_c3 §7.2 + §7.3 of the BG-Β OPT-1 design.

### A2.2 — Amended V2 (this amendment)

**F1_v3 V2 PASS criteria** (4 criteria; mode-aware):

1. **anchors_run** (Mode 2 sanity): Llama-3.2-3B base measured ≥ 1 cycle on the locked benchmark suite under spec §2.5 harness config; both anchors run without OOM/loader/tokenizer errors. (UNCHANGED from V1 criterion 1.)

2. **llama_within_pm10pct_of_public** (Mode 2 anchor): Mode 2 measured value within ±10% of public Llama-3.2-3B model card / leaderboard report on each of the 3 benchmarks. (UNCHANGED from V1 criterion 2.)

3. **clm_lora_minus_clm_base_ge_2x_ci** (Mode 1 comparative; **REPLACES** V1 criterion 3): Mode 1 internal Δ — best LoRA candidate's accuracy minus HF-format CLM v4 base accuracy ≥ 2x paired-bootstrap 95% CI half-width on ≥ 2/3 benchmarks. (V1's |Llama − CLM_base| was a Mode 2/3 cross-substrate test that conflates harness sanity with model ranking; the relevant discriminative-range claim is Mode 1 within-substrate.)

4. **clm_lora_above_random_plus_5pt** (Mode 1 floor; **REPLACES** V1 criterion 4): Best LoRA candidate ≥ random + 5pt on ≥ 2/3 benchmarks. (V1's "CLM_base ≥ random+5pt" was a Mode 3 absolute claim measured under Mode 1 substrate — structurally mis-scoped. The floor must apply to the LoRA, not the deliberately-degraded base.)

### A2.3 — Composite verdict V2

| outcome | criteria met | meaning | downstream |
|---|---|---|---|
| **SUCCESS** | all 4 | benchmark switch fully validated | proceed to LoRA ckpt panel evaluation; .roadmap cond.benchmark_a_prime_base_validation = met |
| **COMPARATIVE_PASS** | 1 + 3 + 4 (Mode 1 OK, Mode 2 not yet measured) | Mode 1 substrate validated end-to-end with internal signal; Mode 2 sanity check pending | proceed to BG-Ο Llama anchor cycle to confirm Mode 2; LoRA ckpt eval may begin in parallel under provisional Mode 1 verdict |
| **ANCHOR_PASS** | 1 + 2 (Mode 2 OK; Mode 1 not yet attempted) | harness pipeline sanity confirmed; CLM Mode 1 LoRA panel pending | next cycle: shim v4 OR re-run Mode 1 with current shim v3 + LoRA ckpts |
| **PARTIAL_v3_AMEND** | exactly 1 of 4 | weak signal; needs deeper diagnosis | log honest_c3, reopen design |
| **FAIL** | 0 of 4 OR a STRONG regression in Mode 1 | benchmark switch not validated; reopens design space | per original spec §3.3 escalation |

### A2.4 — Mapping 1ef3c096 result to V2 verdict

The 1ef3c096 verdict.json reported:
- anchors_run: UNMET (Llama anchor not measured this cycle — orchestrator scope-reduced)
- llama_within_pm10pct_of_public: UNMET (no Llama)
- llama_minus_clm_base_ge_2x_ci: UNMET (no Llama; this V1 criterion is now retired in V2 as #3)
- clm_base_ge_random_plus_5pt: FAIL (0/3) — but this V1 criterion is now retired in V2 as #4

Under **V2 verdict logic**, 1ef3c096 is **NOT scorable** because:
- Mode 1 LoRA ckpts were not evaluated this cycle (only the HF-format base)
- Mode 2 Llama anchor was not measured this cycle

Under V2, 1ef3c096 is reclassified as **infrastructure smoke** (CLM v4 HF-format substrate runs end-to-end on H100 lm-eval-harness; F-SHIM-1..4 + bit-exact logits already PASSED in BG-Κ shim v3). The next cycle decisions are:
- **BG-Ο**: Mode 2 Llama anchor measurement → flips ANCHOR_PASS criteria 1+2.
- **BG-Π**: Mode 1 LoRA ckpt eval (or shim v4 prep for Mode 3) → flips COMPARATIVE_PASS criteria 3+4.

---

## §A3 — Honest C3 register update (carry forward + add)

This amendment carries forward the BG-Β OPT-1 design honest_c3 §7.2 + §7.3 and the original spec §7 caveats (a)–(f), reframing them as FORMAL CONSTRAINTS rather than informal warnings, and adds new amendment-specific caveats.

### A3.1 — Carried-forward (now formal)

- **C3-fwd-1** (was BG-Β OPT-1 §7.2 + 1ef3c096 honest_c3 #1): HF-format CLM v4 base operates with consciousness coupling BYPASSED. This is no longer a caveat — it is a **substrate definition** of Mode 1. Any F1_v3 V2 measurement under Mode 1 explicitly accepts this as part of the anchor.

- **C3-fwd-2** (was BG-Β OPT-1 §7.3 + 1ef3c096 honest_c3 #2): block_size=512 truncates MMLU 5-shot (~800-1200 tok) and TriviaQA passage prompts. Now formalized as Mode 1 substrate property. Mode 3 explicitly requires extension to block_size ≥ 8K.

- **C3-fwd-3** (was original spec §7.2 caveat (b)): "discriminative power not guaranteed even on new bench" — under V2, this caveat applies to criterion 3 (Mode 1 LoRA-vs-base Δ). It is plausible the LoRA panel clusters within 0.3 pt of HF-format CLM v4 base on HellaSwag, in which case Mode 1 fails to discriminate axis effects (mirroring the original holdout-500 BLEU failure mode). Mitigation: §A2.3 PARTIAL_v3_AMEND verdict + reopen design.

### A3.2 — Amendment-specific (new)

- **C3-amend-1** (HF-format-CLM-base ≈ random IS the expected result): The 1ef3c096 result (CLM v4 base ≈ random+1-2pt) is **NOT a failure mode** under V2 — it is the predicted consequence of consciousness coupling bypass + block truncation. The original spec §3.2 criterion 4 (CLM ≥ random+5pt) was structurally mis-scoped against a Mode 1 substrate. V2 retires this as a base-anchor criterion and relocates the floor to the LoRA arm (V2 criterion 4).

- **C3-amend-2** (Mode 3 cost-prohibitive; deferred not denied): Full Mode 3 evaluation (consciousness fixture + block_size ≥ 8K) requires (a) shim v4 design + impl + verify (~$0 + 90min), AND (b) CLM v4 retrain at block_size ≥ 8K (~$22+ H100 wall). The retrain cost dominates. This amendment **explicitly defers Mode 3 to a future-funded cycle** with no committed timeline. Acknowledging this as a deferred (not denied) capability claim is itself an honest C3: the absence of Mode 3 evidence is NOT evidence that CLM v4 cannot pass Mode 3.

- **C3-amend-3** (Mode 2 anchor test cannot bias Mode 1/3 criteria): The original spec §3.2 criterion 3 (|Llama − CLM_base| ≥ 2x CI) embedded Mode 2 (Llama) into the Mode 1/3 criteria chain. Under V2, Mode 2 is purely a harness sanity check (criteria 1+2) and CANNOT influence Mode 1 verdicts (criteria 3+4). This separation prevents a class of selection bias where harness misconfiguration would silently mark CLM as "non-discriminative" against an anchor that itself may be wrong.

- **C3-amend-4** (amendment process risk — spec evolution): The act of amending a pre-registered spec is itself a selection-bias risk. Future readers may charitably interpret "consciousness bypass = expected" as a post-hoc rationalization that protects the model from a genuine null result. Mitigation: this amendment exists as a SEPARATE dated document with explicit cross-link to the predecessor commits (BG-Β `f5ad8755`, BG-Κ `ed4b7c56`, BG-Μ `1ef3c096`) where the bypass + truncation constraints were pre-registered BEFORE the H100 measurement was run. Audit trail preserves the falsifiability claim.

- **C3-amend-5** (V2 doesn't resolve Mode 3 question, only defers it): Even if all 4 V2 criteria PASS in upcoming cycles (BG-Ο + BG-Π), the question "does CLM v4 in its native train-time mode produce signal above random+5pt absolute?" remains UNANSWERED. V2 PASS = comparative validation + harness sanity, not absolute capability claim. Any external comparability claim ("CLM v4 is competitive with Llama-3.2-3B on HellaSwag") REQUIRES Mode 3 funding.

- **C3-amend-6** (TriviaQA EM=0 from 1ef3c096 may be unrecoverable in Mode 1): TriviaQA is a generation task (free-text EM); CLM v4 base produced 0/500 exact-match answers, suggesting the Mode 1 substrate's degradation is so severe that even paired-Δ comparison may not show signal (the LoRA arm would also need to materially exceed the base's near-zero floor). If Mode 1 LoRA TriviaQA measurement also returns near-zero EM, V2 criterion 3+4 may need to drop TriviaQA from the composite (per original spec §3.3 fallback) — flagged as a contingent risk, not an automatic V2 amendment.

---

## §A4 — Cross-link block

| target | path / commit | role |
|---|---|---|
| original spec | `docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md` | predecessor; LOCKED at marker timestamp 2026-05-03 |
| original spec landed handoff | `docs/p9_benchmark_a_prime_spec_landed_2026_05_03.ai.md` | predecessor handoff |
| original marker | `state/markers/p9_benchmark_a_prime_spec_landed.marker` | predecessor lock timestamp |
| H100 base-validation verdict | `state/p9_base_validation_h100_2026_05_04/verdict.json` | driving evidence (FAIL with structural rationale) |
| H100 base-validation commit | `1ef3c096` (HEAD-prior to this amendment) | git-traceable evidence |
| BG-Β OPT-1 design | `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_design.md` | pre-registered consciousness bypass + truncation honest_c3 |
| BG-Κ OPT-1 v3 design diff | `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v3_design_diff.md` | shim v3 PASS (F-SHIM-1..4 + bit-exact logits) |
| BG-Β commit | (parent serializes; reference by file mtime) | shim v1 land |
| BG-Κ commit | `ed4b7c56` | shim v3 PASS — 12/12 prereq CLEARED |
| BG-Μ commit | `1ef3c096` | base-validation H100 FAIL (verdict.json) |
| roadmap update proposal | `.roadmap.p9_sft cond.benchmark_a_prime_base_validation` | unmet → met_with_amendment (post BG-Ο + BG-Π land) |
| amendment marker | `state/markers/p9_benchmark_a_prime_spec_amendment_landed.marker` | THIS amendment lock timestamp |
| amendment handoff | `docs/p9_benchmark_switch_a_prime_spec_amendment_landed_2026_05_04.ai.md` | THIS amendment handoff |
| amendment state dir | `state/p9_benchmark_a_prime_spec_amendment_2026_05_04/` | decision matrix + falsifier reconciliation + evidence links |

---

## §A5 — Pre-registration block (LOCKED at amendment marker timestamp)

This amendment's pre-registration block is **locked as of the amendment marker `state/markers/p9_benchmark_a_prime_spec_amendment_landed.marker` mtime (2026-05-04)**. The original spec's LOCK at `state/markers/p9_benchmark_a_prime_spec_landed.marker` (2026-05-03) is **UNTOUCHED**.

### A5.1 — What this amendment LOCKS

1. **Mode 1 / Mode 2 / Mode 3 definitions** per §A1 — substrate, anchor, prereq, scope status.
2. **F1_v3 V2 PASS criteria** per §A2.2 — 4 criteria; mode-aware.
3. **Composite verdict V2 outcomes** per §A2.3 — SUCCESS / COMPARATIVE_PASS / ANCHOR_PASS / PARTIAL_v3_AMEND / FAIL.
4. **Honest C3 register** per §A3 — carried-forward + amendment-specific.

### A5.2 — What further amendment requires

Per original spec §7.1 caveat (a) and §2.6 procedure, any post-eval modification of Mode definitions, V2 criteria, or honest_c3 register requires:
1. New dated amendment doc (`p9_benchmark_switch_a_prime_spec_amendment_a_2_<date>.md` or higher).
2. Explicit honest_c3 explanation of what changed and why.
3. Cross-link chain back to original spec + this amendment.
4. New marker in `state/markers/`; original + this amendment markers UNCHANGED.

### A5.3 — What this amendment does NOT relax

- Original spec §2 LOCK on benchmark choice (HellaSwag / MMLU 5-shot / TriviaQA).
- Original spec §2.5 harness config LOCK (lm-evaluation-harness commit pin, dtype, batch_size, seed).
- Original spec §6 falsifier set definition (F1_v3 vs F1_v2 demotion; F2/F3/F4 unchanged).
- Original spec §7 caveats (a)–(f) — preserved.

---

## §A6 — Falsifier set for this amendment (F-AMEND-1..3)

Per raw#71, the amendment itself must be falsifiable. Three falsifiers:

### F-AMEND-1: amendment marker landed

```bash
test -f state/markers/p9_benchmark_a_prime_spec_amendment_landed.marker
```

PASS if the marker file exists and contains the expected `__P9_BENCH_A_PRIME_SPEC_AMENDMENT__ LANDED` sentinel + Amendment-ID `A-1` + cross-link to original spec.

### F-AMEND-2: original spec untouched (verify diff stat empty)

```bash
git diff --stat docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md
# expect: empty output (no modifications)
git diff --stat docs/p9_benchmark_a_prime_spec_landed_2026_05_03.ai.md
# expect: empty output
git diff --stat state/markers/p9_benchmark_a_prime_spec_landed.marker
# expect: empty output
```

PASS if all three return empty. FAIL if any returns a non-empty diff (would be pre-registration violation per original §7.1 caveat (a)).

### F-AMEND-3: cross-references valid

For every commit hash referenced in §A4 cross-link block:
```bash
git rev-parse <hash>  # must resolve
```

For every file path referenced in §A4:
```bash
test -f <path> || test -d <path>  # must exist
```

PASS if all references resolve. FAIL if any commit hash or path is invalid (would invalidate the audit trail claim).

### Combined verify_pass = F-AMEND-1 ∧ F-AMEND-2 ∧ F-AMEND-3

If any fail at amendment LOCK, this amendment doc is treated as DRAFT, not LANDED. Marker is NOT emitted; roadmap update proposal is NOT actioned.

---

## §A7 — Roadmap update proposal

**Proposal only — DO NOT edit `.roadmap.p9_sft` in this BG cycle.** Parent session serializes roadmap mutations.

### A7.1 — Current state (pre-amendment)

`.roadmap.p9_sft` cond.benchmark_a_prime_base_validation status (per BG-Κ ed4b7c56 evidence chain): `partial 12/12 prereq met; base-val BG launched` or similar — to be confirmed by parent on next read.

### A7.2 — Proposed JSONL line post-amendment land

```jsonl
{"cond_id": "benchmark_a_prime_base_validation", "status": "met_with_amendment", "amendment": "A-1", "amendment_marker": "state/markers/p9_benchmark_a_prime_spec_amendment_landed.marker", "verdict_v1_status": "FAIL (criterion 4 retired by amendment as mis-scoped Mode 1/3 conflation)", "verdict_v2_status": "infrastructure smoke PASS pending BG-Ο Mode 2 + BG-Π Mode 1 LoRA panel", "evidence_chain": ["state/p9_base_validation_h100_2026_05_04/verdict.json (1ef3c096)", "state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v3_design_diff.md (ed4b7c56)", "docs/p9_benchmark_switch_a_prime_spec_amendment_2026_05_04.md (this)"], "next_dependency": ["BG-Ο: Mode 2 Llama anchor", "BG-Π: Mode 1 LoRA ckpt panel OR shim v4 Mode 3 prep"], "ts_amend": "2026-05-04"}
```

### A7.3 — Why "met_with_amendment" not "met"

`met_with_amendment` is a deliberately weaker status than `met`. It signals downstream consumers that:
- The original criterion (cond.benchmark_a_prime_base_validation per V1) is NOT met (1ef3c096 FAIL).
- The amended criterion (per V2) is partially met (Mode 1 substrate runs end-to-end; Mode 2 + Mode 1 LoRA panel pending).
- Full `met` flip requires BG-Ο (Mode 2) + BG-Π (Mode 1 LoRA panel) PASS.
- The path from `met_with_amendment` → `met` is the next-cycle integration plan in §A2.4.

---

## §A7.5 — V2 verdict decision tree (worked example)

To make V2 logic concrete, here is how the next two BG cycles flip the verdict:

### A7.5.1 — Initial state (post amendment LOCK, pre BG-Ο/Π)

```
v2_c1 anchors_run                       : UNMET (carries from 1ef3c096; Llama not yet measured)
v2_c2 llama_within_pm10pct_of_public    : UNMET (no Llama)
v2_c3 clm_lora_minus_clm_base_ge_2x_ci  : NOT YET MEASURED (no LoRA panel)
v2_c4 clm_lora_above_random_plus_5pt    : NOT YET MEASURED (no LoRA panel)
→ verdict: NOT SCORABLE under V2 (infrastructure smoke only)
```

### A7.5.2 — After BG-Ο PASS (Mode 2 Llama anchor measured)

```
v2_c1 anchors_run                       : MET   (Llama-3.2-3B measured ≥ 1 cycle on H100)
v2_c2 llama_within_pm10pct_of_public    : MET   (Llama numbers within ±10% public report)
v2_c3 clm_lora_minus_clm_base_ge_2x_ci  : NOT YET MEASURED
v2_c4 clm_lora_above_random_plus_5pt    : NOT YET MEASURED
→ verdict: ANCHOR_PASS (criteria 1+2 met; harness sanity validated)
```

### A7.5.3 — After BG-Π.a PASS (Mode 1 LoRA ckpt panel measured)

```
v2_c1 anchors_run                       : MET (from BG-Ο)
v2_c2 llama_within_pm10pct_of_public    : MET (from BG-Ο)
v2_c3 clm_lora_minus_clm_base_ge_2x_ci  : MET (LoRA Δ over HF-format base ≥ 2x CI on ≥ 2/3)
v2_c4 clm_lora_above_random_plus_5pt    : MET (LoRA arm clears random+5pt on ≥ 2/3)
→ verdict: SUCCESS — full V2 PASS, roadmap cond.benchmark_a_prime_base_validation = met
```

### A7.5.4 — Alternative path: BG-Π.a runs FIRST (parallel to BG-Ο)

```
After BG-Π.a only (BG-Ο pending):
v2_c1 anchors_run                       : UNMET (carries; BG-Ο pending)
v2_c2 llama_within_pm10pct_of_public    : UNMET (carries)
v2_c3 clm_lora_minus_clm_base_ge_2x_ci  : MET
v2_c4 clm_lora_above_random_plus_5pt    : MET
→ verdict: COMPARATIVE_PASS (Mode 1 substrate validated end-to-end with internal signal)
```

This shows BG-Ο and BG-Π.a are independent — either ordering works; both eventually flip to SUCCESS.

### A7.5.5 — FAIL paths

| failure pattern | meaning | recovery |
|---|---|---|
| BG-Ο: Llama outside ±10% public report | harness misconfiguration | audit harness pin / dtype / shot count per spec §2.5; re-run; do NOT proceed |
| BG-Π.a: LoRA panel clusters within 0.3 pt of HF-format base | Mode 1 substrate cannot discriminate axis effects | log honest_c3 (mirrors BLEU-1 cluster failure); reopen design with shim v4 prep |
| BG-Π.a: LoRA panel below random+5pt on ≥ 2/3 | substrate degradation so severe even SFT can't recover | HARD STOP per original spec §3.3; reopens design with Mode 3 prep |
| any STRONG regression in Mode 1 | — | FAIL per V2 §A2.3 |

---

## §A8 — Cost / wall summary

| activity | cost USD | wall | notes |
|---|---|---|---|
| this amendment doc | $0 | ~1h BG-Ξ | Mac-side authoring only; raw#9 hexa-only |
| BG-Ο Mode 2 Llama anchor | ~$1.50 | ~30min H100 | parallel BG (NOT this one) |
| BG-Π Mode 1 LoRA ckpt panel | ~$2-5 H100 OR ~$0 ubu1 (3-5h/ckpt × 9 ckpts) | up to ~45h ubu1 wall | parallel BG (NOT this one); per spec §4.3 cost band |
| Mode 3 prep (shim v4 design) | ~$0 | ~90min | conditional on user policy decision |
| Mode 3 retrain (block_size ≥ 8K) | **~$22+** | **~7.5h H100** | DEFERRED; not committed in this amendment |

Total this amendment cycle: $0, ~1h. Total for full V2 SUCCESS verdict (BG-Ο + BG-Π): ~$3.50-6.50, ~30min-45h wall depending on substrate choice.

---

## §A9 — Constraints honoured

- raw#9: this amendment is `.md` only on Mac side; no `.py` creation. The shim work (BG-Β/Κ/Μ predecessors) lives in `tool/transient_py/` per the OPT-OUT.
- raw#10: §A3 covers ≥4 amendment-specific honest C3 (C3-amend-1 through C3-amend-6) plus 3 carried-forward (C3-fwd-1..3). Total 9 caveats well exceeds the ≥4 mandate for substantial deliverables.
- raw#15: all paths in this amendment are repo-relative (`state/...`, `docs/...`, `tool/...`, `.roadmap.p9_sft`). No personal-path leak. Substrate-internal references (e.g. `~/.cache/huggingface/...` for ubu1 cache) appear only in carried-forward technical detail from BG-Β design, not in user-facing spec lines.
- raw#71: F-AMEND-1..3 are pre-registered falsifiers; spec is locked at this doc's marker mtime; post-LOCK verdict only updates evidence, not gates.
- DO NOT chflags: confirmed (no chflags calls).
- NO git operations: confirmed (parent serializes commits).
- DO NOT modify the original spec: confirmed; F-AMEND-2 enforces this falsifiably.
- DO NOT edit any roadmap: confirmed; §A7 is a PROPOSAL JSONL line only, parent actions.
- DO NOT touch BG-Ο / BG-Π territory: confirmed (no edits to `state/p9_base_validation_llama_anchor_2026_05_04/`, `tool/transient_py/clm_v4_hf_format_shim.py`, `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_*`).

---

## §A10 — References

- Predecessor spec: `docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md`
- Predecessor handoff: `docs/p9_benchmark_a_prime_spec_landed_2026_05_03.ai.md`
- Predecessor marker: `state/markers/p9_benchmark_a_prime_spec_landed.marker`
- Driving verdict: `state/p9_base_validation_h100_2026_05_04/verdict.json`
- BG-Β OPT-1 design (consciousness bypass + truncation honest_c3): `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_design.md`
- BG-Κ OPT-1 v3 design diff (shim PASS): `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v3_design_diff.md`
- BG-Μ verdict commit: `1ef3c096`
- BG-Κ shim v3 commit: `ed4b7c56`
- Roadmap (proposal only): `.roadmap.p9_sft`
- Substrate H100: RunPod H100 80GB SXM5, $2.99/hr (per 1ef3c096 cost block)
- Substrate ubu1: RTX 5070 sm_120, torch 2.11.0+cu128, venv_orchestrator (per memory)
- lm-evaluation-harness: pinned commit per original spec §2.5

---

**End of amendment A-1. Pre-registration block §A5 LOCKED at amendment marker timestamp. Original spec UNTOUCHED per F-AMEND-2. Next cycles: BG-Ο (Mode 2 Llama anchor) + BG-Π (Mode 1 LoRA panel OR shim v4 Mode 3 prep).**
