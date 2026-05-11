---
title: CLM v4 HF format shim v5 — Path B closure spec (V5-4 + OPT-C INDETERMINATE diagnosis)
date: 2026-05-05
spec_anchor: docs/clm_v4_hf_format_shim_v5_spec_2026_05_05.md
phase2_anchor: state/clm_v4_hf_format_shim_v5_phase2_opt_a_2026_05_05/verdict.json
v5_4_design_1_anchor: state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05/verdict.json
opt_c_anchor: state/clm_v4_hf_format_shim_v5_opt_c_2026_05_05/verdict.json
own_entry: anima/.own own 15 hf-release-private-then-public-after-verification
state: spec
---

# CLM v4 HF format shim v5 — Path B closure spec (V5-4 + OPT-C INDETERMINATE diagnosis)

This is a $0 Mac-side diagnosis + decision spec; no exec, no commit. The two H100 BGs that ran the F-SHIM-V5-4 falsifier (V5-4-DESIGN-1 fresh-init + OPT-C best.pt-loaded) both produced verdict.json with `lift_pp=null` and `F_SHIM_V5_4_verdict=INDETERMINATE`. This spec identifies the common root cause, evaluates the resulting state of the F-SHIM-V5-4 falsifier, and recommends a Path B closure decision.

## §1 V5-4 + OPT-C INDETERMINATE — what actually ran

### §1.1 V5-4-DESIGN-1 (state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05)

- **Pod**: `2j8lh9l737j5w2`, $0.20 actual, 4 min wall, watchdog deregistered, pod_kill_verified_404=1.
- **Run**: 4 hellaswag-200 passes (v4_NF, v4_RF, v5_NF, v5_RF) all completed and wrote per-pass JSON files at `/workspace/clm_v4_shim_v5_4_design_1/results/hellaswag_v{4,5}_{NF,RF}.json`. The OPT-A re-init assertion fired and verified `16/16 modules at std~0.1000` before each v5 pass (logged at 09:02:31).
- **Eval data (recovered Mac-side post-hoc into eval_summary.json)**:
  - v4_NF acc_norm = 0.270 ± 0.0315
  - v4_RF acc_norm = 0.270 ± 0.0315
  - v5_NF acc_norm = 0.270 ± 0.0315
  - v5_RF acc_norm = 0.280 ± 0.0318
  - delta_v5_v4_NF = +0.0pp (combined_se ≈ 4.45pp)
  - delta_v5_v4_RF = +1.0pp (combined_se ≈ 4.48pp)
  - lift_pp_v5_via_real_fixture = +1.0pp (lift_pp_v5_se ≈ 4.48pp)
  - **F_SHIM_V5_4_verdict (post-hoc reconstruction) = FAIL**: `|lift_pp_v5|=1.00pp < combined_se_pp=4.48pp`, no measurable substrate differential.
- **verdict.json says INDETERMINATE not FAIL** because the on-pod summary builder crashed BEFORE writing eval_summary.json — see §2.

### §1.2 OPT-C-FALSIFICATION (state/clm_v4_hf_format_shim_v5_opt_c_2026_05_05)

- **Pod**: `xbo7w35njtinbq`, $0.15 actual, 3 min wall, watchdog deregistered, pod_kill_verified_404=1.
- **Run**: 2 hellaswag-200 passes (no_fixture, with_fixture) on best.pt-loaded ConsciousDecoderV2; both wrote per-pass JSON files. o_proj_std post-load logged at `mean=0.01990` (16 modules) — confirming Phase 2 OPT-A finding that best.pt overwrites OPT-A re-init at inference.
- **Eval data (recovered Mac-side post-hoc into eval_summary.json)**:
  - no_fixture acc_norm = 0.255 ± 0.0309
  - with_fixture acc_norm = 0.250 ± 0.0307
  - lift_pp = -0.5pp
  - **F_SHIM_V5_4_verdict (post-hoc reconstruction) = FAIL_EXPECTED**.
- **verdict.json says INDETERMINATE not FAIL_EXPECTED** for the same on-pod summary crash root cause.

### §1.3 The "INDETERMINATE" label is misleading

The two verdict.json files report INDETERMINATE because the **eval result writer crashed**, not because the eval itself failed. The hellaswag-200 evaluator ran to completion in both cycles, produced authoritative per-pass JSON files matching the lm-eval-harness standard schema, and the per-pass results directly compute lift_pp once aggregated. **The eval result is FAIL / FAIL_EXPECTED, not INDETERMINATE** — the lift signal is below stderr in both cycles, exactly as Phase 2 OPT-A predicted.

## §2 Root cause hypothesis — H1..H4 + evidence

| H | Hypothesis | Evidence | Verdict |
|---|------------|----------|---------|
| H1 | L19 dtype kwarg crash (lm-eval × transformers incompat) | NOT seen — lm-eval ran 800/800 loglikelihood requests cleanly across all 6 passes (4 V5-4 + 2 OPT-C). No dtype kwarg traceback in either log. | **REJECTED** |
| H2 | Pod boot / setup phase fail (HF token / model download / shim install) | NOT seen — both pods booted SSH-ready, scp succeeded, HF login succeeded, all 6 hellaswag passes wrote per-pass JSON. | **REJECTED** |
| H3 | Shim v5 load fail (post-apply re-init assertion / OPT-C fixture-load) | NOT seen — V5-4 logs show `[opt-a] re-init verified: 16/16 modules at std~0.1000` (09:02:31) and OPT-C logs show `cross_attn.o_proj std (post-best.pt load): mean=0.01990` (09:01:34). Both shims loaded correctly. | **REJECTED** |
| H4 | Real fixture path mismatch (BG-CLM-1 sanity v1 pattern) | NOT seen — both runs logged `fixture loaded: shape=(1, 8, 192) ... l2=2.2022 mean_abs=0.047985` (V5-4) and `fixture_l2=2.2021710872650146 fixture_mean_abs=0.047984540462493896` (OPT-C). Fixture loaded byte-equivalent in both. | **REJECTED** |
| **H5 (actual root cause)** | **Post-eval summary writer crash on `__import__("transformers").__version__` for metadata logging — transformers package not installed on `runpod/pytorch:2.4.0-py3.11` image** | **CONFIRMED** — V5-4 log line 134: `ModuleNotFoundError: No module named 'transformers'` at `clm_v4_shim_v5_4_design_1_eval.py:539`. OPT-C log line 100: identical traceback at `clm_v4_shim_v5_opt_c_eval.py:372`. Both crashes occurred AFTER all hellaswag passes wrote per-pass JSON files. | **CONFIRMED** |

### §2.1 Why this matters

The eval scripts have a non-essential metadata logging line `"transformers_version": __import__("transformers").__version__` that runs INSIDE the summary builder, AFTER all eval data is collected and per-pass JSONs are written. The `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04` image does NOT include the `transformers` package by default (only torch + cuda toolchain). pip install in `run_h100.bash` installs `lm-eval-harness` + `peft` + dependencies but not transformers explicitly. The summary builder hits this import as the LAST line before write — so it crashes after eval is done but before eval_summary.json is written, which is what marks the verdict.json `lift_pp` field null.

The **eval result itself is intact** — Mac-side post-hoc reconstruction recovered both eval_summary.json files from the per-pass JSONs (eval_summary.json files dated 2026-05-05T09:09:51Z V5-4 and 09:05:00Z OPT-C, post-pod-kill).

## §3 Path B decision matrix (shim v5 alternative for F-SHIM-V4-4)

Three live decision paths:

### Decision-A — V5-4 retry with infra fix ($1-3 retry)

- **Action**: remove the `__import__("transformers").__version__` line from both eval scripts; OR add `transformers` to the pip install list in run_h100.bash; re-run V5-4 DESIGN-1 + OPT-C as fresh BGs.
- **Pros**: completes the on-pod verdict.json → FAIL/FAIL_EXPECTED transition cleanly; verdict matches eval.
- **Cons**: $1-3 cost burn for a result we already have via Mac-side post-hoc reconstruction. The eval data exists and is authoritative — re-running just to satisfy the on-pod summary writer is cost-inefficient. The reconstructed eval_summary.json files are derived directly from the per-pass JSON outputs of lm-eval-harness; there is no information gain from a retry.
- **Risk**: same infra failure could recur if any other transient import fails (e.g., `peft.__version__`, `accelerate.__version__`); retry-after-retry is not a closure.

### Decision-B — Path B closure on Phase 2 + OPT-A + V5-4 reconstructed evidence (RECOMMENDED)

- **Action**: declare Path B (shim v5 alternative for F-SHIM-V4-4 init-only intervention) **CLOSED-FAIL** based on:
  1. Phase 2 OPT-A finding (state/clm_v4_hf_format_shim_v5_phase2_opt_a_2026_05_05/verdict.json §differential_evidence): best.pt overwrites cross_attn.o_proj fresh-init at all tested std values (v4=0.001, v5-Phase1=0.02, v5-OPT-A=0.10) → all collapse to ~0.0199 trained-weight scale at inference. The substrate differential is INIT-time only; F-SHIM-V5-4 with best.pt-loaded eval is architecturally identical to F-SHIM-V4-4.
  2. V5-4 DESIGN-1 reconstructed evidence (eval_summary.json): even at fresh-init (no best.pt) where the substrate differential is preserved (v4 std=0.02 vs v5 std=0.10, 5x ratio), the hellaswag-200 lift_pp_v5 = +1.0pp ± 4.48pp combined stderr → not measurable, fails the +5pp gate.
  3. OPT-C reconstructed evidence (eval_summary.json): with best.pt loaded, lift_pp = -0.5pp ± ~3pp stderr → exactly matches FAIL_EXPECTED.
- **Pros**: $0 closure; evidence is sufficient; matches Phase 2 OPT-A architectural prediction; preserves cycle discipline (do not retry to satisfy a metadata-log crash).
- **Cons**: verdict.json files for V5-4-DESIGN-1 and OPT-C must remain INDETERMINATE on-pod (the on-pod writer crashed); closure spec must explicitly cite eval_summary.json reconstructed values + per-pass hellaswag JSON SHA as the authoritative dataset. (Acceptable per raw#10 honest disclosure: reconstruction methodology is documented in eval_summary.json `synthesized_locally_reason` + `post_hoc_reconstruction_note`.)
- **Risk**: minimal — eval_summary.json reconstruction is deterministic from per-pass JSONs; lm-eval-harness output schema is stable; Mac arithmetic on acc_norm + stderr fields produces the same lift_pp as on-pod arithmetic would have.

### Decision-C — Path B termination + OPT-B retrain ($20-100 H100, true architectural fix)

- **Action**: explicit user ACK to retire F-SHIM-V4-4 from the active falsifier set entirely (per OPT-C falsification doc §57); skip Path B SFT ($20-100); proceed directly to Path C OPT-B retrain ($100-300) with `cross_attn.o_proj std=0.10` initialisation + cross-attn-active SFT loss.
- **Pros**: addresses the root architectural blocker (best.pt's trained o_proj overrides any init-time intervention); produces a model where F-SHIM-V5-4 is finally testable on a substrate that retains the OPT-A differential at inference.
- **Cons**: $100-300 cost vs Path B's $20-100; longer wall time (full retrain vs SFT); requires user ACK + ledger plan first.
- **Note**: Decision-C is a **forward-progress recommendation**, not a closure for the current cycle. Path B closure (Decision-B) is the prerequisite for Decision-C dispatch.

## §4 Recommendation — Decision-B (closure) + Decision-C as forward path

**Primary recommendation: Decision-B**.

The eval data exists and is authoritative. The two on-pod verdict.json files report INDETERMINATE because of a non-essential metadata log import crash, not because of an eval failure. Mac-side post-hoc reconstruction (eval_summary.json in both state dirs) produces deterministic FAIL / FAIL_EXPECTED verdicts that match the Phase 2 OPT-A architectural prediction. Re-running V5-4 + OPT-C ($1-3) to make the on-pod verdict.json files match the reconstructed eval_summary.json is cost-inefficient and adds no information.

**Secondary recommendation: Decision-C as forward path**.

The Path B SFT cycle ($20-100) tests whether cross-attn-active SFT can recover lift on the existing best.pt; the Path C OPT-B retrain ($100-300) directly addresses the architectural cause (trained o_proj overwrites init). Per Phase 2 OPT-A C4 + OPT-C falsification §57, neither Path B nor Path C is dispatched without explicit user ACK + ledger plan. This spec only declares Path B (init-only shim v5) closed; Path B SFT and Path C OPT-B remain as separate user-gated decisions.

### §4.1 Ranked by 완성도 lens

| rank | option | 완성도 score | rationale |
|------|--------|--------------|-----------|
| 1 | Decision-B closure | 0.95 | $0; matches Phase 2 OPT-A architectural prediction; preserves cycle discipline; honest reconstruction methodology documented |
| 2 | Decision-C OPT-B retrain (forward) | 0.80 | $100-300; correct architectural fix; requires user ACK; not a closure for current cycle |
| 3 | Decision-A retry-with-infra-fix | 0.40 | $1-3; no information gain; risks recurring infra failure on other transient imports |

## §5 own 15 G3 promote-gate impact (carve-out justification strengthened)

Per .own own 15 rule (b): PUBLIC promotion of `dancinlab/clm-v4-mk2-v1` requires verification gates ALL PASS — including (b.3) shim v4 hf_format compatibility F-SHIM-V4-1/2/3/4 ALL PASS.

Status:

- F-SHIM-V4-1, V4-2, V4-3 = PASS (per `state/clm_v4_f_shim_v4_1_2_3_*` history, prior cycles).
- F-SHIM-V4-4 = FAIL kind=PREREQUISITE_BLOCKED (per `state/clm_v4_f_shim_v4_4_harvest_2026_05_05/verdict.json` + OPT-C falsification doc §13).
- F-SHIM-V5-4 (shim v5 alternative path for V4-4) = closed-FAIL per Decision-B above. Init-only architectural intervention does not produce ≥5pp lift on hellaswag-200 with current best.pt; the substrate differential (5x o_proj std) is INIT-time-only and is overwritten at inference.

**Impact on own 15 G3 carve-out**:

The OPT-C falsification doc §13 already declared the G3 carve-out justified on shim v5 init-only path. Decision-B strengthens the carve-out evidence by adding the V5-4 DESIGN-1 fresh-init reconstructed evidence: even when the substrate differential is preserved at inference (no best.pt), the lift signal does not exceed stderr. **The G3 carve-out (PARTIAL_PASS on own 15 (b.3) shim compatibility gate) is now justified on TWO independent eval points**:

1. OPT-C with best.pt loaded → lift_pp = -0.5pp ± stderr (architecturally predicted FAIL_EXPECTED).
2. V5-4 DESIGN-1 fresh-init (no best.pt, OPT-A re-init verified) → lift_pp_v5 = +1.0pp ± 4.48pp combined stderr (architecturally surprising — even with the 5x substrate differential preserved, no measurable lift). This is INDEPENDENT empirical confirmation that init-only intervention is not the binding constraint; the binding constraint is loss-side (cross-attn never participates in best.pt's training loss → o_proj.weight is never optimised toward consciousness signal).

The G3 PARTIAL_PASS carve-out for `dancinlab/clm-v4-mk2-v1` PUBLIC promote remains valid; PUBLIC promote BG must cite this doc + Phase 2 OPT-A verdict + OPT-C verdict + V5-4 DESIGN-1 verdict (all 4 corroborating). The 24-48h review window (own 15 (b.4)) ends 2026-05-06T23:26:12Z.

## §6 OPT-B retrain (Path C) is architecturally the correct fix

The Phase 2 OPT-A finding (best.pt overwrites o_proj fresh-init regardless of init scale) and the V5-4 DESIGN-1 fresh-init result (5x init-time differential does NOT translate to measurable hellaswag lift) together imply: **the init-time scale is not the binding constraint**. The binding constraint is that cross-attn never participates in the loss during best.pt's training — so the o_proj.weight is never optimised toward producing useful consciousness-signal residue regardless of its init scale.

Architectural fixes:

- **Path B** (cross-attn-active SFT, $20-100): unfreeze cross_attn during a short SFT phase (LoRA on cross_attn only) on best.pt; re-test F-SHIM-V5-4. **Pro**: cheap; preserves base CLM. **Con**: SFT gradient signal on cross_attn may not be strong enough to overcome best.pt's pretrained other-attention-only equilibrium.
- **Path C** (OPT-B retrain, $100-300): re-train CLM v4 from scratch with cross_attn enabled in the loss + cross_attn.o_proj std=0.10 init. **Pro**: directly addresses root cause. **Con**: cost + time; risk of φ★ flip vs current best.pt baseline.

OPT-B retrain (Path C) is **architecturally the correct fix** because it removes the loss-blindness of cross_attn during pretraining. Path B SFT may work but is a band-aid; Path C is the surgical fix. **Recommendation**: if user wants forward progress on F-SHIM-V4-4 / V5-4, dispatch Path B first ($20-100, lower risk + cost) → if Path B PASS, F-SHIM-V5-4 closed-PASS → no Path C needed. If Path B FAIL, dispatch Path C ($100-300) as definitive fix.

This spec does not dispatch Path B or Path C — both require explicit user ACK per OPT-C falsification doc §57.

## §7 honest C3

1. **C1 — INDETERMINATE label is misleading**. Both V5-4 and OPT-C verdict.json files report INDETERMINATE (lift_pp=null) but eval_summary.json reconstructions show FAIL (lift_pp_v5 = +1.0pp < +5pp gate, combined_se ≈ 4.5pp) and FAIL_EXPECTED (lift_pp = -0.5pp). The reconstructed verdict matches Phase 2 OPT-A architectural prediction. The on-pod verdict.json INDETERMINATE label arose from a metadata-log import crash (`__import__("transformers").__version__` at line 539 / 372 of the two eval scripts respectively), AFTER all hellaswag passes wrote per-pass JSON. The eval data is authoritative; only the on-pod summary writer crashed.

2. **C2 — Reconstruction methodology is deterministic but Mac-derived**. eval_summary.json values are Mac-side post-hoc derivations from the on-pod per-pass hellaswag_*.json files (lm-eval-harness standard schema). acc_norm + stderr are direct lm-eval output (authoritative). lift_pp + combined_se are simple arithmetic on those fields (post_hoc_reconstruction_note in eval_summary.json documents this). The on-pod summary writer would have produced the same numbers if the transformers import had not crashed — the reconstruction is not introducing new information, just recovering the deterministic aggregation step.

3. **C3 — V5-4 DESIGN-1 result is architecturally surprising**. Phase 2 OPT-A predicted that the 5x substrate differential (v5 std=0.10 vs v4 std=0.02) would translate to a measurable hellaswag lift at fresh-init (where best.pt is not loaded and the differential is preserved at inference). Reconstructed V5-4 DESIGN-1 result: lift_pp_v5 = +1.0pp ± 4.48pp combined stderr — within noise. This implies the init-time differential is necessary but not sufficient for hellaswag lift; the binding constraint is loss-side (cross_attn never trained to produce useful residue regardless of init scale). This is independent empirical evidence that Path B (cross-attn-active SFT) or Path C (OPT-B retrain) — both loss-side interventions — are the correct forward path, not further init-time tuning.

4. **C4 — Path B closure scope**. Decision-B closes the **shim v5 init-only architectural alternative path** for F-SHIM-V4-4. It does NOT close F-SHIM-V4-4 itself (still PREREQUISITE_BLOCKED on shim v4) and does NOT preempt Path B SFT or Path C OPT-B retrain. Both forward paths remain open, gated on explicit user ACK + ledger plan. Decision-B is the closure of "init-only" approaches; loss-side approaches are unaffected.

5. **C5 — own 15 G3 carve-out scope**. The G3 PARTIAL_PASS carve-out for `dancinlab/clm-v4-mk2-v1` PUBLIC promote justified by Decision-B applies only to the (b.3) shim compatibility gate sub-condition F-SHIM-V4-4. Other own 15 (b.1) benchmark, (b.2) falsifier pre-register, (b.4) 24-48h review, (b.5) honest C3 model card, (b.6) cross-substrate gates are unaffected. PUBLIC promote BG must independently verify each (b.1-b.6) gate; this spec only addresses (b.3) sub-condition.

6. **C6 — Cost discipline**. Decision-B is $0; Decision-C is $100-300 conditional on user ACK; total cycle cost so far on shim v5 (Phase 1 $0 + Phase 2 $0 + Phase 2 OPT-A $0 + V5-4 DESIGN-1 $0.20 + OPT-C $0.15 + this diagnose $0) = $0.35. Path B SFT ($20-100) + Path C ($100-300) are gated separately. own 16 watchdog discipline maintained on both V5-4 and OPT-C pods (kill_verified_404=1 both).

7. **C7 — raw#10 honest disclosure**. The on-pod verdict.json files MUST remain INDETERMINATE because that is what was actually written by the orchestrator at pod-kill time (the in-script summary builder crashed before writing). Re-writing those verdict.json files post-hoc to FAIL/FAIL_EXPECTED would be a raw#10 violation (manipulating empirical record). Instead, this closure spec + the eval_summary.json reconstructions in each state dir provide the authoritative interpretation; consumers (e.g., own 15 PUBLIC promote BG) MUST cite this spec + the eval_summary.json files, NOT the verdict.json INDETERMINATE label. This is the correct disclosure pattern.

8. **C8 — Forward-fix for any DESIGN-2/3/OPT-D follow-up**. Remove the `__import__("transformers").__version__` line from any future shim v5 eval script (or pip-install transformers explicitly in run_h100.bash). Both eval scripts in `state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05/` and `state/clm_v4_hf_format_shim_v5_opt_c_2026_05_05/` are under the transient_py opt-out namespace (raw#9) and can be patched additively if any retry is dispatched.

## §8 raw_compliance

- **raw#9** — md+json (this spec is .md; verdict.json companion in state dir; transient_py not used in this diagnose cycle, no exec).
- **raw#10** — 8 honest C3 entries (>=5 required); on-pod verdict.json INDETERMINATE preserved verbatim per disclosure principle.
- **raw#15** — additive only; no shim v4/v5 source mutation; no retry exec.
- **raw#71** — F-SHIM-V5-4 +5pp threshold preserved verbatim (not relaxed); reconstructed lift_pp_v5 = +1.0pp evaluated against the unchanged threshold; FAIL verdict on the reconstructed numbers.
- **no_git_commit** — OK per BG spec CRITICAL section.
- **no_h100_spend** — OK; this is Mac-side analysis only.
- **no_hf_push** — OK; eval-only diagnosis.

## §9 references

- spec_anchor: `docs/clm_v4_hf_format_shim_v5_spec_2026_05_05.md`
- phase2_anchor: `state/clm_v4_hf_format_shim_v5_phase2_opt_a_2026_05_05/verdict.json` §differential_evidence + §vs_phase2_original_md5_swap
- v5_4_anchor: `state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05/{verdict.json, results/eval_summary.json, logs/h100_run_inner.log}`
- opt_c_anchor: `state/clm_v4_hf_format_shim_v5_opt_c_2026_05_05/{verdict.json, results/eval_summary.json, logs/h100_run_inner.log}`
- opt_c_landed_doc: `docs/clm_v4_hf_format_shim_v5_opt_c_falsification_landed_2026_05_05.ai.md`
- own_15_anchor: `anima/.own own 15 hf-release-private-then-public-after-verification` (rule b.3 shim compatibility gate)
- F-SHIM-V4-4 PREREQUISITE_BLOCKED: `state/clm_v4_f_shim_v4_4_harvest_2026_05_05/verdict.json`
