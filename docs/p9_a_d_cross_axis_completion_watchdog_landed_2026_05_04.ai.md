# P9 A vs D Cross-Axis Completion Watchdog — LANDED 2026-05-04

## TL;DR

Live watchdog (PID 43833, 24h budget, 5min poll) monitors BOTH Path A r=16 mitigation verdict AND Path D 25K Phi-star verdict. On both-landed, auto-fires `tool/p9_a_d_cross_axis_verdict.hexa` to produce 4-cell matrix verdict + per-cell next-cycle recommendation.

## Status

- **Watchdog PID 43833**: alive, iter=1 polled at 2026-05-04T05:30:54Z
  - `A=WAIT:fallback_status_TRAINING_IN_PROGRESS_3SEED` (3-seed retrain still running)
  - `D=MISSING` (eval not yet run on H100 ckpts)
- **Cross-axis hexa selftest**: PASSed (sister BG ac9d8e81)
- **Trigger condition**: BOTH must reach VALID terminal label

## Files

- `tool/p9_a_d_cross_axis_completion_watchdog.hexa` — canonical hexa (~430 LoC, raw#9 hexa-only Mac)
- `state/p9_a_d_cross_axis_2026_05_04/watchdog_loop.sh` — shell-loop wrapper (5min poll, 24h budget)
- `state/p9_a_d_cross_axis_2026_05_04/watchdog.pid` — PID file (43833)
- `state/p9_a_d_cross_axis_2026_05_04/watchdog_shell.log` — append-only shell log
- `state/p9_a_d_cross_axis_2026_05_04/watchdog_log.jsonl` — JSONL append-only hexa log
- `state/markers/p9_a_d_cross_axis_completion_watchdog_live.marker` — marker

On trigger fire (both verdicts present):
- `state/p9_a_d_cross_axis_2026_05_04/verdict.json` — cross-axis 4-cell matrix verdict (from cross-axis hexa)
- `state/p9_a_d_cross_axis_2026_05_04/recommendation.json` — per-cell next-cycle commission recommendation
- `state/p9_a_d_cross_axis_2026_05_04/cell_classification.json` — cell + a_pass/d_pass + cost ceiling band
- `state/p9_a_d_cross_axis_2026_05_04/dispatch.json` — dispatch audit
- `state/p9_a_d_cross_axis_2026_05_04/notify_payload.json` — notify stub

## Trigger Conditions

GUARD-3 (success-signal checklist) — BOTH must satisfy:

1. **Path A**: file exists + parses + label is terminal (NOT *_in_progress / *_launching / *_provisioning / *_pending)
   - Primary: `state/p9_path_a_r16_eval_pipeline_2026_05_03/mitigation_comparison.json` -> `mitigation_verdict` in {MITIGATION_PASS, MITIGATION_PARTIAL, MITIGATION_FAIL_*}
   - Fallback: `state/p9_path_a_r16_3seed_2026_05_04/verdict.json` -> `status` or `verdict.label` not training/launching
2. **Path D**: `state/p9_paradigm_d_25k_eval_2026_05_03_verdict.json` -> `n_ckpts_evaluated > 0` AND `ranking[0].composite.verdict` in {SUCCESS_D, PARTIAL_D, FAIL_D}

## 4-Cell Matrix Mapping (per spec sec.5)

| Cell | A verdict | D verdict | Action | Cost ceiling |
|------|-----------|-----------|--------|--------------|
| I_BOTH_AXES_LIVE | PASS | PASS (no F2 breach) | A_UNION_D_ADDITIVE: stack both LoRA recipes on one substrate | $300-600 |
| II_CHAT_LIVE_ONLY | PASS | FAIL_D | SHIP_A_PLUS_D_ROOT_CAUSE: ship A LoRA, commission D autopsy | $0-50 |
| III_PHI_LIVE_ONLY | FAIL/PARTIAL | PASS | SHIP_D_PLUS_A_DEBUG: ship D LoRA, commission A debug cycle | $50-150 |
| IV_BOTH_NOISE | FAIL/PARTIAL | FAIL_D | ABLATION_MATRIX_ONLY: NO further LoRA, paradigm-rethink ablation | $100-200 |
| UNDETERMINED | missing/parse_error | missing/parse_error | WAIT (re-run after both land) | $0 |

## Dispatch Chain (3 steps)

1. **a_verdict_shim**: emit `state/p9_a_d_cross_axis_2026_05_04/a_verdict_shim.json` mapping mitigation_comparison.json schema (or 3seed verdict.json) into p9_a_prime/verdict/1 schema (CHAT_PASS_v3 / CHAT_FAIL_v3 expected by cross-axis hexa)
2. **cross_axis_hexa**: `hexa run tool/p9_a_d_cross_axis_verdict.hexa` with shim + D verdict env -> `verdict.json`
3. **classify_and_recommend**: parse matrix_cell from verdict.json, emit `recommendation.json` + `cell_classification.json`

## raw#10 honest C3 — 3 caveats

**C1 — depends on both verdicts landing**: 24h max-wait sized for r=16 3-seed completion (4-8h ETA from 04:42Z launch) + D 25K H100 (~6-8h ETA from 22:08Z launch). If only one lands within 24h budget, watchdog timeouts (UNDETERMINED never fires). Manual re-run required after second verdict lands; no auto-extend.

**C2 — cross-axis hexa selftest is on synthetic data**: Cell mapping rules (CHAT_PASS_v3 -> A_PASS, SUCCESS_D/PARTIAL_D no F2 breach -> D_PASS) were validated only against unit-test fixtures. The mitigation_comparison.json schema differs from p9_a_prime verdict schema (mitigation_verdict not f1_v3); watchdog adapts via env-mapping shim (step 1). First real-cycle run may surface edge cases — operator should validate dispatch.json + verdict.json before authorizing follow-up.

**C3 — recommendation is opinion**: Per-cell next-cycle plan + cost ceiling bands are derived from spec sec.5 cost ceilings as of 2026-05-04 (H100 SXM ~$2.99/hr, A100 ~$1.50/hr). Cost figures must be re-verified against current GPU spot market before commissioning. Plans are NOT pre-registered falsifiers; operator validates against latest budget posture.

## Constraints

- raw#9 STRICT: Mac-side hexa-only; canonical hexa is SSOT for trigger logic; shell wrapper = OS-level supervisor
- raw#15 SSOT: `tool/p9_a_d_cross_axis_completion_watchdog.hexa` is single source for cross-axis trigger semantics
- raw#10: 3 caveats explicit
- $0 watchdog: no GPU spend; no pod rentals; cross-axis hexa runs on Mac

## Sister BGs

- **ac9d8e81**: cross-axis verdict hexa (`tool/p9_a_d_cross_axis_verdict.hexa`) — already landed + selftest PASS
- **PID 49397**: `path_a_r16_completion_watchdog --loop --apply` — emits primary trigger via `mitigation_comparison.json`
- **PID 53327**: `d_25k_completion_watchdog --loop --apply` (v2 wrapper) — emits primary trigger via `p9_paradigm_d_25k_eval_2026_05_03_verdict.json`

## Next Actions

- Watchdog polls every 5min until 2026-05-05T05:30Z; fires 3-step dispatch on first BOTH-VALID iter
- On dispatch: cell label written to `dispatch.json` triggers wrapper exit
- If timeout: manual respawn or re-run `hexa run tool/p9_a_d_cross_axis_completion_watchdog.hexa --once --apply` after both verdicts land
