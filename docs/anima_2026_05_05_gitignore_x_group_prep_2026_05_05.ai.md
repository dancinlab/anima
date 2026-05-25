# anima_2026_05_05 — .gitignore X-Group Prep (BG-DY)

**Date**: 2026-05-06
**Author**: BG-DY (subagent, Opus 4.7 1M)
**Type**: doc-only spec (no .gitignore mutation; user fires)
**Cost**: $0 (mac, doc-only)
**Inputs**: BG-DF audit doc `docs/anima_2026_05_05_cycle_final_lock_token_audit_2026_05_05.md`
          (rows X-1 line 63, X-5 line 67, recommendations lines 210/214/243)

---

## §1 — X-1 path + size confirmed

BG-DF identified X-1 as a single 79MB jsonl file. Filesystem audit
(`find state -name "*.jsonl" -size +50M`) reveals **three** copies of
the same anima 30k slice corpus:

| # | absolute path                                                                                  | bytes      | size  | gitignore status (pre-fire)                                  |
|---|------------------------------------------------------------------------------------------------|-----------:|-------|---------------------------------------------------------------|
| 1 | `/Users/ghost/core/anima/state/clm_v4_lora_sft_2026_05_05/corpus/slice_A_anima_30k.jsonl`      | 79,179,209 | 76 MiB | **NOT IGNORED** — primary X-1 target                         |
| 2 | `/Users/ghost/core/anima/state/p9_path_a_retrain_v2_retry_2026_05_04/corpus/slice_A_anima_30k.jsonl` | 79,179,209 | 76 MiB | **NOT IGNORED** — `_retry_` not covered by line 36           |
| 3 | `/Users/ghost/core/anima/state/p9_path_a_retrain_v2_exec_2026_05_04/corpus/slice_A_anima_30k.jsonl`  | 79,179,209 | 76 MiB | already ignored via `.gitignore:36` (`_exec_*` glob)         |

`git check-ignore -v` confirms (1) and (2) are NOT ignored — single push
attempt would hit GitHub's 100MB/file warn-line and bloat anima permanently.

**Note on the “79 MB” label**: 79,179,209 bytes ≈ 75.5 MiB ≈ 79.2 MB
(decimal). BG-DF used decimal (matches `du -h` reporting in some shells);
`du -h` on this filesystem reports `76M` (MiB). Both refer to the same
file.

**Note on `state/anima_core_dialogues/`**: BG-DY task prompt §Sub-2
suggested patterning on this dir, but actual disk size is **140 KB total**
(21 jsonl files, max 8K each), and BG-DF row X-3 (line 65) explicitly
classifies these as **cycle evidence to keep in git** (Group A bound).
Do NOT add a `state/anima_core_dialogues/` ignore — that would erase
intentional dialogue evidence. The "79MB jsonl" only refers to X-1.

---

## §2 — X-5 path + size confirmed

| path                                                                  | files | total size | gitignore status |
|-----------------------------------------------------------------------|------:|-----------:|------------------|
| `/Users/ghost/core/anima/state/anima_eeg_audio_cache_2026_05_05/*.aiff` |   8   | 548 KB     | **NOT IGNORED** |

Files (per-file sizes, all `.aiff`):

```
countdown_3_2_1_start.aiff  89,064 B
ec_start.aiff               39,954 B
eo_start.aiff               83,476 B
failure.aiff                41,382 B
final_complete.aiff         87,974 B
impedance_fail.aiff        107,020 B
impedance_pass.aiff         49,164 B
phase_end.aiff              42,406 B
```

Pre-cached macOS `say`-rendered audio cues for the EEG session
runner. Each file < 5 MB so does not individually breach the
HF-only memory rule, but BG-DF row X-5 + memory rule
`anima models + datasets HF-only` treats binary audio caches as
HF-tier (or local-only). Verdict: gitignore.

---

## §3 — `.gitignore` patch proposal

Append to existing `.gitignore` (currently 258 lines, last entry
line 258 = `state/p9_path_a_*/sft_data_*.jsonl` HF migration).

```gitignore

# ─────────────────────────────────────────────────────────────────────────────
# 2026-05-05 cycle BG-DY — X-Group exclusions (BG-DF X-1 + X-5)
# Spec: docs/anima_2026_05_05_gitignore_x_group_prep_2026_05_05.ai.md
# Reason: HF-only memory rule (>5MB) + binary audio cache + repo bloat guard.
# ─────────────────────────────────────────────────────────────────────────────

# X-1: 79MB CLM v4 LoRA SFT corpus (regenerable; HF dataset for retention)
state/clm_v4_lora_sft_*/corpus/*.jsonl

# X-1: P9 retrain v2 retry corpus (line 36 only covers _exec_*; add _retry_)
state/p9_path_a_retrain_v2_retry_*/corpus/*.jsonl

# X-5: EEG audio cue cache (binary aiff, regenerable from say.hexa)
state/anima_eeg_audio_cache_*/*.aiff
```

### Pattern impact analysis

| pattern                                                  | targets                                               | bytes excluded | scope safety                                            |
|----------------------------------------------------------|-------------------------------------------------------|---------------:|---------------------------------------------------------|
| `state/clm_v4_lora_sft_*/corpus/*.jsonl`                 | X-1 primary (1 file today, future re-runs)            | 79,179,209     | narrow; only `corpus/*.jsonl` under that prefix        |
| `state/p9_path_a_retrain_v2_retry_*/corpus/*.jsonl`      | X-1 P9 retry copy (1 file today)                      | 79,179,209     | narrow; mirrors line 36 `_exec_*` rule                 |
| `state/anima_eeg_audio_cache_*/*.aiff`                   | X-5 (8 files today, future EEG sessions)              | 548 KB         | narrow; `.aiff` only — `.json` ledgers stay trackable  |

### What is **NOT** excluded by these patterns (intentional)

- `state/anima_core_dialogues/2026-05-05/*.jsonl` (21 files, 140 KB) — Group A
  cycle evidence per BG-DF row X-3
- `state/clm_v4_lora_sft_2026_05_05/{logs,results,verdict.json,…}` — SFT
  artefacts other than the 76 MiB jsonl
- `state/anima_eeg_audio_cache_2026_05_05/*.json` (none today, but reserved) —
  metadata sidecars stay trackable
- `state/p9_path_a_retrain_v2_exec_*` — already covered by existing line 36

### What is **deliberately not added** (deviation from BG-DY task prompt)

The prompt suggested four extra patterns; BG-DY rejects three after
audit and adopts one (split):

| prompt-suggested pattern                       | BG-DY decision                                                                                |
|------------------------------------------------|------------------------------------------------------------------------------------------------|
| `state/**/*orchestrator*.jsonl`                | **REJECTED** — no `*orchestrator*.jsonl` exists today (only `.log`, `.marker`); pattern moot   |
| `state/anima_core_dialogues/**/*.jsonl`        | **REJECTED** — would erase BG-DF X-3 cycle evidence; dialogue files 140 KB, intentional commit |
| `.venv-eeg/`                                   | **already on line 172** (skip)                                                                 |
| `.venv-anima*/`                                | **REJECTED** — no such venv exists in repo today; speculative                                  |

If user wants the speculative coverage anyway (defence-in-depth),
they can append the rejected patterns manually — but BG-DY's
recommendation is to keep `.gitignore` minimal and add patterns only
as concrete files appear.

---

## §4 — User fire 3-step

```bash
# ─── Step 1: append X-Group patterns to .gitignore ────────────────────────────
cat >> /Users/ghost/core/anima/.gitignore <<'EOF'

# ─────────────────────────────────────────────────────────────────────────────
# 2026-05-05 cycle BG-DY — X-Group exclusions (BG-DF X-1 + X-5)
# Spec: docs/anima_2026_05_05_gitignore_x_group_prep_2026_05_05.ai.md
# Reason: HF-only memory rule (>5MB) + binary audio cache + repo bloat guard.
# ─────────────────────────────────────────────────────────────────────────────

# X-1: 79MB CLM v4 LoRA SFT corpus (regenerable; HF dataset for retention)
state/clm_v4_lora_sft_*/corpus/*.jsonl

# X-1: P9 retrain v2 retry corpus (line 36 only covers _exec_*; add _retry_)
state/p9_path_a_retrain_v2_retry_*/corpus/*.jsonl

# X-5: EEG audio cue cache (binary aiff, regenerable from say.hexa)
state/anima_eeg_audio_cache_*/*.aiff
EOF

# ─── Step 2: verify nothing accidentally tracked already ─────────────────────
# (these should all return nothing — the X-1/X-5 paths are in the
# untracked-only 'gitStatus ??' bucket per session start state)
cd /Users/ghost/core/anima
git ls-files state/clm_v4_lora_sft_2026_05_05/corpus/
git ls-files state/p9_path_a_retrain_v2_retry_2026_05_04/corpus/
git ls-files state/anima_eeg_audio_cache_2026_05_05/

# defensive (no-op if not tracked):
git rm --cached state/clm_v4_lora_sft_2026_05_05/corpus/slice_A_anima_30k.jsonl 2>/dev/null || true
git rm --cached state/p9_path_a_retrain_v2_retry_2026_05_04/corpus/slice_A_anima_30k.jsonl 2>/dev/null || true
git rm --cached -r state/anima_eeg_audio_cache_2026_05_05/ 2>/dev/null || true

# verify ignore activated:
git check-ignore -v state/clm_v4_lora_sft_2026_05_05/corpus/slice_A_anima_30k.jsonl
git check-ignore -v state/anima_eeg_audio_cache_2026_05_05/eo_start.aiff
git check-ignore -v state/p9_path_a_retrain_v2_retry_2026_05_04/corpus/slice_A_anima_30k.jsonl
# expected: each prints `.gitignore:<line>:<pattern>` with the new lines

# ─── Step 3: now safe to fire commits ────────────────────────────────────────
# BG-BZ priority 5 + BG-DF tier 1-5 commit sequence per
# docs/anima_2026_05_05_cycle_final_lock_token_audit_2026_05_05.md
```

---

## §5 — Honest C3 (cost / caveat / certainty)

1. **C5-A `state/p9_path_a_retrain_v2_exec_*` is already covered by line 36
   but `_retry_` is not** — added a parallel pattern. If the user has
   any other `state/p9_path_a_retrain_v2_<verb>_*` directories with
   `corpus/*.jsonl` (e.g. future `_dryrun_`, `_qa_`), each will need
   its own pattern OR convert line 36 into the broader
   `state/p9_path_a_retrain_v2_*/corpus/*.jsonl` form. BG-DY did not
   broaden line 36 in this patch (out of scope for X-Group prep).
2. **C5-B `state/p9_p0_*/sft_data_full_50k_augmented.jsonl` is 126 MB**
   but already covered by line 200 `state/p9_p0_*/`. No action needed.
3. **C5-C `state/p9_path_a_r16_*/sft_data_llama_template.jsonl` is 69 MB**
   and already covered by line 258 `state/p9_path_a_*/sft_data_*.jsonl`.
   No action needed.
4. **C5-D `state/p9_lora_mode1_*` MMLU samples (16 MB each)** — *not*
   excluded by current `.gitignore`. Out of BG-DY's X-Group scope but
   flagged for next audit cycle (16 MB > 5 MB HF rule). User may want
   a follow-up BG to triage these.
5. **C5-E task prompt size mismatch with reality** — prompt says
   "79MB jsonl + 540KB aiff" and references `state/anima_core_dialogues`
   as a 79MB hotspot; in fact dialogues are 140 KB total and X-1 is in
   `state/clm_v4_lora_sft_2026_05_05/corpus/`. BG-DY corrected based on
   BG-DF audit doc (the authoritative source per task §컨텍스트).
6. **C5-F `git rm --cached` defensive — verified safe.** Pre-fire
   `git ls-files` for the three target paths will return nothing
   (BG-DY confirmed via `git status --short` that all three are
   in the `??` untracked bucket). The `|| true` suffix prevents
   step-2 abort if user runs the script twice.
7. **C5-G no `.gitignore` mutation by BG-DY** — task §제약 forbids it;
   user fire only. `state/anima_2026_05_05_gitignore_x_group_prep_2026_05_05/`
   directory + this spec are the only filesystem mutations.

---

**End of spec — under 200 LoC; user fire path explicit; no token literals.**
