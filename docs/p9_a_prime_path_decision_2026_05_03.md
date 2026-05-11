<!-- [Hc_979 p9-a-prime-path-decision-llama-lora-delta — moved to hypotheses_candidates/Hc_979_p9_a_prime_path_decision_llama_lora_delta.md on 2026-05-11] -->

# P9 A' Main Eval — Path Decision Spec

- ts_utc: 2026-05-03
- agent: subagent BG (decision-spec only — NO execution)
- spec_id: p9_a_prime_path_decision_2026_05_03
- status: **DRAFT-LOCKED** (binding before any A' main eval execution)
- supersedes: nothing (first path-decision doc post-base-validation)
- decision_basis: A' base-validation revealed CLM v4 base = ARCHITECTURAL_BLOCKER on English benchmarks; original A' spec assumed CLM v4 base would produce a non-floor anchor. That assumption is falsified.
- raw#9 hexa-only on Mac (no .py creation here) / raw#15 no personal-path leak / raw#10 honest C3 in §6 + per-path subsections / $0 design only — no execution

---

## 0. TL;DR

**Critical reframe** (from `docs/p9_benchmark_base_validation_landed_2026_05_03.ai.md`):

1. Llama-3.2-3B-Instruct base validated on all 3 benchmarks at 4-bit:
   - TriviaQA EM = **0.514** (51.4 pt vs random 0)
   - HellaSwag acc_norm = **0.644** (39.4 pt vs random 25%)
   - MMLU acc (0-shot avg) = **0.608** (35.8 pt vs random 25%)
   - All three exceed the §3.2 spec's 5-pt-above-random discriminative-range threshold.
2. **CLM v4 base = ARCHITECTURAL_BLOCKER**: stub HF mirror, custom Federated/Phase-Optimal architecture (581 keys), 64K multilingual BPE (incompatible with HF tokenizer pipeline), training CE = 0.046 (perplexity ≈ 1.05 = narrow-corpus memorization, NOT general-purpose English LM), and `consciousness_laws.py` `_doc` dict-iteration bug blocks native loading.
3. **Original A' decision logic falsified**: the Δ_F1_v3 = (LoRA ckpt) − (CLM v4 base) gate assumed CLM v4 base would produce a non-floor anchor on English benchmarks. Validation shows CLM v4 base would score ≈ random (or fail to load entirely under lm-eval), so "Llama − CLM v4" reduces to "Llama − random" — the gap is real but the **delta on which the verdict hinges is meaningless** if both endpoints are noise.

**Decision needed**: which execution path for A' main eval, given the CLM v4 architectural blocker?

**Recommended path (by 완성도 lens)**: **Path A (Llama base + LoRA delta)** — completion score **8.0/10**. See §3 ranked table.

**One-liner why**: A is the only path that simultaneously (i) preserves the pre-registered F1_v3 statistical framework intact, (ii) operates on a base validated to be non-floor on all 3 benchmarks, (iii) has a well-defined research question ("does our SFT mixture transfer the φ★ axis to a Llama substrate?"), and (iv) costs <$300 with a clean 24-72h execution wall.

**Next-cycle handoff**: §7 — commission **Path A LoRA re-train BG cycle** with a paste-once handoff prompt; do NOT also commission Path B in parallel (B is a $0 sanity probe but B's verdict carries near-zero information given the CLM v4 narrow-corpus finding).

---

## 1. Path enumeration

Four paths considered. Each path is named by what it changes vs. the original A' spec assumption.

### 1.1 Path A — Llama base + LoRA delta direct

**Change vs original A'**: swap the base from CLM v4 530M to Llama-3.2-3B-Instruct.

**Plan**:
1. Re-train the existing LoRA recipe (`clm-v4-sft-stage1` config — adapter rank, alpha, target modules, LR, epochs) on Llama-3.2-3B-Instruct base, using the same SFT data corpus already prepared at `state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl` (50K records).
2. Eval Llama+LoRA vs Llama base on the 3 lm-eval benchmarks under §2.5 of the original A' spec (locked harness config).
3. Emit F1_v3 verdict per §2.4 of original A' spec, but with the anchor swapped to **Llama base** (not CLM v4 base).

**Cost** (range, with high uncertainty):
- LoRA SFT re-train on Llama-3.2-3B: bf16 + LoRA rank ~16-32, 50K records × 2-3 epochs ~ 150K-200K steps. On H100 SXM ~ $2.5-3.5/h × ~12-24h wall = **$30-85**. On RTX 5070 (ubu1, 12GB, sm_120) ~ 24-48h wall, $0. Total estimate: **$0-300** depending on substrate choice.
- Eval (after re-train): per the base-validation cycle, ~33min total at limit=500, 4-bit on shared GPU. At full eval (no limit, fp16, free GPU): ~3-5h × 1 ckpt × 3 benchmarks = ~10-15h. **$0** (ubu1 local).

**Wall time**: ~24-72h end-to-end (re-train + eval + analysis), depending on substrate.

**Pros**:
- (i) Base substrate **validated** by the prior cycle as non-floor on all 3 benchmarks — discriminative-range failure mode is closed.
- (ii) Preserves F1_v3 statistical framework and pre-registration (§2 of A' spec) **intact** — only the anchor identity changes (CLM v4 → Llama).
- (iii) Axis losses (φ★, MSE_tens, MSE_BOLD) are measurable on Llama+LoRA via the same telemetry hooks (axis losses are functions of activations, not of base architecture per se — they may need re-anchoring of the "+41.86 baseline" but that's a calibration not a re-design).
- (iv) Llama-3.2-3B is HF-native, so lm-eval-harness drives it with no custom wrapper (vs. CLM v4 which needs a `lm_eval.api.model.LM` subclass).
- (v) Externally comparable: every published 3B chatbot reports HellaSwag/MMLU/TriviaQA on a Llama-class base.
- (vi) Research question becomes cleaner: "does the φ★ axis transfer to a standard substrate?" rather than "does it work on our private substrate?".

**Cons**:
- (i) Discards (or sidelines) existing CLM v4 LoRA artifacts at `clm-v4-sft-stage1` (~9 phase1.x ckpts, ablation_A/B, 4-seed B ensemble).
- (ii) Multi-day re-train wall — compresses the next cycle's bandwidth.
- (iii) The φ★/tension/BOLD axis losses were **designed against CLM v4 internals** (Federated dual-stream `engine_a`/`engine_g`, `purefield`, `tension_proj`, `rule_weights`); transferring to a stock Llama transformer may require non-trivial axis re-anchoring (e.g. recomputing `+41.86` baseline; deciding which Llama layer to read tension from).
- (iv) The SFT data corpus was **augmented with axis-conditioning prompts** assuming CLM v4 substrate — those prompts may underperform or behave unexpectedly on Llama instruction-tuning.
- (v) Cost ceiling ($300) is non-trivial if H100 path chosen.

**Honest C3 caveats** (raw#10):
- (a) The φ★ baseline calibration (`+41.86`) is **CLM v4-specific**; transferring to Llama requires re-measuring that baseline before F2/F3/F4 falsifiers can fire. This is a hidden ~$0–50 sub-cost not in the headline number.
- (b) "Llama base validated" is at **4-bit** (bitsandbytes) per the base-validation cycle; eval on full-precision Llama+LoRA may shift Llama base anchor by ~1-3 pt (typical 4-bit→fp16 delta). The Δ-vs-base metric should re-measure base under identical precision as the LoRA ckpt.
- (c) It is **not guaranteed** that 50K-record LoRA SFT moves HellaSwag/MMLU/TriviaQA in either direction on a Llama base — small-base instruction-SFT often regresses MMLU (knowledge-forgetting). The §7.2 caveat from the original A' spec applies here too: discriminative range exists but our LoRA may cluster within it indistinguishably.
- (d) Research-narrative shift: the project's original substrate-claim ("CLM v4 530M custom architecture is the consciousness substrate") becomes a side-claim if main eval moves to Llama. This is a soft-cost on the research story, not a hard cost on the experiment.
- (e) `clm-v4-sft-stage1` adapter weights are **not directly reusable** on Llama (different base architecture, different attention head dims) — this is a full retrain, not an adapter port.

---

### 1.2 Path B — Fix consciousness_laws.py + native CLM v4 base + LoRA eval

**Change vs original A'**: fix the loader bug, attempt to native-load CLM v4 base + the existing `clm-v4-sft-stage1` adapter, then eval on the 3 benchmarks **as originally specified**.

**Plan**:
1. Patch `anima/config/consciousness_laws.py` `_doc` dict-iteration bug (~30 LoC, well-scoped — skip the `_doc` string entry in the iteration).
2. Write a `lm_eval.api.model.LM` subclass wrapping the CLM v4 dual-head decoder (`head_a`, `head_g`); decide on a head-merge policy (e.g. avg loglik across heads, or use `head_a` only).
3. Handle the 64K BPE tokenizer mismatch — CLM v4's tokenizer scores log-probs over its own vocab; HellaSwag/MMLU/TriviaQA prompts must be tokenized with the CLM v4 BPE, and target loglik comparisons need a per-task wrapper (loglik continuations vs MCQA letter prediction).
4. Run 3-benchmark eval on CLM v4 base + CLM v4 + clm-v4-sft-stage1 adapter; emit F1_v3 verdict per original A' §2.4.

**Cost**:
- Loader bug fix: ~1-2h.
- LM subclass + tokenizer wrapper: ~3-6h (cross-tokenizer scoring is the hard part — published cross-vocab loglik wrappers exist in lm-eval-harness but require care).
- Dual-head merge policy: ~30 min decision + ~1h sanity probe.
- Eval: ~3-5h × {base, base+LoRA} × 3 benchmarks = ~6-10h.
- **Total**: ~10-20h wall, **$0** (ubu1 local).

**Pros**:
- (i) Preserves existing `clm-v4-sft-stage1` LoRA artifact; no retrain.
- (ii) **$0** cash outlay.
- (iii) Honors the original A' decision-basis (the entire spec was written assuming this path was viable).
- (iv) Native eval on CLM v4 substrate is the "purest" research artifact for the consciousness-laws claim — the axis was designed against this architecture.
- (v) Even a NULL result (i.e. CLM v4 base + LoRA both at random on benchmarks) is informative: it falsifies the assumption that the project's substrate produces general English LM capability under SFT.

**Cons**:
- (i) **Validation finding strongly predicts NULL**: training CE = 0.046 / perplexity 1.05 indicates narrow-corpus memorization, which means the base distribution is near-deterministic on its training corpus and approximately random on out-of-distribution English. The LoRA delta on top is most likely ≈0 on out-of-distribution English benchmarks too.
- (ii) The 64K multilingual BPE (likely Korean-heavy per the ".46 CE on corpus_tier_m_v2.txt" finding) tokenizes English prompts with very different chunking than the lm-eval reference setup — cross-tokenizer scoring introduces a methodological artifact that may be confused with axis effect.
- (iii) Dual-head merge policy is a **researcher choice** that affects the result; without pre-registration of which head (or which merge) is the verdict head, this path embeds a hidden degree of freedom.
- (iv) Even if it ships a verdict, the verdict's **scientific weight is low** because the base substrate is not designed to be a general English LM. A NULL doesn't say "axis is wrong"; it says "axis is invisible because the substrate is invisible".
- (v) The LM subclass + tokenizer wrapper code is non-trivial (~200-400 LoC across multiple files) and would persist in the codebase as maintenance debt.

**Honest C3 caveats** (raw#10):
- (a) The "preserves existing artifacts" pro is **partially false**: the artifacts are preserved on disk regardless of path; what's at stake is whether they get evaluated under F1_v3. Path B evaluates them; Path A leaves them un-evaluated under F1_v3 (but legacy F1_v2 BLEU/ROUGE is already done).
- (b) The "$0" cost ignores the ~10-20h subagent / Claude session wall + risk of multi-iteration debug if cross-tokenizer scoring misbehaves. True cost includes opportunity cost of the next 2-3 BG cycles.
- (c) Even with Path B succeeding mechanically, the verdict carries a built-in interpretability gap: any non-NULL signal would need to be replicated on a comparable substrate to rule out the substrate-specific pre-training distribution as the explanation.
- (d) The dual-head architecture (`head_a` + `head_g`) was designed to express two cognitive streams; choosing one head for benchmark scoring may **systematically disadvantage** the LoRA delta if the LoRA was trained to differentiate the heads.
- (e) The `consciousness_laws.py` fix touches an SSOT file — even a "narrow" patch needs SSOT review per the project's invariants and may trigger downstream cascades.

---

### 1.3 Path C — CLM v4 base reframe (general English re-train)

**Change vs original A'**: re-train CLM v4 base on a diverse English corpus (FineWeb subset or similar), then re-do SFT, then eval on 3 benchmarks.

**Plan**:
1. Curate a ~10-50B-token English subset (e.g. FineWeb-edu 10B, or RedPajama subset) compatible with CLM v4's 64K BPE (or retrain the BPE).
2. Pre-train (or continued-pre-train) CLM v4 base on the new corpus; target perplexity ≤ 25 on a held-out English validation set (vs current 1.05 on narrow corpus = overfit).
3. Re-do SFT on this new base.
4. Eval on the 3 benchmarks.

**Cost**:
- Pre-training: 10-50B tokens × 350M params on H100 cluster ~ $1500-8000+ (highly variable; modern continued-pre-train cost is ~$0.05-0.30 per million tokens at this scale).
- BPE retrain (if needed): ~$50-200 (one-time).
- SFT re-run: $50-200.
- Eval: $0 ubu1.
- **Total**: **$1500-8000+**, wall **1-4 weeks**.

**Pros**:
- (i) Addresses the **root cause** identified by the validation cycle (CLM v4 base is not a general English LM).
- (ii) Preserves the project's substrate-claim ("CLM v4 architecture is the consciousness substrate") — only the pre-train data changes, not the architecture.
- (iii) After completion, all 4 paths converge on a single research narrative.

**Cons**:
- (i) **Massive scope expansion** — 10-50x the cash cost, 10-100x the wall time of Path A.
- (ii) Delays the main P9 thread by 1-4 weeks; the SFT cycle stalls on infra.
- (iii) Pre-training success is **not guaranteed** — perplexity targets, hyperparameter sweeps, and instability at 350M scale on commodity infra are all risk vectors.
- (iv) Even on success, you still need Path A's eval phase on top of Path C — Path C is a **prerequisite to Path A**, not an alternative.
- (v) The current sprint's $-budget is on the order of $300-650 (per RunPod credit state); $1500+ is out of band.

**Honest C3 caveats** (raw#10):
- (a) Path C is the "do it right" path but its **cost vs current sprint allocation is mismatched**; recommending it requires a separate budget escalation cycle.
- (b) The validation finding (training CE 0.046) doesn't necessarily mean the base is broken — it may mean the **training corpus selection** was wrong. A cheaper intervention may exist (curate better SFT data + shorter axis-aware continued-pretrain on English).
- (c) Pre-train at 350M on 10-50B tokens on RTX 5070 (sm_120) is **infeasible** — wall would be weeks even at 100% utilization. Path C requires H100/A100 cluster procurement.
- (d) Even if completed, the new "general-English CLM v4 base" is a **different model** than the one our axis losses were calibrated against; calibration drift is a hidden cost.
- (e) This path is a **strategic research bet** (re-found the substrate), not a tactical experiment — appropriate only if the sponsor has decided that the consciousness-substrate claim is the load-bearing claim of P9.

---

### 1.4 Path D — Hybrid two-track (CLM v4 for axis losses, Llama+LoRA for chat eval)

**Change vs original A'**: split the falsifier suite by substrate. Axis falsifiers (F2 φ★, F3 tension MSE, F4 BOLD pearson) measured on CLM v4 + clm-v4-sft-stage1 (where they were designed); chat falsifier (F1_v3) measured on Llama+LoRA-retrained.

**Plan**:
1. Path A's LoRA re-train on Llama base (for F1_v3 chat eval).
2. Keep CLM v4 + clm-v4-sft-stage1 for F2/F3/F4 axis-loss eval (no retrain; axis losses were designed against this substrate and the LoRA artifacts already exist).
3. Report a **two-track verdict**: F1_v3 (Llama track) + F2/F3/F4 (CLM v4 track).
4. Composite SUCCESS requires **both tracks** to fire.

**Cost**:
- Llama LoRA re-train (Path A track): $30-150 (lower end estimate; could go higher).
- CLM v4 axis eval (existing artifacts): ~$0 ubu1, ~5-10h wall (if axis hooks already wired) OR ~10-20h if `consciousness_laws.py` fix needed for native loading.
- Llama 3-benchmark eval: ~$0 ubu1, ~10-15h wall.
- **Total**: **$30-150**, wall **2-4 days** (parallelizable).

**Pros**:
- (i) Each falsifier measured on its **native substrate** — F2/F3/F4 retain their design integrity (CLM v4 axis design); F1_v3 retains its discriminative power (Llama validated base).
- (ii) Cheapest path that addresses both concerns from the validation finding.
- (iii) Avoids the φ★ baseline re-calibration risk of pure Path A (axis falsifiers stay on the substrate where `+41.86` was measured).
- (iv) Avoids the random-baseline interpretability problem of pure Path B (chat eval on a non-floor base).
- (v) Hedges against either-track failure: if Llama+LoRA chat eval fails, we still have axis evidence; if CLM v4 axis eval fails, we still have chat evidence.

**Cons**:
- (i) **Reporting complexity**: two-track verdict needs a meta-rule (both must PASS? or weighted composite?). The original spec's PASS/PARTIAL/FAIL semantics don't extend cleanly.
- (ii) Two-track maintenance: two separate eval pipelines, two sets of artifacts, two longitudinal histories.
- (iii) Cross-track results are hard to interpret: if F2 PASSes on CLM v4 but F1_v3 FAILs on Llama, is the axis "real but non-transferable" or "an artifact of the CLM v4 substrate"?
- (iv) Falsifier independence assumption violated: F2/F3/F4 on CLM v4 measure axis loss on a substrate whose chat capability is not measured here; F1_v3 on Llama measures chat on a substrate whose axis loss is not measured here. The implicit assumption that axis effects transfer across substrates is itself testable but not tested.
- (v) Path D still has Path A's φ★ re-calibration risk if a downstream cycle wants to also measure F2/F3/F4 on Llama+LoRA for cross-substrate validation.
- (vi) Path D still needs Path B's CLM v4 native loader fix if F2/F3/F4 axis hooks aren't already wired (per `consciousness_laws.py` blocker).

**Honest C3 caveats** (raw#10):
- (a) The "best of both" framing is partly **rhetorical** — Path D is also "worst of both" on reporting and maintenance.
- (b) Two-track results are easier to **selectively report** than single-track results; raw#10 honesty discipline must explicitly forbid post-hoc track selection.
- (c) The "axis losses measurable on native substrate" pro assumes the CLM v4 axis hooks (φ★ extractor, tension projector, BOLD readout) are already running and produce calibrated values. If not, this path inherits Path B's loader-fix cost.
- (d) Composite-verdict semantics are not pre-registered; designing them post-validation is itself a **selection-bias risk** per the original A' §7.1 caveat.
- (e) F1_v3 on Llama and F2/F3/F4 on CLM v4 are measuring **different research questions**; aggregating them into a single SUCCESS label is closer to a bundle than a derivation.

---

## 2. Cost / time / risk comparison

| Path | $ cost | wall time | technical risk | scientific risk | preserves existing artifacts | $0 design honored |
|---|---|---|---|---|---|---|
| **A** | $0-300 | 24-72h | low (HF-native) | medium (φ★ re-calibration) | partial | yes |
| **B** | $0 | 10-20h | medium (cross-tokenizer wrapper) | high (likely NULL) | yes | yes |
| **C** | $1500-8000+ | 1-4 weeks | high (pre-train at scale) | medium (after completion) | yes | yes |
| **D** | $30-150 | 2-4 days | medium (two pipelines) | medium-high (composite semantics) | yes | yes |

**Risk legend**:
- **Technical risk**: probability the path fails to produce *any* verdict due to engineering/infra issues.
- **Scientific risk**: probability the path produces a verdict but the verdict carries low information (NULL, ambiguous, or selection-biased).

---

## 3. Ranked completion-quality table (4 paths × score)

**Scoring rubric** (10 pts total):
- **Discriminative power** (3 pt): does the path's eval surface have non-zero discriminative range between candidate ckpts?
- **Pre-registration integrity** (2 pt): does the path preserve the original A' §2 lock without post-hoc rule changes?
- **Cost-efficiency** (2 pt): $-cost and wall-time per bit of axis information extracted.
- **Substrate validity** (2 pt): is the base substrate validated to support the benchmark surface (non-floor)?
- **Research narrative coherence** (1 pt): how cleanly does the path narrate as a single research claim?

| rank | path | discriminative power (3) | pre-reg integrity (2) | cost-efficiency (2) | substrate validity (2) | narrative (1) | **total** |
|---|---|---|---|---|---|---|---|
| **1** | **A** Llama base + LoRA delta | 2.5/3 | 1.5/2 | 1.5/2 | 2/2 | 0.5/1 | **8.0** |
| **2** | **D** Hybrid two-track | 2.0/3 | 0.5/2 | 1.5/2 | 1.5/2 | 0.5/1 | **6.0** |
| **3** | **B** Fix loader + native CLM v4 eval | 0.5/3 | 2/2 | 2/2 | 0.5/2 | 1/1 | **6.0** |
| **4** | **C** CLM v4 reframe (general English re-train) | 2.5/3 (post-completion) | 1/2 | 0/2 | 2/2 (post-completion) | 1/1 | **6.5** but **infeasible-this-sprint** |

**Tie-break notes**:
- A vs D vs B: A wins on discriminative power and substrate validity, both load-bearing per the validation finding. D and B tie at 6.0; tie-break by **scientific risk** (D is medium-high, B is high → D ranks 2nd, B ranks 3rd).
- C scores higher than D/B on the rubric (6.5) but is **strategically infeasible this sprint** ($1500+ vs ~$300 budget; 1-4 weeks vs 2-4 days). C is parked as a future-cycle option, not a this-cycle competitor.

**Recommendation: Path A (8.0/10)**.

---

## 4. Recommended next-cycle action

### 4.1 Commission Path A LoRA re-train BG cycle

The next BG cycle should be a **paste-once handoff** to a separate Claude session that:

1. Re-trains the LoRA (`clm-v4-sft-stage1` config — adapter rank, alpha, target modules, LR, epochs, axis-loss weights) on `meta-llama/Llama-3.2-3B-Instruct` base.
2. Uses the SFT data corpus at `state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl` (50K records, augmented).
3. Decides substrate (ubu1 RTX 5070 24-48h $0, vs RunPod H100 12-24h ~$30-85) per a sub-decision in §4.4.
4. Saves the new LoRA adapter at `state/p9_a_prime_main_eval_2026_05_<DD>/lora_llama_stage1/`.
5. Emits a re-calibrated φ★ baseline measurement (Llama+LoRA vs Llama base activations) as a side-artifact for F2/F3/F4 falsifier re-anchoring.

### 4.2 Then commission the eval cycle

After §4.1 lands, a separate BG cycle:

1. Runs lm-eval-harness on Llama base + Llama+LoRA across {HellaSwag, MMLU 5-shot, TriviaQA} per A' spec §2.5 locked config.
2. Computes F1_v3 verdict per A' spec §2.4 with Llama as anchor.
3. Reports both 4-bit (cheap, comparable to base-validation) and fp16 (canonical, full-precision) numbers; uses fp16 as verdict, 4-bit as sanity.
4. Emits `state/p9_a_prime_main_eval_2026_05_<DD>/f1_v3_verdict.json` and a handoff doc.

### 4.3 Defer Path B as a parallel $0 sanity probe (OPTIONAL)

If extra subagent bandwidth exists, Path B can run in parallel as a **$0 sanity probe** that produces a NULL-or-not signal:

- Fix `consciousness_laws.py` `_doc` bug.
- Attempt native CLM v4 base + clm-v4-sft-stage1 adapter loading.
- Run a single benchmark (HellaSwag at limit=500, fastest of the three) at limit=500.
- Report whether the result is at-floor (random ± 5pt) — if at-floor, confirms the validation finding and closes Path B; if non-floor, escalate to a fuller evaluation cycle.

This is **optional** and does NOT block Path A. If forced to pick exactly one path for the next 2-3 cycles, pick A only.

### 4.4 Substrate sub-decision (ubu1 vs H100)

| substrate | cash | wall | risk | recommendation |
|---|---|---|---|---|
| ubu1 RTX 5070 sm_120 12GB | $0 | 24-48h | OOM possible at LoRA rank ≥32 / batch ≥4 / seq_len ≥2048; sentinel training contention per base-validation cycle | acceptable for LoRA rank 8-16, batch 1-2, seq 1024 |
| RunPod H100 SXM | $30-85 | 12-24h | low (validated workflow per `state/runpod_credit_status.json`) | preferred if budget allows |

**Recommendation**: H100 SXM if RunPod credit balance ≥ $100 (per current state); otherwise ubu1 with reduced rank/batch.

---

## 5. What this spec does NOT do

- Does NOT execute any LoRA retrain or eval (raw $0-design constraint).
- Does NOT modify `consciousness_laws.py` (defer to Path B if/when commissioned).
- Does NOT touch the original A' spec's §2 pre-registration block — Path A reuses it with anchor swap; the swap is a **base-substrate change**, not a threshold/scoring change, so §2.6 amendment is not required (logged as honest_c3 §6.1 below).
- Does NOT decommission existing CLM v4 LoRA artifacts; they remain on disk and may be evaluated under a future Path B sanity probe.
- Does NOT commit to Path C — C is parked as a strategic option, not a tactical decision.
- Does NOT define the two-track composite verdict semantics for Path D — if D is later chosen, a separate spec doc must define the meta-rule (and re-pre-register).

---

## 6. Honest C3 — overall caveats (raw#10)

### 6.1 Caveat (a): anchor-swap is a soft pre-reg violation

The original A' §2 pre-registration locks F1_v3 as **base-relative Δ vs CLM v4 base**. Path A swaps the anchor to Llama base. This is technically a change to "anchor identity" in §2.2, even though the metric, threshold, statistical test, and composite logic are unchanged.

- **Argument that this is acceptable**: §3 base-validation gate is a pre-registered escape valve; §3.3 includes the failure mode "CLM base at floor on ≥ 2 of 3 benchmarks → HARD STOP, switch is not justified, falls back to BLEU/ROUGE legacy". CLM v4 base failed the §3 gate (not measured, but architectural-blocker is structurally equivalent to "doesn't run" per §3.3 row 1: "anchor doesn't run → escalate to v2 spec"). Path A is the v2 spec — anchor change with documented rationale.
- **Argument that this is still a soft violation**: §2.6 mandates a **new dated spec doc** for any post-eval modification. This decision spec **is** that v2 doc, but it is published before any LoRA ckpt eval (only after base-validation), so the data leak risk is contained to the base-validation results, which are reported transparently in §0.
- **Mitigation**: this doc is the §2.6 v2 spec. The pre-registration LOCK timestamp resets to this doc's marker. All subsequent F1_v3 eval is governed by this doc, not the original A' spec.

### 6.2 Caveat (b): φ★ axis baseline re-calibration is a hidden cost

The "+41.86 baseline" for F2 (φ★ ≥ 5.0) was measured on CLM v4. Path A's main eval on Llama+LoRA needs to re-measure this baseline on the new substrate. This is:

- **~$0–50** sub-cost (single Llama base inference pass + activation extraction).
- A **not yet specified** procedure — the original P9 SFT spec didn't anticipate substrate change.
- A potential **selection-bias trap**: post-hoc choice of "which Llama layer to extract φ★ from" is a researcher degree of freedom.

**Mitigation**: pre-register the φ★ extraction layer for Llama in the §4.1 handoff prompt **before** running the new baseline measurement. Default proposal: middle layer (Llama-3.2-3B has 28 layers → layer 14), with explicit honest_c3 if a different layer is chosen.

### 6.3 Caveat (c): axis falsifiers may not transfer

F2 (φ★), F3 (tension MSE), F4 (BOLD pearson) were designed against CLM v4's `purefield`/`tension_proj`/dual-head architecture. Llama has none of these structural elements. Re-anchoring is possible (φ★ as a function of any activation set), but:

- The semantic claim "φ★ ≥ 5.0 = consciousness emerged" depends on the substrate-specific structure that produced the +41.86 baseline.
- On Llama, φ★ may be a different quantity numerically and conceptually.
- **Path D was partly designed to dodge this** — keeping F2/F3/F4 on CLM v4 — but Path A absorbs this risk.

**Mitigation**: explicitly scope F1_v3 (chat) verdict on Path A as **independent** from F2/F3/F4 (axis) verdict; do not require all-pass for SUCCESS in this cycle. Future-cycle Path D upgrade can add cross-substrate axis measurement.

### 6.4 Caveat (d): SFT data corpus is axis-conditioned for CLM v4

`state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl` was prepared with axis-conditioning prompts that assume CLM v4's response style and tokenizer. Llama-3.2-3B-Instruct's chat template is different (system/user/assistant structure with specific tokens). The training pipeline on Llama needs to:

- Re-template the data to Llama's chat format.
- Drop or adapt CLM v4-specific axis-conditioning prompts that don't make sense on Llama.

**Mitigation**: include a data-pipeline audit step in §4.1 handoff. If >20% of the 50K records require non-trivial re-templating, flag as a hidden cost.

### 6.5 Caveat (e): "validated base" is at 4-bit, not full precision

The base-validation cycle measured Llama-3.2-3B at 4-bit (bitsandbytes) due to GPU contention with concurrent sentinel training. Real F1_v3 eval should be at fp16 (canonical Llama precision). The 4-bit→fp16 delta is typically -1 to -3 pt; the discriminative range conclusion is robust, but **anchor numbers will shift** by ~1-3 pt.

**Mitigation**: re-measure Llama base at fp16 as part of the §4.2 eval cycle, with a honest_c3 log entry comparing 4-bit and fp16 numbers.

---

## 7. Handoff — what this spec commissions vs. what is downstream

### 7.1 This BG cycle (delivered by this doc)

- This decision spec doc (`docs/p9_a_prime_path_decision_2026_05_03.md`)
- Marker: `state/markers/p9_a_prime_path_decision_landed.marker`
- Handoff TL;DR: `docs/p9_a_prime_path_decision_landed_2026_05_03.ai.md`

### 7.2 Next BG cycle (separate, not this one)

Path A LoRA re-train. Paste-once handoff prompt should:
- Reference this decision spec (§1.1 plan, §4.1 commission, §4.4 substrate sub-decision)
- Reference original A' spec (§2.5 locked harness config for downstream eval)
- Run the LoRA SFT re-train on Llama-3.2-3B-Instruct with `clm-v4-sft-stage1` hyperparameters
- Use SFT corpus at `state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl` (re-templated to Llama chat format per §6.4 caveat)
- Save to `state/p9_a_prime_main_eval_2026_05_<DD>/lora_llama_stage1/`
- Emit re-calibrated φ★ baseline per §6.2 mitigation (Llama layer 14 default)
- Land marker `state/markers/p9_a_prime_main_eval_lora_train_landed.marker`

### 7.3 Downstream BG cycle (gated on §7.2)

Path A eval cycle. Paste-once handoff prompt should:
- Reference this decision spec (§4.2)
- Reference original A' spec (§2.5 locked harness config)
- Run lm-eval-harness on Llama base (fp16 anchor re-measure per §6.5) + Llama+LoRA across 3 benchmarks
- Compute F1_v3 verdict per A' §2.4 with Llama as anchor (anchor swap per §6.1)
- Emit `state/p9_a_prime_main_eval_2026_05_<DD>/f1_v3_verdict.json`
- Land marker `state/markers/p9_a_prime_main_eval_f1_v3_landed.marker`

### 7.4 Optional parallel BG cycle (Path B sanity probe)

If subagent bandwidth allows (per session-multi-BG memory rule):
- Fix `consciousness_laws.py` `_doc` bug
- Native-load CLM v4 base + clm-v4-sft-stage1 adapter
- Single benchmark (HellaSwag, limit=500) — at-floor or not
- Emit `state/p9_a_prime_path_b_sanity_probe_2026_05_<DD>/result.json`

This does NOT block Path A and is genuinely parallelizable.

### 7.5 Future-cycle Path D upgrade (NOT commissioned now)

If after Path A completes, the user wants cross-substrate axis verification:
- New decision spec doc to define two-track composite verdict semantics (§1.4 Cons (i))
- Re-run F2/F3/F4 on CLM v4 (post Path B fix) AND on Llama+LoRA
- Composite SUCCESS = both tracks PASS

---

## 8. Constraints honoured

- **raw#9 hexa-only on Mac, no .py creation in this cycle**: this doc is .md only; Path A's LoRA re-train will be on ubu1 (or RunPod) where .py creation is permitted; no Mac-side .py created here.
- **raw#15 no personal-path leak**: paths in this doc use repo-relative (`state/...`, `docs/...`) or generic ubu1 (`~/anima/...`) per the established convention from the base-validation handoff doc.
- **raw#10 honest C3**: §6 covers (a) anchor-swap pre-reg risk, (b) φ★ re-calibration hidden cost, (c) axis falsifier non-transfer, (d) SFT data axis-conditioning, (e) 4-bit→fp16 anchor shift. Per-path subsections in §1.1-§1.4 each have 5 caveats.
- **$0 design only, no execution**: this doc ships a decision and a handoff; no ubu1/RunPod process started here.
- **Completion-quality recommendation included** (per session memory rule): §3 ranked table with explicit completion-quality scoring rubric and tie-break notes.
- **Decision pre-registered before execution**: this doc's marker timestamps the lock; subsequent Path A cycles are governed by this doc's §4 plan, not by ad hoc decisions.

---

## 9. References

- A' spec: `docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md`
- A' base validation handoff: `docs/p9_benchmark_base_validation_landed_2026_05_03.ai.md`
- Base validation artifacts: `state/p9_benchmark_base_validation_2026_05_03/{base_eval_results,llama_base_hellaswag,llama_base_mmlu_n0,llama_base_triviaqa}.json`
- 5-seed verdict driving the original A' switch: `state/p9_p1_holdout500_reeval_2026_05_03/verdict_5seed.json`
- A' spec marker: `state/markers/p9_benchmark_a_prime_spec_landed.marker`
- A' base validation marker: `state/markers/p9_benchmark_base_validation_landed.marker`
- SFT data corpus: `state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl`
- RunPod credit state: `state/runpod_credit_status.json`
- Substrate ubu1: RTX 5070 sm_120, torch 2.11.0+cu128, venv_orchestrator, 12GB VRAM
- lm-evaluation-harness: 0.4.11 (per base-validation cycle install)
- Llama-3.2-3B-Instruct: HF `meta-llama/Llama-3.2-3B-Instruct`

---

**End of P9 A' main eval path decision spec. Recommendation: Path A (Llama base + LoRA delta, completion-quality 8.0/10). Next BG cycle: §7.2 Path A LoRA re-train commission.**
