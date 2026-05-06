# Anima 2026-05-05 cycle final lock — token leak audit + commit-readiness manifest (BG-DF)

**Status**: AUDIT_CLEAN / COMMIT_READY_TIERED
**Scope**: 100+ BG cumulative artifact final pre-commit lock
**Mode**: mac doc-only, $0, ~25min
**Predecessors**:
- `docs/anima_2026_05_05_cycle_commit_manifest_landed_2026_05_05.ai.md` (BG-AM full ~250)
- `docs/anima_2026_05_05_priority_subset_commit_manifest_2026_05_05.ai.md` (BG-BZ priority 5)

This doc completes the pre-commit lock by (a) running the full token-leak scan one final time across all 465 untracked artifacts, (b) re-classifying them into 5 fire-tier groups + 1 triage-deferred group, (c) emitting the 5-tier user-fire sequence, and (d) consolidating a 7-fact hand-off summary so the next conversation can carry forward without re-reading 100+ landed docs.

---

## §1 Token leak scan — CLEAN

### Scan command

```bash
git ls-files --others --exclude-standard \
  | xargs grep -l 'hf_[A-Za-z0-9]\{20,\}\|sk-ant-[A-Za-z0-9]\{20,\}\|ghp_[A-Za-z0-9]\{20,\}\|AKIA[A-Z0-9]\{16\}' \
    2>/dev/null \
  | head -20
```

Plus extended cross-checks:
- modified tracked files (`git diff HEAD --name-only | xargs grep ...`)
- broader patterns (`BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY`, `aws_secret_access_key=`)
- file-extension scan for `.env|.key|.pem|.p12`
- explicit re-grep on `state/anima_hf_promotes_2026_05_06_auto_fire.bash` and `state/anima_hf_cleanups_2026_05_07_auto_fire.bash` (Group E)

### Result

| scan | matches | status |
|---|---|---|
| 4-shape token (hf_/sk-ant-/ghp_/AKIA) on 465 untracked | 0 | CLEAN |
| 4-shape token on 47 modified tracked | 0 | CLEAN |
| BEGIN PRIVATE KEY / aws_secret_access_key | 0 | CLEAN |
| .env/.key/.pem/.p12 extensions | 0 | CLEAN |
| explicit grep on Group E HF auto-fire scripts | 0 | CLEAN |

**Verdict**: CLEAN across **465 untracked + 47 modified-tracked = 512 total artifacts**. anima leak_guard PreToolUse hook (9-shape regex) provides second-line defense at user fire-time. No token literal must be embedded in any audit/security doc per memory rule `audit_doc_token_redact` — this doc honors that.

---

## §2 100+ BG artifact classification — 5 tiers + 1 triage group

| group | name | file count | doc count | state count | tool count | fire-tier |
|---|---|---|---|---|---|---|
| **P** | priority 5 (BG-BJ + BG-AY + BG-AN + BG-BL + BG-BN) | **14** (5 doc + 5 state + 4 tool) | 5 | 5 | 4 | **Tier 1** |
| **A** | Stage 1+2 mount layer (KICK-1/2/3 + V1-V6 + mount.hexa + dialogue) | ~25 (incl. 21 dialogue session jsonl) | 6 | ~17 | 2 | **Tier 2** |
| **B** | 5 emerge candidate specs (D + E + F + F-v2 + G+H) | 10 (5 doc + 5 state) | 5 | 5 | 0 | **Tier 3** |
| **C** | empirical 50+ BG (chat_*, cand_d_*, real_mode_sweep, sweeps) | ~190 (101 chat + 56 cand + 35 real-mode/misc) | ~45 | ~145 | 0 | **Tier 4** |
| **D** | cycle insights (close_decision, summary, ledger, aggregate, paradigm_acceptance, naming) | 38 | ~22 | ~16 | 0 | **Tier 4 (semantic cluster)** |
| **E** | HF promote/cleanup auto-fire scripts | 8 (3 doc + 3 state-verdict + 2 bash) | 3 | 5 | 0 | **Tier 5 (time-gated)** |
| **X** | triage-deferred (test artifacts + binaries + churn) | ~152 | 0 | ~152 | 0 | **DEFERRED** |

**Total accounted**: P(14) + A(25) + B(10) + C(190) + D(38) + E(8) + X(152) = **437** of 465 untracked. Residual ~28 = misc spec/audit docs not bound to a single BG (e.g. `anima_clm_3_chat_objective_cycle_0_spec`, `anima_phi_star_proxy_geometry_invariant_spec`, `anima_p10_paradigm_declaration_solicit_own_rule`, `anima_identity_preservation_next_cycle_lock`, `anima_stage_3_corpus_protocol_skeleton`, `anima_external_chat_enable_tools_audit`, `anima_external_sister_candidates_audit`, `anima_eeg_audio_cue_latency_fix`, `anima_top_level_cli_dispatch_audit`, `anima_wrapper_sentencepiece_fallback`, `anima_paradigm_v11_g3_canonical_magnitude_audit`, `anima_cross_substrate_phi_star_audit`) — these merge into Tier 4 Group D as auxiliary cycle-insight commits or Tier 3 as spec-companion commits.

### §2.X Group X (triage-deferred) details

| sub-group | path | files | reason for deferral |
|---|---|---|---|
| X-1 | `state/clm_v4_lora_sft_2026_05_05/` | 29 | **79 MB `corpus/slice_A_anima_30k.jsonl`** violates `anima models + datasets HF-only (>5MB)` memory rule. Must NOT enter git. Decision: HF Hub upload OR local-only with `.gitignore` entry. |
| X-2 | `state/proposals/refinement/20260422-*/v*.json` | 84 | refinement-cycle churn from 2026-04-22; not bound to BG-cycle, may or may not be cycle-relevant. User triage required. |
| X-3 | `state/anima_core_dialogues/2026-05-05/*.jsonl` | 21 | live dialogue session logs. Decision: keep in git as cycle evidence OR move to HF dataset (size 1-30 KB each, well under 5MB threshold). Default = git keep, but **bound to Group A** semantically. |
| X-4 | `state/h100_watchdog/{closed,heartbeats}/` | 8 | watchdog state from yesterday's H100 BGs. own 16 enforcement records. May be ephemeral. |
| X-5 | `state/anima_eeg_audio_cache_2026_05_05/*.aiff` | 8 | binary audio cues. Per memory rule, treat like models — defer to HF or `.gitignore`. |
| X-6 | `state/anima_phase_e_eeg_live_2026_05_05/*.npy` | 2 | 960 KB each (under 5MB). EEG raw signals. May commit OR HF dataset. |

X-1 and X-5 carry **non-zero risk of GitHub size-limit / push-rejection**; user fire-time triage mandatory.

---

## §3 5-tier fire sequence (user-fire commands)

Each tier is independent. Run sequentially or skip/reorder per user judgment. All commits are NEW commits (never amend, per git safety protocol).

### Tier 1 — Priority 5 commits (~5 min, lowest risk)

5 commits per BG-BZ template (`docs/anima_2026_05_05_priority_subset_commit_manifest_2026_05_05.ai.md` §3). Files re-verified present 2026-05-06.

```bash
# P-1 BG-BJ residual basin reframing
git add tool/transient_py/anima_emerge_chat_entropy_trajectory.py \
        state/anima_emerge_chat_entropy_trajectory_2026_05_05/ \
        docs/anima_emerge_chat_entropy_trajectory_landed_2026_05_05.ai.md
git commit -m "..." # full HEREDOC in BG-BZ §3 P-1

# P-2 BG-AY 4-closure theorem
git add docs/anima_115_architectural_4_closure_theorem_2026_05_05.md \
        state/anima_115_architectural_4_closure_theorem_2026_05_05/
git commit -m "..." # full HEREDOC in BG-BZ §3 P-2

# P-3 BG-AN minimum viable dialogue
git add tool/transient_py/anima_emerge_dialogue_repl.py \
        state/anima_emerge_dialogue_first_turn_2026_05_05/ \
        docs/anima_emerge_dialogue_first_turn_landed_2026_05_05.ai.md
git commit -m "..." # full HEREDOC in BG-BZ §3 P-3

# P-4 BG-BL nnsight smoke
git add tool/transient_py/anima_emerge_nnsight_smoke.py \
        state/anima_emerge_nnsight_smoke_2026_05_05/ \
        docs/anima_emerge_nnsight_smoke_landed_2026_05_05.ai.md
git commit -m "..." # full HEREDOC in BG-BZ §3 P-4

# P-5 BG-BN Pythia phi smoke
git add tool/transient_py/anima_emerge_pythia_phi_smoke.py \
        state/anima_emerge_pythia_phi_smoke_2026_05_05/ \
        docs/anima_emerge_pythia_phi_smoke_landed_2026_05_05.ai.md
git commit -m "..." # full HEREDOC in BG-BZ §3 P-5
```

### Tier 2 — Stage 1+2 mount layer Group A (~15 min)

Single bundled commit (mount layer is one logical change). Excludes the 79MB X-1 jsonl and includes 21 dialogue jsonl session logs as cycle evidence.

```bash
git add anima-core/runtime/clm_v4_mount.hexa \
        tool/anima_cli/dialogue.hexa \
        tool/anima_cli/dialogue_session_analyzer.hexa \
        docs/anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md \
        docs/anima_core_clm_v4_mount_stage_1_landed_2026_05_05.ai.md \
        docs/anima_core_clm_v4_mount_stage_1_2_v1_v6_verification_landed_2026_05_05.ai.md \
        docs/anima_core_dialogue_analyzer_landed_2026_05_05.ai.md \
        docs/anima_core_dialogue_stage_2_prep_landed_2026_05_05.ai.md \
        docs/anima_mount_real_mode_wiring_landed_2026_05_05.ai.md \
        state/anima_core_clm_v4_mount_stage_1_2026_05_05/ \
        state/anima_core_dialogue_analyzer_2026_05_05/ \
        state/anima_core_dialogue_stage_2_prep_2026_05_05/ \
        state/anima_mount_real_mode_wiring_2026_05_05/ \
        state/anima_core_dialogues/ \
        state/anima_dialogue_real_load_2026_05_05/

git commit -m "feat(anima-core stage 1+2 mount layer 2026-05-05): clm_v4_mount.hexa + dialogue REPL + analyzer + V1-V6 verification + 21 session logs"
```

### Tier 3 — 5 emerge candidate specs Group B (~30 min)

5 commits, one per candidate (D / E / F / F-v2 / G+H). Each commit binds spec doc + state verdict.

```bash
# Cand D
git add docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md \
        state/anima_emerge_candidate_d_spec_2026_05_05/
git commit -m "spec(anima emerge cand-D always-inject 2026-05-05)"

# Cand E
git add docs/anima_emerge_candidate_e_ode_ar_bridge_spec_2026_05_05.md \
        state/anima_emerge_candidate_e_spec_2026_05_05/
git commit -m "spec(anima emerge cand-E ODE AR-bridge 2026-05-05)"

# Cand F (CA rule 5-axis vote)
git add docs/anima_emerge_candidate_f_ca_rule_5axis_vote_spec_2026_05_05.md \
        state/anima_emerge_candidate_f_spec_2026_05_05/
git commit -m "spec(anima emerge cand-F CA-rule 5-axis vote 2026-05-05)"

# Cand F-v2 (falsifier cosine probe)
git add docs/anima_emerge_candidate_f_falsifier_v2_cosine_probe_spec_2026_05_05.md \
        state/anima_emerge_candidate_f_falsifier_v2_spec_2026_05_05/
git commit -m "spec(anima emerge cand-F v2 cosine-probe falsifier 2026-05-05)"

# Cand G+H (consolidated revival)
git add docs/anima_emerge_candidate_g_h_consolidated_revival_spec_2026_05_05.md \
        state/anima_emerge_candidate_g_h_revival_spec_2026_05_05/ \
        state/anima_emerge_cand_g_tension_fast_2026_05_05/ \
        state/anima_emerge_cand_h_head_g_fast_2026_05_05/ \
        docs/anima_emerge_cand_g_tension_fast_landed_2026_05_05.ai.md
git commit -m "spec(anima emerge cand-G+H consolidated revival + tension/head fast probes 2026-05-05)"
```

### Tier 4 — empirical 50+ BG Group C + cycle insights Group D (~60+ min)

Semantic clustering — bundle related chat_*/cand_d_*/real_mode_sweep BGs into thematic commits to keep `git log` legible:

| cluster | members | rough count |
|---|---|---|
| C-1 chat-axis sweeps | chat_axis_full_sweep + chat_english_sweep + chat_multilingual_sweep + chat_korean_prefix_inject + chat_korean_rank_survey | ~15 files |
| C-2 chat-decode strategies | chat_decode_strategies + chat_temp_extreme + chat_first_token_force + chat_self_feed + chat_fresh_reset + chat_byte_*_ban + chat_byte_monopoly_break | ~25 files |
| C-3 chat-mechanism probes | chat_logit_lens + chat_full_layer_lens + chat_lexical_baseline + chat_partial_layers + chat_lnf_scale_ablate + chat_residual_noise + chat_rmsnorm_diagnostic + chat_sae_pca_features + chat_lm_head_row_norm + chat_pythia_clm_logit_compare + chat_l13_15_ablate | ~30 files |
| C-4 chat-intervention experiments | chat_activation_patching + chat_repe_steering + chat_c_proj_inject + chat_basin_ablate + chat_embed_decode + chat_head_compare + chat_hybrid_pythia_clm + chat_hybrid_repl + chat_semantic_bridge + chat_tribev2 + chat_entropy_trajectory (already in Tier 1 P-1) | ~25 files |
| C-5 cand-d magnitude/empirical | cand_d_attractor_10prompt + cand_d_empirical + cand_d_kl_div_high_mag + cand_d_mag_subsweep + cand_d_mag50_multiprompt + cand_d_magnitude_sweep + emerge_attractor_characterization + emerge_5turn_dialogue_smoke + emerge_dialogue_first_session_manual + emerge_dialogue_precedent_audit + emerge_nnsight_intervention | ~50 files |
| C-6 real-mode + repl smoke | real_mode_sweep + emerge_chat_repl + emerge_repl session jsonl | ~35 files |
| D-1 cycle close decisions | cycle_close_decision + cycle_hard_close_decision + cycle_close_roadmap_memory_update | 6 files |
| D-2 cycle aggregates / summaries | cycle_summary_single_source_of_truth + cycle_summary_v2_final + cycle_final_aggregate + nexus_cycle_aggregate_insight + nexus_cycle_insight_ledger + nexus_cycle_insight_ledger_v2 | ~12 files |
| D-3 paradigm acceptance / naming | paradigm_acceptance_user_intent_reconciliation + paradigm_b_c_final_acceptance + paradigm_b_fire_preview + paradigm_c_demo_session + paradigm_naming_reframing + paradigm_v11_g3_canonical_magnitude_audit + cross_substrate_phi_star_audit + substrate_preamble_and_auto_fire_hygiene + 115_architectural (already in Tier 1 P-2) | ~14 files |
| D-4 misc audits / specs | clm_3_chat_objective_cycle_0_spec + phi_star_proxy_geometry_invariant_spec + p10_paradigm_declaration_solicit_own_rule + identity_preservation_next_cycle_lock + stage_3_corpus_protocol_skeleton + external_chat_enable_tools_audit + external_sister_candidates_audit + eeg_audio_cue_latency_fix + top_level_cli_dispatch_audit + wrapper_sentencepiece_fallback + clm_v4_architecture_archaeology_emerge + core_emerge_paradigm_revision + core_emerge_stage_3_user_protocol_spec + phase_e_perfect_baseline_protocol + session_2026_05_04_to_05_closure_audit_v3/v4 + clm_v4_mount audits | ~30 files |

5+ commits per BG-AM full-manifest semantic-cluster shape; one per cluster (10 commits total in Tier 4).

### Tier 5 — HF promote/cleanup time-gated Group E (deferred until just before T-window dwell)

```bash
# At T = 2026-05-06T23:25Z (before 23:26Z clm window dwell)
git add docs/anima_hf_cleanup_autofire_prep_landed_2026_05_05.ai.md \
        docs/anima_hf_promote_pre_fire_audit_2026_05_05.ai.md \
        docs/anima_hf_promote_watchdog_audit_landed_2026_05_05.ai.md \
        state/anima_hf_promotes_2026_05_06_auto_fire.bash \
        state/anima_hf_cleanups_2026_05_07_auto_fire.bash \
        state/anima_hf_promote_pre_fire_audit_2026_05_05/ \
        state/anima_hf_promote_watchdog_audit_2026_05_05/ \
        state/hf_cleanup_autofire_prep_2026_05_05/

git commit -m "ops(anima HF promote/cleanup auto-fire 2026-05-06/07 time-gated)"
```

### Group X triage-deferred (user decision required)

| sub-group | recommended verdict |
|---|---|
| X-1 clm_v4_lora_sft 79MB jsonl | **DO NOT COMMIT TO GIT.** Add `state/clm_v4_lora_sft_2026_05_05/corpus/slice_A_anima_30k.jsonl` to `.gitignore`. Push to HF dataset if retention needed. Other lora_sft logs/results (small) can commit if user wants. |
| X-2 proposals/refinement/2026-04-22 | DEFER (not 2026-05-05 cycle). Bundle into a separate commit `state(proposals 2026-04-22 refinement churn)` or skip. |
| X-3 anima_core_dialogues 21 jsonl | INCLUDED IN TIER 2 (Group A). |
| X-4 h100_watchdog | bundle with Tier 5 Group E (ops/watchdog cluster). |
| X-5 eeg_audio_cache aiff | DO NOT COMMIT (binary). `.gitignore` entry; HF dataset if needed. |
| X-6 phase_e_eeg_live npy (2 × 960KB) | OK to commit (under 5MB). Bundle with Tier 4 D-4 misc. |

---

## §4 Hand-off summary — 7 facts the next conversation must carry

The next conversation should be able to begin without re-reading 100+ landed docs by carrying these 7 facts:

1. **100+ BG land complete on 2026-05-05.** Total artifacts: 465 untracked + 47 modified-tracked = **512** across docs/+state/+tool/+anima-core/. All token-leak CLEAN. Commit-readiness gated on user fire-permission per memory rule.

2. **#115 architectural 4-closure theorem (BG-AY)**: chat capability on CLM v4 mk2 v1 is FALSIFIED along 4 independent axes — (a) post-hoc LoRA SFT FAIL_REGRESSION -36.298pp, (b) Phi-star distill Pβ Paradigm D 50K FAIL_TRUE composite 0.01176, (c) tribev2 cross-modal FAIL_ARCHITECTURAL_DESIGN_REVIEW (no logits/lm_head/generate), (d) logit-lens + semantic bridge FAIL_RESIDUAL_STREAM_PERVASIVE (1/8 + 0/2 coherent). Bounded by 4 untested H1-H4 hypotheses. **Chat-capability path of record = Llama-3.2-3B Path A v2 (composite 0.5584); CLM v4 = substrate-research-only.**

3. **Paradigm B + C ACHIEVABLE_NOW** (BG-AN minimum viable dialogue + BG-CG / BG-? acceptance reconciliation): F-AN-1 PASS REPL helper emits phi-star + drift + hsd + l2-var per turn; 3-turn auto-fire confirms prior-threading at hsd > 0. Stage 1+2 mount layer (Group A) wires this into anima-core runtime. Paradigm naming reframed (`docs/anima_paradigm_naming_reframing_2026_05_05.md`).

4. **Residual basin reframing (BG-BJ + BG-CI L13-L15 onset)**: collapse mechanism is autoregressive attractor problem **upstream of `lm_head`** in residual-stream geometry, NOT output-projection defect. All output-projection class fixes (LoRA / vocab mask / Korean bias / template / few-shot / c_proj rewrite) are **invalid by construction**. L13-L15 = empirical basin onset layers.

5. **head_a alignment destroyed (BG-CD multilingual sweep)**: cross-language probing on CLM v4 mk2 v1 shows axis alignment broken — phi-star is paradigm v11 G3 + CLM v4 specific geometry (8-cell × 192 tile-reshape of mean-pooled last-layer hidden), NOT a substrate-agnostic invariant. Pythia-70m smoke (BG-BN P-5) confirms cross-substrate carryover unverified.

6. **Stage 3 protocol ready (BG-D 30 sessions)**: `docs/anima_core_emerge_stage_3_user_protocol_spec_2026_05_05.md` + `docs/anima_stage_3_corpus_protocol_skeleton_2026_05_05.md` define 30-session user protocol. State 1+2 mount layer (Tier 2) is the precondition. Phase E perfect baseline protocol + EEG audio cue latency fix landed.

7. **HF promote time-gated**: clm 2026-05-06T23:26Z window, Pβ 2026-05-07T03:48Z window. Auto-fire scripts at `state/anima_hf_promotes_2026_05_06_auto_fire.bash` + `state/anima_hf_cleanups_2026_05_07_auto_fire.bash`. own 15 PRIVATE→PUBLIC lifecycle: PRIVATE first → verification gates → PUBLIC. Watchdog audit + pre-fire audit verdicts CLEAN.

---

## §5 Honest C3 (≥ 5)

1. **C3-A**: this manifest does NOT execute commits. raw#9 honest scope — task explicitly forbids commit, only emits manifest. User remains the fire-permission authority. Tier 1 commits (BG-BZ priority 5) inherit BG-BZ §3 HEREDOCs verbatim; this doc references but does not duplicate them.

2. **C3-B**: Group X-1 (`state/clm_v4_lora_sft_2026_05_05/corpus/slice_A_anima_30k.jsonl` 79 MB) **violates the `anima models + datasets HF-only (>5MB)` memory rule**. If user accidentally `git add state/clm_v4_lora_sft_2026_05_05/` without the per-file exclusion below, GitHub push will reject (100 MB hard limit) OR succeed but bloat repo. Recommended: add to `.gitignore` BEFORE any Tier 4/5 commit:
   ```
   state/clm_v4_lora_sft_2026_05_05/corpus/slice_A_anima_30k.jsonl
   state/anima_eeg_audio_cache_2026_05_05/*.aiff
   ```

3. **C3-C**: file-count arithmetic mismatch — total accounted in §2 is 437 of 465 untracked (28 unbound). I've assigned them to Tier 4 D-4 misc cluster, but the assignment is **judgment-call, not derived from a BG-cycle bind**. Honest description: 28 docs are spec/audit artifacts that don't have a clean BG-mapping back to today's cycle landings. User may prefer to bundle differently or drop some entirely (e.g., `anima_external_chat_enable_tools_audit` may be 어제-cycle residue).

4. **C3-D**: Group P (priority 5) re-verification on 2026-05-06 — 5 doc files all present, sizes 4-19 KB, healthy. **However**, the `anima_emerge_chat_entropy_trajectory_landed` doc was 7,255 bytes vs. the 5,818 bytes recorded in BG-BZ; size drift = 1.4 KB suggests subsequent edit. User should `git diff` if they want byte-exact reproduction of BG-BZ's planned commit.

5. **C3-E**: 4 conversation-context docs (`anima_session_2026_05_04_to_05_closure_audit_v3/v4`) are dated 2026-05-05 but describe yesterday's session — they may belong to **previous cycle's commit lane**, not today's. Honest verdict: bundle them into Tier 4 D-4 misc OR consider **NOT** committing if user prefers session-audit docs stay session-private.

6. **C3-F**: BG-BZ §3 contains full HEREDOC commit messages for Tier 1 P-1..P-5; this doc references rather than duplicating. If user runs Tier 1 by copy-paste from this doc, they will hit `git commit -m "..."` placeholders. They MUST open BG-BZ to copy the actual HEREDOC. Mitigation: this is intentional (DRY) but tradeoff-aware.

7. **C3-G**: Group X triage decisions in §3 are **recommendations, not commands**. Specifically the X-2 proposals/refinement 84 files from 2026-04-22 may be either (a) legitimately drifting cycle artifacts that need their own commit, or (b) build-product churn that should be `.gitignore`d. Verifying intent requires inspecting at least 2-3 sample files (`v25.json`, `v28.json`) — not done here. User triage required.

---

## §6 Output artifact paths

- this doc: `/Users/ghost/core/anima/docs/anima_2026_05_05_cycle_final_lock_token_audit_2026_05_05.md`
- verdict: `/Users/ghost/core/anima/state/anima_2026_05_05_cycle_final_lock_token_audit_2026_05_05/verdict.json`

raw#9 honest scope + raw#10 honest C3 + raw#15 additive PASS.
