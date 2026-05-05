---
title: "anima `.roadmap.p9_sft` CLM v4 LoRA SFT lane closure annotation — APPLIED"
status: APPLIED — CLM_2_LANE_4_OF_5_PASS_PENDING_F2
ts_utc: 2026-05-05
cycle: 2026-05-05
artifact_kind: ai_landed_handoff
ssot_path: .roadmap.p9_sft
mutation_kind: additive_only_new_sibling_cond_entry
applied_by: BG-LANE-CLOSURE-APPLY
spec_source: docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md (§3.2 Option A)
companion_amendment: docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md
verdict_sources:
  - state/clm_v4_lora_sft_2026_05_05/verdict.json
  - state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json
  - state/clm_v4_lora_4_axis_remeasure_2026_05_05/verdict.json
new_cond_id: p9_sft.cond.clm_v4_lora_sft_2026_05_05
lane_status: CLM_2_LANE_4_OF_5_PASS_PENDING_F2_VIA_MMLU_TQ
git_commit: NONE (per BG-LANE-CLOSURE-APPLY directive — $0 SSOT mutation, no commit)
---

# anima `.roadmap.p9_sft` CLM v4 LoRA SFT lane closure annotation — APPLIED

This handoff documents the application of Option A from `docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md` §3.2 — the addition of a new sibling cond entry `p9_sft.cond.clm_v4_lora_sft_2026_05_05` to the `.roadmap.p9_sft` JSONL SSOT, carrying the official 4-of-5 PASS lane closure annotation for the BG-CLM-2-EXEC LoRA SFT lane on the CLM v4 530M substrate.

## 1. What was applied

A new `type=entry, kind=cond` line was appended as line 6 of `.roadmap.p9_sft` with id `p9_sft.cond.clm_v4_lora_sft_2026_05_05`. The entry carries:

- Standard cond wrapper (title, desc, status, substrates, source, cycle, contributes_to, verifier, evidence, predecessor, ts).
- A nested `lane_closure_2026_05_05` annotation payload mirroring the spec from BG-CLM-2-LANE-AMEND with all five falsifier outcomes (`amended_F-CLM-LORA-1` PASS_TRUE, `F-CLM-LORA-2` INCONCLUSIVE_PARTIAL_DATA pending BG-CLM-2-MMLU-TQ-EVAL, `F-CLM-LORA-3` PASS, `amended_F-CLM-LORA-4` PASS_VIA_PART_A_ONLY, `F-CLM-LORA-5` PASS), `lane_status="CLM_2_LANE_4_OF_5_PASS_PENDING_F2_VIA_MMLU_TQ"`, and the supersession marker for the predecessor F4 strict FAIL via locus-architectural remeasure rationale.
- Explicit `additive_only_mutation: true`, `semantics_preserved: true`, `historical_evidence_preserved: true` flags both at the entry and annotation level.

## 2. Verification recipe (all PASS)

```bash
# 1. JSONL parses
while IFS= read -r line; do case "$line" in '#'*|'') continue;; esac; \
  echo "$line" | jq -e . >/dev/null || { echo FAIL; exit 1; }; done < .roadmap.p9_sft
# -> JSONL OK (all 4 JSON entries parse: header + paradigm_d_distill + path_a_lora_train_complete + clm_v4_lora_sft_2026_05_05)

# 2. New cond present + annotation correct
sed -n '6p' .roadmap.p9_sft | \
  jq -e '.id=="p9_sft.cond.clm_v4_lora_sft_2026_05_05" and .lane_closure_2026_05_05.lane_status=="CLM_2_LANE_4_OF_5_PASS_PENDING_F2_VIA_MMLU_TQ"'
# -> true

# 3. Sibling preservation (lines 1-5 byte-identical to pre-state)
diff <(sed -n '1,5p' /tmp/roadmap_p9_sft_pre.bak) <(sed -n '1,5p' .roadmap.p9_sft)
# -> empty (identical)

# 4. Line count grew exactly 1 (5 → 6)
wc -l .roadmap.p9_sft  # -> 6
```

Pre/post sha256 audit confirmed line 3 (header), line 4 (`paradigm_d_distill`), and line 5 (`path_a_lora_train_complete`) byte-identical pre-mutation vs post-mutation. The mutation is strictly additive (one new tail line); no existing line was rewritten.

## 3. Five honest C3 caveats (raw#10)

1. **C3-1 — header `required_conditions` array UNCHANGED**. The header on line 3 carries a separate `required_conditions: [...]` array (5 entries: `cond.1`, `cond.2`, `cond.3`, `benchmark_a_prime_spec`, `benchmark_a_prime_base_validation`). Following the additive precedent of `paradigm_d_distill` and `path_a_lora_train_complete` (both standalone entry-line conds NOT registered in the header array), the new `clm_v4_lora_sft_2026_05_05` cond was added ONLY as a JSONL entry line and was NOT registered in the header's `required_conditions`. If lane-roll-up tooling scans the header array (rather than the entry-line list), this cond will not surface there. This matches the existing precedent — verification or roll-up against the JSONL entry stream is required.
2. **C3-2 — F-CLM-LORA-2 INCONCLUSIVE blocks lane "5-of-5"**. The lane is annotated `partial_pass_pending_f2_finalize`, NOT closed. F-CLM-LORA-2 (Anima vs Llama LoRA C-CLM-LORA-2 differentiator) is INCONCLUSIVE_PARTIAL_DATA pending BG-CLM-2-MMLU-TQ-EVAL completion. The "4-of-5 PASS" framing is structurally honest about the open falsifier; this annotation must be revisited once F2 finalizes (PASS or FAIL).
3. **C3-3 — F-CLM-LORA-4 amendment supersedes strict re-measure FAIL**. The 4-axis re-measure at `state/clm_v4_lora_4_axis_remeasure_2026_05_05/verdict.json` returned FAIL on the strict criterion. The amendment in `docs/clm_v4_lora_sft_f4_amendment_2026_05_05.md` invokes a locus-architectural moot rationale to declare PASS via Part A only (3/3 bridge fixture). The annotation flags `supersedes_predecessor_F4_strict_FAIL_via_locus_remeasure: true` and preserves the FAIL verdict in evidence. This is structurally an amendment (not new measurement), and reviewers downstream must verify the locus-architectural rationale is acceptable before treating the lane as 5-of-5 PASS once F2 lands.
4. **C3-4 — verdict + status copy are derived, not re-measured**. The annotation re-states falsifier outcomes from the source verdicts (`clm_v4_lora_sft_2026_05_05`, `clm_v4_lora_phi_canonical_2026_05_05`, `clm_v4_lora_4_axis_remeasure_2026_05_05`) without re-running any falsifier. The drift figure (-4.46pp), forgetting_index (0.0196), adapter size (10.02 MB), and the Part A 3/3 fixture PASS are all transcribed from upstream artifacts; downstream consumers should re-verify against the cited verdict JSONs if doubt arises about transcription fidelity.
5. **C3-5 — `lane_closure_2026_05_05` schema is ad-hoc**. The annotation payload nested under `lane_closure_2026_05_05` is not formally schematized in any roadmap-mk2 spec. Field names mirror the BG-CLM-2-LANE-AMEND proposal verbatim. If a future cycle introduces a canonical lane-closure annotation schema, this entry will need a structural migration; for now the field is opaque to generic mk2 readers and must be parsed by lane-aware consumers only.
6. **C3-6 — no git commit performed**. Per BG-LANE-CLOSURE-APPLY directive, the working tree was mutated but NO `git commit` was executed. The cond entry is on disk only; downstream cycles or a follow-up commit BG must persist this to git. The companion handoff doc itself is also untracked at write time.

## 4. Pending downstream work

- **BG-CLM-2-MMLU-TQ-EVAL**: must complete to finalize F-CLM-LORA-2 (PASS or FAIL). On F2 PASS, this cond's `status` should be amended to `pass_5_of_5` and `lane_status` to `CLM_2_LANE_5_OF_5_PASS`. On F2 FAIL, `lane_status` should reflect `CLM_2_LANE_F2_FAIL`. Either way, the additive precedent should be preserved (new amendment field, not mutation of `lane_closure_2026_05_05`).
- **Sibling cycle BLM phase 5 / EEG B-track**: unaffected by this mutation (different domain SSOTs).
- **Git commit**: separate BG (or user-initiated `/commit` cycle) needed to persist `.roadmap.p9_sft` line 6 + this handoff doc to git.

## 5. Spec ↔ apply linkage

| Spec field (closure doc §3.2 Option A) | Applied location |
| --- | --- |
| `id: p9_sft.cond.clm_v4_lora_sft_2026_05_05` | `.roadmap.p9_sft` line 6 `.id` |
| `type: entry, kind: cond` | line 6 `.type`, `.kind` |
| `verifier.manual_override_path` | line 6 `.verifier.manual_override_path` |
| `evidence[]` (4 verdict JSONs + closure doc + adapter sha256) | line 6 `.evidence[]` |
| `lane_closure_2026_05_05.{...}` (15 fields per BG-CLM-2-LANE-AMEND) | line 6 `.lane_closure_2026_05_05.*` |
| `predecessor: [clm.cond.1, clm.cond.2, p9_sft.cond.3, p9_sft.cond.path_a_lora_train_complete]` | line 6 `.predecessor` |

All spec fields applied verbatim modulo merge with the user-specified `lane_closure_2026_05_05` annotation payload.
