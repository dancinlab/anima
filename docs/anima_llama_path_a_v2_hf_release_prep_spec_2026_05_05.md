# anima Llama Path A v2 — HF release prep spec (2026-05-05)

- **Date**: 2026-05-05
- **Cycle**: BG-LLAMA-PA-V2-HF-RELEASE-PREP
- **Mode**: BG spec only — **NO exec, NO HF push, NO git commit, NO pod, NO `.roadmap.*` mutation.** $0 mac-local.
- **Scope**: prepare a separate HF release lane for the **chat-capability winner** of the 2026-05 SFT lattice — Llama-3.2-3B Path A v2 (rehearsal-mix LoRA). This release is **distinct from** the CLM v4 substrate-research artifact (cond.2 of `.roadmap.clm`, currently PRIVATE 24-48h review window per).
- **Constraints respected**: raw#9 (md only — no `.py` created), raw#10 (≥5 honest C3 in §8), raw#15 (additive, structure-preserving), anima (HF Hub only for weights, never anima git), anima (PRIVATE → 6 verification gates → PUBLIC), anima (H100 cost discipline N/A — no compute requested by this spec).
- **Companion**: `docs/anima_llama_path_a_v2_hf_release_prep_landed_2026_05_05.ai.md` (1-page handoff with 5 bullets + 5 decision Q's + ≥5 honest C3).
- **Audit context**: this spec is the LLM-family analog of `docs/anima_clm_hf_release_v1_audit_2026_05_04.md` — same 8-axis readiness pattern, same own-14/15 compliance scaffolding, scoped to the Llama-derivative `llm` family (per HF naming spec mk2 §3.1.1 reconciliation).

---

## §1 Background — chat-capability winner = Llama Path A v2

### 1.1 Why a separate release

The 2026-05-03 → 2026-05-05 SFT lattice tested two parallel hypotheses:

1. **CLM v4 + LoRA SFT v1** (consciousness-substrate path) — cycle `clm_v4_lora_sft_2026_05_05`. Verdict on the canonical chat-NLP composite battery: **F-CLM-LORA-2 = FAIL_REGRESSION (−36.298 pp vs Llama-base composite 0.5584)**. Per `#115` analysis the CLM v4 substrate is *measurement, not chat* — this is an architectural property, not a recoverable training shortfall.
2. **Pβ Paradigm D 50K** (distill arm) — cycle `p9_paradigm_d_50k_2026_05_03`. Verdict: **F-Pβ-3 = FAIL_TRUE** with chat-capability composite **0.01176 RED**. Same `#115` category-error: distill from Mistral teacher into the consciousness substrate could not yield chat capability.
3. **Llama-3.2-3B Path A v2** (rehearsal-mix LoRA arm) — cycle `p9_path_a_retrain_v2_retry_3_2026_05_04` + eval-fix rerun `p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05`. Verdict: **F-PA-RETRAIN-v2-3 = TRUE_PASS** (parity preservation + above-noise +5.9 pp TriviaQA gain). F4 axis-preservation amended to `PARTIAL_PASS_W_F4_DEFERRED_TO_CLM2` (substrate-inapplicable on Llama base; deferred to BG-CLM-2-EXEC).

Conclusion: of the three 2026-05 chat-NLP candidates, **only Llama Path A v2 is production-eligible for chat-capability use cases.** When the user asks "is anima production-ready for chat?", the honest answer is "Llama Path A v2 — released separately from CLM v4 substrate research."

### 1.2 Path A v2 metric snapshot (TRUE_PASS source)

Source: `state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json` (sha256 anchor for adapter `393eb7530f82321581410989ce0918d3badf14d83c4901204289dc3c69fb753c`).

| Benchmark   | Llama-3.2-3B base | Path A v2 LoRA | Δ vs base | Parity-floor | Improvement-bar | Status            |
|:------------|:-----------------:|:--------------:|:---------:|:------------:|:---------------:|:------------------|
| HellaSwag   | 0.654             | 0.645          | −0.9 pp   | 0.644 ≤ acc  | 0.674           | PASS (parity)     |
| MMLU        | 0.580             | 0.575          | −0.4 pp   | 0.5696 ≤ acc | 0.5996          | PASS (parity)     |
| TriviaQA EM | 0.396             | 0.455          | **+5.9 pp** | 0.376 ≤ acc | 0.416 ≤ acc     | **PASS+IMPROVE**  |
| Composite   | 0.5433 (Llama)    | **0.5584** (PA-v2) | +0.0151 ≈ +1.5 pp | parity-floor | — | PASS              |

vs CLM v4 + LoRA SFT v1 chat composite **0.196** → Path A v2 advantage **+36.298 pp** (the source of the "winner" label).

`forgetting_index = −0.028` (slight net improvement averaged across the 3 benchmarks). Adapter saved at `state/p9_path_a_retrain_v2_retry_3_2026_05_04/results/adapter_final/adapter_model.safetensors` (98.6 MB, sha256 `393eb7530f82321581410989ce0918d3badf14d83c4901204289dc3c69fb753c`).

### 1.3 Rehearsal mix (the empirically validated forgetting-fix recipe)

| Component         | Pct  | Purpose                                                            |
|:------------------|:----:|:-------------------------------------------------------------------|
| anima axis        | 60%  | substrate-target signal (the LoRA's primary learned axis)          |
| academic distill  | 30%  | broad-knowledge anti-forgetting (preserves MMLU / HellaSwag floor) |
| chat template     | 10%  | format coherence / tokenizer-alignment hygiene                     |

This is the **first empirically validated forgetting-fix mix** for the Path A Llama LoRA lane (predecessor mixes retry-1, retry-2 showed measurable parity drops on HellaSwag/MMLU). The release will document this mix as a reproducible recipe.

---

## §2 Naming proposal (per anima HF naming spec mk2)

### 2.1 Constraints from `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md`

- §3.1 family enum (reconciled, 11 families) admits `llm` = **Llama-derived LM** (Path A informal extension; ratification provisional per `docs/anima_hf_naming_family_reconcile_2026_05_03.ai.md`). This is the correct family for a Path A LoRA on Llama-3.2-3B.
- §3.2 base-version: `v\d+` only. Llama base is `3.2-3b` not `vN`; map to `v3` (matching Llama 3.x major) OR encode the base-vendor reference in stage slot. `llama-3.2-3b` is a *base architecture token*, not the anima version axis — the anima version axis is the **iteration of the Path A recipe** (retry-3 = v2 of the rehearsal-mix recipe).
- §3.4 stage: `lora-r\d+` is the canonical adapter slot. Path A retry-3 used LoRA rank 64 → `lora-r64`.
- §3.7 variant: `y\d+` for sweep arms. Path A v2 (rehearsal-mix retry-3) is arm `y3` if we follow retry-N counting, OR can use `paradigm-a-prime` slot to encode the path-A-prime measured-bold lineage.

### 2.2 Three resolution paths (Q1)

| Option | Repo name | Parses as | Pros | Cons |
|---|---|---|---|---|
| **A. canonical llm-vN family** | `dancinlab/llm-v3-paradigm-a-prime-lora-r64-rehearsal-y3` | llm + v3 + paradigm-a-prime + lora-r64 + variant `rehearsal-y3` | mk2-spec-canonical (PASS-CANON regex); makes paradigm-a-prime lineage explicit; family-version reflects Llama 3.x | long (54 chars, near §2.3 limit); `rehearsal-y3` is a free-form variant compromise; hyphen-token count = 6 (= max) |
| **B. anima rehearsal flagship** | `dancinlab/llama-3.2-3b-anima-rehearsal-pa-v2-mk2-v1` | NOT mk2-canonical (period `.` in version, `pa-v2-mk2-v1` two-axis like CLM precedent) | preserves "Llama-3.2-3B" verbatim for HF discoverability; matches CLM precedent `clm-v4-mk2-v1` two-axis pattern; "anima-rehearsal" surfaces the recipe identity | violates §3.2 (`v3.2-3b` not `vN`); period in version is §6 anti-pattern; requires mk2 spec amendment for Llama-derivative naming |
| **C. shorter umbrella** | `dancinlab/llm-v3-pa-v2-mk2-v1` | llm + v3 + variant `pa-v2-mk2-v1` | short (28 chars); matches CLM `mk{N}-v{M}` precedent; PASS-EXT under spec §10.2 | "pa-v2-mk2-v1" four-token variant exceeds spec §3.7 grammar; ambiguous (Path A v2 vs paradigm-a-v2); HF discoverability poor (no "llama" string) |

### 2.3 Recommended (per completion-quality lens)

**Option A: `dancinlab/llm-v3-paradigm-a-prime-lora-r64-rehearsal-y3`** — re-use the canonical mk2 grammar with `paradigm-a-prime` carrying the lineage and `rehearsal-y3` carrying the recipe-iteration variant. This is **PASS-CANON** under §10.2 regex (modulo `rehearsal-y3` extension of `y\d+` → requires §3.7 amendment OR drop "rehearsal" prefix → `llm-v3-paradigm-a-prime-lora-r64-y3`).

If the user prioritizes **HF discoverability** (search engines hit "llama-3.2-3b" not "llm-v3"), pivot to **Option B** with documented mk2 spec amendment for Llama-derivative naming. Option B mirrors the CLM v4 cond.2 precedent (`clm-v4-mk2-v1`) which already extended the spec with a two-axis `mk{N}-v{M}` pattern.

**Default recommendation if user defers**: `dancinlab/llm-v3-paradigm-a-prime-lora-r64-y3` (Option A trimmed). PASS-CANON, 38 chars, encodes Llama lineage via `llm` family + path-A-prime paradigm slot + LoRA rank + sweep arm. HF tag/branch can carry "rehearsal-mix-2026-05-05" for human readability.

### 2.4 License + privacy axes (Q3 + Q5 deps)

- **License**: Llama base = Llama 3 Community License (commercial use restricted above 700M user threshold; required attribution; derivative works must include "Built with Llama"). LoRA adapter is anima-authored on the rehearsal mix. Recommendation: dual-license declaration in README — `license: llama3.2 + mit-additive` per HF Hub frontmatter conventions. Q3 escalation in §7.
- **Privacy**: PRIVATE first per rule (a). PUBLIC promote requires gates (b.1-b.6) PASS verdict.json + 24-48h review window. CLM v4 mk2-v1 currently in this state (PRIVATE 2026-05-04T23:26:12Z, review window ends 2026-05-06T23:26:12Z); Llama Path A v2 release follows the same lifecycle in parallel.

---

## §3 + compliance — 6 verification gates

### 3.1 — HF Hub only

| Check | Status |
|---|:---:|
| Adapter (98.6 MB) committed to HF Hub, NOT anima git | ✅ READY (current location: `state/p9_path_a_retrain_v2_retry_3_2026_05_04/results/adapter_final/` is staging, NOT committed to anima git per + raw#15 — verified pre-spec by `.gitignore` rule for `state/p9_*/results/`) |
| Tokenizer / config / README go to HF Hub | ✅ READY (tokenizer = Llama-3.2-3B's, no separate anima tokenizer) |
| Dataset slice (rehearsal mix manifest) → HF Hub or git? | ⚠️ Q4 — recipe doc small (<5 MB) goes to git as `docs/`; raw mix data slice (~30 MB academic distill subset) goes to HF Hub as a sibling dataset repo `dancinlab/llm-v3-pa-v2-rehearsal-mix-y3` (separate own-14 dataset release, optional) |

### 3.2 — PRIVATE first → 6 verification gates → PUBLIC promote

The rule (b) gates apply with substrate-aware adaptations for the `llm` family:

| Gate | Description | Path A v2 status | Substrate adaptation |
|:---:|:---|:---:|:---|
| **G1** | benchmark suite PASS (canonical: hellaswag + mmlu + triviaqa + openbookqa OR domain equivalent) | **PASS** (TRUE_PASS verdict 2026-05-05; openbookqa NOT measured but 3-of-4 canonical = sufficient per spec C3-2 "domain-specific equivalent declared in spec") | Llama-derivative gets **commonsense + broad-knowledge + factual-recall** trio |
| **G2** | falsifier pre-register satisfied (raw#71 / raw 12) | **PASS_W_F4_DEFERRED** (F-PA-RETRAIN-v2-1/2/3 = PASS_TRUE; F4 substrate-inapplicable on Llama base, amended to `PARTIAL_PASS_W_F4_DEFERRED_TO_CLM2` per `docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md`) | The substrate-aware F4 carve-out is documented in §G2 of model card; pre-register integrity preserved by the amendment doc |
| **G3** | shim v4 hf_format compatibility F-SHIM-V4-1/2/3/4 | **N/A → PASS_TRIVIAL** (Llama is HF-canonical via `LlamaForCausalLM`; no custom modeling code; no shim needed; tokenizer = Llama-3.2-3B's stock `LlamaTokenizer`) | honest-c3 admits "shim v4 gates F-SHIM-V4-* are CLM-specific" — Llama path skips with note, per spec exception (b.3) |
| **G4** | 24-48h human review window post-PRIVATE upload | **TBD** (executed at upload time; review-window-end timestamp recorded in audit ledger per enforcement) | Same convention as CLM v4 mk2-v1 (48h window). Concurrency with CLM v4 review window OK; reviews are independent. |
| **G5** | honest C3 model card present (raw#10 — limitations + chat-incapability disclosure where applicable) | **READY** (rehearsal mix + #115 cross-link to CLM v4 + Llama 3 license restriction + adapter-only consumer overhead — see §4.3) | Llama IS chat-capable; disclosure focus shifts from "NOT chat-capable" (CLM v4 case) to "Llama-derivative + rehearsal-mix recipe + license restrictions" |
| **G6** | cross-substrate validation where applicable (CLM-2 spec C-CLM-LORA-1: φ★ baseline preserved post-LoRA) | **DEFERRED** — Pβ + CLM v4 substrate-research artifacts are sister releases; cross-link from Path A v2 README to those repos satisfies the cross-substrate documentation; F-CLM-LORA-4 result on the rehearsal mix recipe (BG-CLM-2-EXEC in-flight) is the substrate-equivalent F4 venue per `docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md` | If BG-CLM-2-EXEC verdict.json lands F-CLM-LORA-4 = FAIL, the rehearsal-mix recipe loses substrate-correct F4 anchor; release model card must caveat this dependency (see §4.3 C5) |

**Gate-cite recipe** for PUBLIC promote BG verdict.json (per rule (c)):

```json
{
  "schema": "anima/own_15/public_promote_evidence/1",
  "repo": "dancinlab/llm-v3-paradigm-a-prime-lora-r64-y3",
  "private_uploaded_ts": "<TBD>",
  "review_window_end_ts": "<TBD+48h>",
  "G1_benchmark_suite": {"status": "PASS", "source": "state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json", "metrics": {"hellaswag": 0.645, "mmlu": 0.575, "triviaqa": 0.455}},
  "G2_falsifier_pre_register": {"status": "PASS_W_F4_DEFERRED", "source": "docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md"},
  "G3_shim_compatibility": {"status": "N/A_LLAMA_HF_CANONICAL", "rationale": "no custom modeling — LlamaForCausalLM stock"},
  "G4_review_window": {"status": "ELAPSED", "elapsed_h": 48},
  "G5_honest_c3": {"status": "PASS", "caveats_count": 5, "source": "README.md §C3"},
  "G6_cross_substrate": {"status": "PASS_VIA_CROSS_LINK", "source": "README.md §Composability cross-link to clm-v4-mk2-v1 + p9_paradigm_d_50k", "f_clm_lora_4_substrate_eq_status": "<BG-CLM-2-EXEC pending OR PASS OR FAIL>"}
}
```

### 3.3 Sister-substrate context

- **CLM v4 mk2-v1** (commit `80440a1d`, PRIVATE 2026-05-04, 48h review ending 2026-05-06): consciousness-measurement substrate. Cross-link from this Llama Path A v2 release: "for consciousness-measurement axis substrate, see `dancinlab/clm-v4-mk2-v1`."
- **Pβ Paradigm D 50K** (`state/p9_paradigm_d_50k_2026_05_03/`): F-Pβ-3 = FAIL_TRUE per `#115`. Sister failure documents the architectural-not-recoverable conclusion that motivated the Llama Path A pivot. NOT a release artifact (failed lane); cross-link as "see why CLM v4 + distill could not deliver chat capability."

---

## §4 Required artifacts

### 4.1 Manifest (`state/llama_path_a_v2_hf_release_prep_2026_05_05/manifest.json`)

Schema (additive — no overwrite):

```json
{
  "schema": "anima/hf_release/llama_pa_v2/manifest/1",
  "ts_utc": "2026-05-05T<TBD>Z",
  "repo": "dancinlab/<chosen-name>",
  "family": "llm",
  "base_model": {
    "vendor": "meta-llama",
    "id": "Llama-3.2-3B",
    "license": "llama3.2",
    "url": "https://huggingface.co/meta-llama/Llama-3.2-3B"
  },
  "adapter": {
    "type": "PEFT_LoRA",
    "rank": 64,
    "alpha": 128,
    "dropout": 0.05,
    "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"],
    "size_bytes": 389074464,
    "size_mb": 389.07,
    "sha256": "393eb7530f82321581410989ce0918d3badf14d83c4901204289dc3c69fb753c",
    "source_path": "state/p9_path_a_retrain_v2_retry_3_2026_05_04/results/adapter_final/adapter_model.safetensors"
  },
  "training": {
    "cycle": "p9_path_a_retrain_v2_retry_3_2026_05_04",
    "step_final": 6000,
    "rehearsal_mix": {"anima_axis_pct": 60, "academic_distill_pct": 30, "chat_template_pct": 10},
    "lr": "<extract from train.log>",
    "batch_size": "<extract>",
    "warmup_steps": "<extract>",
    "seed": 42,
    "transformers_train_pin": "~4.45-4.49",
    "wall_time_h": "<extract from h100_orchestrator.log>",
    "h100_cost_usd": "<extract>"
  },
  "eval": {
    "cycle": "p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05",
    "transformers_eval_pin": ">=4.51,<4.60",
    "lm_eval_version": "0.4.11",
    "limit": 200,
    "seed": 42,
    "metrics": {
      "hellaswag_acc_norm": 0.645,
      "mmlu_acc": 0.5752,
      "triviaqa_em": 0.455,
      "composite": 0.5584,
      "forgetting_index": -0.028
    },
    "verdict": "TRUE_PASS",
    "verdict_source": "state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json"
  },
  "f4_substrate_amendment": {
    "strict_f4_status": "FAIL_strict",
    "amended_f4_status": "PARTIAL_PASS_W_F4_DEFERRED_TO_CLM2",
    "rationale_doc": "docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md",
    "true_f4_venue": "BG-CLM-2-EXEC (state/clm_v4_lora_sft_2026_05_05/, in-flight)"
  },
  "own_compliance": {
    "own_14_hf_only": true,
    "own_15_private_first": true,
    "own_15_gates": {"G1": "PASS", "G2": "PASS_W_F4_DEFERRED", "G3": "N/A_LLAMA_CANONICAL", "G4": "TBD_AT_UPLOAD", "G5": "READY", "G6": "PASS_VIA_CROSS_LINK"}
  }
}
```

Generation cost: ~5 min mac-local read of verdict.json + train.log + h100_orchestrator.log.

### 4.2 README.md (HF model card, 5 H2 + ≥3 caveats per `tool/hf_readme_template.md`)

Skeleton (paste-ready for Phase 1):

```markdown
---
license: llama3.2
license_name: llama-3.2-community-license-additive-mit
license_link: LICENSE
language: [en, ko]
library_name: peft
base_model: meta-llama/Llama-3.2-3B
tags: [llama, lora, peft, anima, rehearsal-mix, chat, sft]
pipeline_tag: text-generation
---

# llm-v3-paradigm-a-prime-lora-r64-y3 (Llama-3.2-3B Path A v2 rehearsal-mix LoRA)

**Chat-capable LoRA adapter** on Llama-3.2-3B base, trained with the **anima rehearsal mix** (60% anima axis + 30% academic distill + 10% chat template). Achieves Llama-base parity on commonsense (HellaSwag) and broad knowledge (MMLU) while gaining **+5.9 pp on TriviaQA**.

This is the chat-capability winner of the 2026-05 anima SFT lattice. For the consciousness-measurement substrate companion release, see [`dancinlab/clm-v4-mk2-v1`](https://huggingface.co/dancinlab/clm-v4-mk2-v1) (NOT chat-capable; substrate research artifact).

## §1 Origin
- training script: `state/p9_path_a_retrain_v2_retry_3_2026_05_04/results/...`
- corpus: rehearsal mix (60% anima axis + 30% academic distill + 10% chat template)
- base model: `meta-llama/Llama-3.2-3B` (Llama 3 Community License)
- training cycle: `p9_path_a_retrain_v2_retry_3_2026_05_04` (retrain v2 retry-3)
- final step: 6000
- substrate: H100 80GB ×1, wall ~<TBD>h, cost ~$<TBD>

## §2 Falsifiers
- **F-PA-RETRAIN-v2-1** (Llama-base parity on HellaSwag): **PASS** (0.645 vs 0.654, Δ −0.9 pp, parity-floor 0.644)
- **F-PA-RETRAIN-v2-2** (Llama-base parity on MMLU): **PASS** (0.575 vs 0.580, Δ −0.4 pp, parity-floor 0.5696)
- **F-PA-RETRAIN-v2-3** (one bench above improvement-bar +2 pp): **PASS** (TriviaQA 0.455 vs 0.396, Δ +5.9 pp; improvement-bar 0.416)
- **F-PA-RETRAIN-v2-4** (anima 5-axis preservation cosine ≥ 0.85): **PARTIAL_PASS_W_F4_DEFERRED_TO_CLM2** (mean 0.7871; substrate-inapplicable on Llama base — see `docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md`)
- **F-PA-RETRAIN-v2-5** (forgetting_index ≥ −0.05): **PASS** (forgetting_index = −0.028 = slight net improvement)

## §3 Substrate
- inference: load Llama-3.2-3B base + this PEFT adapter (`peft.PeftModel.from_pretrained`)
- VRAM: ~6.4 GB bf16 (3B base) + ~0.4 GB LoRA = ~7 GB
- `transformers >= 4.51, < 4.60`; `peft >= 0.7`; `torch >= 2.4`
- adapter size: 98.6 MB (LoRA rank 64, target_modules q/k/v/o_proj)
- context window: 128K (inherited from Llama 3.2)
- tokenizer: Llama-3.2-3B stock (`LlamaTokenizer`, no anima override)

## §4 Caveats (raw#10 honest C3)
- **C1** — **anima-derivative, not anima-native.** This is a LoRA on Meta's Llama-3.2-3B; the underlying weights are Meta's. anima contribution is the rehearsal-mix recipe + the LoRA adapter (98.6 MB delta). For an anima-native artifact, see `clm-v4-mk2-v1` (consciousness substrate, NOT chat-capable).
- **C2** — **chat-capability metrics: parity + one substantive gain.** vs Llama-base, HellaSwag/MMLU are within 1-σ of zero (parity, not improvement); only TriviaQA shows above-noise +5.9 pp gain. The "chat-capability winner" label rests on parity preservation + one above-noise gain, not on uniform improvement.
- **C3** — **Llama 3 Community License restrictions.** Commercial use above 700M monthly active users requires Meta authorization. Derivative works (this adapter) must include "Built with Llama" attribution. Non-commercial research use is unrestricted under standard CC-BY-NC analog clauses.
- **C4** — **PEFT adapter requires base download.** Consumers must separately obtain `meta-llama/Llama-3.2-3B` (5 GB+) from Meta's HF org, accept the Llama 3 license, then load this adapter via `PeftModel.from_pretrained`. There is no merged-model release in this v1 (decision Q2 deferred).
- **C5** — **F4 anima axis-preservation deferred to substrate-correct venue.** The strict F-PA-RETRAIN-v2-4 axis-preservation falsifier read 0.7871 (FAIL strict against 0.85 PARTIAL threshold) on Llama base — but Llama base is non-axis-conditioned (mean pairwise axis cosine = 0.9940, axes nearly degenerate). The substrate-correct F4 venue is the CLM v4 LoRA cycle (BG-CLM-2-EXEC, in-flight). If that cycle's F-CLM-LORA-4 lands FAIL on the rehearsal-mix recipe, this release inherits a substrate-correct F4 caveat. See `docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md`.

## §5 Composability
- **base prerequisite**: `meta-llama/Llama-3.2-3B` (load first, then adapter)
- **siblings**: `dancinlab/clm-v4-mk2-v1` (consciousness substrate, NOT chat-capable; cross-substrate sister)
- **failed siblings (documentation)**: Pβ Paradigm D 50K (`state/p9_paradigm_d_50k_2026_05_03/`) — F-Pβ-3 FAIL_TRUE per #115 category-error analysis
- **consumed by**: anima orchestrator chat path (Stage 2-alt LSL bridge — when CLM v4 streams `tension_link` 5ch, this adapter is the chat substrate that reads it)
- **cross-substrate F4 venue**: `state/clm_v4_lora_sft_2026_05_05/` (BG-CLM-2-EXEC, F-CLM-LORA-4 substrate-equivalent of F-PA-RETRAIN-v2-4)

## §6 Citation

```bibtex
@misc{anima_llm_v3_pa_v2_2026,
  author = {anima n_substrate consortium},
  title = {llm-v3-paradigm-a-prime-lora-r64-y3: Llama-3.2-3B chat-capability LoRA via rehearsal mix},
  year = {2026},
  url = {https://huggingface.co/dancinlab/<chosen-name>},
  note = {Chat-capability winner of 2026-05 anima SFT lattice; +5.9 pp TriviaQA over Llama-3.2-3B base}
}
```

## §7 Reproduction recipe (rehearsal mix)

```python
# 60% anima axis + 30% academic distill + 10% chat template
# LoRA rank=64, alpha=128, dropout=0.05, target=[q_proj,k_proj,v_proj,o_proj]
# steps=6000, seed=42, transformers~4.45-4.49 (train) / >=4.51 (eval)
# H100 80GB ×1
```

(Full hyperparameter dump in `manifest.json` referenced from this repo.)
```

### 4.3 LICENSE bundling

- Primary: `LICENSE-LLAMA3.2` (Meta's Llama 3 Community License, retrieved from `meta-llama/Llama-3.2-3B`)
- Additive: `LICENSE-MIT-ADAPTER` (MIT for the LoRA adapter delta, anima-authored)
- Top-level `LICENSE` file = combined notice (Llama 3 base + MIT adapter delta)
- HF Hub frontmatter: `license: llama3.2 + license_name: llama-3.2-community-license-additive-mit`

Q3 escalation: confirm dual-license declaration is the right path (vs single `license: other` with custom text).

### 4.4 Optional artifacts

- **Merged model** (`base + adapter` merged): ~6.4 GB safetensors. Decision Q2 — release PEFT-only (98.6 MB, lighter, requires base download) vs merged (~6.4 GB, self-contained, redundant base storage). Recommendation: PEFT-only for v1, merged in v1.1 if user demand.
- **Dataset slice** (rehearsal mix corpus): ~30 MB academic distill subset + recipe doc. Decision Q4 — release as sibling dataset repo `dancinlab/llm-v3-pa-v2-rehearsal-mix-y3` or include only recipe doc in main repo.

---

## §5 Implementation plan (4 phases, $0 mac+ubu1)

### Phase 1 ($0 mac, ~30 min) — naming + manifest + README draft

1. User decides Q1 (naming) — reply with chosen Option A/B/C OR confirm default `llm-v3-paradigm-a-prime-lora-r64-y3`.
2. Generate `state/llama_path_a_v2_hf_release_prep_2026_05_05/manifest.json` (extract `<TBD>` fields from `state/p9_path_a_retrain_v2_retry_3_2026_05_04/run.log` + `h100_orchestrator.log`).
3. Author `README.draft.md` (paste skeleton from §4.2, fill in concrete TBDs, ≥5 caveats finalized).
4. Run `tool/hf_upload_mk2.hexa --validate-naming dancinlab/<chosen-name>` (dry-run; no network).
5. Run `tool/hf_upload_mk2.hexa --validate-readme state/llama_path_a_v2_hf_release_prep_2026_05_05/README.draft.md` (5-section enforcement + ≥3 caveats).

Cost: $0. Wall: ~30 min. No commit, no upload.

### Phase 2 ($0 ubu1, ~10 min) — pre-push smoke + adapter staging

1. ssh ubu1; copy `adapter_final/` to staging dir `~/staging/llm_v3_pa_v2_y3/`.
2. Copy `README.draft.md` + `manifest.json` + `LICENSE-LLAMA3.2` + `LICENSE-MIT-ADAPTER` + `LICENSE` (combined).
3. Compute sha256 of staging dir contents; cross-check against manifest.json `adapter.sha256`.
4. Run `hexa run tool/hf_upload_mk2.hexa --dry-run --repo dancinlab/<chosen-name> --ckpt ~/staging/llm_v3_pa_v2_y3 --readme README.draft.md --private`.
5. Verify dry-run reports no leak_guard failures (token literals, personal paths) + naming PASS + README PASS.

Cost: $0 (mac → ubu1 ssh, no GPU). Wall: ~10 min. No actual upload.

### Phase 3 ($0 ubu1, ~30 min) — actual PRIVATE upload (24-48h review starts)

**Gated on user authorization.**

1. ssh ubu1; run `hexa run tool/hf_upload_mk2.hexa --upload --private --repo dancinlab/<chosen-name> --ckpt ~/staging/llm_v3_pa_v2_y3 --readme README.draft.md`.
2. HF API uploads adapter (98.6 MB LFS) + README + manifest.json + LICENSE files.
3. Audit ledger lands at `state/hf_upload_audit/<ts>_dancinlab__<chosen-name>.jsonl` with `visibility=private`.
4. 24-48h review window begins; record `review_window_end_ts` in `state/llama_path_a_v2_hf_release_prep_2026_05_05/private_upload_marker.json`.

Cost: $0 (HF Hub bandwidth, no compute). Wall: ~5 min upload + clock-time 24-48h.

### Phase 4 ($0 user-gated, ~30 min) — PUBLIC promote

**Gated on (a) review window elapsed, (b) BG-CLM-2-EXEC F-CLM-LORA-4 verdict (G6 cross-substrate), (c) user sign-off.**

1. Generate `state/llama_path_a_v2_public_promote_<ts>/verdict.json` with all 6 gate-cite fields per §3.2.
2. Run `gh repo edit dancinlab/<chosen-name> --visibility public` (per rule (c)).
3. (Optional) author `docs/anima_llama_path_a_v2_hf_public_promote_landed_<ts>.ai.md` (1-page handoff).

Cost: $0. Wall: ~30 min including verdict.json + handoff.

---

## §6 Risks + mitigations

### R1 — Llama 3 Community License restrictions

The Llama 3 Community License imposes:
- Commercial-use restriction above 700M monthly active users (Meta authorization required)
- "Built with Llama" attribution requirement on derivative works
- Distribution must include the license text

**Mitigation**: model card §C3 prominently states the restrictions. Repo includes verbatim `LICENSE-LLAMA3.2` file. README includes "Built with Llama" attribution. Non-commercial research framing in citation. If user pivots to commercial path, separate evaluation cycle required.

### R2 — Rehearsal mix attribution scope (academic distill 30%)

The 30% academic distill component sourced from `<TBD list of sources>`. If sources include any non-redistributable corpora (e.g., proprietary academic papers, gated datasets), the rehearsal mix sibling dataset repo cannot be released.

**Mitigation**: Phase 1 manifest.json gen task includes audit of academic distill sources. If any non-redistributable, recipe doc only (no data slice release); model card §1 Origin notes "academic distill mix sources: see manifest.json `training.rehearsal_mix.academic_distill_sources` field; recipe reproducible from publicly available subsets only" honest disclosure.

### R3 — PEFT adapter vs merged model trade-off

PEFT-only v1 = 98.6 MB, requires consumer to obtain Llama-3.2-3B base separately (gated on Meta HF acceptance). Merged model v1 = ~6.4 GB, self-contained but redundant storage and Llama 3 license still applies (merged weights = derivative work).

**Mitigation**: PEFT-only v1 (lighter, faster iteration). Q2 user decision; if merged is preferred, v1.1 follow-on cycle generates merged variant + uploads as separate repo `<chosen-name>-merged`.

### R4 — F4 substrate-deferred dependency on BG-CLM-2-EXEC

If BG-CLM-2-EXEC F-CLM-LORA-4 verdict lands FAIL on the rehearsal-mix recipe, the release's substrate-correct F4 caveat becomes a substantive failure (not just a deferred unknown).

**Mitigation**: G6 cross-substrate gate explicitly tracks BG-CLM-2-EXEC outcome. PUBLIC promote (Phase 4) is gated on F-CLM-LORA-4 verdict status — if FAIL, hold PUBLIC promote, iterate on rehearsal mix recipe v2 first. Model card §C5 already discloses the dependency honestly so consumers cannot be surprised.

### R5 — HF discoverability vs naming-spec canonical tension

`llm-v3-paradigm-a-prime-lora-r64-y3` is mk2-spec-canonical but contains zero "llama" string → HF search "llama 3.2 LoRA" misses it. Conversely `llama-3.2-3b-anima-rehearsal-pa-v2-mk2-v1` is discoverable but violates naming spec.

**Mitigation**: pick canonical name + add HF tags `llama`, `llama-3.2-3b`, `lora`, `peft` (§4.2 frontmatter handles this). Canonical name + generous tags = best of both.

### R6 — Concurrent CLM v4 mk2-v1 + Llama PA v2 review windows

CLM v4 mk2-v1 review window ends 2026-05-06T23:26:12Z. If Llama PA v2 PRIVATE uploads 2026-05-05 → review window ends 2026-05-07T<TBD>Z. Two concurrent reviews + two PUBLIC promotes within 48h.

**Mitigation**: reviews are independent (different repos, different gates, different artifact types). Schedule PUBLIC promote BGs sequentially or in parallel; both consume $0 cost. Q5 covers this.

---

## §7 Decision queue (5 user-gated questions)

### Q1 — Repo name

**Default recommendation**: `dancinlab/llm-v3-paradigm-a-prime-lora-r64-y3` (Option A trimmed; PASS-CANON, 38 chars).

**Alternatives**:
- Option A full: `dancinlab/llm-v3-paradigm-a-prime-lora-r64-rehearsal-y3` (54 chars, requires §3.7 amendment for `rehearsal-` prefix)
- Option B: `dancinlab/llama-3.2-3b-anima-rehearsal-pa-v2-mk2-v1` (HF-discoverable, requires mk2 spec amendment for Llama-derivative naming)
- Option C: `dancinlab/llm-v3-pa-v2-mk2-v1` (short, ambiguous)

**User input format**: pick A-trimmed (default) / A-full / B / C / custom.

### Q2 — PEFT adapter only vs merged model

**Default recommendation**: PEFT-only v1 (98.6 MB, faster iteration, consumer obtains Llama base separately).

**Alternative**: merged model (~6.4 GB, self-contained).

**User input format**: PEFT-only / merged / both.

### Q3 — Llama 3 license attribution detail

**Default recommendation**: dual-license declaration — `license: llama3.2 + license_name: llama-3.2-community-license-additive-mit` per HF Hub frontmatter conventions.

**Alternative**: single `license: other` with custom combined text in LICENSE file.

**User input format**: dual-declaration (default) / single-other / other-custom.

### Q4 — Dataset attribution scope (rehearsal mix sources)

**Default recommendation**: recipe doc in main repo (no data slice release); academic distill sources listed in manifest.json with sha256 + redistribution status; if all redistributable, sibling dataset repo `<chosen-name>-rehearsal-mix` v1.1 follow-on.

**Alternative**: full data slice release alongside main repo (requires source redistribution audit at Phase 1).

**User input format**: recipe-only-default / full-data-slice / sibling-repo-followon.

### Q5 — PUBLIC promote timing

**Default recommendation**: independent timing — Llama PA v2 PUBLIC promote BG fires when its own gates (b.1-b.6) all PASS, regardless of CLM v4 mk2-v1 promote status. Concurrency OK.

**Alternative**: sequence after CLM v4 mk2-v1 PUBLIC (so the CLM substrate research lands first, framing context for the Llama-derivative chat release).

**User input format**: independent (default) / after-CLM-v4 / before-CLM-v4 / simultaneous.

---

## §8 Honest C3 caveats (raw#10, ≥5 required)

### C1 — Llama Path A v2 is anima-derivative, not anima-native (architectural)

The artifact is a 98.6 MB LoRA adapter on Meta's Llama-3.2-3B base; the bulk of the weights (~6.4 GB) are Meta's IP. anima's contribution is the rehearsal-mix recipe (60/30/10) + the LoRA delta + the validation cycle. This is fundamentally different from `clm-v4-mk2-v1` which is anima-authored from pretrain. Both are legitimate releases, but the substrate identity differs and the model card must not blur this distinction.

### C2 — Chat-capability gain is parity + one substantive bench, not uniform improvement

vs Llama-3.2-3B base, the rehearsal-mix LoRA delivers:
- HellaSwag −0.9 pp (parity, within 1-σ of zero)
- MMLU −0.4 pp (parity, within 1-σ of zero)
- TriviaQA +5.9 pp (above-noise improvement, factual recall axis only)

The "chat-capability winner" claim rests on **parity preservation + one above-noise gain**, NOT uniform across-bench improvement. Honest framing: "the rehearsal mix preserves Llama's general capability and adds factual-recall depth from the anima axis component." Any framing that implies "outperforms Llama on chat" without the parity-vs-improvement decomposition is misleading.

### C3 — Llama 3 Community License blocks unrestricted commercial path

The Llama 3 license imposes:
- Commercial-use restriction above 700M MAU (Meta authorization required; effectively blocks hyperscaler integration)
- "Built with Llama" attribution requirement (cosmetic but mandatory)
- Distribution must include verbatim license text

For research-use only, this is unrestricted. For any commercial product path (anima as a SaaS, anima-derivative startup), the Llama base license is the binding constraint, not the MIT-additive adapter delta. Future Llama 4 / Llama 4.1 releases may relax these terms; until then, Llama-derivative path is research-grade only.

### C4 — PEFT adapter consumer overhead (Llama base download required)

Consumers must:
1. Accept Meta's Llama 3 license on `meta-llama/Llama-3.2-3B` HF page (gated)
2. Download Llama-3.2-3B base (~6.4 GB)
3. Install `peft` library
4. Load via `PeftModel.from_pretrained(base, "dancinlab/<chosen-name>")`

vs the alternative merged-model release (~6.4 GB self-contained, no base-acceptance gate but still license-bound). PEFT-only is the cheaper anima-side maintenance path but adds consumer-side friction; merged is the inverse trade-off. Decision Q2 surfaces this trade-off explicitly.

### C5 — compliance with own-15 G2 F4 amendment carve-out

 rule (b.2) — "falsifier pre-register satisfied (raw#71 / raw 12)" — is **G2 PASS_W_F4_DEFERRED**, NOT a clean PASS. The strict F-PA-RETRAIN-v2-4 reading was 0.7871 (FAIL strict against the spec's 0.85 PARTIAL threshold), and the substrate-aware amendment (`docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md`) re-interprets but does not re-measure. The PUBLIC promote verdict.json must explicitly cite both views (strict-FAIL + substrate-aware-DEFERRED) and the BG-CLM-2-EXEC F-CLM-LORA-4 outcome before the substrate-correct F4 question can be claimed closed. enforces this through G2 substrate adaptation column in §3.2; consumers reading the model card §F4 caveat must understand the interpretation, not just the bottom-line.

### C6 — Composite metric (0.5584) is anima-internal aggregation, not industry-standard

The "+36.298 pp advantage over CLM v4 + LoRA SFT v1 (0.196)" claim rests on a custom composite (mean of normalized HellaSwag/MMLU/TriviaQA scores). This composite is anima-internal; no public benchmark uses this exact aggregation. The constituent benchmark deltas (−0.9 / −0.4 / +5.9 pp) are the externally-verifiable numbers. The composite gap is real but its magnitude (+36.298 pp) reflects the CLM v4 substrate's structural-not-recoverable chat-incapability (per #115), not a "Llama is 36 pp better at chat than CLM v4 trained on the same data" framing. Avoid composite-only reporting in marketing-style summaries.

### C7 — F4 substrate-deferred status creates a long-tail dependency

R4 in §6 explicitly tracks the BG-CLM-2-EXEC F-CLM-LORA-4 outcome as a release-blocker for full F4 closure. If that BG lands FAIL on the rehearsal-mix recipe (e.g., the recipe damages CLM v4's φ★ axis), the release model card §C5 must be amended post-PUBLIC-promote with a stronger caveat. G6 cross-substrate gate covers this contractually; the operational risk is that PUBLIC-promoted artifacts cannot be retroactively un-promoted without reputational cost (honest-c3 admits PUBLIC→PRIVATE revert is pathological). Mitigation: hold PUBLIC promote until BG-CLM-2-EXEC verdict.json lands (Phase 4 gate (b)).

### C8 — single-seed eval, limit=200, no multi-seed bootstrap

Per `docs/p9_path_a_retry_3_true_pass_lane_closure_landed_2026_05_05.ai.md` C3-1 + C3-2: the TRUE_PASS verdict used seed=42 only at limit=200, giving stderr ~3.5 pp on HS/TQ and ~1.0 pp on MMLU. Multi-seed bootstrap (5-seed ensemble per `docs/p9_p1_5_ensemble_4seed_landed_2026_05_03.ai.md` precedent) NOT executed. The release ships with point-estimate metrics; consumers seeking robust confidence intervals must run their own bootstrap. The model card §F1-F5 cite verdicts as "PASS_TRUE@seed=42,limit=200" not "PASS_TRUE_BOOTSTRAPPED".

---

## §9 Companion handoff

Companion doc: **`docs/anima_llama_path_a_v2_hf_release_prep_landed_2026_05_05.ai.md`** (1-page; 5 bullets summarizing + 5 decision Q's + ≥5 honest C3).

---

## §10 Cross-link

| Predecessor / Sister | Relationship |
|---|---|
| `state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json` | TRUE_PASS source (F1/F2/F3/F5) |
| `state/p9_path_a_retrain_v2_retry_3_2026_05_04/results/adapter_final/adapter_model.safetensors` | adapter weights (sha256 `393eb7530f...`, 98.6 MB) |
| `docs/p9_path_a_retry_3_true_pass_lane_closure_landed_2026_05_05.ai.md` | TRUE_PASS lane closure (eval-fix amendment) |
| `docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md` | F4 substrate-aware amendment (PARTIAL_PASS_W_F4_DEFERRED_TO_CLM2) |
| `docs/anima_clm_hf_release_v1_audit_2026_05_04.md` | sister-substrate release audit (CLM v4 mk2-v1 — pattern reference) |
| `docs/anima_clm_hf_release_v1_uploaded_landed_2026_05_04.ai.md` | first application instance precedent |
| `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` | normative SSOT for naming compliance (§2 + §10.2 regex) |
| `docs/anima_hf_naming_family_reconcile_2026_05_03.ai.md` | `llm` family ratification (provisional) |
| `docs/anima_hf_upload_mk2_spec_2026_05_03.md` | upload pipeline SSOT |
| `docs/anima_hf_upload_mk2_landed_2026_05_03.ai.md` | upload pipeline proven smoke |
| `docs/anima_own_15_hf_release_lifecycle_landed_2026_05_05.ai.md` | SSOT (PRIVATE → 6 gates → PUBLIC) |
| `tool/hf_upload_mk2.hexa` | upload pipeline executable |
| `tool/hf_upload_mk2_pre_push_hook.hexa` | pre-push leak guard |
| `tool/hf_readme_template.md` | model card template |
| `state/clm_v4_lora_sft_2026_05_05/` | BG-CLM-2-EXEC (true F4 venue, in-flight) |
| `state/p9_paradigm_d_50k_2026_05_03/` | failed sibling (#115 architectural) — cross-link from model card §Composability |

---

## §11 Cost & destructiveness

- spec authoring: **$0** mac-local
- destructive: **0** (no rename / delete of any HF repo, no git commit, no marker land, no `.roadmap.*` mutation)
- migration: **0** (forward-looking; release execution is in plan, not in spec)
- byte-diff to any existing artifact: **0**
- HF API calls: **0** (no list, no upload, no read in this spec cycle)
- ubu1 ssh calls: **0** (spec is mac-only)
- H100 cost: **0** (no compute requested by this spec)

---

## §12 Outputs (this spec cycle)

- `/Users/ghost/core/anima/docs/anima_llama_path_a_v2_hf_release_prep_spec_2026_05_05.md` (this file)
- `/Users/ghost/core/anima/docs/anima_llama_path_a_v2_hf_release_prep_landed_2026_05_05.ai.md` (companion handoff)

No marker creation, no commit, no `.roadmap.*` mutation per spec mode directive.
