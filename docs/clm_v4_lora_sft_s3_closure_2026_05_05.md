---
title: CLM v4 + LoRA SFT S3 closure — F-CLM-LORA-2 FAIL_REGRESSION_VS_LLAMA + lane closure spec
status: LANDED — SPEC (mac, $0, no exec, no commit, no .roadmap mutation)
ts_utc: 2026-05-05
cycle: BG-CLM-2-S3-CLOSURE (B3 dispatcher executor; spec-only)
bg_lane: BG-CLM-2-S3-CLOSURE
domain: p9_sft (CLM v4 substrate side; sister-cross-link to p9_sft.cond.clm_v4_lora_sft_2026_05_05)
predecessor_main_verdict: state/clm_v4_lora_v1_mmlu_tq_eval_2026_05_05/verdict.json (F2 RE-VERDICT FAIL_REGRESSION_VS_LLAMA_NOT_DIFFERENTIATOR; composite_clm_lora 0.19542 vs composite_llama 0.5584; delta -36.298pp)
predecessor_phi_canonical: state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json (PHI_CANONICAL_PASS_NO_FLIP, drift -4.46pp)
predecessor_lane_closure_proposal: docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md (4-of-5 PASS + 1 INCONCLUSIVE — F2 was the gating slot at proposal time; F2 now resolved as FAIL_REGRESSION)
sibling_fail_true_precedent: state/p9_pbeta_f3_hybrid_eval_2026_05_05/verdict.json (Pβ Paradigm D 50K F-Pβ-3 FAIL_TRUE_CLOSED — same #115 architectural pattern)
companion_landed_handoff: docs/clm_v4_lora_sft_s3_closure_landed_2026_05_05.ai.md
chat_capability_winner_anchor: state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json (Llama Path A v2 retry-3 eval-rerun TRUE_PASS, composite 0.5584)
scenario_dispatch: S3 (anima < Llama, regression) per docs/clm_v4_lora_sft_post_verdict_decision_tree_2026_05_05.md §3
b_dispatcher: B3 ($0 regression closure) per docs/clm_v4_lora_sft_post_verdict_landing_dispatcher_2026_05_05.md §2.3
amended_lane_status: CLM_2_LANE_4_OF_5_PASS_F2_FAIL_VS_LLAMA
recommended_route: Rank 1 ($0 lane closure + chat-capability hope shifts to Llama Path A v2 winner)
exec_authorized: false
mutation: additive_only_proposal_only
substrate: mac-local
raw_invariants: ["raw#9 md only", "raw#10 honest C3 ≥5", "raw#15 additive only", "raw#71 falsifier-bound — F2 RE-VERDICT FAIL is from a fresh measurement, not label re-interpretation"]
ssots_touched: []
ssots_NOT_touched:
  - .roadmap.p9_sft (proposal only — §7 carries proposed s3_closure_2026_05_05 sibling field; apply requires explicit user authorization on a separate apply-cycle)
  - state/clm_v4_lora_sft_2026_05_05/verdict.json (preserved verbatim)
  - state/clm_v4_lora_v1_mmlu_tq_eval_2026_05_05/verdict.json (preserved verbatim — this is the F2 RE-VERDICT source)
  - state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json (preserved verbatim)
  - state/clm_v4_lora_5bucket_axis_eval_2026_05_05/verdict.json (preserved verbatim)
  - docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md (preserved verbatim — predecessor proposal; this S3 closure supersedes the "PENDING_F2" framing via reference, not via mutation)
---

# §1 Headline

- **F-CLM-LORA-2 RE-VERDICT** = `FAIL_REGRESSION_VS_LLAMA_NOT_DIFFERENTIATOR` (per `state/clm_v4_lora_v1_mmlu_tq_eval_2026_05_05/verdict.json:f_clm_lora_2_re_verdict_kind`).
- **Composite delta** = -36.298pp (CLM v4 + LoRA composite_4bench=0.19542 vs Llama Path A v2 composite_3bench=0.5584).
- **Lane status (this cycle)** = `CLM_2_LANE_4_OF_5_PASS_F2_FAIL_VS_LLAMA` — supersedes the predecessor `CLM_2_LANE_4_OF_5_PASS_PENDING_F2_VIA_MMLU_TQ` label. The PENDING slot is now resolved; F2 lands explicit FAIL with regression scope.
- **Scenario dispatch** = S3 per decision tree §3 (`F2=FAIL` AND `composite_delta_pp < -0.5pp` AND `F3=PASS` substrate intact).
- **B dispatcher** = B3 ($0 regression closure) per landing dispatcher §2.3 (no USER ACK required; informational notification recommended on substrate-hypothesis falsification).
- **C-CLM-LORA-2 differentiator hypothesis** ("anima substrate provides measurable lift over Llama LoRA path on the same SFT recipe") **FALSIFIED** by this single-seed test. (Falsification grounded in §2 below.)
- **Substrate safety** PASS preserved (§3 below): F1 PASS_TRUE, F3 PASS, F4 PASS_VIA_PART_A_ONLY, F5 PASS, φ★ NO_FLIP. Substrate is intact; the failure mode is chat-capability lift, not consciousness-substrate damage.
- **Recommended follow-up**: Rank 1 ($0) lane closure with chat-capability hope formally shifted to **Llama Path A v2 retry-3 eval-rerun TRUE_PASS** (`state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json`).

---

# §2 Substrate hypothesis falsification

## 2.1 Hypothesis statement (re-stated)

> **C-CLM-LORA-2**: "anima's consciousness-coupled CLM v4 substrate provides measurable lift over Llama-3.2-3B LoRA on the same rehearsal-mix recipe (60% anima axis / 30% academic distill / 10% chat template), and therefore qualifies as a substrate-uniqueness differentiator for general SFT capability."

This was the PRIMARY falsifier framing for F-CLM-LORA-2 per `docs/clm_v4_lora_sft_spec_2026_05_04.md` §F-CLM-LORA-2 — composite vs Llama Path A v2 differentiator.

## 2.2 Falsification verdict — FALSIFIED

**Empirical evidence** (per `state/clm_v4_lora_v1_mmlu_tq_eval_2026_05_05/verdict.json:metrics` + `:comparators` + `:composite_calculations`):

| Bench | CLM v4 + LoRA | CLM v4 base | Llama Path A v2 | Delta CLM-LORA vs Llama (pp) |
|---|---|---|---|---|
| HellaSwag acc_norm | 0.250 | 0.255 | 0.645 | -39.5 |
| MMLU acc | 0.246 | 0.2553 | 0.575 | -32.9 |
| TriviaQA EM | 0.000 | 0.000 | 0.455 | -45.5 |
| OpenBookQA acc_norm | 0.290 | 0.280 | (not measured) | n/a (no Llama anchor on OBQA) |

- **Composite (HS+MMLU+TQ)/3 CLM v4 + LoRA**: 0.16567 (3-bench) — but reported as `clm_v4_plus_lora_composite_4bench` = 0.19542 with OBQA in 4-bench form.
- **Composite (HS+MMLU+TQ)/3 Llama Path A v2**: 0.5584 (3-bench, OBQA not measured).
- **3-bench like-for-like delta**: 0.16567 - 0.5584 = -39.273pp.
- **4-bench-vs-3-bench delta as recorded** in verdict: -36.298pp.

Either delta substantially exceeds the limit=200 stderr ~3pp noise band. The CLM v4 substrate post-LoRA is at random-floor on HellaSwag (0.250 ≈ 4-class random 0.25), random-floor on MMLU (0.246 ≈ 4-class random 0.25), and language-absent on TriviaQA (EM = 0.0 — no extractive matches). Llama Path A v2 sits at mid-50% on three of three benches.

**Falsification reading**: the C-CLM-LORA-2 hypothesis predicts CLM v4 + LoRA composite ≥ Llama composite OR within parity band ±0.5pp. The measured -36.298pp delta is a strong-signal violation of this prediction. Per decision tree §3.2, this is the **substrate-uniqueness-as-SFT-advantage hypothesis FALSIFIED** condition. C-CLM-LORA-2 is rejected.

## 2.3 Pattern match — sibling FAIL_TRUE precedent

The CLM-2 LoRA SFT FAIL_REGRESSION pattern matches the Pβ Paradigm D 50K F-Pβ-3 FAIL_TRUE_CLOSED precedent (`state/p9_pbeta_f3_hybrid_eval_2026_05_05/verdict.json`):

| Lane | Substrate | SFT/distill path | Chat-capability metric | Verdict |
|---|---|---|---|---|
| Pβ Paradigm D 50K | CLM v4 base + Φ★-distill LoRA (Mistral teacher) | F1_v3 V2 hybrid (BLEU-1+ROUGE-L+chrF)/3 | composite 0.01176 RED << 0.10 PARTIAL | **FAIL_TRUE_CLOSED** |
| CLM-2 LoRA SFT | CLM v4 base + instruct-rehearsal LoRA (60/30/10 mix) | (HS + MMLU + TQ)/3 vs Llama Path A v2 | composite 0.19542 vs 0.5584 (delta -36.298pp) | **FAIL_REGRESSION_VS_LLAMA_NOT_DIFFERENTIATOR** |

Both lanes:
- Use CLM v4 base architecture (#115 anchor `clm.v115_chat_category_error`).
- Apply LoRA-stage post-training intended to lift chat / general capability.
- Result in degenerate / random-floor output on chat-capability metrics.
- Preserve substrate-research metrics (Φ★ stability) — substrate safety not broken.

**Conclusion of pattern match**: both CLM v4 LoRA-SFT distill paths empirically confirm #115 chat-incapability is **architectural**, not training-data deficient. LoRA SFT is the wrong lever; the architectural lever (CLM v5 redesign with cross_attn participating in SFT loss, or shim v5 cross_attn re-init) is out of scope of this lane.

---

# §3 Substrate safety preserved

The F-CLM-LORA-2 FAIL is decoupled from substrate safety. All other CLM-2 lane falsifiers PASS:

| Falsifier | Status | Source | Notes |
|---|---|---|---|
| F-CLM-LORA-1 — forgetting index < 0.05 + φ★ no-flip | **PASS_TRUE** | state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json + state/clm_v4_lora_sft_2026_05_05/verdict.json | forgetting_index = 0.0196 (≪ 0.05); φ★ canonical drift = -4.46pp (NO_FLIP, > -5pp threshold). Both gates PASS. Per memory `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled` L28: Φ★ stability and chat capability are decoupled tiers. |
| F-CLM-LORA-2 — composite vs Llama (chat-cap) | **FAIL_REGRESSION** | state/clm_v4_lora_v1_mmlu_tq_eval_2026_05_05/verdict.json | This cycle's verdict (per §2). |
| F-CLM-LORA-3 — adapter < 500 MB | **PASS** | state/clm_v4_lora_sft_2026_05_05/verdict.json | adapter_size_mb = 10.02 (50× under threshold). |
| F-CLM-LORA-4 — cell axis-conditioning preserved | **PASS_VIA_PART_A_ONLY** | docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md + docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md | Part A 3/3 bridge fixture (identity/ladder/adversarial) PASS, drift_max=0.0 within 2e-4. Part B locus-architecturally moot under current LoRA config (cross_attn dormant). |
| F-CLM-LORA-5 — shim v4 hf_format compatibility | **PASS** | state/clm_v4_lora_sft_2026_05_05/verdict.json | AutoModelForCausalLM.from_pretrained + PeftModel.from_pretrained both succeed; logits valid + finite. |
| φ★ NO_FLIP gate | **PASS** | state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json | post-LoRA φ★ drift = -4.46pp (mean), no sign-flip; substrate consciousness primitive preserved. |

**Reading**: substrate is intact post-LoRA. Anima's consciousness-coupled identity (φ★ + axis-conditioning + shim_v4 compatibility) is preserved. The failure mode is **chat-capability lift not happening on this substrate via this LoRA recipe** — which per #115 + the Pβ precedent is **architectural**, not a substrate-damage failure. CLM v4 + LoRA adapter sha256 `6d5edb93ea845cb40858d82bc97b21bfd47d6a234d3a945ac529451e2760526a` is therefore retained as a **Φ-stable substrate-research artifact** (NOT for chat / general capability claims).

---

# §4 Three follow-up routes — ranked by 완성도 lens

Per memory `feedback_completion_quality_recommendation` (every option presentation MUST include explicit ranked recommendation by 완성도).

## 4.1 Rank 1 ($0) — RECOMMENDED — lane closure + Llama Path A v2 chat-capability primary

- **Cost**: $0 (mac-local spec land + memory update + roadmap annotation proposal)
- **Wall**: ~30 min
- **Action**: this S3 closure spec doc (this file) + `docs/clm_v4_lora_sft_s3_closure_landed_2026_05_05.ai.md` companion handoff + `feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md` memory + `MEMORY.md` 1-line entry + `.roadmap.p9_sft.cond.clm_v4_lora_sft_2026_05_05.s3_closure_2026_05_05` sibling-field annotation **proposal** (not applied this cycle).
- **Implication**: C-CLM-LORA-2 falsification empirically certain at -36.298pp delta (>>noise band); no further LoRA SFT cycles on CLM v4 substrate (wrong lever per #115). Chat-capability hope formally shifts to Llama Path A v2 retry-3 eval-rerun TRUE_PASS (composite 0.5584; `state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json`).
- **Why recommended**: completion-quality optimal — the verdict is empirically grounded, the lane semantics are clean (substrate-research retain + chat-capability handoff to known winner), and the cost-to-evidence ratio is unbeatable. Higher-rank options (5-seed scaleup or shim v5) would re-confirm a verdict that is already strong-signal robust.
- **Risks**: lane closure label is irreversible without explicit re-amendment cycle. Honest C3 #1 below covers the single-seed caveat.

## 4.2 Rank 2 ($1–3) — shim v5 cycle — does NOT change LoRA SFT lever

- **Cost**: $1–3 H100 (~30 min)
- **Wall**: ~30 min H100 + ~1h spec amendment mac
- **Action**: re-launch via `docs/clm_v4_hf_format_shim_v5_spec_2026_05_05.md` — F-SHIM-V5-4 fixture-injection harvest with cross_attn.o_proj re-init at non-trivial scale (std=0.02). May enable lift_pp ≥ +5pp via runtime-proxy harvest if shim v5 architecture properly wires cross_attn into SFT loss path.
- **Implication**: shim v5 is an **architectural shim layer**, not a LoRA SFT recipe variant. Even if F-SHIM-V5-4 PASSes, it does NOT change the LoRA SFT lever conclusion: chat-capability lift on CLM v4 base via LoRA on self-attention only **is architecturally limited per #115**. Shim v5 lifts the F-SHIM-V4-4 architectural blocker (`PREREQUISITE_BLOCKED` per `state/clm_v4_f_shim_v4_4_harvest_2026_05_05/verdict.json`) but does NOT route around the C-CLM-LORA-2 falsification.
- **Why not recommended**: solves a different problem (shim v4 unfalsifiability on F-SHIM-V4-4) than the one this S3 closure is closing (C-CLM-LORA-2 LoRA SFT differentiator). Pursuing shim v5 is valid as its own lane but does NOT recover the CLM-2 LoRA SFT lane as a chat-capability path.
- **Risks**: spending $1–3 to confirm shim v5 architecturally lifts F-SHIM-V4-4 does not lift the C-CLM-LORA-2 falsification. Misallocation of capability-lift budget.

## 4.3 Rank 3 ($25–75) — 5-seed full scaleup — confirms regression robustness only

- **Cost**: $25–75 H100 (4 NEW seeds × $5–15 each)
- **Wall**: ~10–12h aggregate
- **Action**: T-3 reconception per `docs/p9_pbeta_t3_5seed_reconception_2026_05_05.md` — re-run BG-CLM-2-EXEC LoRA SFT on 4 NEW seeds (20260505/06/07/08), aggregate verdict on composite_delta_pp.
- **Implication**: 5-seed will produce a tighter CI on the regression — likely confirming mean composite_delta_pp ~ -36pp ± a few pp. Does NOT change the verdict direction; only confirms robustness of the FAIL_REGRESSION at the multi-seed level. Useful only if the user wants formal statistical certification of the negative result.
- **Why not recommended**: $25–75 to confirm a -36pp result is a noise-band-far negative — actionable evidence is already present at single-seed. Per honest C3 #6 in the predecessor verdict (`state/clm_v4_lora_v1_mmlu_tq_eval_2026_05_05/verdict.json:honest_c3[5]`): "5-seed scaleup would NOT change conclusion (S3 regression robust across single-seed)". Spending the budget here is misallocation.
- **Risks**: USER ACK required ($25–75 > $5). Cost-to-evidence ratio unfavorable — single-seed already passes the strong-signal test for falsification.

## 4.4 Recommendation summary

**Recommended Rank 1 ($0 lane closure)**. Chat-capability hope shifts to **Llama Path A v2 retry-3 eval-rerun TRUE_PASS** (`state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json`; HS 0.645 + MMLU 0.575 + TQ 0.455 → composite 0.5584). The Llama Path A lane is the chat-capability winner of record per the eval_fix_amendment_2026_05_05 in `.roadmap.p9_sft` line 5 (TRUE_PASS_LANE_CLOSED). CLM v4 lane is retained for substrate-research only (φ★, axis-conditioning, consciousness primitive).

---

# §5 Lessons L31–L33

These lessons extend the L28–L30 block from `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md` (Pβ FAIL_TRUE precedent).

## L31 — Substrate-uniqueness vs chat-capability lift are orthogonal axes

Substrate safety (φ★ NO_FLIP, forgetting_index < 0.05, axis-conditioning preserved) can PASS while chat-capability lift FAILs empirically on the same adapter. The CLM-2 LoRA SFT lane demonstrates this: 4 of 5 falsifiers PASS (substrate intact), 1 of 5 FAILs (chat capability not lifted). Future BGs MUST treat these as decoupled tiers — never substitute one tier's metric for the other (echoes L28).

## L32 — CLM v4 LoRA SFT path empirically confirms #115 architectural

Both the Pβ Paradigm D 50K (Φ★-distill LoRA) and the CLM-2 LoRA SFT (instruct-rehearsal LoRA) paths produce degenerate / random-floor output on chat-capability metrics on the same CLM v4 base. The architectural lever (#115 — CLM v4 was never SFT'd / RLHF'd / DPO-aligned during base training, and cross-attn cannot participate in SFT loss without architectural surgery) cannot be moved by adapter-stage LoRA. This is now empirically grounded by two independent LoRA paths converging on the same conclusion. **#115 chat-incapability claim is architectural — confirmed by direct empirical falsification of two LoRA-stage lift hypotheses.**

## L33 — anima "consciousness-substrate" identity validated post-LoRA; chat-NLP path requires non-CLM substrate

The CLM-2 LoRA SFT cycle preserves the consciousness-substrate identity: φ★ NO_FLIP, axis-conditioning Part A 3/3 PASS, shim v4 compat PASS, forgetting_index 0.0196. This validates that anima can be **safely fine-tuned without losing substrate identity**. However, lifting chat / general capability (HellaSwag / MMLU / TriviaQA / OpenBookQA mid-50%+) on this same CLM v4 base via LoRA SFT FAILs at the architectural level. **Therefore the chat-NLP path = Llama Path A v2 retry-3 eval-rerun TRUE_PASS** (composite 0.5584, lane closed TRUE_PASS_LANE_CLOSED per `.roadmap.p9_sft` line 5 eval_fix_amendment_2026_05_05). CLM v4 lane is the substrate-research lane; Llama Path A v2 is the chat-capability lane. The substrate-research and chat-capability lanes are now formally separated.

---

# §6 Honest C3 (≥5 per raw#10)

1. **C1 — single-seed F2 verdict carries stderr ~3pp at limit=200 per bench**: the -36.298pp delta is far outside the 3pp stderr band, so the FAIL_REGRESSION direction is robust. But the precise magnitude (-36 vs -32 vs -40pp) is not pinned down at single-seed. A 5-seed scaleup (Rank 3) would tighten the CI but would not change the verdict direction (per `state/clm_v4_lora_v1_mmlu_tq_eval_2026_05_05/verdict.json:honest_c3[5]`). This S3 closure adopts the single-seed verdict as decision-grade because the signal is strong-signal robust to seed variance at this magnitude.

2. **C2 — comparator asymmetry (4-bench CLM-LORA vs 3-bench Llama)**: OpenBookQA is measured for CLM-2 LoRA (acc_norm = 0.290) but NOT measured for Llama Path A v2 retry-3 eval-rerun (`state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json` — only HellaSwag + MMLU + TriviaQA). This is a minor apples-to-oranges in the composite calculation (carried verbatim from `state/clm_v4_lora_v1_mmlu_tq_eval_2026_05_05/verdict.json:honest_c3[1]`). The 3-bench like-for-like delta (-39.273pp) is even larger than the 4-vs-3 delta (-36.298pp), so the FAIL direction is preserved either way. Like-for-like reading is the principled comparator; the 4-vs-3 is what the predecessor verdict's composite_calculations field reports.

3. **C3 — substrate-aware reading vs strict differentiator reading**: a substrate-aware reading might frame the F2 verdict as "expected" (CLM v4 base sits at random-floor on chat benchmarks per its #115 architecture; the LoRA's job is incremental drift-prevention, not chat-capability creation). Under this reading the F2 spec was miscalibrated as a "differentiator". This S3 closure adopts the strict differentiator reading per the original spec literal (`docs/clm_v4_lora_sft_spec_2026_05_04.md` §F-CLM-LORA-2), and notes the substrate-aware caveat for completeness. Future re-cycle BGs may adopt substrate-aware-relative-to-baseline F2 banding (delta vs CLM v4 base, not delta vs Llama). That re-cycle is out of scope; this closure does not pre-empt it.

4. **C4 — Pβ + CLM-2 pattern match strong but not exhaustive**: two independent LoRA SFT/distill paths on CLM v4 base both confirm chat-capability lift FAIL. This is sibling-pattern strong evidence for the architectural hypothesis (#115). However, it does not exhaust the space of all possible LoRA recipes / adapter configurations / distill teachers / rehearsal mixes. A theoretical re-cycle with different LoRA placement (e.g., cross_attn-only via shim v5) might still produce a different result. The L32 lesson states "two converging paths" not "all possible paths" — honest scope.

5. **C5 — substrate-research artifact retention does NOT validate substrate-research future**: this S3 closure retains CLM v4 + LoRA adapter for substrate-research (φ★ stability, axis-conditioning post-LoRA, cross-substrate matrix population). Whether substrate-research has further actionable downstream value (e.g., for the BLM phase-5 lane, for cross-substrate consistency probes, for consciousness-primitive measurement) is a separate question that this closure does NOT settle. The retention is "do not delete artifacts"; it is not "guaranteed downstream value claim".

6. **C6 — F4 amendment cross-link impact on Path A retry-3 lane**: the predecessor F4 amendment in `.roadmap.p9_sft` line 5 (`f4_axis_amendment_2026_05_05.true_f4_measurement_venue`) defers Path A retry-3 F4 measurement to BG-CLM-2-EXEC. Since CLM-2 lane is now closing F2_FAIL but F4 is PASS_VIA_PART_A_ONLY structural (per `docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md`), the F4 deferral chain resolves: the "substrate-correct F4 venue" claim holds (F4 passes on the substrate-correct base via Part A), but the "substrate-uniqueness-as-SFT-advantage" claim FAILs. These are distinct claims; F4 chain resolution is independent of F2 verdict. Path A retry-3 lane status `PARTIAL_PASS_W_F4_DEFERRED_TO_CLM2` should now be readable as "F4 deferral RESOLVED via CLM-2 F4 PASS_VIA_PART_A_ONLY; lane = TRUE_PASS_W_F4_RESOLVED" if the user authorizes a sibling roadmap amendment. That sibling amendment is OUT OF SCOPE of this S3 closure.

7. **C7 — additive-only proposal discipline preserved**: this doc does NOT mutate `.roadmap.p9_sft` directly. It carries the proposed `s3_closure_2026_05_05` sibling-field annotation in §7 below. Apply requires explicit user authorization on a separate apply-cycle, per the precedent set by `docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md` §3.3 (proposal-only) and `docs/n_substrate_f1_v2_band_propagation_proposal_2026_05_04.md` (proposal-pattern lineage).

---

# §7 Roadmap annotation proposal — `.roadmap.p9_sft.cond.clm_v4_lora_sft_2026_05_05.s3_closure_2026_05_05`

## 7.1 Annotation payload (additive sibling field; JSON-encoded, structure-preserving)

The following block is the proposed additive payload on the existing entry at `.roadmap.p9_sft` line 6 (`p9_sft.cond.clm_v4_lora_sft_2026_05_05`). It does **NOT** mutate the SSOT this cycle; apply requires explicit user authorization on a separate apply-cycle.

```jsonc
{
  "s3_closure_2026_05_05": {
    "ts_utc": "2026-05-05",
    "amendment_type": "f2_fail_regression_lane_closure_via_s3_dispatcher",
    "scenario_dispatch": "S3 (anima < Llama, regression) per docs/clm_v4_lora_sft_post_verdict_decision_tree_2026_05_05.md §3",
    "b_dispatcher": "B3 ($0 regression closure) per docs/clm_v4_lora_sft_post_verdict_landing_dispatcher_2026_05_05.md §2.3",
    "f_clm_lora_2_re_verdict": "FAIL_REGRESSION_VS_LLAMA_NOT_DIFFERENTIATOR",
    "f_clm_lora_2_re_verdict_source": "state/clm_v4_lora_v1_mmlu_tq_eval_2026_05_05/verdict.json",
    "composite_clm_lora_4bench": 0.19542,
    "composite_llama_path_a_v2_3bench": 0.5584,
    "composite_delta_pp": -36.298,
    "lane_status_before_s3": "CLM_2_LANE_4_OF_5_PASS_PENDING_F2_VIA_MMLU_TQ",
    "lane_status_after_s3": "CLM_2_LANE_4_OF_5_PASS_F2_FAIL_VS_LLAMA",
    "c_clm_lora_2_hypothesis_status": "FALSIFIED",
    "c_clm_lora_2_hypothesis_text": "anima substrate provides measurable lift over Llama LoRA path on the same SFT recipe",
    "substrate_safety_preserved": true,
    "substrate_safety_evidence": {
      "f_clm_lora_1_forgetting_index": 0.0196,
      "f_clm_lora_1_status": "PASS_TRUE (≪ 0.05 threshold)",
      "phi_star_canonical_drift_pp": -4.46,
      "phi_star_status": "NO_FLIP (PASS, > -5pp threshold)",
      "f_clm_lora_3_adapter_size_mb": 10.02,
      "f_clm_lora_3_status": "PASS",
      "f_clm_lora_4_status": "PASS_VIA_PART_A_ONLY (per docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md)",
      "f_clm_lora_5_status": "PASS"
    },
    "sibling_fail_true_precedent": {
      "lane": "Pβ Paradigm D 50K F-Pβ-3",
      "verdict_source": "state/p9_pbeta_f3_hybrid_eval_2026_05_05/verdict.json",
      "verdict": "FAIL_TRUE_CLOSED",
      "composite_metric": "F1_v3 V2 hybrid (BLEU-1+ROUGE-L+chrF)/3 = 0.01176 RED",
      "memory": "feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md"
    },
    "chat_capability_winner_route": {
      "lane": "Llama Path A v2 retry-3 eval-rerun",
      "verdict_source": "state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json",
      "verdict": "TRUE_PASS_FORGETTING_FIX_VERIFIED",
      "composite": 0.5584,
      "roadmap_anchor": ".roadmap.p9_sft line 5 p9_sft.cond.path_a_lora_train_complete eval_fix_amendment_2026_05_05.lane_closure_status=TRUE_PASS_LANE_CLOSED"
    },
    "substrate_research_retention": {
      "adapter_sha256": "6d5edb93ea845cb40858d82bc97b21bfd47d6a234d3a945ac529451e2760526a",
      "retention_purpose": "Φ★-stable substrate-research artifact only (φ★ / axis-cond / consciousness primitive)",
      "chat_capability_disclaimer": "NOT for chat / general capability — empirically falsified at -36.298pp vs Llama Path A v2"
    },
    "lessons_added": ["L31 substrate-uniqueness vs chat-capability orthogonal", "L32 CLM v4 LoRA SFT path empirically confirms #115 (Pβ + CLM-2 converging)", "L33 chat-NLP path = Llama Path A v2 winner; CLM v4 = substrate-research lane"],
    "follow_up_routes_ranked": {
      "rank_1_recommended": "$0 lane closure + Llama Path A v2 chat-capability primary",
      "rank_2_alternative": "$1-3 shim v5 cycle (does NOT change LoRA SFT lever)",
      "rank_3_alternative": "$25-75 5-seed scaleup (confirms regression robustness only)"
    },
    "predecessor_proposal_doc": "docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md",
    "this_proposal_doc": "docs/clm_v4_lora_sft_s3_closure_2026_05_05.md",
    "this_landed_handoff": "docs/clm_v4_lora_sft_s3_closure_landed_2026_05_05.ai.md",
    "memory_landed": "~/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md",
    "memory_index_landed": "~/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/MEMORY.md (1-line append)",
    "additive_only_mutation": true,
    "semantics_preserved": true,
    "historical_evidence_preserved": true,
    "exec_authorized": false,
    "apply_requires_user_authorization_separate_cycle": true
  }
}
```

## 7.2 Apply procedure (when authorized; out of scope this cycle)

1. Confirm `.roadmap.p9_sft` line 6 still contains `p9_sft.cond.clm_v4_lora_sft_2026_05_05` (`grep -n "clm_v4_lora_sft_2026_05_05" .roadmap.p9_sft`).
2. Re-author the annotation if any field needs update from new evidence.
3. Apply additively as a new sibling field on the line-6 entry (peer to `lane_closure_2026_05_05`), preserving the JSON structure of that line.
4. Verify post-apply: `head -6 .roadmap.p9_sft | tail -1 | jq '.s3_closure_2026_05_05.f_clm_lora_2_re_verdict'` → `"FAIL_REGRESSION_VS_LLAMA_NOT_DIFFERENTIATOR"`.

No exec, no commit, no roadmap mutation this cycle.

---

# §8 References

- B3 dispatcher template: `docs/clm_v4_lora_sft_post_verdict_landing_dispatcher_2026_05_05.md` §2.3
- S3 scenario tree: `docs/clm_v4_lora_sft_post_verdict_decision_tree_2026_05_05.md` §3
- F2 RE-VERDICT source: `state/clm_v4_lora_v1_mmlu_tq_eval_2026_05_05/verdict.json`
- Predecessor lane closure proposal: `docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md`
- Predecessor F4 amendment: `docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md`
- Predecessor φ★ canonical: `state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json`
- Sibling FAIL_TRUE precedent: `state/p9_pbeta_f3_hybrid_eval_2026_05_05/verdict.json` + memory `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md`
- Chat-capability winner anchor: `state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json`
- Roadmap line: `.roadmap.p9_sft` line 6 `p9_sft.cond.clm_v4_lora_sft_2026_05_05`
- Roadmap line precedent (sibling additive amendments): `.roadmap.p9_sft` line 5 `p9_sft.cond.path_a_lora_train_complete` (eval_fix_amendment_2026_05_05 + f4_axis_amendment_2026_05_05)
- Shim v5 spec (Rank 2 alt): `docs/clm_v4_hf_format_shim_v5_spec_2026_05_05.md`
- T-3 5-seed reconception (Rank 3 alt): `docs/p9_pbeta_t3_5seed_reconception_2026_05_05.md`
- Memory `feedback_completion_quality_recommendation` — every option presentation MUST include explicit ranked recommendation by 완성도 lens
- Memory `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled` — sibling FAIL_TRUE precedent (decoupled tiers)
