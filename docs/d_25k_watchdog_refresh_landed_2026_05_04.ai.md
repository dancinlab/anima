# D 25K Watchdog Refresh — LANDED 2026-05-04

## TL;DR

Refreshed D 25K H100 completion watchdog before 12h budget expiry. Old PID 94198 (started 2026-05-03T22:08Z, expires 2026-05-04T10:08Z, ~5h45m budget remaining at assessment) replaced with PID 53327 (started 2026-05-04T04:26Z, 24h budget, 5-min poll). Wrapper script for old watchdog had been deleted from disk (held alive only via bash fd 255r).

## Status

- **Old watchdog (PID 94198)**: SIGTERM'd at 2026-05-04T04:27:00Z (clean exit, no zombie)
- **New watchdog (PID 53327)**: alive, first poll verified at 2026-05-04T04:26:17Z, hexa_rc=0, all 3 signals MISSING (expected — H100 still training)
- **Trigger chain**: 4-step (ssh_run_all → scp → d_verdict → cross_axis) configured and selftested

## Files

- `state/d_25k_eval_auto_trigger_2026_05_03/watchdog_loop_v2.sh` — new wrapper (5min poll, 24h budget)
- `state/d_25k_eval_auto_trigger_2026_05_03/watchdog.pid.v2` — new pid file
- `state/d_25k_eval_auto_trigger_2026_05_03/watchdog_shell.log` — append log (continues from old)
- `state/d_25k_eval_auto_trigger_2026_05_03/watchdog_log.jsonl` — JSONL append log (continues)
- `state/d_25k_watchdog_refresh_2026_05_04/audit.json` — full audit
- `state/markers/d_25k_watchdog_refresh_landed.marker`
- `state/markers/d_25k_completion_watchdog_live.marker` — UPDATED (PID 94198 → 53327)
- `tool/d_25k_completion_watchdog.hexa` — UNCHANGED (canonical hexa)

## Trigger Conditions

GUARD-3 (success-signal checklist) — any 1 of 3 fires the chain:

1. **Local**: `state/p9_paradigm_d_25k_h100_2026_05_03/verdict.json` exists + parses + label ∈ {SUCCESS, PARTIAL, COMPLETE, ABORT, FAIL}
2. **Ubu1**: `ssh ubu1` to `/home/aiden/anima/state/p9_paradigm_d_25k_h100_2026_05_03/verdict.json` (same label set)
3. **HF**: `https://huggingface.co/api/models/need-singularity/clm-v4-paradigm-d-25k-final/tree/step-25000` returns http 200

## H100 Pod State (NOT TOUCHED)

- pod_id: `fuewrx9moxe6gz`, $2.99/hr H100 SXM
- started 2026-05-03T22:01:30Z, ~6h27m uptime at refresh, ~$19.29 spent
- ETA completion ~2026-05-04T06:25Z (~2h from refresh)
- DO NOT preempt (Path B HIGH completion-quality choice)

## raw#10 honest C3 — 3 caveats

**C1 — watchdog respawn race**: ~44s overlap between v2 spawn (04:26:16Z) and old SIGTERM (04:27:00Z). Both polled, both saw MISSING; risk realized = 0. If trigger had fired in window, dispatch step-1 (ssh run_all) is overwrite-safe but step-2/3 could have raced.

**C2 — trigger condition drift**: HF probe currently returns 401 (not 404) — hexa code returns "MISSING:http_401" → no trigger. _check_hf_repo only validates http_code==200, not body. Acceptable since training pushes step-25000 only on completion.

**C3 — cross-axis depends on r=16/r=64 baselines**: Step 4 (cross-axis) requires `state/p9_a_prime_main_eval_2026_05_03_verdict.json`. Path A r=16/r=64 still in progress (markers last 13:24Z UTC = ~07:24Z local). If D completes first, cross-axis SKIPS (D verdict still emitted standalone); operator manually re-fires `tool/p9_a_d_cross_axis_verdict.hexa` once Path A baselines land.

## Constraints

- raw#9 STRICT: Mac side hexa-only (canonical hexa unchanged); shell wrapper = OS-level supervisor
- raw#15: ubu1 paths use `/home/aiden/anima/state/...`
- $0: no GPU spend, no eval triggered (signals all MISSING)

## Next Actions

- v2 polls every 5min until 2026-05-05T04:26Z; auto-fires 4-step chain on first VALID signal
- If H100 ETA slips past 24h budget, manual respawn required
- If cross-axis SKIPS, run `hexa run tool/p9_a_d_cross_axis_verdict.hexa` after Path A baselines land
