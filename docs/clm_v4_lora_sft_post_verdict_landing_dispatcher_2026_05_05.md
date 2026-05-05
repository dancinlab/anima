# CLM v4 + LoRA SFT — post-verdict landing dispatcher

- **ts_utc**: 2026-05-05T_BG-CLM-2-FOLLOWUP-SCENARIOS
- **bg_lane**: CLM-2-FOLLOWUP-SCENARIOS (companion to scenario decision tree; **$0, mac, no exec, no commit**)
- **status**: DISPATCHER_LANDED — design only; consumed at BG-CLM-2-EXEC verdict-emit time
- **scope**: 1-paragraph routing rules + concrete `Agent({...})` invocation templates per scenario
- **scenario tree**: `docs/clm_v4_lora_sft_post_verdict_decision_tree_2026_05_05.md` (read FIRST for trigger conditions + implications)
- **raw**: raw#9 (md only), raw#10 (≥5 honest C3 in scenario doc; this dispatcher inherits), raw#15 (additive)

---

## §1 — Routing rule (1 paragraph)

When `state/clm_v4_lora_sft_2026_05_05/verdict.json` lands (sentinel `__P9_CLM_V4_LORA_SFT__ <STATUS>`), read `lane_status` + `F_CLM_LORA_{1..5}` + `composite_delta_pp` + `phi_star_post_lora` + `forgetting_index` from the verdict payload. **If** `lane_status == "V2_EVAL_CRASHED"` OR verdict.json is missing OR all eval fields are null **→ launch B5 (S5)**. **Else if** `F_CLM_LORA_3 == "FAIL"` OR `phi_star_post_lora < +10` OR `lane_status == "V2_FAIL_EARLY_STOP"` OR `F_CLM_LORA_1 == "FAIL"` OR `forgetting_index >= 0.05` **→ launch B4 (S4)**. **Else if** `F_CLM_LORA_2 == "FAIL"` AND `composite_delta_pp < -0.5` **→ launch B3 (S3)**. **Else if** `F_CLM_LORA_2 == "PARTIAL"` OR (`F_CLM_LORA_2 == "PASS"` AND `-0.5 <= composite_delta_pp <= +0.5`) **→ launch B2 (S2)** (and optionally B2' under USER ACK). **Else if** `F_CLM_LORA_2 == "PASS"` AND `composite_delta_pp > 0.5` AND `F_CLM_LORA_3 == "PASS"` **→ launch B1 + B1' (S1)** (B1 under USER ACK; B1' parallel $0). The routing prefers `F_CLM_LORA_*` status fields over computed delta-pp where they disagree (per scenario tree §7 honest C3 #9), and the S4 trigger (φ★ / forgetting health) takes precedence over S1/S2/S3 (substrate-health gates substrate-comparison) regardless of F2 status.

### 1.1 Routing decision flow (precedence-ordered)

```text
verdict_loaded = read("state/clm_v4_lora_sft_2026_05_05/verdict.json")

# Tier 0: infra failure (highest precedence)
if verdict_loaded is None or verdict.lane_status == "V2_EVAL_CRASHED":
    if adapter_exists_and_sha256_verifies():
        scenario = "S5a"  # eval-only rerun
        bg = "B5"
    elif training_partial_or_crashed():
        scenario = "S5b"  # full retrain
        bg = "B5b"
    else:
        scenario = "S5c"  # pod hung; full retrain
        bg = "B5b"
    halt_routing()

# Tier 1: substrate-health gate (φ★ / forgetting must be intact)
elif (verdict.F_CLM_LORA_3 == "FAIL"
      or verdict.phi_star_post_lora < 10
      or verdict.lane_status == "V2_FAIL_EARLY_STOP"
      or verdict.F_CLM_LORA_1 == "FAIL"
      or verdict.forgetting_index >= 0.05):
    if verdict.phi_star_post_lora <= 0:
        scenario = "S4a"  # φ★ flipped
    elif 0 < verdict.phi_star_post_lora < 10:
        scenario = "S4b"  # φ★ degraded
    else:
        scenario = "S4c"  # forgetting only
    bg = "B4"
    halt_routing()

# Tier 2: substrate comparison (only if substrate is healthy)
elif verdict.F_CLM_LORA_2 == "FAIL" and verdict.composite_delta_pp < -0.5:
    scenario = "S3"
    bg = "B3"

elif (verdict.F_CLM_LORA_2 == "PARTIAL"
      or (verdict.F_CLM_LORA_2 == "PASS" and -0.5 <= verdict.composite_delta_pp <= 0.5)):
    scenario = "S2"
    bg = "B2"  # B2' optional under USER ACK

elif (verdict.F_CLM_LORA_2 == "PASS"
      and verdict.composite_delta_pp > 0.5
      and verdict.F_CLM_LORA_3 == "PASS"):
    scenario = "S1"
    bg = "B1+B1'"  # B1 under USER ACK; B1' parallel $0

else:
    scenario = "AMBIGUOUS"  # fall to manual USER review
    bg = None
```

---

## §2 — `Agent({...})` invocation templates per scenario

These are scaffolds. Substitute `{verdict_field}` placeholders with actual values at dispatch time. All run via `Agent` with `run_in_background=true` (per memory `feedback_always_subagent_bg`); parallel BGs serialize git via worktree (per memory `feedback_parallel_bg_git_race`).

### 2.1 S1 → B1 (5-seed scaleup) + B1' (HF release prep)

**B1 invocation template** (USER ACK required first; cost $25–75):

```text
Agent({
  description: "BG-CLM-3-5SEED-SCALEUP",
  run_in_background: true,
  prompt: """
## BG-CLM-3-5SEED-SCALEUP: CLM v4 + LoRA 5-seed cross-validation — $25-75, H100, ~10-12h aggregate

Working in `/Users/ghost/core/anima` on macOS. Spec landing first ($0, mac); H100 EXEC under USER ACK.

### USER ACK STATUS
USER acknowledged $25-75 cost on {ack_ts} for B1 launch.

### Predecessor verdict
state/clm_v4_lora_sft_2026_05_05/verdict.json: V2_PASS, composite_delta_pp={delta_pp_actual}pp,
F1=PASS, F2=PASS, F3=PASS, F4={f4_status}, F5=PASS.

### Why
Single-seed PASS at composite_delta_pp={delta_pp_actual}pp; per scenario tree §1 (S1) +
honest C3 #7, single-seed signal noisy at 1-2pp. 5-seed cross-val required for
"substrate validated" claim.

### Seeds (LOCKED — raw#71 re-pre-registration)
- 20260504 (already run; reuse adapter from state/clm_v4_lora_sft_2026_05_05/results/adapter_final/)
- 20260505, 20260506, 20260507, 20260508 (4 NEW; reuse spec §3 hyperparameters verbatim except seed)

### Hyperparams
Copy from docs/clm_v4_lora_sft_spec_2026_05_04.md §3 verbatim:
- Base: need-singularity/clm-v4-mk2-v1
- LoRA: r=32, alpha=64, dropout=0.05
- target_modules: decoder.blocks.{0..15}.attn.{q,k,v,o}_proj (self-attn ONLY)
- LR=3e-5, cosine warmup=300, max_steps=6000, save_steps=1000
- micro_batch=8, grad_accum=4 (eff_batch=32), seq_len=512, bf16
- Slice D = 0% (deferred); 60/30/10 mix only

### PASS aggregate
- 5-of-5 seeds composite_delta_pp > 0 → STRICT_PASS
- mean > 0 with 95%CI lower > -0.5pp → PERMISSIVE_PASS (default; tighter test optional per scenario tree §7 C3 #7)

### Output
- state/clm_v4_lora_sft_5seed_2026_05_06/seed_{N}/verdict.json (×5)
- state/clm_v4_lora_sft_5seed_2026_05_06/aggregate_verdict.json
- docs/clm_v4_lora_sft_5seed_landed_2026_05_06.ai.md

### CRITICAL
- DO NOT git commit until aggregate verdict landed
- DO NOT push to HF Hub (B1' handles pre-flight; actual upload requires SECOND USER ACK post-aggregate)
- raw#9, raw#10 (≥5 honest C3), raw#15
"""
})
```

**B1' invocation template** (parallel; $0; no USER ACK):

```text
Agent({
  description: "BG-CLM-2-HF-RELEASE-PREP",
  run_in_background: true,
  prompt: """
## BG-CLM-2-HF-RELEASE-PREP: HF release pre-flight for clm-v4-mk2-lora-v1 — $0, mac, ~1h

Working in `/Users/ghost/core/anima` on macOS.

### Why
S1 V2_PASS (single-seed). Pre-stage HF release artifacts in parallel with B1 5-seed scaleup.
B1' is DRY-RUN only; actual upload gated on B1 aggregate PASS (per scenario tree §7 C3 #8).

### Tasks
1. Build model card via tool/hf_readme_template.md scaffold for need-singularity/clm-v4-mk2-lora-v1
2. Document adapter-merged shape, tokenizer dependency, trust_remote_code=True requirement
3. Pre-stage tool/hf_upload_mk2.hexa run-config (DRY-RUN; no upload)
4. Land docs/clm_v4_lora_release_prep_2026_05_06.md with USER ACK gate for actual upload

### Output
- HF release prep doc + model card draft
- tool/hf_upload_mk2.hexa DRY-RUN config

### CRITICAL
- DO NOT actually push to HF Hub
- DO NOT commit
- raw#9, raw#15 additive only
"""
})
```

### 2.2 S2 → B2 (parity amendment) + optional B2' (3-seed confidence)

**B2 invocation template** ($0; no USER ACK):

```text
Agent({
  description: "BG-CLM-2-PARITY-AMENDMENT",
  run_in_background: true,
  prompt: """
## BG-CLM-2-PARITY-AMENDMENT: CLM-2 verdict re-frame from differentiator to parity — $0, mac, ~1h

Working in `/Users/ghost/core/anima` on macOS.

### Predecessor verdict
state/clm_v4_lora_sft_2026_05_05/verdict.json: lane_status={lane_status_actual},
F2={f2_actual}, composite_delta_pp={delta_pp_actual}pp (parity band).

### Tasks
1. Amend `.roadmap.p9_sft.cond.clm_v4_lora_sft` → status=v2_pass_parity (sibling JSONL line, additive only per raw#15)
2. Land docs/clm_v4_lora_sft_parity_amendment_2026_05_06.ai.md with substrate-equivalence claim + ≥5 honest C3
3. If F-CLM-LORA-4 == PASS, propagate "axis-cond preserved on substrate-correct base" finding to L26-L27 lessons block in cross-link to docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md
4. Update tool/p9_a_d_cross_axis_verdict.hexa cross-substrate matrix: 3-way (Llama / CLM-LORA / Paradigm-D) with PARITY label on CLM-LORA cell

### Output
- Roadmap amendment line (JSONL parse-verified post-edit)
- Parity amendment landing doc
- Cross-axis verdict matrix update (additive)

### CRITICAL
- DO NOT git commit
- raw#15 additive only — original spec land doc UNTOUCHED
- raw#10 ≥5 honest C3
- ROADMAP-SHIFTING: this amendment changes substrate-hypothesis claim direction; per scenario tree §7 C3 #5, dispatcher recommends optional USER notification before launch (informational, not gating)
"""
})
```

**B2' invocation template** (optional; $15–45; USER ACK required):

```text
Agent({
  description: "BG-CLM-2-PARITY-CONFIDENCE-3SEED",
  run_in_background: true,
  prompt: """
## BG-CLM-2-PARITY-CONFIDENCE-3SEED: 3-seed parity-band confidence — $15-45, H100, ~6-9h

### USER ACK STATUS
USER acknowledged $15-45 cost on {ack_ts} for B2' launch (optional, per scenario tree §2.5).

### Why
PARITY claim from single seed has wide stderr (~±2pp). 3-seed yields tighter CI on parity claim
WITHOUT over-investing in a substrate that has no demonstrated lift.

### Seeds
20260505, 20260506, 20260507 (3 NEW; original 20260504 reused)

### PASS criterion (re-pre-registered for parity scope; raw#71)
- mean composite_delta_pp 95%CI overlaps 0 (consistent with PARITY)
- AND mean within ±2pp of Llama Path A v2 composite (within stderr)

### Output
- state/clm_v4_lora_parity_3seed_2026_05_06/aggregate_verdict.json
- docs/clm_v4_lora_parity_3seed_landed_2026_05_06.ai.md

### CRITICAL
- raw#9, raw#10, raw#15
"""
})
```

### 2.3 S3 → B3 (regression closure)

**B3 invocation template** ($0; no USER ACK; informational notification):

```text
Agent({
  description: "BG-CLM-2-REGRESSION-CLOSURE",
  run_in_background: true,
  prompt: """
## BG-CLM-2-REGRESSION-CLOSURE: CLM v4 SFT lane closure + Llama-primary roadmap amendment — $0, mac, ~1h

Working in `/Users/ghost/core/anima` on macOS.

### Predecessor verdict
state/clm_v4_lora_sft_2026_05_05/verdict.json: lane_status=V2_FAIL,
F2=FAIL, composite_delta_pp={delta_pp_actual}pp negative (anima < Llama).

### Tasks
1. Amend `.roadmap.p9_sft.cond.clm_v4_lora_sft` → status=v2_fail_regression (sibling JSONL, additive only)
2. Re-prioritize `.roadmap.p9_sft.cond.path_a_retrain_v2` → primary SFT lane (upgrade from TRUE_PASS_W_F4_DEFERRED_TO_CLM2 to TRUE_PASS_PRIMARY)
3. Re-cast F4 amendment doc (docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md):
   - Sibling AMENDMENT entry: "F4 deferral resolved as substrate venue collapsed; F4 question deferred to next axis-conditioned substrate (BLM phase-5? — out of scope this cycle)"
   - Preserve original strict-FAIL label (per F4 amendment §5 C3 #1: strict label not retroactively overturned)
4. Land docs/clm_v4_lora_sft_regression_closure_2026_05_06.ai.md with full implication chain + ≥5 honest C3
5. CLM v4 retained in roadmap as `cond.clm_v4_substrate_research` (φ★ / axis-cond / consciousness primitive ONLY; NOT chat/SFT)

### Output
- Roadmap amendments (2 lines: CLM-2 closure + Path A primary; both JSONL parse-verified)
- Regression closure landing doc
- F4 amendment cross-link sibling entry

### CRITICAL
- DO NOT git commit
- raw#15 additive only
- raw#10 ≥5 honest C3
- DO NOT delete CLM v4 substrate research artifacts (φ★, axis-cond fixtures retained)
- ROADMAP-SHIFTING: substrate-uniqueness-as-SFT-advantage hypothesis falsified; per scenario tree §7 C3 #5, dispatcher recommends optional USER notification before launch
"""
})
```

### 2.4 S4 → B4 (refined-HP retry)

**B4 invocation template** (USER ACK required; cost $5–10):

```text
Agent({
  description: "BG-CLM-2-RETRY-REFINED-HP",
  run_in_background: true,
  prompt: """
## BG-CLM-2-RETRY-REFINED-HP: CLM v4 LoRA retry with refined HP — $5-10, H100, ~2h

Working in `/Users/ghost/core/anima` on macOS. Spec amendment first ($0); retry EXEC under USER ACK.

### USER ACK STATUS
USER acknowledged $5-10 cost on {ack_ts} for B4 retry EXEC.

### Predecessor verdict
state/clm_v4_lora_sft_2026_05_05/verdict.json:
- Sub-scenario: {S4a|S4b|S4c}
- φ★ post-LoRA: {phi_star_post_lora_actual} (threshold +10)
- forgetting_index: {forgetting_index_actual}
- F1={f1_status}, F3={f3_status}

### Refined HP (LOCKED — raw#71 re-pre-registration)
| Param | BG-CLM-2 (failed) | BG-CLM-2-RETRY-REFINED-HP |
|---|---|---|
| LR | 3e-5 | **1e-5** (3× lower) |
| LoRA dropout | 0.05 | **0.10** (2× higher regularization) |
| target_modules | qkvo (16 layers × 4) | **qkv only** (drop o_proj per spec §5 F-CLM-LORA-4 FAIL action) |
| max_steps | 6000 | **4000** (33% shorter) |
| save_steps | 1000 | **500** (finer early-stop) |
| φ★ probe cadence | pre/post only | **pre+post + every 1000 steps** |
| φ★ abort threshold | +10 | **+15** |

### Sub-scenario routing
- S4a (φ★ ≤ 0): retry MANDATORY (substrate must be recoverable; if retry also flips, HOLD for next-cycle re-design)
- S4b (0 < φ★ < 10): retry RECOMMENDED
- S4c (forgetting only): retry OPTIONAL — alternative is Slice D consciousness-coupled inclusion (5%) instead of HP retune; USER may select alternative at ACK time

### Output
- docs/clm_v4_lora_sft_retry_refined_hp_spec_2026_05_06.md
- state/clm_v4_lora_sft_retry_2026_05_06/verdict.json
- docs/clm_v4_lora_sft_retry_landed_2026_05_06.ai.md

### CRITICAL
- adapter from BG-CLM-2 (failed cycle) MUST be archived to state/clm_v4_lora_sft_2026_05_05/adapter_aborted/ (NOT deleted; post-mortem evidence)
- DO NOT reuse adapter weights — fresh LoRA init from base
- raw#9, raw#10, raw#15
"""
})
```

### 2.5 S5a → B5 (eval-only rerun); S5b/S5c → B5b (full retrain)

**B5 invocation template** (S5a; $1–3; no USER ACK; USER notified):

```text
Agent({
  description: "BG-CLM-2-EVAL-FIX",
  run_in_background: true,
  prompt: """
## BG-CLM-2-EVAL-FIX: CLM v4 LoRA eval-only rerun on saved adapter — $1-3, H100, ~30min

Working in `/Users/ghost/core/anima` on macOS.

### USER NOTIFIED (under $5 ACK threshold)
Cost $1-3; USER notified informationally per scenario tree §5.5.

### Predecessor crash root cause
state/clm_v4_lora_sft_2026_05_05/run.log analyzed:
- Crash class: {dtype_kwarg|lm_eval_version|task_config|other}
- Adapter sha256: {adapter_sha256_actual} (saved at state/clm_v4_lora_sft_2026_05_05/results/adapter_final/)

### Why (mirrors α'''-EVAL-FIX pattern)
- Pattern source: state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json
- Diagnose: dtype kwarg (L19), transformers version pin, lm-eval task config
- Fix: pin transformers>=4.51,<4.60 if dtype kwarg; lm-eval version match if task config drift
- Add: PEFT load + forward smoke test pre-bench (L14 lesson)
- Re-eval: load adapter, run F1-F5 + composite, emit fresh verdict

### Pre-flight
1. Verify adapter sha256 matches state/clm_v4_lora_sft_2026_05_05/results/adapter_final/ (immutable)
2. Diagnose eval crash root cause via state/clm_v4_lora_sft_2026_05_05/run.log
3. Apply fix; smoke test on Mac before pod launch ($0 fail-fast)

### Output
- state/clm_v4_lora_sft_eval_rerun_2026_05_06/verdict.json
- docs/clm_v4_lora_sft_eval_rerun_landed_2026_05_06.ai.md

### Post-rerun: re-route to S1/S2/S3/S4 per refreshed verdict
After verdict.json lands, dispatcher re-runs §1 routing flow against refreshed payload.

### CRITICAL
- raw#9, raw#10, raw#15
"""
})
```

**B5b invocation template** (S5b/S5c; USER ACK required; $6–10):

```text
Agent({
  description: "BG-CLM-2-RETRAIN",
  run_in_background: true,
  prompt: """
## BG-CLM-2-RETRAIN: CLM v4 LoRA full retrain (training crashed) — $6-10, H100, ~2-2.5h

Working in `/Users/ghost/core/anima` on macOS.

### USER ACK STATUS
USER acknowledged $6-10 cost on {ack_ts} for B5b retrain.

### Predecessor crash class
- S5b: training crashed mid-flight; partial or no adapter
- S5c: pod hung / SCP failed; artifacts unrecoverable

state/clm_v4_lora_sft_2026_05_05/run.log root-cause:
{root_cause_actual}

### Why
Re-EXEC BG-CLM-2 from spec (docs/clm_v4_lora_sft_spec_2026_05_04.md) verbatim with crash-fix applied.

### Tasks
1. Diagnose original crash via run.log
2. Apply fix (pod boot SCP sentinel, transient script harden)
3. Re-launch BG-CLM-2-EXEC with same spec, same hyperparams, same seed=20260504

### Output
- state/clm_v4_lora_sft_retrain_2026_05_06/verdict.json (overwrites/sibling original)
- docs/clm_v4_lora_sft_retrain_landed_2026_05_06.ai.md

### CRITICAL
- DO NOT modify spec hyperparameters (raw#71 — only re-pre-registration permits HP changes; this is INFRA fix only)
- raw#9, raw#10, raw#15
- L11 cleanup BG guards (verb classification, pre+post pod state)
- L13 trap pre-kill scp
"""
})
```

---

## §3 — Tie-break rules for ambiguous verdicts

When verdict fields disagree (e.g., F2=PASS but composite_delta_pp=+0.3 in PARITY band), dispatcher applies these tie-breaks (in order):

1. **F status field wins over computed delta** — if `F_CLM_LORA_2 == "PASS"`, route to S1 even if delta is in [+0.5, +0.5] PARITY band; if `F_CLM_LORA_2 == "PARTIAL"`, route to S2.
2. **Substrate-health (F1, F3, forgetting) precedence over substrate-comparison (F2)** — if F1 OR F3 OR φ★ OR forgetting fail, S4 fires regardless of F2 status.
3. **lane_status precedence over individual F fields** — if `lane_status == "V2_EVAL_CRASHED"`, S5 fires regardless of partial F values.
4. **AMBIGUOUS verdict → manual USER review** — if no scenario triggers cleanly (e.g., F2=PASS but F4=FAIL on substrate-correct base creates a "S1-with-axis-broken" sub-branch not enumerated), dispatcher emits `__P9_CLM_V4_LORA_SFT_DISPATCHER__ AMBIGUOUS_VERDICT` and pauses. USER manually selects scenario. (Per scenario tree §7 C3 #1.)

---

## §4 — USER ACK gate summary

| Scenario | BG | Cost | USER ACK | Notes |
|---|---|---|---|---|
| S1 | B1 | $25–75 | **YES** | required before launch |
| S1 | B1' | $0 | NO | parallel; DRY-RUN only |
| S2 | B2 | $0 | NO | informational notification recommended (roadmap-shifting) |
| S2 | B2' | $15–45 | **YES** | optional; required if launched |
| S3 | B3 | $0 | NO | informational notification recommended (substrate hypothesis falsified) |
| S4 | B4 | $5–10 | **YES** | conservatively gated at $5 boundary |
| S5a | B5 | $1–3 | NO | USER notified |
| S5b/c | B5b | $6–10 | **YES** | retrain required |

---

## §5 — Failure modes of dispatcher itself

1. **verdict.json schema drift** — if BG-CLM-2-EXEC emits fields with different names than §0 of scenario tree assumes, routing fails. Dispatcher must `KeyError`-tolerate and emit `AMBIGUOUS_VERDICT` rather than mis-route. Mitigation: dispatcher includes a schema validation step BEFORE routing.

2. **verdict.json emit timing race** — if dispatcher reads verdict.json while it's being written (partial JSON), parse fails. Mitigation: dispatcher polls for `state/clm_v4_lora_sft_2026_05_05/verdict.json.complete` sentinel marker first; only reads payload after marker exists.

3. **multi-BG git race** — B1 (5-seed) and B1' (HF release prep) launched in parallel both write to `state/` and `docs/` and `tool/`. Per memory `feedback_parallel_bg_git_race`, parallel BGs sharing working tree race git index. Mitigation: dispatcher launches B1 + B1' as separate `git worktree` per BG OR serializes commits via the queue mechanism. Dispatcher does NOT auto-commit; both BGs follow `DO NOT git commit` rule.

4. **USER ACK timing** — USER ACK gate is enforced at BG prompt time, not at dispatcher routing time. Dispatcher routes; BG launches with `USER ACK STATUS` placeholder. Actual launch is gated on USER providing ACK in the launch turn. If USER does not ACK, BG does not run. Dispatcher must NOT auto-launch USER-ACK-required BGs without the explicit ACK.

5. **Scenario boundary edge cases** — see scenario tree §7 honest C3 #1, #9 for known boundary issues. Dispatcher §3 tie-breaks cover the common cases; rare cases route to AMBIGUOUS for manual review.

---

## §6 — References

- Scenario decision tree (read first): `docs/clm_v4_lora_sft_post_verdict_decision_tree_2026_05_05.md`
- BG-CLM-2-EXEC spec: `docs/clm_v4_lora_sft_spec_2026_05_04.md`
- BG-CLM-2-EXEC landed: `docs/clm_v4_lora_sft_landed_2026_05_05.ai.md`
- Verdict surface (in-flight): `state/clm_v4_lora_sft_2026_05_05/verdict.json`
- CLM v4 baseline: `state/clm_v4_baseline_eval_2026_05_05/verdict.json`
- Llama Path A v2 retry-3 anchor: `state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json`
- F4 substrate amendment: `docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md`
- α'''-EVAL-FIX pattern: same retry-3 verdict.json `eval_pipeline_root_cause_v3` + `eval_pipeline_fix_applied`
- Memory `feedback_always_subagent_bg`: ALL execution work via `Agent run_in_background=true`
- Memory `feedback_parallel_bg_git_race`: parallel BGs sharing working tree race git index; serialize via worktree
- Memory `feedback_completion_quality_recommendation`: every option presentation MUST include explicit ranked recommendation by 완성도 lens
