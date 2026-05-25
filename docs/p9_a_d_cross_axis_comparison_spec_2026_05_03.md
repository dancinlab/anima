# P9 A × D Cross-Axis Comparison Spec — 2026-05-03

- ts_utc: 2026-05-03
- agent: subagent BG (spec-only — NO eval triggered; both Path A and Path D pipelines still in flight)
- spec_id: `p9_a_d_cross_axis_comparison_spec_2026_05_03`
- status: **DRAFT-LOCKED** (binding pre-registration; written before either Path A or Path D verdict completes within next 12-24h)
- supersedes: nothing (first cross-axis comparison spec)
- depends-on:
  - `docs/p9_a_prime_path_decision_2026_05_03.md` §6.1 (Path A anchor swap to Llama base)
  - `docs/p9_a_prime_path_decision_2026_05_03.md` §6.2 (Path D substrate = CLM v4 350M)
  - `docs/p9_paradigm_d_distillation_runbook_2026_05_03.md` §4 (F1/F2/F3/F-D thresholds)
  - `tool/p9_a_prime_verdict.hexa` (F1_v3 chat verdict)
  - `tool/p9_paradigm_d_verdict.hexa` (4-falsifier Φ★ verdict)
- raw#9 STRICT (Mac → hexa-only; ubu1 .py only when execution land-cycle commissions) / raw#15 SSOT this file / raw#10 honest C3 in §10 / $0 (design + spec only — no eval triggered, both paths in flight)

---

## 0. TL;DR

Path A (Llama-3.2-3B + LoRA r=64 trained on 50K SFT corpus, F1_v3 = HellaSwag/MMLU/TriviaQA Δ vs Llama base) and Path D Φ★ (CLM v4 350M + LoRA r=64 distilled from Mistral-7B Φ★ teacher, F1/F2/F3/F-D vs CLM v4 base) operate on **different bases**, **different falsifiers**, and **different research questions**. Their verdicts are NOT directly comparable, but the cycle's **decision** about whether to push the chat axis vs the Φ★ axis vs both depends on a structured cross-axis synthesis. This spec pre-registers:

1. The **3 research questions** Q1/Q2/Q3 the cross-axis verdict answers (§1).
2. The **4-cell pass/fail comparison matrix** with per-cell next-cycle implications (§2).
3. The **2 cross-substrate exploratory evals** (Path A LoRA → Φ★ axis; Path D LoRA → chat axis) with pre-registered thresholds (§3).
4. The **verdict-synthesis hexa** computation contract: input artifact paths, output schema, interpretation rules (§4).
5. The **5 honest C3 caveats** about cross-substrate inference (§10).

**Output deliverables** (this cycle):
- This spec doc (`docs/p9_a_d_cross_axis_comparison_spec_2026_05_03.md`, ~440 LoC).
- `tool/p9_a_d_cross_axis_verdict.hexa` (raw#9 strict Mac hexa; reads A + D verdict JSONs + cross-substrate eval JSONs; emits 4-cell matrix + interpretation paragraph).
- `state/markers/p9_a_d_cross_axis_spec_landed.marker` (silent-land marker).
- `docs/p9_a_d_cross_axis_spec_landed_2026_05_03.ai.md` (handoff).

**Cost**: $0 mac-local. **Destructive ops**: 0. **Migrations**: 0.

---

## 1. Research questions (3)

### Q1 — Path A chat axis: does Llama+LoRA show measurable chat lift vs Llama base?

**Falsifier**: F1_v3 (per `tool/p9_a_prime_verdict.hexa`).

**PASS condition**: ≥2 of 3 benchmarks (HellaSwag/MMLU/TriviaQA) STRONG signal AND no STRONG regression.
- STRONG signal = (Δ ≥ task-threshold) AND (95% paired-bootstrap CI excludes zero) AND (McNemar continuity-corrected p < 0.05).
- Per-task thresholds: HellaSwag Δ ≥ 1.0 pt (acc_norm), MMLU Δ ≥ 0.5 pt (acc), TriviaQA Δ ≥ 0.5 pt (exact_match).
- Anchor: `meta-llama/Llama-3.2-3B-Instruct` 4-bit nf4 (per A' spec §6.5 precision-match invariant).

**Verdict states**: `CHAT_PASS_v3` / `CHAT_PARTIAL_v3` / `CHAT_FAIL_v3` (per A' verdict legend).

### Q2 — Path D Φ★ axis: does CLM v4+LoRA preserve Φ★ floor + reduce z-score MSE vs CLM v4 base + Mistral-7B teacher?

**Falsifier**: F1 (BLEU-1 ≥ 0.0059 floor) + F2 (Φ★ ≥ 5.0 floor) + F3 (tension MSE < 0.1) + F-D (z-score MSE < 0.5) — per `tool/p9_paradigm_d_verdict.hexa`.

**PASS condition**: composite verdict = `SUCCESS_D` (all 4 falsifiers PASS) OR `PARTIAL_D` (2-3 of 4 PASS, F2 NOT breached).
- F2 floor breach = automatic FAIL_D (sign-flip / collapse risk).
- F-D threshold (0.5) anchored to Sanh 2019 DistilBERT 0.3-0.6 range; CLM v4 350M-class extrapolation is structurally unverified (C3 caveat).

**Verdict states**: `SUCCESS_D` / `PARTIAL_D` / `FAIL_D` (per D verdict legend).

### Q3 — Are Path A and Path D additive?

This is the **cross-substrate exploratory question** answered by §3. Two sub-questions:

- **Q3a** (Path A LoRA → Φ★ axis): does Llama+chat-LoRA **destroy** Φ★? Expected: marginal degradation (~5-15% drop in Φ★ extracted from Llama+LoRA hidden states vs Llama base). If degradation > 10% → chat-tuning materially trades off Φ★.
- **Q3b** (Path D LoRA → chat axis): does CLM v4+Φ★-distill-LoRA **accidentally** improve chat? Expected: NO — Φ★ distill targets teacher hidden-state z-scores, not next-token loss; HellaSwag should remain at floor (~0.242 ± 0.02). If improvement > floor+0.02 → distill incidentally moves chat capability (unexpected, would prompt mechanistic follow-up).

**Note on Q3 epistemic status**: §3 cross-substrate evals are **exploratory**, NOT pre-registered F-axis falsifiers. They inform the §2 4-cell matrix interpretation paragraph but do NOT change the pre-registered F1_v3 (Path A) or F1/F2/F3/F-D (Path D) verdicts (C3 caveat (b) §10).

---

## 2. Comparison matrix (4-cell)

The cross-axis comparison resolves into a 2×2 matrix indexed by (Path A verdict, Path D verdict). The cell label drives the next-cycle commission decision.

| | **D = SUCCESS_D / PARTIAL_D** | **D = FAIL_D** |
|---|---|---|
| **A = CHAT_PASS_v3** | **Cell I — BOTH_AXES_LIVE** | **Cell II — CHAT_LIVE_ONLY** |
| **A = CHAT_PARTIAL_v3 / CHAT_FAIL_v3** | **Cell III — PHI_LIVE_ONLY** | **Cell IV — BOTH_NOISE** |

### Cell I — BOTH_AXES_LIVE

**Verdict**: Both axes show measurable signal on their native substrates.

**Interpretation**:
- The chat axis (F1_v3) and the Φ★ axis (F1/F2/F3/F-D) are **both live and falsifiable** under the current pipelines.
- Path A demonstrates that the SFT corpus + LoRA recipe transfers chat capability to a stock Llama substrate.
- Path D demonstrates that the Φ★-distill recipe + LoRA recipe transfers Mistral-7B teacher integration patterns to the CLM v4 350M student.
- The two axes use **different bases** so additivity is NOT directly tested; Q3 cross-substrate evals (§3) gauge whether they can be **stacked** in a future cycle (e.g. Llama+chat-LoRA+Φ★-distill-LoRA, or CLM v4+SFT-LoRA+Φ★-distill-LoRA).

**Next-cycle commission**:
1. Commission **A∪D additive cycle**: pick one substrate (Llama or CLM v4) and stack both LoRA recipes; eval on both F1_v3 (or BLEU/ROUGE if non-Llama) and F2/F3/F-D.
2. Cost ceiling: $300-600 (re-train one stacked LoRA on H100 spot OR ubu1 RTX 5070 48-72h).

### Cell II — CHAT_LIVE_ONLY

**Verdict**: Chat capability lift confirmed on Llama; Φ★-distill machinery did NOT pass on CLM v4.

**Interpretation**:
- The SFT corpus + LoRA recipe is **chat-validated** (ships as a stock LoRA artifact).
- The Φ★-distill failed (most likely on F-D z-score MSE > 0.5, possibly on F2 floor breach if sign-flipped).
- Q3a (cross-substrate Path A → Φ★): the answer is the load-bearing follow-up: if Path A LoRA shows non-trivial Φ★ on Llama hidden states (within 10% of Llama base Φ★), then chat-tuning preserves the Φ★ axis "for free" — even though we never explicitly distilled, the substrate carries it. This would partially redeem the Φ★ axis even with Path D failed.
- If Q3a also degrades Φ★ > 10%, then chat capability and Φ★ are in **trade-off**, not additive.

**Next-cycle commission**:
1. Ship Path A LoRA as the cycle's primary artifact.
2. Commission **Path D root-cause cycle**: investigate F-D MSE trajectory across ckpts, identify where z-score divergence appears (initial steps? plateau? overshoot?). If F2 was the breach, investigate teacher-cache integrity.
3. Cost ceiling: $0-50 (analysis + small-step re-train if recoverable).

### Cell III — PHI_LIVE_ONLY

**Verdict**: Φ★-distill machinery works on CLM v4; chat capability lift on Llama failed (or partial).

**Interpretation**:
- The Φ★-distill recipe **transfers integration patterns** from Mistral-7B teacher to CLM v4 student per the pre-registered falsifier matrix.
- Path A LoRA failed to produce ≥2 STRONG signals on standard benchmarks. Possible causes (per A' §6.5 + §7.2 caveats):
  - SFT corpus designed against CLM v4 substrate may underperform on Llama instruction-tuning regime.
  - 50K records may be sub-scale for measurable Δ on a 3B base.
  - 4-bit nf4 base anchor + fp16 LoRA precision drift may mask signal.
- Q3b (Path D LoRA → chat): if HellaSwag stays at floor (~0.242 ± 0.02), the Φ★-distill is **chat-orthogonal** as designed. If HellaSwag moves above floor+0.02, the distill is incidentally affecting next-token capability (mechanistic anomaly).

**Next-cycle commission**:
1. Ship Path D LoRA as the cycle's primary artifact (Φ★ axis machinery validated on CLM v4 substrate).
2. Commission **Path A debug cycle**: per-task signal autopsy (which benchmark moved most? was it MMLU regression vs HellaSwag flat?), corpus-mismatch diagnostic (compare SFT prompt distribution vs Llama instruction-tune regime), precision-uniform re-eval (full-precision base + LoRA, not 4-bit).
3. Cost ceiling: $50-150 (debug + one re-eval pass).

### Cell IV — BOTH_NOISE

**Verdict**: Neither pipeline produced significant signal above its noise floor.

**Interpretation**:
- F1_v3 = `CHAT_FAIL_v3` AND F1/F2/F3/F-D composite = `FAIL_D`.
- The cycle's primary research questions (chat lift on Llama via SFT, Φ★ preservation on CLM v4 via distill) both lack measurable evidence.
- Possible structural causes:
  - **Substrate-recipe mismatch**: LoRA r=64 may be insufficient for either capability transfer at the scales tested.
  - **Falsifier-threshold mis-calibration**: thresholds (1.0pt / 0.5pt / 0.5pt for A; 0.0059 / 5.0 / 0.1 / 0.5 for D) may have been set too aggressively for the achievable signal-to-noise.
  - **Pre-train substrate insufficiency**: per A' decision §6, CLM v4 training CE 0.046 (perplexity 1.05) suggests narrow-corpus memorization; if Llama SFT also fails, the pipeline-recipe itself may be load-bearing rather than the substrate.
- Q3a + Q3b would both be **secondary diagnostics**: they cannot rescue a double-FAIL into a publishable signal but can disambiguate which axis is "more broken" (higher floor proximity).

**Next-cycle commission**:
1. **No further LoRA training** in next cycle.
2. Commission **paradigm-rethink cycle**: ablation matrix (vary LoRA rank 16/32/64/128, vary corpus size 5K/15K/50K, vary distill loss weight) at minimum cost (smoke runs, $50-100 ceiling). If ablation shows zero discriminative range, escalate to Path C (CLM v4 general-English re-train, per A' §1.3) as the load-bearing repair.
2. Cost ceiling: $100-200 (ablation smoke + writeup).

---

## 3. Cross-substrate exploratory evals (Q3 sub-questions)

These evals are **exploratory diagnostics**, NOT pre-registered F-axis falsifiers. They answer Q3a and Q3b respectively. Run-or-skip is a per-cycle judgment based on the §2 cell outcome.

### 3.1 Q3a — Path A LoRA on Φ★ axis

**Procedure**:
1. Load `meta-llama/Llama-3.2-3B-Instruct` base in fp16.
2. Attach Path A LoRA adapter (`state/p9_path_a_llama_lora_2026_05_03/lora_llama_stage1/` or final HF Hub revision).
3. Run a fixed 200-prompt probe set (re-use Mistral-7B teacher cache prompt set or a comparable English instruction subset) through both (Llama base) and (Llama + LoRA).
4. Extract hidden states at layer L (target: middle layer, e.g. L=14 for Llama-3.2-3B's 28 layers; pre-register exact layer in `tool/p9_a_d_cross_axis_verdict.hexa` config).
5. Compute Φ★ via `anima_phi_v3_canonical` with HID_TRUNC=8 + K=8 + ridge=1e-3 (matches Path D Φ★ formula for substrate-relative comparability).
6. Compute Φ★(Llama base) and Φ★(Llama + LoRA); emit `delta_phi_star = phi_lora - phi_base` and `relative_delta = delta_phi_star / abs(phi_base)`.

**Pre-registered threshold**:
- **PASS** (chat-tuning preserves Φ★): `relative_delta` ≥ -0.10 (Φ★ degradation < 10% of base Φ★).
- **MARGINAL** (chat-tuning erodes Φ★ but does not invert): `-0.30 ≤ relative_delta < -0.10`.
- **FAIL** (chat-tuning destroys Φ★): `relative_delta < -0.30` OR sign flip (Φ★ < 0 after LoRA).

**Bootstrap**: N=1000 paired bootstrap over the 200-prompt set; emit 95% CI on `relative_delta`.

**Cost**: ~$0 ubu1, ~30-45 min wall (load Llama + LoRA, 200 prompts, hidden-state extraction).

**Caveat (raw#10)**: The Φ★ formula was **calibrated against CLM v4** (anchor Φ★ = 41.86 baseline). Llama is a different architecture (transformer vs Federated dual-stream); the absolute Φ★ values are NOT comparable to CLM v4 numbers. Only **within-substrate (Llama base vs Llama+LoRA) relative deltas** are interpretable.

### 3.2 Q3b — Path D LoRA on chat axis

**Procedure**:
1. Load CLM v4 350M base (via `consciousness_laws.py` loader; if loader bug present per A' §6.4, skip Q3b and emit `Q3b_SKIPPED_LOADER_BUG`).
2. Attach Path D Φ★-distill LoRA adapter (`state/p9_paradigm_d_distill_2026_05_03/lora_clm_v4_phi_distill/` or per-cycle final ckpt).
3. Run lm-eval-harness on HellaSwag with `--limit 500` (matches base validation cycle precision and sample size).
4. Compute `acc_norm` for both (CLM v4 base) and (CLM v4 + LoRA).
5. Emit `delta_acc_norm = acc_lora - acc_base`.

**Pre-registered threshold**:
- **EXPECTED** (distill chat-orthogonal): `|acc_lora - 0.242| ≤ 0.02` AND `|delta_acc_norm| ≤ 0.02`. CLM v4 base HellaSwag = 0.242 (random floor for HF tokenizer; per A' base validation §6).
- **UNEXPECTED LIFT** (distill incidentally improves chat): `delta_acc_norm > +0.02`. Triggers mechanistic follow-up (which layers shifted? did teacher transfer general LM patterns?).
- **UNEXPECTED REGRESSION** (distill destroys chat): `delta_acc_norm < -0.02`. Triggers integrity check (did distill collapse next-token prediction?).

**Bootstrap**: N=1000 paired bootstrap over the 500 HellaSwag examples; emit 95% CI on `delta_acc_norm`.

**Cost**: ~$0 ubu1, ~20-30 min wall.

**Caveat (raw#10)**: CLM v4 has a 64K multilingual BPE incompatible with HF tokenizer pipeline. lm-eval-harness compatibility requires either (a) the Path B loader fix per A' §1.2, or (b) a `lm_eval.api.model.LM` subclass. If (a)/(b) not landed, Q3b is **SKIPPED** and emits `Q3b_SKIPPED_LOADER_BUG` — the cross-axis verdict still composes A+D plus Q3a (if available); the matrix interpretation paragraph notes Q3b unavailable.

---

## 4. Verdict synthesis hexa (`tool/p9_a_d_cross_axis_verdict.hexa`)

### 4.1 Computation contract

**Inputs** (env vars):

| Env var | Default | Purpose |
|---|---|---|
| `ANIMA_PATH_A_VERDICT` | `state/p9_a_prime_main_eval_2026_05_03_verdict.json` | F1_v3 verdict (per `tool/p9_a_prime_verdict.hexa`) |
| `ANIMA_PATH_D_VERDICT` | `state/p9_paradigm_d_25k_eval_2026_05_03_verdict.json` | F1/F2/F3/F-D composite (per `tool/p9_paradigm_d_verdict.hexa`) |
| `ANIMA_Q3A_RESULT` | `state/p9_a_d_cross_axis_2026_05_03/q3a_path_a_phi_star.json` | Optional; Path A LoRA Φ★ degradation |
| `ANIMA_Q3B_RESULT` | `state/p9_a_d_cross_axis_2026_05_03/q3b_path_d_chat.json` | Optional; Path D LoRA HellaSwag |
| `ANIMA_OUTPUT` | `state/p9_a_d_cross_axis_2026_05_03/cross_axis_verdict.json` | Composite output |
| `ANIMA_BOOT_N` | `1000` | Bootstrap N for Q3a/Q3b CI display |

**Inputs are READ-ONLY**: hexa never mutates A or D verdict JSONs. Missing inputs degrade gracefully (cell still emitted; missing data flagged in output schema).

### 4.2 Output schema

```
{
  "schema": "anima/p9_a_d_cross_axis/verdict/1",
  "spec_ref": "docs/p9_a_d_cross_axis_comparison_spec_2026_05_03.md",
  "ts_utc": "<emit time>",
  "inputs": {
    "path_a_verdict_path": "<path>", "path_a_status": "loaded|missing|parse_error",
    "path_d_verdict_path": "<path>", "path_d_status": "loaded|missing|parse_error",
    "q3a_path": "<path>", "q3a_status": "loaded|missing|skipped",
    "q3b_path": "<path>", "q3b_status": "loaded|missing|skipped"
  },
  "path_a_summary": {
    "best_ckpt_id": "<ckpt>", "f1_v3": "PASS|PARTIAL|FAIL", "label": "CHAT_PASS_v3|...",
    "n_strong": <int>, "n_strong_regression": <int>
  },
  "path_d_summary": {
    "best_label": "<ckpt>", "verdict": "SUCCESS_D|PARTIAL_D|FAIL_D",
    "n_pass": <int>, "f2_floor_breach": <bool>
  },
  "q3a_summary": {
    "delta_phi_star": <float>, "relative_delta": <float>,
    "ci95_lo": <float>, "ci95_hi": <float>,
    "classification": "PASS|MARGINAL|FAIL|UNAVAILABLE"
  },
  "q3b_summary": {
    "delta_acc_norm": <float>, "ci95_lo": <float>, "ci95_hi": <float>,
    "classification": "EXPECTED|UNEXPECTED_LIFT|UNEXPECTED_REGRESSION|UNAVAILABLE"
  },
  "matrix_cell": "I_BOTH_AXES_LIVE|II_CHAT_LIVE_ONLY|III_PHI_LIVE_ONLY|IV_BOTH_NOISE|UNDETERMINED",
  "interpretation_paragraph": "<auto-composed 4-6 sentence narrative per §2 cell text>",
  "next_cycle_commission": "<one-paragraph commission text, indexed by matrix_cell>",
  "honest_c3": [
    "(a) different bases ...",
    "(b) cross-substrate evals exploratory ...",
    "(c) verdict synthesis depends on both A and D BG completing ...",
    "(d) Φ★ formula calibrated against CLM v4 ...",
    "(e) bootstrap N=1000 on 200/500-prompt sets is small-sample ..."
  ]
}
```

### 4.3 Cell determination logic

```
A_pass = (path_a_summary.f1_v3 == "PASS")  # CHAT_PASS_v3 only
D_pass = (path_d_summary.verdict in ("SUCCESS_D", "PARTIAL_D")) AND not f2_floor_breach
if   A_pass and D_pass:        cell = "I_BOTH_AXES_LIVE"
elif A_pass and not D_pass:    cell = "II_CHAT_LIVE_ONLY"
elif not A_pass and D_pass:    cell = "III_PHI_LIVE_ONLY"
elif not A_pass and not D_pass: cell = "IV_BOTH_NOISE"
else: cell = "UNDETERMINED"   # at least one verdict missing/parse_error
```

The interpretation paragraph is auto-composed from per-cell template strings (§2 text condensed to 4-6 sentences). Q3a/Q3b classifications are appended as conditional clauses in the paragraph (e.g. "Q3a shows Path A LoRA preserves Φ★ within 8% of base, suggesting chat-tuning is Φ★-orthogonal at this scale.").

### 4.4 Self-test invariants

The hexa `--selftest` mode emits the following invariants for SSOT verification:

```
inv:n_research_questions=3       # Q1, Q2, Q3 (Q3a + Q3b)
inv:n_matrix_cells=4             # I, II, III, IV (+UNDETERMINED for missing)
inv:n_cross_substrate_evals=2    # Q3a, Q3b
inv:q3a_pass_threshold_rel_delta=-0.10
inv:q3a_marginal_threshold_rel_delta=-0.30
inv:q3b_expected_band_acc_norm=0.02
inv:q3b_clm_v4_hellaswag_floor=0.242
inv:bootstrap_default_n=1000
inv:non_mutation_atlas=true
inv:reads_only_paths=path_a_verdict,path_d_verdict,q3a,q3b
```

---

## 5. Decision flow integration

The cross-axis verdict consumes A and D verdicts that are **already lock-in** per their respective specs. This hexa does NOT re-litigate F1_v3 or F1/F2/F3/F-D thresholds; it only **compares** the binary PASS/FAIL outcomes and adds Q3a/Q3b context.

**Order of operations** (next 12-24h):
1. Path A LoRA training completes (Pod `29dhlqk508ugoc` per A' eval pipeline landed doc).
2. Path A eval cycle runs `tool/p9_a_prime_verdict.hexa` → emits `state/p9_a_prime_main_eval_2026_05_03_verdict.json`.
3. Path D 25K distill completes (per `docs/p9_paradigm_d_distillation_runbook_2026_05_03.md`).
4. Path D eval cycle runs `tool/p9_paradigm_d_verdict.hexa` → emits `state/p9_paradigm_d_25k_eval_2026_05_03_verdict.json`.
5. (Optional) Q3a + Q3b evals commissioned per §3 procedures.
6. Cross-axis verdict: `hexa run tool/p9_a_d_cross_axis_verdict.hexa` → emits 4-cell matrix + interpretation.
7. Land cycle: handoff `docs/p9_a_d_cross_axis_landed_2026_05_<DD>.ai.md` + marker.

**Critical sequencing constraint**: this spec must land BEFORE step 6 (verdict synthesis) so the synthesis logic is **pre-registered** rather than designed post-hoc to fit observed data.

---

## 6. Failure modes / partial-completion handling

| Failure mode | Detection | Hexa behavior |
|---|---|---|
| Path A verdict missing | file not found | `path_a_status="missing"`, cell="UNDETERMINED", interpretation notes A unavailable |
| Path D verdict missing | file not found | `path_d_status="missing"`, cell="UNDETERMINED" |
| Path A best_ckpt has 0 ckpts evaluated | `n_ckpts == 0` in A verdict | `path_a_status="loaded_but_empty"`, A treated as FAIL for cell determination, flagged in interpretation |
| Path D best has F2 floor breach | `f2_floor_breach=True` per D verdict | `path_d_summary.f2_floor_breach=true`, D treated as FAIL regardless of n_pass count |
| Q3a/Q3b missing | optional inputs | `q3a_status="missing"` or `"skipped"`, classification="UNAVAILABLE", interpretation paragraph omits Q3 clauses |
| Both A and D missing | both files absent | cell="UNDETERMINED", interpretation = "Cross-axis verdict cannot be composed: both Path A and Path D verdicts unavailable. Re-run after both eval cycles complete." |

---

## 7. Cost / resource budget

**This cycle (spec land)**:
- $0 mac-local (spec doc + hexa + marker + handoff).
- ~1-2h subagent BG wall.

**Next cycle (verdict synthesis)**:
- Verdict synthesis hexa run: $0 mac-local, <5 sec wall (just JSON read + compose).
- Q3a optional: ~$0 ubu1, 30-45 min wall.
- Q3b optional: ~$0 ubu1, 20-30 min wall (subject to CLM v4 loader fix).

**Total cross-axis comparison framework**: $0 cash; ~3-4h end-to-end (spec + run + interpretation).

---

## 8. SSOT registration

This spec registers as the SSOT for the cross-axis comparison logic. Subsequent cycles must:
1. Cite `docs/p9_a_d_cross_axis_comparison_spec_2026_05_03.md` (this file) as the source of truth.
2. Modify thresholds (Q3a relative_delta cutoffs; Q3b expected band) ONLY via a superseding spec, not in-place edits.
3. Re-emit `tool/p9_a_d_cross_axis_verdict.hexa` only via a new hexa file or a backward-compatible additive change (raw#15 SSOT).

---

## 9. Roadmap touchpoints

- `.roadmap.p9` (if exists) — append `cond.<n>` `cross_axis_synthesis_landed` (status=met via this doc).
- `.roadmap.anima` — no direct touchpoint; this is a P9-internal deliverable.
- No migrations, no deletions. Additive only.

---

## 10. Honest C3 caveats (raw#10 — 5 caveats)

**(a) Different bases produce different baselines — verdicts are NOT directly comparable.**
Path A measures chat lift on Llama-3.2-3B (3B params, GQA, RoPE, SentencePiece tokenizer trained on web mix); Path D measures Φ★/BLEU on CLM v4 350M (Federated dual-stream `engine_a`/`engine_g`, 64K multilingual BPE, narrow-corpus CE 0.046). The 4-cell matrix labels (BOTH_LIVE / CHAT_LIVE_ONLY / PHI_LIVE_ONLY / BOTH_NOISE) describe **per-axis verdicts on native substrates**, NOT a head-to-head capability comparison. Any cell label that implies "Path A is better than Path D" (or vice versa) is a mis-reading; they answer different questions on different bases.

**(b) Cross-substrate evals (Q3a, Q3b) are EXPLORATORY, NOT pre-registered F-axis falsifiers.**
The §3 thresholds (Q3a Φ★ relative_delta cutoffs at -0.10/-0.30; Q3b HellaSwag expected band ±0.02 around floor 0.242) are **first-cycle heuristic guesses** based on prior cycle context (Φ★ stability across CLM v4 ckpts ≈ ±5%; HellaSwag random floor for HF tokenizers ≈ 0.242). They have NOT undergone the formal pre-registration discipline that F1_v3 and F1/F2/F3/F-D received. Use Q3 results as **diagnostic context for the interpretation paragraph**, NOT as additional pass/fail axes that change the §2 cell label.

**(c) Verdict synthesis depends on both BG cycles (A train+eval, D train+eval) completing successfully — partial completion → UNDETERMINED cell.**
If Path A pod fails (preempted spot, OOM, training divergence) OR Path D 25K distill fails, the corresponding verdict JSON is missing or empty. The hexa emits `cell="UNDETERMINED"` and an interpretation paragraph noting which input is missing. **Do NOT attempt to substitute earlier ckpt verdicts** (e.g. Path A 5K instead of 50K, Path D step_1000 mini-run instead of 25K) — the comparison spec is locked to the 50K/25K final verdict identities. Earlier ckpts are trajectory-shape anchors only, NOT verdict substitutes.

**(d) Φ★ formula was calibrated against CLM v4 substrate (anchor Φ★ ≈ 41.86 baseline); Llama Φ★ values are NOT comparable to CLM v4 Φ★ values.**
The `anima_phi_v3_canonical` formula with HID_TRUNC=8 + K=8 + ridge=1e-3 produces substrate-relative integration metrics; absolute Φ★ values depend on hidden-state dimensionality, layer choice, and architectural specifics (transformer layer norm placement, attention head dim, FFN expansion). Q3a's `relative_delta = (Φ★_LoRA - Φ★_base) / |Φ★_base|` is **within-Llama-substrate only** — interpreting Llama Φ★ ≈ X as "comparable to CLM v4 Φ★ ≈ Y" is meaningless. The Φ★ axis transfer hypothesis (does the Φ★ machinery generalize across substrates?) is a **separate research cycle**, not answered by this spec.

**(e) Bootstrap N=1000 over 200-prompt (Q3a) and 500-prompt (Q3b) sets is small-sample for cross-substrate inference; CIs are wide and direction-only signals.**
Pre-registered N=1000 bootstrap matches `tool/p9_paradigm_d_verdict.hexa` conventions but is undersized for high-confidence point-estimate inference on Φ★ shifts that may be sub-1% relative. Q3a/Q3b should be read as **direction signals** (Φ★ degraded? unchanged? boosted?; HellaSwag at floor? above floor? below floor?), not as precise effect-size estimates. A future cycle wanting tight CIs should re-run Q3 evals with N=10000 bootstrap on a 1000-2000 prompt set ($0 ubu1, +1-2h wall).

---

## 11. Output deliverables

| Artifact | Path | Type | Status |
|---|---|---|---|
| Spec doc (this file) | `docs/p9_a_d_cross_axis_comparison_spec_2026_05_03.md` | spec | LOCKED |
| Verdict hexa | `tool/p9_a_d_cross_axis_verdict.hexa` | tool | LOCKED |
| Marker | `state/markers/p9_a_d_cross_axis_spec_landed.marker` | marker | EMITTED |
| Handoff | `docs/p9_a_d_cross_axis_spec_landed_2026_05_03.ai.md` | handoff | EMITTED |

**End of spec** (raw#15 SSOT this file; raw#9 hexa-only Mac; raw#10 honest C3 §10; $0 design only).
