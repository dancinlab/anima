# anima CLM v4 HF release v1 — model card S3 update landed (2026-05-05)

Companion handoff for the BG-HF-V1-MODELCARD-S3-UPDATE cycle. The HF v1
release model card surface (anima draft + ubu1 staging mirror + sister
sync source) was strengthened with empirical chat-capability falsification
evidence from two independent training cycles. This is an **additive**
documentation update — no HF Hub push, no git commit, no `.own` mutation.

## Summary (5 bullets)

- **Part A — README empirical falsification block**: Added new
  `## Empirical chat-capability falsification (2026-05-05)` section (after
  Caveats C6, before Composability) to both
  `docs/anima_clm_hf_release_v1_README_draft.md` and
  `state/clm_v4_hf_release_v1_upload_stage_2026_05_04/README.md`. The
  block documents Cycle 1 (Pβ Paradigm D 50K F-Pβ-3 FAIL_TRUE composite
  0.01176 RED) + Cycle 2 (CLM v4 LoRA SFT v1 F-CLM-LORA-2
  FAIL_REGRESSION_VS_LLAMA composite 0.19542 delta -36.298pp), substrate
  safety preserved (forgetting_index 0.0196 + φ★ NO_FLIP -4.46pp drift),
  architectural conclusion per #115, and explicit IS-FOR / NOT-FOR lists.
- **Part B — manifest.json evidence trail**: Added top-level
  `empirical_chat_capability_falsification_2026_05_05` field to
  `state/clm_v4_hf_release_v1_manifest_2026_05_04/manifest.json` with
  `two_cycle_evidence` array (paradigm_d_pbeta_50k +
  clm_v4_lora_sft_v1 entries with verdict_path / f_verdict / composite /
  band+delta), `substrate_safety_evidence` block (forgetting_index 0.0196
  + phi_star_drift_pp -4.46 + phi_star_no_flip + f_clm_lora_1_pass true),
  `chat_capability_winner` cross-link to Llama Path A v2 TRUE_PASS, and
  `intended_use_disclosure` ("consciousness-substrate research artifact
  only, NOT chat-capable"). JSON validated `python -m json.tool` clean —
  23 top-level keys, 2 cycle entries.
- **Part C — docs/modules/clm.md sister doc sync**: Added the same
  empirical falsification block (Cycle 1 + Cycle 2 + substrate safety +
  architectural conclusion + IS-FOR / NOT-FOR) after Caveats C9 and
  before References, with an additional closing paragraph anchoring the
  block as the empirical-evidence amendment to C1 (#115 architectural
  disclosure) and C2 (F1_score_v2 RED-band) caveats. SSOT-side narrative
  preserved; HF README sync source kept consistent with the downstream
  README surface for any future hash-based drift detection.
- **Part D — own 15 G5 evidence amendment proposal**: own 15 verification
  gate G5 (honest C3 model card with chat-incapability disclosure) is
  strengthened from architectural-disclosure-only to architectural +
  empirical-two-cycle-evidence. The amendment is **proposed only** in this
  doc — `.own` is not mutated by this BG cycle. Public promote command
  remains unchanged because the model card update is additive disclosure
  (raw#15 additive convention); promote at the 2026-05-06T23:26:12Z
  review window can carry this strengthened model card surface.
- **Part E — public promote readiness**: All four edited surfaces (anima
  draft README, ubu1 staging mirror README, manifest.json, modules/clm.md
  SSOT) now carry the same two-cycle empirical evidence with consistent
  numbers (composite 0.01176 / 0.19542, delta -36.298pp, drift -4.46pp,
  forgetting 0.0196). own 15 G5 strengthened; promote can fire at the
  review window with strengthened model card. No HF Hub push performed in
  this cycle (staging mirror is the truth surface; HF Hub gets the README
  via the next promote cycle's `tool/hf_upload_mk2.hexa --readme` flag).

## Honest C3 (≥5)

- **C1 — additive-only edit, no replacement of prior caveats**: Existing
  C1-C6 architectural disclosure block is unchanged; the new empirical
  block sits between Caveats and Composability as a new top-level section.
  This preserves diff-readability and makes the empirical-vs-architectural
  evidence trail explicit. Future cycles can collapse the two into a
  single "C1 — chat-incapability (architectural + empirical)" caveat
  during a v1.1 audit pass.
- **C2 — manifest evidence_trail is post-hoc, not training-time**: The
  `empirical_chat_capability_falsification_2026_05_05` block was authored
  on 2026-05-05 from already-landed verdict JSONs. It is a *cross-link
  index* into the verdict files, not a re-derivation. Source-of-truth
  remains the verdict JSONs themselves; the manifest field is a
  navigation aid for downstream consumers (HF model card readers,
  researchers) who want a single composite evidence digest.
- **C3 — gen_str degenerate-output examples (`....`, `''''`,
  `not ground To at at의의uld`) are illustrative carry from the F-Pβ-3
  per-prompt JSONL** — they were quoted in the BG-HF-V1-MODELCARD-S3
  spec, not re-extracted in this cycle. Future cycle can verify
  per_prompt.jsonl idx=0,1,2 if exact quotation precision is needed for
  publication-grade citation.
- **C4 — Cycle 1 and Cycle 2 use different LoRA topologies and substrate
  paths**: Pβ used r=64 a=128 with mlp gate/up/down on
  ConsciousDecoderV2 + best.pt + ubu1 GPU bf16; CLM v4 LoRA SFT v1 used
  r=32 a=64 qkvo-only on HF-format mk2-v1 + Mac CPU fp32. Both fail
  chat-capability lift; cross-substrate-path consistency strengthens the
  architectural conclusion (the failure is not a topology / substrate-path
  artifact). Honest C3 from the source verdicts.
- **C5 — Llama Path A v2 cross-link is single-cycle, not 5-seed
  ensembled**: The `chat_capability_winner` field cites the v2 retry-3
  rerun verdict (single-seed). Path A v2 5-seed ensemble (when landed)
  will replace the single-cycle anchor; for now, single-cycle is the
  best available chat-capability winner reference.
- **C6 — public promote command is unchanged**: Per raw#15 additive
  convention, the README update does NOT trigger a re-validation of any
  of the F-CLM-RELEASE-1/2/3 falsifiers, F-SHIM-V4-1/2/3/4 shim integrity,
  or the manifest's existing 11-honest-C3 list. Promote runbook
  (`docs/anima_clm_hf_release_v1_plan_2026_05_04.md` §1 step 7-10) fires
  at the 2026-05-06T23:26:12Z review window with the strengthened model
  card surface, not delayed.

## Files touched

- `docs/anima_clm_hf_release_v1_README_draft.md` (anima draft README)
- `state/clm_v4_hf_release_v1_upload_stage_2026_05_04/README.md` (ubu1 staging mirror)
- `state/clm_v4_hf_release_v1_manifest_2026_05_04/manifest.json`
- `docs/modules/clm.md` (sister doc / sync source)

## What this BG did NOT do (CRITICAL boundaries respected)

- did NOT git commit
- did NOT push to HF Hub (model card update is staging-only; actual HF
  Hub README sync happens at promote-time via
  `tool/hf_upload_mk2.hexa --readme docs/modules/clm.md`)
- did NOT mutate `.own` (G5 strengthening is proposal only; landing is
  reserved for an explicit own-amendment cycle)
- did NOT regenerate verdict JSONs (Cycle 1 + Cycle 2 verdicts already
  landed by sibling BGs; this cycle only cross-links them)

## Promote-time checklist (forward-looking)

When the 2026-05-06T23:26:12Z review window opens:

- run `tool/hf_upload_mk2.hexa --upload --public --repo
  dancinlab/clm-v4-mk2-v1 --readme
  state/clm_v4_hf_release_v1_upload_stage_2026_05_04/README.md` (or
  `--readme docs/modules/clm.md` if SSOT-source surface is preferred)
- the README pushed will carry the new
  `## Empirical chat-capability falsification (2026-05-05)` section
- `.roadmap.clm` cond.2 PASS landing per
  `docs/anima_clm_hf_release_v1_plan_2026_05_04.md` §1 step 10
- own 15 G5 amendment landing (separate cycle, single-line `.own` edit)
