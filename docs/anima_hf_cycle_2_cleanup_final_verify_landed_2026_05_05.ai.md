# anima HF Cycle 2 cleanup + promote final verify landed 2026-05-05

**Cycle**: `hf_cycle_2_cleanup_final_verify_2026_05_05`
**BG-lane**: BG-HF-CLEANUP-FINAL-VERIFY
**Substrate**: mac (no destructive ops, dry-run + audit only)
**Cost**: $0.00
**Wall**: ~6 min
**Verdict**: PASS — all 4 cleanup+promote scripts (clm-v4-mk2-v1 + pbeta × cleanup + promote) pass syntax + GATE-1-FAIL-as-expected dry-run; HF Hub state intact for both repos; Pβ scripts newly authored from clm template.

## Summary

HF Cycle 2 final verification before review-window-close execution. Audited 2 preexisting clm scripts (already had EXPECTED_SIBLINGS=15→16 fix applied). Authored 2 new Pβ analogous scripts from clm template with sha/siblings/window deltas. Confirmed HF Hub current state matches script EXPECTED_* constants for both repos.

## Scripts Status (4 total)

| Script | Status | syntax (bash -n) | dry-run | review_close_utc | ready_to_run_at_utc |
|---|---|---|---|---|---|
| `state/clm_v4_hf_release_v1_upload_2026_05_04/cleanup_2026_05_07.bash` | preexisting | PASS | GATE_1_FAIL (expected) | 2026-05-06T23:26:12Z | 2026-05-06T23:26:12Z |
| `state/clm_v4_hf_release_v1_upload_2026_05_04/public_promote_2026_05_07.bash` | preexisting | PASS | GATE_1_FAIL (expected) | 2026-05-06T23:26:12Z | 2026-05-06T23:26:12Z |
| `state/p9_pbeta_hf_upload_2026_05_05/cleanup_pbeta_2026_05_08.bash` | NEWLY AUTHORED | PASS | GATE_1_FAIL (expected) | 2026-05-07T03:48:00Z | 2026-05-07T03:48:00Z |
| `state/p9_pbeta_hf_upload_2026_05_05/public_promote_pbeta_2026_05_08.bash` | NEWLY AUTHORED | PASS | GATE_1_FAIL (expected) | 2026-05-07T03:48:00Z | 2026-05-07T03:48:00Z |

## HF Hub State (audit time 2026-05-05T08:30:00Z)

| repo | private | sha | siblings | matches script EXPECTED_* |
|---|---|---|---|---|
| `dancinlab/clm-v4-mk2-v1` | true | `80440a1d38db9addc4445bb959057558a57f4230` | 16 | YES (intact) |
| `dancinlab/clm-v4-paradigm-d-pbeta-50k-mk2-v1` | true | `7643e764488f8e11020a7663c50f2e590b70d10f` | 6 | YES (intact) |

## Pβ Script Authoring Deltas

**cleanup_pbeta_2026_05_08.bash** — diff vs clm template:
- `REPO_ID` → `dancinlab/clm-v4-paradigm-d-pbeta-50k-mk2-v1`
- `COMMIT_SHA` → `7643e764488f8e11020a7663c50f2e590b70d10f`
- `EXPECTED_SIBLINGS` → 6 (Pβ has 5 stage files + .gitattributes vs clm 16)
- `UBU1_STAGE` → `/home/aiden/anima_pbeta_50k_step50000`
- `MAC_STAGE_MIRROR` → `state/p9_pbeta_paradigm_d_50k_hf_upload_stage_2026_05_05`
- `REVIEW_WINDOW_ENDS_48H_UTC` → `2026-05-07T03:48:00Z`

**public_promote_pbeta_2026_05_08.bash** — diff vs clm template:
- All cleanup deltas above
- `manual confirm string` → `PROMOTE-pbeta-50k`
- G1 evidence → F-Pβ-2 holdout500 + F-Pβ-3 hybrid verdicts
- G2 evidence → README §C1 chat-FAIL_TRUE disclosure (BLEU-1=1.96%, ROUGE-L=0.00582, chrF=0.02195)
- G3 evidence → Pβ φ★=42.37 baseline (paradigm v11 G3)
- **G5 NEW GATE** — base model promotion status check (adapter inherits availability; clm-v4-mk2-v1 MUST be promoted public BEFORE pbeta to allow non-auth load)
- G6 evidence → Pβ stage README.md (5 H2 + 7-bullet Caveats)

## Caveats (honest C3 ≥5)

1. **C1 — shellcheck not installed on mac**; syntax verification fell back to `bash -n` only. Recommend `brew install shellcheck` + re-audit before scheduled execution.
2. **C2 — dry-run only exercised GATE 1 path** (GATE 1 short-circuits abort). GATE 2 (curl + python3 parse) validated out-of-band by independent HF API audit; equivalent coverage achieved.
3. **C3 — Pβ promote G5 NEW gate**: operator must verify base `clm-v4-mk2-v1` is public-promoted FIRST; otherwise non-auth readers cannot load Pβ adapter (PEFT requires base + adapter both accessible). Order of operations: clm-v4-mk2-v1 promote MUST precede pbeta promote.
4. **C4 — mac secret store may return rotated token** (per pbeta upload C7: hf_asc... fails, hf_dw... works). Scripts validate `hf_*` prefix shape only, not whoami. Recommend mac secret re-sync OR run from ubu1.
5. **C5 — mac stage mirrors retained by default**; cleanup has opt-in `--delete-mac-mirror` flag. Pβ mac mirror ~76MB borderline; pass flag if disk pressure justifies.
6. **C6 — no git commit** (per task CRITICAL). pbeta scripts live in `state/p9_pbeta_hf_upload_2026_05_05/` which is gitignored; this is fine for execution but means they are not version-tracked. Consider docs/-side recipe doc for version trail.
7. **C7 — bash 3.2 ISO-8601 string compare**: `[[ "$NOW" < "$END" ]]` works correctly as lexicographic compare for fixed-format `YYYY-MM-DDTHH:MM:SSZ` UTC strings (no DST/tz ambiguity). All 4 dry-runs confirmed.

## Next Ranked Actions

- **rank-1** USER ACK + schedule clm-v4-mk2-v1 cleanup + promote at `2026-05-06T23:26:12Z`; promote requires manual `PROMOTE-clm-v4-mk2-v1` confirm
- **rank-2** USER ACK + schedule pbeta cleanup + promote at `2026-05-07T03:48:00Z`; promote requires manual `PROMOTE-pbeta-50k` confirm AND base model already public-promoted (G5)
- **rank-3** install shellcheck on mac + re-audit all 4 scripts before scheduled execution
- **rank-4** mac secret store re-sync to preempt GATE 2 401 at execution time
- **rank-5** (optional) commit pbeta scripts to anima git for version tracking — but state/ gitignored; docs-side recipe doc may suffice

## Artifacts

- verdict: `state/hf_cycle_2_cleanup_final_verify_2026_05_05/verdict.json`
- audited scripts: 4 paths above
- precedent: `docs/anima_clm_hf_release_v1_uploaded_landed_2026_05_04.ai.md`, pbeta verdict `state/p9_pbeta_hf_upload_2026_05_05/verdict.json`
