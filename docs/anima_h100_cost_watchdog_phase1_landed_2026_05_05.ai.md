---
title: H100 cost watchdog Phase 1 — landed (tooling emission + selftest PASS)
cycle: 2026-05-05
ts: 2026-05-05T_h100_cost_watchdog_phase1_landed
bg_lane: BG-COST-WATCHDOG-PHASE1-IMPL
substrate: mac ($0, hexa codegen + bash daemon, no exec)
status: PHASE1_LANDED
type: tooling_emission_handoff
predecessor:
  - docs/anima_h100_cost_discipline_operationalization_spec_2026_05_05.md (full spec — Phase 1 scope §3.1+§3.2)
related:
  - state/h100_cost_watchdog_phase1_2026_05_05/legacy_tooling_audit.md (KEEP/ADD decisions)
  - tool/h100_cost_watchdog.hexa (NEW)
  - tool/h100_idle_auto_killer.hexa (NEW)
  - tool/h100_alert_emit.bash (NEW)
  - tool/h100_register.bash (NEW)
raw_invariants:
  - raw#9 (hexa-only loader; bash carve-out for alert-script + register wrapper)
  - raw#10 (≥6 honest C3 per script in selftest banners + below)
  - raw#15 (additive — no legacy retire/absorb this cycle)
---

# H100 cost watchdog Phase 1 — landed (2026-05-05)

## Summary (5 bullets)

- **4 net-new files written** under `tool/`: `h100_cost_watchdog.hexa`
  (~430 LoC, polls registered pods → ledger row + alert ladder),
  `h100_idle_auto_killer.hexa` (~210 LoC, action ladder consumer:
  alert → auto-pause → user-confirm → auto-delete), `h100_alert_emit.bash`
  (~60 LoC, pure-bash alert sink — avoids recursive Anthropic 429),
  `h100_register.bash` (~35 LoC, orchestrator boot-time wrapper).
  All four registered with executable bits where applicable; state
  scaffolding `state/h100_watchdog/{pods,heartbeats,alerts,closed,acks}/`
  created.

- **Legacy tooling audit decision = KEEP-ALL (additive, raw#15)**:
  `tool/h100_idle_guard.bash` (launchd reclaim wrapper, KEEP),
  `tool/h100_auto_kill.hexa` (inactivity binary STOP, KEEP),
  `tool/h100_cost_tracker.hexa` (offline per-round rollup, KEEP). All
  three occupy distinct lanes from the new live cost watchdog (which
  fills the cost-overrun + heartbeat-staleness + BG-dead-pod-alive
  gap). Full audit at
  `state/h100_cost_watchdog_phase1_2026_05_05/legacy_tooling_audit.md`.

- **Selftest PASS for both new hexa scripts**: `h100_cost_watchdog
  --selftest` = 5/5 PASS (register / no-heartbeat=-1 / fresh-heartbeat /
  ledger-emit / deregister archive); `h100_idle_auto_killer --selftest`
  = 4/4 PASS (no-ack ladder halt at tier3 / ack-present ladder reaches
  tier4 / `_has_user_ack` false-path / true-path). Both emit ≥6 honest
  C3 lines after the test summary. Smoke-tested
  `h100_alert_emit.bash` end-to-end — stderr emit + ledger JSONL
  append both work; `--status` mode on watchdog also confirmed
  (registry_dir reachable, 0 pods).

- **Phase 2 readiness = GO**: orchestrator patch surface is well-scoped.
  Boot hook = call `bash tool/h100_register.bash <POD> <BG_LANE>
  <TARGET_USD>` after pod allocation. Heartbeat hook = touch
  `state/h100_watchdog/heartbeats/<bg_id>.txt` every 5 min in the
  existing orchestrator main loop (clm_v4 line 41 pattern reusable).
  Trap pre-stop hook = call `hexa run tool/h100_cost_watchdog.hexa
  --deregister <POD>` after `runpodctl pod delete` 404 verify. Verdict
  schema additions = `pod_kill_verified_404 + watchdog_deregistered +
  actual_usd + target_usd + cost_overrun_ratio`. No new file writes
  required for Phase 2 — just additive PATCH_NOTES.md per raw#15.

- **Honest C3 (≥5)**: (1) watchdog assumes `runpodctl` is on PATH +
  authenticated; if either is missing, `_pod_state` returns UNKNOWN
  and the daemon iter still emits ledger rows but cannot deregister
  on 404 — orchestrator trap remains the authoritative kill path.
  (2) ledger format `anima/h100_watchdog/pods/1` is a v1 schema; if
  Phase 4 smoke surfaces missing fields (e.g., per-pod cumulative
  heartbeat-age stats), the schema will bump to v2 and old rows must
  be migrated. (3) pure-bash alert-script avoids the recursive 429
  cascade for the **emit** path, but downstream **push notification**
  wiring (TODO marker in `h100_alert_emit.bash`) is deferred to Phase
  2+; until that lands, alerts are ledger-only and require manual
  review (operator must `tail` the ledger JSONL). (4) selftest is
  shape-only — synthetic pod registration + heartbeat freshness +
  ledger emit; it does NOT exercise the live `runpodctl pod get`
  branch nor the alert-script invocation under load. Phase 4 smoke
  ($1-3 budget) is required to functionally validate. (5) the
  recursive Anthropic-429 risk is **avoided** for the alert-emit
  hot path, but **not eliminated** for the watchdog daemon itself
  (the hexa runtime is not under 429 isolation; if hexa-lang
  startup paths trip a future provider rate limit, the watchdog
  daemon dies and only launchd respawn restores it). (6) `--daemon`
  mode is implemented as a **single-iteration** function; production
  deployment relies on a launchd plist (or equivalent) to repeat
  every `--poll-interval-sec` seconds. The poll-loop wrapper is
  intentionally external so the watchdog process is restartable
  without losing ledger continuity. (7) the stale-heartbeat
  threshold (300s) and unack autopause window (1800s) are
  hard-coded constants in the two hexa files; future cycle should
  hoist to a config JSON if Phase 4 smoke surfaces tuning needs.

## Files written

| Path                                                                                  | LoC | Mode  | Role                                          |
|---------------------------------------------------------------------------------------|-----|-------|-----------------------------------------------|
| `tool/h100_cost_watchdog.hexa`                                                        | 430 | n/a   | poll-loop daemon: register/deregister/status/selftest/daemon |
| `tool/h100_idle_auto_killer.hexa`                                                     | 210 | n/a   | action ladder consumer (alert→pause→confirm→delete) |
| `tool/h100_alert_emit.bash`                                                           | 60  | 0755  | pure-bash alert sink (stderr + JSONL append)  |
| `tool/h100_register.bash`                                                             | 35  | 0755  | orchestrator boot-time `--register` wrapper   |
| `state/h100_cost_watchdog_phase1_2026_05_05/legacy_tooling_audit.md`                  | 110 | n/a   | KEEP/ADD decisions for 3 legacy + 4 new files |
| `state/h100_watchdog/{pods,heartbeats,alerts,closed,acks}/` (dirs)                    | n/a | 0755  | runtime state scaffolding                     |

## Selftest evidence

```
$ hexa run tool/h100_cost_watchdog.hexa --selftest
── h100_cost_watchdog selftest 2026-05-05T04:19:50Z ──
  S1 PASS (register wrote /tmp/.../SELFTEST_POD_1.json)
  S2 PASS (no heartbeat → age=-1 sentinel)
  S3 PASS (fresh heartbeat age=0s)
  S4 PASS (ledger row appended)
  S5 PASS (deregister archived)
h100_cost_watchdog selftest: 5/5 PASS, 0 FAIL

$ hexa run tool/h100_idle_auto_killer.hexa --selftest
── h100_idle_auto_killer selftest 2026-05-05T04:20:03Z ──
  S1 PASS (no-ack ladder halts at tier3, dry rc=0)
  S2 PASS (ack-present ladder reaches tier4 dry rc=0)
  S3 PASS (no ack file → false)
  S4 PASS (ack file present → true)
h100_idle_auto_killer selftest: 4/4 PASS, 0 FAIL
```

## Next-cycle handoff

Phase 2 (orchestrator hexa boot/heartbeat/trap/verdict patches) can land
as soon as the next-cycle BG opens. Surface is the four files
documented above; the orchestrator side just needs to call into them at
the right lifecycle points. No commit was made this cycle (per
spec / BG-COST-WATCHDOG-PHASE1-IMPL CRITICAL bullet); next cycle should
batch Phase 1 + Phase 2 + Phase 3 (memory update) into a single additive
commit.
