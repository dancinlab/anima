# Commit Note — fe1e3d09 unintended scope (2026-05-07)

## What this note is for

Clarifies the actual scope of anima commit **fe1e3d09** (`refactor(scrub): EEG axis sweep — 14 docs + .roadmap.galea → hexa-brain`). The commit message describes only the EEG / Galea scrub, but the diff included far more.

## Actual scope of fe1e3d09

**Intended (matches commit message):**
- 14 EEG-axis docs deleted from `anima/docs/` and `anima/docs/ai-native/` (anima_eeg_*, p9_paradigm_b_*, btr_evo_4_eeg_*, closed-loop-pipeline.md, openbci_auditory_listening, eeg_arrival_session_closure_*, ec_eo_label_fix_investigation, clm_eeg_smoke_v6_real_run)
- `.roadmap.galea` deleted (provider SSOT migrated to hexa-brain)

**Unintended (also swept in):**
- 100+ pre-existing untracked WIP files in `anima/docs/` got staged and committed alongside the EEG scrub. These were anima cycle work-in-progress (anima_2026_05_05_cycle_*, anima_clm_v2/v4_*, anima_core_*, anima_paradigm_*, etc.) that the user had presumably held back for a separate commit.

**Diff stats (actual):** 142 files changed, 27354 insertions(+), 3241 deletions(-). Insertions are the unintended additions; deletions match the intended EEG scrub.

## Cause

Used `git add -A docs/ .roadmap.galea` instead of enumerating each EEG-related file path. `-A` staged all untracked files in `docs/` regardless of relation to the EEG axis.

## Decision

Per user's directive (option A — leave as is): no revert, no force-push, no rewrite of the published commit. The unintended additions are legitimate anima work that was going to be committed eventually anyway, and force-rewrite of pushed history is destructive. The historical record stays slightly misleading; this note documents the discrepancy.

## Followup

- AI assistant memory updated to never use `git add -A <dir>` for scoped commits — always enumerate paths or use `git add -u <paths>` (tracked-only).
- Future scoped commits will run `git diff --cached --stat` and abort if the line count dramatically exceeds expectations.
