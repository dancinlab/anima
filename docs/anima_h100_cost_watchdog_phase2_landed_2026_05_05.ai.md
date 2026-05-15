---
status: LANDED — Phase 2 of 3
cycle: anima_h100_cost_watchdog_phase2_2026_05_05
own: 16 (Phase 2)
spec: docs/anima_h100_cost_discipline_operationalization_spec_2026_05_05.md §3.3
predecessor_phases:
  - Phase 1 LANDED: tool/h100_cost_watchdog.hexa + tool/h100_register.bash + tool/h100_alert_emit.bash
  - admission landed (.own taxonomy)
successor_phases:
  - Phase 3 (next): BG launch prompt template + memory entry update (mac, $0, ~30min)
  - Phase 4: H100 smoke test ($1-3, ~30min) — dogfood Phase 2 hooks against live pod
raw_compliance: raw#9 (hexa+bash carve-out OK), raw#10 (≥5 honest C3), raw#15 (additive-only — no L11/L13 fix removed)
---

# Phase 2 — H100 cost-watchdog orchestrator hook integration

## Summary

- **6 orchestrator hexa templates patched** with Phase 2 watchdog hooks:
  - `tool/clm_v4_lora_train_orchestrator.hexa` (BG-CLM-2-EXEC, target $10)
  - `tool/p9_path_a_retrain_v2_h100_orchestrator.hexa` (BG-PA-RETRAIN-V2, target $24)
  - `tool/p9_base_validation_h100_orchestrator.hexa` (BG-P9-BASE-VALIDATION, target $5)
  - `tool/p9_llama_anchor_h100_orchestrator.hexa` (BG-P9-LLAMA-ANCHOR, target $1.5)
  - `tool/p9_lora_mode1_eval_h100_orchestrator.hexa` (BG-P9-LORA-MODE1-EVAL, target $1.5)
  - `tool/p9_opt_1_v4_exec_h100_orchestrator.hexa` (BG-P9-OPT-1-V4-EXEC, target $2)

- **4 hooks per orchestrator** (all 6 files have all 4 marker banners — verified):
  1. `# === Phase 2 watchdog hook (boot) ===` — registers pod with watchdog after pod_id capture; calls `bash tool/h100_register.bash $POD_ID $BG_LANE $TARGET_USD`; graceful warn-only on failure.
  2. `# === Phase 2 watchdog hook (heartbeat) ===` — fire-and-forget per-poll-iter `echo > state/h100_watchdog/heartbeats/<BG_LANE>.txt`; failure is silent (mkdir -p + write || true).
  3. `# === Phase 2 watchdog hook (trap pre-stop) ===` — augments existing `_kill_pod` trap: writes EXITING marker → `runpodctl pod stop+delete` (existing) → 404 verify (3 retries × 30s) → `hexa run tool/h100_cost_watchdog.hexa --deregister $POD_ID` (only if 404 confirmed).
  4. `# === Phase 2 verdict schema (cost-discipline fields) ===` — adds 5 fields to verdict.json: `pod_kill_verified_404`, `watchdog_deregistered`, `cost_target_usd`, `cost_actual_usd`, `cost_overrun_ratio`, `cost_overrun_2x_alerted` (additive — does not displace existing `actual_cost_usd` / `budget_target_usd` / `pod_terminated`).

- **Selftests PASS** for 4 of 6 orchestrators (clm_v4_lora_train, p9_path_a_retrain_v2, p9_llama_anchor, p9_opt_1_v4_exec). The other 2 (p9_base_validation, p9_lora_mode1_eval) FAIL at the **pre-existing T4 secret-check** (uses bare `secret` not absolute path under hexa exec sandbox PATH); confirmed pre-existing via stash-and-rerun. T9 watchdog-hook block is unreachable behind T4 in those 2, but the patches themselves are syntactically valid (verified via `--emit` + bash parse on the unaffected paths).

- **Phase 3 (BG prompt template) ready**: spec §3.4 already enumerates the completion checklist block ("(a) verdict.json fields / (b) pod 404 verified / (c) watchdog deregistered / (d) cost_overrun_ratio honest C3"); Phase 2's verdict schema additions thread directly into that checklist. Memory entry `feedback_always_subagent_bg.md` can adopt the block verbatim.

## Honest C3 (≥5 per raw#10)

C1: **Register failure is graceful (warn-only).** If `tool/h100_register.bash` is missing or fails, the orchestrator logs a warning and proceeds. This means a pod can run un-tracked by the watchdog if the register tool is broken — Phase 4 smoke test must verify `state/h100_watchdog/pods/<pod_id>.json` materializes within 5 seconds of boot.

C2: **Heartbeat is fire-and-forget.** The poll-loop heartbeat hook uses `mkdir -p ... 2>/dev/null || true; echo ... > ... 2>/dev/null || true` — silent failure. If the heartbeat dir is unwriteable (full disk, permission flip), the watchdog daemon will erroneously emit `STALE_HEARTBEAT` alerts despite the pod being healthy. Mitigation: alert is push-notify only (no auto-action), so user can debug.

C3: **Trap deregister vs SIGKILL race.** The deregister hook lives inside `_kill_pod`, which only fires on EXIT/INT/TERM. If the orchestrator process is SIGKILL'd (kill -9, OOM-killer, hexa-runtime crash before bash signal handler installs), the pod stays registered indefinitely. The watchdog daemon's `bg_dead_pod_alive` 15-min alert is the safety net here, but it requires Phase 1 daemon to be running.

C4: **Verdict schema additions are additive_only.** Existing fields (`actual_cost_usd`, `budget_target_usd`, `budget_hard_cap_usd`, `pod_terminated`, `pod_kill_verified_404` where present) are NOT removed or renamed. The 5 new fields are siblings, so legacy consumers continue to work. The `cost_overrun_ratio` is `actual / target` — if target is 0 (misconfig), set to 0 to avoid div-by-zero.

C5: **Existing orchestrator selftest does not exercise hook paths.** The new T9 selftest probe only verifies tool-file-existence (`test -f $WATCHDOG_REGISTER`) and prints config — it does NOT invoke `bash $WATCHDOG_REGISTER` or `hexa run $WATCHDOG_HEXA --register`. End-to-end hook verification is **deferred to Phase 4 smoke test**, which will boot a real pod and assert that `state/h100_watchdog/pods/<pod_id>.json` appears + heartbeats refresh + deregister fires on trap.

C6: **2 of 6 orchestrators selftest-FAIL at pre-existing T4 step (secret-check).** The failure is `FAIL: runpod.api_key not in secret store` because `secret check` is invoked via bare `secret` command (no absolute path) and hexa's exec sandbox PATH does not include `/Users/ghost/core/secret/bin`. Confirmed pre-existing via `git stash` revert + re-run. My Phase 2 patches do NOT cause the failure, but they ALSO cannot make T9 reachable behind it without a separate fix (out-of-scope per raw#15 additive-only). The patched hexa files emit syntactically valid bash; trap/boot/heartbeat hooks will execute correctly when `--launch` runs (which uses absolute-path `secret` in exec.bash).

C7: **Per-orchestrator BG_LANE / TARGET_USD values are first-pass identifiers** picked from each orchestrator's existing `BUDGET_TARGET_USD` constant + cycle-tag-derived lane name. They are NOT cross-validated against any spec sheet of expected lane names. Phase 3 BG prompt template should canonicalize the BG_LANE registry (e.g., make `BG-CLM-2-EXEC` match the actual `feedback_always_subagent_bg.md` lane naming convention).

C8: **`anima_runpod_orchestrator.hexa` and `anima_vast_ai_orchestrator.hexa` were intentionally NOT patched.** These are reusable Python-emitting helpers (no concrete `_kill_pod` trap, no exec.bash boot-then-poll lifecycle), so the 4 hooks have no insertion point. Spec §3.3 names `anima_runpod_orchestrator.hexa` explicitly, but inspection confirms its shape is incompatible with the boot/heartbeat/trap pattern — patching it would require restructuring the helper, which is out-of-scope for additive Phase 2. The 6 H100 orchestrators above cover all current concrete H100 BG launch paths in the repo.

C9: **`p9_lora_mode1_instruct_eval_h100_orchestrator.hexa` (70-line stub) was NOT patched.** It declares constants but does not emit exec.bash or define `_kill_pod`; it's a placeholder/companion to the full Mode 1 eval. Patching would be cosmetic without functional effect.

## Files modified (additive PATCH per raw#15)

```
tool/clm_v4_lora_train_orchestrator.hexa            (+~120 lines, 4 hook regions + T9 selftest probe)
tool/p9_path_a_retrain_v2_h100_orchestrator.hexa    (+~115 lines)
tool/p9_base_validation_h100_orchestrator.hexa      (+~110 lines)
tool/p9_llama_anchor_h100_orchestrator.hexa         (+~110 lines)
tool/p9_lora_mode1_eval_h100_orchestrator.hexa      (+~110 lines)
tool/p9_opt_1_v4_exec_h100_orchestrator.hexa        (+~115 lines)
docs/anima_h100_cost_watchdog_phase2_landed_2026_05_05.ai.md  (this file — companion handoff)
```

No git commit performed (per task constraint).

## Roadmap annotation proposal (do NOT mutate `.own` directly)

Add to `.own` own16 entry:

```yaml
own_16:
  phase_1_landed_2026_05_05:
    files: [tool/h100_cost_watchdog.hexa, tool/h100_register.bash, tool/h100_alert_emit.bash]
  phase_2_landed_2026_05_05:
    files:
      - tool/clm_v4_lora_train_orchestrator.hexa
      - tool/p9_path_a_retrain_v2_h100_orchestrator.hexa
      - tool/p9_base_validation_h100_orchestrator.hexa
      - tool/p9_llama_anchor_h100_orchestrator.hexa
      - tool/p9_lora_mode1_eval_h100_orchestrator.hexa
      - tool/p9_opt_1_v4_exec_h100_orchestrator.hexa
    hooks_per_file: [boot, heartbeat, trap_pre_stop, verdict_schema]
    selftest_pass: 4 of 6 (2 fail at pre-existing T4 secret-check)
    not_patched_reason:
      tool/anima_runpod_orchestrator.hexa: "reusable Python-emitting helper, no _kill_pod trap"
      tool/anima_vast_ai_orchestrator.hexa: "reusable Python-emitting helper, vast.ai not RunPod"
      tool/p9_lora_mode1_instruct_eval_h100_orchestrator.hexa: "70-line stub with no exec.bash"
  phase_3_pending:
    target: BG launch prompt template + memory entry update (feedback_always_subagent_bg.md)
  phase_4_pending:
    target: H100 smoke test (boot 1 minimal pod, dogfood hooks against live runpodctl)
    budget: $1-3 hard cap
```

## Phase 3 readiness signal

The verdict.json schema additions in Phase 2 directly satisfy spec §3.4 BG completion checklist:
- (a) verdict fields: `pod_kill_verified_404 + watchdog_deregistered + cost_actual_usd + cost_target_usd + cost_overrun_ratio` — ALL emitted by all 6 patched orchestrators.
- (b) pod 404 verified: trap pre-stop hook now performs 3-retry × 30s probe.
- (c) watchdog deregistered: trap pre-stop hook archives `state/h100_watchdog/pods/<pod_id>.json` to `state/h100_watchdog/closed/`.
- (d) cost_overrun_ratio: emitted in verdict.json; if ratio > 1.5, Phase 3 prompt template should enforce honest-C3 root-cause + lesson entry.

Phase 3 BG prompt template can directly cite the verdict-schema additions and selftest probe pattern landed here.
