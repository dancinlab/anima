# P9 A × D Cross-Axis Comparison Spec — Landed 2026-05-03

## TL;DR (handoff)

Pre-registered cross-axis comparison framework for **Path A** (Llama-3.2-3B + LoRA r=64 chat lift via F1_v3) vs **Path D Φ★** (CLM v4 350M + LoRA r=64 Φ★-distill via F1/F2/F3/F-D). Both pipelines complete in next 12-24h. Spec, verdict hexa, marker, handoff all landed; **NO eval triggered** ($0 mac-local design). Run `tool/p9_a_d_cross_axis_verdict.hexa` after both Path A and Path D verdict JSONs land to emit the 4-cell matrix + interpretation paragraph + next-cycle commission text.

---

## 1. What was built

| Artifact | Path | LoC (approx) | Purpose |
|---|---|---|---|
| Spec doc | `docs/p9_a_d_cross_axis_comparison_spec_2026_05_03.md` | ~440 | Pre-registers Q1/Q2/Q3, 4-cell matrix, cross-substrate eval thresholds, hexa contract, 5 honest C3 caveats |
| Verdict hexa | `tool/p9_a_d_cross_axis_verdict.hexa` | ~300 | Reads A + D + optional Q3a/Q3b verdicts, emits 4-cell matrix + interpretation + commission |
| Marker | `state/markers/p9_a_d_cross_axis_spec_landed.marker` | 30 | Silent-land marker (key invariants + thresholds) |
| Handoff | `docs/p9_a_d_cross_axis_spec_landed_2026_05_03.ai.md` (this file) | ~140 | Landing summary + run instructions |

---

## 2. 4-cell matrix (verbatim from spec §2)

| | **D = SUCCESS_D / PARTIAL_D** | **D = FAIL_D** |
|---|---|---|
| **A = CHAT_PASS_v3** | **Cell I — BOTH_AXES_LIVE** | **Cell II — CHAT_LIVE_ONLY** |
| **A = CHAT_PARTIAL_v3 / CHAT_FAIL_v3** | **Cell III — PHI_LIVE_ONLY** | **Cell IV — BOTH_NOISE** |

**+UNDETERMINED** fallback when one or both verdict inputs missing/parse_error/empty (n_ckpts=0).

**Per-cell next-cycle commission** (one-paragraph each):
- **Cell I**: A∪D additive cycle ($300-600 ceiling).
- **Cell II**: ship Path A; commission Path D root-cause cycle ($0-50 ceiling).
- **Cell III**: ship Path D; commission Path A debug cycle ($50-150 ceiling).
- **Cell IV**: NO further LoRA training; commission paradigm-rethink ablation ($100-200 ceiling).

---

## 3. Cross-substrate exploratory eval thresholds (Q3a, Q3b)

These are **EXPLORATORY DIAGNOSTICS, NOT pre-registered F-axis falsifiers** (C3 caveat (b)).

### Q3a — Path A LoRA Φ★ on Llama hidden states

| Classification | `relative_delta = (Φ★_LoRA - Φ★_base) / |Φ★_base|` | Interpretation |
|---|---|---|
| **PASS** | `≥ -0.10` | Chat-tuning preserves Φ★ axis (within 10% of Llama base) |
| **MARGINAL** | `-0.30 ≤ x < -0.10` | Chat-tuning erodes Φ★ but no inversion |
| **FAIL** | `< -0.30` OR sign flip | Chat-tuning destroys Φ★ axis |

**Procedure**: 200-prompt probe, layer L=14 (mid-layer of Llama-3.2-3B's 28 layers), `anima_phi_v3_canonical` formula (HID_TRUNC=8, K=8, ridge=1e-3). Bootstrap N=1000.

### Q3b — Path D LoRA HellaSwag on CLM v4

| Classification | `delta_acc_norm = acc_LoRA - acc_base` | Interpretation |
|---|---|---|
| **EXPECTED** | `|x| ≤ 0.02` (LoRA stays near floor 0.242 ± 0.02) | Distill is chat-orthogonal as designed |
| **UNEXPECTED_LIFT** | `> +0.02` | Distill incidentally improves chat (mechanistic anomaly) |
| **UNEXPECTED_REGRESSION** | `< -0.02` | Distill destroys chat (integrity check needed) |

**Procedure**: lm-eval-harness HellaSwag `--limit 500` (matches A' base validation precision). Bootstrap N=1000. Skipped if CLM v4 loader bug (per A' §1.2) not yet fixed.

---

## 4. Verdict hexa contract (`tool/p9_a_d_cross_axis_verdict.hexa`)

### Inputs (env vars)

| Env var | Default |
|---|---|
| `ANIMA_PATH_A_VERDICT` | `state/p9_a_prime_main_eval_2026_05_03_verdict.json` |
| `ANIMA_PATH_D_VERDICT` | `state/p9_paradigm_d_25k_eval_2026_05_03_verdict.json` |
| `ANIMA_Q3A_RESULT` | `state/p9_a_d_cross_axis_2026_05_03/q3a_path_a_phi_star.json` (optional) |
| `ANIMA_Q3B_RESULT` | `state/p9_a_d_cross_axis_2026_05_03/q3b_path_d_chat.json` (optional) |
| `ANIMA_OUTPUT` | `state/p9_a_d_cross_axis_2026_05_03/cross_axis_verdict.json` |
| `ANIMA_BOOT_N` | `1000` |

**Reads-only**: hexa never mutates A or D verdict JSONs.

### Self-test

```
hexa run tool/p9_a_d_cross_axis_verdict.hexa --selftest
```

Emits 16 invariants: `n_research_questions=3`, `n_matrix_cells=4`, `n_cross_substrate_evals=2`, `n_honest_c3=5`, `bootstrap_default_n=1000`, plus per-threshold values + schema names + non-mutation flag.

### Run

```
hexa run tool/p9_a_d_cross_axis_verdict.hexa
```

Emits `state/p9_a_d_cross_axis_2026_05_03/cross_axis_verdict.json` (schema `anima/p9_a_d_cross_axis/verdict/1`) with:
- `path_a_summary`: best ckpt F1_v3 verdict
- `path_d_summary`: best ckpt 4-falsifier verdict + F2 floor breach flag
- `q3a_summary` / `q3b_summary`: classification + delta + CI95 bounds (or UNAVAILABLE)
- `matrix_cell`: I/II/III/IV/UNDETERMINED
- `interpretation_paragraph`: auto-composed 4-6 sentence narrative + Q3 clauses
- `next_cycle_commission`: per-cell commission text
- `honest_c3`: 5 caveats

---

## 5. Order of operations (next 12-24h)

1. **Path A**: LoRA training pod completes → eval cycle runs `tool/p9_a_prime_verdict.hexa` → `state/p9_a_prime_main_eval_2026_05_03_verdict.json` populated.
2. **Path D**: 25K distill completes → eval cycle runs `tool/p9_paradigm_d_verdict.hexa` → `state/p9_paradigm_d_25k_eval_2026_05_03_verdict.json` populated.
3. **(Optional) Q3a**: commission Path A LoRA Φ★ probe on Llama (200 prompts, layer 14, ~30-45 min ubu1 $0).
4. **(Optional) Q3b**: commission Path D LoRA HellaSwag on CLM v4 (limit 500, ~20-30 min ubu1 $0; subject to loader fix).
5. **Cross-axis verdict**: `hexa run tool/p9_a_d_cross_axis_verdict.hexa` → `state/p9_a_d_cross_axis_2026_05_03/cross_axis_verdict.json`.
6. **Land cycle**: emit `docs/p9_a_d_cross_axis_landed_2026_05_<DD>.ai.md` + `state/markers/p9_a_d_cross_axis_landed.marker` (separate land cycle, NOT this spec land).

**Critical sequencing**: this spec is locked-in BEFORE step 5 → verdict synthesis logic is **pre-registered**, not designed post-hoc to fit observed data.

---

## 6. 5 honest C3 caveats (raw#10, full text in spec §10)

(a) **Different bases produce different baselines** — Llama-3.2-3B vs CLM v4 350M; cell labels are per-axis verdicts on native substrates, NOT head-to-head capability comparisons.

(b) **Q3a/Q3b are EXPLORATORY, NOT pre-registered F-axis falsifiers** — first-cycle heuristic thresholds; use as diagnostic context for the interpretation paragraph, NOT as additional pass/fail axes.

(c) **Verdict synthesis depends on both BG cycles completing** — partial completion → UNDETERMINED cell. Do NOT substitute earlier ckpts (e.g. Path A 5K instead of 50K, Path D step_1000 mini-run instead of 25K) — comparison spec locked to final verdict identities.

(d) **Φ★ formula calibrated against CLM v4** (anchor Φ★ ≈ 41.86); Llama Φ★ values NOT comparable to CLM v4 Φ★ values. Q3a's `relative_delta` is within-Llama-substrate only.

(e) **Bootstrap N=1000 over 200/500-prompt sets is direction-only signal**, not precise effect size. Future cycle wanting tight CIs should use N=10000 over 1-2K prompts ($0 ubu1, +1-2h wall).

---

## 7. Cost / destructive ops

| Item | Value |
|---|---|
| $-cost (this cycle, spec land) | **$0 mac-local** |
| $-cost (next cycle, verdict synthesis run) | $0 (~5 sec wall) |
| $-cost (Q3a + Q3b optional evals) | $0 ubu1 (~50-75 min wall total) |
| Destructive ops | 0 |
| Migrations | 0 |
| Files added | 4 (spec + hexa + marker + handoff) |
| Files modified | 0 (no in-place edits to existing SSOT) |

---

## 8. Validation

- ✅ Spec doc written (~440 LoC, all 11 sections per pre-registration discipline).
- ✅ Verdict hexa written (~300 LoC, raw#9 strict Mac hexa, emits Python helper to `/tmp/...py_tmp` per raw#37).
- ✅ Marker emitted (30 lines, key invariants + thresholds).
- ✅ Handoff doc emitted (this file).
- ⚠️ Hexa selftest NOT executed in this cycle (no `hexa` binary invocation; spec-only land per task constraint). Selftest validates 16 invariants when run; recommended as first action of next cycle.

---

## 9. Cross-references

- `docs/p9_a_prime_path_decision_2026_05_03.md` §6.1 (anchor swap to Llama base).
- `docs/p9_a_prime_path_decision_2026_05_03.md` §6.2 (Path D substrate = CLM v4 350M).
- `docs/p9_paradigm_d_distillation_runbook_2026_05_03.md` §4 (F1/F2/F3/F-D thresholds).
- `tool/p9_a_prime_verdict.hexa` (F1_v3 chat verdict producer).
- `tool/p9_paradigm_d_verdict.hexa` (4-falsifier Φ★ verdict producer).
- `docs/p9_a_prime_eval_pipeline_landed_2026_05_03.ai.md` (Path A eval pipeline ready).

---

## 10. Next cycle handoff (paste-once)

> Run cross-axis verdict synthesis. Path A and Path D 25K verdicts should both be present at:
> - `state/p9_a_prime_main_eval_2026_05_03_verdict.json`
> - `state/p9_paradigm_d_25k_eval_2026_05_03_verdict.json`
>
> Step 1: `hexa run tool/p9_a_d_cross_axis_verdict.hexa --selftest` — verify 16 invariants emit cleanly.
>
> Step 2: `hexa run tool/p9_a_d_cross_axis_verdict.hexa` — emits `state/p9_a_d_cross_axis_2026_05_03/cross_axis_verdict.json`.
>
> Step 3: read `matrix_cell` + `interpretation_paragraph` + `next_cycle_commission` fields. If `cell == "UNDETERMINED"`, the inputs aren't both ready — re-run after Path A and Path D verdicts both land. Do NOT substitute earlier ckpt verdicts.
>
> Step 4 (optional): commission Q3a (Llama Φ★ probe, ~30-45 min ubu1 $0) and/or Q3b (CLM v4 HellaSwag eval, ~20-30 min ubu1 $0; skipped if loader bug). Re-run hexa with `ANIMA_Q3A_RESULT` / `ANIMA_Q3B_RESULT` env vars.
>
> Step 5: emit `docs/p9_a_d_cross_axis_landed_2026_05_<DD>.ai.md` + `state/markers/p9_a_d_cross_axis_landed.marker` (separate land cycle; commit message: "feat(p9 cross-axis land): A x D 4-cell matrix verdict + Q3 cross-substrate diagnostics").
>
> Constraints: raw#9 STRICT (Mac → hexa only; no .py creation), raw#15, raw#10. $0 mac-local.

---

**End of handoff** (raw#9 STRICT / raw#15 SSOT / raw#10 honest C3 §6 / $0 mac-local design only — no eval triggered).
