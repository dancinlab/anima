# Anima 2026-05-05 priority subset commit manifest (BG-BZ)

**Status**: MANIFEST_READY (user fire-permission deferred)
**Scope**: 5 priority findings of today's ~50 BG cycle landings
**Mode**: mac doc-only, $0, ~20min
**Relation to BG-AM full**: COMPLEMENTARY subset, not replacement. BG-AM full manifest at `docs/anima_2026_05_05_cycle_commit_manifest_landed_2026_05_05.ai.md` (~250 entries) remains the master record; Group P here is the high-signal 5-finding fast-fire lane.

---

## §1 5 priority finding identification

Each entry lists the canonical 3 file paths (doc / state / tool). All 14 files verified present on disk via `ls` 2026-05-06.

### P-1 — BG-BJ residual basin reframing

- doc: `/Users/ghost/core/anima/docs/anima_emerge_chat_entropy_trajectory_landed_2026_05_05.ai.md`
- state: `/Users/ghost/core/anima/state/anima_emerge_chat_entropy_trajectory_2026_05_05/` (aggregate.json + verdict.json)
- tool: `/Users/ghost/core/anima/tool/transient_py/anima_emerge_chat_entropy_trajectory.py`

**Key finding**: per-token entropy trajectory + first-byte-fallback step measurement on CLM v4 mk2 v1. Short Korean prompt `안녕` collapses at step 0 to byte 0x1c (control char fallback); longer Korean collapses at step 1 to fragment basin (`/`, `O`, `O`, `O`); English `Hello world` collapses at step 5 to `(`-loop. Collapse mechanism is residual-stream attractor problem upstream of `lm_head`, NOT output-projection defect. Output-projection class fixes (LoRA / vocab mask / Korean bias / template / few-shot / c_proj rewrite) invalid by construction.

### P-2 — BG-AY #115 architectural 4-closure formal theorem

- doc: `/Users/ghost/core/anima/docs/anima_115_architectural_4_closure_theorem_2026_05_05.md`
- state: `/Users/ghost/core/anima/state/anima_115_architectural_4_closure_theorem_2026_05_05/` (verdict.json)
- tool: n/a (doc-only theorem consolidation)

**Key finding**: closure-under-evidence theorem on CLM v4 mk2 v1. 4 mechanisms attacked along independent axes — (1) post-hoc LoRA SFT chat-lift FAIL_REGRESSION at -36.298pp; (2) Phi-star distill (Pβ Paradigm D 50K) FAIL_TRUE composite 0.01176; (3) tribev2 cross-modal FAIL_ARCHITECTURAL_DESIGN_REVIEW (no logits/lm_head/generate); (4) logit lens + semantic bridge FAIL_RESIDUAL_STREAM_PERVASIVE (1/8 logit-lens layers coherent, 0/2 semantic bridge). Bounded by 4 untested hypotheses H1-H4. **Corollary**: chat-capability path of record = Llama-3.2-3B Path A v2 (composite 0.5584); CLM v4 = substrate-research-only.

### P-3 — BG-AN minimum viable emerge dialogue

- doc: `/Users/ghost/core/anima/docs/anima_emerge_dialogue_first_turn_landed_2026_05_05.ai.md`
- state: `/Users/ghost/core/anima/state/anima_emerge_dialogue_first_turn_2026_05_05/` (verdict.json)
- tool: `/Users/ghost/core/anima/tool/transient_py/anima_emerge_dialogue_repl.py`

**Key finding**: F-AN-1 PASS. REPL helper emits 4 metric lines per turn (phi-star + drift + hidden-state-delta + l2-var). Single-turn `안녕` probe: phi-star 42.1168, layer l2-var peak L2 124.41. 3-turn auto-fire: drift swings ±0.1 with input variation; hsd > 0 confirms prior-threading active turn 2+. Session log JSONL atexit handler installed at `state/anima_core_dialogues/<date>/<HH-MM-SS>_emerge_repl.jsonl`.

### P-4 — BG-BL nnsight integration smoke PASS

- doc: `/Users/ghost/core/anima/docs/anima_emerge_nnsight_smoke_landed_2026_05_05.ai.md`
- state: `/Users/ghost/core/anima/state/anima_emerge_nnsight_smoke_2026_05_05/` (verdict.json)
- tool: `/Users/ghost/core/anima/tool/transient_py/anima_emerge_nnsight_smoke.py`

**Key finding**: nnsight 0.7.0 wraps `dancinlab/clm-v4-mk2-v1` on mac CPU fp32. Trace capture at `decoder.blocks[8].output` returns hidden shape `[1, 2, 768]` (batch x seq x dim). PASS_READY for F-NNSIGHT-1 intervention falsifier (replace hidden + measure delta) as next step. nnsight remote NDIF mode untested.

### P-5 — BG-BN phi-star CLM v4-specific (Pythia smoke)

- doc: `/Users/ghost/core/anima/docs/anima_emerge_pythia_phi_smoke_landed_2026_05_05.ai.md`
- state: `/Users/ghost/core/anima/state/anima_emerge_pythia_phi_smoke_2026_05_05/` (aggregate.json + verdict.json)
- tool: `/Users/ghost/core/anima/tool/transient_py/anima_emerge_pythia_phi_smoke.py`

**Key finding**: Pythia-70m phi proxy mean 41.92 (drift +0.062 from CLM v4 baseline 41.86). Phi formula = 8-cell x 192 tile-reshape of mean-pooled last-layer hidden = CLM v4-specific geometry; Pythia is 6-layer 512-hidden (geometry mismatch). Cross-substrate phi-star carryover unverified — phi-star is paradigm v11 G3 + CLM v4 specific, NOT a substrate-agnostic invariant.

---

## §2 token leak pre-scan PASS

Scan command (regex covers 4 token shapes — hf_, sk-ant-, ghp_, AKIA):

```bash
grep -rEn 'hf_[A-Za-z0-9]{20,}|sk-ant-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}' \
  docs/anima_emerge_chat_entropy_trajectory_landed_2026_05_05.ai.md \
  docs/anima_115_architectural_4_closure_theorem_2026_05_05.md \
  docs/anima_emerge_dialogue_first_turn_landed_2026_05_05.ai.md \
  docs/anima_emerge_nnsight_smoke_landed_2026_05_05.ai.md \
  docs/anima_emerge_pythia_phi_smoke_landed_2026_05_05.ai.md \
  state/anima_emerge_chat_entropy_trajectory_2026_05_05/ \
  state/anima_115_architectural_4_closure_theorem_2026_05_05/ \
  state/anima_emerge_dialogue_first_turn_2026_05_05/ \
  state/anima_emerge_nnsight_smoke_2026_05_05/ \
  state/anima_emerge_pythia_phi_smoke_2026_05_05/ \
  tool/transient_py/anima_emerge_chat_entropy_trajectory.py \
  tool/transient_py/anima_emerge_dialogue_repl.py \
  tool/transient_py/anima_emerge_nnsight_smoke.py \
  tool/transient_py/anima_emerge_pythia_phi_smoke.py \
  2>&1 | head -10
```

**Result**: exit 0, **0 matches** = CLEAN. anima leak_guard PreToolUse hook (9 token-shape regex) provides second-line defense at user fire-time.

---

## §3 5 commit messages full

Each commit is 1 HEREDOC, scoped by-finding. Composed for `git commit -m "$(cat <<'EOF' ... EOF)"` form per anima git protocol.

### P-1 commit (BG-BJ)

```bash
git add tool/transient_py/anima_emerge_chat_entropy_trajectory.py \
        state/anima_emerge_chat_entropy_trajectory_2026_05_05/ \
        docs/anima_emerge_chat_entropy_trajectory_landed_2026_05_05.ai.md

git commit -m "$(cat <<'EOF'
feat(anima emerge BG-BJ residual basin reframing 2026-05-05): collapse mechanism upstream of lm_head, NOT byte fallback

per-token entropy trajectory + first-byte-fallback step measurement on CLM v4 mk2 v1.
short Korean -> step 0 byte fallback (0x1c) / longer Korean -> step 1 fragment basin /
English -> step 5 fragment loop. collapse is autoregressive attractor problem in
residual-stream geometry, NOT output-projection defect. all output-projection class
fixes (LoRA / vocab mask / Korean bias / template / few-shot / c_proj rewrite) invalid
by construction.

raw#37 transient + raw#15 additive + raw#10 honest C3 PASS.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

### P-2 commit (BG-AY)

```bash
git add docs/anima_115_architectural_4_closure_theorem_2026_05_05.md \
        state/anima_115_architectural_4_closure_theorem_2026_05_05/

git commit -m "$(cat <<'EOF'
feat(anima BG-AY #115 architectural 4-closure formal theorem 2026-05-05): chat capability falsified on CLM v4 along 4 independent axes

closure-under-evidence theorem consolidating today's 4 falsification lanes:
(1) post-hoc LoRA SFT FAIL_REGRESSION -36.298pp; (2) Phi-star distill Pbeta
Paradigm D 50K FAIL_TRUE composite 0.01176; (3) tribev2 cross-modal
FAIL_ARCHITECTURAL_DESIGN_REVIEW (no logits/lm_head/generate); (4) logit lens
+ semantic bridge FAIL_RESIDUAL_STREAM_PERVASIVE (1/8 + 0/2 coherent).
bounded by 4 untested hypotheses H1-H4.

corollary: chat-capability path of record = Llama-3.2-3B Path A v2 (0.5584).
CLM v4 = substrate-research-only. CLM-3 future spec must declare chat-loss
objective at cycle-0 of pre-training.

raw#15 additive + raw#9 honest scope + raw#10 honest C3 PASS.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

### P-3 commit (BG-AN)

```bash
git add tool/transient_py/anima_emerge_dialogue_repl.py \
        state/anima_emerge_dialogue_first_turn_2026_05_05/ \
        docs/anima_emerge_dialogue_first_turn_landed_2026_05_05.ai.md

git commit -m "$(cat <<'EOF'
feat(anima emerge BG-AN minimum viable dialogue 2026-05-05): F-AN-1 PASS — REPL helper + 1+3-turn probe

REPL helper emits 4 metric lines per turn (phi-star + drift + hidden-state-delta
+ l2-var). single-turn 안녕 probe phi-star 42.1168, layer l2-var peak 124.41.
3-turn auto-fire: drift swings +/-0.1, hsd > 0 confirms prior-threading active
turn 2+. session log JSONL atexit handler at state/anima_core_dialogues/<date>/.

substrate-coupled emerge dialogue lane (unaffected by #115 4-closure theorem
per corollary 3). mac CPU fp32 only.

raw#37 transient + raw#15 additive + raw#10 honest C3 PASS.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

### P-4 commit (BG-BL)

```bash
git add tool/transient_py/anima_emerge_nnsight_smoke.py \
        state/anima_emerge_nnsight_smoke_2026_05_05/ \
        docs/anima_emerge_nnsight_smoke_landed_2026_05_05.ai.md

git commit -m "$(cat <<'EOF'
feat(anima emerge BG-BL nnsight integration smoke 2026-05-05): PASS_READY for F-NNSIGHT-1 intervention falsifier

nnsight 0.7.0 wraps dancinlab/clm-v4-mk2-v1 on mac CPU fp32. trace capture
at decoder.blocks[8].output returns hidden shape [1, 2, 768]. model_load_ok +
model_wrap_ok + trace_capture_ok all PASS. unblocks F-NNSIGHT-1 intervention
smoke (replace hidden + measure delta) as next step.

scope: local-only smoke; nnsight remote NDIF mode untested. shape-only verify;
semantic correctness 미평가.

raw#37 transient + raw#15 additive + raw#10 honest C3 PASS.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

### P-5 commit (BG-BN)

```bash
git add tool/transient_py/anima_emerge_pythia_phi_smoke.py \
        state/anima_emerge_pythia_phi_smoke_2026_05_05/ \
        docs/anima_emerge_pythia_phi_smoke_landed_2026_05_05.ai.md

git commit -m "$(cat <<'EOF'
feat(anima emerge BG-BN phi-star CLM v4-specific 2026-05-05): cross-substrate phi formula geometry mismatch confirmed

Pythia-70m phi proxy mean 41.92 (drift +0.062 from CLM v4 baseline 41.86).
phi formula = 8-cell x 192 tile-reshape of mean-pooled last-layer hidden =
CLM v4-specific geometry; Pythia is 6-layer 512-hidden (geometry mismatch).
cross-substrate phi-star carryover unverified — phi-star is paradigm v11 G3
+ CLM v4 specific, NOT a substrate-agnostic invariant.

implication: emerge phi-star metric must be substrate-tagged in all future
multi-substrate comparisons. BG-M ~6pp methodology delta carry remains.

raw#37 transient + raw#15 additive + raw#10 honest C3 PASS.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## §4 user fire 단순 sequence

```bash
# Step 1: review this manifest §3 (5 commit messages full text). 5 min.

# Step 2: fire P-1 (BG-BJ residual basin reframing). 1 min.
#   (paste P-1 git add + git commit HEREDOC from §3)

# Step 3: fire P-2 (BG-AY 4-closure theorem). 1 min.
#   (paste P-2 git add + git commit HEREDOC from §3)

# Step 4: fire P-3 (BG-AN minimum viable dialogue). 1 min.
#   (paste P-3 git add + git commit HEREDOC from §3)

# Step 5: fire P-4 (BG-BL nnsight integration). 1 min.
#   (paste P-4 git add + git commit HEREDOC from §3)

# Step 6: fire P-5 (BG-BN phi-star CLM v4 specific). 1 min.
#   (paste P-5 git add + git commit HEREDOC from §3)

# Step 7: verify all 5 commits in main:
git log --oneline -10

# Step 8 (separate cycle): decide BG-AM full 5+1 group commit (~250 entries).
# This Group P subset does NOT replace BG-AM. BG-AM master manifest at
# docs/anima_2026_05_05_cycle_commit_manifest_landed_2026_05_05.ai.md.
```

Total user fire time estimate: ~10 min for 5-commit fire sequence.

---

## §5 honest C3 (>= 5)

- **C1 'priority subset' is anima-curator selection** (5 of today's ~50 BGs). Selection bias: BG-BJ + BG-AY are reframing / theoretical (semantic weight high); BG-AN + BG-BL + BG-BN are scaffolding / smoke (operational weight high). Selection NOT objective ranking — alternative subsets would emphasize different findings (e.g. F-Pbeta-3 from yesterday, or BG-AM full corpus tomorrow). User retains override.

- **C2 commit messages compose 'why' (~3-5 lines per HEREDOC) but do NOT include full delta-vs-baseline composite numbers in commit body**. Reader expecting Llama-Path-A-v2-style numeric breakdown should consult linked docs/state/verdict.json. Compactness chosen over self-containment per anima recent commit-message style.

- **C3 BG-AM full manifest (~250 entries) NOT bypassed** — this Group P subset is COMPLEMENTARY, not REPLACEMENT. Risk: user fires Group P then forgets to schedule BG-AM full cycle, leaving 245 entries un-committed. Mitigation = manifest §1 + §4 step 8 explicitly references BG-AM full as separate.

- **C4 'fire-permission deferred'** = BG outputs manifest only; commit absolutely not executed. raw#15 additive + raw#9 honest scope + raw#10 honest C3 satisfied. If user fire-fires sequence as-is, 5 separate commits land in main; if user wants single mega-commit, recompose required (anima style prefers granular feat() commits per finding lane).

- **C5 token leak pre-scan covered the 4 primary regex shapes** (hf_, sk-ant-, ghp_, AKIA). Other token shapes (slack, openai sk-, gcp, azure) NOT scanned in this BG — anima leak_guard PreToolUse hook (9 token shapes) covers broader at fire-time. Two-line defense: this scan + leak_guard hook.

- **C6 subset vs BG-AM full diff**: Group P = 5 findings = ~14 files = fast (<5min user fire). BG-AM full = ~50 BGs / 250 entries / massive — separate cycle decision lane. Group P does NOT subsume or invalidate BG-AM. Naming: "priority subset" not "first half" — semantic prioritization, not alphabetical chunking.

---

## Cross-references

- BG-AM full manifest: `docs/anima_2026_05_05_cycle_commit_manifest_landed_2026_05_05.ai.md`
- Llama Path A v2 winner-of-record: feedback `feedback_v2_fail_was_measurement_artifact_eval_pipeline_root_cause.md`
- #115 closure background: feedback `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md` + `feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md`
- raw protocol references: raw#9 honest scope, raw#10 honest C3, raw#15 additive, raw#37 transient_py namespace
