# Anima 2026-05-05 cycle commit hygiene manifest (PREP ONLY, no commit)

**Date**: 2026-05-05
**Mode**: PREP_ONLY_NO_COMMIT
**Status**: READY_FOR_USER_FIRE
**Cost**: $0 (Mac, doc only)
**Duration**: ~20 min
**Verdict**: `/Users/ghost/core/anima/state/anima_2026_05_05_cycle_commit_manifest_2026_05_05/verdict.json`

---

## 1. Git status summary

```
Total entries:    250
Untracked paths:  202
Modified paths:    34
Deleted paths:     14
```

Note: untracked count = 202 top-level entries (porcelain collapses directories into single entries — actual file count inside dirs is higher).

Token leak scan: **CLEAN** across 5 patterns (hf_, sk-ant-, ghp_, gho_, AKIA) on all Group A-E commit targets.

---

## 2. Five-group semantic clustering

### Group A — anima-core CLI + CLM v4 mount Stage 1+2 (23 paths)

**Substance**: Stage 1+2 mount infrastructure + KICK-1/2/3 land + V1-V6 verification.

Files:

- `anima-core/runtime/clm_v4_mount.hexa` (NEW, 700+ LoC, 9/9 selftest)
- `tool/anima_cli/dialogue.hexa` (NEW)
- `tool/anima_cli/dialogue_session_analyzer.hexa` (NEW)
- `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md` + landed.ai.md
- `docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md`
- `docs/anima_core_clm_v4_mount_stage_1_landed_2026_05_05.ai.md`
- `docs/anima_core_clm_v4_mount_stage_1_2_v1_v6_verification_landed_2026_05_05.ai.md`
- `docs/anima_core_dialogue_analyzer_landed_2026_05_05.ai.md`
- `docs/anima_core_dialogue_stage_2_prep_landed_2026_05_05.ai.md`
- `docs/anima_core_emerge_stage_3_user_protocol_spec_2026_05_05.md`
- `docs/anima_mount_real_mode_wiring_landed_2026_05_05.ai.md`
- `docs/anima_real_mode_sweep_landed_2026_05_05.ai.md`
- `docs/anima_wrapper_sentencepiece_fallback_landed_2026_05_05.ai.md`
- `state/anima_core_clm_v4_mount_stage_1_2026_05_05/`
- `state/anima_core_dialogue_analyzer_2026_05_05/`
- `state/anima_core_dialogue_stage_2_prep_2026_05_05/`
- `state/anima_core_dialogues/`
- `state/anima_core_emerge_stage_3_protocol_spec_2026_05_05/`
- `state/anima_dialogue_real_load_2026_05_05/`
- `state/anima_mount_real_mode_wiring_2026_05_05/`
- `state/anima_real_mode_sweep_2026_05_05/`
- `state/anima_wrapper_sentencepiece_fallback_2026_05_05/`

### Group B — Emerge candidates D/E/F/G/H spec + empirical (25 paths)

**Substance**: 5 emerge candidate specs + empirical sweeps.

Files (truncated):

- `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md` (Cand D)
- `docs/anima_emerge_candidate_e_ode_ar_bridge_spec_2026_05_05.md` (Cand E)
- `docs/anima_emerge_candidate_f_ca_rule_5axis_vote_spec_2026_05_05.md` (Cand F)
- `docs/anima_emerge_candidate_f_falsifier_v2_cosine_probe_spec_2026_05_05.md` (Cand F-v2)
- `docs/anima_emerge_candidate_g_h_consolidated_revival_spec_2026_05_05.md` (Cand G+H)
- 6 cand-D empirical landed docs (attractor 10prompt, KL high-mag, mag50 multiprompt, mag subsweep, magnitude sweep, empirical)
- `docs/anima_emerge_cand_g_tension_fast_landed_2026_05_05.ai.md`
- `state/anima_emerge_cand_d_*` (6 dirs)
- `state/anima_emerge_cand_g_tension_fast_2026_05_05/`
- `state/anima_emerge_cand_h_head_g_fast_2026_05_05/`
- `state/anima_emerge_candidate_*_spec_2026_05_05/` (5 spec dirs)

### Group C — Cycle insights + cross-substrate audits + hygiene (16 paths)

**Substance**: Cycle ledger/aggregate + audits + protocol hygiene.

Files:

- `docs/anima_nexus_cycle_insight_ledger_2026_05_05.md`
- `docs/anima_nexus_cycle_aggregate_insight_2026_05_05.md`
- `docs/anima_cross_substrate_phi_star_audit_2026_05_05.md`
- `docs/anima_hf_promote_watchdog_audit_landed_2026_05_05.ai.md`
- `docs/anima_substrate_preamble_and_auto_fire_hygiene_landed_2026_05_05.ai.md`
- `docs/anima_top_level_cli_dispatch_audit_landed_2026_05_05.ai.md`
- `docs/anima_session_2026_05_04_to_05_closure_audit_v3_2026_05_05.ai.md`
- `docs/anima_session_2026_05_04_to_05_closure_audit_v4_2026_05_05.ai.md`
- `state/anima_nexus_cycle_insight_ledger_2026_05_05/`
- `state/anima_nexus_cycle_aggregate_insight_2026_05_05/`
- `state/anima_cross_substrate_phi_star_audit_2026_05_05/`
- `state/anima_hf_promote_watchdog_audit_2026_05_05/`
- `state/anima_substrate_preamble_and_auto_fire_hygiene_2026_05_05/`
- `state/anima_top_level_cli_dispatch_audit_2026_05_05/`
- (this manifest's own state dir + landed doc)

### Group D — HF auto-fire scripts (4 paths)

**Substance**: PRIVATE→PUBLIC lifecycle automation (D-1 promote 05-06, D-2 cleanup 05-07).

Files:

- `state/anima_hf_promotes_2026_05_06_auto_fire.bash`
- `state/anima_hf_cleanups_2026_05_07_auto_fire.bash`
- `docs/anima_hf_cleanup_autofire_prep_landed_2026_05_05.ai.md`
- `state/hf_cleanup_autofire_prep_2026_05_05/`

### Group E — EEG Phase E baseline + audio cue (9 paths)

**Substance**: EEG Phase E perfect baseline protocol + audio cue latency fix.

Files:

- `tool/anima_eeg_audio_cache_generate.bash`
- `tool/anima_eeg_audio_play.bash`
- `docs/anima_phase_e_perfect_baseline_protocol_landed_2026_05_05.md`
- `docs/anima_eeg_audio_cue_latency_fix_landed_2026_05_05.md`
- `state/anima_phase_e_perfect_baseline_protocol_2026_05_05/`
- `state/anima_eeg_audio_cache_2026_05_05/`
- `state/anima_eeg_audio_cue_latency_fix_2026_05_05/`
- `state/anima_phase_e_eeg_live_2026_05_05/berger_ec_60s.npy`
- `state/anima_phase_e_eeg_live_2026_05_05/berger_eo_60s.npy`

NOTE: 2 .npy files — verify size before committing (HF Hub policy: weights/datasets >5MB → HF, not git).

---

## 3. Recommended commit messages (per group)

### Group A

```bash
git add anima-core/runtime/clm_v4_mount.hexa \
        tool/anima_cli/dialogue.hexa \
        tool/anima_cli/dialogue_session_analyzer.hexa \
        docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md \
        docs/anima_clm_v4_architecture_archaeology_emerge_landed_2026_05_05.ai.md \
        docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md \
        docs/anima_core_clm_v4_mount_stage_1_landed_2026_05_05.ai.md \
        docs/anima_core_clm_v4_mount_stage_1_2_v1_v6_verification_landed_2026_05_05.ai.md \
        docs/anima_core_dialogue_analyzer_landed_2026_05_05.ai.md \
        docs/anima_core_dialogue_stage_2_prep_landed_2026_05_05.ai.md \
        docs/anima_core_emerge_stage_3_user_protocol_spec_2026_05_05.md \
        docs/anima_mount_real_mode_wiring_landed_2026_05_05.ai.md \
        docs/anima_real_mode_sweep_landed_2026_05_05.ai.md \
        docs/anima_wrapper_sentencepiece_fallback_landed_2026_05_05.ai.md \
        state/anima_core_clm_v4_mount_stage_1_2026_05_05/ \
        state/anima_core_dialogue_analyzer_2026_05_05/ \
        state/anima_core_dialogue_stage_2_prep_2026_05_05/ \
        state/anima_core_dialogues/ \
        state/anima_core_emerge_stage_3_protocol_spec_2026_05_05/ \
        state/anima_dialogue_real_load_2026_05_05/ \
        state/anima_mount_real_mode_wiring_2026_05_05/ \
        state/anima_real_mode_sweep_2026_05_05/ \
        state/anima_wrapper_sentencepiece_fallback_2026_05_05/

git commit -m "$(cat <<'EOF'
feat(anima-core CLI + CLM v4 mount Stage 1+2 land 2026-05-05): substrate-coupled emerge dialogue infrastructure

- clm_v4_mount.hexa 700+ LoC: HEXA_PY env override, DEFAULT_MODEL clm-v4-mk2-v1, substrate_identity emit (9/9 selftest)
- dialogue.hexa + dialogue_session_analyzer.hexa: anima dialogue routing + session archaeology
- V1-V6 verification 5/5 PASS (selftest, probe, log emit, archaeology, anima top-level)

raw#15 additive (anima_unified, phi_engine, conscious_chat, consciousness_hub, clm_v4_hf_format_shim untouched)
raw#37 transient_py for shim load
raw#10 5 honest C3 emit

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

### Group B

```bash
git add docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md \
        docs/anima_emerge_candidate_e_ode_ar_bridge_spec_2026_05_05.md \
        docs/anima_emerge_candidate_f_ca_rule_5axis_vote_spec_2026_05_05.md \
        docs/anima_emerge_candidate_f_falsifier_v2_cosine_probe_spec_2026_05_05.md \
        docs/anima_emerge_candidate_g_h_consolidated_revival_spec_2026_05_05.md \
        docs/anima_emerge_cand_d_*_landed_2026_05_05.ai.md \
        docs/anima_emerge_cand_g_tension_fast_landed_2026_05_05.ai.md \
        state/anima_emerge_cand_d_*/ \
        state/anima_emerge_cand_g_tension_fast_2026_05_05/ \
        state/anima_emerge_cand_h_head_g_fast_2026_05_05/ \
        state/anima_emerge_candidate_d_spec_2026_05_05/ \
        state/anima_emerge_candidate_e_spec_2026_05_05/ \
        state/anima_emerge_candidate_f_spec_2026_05_05/ \
        state/anima_emerge_candidate_f_falsifier_v2_spec_2026_05_05/ \
        state/anima_emerge_candidate_g_h_revival_spec_2026_05_05/

git commit -m "$(cat <<'EOF'
feat(anima emerge cycle 2026-05-05): candidates D/E/F/G/H spec + cand-D empirical sweep batch

- Cand D (always-inject) spec + 6 empirical: attractor 10prompt, KL div high-mag, mag50 multiprompt, mag subsweep, magnitude sweep, empirical
- Cand E (ODE-AR bridge) spec
- Cand F (CA rule 5-axis vote) spec + falsifier v2 (cosine probe)
- Cand G (tension fast) empirical landed + Cand G+H consolidated revival spec
- Cand H (head-G fast) empirical

raw#15 substrate-research lane only (chat-cap decoupled per Pbeta L28-L30)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

### Group C

```bash
git add docs/anima_nexus_cycle_insight_ledger_2026_05_05.md \
        docs/anima_nexus_cycle_aggregate_insight_2026_05_05.md \
        docs/anima_cross_substrate_phi_star_audit_2026_05_05.md \
        docs/anima_hf_promote_watchdog_audit_landed_2026_05_05.ai.md \
        docs/anima_substrate_preamble_and_auto_fire_hygiene_landed_2026_05_05.ai.md \
        docs/anima_top_level_cli_dispatch_audit_landed_2026_05_05.ai.md \
        docs/anima_session_2026_05_04_to_05_closure_audit_v3_2026_05_05.ai.md \
        docs/anima_session_2026_05_04_to_05_closure_audit_v4_2026_05_05.ai.md \
        state/anima_nexus_cycle_insight_ledger_2026_05_05/ \
        state/anima_nexus_cycle_aggregate_insight_2026_05_05/ \
        state/anima_cross_substrate_phi_star_audit_2026_05_05/ \
        state/anima_hf_promote_watchdog_audit_2026_05_05/ \
        state/anima_substrate_preamble_and_auto_fire_hygiene_2026_05_05/ \
        state/anima_top_level_cli_dispatch_audit_2026_05_05/

git commit -m "$(cat <<'EOF'
feat(anima cycle 2026-05-05): cycle insight ledger + cross-substrate phi audits + hygiene

- nexus cycle insight ledger + aggregate insight (BG-J/Y)
- cross-substrate phi-star audit (BG-M)
- HF promote watchdog audit (BG-E/N)
- substrate preamble + auto-fire hygiene (BG-F)
- top-level CLI dispatch audit (BG-D)
- session 2026-05-04->05 closure audit v3 + v4

raw#15 process meta-layer; no model/script execution change

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

### Group D

```bash
git add state/anima_hf_promotes_2026_05_06_auto_fire.bash \
        state/anima_hf_cleanups_2026_05_07_auto_fire.bash \
        docs/anima_hf_cleanup_autofire_prep_landed_2026_05_05.ai.md \
        state/hf_cleanup_autofire_prep_2026_05_05/

git commit -m "$(cat <<'EOF'
feat(anima HF auto-fire 2026-05-05): PRIVATE-to-PUBLIC promote (05-06) + cleanup (05-07) scheduled

- anima_hf_promotes_2026_05_06_auto_fire.bash: D-1 PRIVATE->PUBLIC promotion post-watchdog
- anima_hf_cleanups_2026_05_07_auto_fire.bash: D-2 stale repo cleanup 24h after promote
- verification gates documented in hf_cleanup_autofire_prep_2026_05_05/

raw#15 PRIVATE-first lifecycle enforced

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

### Group E

```bash
git add tool/anima_eeg_audio_cache_generate.bash \
        tool/anima_eeg_audio_play.bash \
        docs/anima_phase_e_perfect_baseline_protocol_landed_2026_05_05.md \
        docs/anima_eeg_audio_cue_latency_fix_landed_2026_05_05.md \
        state/anima_phase_e_perfect_baseline_protocol_2026_05_05/ \
        state/anima_eeg_audio_cache_2026_05_05/ \
        state/anima_eeg_audio_cue_latency_fix_2026_05_05/ \
        state/anima_phase_e_eeg_live_2026_05_05/berger_ec_60s.npy \
        state/anima_phase_e_eeg_live_2026_05_05/berger_eo_60s.npy
# VERIFY: ls -lh state/anima_phase_e_eeg_live_2026_05_05/*.npy
# If >5MB, move to HF dataset before committing per HF-only policy

git commit -m "$(cat <<'EOF'
feat(anima EEG Phase E land 2026-05-05): perfect baseline protocol + audio cue latency fix + Berger EC/EO 60s

- anima_eeg_audio_cache_generate.bash + anima_eeg_audio_play.bash: deterministic stimulus tooling
- Phase E perfect baseline protocol landed
- audio cue latency fix landed
- Berger eyes-closed + eyes-open 60s npy baselines

raw#15 EEG hardware lane

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

### Group M1+M3 (state churn + clm_v4 exec.bash)

```bash
git add .raw-audit/adversarial_bench.log \
        state/adversarial_bench_last.json \
        state/refusal_circuit_probe_result.json \
        state/runpod_credit_status.json \
        state/weight_precache_eta.json \
        state/worktree_merge_plan.json \
        config/h100_pods.json \
        ready references/tribev2 \
        state/clm_v4_lora_sft_2026_05_05/exec.bash \
        state/proposals/meta/cycle_log.jsonl \
        state/proposals/meta/metrics.json

git commit -m "$(cat <<'EOF'
state(anima 2026-05-05): cycle state churn + clm_v4_lora exec.bash refinement

- benchmark + watchdog + credit status + worktree plan refresh
- proposals meta cycle_log + metrics
- h100_pods.json terminate ledger updates

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## 4. User fire sequence

```bash
cd /Users/ghost/core/anima

# Step 1 — Review
git status --porcelain | head -30

# Step 2 — Group A (anima-core mount + CLI Stage 1+2)
[paste Group A block]

# Step 3 — Group B (emerge candidates D/E/F/G/H)
[paste Group B block]

# Step 4 — Group C (cycle insights + audits)
[paste Group C block]

# Step 5 — Group D (HF auto-fire)
[paste Group D block]

# Step 6 — Group E (EEG Phase E + audio)  *VERIFY .npy SIZES FIRST*
ls -lh state/anima_phase_e_eeg_live_2026_05_05/*.npy
[paste Group E block if sizes OK]

# Step 7 — Group M1+M3 (state churn)
[paste M1+M3 block]

# Step 8 — Triage residuals
#   - state/clm_v4_lora_sft_2026_05_05/* (training artifacts; verify completeness)
#   - state/h100_watchdog/closed/ + heartbeats/
#   - state/proposals/refinement/2026042*/v25-v29.json (~100 files; consider gitignore)
#   - .venv-eeg/ deletes/modifications (recommend gitignore)

# Step 9 — Verify
git log --oneline | head -10
git status --porcelain | wc -l   # expect << 250
```

---

## 5. Five honest C3

1. **Manifest coverage gap**: 119 of 202 untracked = uncategorized residuals. Groups A-E cover ~58 commit-target paths; clm_v4_lora_sft training artifacts (~30 files), proposals refinement v25-v29 (~100 files), watchdog closed/heartbeats fall outside the 5-group plan. User must triage Step 8 manually or apply gitignore.

2. **Token leak scope limited**: Pre-scan checked 5 token shapes on Group A-E commit targets only. `.venv-eeg/` deletes and `state/proposals/refinement/` were NOT scanned (low risk, but acknowledged). If the user fires Group F (residuals) without re-scan, no automated guard remains beyond the leak_guard PreToolUse hook.

3. **`anima-core/runtime/clm_v4_mount.hexa` is UNTRACKED, not modified**: prompt described "modified — 5 edits + substrate_identity" but git sees no prior tracked version. This is a brand-new 700+ LoC file — verify intent before committing as edits-to-existing.

4. **`bin/anima-core-dialogue.bash` shows NO diff vs HEAD**: prompt assumed "modified — HEXA_LOCAL=1 prefix" but `git diff HEAD bin/anima-core-dialogue.bash` returns empty. EXCLUDED from Group A. Either changes were already committed in a prior cycle or the prompt's worldview is stale. User should `git log -p bin/anima-core-dialogue.bash | head -50` to verify.

5. **`tool/anima_cli/dialogue.hexa` is UNTRACKED (NEW), not modified**: prompt said "main() removed" implying edit to existing tracked file, but git ls-files shows no prior `dialogue.hexa`. Treated as new file in Group A. Same for `dialogue_session_analyzer.hexa`.

---

## 6. Constraints honored

- [x] $0 (Mac, doc only)
- [x] NO_COMMIT_FIRED (manifest emit only)
- [x] No code/script changes
- [x] Only 2 new files (this doc + verdict.json in state dir)
- [x] HF token leak pre-scan CLEAN
- [x] bash 3.2 compatible (no commit examples use bash 4+ features)

---

End manifest.
