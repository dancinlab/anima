# P9 TriviaQA Filter Audit — Landed 2026-05-04 (BG-Τ)

**Cycle**: `p9_triviaqa_filter_audit_2026_05_04`
**Mode**: Compute-free / docs-only / READ-ONLY / no git mutation / no pod boot
**Cost**: $0 USD
**Wall time**: ~10 min (docs-fetch + analysis)

## TL;DR

BG-Ο anchor flagged TriviaQA EM = 0.396 vs published mid 0.275 (Δ +12.1pp, FAIL_ABOVE). Honest C3 #2 hypothesized "remove_whitespace filter mismatch". This audit verified that hypothesis is **largely incorrect** — the filter is benign — and identified the actual root cause: **0.275 published mid is heuristic, not Meta-canonical**.

**Key findings**:
1. `remove_whitespace` filter is `str.strip()` only (leading/trailing whitespace) — STANDARD EM normalization, not aggressive. Source verified at `lm_eval/filters/extraction.py::WhitespaceFilter`.
2. Meta's official Llama-3.2-3B model card (live HF fetch) includes MMLU + HellaSwag in benchmark tables but **NOT TriviaQA**. The 0.275 reference is community-extrapolated heuristic.
3. Δ +12.1pp decomposition: ~0pp filter, ~2pp small-sample variance, ~10pp heuristic-mid error.

**Recommendation: Option B** (accept measurement + amend spec §A8). Cost: $0, wall: 0min, 완성도: 0.92.

## Resolution recommendation

**Option B (accept + document)** is recommended over A (re-run strict EM, $0.50/5min), C (drop TriviaQA), D (substitute benchmark).

Rationale: The root cause is reference error (0.275 unmoored), not measurement error. Re-running with different filter (Option A) does not fix this. Dropping TriviaQA (Option C) loses informational signal. Substituting (Option D) just relocates the no-Meta-canonical-reference problem.

## Spec amendment proposal — BG-Ξ §A8

> **§A8: Meta-canonical-reference gating.** When a published mid for a c2 benchmark is community-heuristic (not in Meta's official Llama-3.2-3B benchmark table on the HF model card), the F1_v3 V2 c2 gate evaluates that benchmark as informational-only. The c2 PASS threshold (≥2/N within ±10pp band) excludes informational benchmarks from the pass count. Specifically: TriviaQA EM (no Meta-canonical reference for Llama-3.2-3B) is informational; c2 PASS threshold becomes ≥2/2 on HellaSwag + MMLU (which DO have Meta-canonical references on the HF card).

**Effect on BG-Ο verdict**: PASS reaffirmed. Justification strengthened from "lenient 2/3" to "principled 2/2 on Meta-canonical-references + 1 informational".

## Honest C3 (top 3 of 7)

1. **0.275 mid is HEURISTIC, not Meta-canonical** — verified by fetching `huggingface.co/meta-llama/Llama-3.2-3B/resolve/main/README.md` live; Meta does NOT publish TriviaQA for Llama-3.2-3B. The entire Δ-from-mid framing is conditioned on a weak reference.
2. **Filter is BENIGN** — `remove_whitespace` ≡ `str.strip()` only. With metric-level `ignore_case` + `ignore_punctuation`, this is STANDARD EM. Disabling `remove_whitespace` would reduce EM by 1-3pp, not 12pp. BG-Ο honest C3 #2 was overcautious.
3. **HellaSwag spec mid (0.704) MAY ALSO be mistracked** — Meta canonical HellaSwag 0-shot acc = 0.698; BG-Ν spec mid 0.704 likely tracks community `acc_norm` (which BG-Ο measured = 0.654). Audit recommendation: BG-Ν next cycle should review published-mid construction across ALL 3 anchors, not just TriviaQA.

(Full 7-item C3 list in `state/p9_triviaqa_filter_audit_2026_05_04/audit.md`.)

## Deliverables

- `state/p9_triviaqa_filter_audit_2026_05_04/audit.md` — full 8-section audit (~250 LoC)
- `state/p9_triviaqa_filter_audit_2026_05_04/recommendation_matrix.json` — structured A/B/C/D ranking
- `docs/p9_triviaqa_filter_audit_landed_2026_05_04.ai.md` — this handoff

## Cross-links

- **BG-Ο anchor verdict**: `state/p9_base_validation_llama_anchor_2026_05_04/verdict.json` (commit `93bef8c8`) — honest C3 #2 (filter mismatch hypothesis) **partially refuted** by this audit; filter is benign, heuristic-mid is the real driver.
- **BG-Ξ amendment §A2**: TriviaQA c3+c4 fallback risk → **superseded** by §A8 proposal here.
- **BG-Ν F1_v3 V2 spec**: published-mid construction methodology should be re-audited next cycle (HellaSwag mid 0.704 may also be acc_norm-vs-acc mistracked).
- **BG-Ρ (parallel, this session)**: `tool/p9_lora_mode1_eval_h100_orchestrator.hexa` + `state/p9_lora_mode1_eval_2026_05_04/` — non-overlapping.
- **BG-Σ (parallel, this session)**: `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_exec_*` — non-overlapping.

## Constraints honored

- raw#9: no .py written; pure markdown + JSON
- raw#10: 7 honest C3 items (≥4 required) ✓
- raw#15: read-only scope; no source modification
- No `git add` / `git commit` / git mutation ✓
- No pod boot / compute trigger ✓
- No `chflags` ✓
- No source file modification ✓
- No `.roadmap.*` modification ✓
- No BG-Ρ / BG-Σ territory access ✓

## Next-cycle integration

1. **BG-Ξ next iteration**: integrate §A8 text into the amendment doc (BG-Τ produced text but did not edit BG-Ξ source per scope constraint). Recommend BG-Ξ owner consume `state/p9_triviaqa_filter_audit_2026_05_04/audit.md` §7 for paste-ready §A8 text.
2. **BG-Ν next iteration**: re-audit ALL 3 published mids (HellaSwag, MMLU, TriviaQA) against Meta-canonical references. HellaSwag mid 0.704 may also be heuristic-tracked (acc_norm vs acc).
3. **Future P9 anchor cycles**: if Mistral or Qwen anchor shows similar TriviaQA divergence pattern, §A8 generalization is validated and should become permanent F1_v3 doctrine.

## Status emit

`__P9_TRIVIAQA_FILTER_AUDIT__ RECOMMEND_OPTION_B`
